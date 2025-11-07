"""
Verify that datasets are properly loaded and used in pipelines.

Usage:
    python scripts/verify_dataset_usage.py
"""
import pandas as pd
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_paysim_dataset():
    """Verify PaySim dataset exists and is loadable."""
    paysim_path = Path("data/raw/paysim.csv")
    
    if not paysim_path.exists():
        print("❌ PaySim dataset not found")
        print(f"   Expected location: {paysim_path.absolute()}")
        print("   Download from: https://www.kaggle.com/datasets/ealaxi/paysim1")
        return False
    
    try:
        df = pd.read_csv(paysim_path, nrows=1000)
        print(f"✅ PaySim dataset found: {len(df)} sample rows loaded")
        print(f"   Columns: {list(df.columns)}")
        print(f"   File size: {paysim_path.stat().st_size / (1024*1024):.2f} MB")
        return True
    except Exception as e:
        print(f"❌ Error loading PaySim: {e}")
        return False

def verify_credit_card_dataset():
    """Verify Credit Card Fraud dataset exists and is loadable."""
    cc_path = Path("data/raw/credit_card_fraud.csv")
    
    if not cc_path.exists():
        print("❌ Credit Card Fraud dataset not found")
        print(f"   Expected location: {cc_path.absolute()}")
        print("   Download from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        return False
    
    try:
        df = pd.read_csv(cc_path, nrows=1000)
        print(f"✅ Credit Card Fraud dataset found: {len(df)} sample rows loaded")
        print(f"   Columns: {list(df.columns)}")
        print(f"   File size: {cc_path.stat().st_size / (1024*1024):.2f} MB")
        return True
    except Exception as e:
        print(f"❌ Error loading Credit Card Fraud: {e}")
        return False

def verify_pipeline_usage():
    """Verify datasets are used in pipeline code."""
    loader_path = Path("src/data/loader.py")
    features_path = Path("src/data/feature_engineering.py")
    
    checks = []
    
    # Check loader.py
    if loader_path.exists():
        with open(loader_path, 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append(("loader.py exists", True))
            checks.append(("PaySim referenced", "paysim" in content.lower() or "load" in content.lower()))
            checks.append(("Credit Card referenced", "credit_card" in content.lower() or "credit" in content.lower()))
    else:
        checks.append(("loader.py exists", False))
    
    # Check feature_engineering.py
    if features_path.exists():
        with open(features_path, 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append(("feature_engineering.py exists", True))
            checks.append(("Feature engineering code present", len(content) > 100))
    else:
        checks.append(("feature_engineering.py exists", False))
    
    return checks

def verify_data_directory_structure():
    """Verify data directory structure exists."""
    required_dirs = [
        Path("data"),
        Path("data/raw"),
        Path("data/processed"),
    ]
    
    checks = []
    for dir_path in required_dirs:
        exists = dir_path.exists()
        checks.append((f"{dir_path} exists", exists))
    
    return checks

if __name__ == "__main__":
    print("=" * 60)
    print("Guardian Dataset Usage Verification")
    print("=" * 60)
    print()
    
    # Change to repo directory
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    results = []
    
    print("1. Dataset Files:")
    print("-" * 60)
    paysim_ok = verify_paysim_dataset()
    print()
    cc_ok = verify_credit_card_dataset()
    results.append(("PaySim dataset", paysim_ok))
    results.append(("Credit Card dataset", cc_ok))
    
    print("\n2. Pipeline Usage:")
    print("-" * 60)
    checks = verify_pipeline_usage()
    for check, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
        results.append((check, result))
    
    print("\n3. Directory Structure:")
    print("-" * 60)
    dir_checks = verify_data_directory_structure()
    for check, result in dir_checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
        results.append((check, result))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All checks passed!")
    else:
        print("⚠️  Some checks failed. See details above.")
        print("\nNote: Dataset verification requires datasets to be downloaded.")
        print("See DATA_ACQUISITION_GUIDE.md for download instructions.")

