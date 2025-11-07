"""
Train/test split utility with stratification.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)


def create_train_test_split(
    df: pd.DataFrame,
    target_col: str = 'is_fraud',
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True
) -> tuple:
    """
    Create stratified train/test split.
    
    Args:
        df: Combined feature DataFrame
        target_col: Target column name
        test_size: Proportion of test set
        random_state: Random seed
        stratify: Whether to stratify by target
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    logger.info("Creating train/test split...")
    
    # Separate features and target
    # Drop target, dataset, and non-numeric columns (IDs, categorical)
    columns_to_drop = [target_col, 'dataset', 'isFraud', 'isFlaggedFraud', 
                       'nameOrig', 'nameDest', 'type']
    X = df.drop(columns=columns_to_drop, errors='ignore')
    y = df[target_col]
    
    # Handle missing values
    X = X.fillna(0)
    
    # Handle infinite values
    X = X.replace([np.inf, -np.inf], 0)
    
    # Create split
    if stratify:
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, 
                stratify=y
            )
        except ValueError as e:
            logger.warning(f"Stratification failed: {e}. Using non-stratified split.")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
    
    logger.info(f"Train set: {len(X_train):,} samples")
    logger.info(f"Test set: {len(X_test):,} samples")
    logger.info(f"Fraud rate - Train: {y_train.mean():.4f}, Test: {y_test.mean():.4f}")
    
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Run end-to-end pipeline
    from data.loader import load_datasets
    from data.feature_engineering import engineer_features
    
    # Load and engineer
    paysim, credit = load_datasets()
    combined = engineer_features(paysim, credit)
    
    # Create splits
    X_train, X_test, y_train, y_test = create_train_test_split(combined)
    
    print(f"\nTrain/Test Split Complete:")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")

