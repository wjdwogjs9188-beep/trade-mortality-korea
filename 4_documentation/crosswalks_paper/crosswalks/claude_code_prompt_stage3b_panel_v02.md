# Claude Code Prompt — Stage 3B Panel v02 재구성 (Tier A audit 처리)

## 작업 목적

Panel audit 의 Tier A 3 issue 처리:
1. **A.1 Component decomposition** — outcome_group 6 → 10 (suicide/drug/psych/liver 분리)
2. **A.2 인구 panel 외국인 처리** — 분모 = 주민등록 - 외국인등록 (내국인 only)
3. **A.3 KCD 정의 cross-check + COVID-057 verify**

추가 처리 (Tier B):
4. **B.4 age band 의미 정합성 검증** — KOSIS C3 360-440 코드 의미 확인
5. **B.5 D-1 standardization** — WHO 2000 + Eurostat 2013 baseline 추가
6. **B.6 분구 시계열 break** — 11 분구 시군구 분구 직전·직후 5년 비교

## 입력 파일

```
3_derived/mortality/mortality_microdata_combined.parquet  (7.3M records)
3_derived/mortality/mortality_panel_v01.parquet
3_derived/population/population_panel_v01.parquet
0_raw/kosis_foreign_residents/osis_foreign_residents_시군구_*.csv (3 파일, 2006-2024)
1_codebooks/sigungu_crosswalk_v2.csv
지역별 자살 데이터/사망원인통계_사망연간자료_코드집(8차질병분류코드).xlsx
지역별 자살 데이터/파일설계서(공공용)_사망원인통계_사망_연간자료_B형(제공)_2020(코드집포함).xlsx
```

## 산출물

```
3_derived/mortality/mortality_panel_v02.parquet              # outcome_group 10 개
3_derived/mortality/mortality_rate_panel_v02.parquet         # 분자 v02 + 분모 v02 (외국인 빼기)
3_derived/population/population_panel_v02.parquet            # 내국인 only
3_derived/mortality/mortality_panel_v02_validation.md
3_derived/mortality/mortality_rate_panel_v02_validation.md
3_derived/mortality/covid_057_audit_report.md                # COVID-057 verify 결과
3_derived/mortality/age_band_semantic_audit.md               # Tier B.4 검증
3_derived/mortality/sigungu_collapse_timeseries_break.md     # Tier B.6 검증
```

## Tier A.1 — Panel v02 Component Decomposition

### Step 1: cause_104 별 outcome_group 재정의

```python
OUTCOME_GROUPS_V02 = {
    "suicide_102":     {"102"},                    # 자살
    "drug_101":        {"101"},                    # 유독성 물질 불의의 중독
    "psych_057":       {"057"},                    # 정신활성물질 (COVID 처리는 Step 2 참조)
    "liver_081":       {"081"},                    # 간 질환
    "despair_total":   {"057", "081", "101", "102"},  # 합산 (robustness)
    "cancer":          {f"{i:03d}" for i in range(27, 48)},
    "cardiovascular":  {"067", "068", "069", "070"},
    "respiratory":     {f"{i:03d}" for i in range(73, 79)},
    "external_other":  {"097", "098", "099", "100", "103", "104"},
    "other":           "fallback",                 # 나머지 모두
}
```

**중요**: `despair_total` 은 합산 outcome 으로 separate row. Component 4 개와 별도. 즉 한 record 가 (예: 102 자살) 가 mortality panel 에 두 row (suicide_102 + despair_total) 로 표시. **이는 mutually exclusive 가 아닌 overlap 구조**.

→ 분석 시 회귀 spec 마다 다른 outcome (component 만 vs 합산만) 사용. mortality panel cell 의 합 ≠ total deaths.

### Step 2: COVID-057 verify

