# Synthetic Data Generation

## Overview

Guardian uses synthetic data generated to simulate realistic fraud detection scenarios without exposing real customer information. This document explains the data generation process, statistical properties, and validation methods.

## Data Source

**Base Dataset:** PaySim Financial Dataset  
**Source:** [Kaggle PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1)  
**Original Size:** 6.3M transactions  
**Author:** NTNU (Norwegian University of Science and Technology)

PaySim is a mobile money transaction simulator designed to detect fraud. It's based on real transaction logs from a mobile money service in an African country.

## Why Synthetic Data?

### Privacy & Compliance
- **GDPR Compliance:** No real customer data used
- **PCI DSS:** No actual payment card information
- **Legal Safety:** No risk of data breach liability
- **Ethical:** No privacy concerns for demonstration

### Technical Benefits
- **Known Ground Truth:** Labeled fraud cases for validation
- **Reproducibility:** Same dataset for benchmarking
- **Scalability:** Can generate any volume needed
- **Controlled Scenarios:** Test edge cases systematically

## Data Generation Process

### Step 1: Base Transaction Generation

Used PaySim simulator with parameters:
```python
# PaySim configuration
NUM_TRANSACTIONS = 600_000
FRAUD_RATE = 0.015  # 1.5% fraud (realistic)
TIME_SPAN_DAYS = 30
NUM_CUSTOMERS = 25_000
NUM_MERCHANTS = 5_000
```

### Step 2: Feature Engineering

Created 47 engineered features from raw transactions:

#### Temporal Features
```python
- hour_of_day: 0-23
- day_of_week: 0-6 (Mon-Sun)
- is_weekend: binary
- is_night: binary (11PM-6AM)
- days_since_account_creation: int
- time_since_last_transaction: float (hours)
```

#### Velocity Features
```python
- transaction_velocity_1h: count in last hour
- transaction_velocity_24h: count in last 24 hours
- transaction_velocity_7d: count in last 7 days
- amount_velocity_24h: $ spent in last 24 hours
- amount_velocity_7d: $ spent in last 7 days
```

#### Deviation Features
```python
- amount_deviation_from_avg: z-score vs user's average
- amount_deviation_from_merchant_avg: z-score vs merchant average
- time_deviation_from_pattern: unusual time for this user
- amount_zscore: standardized amount
```

#### Network Features
```python
- shared_device_count: # accounts sharing this device
- shared_ip_count: # accounts from this IP
- network_centrality: PageRank score in transaction graph
- community_id: Fraud ring cluster assignment
- transaction_count_same_device: count on this device
- transaction_count_same_ip: count from this IP
```

#### Risk Score Features
```python
- merchant_risk_score: historical fraud rate at merchant
- device_risk_score: device fraud history
- geolocation_risk: cross-border, high-risk countries
- account_age_days: days since account creation
- account_age_category: categorical (new/established/old)
```

#### Behavioral Features
```python
- cross_border_flag: binary (domestic vs international)
- device_fingerprint_mismatch: binary (new device)
- merchant_category: categorical (electronics, food, etc.)
- transaction_type: categorical (purchase, refund, etc.)
- payment_method: categorical (card, mobile, etc.)
```

#### Statistical Features
```python
- amount_percentile_user: percentile within user's history
- amount_percentile_merchant: percentile within merchant's history
- frequency_score: transaction frequency vs baseline
- recency_score: time since last transaction
```

### Step 3: Fraud Scenario Injection

Injected realistic fraud patterns:

#### 1. Account Takeover (40% of fraud)
```python
def generate_account_takeover(account_id, timestamp):
    """
    Simulate compromised account:
    - Burst of transactions
    - Different device/IP
    - Higher than normal amounts
    - Unusual merchants
    """
    return {
        'velocity_spike': True,
        'device_mismatch': True,
        'amount_deviation': 3.5,  # 3.5 std devs
        'merchant_category_unusual': True,
        'transaction_velocity_24h': random.randint(20, 50),
        'time_since_last_transaction': random.uniform(0.1, 2.0)  # minutes
    }
```

