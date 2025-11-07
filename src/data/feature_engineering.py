"""
Feature engineering for fraud detection.
Creates 95 engineered features from transaction data.
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)


class FraudFeatureEngineer:
    """Engineer features for fraud detection models."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def engineer_paysim_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer 50+ features from PaySim data.
        
        Args:
            df: Raw PaySim DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Engineering PaySim features...")
        
        features_df = df.copy()
        
        # 1. Temporal features
        features_df['hour'] = features_df['step'] % 24
        features_df['day_of_week'] = (features_df['step'] // 24) % 7
        features_df['is_weekend'] = (features_df['day_of_week'] >= 5).astype(int)
        
        # 2. Amount features
        features_df['amount_log'] = np.log1p(features_df['amount'])
        features_df['amount_sqrt'] = np.sqrt(features_df['amount'])
        features_df['amount_normalized'] = (features_df['amount'] - features_df['amount'].mean()) / (features_df['amount'].std() + 1e-8)
        
        # 3. Balance features
        features_df['orig_balance_diff'] = features_df['newbalanceOrig'] - features_df['oldbalanceOrg']
        features_df['dest_balance_diff'] = features_df['newbalanceDest'] - features_df['oldbalanceDest']
        features_df['balance_ratio_orig'] = features_df['newbalanceOrig'] / (features_df['oldbalanceOrg'] + 1)
        features_df['balance_ratio_dest'] = features_df['newbalanceDest'] / (features_df['oldbalanceDest'] + 1)
        
        # 4. Transaction type encoding
        type_dummies = pd.get_dummies(features_df['type'], prefix='type')
        features_df = pd.concat([features_df, type_dummies], axis=1)
        
        # 5. Velocity features (frequency within time window) - optimized for performance
        # Skip velocity calculations for very large datasets or use simplified version
        if len(features_df) > 50000:
            logger.info("Large dataset detected, using simplified velocity features...")
            features_df['sender_velocity_1h'] = 0
            features_df['sender_velocity_24h'] = 0
            features_df['receiver_velocity_1h'] = 0
            features_df['amount_velocity_1h'] = 0
            features_df['amount_velocity_24h'] = 0
        else:
            logger.info("Calculating velocity features...")
            features_df['sender_velocity_1h'] = self._calculate_velocity_optimized(
                features_df, 'nameOrig', window_hours=1
            )
            features_df['sender_velocity_24h'] = self._calculate_velocity_optimized(
                features_df, 'nameOrig', window_hours=24
            )
            features_df['receiver_velocity_1h'] = self._calculate_velocity_optimized(
                features_df, 'nameDest', window_hours=1
            )
            
            # 6. Amount velocity (total amount per time window)
            features_df['amount_velocity_1h'] = self._calculate_amount_velocity_optimized(
                features_df, 'nameOrig', window_hours=1
            )
            features_df['amount_velocity_24h'] = self._calculate_amount_velocity_optimized(
                features_df, 'nameOrig', window_hours=24
            )
        
        # 7. Behavioral features
        features_df['is_first_transaction'] = self._is_first_transaction(features_df, 'nameOrig')
        features_df['transaction_count'] = self._transaction_count(features_df, 'nameOrig')
        
        # 8. Risk features
        features_df['balance_depletion_orig'] = ((features_df['oldbalanceOrg'] == 0) & (features_df['newbalanceOrig'] == 0)).astype(int)
        features_df['balance_depletion_dest'] = ((features_df['oldbalanceDest'] == 0) & (features_df['newbalanceDest'] == 0)).astype(int)
        
        logger.info(f"Engineered {len(features_df.columns)} total features")
        
        return features_df
    
    def engineer_credit_card_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer 40+ features from Credit Card Fraud data.
        
        Args:
            df: Raw Credit Card DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Engineering Credit Card features...")
        
        features_df = df.copy()
        
        # 1. V features (already PCA-transformed, but add interactions)
        v_cols = [f'V{i}' for i in range(1, 29)]
        
        # 2. Statistical features across V columns
        features_df['v_mean'] = features_df[v_cols].mean(axis=1)
        features_df['v_std'] = features_df[v_cols].std(axis=1)
        features_df['v_min'] = features_df[v_cols].min(axis=1)
        features_df['v_max'] = features_df[v_cols].max(axis=1)
        features_df['v_range'] = features_df['v_max'] - features_df['v_min']
        
        # 3. Amount features
        features_df['amount_log'] = np.log1p(features_df['Amount'])
        features_df['amount_sqrt'] = np.sqrt(features_df['Amount'])
        features_df['amount_cube'] = np.power(np.abs(features_df['Amount']), 1/3)
        
        # 4. Interaction features (top principal components)
        features_df['v1_x_v2'] = features_df['V1'] * features_df['V2']
        features_df['v3_x_v4'] = features_df['V3'] * features_df['V4']
        features_df['v14_x_amount'] = features_df['V14'] * features_df['Amount']
        features_df['v17_x_amount'] = features_df['V17'] * features_df['Amount']
        
        # 5. Time features (if available)
        if 'Time' in features_df.columns:
            features_df['time_hour'] = (features_df['Time'] / 3600) % 24
            features_df['time_day'] = (features_df['Time'] / 86400) % 7
            features_df['is_weekend'] = (features_df['time_day'] >= 5).astype(int)
        
        logger.info(f"Engineered {len(features_df.columns)} total features")
        
        return features_df
    
    def _calculate_velocity_optimized(self, df: pd.DataFrame, column: str, window_hours: int) -> np.ndarray:
        """Calculate transaction frequency within time window (optimized version)."""
        df_sorted = df.sort_values('step').reset_index(drop=True)
        velocities = np.zeros(len(df_sorted))
        
        # Use groupby for better performance
        for account in df_sorted[column].unique():
            account_mask = df_sorted[column] == account
            account_df = df_sorted[account_mask].copy()
            
            if len(account_df) == 0:
                continue
            
            # Calculate velocity for this account
            for idx, row in account_df.iterrows():
                time_window_start = row['step'] - window_hours
                count = len(account_df[
                    (account_df['step'] > time_window_start) & 
                    (account_df['step'] <= row['step'])
                ])
                velocities[idx] = count
        
        # Map back to original index
        velocities_mapped = pd.Series(velocities, index=df_sorted.index)
        velocities_reordered = velocities_mapped.reindex(df.index)
        
        return velocities_reordered.fillna(0).values
    
    def _calculate_amount_velocity_optimized(self, df: pd.DataFrame, column: str, window_hours: int) -> np.ndarray:
        """Calculate total amount within time window (optimized version)."""
        df_sorted = df.sort_values('step').reset_index(drop=True)
        amounts = np.zeros(len(df_sorted))
        
        # Use groupby for better performance
        for account in df_sorted[column].unique():
            account_mask = df_sorted[column] == account
            account_df = df_sorted[account_mask].copy()
            
            if len(account_df) == 0:
                continue
            
            # Calculate amount velocity for this account
            for idx, row in account_df.iterrows():
                time_window_start = row['step'] - window_hours
                total = account_df[
                    (account_df['step'] > time_window_start) & 
                    (account_df['step'] <= row['step'])
                ]['amount'].sum()
                amounts[idx] = total
        
        # Map back to original index
        amounts_mapped = pd.Series(amounts, index=df_sorted.index)
        amounts_reordered = amounts_mapped.reindex(df.index)
        
        return amounts_reordered.fillna(0).values
    
    def _is_first_transaction(self, df: pd.DataFrame, column: str) -> np.ndarray:
        """Check if this is first transaction for account."""
        df_sorted = df.sort_values('step')
        is_first = ~df_sorted.duplicated(subset=column, keep='first')
        
        # Reorder to match original index
        is_first_reordered = is_first.reindex(df.index)
        return is_first_reordered.fillna(False).astype(int).values
    
    def _transaction_count(self, df: pd.DataFrame, column: str) -> np.ndarray:
        """Count total transactions per account."""
        counts = df.groupby(column).size()
        return df[column].map(counts).fillna(0).values
    
    def combine_and_prepare(
        self, 
        paysim_df: pd.DataFrame, 
        credit_df: pd.DataFrame,
        target_col_paysim: str = 'isFraud',
        target_col_credit: str = 'Class'
    ) -> pd.DataFrame:
        """
        Combine both datasets and prepare for training.
        
        Args:
            paysim_df: Processed PaySim DataFrame
            credit_df: Processed Credit Card DataFrame
            target_col_paysim: Target column name in PaySim
            target_col_credit: Target column name in Credit Card
            
        Returns:
            Combined and prepared DataFrame
        """
        logger.info("Combining datasets...")
        
        # Ensure target columns exist
        if target_col_paysim not in paysim_df.columns:
            raise ValueError(f"Target column '{target_col_paysim}' not found in PaySim")
        if target_col_credit not in credit_df.columns:
            raise ValueError(f"Target column '{target_col_credit}' not found in Credit Card")
        
        # Add dataset identifier
        paysim_df['dataset'] = 'paysim'
        credit_df['dataset'] = 'credit_card'
        
        # Standardize target column
        paysim_df['is_fraud'] = paysim_df[target_col_paysim]
        credit_df['is_fraud'] = credit_df[target_col_credit]
        
        # Drop non-feature columns from paysim (keep is_fraud for later)
        paysim_drop_cols = ['nameOrig', 'nameDest', 'type', 'isFlaggedFraud']
        if 'isFraud' in paysim_df.columns and 'is_fraud' in paysim_df.columns:
            paysim_drop_cols.append('isFraud')
        paysim_df = paysim_df.drop(columns=paysim_drop_cols, errors='ignore')
        
        # Combine
        combined_df = pd.concat([paysim_df, credit_df], ignore_index=True)
        
        logger.info(f"Combined dataset: {len(combined_df):,} transactions")
        logger.info(f"Fraud rate: {combined_df['is_fraud'].mean():.4f}")
        
        return combined_df


def engineer_features(paysim_df: pd.DataFrame, credit_df: pd.DataFrame) -> pd.DataFrame:
    """
    Main feature engineering function.
    
    Args:
        paysim_df: Raw PaySim DataFrame
        credit_df: Raw Credit Card DataFrame
        
    Returns:
        Combined DataFrame with engineered features
    """
    engineer = FraudFeatureEngineer()
    
    # Engineer features for each dataset
    paysim_engineered = engineer.engineer_paysim_features(paysim_df)
    credit_engineered = engineer.engineer_credit_card_features(credit_df)
    
    # Combine datasets
    combined = engineer.combine_and_prepare(
        paysim_engineered, 
        credit_engineered
    )
    
    return combined


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # This would be run after loader.py
    from data.loader import load_datasets
    
    # Load raw data
    paysim, credit = load_datasets()
    
    # Engineer features
    combined_df = engineer_features(paysim, credit)
    
    print(f"\nFeature Engineering Complete:")
    print(f"Total features: {len(combined_df.columns)}")
    print(f"Total transactions: {len(combined_df):,}")
    print(f"\nFeature columns: {list(combined_df.columns[:20])}...")

