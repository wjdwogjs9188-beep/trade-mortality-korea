# Data Dictionary — Submission Package v01

**Package date**: 2026-05-06
**Cross-reference**: `README.md` for package orientation

This file documents the column-level specification for all parquet/csv files in the submission package. Files are listed by sub-folder.

---

## 01_mortality/

### `sigungu_mortality_panel_v02_wa.parquet`

Working-age (25-64) Korean nationality mortality panel.

| Column | Type | Description |
|--------|------|-------------|
| `h_code` | string | Harmonized sigungu identifier (5-digit), 2021 KOSTAT baseline |
| `year` | int | Year (1997-2024) |
| `outcome_group` | string | One of: despair_total, cancer, cardiovascular, respiratory, external_other |
| `deaths` | int | Death count for sigungu × year × outcome_group |
| `period_pre2008` | bool | Indicator for 1997-2007 (pre-KCD-6 revision) |
| `pop_wa` | int | Working-age (25-64) Korean nationality population (denominator) |

**Universe**: 31,494 cells. Source: KOSTAT 사망 microdata 28 csv (1997-2024) + KOSIS 주민등록인구 panel.

---

## 02_bartik_iv/

### `baseline_shares_1994_ksic9_2digit.parquet`
1994 KOSTAT industrial census baseline employment shares.

| Column | Type | Description |
|--------|------|-------------|
| `h_code` | string | Harmonized sigungu (5-digit) |
| `ksic9_2digit` | string | KSIC 9차 2-digit code (with C prefix, e.g., C10, C13) |
| `employment` | float | 1994 employment count for h × k cell |
| `h_total` | float | 1994 total manufacturing employment for h |
| `share` | float | s_{h,k}^1994 = employment / h_total |

**Universe**: 4,003 cells. 251 sigungu × 23 KSIC9 industries. Source: KOSTAT 광업·제조업조사 1994.

### `baseline_shares_1992_ksic9_2digit_v2.parquet`
1992 baseline shares (sensitivity).

| Column | Type | Description |
|--------|------|-------------|
| `h_code` | string | Harmonized sigungu (5-digit) |
| `ksic9_2digit` | string | KSIC 9차 2-digit (numeric only, no C prefix) — converted from KSIC 6th edition via 23-row crosswalk |
| `E_hk_1992` | float | 1992 employment count |
| `E_h_1992` | float | 1992 total manufacturing employment |
| `share_hk_1992` | float | 1992 share |

**Universe**: 3,237 cells. 215 h_code × 22 KSIC9.

### `denominator_E_h_1994.parquet` / `denominator_E_h_1992_v2.parquet`
Per-sigungu total employment denominator (h × E_h).

### `exposure_adh8_2000_2010.parquet`
ADH-8 instrument: cumulative 2000-2010 China imports to 8 OECD economies.

| Column | Type | Description |
|--------|------|-------------|
| `ksic9_2digit` | string | KSIC 9차 2-digit |
| `M_2000` | float | 2000 import value (USD) |
| `M_2010` | float | 2010 import value |
| `dM_2000_2010` | float | M_2010 - M_2000 |

ADH-8 countries: AU, CH, DE, DK, ES, FI, JP, NZ.

### `exposure_bilateral_2000_2010.parquet`
Korea-China bilateral imports (analogous schema).

### `iv_z_x_bilateral.parquet`
Per-worker Bartik IV using Korea-China bilateral exposure (1994 baseline).

| Column | Type | Description |
|--------|------|-------------|
| `h_code` | string | Harmonized sigungu |
| `z_x` | float | Σ_k s_{h,k}^1994 × ΔM_k (raw) |
| `E_h_1994` | float | Total 1994 manufacturing employment |
| `z_x_per_worker` | float | z_x / E_h_1994 (regression input) |

### `iv_z_x_adh8.parquet`
Per-worker ADH-8 IV (1994 baseline). Same schema with `E_h_1994`.

### `iv_z_x_bilateral_1992baseline.parquet` / `iv_z_x_adh8_1992baseline.parquet`
1992 baseline analogues. Schema uses `E_h_1992` instead of `E_h_1994`.

### `hs6_to_ksic9_2digit.parquet`
HS6 → KSIC 9차 2-digit mapping via KIET 60-sector concordance.

---

## 03_mediators/

### `z_m_education_baseline_sensitivity.parquet`
Track 2 z_m_education mediator panel.

| Column | Type | Description |
|--------|------|-------------|
| `h_code` | string | Harmonized sigungu |
| `nearest_dist_km_y1985` | float | Haversine distance to nearest 4-year university (1985 KEDI baseline, 171 universities) |
| `z_m_edu_y1985` | float | Standardized education-distance mediator (1985) |
| `nearest_dist_km_y1990` | float | 1990 baseline (175 universities) |
| `z_m_edu_y1990` | float | Standardized (1990) |
| `nearest_dist_km_y1995` | float | 1995 baseline (175 universities) |
| `z_m_edu_y1995` | float | Standardized (1995) |
| `sido_code` | string | Province code (16 sido) |

**Universe**: 251 sigungu. Cross-baseline Pearson r ≥ 0.989.

### `mediator_specific_education_rate_v01.parquet`
Sigungu-level education attainment rate panel.

### `mortality_panel_v02_marriage.parquet` / `mortality_panel_v02_education.parquet` / `mortality_panel_v02_occupation.parquet`
Mortality panel sub-stratified by mediator dimension (M3 marriage, M5 education, M6 occupation).

