# Phase 2 sub-task 2.3 -- M1 composite outcome wrapper
# Usage: powershell -ExecutionPolicy Bypass -File run_m1_composite.ps1

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pyScript = Join-Path $scriptDir "2_3_m1_composite.py"

Write-Host "[run_m1_composite] starting Python: $pyScript"
$start = Get-Date
python $pyScript
$exit = $LASTEXITCODE
$dur = (Get-Date) - $start
Write-Host ("[run_m1_composite] done in {0:N1}s (exit={1})" -f $dur.TotalSeconds, $exit)
exit $exit
