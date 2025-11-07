"""
Execute Chat 1: Data Acquisition and Feature Engineering
"""

import logging
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.loader import FraudDataLoader
from data.feature_engineering import engineer_features
from data.train_test_split import create_train_test_split

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main execution pipeline."""
    logger.info("Starting Chat 1: Data Acquisition...")
    
    # 1. Load datasets
    loader = FraudDataLoader()
    paysim_df = loader.download_paysim()
    credit_df = loader.download_credit_card_fraud()
    
    # Save raw data
    loader.save_processed(paysim_df, "raw_paysim.csv")
    loader.save_processed(credit_df, "raw_credit_card.csv")
    
    # 2. Engineer features
    combined_df = engineer_features(paysim_df, credit_df)
    
    # Save processed data
    loader.save_processed(combined_df, "combined_features.csv")
    
    # 3. Create train/test split
    X_train, X_test, y_train, y_test = create_train_test_split(combined_df)
    
    # Save splits
    X_train.to_csv("data/processed/X_train.csv", index=False)
    X_test.to_csv("data/processed/X_test.csv", index=False)
    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv", index=False)
    
    logger.info("Chat 1 Complete!")
    logger.info(f"Ready for Chat 2: Model Training")
    logger.info(f"Training samples: {len(X_train):,}")
    logger.info(f"Test samples: {len(X_test):,}")


if __name__ == "__main__":
    main()

