"""
PostgreSQL database configuration and ORM models
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import logging

from .config import settings

logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ===== Database Models =====

class TransactionLog(Base):
    """Transaction logging table for audit trail"""
    
    __tablename__ = "transaction_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    
    # Transaction details
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=True)
    step = Column(Integer, nullable=True)
    
    # Prediction results
    is_fraud = Column(Boolean, nullable=False)
    fraud_probability = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    
    # Feature data (stored as JSON for flexibility)
    features = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    prediction_timestamp = Column(DateTime, nullable=False)
    
    # Metadata
    processing_time_ms = Column(Float, nullable=True)
    model_version = Column(String, nullable=True)
    
    class Config:
        orm_mode = True


class PredictionCache(Base):
    """Cache for predictions (optional optimization)"""
    
    __tablename__ = "prediction_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True, nullable=False)
    
    # Prediction results
    is_fraud = Column(Boolean, nullable=False)
    fraud_probability = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    class Config:
        orm_mode = True


# ===== Database Functions =====

def get_db() -> Session:
    """
    Dependency for getting database session.
    Yields a database session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def check_db_connection() -> bool:
    """Check if database connection is healthy"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

