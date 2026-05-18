# Phase 2-A — mortality panel v02 working-age build (v3 positional)
_2026-05-05_

- working-age age_5y codes: [6, 7, 8, 9, 10, 11, 12, 13] (25-29 ~ 60-64)

## Mortality microdata
- files: 28
- combined rows: **7,657,389**

## Pre-filter 진단
- year range: 1997-2024
- sido_resid distinct: 17
- sgg_resid distinct: 342
- raw_code (시도+시군구) distinct: 612
- age_5y distribution: {np.int64(1): 42486, np.int64(2): 15681, np.int64(3): 12171, np.int64(4): 11486, np.int64(5): 30220, np.int64(6): 45242, np.int64(7): 62376, np.int64(8): 82548, np.int64(9): 124839, np.int64(10): 191165, np.int64(11): 267976, np.int64(12): 346931, np.int64(13): 433674, np.int64(14): 540942, np.int64(15): 661128, np.int64(16): 836470, np.int64(17): 1052481, np.int64(18): 1172175, np.int64(19): 1206296, np.int64(20): 520119, np.int64(99): 983}
- nationality top 5: {'1': 4943484, '(NaN)': 2707530, '2': 6375}
- cause_104 distinct: 89

## Korean filter
- nationality '1' or NaN: 7,651,014/7,657,389 (99.92%)

## Working-age filter
- age_5y ∈ [6, 7, 8, 9, 10, 11, 12, 13]: 1,553,192/7,651,014 (20.3%)

## Outcome group expand
- rows: 1,305,636
- by group: {'cancer': 472099, 'despair_total': 364639, 'cardiovascular': 218093, 'external_other': 215959, 'respiratory': 34846}

## Crosswalk match
- match rate: 1,235,319/1,305,636 (94.6%)
- unmatched raw_code top 10: {'31240': 557, '3131050': 535, '31070': 508, '3131240': 486, '31130': 486, '3131130': 482, '39010': 457, '23080': 438, '38070': 408, '31150': 400}

## Panel aggregate
- rows: 31,494
- distinct h_code: 256
- year range: 1997-2022

## Population panel
- cols: ['C1', 'C1_NM', 'C2', 'C2_NM', 'C3', 'C3_NM', 'year', 'population']
- ⚠️ pop column 미식별 (pop=population, age=None, h=None, year=year)

- saved: `3_derived\mortality\sigungu_mortality_panel_v02_wa.parquet`
- final shape: (31494, 6)

## External validation

## 다음 step
- script 24 (Test 3 Pierce-Schott) 재실행
- 첫 reduced form: Δlog despair ~ z_x_h^{KR-CN} + year FE