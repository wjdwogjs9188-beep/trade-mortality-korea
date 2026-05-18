# Goldsmith-Pinkham-Sorkin-Swift 2018 (Rotemberg Weights) — 본 연구 적용 노트

**원논문:** Goldsmith-Pinkham, P., Sorkin, I., & Swift, H. (2018, revised 2019). "Bartik Instruments: What, When, Why, and How." *NBER WP 24408*. Published in *American Economic Review* 110(8): 2586-2624 (2020).

**작성:** 2026-05-01 (Phase 3 IV diagnostic 의 핵심)

---

## 1. Big Picture — Rotemberg 분해의 핵심

이 paper 는 **Bartik IV 가 어떤 산업이 끄는지** 를 분석하는 표준 도구를 제공. 본 연구의 5-layer SE 의 **4번째 layer (Rotemberg diagnostic)** 의 직접 reference.

### Core insight

> Bartik instrument = 산업별 just-identified IV estimator 들의 **가중평균**
> 가중치 = **Rotemberg weights** (k 산업의 instrument 가 어느 정도 contribution)
> 합 = 1

→ "어떤 산업이 IV의 95% variation 을 끄는가?" 분석 가능.

### 핵심 명제

> **Bartik IV 의 식별 가정 = Share exogeneity** (1990 employment share 가 외생)
> Shift exogeneity 가정과 별개 (BHJ 2022 의 path 1 과 다름)

→ 두 가정 (share vs shift) 중 어느 것이 맞는지에 따라 valid IV 가 달라짐.

---

## 2. Rotemberg Decomposition — 본 연구 직접 사용

### 공식
$$\hat{\beta}_{Bartik} = \sum_k \omega_k \hat{\beta}_k$$

- $\hat{\beta}_k$: industry $k$ employment share 를 단독 IV 로 사용한 just-identified estimator
- $\omega_k$: Rotemberg weight (산업 $k$ 의 contribution)
- $\sum_k \omega_k = 1$

### Rotemberg weight 정의
$$\omega_k = \frac{\text{Cov}(z_k, \hat{x}_k)}{\text{Var}(\hat{x}_k)}$$

여기서 $z_k = s_k \cdot g_k$ (share × shift), $\hat{x}_k$ = 산업 $k$ 의 fitted value.

### 본 연구 적용
v3.x 분석 시 발견:
- **KSIC 201 (chemicals) 가 95% Rotemberg weight 점유**
- 즉 Bartik IV 의 거의 모든 variation 이 chemicals 한 산업에서

→ 본 연구의 main result 가 사실 **chemicals industry 에 대한 효과** 임을 의미.

---

## 3. Three Diagnostic Tests (본 연구 직접 차용)

### Test 1: Top-N Rotemberg weights
- 어떤 산업들이 가장 큰 weight 를 가지는지
- v3.x: top 5 = chemicals (95%), textiles (2%), electronics (1%), ...
- **Diagnosis**: chemicals 단독 IV 결과와 비교

### Test 2: Industry-level β_k 분포
- 각 산업의 just-identified β_k 를 다 보기
- Rotemberg weight 큰 산업들의 β_k 가 비슷한 방향이면 robust
- 산업별로 부호 다르면 (heterogeneity 큰) → 결과 의심

### Test 3: Pre-trend by industry
- Rotemberg weight 큰 산업의 pre-trend 별도 검증
- v3.x 의 chemicals industry 가 pre-trend 있으면 결과 비유효

---

## 4. 본 연구 (Trade × Mortality Korea) 적용

### A. Phase 3 의 4번째 SE Layer — Rotemberg

```
Layer 1: HC1 robust SE (baseline)
Layer 2: Cluster-sido SE
Layer 3: AKM SE (Adão-Kolesár-Morales)
Layer 4: Rotemberg weights diagnostic ⭐ ← 이 paper
Layer 5: AR + tF (weak IV)
```

### B. 본 연구 specification

본 연구의 Bartik IV (Korea-China bilateral):
$$\text{Bartik}^{KR-CN}_{c,t} = \sum_j s_{cj,1997} \cdot g_{j,t}$$

- $s_{cj,1997}$: 1997 시군구 c의 산업 j employment share (KSIC 약 24개 KSIC2)
- $g_{j,t}$: t년의 KR-CN net export shock (산업 j)

### C. 본 연구의 Rotemberg 분해 코드 (Phase 3)

```python
# Phase 3 시 작성할 코드
import pandas as pd
import numpy as np

def rotemberg_weights(panel, share_matrix, shifts, outcome):
    """
    panel: 시군구 × year × outcome
    share_matrix: 시군구 × 산업 (1997)
    shifts: 산업 × year (KR-CN net export shock)
    """
    # 산업별 just-identified IV
    betas_k = []
    weights_k = []
    for k in range(n_industries):
        z_k = share_matrix[:, k] * shifts[k, :]  # 산업 k 의 shift-share
        beta_k = np.cov(panel[outcome], z_k) / np.var(z_k)
        betas_k.append(beta_k)
    
    # Rotemberg weights
    fitted_x = bartik_iv  # 전체 Bartik 의 fitted value
    weights_k = np.array([np.cov(z_k, fitted_x) / np.var(fitted_x) for k in range(n_industries)])
    weights_k /= weights_k.sum()  # normalize to 1
    
    return betas_k, weights_k

# 출력: 본 연구 paper 의 robustness table
```

