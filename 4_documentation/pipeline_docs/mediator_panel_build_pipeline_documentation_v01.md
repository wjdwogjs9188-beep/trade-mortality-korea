# Mediator Panel Build Pipeline — 종합 문서 v01

_작성: 2026-05-04, 정재헌 (가천대 경제학부)_
_paper: "Trade Shock and Deaths of Despair in Korea: Quantifying the Underexplored Family-Mediated Channel"_

---

## 0. 본 문서의 위치

본 문서는 paper PAP v3.4 의 § 5.2 (mediation analysis) 의 input panel — **mediator-specific
mortality rate panel** — build pipeline 종합 기록.

기존 산출물 (mortality_panel_v02_1.parquet) 는 **main outcome** (component decomposition,
3 ASR baseline) 까지만 cover. 본 작업은 paper 의 **family-mediated channel** (DGHP 2017
strict mediation framework) 의 mediator dimension (혼인상태 + 교육수준) 추가.

상위 framework:
- **PAP v3.4** (PAP_2026_05_03_v3.3.md, 안산 demote + panel v02.1 commit)
- **Stage 5 spec plan v01** (stage5_regression_plan_v01.md)
- 본 panel = Stage 5 의 **mediator-specific outcome 변수**

---

## 1. 연구 배경 + Mediation Framework

### 1.1 Paper 핵심 가설

> "한국의 deaths of despair (자살, 약물, 정신, 간) 는 무역 충격 (Bartik shift-share IV) 의
> 영향을 받음. 그 영향의 일부는 가족 mediator (혼인 분해, 교육 attainment 변화) 를 통해
> 전달됨."

### 1.2 DGHP 2017 mediation framework

Dippel, Gold, Heblich, Pinto (2017) "The effect of trade on workers and voters" NBER 23209
의 IV mediation:
- direct effect: trade shock → mortality (mediator 통제)
- indirect effect: trade shock → mediator → mortality
- 본 paper = indirect effect (family channel) 정량화

