"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


# ===== Request Schemas =====

class TransactionRequest(BaseModel):
    """Single transaction prediction request"""
    
    amount: float = Field(..., description="Transaction amount", gt=0)
    step: Optional[int] = Field(None, description="Time step")
    type: Optional[str] = Field(None, description="Transaction type")
    oldbalanceOrg: Optional[float] = Field(None, description="Original balance before transaction")
    newbalanceOrig: Optional[float] = Field(None, description="Original balance after transaction")
    oldbalanceDest: Optional[float] = Field(None, description="Destination balance before transaction")
    newbalanceDest: Optional[float] = Field(None, description="Destination balance after transaction")
    
    # Additional feature fields (will be expanded based on Chat 1 features)
    hour: Optional[int] = Field(None, ge=0, le=23, description="Hour of day")
    day_of_week: Optional[int] = Field(None, ge=0, le=6, description="Day of week (0=Monday)")
    month: Optional[int] = Field(None, ge=1, le=12, description="Month")
    
    # Allow additional features as dict for flexibility
    features: Optional[Dict[str, Any]] = Field(None, description="Additional transaction features")
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 1000.0,
                "step": 1,
                "type": "TRANSFER",
                "oldbalanceOrg": 5000.0,
                "newbalanceOrig": 4000.0,
                "oldbalanceDest": 10000.0,
                "newbalanceDest": 11000.0,
                "hour": 15,
                "day_of_week": 3,
                "month": 12
            }
        }


class BatchTransactionRequest(BaseModel):
    """Batch transaction prediction request"""
    
    transactions: List[TransactionRequest] = Field(..., min_items=1, max_items=1000)
    threshold: Optional[float] = Field(0.5, ge=0.0, le=1.0, description="Fraud classification threshold")
    
    class Config:
        schema_extra = {
            "example": {
                "transactions": [
                    {
                        "amount": 1000.0,
                        "type": "TRANSFER",
                        "hour": 15
                    }
                ],
                "threshold": 0.5
            }
        }


class ExplainRequest(BaseModel):
    """SHAP explanation request"""
    
    transaction: TransactionRequest
    top_features: Optional[int] = Field(10, ge=1, le=50, description="Number of top features to return")
    
    class Config:
        schema_extra = {
            "example": {
                "transaction": {
                    "amount": 1000.0,
                    "type": "TRANSFER",
                    "hour": 15
                },
                "top_features": 10
            }
        }


# ===== Response Schemas =====

class PredictionResponse(BaseModel):
    """Single transaction prediction response"""
    
    is_fraud: int = Field(..., description="Fraud prediction (0=legitimate, 1=fraud)")
    fraud_probability: float = Field(..., ge=0.0, le=1.0, description="Fraud probability score")
    threshold: float = Field(..., ge=0.0, le=1.0, description="Classification threshold used")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Prediction timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    
    class Config:
        schema_extra = {
            "example": {
                "is_fraud": 0,
                "fraud_probability": 0.23,
                "threshold": 0.5,
                "timestamp": "2024-12-20T10:30:00Z",
                "request_id": "req_123456"
            }
        }


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    total_transactions: int = Field(..., description="Total number of transactions")
    fraud_count: int = Field(..., description="Number of transactions flagged as fraud")
    threshold: float = Field(..., ge=0.0, le=1.0, description="Classification threshold used")
    processing_time_ms: Optional[float] = Field(None, description="Total processing time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Batch prediction timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "predictions": [
                    {
                        "is_fraud": 0,
                        "fraud_probability": 0.23,
                        "threshold": 0.5
                    }
                ],
                "total_transactions": 1,
                "fraud_count": 0,
                "threshold": 0.5,
                "processing_time_ms": 45.2
            }
        }


class FeatureExplanation(BaseModel):
    """Individual feature contribution to prediction"""
    
    feature_name: str = Field(..., description="Feature name")
    shap_value: float = Field(..., description="SHAP value (contribution to prediction)")
    feature_value: Optional[Any] = Field(None, description="Actual feature value")
    
    class Config:
        schema_extra = {
            "example": {
                "feature_name": "amount",
                "shap_value": 0.15,
                "feature_value": 1000.0
            }
        }


class ExplainResponse(BaseModel):
    """SHAP explanation response"""
    
    prediction: PredictionResponse = Field(..., description="Underlying prediction")
    explanations: List[FeatureExplanation] = Field(..., description="Top feature explanations")
    base_value: float = Field(..., description="Base prediction value (before feature contributions)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Explanation timestamp")
    computation_time_ms: Optional[float] = Field(None, description="SHAP computation time in milliseconds")
    
    class Config:
        schema_extra = {
            "example": {
                "prediction": {
                    "is_fraud": 0,
                    "fraud_probability": 0.23,
                    "threshold": 0.5
                },
                "explanations": [
                    {
                        "feature_name": "amount",
                        "shap_value": 0.15,
                        "feature_value": 1000.0
                    }
                ],
                "base_value": 0.08,
                "computation_time_ms": 150.3
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    database_connected: bool = Field(..., description="Whether database is connected")
    redis_connected: bool = Field(..., description="Whether Redis cache is connected")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-12-20T10:30:00Z",
                "version": "1.0.0",
                "model_loaded": True,
                "database_connected": True,
                "redis_connected": True
            }
        }

