"""
Celery task definitions for async job execution
"""

from celery import Celery
from celery.utils.log import get_task_logger
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import TrainingJob, Deployment
from training_runner import run_training_job, deploy_model

# Logger
logger = get_task_logger(__name__)

# Celery app
celery_app = Celery(
    'ownai',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1
)

# Database session for tasks
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ownai.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session for tasks"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, let task handle it


@celery_app.task(bind=True, name='ownai.train_model')
def train_model_task(self, job_id: str, user_id: int):
    """
    Execute model training job asynchronously.

    Args:
        job_id: Training job ID
        user_id: User ID who owns the job
    """
    db = get_db()

    try:
        # Get job from database
        job = db.query(TrainingJob).filter(TrainingJob.job_id == job_id).first()

        if not job:
            logger.error(f"Job {job_id} not found")
            return {'status': 'error', 'error': 'Job not found'}

        # Update status to running
        job.status = 'running'
        job.started_at = datetime.utcnow()
        job.progress_percent = 0.0
        db.commit()

        logger.info(f"Starting training job {job_id}")

        # Progress callback
        def update_progress(percent, message=""):
            job.progress_percent = percent
            db.commit()
            logger.info(f"Job {job_id} progress: {percent}%")
            self.update_state(
                state='PROGRESS',
                meta={'percent': percent, 'message': message}
            )

        # Run actual training
        result = run_training_job(
            job_id=job_id,
            dataset_path=job.dataset_id,
            config={
                'base_model': job.base_model,
                'learning_rate': job.learning_rate,
                'num_epochs': job.num_epochs,
                'batch_size': job.batch_size,
                'max_seq_length': job.max_seq_length
            },
            progress_callback=update_progress,
            db=db
        )

        # Update job with results
        if result['success']:
            job.status = 'completed'
            job.progress_percent = 100.0
            job.model_path = result.get('model_path')
            job.final_loss = result.get('final_loss')
            job.training_time_seconds = result.get('training_time_seconds')
            job.completed_at = datetime.utcnow()
            logger.info(f"Job {job_id} completed successfully")
        else:
            job.status = 'failed'
            job.error_message = result.get('error', 'Unknown error')
            logger.error(f"Job {job_id} failed: {job.error_message}")

        db.commit()

        return {
            'status': job.status,
            'job_id': job_id,
            'model_path': job.model_path,
            'error': job.error_message
        }

    except Exception as e:
        logger.error(f"Job {job_id} crashed: {str(e)}")

        # Mark job as failed
        job = db.query(TrainingJob).filter(TrainingJob.job_id == job_id).first()
        if job:
            job.status = 'failed'
            job.error_message = str(e)
            db.commit()

        return {'status': 'error', 'error': str(e)}

    finally:
        db.close()


@celery_app.task(bind=True, name='ownai.deploy_model')
def deploy_model_task(self, deployment_id: str, job_id: str, user_id: int):
    """
    Deploy trained model for inference.

    Args:
        deployment_id: Deployment ID
        job_id: Training job ID to deploy
        user_id: User ID who owns the deployment
    """
    db = get_db()

    try:
        # Get deployment from database
        deployment = db.query(Deployment).filter(
            Deployment.deployment_id == deployment_id
        ).first()

        if not deployment:
            logger.error(f"Deployment {deployment_id} not found")
            return {'status': 'error', 'error': 'Deployment not found'}

        # Get training job
        job = db.query(TrainingJob).filter(TrainingJob.job_id == job_id).first()

        if not job or job.status != 'completed':
            logger.error(f"Job {job_id} not ready for deployment")
            deployment.status = 'failed'
            db.commit()
            return {'status': 'error', 'error': 'Job not completed'}

        # Update status
        deployment.status = 'deploying'
        db.commit()

        logger.info(f"Deploying model from job {job_id}")

        # Actually deploy model
        result = deploy_model(
            model_path=job.model_path,
            deployment_type=deployment.deployment_type,
            deployment_id=deployment_id,
            db=db
        )

        # Update deployment
        if result['success']:
            deployment.status = 'running'
            deployment.api_endpoint = result.get('api_endpoint')
            logger.info(f"Deployment {deployment_id} running at {deployment.api_endpoint}")
        else:
            deployment.status = 'failed'
            logger.error(f"Deployment {deployment_id} failed: {result.get('error')}")

        db.commit()

        return {
            'status': deployment.status,
            'deployment_id': deployment_id,
            'api_endpoint': deployment.api_endpoint
        }

    except Exception as e:
        logger.error(f"Deployment {deployment_id} crashed: {str(e)}")

        deployment = db.query(Deployment).filter(
            Deployment.deployment_id == deployment_id
        ).first()
        if deployment:
            deployment.status = 'failed'
            db.commit()

        return {'status': 'error', 'error': str(e)}

    finally:
        db.close()


if __name__ == '__main__':
    # Run worker
    celery_app.start()
