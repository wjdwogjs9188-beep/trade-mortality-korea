# Claude Code 위임 prompt — Phase 2 sub-task 2.5: M3 + M4 + M5 + M6 mediator panel build + analysis

**작성**: 2026-05-07 R-A (공동저자 mode) → 정재헌 → Claude Code
**대상 박사논문**: Trade Exposure and Mortality in Export-Oriented Korea (KER July 2026 target)
**Phase**: 2 sub-task 2.5 (4 active mediator: M3 KOSIS family + M4 cohort sex ratio + M5 education distance + M6 suicide validation)
**선행 의존성**: ✅ sub-task 2.4 (DGHP framework + N05BA single-mediator + 5 ATC4 reduced-form decomposition)
**후행 의존성**: paper § 7.3-7.5 narrative finalization
**예상 소요**: ~120-180분 (4 mediator ETL + analysis 합본)

**Strict workflow anchor**: 본 prompt 의 모든 substantive 분석 (regression, ETL, bootstrap, mediator decomposition) 은 사용자 측 Spyder + Claude Code 환경 위 직접 실행 + 결과 paste form. R-A sandbox 위 substantive 분석 부재 (memory: feedback_no_sandbox_analysis.md).

---

## 본 paper context (self-contained)

본 paper § 7 mechanism analysis 의 active mediator set: M1, M3, M4, M5, M6 (M2 deprecated). M1 N05BA single-mediator pathway 위 ACME = -0.025 (13.4% of β_RF = -0.185). 본 sub-task 2.5 는 나머지 4 mediator 의 cumulative form:

- **M3 KOSIS family aggregates**: 시군구 × year 위 marriage rate + divorce rate + fertility rate 의 cumulative form. 시간변동 mediator → DGHP framework valid path
- **M4 z_m_marital**: MDIS census 1975-1995 cohorts 의 pre-determined sigungu-level cohort sex ratio. 시점 invariant pre-determined mediator → effect modifier path
- **M5 z_m_education**: KEDI 1985 yearbook (171 four-year universities) 의 sigungu-level minimum distance to nearest university. 시점 invariant pre-determined mediator → effect modifier path. paper § 6.4 sensitivity: 1985/1990/1995 baseline Pearson r ≥ 0.989
- **M6 KOSTAT suicide rate**: sigungu_mortality_panel_v02_wa.parquet 위 outcome_group = '자살' (KOSTAT 102, X60-X84). validation channel (suicide is a sub-component of despair_total composite — direct mortality outcome rather than mediator)

paper § 7.3 = M3 + M4, § 7.4 = M5, § 7.5 = M6 의 cumulative form.

---

## 1. 목적

4 active mediator (M3 + M4 + M5 + M6) 의:
1. ETL: raw → sigungu × year (M3) 또는 sigungu pre-determined (M4 + M5) 또는 sigungu × year suicide (M6) panel
2. First-stage F: z_x → 각 mediator (시간변동 mediator M3 만 applicable; M4/M5 pre-determined → effect modifier 만)
3. Reduced-form mediator regression: 각 mediator → mortality (control z_x)
4. DGHP decomposition: M3 (where first-stage strong) + N05BA + multi-mediator joint
5. Effect modifier check: M4 + M5 위 z_x × M_pre interaction term
6. paper § 7.3-7.5 narrative draft prep

---

## 2. Input files (Windows path)