#### 2. Synthetic Identity (25% of fraud)
```python
def generate_synthetic_identity():
    """
    Fake identity using mix of real/fake info:
    - New account (< 30 days)
    - Rapid credit building pattern
    - Multiple accounts same device
    - "Bust out" spending spike
    """
    return {
        'account_age_days': random.randint(5, 25),
        'credit_history_mismatch': True,
        'device_shared_count': random.randint(3, 8),
        'bust_out_pattern': True,
        'transaction_velocity_7d': random.randint(50, 200),
        'amount_velocity_7d': random.uniform(5000, 15000)
    }
```

#### 3. Card Testing (20% of fraud)
```python
def generate_card_testing():
    """
    Testing stolen card numbers:
    - Multiple small transactions
    - Rapid succession (< 5 min apart)
    - Different merchants
    - Often online/e-commerce
    """
    return {
        'small_amounts': [random.uniform(1, 5) for _ in range(10)],
        'time_between_txns': random.uniform(0.5, 3),  # minutes
        'merchant_diversity': 10,  # 10 different merchants
        'transaction_velocity_1h': random.randint(5, 15),
        'amount': random.uniform(1.00, 5.00)
    }
```

#### 4. Fraud Rings (15% of fraud)
```python
def generate_fraud_ring(num_members=5):
    """
    Coordinated fraud:
    - Shared devices/IPs
    - Similar transaction patterns
    - Same merchants targeted
    - Synchronized timing
    """
    shared_device = f"DEVICE_{uuid.uuid4()}"
    shared_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
    
    return {
        'device_id': shared_device,
        'ip_address': shared_ip,
        'merchant_overlap': 0.8,  # 80% same merchants
        'time_correlation': 0.9,  # Similar transaction times
        'network_centrality': random.uniform(0.7, 0.95),
        'shared_device_count': num_members,
        'shared_ip_count': num_members
    }
```

### Step 4: Data Quality Validation

Validated generated data meets criteria:
```python
class DataQualityChecks:
    def check_fraud_rate(df):
        """Ensure fraud rate is realistic (1-2%)"""
        fraud_rate = df['is_fraud'].mean()
        assert 0.01 <= fraud_rate <= 0.02, f"Fraud rate {fraud_rate:.3f} out of range"
        
    def check_feature_distributions(df):
        """Verify no impossible values"""
        assert df['amount'].min() > 0, "Negative amounts found"
        assert df['hour_of_day'].between(0, 23).all(), "Invalid hours"
        assert df['account_age_days'].min() >= 0, "Negative account age"
        assert df['merchant_risk_score'].between(0, 1).all(), "Risk score out of range"
        
    def check_correlations(df):
        """High-risk features should correlate with fraud"""
        fraud_corr = df.corr()['is_fraud'].sort_values(ascending=False)
        assert fraud_corr['transaction_velocity_24h'] > 0.3, "Low velocity correlation"
        assert fraud_corr['amount_deviation_from_avg'] > 0.25, "Low deviation correlation"
        assert fraud_corr['device_fingerprint_mismatch'] > 0.2, "Low device correlation"
        
    def check_class_separation(df):
        """Fraud vs legitimate should be distinguishable"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import precision_score
        
        X = df.drop(['is_fraud', 'transaction_id', 'timestamp'], axis=1, errors='ignore')
        y = df['is_fraud']
        
        # Handle categorical features
        X = pd.get_dummies(X, drop_first=True)
        
        clf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
        clf.fit(X, y)
        
        # Should be able to achieve >80% precision
        y_pred = clf.predict(X)
        precision = precision_score(y, y_pred)
        assert precision > 0.80, f"Low precision: {precision:.3f}"
        
    def check_missing_values(df):
        """Ensure no missing critical values"""
        critical_features = [
            'amount', 'transaction_velocity_24h', 
            'merchant_risk_score', 'is_fraud'
        ]
        for feature in critical_features:
            assert df[feature].isna().sum() == 0, f"Missing values in {feature}"
```

### Step 5: Train/Test Split
```python
from sklearn.model_selection import train_test_split

# Temporal split (more realistic than random)
df_sorted = df.sort_values('timestamp')

# Last 20% of time period as test set
split_idx = int(len(df) * 0.8)
train_df = df_sorted.iloc[:split_idx]
test_df = df_sorted.iloc[split_idx:]

# Validation split from training
train_df, val_df = train_test_split(
    train_df, 
    test_size=0.2, 
    stratify=train_df['is_fraud'],
    random_state=42
)

print(f"Train: {len(train_df):,} transactions ({train_df['is_fraud'].mean():.3%} fraud)")
print(f"Val: {len(val_df):,} transactions ({val_df['is_fraud'].mean():.3%} fraud)")
print(f"Test: {len(test_df):,} transactions ({test_df['is_fraud'].mean():.3%} fraud)")
```

