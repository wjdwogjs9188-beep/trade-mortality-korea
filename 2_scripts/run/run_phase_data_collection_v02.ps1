<#
.SYNOPSIS Phase 0+1 v02 — 4 step 패치 후 재실행.
.DESCRIPTION
 v01 → v02 변경:
 - 13_ECOS: 분기 period "20001Q1" → "2000Q1", monthly year-by-year fetch, timeout 60s
 - 14_centroid: stdout UTF-8 reconfigure (이미 데이터 saved, 재실행 시 idempotent)
 - 15_KOSIS: getMeta probe 우선, error 메시지 자세히 출력
 - 16_WEO: sandbox 에서 이미 배치됨, skip-if-exists 동작
.NOTES
 실행: powershell -ExecutionPolicy Bypass -File "C:\Users\82103\Downloads\trade_mortality_korea\run_phase_data_collection_v02.ps1"
#>
param(
 [string]$Project = "C:\Users\82103\Downloads\trade_mortality_korea"
)

$ErrorActionPreference = "Continue"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location -Path $Project

$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "========================================================================"
Write-Host " Phase 0+1 v02 -- $ts"
Write-Host "========================================================================"

$results = @
function Run-Step {
 param([string]$Label, [string]$Script)
 Write-Host ""
 Write-Host "------------------------------------------------------------------------"
 Write-Host " [$Label]"
 Write-Host "------------------------------------------------------------------------"
 $sw = [System.Diagnostics.Stopwatch]::StartNew
 & python $Script
 $code = $LASTEXITCODE
 $sw.Stop
 $secs = [math]::Round($sw.Elapsed.TotalSeconds, 1)
 $status = if ($code -eq 0) { "[OK]" } elseif ($code -eq 2) { "[PARTIAL]" } else { "[FL]" }
 Write-Host " $status exit=$code, $secs s"
 return [pscustomobject]@{ Label=$Label; Exit=$code; Sec=$secs; Status=$status }
}

$results += Run-Step "Phase 0 WEO 배치 " "2_scripts/data_collection/16_weo_relocate.py"
$results += Run-Step "Phase 1.1 sigungu centroid " "2_scripts/data_collection/14_sigungu_centroid.py"
$results += Run-Step "Phase 1.2 ECOS Test 1 v02 " "2_scripts/data_collection/13_ecos_test1_macro_vars.py"
$results += Run-Step "Phase 1.3 KOSIS 출생성비 v02 " "2_scripts/data_collection/15_kosis_birth_sex_ratio.py"

Write-Host ""
Write-Host "========================================================================"
Write-Host " 종합"
Write-Host "========================================================================"
$results | Format-Table Label, Status, Exit, Sec -AutoSize

$folders = @(
 "0_raw\imf_weo_korea_vintage",
 "0_raw\sigungu_centroid",
 "0_raw\ecos_macro_extra",
 "0_raw\kosis_birth_sex_ratio"
)
foreach ($f in $folders) {
 $full = Join-Path $Project $f
 if (Test-Path $full) {
 $files = Get-ChildItem $full -File -ErrorAction SilentlyContinue
 $count = if ($files) { $files.Count } else { 0 }
 $size_mb = if ($files) { [math]::Round(($files | Measure-Object -Sum Length).Sum / 1MB, 2) } else { 0 }
 Write-Host (" {0,-40}: {1,3} files, {2,7} MB" -f $f, $count, $size_mb)
 }
}

Write-Host ""
Write-Host " 로그: 5_logs\data_collection\$(Get-Date -Format yyyy-MM-dd)_*.md"
exit 0
