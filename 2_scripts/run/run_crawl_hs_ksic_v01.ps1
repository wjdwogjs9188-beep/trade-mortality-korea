<#
.SYNOPSIS  researchall.net API 직접 호출 (HS↔KSIC 매핑).
.DESCRIPTION
    1단계: --probe 로 API 한도 + totalCount 탐색.
    2단계: --crawl 로 풀 다운 + CSV 산출.
.NOTES
    의존    : pip install requests
    실행    : powershell -ExecutionPolicy Bypass -File .\run_crawl_hs_ksic_v01.ps1 -Mode probe
              또는       -Mode crawl -Limit 100
#>

param(
    [string]$Project = "C:\Users\82103\Downloads\trade_mortality_korea",
    [ValidateSet("probe", "crawl")][string]$Mode = "probe",
    [int]$Limit = 100
)

$ErrorActionPreference = "Continue"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location -Path $Project

Write-Host "========================================================================"
Write-Host " researchall.net HS-KSIC API — Mode=$Mode, Limit=$Limit"
Write-Host "========================================================================"

# requests 의존성 확인
$check = & python -c "import requests; print('ok')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [install] requests"
    & python -m pip install --quiet requests
}

if ($Mode -eq "probe") {
    & python "2_scripts/data_collection/17_researchall_hs_ksic_crawl.py" --probe
    Write-Host ""
    Write-Host " 다음 step:"
    Write-Host "   1. 5_logs\data_collection\$(Get-Date -Format yyyy-MM-dd)_researchall_api.md 의 권장 limit 확인"
    Write-Host "   2. powershell -ExecutionPolicy Bypass -File .\run_crawl_hs_ksic_v01.ps1 -Mode crawl -Limit <권장>"
} else {
    Write-Host "  [crawl] limit=$Limit"
    & python "2_scripts/data_collection/17_researchall_hs_ksic_crawl.py" --crawl --limit $Limit
    Write-Host ""
    Write-Host " 결과:"
    Write-Host "   - CSV  : 0_raw\hs_ksic_concordance\researchall_HS6_to_KSIC_link.csv"
    Write-Host "   - raw  : 0_raw\hs_ksic_concordance\researchall_api_raw\page_NNNN.json"
    Write-Host "   - log  : 5_logs\data_collection\$(Get-Date -Format yyyy-MM-dd)_researchall_api.md"
}

exit $LASTEXITCODE
