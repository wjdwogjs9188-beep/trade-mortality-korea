# Claude Code Prompt — Stage 3 인구 Panel Build (v1)

## 작업 목적

KOSIS 주민등록인구 raw 를 처리하여 시군구 × 연도 × 성 × 연령 인구 panel 을 구축.
Stage 2 mortality panel 과 join 하여 사망률 (per 100k) 계산 및 연령 표준화 (2010 한국 baseline).
최종 산출물: `mortality_rate_panel_v01.parquet` (회귀 분석에 직접 사용 가능한 형태).

## 입력 파일

- `0_raw/kosis_population/population_combined.csv` (KOSIS 주민등록인구, 약 516,750 rows)
- `1_codebooks/sigungu_crosswalk_v2.csv` (229 시군구 매핑)
- `3_derived/mortality/mortality_panel_v01.parquet` (Stage 2 v4 결과, 1,483,920 cells)

## 출력 파일

```
3_derived/population/population_panel_v01.parquet     # 시군구×연도×성×연령 인구 panel
3_derived/population/population_panel_validation.md   # 검증 보고서
3_derived/mortality/mortality_rate_panel_v01.parquet  # 사망률 panel (per 100k + log)
3_derived/mortality/mortality_rate_validation.md      # 사망률 검증 보고서
```

---

## 처리 단계

### Step 1: KOSIS population_combined.csv 처리

```python
import pandas as pd
pop = pd.read_csv("0_raw/kosis_population/population_combined.csv", dtype=str)
# 컬럼: C1 (시군구 5-digit), C2 (성: 0=계, 1=남, 2=여),
#       C3 (연령: 020=0-4세, ..., 340=80+세, 000=계, 410+=불필요한 세부 행),
#       year, population
```

**필터 1**: C1 이 5자리인 행만 (시도/전국 합계 행 제외).
```python
pop = pop[pop["C1"].str.len() == 5]
```

**필터 2**: C2 in {"1", "2"} 만 (계 행 제외, 남녀만 사용).
```python
pop = pop[pop["C2"].isin(["1", "2"])]
```

**필터 3**: C3 가 5세 단위 코드 (020, 050, 070, 100, 120, 130, 150, 160, 180, 190, 210, 230, 260, 280, 310, 330, 340) 인 행만.
```python
KOSIS_AGE_CODES_VALID = {
    "020", "050", "070", "100", "120", "130",
    "150", "160", "180", "190", "210", "230",
    "260", "280", "310", "330", "340"
}
pop = pop[pop["C3"].isin(KOSIS_AGE_CODES_VALID)]
```

**참고**: KOSIS C3 코드의 정확한 의미:
- `020` = 0-4세, `050` = 5-9세, `070` = 10-14세, `100` = 15-19세,
- `120` = 20-24세, `130` = 25-29세, `150` = 30-34세, `160` = 35-39세,
- `180` = 40-44세, `190` = 45-49세, `210` = 50-54세, `230` = 55-59세,
- `260` = 60-64세, `280` = 65-69세, `310` = 70-74세, `330` = 75-79세,
- **`340` = 80세 이상** (단일 통합 코드, 80+).
- `000` = 계 (제외), `410`/`420`/`430` = 90+ 세부 (사용 안 함, 340 안에 이미 포함).

### Step 2: KOSTAT age 1-20 → KOSIS C3 매핑 dict

Stage 2 mortality panel 은 KOSTAT 5세 코드 1-20 사용. 인구는 KOSIS C3 사용. 양자 alignment 필요.

```python
# KOSTAT age_5yr_code (1-20) → KOSIS C3 매핑
# KOSTAT 1 (0세) + 2 (1-4세) → KOSIS 020 (0-4세, 합쳐야 함)
# KOSTAT 18 (80-84) + 19 (85-89) + 20 (90+) → KOSIS 340 (80+, 합쳐야 함)
# 나머지는 1:1

# Population side: KOSIS C3 → 통합 KOSTAT-aligned age_5yr_code
KOSIS_TO_KOSTAT_AGE = {
    "020": "01_02",   # 0-4세 (KOSTAT 1+2 합)
    "050": "03",      # 5-9세
    "070": "04",      # 10-14세
    "100": "05",      # 15-19세
    "120": "06",      # 20-24세
    "130": "07",      # 25-29세
    "150": "08",      # 30-34세
    "160": "09",      # 35-39세
    "180": "10",      # 40-44세
    "190": "11",      # 45-49세
    "210": "12",      # 50-54세
    "230": "13",      # 55-59세
    "260": "14",      # 60-64세
    "280": "15",      # 65-69세
    "310": "16",      # 70-74세
    "330": "17",      # 75-79세
    "340": "18_19_20" # 80+ (KOSTAT 18+19+20 합)
}

# Mortality side: KOSTAT 1-20 → 동일 통합 코드
KOSTAT_TO_UNIFIED_AGE = {
    "1": "01_02", "2": "01_02",
    "3": "03", "4": "04", "5": "05", "6": "06", "7": "07",
    "8": "08", "9": "09", "10": "10", "11": "11", "12": "12",
    "13": "13", "14": "14", "15": "15", "16": "16", "17": "17",
    "18": "18_19_20", "19": "18_19_20", "20": "18_19_20"
}
```

