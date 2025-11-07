# Quick Setup Guide for Chat 1

## Fastest Way to Get Started

### Option 1: Manual Setup (Recommended)

```powershell
# 1. Install dependencies
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-guardian
python -m pip install kaggle pandas numpy scikit-learn xgboost shap fastapi uvicorn python-dotenv

# 2. Configure Kaggle API
# - Go to https://www.kaggle.com/settings
# - Click "Create New Token"
# - Download kaggle.json
# - Place in: C:\Users\reich\.kaggle\kaggle.json

# 3. Run the pipeline
python scripts\run_chat1.py
```

### Option 2: Verify Each Step

```powershell
# Check Python
python --version

# Check if packages are installed
python -c "import kaggle, pandas, numpy, sklearn, xgboost; print('All packages installed')"

# Check Kaggle credentials
Test-Path "$env:USERPROFILE\.kaggle\kaggle.json"
```

## What Will Happen

When you run `python scripts\run_chat1.py`, it will:

1. ✅ Download PaySim dataset (6.4M transactions) → `data/raw/guardian/`
2. ✅ Download Credit Card Fraud dataset (285K transactions) → `data/raw/guardian/`
3. ✅ Engineer 95+ features
4. ✅ Create train/test splits (80/20)
5. ✅ Save all processed data to `data/processed/`

## Expected Runtime

- **First run:** 10-30 minutes (downloading ~500MB of data)
- **Subsequent runs:** 2-5 minutes (skips download if files exist)

## Troubleshooting

### "No module named 'kaggle'"
```powershell
python -m pip install kaggle
```

### "401 Unauthorized"
- Re-download kaggle.json from https://www.kaggle.com/settings
- Ensure it's in: `C:\Users\reich\.kaggle\kaggle.json`

### "Memory Error"
- Close other applications
- Ensure 8GB+ RAM available

## Success Criteria

✅ All files created in `data/processed/`:
- `raw_paysim.csv`
- `raw_credit_card.csv`
- `combined_features.csv`
- `X_train.csv`, `X_test.csv`
- `y_train.csv`, `y_test.csv`

✅ Ready for Chat 2: Model Training