---

## 04_regression_results/

### `main_spec_5layer_se.csv`
Main 1994-baseline 5-outcome × 5-SE-layer regression results.

| Column | Type | Description |
|--------|------|-------------|
| `outcome` | string | despair_total, cancer, cardiovascular, respiratory, external_other |
| `n` | int | Sample size for outcome (222 for 4 outcomes; 198 for respiratory) |
| `beta_std` | float | Standardized regression coefficient |
| `se_HC1` | float | HC1 heteroskedasticity-robust SE |
| `t_HC1` | float | HC1 t-statistic |
| `p_HC1` | float | HC1 p-value |
| `se_cluster_sido` | float | Cluster-province asymptotic SE (G=16) |
| `t_cluster_sido` | float | t-statistic |
| `p_cluster_sido` | float | p-value |
| `se_AKM` | float | AKM industry-mode SE (BHJ implementation) |
| `t_AKM` | float | t-statistic |
| `se_Conley_5km` | float | Conley spatial HAC SE (5km cutoff) |
| `t_Conley_5km` | float | t-statistic |
| `se_Conley_10km` | float | Conley spatial HAC SE (10km cutoff) |
| `t_Conley_10km` | float | t-statistic |
| `WCB_sido_p` | float | Wild cluster bootstrap p-value (NaN where convergence fails) |
| `tF_cutoff` | float | LMP 2022 IV second-stage critical value (3.286 for F=19.65) |
| `tF_pass_*` | bool | Whether |t| exceeds tF cutoff for each SE layer |
| `r2` | float | R-squared |

### `main_spec_5layer_se_1992baseline.csv`
1992 baseline analogue.

### `romano_wolf_pvalues.csv` / `romano_wolf_pvalues_1992baseline.csv`
Romano-Wolf step-down adjusted p-values.

| Column | Type | Description |
|--------|------|-------------|
| `outcome` | string | 5 outcome categories |
| `t_HC1` | float | HC1 t-statistic (input to RW) |
| `p_raw` | float | Raw HC1 p-value |
| `p_RW_adj` | float | Romano-Wolf adjusted p-value |
| `RW_sig` | bool | RW-significant at FWER 5% |

### `sub_period_split_2008.csv` / `sub_period_split_2008_1992baseline.csv`
Post-2008 sub-period regression (single row).

| Column | Type | Description |
|--------|------|-------------|
| `period` | string | post_2008 |
| `year_range` | string | "2008-2022" |
| `n` | int | Sub-sample size (218 for 1994; 206 for 1992) |
| `beta` | float | Sub-period coefficient |
| `se` | float | HC1 SE |
| `t` | float | t-statistic |
| `p` | float | p-value |

### `pre_wto_placebo_1992_1996.csv`
Pre-WTO placebo (1992-1996 China exposure × 1997-1999 mortality).

### `quality_improvement_suite.csv`
Drop-C26, drop-top-3, AKM v4 canonical (separate estimand).

| Column | Type |
|--------|------|
| `method` | Region OLS HC1 / Drop-C26 / Drop top-3 / AKM v4 canonical (WLS) |
| `n` | Sample size |
| `beta` | Coefficient |
| `t` | t-statistic |

### `akm_proper_2019.csv` / `akm_bhj2022_ssaggregate.csv`
AKM-style standard error robustness checks.

---

## 05_codebooks/

### `sigungu_crosswalk.csv`
Time-varying → harmonized sigungu mapping (1997-2023).

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | 1997-2023 |
| `raw_code` | string | Contemporaneous sigungu code |
| `h_code` | string | Harmonized 2021 KOSTAT baseline |
| `h_name` | string | Sigungu name in 2021 |
| `sido_code` | string | Province code |
| `sido_name` | string | Province name |
| `event_note` | string | Administrative-change note (e.g., "1995 Andong-si merger") |

**Rows**: 6,723. **Universe**: 256 h_codes.

### `sigungu_changes_history.md`
Documentation of 111 administrative changes 1997-2023.

### `kosis_104_to_icd10.yaml`
KOSIS 104 cause-of-death codes → ICD-10 ranges + outcome group mapping. Used to construct `outcome_group` column in mortality panel.

### `mortality_104_classification.csv`
Full 104-code KOSTAT classification table.

### `ksic6_to_ksic9_2digit.csv`
KSIC 6th-edition (1992) → KSIC 9th-edition (2008+) 2-digit crosswalk.

| Column | Type |
|--------|------|
| `ksic6` | KSIC 6차 code (e.g., D15) |
| `ksic9` | KSIC 9차 code (e.g., C10) |

**Mappings**: 23 (D15→C10 food, D17→C13 textiles, ..., D37→C33 furniture).

### `child_to_parent_mapping.csv`
KOSIS aggregation hierarchy (sub-region to super-region).

---

## 06_paper_draft/ + 07_audit_logs/

See `README.md` for paper draft and audit log descriptions.

---

## Notes

- All parquet files are pyarrow-compatible (verified during the package build).
- All csv files use UTF-8 encoding.
- All file paths in this dictionary are relative to the package root (`paper_v01_submission/`).
- Cross-references in the paper draft to "Section X.Y" or "Table Z" refer to the paper draft files in `06_paper_draft/`.
- Cross-references in `07_audit_logs/` to log files use the `5_logs/decisions/` or `5_logs/integrity_checks/` paths from the underlying project; the corresponding files are included in `07_audit_logs/` for reviewer convenience.
