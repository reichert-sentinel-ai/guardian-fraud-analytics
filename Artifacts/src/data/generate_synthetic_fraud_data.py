"""
Create synthetic fraud detection dataset for quick prototyping.
100K transactions instead of 6M for faster iteration.
"""

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

def create_synthetic_fraud_data(n_samples=100_000, fraud_rate=0.015):
    """Generate synthetic fraud dataset."""
    
    print(f"Generating {n_samples:,} synthetic transactions...")
    
    n_fraud = int(n_samples * fraud_rate)
    n_legit = n_samples - n_fraud
    
    # Generate legitimate transactions
    legit_data = {
        'amount': np.random.lognormal(4.5, 0.8, n_legit).clip(1, 5000),
        'hour': np.random.choice(range(8, 22), n_legit),  # Business hours
        'is_fraud': 0
    }
    
    # Generate fraud transactions
    fraud_data = {
        'amount': np.random.lognormal(6.0, 1.2, n_fraud).clip(100, 10000),
        'hour': np.random.choice(range(0, 7), n_fraud),  # Night time
        'is_fraud': 1
    }
    
    # Combine
    df_legit = pd.DataFrame(legit_data)
    df_fraud = pd.DataFrame(fraud_data)
    df = pd.concat([df_legit, df_fraud], ignore_index=True)
    
    # Add more features
    df['amount_log'] = np.log1p(df['amount'])
    df['is_weekend'] = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    df['velocity_24h'] = np.where(
        df['is_fraud'] == 1,
        np.random.poisson(15, n_samples),  # High velocity for fraud
        np.random.poisson(3, n_samples)    # Low velocity for legit
    )
    df['amount_deviation'] = np.where(
        df['is_fraud'] == 1,
        np.random.exponential(2.5, n_samples),  # High deviation for fraud
        np.random.exponential(0.5, n_samples)   # Low deviation for legit
    )
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"✅ Generated {len(df):,} transactions")
    print(f"   Fraud: {df['is_fraud'].sum():,} ({df['is_fraud'].mean()*100:.2f}%)")
    print(f"   Legitimate: {(~df['is_fraud'].astype(bool)).sum():,}")
    
    return df

def create_train_test_split(df, test_size=0.2):
    """Split into train/test."""
    from sklearn.model_selection import train_test_split
    
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Create directories (relative to script location)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    data_dir = project_root / "data" / "processed"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate data
    df = create_synthetic_fraud_data(n_samples=100_000)
    
    # Split
    X_train, X_test, y_train, y_test = create_train_test_split(df)
    
    # Save
    X_train.to_csv(data_dir / "X_train.csv", index=False)
    X_test.to_csv(data_dir / "X_test.csv", index=False)
    y_train.to_csv(data_dir / "y_train.csv", index=False)
    y_test.to_csv(data_dir / "y_test.csv", index=False)
    
    print(f"\n✅ Data saved to {data_dir}")
    print(f"   Training samples: {len(X_train):,}")
    print(f"   Test samples: {len(X_test):,}")

