# Phase 5 — 1999 baseline robustness build
_2026-05-12_

## 1999 raw schema (probe-verified)
- file: `0_raw/kosis_business_survey/microdata_1994_2024/1999_연간자료_20260415_35230.csv`
- shape: (2927330, 29) (rows × cols)
- encoding: utf-8-sig, header=None, 29 columns
- column convention: col 0=시도, col 1=시군구, col 3=KSIC letter,
  col 4=KSIC 2-digit (15-37 for D), col 28=종사자 합계 annual (M+F)

## Manufacturing filter
- D-filter rows: 297,416 / 2,927,330 (10.2%)
- distinct sgg5 (D only): 246
- distinct KSIC 2-digit (D only): 23
- 종사자수 national sum (col 28, D only): **2,459,919**
  - 통계청 1999 광업제조업 annual employment anchor ≈ 2.4-2.7M → ✅ 정합

## Sigungu crosswalk (year=1999, raw → h_code)
- row-level match: 297,416/297,416 (100.0%)
- 종사자 weighted match: 2,459,919/2,459,919 (100.0%)

## KSIC 7→9 crosswalk (manufacturing 2-digit)
- file: `1_codebooks/ksic6_to_ksic9_2digit.csv` (label legacy; D-prefix = KSIC 7th)
- D-prefix mapping rows: 23
- D15→C10 food, D17→C13 textiles, ..., D37→C33 (1-to-1 dominant target)

## 1999 baseline shares (KSIC9 2-digit)
- agg rows: 4,361
- distinct h_code: 241
- distinct KSIC9 2-digit: 22
- median h_total (E_h^{1999}): 3651
- mean h_total: 10207
- saved: `3_derived\bartik\baseline_shares_1999_ksic9_2digit.parquet`
- denominator E_h_1999: median=3651, mean=10207

## Bartik IV 1999 baseline
- exposure bilateral (KR-CN): 23 KSIC9 2-digit cells
- exposure ADH-8 (8 advanced→CN): 23 KSIC9 2-digit cells

### KR-CN bilateral IV (1999 baseline)
- n h_code: 241
- z_x_per_worker mean=1401915.86, sd=3753540.37

### ADH-8 IV (1999 baseline)
- n h_code: 241
- z_x_per_worker mean=1498584.92, sd=2486453.92

## Native long-difference panel (despair_total, 1999 baseline)
- n = 235 sigungu, G (sido) = 17
- z_x_per_worker SD (σ_z, 1999): 3796256.8533
  (compare: 1994 baseline σ_z = reference value from main spec)

### 5-layer SE for β_1999 (despair_total)
- β = -0.0872, n = 235
- HC1: SE=0.0330, t=-2.646, p=0.0082
- cluster-province (G=17, t-dist): SE=0.0350, t=-2.496, p=0.0239
- Conley 5km: SE=0.0321, t=-2.716
- Conley 10km: SE=0.0328, t=-2.662
- WCR Webb 6-pt (B=9999, cluster=sido): p = **0.3223**
- AKM-proper (Kolesár 2024 ShiftShareSE): ⚠️ requires external R package — reported as `pending external compute` in this Python pipeline

## First-stage F (1999 baseline)
- spec: z_bil^{1999} on z_adh^{1999}, n = 241
- HC1 F = 16.79
- cluster-sido F = 18.31
- 1994 baseline reference (Phase B-x cluster-sido): F = 19.65
- ⚠️ 1999 baseline attenuates instrument relevance: F = 18.31 < 19.65 (attenuation -6.8%)

- saved: `4_results\regression\main_native_5layer_1999baseline.csv`

## Cross-baseline cascade (β coefficient)
| Baseline year | β | n | First-stage F (cluster-sido) | Notes |
|---------------|---|---|------------------------------|-------|
| 1992 (winsorized) | -0.0640 | 209 | (not reported) | KSIC 6→9 crosswalk, winsorize 99% |
| **1994 (main)** | **-0.127** | **221** | **19.65** | KSIC 9 native, pre-shock 6yr |
| 1999 (Phase 5) | **-0.0872** | 235 | **18.31** | KSIC 7→9 crosswalk, pre-shock 1yr |