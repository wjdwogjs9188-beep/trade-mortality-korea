# Stage 0 - Raw Data 통합 정리 (2026-05-03)
# 분산된 raw data 를 trade_mortality_korea/0_raw/ 로 복사
#
# 실행:
#   cd C:\Users\82103\Downloads\trade_mortality_korea
#   powershell -ExecutionPolicy Bypass -File 2_scripts\data_organization\copy_raw_data.ps1
#
# 또는 PowerShell 에서 직접:
#   .\2_scripts\data_organization\copy_raw_data.ps1

# UTF-8 설정 (한글 처리)
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# Source paths
$Desktop      = "C:\Users\82103\Desktop"
$Industry     = "$Desktop\산업 비중 데이터"
$Research     = "$Desktop\연구 자료"
$ResearchUse  = "$Desktop\연구용"
$Lda          = "L:\da\_paper_raw"
$RefMd        = "$Desktop\연구 자료\참고논문\md"

# Destination root
$ProjectRoot = "C:\Users\82103\Downloads\trade_mortality_korea"
$Root        = "$ProjectRoot\0_raw"

Write-Host ("=" * 72)
Write-Host "Stage 0 - Raw Data 통합 정리 시작"
Write-Host ("=" * 72)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

function MakeDir {
    param($Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
        Write-Host "  [mkdir] $Path"
    }
}

function CopySafe {
    param($Source, $Dest, $Label = "")
    if (Test-Path $Source) {
        try {
            Copy-Item -Path $Source -Destination $Dest -Force -ErrorAction Stop
            $script:CopyCount++
            return $true
        } catch {
            Write-Host "  [FAIL] $Label : $($_.Exception.Message)" -ForegroundColor Red
            $script:FailCount++
            return $false
        }
    } else {
        Write-Host "  [SKIP] $Source (not found)" -ForegroundColor Yellow
        $script:SkipCount++
        return $false
    }
}

function CopyByFilter {
    param($SourceDir, $DestDir, $Filter, $Label = "")
    if (-not (Test-Path $SourceDir)) {
        Write-Host "  [SKIP] $SourceDir (not found)" -ForegroundColor Yellow
        return
    }
    $Files = Get-ChildItem -Path $SourceDir -Filter $Filter -File -ErrorAction SilentlyContinue
    foreach ($f in $Files) {
        try {
            Copy-Item -Path $f.FullName -Destination $DestDir -Force
            $script:CopyCount++
        } catch {
            Write-Host "  [FAIL] $($f.Name)" -ForegroundColor Red
            $script:FailCount++
        }
    }
    Write-Host "  [copy] $($Files.Count) files matching '$Filter' from $Label"
}

# Counters
$script:CopyCount = 0
$script:FailCount = 0
$script:SkipCount = 0

# ---------------------------------------------------------------------------
# A. KOSIS 사업체조사 (광업·제조업)
# ---------------------------------------------------------------------------
Write-Host "`n[A] kosis_business_survey/ - 광업·제조업조사 1994-2024"

MakeDir "$Root\kosis_business_survey\microdata_1994_2024"
MakeDir "$Root\kosis_business_survey\codebook"
MakeDir "$Root\kosis_business_survey\ksic_version_concordance"

# Microdata CSV (31 년 panel)
CopyByFilter -SourceDir $Industry -DestDir "$Root\kosis_business_survey\microdata_1994_2024" -Filter "*.csv" -Label "산업 비중 데이터"

# Codebook (조사 및 파일설계서)
$CodebookSrc = "$Industry\조사 및 파일설계서"
if (Test-Path $CodebookSrc) {
    Copy-Item -Path "$CodebookSrc\*" -Destination "$Root\kosis_business_survey\codebook" -Recurse -Force -ErrorAction SilentlyContinue
    $script:CopyCount += (Get-ChildItem -Path $CodebookSrc -Recurse -File).Count
    Write-Host "  [copy] codebook directory (recursive)"
}