microdata 에서 cause_104=057 의 시계열 분포 확인:
```python
df = pd.read_parquet("mortality_microdata_combined.parquet")
covid_audit = df[df["cause_104"] == "057"].groupby("year")["deaths"].sum() if "deaths" in df.columns else \
              df[df["cause_104"] == "057"].groupby("year").size()
print(covid_audit)
```

**합격 기준**:
- 2020-2023 의 057 count 가 2010-2019 평균 ± 50% 이내 → COVID-057 codebook entry 는 typo (정신질환만)
- 2020-2023 의 057 count 가 폭증 (수배+) → COVID 합쳐있음 → microdata 에 별도 column (예: COVID flag) 또는 ICD-10 직접 코드로 분리 필요

산출: `covid_057_audit_report.md` (시계열 표 + 결론)

만약 COVID 합쳐있으면 **psych_057 outcome 에서 2020-2024 별도 처리** 또는 panel 명시.

### Step 3: ASR 계산 (모든 10 outcome × 시군구 × 연도 × 성)

기존 Stage 3A 의 logic 그대로 적용:
- 2010 한국 baseline within-sex weight (Σw=1 per sex)
- 17 unified age band
- ln_asr = log(asr + 1)

산출: `mortality_panel_v02.parquet` + `mortality_rate_panel_v02.parquet`

## Tier A.2 — 인구 panel v02 외국인 빼기

### Step 1: KOSIS 외국인등록 1B040A26 처리

3 파일 (2006, 2007-2015, 2016-2024) 각각 다른 format:
- 2006 단일 행 format
- 2007-2015: cell-level long format
- 2016-2024: 다른 format

각 파일 별 시군구 × 연도 × 성 × (가능하면 연령) → 외국인 인구 추출.

**주의**: 외국인등록인구는 한국의 이전 등록외국인만. 미등록 외국인 (불법체류 등) 미포함.

### Step 2: 1997-2005 처리

KOSIS 외국인등록 = 2006 부터 시작. 1997-2005 은 외국인 비율 < 1-2% 라 무시 가능 (한계 paper 명시). 두 옵션:
- (a) 1997-2005 분모 = 주민등록 그대로 (무시)
- (b) 1997-2005 분모 = 주민등록 × (1 - 외국인_2006_비율) (보수적 보정)

**권고: (a)**. 한계 명시 + 1997-2005 시기 외국인 < 2% 라 영향 미미.

### Step 3: population_panel_v02 build

```python
# Stage 3A logic 재사용
pop_panel_v01 = read_parquet("population_panel_v01.parquet")  # 주민등록 (외국인 포함)
foreign_panel = process_kosis_foreign(2006_csv, 2007_2015_csv, 2016_2024_csv)
# 시군구 × 연도 × 성 × age_band → 외국인 인구

# 분모 재구성
pop_panel_v02 = pop_panel_v01.merge(foreign_panel, on=["h_code", "year", "sex_code", "age_band"], how="left")
pop_panel_v02["foreign_pop"] = pop_panel_v02["foreign_pop"].fillna(0)  # 1997-2005 = 0 (무시)
pop_panel_v02["population"] = pop_panel_v02["population"] - pop_panel_v02["foreign_pop"]
pop_panel_v02 = pop_panel_v02[["h_code", "year", "sex_code", "age_band", "population"]]
```

### Step 4: mortality_rate_panel_v02 재계산

분자 = mortality_panel_v02 (10 outcome)
분모 = population_panel_v02 (내국인 only)

ASR + ln_asr 재계산 → `mortality_rate_panel_v02.parquet`

## Tier A.3 — KCD 정의 cross-check (R-A audit 결과)

이미 verify 완료:
- **057** = 정신활성물질 (F10-F19), 2020+ codebook entry COVID 추가 (typo 가능성, Step 2 verify)
- **081** = 간 질환 (K70-K77)
- **101** = 유독성 물질 불의의 중독 (X40-X49 broader)
- **102** = 자살 (X60-X84)

