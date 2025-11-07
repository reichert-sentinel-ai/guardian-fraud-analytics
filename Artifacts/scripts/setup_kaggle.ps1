# Kaggle API Setup Helper Script
# This script helps configure Kaggle API credentials

Write-Host "=== Kaggle API Setup ===" -ForegroundColor Cyan
Write-Host ""

$kaggleDir = "$env:USERPROFILE\.kaggle"
$kaggleFile = "$kaggleDir\kaggle.json"

# Check if kaggle.json already exists
if (Test-Path $kaggleFile) {
    Write-Host "✓ Kaggle credentials already configured!" -ForegroundColor Green
    Write-Host "Location: $kaggleFile"
    Write-Host ""
    Write-Host "Testing Kaggle API..." -ForegroundColor Yellow
    
    python -c "import kaggle; print('Kaggle API is working!')" 2>&1
    exit 0
}

# Create directory if it doesn't exist
if (-not (Test-Path $kaggleDir)) {
    Write-Host "Creating Kaggle directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $kaggleDir | Out-Null
    Write-Host "✓ Created: $kaggleDir" -ForegroundColor Green
}

Write-Host "Kaggle credentials NOT found." -ForegroundColor Yellow
Write-Host ""
Write-Host "To set up Kaggle API:" -ForegroundColor Cyan
Write-Host "1. Visit: https://www.kaggle.com/settings" -ForegroundColor White
Write-Host "2. Scroll to 'API' section" -ForegroundColor White
Write-Host "3. Click 'Create New Token'" -ForegroundColor White
Write-Host "4. Download kaggle.json" -ForegroundColor White
Write-Host ""
Write-Host "Once downloaded, run this script again with the file:" -ForegroundColor Cyan
Write-Host "  .\scripts\setup_kaggle.ps1 -KaggleJson 'path\to\kaggle.json'" -ForegroundColor White
Write-Host ""
Write-Host "Or manually copy it to: $kaggleFile" -ForegroundColor White
Write-Host ""

# Check if kaggle.json was provided as parameter
param(
    [string]$KaggleJson
)

if ($KaggleJson -and (Test-Path $KaggleJson)) {
    Write-Host "Copying $KaggleJson to $kaggleFile..." -ForegroundColor Yellow
    Copy-Item -Path $KaggleJson -Destination $kaggleFile -Force
    Write-Host "✓ Kaggle credentials configured!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Testing Kaggle API..." -ForegroundColor Yellow
    
    $result = python -c "import kaggle; print('Kaggle API is working!')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Kaggle API is ready!" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can now run Chat 1:" -ForegroundColor Cyan
        Write-Host "  python scripts\run_chat1.py" -ForegroundColor White
    } else {
        Write-Host "⚠ There may be an issue with your credentials. Check the error above." -ForegroundColor Yellow
    }
}