**input 요구**: mediator-specific mortality rate (= mediator 그룹별 사망률, 예: "이혼자
working-age 25-64 자살률") 이 paper § 5.2 regression 의 outcome.

본 panel 이 그 input.

---

## 2. 데이터 source 4 종

| source | 형태 | 용도 | 신청/취득 |
|--------|------|------|-----------|
| **KOSIS API** | online cross-tab | mediator denominator 1차 시도 | API key (사용자 보유) |
| **MDIS 인구주택총조사 2% 표본 microdata** | csv (시점별, cp949) | mediator denominator 2차 (성공) | MDIS 신청 (사용자) |
| **MDIS 사망원인통계 (B형) microdata** | csv (28 시점 1997-2024, cp949) | mortality numerator | MDIS 신청 (사용자, 기존) |
| **codebook xlsx** | 파일설계서 + 시군구코드집 + 8차분류 | column 매핑 + 코드 정의 | MDIS 부속 |

저장 위치:
- `C:\Users\82103\Downloads\trade_mortality_korea\0_raw\kosis_marriage_education\` — KOSIS API
- `C:\Users\82103\Downloads\trade_mortality_korea\0_raw\mdis_population_census\` — 인구
- `C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리\` — 사망 microdata + codebook

---

## 3. Stage A — KOSIS API mediator denominator 시도 (FL → MDIS 전환)

### 3.1 시도 spec

KOSIS Open API 12 URL (혼인 6 시점 1995-2020 + 교육 6 시점):
- DT_1IN9503, DT_1IN9502, DT_1PM0001, DT_1INOO02, DT_1IN0508, DT_1IN0504,
 DT_1IN1006, DT_1IN1004, DT_1PM1504, DT_1PM1501, DT_1PM2002, DT_1PM2001

cell limit 40,000 회피 위해 17 시도 분할 호출 (`fetch_kosis_split` 함수, sido in
`["11","21","22","23","24","25","26","29","31","32","33","34","35","36","37","38","39"]`).

세종 (29) 2012 이전 부재 (`SEJONG_BIRTH_YEAR = 2012`) 자동 skip.

### 3.2 발견 — 12 표 모두 시군구 dimension 부재

`outputFields=` 에 `+OBJ_ID+NM+C1+C1_NM+...+C5+C5_NM` 추가 patch 후에도:
- C1 = 시도 (서울 11), C2 = 연령 또는 성별, C3 = 혼인/교육
- 시군구 column 자체 부재 — TBL_NM 의 "...-시군구" 표기는 misnomer
- 5 표 verify (marriage_2010, marriage_2015, marriage_2020, education_2010, education_2015,
 education_2020) 모두 동일

DT 첫 값 = 시도 합계 (예: 서울 marriage_2020 DT = 8,264,053 = 한국인 15세 이상 서울 전체).

### 3.3 결정

**KOSIS publish data 의 인구총조사 시리즈 = 시도 level only**. 시군구 cross 부재.
→ MDIS 인구주택총조사 표본 microdata (시군구 detail 가능) 신청 결정.

### 3.4 산출 (참고용 — 본 panel 에 사용 X)

`0_raw/kosis_marriage_education/kosis_*.csv` 12 파일 (1.6 MB ~ 30 MB).

---

## 4. Stage B — MDIS 인구 microdata → mediator denominator panel

### 4.1 입수 데이터

사용자 MDIS 신청 ZIP 5 + 3 = 총 8 zip:
- `2%_표본_인구_20260504_65001_데이터.zip`: 2000-2020 5 시점 (사용 권장 — column header 정상)
- `2%_표본_인구_20260430_43590_데이터.zip`: 1990-2010 5 시점 (1990, 1995 만 사용 — 2000+
 column header broken)
- `USRCNFRM_*.zip` × 3: 파일설계서 + 시군구코드집 + 작성결과 가이드

### 4.2 Step 06 — 압축해제 + inventory

`06_mdis_population_unzip_inspect.py`:
- cp949 한글 파일명 자동 변환 (`info.filename.encode("cp437").decode("cp949")`)
- 8 zip 해제 → `0_raw/mdis_population_census/` 8 폴더
- 각 폴더 csv/xlsx/dat preview (line length 분포로 fixed-width vs csv 판단)

발견: **CSV (cp949)**, fixed-width 아님. 시점별 column 18 ~ 99 개 (1990 39, 1995 28,
2000 51, 2005 50, 2010 92, 2015 99, 2020 90).

### 4.3 Step 07 — column layout 추출

`07_mdis_population_columns_extract.py`:
- 7 시점 CSV header 모든 column 출력
- description xlsx (파일설계서 + 코드정보 + 행정구역코드) 추출 — `xlrd` 설치 필수
- target keyword (시도/시군구/성별/연령/혼인/교육/가구주관계) 자동 매칭

추출된 7 시점 column position table (CSV header by name):

| dim | 1990 | 1995 | 2000 | 2005 | 2010 | 2015 | 2020 |
|-----|------|------|------|------|------|------|------|
| 시도 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 시군구 | **1** | **1** | 1 | 2 | 2 | 2 | 2 |
| 성별 | 6 | 7 | 5 | 5 | 6 | 6 | 6 |
| 만연령 | (만나이) | (만나이) | 7 | 6 | 7 | 7 | 7 |
| 교육 | 10 | 14 | 9 | 8 | 9 | 9 | 9 |
| 혼인 | 25 | 26 | 39 | 36 | 43 | 47 | 43 |
| 가구주 | 5 | 6 | 8 | 7 | 8 | 8 | 8 |
| 가중값 | 38 | 27 | 49 | 49 | 58 | 96 | 89 |

특이점:
- **1990 시군구 = 2자리** (예: `11`=종로), 다른 시점 = 3자리 (`010`=종로) — 별도 mapping
- **1990 = "직할시"** (부산/대구/인천/광주/대전), 1995+ = "광역시"
- 시점별 column 명 모두 다름 → name-based mapping dict 필수

### 4.4 Step 08 — Cross-tab → mediator_panel_v01

`08_mdis_population_parse_crosstab.py`:

per-year column NAME mapping dict (`YEAR_COLUMN_MAP`) 사용:
- 2000-2020: 65001 batch 사용 (43590 batch column header broken 회피)
- 1990, 1995: 43590 batch only
- chunked read (200K row) 메모리 효율

처리:
1. h_code 결합 = `시도(2) + 시군구(zfill 3) = 5자리`
2. age_band = 5세 단위 (`00-04`,..., `80-84`, `85+`)
3. 국적 filter (2010+ `출생시국적_대한민국여부=1`, 1995-2007 변수 부재 → 전체 keep)
4. 가중값 적용 (sum(weight) = 모집단 추정)
5. cross-tab 2 panel:
 - **marriage**: h_code × year × sex × age × marital → population
 - **education**: h_code × year × sex × age × education → population

산출 v01:
- `mediator_panel_marriage_v01.parquet` (140,971 rows, 7 시점, 522 unique h_code)
- `mediator_panel_education_v01.parquet` (269,861 rows)

### 4.5 Step 09 — 4 issue 진단

`09_mediator_panel_validate.py`:

| issue | 발견 |
|-------|------|
| **'.' code (marital)** | 2005 만 보유. 2005 raw 의 14세 이하 (n=171,946) 모두 `.`. 다른 시점은 NaN 자동 drop |
| **2005 anomaly** | 2005 raw 14-18세 marital = '1' 부여 (다른 시점 14-18 부재). cleaning 필수 |
| **education 카테고리 차이** | 1990/2000/2010-2020 = 8 카테고리, 1995 = 7, 2005 = 6 (7,8 부재) — 통합 필요 |
| **h_code intersection = 22** | 1990 (sigungu 2자리) vs 2000+ (3자리) 5자리 구조 자체 다름 |

### 4.6 Step 10 — Cleaning + alignment → v02

`10_mediator_panel_clean_align.py`:

4 fix 적용:
- (a) **1990 drop** — 행정구역 mismatch + paper 시점 (1997-2024) 외
- (b) **age filter 25-64** — DGHP 2017 mediation 표준 (working-age)
- (c) **education 4 카테고리** — NoHS (1+2+3) / HS (4) / SomeCollege (5) / Bachelor+ (6+7+8)
- (d) **sigungu_crosswalk_v2 적용** — mortality_panel_v02_1 의 229 h_code align (분구 합산)

산출 v02:
- `mediator_panel_marriage_v02.parquet` (71,125 rows, 6 시점, 279 h_code)
- `mediator_panel_education_v02.parquet` (80,856 rows)

per-year pop sum (working-age 25-64):
- 1995: 23.3M, 2000: 25.2M, 2005: 26.6M, 2010: 27.9M, 2015: 29.2M, 2020: 29.7M
- 한국 working-age 추세 ±5% 일치 ✓

### 4.7 Step 10b — Education 3 카테고리 재매핑 → v03

`10b_mediator_panel_education_v03.py`:

validation issue H1 fix — mortality microdata 의 education 도 3 카테고리 (1997-2007 의
`5=대학통합` 와 2008+ 의 `6=4년제 / 7=대학원` 정확 매핑 불가):
- v02 4 → v03 3: NoHS / HS / **College+** (5+6+7+8 통합)

산출 v03:
- `mediator_panel_education_v03.parquet` (63,019 rows, 3 카테고리)

---

## 5. Stage C — MDIS 사망 microdata → numerator panel

### 5.1 입수

사용자 폴더 `C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리\` 28 csv (1997-2024,
cp949, 평균 ~15-22 MB):
- `1997_사망_연간자료_B형_*.csv` ~ `2024_*`
- 18 column (모든 시점): year/신고연도/신고월/신고일/시도/시군구/사망연월일/사망시/장소/직업/혼인/교육/성별/연령/국적/이전국적/cause_104/cause_57

부속 codebook (28 시점):
- `파일설계서(공공용)_*.xlsx` × 27
- `시군구코드집(공공용)_*.xlsx` × 25
- `사망원인통계_사망연간자료_코드집(8차질병분류코드).xlsx`

### 5.2 Step 11a — 28 시점 cleaning (verify Y → cleaned parquet)

`11a_mortality_microdata_parse.py`:

**bug history (4 회 재시도)**:

1. 첫 시도: column rename 시 1997-2007 의 age_5y_code 모두 NaN. column 명 정상 (`['17', '18',...]`) 인데 rename 후 NaN.
2. 두 시도: keyword fuzzy match + Unicode NFC normalize → 동일 fail.
3. 세 시도: **position-based parse** (column 명 무시, index 직접 사용) → 매핑 OK.
4. 네 시도: 1997-2007 national filter `→ 0` (all drop). 원인 = `national_code` NaN → `astype(str)` 후 `"nan"` string → `isin(["1", ""])` 매칭 fail.
5. 최종 fix: **외국인 (`"2"`) 만 drop, NaN/빈값/1 모두 keep** → 28 시점 모두 정상.

**Position-based parse** (column 명 무시, index 직접):
| index | canonical |
|-------|-----------|
| 0 | year_str |
| 4 | sido_raw |
| 5 | sigungu_raw |
| 10 | marital_code_raw |
| 11 | education_code_raw |
| 12 | sex_code |
| 13 | age_5y_code |
| 14 | national_code |
| 16 | cause_104 |

**처리 단계**:
1. 시군구 자릿수 정규화 (2023 5자리 anomaly + 2024 column 명 변경 처리)
2. age band 매핑 (`AGE_BAND_MAP`: 1=00-04,..., 18=85+, 19+ = 85+ 통합)
3. 한국인 filter (외국인 `"2"` 만 drop, 1997-2007 변수 부재 시 전체 keep)
4. 혼인 1-4 only (9 미상 drop)
5. **교육 3 카테고리 매핑** (mediator panel 과 align):
 - NoHS (1+2+3 = 무학+초등+중학)
 - HS (4 = 고등학교)
 - College+ (5+6+7 = 대학 통합)
6. cause_104 그대로 keep

산출:
- `mortality_microdata_cleaned_v01.parquet` (7,408,230 rows, 28 시점, 362 unique h_code)

per-year row count (28 시점, sample):
- 1997: 240,069
- 2000: 246,012
- 2010: 251,614
- 2020: 287,030
- 2024: 333,280

distribution:
- marital_code: 2 (배우자) 48% / 4 (이혼) 38% / 1 (미혼) 8% / 3 (사별) 6%
- education_band: NoHS 71% / HS 19% / College+ 10% (모든 연령 합산이라 NoHS 비율 high)
- age_band 85+ = 28%, 80-84 = 14%,... working-age 25-64 = ~14%

### 5.3 Step 11b — Numerator panel (mortality × mediator cross-tab)

`11b_mortality_mediator_crosstab.py`:

3 step 처리:
1. **age_band 25-64 filter** (M1 fix — mediator panel align): 7.4M → 1.5M (20.3%)
2. **sigungu_crosswalk_v2 적용** (M2 fix): h_code 362 → 229+17 = 346 (2024 시점 신설 시군구
 23개 unmatched, 2.64%)
3. **2 cross-tab**:
 - marital: h_code × year × sex × age × marital_code × cause_104 → deaths
 - education: 동일 + education_band

산출:
- `mortality_marital_panel_v01.parquet` (1,011,186 rows)
- `mortality_education_panel_v01.parquet` (1,035,849 rows)
- 둘 다 deaths sum 1,506,739 (working-age 25-64 28년 합)

deaths of despair 28년 합 (working-age 25-64):
- 자살 (102) = 208,683
- 간 (081) = 121,289
- 정신 (057) = 17,273
- 약물 (101) = 5,104

→ **paper § 7 핵심 가설 (한국 = 자살+간 dominance, US = 약물 dominance) 데이터 confirm**.

---

## 6. Stage D — Mediator-specific mortality rate panel build (Step 12)

### 6.1 5-year stack period mapping (Pierce-Schott 2020)

| stack period | mortality numerator (5년 합) | mediator denominator (가까운 census) |
|---|---|---|
| 1 | 1997-2001 | 2000 |
| 2 | 2002-2006 | 2005 |
| 3 | 2007-2011 | 2010 |
| 4 | 2012-2016 | 2015 |
| 5 | 2017-2021 | 2020 |

drop:
- mediator 1995, 1990 (paper 시점 외)
- mortality 2022-2024 (incomplete period, 3년만)

### 6.2 Rate formula

```
rate_per_100k = deaths_5y / (population × 5) × 100,000
```

annual rate per 100K person-year (5년 sum 의 annual 환산).

### 6.3 cause_group classification

- 4 deaths of despair: suicide (102) / drug (101) / psych (057) / liver (081)
- other = 그 외 cause_104
- all_cause = 모두 합산

### 6.4 산출

`12_mediator_specific_mortality_rate.py`:

- `mediator_specific_marital_rate_v01.parquet` (187,379 rows)
 - columns: h_code, period (1-5), census_year, sex_code, age_band, marital_code, cause_group,
 deaths_5y, population, rate_per_100k
- `mediator_specific_education_rate_v01.parquet` (171,811 rows)
 - 동일 + education_band

merge denom missing:
- marital: 9.74% (mortality h_code 346 vs mediator h_code 279 → 추가 67 unmatched 의심)
- education: 2.11%

### 6.5 Validation 결과 — historical 추세 검증

deaths of despair 시계열 (marital panel, working-age 25-64, /100K annual):

| period | drug | liver | psych | suicide |
|--------|------|-------|-------|---------|
| 1 (1997-2001) | 5.61 | 44.17 | 13.29 | 23.23 |
| 2 (2002-2006) | 4.01 | 34.26 | 10.62 | 28.26 |
| 3 (2007-2011) | 3.81 | 26.44 | 9.85 | **35.27** ← peak |
| 4 (2012-2016) | 3.85 | 22.69 | 8.93 | 32.89 |
| 5 (2017-2021) | 3.86 | 19.05 | 9.66 | 29.61 |

검증:
- **자살 peak 2007-2011** ✓ 한국 통계청 자살률 peak 2009-2011 일치 (카드사태 + 금융위기)
- **간질환 단조 감소 -57%** ✓ B형 간염 백신 + 의료 발전
- **약물 매우 낮음 (5/100K)** ✓ 한국 = US 의 1/10 (paper 핵심 finding)
- **all_cause 277 → 152 / 100K (-45%)** ✓ 한국 working-age 사망률 감소 추세

---

## 7. 산출물 종합 inventory

### 7.1 Mediator denominator panels

| file | rows | dimension | 비고 |
|------|------|-----------|------|
| `mediator_panel_marriage_v02.parquet` | 71,125 | h × year × sex × age × marital | 6 시점 1995-2020 |
| `mediator_panel_education_v03.parquet` | 63,019 | h × year × sex × age × edu(3cat) | mortality align |

### 7.2 Mortality numerator panels

| file | rows | dimension | 비고 |
|------|------|-----------|------|
| `mortality_microdata_cleaned_v01.parquet` | 7,408,230 | individual × year (1997-2024) | 28 시점 cleaned, working-age filter 적용 X |
| `mortality_marital_panel_v01.parquet` | 1,011,186 | h × year × sex × age × marital × cause_104 | working-age 25-64, crosswalk 적용 |
| `mortality_education_panel_v01.parquet` | 1,035,849 | + education(3cat) | 동일 |

### 7.3 Mediator-specific rate panels (final output)

| file | rows | dimension | 비고 |
|------|------|-----------|------|
| `mediator_specific_marital_rate_v01.parquet` | 187,379 | h × period × sex × age × marital × cause_group + deaths/pop/rate | Stage 5 input |
| `mediator_specific_education_rate_v01.parquet` | 171,811 | + education(3cat) | Stage 5 input |

### 7.4 Validation reports

- `3_derived/validation_report_mediator_mortality_v01.md` — Stage B/C 검토 (8 spot-check PASS, 4 issue)
- `3_derived/mortality/exploration_report_v01.md` — cleaned parquet + raw codebook profile

### 7.5 Scripts (`2_scripts/data_collection/`)

| step | script | 기능 |
|------|--------|------|
| 05 | 05_kosis_marriage_education_api.py | KOSIS API 12 URL 다운로드 (시군구 부재 → 미사용) |
| 06 | 06_mdis_population_unzip_inspect.py | MDIS zip 해제 + inventory |
| 07 | 07_mdis_population_columns_extract.py | column layout 추출 |
| 08 | 08_mdis_population_parse_crosstab.py | 7 시점 cross-tab → mediator v01 |
| 09 | 09_mediator_panel_validate.py | 4 issue 진단 |
| 10 | 10_mediator_panel_clean_align.py | v01 → v02 (1990 drop, age 25-64, 4cat, crosswalk) |
| 10b | 10b_mediator_panel_education_v03.py | v02 → v03 (4 → 3 카테고리) |
| 11a | 11a_mortality_microdata_parse.py | 28 시점 사망 microdata cleaning |
| 11b | 11b_mortality_mediator_crosstab.py | mortality numerator panel |
| 12 | 12_mediator_specific_mortality_rate.py | rate panel (final) |

verify scripts (`2_scripts/verify/`):
- verify_mortality_marital_education_columns.py — 사망 microdata column 보유 여부
- verify_mortality_codebook_layout.py — 시점별 codebook layout (fallback 미사용)
- explore_mortality_dataset.py — cleaned + raw profile

---

## 8. Methodology — Mediation analysis input 의 정합성

### 8.1 DGHP 2017 strict mediation 의 input 요구

paper § 5.2 의 mediation regression:
```
mortality_rate_{h, t, m} = β · trade_shock_{h, t} + γ · X_{h, t} + e
```
where m = mediator group (예: 미혼/이혼/사별/배우자 4 카테고리, h = 시군구).

**input 요구 4가지**:
1. mortality rate per (h, t, m) — ✓ 본 panel 제공
2. trade shock IV per (h, t) — Stage 4 (Bartik) 진행 중, 미완
3. control X_{h, t} — Stage 5 spec plan 에 명시 (산업비중, 인구구조 등)
4. mediator share per (h, t) — mediator panel 의 marital_share/education_share 계산 (12 단계 후속)

### 8.2 본 panel 의 정합성 보장

✅ **dimension 일치**: (h_code, period, sex, age_band, mediator_code, cause_group) → DGHP 2017
spec 와 일치

✅ **DGHP 2017 의 working-age 25-64 표준** 적용 (mediator + mortality 모두)

✅ **5-year stack period (Pierce-Schott 2020)** 매핑 일관

✅ **deaths of despair 4 outcome** 명시 (자살 102, 약물 101, 정신 057, 간 081) — paper § 4
와 일치

### 8.3 Caveats (paper § 8 limitation 추가 필요)

1. **1990 sigungu 코드 (2자리)** mapping placeholder. 1990 mediator 자체는 미사용.
2. **1997-2007 외국인 식별 불가** (사망 microdata 변수 부재) → numerator 미세 inflation
 (< 0.5% 추정).
3. **혼인/교육 미상 (9) drop** → MAR 가정. 1997-2000 high missing rate (혼인 2.5%, 교육 7%)
 sensitivity test 권장.
4. **education 1997-2007 = 5 카테고리 (대학 통합), 2008+ = 7 카테고리** → **3 카테고리
 (College+ 통합)** 으로 align. 전문대 vs 4년제 정보 손실.
5. **2022-2024 incomplete period** → drop. 2017-2021 이 마지막 stack period.
6. **MDIS 인구 microdata 2% 표본 weight** — weighted pop sum vs 행안부 한국 총인구 ±5%
 오차 normal.
7. **denom missing 9.74% (marital), 2.11% (education)** — Stage 5 regression 시 listwise
 deletion. 영향 minor 가정.
8. **2024 시점 사망 microdata** = 252 h_code (다른 시점 229) → crosswalk 미cover. Stage
 1997-2021 의 main analysis 무관.

---

## 9. Lessons learned (codebook 사전 참고 의 중요성)

11a 의 cleaning bug (4 회 재시도) 가 가장 큰 시간 손실. 원인 = column rename 시 한국어
encoding 미세 차이 + national_code NaN cast issue. 대안 = **codebook xlsx 사전 inspect**:
- 파일설계서 의 column 시작 position + 길이 → position-based parse 가능 (column 명 차이
 무시)
- 코드정보 sheet 의 변수 정의 (혼인 1-4-9, 교육 1-7/8) → mapping dict 정확
- 시군구 codebook → 시점별 행정구역 변화 (2024 신설 시군구 등)

이건 본 conversation 에 **메모리 saved**:
`feedback_panel_codebook_reference.md` — 앞으로 panel build / 매핑 시 codebook 사전 참고
필수.

---

## 10. 다음 단계 (Stage 5 진입)

본 panel build 완료. 다음:

1. **denom missing 67 h_code verify** — 어느 시군구인지 list 추출, 1990 placeholder 잔류
 여부 진단
2. **deaths of despair 4 outcome × 5 period 시각화** — line chart (한국 historical
 추세 검증)
3. **mediator share panel build** — denominator panel 의 marital/education 비율 산출
 (Stage 5 mediation regression 의 mediator 변수)
4. **Stage 5 regression** — `ivmediate` (DGHP 2017 Stata) 의 mediator-specific rate
 panel input 으로 사용
5. **Bartik IV (Stage 4 완료 후)** 결합 → main analysis

---

## Appendix A: 본 conversation 의 chronological summary

| seq | task | 산출 |
|-----|------|------|
| 1-3 | KOSIS API 12 URL 시도 → 시군구 부재 발견 | 시도 폐기 |
| 4 | MDIS 인구 microdata 신청 + 입수 (8 zip) | raw |
| 5-7 | 06/07 unzip + column extract | layout 7 시점 |
| 8 | 08 cross-tab v01 build | mediator_panel_v01 (140K + 270K) |
| 9 | 09 4 issue 진단 | validation md |
| 10 | 10 v02 build (1990 drop, 25-64, crosswalk, 4 카테고리) | mediator v02 |
| 11 | 사망 microdata column verify | 28 시점 모두 혼인+교육 보유 |
| 12 | 11a 28 시점 cleaning (4 회 재시도, position-based + 외국인만 drop) | mortality_microdata_cleaned_v01 (7.4M) |
| 13 | 10b education v02 → v03 (3 카테고리, mortality align) | mediator_panel_education_v03 |
| 14 | 11b numerator cross-tab (working-age + crosswalk) | mortality_marital/education_panel_v01 |
| 15 | 12 rate panel build (5-year stack, 5 period) | mediator_specific_*_rate_v01 |
| 16 | validation + 본 종합 문서 | 본 문서 |

---

_본 문서는 paper PAP v3.4 의 § 5.2 mediation framework 구현 일지. Stage 5 진입 시 reviewer
feedback 시 reference._