# KSIC version 연계표
CopySafe "$Industry\8차_9차개정 연계표.xls"                                 "$Root\kosis_business_survey\ksic_version_concordance\" "KSIC 8->9"
CopySafe "$Industry\KSIC연계표(9차_10차).xlsx"                              "$Root\kosis_business_survey\ksic_version_concordance\" "KSIC 9->10"
CopySafe "$Industry\한국표준산업분류 제11차-제10차 연계표.xlsx"            "$Root\kosis_business_survey\ksic_version_concordance\" "KSIC 11->10"

# ---------------------------------------------------------------------------
# B. HS-ISIC4 concordance
# ---------------------------------------------------------------------------
Write-Host "`n[B] hs_isic4_concordance/ - Stage 4B 매핑용"

MakeDir "$Root\hs_isic4_concordance"

CopySafe "$Research\cpc21-hs2012.txt"                                       "$Root\hs_isic4_concordance\" "CPC-HS"
CopySafe "$Research\cpc21-isic4.txt"                                        "$Root\hs_isic4_concordance\" "CPC-ISIC4"

# Stata .do 파일 3 개
$HSdoDir = "$ResearchUse\hs 연계표"
if (Test-Path $HSdoDir) {
    Copy-Item "$HSdoDir\*.do" -Destination "$Root\hs_isic4_concordance\" -Force
    $script:CopyCount += (Get-ChildItem -Path $HSdoDir -Filter "*.do" -File).Count
    Write-Host "  [copy] HS-ISIC4 .do scripts (3 files)"
}

# KSIC11-ISIC4 연계표
CopySafe "$Research\8.한국표준산업분류 제11차-국제표준산업분류 제4차 연계표_20240626043559.xlsx" "$Root\hs_isic4_concordance\KSIC11_ISIC4_연계표.xlsx" "KSIC11-ISIC4"

# ---------------------------------------------------------------------------
# C. 가족 mediator
# ---------------------------------------------------------------------------
Write-Host "`n[C] kosis_family_mediators/ - 이혼·결혼·출산"

MakeDir "$Root\kosis_family_mediators"

CopySafe "$ResearchUse\시군구 혼인.xls"     "$Root\kosis_family_mediators\" "시군구 혼인"
CopySafe "$ResearchUse\시군구 이혼.xls"     "$Root\kosis_family_mediators\" "시군구 이혼"
CopySafe "$ResearchUse\시군구 출생아.xls"   "$Root\kosis_family_mediators\" "시군구 출생아"
CopySafe "$ResearchUse\시군구_출생아수__합계출산율_20260419183410.xlsx" "$Root\kosis_family_mediators\시군구_합계출산율.xlsx" "합계출산율"

# ---------------------------------------------------------------------------
# D. 복지사업 수급권자 (빈곤 control + 한부모 일부)
# ---------------------------------------------------------------------------
Write-Host "`n[D] kosis_welfare_recipients/ - 복지사업 수급권자 2003-2019"

MakeDir "$Root\kosis_welfare_recipients"

$WelfareDir = "$Research\복지사업 시군구별 수급권자 현황(2012년 12월)"
if (Test-Path $WelfareDir) {
    Copy-Item -Path "$WelfareDir\*" -Destination "$Root\kosis_welfare_recipients" -Recurse -Force -ErrorAction SilentlyContinue
    $script:CopyCount += (Get-ChildItem -Path $WelfareDir -Recurse -File).Count
    Write-Host "  [copy] welfare recipients directory (recursive)"
}

# ---------------------------------------------------------------------------
# E. ECOS 가계 부채
# ---------------------------------------------------------------------------
Write-Host "`n[E] ecos_household_credit/ - other channel"

MakeDir "$Root\ecos_household_credit"

CopySafe "$ResearchUse\bok_household_가계대출_은행.csv"   "$Root\ecos_household_credit\" "가계대출 은행"
CopySafe "$ResearchUse\bok_household_가계대출_비은행.csv" "$Root\ecos_household_credit\" "가계대출 비은행"
CopySafe "$ResearchUse\bok_household_연체율.csv"          "$Root\ecos_household_credit\" "연체율"

