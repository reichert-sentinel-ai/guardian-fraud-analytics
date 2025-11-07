"""
Execute Chat 1: Data Acquisition and Feature Engineering
WITH SAMPLE DATA for testing when Kaggle/datasets unavailable
"""

import logging
from pathlib import Path
import sys
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.feature_engineering import engineer_features
from data.train_test_split import create_train_test_split

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_sample_paysim(n_samples=5000) -> pd.DataFrame:
    """Create sample PaySim dataset for testing."""
    logger.info(f"Creating sample PaySim dataset with {n_samples:,} transactions...")
    
    np.random.seed(42)
    
    # Sample PaySim structure
    data = {
        'step': np.random.randint(1, 744, n_samples),
        'type': np.random.choice(['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN'], n_samples),
        'amount': np.random.lognormal(mean=8, sigma=2, size=n_samples),
        'nameOrig': [f'C{np.random.randint(1000000, 9999999)}' for _ in range(n_samples)],
        'oldbalanceOrg': np.random.lognormal(mean=9, sigma=2, size=n_samples),
        'newbalanceOrig': np.zeros(n_samples),
        'nameDest': [f'C{np.random.randint(1000000, 9999999)}' for _ in range(n_samples)],
        'oldbalanceDest': np.random.lognormal(mean=9, sigma=2, size=n_samples),
        'newbalanceDest': np.zeros(n_samples),
        'isFraud': np.random.choice([0, 1], n_samples, p=[0.997, 0.003])
    }
    
    df = pd.DataFrame(data)
    
    # Update balances based on amounts
    df['newbalanceOrig'] = df['oldbalanceOrg'] - df['amount']
    df['newbalanceDest'] = df['oldbalanceDest'] + df['amount']
    
    # Ensure non-negative balances
    df.loc[df['newbalanceOrig'] < 0, 'newbalanceOrig'] = 0
    df.loc[df['newbalanceDest'] < 0, 'newbalanceDest'] = 0
    
    logger.info(f"Sample PaySim created: {len(df):,} transactions, fraud rate: {df['isFraud'].mean():.4f}")
    return df


def create_sample_credit_card(n_samples=2500) -> pd.DataFrame:
    """Create sample Credit Card Fraud dataset for testing."""
    logger.info(f"Creating sample Credit Card Fraud dataset with {n_samples:,} transactions...")
    
    np.random.seed(42)
    
    # Create V1-V28 features (PCA-transformed)
    v_features = {}
    for i in range(1, 29):
        v_features[f'V{i}'] = np.random.randn(n_samples)
    
    # Create Amount (with log-normal distribution)
    amounts = np.random.lognormal(mean=4, sigma=1.5, size=n_samples)
    
    # Create Time feature
    time_values = np.random.randint(0, 172792, n_samples)
    
    # Create Class (fraud label) - highly imbalanced
    fraud_rate = 0.0017  # Real dataset has ~0.17% fraud
    classes = np.random.choice([0, 1], n_samples, p=[1-fraud_rate, fraud_rate])
    
    data = {
        **v_features,
        'Time': time_values,
        'Amount': amounts,
        'Class': classes
    }
    
    df = pd.DataFrame(data)
    
    logger.info(f"Sample Credit Card created: {len(df):,} transactions, fraud rate: {df['Class'].mean():.4f}")
    return df


def main():
    """Main execution pipeline with sample data."""
    logger.info("Starting Chat 1: Data Acquisition (SAMPLE MODE)...")
    logger.info("=" * 60)
    
    # 1. Create sample datasets
    logger.info("Creating sample datasets for testing...")
    paysim_df = create_sample_paysim(n_samples=10000)
    credit_df = create_sample_credit_card(n_samples=5000)
    
    # Save raw sample data
    from data.loader import FraudDataLoader
    loader = FraudDataLoader()
    loader.save_processed(paysim_df, "sample_raw_paysim.csv")
    loader.save_processed(credit_df, "sample_raw_credit_card.csv")
    
    logger.info("=" * 60)
    
    # 2. Engineer features
    logger.info("Engineering features...")
    combined_df = engineer_features(paysim_df, credit_df)
    
    # Save processed data
    loader.save_processed(combined_df, "sample_combined_features.csv")
    
    logger.info("=" * 60)
    
    # 3. Create train/test split
    logger.info("Creating train/test split...")
    X_train, X_test, y_train, y_test = create_train_test_split(combined_df)
    
    # Save splits
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    X_train.to_csv("data/processed/sample_X_train.csv", index=False)
    X_test.to_csv("data/processed/sample_X_test.csv", index=False)
    y_train.to_csv("data/processed/sample_y_train.csv", index=False)
    y_test.to_csv("data/processed/sample_y_test.csv", index=False)
    
    logger.info("=" * 60)
    logger.info("Chat 1 Complete (SAMPLE MODE)!")
    logger.info(f"Ready for Chat 2: Model Training")
    logger.info(f"Training samples: {len(X_train):,}")
    logger.info(f"Test samples: {len(X_test):,}")
    logger.info(f"Total features: {X_train.shape[1]}")
    logger.info("=" * 60)
    logger.info("")
    logger.info("NOTE: This used SAMPLE DATA for testing.")
    logger.info("For full datasets, configure Kaggle API and run: python scripts\\run_chat1.py")


if __name__ == "__main__":
    main()

