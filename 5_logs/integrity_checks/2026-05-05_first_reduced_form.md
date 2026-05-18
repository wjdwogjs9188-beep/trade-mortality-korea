# 첫 reduced form (preliminary main result)
_2026-05-05_

- spec: Δlog(rate)_2000_2010 ~ z_x_h^{KR-CN}
- IV: bilateral KR-CN z_x_per_worker (Phase B-x A.ii main)

- mortality panel: (31494, 8)
- IV panel: (226, 4)

## Outcome: **despair_total**
- d_log panel: 236 h_code
- after merge IV: n=222
- N=222, R²=0.043
- β (standardized) = -0.0685
- SE HC1 = 0.0323, t=-2.12, p=0.0340
- SE cluster-sido = 0.0221, t=-3.11, p=0.0019
- tF inference (cutoff |t|>3.43): HC1 ❌, cluster ❌
- 해석: 1 sd 더 노출 → 6.9% 더 사망률 *감소* (protective effect — 본 paper 핵심 가설)

## Outcome: **cancer**
- d_log panel: 236 h_code
- after merge IV: n=222
- N=222, R²=0.000
- β (standardized) = -0.0050
- SE HC1 = 0.0264, t=-0.19, p=0.8502
- SE cluster-sido = 0.0333, t=-0.15, p=0.8811
- tF inference (cutoff |t|>3.43): HC1 ❌, cluster ❌
- 해석: 1 sd 더 노출 → 0.5% 더 사망률 *감소* (protective effect — 본 paper 핵심 가설)

## Outcome: **cardiovascular**
- d_log panel: 236 h_code
- after merge IV: n=222
- N=222, R²=0.001
- β (standardized) = -0.0129
- SE HC1 = 0.0284, t=-0.46, p=0.6488
- SE cluster-sido = 0.0259, t=-0.50, p=0.6181
- tF inference (cutoff |t|>3.43): HC1 ❌, cluster ❌
- 해석: 1 sd 더 노출 → 1.3% 더 사망률 *감소* (protective effect — 본 paper 핵심 가설)

## Outcome: **respiratory**
- d_log panel: 211 h_code
- after merge IV: n=198
- N=198, R²=0.000
- β (standardized) = -0.0118
- SE HC1 = 0.0439, t=-0.27, p=0.7889
- SE cluster-sido = 0.0602, t=-0.20, p=0.8452
- tF inference (cutoff |t|>3.43): HC1 ❌, cluster ❌
- 해석: 1 sd 더 노출 → 1.2% 더 사망률 *감소* (protective effect — 본 paper 핵심 가설)

## Outcome: **external_other**
- d_log panel: 236 h_code
- after merge IV: n=222
- N=222, R²=0.002
- β (standardized) = +0.0135
- SE HC1 = 0.0468, t=+0.29, p=0.7727
- SE cluster-sido = 0.0758, t=+0.18, p=0.8584
- tF inference (cutoff |t|>3.43): HC1 ❌, cluster ❌
- 해석: 1 sd 더 노출 → 1.4% 더 사망률 증가 (positive trade shock effect on external_other)

- saved: `3_derived\regression\first_reduced_form_results.csv`

## Summary table
| outcome | n | β | SE_HC1 | t_HC1 | tF sig (HC1) | t_cluster | tF sig (cluster) |
|---------|---|---|--------|-------|--------------|-----------|-------------------|
| despair_total | 222 | -0.069 | 0.032 | -2.12 | — | -3.11 | — |
| cancer | 222 | -0.005 | 0.026 | -0.19 | — | -0.15 | — |
| cardiovascular | 222 | -0.013 | 0.028 | -0.46 | — | -0.50 | — |
| respiratory | 198 | -0.012 | 0.044 | -0.27 | — | -0.20 | — |
| external_other | 222 | +0.014 | 0.047 | +0.29 | — | +0.18 | — |

## 결정
- 본 turn 의 spec: 10y change (2000-2010), no FE, HC1 + cluster-sido, tF inference
- year FE 와 5-layer SE 추가 = Phase 4 별도 turn
- 본 결과는 **preliminary** — final 은 Romano-Wolf step-down 후 확정