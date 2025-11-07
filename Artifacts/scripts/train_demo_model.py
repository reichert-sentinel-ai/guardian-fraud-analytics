"""
Quick XGBoost training on synthetic data.
~5 minutes instead of hours.
"""

import sys
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
from pathlib import Path
import json
import logging

# Add src to path if needed
sys.path.append(str(Path(__file__).parent.parent / "src"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Train quick XGBoost model on synthetic demo data."""
    print("Loading data...")
    logger.info("Loading demo data...")
    
    # Get project root (scripts directory's parent)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / "data" / "processed"
    models_dir = project_root / "models"
    reports_dir = project_root / "reports"
    
    # Create directories
    models_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    # Load data
    X_train = pd.read_csv(data_dir / "X_train.csv")
    y_train = pd.read_csv(data_dir / "y_train.csv").squeeze()
    X_test = pd.read_csv(data_dir / "X_test.csv")
    y_test = pd.read_csv(data_dir / "y_test.csv").squeeze()
    
    print(f"Training on {len(X_train):,} samples...")
    logger.info(f"Training on {len(X_train):,} samples...")
    logger.info(f"Test set: {len(X_test):,} samples")
    
    # Train simple model (optimized for speed)
    print("Training XGBoost model...")
    logger.info("Training XGBoost model...")
    model = xgb.XGBClassifier(
        max_depth=6,
        learning_rate=0.1,
        n_estimators=100,
        scale_pos_weight=(1 - y_train.mean()) / y_train.mean(),
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=10)
    
    # Evaluate
    logger.info("Evaluating model...")
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1_score': float(f1_score(y_test, y_pred)),
        'auc_roc': float(roc_auc_score(y_test, y_pred_proba))
    }
    
    # Print results
    print("\n" + "="*50)
    print("MODEL PERFORMANCE")
    print("="*50)
    for metric, value in metrics.items():
        print(f"{metric:12s}: {value:.4f}")
    print("="*50)
    
    # Save model
    model_path = models_dir / "xgboost_fraud_demo.pkl"
    joblib.dump(model, model_path)
    print(f"\n✅ Model saved to {model_path}")
    
    # Save metrics
    metrics_path = reports_dir / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"✅ Metrics saved to {metrics_path}")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Starting train_demo_model.py...", flush=True)
    try:
        main()
        print("Script completed successfully!", flush=True)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

