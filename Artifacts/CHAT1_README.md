# Chat 1: Guardian Data Acquisition - Quick Start

This guide helps you execute Chat 1: Data Acquisition for the Guardian fraud detection system.

## Prerequisites

1. **Python 3.11+** installed
2. **Kaggle API credentials** configured
3. **Dependencies** installed

## Setup

### 1. Install Dependencies

```bash
cd project/repo-guardian
pip install -r requirements.txt
```

### 2. Configure Kaggle API

1. Go to https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New Token"
4. Download `kaggle.json`

**Windows:**
```powershell
# Create directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.kaggle"

# Copy kaggle.json to .kaggle directory
Copy-Item path\to\kaggle.json "$env:USERPROFILE\.kaggle\kaggle.json"
```

**Mac/Linux:**
```bash
# Create directory
mkdir -p ~/.kaggle

# Copy kaggle.json
cp ~/Downloads/kaggle.json ~/.kaggle/kaggle.json

# Set permissions
chmod 600 ~/.kaggle/kaggle.json
```

### 3. Test Kaggle Authentication

```bash
kaggle datasets list | Select-String "paysim"  # Windows PowerShell
# or
kaggle datasets list | grep paysim  # Mac/Linux
```

## Execution

### Option 1: Run Complete Pipeline

```bash
cd project/repo-guardian
python scripts/run_chat1.py
```

This will:
1. Download PaySim dataset (6.4M transactions)
2. Download Credit Card Fraud dataset (285K transactions)
3. Engineer 95+ features
4. Create train/test splits (80/20)
5. Save all processed data to `data/processed/`

### Option 2: Run Individual Steps

```bash
# Step 1: Download datasets
python src/data/loader.py

# Step 2: Engineer features
python src/data/feature_engineering.py

# Step 3: Create train/test split
python src/data/train_test_split.py
```

## Expected Outputs

After successful execution, you should have:

```
project/repo-guardian/
├── data/
│   ├── raw/
│   │   └── guardian/
│   │       ├── PS_20174392719_1491204439457_log.csv
│   │       └── creditcard.csv
│   └── processed/
│       ├── raw_paysim.csv
│       ├── raw_credit_card.csv
│       ├── combined_features.csv
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
```

## Troubleshooting

### Kaggle Authentication Issues

If you see "401 Unauthorized" errors:

1. Verify `kaggle.json` is in the correct location:
   - Windows: `C:\Users\%USERNAME%\.kaggle\kaggle.json`
   - Mac/Linux: `~/.kaggle/kaggle.json`

2. Check file permissions (Linux/Mac):
   ```bash
   chmod 600 ~/.kaggle/kaggle.json
   ```

3. Verify API token is not expired - download a new one from Kaggle settings

### Memory Issues

If you encounter memory errors:

1. Process datasets in smaller chunks
2. Consider using Dask for large dataframes
3. Ensure you have at least 8GB RAM available

### Download Timeouts

If downloads timeout:

1. Check internet connection
2. Try downloading during off-peak hours
3. Download datasets manually from Kaggle website and place in `data/raw/guardian/`

## Next Steps

Once Chat 1 is complete:

- ✅ Datasets downloaded and saved
- ✅ Features engineered (95+ features)
- ✅ Train/test splits created
- ✅ Ready for Chat 2: Model Training

## Success Criteria

- [x] PaySim downloaded (6.4M transactions)
- [x] Credit Card downloaded (285K transactions)
- [x] 95+ features engineered
- [x] Train/test split created (80/20)
- [x] All files saved to `data/processed/`

---

**Questions?** See `CHAT_1_IMPLEMENTATION_GUIDE.md` for detailed documentation.

