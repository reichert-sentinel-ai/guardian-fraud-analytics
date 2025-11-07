"""
Data loader for Guardian fraud detection datasets.
Handles downloading and loading PaySim and Credit Card fraud datasets.
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

# Try to import kaggle, but don't fail if it's not available or not configured
try:
    import kaggle
    KAGGLE_AVAILABLE = True
except (ImportError, OSError) as e:
    logger.warning(f"Kaggle API not available: {e}")
    KAGGLE_AVAILABLE = False
    kaggle = None


class FraudDataLoader:
    """Load and manage fraud detection datasets."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def download_paysim(self) -> pd.DataFrame:
        """
        Download PaySim fraud dataset from Kaggle.
        
        Returns:
            DataFrame with PaySim transactions
        """
        logger.info("Downloading PaySim dataset...")
        
        output_path = self.raw_dir / "guardian"
        output_path.mkdir(exist_ok=True)
        
        # Check if file already exists
        csv_file = output_path / "PS_20174392719_1491204439457_log.csv"
        if csv_file.exists():
            logger.info(f"PaySim file already exists at {csv_file}, loading from disk...")
            df = pd.read_csv(csv_file)
            logger.info(f"PaySim loaded: {len(df):,} transactions")
            return df
        
        # Download dataset
        if not KAGGLE_AVAILABLE:
            raise FileNotFoundError(
                f"PaySim dataset not found at {csv_file} and Kaggle API is not available. "
                "Please either:\n"
                "1. Download kaggle.json from https://www.kaggle.com/settings and place it in "
                f"{Path.home() / '.kaggle' / 'kaggle.json'}, or\n"
                "2. Manually download the dataset from Kaggle and place it in the data/raw/guardian directory."
            )
        
        try:
            kaggle.api.dataset_download_files(
                'ealaxi/paysim1',
                path=str(output_path),
                unzip=True
            )
            
            # Load CSV
            if csv_file.exists():
                df = pd.read_csv(csv_file)
            else:
                # Try to find any CSV file in the directory
                csv_files = list(output_path.glob("*.csv"))
                if csv_files:
                    df = pd.read_csv(csv_files[0])
                else:
                    raise FileNotFoundError(f"PaySim CSV file not found in {output_path}")
            
            logger.info(f"PaySim loaded: {len(df):,} transactions")
            return df
        except Exception as e:
            logger.error(f"Error downloading PaySim dataset: {e}")
            logger.info("If Kaggle authentication fails, please:")
            logger.info("1. Download kaggle.json from https://www.kaggle.com/settings")
            logger.info("2. Place it in ~/.kaggle/kaggle.json (Mac/Linux) or C:\\Users\\%USERNAME%\\.kaggle\\kaggle.json (Windows)")
            raise
    
    def download_credit_card_fraud(self) -> pd.DataFrame:
        """
        Download Credit Card Fraud dataset from Kaggle.
        
        Returns:
            DataFrame with credit card transactions
        """
        logger.info("Downloading Credit Card Fraud dataset...")
        
        output_path = self.raw_dir / "guardian"
        output_path.mkdir(exist_ok=True)
        
        # Check if file already exists
        csv_file = output_path / "creditcard.csv"
        if csv_file.exists():
            logger.info(f"Credit Card Fraud file already exists at {csv_file}, loading from disk...")
            df = pd.read_csv(csv_file)
            logger.info(f"Credit Card Fraud loaded: {len(df):,} transactions")
            return df
        
        # Download dataset
        if not KAGGLE_AVAILABLE:
            raise FileNotFoundError(
                f"Credit Card Fraud dataset not found at {csv_file} and Kaggle API is not available. "
                "Please either:\n"
                "1. Download kaggle.json from https://www.kaggle.com/settings and place it in "
                f"{Path.home() / '.kaggle' / 'kaggle.json'}, or\n"
                "2. Manually download the dataset from Kaggle and place it in the data/raw/guardian directory."
            )
        
        try:
            kaggle.api.dataset_download_files(
                'mlg-ulb/creditcardfraud',
                path=str(output_path),
                unzip=True
            )
            
            # Load CSV
            if csv_file.exists():
                df = pd.read_csv(csv_file)
            else:
                # Try to find any CSV file in the directory
                csv_files = list(output_path.glob("*.csv"))
                if csv_files:
                    df = pd.read_csv(csv_files[0])
                else:
                    raise FileNotFoundError(f"Credit Card Fraud CSV file not found in {output_path}")
            
            logger.info(f"Credit Card Fraud loaded: {len(df):,} transactions")
            return df
        except Exception as e:
            logger.error(f"Error downloading Credit Card Fraud dataset: {e}")
            logger.info("If Kaggle authentication fails, please:")
            logger.info("1. Download kaggle.json from https://www.kaggle.com/settings")
            logger.info("2. Place it in ~/.kaggle/kaggle.json (Mac/Linux) or C:\\Users\\%USERNAME%\\.kaggle\\kaggle.json (Windows)")
            raise
    
    def save_processed(self, df: pd.DataFrame, filename: str):
        """Save processed dataset to CSV."""
        output_path = self.processed_dir / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Saved processed data to {output_path}")


def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load both fraud datasets.
    
    Returns:
        Tuple of (paysim_df, creditcard_df)
    """
    loader = FraudDataLoader()
    
    # Load PaySim
    paysim_df = loader.download_paysim()
    
    # Load Credit Card
    credit_df = loader.download_credit_card_fraud()
    
    return paysim_df, credit_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Load datasets
    paysim, credit = load_datasets()
    
    print(f"\nDataset Summary:")
    print(f"PaySim: {len(paysim):,} transactions")
    print(f"Credit Card: {len(credit):,} transactions")
    print(f"\nPaySim columns: {list(paysim.columns)}")
    print(f"Credit Card columns: {list(credit.columns)}")

