"""
OWN-AI Backend API - Production Version
Integrated with database, auth, and real file storage
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import shutil
import uuid

# Import our modules
from database import get_db, init_db, Dataset, TrainingJob, Deployment, User
from auth import (
    get_current_user,
    authenticate_user,
    create_user,
    create_access_token,
    get_password_hash
)

# Initialize FastAPI app
app = FastAPI(
    title="OWN-AI API",
    description="Enterprise AI Fine-Tuning as a Service",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File upload directory
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ===========================
# Pydantic Models (Request/Response)
# ===========================

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None
    company: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class DatasetResponse(BaseModel):
    dataset_id: str
    filename: str
    size_bytes: int
    num_examples: Optional[int]
    status: str
    created_at: datetime


class JobCreate(BaseModel):
    dataset_id: str
    base_model: str = "meta-llama/Llama-3.1-8B"
    model_name: Optional[str] = None
    learning_rate: float = 2e-5
    num_epochs: int = 3
    batch_size: int = 4
    max_seq_length: int = 2048


class JobResponse(BaseModel):
    job_id: str
    dataset_id: str
    base_model: str
    status: str
    progress_percent: float
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]


class DeploymentCreate(BaseModel):
    job_id: str
    deployment_type: str = "cloud"
    instance_type: str = "gpu-1x-a100"


class DeploymentResponse(BaseModel):
    deployment_id: str
    job_id: str
    api_endpoint: str
    api_key: str
    status: str


# ===========================
# Startup/Shutdown Events
# ===========================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")


# ===========================
# Authentication Endpoints
# ===========================

@app.post("/api/v1/auth/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register new user"""
    try:
        user = create_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            company=user_data.company
        )

        # Create access token
        access_token = create_access_token(data={"sub": user.id})

        return Token(
            access_token=access_token,
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "company": user.company
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/auth/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return Token(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "company": user.company
        }
    )


@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "company": current_user.company,
        "created_at": current_user.created_at
    }


# ===========================
# Dataset Endpoints
# ===========================

@app.post("/api/v1/datasets/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload training dataset"""
    try:
        # Validate file type
        allowed_extensions = [".jsonl", ".txt", ".csv"]
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )

        # Generate dataset ID
        dataset_id = f"ds_{uuid.uuid4().hex[:16]}"

        # Save file
        file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}_{file.filename}")

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        file_size = len(content)

        # Count examples (simplified)
        num_examples = None
        if file_ext == ".jsonl":
            num_examples = content.decode().count('\n')

        # Create database record
        dataset = Dataset(
            user_id=current_user.id,
            dataset_id=dataset_id,
            filename=file.filename,
            file_path=file_path,
            size_bytes=file_size,
            num_examples=num_examples,
            status="uploaded"
        )

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return DatasetResponse(
            dataset_id=dataset.dataset_id,
            filename=dataset.filename,
            size_bytes=dataset.size_bytes,
            num_examples=dataset.num_examples,
            status=dataset.status,
            created_at=dataset.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/datasets", response_model=List[DatasetResponse])
async def list_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's datasets"""
    datasets = db.query(Dataset).filter(Dataset.user_id == current_user.id).all()

    return [
        DatasetResponse(
            dataset_id=ds.dataset_id,
            filename=ds.filename,
            size_bytes=ds.size_bytes,
            num_examples=ds.num_examples,
            status=ds.status,
            created_at=ds.created_at
        )
        for ds in datasets
    ]


# ===========================
# Training Job Endpoints
# ===========================

@app.post("/api/v1/jobs/create", response_model=JobResponse)
async def create_training_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create fine-tuning job"""
    # Verify dataset exists and belongs to user
    dataset = db.query(Dataset).filter(
        Dataset.dataset_id == job_data.dataset_id,
        Dataset.user_id == current_user.id
    ).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Generate job ID
    job_id = f"job_{uuid.uuid4().hex[:16]}"

    # Create job
    job = TrainingJob(
        user_id=current_user.id,
        job_id=job_id,
        dataset_id=job_data.dataset_id,
        base_model=job_data.base_model,
        model_name=job_data.model_name or f"{current_user.company}_{job_data.base_model.split('/')[-1]}",
        learning_rate=job_data.learning_rate,
        num_epochs=job_data.num_epochs,
        batch_size=job_data.batch_size,
        max_seq_length=job_data.max_seq_length,
        status="queued",
        progress_percent=0.0,
        config_json=job_data.dict()
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # TODO: Actually queue job for training (Celery task)
    # For now, just return queued status

    return JobResponse(
        job_id=job.job_id,
        dataset_id=job.dataset_id,
        base_model=job.base_model,
        status=job.status,
        progress_percent=job.progress_percent,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message
    )


@app.get("/api/v1/jobs/{job_id}", response_model=JobResponse)
async def get_job_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get training job status"""
    job = db.query(TrainingJob).filter(
        TrainingJob.job_id == job_id,
        TrainingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        job_id=job.job_id,
        dataset_id=job.dataset_id,
        base_model=job.base_model,
        status=job.status,
        progress_percent=job.progress_percent,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message
    )


@app.get("/api/v1/jobs", response_model=List[JobResponse])
async def list_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's training jobs"""
    jobs = db.query(TrainingJob).filter(
        TrainingJob.user_id == current_user.id
    ).order_by(TrainingJob.created_at.desc()).all()

    return [
        JobResponse(
            job_id=job.job_id,
            dataset_id=job.dataset_id,
            base_model=job.base_model,
            status=job.status,
            progress_percent=job.progress_percent,
            started_at=job.started_at,
            completed_at=job.completed_at,
            error_message=job.error_message
        )
        for job in jobs
    ]


# ===========================
# Health Check
# ===========================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.2.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# ===========================
# Run Server
# ===========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main_v2:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
