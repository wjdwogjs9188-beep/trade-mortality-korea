<#
.SYNOPSIS Comtrade KR-CN bilateral 1995-1999 추가 호출 (pre-WTO).
.DESCRIPTION
    PAP v4.0 § 2.2 Test 2 (pre-WTO lead orthogonality) 용 1995-1999 trade.
    기존 2000-2024 (50 files) 와 동일 naming convention.
.NOTES
    선결    : .env 의 COMTRADE_API_KEY (4-way 로테이션 활용)
    실행    : powershell -ExecutionPolicy Bypass -File "C:\Users\82103\Downloads\trade_mortality_korea\2_scripts\run\run_comtrade_pre_wto.ps1"
    소요    : 10 호출 × 1초 = ~15초 (truncated 시 chapter 분할 + 시간↑)
#>
param(
    [string]$Project = "C:\Users\82103\Downloads\trade_mortality_korea"
)

$ErrorActionPreference = "Continue"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location -Path $Project

Write-Host "========================================================================"
Write-Host " Comtrade KR-CN 1995-1999 추가 호출"
Write-Host " Project: $Project"
Write-Host "========================================================================"

# 의존성 확인
$check = & python -c "import requests, pandas, dotenv; print('ok')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [install] requests pandas python-dotenv"
    & python -m pip install --quiet requests pandas python-dotenv
}

$sw = [System.Diagnostics.Stopwatch]::StartNew()
& python "2_scripts/data_collection/20_comtrade_kr_cn_pre_wto.py"
$code = $LASTEXITCODE
$sw.Stop()
$secs = [math]::Round($sw.Elapsed.TotalSeconds, 1)

Write-Host ""
Write-Host "========================================================================"
$status = if ($code -eq 0) { "[OK]" } elseif ($code -eq 2) { "[PARTIAL]" } else { "[FAIL]" }
Write-Host " $status exit=$code, $secs s"
Write-Host "========================================================================"
Write-Host ""
Write-Host "  결과:"
$folder = Join-Path $Project "0_raw\comtrade_korea_china"
$files = Get-ChildItem $folder -Filter "KR_*_199*.csv" -ErrorAction SilentlyContinue
if ($files) {
    Write-Host "  KR-CN 1995-1999 files: $($files.Count) / 10"
    foreach ($f in $files | Sort-Object Name) {
        $size_kb = [math]::Round($f.Length / 1024, 1)
        Write-Host ("    {0,-30} : {1,7} KB" -f $f.Name, $size_kb)
    }
} else {
    Write-Host "  KR-CN 1995-1999 files: 0 (모두 미수집)"
}
Write-Host ""
Write-Host "  로그: 5_logs\data_collection\$(Get-Date -Format yyyy-MM-dd)_comtrade_kr_cn_pre_wto.md"
exit $code
