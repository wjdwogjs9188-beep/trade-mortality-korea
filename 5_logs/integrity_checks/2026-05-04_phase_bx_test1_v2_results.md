# Phase B-x Test 1 v2 — Reduced univariate spec
_2026-05-04_

v1 결과의 saturation/multicollinearity 인공물 가능성 후 재spec.
- Bonferroni-corrected α = 0.05/6 = **0.0083**

- panel rows: 25 (2000-2024)
- usable obs (all macros non-null): 19

## VIF report (multicollinearity 진단)

```
             variable       VIF
d5_log_GDP_지출_실질_lag1  4.005213
      d5_log_수출가_lag1 10.000943
      d5_log_수입가_lag1 27.941655
      d5_log_CPI_lag1  1.832377
  d5_log_KRW_USD_lag1  6.433608
 d5_log_BoK_rate_lag1  1.745422
```

[WARN] VIF > 10 for 2 variables — v1 saturation 진단 확인

## Univariate test (1 macro at a time, HAC maxlags=4)

| macro | N | β | SE | p | sig (Bonf) |
|-------|---|---|----|---|-----|
| GDP_지출_실질 | 19 | +4.820 | 1.753 | 0.0060 | **YES** |
| 수출가 | 19 | +1.005 | 0.674 | 0.1357 |  |
| 수입가 | 19 | +0.759 | 0.270 | 0.0049 | **YES** |
| CPI | 19 | -3.859 | 3.070 | 0.2088 |  |
| KRW_USD | 19 | +0.526 | 0.247 | 0.0336 | . |
| BoK_rate | 19 | +0.135 | 0.192 | 0.4836 |  |

**Bonferroni-significant macros: 2 / 6**

## Non-overlapping 5y bin (saturation-free)

- non-overlapping bin obs: **4** (only diagnostic — N too low for inference)
```
 year     log_M  d_log_M
 2000 23.272606      NaN
 2005 24.377763 1.105157
 2010 24.993985 0.616222
 2015 25.225836 0.231850
 2020 25.413551 0.187715
```

## v2 결정

- [FAIL] 2 macros Bonferroni 후 유의
- bilateral 의 Korea macro contamination 의 강한 증거
- **C.ii branch 진입 검토**: ADH-8 Bartik 으로 main spec, bilateral 은 robustness 만