### D. 본 연구의 Rotemberg result 해석

**Scenario 1**: Rotemberg weight 가 분산 (top 5 합 < 50%)
- → IV 가 다양한 산업에서 variation 받음
- → robust, narrative 명확

**Scenario 2**: 한 산업이 50%+ 점유
- → 그 산업의 specific 충격 으로 해석
- → paper 에 명시: "본 연구 결과는 주로 [산업] 의 무역 충격에 의해 끌림"

**Scenario 3 (v3.x 처럼)**: 한 산업이 95%+ 점유
- → 사실상 single-instrument design
- → 보수적 해석, robustness 강화 필요

본 연구 v4.0 에서 KR-CN bilateral 사용 시 **chemicals 외에도 자동차·반도체·기계** 가 important → Rotemberg weight 분산 가능성. v3.x 보다 개선.

### E. 본 연구의 robustness narrative

paper 에 명시:
1. **Main Bartik IV result**: $\hat{\beta} = -1.015$
2. **Rotemberg analysis**:
   - Top 3 산업 weight: chemicals 0.45, automobile 0.25, electronics 0.15
   - 이 3개 산업의 just-identified β_k: -0.9, -1.1, -0.8 (모두 음, 비슷한 magnitude)
   - → IV가 한 산업에 의존 안 함 (v3.x 의 95% 집중과 대조)

**이런 결과가 나오면 본 연구의 robustness 가 매우 강해짐.**

---

## 5. 핵심 인용구

> "We show that the typical use of a Bartik instrument assumes a pooled exposure research design, where the shares measure differential exposure to common shocks, and identification is based on exogeneity of the shares." (Abstract)

> "We build on Rotemberg (1983) and decompose the Bartik estimator into a weighted sum of the just-identified instrumental variable estimators that use each industry share as a separate instrument. The weights, which we refer to as Rotemberg weights, are simple to compute and sum to 1." (Section 1)

> "Heuristically, they [Rotemberg weights] also tell us which exposure design gets more weight." (Section 1)

---

## 6. BHJ 2022 vs Goldsmith-Pinkham 2018 — 두 path

| 가정 | Goldsmith-Pinkham 2018 | BHJ 2022 / 2025 |
|------|----------------------|-----------------|
| Identification | **Share exogeneity** | **Shift exogeneity** |
| Diagnostic | Rotemberg weights | Shift-level F-stat |
| Implication | 산업 별 의존도 | shift 의 randomness |
| Standard error | OLS-based + clustering | AKM SE |

**본 연구는 두 path 모두 사용:**
- Main result: BHJ 2022 (shift exogeneity, AKM SE)
- Robustness: Goldsmith-Pinkham (Rotemberg diagnostic)

→ 두 가정 어느 것이 맞든 결과 robust 함을 보임. 가장 conservative.

---

## 7. 본 연구 paper 의 GP 인용 위치

### Section 3 (Methodology)
- Bartik IV 의 두 가지 식별 path 설명
- 본 연구는 BHJ 2022 main + Goldsmith-Pinkham robustness

### Section 4 (Identification & Diagnostic)
- Rotemberg weights 결과 표 (산업별 weight + β_k)
- 본 연구의 v3.x 와 v4.0 비교 (집중 → 분산)

### Section 6 (Robustness)
- 산업 단독 IV 결과 표
- Top 5 industry 별 robustness

---

## 8. 다음 단계 메모

1. **Phase 3 시 Rotemberg 분해 코드** 작성 (위 example 참고)
2. **시각화**: Rotemberg weights 산업별 bar chart (paper Figure)
3. **0_raw/ssaggregate-main/** R 패키지에 Rotemberg 함수 있는지 확인
4. v3.x 의 chemicals 95% 집중 결과 → v4.0 KR-CN bilateral 로 변경 후 분산 예상 → paper 에 v3 vs v4 변화 명시

---

## 9. 본 연구의 ssaggregate 활용 (R)

```r
library(ssaggregate)

# Bartik IV
bartik_results <- bartik_estimate(
  outcome = mortality_panel$ln_mortality_despair,
  shares = sigungu_industry_share_1997,
  shifts = kr_cn_net_export_shocks
)

# Rotemberg weights
rot_weights <- rotemberg_decomposition(bartik_results)

# 결과 표
print(rot_weights[order(-weight)][1:10, ])  # top 10 산업
```

---

## 10. 본 연구의 v3 → v4 quality 향상

| 항목 | v3.x | v4.0 (이 paper 가이드) |
|------|------|---------------------|
| IV variation 집중 | chemicals 95% (warning) | KR-CN net 분산 (예상) |
| Rotemberg 분석 | 보고만 | 정식 robustness 표 |
| 산업별 β_k | 보고 안 함 | 표로 보고 |
| Pre-trend by industry | 안 함 | 명시 |

→ Goldsmith-Pinkham 2018 의 표준 따름.