# ---------------------------------------------------------------------------
# F. NHIS 건강 데이터
# ---------------------------------------------------------------------------
Write-Host "`n[F] nhis_health/ - L:\da NHIS 진료·의약품·검진"

MakeDir "$Root\nhis_health"
MakeDir "$Root\nhis_health\국민건강통계_2024_엑셀"
MakeDir "$Root\nhis_health\국민건강통계_2024_한글"

$NHISDir = "$Lda\07_mechanisms\nhis"
if (Test-Path $NHISDir) {
    # microdata + manuals
    Get-ChildItem -Path $NHISDir -File -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination "$Root\nhis_health\" -Force -ErrorAction SilentlyContinue
        $script:CopyCount++
    }

    # 국민건강통계 2024 엑셀 (28 분야)
    $HKExcel = "$NHISDir\2024국민건강통계(ver.엑셀)"
    if (Test-Path $HKExcel) {
        Copy-Item -Path "$HKExcel\*" -Destination "$Root\nhis_health\국민건강통계_2024_엑셀\" -Force -ErrorAction SilentlyContinue
        $script:CopyCount += (Get-ChildItem -Path $HKExcel -File).Count
        Write-Host "  [copy] 국민건강통계 2024 엑셀 28 분야"
    }

    # 국민건강통계 2024 한글
    $HKHwp = "$NHISDir\2024국민건강통계(ver.한글)"
    if (Test-Path $HKHwp) {
        Copy-Item -Path "$HKHwp\*" -Destination "$Root\nhis_health\국민건강통계_2024_한글\" -Force -ErrorAction SilentlyContinue
        $script:CopyCount += (Get-ChildItem -Path $HKHwp -File).Count
    }
} else {
    Write-Host "  [SKIP] L:\da NHIS dir not accessible" -ForegroundColor Yellow
}

# ---------------------------------------------------------------------------
# G. HIRA quarterly
# ---------------------------------------------------------------------------
Write-Host "`n[G] hira_quarterly/"

MakeDir "$Root\hira_quarterly"
CopySafe "$ResearchUse\kosis_hira_quarterly_2009_2025.csv" "$Root\hira_quarterly\" "HIRA 분기"

# ---------------------------------------------------------------------------
# H. 주택가격
# ---------------------------------------------------------------------------
Write-Host "`n[H] kosis_housing/ - 주택매매가격지수"

MakeDir "$Root\kosis_housing"
CopySafe "$ResearchUse\그외 지표\유형별_주택매매가격지수_2011.6100__20260408180958.csv" "$Root\kosis_housing\주택매매가격지수.csv" "주택매매가격"

# ---------------------------------------------------------------------------
# I. 산업분류별 주요지표
# ---------------------------------------------------------------------------
Write-Host "`n[I] kosis_industry_summary/ - 산업분류별 주요지표"

MakeDir "$Root\kosis_industry_summary"

$IndSumDir = "$ResearchUse\그외 지표"
if (Test-Path $IndSumDir) {
    # 주택매매가격지수 제외하고 나머지 모든 csv
    Get-ChildItem -Path $IndSumDir -Filter "*.csv" -File | Where-Object { $_.Name -notlike "*주택매매*" } | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination "$Root\kosis_industry_summary\" -Force
        $script:CopyCount++
    }
    Write-Host "  [copy] 산업분류 csv files"
}

# ---------------------------------------------------------------------------
# J. 사망 집계 (시도 + 시군구)
# ---------------------------------------------------------------------------
Write-Host "`n[J] kostat_mortality_aggregated/ - 사망원인 집계"

MakeDir "$Root\kostat_mortality_aggregated"

