# Chat 1 Completion Monitor
# This script monitors the Chat1Run job and notifies when complete

Write-Host "=== Chat 1 Completion Monitor ===" -ForegroundColor Cyan
Write-Host ""

$jobName = "Chat1Run"
$checkInterval = 10  # Check every 10 seconds
$maxWaitTime = 3600  # Maximum 60 minutes

$startTime = Get-Date
$elapsedTime = 0

# Find the job
$job = Get-Job -Name $jobName -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Running" } | Select-Object -First 1

if (-not $job) {
    Write-Host "⚠ No running Chat1Run job found." -ForegroundColor Yellow
    Write-Host "Checking all jobs..." -ForegroundColor Cyan
    Get-Job | Format-Table Id, Name, State, HasMoreData
    exit 1
}

Write-Host "✓ Found running job: $($job.Name) (ID: $($job.Id))" -ForegroundColor Green
Write-Host "Monitoring for completion..." -ForegroundColor Yellow
Write-Host "Check interval: $checkInterval seconds" -ForegroundColor Gray
Write-Host ""

$notified = $false

while ($elapsedTime -lt $maxWaitTime) {
    Start-Sleep -Seconds $checkInterval
    $elapsedTime = (Get-Date) - $startTime
    
    # Refresh job status
    $job = Get-Job -Id $job.Id -ErrorAction SilentlyContinue
    
    if (-not $job) {
        Write-Host "⚠ Job not found. It may have completed or been removed." -ForegroundColor Yellow
        break
    }
    
    $elapsedMinutes = [math]::Round($elapsedTime.TotalMinutes, 1)
    Write-Host "[$elapsedMinutes min] Job Status: $($job.State)..." -ForegroundColor Gray
    
    if ($job.State -eq "Completed") {
        Write-Host ""
        Write-Host "═══════════════════════════════════════" -ForegroundColor Green
        Write-Host "🎉 CHAT 1 COMPLETED! 🎉" -ForegroundColor Green -BackgroundColor Black
        Write-Host "═══════════════════════════════════════" -ForegroundColor Green
        Write-Host ""
        
        # Get output
        Write-Host "Final Output:" -ForegroundColor Cyan
        Write-Host "─────────────────────────────────────" -ForegroundColor Gray
        $output = Receive-Job -Id $job.Id
        $output | Select-Object -Last 30
        Write-Host "─────────────────────────────────────" -ForegroundColor Gray
        Write-Host ""
        
        # Check created files
        Write-Host "Generated Files:" -ForegroundColor Cyan
        $files = Get-ChildItem data\processed\*.csv -ErrorAction SilentlyContinue | 
            Where-Object { $_.Name -notlike "sample_*" } |
            Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB, 2)}}, LastWriteTime |
            Sort-Object LastWriteTime -Descending
        
        $files | Format-Table -AutoSize
        
        Write-Host "✓ Total processing time: $elapsedMinutes minutes" -ForegroundColor Green
        Write-Host ""
        Write-Host "Chat 1 is COMPLETE! Ready for Chat 2: Model Training" -ForegroundColor Green -BackgroundColor Black
        Write-Host ""
        
        # System notification (if available)
        if (Get-Command New-BurntToastNotification -ErrorAction SilentlyContinue) {
            New-BurntToastNotification -Text "Chat 1 Complete!", "Feature engineering finished successfully!" -Sound Default
        }
        
        $notified = $true
        break
    }
    elseif ($job.State -eq "Failed") {
        Write-Host ""
        Write-Host "❌ Job Failed!" -ForegroundColor Red
        Write-Host "Error Output:" -ForegroundColor Red
        Receive-Job -Id $job.Id
        break
    }
}

if (-not $notified -and $elapsedTime.TotalMinutes -ge ($maxWaitTime / 60)) {
    Write-Host ""
    Write-Host "⚠ Monitoring timeout reached ($maxWaitTime seconds)" -ForegroundColor Yellow
    Write-Host "Job may still be running. Check manually:" -ForegroundColor Yellow
    Write-Host "  Get-Job Chat1Run | Receive-Job -Keep" -ForegroundColor White
}

