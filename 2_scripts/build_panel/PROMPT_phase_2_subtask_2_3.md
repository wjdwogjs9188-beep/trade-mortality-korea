# Claude Code 위임 prompt — Phase 2 sub-task 2.3: M1 composite outcome variable 정의

**작성**: 2026-05-07 R-A (공동저자 mode) → 정재헌 → Claude Code
**대상 박사논문**: Trade Exposure and Mortality in Export-Oriented Korea (KER July 2026 target)
**Phase**: 2 (mediator panel build) sub-task 2.3 (M1 composite outcome variable + sparse cell treatment)
**선행 의존성**: ✅ sub-task 2.2 (HIRA panel ETL) 완료 (panel 168 + intersection 147 + β_147 재추정 cumulative commit)
**후행 의존성**: sub-task 2.4 (DGHP 2017 single-IV mediation framework R/Stata implementation)
**예상 소요**: ~45-60분 (Python composite + log + z-score + first-stage scatter + 6-step verify)

---

## 본 paper context (Claude Code 가 본 prompt 만으로 작업 시작 가능 self-contained form)

본 paper 는 Korea-China bilateral trade integration (1994 baseline + 1997-1999 ↔ 2018-2022 long difference) 의 working-age deaths-of-despair mortality 에 대한 protective effect (β_221 = -0.128, AKM-proper t = -4.92, Romano-Wolf p_RW = 0.0161 FWER pass) 추정. § 7 mechanism analysis 는 DGHP 2017 single-IV mediation framework 위 5개 active mediator (M1 HIRA pharmaceutical + M3 + M4 + M5 + M6) 의 protective channel decomposition.

**Sub-task 2.2 cumulative commit**:
- HIRA crosswalk: 220001 → 23090 (인천미추홀구) MATCH 정정 commit (UNMATCHED 0)
- Panel: long 1,640 rows + wide 325 rows
- Intersection: 147 sigungu (= main 221 ∩ HIRA 168, 미추홀구 + 경상남도 6 + 제주 2 추가)
- β_147 = -0.155 (HC1 t = -4.81, cluster t = -5.65, p = 0.0001), \|Δβ\|/SE_full = 1.025 (honest minor caveat)
- 30 sparse cells: 6 sigungu × 5 ATC4 × 1 endpoint year (3 행정 변경 transition + 3 reporting absence)

**본 sub-task 2.3 의 substantive 영역**: HIRA panel 의 5 ATC4 prescription rates 를 M1 composite outcome variable 로 변환. log + z-score normalization 으로 ATC4 간 scale 차이 (median ~25만~280만 per 100k, ratio 53× to 551×) 정규화. 147 intersection sample 위 sigungu × year cell 의 long-difference form 으로 reshape (Δlog M1 = log M1_2019 − log M1_2010). DGHP single-IV mediation framework input 준비.

---

## 1. 목적

HIRA pharmaceutical panel (5 ATC4 × 168 sigungu × 2 endpoint year) 을 M1 composite outcome variable 의 long-difference form 으로 변환 + 147 intersection sample 위 build.

---

## 2. Input files

| File | Path | 영역 |
|------|------|------|
| HIRA panel long | `3_derived/hira_atc4_panel.parquet` | 1,640 rows (5 ATC4 × 168 sigungu × 2 year - 30 sparse) |
| HIRA panel wide | `3_derived/hira_atc4_panel_wide.parquet` | 325 rows |
| Intersection 147 | `1_codebooks/intersection_main_hira_h_codes.csv` | 147 sigungu list |
| Mortality panel | `8_submission/paper_v01_submission/01_mortality/sigungu_mortality_panel_v02_wa.parquet` | 31,494 rows |
| IV panel | `8_submission/paper_v01_submission/02_bartik_iv/iv_z_x_bilateral.parquet` | 226 rows |

---

## 3. M1 composite outcome variable 정의

### 3.1 Definition (paper § 7.1.1 narrative anchor commit 기준)

본 paper 의 M1 composite 는 4-component despair mapping (Case-Deaton 2015 PNAS) 의 한국 KOSTAT extension 와 cumulative 호환:

```
M1_composite_{h,y} = mean of standardized log-rates across 5 ATC4 categories
                   = mean over k ∈ {N06AB, N06AX, N05BA, N05AX, A05BA} of zscore(log(rate_{h,y,k}))
```

