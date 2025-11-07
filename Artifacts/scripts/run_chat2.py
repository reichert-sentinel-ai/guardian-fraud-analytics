"""
Chat 2: Model Training and Evaluation - Main Execution Script
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import logging
from datetime import datetime
from models.trainer import FraudModelTrainer
from models.visualizer import ModelVisualizer
import pandas as pd
import numpy as np

# Configure logging
log_file = Path(__file__).parent.parent / f'chat2_training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Execute Chat 2: Model Training and Evaluation."""
    
    logger.info("=" * 70)
    logger.info("CHAT 2: GUARDIAN MODEL TRAINING & EVALUATION")
    logger.info("=" * 70)
    
    try:
        # Initialize trainer
        logger.info("Initializing model trainer...")
        trainer = FraudModelTrainer()
        
        # Load training data
        logger.info("\n" + "-" * 70)
        logger.info("STEP 1: Loading Training Data")
        logger.info("-" * 70)
        X_train, y_train, X_test, y_test = trainer.load_training_data()
        
        # Train model
        logger.info("\n" + "-" * 70)
        logger.info("STEP 2: Training XGBoost Model")
        logger.info("-" * 70)
        model = trainer.train_xgboost(X_train, y_train)
        
        # Evaluate model
        logger.info("\n" + "-" * 70)
        logger.info("STEP 3: Evaluating Model Performance")
        logger.info("-" * 70)
        metrics = trainer.evaluate_model(X_test, y_test)
        
        # Generate predictions for visualization
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba >= 0.5).astype(int)
        
        # Create visualizations
        logger.info("\n" + "-" * 70)
        logger.info("STEP 4: Generating Visualizations")
        logger.info("-" * 70)
        visualizer = ModelVisualizer()
        
        # Confusion matrix
        visualizer.plot_confusion_matrix(
            y_test.values,
            y_pred,
            title="XGBoost Fraud Detection - Confusion Matrix"
        )
        
        # ROC curve
        visualizer.plot_roc_curve(
            y_test.values,
            y_pred_proba,
            title="XGBoost Fraud Detection - ROC Curve"
        )
        
        # Feature importance
        visualizer.plot_feature_importance(
            trainer.feature_importance,
            top_n=20,
            title="XGBoost Fraud Detection - Top 20 Feature Importance"
        )
        
        # Save model and report
        logger.info("\n" + "-" * 70)
        logger.info("STEP 5: Saving Model and Reports")
        logger.info("-" * 70)
        model_path = trainer.save_model("xgboost_fraud")
        report_path = trainer.save_evaluation_report("xgboost_fraud")
        
        # Final summary
        logger.info("\n" + "=" * 70)
        logger.info("CHAT 2 COMPLETE!")
        logger.info("=" * 70)
        logger.info(f"Model saved to: {model_path}")
        logger.info(f"Evaluation report saved to: {report_path}")
        logger.info(f"\nPerformance Summary:")
        logger.info(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall:    {metrics['recall']:.4f}")
        logger.info(f"  F1 Score:  {metrics['f1_score']:.4f}")
        logger.info(f"  AUC-ROC:   {metrics['auc_roc']:.4f}")
        logger.info("\n" + "=" * 70)
        logger.info("Ready for Chat 3: FastAPI Backend")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Error in Chat 2 execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

