# ============================================================================
# Phase B-x diagnostics -- single-shot runner
# PAP v4.0 § 2.2 Tests 1, 1 v2, 1b, 3 + first-stage F
# usage: powershell -ExecutionPolicy Bypass -File run_phase_bx_all.ps1
# ============================================================================
$ErrorActionPreference = "Continue"

# ---- UTF-8 console encoding (Korean print fix) ----
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new
$OutputEncoding = [System.Text.UTF8Encoding]::new
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

$proj = "C:\Users\82103\Downloads\trade_mortality_korea"
Set-Location $proj
$ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " Phase B-x diagnostics ($ts)" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

$scripts = @(
 @{ name = "Test 1 Romer-Romer macro predictability"; file = "22_phase_bx_test1_macro_predictability.py" },
 @{ name = "Test 1 v2 (univariate Bonferroni + HAC)"; file = "22b_phase_bx_test1_v2_reduced.py" },
 @{ name = "Test 1b WEO forecast surprise robustness"; file = "23_phase_bx_test1b_weo_surprise.py" },
 @{ name = "Test 3 Pierce-Schott pre-trend"; file = "24_phase_bx_test3_pierce_schott_pretrend.py" },
 @{ name = "First-stage F (z_x: ADH-8 vs KR-CN)"; file = "25_phase_bx_first_stage_f.py" }
)

$summary = @
foreach ($s in $scripts) {
 $path = Join-Path "2_scripts\identification" $s.file
 Write-Host ""
 Write-Host "[RUN] $($s.name)" -ForegroundColor Yellow
 Write-Host " $path"
 if (-not (Test-Path $path)) {
 Write-Host " [SKIP] file not found" -ForegroundColor Red
 $summary += [pscustomobject]@{ name = $s.name; status = "MISSING" }
 continue
 }
 $start = Get-Date
 try {
 python -X utf8 $path 2>&1 | Tee-Object -Variable out | Out-Host
 $elapsed = ((Get-Date) - $start).TotalSeconds
 $summary += [pscustomobject]@{
 name = $s.name
 status = "OK"
 seconds = [math]::Round($elapsed, 1)
 }
 } catch {
 $summary += [pscustomobject]@{ name = $s.name; status = "ERROR: $_" }
 }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host " Summary" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
$summary | Format-Table -AutoSize

$today = Get-Date -Format "yyyy-MM-dd"
Write-Host ""
Write-Host "Logs: 5_logs\integrity_checks\${today}_phase_bx_*.md" -ForegroundColor Cyan
Write-Host "Data: 3_derived\identification\test*_*.csv" -ForegroundColor Cyan
