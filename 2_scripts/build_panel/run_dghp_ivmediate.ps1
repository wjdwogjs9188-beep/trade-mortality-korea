# Phase 2 sub-task 2.4 -- DGHP ivmediate wrapper
# Usage: powershell -ExecutionPolicy Bypass -File run_dghp_ivmediate.ps1

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pyScript = Join-Path $scriptDir "2_4_dghp_ivmediate.py"

Write-Host "[run_dghp_ivmediate] starting Python: $pyScript"
$start = Get-Date
python $pyScript
$exit = $LASTEXITCODE
$dur = (Get-Date) - $start
Write-Host ("[run_dghp_ivmediate] done in {0:N1}s (exit={1})" -f $dur.TotalSeconds, $exit)
exit $exit