ATC4 간 scale 차이 (median ratio 53× to 551×) 의 정규화 위 다음 2-stage transformation:

**Stage 1 — log transformation**: 각 ATC4 별 raw rate 의 log + Laplace smoothing (zero rate 처리):
```
log_rate_{h,y,k} = log(rate_per_100k_{h,y,k} + 1)
```

**Stage 2 — z-score normalization**: pooled across (h, y) sample 위 mean=0, std=1 normalization:
```
z_log_rate_{h,y,k} = (log_rate_{h,y,k} - μ_k) / σ_k
```

**Composite**: 5 ATC4 평균:
```
M1_composite_{h,y} = mean over k of z_log_rate_{h,y,k}
```

### 3.2 Long-difference form (DGHP framework input)

```
ΔM1_h = M1_composite_{h, 2019} − M1_composite_{h, 2010}
```

본 long-difference 는 paper § 5.1 의 main mortality long-difference (Δlog asr_p1 = log asr_2018-2022 − log asr_1997-1999) 와 framework 일관 (단 mortality 는 21-year window, M1 은 9-year window).

### 3.3 Sparse cell treatment (R-A 직전 turn 권고)

**Default**: complete-case form. sigungu × year cell 위 5 ATC4 중 NaN cell 이 1 개 이상이면 해당 sigungu × year cell 자체를 NaN 처리.

- 30 sparse cell (6 sigungu × 5 ATC4 × 1 year) → 6 sigungu × 1 year = 6 sigungu × year cell 의 M1_composite NaN
- 5 cells 미추홀구 23090 의 2010 영역 (KOSIS pop join 영역) → 23090 의 2010 M1_composite NaN

**Effective sample after long-difference**:
- 147 intersection sample 위 ΔM1 의 effective sigungu = 147 − 4 (4 sigungu 가 long-difference 양 endpoint 모두 valid 한 sigungu 만 포함, 행정 변경 + 미추홀구 2010 KOSIS pop missing 의 cumulative 영역)
- 정확한 effective n 은 sub-task 2.3 build 후 verify

### 3.4 Alternative composite (sensitivity check)

**Alt 1 (4 mental ATC4 only)**: A05BA 제외, 4 mental-health ATC4 (N06AB + N06AX + N05BA + N05AX) 의 z-score 평균. KOSTAT 057 + 102 (mental + suicide) 영역의 직접 매핑.

**Alt 2 (Liver therapy only)**: A05BA 만의 z-score. KOSTAT 081 (chronic liver disease) 영역의 direct measure.

**Alt 3 (PCA 1st component)**: 5 ATC4 위 PCA 의 1st principal component. cross-ATC4 correlation matrix (R-A 직전 turn cumulative confirm 결과: N06AB ↔ N06AX r = 0.84) 의 substantive 영역의 cumulative form.

본 paper 의 main spec 는 Alt 0 (5 ATC4 weighted average); Alt 1-3 은 sub-task 2.4 의 sensitivity check input.

---

## 4. Output files

### 4.1 M1 panel long form

`3_derived/hira_m1_panel.parquet`

| Column | dtype | Description |
|--------|-------|-------------|
| `h_code` | int32 | KOSTAT 5-digit sigungu code |
| `year` | int16 | 2010 or 2019 |
| `m1_composite` | float32 | 5 ATC4 z-score 평균 (Alt 0 main) |
| `m1_4mental` | float32 | 4 mental-health ATC4 z-score 평균 (Alt 1) |
| `m1_liver` | float32 | A05BA z-score (Alt 2) |
| `m1_pca1` | float32 | PCA 1st component (Alt 3) |
| `working_age_pop_25_64` | float32 | KOSIS working-age pop |
| `in_intersection_147` | bool | 147 intersection inclusion |

예상 row 수: 168 × 2 = 336 (sparse cells 의 NaN 영역 inclusion).

### 4.2 ΔM1 long-difference form

`3_derived/hira_delta_m1_panel.parquet`

| Column | dtype | Description |
|--------|-------|-------------|
| `h_code` | int32 | KOSTAT 5-digit sigungu code |
| `delta_m1_composite` | float32 | ΔM1 = M1_2019 − M1_2010 |
| `delta_m1_4mental` | float32 | Alt 1 ΔM1 |
| `delta_m1_liver` | float32 | Alt 2 ΔM1 |
| `delta_m1_pca1` | float32 | Alt 3 ΔM1 |
| `in_intersection_147` | bool | 147 inclusion |
| `complete_case` | bool | both 2010 + 2019 valid (NaN 부재) |

