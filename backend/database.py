"""
Database models and connection
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ownai.db")

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# ===========================
# Database Models
# ===========================

class User(Base):
    """User account"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    company = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Dataset(Base):
    """Training dataset"""
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    dataset_id = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String)  # S3 path or local path
    size_bytes = Column(Integer)
    num_examples = Column(Integer)
    status = Column(String, default="uploaded")  # uploaded, validated, error
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrainingJob(Base):
    """Fine-tuning job"""
    __tablename__ = "training_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    job_id = Column(String, unique=True, index=True, nullable=False)
    dataset_id = Column(String, nullable=False)

    # Model config
    base_model = Column(String, nullable=False)
    model_name = Column(String)

    # Hyperparameters
    learning_rate = Column(Float)
    num_epochs = Column(Integer)
    batch_size = Column(Integer)
    max_seq_length = Column(Integer)
    config_json = Column(JSON)  # Full config

    # Status
    status = Column(String, default="queued")  # queued, running, completed, failed
    progress_percent = Column(Float, default=0.0)

    # Results
    final_loss = Column(Float)
    training_time_seconds = Column(Integer)
    model_path = Column(String)  # Where trained model is stored

    # Timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Error handling
    error_message = Column(Text)


class Deployment(Base):
    """Model deployment"""
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    deployment_id = Column(String, unique=True, index=True, nullable=False)
    job_id = Column(String, nullable=False)

    # Deployment config
    deployment_type = Column(String)  # cloud, on-premise
    instance_type = Column(String)

    # API details
    api_endpoint = Column(String)
    api_key = Column(String)

    # Status
    status = Column(String, default="deploying")  # deploying, running, stopped, error

    # Usage stats
    total_requests = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    stopped_at = Column(DateTime)


class APIKey(Base):
    """API keys for users"""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime)


# ===========================
# Database utilities
# ===========================

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")


if __name__ == "__main__":
    # Initialize database
    init_db()
