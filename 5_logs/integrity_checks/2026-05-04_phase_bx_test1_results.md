# Phase B-x Test 1 — Macro predictability
_timestamp: 2026-05-04T23:02:08.034932_

## bilateral coverage
- years 2000-2024, n=25

## Test 1 — bilateral M change ~ lagged macro

- obs: 19
- macro variables: ['d5_log_macro_분기GDP_지출_실질_lag1', 'd5_log_macro_수출물가지수_lag1', 'd5_log_macro_수입물가지수_lag1', 'd5_log_macro_CPI_lag1', 'd5_log_macro_KRW_USD_lag1', 'd5_log_macro_BoK_rate_lag1']
- **Joint F-stat**: 129.957
- **Joint p-value**: 0.0000
- **결정**:
 - p < 0.05 → **bilateral 외생성 의심** → C.ii branch 진입 위험