# 시도 사망원인 표준화 사망률 1996+
$Mort01Dir = "$Lda\01_mortality"
if (Test-Path $Mort01Dir) {
    Get-ChildItem -Path $Mort01Dir -Filter "*.csv" -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination "$Root\kostat_mortality_aggregated\" -Force
        $script:CopyCount++
    }
    Write-Host "  [copy] 시도 사망원인 표준화 사망률"
}

# 시군구 사망원인.csv (이전 reference)
CopySafe "$ResearchUse\시군구 사망원인.csv" "$Root\kostat_mortality_aggregated\시군구_사망원인.csv" "시군구 사망원인"

# ---------------------------------------------------------------------------
# K. crosswalks (법정동코드 + country)
# ---------------------------------------------------------------------------
Write-Host "`n[K] crosswalks/ - 행정구역 + 국가코드"

MakeDir "$Root\crosswalks"

$CWDir = "$Lda\05_crosswalks"
if (Test-Path $CWDir) {
    Get-ChildItem -Path $CWDir -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination "$Root\crosswalks\" -Force
        $script:CopyCount++
    }
    Write-Host "  [copy] crosswalks (법정동코드, country)"
}

# ---------------------------------------------------------------------------
# L. 참고논문 (md / docx 만, 별도 위치)
# ---------------------------------------------------------------------------
Write-Host "`n[L] 6_references/ - md / docx 만 (PDFs 그대로 둠)"

$RefDir = "$ProjectRoot\6_references"
MakeDir $RefDir
MakeDir "$RefDir\md_converted"

# 참고논문 폴더의 md / docx
$RefSrc = "$Research\참고논문"
if (Test-Path $RefSrc) {
    Get-ChildItem -Path $RefSrc -Filter "*.md" -File -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination "$RefDir\" -Force
        $script:CopyCount++
    }
    Get-ChildItem -Path $RefSrc -Filter "*.docx" -File -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination "$RefDir\" -Force
        $script:CopyCount++
    }
    Write-Host "  [copy] *.md / *.docx from 참고논문/"
}

# md 별도 폴더 (사용자가 mounted 한 것)
if (Test-Path $RefMd) {
    Copy-Item -Path "$RefMd\*" -Destination "$RefDir\md_converted\" -Recurse -Force -ErrorAction SilentlyContinue
    $script:CopyCount += (Get-ChildItem -Path $RefMd -Recurse -File).Count
    Write-Host "  [copy] md_converted directory (recursive)"
}

# ---------------------------------------------------------------------------
# Summary + Inventory CSV
# ---------------------------------------------------------------------------
Write-Host "`n" + ("=" * 72)
Write-Host "복사 완료 - 통계"
Write-Host ("=" * 72)
Write-Host "  성공:  $($script:CopyCount) 파일"
Write-Host "  실패:  $($script:FailCount) 파일"
Write-Host "  SKIP:  $($script:SkipCount) 파일 (source 부재)"

# 최종 0_raw/ 통계
$TotalFiles = (Get-ChildItem -Path $Root -Recurse -File -ErrorAction SilentlyContinue).Count
$TotalSize  = (Get-ChildItem -Path $Root -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
Write-Host "`n0_raw/ 최종:"
Write-Host "  총 파일 수: $TotalFiles"
Write-Host "  총 크기:    $([math]::Round($TotalSize, 2)) GB"

# Inventory CSV 생성
$InventoryPath = "$ProjectRoot\0_raw_inventory_2026_05_03.csv"
Get-ChildItem -Path $Root -Recurse -File -ErrorAction SilentlyContinue |
    Select-Object @{N='RelativePath';E={$_.FullName.Replace("$Root\","")}},
                  @{N='SizeKB';E={[math]::Round($_.Length / 1KB, 2)}},
                  LastWriteTime |
    Export-Csv -Path $InventoryPath -NoTypeInformation -Encoding UTF8

Write-Host "`nInventory: $InventoryPath"
Write-Host ("=" * 72)
Write-Host "완료"
Write-Host ("=" * 72)
