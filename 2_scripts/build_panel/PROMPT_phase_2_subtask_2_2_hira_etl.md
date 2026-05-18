# Claude Code 위임 prompt — Phase 2 sub-task 2.2: HIRA pharmaceutical panel ETL

**작성**: 2026-05-07 R-A (공동저자 mode) → 정재헌 → Claude Code
**대상 박사논문**: Trade Exposure and Mortality in Export-Oriented Korea (KER July 2026 target)
**Phase**: 2 (mediator panel build) sub-task 2.2 (HIRA M1 ATC4 panel ETL)
**선행 의존성**: ✅ 1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv (168 mapped, 99.4%) + ✅ paper § 7.1.1 commit (n=146 intersection sample)
**후행 의존성**: sub-task 2.3 (M1 composite outcome variable) → sub-task 2.4 (DGHP ivmediate)
**예상 소요**: ~30-45분 (Python ETL + pandas + parquet write + 6-step verify)

---

## 본 paper context (Claude Code 가 이 prompt 만으로 작업 시작 가능하도록 self-contained)

본 paper 는 Korea-China bilateral trade integration (1994 baseline + 1997-1999 ↔ 2018-2022 long difference) 의 working-age deaths-of-despair mortality 에 대한 protective effect (β = -0.127, AKM-proper t = -4.92, Romano-Wolf p_RW = 0.0161 FWER pass) 를 sigungu × year panel 에서 추정. § 7 mechanism analysis 는 DGHP 2017 single-IV mediation framework 를 사용해 5개 active mediator (M1 HIRA pharmaceutical + M3 KOSIS family aggregates + M4 z_m_marital + M5 z_m_education + M6 KOSTAT suicide) 를 통한 protective channel decomposition 을 commit.

본 sub-task 는 M1 mediator (HIRA pharmaceutical prescription) 의 panel build 첫 단계. paper § 7.1.1 에서 main 221 sigungu ∩ HIRA 167 sigungu = 146 intersection sample 위에서 main β 가 substantively comparable (β_146 = -0.153, |Δβ|/SE_full = 0.969 < 1) 임을 verify 했으므로, 본 sub-task 의 output 은 146 intersection sample 의 sigungu × year × ATC4 panel.

---

## 1. 목적

HIRA pharmaceutical prescription 5 ATC4 × 167 sigungu × 2010-2019 raw data 를 sigungu × year × ATC4 long-form parquet panel 로 ETL.

---

## 2. Input files (정확한 absolute path)

| File | Description | 검증된 row 수 |
|------|-------------|---------------|
| `C:\Users\82103\Downloads\trade_mortality_korea\0_raw\hira_pharmaceutical\` | HIRA 5 ATC4 raw csv (Phase 1-F 다운 완료) | ~152,208 row 추정 |
| `C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\hira_sgguCd_to_hcode_crosswalk.csv` | HIRA sgguCd → KOSTAT h_code crosswalk (name-based, 99.4% coverage) | 168 row |
| `C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\intersection_main_hira_h_codes.csv` | 146 main ∩ HIRA intersection h_code list (paper § 7.1.1 검증) | 146 row |
| `C:\Users\82103\Downloads\trade_mortality_korea\0_raw\kosis_population\population_combined.csv` | KOSIS 인구 panel 1993-2023 (rate per 100K 계산용) | 516,750 row |

**ATC4 카테고리** (5개 active, 본 paper 검증된 spec):
- `N06AB` — Selective serotonin reuptake inhibitors (SSRI antidepressants)
- `N06AX` — Other antidepressants
- `N05BA` — Benzodiazepine derivatives (anxiolytics)
- `N05AX` — Other antipsychotics
- `A05BA` — Liver therapy drugs

**KOSTAT 사망원인 매핑** (composite M1 outcome 의 4-component, paper § 7.1.1):
- 4 mental-health ATC4 (N06AB, N06AX, N05BA, N05AX) → KOSTAT 057 (F10-F19) + 102 (X60-X84)
- 1 liver therapy ATC4 (A05BA) → KOSTAT 081 (K70-K77)

---

## 3. Output files (정확한 absolute path + schema)

### 3.1 Long-form ATC4 panel

`C:\Users\82103\Downloads\trade_mortality_korea\3_derived\hira_atc4_panel.parquet`

| Column | dtype | Description |
|--------|-------|-------------|
| `h_code` | int32 | KOSTAT 5-digit sigungu code (crosswalk 적용 후) |
| `year` | int16 | 2010-2019 |
| `atc4` | string | "N06AB" / "N06AX" / "N05BA" / "N05AX" / "A05BA" |
| `prescription_count` | float32 | HIRA raw prescription count |
| `working_age_pop_25_64` | float32 | KOSIS 인구 panel working-age 25-64 |
| `prescription_rate_per_100k` | float32 | (prescription_count / working_age_pop_25_64) * 1e5 |
| `in_intersection_146` | bool | True if h_code in 146 intersection sample |

예상 row 수: 5 × 167 × 10 = 8,350 (raw) → 5 × 146 × 10 = 7,300 (intersection 146 sigungu).

### 3.2 Wide-form ATC4 panel

`C:\Users\82103\Downloads\trade_mortality_korea\3_derived\hira_atc4_panel_wide.parquet`

| Column | dtype |
|--------|-------|
| `h_code`, `year`, `working_age_pop_25_64`, `in_intersection_146` | int32/int16/float32/bool |
| `n06ab_rate`, `n06ax_rate`, `n05ba_rate`, `n05ax_rate`, `a05ba_rate` | float32 |

예상 row 수: 167 × 10 = 1,670 (raw) → 146 × 10 = 1,460 (intersection).

---

## 4. Implementation steps

### Step 1: Load HIRA raw + crosswalk + intersection list

```python
import pandas as pd
from pathlib import Path

