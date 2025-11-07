# Install and Run Chat 1 - Simple Instructions

## Step 1: Install Dependencies

Open PowerShell and run:

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-guardian
python -m pip install kaggle pandas numpy scikit-learn xgboost shap fastapi uvicorn python-dotenv
```

## Step 2: Configure Kaggle API

1. Go to: https://www.kaggle.com/settings
2. Click "Create New Token" in the API section
3. Download the `kaggle.json` file
4. Create directory: `mkdir C:\Users\reich\.kaggle`
5. Move `kaggle.json` to: `C:\Users\reich\.kaggle\kaggle.json`

Verify:
```powershell
Test-Path C:\Users\reich\.kaggle\kaggle.json
```

## Step 3: Run Chat 1

```powershell
python scripts\run_chat1.py
```

## What You'll See

```
Starting Chat 1: Data Acquisition...
Downloading PaySim dataset...
PaySim loaded: 6,362,620 transactions
Downloading Credit Card Fraud dataset...
Credit Card Fraud loaded: 284,807 transactions
Engineering PaySim features...
Engineering Credit Card features...
Combining datasets...
Creating train/test split...
Chat 1 Complete!
Ready for Chat 2: Model Training
Training samples: X,XXX,XXX
Test samples: X,XXX,XXX
```

## Output Files

After successful completion, you'll have:

```
data/
  raw/
    guardian/
      PS_20174392719_1491204439457_log.csv  (6.4M transactions)
      creditcard.csv                         (285K transactions)
  processed/
    raw_paysim.csv
    raw_credit_card.csv
    combined_features.csv
    X_train.csv, X_test.csv
    y_train.csv, y_test.csv
```

## Troubleshooting

**"No module named 'kaggle'"**  
→ Run: `python -m pip install kaggle`

**"401 Unauthorized"**  
→ Download new token from https://www.kaggle.com/settings

**"Memory Error"**  
→ Close other applications, ensure 8GB+ RAM

---

**Ready? Run:** `python scripts\run_chat1.py`