**결과**: 양쪽 모두 17개 통합 age band 사용 (`age_band` 컬럼).

### Step 3: Sigungu crosswalk 매핑

```python
xw = pd.read_csv("1_codebooks/sigungu_crosswalk_v2.csv", dtype=str)
# raw_code (KOSIS/KOSTAT 5-digit) → h_code (229 통합 시군구)

# Population merge
pop["h_code"] = pop["C1"].map(xw.set_index("raw_code")["h_code"].to_dict())
unmatched = pop[pop["h_code"].isna()]
# unmatched 출력: 어떤 raw_code 가 crosswalk 에 없는지 진단
```

매핑 안 된 행이 있으면 진단 후 처리 (보통 행정구역 신설/폐지 케이스, year × raw_code 조합 검토).

### Step 4: Population panel collapse

```python
# 분구 시군구 collapse (예: 수원시 4개 자치구 → 41110 통합 수원시)
pop["population"] = pop["population"].astype(float)
pop["age_band"] = pop["C3"].map(KOSIS_TO_KOSTAT_AGE)
pop_panel = pop.groupby(["h_code", "year", "C2", "age_band"], as_index=False)["population"].sum()
pop_panel = pop_panel.rename(columns={"C2": "sex_code"})
# 산출: h_code × year × sex_code × age_band → population
```

저장: `3_derived/population/population_panel_v01.parquet`.

### Step 5: Mortality panel + age band 통합

```python
mort = pd.read_parquet("3_derived/mortality/mortality_panel_v01.parquet")
mort["age_band"] = mort["age_5yr_code"].map(KOSTAT_TO_UNIFIED_AGE)
mort_band = mort.groupby(
    ["h_code", "year", "sex_code", "age_band", "outcome_group"],
    as_index=False
)["deaths"].sum()
# 1,483,920 / 20 age × 17 band ≈ 1,261,332 cells (예상)
```

### Step 6: Mortality × Population join → rate

```python
panel = mort_band.merge(pop_panel, on=["h_code", "year", "sex_code", "age_band"], how="left")
# 인구 결측 진단
n_missing = panel["population"].isna().sum()
# 0 또는 매우 작은 수여야 함 (행정구역 변동 케이스)

panel["rate_per_100k"] = panel["deaths"] / panel["population"] * 100_000
# 0 cell 처리: 인구 0 인 경우 rate = NaN, 인구 양수 + 사망 0 인 경우 rate = 0
panel.loc[panel["population"] == 0, "rate_per_100k"] = pd.NA
```

### Step 7: 연령 표준화 (2010 한국 baseline)

```python
# 2010 한국 전체 인구의 age_band × sex 분포를 표준 인구로 사용
ref_2010 = pop_panel[pop_panel["year"] == "2010"].groupby(
    ["sex_code", "age_band"], as_index=False
)["population"].sum()
ref_2010["weight"] = ref_2010.groupby("sex_code")["population"].transform(
    lambda x: x / x.sum()
)
# weight: 같은 성 안에서 age_band 비중

# 표준화 사망률: sigungu × year × sex × outcome 단위
panel = panel.merge(
    ref_2010[["sex_code", "age_band", "weight"]],
    on=["sex_code", "age_band"], how="left"
)
# 직접 표준화 (Direct standardization):
# ASR = Σ (rate_age × weight_age)
asr = panel.groupby(["h_code", "year", "sex_code", "outcome_group"]).apply(
    lambda g: (g["rate_per_100k"] * g["weight"]).sum()
).reset_index(name="asr_per_100k")
```

### Step 8: 로그 변환

```python
asr["ln_asr"] = (asr["asr_per_100k"] + 1).apply(lambda x: pd.NA if pd.isna(x) else __import__("math").log(x))
# 또는 numpy: np.log(asr["asr_per_100k"] + 1)
```

저장: `3_derived/mortality/mortality_rate_panel_v01.parquet` (h_code × year × sex × outcome 단위, asr_per_100k + ln_asr 포함).

### Step 9: 검증

#### V1 — KOSIS 인구 합 보존
```python
# Filter 전후 합 비교 (계 행 제외 후 남녀 합 = 원본 계 행 합)
# 시군구 collapse 전후 합 보존
total_raw = float(pop_filtered_before_collapse["population"].sum())
total_panel = float(pop_panel["population"].sum())
assert abs(total_raw - total_panel) / total_raw < 1e-6
```

#### V2 — 229 시군구 cover
```python
n_h = pop_panel["h_code"].nunique()
assert n_h == 229
```

#### V3 — Year cover (1997-2023, 27 years)
```python
years = sorted(pop_panel["year"].unique())
assert len(years) == 27
```

