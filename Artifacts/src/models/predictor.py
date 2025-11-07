"""
Model prediction and inference pipeline.
Handles loading trained models and making predictions.
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class FraudPredictor:
    """Load trained models and make fraud predictions."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """
        Load trained XGBoost model.
        
        Args:
            model_path: Path to saved model file
        """
        logger.info(f"Loading model from {model_path}...")
        
        if model_path.endswith('.pkl') or model_path.endswith('.joblib'):
            self.model = joblib.load(model_path)
        elif model_path.endswith('.json'):
            self.model = xgb.XGBClassifier()
            self.model.load_model(model_path)
        else:
            raise ValueError(f"Unknown model format: {model_path}")
        
        self.model_path = model_path
        logger.info("Model loaded successfully!")
    
    def predict(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        threshold: float = 0.5,
        return_proba: bool = False
    ) -> Union[np.ndarray, tuple]:
        """
        Predict fraud probability and class.
        
        Args:
            X: Feature matrix
            threshold: Classification threshold
            return_proba: Whether to return probabilities
            
        Returns:
            Predictions (and probabilities if return_proba=True)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Handle missing values
        if isinstance(X, pd.DataFrame):
            X = X.fillna(0)
            X = X.replace([np.inf, -np.inf], 0)
        
        # Predict probabilities
        y_proba = self.model.predict_proba(X)[:, 1]
        
        # Predict classes
        y_pred = (y_proba >= threshold).astype(int)
        
        if return_proba:
            return y_pred, y_proba
        else:
            return y_pred
    
    def predict_single(
        self,
        transaction: Dict,
        threshold: float = 0.5
    ) -> Dict:
        """
        Predict fraud for a single transaction.
        
        Args:
            transaction: Dictionary of transaction features
            threshold: Classification threshold
            
        Returns:
            Dictionary with prediction and probability
        """
        # Convert to DataFrame
        X = pd.DataFrame([transaction])
        
        # Predict
        y_pred, y_proba = self.predict(X, threshold=threshold, return_proba=True)
        
        return {
            'is_fraud': int(y_pred[0]),
            'fraud_probability': float(y_proba[0]),
            'threshold': threshold
        }
    
    def predict_batch(
        self,
        transactions: List[Dict],
        threshold: float = 0.5
    ) -> List[Dict]:
        """
        Predict fraud for multiple transactions.
        
        Args:
            transactions: List of transaction dictionaries
            threshold: Classification threshold
            
        Returns:
            List of prediction dictionaries
        """
        # Convert to DataFrame
        X = pd.DataFrame(transactions)
        
        # Predict
        y_pred, y_proba = self.predict(X, threshold=threshold, return_proba=True)
        
        # Format results
        results = [
            {
                'is_fraud': int(pred),
                'fraud_probability': float(proba),
                'threshold': threshold
            }
            for pred, proba in zip(y_pred, y_proba)
        ]
        
        return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    # predictor = FraudPredictor("models/xgboost_fraud_latest.pkl")
    
    # Single prediction example
    # transaction = {
    #     'amount': 1000.0,
    #     'hour': 3,
    #     'day_of_week': 1,
    #     # ... other features
    # }
    
    # result = predictor.predict_single(transaction)
    # print(f"Prediction: {result}")

