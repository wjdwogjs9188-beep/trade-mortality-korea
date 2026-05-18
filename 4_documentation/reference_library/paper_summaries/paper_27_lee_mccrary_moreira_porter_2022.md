# [#27] Valid t-Ratio Inference for IV

## 메타정보
- **저자**: David S. Lee (Princeton), Justin McCrary (Columbia), Marcelo J. Moreira (FGV), Jack R. Porter (Wisconsin)
- **출판년도**: 2022
- **학술지**: **American Economic Review** vol 112(10): 3260-3290
- **WP**: NBER WP 29124, August 2021 / Revised March 2022
- **JEL**: C01, C1, C26, C36
- **Software**: STATA package at davidlee.princeton.edu/wp/SupplementarytF.html

## Research Question
Single-IV 모형의 t-ratio inference 의 size distortion. F-statistic 함수로서의 **tF critical value c₀.₀₅(F)** 제안. 기존 Stock-Yogo (2005) F=10 rule of thumb 의 정확한 alternative.

## 핵심 contribution

### 1. tF critical value function c₀.₀₅(F)
- F 의 함수로서 정의된 매끄러운 critical value
- F → ∞: c₀.₀₅(F) → 1.96 (conventional)
- F → 3.84⁺: c₀.₀₅(F) → ∞ (infinite, AR matches)
- F = 104.7 부터: c₀.₀₅(F) = 1.96 (no adjustment)

### 2. Standard error adjustment factor
- SE_tF = SE_2SLS × c₀.₀₅(F)/1.96
- → 5% 검정시 |β̂/SE_tF| > 1.96 ⟺ |β̂/SE_2SLS| > c₀.₀₅(F)
- 95% CI: β̂ ± 1.96 × SE_tF

### 3. 정확 critical value 표 (Round 2 정독 후 본 paper 적용 정밀)

| F | c₀.₀₅(F) | SE adjustment factor c₀.₀₅(F)/1.96 |
|---|---|---|
| 4.000 | 18.656 | 9.519 |
| 5.000 | 6.117 | 3.121 |
| 6.000 | ~5.10 | ~2.60 |
| **6.10 (본 paper KR-CN)** | **~5.05** | **~2.58** |
| 8.196 | 3.969 | 2.025 |
| 10.253 | 3.385 | 1.727 |
| 12.374 | 3.090 | 1.577 |
| 17.810 | 3.385 | 1.727 | (오타? 아래 참조)
| 19.167 | 3.309 | 1.688 |
| **19.65 (본 paper ADH-8)** | **3.286** | **1.677** (interpolated) |
| 20.721 | 3.234 | 1.650 |
| 23.455 | 3.090 | 1.576 |
| 33.624 | 2.696 | 1.376 |
| 49.495 | 2.385 | 1.218 |
| 104.67 | 1.96 | 1.00 |

> 정정: 본 paper 의 prior summary "F=20 → cutoff 3.43" 표기는 부정확. 정확값은 F=20.721 → 3.234. 그리고 본 paper 의 F=19.65 의 cutoff 는 **3.286** (interpolation by formula in p.14).

### 4. AR test 와의 비교
- AR (Anderson-Rubin 1949): weak-IV-robust, 모든 F 에서 valid size
- AR CI: F < 3.84 unbounded; F ≥ 3.84 bounded
- **tF expected length < AR expected length** (when both bounded)
- F < 3.84: tF undefined; AR 만 가능

### 5. Magnitude in published AER papers (LMP 2022 의 audit)
- 61개 AER paper 의 single-IV spec audit
- **1/4 specification 에서 SE > 49% 더 커짐** (5% level)
- **1/4 specification 에서 SE > 136% 더 커짐** (1% level)
- 즉, 25% 의 published paper 가 tF 적용 시 inference 변경

## Connection to Trade × Mortality Korea

**역할: § 5 / § 7 의 핵심 method anchor**

본 paper 의 PAP v4.0/4.1 § 7 의 tF inference cutoff 가 직접 LMP 2022 에서 도출:

| 본 paper IV | First-stage F | LMP cutoff (5%) | 본 paper |t| (HC1) | 결과 |
|---|---|---|---|---|
| ADH-8 IV | 19.65 | **3.286** | 1.85 (β=−0.099) | 미달, IV 폐기 |
| KR-CN bilateral IV | 6.10 | **~5.05** | n/a | 적용 불가 (weak-IV) |
| RF z_x_h | (no IV) | 1.96 (HC1) | 2.42 (β=−0.069) | conventional 사용 가능 |

본 paper 의 § 5 / § 7 inference 보고 시 직접 인용:
> "Following Lee, McCrary, Moreira, and Porter (2022), we apply the tF inference correction 
> for IV. Given a first-stage F-statistic of 19.65, the 5% critical value is c₀.₀₅(F) = 3.286 
> (interpolated from Table 3 Panel A). Our 2SLS coefficient β = −0.099 with HC1 standard error 
> 0.054 yields |t| = 1.85, which fails the LMP threshold for IV interpretation. We therefore 
> present results in both reduced-form and IV frames, with the reduced-form coefficient 
> β = −0.069 (HC1 t = 2.42) clearing the conventional 5% threshold."

## 본 paper publication 시 5-layer SE inference 보고 표준

| Inference layer | Description | Cutoff for 5% |
|---|---|---|
| HC1 | t-ratio with HC1 SE | 1.96 (RF) |
| Cluster-sigungu (WCB) | wild bootstrap CR | 1.96 (RF) |
| Cluster-sido | clustered | 1.96 (RF) |
| AKM (BHJ 2022) | shock-only SE | 1.96 (RF) |
| **tF (LMP 2022) for IV** | **F-adjusted t-cutoff** | **3.286 (F=19.65)** |
| AR confidence set | weak-IV robust | bounded if F > 3.84 |

→ 본 paper 가 LMP 적용 한 첫 paper 중 하나 (mortality outcome 측면) 가능성

## Tier
- AER (top-5) — 본 paper publication 시 method 인용 필수
- Software: STATA package, F-statistic 만 있으면 published paper 도 retrospective 적용 가능

## 추가 발견 (Round 2)

### 5% level 외 1% level cutoff
LMP 2022 Panel B (1% level):
- F = 19.65: cutoff ≈ 5.0 (interpolated)
- F = 6.10: cutoff > 10
- 본 paper § 7 의 "1% level" claim 시 더 엄격한 cutoff 적용 필요

### 보고 권고 (LMP 2022 § 5)
1. First-stage F-statistic 보고 (Kleibergen-Paap = F in single-IV)
2. tF SE 가공 → 95% CI: β ± 1.96 × SE_tF
3. 만약 F < 3.84: tF 적용 불가 → AR test only
4. 본 paper 의 F=19.65 ≥ 3.84 → tF 가능 (但 cutoff 3.286)