→ panel v02 OUTCOME_GROUPS 정의 정확. 단 1997-1999 cause_103 vs 2000+ cause_104 매핑 verify 필요.

### Step 1: 1997-1999 cause_103 ↔ cause_104 매핑

`파일설계서_(공공용)1997_1999년_사망원인통계_B형.xlsx` 의 "103항목" sheet 읽기. cause_103 = 057, 081, 101, 102 의 ICD-10 매핑 확인.

만약 1997-1999 cause_103 와 2000+ cause_104 의 057 (정신활성물질) 정의 다르면 panel 의 1997-1999 처리 점검 필요 (Stage 2 v4 가 어떻게 처리했는지).

산출: `cause_103_to_104_mapping.md`

## Tier B.4 — Age Band 의미 정합성 검증

### Step 1: KOSIS C3 360-440 코드 의미 확인

KOSIS DT_1B040M5 의 C3 코드 list:
- 020 = 0-4세
- 050 = 5-9세
- ...
- 340 = 80+ aggregate
- **360, 370, 380 = ?** (Stage 3 에서 제외했음)
- **410, 430, 440 = ?** (Stage 3 에서 제외했음)

KOSIS 사이트 또는 codebook 에서 정확 의미 확인. 만약 360+ 가 80-84/85-89/90+/95+/100+ 세부 분리이고 340 = 80+ aggregate 라면 panel 정확 ✅.

만약 다른 의미 (예: 외국인 또는 군병력) 면 panel silent error.

### Step 2: KOSTAT age 1+2 vs KOSIS 020 의미 동일성

KOSTAT age 1 = 0세, age 2 = 1-4세.
KOSIS C3 020 = 0-4세 단일.
→ panel 의 mortality 01_02 band = (1+2 합) vs population 01_02 band = (020) — 의미 동일 ✅.

### Step 3: KOSTAT 18+19+20 vs KOSIS 340 의미 동일성

KOSTAT age 18 = 80-84세, 19 = 85-89세, 20 = 90+세.
KOSIS C3 340 = 80+ aggregate.
→ mortality 18_19_20 band = (18+19+20 합) vs population 18_19_20 = (340 aggregate) — 의미 동일 ✅.

산출: `age_band_semantic_audit.md`

## Tier B.5 — D-1 Standardization (WHO 2000 + Eurostat 2013)

### Step 1: WHO 2000 World Standard Population

WHO 2000 standard age weights:
```
0-4: 0.0886, 5-9: 0.0869, 10-14: 0.086, 15-19: 0.0847, 20-24: 0.0822,
25-29: 0.0793, 30-34: 0.0761, 35-39: 0.0715, 40-44: 0.0659, 45-49: 0.0604,
50-54: 0.0537, 55-59: 0.0455, 60-64: 0.0372, 65-69: 0.0296, 70-74: 0.0221,
75-79: 0.0152, 80+: 0.0152
```

→ 17 age band 와 매핑. ASR 계산 시 within-sex 가중 = world standard.

### Step 2: Eurostat 2013 European Standard Population

Eurostat 2013 standard:
```
0-4: 0.05, 5-9: 0.055, 10-14: 0.055, 15-19: 0.055, 20-24: 0.06,
25-29: 0.06, 30-34: 0.065, 35-39: 0.07, 40-44: 0.07, 45-49: 0.07,
50-54: 0.07, 55-59: 0.0625, 60-64: 0.06, 65-69: 0.055, 70-74: 0.05,
75-79: 0.04, 80+: 0.05
```

산출: `mortality_rate_panel_v02.parquet` 에 다음 columns:
- asr_per_100k (2010 한국, main)
- asr_who_2000_per_100k (sensitivity)
- asr_eurostat_2013_per_100k (sensitivity)
- ln_asr, ln_asr_who, ln_asr_eurostat

## Tier B.6 — 분구 시계열 Break 검증

### Step 1: 11 분구 시군구 list

