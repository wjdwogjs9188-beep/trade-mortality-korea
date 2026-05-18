<#
.SYNOPSIS
    Phase 0 + Phase 1 데이터 수집 일괄 실행.

.DESCRIPTION
    PAP v4.0 § 7 의 Phase A-B 진입 전 차단 데이터 4 source 수집:
      - Phase 0   : WEO Historical xlsx 배치
      - Phase 1.1 : 시군구 centroid (GitHub southkorea-maps)
      - Phase 1.2 : ECOS 신규 시리즈 3개 (200Y007, 401Y014, 401Y015)
      - Phase 1.3 : KOSIS 출생성비 시군구 1980-1995

    각 step 실패해도 다음 진행. 결과 로그는 5_logs/data_collection/<date>_*.md.

.NOTES
    실행 위치 : trade_mortality_korea/ 루트
    선결      : .env 에 ECOS_API_KEY, KOSIS_API_KEY 설정
    실행      : powershell -ExecutionPolicy Bypass -File .\run_phase_data_collection_v01.ps1
#>

param(
    [string]$Project = "C:\Users\82103\Downloads\trade_mortality_korea"
)

$ErrorActionPreference = "Continue"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location -Path $Project

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "========================================================================"
Write-Host " Phase 0+1 데이터 수집 -- $timestamp"
Write-Host " Project: $Project"
Write-Host "========================================================================"

$results = @()
function Run-Step {
    param([string]$Label, [string]$Script)
    Write-Host ""
    Write-Host "------------------------------------------------------------------------"
    Write-Host " [$Label] python $Script"
    Write-Host "------------------------------------------------------------------------"
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    & python $Script
    $code = $LASTEXITCODE
    $sw.Stop()
    $secs = [math]::Round($sw.Elapsed.TotalSeconds, 1)
    if ($code -eq 0) {
        $status = "[OK]"
    } elseif ($code -eq 2) {
        $status = "[PARTIAL]"
    } else {
        $status = "[FAIL]"
    }
    Write-Host "  $status exit=$code, $secs s"
    return [pscustomobject]@{
        Label  = $Label
        Script = $Script
        Exit   = $code
        Sec    = $secs
        Status = $status
    }
}

# Phase 0
$results += Run-Step "Phase 0   WEO 배치           " "2_scripts/data_collection/16_weo_relocate.py"

# Phase 1.1
$results += Run-Step "Phase 1.1 sigungu centroid    " "2_scripts/data_collection/14_sigungu_centroid.py"

# Phase 1.2
$results += Run-Step "Phase 1.2 ECOS Test 1 macro   " "2_scripts/data_collection/13_ecos_test1_macro_vars.py"

# Phase 1.3
$results += Run-Step "Phase 1.3 KOSIS 출생성비      " "2_scripts/data_collection/15_kosis_birth_sex_ratio.py"

# 종합 보고
Write-Host ""
Write-Host "========================================================================"
Write-Host " 종합"
Write-Host "========================================================================"
$results | Format-Table Label, Status, Exit, Sec -AutoSize

# 결과 데이터 폴더 점검
Write-Host ""
Write-Host "  데이터 폴더 상태:"
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
        Write-Host ("    {0,-40} : {1,3} files, {2,7} MB" -f $f, $count, $size_mb)
    } else {
        Write-Host ("    {0,-40} : (folder missing)" -f $f)
    }
}

Write-Host ""
Write-Host "  로그 위치: 5_logs\data_collection\$(Get-Date -Format yyyy-MM-dd)_phase*.md"
Write-Host ""

# Final exit
$failures = ($results | Where-Object { $_.Exit -ne 0 -and $_.Exit -ne 2 }).Count
if ($failures -gt 0) {
    Write-Host "  [WARN] $failures step 실패 -- 로그 확인 후 재실행 또는 수동 처리"
    exit 1
} else {
    Write-Host "  [DONE] 모두 완료 (또는 partial 만)"
    exit 0
}
