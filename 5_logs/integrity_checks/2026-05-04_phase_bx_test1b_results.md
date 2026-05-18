# Phase B-x Test 1b — WEO surprise predictability (v2)
_2026-05-04_

- WEO Korea NGDP_RPCH long rows: **524**
- vintage_year range: 1990-2022
- target_year range: 1988-2027
- horizon range: -2..5
- season distribution: {'F': 264, 'S': 260}

- forecast-surprise rows (Fall horizon-0 vs horizon-1): **32**
- year range: 1991-2022
- surprise stats: mean=-0.55, sd=3.24, min=-12.99, max=7.53

- KR-CN bilateral year rows: **25** (2000-2024)
- regression sample: **18** years

## d5_log_M ~ d5_surprise_avg (HAC SE, maxlags=4)
- N=18, β=-0.0489, SE=0.1452, p=0.7365, R²=0.001
- [PASS] p > 0.10 → WEO surprise 가 bilateral 예측 X → 외생성 robust 신호

## d5_log_X ~ d5_surprise_avg (HAC SE, maxlags=4)
- N=18, β=-0.1056, SE=0.1499, p=0.4812, R²=0.005
- [PASS] p > 0.10 → WEO surprise 가 bilateral 예측 X → 외생성 robust 신호

- saved: `3_derived\identification\test1b_weo_surprise.csv`