예상 row 수: 168.

### 4.3 First-stage scatter data (paper figure 위)

`3_derived/hira_first_stage_scatter.parquet`

| Column | Description |
|--------|-------------|
| `h_code` | sigungu code |
| `z_x_per_worker` | trade exposure (Bartik IV) |
| `delta_m1_composite` | M1 ΔM1 outcome |
| `in_intersection_147` | True for 147 sample |

DGHP framework 의 first-stage F (z_x → ΔM1) 추정 input.

---

## 5. Implementation steps

### Step 1: Load + filter

```python
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.decomposition import PCA

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
panel = pd.read_parquet(PROJ / "3_derived" / "hira_atc4_panel.parquet")
intersect = pd.read_csv(PROJ / "1_codebooks" / "intersection_main_hira_h_codes.csv")
print(f'Input panel: {len(panel)} rows, intersection: {len(intersect)} sigungu')
```

### Step 2: Wide pivot + log + z-score

```python
ATC4_LIST = ['N06AB', 'N06AX', 'N05BA', 'N05AX', 'A05BA']
MENTAL_ATC4 = ['N06AB', 'N06AX', 'N05BA', 'N05AX']
LIVER_ATC4 = ['A05BA']

# Wide pivot (h_code, year × atc4)
wide = panel.pivot_table(
    index=['h_code', 'year', 'in_intersection_147', 'working_age_pop_25_64'],
    columns='atc4',
    values='prescription_rate_per_100k',
    aggfunc='first'
).reset_index()

# Log + Laplace smoothing
for atc in ATC4_LIST:
    wide[f'log_{atc.lower()}'] = np.log(wide[atc] + 1)

# Z-score normalization (pooled across h, y)
for atc in ATC4_LIST:
    col_log = f'log_{atc.lower()}'
    mu = wide[col_log].mean()
    sigma = wide[col_log].std()
    wide[f'z_{atc.lower()}'] = (wide[col_log] - mu) / sigma
```

### Step 3: M1 composite (Alt 0/1/2/3)

```python
# Alt 0: 5 ATC4 z-score 평균
z_cols_5 = [f'z_{a.lower()}' for a in ATC4_LIST]
wide['m1_composite'] = wide[z_cols_5].mean(axis=1, skipna=False)  # complete-case

# Alt 1: 4 mental ATC4 평균
z_cols_4 = [f'z_{a.lower()}' for a in MENTAL_ATC4]
wide['m1_4mental'] = wide[z_cols_4].mean(axis=1, skipna=False)

# Alt 2: A05BA only
wide['m1_liver'] = wide['z_a05ba']

# Alt 3: PCA 1st component (complete-case only)
mask_complete = wide[z_cols_5].notna().all(axis=1)
pca = PCA(n_components=1)
pca_fit = pca.fit_transform(wide.loc[mask_complete, z_cols_5])
wide['m1_pca1'] = np.nan
wide.loc[mask_complete, 'm1_pca1'] = pca_fit.flatten()
print(f'PCA 1st component explained variance: {pca.explained_variance_ratio_[0]:.3f}')
```

### Step 4: Long-difference form

```python
# 2010 / 2019 pivot
m1_2010 = wide[wide['year']==2010][['h_code','m1_composite','m1_4mental','m1_liver','m1_pca1','in_intersection_147']].rename(columns=lambda c: c+'_2010' if c not in ['h_code','in_intersection_147'] else c)
m1_2019 = wide[wide['year']==2019][['h_code','m1_composite','m1_4mental','m1_liver','m1_pca1']].rename(columns=lambda c: c+'_2019' if c != 'h_code' else c)

delta = m1_2010.merge(m1_2019, on='h_code', how='outer')
for ms in ['m1_composite','m1_4mental','m1_liver','m1_pca1']:
    delta[f'delta_{ms}'] = delta[f'{ms}_2019'] - delta[f'{ms}_2010']

delta['complete_case'] = (
    delta['m1_composite_2010'].notna() & delta['m1_composite_2019'].notna()
)
print(f'delta panel: {len(delta)} sigungu')
print(f'complete-case 147 intersection: {(delta["in_intersection_147"] & delta["complete_case"]).sum()}')
```