| Mediator | Raw path | 영역 |
|----------|----------|------|
| M3 KOSIS family | `0_raw\kosis_family_mediators\` | KOSIS 시군구 단위 가족통계 (혼인/이혼/출산) |
| M3 보조 | `0_raw\kosis_marriage_education\` | 혼인-교육수준 cross-tab |
| M4 birth sex ratio | `0_raw\kosis_birth_sex_ratio\` | 시군구 × year × 성별 출생 |
| M4 MDIS census | (raw 부재 시 KOSIS API 위 census 1975-1995 재build) | 시군구 × cohort × sex 인구 |
| M5 KEDI 1985 | `0_raw\1985_yunbo_total\` | 1985 한국교육통계연보 |
| M5 KEDI 1990 | `0_raw\1990_yunbo_total\` | sensitivity baseline |
| M5 KEDI 1995 | `0_raw\1995_yunbo_total\` | sensitivity baseline |
| M5 보조 university list | `0_raw\edu_university_list_1990\` | 대학 목록 supplementary |
| M6 mortality | `8_submission\paper_v01_submission\01_mortality\sigungu_mortality_panel_v02_wa.parquet` | KOSTAT 사망 panel (자살 X60-X84) |
| Common: IV | `8_submission\paper_v01_submission\02_bartik_iv\iv_z_x_bilateral.parquet` | z_x_per_worker |
| Common: 시군구 crosswalk | `1_codebooks\sigungu_crosswalk.csv` | h_code harmonization |
| Common: KOSIS 인구 | `0_raw\kosis_population\population_combined.csv` | rate denominator (working-age 25-64) |

---

## 3. Output files (Windows path)

### M3 KOSIS family panel
`3_derived/m3_kosis_family_panel.parquet` (sigungu × year, columns: marriage_rate, divorce_rate, fertility_rate)
`3_derived/m3_delta_panel.parquet` (sigungu, columns: delta_marriage, delta_divorce, delta_fertility)

### M4 z_m_marital
`3_derived/m4_z_marital_pre.parquet` (sigungu, columns: cohort_sex_ratio_1975, cohort_sex_ratio_1985, cohort_sex_ratio_1995, z_m_marital)

### M5 z_m_education
`3_derived/m5_z_education_pre.parquet` (sigungu, columns: dist_nearest_univ_1985, z_m_education_1985, z_m_education_1990, z_m_education_1995)

### M6 KOSTAT suicide
`3_derived/m6_suicide_panel.parquet` (sigungu, columns: log_suicide_rate_baseline, log_suicide_rate_endpoint, delta_log_suicide)

### Multi-mediator joint analysis
`4_results/m3_m6_first_stage_table.parquet` (mediator, γ_FS, F, p, sample_n)
`4_results/m3_m6_reduced_form_table.parquet` (mediator, β, se_hc1, se_cluster, t_cluster, p_cluster, sample_n)
`4_results/multi_mediator_dghp_decomposition.parquet` (mediator, ACME_point, ACME_CI_lo, ACME_CI_hi, ACME_proportion)

---

## 4. Implementation steps

### 4.1 M3 KOSIS family ETL (`2_5a_m3_kosis_family.py`)

```python
import pandas as pd
import numpy as np
from pathlib import Path

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
M3_RAW = PROJ / "0_raw" / "kosis_family_mediators"

# Step 1: Inventory raw csv files
csvs = list(M3_RAW.glob("*.csv"))
print(f"M3 raw CSVs: {[f.name for f in csvs]}")

# Step 2: Read + identify columns (사용자 메모리 feedback: codebook 사전 inspect)
for f in csvs[:3]:
    df = pd.read_csv(f, encoding='utf-8', nrows=5)
    print(f"\n{f.name}: {df.columns.tolist()}")
    print(df.head().to_string())

# Step 3: Build sigungu × year panel for marriage / divorce / fertility
# (각 raw csv 의 schema 위 적합한 reshape 필요)
# ...

# Step 4: Long-difference (1997-1999 baseline ↔ 2018-2022 endpoint) sigungu-level
# Mirror main spec window
# ...

# Step 5: parquet commit
```

### 4.2 M4 z_m_marital ETL (`2_5b_m4_cohort_sex_ratio.py`)

```python
# z_m_marital = sigungu-level pre-determined cohort sex ratio
# from MDIS census 1975 / 1985 / 1995 cohorts
# (만약 MDIS 직접 access 부재 시 KOSIS 시군구 × cohort × sex 인구 통계 위 재build)

