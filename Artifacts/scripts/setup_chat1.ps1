# Chat 1 Setup Script
# Automates installation of dependencies and configuration

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Chat 1: Guardian Data Acquisition - Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python version
Write-Host "[1/4] Checking Python version..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "⚠ Warning: Python 3.11+ recommended" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Install dependencies
Write-Host "[2/4] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

$packages = @(
    "kaggle",
    "pandas",
    "numpy",
    "scikit-learn",
    "xgboost",
    "shap",
    "fastapi",
    "uvicorn",
    "python-dotenv"
)

$installed = 0
$failed = 0

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    $null = python -m pip install $package 2>&1
    if ($LASTEXITCODE -eq 0) {
        $installed++
        Write-Host "  ✓ $package installed" -ForegroundColor Green
    } else {
        $failed++
        Write-Host "  ✗ Failed to install $package" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✓ Installed: $installed/$($packages.Count) packages" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "✗ Failed: $failed packages" -ForegroundColor Red
}
Write-Host ""

# Step 3: Check Kaggle API configuration
Write-Host "[3/4] Checking Kaggle API configuration..." -ForegroundColor Yellow

$kagglePath = "$env:USERPROFILE\.kaggle"
$kaggleJson = "$kagglePath\kaggle.json"

if (Test-Path $kaggleJson) {
    Write-Host "✓ Kaggle API credentials found" -ForegroundColor Green
    $kaggleConfigured = $true
} else {
    Write-Host "✗ Kaggle API credentials NOT found" -ForegroundColor Red
    Write-Host ""
    Write-Host "To configure Kaggle API:" -ForegroundColor Yellow
    Write-Host "  1. Go to: https://www.kaggle.com/settings" -ForegroundColor White
    Write-Host "  2. Click 'Create New Token' in the API section" -ForegroundColor White
    Write-Host "  3. Download kaggle.json" -ForegroundColor White
    Write-Host "  4. Place it in: $kaggleJson" -ForegroundColor White
    Write-Host ""
    
    # Offer to create directory
    if (-not (Test-Path $kagglePath)) {
        $createDir = Read-Host "Create .kaggle directory? (Y/N)"
        if ($createDir -eq "Y" -or $createDir -eq "y") {
            New-Item -ItemType Directory -Force -Path $kagglePath | Out-Null
            Write-Host "✓ Directory created: $kagglePath" -ForegroundColor Green
        }
    }
    
    $kaggleConfigured = $false
}
Write-Host ""

# Step 4: Verify installations
Write-Host "[4/4] Verifying installations..." -ForegroundColor Yellow

$missingModules = @()

$modules = @("kaggle", "pandas", "numpy", "sklearn", "xgboost")
foreach ($module in $modules) {
    $result = python -c "import $module" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $module" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $module" -ForegroundColor Red
        $missingModules += $module
    }
}
Write-Host ""

# Summary
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Setup Summary" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

$allGood = $true

# Check Python
Write-Host "Python: " -NoNewline
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Not found" -ForegroundColor Red
    $allGood = $false
}

# Check dependencies
Write-Host "Dependencies: " -NoNewline
if ($missingModules.Count -eq 0) {
    Write-Host "✓ All installed" -ForegroundColor Green
} else {
    Write-Host "✗ Missing: $($missingModules -join ', ')" -ForegroundColor Red
    $allGood = $false
}

# Check Kaggle
Write-Host "Kaggle API: " -NoNewline
if ($kaggleConfigured) {
    Write-Host "✓ Configured" -ForegroundColor Green
} else {
    Write-Host "✗ Not configured" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

if ($allGood) {
    Write-Host "✓ Setup complete! Ready to run Chat 1." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next step:" -ForegroundColor Yellow
    Write-Host "  python scripts\run_chat1.py" -ForegroundColor White
} else {
    Write-Host "⚠ Setup incomplete. Please address the issues above." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "See RUN_CHAT1_STATUS.md for detailed instructions." -ForegroundColor Gray
}

Write-Host ""