### Step 5: First-stage scatter (z_x × ΔM1)

```python
iv = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/02_bartik_iv/iv_z_x_bilateral.parquet")
iv['h_code'] = iv['h_code'].astype(int)
fs = delta.merge(iv[['h_code','z_x','z_x_per_worker']], on='h_code', how='inner')
fs_clean = fs[fs['complete_case']].copy()

# First-stage regression: ΔM1 ~ z_x_per_worker
import statsmodels.api as sm
fs_int = fs_clean[fs_clean['in_intersection_147']].copy()
fs_int['z_x_std'] = (fs_int['z_x_per_worker'] - fs_int['z_x_per_worker'].mean()) / fs_int['z_x_per_worker'].std()
X = sm.add_constant(fs_int['z_x_std'])
fit_fs = sm.OLS(fs_int['delta_m1_composite'], X).fit(cov_type='HC1')
print(f'First-stage F: {fit_fs.fvalue:.2f}, F p-value: {fit_fs.f_pvalue:.4f}')
print(f'γ_FS = {fit_fs.params[1]:.6f} (SE = {fit_fs.bse[1]:.6f}, t = {fit_fs.tvalues[1]:.4f})')
```

### Step 6: Output write + audit

```python
# Wide form M1 panel
wide_out = wide[[
    'h_code','year','m1_composite','m1_4mental','m1_liver','m1_pca1',
    'working_age_pop_25_64','in_intersection_147'
]].copy()
wide_out.to_parquet(PROJ / "3_derived/hira_m1_panel.parquet", index=False)

# Long-difference panel
delta[[
    'h_code','delta_m1_composite','delta_m1_4mental','delta_m1_liver','delta_m1_pca1',
    'in_intersection_147','complete_case'
]].to_parquet(PROJ / "3_derived/hira_delta_m1_panel.parquet", index=False)

# First-stage scatter
fs_clean[[
    'h_code','z_x','z_x_per_worker','delta_m1_composite','in_intersection_147'
]].to_parquet(PROJ / "3_derived/hira_first_stage_scatter.parquet", index=False)

# Audit-after-action 6-step verify (file integrity + schema + row counts + NaN ratios + complete-case n + first-stage F)
```

---

## 6. 검증 commit 형식

작업 완료 후 다음 형식으로 보고:

```markdown
## Phase 2 sub-task 2.3 완료 — M1 composite outcome variable

**Output**:
- `3_derived/hira_m1_panel.parquet` (n=336 rows)
- `3_derived/hira_delta_m1_panel.parquet` (n=168 sigungu)
- `3_derived/hira_first_stage_scatter.parquet` (n=147 intersection complete-case)

**Verify 결과**:
- M1 composite range: [min, max], mean ≈ 0, std ≈ 1
- Complete-case 147 intersection effective n: ?
- PCA 1st explained variance: ?
- First-stage F = ?, γ_FS = ?, t = ?

**P1/P2/P3 issue**: ...

**다음 step**: Phase 2 sub-task 2.4 (DGHP ivmediate R/Stata implementation)
```

---

## 7. 주의사항

1. **Complete-case form**: sparse cell 의 NaN propagation 위 5 ATC4 중 1개 NaN 시 sigungu × year cell 의 M1 NaN 처리 (mean(skipna=False))
2. **Long-difference effective sample**: 147 intersection 위 long-difference 양 endpoint 모두 valid 한 sigungu 만 first-stage scatter 에 inclusion
3. **z-score normalization**: pooled across (h, y) sample 위 mean=0, std=1
4. **PCA**: complete-case sample 위에서만 fit (NaN 영역 부재). PCA 1st explained variance > 60% 가 expected (cross-ATC4 correlation r=0.48-0.84 의 cumulative 영향)
5. **한자 사용 금지** (사용자 메모리)
6. **0_raw/ 절대 수정 X**

---

## 8. 실행 명령

Claude Code 에 본 prompt 를 붙여넣고:

```
이 prompt 의 spec 대로 Python script 를 작성하고 실행해줘.
script: 2_scripts/build_panel/2_3_m1_composite.py
PowerShell wrapper: 2_scripts/build_panel/run_m1_composite.ps1
완료 후 verify 결과를 § 6 형식으로 보고.
```

---

**End of Claude Code 위임 prompt**
