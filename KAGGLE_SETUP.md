# Kaggle API Setup Guide

Quick guide to configure Kaggle API for Chat 1 dataset downloads.

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Get Kaggle API Token

1. **Visit**: https://www.kaggle.com/settings
2. **Scroll** to "API" section
3. **Click** "Create New Token"
4. **Download** `kaggle.json` file

### Step 2: Place Token File

**Option A: Using PowerShell Script (Easiest)**
```powershell
cd project\repo-guardian
.\scripts\setup_kaggle.ps1 -KaggleJson "C:\Users\reich\Downloads\kaggle.json"
```

**Option B: Manual Copy**
```powershell
# Create directory (if needed)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.kaggle"

# Copy kaggle.json to:
# C:\Users\reich\.kaggle\kaggle.json
```

### Step 3: Verify

```powershell
# Run setup script to verify
.\scripts\setup_kaggle.ps1

# Or test directly
python -c "import kaggle; print('OK')"
```

---

## ✅ Verify Setup

After setup, verify it works:

```powershell
# Test Kaggle API
python -c "import kaggle; kaggle.api.datasets_list(search='paysim')"
```

If you see dataset listings, you're all set! ✅

---

## 🚀 Run Chat 1

Once configured, run Chat 1:

```powershell
cd project\repo-guardian
python scripts\run_chat1.py
```

---

## 🔧 Troubleshooting

### "Could not find kaggle.json"
- Ensure file is at: `C:\Users\reich\.kaggle\kaggle.json`
- Check file name is exactly `kaggle.json` (not `kaggle.json.json`)

### "Invalid credentials"
- Re-download token from Kaggle settings
- Ensure token hasn't expired
- Check JSON file is valid (opened in text editor)

### Import Error
- Ensure kaggle package is installed: `python -m pip install kaggle`

---

**Ready?** Once configured, Chat 1 will automatically download:
- PaySim dataset (6.4M transactions)
- Credit Card Fraud dataset (285K transactions)

