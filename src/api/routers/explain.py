"""
SHAP explanation endpoint router
Model explainability for fraud predictions
"""

import time
import logging
from fastapi import APIRouter, HTTPException

from ..schemas import ExplainRequest, ExplainResponse, PredictionResponse, FeatureExplanation

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/explain", response_model=ExplainResponse)
async def explain_prediction(request: ExplainRequest):
    """
    Generate SHAP explanation for a fraud prediction.
    
    **NOTE**: This endpoint is a stub until Chat 2 completes.
    SHAP explainer will be integrated after model training is complete.
    
    Args:
        request: Explanation request with transaction data
        
    Returns:
        SHAP explanation with feature contributions
    """
    start_time = time.time()
    
    try:
        # TODO: Load model and SHAP explainer after Chat 2 completes
        # For now, return placeholder explanation
        logger.warning("Model not loaded. Returning placeholder SHAP explanation.")
        
        # Placeholder prediction (will be replaced after Chat 2)
        prediction = PredictionResponse(
            is_fraud=0,
            fraud_probability=0.25,  # Placeholder
            threshold=0.5
        )
        
        # Placeholder explanations (will be replaced after Chat 2)
        # These will come from actual SHAP values
        explanations = [
            FeatureExplanation(
                feature_name="amount",
                shap_value=0.05,
                feature_value=request.transaction.amount
            ),
            FeatureExplanation(
                feature_name="hour",
                shap_value=0.02,
                feature_value=request.transaction.hour
            ),
            FeatureExplanation(
                feature_name="type",
                shap_value=-0.01,
                feature_value=request.transaction.type
            )
        ]
        
        # Return top N features
        top_explanations = explanations[:request.top_features]
        
        computation_time_ms = (time.time() - start_time) * 1000
        
        return ExplainResponse(
            prediction=prediction,
            explanations=top_explanations,
            base_value=0.08,  # Placeholder base value
            computation_time_ms=computation_time_ms
        )
        
    except Exception as e:
        logger.error(f"Explanation error: {e}")
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")

