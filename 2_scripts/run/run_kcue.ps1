<#
.SYNOPSIS KCUE 한국대학교육협의회 OpenAPI — 1990 이전 설립 4년제 baseline.
.NOTES
 선결:.env 의 DATA_GO_KR_API_KEY (data.go.kr 서비스키)
 주의: KCUE API 가 본인 key 로 *승인* 받아야 호출 가능
 미승인 시 첫 응답에 resultCode!= "00" 출현 — log 확인 후 data.go.kr 에서 신청
 실행: powershell -ExecutionPolicy Bypass -File "C:\Users\82103\Downloads\trade_mortality_korea\2_scripts\run\run_kcue.ps1"
#>
param(
 [string]$Project = "C:\Users\82103\Downloads\trade_mortality_korea"
)

$ErrorActionPreference = "Continue"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $Project

Write-Host "========================================================================"
Write-Host " KCUE getSchoolInfo — 1990 baseline 4년제 추출"
Write-Host "========================================================================"

$check = & python -c "import requests, dotenv; print('ok')" 2>&1
if ($LASTEXITCODE -ne 0) {
 & python -m pip install --quiet requests python-dotenv
}

$sw = [System.Diagnostics.Stopwatch]::StartNew
& python "2_scripts/data_collection/21_kcue_university_api.py"
$code = $LASTEXITCODE
$sw.Stop
$secs = [math]::Round($sw.Elapsed.TotalSeconds, 1)

Write-Host ""
$status = if ($code -eq 0) { "[OK]" } elseif ($code -eq 2) { "[PARTIAL]" } else { "[FL]" }
Write-Host "$status exit=$code, $secs s"
Write-Host ""
Write-Host " 결과:"
$folder = Join-Path $Project "0_raw\edu_university_list_1990"
$files = Get-ChildItem $folder -Filter "*.csv" -ErrorAction SilentlyContinue
foreach ($f in $files | Sort-Object Name) {
 $size_kb = [math]::Round($f.Length / 1024, 1)
 Write-Host (" {0,-50}: {1,7} KB" -f $f.Name, $size_kb)
}
Write-Host ""
Write-Host " log: 5_logs\data_collection\$(Get-Date -Format yyyy-MM-dd)_kcue_university.md"
exit $code
