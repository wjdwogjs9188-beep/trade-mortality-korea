# Test 1 v3 — drop 수입가 (VIF=27.9 sensitivity)
_2026-05-04_

- Bonferroni α = 0.05/5 = **0.0100**

- usable obs: 19

## VIF (5 macros, 수입가 제외)
```
d5_log_GDP_지출_실질_lag1 VIF = 1.24
d5_log_수출가_lag1 VIF = 2.27
d5_log_CPI_lag1 VIF = 1.78
d5_log_KRW_USD_lag1 VIF = 2.71
d5_log_BoK_rate_lag1 VIF = 1.64
```

## Univariate (HAC maxlags=4)

| macro | N | β | SE | p | sig (Bonf α=0.01) |
|-------|---|---|----|---|-----|
| GDP_지출_실질 | 19 | +4.820 | 1.753 | 0.0060 | **YES** |
| 수출가 | 19 | +1.005 | 0.674 | 0.1357 | |
| CPI | 19 | -3.859 | 3.070 | 0.2088 | |
| KRW_USD | 19 | +0.526 | 0.247 | 0.0336 |. |
| BoK_rate | 19 | +0.135 | 0.192 | 0.4836 | |

**Bonferroni-significant: 1/5**

## v3 결정

- v2 의 GDP 단독 유의 - business cycle 동조 (year FE 가 흡수)
- 수입가 유의성은 multicollinearity 인공물 확정
- **A.i main 결정 strong**: year FE 가 GDP comovement 흡수, identification 유효