PROJ = Path("C:/Users/82103/Downloads/trade_mortality_korea")
RAW_HIRA = PROJ / "0_raw" / "hira_pharmaceutical"
CW = PROJ / "1_codebooks" / "hira_sgguCd_to_hcode_crosswalk.csv"
INTERSECT = PROJ / "1_codebooks" / "intersection_main_hira_h_codes.csv"
POP = PROJ / "0_raw" / "kosis_population" / "population_combined.csv"
OUT_DIR = PROJ / "3_derived"
OUT_DIR.mkdir(exist_ok=True)

hira_files = list(RAW_HIRA.glob("*.csv"))
print(f"HIRA raw files found: {len(hira_files)}")
for f in hira_files:
    print(f"  {f.name}")

cw = pd.read_csv(CW, encoding="utf-8")
print(f"crosswalk rows: {len(cw)}, cols: {cw.columns.tolist()}")

intersect = pd.read_csv(INTERSECT, encoding="utf-8")
intersect_h_codes = set(intersect['h_code'].astype(int))
print(f"intersection h_codes: {len(intersect_h_codes)}")
```

### Step 2: HIRA raw → long form

HIRA raw schema 사전 inspect 필수 (codebook reference 사전 inspect feedback). 가능한 cases:
- **Case A**: 단일 long csv with ATC4 column (preferred)
- **Case B**: 5 csv split by ATC4
- **Case C**: ATC4 × year wide form

```python
sample = pd.read_csv(hira_files[0], encoding="utf-8", nrows=5)
print(sample.head())
print(sample.dtypes)

# Long form 가정 (Case A):
hira_long = pd.concat([pd.read_csv(f, encoding="utf-8") for f in hira_files], ignore_index=True)
hira_long = hira_long.merge(cw, on="sgguCdNm", how="inner")  # name-based
print(f"after crosswalk merge: {hira_long.shape}")
```

### Step 3: KOSIS population join + rate per 100K

```python
pop = pd.read_csv(POP, encoding="utf-8")
print(f"KOSIS pop cols: {pop.columns.tolist()}")

# Working-age 25-64 = age_5y codes 6-13
pop_wa = pop[pop['age_band_code'].between(6, 13)]
pop_wa_agg = pop_wa.groupby(['h_code', 'year'])['value'].sum().reset_index()
pop_wa_agg.columns = ['h_code', 'year', 'working_age_pop_25_64']

hira_long = hira_long.merge(pop_wa_agg, on=['h_code', 'year'], how='left')
hira_long['prescription_rate_per_100k'] = (
    hira_long['prescription_count'] / hira_long['working_age_pop_25_64'].replace(0, pd.NA)
) * 1e5
```

### Step 4: Intersection flag + parquet write

```python
hira_long['in_intersection_146'] = hira_long['h_code'].astype(int).isin(intersect_h_codes)

hira_long_out = hira_long[[
    'h_code', 'year', 'atc4', 'prescription_count',
    'working_age_pop_25_64', 'prescription_rate_per_100k', 'in_intersection_146'
]]
hira_long_out.to_parquet(OUT_DIR / "hira_atc4_panel.parquet", index=False)

hira_wide = hira_long.pivot_table(
    index=['h_code', 'year', 'in_intersection_146', 'working_age_pop_25_64'],
    columns='atc4',
    values='prescription_rate_per_100k',
    aggfunc='first'
).reset_index()
hira_wide.columns = [c.lower() + ('_rate' if c.upper() in ['N06AB','N06AX','N05BA','N05AX','A05BA'] else '') for c in hira_wide.columns]
hira_wide.to_parquet(OUT_DIR / "hira_atc4_panel_wide.parquet", index=False)
```

### Step 5: Audit-after-action 6-step verify

```python
import os
print("\n=== Audit-after-action 6-step verify ===\n")