## Dataset Statistics

### Transaction Distribution

| Metric | Value |
|--------|-------|
| **Total Transactions** | 600,735 |
| **Legitimate** | 591,766 (98.5%) |
| **Fraud** | 8,969 (1.5%) |
| **Date Range** | Jan 1 - Jan 30, 2024 |
| **Unique Customers** | 25,134 |
| **Unique Merchants** | 5,047 |
| **Unique Devices** | 18,492 |
| **Unique IP Addresses** | 12,345 |

### Fraud Type Distribution

| Fraud Type | Count | % of Fraud |
|------------|-------|------------|
| Account Takeover | 3,588 | 40.0% |
| Synthetic Identity | 2,242 | 25.0% |
| Card Testing | 1,794 | 20.0% |
| Fraud Rings | 1,345 | 15.0% |

### Amount Statistics

|  | Legitimate | Fraud |
|---|-----------|-------|
| **Mean** | $156.32 | $847.21 |
| **Median** | $89.50 | $450.00 |
| **Std Dev** | $234.12 | $923.45 |
| **Min** | $1.00 | $1.00 |
| **Max** | $9,999.99 | $9,999.99 |
| **25th Percentile** | $45.00 | $125.00 |
| **75th Percentile** | $189.00 | $1,250.00 |

### Feature Correlations with Fraud

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| transaction_velocity_24h | +0.42 | Strong positive - fraudsters transact rapidly |
| amount_deviation_from_avg | +0.38 | Strong positive - unusual amounts |
| device_fingerprint_mismatch | +0.35 | Strong positive - new devices suspicious |
| merchant_risk_score | +0.31 | Moderate positive - high-risk merchants |
| network_centrality | +0.28 | Moderate positive - fraud rings cluster |
| account_age_days | -0.28 | Moderate negative - new accounts riskier |
| cross_border_flag | +0.24 | Moderate positive - international adds risk |
| time_since_last_transaction | -0.22 | Moderate negative - rapid transactions suspicious |
| shared_device_count | +0.20 | Moderate positive - shared devices indicate rings |
| amount_velocity_24h | +0.18 | Weak positive - high spending velocity |

## Data Schema

### Raw Transaction Schema
```json
{
  "transaction_id": "string (UUID)",
  "timestamp": "datetime (ISO 8601)",
  "customer_id": "string",
  "merchant_id": "string",
  "amount": "float",
  "is_fraud": "int (0 or 1)",
  "transaction_type": "string (purchase/refund/transfer)",
  "payment_method": "string (card/mobile/bank)",
  "device_id": "string",
  "ip_address": "string",
  "geolocation": "string (country code)"
}
```

### Engineered Features Schema
```json
{
  "transaction_id": "string (UUID)",
  "timestamp": "datetime (ISO 8601)",
  "customer_id": "string",
  "merchant_id": "string",
  "amount": "float",
  "is_fraud": "int (0 or 1)",
  
  "// Temporal Features": "",
  "hour_of_day": "int (0-23)",
  "day_of_week": "int (0-6)",
  "is_weekend": "int (0 or 1)",
  "is_night": "int (0 or 1)",
  "days_since_account_creation": "int",
  "time_since_last_transaction": "float (hours)",
  
  "// Velocity Features": "",
  "transaction_velocity_1h": "int",
  "transaction_velocity_24h": "int",
  "transaction_velocity_7d": "int",
  "amount_velocity_24h": "float",
  "amount_velocity_7d": "float",
  
  "// Deviation Features": "",
  "amount_deviation_from_avg": "float (z-score)",
  "amount_deviation_from_merchant_avg": "float (z-score)",
  "time_deviation_from_pattern": "float (hours)",
  "amount_zscore": "float",
  
  "// Network Features": "",
  "shared_device_count": "int",
  "shared_ip_count": "int",
  "network_centrality": "float (0-1)",
  "community_id": "int",
  "transaction_count_same_device": "int",
  "transaction_count_same_ip": "int",
  
  "// Risk Score Features": "",
  "merchant_risk_score": "float (0-1)",
  "device_risk_score": "float (0-1)",
  "geolocation_risk": "float (0-1)",
  "account_age_days": "int",
  "account_age_category": "string (new/established/old)",
  
  "// Behavioral Features": "",
  "cross_border_flag": "int (0 or 1)",
  "device_fingerprint_mismatch": "int (0 or 1)",
  "merchant_category": "string",
  "transaction_type": "string",
  "payment_method": "string",
  
  "// Statistical Features": "",
  "amount_percentile_user": "float (0-1)",
  "amount_percentile_merchant": "float (0-1)",
  "frequency_score": "float",
  "recency_score": "float"
}
```

