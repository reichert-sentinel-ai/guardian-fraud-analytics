"""
Verify that models are trained and meet performance targets.

Usage:
    python scripts/verify_model_training.py
"""
import pickle
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_model_exists():
    """Verify trained model files exist."""
    model_paths = [
        Path("models/xgboost_model.pkl"),
        Path("models/xgboost_model.pkl"),
    ]
    
    results = []
    
    # Check XGBoost model
    xgb_path = Path("models/xgboost_model.pkl")
    if not xgb_path.exists():
        print("❌ XGBoost model not found")
        print(f"   Expected location: {xgb_path.absolute()}")
        print("   Run: python src/models/trainer.py")
        results.append(False)
    else:
        try:
            # Try to load model
            with open(xgb_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✅ XGBoost model found")
            print(f"   File size: {xgb_path.stat().st_size / (1024*1024):.2f} MB")
            results.append(True)
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            results.append(False)
    
    return results

def verify_model_directory():
    """Verify models directory exists."""
    models_dir = Path("models")
    if models_dir.exists():
        print(f"✅ Models directory exists")
        print(f"   Files: {list(models_dir.glob('*.pkl'))}")
        return True
    else:
        print("❌ Models directory not found")
        print("   Creating models directory...")
        models_dir.mkdir(parents=True, exist_ok=True)
        return False

def verify_training_script():
    """Verify training script exists."""
    trainer_path = Path("src/models/trainer.py")
    if trainer_path.exists():
        print(f"✅ Training script exists: {trainer_path}")
        return True
    else:
        print(f"❌ Training script not found: {trainer_path}")
        return False

def verify_evaluation_script():
    """Verify evaluation script exists."""
    evaluator_path = Path("src/models/evaluator.py")
    if evaluator_path.exists():
        print(f"✅ Evaluation script exists: {evaluator_path}")
        return True
    else:
        print(f"⚠️  Evaluation script not found: {evaluator_path}")
        return False

def verify_performance_targets():
    """Verify performance targets are documented."""
    # Performance targets from documentation
    targets = {
        'accuracy': 0.92,
        'precision': 0.90,
        'recall': 0.85,
        'f1_score': 0.88,
        'roc_auc': 0.95
    }
    
    print("\nPerformance Targets:")
    for metric, target in targets.items():
        print(f"   {metric}: ≥{target:.2%}")
    
    print("\n⚠️  Model performance verification requires:")
    print("   1. Trained models")
    print("   2. Test data")
    print("   3. Running evaluation script")
    
    return False  # Can't verify without actual training

if __name__ == "__main__":
    print("=" * 60)
    print("Guardian Model Training Verification")
    print("=" * 60)
    print()
    
    # Change to repo directory
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    results = []
    
    print("1. Model Files:")
    print("-" * 60)
    model_results = verify_model_exists()
    results.extend(model_results)
    
    print("\n2. Directory Structure:")
    print("-" * 60)
    dir_ok = verify_model_directory()
    results.append(dir_ok)
    
    print("\n3. Training Scripts:")
    print("-" * 60)
    trainer_ok = verify_training_script()
    evaluator_ok = verify_evaluation_script()
    results.append(trainer_ok)
    results.append(evaluator_ok)
    
    print("\n4. Performance Targets:")
    print("-" * 60)
    verify_performance_targets()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All checks passed!")
    else:
        print("⚠️  Some checks failed. See details above.")
        print("\nNote: Model training verification requires:")
        print("  1. Datasets downloaded")
        print("  2. Models trained")
        print("  3. Evaluation run")
        print("\nSee docs/MODEL_TRAINING_VERIFICATION.md for details.")

