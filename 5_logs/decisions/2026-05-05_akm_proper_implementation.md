# AKM 2019 정식 implementation
_2026-05-05_

- Reference: Adão-Kolesár-Morales (2019, QJE 134(4): 1949-2010)
- vs PAP v4.1 § 4.1 의 'AKM (BHJ 2022 simplified)' = industry-mode cluster (NOT 정식 AKM)

- despair panel: n=222
- S matrix: (222, 22) (sigungu × industries)
- w vector: shape (22,), sum=5.77e+10, max=1.98e+10

## Standard OLS
- β = -0.0685
- HC1 SE = 0.0323, t = -2.12

## AKM 2019 정식 SE
- β = -0.0685 (same as OLS)
- AKM SE = 18141390.6095
- AKM t = -0.00

## Simplified AKM (industry-mode cluster, PAP v4.1 § 4.1)
- SE = 0.0188, t = -3.65

## SE 비교
| layer | SE | t-stat |
|-------|-----|--------|
| HC1 | 0.0323 | -2.12 |
| Simplified AKM (industry-mode cluster) | 0.0188 | -3.65 |
| **AKM 2019 정식 (exposure-design)** | **18141390.6095** | **-0.00** |

→ 정식 AKM 가 simplified 보다 conservative (under-clustering 의심 확인)

## tF cutoff (LMP 2022, F=19.65)
- cutoff |t| > 3.84
- AKM 2019 정식 |t|=0.00 ❌ fail

- saved: `4_results\regression\akm_proper_2019.csv`