# Definition: sigungu h 의 cohort c 위
#   sex_ratio_h_c = (male population h, c at census) / (female population h, c at census)
# z_m_marital_h = z-score of sex ratio across sigungu (pooled cohorts 1975-1995 or specific cohort 1985 main)

# Step 1: Read kosis_birth_sex_ratio raw
# Step 2: aggregate by sigungu + cohort
# Step 3: compute z_m_marital
# Step 4: parquet commit
```

### 4.3 M5 z_m_education ETL (`2_5c_m5_university_distance.py`)

```python
# z_m_education = sigungu-level minimum distance to nearest 4-year university
# from KEDI 1985 yearbook (171 universities)

# Step 1: Read 1985_yunbo_total raw
# Identify university rows (4-year, exclude technical / vocational)
# Extract: name, address (또는 sigungu code if available), latitude/longitude (Haversine)

# Step 2: Sigungu centroid lookup (or sigungu_crosswalk + KOSIS 시군구 좌표)
# Step 3: Compute Haversine distance from each sigungu centroid to nearest university
# Step 4: z-score: z_m_education = z(min_dist) (or 1/min_dist for "access" form)
# Step 5: Sensitivity: 1990 + 1995 baselines (paper § 6.4 cumulative anchor: r ≥ 0.989)
# Step 6: parquet commit

# Reference: paper § 6.4 narrative (이미 commit 됨)
# Pearson(1985, 1990) = 0.989; Pearson(1990, 1995) = 1.000; Pearson(1985, 1995) = 0.989
# Mean nearest-university distance: 1985 = 18.10 km, 1990 = 17.81 km, 1995 = 17.81 km
```

### 4.4 M6 KOSTAT suicide validation (`2_5d_m6_suicide.py`)

```python
import pandas as pd
import numpy as np
from pathlib import Path

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")

mort = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/01_mortality/sigungu_mortality_panel_v02_wa.parquet")
print(f"mortality outcome_group distinct: {mort['outcome_group'].unique()}")

# Step 1: Filter outcome_group == '자살' (KOSTAT code 102, X60-X84)
suicide = mort[mort['outcome_group'].str.contains('자살|suicide', na=False)]

# Step 2: Long-difference (1997-1999 ↔ 2018-2022)
# log_suicide_rate = log(deaths / pop_wa + 1e-6)
# delta_log_suicide_h = log_suicide_2018-2022 - log_suicide_1997-1999

# Step 3: parquet commit
```

### 4.5 Multi-mediator analysis (`2_5e_multi_mediator_analysis.py`)

```python
"""4 mediator first-stage + reduced-form + DGHP decomposition cumulative."""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from pathlib import Path

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")

# Step 1: Load all 4 mediator panels + IV + mortality
m3 = pd.read_parquet(PROJ / "3_derived/m3_delta_panel.parquet")
m4 = pd.read_parquet(PROJ / "3_derived/m4_z_marital_pre.parquet")
m5 = pd.read_parquet(PROJ / "3_derived/m5_z_education_pre.parquet")
m6 = pd.read_parquet(PROJ / "3_derived/m6_suicide_panel.parquet")
iv = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/02_bartik_iv/iv_z_x_bilateral.parquet")
mort = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/01_mortality/sigungu_mortality_panel_v02_wa.parquet")

# Step 2: build joint sample (sigungu intersection across all 4 mediators ∩ main 221)
# ... (complete-case 영역의 cumulative form)

# Step 3: First-stage F by mediator (z_x → mediator)
# M3: γ_FS for each of {delta_marriage, delta_divorce, delta_fertility}
# M4: skip (pre-determined → no first-stage path)
# M5: skip (pre-determined → no first-stage path)
# M6: γ_FS for delta_log_suicide (validation: suicide should follow despair_total protective sign)

