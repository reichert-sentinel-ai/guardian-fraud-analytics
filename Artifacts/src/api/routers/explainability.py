"""
Explainability endpoint router
SHAP explanation API for fraud detection predictions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import numpy as np

router = APIRouter(prefix="/api/explainability", tags=["explainability"])


class TransactionExplanation(BaseModel):
    transaction_id: str
    predicted_fraud_probability: float
    prediction_label: str
    shap_values: Dict[str, float]  # feature -> SHAP value
    base_value: float
    feature_values: Dict[str, any]


class ExplanationRequest(BaseModel):
    transaction_id: str


@router.post("/explain")
async def explain_prediction(request: ExplanationRequest) -> TransactionExplanation:
    """
    Generate SHAP explanation for a transaction prediction
    
    Demonstrates:
    - SHAP (SHapley Additive exPlanations) understanding
    - Model interpretability
    - Regulatory compliance (explainable AI)
    """
    
    # For demo: generate synthetic explanation
    # In production: would call actual SHAP explainer
    
    transaction_id = request.transaction_id
    
    # Simulate different transaction scenarios
    scenarios = {
        "TXN_001": {  # High-risk fraud
            "probability": 0.94,
            "shap_values": {
                "transaction_velocity_24h": 0.28,
                "amount_deviation_from_avg": 0.19,
                "merchant_risk_score": 0.15,
                "time_since_last_transaction": -0.08,
                "cross_border_flag": 0.12,
                "device_fingerprint_mismatch": 0.11,
                "account_age_days": -0.06,
                "transaction_hour": 0.04,
                "network_centrality": 0.09,
                "amount": 0.03,
            },
            "feature_values": {
                "transaction_velocity_24h": 47,
                "amount_deviation_from_avg": 8.3,
                "merchant_risk_score": 0.82,
                "time_since_last_transaction": 0.5,
                "cross_border_flag": 1,
                "device_fingerprint_mismatch": 1,
                "account_age_days": 12,
                "transaction_hour": 3,
                "network_centrality": 0.73,
                "amount": 1247.50,
            }
        },
        "TXN_002": {  # Legitimate but flagged
            "probability": 0.52,
            "shap_values": {
                "transaction_velocity_24h": 0.08,
                "amount_deviation_from_avg": 0.12,
                "merchant_risk_score": -0.04,
                "time_since_last_transaction": 0.03,
                "cross_border_flag": 0.09,
                "device_fingerprint_mismatch": -0.02,
                "account_age_days": -0.08,
                "transaction_hour": 0.02,
                "network_centrality": -0.03,
                "amount": 0.06,
            },
            "feature_values": {
                "transaction_velocity_24h": 8,
                "amount_deviation_from_avg": 2.1,
                "merchant_risk_score": 0.35,
                "time_since_last_transaction": 12.0,
                "cross_border_flag": 1,
                "device_fingerprint_mismatch": 0,
                "account_age_days": 890,
                "transaction_hour": 14,
                "network_centrality": 0.12,
                "amount": 450.00,
            }
        },
        "TXN_003": {  # Clearly legitimate
            "probability": 0.02,
            "shap_values": {
                "transaction_velocity_24h": -0.02,
                "amount_deviation_from_avg": -0.01,
                "merchant_risk_score": -0.03,
                "time_since_last_transaction": -0.01,
                "cross_border_flag": 0.0,
                "device_fingerprint_mismatch": 0.0,
                "account_age_days": -0.04,
                "transaction_hour": -0.01,
                "network_centrality": -0.02,
                "amount": 0.01,
            },
            "feature_values": {
                "transaction_velocity_24h": 2,
                "amount_deviation_from_avg": 0.3,
                "merchant_risk_score": 0.15,
                "time_since_last_transaction": 72.0,
                "cross_border_flag": 0,
                "device_fingerprint_mismatch": 0,
                "account_age_days": 1245,
                "transaction_hour": 10,
                "network_centrality": 0.05,
                "amount": 89.99,
            }
        }
    }
    
    if transaction_id not in scenarios:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    scenario = scenarios[transaction_id]
    probability = scenario["probability"]
    
    return TransactionExplanation(
        transaction_id=transaction_id,
        predicted_fraud_probability=probability,
        prediction_label="FRAUD" if probability > 0.5 else "LEGITIMATE",
        shap_values=scenario["shap_values"],
        base_value=0.015,  # Base fraud rate
        feature_values=scenario["feature_values"]
    )


@router.get("/feature-glossary")
async def get_feature_glossary() -> Dict[str, Dict]:
    """Return human-readable descriptions of features"""
    return {
        "transaction_velocity_24h": {
            "name": "24-Hour Transaction Velocity",
            "description": "Number of transactions in the last 24 hours",
            "interpretation": "Higher values indicate rapid transaction activity, common in fraud",
            "unit": "count"
        },
        "amount_deviation_from_avg": {
            "name": "Amount Deviation",
            "description": "How much this transaction deviates from user's average",
            "interpretation": "Larger deviations suggest unusual activity",
            "unit": "standard deviations"
        },
        "merchant_risk_score": {
            "name": "Merchant Risk Score",
            "description": "Historical fraud rate at this merchant",
            "interpretation": "0-1 scale; higher means more fraud reported",
            "unit": "probability"
        },
        "time_since_last_transaction": {
            "name": "Time Since Last Transaction",
            "description": "Hours since previous transaction",
            "interpretation": "Very short times suggest automated/scripted activity",
            "unit": "hours"
        },
        "cross_border_flag": {
            "name": "Cross-Border Transaction",
            "description": "Transaction crosses international borders",
            "interpretation": "1 = cross-border, 0 = domestic",
            "unit": "binary"
        },
        "device_fingerprint_mismatch": {
            "name": "Device Mismatch",
            "description": "Transaction from new/unrecognized device",
            "interpretation": "1 = new device, 0 = recognized device",
            "unit": "binary"
        },
        "account_age_days": {
            "name": "Account Age",
            "description": "Days since account creation",
            "interpretation": "Very new accounts are higher risk",
            "unit": "days"
        },
        "transaction_hour": {
            "name": "Transaction Hour",
            "description": "Hour of day (0-23) when transaction occurred",
            "interpretation": "Late night/early morning slightly riskier",
            "unit": "hour"
        },
        "network_centrality": {
            "name": "Network Centrality",
            "description": "Position in transaction network graph",
            "interpretation": "High centrality suggests hub in fraud ring",
            "unit": "score 0-1"
        },
        "amount": {
            "name": "Transaction Amount",
            "description": "Dollar value of transaction",
            "interpretation": "Extremely high/low amounts can be suspicious",
            "unit": "USD"
        }
    }

