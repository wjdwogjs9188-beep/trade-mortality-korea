# Stage 3 — Population Panel Validation (v1)

- Generated: 2026-05-03
- Source: `0_raw\kosis_population\population_combined.csv` (KOSIS 주민등록인구)
- Crosswalk: `1_codebooks\sigungu_crosswalk_v2.csv` (year-aware merge on raw_code=C1)
- Output: `3_derived\population\population_panel_v01.parquet` (210,222 rows)

## Filter pipeline

- C1 5-digit only (제외 시도/전국 합계)
- C2 ∈ {1, 2} (남/여, 계 행 제외)
- C3 ∈ 17 valid 5-yr bands (000=계, 360-440=80+ 세부 제외 — 340='80+' aggregated 만 사용)
- year ≥ 1997
- Year-aware merge with sigungu_crosswalk_v2 → 자동 drop 9,316 parent city totals (자치구 children 와 중복)

## Panel dimensions

- distinct h_code: 229
- year range: 1997-2023 (27 yrs)
- sex codes: {1=남, 2=여}
- age bands (17): `['01_02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18_19_20']`
- max cells: 229 × 27 × 2 × 17 = 210,222
- actual cells: 210,222

## Validation

| check | result | detail |
|---|:---:|---|
| V1 KOSIS 인구 합 보존 (pre vs post collapse) | PASS | pre=1,292,773,441.0 post=1,292,773,441.0 diff=0.000000 |
| V2 229 시군구 cover | PASS | distinct h_code = 229 |
| V3 27 year cover (1997-2023) | PASS | n_years=27, range=1997-2023 |
| V4 17 age band cover | PASS | bands=['01_02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18_19_20'] |
| V5 한국 총인구 cross-check (5 yrs, ±2%) | PASS | 2000: panel=47,534,117 official=47,008,000 diff=1.119%; 2010: panel=49,879,812 official=49,410,000 diff=0.951%; 2015: panel=50,951,719 official=51,015,000 diff=0.124%; 2020: panel=51,349,259 official=51,836,000 diff=0.939%; 2023: panel=51,145,884 official=51,753,000 diff=1.173% |
| V9 standardization weight 합 = 1 per sex | PASS | sex=1: Σw=1.000000000000; sex=2: Σw=1.000000000000 |

**Overall (population panel)**: ALL PASS
