# AKM v2 — BHJ 2022 ssaggregate approach
_2026-05-05_

- Task 13 v1 의 unit 폭발 (SE=18M) 교정
- BHJ 2022 RES 의 ssaggregate equivalence + cluster SE

- region panel: n=222

## Standard OLS (region-level)
- β (std) = -0.0685
- HC1 SE = 0.0323, t = -2.12
- industry filter: 22 → 21 (zero-emp drop 1)

## ssaggregate transformation
- J = 21 industries
- Ȳ stats: mean=0.1126, sd=0.0813
- w stats: mean=2.75e+09, sd=4.15e+09
- w_std stats: mean=0, sd=1 (standardized)

## ssaggregate (BHJ 2022) regression — AKM SE equivalent
- β = +0.0191 (note: scale different from region-level β)
- SE = 0.0118
- t = +1.61
- N (industries) = 21
- 해석: industry-level 회귀에서 1 sd shock 증가시 exposure-weighted mortality +1.9% 변화

## Rotemberg HHI + effective J (BHJ 2022 § 5)
- Rotemberg HHI = 0.6644
- Effective J = 1/HHI = 1.5
- 해석: J=22 nominal industries, but effective J = 2 (concentration check)

## Top 5 industries (Rotemberg weight)
```
ksic9_2digit rotemberg_weight
 C26 0.806811
 C24 0.111552
 C20 0.020084
 C28 0.014498
 C30 0.014053
```

## SE 비교 (final)
| Layer | SE | t-stat |
|-------|-----|--------|
| HC1 (region-level) | 0.0323 | -2.12 |
| **ssaggregate (BHJ 2022, AKM equivalent)** | **0.0118** | **+1.61** |

## tF cutoff (LMP 2022, F=19.65)
- cutoff |t| > 3.84
- ssaggregate (AKM equivalent) |t| = 1.61 ❌ fail

- saved: `4_results\regression\akm_bhj2022_ssaggregate.csv`