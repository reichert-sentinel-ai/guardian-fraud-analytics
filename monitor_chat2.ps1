# Chat 2 Status Monitor - Checks every 30 minutes
# Run this script to monitor Chat 2 progress

param(
    [int]$CheckIntervalMinutes = 30
)

$repoPath = "C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-guardian"
$modelsPath = Join-Path $repoPath "models"
$reportsPath = Join-Path $repoPath "reports"
$visualizationsPath = Join-Path $repoPath "visualizations"
$logsPath = $repoPath

Write-Host "=" * 70
Write-Host "Chat 2: Model Training - Status Monitor"
Write-Host "=" * 70
Write-Host "Checking every $CheckIntervalMinutes minutes..."
Write-Host "Press Ctrl+C to stop monitoring"
Write-Host "=" * 70
Write-Host ""

$iteration = 0
$lastStatus = ""

while ($true) {
    $iteration++
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    Write-Host "`n[$timestamp] Check #$iteration" -ForegroundColor Cyan
    Write-Host "-" * 70
    
    # Check for model file
    $modelFiles = Get-ChildItem -Path $modelsPath -Filter "xgboost_fraud_*.pkl" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    $modelExists = $modelFiles.Count -gt 0
    
    # Check for report file
    $reportFiles = Get-ChildItem -Path $reportsPath -Filter "xgboost_fraud_evaluation_*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    $reportExists = $reportFiles.Count -gt 0
    
    # Check for visualizations
    $vizFiles = Get-ChildItem -Path $visualizationsPath -Filter "*.png" -ErrorAction SilentlyContinue
    $vizCount = $vizFiles.Count
    
    # Check for log files
    $logFiles = Get-ChildItem -Path $logsPath -Filter "chat2_training_*.log" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    $latestLog = $logFiles | Select-Object -First 1
    
    # Check Python processes
    $chat2Processes = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.StartTime -gt (Get-Date).AddHours(-2) }
    $processRunning = $chat2Processes.Count -gt 0
    
    # Display status
    Write-Host "📊 Status Summary:" -ForegroundColor Yellow
    
    if ($modelExists) {
        $model = $modelFiles | Select-Object -First 1
        $size = [math]::Round($model.Length / 1MB, 2)
        Write-Host "  ✅ Model: $($model.Name) ($size MB)" -ForegroundColor Green
        Write-Host "     Last Modified: $($model.LastWriteTime)" -ForegroundColor Gray
    } else {
        Write-Host "  ⏳ Model: Not yet created" -ForegroundColor Yellow
    }
    
    if ($reportExists) {
        $report = $reportFiles | Select-Object -First 1
        Write-Host "  ✅ Report: $($report.Name)" -ForegroundColor Green
    } else {
        Write-Host "  ⏳ Report: Not yet created" -ForegroundColor Yellow
    }
    
    Write-Host "  📊 Visualizations: $vizCount/3 files" -ForegroundColor $(if ($vizCount -eq 3) { "Green" } else { "Yellow" })
    if ($vizFiles.Count -gt 0) {
        foreach ($viz in $vizFiles) {
            Write-Host "     - $($viz.Name)" -ForegroundColor Gray
        }
    }
    
    if ($latestLog) {
        $logSize = [math]::Round($latestLog.Length / 1KB, 2)
        Write-Host "  📝 Log: $($latestLog.Name) ($logSize KB)" -ForegroundColor Cyan
        Write-Host "     Last Modified: $($latestLog.LastWriteTime)" -ForegroundColor Gray
        
        # Show last few lines of log
        try {
            $lastLines = Get-Content $latestLog.FullName -Tail 3 -ErrorAction SilentlyContinue
            if ($lastLines) {
                Write-Host "     Recent output:" -ForegroundColor Gray
                $lastLines | ForEach-Object { Write-Host "        $_" -ForegroundColor DarkGray }
            }
        } catch {
            # Ignore errors reading log
        }
    } else {
        Write-Host "  ⏳ Log: Not yet created" -ForegroundColor Yellow
    }
    
    Write-Host "  🔄 Process: $(if ($processRunning) { 'Running' } else { 'Not detected' })" -ForegroundColor $(if ($processRunning) { "Green" } else { "Yellow" })
    if ($processRunning) {
        $totalMemory = ($chat2Processes | Measure-Object -Property WorkingSet64 -Sum).Sum / 1GB
        Write-Host "     Memory Usage: $([math]::Round($totalMemory, 2)) GB" -ForegroundColor Gray
    }
    
    # Determine completion status
    if ($modelExists -and $reportExists -and $vizCount -eq 3) {
        Write-Host "`n🎉 CHAT 2 COMPLETE!" -ForegroundColor Green
        Write-Host "=" * 70
        
        # Show performance metrics if report exists
        if ($reportExists) {
            try {
                $reportPath = ($reportFiles | Select-Object -First 1).FullName
                $reportContent = Get-Content $reportPath | ConvertFrom-Json -ErrorAction SilentlyContinue
                if ($reportContent) {
                    Write-Host "`n📊 Performance Metrics:" -ForegroundColor Yellow
                    Write-Host "   Accuracy:  $([math]::Round($reportContent.accuracy * 100, 2))%" -ForegroundColor $(if ($reportContent.accuracy -ge 0.92) { "Green" } else { "Yellow" })
                    Write-Host "   Precision: $([math]::Round($reportContent.precision, 4))" -ForegroundColor White
                    Write-Host "   Recall:    $([math]::Round($reportContent.recall, 4))" -ForegroundColor White
                    Write-Host "   F1 Score:  $([math]::Round($reportContent.f1_score, 4))" -ForegroundColor White
                    Write-Host "   AUC-ROC:   $([math]::Round($reportContent.auc_roc, 4))" -ForegroundColor $(if ($reportContent.auc_roc -ge 0.95) { "Green" } else { "Yellow" })
                    
                    if ($reportContent.accuracy -ge 0.92 -and $reportContent.auc_roc -ge 0.95) {
                        Write-Host "`n✅ All success criteria met!" -ForegroundColor Green
                    } else {
                        Write-Host "`n⚠️  Some criteria not met - check report for details" -ForegroundColor Yellow
                    }
                }
            } catch {
                Write-Host "   (Could not parse report JSON)" -ForegroundColor Gray
            }
        }
        
        Write-Host "`n✅ Chat 2 has completed successfully!" -ForegroundColor Green
        Write-Host "📁 Output files are ready in:" -ForegroundColor Cyan
        Write-Host "   - Models: $modelsPath" -ForegroundColor White
        Write-Host "   - Reports: $reportsPath" -ForegroundColor White
        Write-Host "   - Visualizations: $visualizationsPath" -ForegroundColor White
        Write-Host "`n🎯 Ready for Chat 3: FastAPI Backend" -ForegroundColor Green
        
        break
    } elseif ($processRunning -or $latestLog) {
        $currentStatus = "In Progress"
        if ($currentStatus -ne $lastStatus) {
            Write-Host "`n🟢 Status: $currentStatus" -ForegroundColor Green
            $lastStatus = $currentStatus
        }
    } else {
        Write-Host "`n⏳ Status: Waiting to start or checking..." -ForegroundColor Yellow
    }
    
    # Wait before next check
    Write-Host "`n⏱️  Next check in $CheckIntervalMinutes minutes..." -ForegroundColor Cyan
    Write-Host "   (Press Ctrl+C to stop monitoring)" -ForegroundColor DarkGray
    Start-Sleep -Seconds ($CheckIntervalMinutes * 60)
}

Write-Host "`nMonitoring stopped." -ForegroundColor Yellow

