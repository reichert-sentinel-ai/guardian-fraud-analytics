# Quick Chat 1 Status Check
# Run this anytime to check progress

Write-Host "=== Chat 1 Status Check ===" -ForegroundColor Cyan
Write-Host ""

# Check job status
$jobs = Get-Job Chat1Run -ErrorAction SilentlyContinue

if ($jobs) {
    $running = $jobs | Where-Object { $_.State -eq "Running" }
    $completed = $jobs | Where-Object { $_.State -eq "Completed" }
    $failed = $jobs | Where-Object { $_.State -eq "Failed" }
    
    if ($running) {
        Write-Host "✓ Job Status: RUNNING" -ForegroundColor Green
        $running | Format-Table Id, Name, State, HasMoreData
        Write-Host ""
        Write-Host "Recent Output:" -ForegroundColor Yellow
        Get-Job Chat1Run | Where-Object { $_.State -eq "Running" } | Receive-Job -Keep | Select-Object -Last 10
    }
    
    if ($completed) {
        Write-Host ""
        Write-Host "🎉 Job Status: COMPLETED! 🎉" -ForegroundColor Green -BackgroundColor Black
        Write-Host ""
        Write-Host "Final Output:" -ForegroundColor Cyan
        Get-Job Chat1Run | Where-Object { $_.State -eq "Completed" } | Receive-Job -Keep | Select-Object -Last 30
    }
    
    if ($failed) {
        Write-Host ""
        Write-Host "❌ Job Status: FAILED" -ForegroundColor Red
        Write-Host ""
        Write-Host "Error Output:" -ForegroundColor Red
        Get-Job Chat1Run | Where-Object { $_.State -eq "Failed" } | Receive-Job -Keep
    }
} else {
    Write-Host "⚠ No Chat1Run job found." -ForegroundColor Yellow
    Write-Host "It may have completed or been removed." -ForegroundColor Gray
}

Write-Host ""
Write-Host "─────────────────────────────────────" -ForegroundColor Gray
Write-Host "Current Processed Files:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────" -ForegroundColor Gray

$files = Get-ChildItem data\processed\*.csv -ErrorAction SilentlyContinue | 
    Where-Object { $_.Name -notlike "sample_*" } |
    Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB, 2)}}, LastWriteTime |
    Sort-Object LastWriteTime -Descending

if ($files) {
    $files | Format-Table -AutoSize
    
    # Check for expected completion files
    $expectedFiles = @("combined_features.csv", "X_train.csv", "X_test.csv", "y_train.csv", "y_test.csv")
    $existingFiles = $files.Name
    
    Write-Host ""
    Write-Host "Completion Status:" -ForegroundColor Cyan
    foreach ($file in $expectedFiles) {
        if ($existingFiles -contains $file) {
            Write-Host "  ✓ $file" -ForegroundColor Green
        } else {
            Write-Host "  ⏳ $file (not yet created)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "No processed files found yet." -ForegroundColor Yellow
}

Write-Host ""

