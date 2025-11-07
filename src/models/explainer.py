"""
SHAP explainability integration for fraud detection model.
Generates feature importance explanations for predictions.
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import shap
import joblib
import xgboost as xgb
from typing import Dict, List, Optional, Union
import time

logger = logging.getLogger(__name__)


class FraudExplainer:
    """Generate SHAP explanations for fraud predictions."""
    
    def __init__(self, model_path: Optional[str] = None, model=None):
        self.model = model
        self.explainer = None
        self.shap_values = None
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """
        Load trained model for explanation.
        
        Args:
            model_path: Path to saved model
        """
        logger.info(f"Loading model from {model_path}...")
        
        if model_path.endswith('.pkl') or model_path.endswith('.joblib'):
            self.model = joblib.load(model_path)
        elif model_path.endswith('.json'):
            self.model = xgb.XGBClassifier()
            self.model.load_model(model_path)
        else:
            raise ValueError(f"Unknown model format: {model_path}")
        
        logger.info("Model loaded for explanation!")
    
    def create_explainer(
        self,
        X_train: pd.DataFrame,
        explainer_type: str = "tree",
        sample_size: int = 1000
    ):
        """
        Create SHAP explainer.
        
        Args:
            X_train: Training data for background
            explainer_type: Type of explainer ('tree' or 'exact')
            sample_size: Number of samples for TreeExplainer background
        """
        logger.info(f"Creating SHAP {explainer_type} explainer...")
        
        # Sample training data for efficiency
        if len(X_train) > sample_size:
            X_background = X_train.sample(n=sample_size, random_state=42)
            logger.info(f"Sampled {sample_size} rows for background")
        else:
            X_background = X_train
        
        # Handle missing values
        X_background = X_background.fillna(0)
        X_background = X_background.replace([np.inf, -np.inf], 0)
        
        start_time = time.time()
        
        if explainer_type == "tree":
            # TreeExplainer for XGBoost (fast and exact)
            self.explainer = shap.TreeExplainer(self.model)
        elif explainer_type == "exact":
            # Exact explainer (slower but more accurate)
            self.explainer = shap.ExactExplainer(
                self.model.predict_proba,
                X_background.values
            )
        else:
            raise ValueError(f"Unknown explainer type: {explainer_type}")
        
        elapsed = time.time() - start_time
        logger.info(f"Explainer created in {elapsed:.2f} seconds")
    
    def explain_prediction(
        self,
        X: Union[pd.DataFrame, pd.Series, Dict],
        max_evals: int = 100,
        return_time: bool = False
    ) -> Dict:
        """
        Explain a single prediction.
        
        Args:
            X: Single transaction features
            max_evals: Max evaluations for KernelExplainer
            return_time: Whether to return computation time
            
        Returns:
            Dictionary with SHAP values and explanation
        """
        if self.explainer is None:
            raise ValueError("Explainer not created. Call create_explainer() first.")
        
        start_time = time.time()
        
        # Convert to DataFrame if needed
        if isinstance(X, dict):
            X = pd.DataFrame([X])
        elif isinstance(X, pd.Series):
            X = X.to_frame().T
        
        # Handle missing values
        X = X.fillna(0)
        X = X.replace([np.inf, -np.inf], 0)
        
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(X)
        
        # Handle array format
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # Get positive class (fraud) SHAP values
        
        elapsed = time.time() - start_time
        
        if elapsed > 0.2:
            logger.warning(f"⚠️  SHAP computation took {elapsed:.3f}s (>200ms target)")
        else:
            logger.info(f"✅ SHAP computation: {elapsed:.3f}s")
        
        # Get top contributing features
        feature_names = X.columns
        shap_series = pd.Series(shap_values[0], index=feature_names)
        top_features = shap_series.abs().nlargest(10).to_dict()
        
        result = {
            'shap_values': shap_values[0].tolist(),
            'feature_names': list(feature_names),
            'top_features': top_features,
            'computation_time_ms': elapsed * 1000
        }
        
        if return_time:
            result['computation_time'] = elapsed
        
        return result
    
    def explain_batch(
        self,
        X: pd.DataFrame,
        max_evals: int = 100
    ) -> np.ndarray:
        """
        Explain multiple predictions.
        
        Args:
            X: Feature matrix
            max_evals: Max evaluations for KernelExplainer
            
        Returns:
            Array of SHAP values
        """
        if self.explainer is None:
            raise ValueError("Explainer not created. Call create_explainer() first.")
        
        logger.info(f"Explaining {len(X)} predictions...")
        
        start_time = time.time()
        
        # Handle missing values
        X = X.fillna(0)
        X = X.replace([np.inf, -np.inf], 0)
        
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(X)
        
        # Handle array format
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        elapsed = time.time() - start_time
        logger.info(f"Batch explanation complete in {elapsed:.2f} seconds")
        logger.info(f"Average time per prediction: {elapsed/len(X)*1000:.2f}ms")
        
        return shap_values
    
    def get_summary_plot_data(
        self,
        X: pd.DataFrame,
        n_features: int = 20
    ) -> Dict:
        """
        Generate data for SHAP summary plot.
        
        Args:
            X: Feature matrix
            n_features: Number of top features to include
            
        Returns:
            Dictionary with SHAP values and feature names
        """
        shap_values = self.explain_batch(X)
        
        # Get top features by mean absolute SHAP value
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        top_indices = np.argsort(mean_abs_shap)[-n_features:][::-1]
        
        return {
            'shap_values': shap_values[:, top_indices],
            'feature_names': [X.columns[i] for i in top_indices],
            'feature_values': X.iloc[:, top_indices].values
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    # explainer = FraudExplainer("models/xgboost_fraud_latest.pkl")
    
    # Load training data for background
    # X_train = pd.read_csv("data/processed/X_train.csv")
    
    # Create explainer
    # explainer.create_explainer(X_train, sample_size=1000)
    
    # Explain single prediction
    # X_test = pd.read_csv("data/processed/X_test.csv").head(1)
    # explanation = explainer.explain_prediction(X_test.iloc[0])
    
    # print(f"Top contributing features: {explanation['top_features']}")
    # print(f"Computation time: {explanation['computation_time_ms']:.2f}ms")

