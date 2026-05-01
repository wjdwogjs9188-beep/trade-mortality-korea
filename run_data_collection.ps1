# 데이터 수집 자동 실행 스크립트
# 사용법: PowerShell 에서 .\run_data_collection.ps1

$ErrorActionPreference = "Stop"

Write-Host "=== Phase 1 데이터 수집 시작 ===" -ForegroundColor Green
Set-Location $PSScriptRoot

# Step 0: 패키지 설치
Write-Host "`n[0/5] 패키지 설치..." -ForegroundColor Cyan
python -m pip install -r requirements.txt

# Step 1: ECOS 탐색
Write-Host "`n[1/5] ECOS 가계대출 연체율 통계표 탐색..." -ForegroundColor Cyan
python 2_scripts\data_collection\01_ecos_explore.py

# Step 2: ECOS 다운로드
Write-Host "`n[2/5] ECOS 가계대출 연체율 다운로드..." -ForegroundColor Cyan
python 2_scripts\data_collection\02_ecos_household_delinquency.py

# Step 3: Comtrade ADH 8국
Write-Host "`n[3/5] UN Comtrade ADH 8국 x China imports 다운로드 (30-60분 예상)..." -ForegroundColor Cyan
python 2_scripts\data_collection\03_comtrade_adh_china.py

# Step 4: Korea-China bilateral
Write-Host "`n[4/5] UN Comtrade Korea-China bilateral 다운로드..." -ForegroundColor Cyan
python 2_scripts\data_collection\04_comtrade_korea_china.py

# Step 5: China-World
Write-Host "`n[5/5] UN Comtrade China-World 다운로드..." -ForegroundColor Cyan
python 2_scripts\data_collection\05_comtrade_china_world.py

Write-Host "`n=== 모두 완료 ===" -ForegroundColor Green
Write-Host "결과: 0_raw/ecos_delinquency/ + 0_raw/comtrade_*/ 확인"