# Step 4: Reduced-form mediator → mortality (control z_x)
# δ_M_marriage, δ_M_divorce, δ_M_fertility, δ_M_marital, δ_M_education, δ_M_suicide

# Step 5: DGHP decomposition where first-stage strong (M3 components if F > 16.4)
# 또는 multi-mediator joint reduced-form (no IV)

# Step 6: Effect modifier check (M4 + M5):
# d_log_asr ~ z_x_std + M_pre + z_x_std × M_pre
# Protective effect heterogeneity by pre-determined cohort sex ratio + education distance

# Step 7: Sub-period sensitivity (post-2008 sub-period parallel)
# Step 8: parquet commit + cluster bootstrap (sido G=12-13)
```

### 4.6 PowerShell wrapper (`run_subtask_2_5.ps1`)

```powershell
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "=== Sub-task 2.5: 4-mediator pipeline ==="
Write-Host "Step 1/5: M3 KOSIS family ETL"
python (Join-Path $scriptDir "2_5a_m3_kosis_family.py")

Write-Host "Step 2/5: M4 cohort sex ratio ETL"
python (Join-Path $scriptDir "2_5b_m4_cohort_sex_ratio.py")

Write-Host "Step 3/5: M5 university distance ETL"
python (Join-Path $scriptDir "2_5c_m5_university_distance.py")

Write-Host "Step 4/5: M6 suicide validation ETL"
python (Join-Path $scriptDir "2_5d_m6_suicide.py")

Write-Host "Step 5/5: multi-mediator analysis"
python (Join-Path $scriptDir "2_5e_multi_mediator_analysis.py")

Write-Host "=== Done ==="
```

---

## 5. 검증 commit 형식

```markdown
## Phase 2 sub-task 2.5 완료 — M3/M4/M5/M6 mediator + multi-mediator analysis

**Output**:
- 3_derived/m3_kosis_family_panel.parquet (sigungu × year × {3 family vars})
- 3_derived/m3_delta_panel.parquet (sigungu × {delta_marriage, delta_divorce, delta_fertility})
- 3_derived/m4_z_marital_pre.parquet (sigungu × cohort sex ratio)
- 3_derived/m5_z_education_pre.parquet (sigungu × distance)
- 3_derived/m6_suicide_panel.parquet (sigungu × delta_log_suicide)
- 4_results/m3_m6_first_stage_table.parquet (4 mediator first-stage F)
- 4_results/m3_m6_reduced_form_table.parquet (4 mediator reduced-form mortality)
- 4_results/multi_mediator_dghp_decomposition.parquet (DGHP decomposition table)

**Verify 결과**:
- M3 first-stage F: marriage = ?, divorce = ?, fertility = ?
- M4 + M5 effect modifier interaction t-stat: ?, ?
- M6 suicide validation reduced-form β: ?, t = ? (despair_total vs suicide-only sign consistency)
- Multi-mediator joint R²: ?
- Sub-period sensitivity: post-2008 sub-period parallel ?

**P1/P2/P3**: ...

