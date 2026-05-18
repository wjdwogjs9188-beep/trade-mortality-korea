# Phase 2 sub-task 2.2 -- HIRA ATC4 panel ETL wrapper
# Usage: powershell -ExecutionPolicy Bypass -File run_hira_atc4_etl.ps1

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pyScript = Join-Path $scriptDir "2_2_hira_atc4_etl.py"

Write-Host "[run_hira_atc4_etl] starting Python ETL: $pyScript"
$start = Get-Date
python $pyScript
$exit = $LASTEXITCODE
$dur = (Get-Date) - $start
Write-Host ("[run_hira_atc4_etl] done in {0:N1}s (exit={1})" -f $dur.TotalSeconds, $exit)
exit $exit