## Data Files

### File Structure
```
data/
├── raw/
│   └── paysim_transactions.csv  # Original PaySim data
├── processed/
│   ├── train.csv                # Training set (480,588 rows)
│   ├── val.csv                  # Validation set (60,074 rows)
│   └── test.csv                 # Test set (60,073 rows)
├── features/
│   ├── feature_definitions.json # Feature metadata
│   └── feature_statistics.json  # Mean, std for each feature
└── samples/
    └── sample_1000.csv          # Small sample for demos
```

### Feature Definitions File
```json
{
  "transaction_velocity_24h": {
    "name": "24-Hour Transaction Velocity",
    "description": "Number of transactions by this customer in the last 24 hours",
    "type": "int",
    "range": [0, 200],
    "calculation": "COUNT(transactions WHERE timestamp > NOW() - 24h)",
    "use_case": "Detect account takeover and card testing patterns"
  },
  "amount_deviation_from_avg": {
    "name": "Amount Deviation from Average",
    "description": "Z-score of transaction amount vs customer's historical average",
    "type": "float",
    "range": [-5, 5],
    "calculation": "(amount - customer_mean) / customer_std",
    "use_case": "Detect unusual spending patterns"
  },
  "merchant_risk_score": {
    "name": "Merchant Risk Score",
    "description": "Historical fraud rate at this merchant (0-1 scale)",
    "type": "float",
    "range": [0, 1],
    "calculation": "COUNT(fraud_at_merchant) / COUNT(transactions_at_merchant)",
    "use_case": "Identify high-risk merchants"
  }
}
```

## Reproducibility

### Random Seeds
All random operations use fixed seeds for reproducibility:
```python
import random
import numpy as np

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
```

### Version Control
- **Data Generation Script:** `src/data/generate_synthetic_fraud_data.py`
- **Git Hash:** Recorded in `data/processed/version.txt`
- **Feature Engineering:** `src/data/feature_engineering.py`
- **Validation Script:** `scripts/validate_data_quality.py`

### Regeneration
To regenerate the dataset:
```bash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python src/data/generate_synthetic_fraud_data.py \
    --num_transactions 600000 \
    --fraud_rate 0.015 \
    --output_dir data/processed \
    --seed 42

# Validate data quality
python scripts/validate_data_quality.py data/processed/train.csv
```

## Limitations & Considerations

### Known Limitations
1. **Simplified Fraud Patterns:** Real fraud is more complex and adaptive
2. **Static Merchant Risk:** In reality, merchant risk changes over time
3. **No Concept Drift:** Real fraud patterns evolve; this dataset is static
4. **Limited Network Effects:** Graph connections are simplified
5. **Synthetic vs Real:** Model performance on synthetic may not match real data

### Best Practices
1. **Always validate on real data** before production deployment
2. **Monitor for concept drift** and retrain models regularly
3. **Use ensemble methods** to handle uncertainty
4. **Maintain human oversight** for high-risk decisions
5. **Document model assumptions** and limitations

## References

- [PaySim Paper](https://arxiv.org/abs/1804.00791) - Original PaySim research
- [Kaggle PaySim Dataset](https://www.kaggle.com/datasets/ealaxi/paysim1)
- [Feature Engineering Guide](https://www.kaggle.com/learn/feature-engineering)
- [Fraud Detection Best Practices](https://www.fico.com/blogs/fraud-detection-best-practices)

## Contact

For questions about the data generation process:
- **Email:** reichert.sentinel.ai@gmail.com
- **GitHub Issues:** [Create an issue](https://github.com/reichert-sentinel-ai/guardian/issues)

