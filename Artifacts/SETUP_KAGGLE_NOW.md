# Kaggle API Setup - Quick Guide

## 🚀 Steps to Configure (Takes 2 minutes)

### Step 1: Get Your Kaggle Token

1. **Go to**: https://www.kaggle.com/settings
2. **Scroll down** to "API" section  
3. **Click** "Create New Token" button
4. Your browser will download `kaggle.json`

### Step 2: Place the Token

**Option A: Using PowerShell (Easiest)**
```powershell
# After downloading kaggle.json, run this:
cd project\repo-guardian
.\scripts\setup_kaggle.ps1 -KaggleJson "$env:USERPROFILE\Downloads\kaggle.json"
```

**Option B: Manual Copy**
```powershell
# Copy the downloaded kaggle.json to:
Copy-Item "$env:USERPROFILE\Downloads\kaggle.json" "$env:USERPROFILE\.kaggle\kaggle.json"
```

### Step 3: Verify Setup

```powershell
# Test if it works
python -c "import kaggle; print('✓ Kaggle API configured successfully!')"
```

### Step 4: Run Chat 1

```powershell
cd project\repo-guardian
python scripts\run_chat1.py
```

---

## 📊 What Will Happen

Once configured, Chat 1 will:
- ✅ Download PaySim dataset (~6.4M transactions, ~500MB)
- ✅ Download Credit Card Fraud dataset (~285K transactions, ~140MB)  
- ✅ Engineer 95+ features
- ✅ Create train/test splits
- ⏱️ Estimated time: 10-20 minutes (depending on internet speed)

---

## 🔧 Troubleshooting

**"Could not find kaggle.json"**
- Make sure file is at: `C:\Users\reich\.kaggle\kaggle.json`
- Check file name is exactly `kaggle.json` (not `kaggle (1).json`)

**"Invalid credentials"**
- Re-download token from Kaggle (tokens can expire)
- Make sure you're logged into Kaggle when creating token

**Download fails**
- Check internet connection
- Ensure you've accepted dataset terms on Kaggle website
- Some datasets require clicking "I Understand and Accept" on Kaggle

---

**Ready?** Once you've placed kaggle.json, let me know and I'll run Chat 1! 🚀