# 1. File integrity
for fn in ['hira_atc4_panel.parquet', 'hira_atc4_panel_wide.parquet']:
    fp = OUT_DIR / fn
    print(f"  {fn}: exists={fp.exists()}, size={os.path.getsize(fp)/1024:.1f} KB")

# 2. Schema check
expected_long = ['h_code','year','atc4','prescription_count','working_age_pop_25_64','prescription_rate_per_100k','in_intersection_146']
expected_wide = ['h_code','year','in_intersection_146','working_age_pop_25_64','n06ab_rate','n06ax_rate','n05ba_rate','n05ax_rate','a05ba_rate']
for fn, expected in [('hira_atc4_panel.parquet', expected_long), ('hira_atc4_panel_wide.parquet', expected_wide)]:
    df_chk = pd.read_parquet(OUT_DIR / fn)
    assert set(expected).issubset(set(df_chk.columns)), f"Missing in {fn}: {set(expected) - set(df_chk.columns)}"
    print(f"  {fn}: schema OK")

# 3. NaN profile
nan_rate = hira_long_out['prescription_rate_per_100k'].isna().mean()
print(f"  prescription_rate_per_100k NaN ratio: {nan_rate:.4f}")
assert nan_rate < 0.10, f"NaN ratio {nan_rate:.4f} > 10% threshold"

# 4. Intersection sample row count
intersect_rows = hira_long_out[hira_long_out['in_intersection_146']]
expected_intersect = 5 * 146 * 10
print(f"  intersection rows: {len(intersect_rows)} (expected {expected_intersect})")

# 5. Year coverage per sigungu
year_cov = hira_long_out.groupby('h_code')['year'].nunique()
print(f"  Year coverage min/median/max: {year_cov.min()}/{year_cov.median()}/{year_cov.max()}")

# 6. Outlier check by ATC4
for atc in ['N06AB', 'N06AX', 'N05BA', 'N05AX', 'A05BA']:
    sub = hira_long_out[hira_long_out['atc4']==atc]['prescription_rate_per_100k']
    print(f"  {atc}: median={sub.median():.0f}, p99={sub.quantile(0.99):.0f}, n_outlier={(sub > sub.quantile(0.99)).sum()}")

print("\n=== Verify complete ===")
```

---

## 5. 검증 commit 형식

작업 완료 후 다음 형식으로 보고:

```markdown
## Phase 2 sub-task 2.2 완료 — HIRA ATC4 panel ETL

**Output**:
- `3_derived/hira_atc4_panel.parquet` (long, n_rows = ?, size = ? KB)
- `3_derived/hira_atc4_panel_wide.parquet` (wide, n_rows = ?, size = ? KB)

**Verify 결과**:
- intersection 146 × 10 × 5 = 7,300 expected, actual = ?
- prescription_rate_per_100k NaN ratio: ?%
- ATC4 별 median / p99 / n_outlier: ...

**P1/P2/P3 issue**: ...

**다음 step**: Phase 2 sub-task 2.3 (M1 composite outcome variable)
```

---

## 6. 주의사항

1. **Crosswalk name-based**: HIRA sgguCd 의 6-digit 구조는 hierarchical sub-grouping. int(sgguCd/10) 변환 X. name-based matching (sgguCdNm) 만 사용.
2. **Rate denominator**: working-age 25-64 (age_5y codes 6-13).
3. **NaN 10% threshold**: 초과 시 P2 issue 보고.
4. **Year range**: 2010-2019 only.
5. **한자 사용 금지** (사용자 메모리).
6. **0_raw/ 절대 수정 X** (raw 데이터 commit).

---

## 7. 실행 명령

Claude Code 에 본 prompt 를 붙여넣고:

```
이 prompt 의 spec 대로 Python script 를 작성하고 실행해줘.
script: 2_scripts/build_panel/2_2_hira_atc4_etl.py
PowerShell wrapper: 2_scripts/build_panel/run_hira_atc4_etl.ps1
완료 후 verify 결과를 § 5 형식으로 보고.
```

---

**End of Claude Code 위임 prompt — 본 prompt 의 outputs/ 원본**:
`C:\Users\82103\AppData\Roaming\Claude\local-agent-mode-sessions\b2ac566b-eb8a-4089-82f5-2f6381cd4f6d\56af0025-aff0-4142-af78-7fd57175e97e\local_eb4f92d2-4def-433d-b666-e29cab4bb99b\outputs\phase_2_subtask_2_2_hira_etl_prompt.md`