#### V4 — Age band cover
```python
bands = sorted(pop_panel["age_band"].unique())
expected = ["01_02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18_19_20"]
assert set(bands) == set(expected)
```

#### V5 — KOSIS 공식 한국 총인구 cross-check
```python
KOREAN_POP_OFFICIAL = {
    "2000": 47_008_000,
    "2010": 49_410_000,
    "2015": 51_015_000,
    "2020": 51_836_000,
    "2023": 51_753_000
}
for y, official in KOREAN_POP_OFFICIAL.items():
    panel_total = pop_panel[pop_panel["year"]==y]["population"].sum()
    diff_pct = abs(panel_total - official) / official * 100
    assert diff_pct < 2.0, f"{y}: panel={panel_total:.0f}, official={official}, diff={diff_pct:.2f}%"
```

#### V6 — 사망률 sanity check
```python
# 한국 자살률 ASR (전국 합계 가중)
suicide_asr = asr[asr["outcome_group"]=="despair_total"]
# 가중 평균: 시군구 인구 가중
# 2010 자살률 (despair_total) 약 35-40/100k 예상 (despair = 자살+약물+정신+간 합)
```

#### V7 — Mortality panel join coverage
```python
n_mort_cells = mort_band.shape[0]
n_joined = panel[panel["population"].notna()].shape[0]
join_coverage = n_joined / n_mort_cells * 100
assert join_coverage > 99.5, f"Join coverage {join_coverage:.2f}% (목표 99.5%+)"
```

#### V8 — Age band 매핑 무결성
```python
# Mortality 에서 age band 적용 후 deaths 합 보존
total_mort_orig = mort["deaths"].sum()
total_mort_band = mort_band["deaths"].sum()
assert total_mort_orig == total_mort_band
```

#### V9 — Standardization weight 합 = 1
```python
for sex in ["1", "2"]:
    w_sum = ref_2010[ref_2010["sex_code"]==sex]["weight"].sum()
    assert abs(w_sum - 1.0) < 1e-9
```

---

## 주의 사항

1. **C2='0' (계) 행 절대 사용 금지** — 남녀 따로 사용. C2='0' 은 cross-check 용도만.
2. **C3='000' (총합) 및 410+ (90+ 세분) 행 제외** — 17개 5세 band 만 사용.
3. **80+ 통합**: KOSIS C3 340 = 80세 이상 단일 코드. KOSTAT 18, 19, 20 모두 합쳐서 80+ band 로.
4. **0-4세 통합**: KOSIS 020 = 0-4세 단일 코드. KOSTAT 1 (0세) + 2 (1-4세) 합쳐서 0-4 band 로.
5. **인구 0 cell 처리**: 인구 0 + 사망 0 → rate = 0 (정상). 인구 0 + 사망 > 0 → 데이터 오류 (진단 필요).
6. **분구 collapse**: population panel 도 sigungu_crosswalk_v2 매핑으로 11개 일반시 자치구 → 통합시로 collapse.
7. **연령 표준화 baseline**: 2010 한국 인구 (남녀 별도 표준 인구). 회귀 분석 시 일관 사용.
8. **Log 변환**: `ln(asr + 1)` 사용. 0 cell handling.

---

## Expected 결과

- `population_panel_v01.parquet`: 약 105,000 rows (229 × 27 × 2 × 17 = 210,222 — 일부 결측 가능)
- `mortality_rate_panel_v01.parquet`: 약 74,000 rows (229 × 27 × 2 × 6 outcomes = 74,196)
- 한국 총인구 V5 cross-check 5/5 PASS (모두 ±2% 이내)
- 자살 ASR 시계열 패턴 V6: 한국 historical pattern 일치
- Join coverage > 99.5%
- 모든 V1-V9 PASS

---

## 결과 검토

다음 7가지 본인이 직접 검증:

1. `population_panel_v01.parquet` 행 수 약 105,000–210,000 (229×27×2×17 = 210,222 max)
2. KOSIS V5 cross-check (2000, 2010, 2015, 2020, 2023) 모두 ±2% 이내
3. 229 sigungu 모두 cover (V2)
4. 27 year (1997-2023) 모두 cover (V3)
5. 17 age band 모두 cover (V4)
6. Mortality join coverage > 99.5% (V7)
7. ASR 자살률 시계열 한국 pattern (2010 ~31, 2017 ~24, 2023 ~27) 일치

위 7개 OK 면 Stage 3 v1 채택. 다음 단계:
- **Stage 4**: 무역 IV panel build (KSIC2 → 시군구 산업 비중 + KR-CN bilateral net export)
- **Stage 5**: 회귀 분석 (5-year stacked first-difference 2SLS)

---

이 prompt 를 Claude Code 에 file path 로 전달:
`C:\Users\82103\Desktop\뉴 논문\crosswalks\claude_code_prompt_stage3_population_panel.md`