**다음 step**: paper § 7.3-7.5 narrative draft commit
```

---

## 6. 주의사항

1. **Strict workflow anchor**: R-A sandbox 직접 분석 금지 (memory: feedback_no_sandbox_analysis.md)
2. **한자 사용 금지** (memory: feedback_no_hanja.md)
3. **0_raw 절대 수정 금지**
4. **Codebook 사전 inspect** (memory: feedback_panel_codebook_reference.md): kosis_family_mediators, 1985_yunbo_total 의 schema 사전 inspect 후 mapping
5. **Audit-after-action 6-step verify** (memory: feedback_audit_after_every_action.md)
6. **Sample 보존**: 각 mediator 의 effective n + intersection cumulative carry (M1 138 ↔ M3-M6 sample 의 cumulative diff)
7. **Cluster bootstrap**: sido G = 12-13 영역의 cumulative form

---

## 7. 실행 명령

```
이 prompt 의 spec 대로 5 Python script + PowerShell wrapper 작성 + 실행:
- 2_scripts/build_panel/2_5a_m3_kosis_family.py
- 2_scripts/build_panel/2_5b_m4_cohort_sex_ratio.py
- 2_scripts/build_panel/2_5c_m5_university_distance.py
- 2_scripts/build_panel/2_5d_m6_suicide.py
- 2_scripts/build_panel/2_5e_multi_mediator_analysis.py
- 2_scripts/build_panel/run_subtask_2_5.ps1
완료 후 verify 결과를 § 5 형식으로 보고.
```

---

## 8. R-A 의 substantive 권고 (각 mediator 의 substantive direction 의 cumulative form)

### 8.1 M3 KOSIS family aggregates (paper § 7.3 first half)

**Substantive 가설**: Trade exposure → 노동시장 안정화 → 경제적 기반 → 혼인율 ↑ + 이혼율 ↓ + 출산율 ↑ → deaths-of-despair (자살 + 약물중독 + 알코올성 간질환) ↓.

**구체 first-stage 영역**:
- z_x → Δlog(marriage_rate): protective sign expected (γ_FS > 0)
- z_x → Δlog(divorce_rate): protective sign expected (γ_FS < 0)
- z_x → Δlog(fertility_rate): protective sign expected (γ_FS > 0)

**Anchor 비교 영역**:
- ADH 2019 AERI: trade-induced marriage market value of young men in U.S. (negative direction for U.S. import competition)
- Korean evidence: opposite direction expected (export-driven trade integration → improved marriage market 위 substantive direction)

### 8.2 M4 z_m_marital pre-determined cohort sex ratio (paper § 7.3 second half)

**Substantive 가설**: 1975-1995 cohort 의 sigungu-level pre-determined sex ratio 가 trade exposure 의 mortality protective effect 의 effect modifier. Male-skewed sigungu (sex ratio > 1.05) 위 working-age population 의 marriage market pressure 가 cumulative form 위 trade exposure 의 protective channel 의 amplification 또는 dampening 영역의 cumulative form.

**구체 spec**:
- d_log_asr ~ z_x_std + z_m_marital + z_x_std × z_m_marital
- Interaction term sign + magnitude 의 cumulative direction

### 8.3 M5 z_m_education pre-determined university distance (paper § 7.4)

**Substantive 가설**: 1985 KEDI 4-year university 위 sigungu-level minimum distance 가 trade exposure 의 protective effect 의 effect modifier. 가까운 sigungu (distance ↓) 위 human capital endowment ↑ 의 cumulative form 위 trade-induced labor market shock 의 absorption capacity ↑ 의 substantive direction.

**구체 spec**:
- d_log_asr ~ z_x_std + z_m_education + z_x_std × z_m_education
- Interaction term sign + magnitude 의 cumulative direction
- Sensitivity: 1985/1990/1995 baselines (paper § 6.4 cumulative anchor: r ≥ 0.989)

### 8.4 M6 KOSTAT suicide validation (paper § 7.5)

**Substantive 가설**: Composite despair_total 위 protective β = -0.155 (cluster t = -5.65) 의 substantive direction 위 + 자살 (KOSTAT 102, X60-X84) sub-component 위 동일 direction 의 cumulative form 의 evidence-based validation.

**구체 spec**:
- d_log_suicide_h = log_suicide_2018-2022 - log_suicide_1997-1999
- d_log_suicide ~ z_x_std (147 intersection sample 위 또는 main 221 위)
- Sign consistency check: β_suicide < 0 expected, t < -2 expected

**Substantive 가치**:
- Composite outcome 위 dilution 영역 의 cumulative form 위 + 자살 single-component 위 protective sign 의 evidence-based confirm 의 cumulative direction
- Pierce-Schott 2020 + ADH 2019 위 자살 + drug overdose mortality 의 substantive direction 의 cumulative parallel 의 evidence

---

**End of Claude Code 위임 prompt**