```python
SIGUNGU_COLLAPSE_CASES = {
    "31050": {"city": "부천시", "split_year": "?"},
    "34010": {"city": "천안시", "split_year": "?"},
    "35010": {"city": "전주시", "split_year": "?"},
    "37010": {"city": "포항시", "split_year": "?"},
    "33020": {"city": "청주시", "split_year": 2014},  # 통합 청주
    "41110": {"city": "수원시", "split_year": "?"},
    "41130": {"city": "성남시", "split_year": "?"},
    "41170": {"city": "안양시", "split_year": "?"},
    "41190": {"city": "안산시", "split_year": "?"},
    "41280": {"city": "고양시", "split_year": "?"},
    "41460": {"city": "용인시", "split_year": "?"},
    "38110": {"city": "통합창원시", "split_year": 2010},  # 통합 창원
}
```

### Step 2: 분구 직전·직후 5년 평균 사망률 비교

```python
for h_code, info in SIGUNGU_COLLAPSE_CASES.items():
    pre_5yr = mortality_rate_panel_v02[
        (panel.h_code == h_code) &
        (panel.year.between(split_year - 5, split_year - 1))
    ]["asr_per_100k"].mean()
    post_5yr = mortality_rate_panel_v02[
        (panel.h_code == h_code) &
        (panel.year.between(split_year + 1, split_year + 5))
    ]["asr_per_100k"].mean()
    diff_pct = (post_5yr - pre_5yr) / pre_5yr * 100
    # > ±20% 면 break 의심
```

### Step 3: split_year 모르는 케이스

각 분구 시군구의 정확한 분구 시점 확인 필요:
- 통합창원: 2010 (verified)
- 통합 청주: 2014 (verified)
- 나머지 9 개: 한국 행정구역 개편 history 참조 (위키피디아 또는 행정안전부)

산출: `sigungu_collapse_timeseries_break.md` (각 분구 케이스별 결과 + abrupt break 여부)

## 검증 V1-V12

V1-V9: Stage 3A 와 동일 (인구 합 보존, 229 sigungu, 27 year, 17 age band, KOSIS V5 cross-check, ASR 시계열, join coverage, deaths 합 보존, weight 합)

**V10 (신규)** - Component decomposition mutually exclusive:
- suicide_102 + drug_101 + psych_057 + liver_081 = despair_total (정확 일치)
- 모든 component sum = total deaths (other 포함)

**V11 (신규)** - 외국인 빼기 정확성:
- 2006-2024 의 시군구별 (주민등록 - 외국인등록) > 0 모두 (음수 cell 0 개)
- 외국인 빼기 후 KOSIS 추계인구 (외국인 미포함 추정) 와 ±2% 이내

**V12 (신규)** - COVID-057 audit:
- cause_104=057 시계열 1997-2023 분포
- 2020-2023 spike 여부

## Expected 결과

- panel v02: ~123,660 rows (229 × 27 × 2 × 10 outcome)
- rate panel v02: ~123,660 rows (3 baseline asr + ln_asr × 3)
- pop panel v02: ~210,222 rows (외국인 빼기 후)
- 모든 V1-V12 PASS

## 결과 검토

다음 5가지 본인 검증:
1. mortality_panel_v02 의 outcome_group 10 개 cover
2. mortality_rate_panel_v02 의 3 baseline asr columns
3. population_panel_v02 의 1997-2005 분모 = 주민등록 (외국인 빼기 안 함)
4. COVID-057 audit 결과 (typo / 진짜 합쳐 / 시계열 분포)
5. 분구 시계열 break audit 결과 (11 케이스 별 abrupt break 여부)

위 5개 OK 면 panel v02 채택 + Stage 5 진입.

---

이 prompt 를 Claude Code 에 file path 로 전달:
`C:\Users\82103\Desktop\뉴 논문\crosswalks\claude_code_prompt_stage3b_panel_v02.md`
