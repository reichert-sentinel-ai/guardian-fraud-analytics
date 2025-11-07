"""
XGBoost fraud detection model trainer.
Handles model training, hyperparameter tuning, and evaluation.
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
from sklearn.model_selection import cross_val_score
import joblib
import json
from datetime import datetime
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)


class FraudModelTrainer:
    """Train and evaluate XGBoost fraud detection models."""
    
    def __init__(
        self,
        models_dir: str = "models",
        reports_dir: str = "reports",
        random_state: int = 42
    ):
        self.models_dir = Path(models_dir)
        self.reports_dir = Path(reports_dir)
        self.random_state = random_state
        
        # Create directories
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.feature_importance = None
        self.evaluation_metrics = {}
        
    def load_training_data(
        self,
        X_train_path: str = "data/processed/X_train.csv",
        y_train_path: str = "data/processed/y_train.csv",
        X_test_path: str = "data/processed/X_test.csv",
        y_test_path: str = "data/processed/y_test.csv"
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        """
        Load training and test data.
        
        Args:
            X_train_path: Path to training features
            y_train_path: Path to training labels
            X_test_path: Path to test features
            y_test_path: Path to test labels
            
        Returns:
            X_train, y_train, X_test, y_test
        """
        logger.info("Loading training data...")
        
        X_train = pd.read_csv(X_train_path)
        y_train = pd.read_csv(y_train_path).squeeze()
        X_test = pd.read_csv(X_test_path)
        y_test = pd.read_csv(y_test_path).squeeze()
        
        # Handle missing values
        X_train = X_train.fillna(0)
        X_test = X_test.fillna(0)
        
        # Handle infinite values
        X_train = X_train.replace([np.inf, -np.inf], 0)
        X_test = X_test.replace([np.inf, -np.inf], 0)
        
        logger.info(f"Training set: {X_train.shape[0]:,} samples, {X_train.shape[1]} features")
        logger.info(f"Test set: {X_test.shape[0]:,} samples")
        logger.info(f"Fraud rate - Train: {y_train.mean():.4f}, Test: {y_test.mean():.4f}")
        
        return X_train, y_train, X_test, y_test
    
    def train_xgboost(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        hyperparameters: Optional[Dict] = None
    ) -> xgb.XGBClassifier:
        """
        Train XGBoost fraud classifier.
        
        Args:
            X_train: Training features
            y_train: Training labels
            hyperparameters: Optional custom hyperparameters
            
        Returns:
            Trained XGBoost model
        """
        logger.info("Training XGBoost fraud classifier...")
        
        # Default hyperparameters (optimized for fraud detection)
        default_params = {
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            'max_depth': 8,
            'learning_rate': 0.01,
            'n_estimators': 500,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'min_child_weight': 3,
            'gamma': 0.1,
            'reg_alpha': 0.1,
            'reg_lambda': 1.0,
            'scale_pos_weight': (1 - y_train.mean()) / y_train.mean(),  # Handle class imbalance
            'random_state': self.random_state,
            'n_jobs': -1,
            'tree_method': 'hist'
        }
        
        # Merge with custom hyperparameters if provided
        if hyperparameters:
            default_params.update(hyperparameters)
        
        logger.info(f"Hyperparameters: {default_params}")
        
        # Create and train model
        self.model = xgb.XGBClassifier(**default_params)
        
        # Train with early stopping
        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_train, y_train)],
            verbose=100
        )
        
        logger.info("Model training complete!")
        
        # Extract feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info(f"Top 10 features:\n{self.feature_importance.head(10)}")
        
        return self.model
    
    def evaluate_model(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        threshold: float = 0.5
    ) -> Dict:
        """
        Evaluate model performance.
        
        Args:
            X_test: Test features
            y_test: Test labels
            threshold: Classification threshold
            
        Returns:
            Dictionary of evaluation metrics
        """
        logger.info("Evaluating model performance...")
        
        if self.model is None:
            raise ValueError("Model not trained. Call train_xgboost() first.")
        
        # Predictions
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba >= threshold).astype(int)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc_roc = roc_auc_score(y_test, y_pred_proba)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Store metrics
        self.evaluation_metrics = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'auc_roc': float(auc_roc),
            'threshold': float(threshold),
            'confusion_matrix': cm.tolist(),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        # Log metrics
        logger.info("=" * 50)
        logger.info("MODEL EVALUATION RESULTS")
        logger.info("=" * 50)
        logger.info(f"Accuracy:  {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1 Score:  {f1:.4f}")
        logger.info(f"AUC-ROC:   {auc_roc:.4f}")
        logger.info("=" * 50)
        
        # Check success criteria
        if accuracy >= 0.92:
            logger.info("✅ Accuracy target met (≥92%)")
        else:
            logger.warning(f"⚠️  Accuracy below target (current: {accuracy:.2%}, target: 92%)")
        
        if auc_roc >= 0.95:
            logger.info("✅ AUC-ROC target met (≥0.95)")
        else:
            logger.warning(f"⚠️  AUC-ROC below target (current: {auc_roc:.4f}, target: 0.95)")
        
        return self.evaluation_metrics
    
    def save_model(
        self,
        model_name: str = "xgboost_fraud",
        format: str = "joblib"
    ) -> Path:
        """
        Save trained model to disk.
        
        Args:
            model_name: Name for saved model
            format: Format to save ('joblib' or 'json')
            
        Returns:
            Path to saved model
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_xgboost() first.")
        
        logger.info(f"Saving model as {model_name}...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "joblib":
            model_path = self.models_dir / f"{model_name}_{timestamp}.pkl"
            joblib.dump(self.model, model_path)
        elif format == "json":
            model_path = self.models_dir / f"{model_name}_{timestamp}.json"
            self.model.save_model(str(model_path))
        else:
            raise ValueError(f"Unknown format: {format}")
        
        logger.info(f"Model saved to: {model_path}")
        
        # Also save feature importance
        if self.feature_importance is not None:
            importance_path = self.models_dir / f"{model_name}_feature_importance_{timestamp}.csv"
            self.feature_importance.to_csv(importance_path, index=False)
            logger.info(f"Feature importance saved to: {importance_path}")
        
        return model_path
    
    def save_evaluation_report(self, model_name: str = "xgboost_fraud") -> Path:
        """
        Save evaluation metrics to JSON report.
        
        Args:
            model_name: Name for report
            
        Returns:
            Path to saved report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.reports_dir / f"{model_name}_evaluation_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(self.evaluation_metrics, f, indent=2)
        
        logger.info(f"Evaluation report saved to: {report_path}")
        
        return report_path


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize trainer
    trainer = FraudModelTrainer()
    
    # Load data
    X_train, y_train, X_test, y_test = trainer.load_training_data()
    
    # Train model
    model = trainer.train_xgboost(X_train, y_train)
    
    # Evaluate model
    metrics = trainer.evaluate_model(X_test, y_test)
    
    # Save model and report
    model_path = trainer.save_model()
    report_path = trainer.save_evaluation_report()
    
    print("\n" + "=" * 50)
    print("Chat 2: Model Training Complete!")
    print("=" * 50)
    print(f"Model saved to: {model_path}")
    print(f"Report saved to: {report_path}")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"AUC-ROC: {metrics['auc_roc']:.4f}")
    print("=" * 50)

