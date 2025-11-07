# Quick Kaggle Configuration Script
# Run this after downloading kaggle.json from https://www.kaggle.com/settings

param(
    [string]$KaggleJsonPath = ""
)

$kaggleDir = "$env:USERPROFILE\.kaggle"
$kaggleFile = "$kaggleDir\kaggle.json"

Write-Host "=== Kaggle API Configuration ===" -ForegroundColor Cyan
Write-Host ""

# Check if already configured
if (Test-Path $kaggleFile) {
    Write-Host "✓ Kaggle credentials already configured!" -ForegroundColor Green
    Write-Host "Location: $kaggleFile"
    Write-Host ""
    
    # Test it
    Write-Host "Testing Kaggle API..." -ForegroundColor Yellow
    python -c "import kaggle; print('✓ Kaggle API is working!')" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Everything is ready!" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can now run Chat 1:" -ForegroundColor Cyan
        Write-Host "  cd project\repo-guardian" -ForegroundColor White
        Write-Host "  python scripts\run_chat1.py" -ForegroundColor White
    }
    exit 0
}

# Find kaggle.json if not provided
if ([string]::IsNullOrEmpty($KaggleJsonPath)) {
    Write-Host "Searching for kaggle.json..." -ForegroundColor Yellow
    
    # Check common locations
    $possibleLocations = @(
        "$env:USERPROFILE\Downloads\kaggle.json",
        "$env:USERPROFILE\Desktop\kaggle.json",
        "$PWD\kaggle.json"
    )
    
    foreach ($loc in $possibleLocations) {
        if (Test-Path $loc) {
            $KaggleJsonPath = $loc
            Write-Host "Found: $loc" -ForegroundColor Green
            break
        }
    }
}

# If still not found, ask user
if ([string]::IsNullOrEmpty($KaggleJsonPath)) {
    Write-Host ""
    Write-Host "⚠ kaggle.json not found automatically." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please either:" -ForegroundColor Cyan
    Write-Host "1. Run this script with the path:" -ForegroundColor White
    Write-Host "   .\configure_kaggle.ps1 -KaggleJsonPath 'C:\path\to\kaggle.json'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Download kaggle.json from: https://www.kaggle.com/settings" -ForegroundColor White
    Write-Host "   Then run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Manually copy kaggle.json to: $kaggleFile" -ForegroundColor White
    exit 1
}

# Copy the file
Write-Host ""
Write-Host "Configuring Kaggle API..." -ForegroundColor Yellow

# Create directory if needed
if (-not (Test-Path $kaggleDir)) {
    New-Item -ItemType Directory -Force -Path $kaggleDir | Out-Null
    Write-Host "Created directory: $kaggleDir" -ForegroundColor Green
}

# Copy file
Copy-Item -Path $KaggleJsonPath -Destination $kaggleFile -Force
Write-Host "✓ Copied kaggle.json to: $kaggleFile" -ForegroundColor Green

# Verify
Write-Host ""
Write-Host "Testing Kaggle API..." -ForegroundColor Yellow
$testResult = python -c "import kaggle; print('✓ Kaggle API is working!')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Kaggle API configured successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ready to run Chat 1:" -ForegroundColor Cyan
    Write-Host "  cd project\repo-guardian" -ForegroundColor White
    Write-Host "  python scripts\run_chat1.py" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "⚠ There may be an issue with your credentials:" -ForegroundColor Yellow
    Write-Host $testResult
    Write-Host ""
    Write-Host "Please check:" -ForegroundColor Cyan
    Write-Host "  - Token was downloaded recently (not expired)" -ForegroundColor White
    Write-Host "  - You're logged into Kaggle when creating token" -ForegroundColor White
    Write-Host "  - Token file is valid JSON" -ForegroundColor White
}

