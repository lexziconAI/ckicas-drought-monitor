# Debate Monitor Script - Updates every 30 seconds
$startTime = Get-Date
$updateInterval = 30

Write-Host "🌀 AXIOM-X PHASE 1 DEBATE MONITOR" -ForegroundColor Cyan
Write-Host "Started at: $startTime" -ForegroundColor Yellow
Write-Host "Updates every $updateInterval seconds" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Cyan

while ($true) {
    $currentTime = Get-Date
    $elapsed = $currentTime - $startTime

    # Check if debate is still running
    $pythonProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*orchestrator.py*" }

    if (-not $pythonProcess) {
        Write-Host "❌ Debate process not found - may have completed or crashed" -ForegroundColor Red
        break
    }

    # Check for output files
    $outputDir = "c:\Users\regan\ID SYSTEM\axiom-x\self-optimization\phase1"
    if (Test-Path $outputDir) {
        $files = Get-ChildItem $outputDir -File
        $debateLogExists = Test-Path "$outputDir\DEBATE_LOG.json"
        $synthesisExists = Test-Path "$outputDir\DEBATE_SYNTHESIS.json"
    } else {
        $files = @()
        $debateLogExists = $false
        $synthesisExists = $false
    }

    # Try to read debate status
    try {
        $statusOutput = python -c "
from core.orchestrator import Phase1Orchestrator
import os
o = Phase1Orchestrator()
turns = len(o.debate_log)
resonance = o.chaos_tracker.calculate_resonance()
print(f'{turns},{resonance:.3f}')
" 2>$null

        if ($statusOutput) {
            $parts = $statusOutput -split ','
            $turns = [int]$parts[0]
            $resonance = [float]$parts[1]
        } else {
            $turns = 0
            $resonance = 0.0
        }
    } catch {
        $turns = 0
        $resonance = 0.0
    }

    # Display status
    Write-Host "[$($elapsed.ToString('hh\:mm\:ss'))] Debate Status:" -ForegroundColor Green
    Write-Host "  📊 Turns: $turns" -ForegroundColor White
    Write-Host "  🌊 Resonance: $resonance" -ForegroundColor White
    Write-Host "  📁 Output files: $($files.Count)" -ForegroundColor White
    Write-Host "  📝 Debate log: $(if ($debateLogExists) { '✅' } else { '❌' })" -ForegroundColor White
    Write-Host "  🧠 Synthesis: $(if ($synthesisExists) { '✅' } else { '❌' })" -ForegroundColor White
    Write-Host "  ⚙️ Process running: ✅ (PID: $($pythonProcess.Id))" -ForegroundColor White

    # Check convergence
    if ($resonance -ge 0.85 -and $turns -gt 0) {
        Write-Host "🎯 CONVERGENCE ACHIEVED! Resonance ≥ 0.85" -ForegroundColor Green
    } elseif ($elapsed.TotalHours -ge 3) {
        Write-Host "⏰ TIMEOUT REACHED (3 hours)" -ForegroundColor Yellow
    }

    Write-Host "-" * 50 -ForegroundColor Gray

    Start-Sleep -Seconds $updateInterval
}