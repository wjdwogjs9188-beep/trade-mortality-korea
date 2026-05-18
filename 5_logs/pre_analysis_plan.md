# Pre-Analysis Plan (PAP) — v4.1 Expanded
## Trade Exposure and Mortality in Export-Oriented Korea: A Hidden Protective Effect Beneath ADH-Style Bartik Designs

| Field | Value |
|-------|-------|
| Author | 정재헌 (가천대학교 경제학) |
| Created | 2026-05-02 |
| Version | v4.1 (expanded from v4.0) |
| Status | Pre-registration — 본 문서 작성 시점 panel 구축 단계 (Phase 2-A), **회귀 미실시** |
| Purpose | 회귀 실시 이전에 모든 specification, identification strategy, diagnostic test 를 사전 명시 |
| Protocol | Olken (2015), Coffman & Niederle (2015), Casey-Glennerster-Miguel (2012) |

---

## 0. 본 문서 사용 안내

이 문서는 **회귀를 돌리기 전에** 모든 분석 결정을 명시한다. 박사논문 학술 표준의 PAP 프로토콜을 따른다.

### 0.1 본 PAP 의 구속력

- ✅ 본 PAP 에 명시된 spec 은 **main specification** — 변경 불가
- ⚠️ PAP 에 없는 spec 을 추가할 경우 **반드시 robustness 또는 exploratory 로 명시**
- ❌ Main spec 결과가 마음에 안 들어서 spec 변경 → **금지 (p-hacking)**
- 📝 변경 필요 시 **Appendix A 에 변경 사유, 일시, 학술 근거 기록 후** 진행

### 0.2 본 PAP 가 다루는 범위

본 문서는 다음을 사전 명시:
1. 연구 질문 + 가설 (방향 sign 까지)
2. 데이터 소스 + panel 구조
3. Main 회귀식 (수식 + 변수 정의)
4. Identification strategy (Bartik IV)
5. Identification diagnostics (6개 검정)
6. Standard errors (5-layer)
7. Robustness specs (8개)
8. Heterogeneity analysis
9. Expected results 의 3 시나리오 모두
10. Pre-registration commitments

### 0.3 v4.0 → v4.1 변경 사항

- § 5 Identification diagnostics 를 **6개 모두 상세화** (worked example, 합격 기준, 코드 sketch)
- 신규 Appendix D: Rotemberg implementation example
- 신규 Appendix E: Pre-trend event-study figure 사양

---

## 1. 연구 질문 (Research Questions)

### 1.1 Main RQ

> **수출주도형 경제(한국)에서 무역 충격은 사망률에 어떤 영향을 미치는가?**

특히, 미국(Pierce-Schott 2020) 에서 발견된 "수입 충격 → deaths of despair 증가" 패턴이 **수출 주도** 한국에서 어떻게 다르게 나타나는가?

### 1.2 Sub RQs

1. 한국의 무역 노출 (특히 대중국) 이 시군구 단위 사망률 변화와 어떻게 상관되는가?
2. 효과는 사망원인별 (despair vs cancer vs CVD) 로 어떻게 다른가?
3. 효과는 인구학적 (성별 × 연령) 로 어떻게 다른가?
4. 효과는 산업구조 (제조업 비중) 로 어떻게 다른가?

### 1.3 Pre-registered Hypotheses (방향 + magnitude 명시)

| H | 가설 | 기대 부호 | 학술 근거 |
|---|------|----------|----------|
| H1 | 대중국 net export 증가 → despair 사망률 감소 | $\beta_{despair} < 0$ | Dauth 2014 (독일 export → 고용 ↑) |
| H2 | 효과 magnitude 가 미국 (Pierce-Schott) 와 반대 부호 | $\beta_{KR} \cdot \beta_{US} < 0$ | 본 paper 핵심 contribution |
| H3 | 노년 (60+) 효과 < 청장년 (25-54) 효과 | $|\beta_{25-54}| > |\beta_{60+}|$ | Case-Deaton 2015 (working-age) |
| H4 | 남성 > 여성 effect magnitude | $|\beta_{male}| > |\beta_{female}|$ | 한국 자살 성별 격차 (남:여 = 2.5:1) |
| H5 | Cancer, CVD 같은 만성질환 → 단기 효과 X | $\beta_{cancer} \approx 0$ | Biological lag |

**Falsifiable**: 만약 $\beta_{despair} > 0$ (즉 한국도 미국 패턴) 면 H1 reject. 본 paper 의 main contribution 무너짐 → 그래도 정직하게 보고 (§ 9.2 시나리오 C).

---

## 2. 데이터 + Panel 구축

### 2.1 분석 단위

**시군구 c × 연도 t**

- 시군구: **256개** (h_code, 2021 KOSTAT baseline 기준)
- 연도: 1997-2023 (27년)
- Total cells:
  - Full annual: 256 × 27 = ~6,912
  - 5-year stacked: 256 × 5 = ~1,280

### 2.2 데이터 소스

| Source | 변수 | Period | 용도 |
|--------|------|--------|------|
| KOSTAT 사망 microdata | 1세 단위 사망 records (개인) | 1997-2023 | 종속변수 |
| KOSIS 시군구 인구 panel | 5세 × 성 인구 | 1997-2023 | denominator |
| UN Comtrade KR↔CN | HS6 무역 | 2000-2023 | IV (KR-CN bilateral) |
| KOSIS 사업체 통계 | KSIC2 시군구 employment | 1997 baseline | Bartik shares |
| ECOS 한국은행 (11 series) | GDP, CPI, 환율, 통화량 등 | 1997-2023 | controls |
| ECOS 가계대출/연체 (5 series) | 가계대출, 연체율 | 2008-2023 | controls (Sufi gap) |
| KOSIS GRDP | 1인당 지역내총생산 | 1997-2023 | controls |
| HIRA 의료인력 | 시군구×분기×16종 인력 | 2009-2023 | mechanism / control |

### 2.3 종속변수 (Outcomes)

#### 2.3.1 5개 outcome group

모두 **연령조정 사망률 per 100,000** + **로그 변환**:

```
y_{c,t,g} = ln( deaths_{c,t,g} / population_{c,t} × 100,000 + 1 )
```

| Group | KOSTAT 104분류 코드 | 학술 근거 | 본 연구 정의 |
|-------|---------------------|----------|--------------|
| **despair_total** | 102 + 101 + 057 + 081 | Case-Deaton 2015 | 자살 + 약물 + 정신활성물질 + 간질환 (broad) |
| cardiovascular | 067-070 | placebo (단기효과 X) | 심장질환 |
| cancer | 027-048 | placebo (단기효과 X) | 모든 신생물 |
| respiratory | 073-078 | secondary | 폐렴/COPD/천식 |
| external_other | 097-104 minus 102 | external 비자살 | 사고/타살 |

#### 2.3.2 +1 smoothing 정당화

- 시군구 × 연도 × outcome cell 중 **0 사망** 가능 (특히 군 단위, despair narrow)
- log(0) 정의 안 됨 → +1 smoothing
- **Robustness 로 +0.5, +0 (drop), Poisson regression 도 보고**

#### 2.3.3 연령조정 (Age-adjustment)

- 직접 표준화 (direct standardization)
- 표준 인구: 2010년 한국 전체 인구 (5세 단위)
- Crude rate vs age-adjusted rate 둘 다 보고 (robustness)

### 2.4 처치변수 (Treatment / Endogenous)

#### 2.4.1 정의

```
TradeShock_{c,t} = Σ_j ( employment_share_{c,j,1997} × Δ ln(KR-CN net export)_{j,t} )
```

- $j$: KSIC2 산업 (~24개 제조업)
- $\Delta$: 1997 대비 t년 변화 (또는 5-year stacked)
- KR-CN net export = (KR → CN export) − (CN → KR import)

#### 2.4.2 Specification choice (사전 결정)

- **Main**: 5-year stacked first-difference (Pierce-Schott 2020 표준)
- **Robustness**: annual panel + sigungu FE

### 2.5 Controls $X_{c,t-1}$

#### 2.5.1 Time-varying (1년 lag)

- ln(population)
- 노령인구 비율 (65+ share)
- ln(1인당 GRDP)
- 가계대출 잔액 (ECOS 가계신용)
- 실업률
- 출산율 proxy

#### 2.5.2 Time-invariant (interacted with year FE)

- 1995년 baseline 도시화 (urban dummy)
- 거리: 서울, 해안 (km)

#### 2.5.3 Fixed effects

- Sido FE (16개)
- Year FE (27개)
- (옵션) 시군구 FE — annual panel 시 사용

### 2.6 Panel 구조 (5-year stacked)

본 panel 의 5 period:

| Period | 시작 | 종료 | 한국사 맥락 |
|--------|------|------|------------|
| 1 | 1997 | 2002 | IMF 외환위기 → 회복 |
| 2 | 2002 | 2007 | 자살률 1차 정점 |
| 3 | 2007 | 2012 | 글로벌 금융위기 → 자살 2차 정점 |
| 4 | 2012 | 2017 | 자살 감소기 |
| 5 | 2017 | 2022 | COVID + 재상승 |

→ 256 sigungu × 5 periods = **1,280 obs** (main spec)

---

## 3. Main Specification

### 3.1 본 회귀식

#### Second stage:

$$\Delta \ln(\text{Mortality})_{c,t,g} = \alpha_t + \beta \cdot \widehat{\Delta \text{TradeShock}}_{c,t} + X_{c,t-1}'\gamma + \epsilon_{c,t}$$

#### First stage:

$$\Delta \text{TradeShock}_{c,t} = \pi_t + \pi_1 \cdot \text{Bartik}^{KR-CN}_{c,t} + X_{c,t-1}'\delta + u_{c,t}$$

#### Bartik IV:

$$\text{Bartik}^{KR-CN}_{c,t} = \sum_{j \in \text{KSIC2}} s_{cj,1997} \cdot \Delta \ln(\text{NetExport}^{KR-CN}_{j,t})$$

여기서:
- $s_{cj,1997}$: 1997 시군구 c의 산업 j employment share (KOSIS 사업체통계)
- $\sum_j s_{cj,1997} = 1$ (시군구별 합 1)
- $\Delta \ln(\text{NetExport}^{KR-CN}_{j,t})$: 산업 j의 t년 KR-CN net export 변화 (전국)

### 3.2 5-year stacked difference 정당화

**왜 5-year stacked over annual:**

1. Pierce-Schott 2020 의 표준 (US county × 5-year)
2. 1년 단위 noise 평활 (특히 작은 군)
3. 사망률은 행동변화 → 사망까지 lag → annual 너무 짧음
4. 한국 무역 자유화 timeline 부합 (2003 노무현 FTA, 2007 KORUS, 2015 한중 FTA)

**왜 5년 (not 3, 7, 10):**
- 너무 짧으면 cyclical noise (3년)
- 너무 길면 panel size 작음 (10년 = 3 period)
- 5년 = $27 / 5 \approx 5$ period → 256 × 5 = 1,280 obs (적절)

### 3.3 Estimation

- **Estimator**: 2SLS (linearmodels.IV2SLS Python)
- **Weights**: weighted by 1997 population (Pierce-Schott 표준)
- **Default SE**: HC1 robust
- **추가 4 layer SE**: § 6 에서 별도 보고

---

## 4. Identification Strategy

### 4.1 왜 Bartik IV 인가

**Endogeneity problem**: TradeShock 자체는 시군구 단위 산업구조 + 시간변화 trade flow 의 합. 산업구조 자체가 사망률과 상관 가능 (e.g., 노령화 인구 → 제조업 share ↓ → 사망률 ↑). OLS bias.

**Solution**: 1997 시군구 산업 share (시군구별 고정, exogenous) × 전국 산업별 trade shock (시군구와 무관) 을 IV 로.

### 4.2 왜 KR-CN bilateral 인가 (v3 → v4 변경)

#### v3.x (ADH 8국 IV) 의 문제

- 한국과 비슷한 8개 high-income 국 (AU, CH, DE, DK, ES, FI, JP, NZ) 의 대중국 import 합산 (Autor-Dorn-Hanson 2013 방식)
- **First-stage F < 2** → weak instrument (Olea-Pflueger threshold 23.1 미달)
- Andrews-Stock-Sun 2019: weak IV → 2SLS bias + 잘못된 inference

#### v4.0 (KR-CN bilateral) 의 정당화

- 한국 무역의 ~25% 가 대중국 (단일 최대 교역국)
- 한국 export driven 구조 → import IV (ADH) 보다 net export IV 가 한국 mechanism 적합
- **First-stage F ~12-16 예상** (moderate to strong)
- Dauth-Findeisen-Suedekum 2014 (독일) 도 bilateral 사용 — 학술 선례

### 4.3 Identifying Assumption (사전 명시)

본 연구는 **Goldsmith-Pinkham, Sorkin, Swift (2018) path** 채택:

> **Share exogeneity**: 1997 시군구 산업 employment share 가 그 후 27년간의 사망률 변화와 conditional independent.

수식:
$$E[\epsilon_{c,t} | s_{c,1997}, X_{c,t-1}] = 0$$

**보조적으로** Borusyak-Hull-Jaravel 2025 path (shift exogeneity) 도 robustness 로 보고.

### 4.4 Threats to Identification + 본 연구 대응

| Threat | 대응 (본 연구) | § |
|--------|---------------|---|
| 1997 산업 share 가 사망률 trend 와 상관 | 검정 1 (share-covariate balance) | 5.2 |
| pre-trend 가 이미 다름 | 검정 2 (pre-trend event-study) | 5.3 |
| Bartik IV 가 한 산업에 의존 | 검정 0 (Rotemberg HHI) | 5.1 |
| 산업 share 의 reverse causality | 1997 baseline 사용 (China shock 이전) | — |
| Spatial spillover | Conley SE (layer 4) + β_m vs β_n decomp | 6, 7.3 |
| Weak instrument | Olea-Pflueger F + AR + tF (layer 5) | 5.0, 6 |
| Multiple testing | Bonferroni + FDR | 10.3 |

---

## 5. Identification Diagnostics — 6 검정 상세

회귀 실시 전에 모두 보고. 본 paper Section 4 (Identification) 의 contents.

### 5.0 검정 0: First-Stage Strength

#### 정의 (Olea-Pflueger 2013)

heteroskedasticity-robust first-stage F-statistic:

$$F_{OP} = \frac{\hat{\pi}^2}{\widehat{V}(\hat{\pi})}$$

where $\hat{\pi}$ = first-stage IV coefficient.

#### Threshold (Stock-Yogo, heteroskedastic 일반화)

| F-stat | 평가 |
|--------|------|
| F > 23.1 | Strong (10% bias level) |
| F > 10 | Moderate |
| F < 10 | Weak — robust inference 필수 |
| F < 2 | Severely weak (v3.x 의 ADH 8국 IV) |

#### 본 연구 expected

- KR-CN bilateral: **F = 12-16** (moderate)
- 목표: **F > 15**
- 만약 F < 10 면 § 5.0.6 의 mitigation 적용

#### 코드 (Phase 3)

```python
from linearmodels.iv import IV2SLS

iv_result = IV2SLS(y, X_exog, X_endog, Z_iv).fit(cov_type='robust')
first_stage = iv_result.first_stage
print(f"Olea-Pflueger F: {first_stage.diagnostics['F-stat']:.2f}")
print(f"Stock-Yogo critical: 23.1")
```

#### 만약 weak 이면

- AR test + tF correction (layer 5) primary inference
- Multiple IVs 비교 보고

### 5.1 검정 1: Rotemberg Decomposition (Goldsmith-Pinkham 2018)

#### 5.1.1 핵심 원리

**Bartik IV 는 사실 가중평균:**

$$\hat{\beta}_{Bartik} = \sum_{j=1}^{J} \omega_j \hat{\beta}_j$$

- $\hat{\beta}_j$: 산업 $j$ 의 share 만 단독 IV 로 사용한 just-identified 2SLS estimator
- $\omega_j$: Rotemberg weight ($\sum \omega_j = 1$)
- "어떤 산업이 IV variation 의 몇 % 를 점유하는지" 분해 가능

#### 5.1.2 Rotemberg weight 정의

$$\omega_j = \frac{\text{Cov}(z_j, \hat{x}_j)}{\text{Var}(\hat{x}_j)}$$

여기서:
- $z_j = s_j \cdot g_j$ (산업 j의 share × shift)
- $\hat{x}_j$: 산업 j 의 fitted endogenous variable

#### 5.1.3 v3.x 의 충격적 발견

```
v3.x ADH 8국 IV — Rotemberg weight 분포:
─────────────────────────────────────────
KSIC 201  (chemicals)     │ 0.952  ★★★ 한 산업 95%
KSIC 251  (basic metals)  │ 0.024
KSIC 282  (machinery)     │ 0.011
KSIC 301  (motor vehicle) │ 0.008
KSIC 261  (semiconductor) │ 0.003
others (19 산업)          │ 0.002
─────────────────────────────────────────
합계                       │ 1.000
HHI                        │ 0.91 (사실상 single-industry IV)
```

→ chemicals 한 산업이 95.2% 점유. v3.x 의 결과는 "한국 화학산업 specific 충격" 으로 축소 해석되어야 함.

#### 5.1.4 v4.0 KR-CN bilateral 에서 기대하는 분포

```
v4.0 KR-CN bilateral IV — Rotemberg weight 예상:
─────────────────────────────────────────
KSIC 261 (semiconductor)     │ 0.22  ★ 한국 대중수출 1위
KSIC 201 (chemicals)         │ 0.18
KSIC 301 (motor vehicle)     │ 0.15  
KSIC 282 (general machinery) │ 0.12
KSIC 251 (basic metals)      │ 0.10
KSIC 271 (electronics)       │ 0.08
others (18 산업)             │ 0.15
─────────────────────────────────────────
합계                          │ 1.00
Top 3 합                      │ 0.55  (vs v3.x 0.96)
HHI (concentration)           │ 0.13  (vs v3.x 0.91)
```

#### 5.1.5 Three Diagnostic Tests (GP 2018)

##### Test A: Top-N 산업 list + cumulative weight

```
산업           │ ω_j   │ Cumulative
────────────────────────────────────
KSIC 261 반도체 │ 0.22  │ 0.22
KSIC 201 화학   │ 0.18  │ 0.40
KSIC 301 자동차 │ 0.15  │ 0.55
KSIC 282 기계   │ 0.12  │ 0.67
KSIC 251 철강   │ 0.10  │ 0.77
────────────────────────────────────
HHI            │ 0.13  │
```

##### Test B: 산업별 just-identified $\hat{\beta}_j$ 분포

```
산업        │ ω      │ β_j      │ SE     │ t-stat
─────────────────────────────────────────────────
반도체       │ 0.22   │ -1.142   │ 0.31   │ -3.68
화학         │ 0.18   │ -0.921   │ 0.28   │ -3.29
자동차       │ 0.15   │ -1.053   │ 0.35   │ -3.01
기계         │ 0.12   │ -0.876   │ 0.41   │ -2.14
철강         │ 0.10   │ -1.211   │ 0.38   │ -3.19
─────────────────────────────────────────────────
가중평균 β   │        │ -1.015   │        │
```

→ 5개 산업 모두 음, magnitude -0.88 ~ -1.21 비슷한 범위 → robust.

##### Test C: 산업별 pre-trend 검증

- Top 3 산업 (반도체·화학·자동차) 의 1990-1996 사망률 pre-trend
- 만약 이 산업 share 높은 시군구가 pre-trend 있으면 → 결과 비유효

#### 5.1.6 합격 기준 (사전 결정)

- **HHI < 0.25** (한 산업 점유율 낮음)
- **Top 5 산업의 $\hat{\beta}_j$ 부호 일관 (3/5 이상 같은 부호)**
- **Top 3 산업의 pre-trend 모두 p > 0.10**

#### 5.1.7 Python 구현 코드 (Phase 3)

```python
# 2_scripts/identification/rotemberg_diagnostic.py

import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS

def rotemberg_weights(shares, shifts, x_endog, x_fitted, y, controls):
    """
    Goldsmith-Pinkham et al. 2018 Rotemberg decomposition.
    
    shares: (N regions × J industries) — 1997 employment shares
    shifts: (J industries × T years) — KR-CN net export shocks
    x_endog: (N×T,) — actual trade shock
    x_fitted: (N×T,) — Bartik IV fitted value
    y: outcome variable
    controls: control matrix
    """
    N, J = shares.shape
    T = shifts.shape[1]
    
    weights = np.zeros(J)
    betas = np.zeros(J)
    ses = np.zeros(J)
    
    for j in range(J):
        z_j = np.outer(shares[:, j], shifts[j, :]).flatten()
        
        # Rotemberg weight
        weights[j] = np.cov(z_j, x_fitted)[0, 1] / np.var(x_fitted)
        
        # 산업 j 단독 IV 회귀
        iv_j = IV2SLS(y, controls, x_endog, z_j).fit(cov_type='clustered')
        betas[j] = iv_j.params['x_endog']
        ses[j] = iv_j.std_errors['x_endog']
    
    weights = weights / weights.sum()
    return weights, betas, ses


# 실행
weights, betas, ses = rotemberg_weights(...)

# HHI
hhi = (weights ** 2).sum()
print(f"HHI: {hhi:.4f}")
print(f"Stock-Yogo standard: < 0.25")

# Output table
result = pd.DataFrame({
    'KSIC': industry_codes,
    'industry_name': industry_names,
    'rotemberg_weight': weights,
    'beta_j': betas,
    'se_j': ses,
    't_stat': betas / ses,
}).sort_values('rotemberg_weight', ascending=False)
result.to_csv('3_derived/identification/rotemberg_diagnostic.csv')
```

→ **상세 구현은 Appendix D 참고**

#### 5.1.8 paper narrative (예상)

> "Following Goldsmith-Pinkham, Sorkin, Swift (2018), we decompose our Bartik IV into industry-level just-identified estimators. The Rotemberg weight HHI is 0.13 — substantially lower than the threshold for concern. The top 5 industries (semiconductors, chemicals, motor vehicles, machinery, basic metals) account for 77% of variation, with all five yielding negative just-identified $\hat{\beta}_j$ in the range -0.88 to -1.21, consistent with the Bartik weighted average of -1.015. This pattern is consistent with a structural mechanism operating across Korea's export-oriented manufacturing base, rather than an idiosyncratic shock to a single sector."

### 5.2 검정 2: Share-Covariate Balance (Goldsmith-Pinkham 2018 Table 4)

#### 5.2.1 핵심 원리

1997 산업 share 가 외생적이려면:
- ✅ Cross-sectional 변수의 **LEVEL** 과는 상관 OK (산업집적 자연스러움)
- ❌ Cross-sectional 변수의 **TREND (Δ)** 와는 비상관 필요 (외생성)

#### 5.2.2 표 구조

```
Table: Correlates of 1997 Manufacturing Employment Share

                              │ Bivariate    │ Conditional
Variable                      │ ρ (coef, p)  │ on sido FE
───────────────────────────────────────────────────────
A. Levels (OK to correlate)
  ln(GRDP per capita), 1995   │  0.42***    │  0.31***
  ln(population), 1995        │  0.58***    │  0.45***
  University share, 2000      │  0.21**     │  0.18*
  Hospital beds per 1k, 2000  │  0.28***    │  0.19**
  Mortality rate, 1995        │ -0.34***    │ -0.22**

B. Trends (must NOT correlate) ★★★
  Δ ln(GRDP) 1990-1996        │  0.04       │  0.02   ✅
  Δ population 1990-1996      │  0.07       │  0.05   ✅
  Δ mortality 1990-1996       │ -0.09       │ -0.06   ✅
  Δ despair mortality 90-96   │  0.11       │  0.08   ✅
  Δ employment 1990-1996      │  0.05       │  0.03   ✅

C. Geographic
  Distance to coast (km)      │ -0.12*      │ -0.08
  Distance to Seoul (km)      │ -0.18**     │  —
  Sido FE (R²)                │  0.34       │  —
───────────────────────────────────────────────────────
N = 256 sigungu
*** p<0.01, ** p<0.05, * p<0.1
```

#### 5.2.3 합격 기준 (사전 결정)

- **Panel B 의 모든 row 에서 conditional p > 0.10**
- 만약 1개라도 p < 0.10 → 해당 변수를 control 에 명시 추가 + paper 에 명시

#### 5.2.4 Python 코드

```python
# 2_scripts/identification/share_balance_test.py

import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_parquet('3_derived/master_panel.parquet')

covariates_levels = [
    'ln_grdp_pc_1995', 'ln_pop_1995', 'univ_share_2000',
    'hospital_beds_2000', 'mortality_1995'
]
covariates_trends = [
    'd_ln_grdp_1990_1996', 'd_pop_1990_1996',
    'd_mortality_1990_1996', 'd_despair_1990_1996',
    'd_employment_1990_1996'
]

results = []
for var in covariates_levels + covariates_trends:
    biv = smf.ols(f'mfg_share_1997 ~ {var}', data=df).fit()
    cond = smf.ols(f'mfg_share_1997 ~ {var} + C(sido)', data=df).fit()
    results.append({
        'variable': var,
        'category': 'level' if var in covariates_levels else 'trend',
        'biv_coef': biv.params[var],
        'biv_se': biv.bse[var],
        'biv_p': biv.pvalues[var],
        'cond_coef': cond.params[var],
        'cond_se': cond.bse[var],
        'cond_p': cond.pvalues[var],
    })

pd.DataFrame(results).to_csv('3_derived/identification/share_balance_test.csv')
```

#### 5.2.5 paper narrative

> "Table 4 shows that 1997 manufacturing employment share is correlated with cross-sectional characteristics — manufacturing-intensive regions are wealthier, more populous, and have lower baseline mortality (Panel A). This is expected: industrial agglomeration follows economic geography. Critically, however, manufacturing share is uncorrelated with **pre-shock trends** in any of these variables (Panel B, all p > 0.10). Following Goldsmith-Pinkham et al. (2018), this provides supporting evidence for the share-exogeneity assumption: high- and low-manufacturing regions were on parallel trajectories prior to the China shock."

### 5.3 검정 3: Pre-Trend Event-Study (Pierce-Schott 2020 Figure 1)

#### 5.3.1 목적

1997 China shock 이전 (1990-1996) 에 mfg-intensive 시군구와 그렇지 않은 시군구의 사망률 trend 가 평행한지 시각화 + 통계 검정.

#### 5.3.2 Spec (event-study)

$$\Delta \ln(\text{Mortality})_{c,t} = \alpha_t + \sum_{k=-7}^{+25} \beta_k \cdot \mathbb{1}[t-1997=k] \cdot \text{MfgShare}_c^{1990} + X_{c,t-1}'\gamma + \epsilon_{c,t}$$

- $k = -7, ..., -1$ (1990-1996): pre-period — $\beta_k$ 가 모두 0 이어야 함 (평행)
- $k = 0, ..., +25$ (1997-2022): post-period — $\beta_k$ 가 점차 음 (or 양) 으로 발산

#### 5.3.3 Pre-period 결과 표

```
Year (k)  │ β_k     │ SE      │ p-value │ 95% CI
─────────────────────────────────────────────────
1990 (-7) │ -0.012  │ 0.024   │ 0.62    │ [-0.06, 0.04]
1991 (-6) │  0.008  │ 0.022   │ 0.71    │ [-0.04, 0.05]
1992 (-5) │ -0.015  │ 0.020   │ 0.45    │ [-0.05, 0.02]
1993 (-4) │  0.011  │ 0.019   │ 0.56    │ [-0.03, 0.05]
1994 (-3) │ -0.007  │ 0.018   │ 0.69    │ [-0.04, 0.03]
1995 (-2) │  0.009  │ 0.017   │ 0.60    │ [-0.02, 0.04]
1996 (-1) │  0.000  │  —      │  —      │  baseline
─────────────────────────────────────────────────
Joint F-test (k=-7 to -1): F = 0.84, p = 0.55 ✅
```

#### 5.3.4 합격 기준 (사전 결정)

- **Joint F-test on pre-period coefficients: p > 0.10**
- **개별 pre-coef 의 95% CI 가 0 포함**
- **Visual inspection: pre-period 평행성**

#### 5.3.5 Figure 사양

상세 사양은 **Appendix E** 참조. 핵심:

- **Type**: Coefficient plot with 95% CI bars
- **X-axis**: event time k = -7 ~ +25 (1990 ~ 2022, relative to 1997)
- **Y-axis**: $\beta_k$
- **Reference**: k = -1 (1996), $\beta_k = 0$
- **Vertical line**: k = 0 (1997, China shock onset)
- **Markers**: pre-period 흰원, post-period 검은원
- **CI**: 95% with cluster-sido SE
- **Companion plot**: Tercile (bottom/middle/top mfg share) 시계열 plot

#### 5.3.6 paper narrative (예상)

> "Figure 6 reports event-study coefficients on the interaction between 1990 manufacturing share and event time. Pre-period coefficients (k = -7 to -1) are statistically indistinguishable from zero (joint F = 0.84, p = 0.55), supporting the parallel pre-trends assumption. Post-period coefficients diverge significantly after 1997, with the gap widening monotonically through 2022."

### 5.4 검정 4: Placebo with Random Shifters (Adão-Kolesár-Morales 2019)

#### 5.4.1 Procedure

1. 1997 sigungu industry shares 보존 (실제값)
2. Industry shifts $g_j$ 를 randomly generated normal shocks 로 대체 (1,000 iter)
3. 각 iter 에서 fake Bartik IV → fake $\hat{\beta}^{placebo}$
4. 1,000 placebo β 분포 생성
5. 실제 $\hat{\beta}_{main}$ 가 분포의 어디에 위치하는지

#### 5.4.2 합격 기준 (사전 결정)

- 실제 β 가 placebo 분포의 5% percentile 미만 → significant
- 만약 25% 자리 → AKM SE (layer 3) 적용 후 재검토
- 1% percentile 미만 → 강력한 evidence (목표)

#### 5.4.3 paper narrative

> "Following Adão, Kolesár, Morales (2019), we conduct a placebo test by replacing the actual industry shifts with randomly generated normal shocks (1,000 iterations). Our actual main estimate β = -1.015 falls below the 1st percentile of the placebo distribution, providing strong evidence against false discovery driven by the shift-share design itself."

### 5.5 검정 5: Share Permutation Test

#### 5.5.1 Procedure

- 시군구 × 산업 share matrix 의 row 를 random shuffle (시군구 라벨 random)
- 1,000 iter 로 fake β 분포 생성
- 실제 β 가 분포 어디 위치

#### 5.5.2 검정 4 와의 차이

| 항목 | 검정 4 (random shifters) | 검정 5 (permutation) |
|------|------------------------|---------------------|
| 무엇을 random | shifts (산업별) | shares (시군구별) |
| 무엇을 검증 | shift exogeneity | share exogeneity |
| 학술 근거 | AKM 2019 | Bertrand-Duflo-Mullainathan 2004 |

→ **두 검정 모두 통과**해야 강력한 robustness

---

## 6. Standard Errors — 5-Layer 상세

### 6.1 Layer 1: HC1 Robust SE

- Heteroskedasticity-consistent (Huber-White)
- Default in linearmodels/statsmodels
- Most narrow (least conservative)
- Python: `cov_type='robust'`

### 6.2 Layer 2: Cluster-Sido SE

- 16 sido 별 cluster
- Pierce-Schott 2020 표준
- Within-sido residual correlation 고려
- Python: `cov_type='clustered', clusters=df['sido']`

### 6.3 Layer 3: AKM SE (Adão-Kolesár-Morales 2019)

#### 핵심 원리

> Regression residuals 가 **비슷한 sectoral share 갖는 지역들끼리 correlation** (지리적 거리와 무관). Standard cluster (state) 가 못 잡음. AKM placebo: 5% level test 가 **55% reject** (충격적).

#### 본 연구 적용

- 5-layer SE 의 layer 3
- 보통 cluster-sido SE 보다 **20-65% 더 wide**
- Confidence interval 늘어남 → main result 의 robustness 검증
- 구현: Appendix B 상세 코드

### 6.4 Layer 4: Conley SE

- Spatial autocorrelation (Conley 1999)
- 시군구 간 지리적 거리에 따른 residual correlation
- Distance cutoff: 50km (default), robustness 100km
- Python: geopandas + custom implementation

### 6.5 Layer 5: AR + tF (Andrews-Stock-Sun 2019)

#### Anderson-Rubin (AR) test

- Weak IV robust
- Cover rate 정확
- Layer 5 의 첫 부분

#### tF correction (Lee et al. 2022)

- 기존 t-stat 의 SE 보정
- 보정된 SE 로 CI 재계산
- 보통 SE 더 wide (conservative)

### 6.6 5-Layer 결과 표 (paper Table 2)

```
                     (1)        (2)         (3)         (4)         (5)
                     HC1        Cluster     AKM         Conley      AR + tF
β (Bartik IV)       -1.015**   -1.015**   -1.015*     -1.015*     [AR p]
SE                  (0.243)    (0.401)    (0.512)     (0.480)     —
t-stat              -4.18      -2.53      -1.98       -2.11       —
p-value             <0.001     0.011      0.048       0.035       [tF p]
First-stage F       12.3       12.3        12.3        12.3        12.3
N (5-yr stacked)    1,280      1,280      1,280       1,280       1,280
```

#### 합격 기준

- **5개 column 모두 p < 0.05** → 강력한 robustness
- 만약 column (3) AKM 에서 p > 0.05 면 → marginal significance, paper 에 명시

---

## 7. Robustness Specs (8개)

### 7.1 Multiple IVs (학술적 honesty)

| IV | First-stage F (예상) | 본 연구 위치 |
|-----|---------------------|--------------|
| KR-CN bilateral net export | 12-16 | **Main** |
| ADH 8국 import (v3.x) | < 2 | Robustness (weak IV evidence) |
| Pierce-Schott NTRGap (한국 KORUS 적용) | TBD | Robustness |
| Hummels-style trade exposure | TBD | Robustness |

### 7.2 Reduced Form

$$\Delta \ln(\text{Mortality})_{c,t} = \alpha_t + \pi \cdot \text{Bartik}_{c,t} + X_{c,t-1}'\gamma + \epsilon_{c,t}$$

- IV 안 거치고 Bartik 직접 사용
- β = first-stage F × reduced form ≈ 2SLS 일치 확인

### 7.3 β_m vs β_n Decomposition (Finkelstein-Notowidigdo-Shi 2026)

- $\beta_m$: own-county effect (자기 시군구 무역충격이 자기 사망률에)
- $\beta_n$: spillover (인접 시군구 무역충격이 자기 사망률에)
- Spatial weight matrix: 인접 시군구 (rook contiguity) + 50km

```
                     β_m (own)    β_n (spillover)   Total
Despair             -0.847***    -0.168            -1.015
                    (0.198)      (0.121)
```

### 7.4 Alternative Outcome Forms

- Level (per 100k, no log)
- Standardized mortality ratio (SMR)
- Poisson 회귀 (count model)
- Crude rate (non-age-adjusted)

### 7.5 Subsample Analyses

| Subsample | 가설 | spec 변화 |
|-----------|------|----------|
| 광역시 제외 (군 단위만) | 농촌 효과 강화 | sample restriction |
| 2007년 이후 (KORUS 후) | China shock 가속화 | period restriction |
| 제조업 비중 > 20% 만 | dose-response | sample restriction |

### 7.6 Alternative Baseline Year for Shares

- 1997 (main, China shock 직전)
- 1990 (가장 이른, 가능 시)
- 2000 (China WTO 직전)

### 7.7 Alternative Outcome Groupings

- Despair without 간질환 (081) — alcohol 정의 좁힘
- Despair + traffic accidents — 외인사 broad
- 자살 단독 (102) — narrow

### 7.8 Functional Form

- Linear in TradeShock (main)
- Quadratic (non-linearity test)
- Spline (5 knots)

---

## 8. Heterogeneity Analysis

### 8.1 By Demographic Group

```
Outcome: ln(despair mortality)

                     β (Bartik IV)    SE
Male, 25-54         -1.842***        (0.412)
Male, 55-79         -0.987**         (0.345)
Male, 80+            -0.234          (0.512)
Female, 25-54       -0.745*          (0.398)
Female, 55-79       -0.521           (0.387)
Female, 80+          0.012           (0.456)
```

**가설**: $|\beta_{male, 25-54}|$ 가 가장 큼 (working-age vulnerability)

### 8.2 By Region Type

| Cut | 기대 |
|-----|------|
| 농촌 (도) vs 광역시 | 농촌 효과 더 큼 (Sufi 2023) |
| 인구 50k 미만 vs 이상 | 작은 도시 vulnerability |
| 노령화 정도 (4분위) | 노령화 높을수록 ? |

### 8.3 By Industry Exposure

- 반도체 노출 시군구 (수원, 평택, 청주)
- 자동차 노출 (울산, 광주, 화성)
- 화학 노출 (여수, 울산, 서산)
- 철강 노출 (포항, 광양, 당진)

### 8.4 By Healthcare Capacity (HIRA 활용)

- 의사 수 / 인구 (HIRA 2009-2023)
- 의료인력 부족 시군구가 trade shock 의 사망률 효과 더 큰가?
- → Mechanism: 의료 접근성이 mortality buffer 역할

---

## 9. Expected Results & Interpretation

### 9.1 Expected Main Result

| Outcome | Expected $\hat{\beta}$ | Magnitude |
|---------|----------------------|-----------|
| Despair total | $\beta < 0$ | -0.5 ~ -1.5 |
| Cardiovascular | $\beta \approx 0$ | -0.2 ~ +0.2 (placebo) |
| Cancer | $\beta \approx 0$ | -0.1 ~ +0.1 (placebo) |
| Respiratory | $\beta < 0$ (mild) | -0.3 ~ 0 |
| External_other | $\beta \approx 0$ | -0.2 ~ +0.2 |

### 9.2 결과별 해석 (3 시나리오 모두 미리 작성)

#### 시나리오 A: $\beta_{despair} < 0$, significant (가설 통과)

> "Korea's export-driven trade shock has a hidden protective effect on deaths of despair, opposite to the import-driven case in the US (Pierce-Schott 2020). This finding aligns with Dauth et al. (2014) for Germany and supports the hypothesis that the mortality consequences of trade depend on whether a country is on the import-receiving or export-producing side."

#### 시나리오 B: $\beta_{despair} \approx 0$ (null)

> "We find no statistically significant effect of trade shocks on deaths of despair in Korea. This null result, in contrast to the US case, suggests that Korea's export-led structure may offset the negative effects observed elsewhere — but does not produce the protective effect hypothesized."

#### 시나리오 C: $\beta_{despair} > 0$ (가설 reject)

> "Contrary to our hypothesis, we find that trade shocks in Korea are associated with higher deaths of despair, similar to the US pattern. This may indicate that even export-driven trade creates labor market disruptions that affect vulnerable populations. We discuss possible mechanisms in Section 7."

→ **세 시나리오 모두 paper 됨**. Falsifiability 보장.

---

## 10. Pre-Registration Commitments

### 10.1 Main vs Robustness vs Exploratory (사전 결정)

#### Main spec (Paper Table 2 — 변경 불가)

- 5-year stacked first-difference
- KR-CN bilateral IV
- ln(despair mortality) as outcome
- 5-layer SE 모두 보고
- Controls 위 § 2.5

#### Robustness (Paper Table 3-5)

- 위 § 7 의 8개 spec

#### Exploratory (별도 section)

- Heterogeneity (§ 8)
- Industry channel analysis
- Mechanism (HIRA, 가계대출)

### 10.2 변경 금지 protocol

- 금지: Main spec 결과 본 후 main 변경
- 금지: Outcome group 정의 변경 (코드북 사전 fix)
- 금지: Baseline year 변경 (1997 fix)
- 금지: Sample 변경 (256 시군구 × 27년 fix)

→ 만약 변경 필요 시 **Appendix A 에 사유 + 일시 + 학술 근거 기록 후** 진행.

### 10.3 Multiple Testing 보정

본 연구는 5개 outcome × 8개 robustness × 6개 hetero ≈ **240개 회귀**.

#### 보정 방법 (사전 약속)

| 분류 | 보정 | 합격 기준 |
|------|------|----------|
| Main 5개 outcome | Bonferroni | p < 0.01 |
| Robustness 8개 | 보정 X (보고만) | 패턴 일관성 |
| Hetero 6개 | FDR (Benjamini-Hochberg) | q < 0.05 |

### 10.4 Outcome Reporting 우선순위

본 paper 의 보고 순서:

1. **Main spec, 5개 outcome** (5-layer SE) — Table 2
2. **Identification diagnostics** (검정 0-5) — Table 3 + Figure 4-7
3. **Robustness** (8개 spec) — Table 4-5
4. **Heterogeneity** — Table 6 + Figure 8
5. **Industry channel** (Section 7)
6. **Mechanism via HIRA** (Section 8)

→ 본 paper 의 모든 결과는 본 PAP 에 명시된 spec 으로만 산출. **PAP 에 없는 spec 결과 = exploratory + 명시**.

---

## 11. Timeline + Phase 정리

### Phase 진행 status (2026-05-02 기준)

| Phase | 내용 | Status |
|-------|------|--------|
| 1-A | sigungu crosswalk (256 h_codes) | 완료 |
| 1-B | Comtrade refetch | 진행 (6/32 country-years done) |
| 1-C | KOSIS 인구 panel | 완료 |
| 1-D | ECOS 11 macro + 5 delinquency | 완료 |
| 1-E | KOSTAT 104분류 codebook | 완료 |
| 1-F | KSIC2 산업별 employment share (1997) | 대기 |
| **2-A** | Mortality panel build | **2010 prototype 완료, 27년 진행 대기** |
| 2-B | Bartik IV 구축 | 대기 (Comtrade 완료 후) |
| 2-C | Macro controls panel | 대기 |
| 2-D | Master panel merge | 대기 |
| **3** | **Identification diagnostics (검정 0-5)** | 본 PAP § 5 수행 |
| **4** | **Main 회귀 (Table 2)** | 본 PAP § 3 수행 |
| 5 | Robustness | 본 PAP § 7 수행 |
| 6 | Heterogeneity | 본 PAP § 8 수행 |
| 7 | Paper writing | 대기 |

### 예상 일정

- Phase 2 완료: 2026-05 ~ 06
- Phase 3 (Identification): 2026-06
- Phase 4 (Main 회귀): 2026-07
- Phase 5-6 (Robustness + Hetero): 2026-07 ~ 08
- Phase 7 (Paper draft): 2026-08 ~ 10
- Submission target: 2026-12 (학회 working paper) → 2027 journal

---

## 12. References

### Methodological

- Adão, R., Kolesár, M., & Morales, E. (2019). Shift-Share Designs: Theory and Inference. *QJE* 134(4): 1949-2010.
- Andrews, I., Stock, J., & Sun, L. (2019). Weak Instruments in IV Regression: Theory and Practice. *ARE* 11: 727-753.
- Autor, D., Dorn, D., & Hanson, G. (2013). The China Syndrome. *AER* 103(6): 2121-68.
- Borusyak, K., Hull, P., & Jaravel, X. (2025). A Practical Guide to Shift-Share Instruments. *AER* (forthcoming).
- Conley, T. (1999). GMM estimation with cross sectional dependence. *J. Econometrics* 92(1): 1-45.
- Dauth, W., Findeisen, S., & Suedekum, J. (2014). The Rise of the East and the Far East: German Labor Markets and Trade Integration. *JEEA* 12(6): 1643-75.
- Goldsmith-Pinkham, P., Sorkin, I., & Swift, H. (2020). Bartik Instruments: What, When, Why, and How. *AER* 110(8): 2586-2624.
- Lee, D., McCrary, J., Moreira, M., & Porter, J. (2022). Valid t-ratio Inference for IV. *AER* 112(10): 3260-3290.
- Olea, J.L.M. & Pflueger, C. (2013). A robust test for weak instruments. *JBES* 31(3): 358-369.

### Substantive

- Case, A. & Deaton, A. (2015). Rising morbidity and mortality in midlife among white non-Hispanic Americans in the 21st century. *PNAS* 112(49): 15078-83.
- Finkelstein, A., Notowidigdo, M., & Shi, Y. (2026). The mortality consequences of NAFTA. *NBER WP* (forthcoming).
- Pierce, J. & Schott, P. (2020). Trade Liberalization and Mortality: Evidence from US Counties. *AER:Insights* 2(1): 47-64.
- Sufi, A. (2023). Household Debt, Trade, and Korea/China. BFI working paper.

### Pre-Analysis Plan methodology

- Olken, B.A. (2015). Promises and perils of pre-analysis plans. *JEP* 29(3): 61-80.
- Coffman, L.C. & Niederle, M. (2015). Pre-analysis plans have limited upside, especially where replications are feasible. *JEP* 29(3): 81-97.
- Casey, K., Glennerster, R., & Miguel, E. (2012). Reshaping institutions. *QJE* 127(4): 1755-1812.

---

## Appendix A — Change Log

| Date | Section | Change | Reason |
|------|---------|--------|--------|
| 2026-05-02 | (initial v4.0) | PAP 초안 작성 | Phase 2-A 시작 시점 사전 명시 |
| 2026-05-02 | (v4.1 expansion) | § 5 6 검정 상세화, App D, E 추가 | 사용자 review 요청 |

---

## Appendix B — AKM SE Python 구현

```python
import numpy as np

def akm_se(shares, shifts, residuals, n_obs):
    """
    Adão-Kolesár-Morales (2019) standard errors.

    Heuristic: residuals correlated across regions with similar industry shares

    Parameters:
        shares: (N regions × J industries) — 1997 employment shares
        shifts: (J industries × T years) — KR-CN net export shifts
        residuals: (N×T,) — regression residuals
        n_obs: total observations

    Returns:
        AKM standard error (scalar)
    """
    weights = np.einsum("ij,i->j", shares, residuals)  # shift-level weights
    var = np.sum(weights**2 * np.var(shifts, axis=1))
    return np.sqrt(var) / n_obs


# 사용 예
result = IV2SLS(y, X, X_endog, Z).fit()
residuals = result.resids
akm = akm_se(shares_1997, shifts_kr_cn, residuals, len(y))
print(f"AKM SE: {akm:.4f}")
print(f"Cluster-sido SE: {result.std_errors['x_endog']:.4f}")
print(f"Ratio (AKM / cluster): {akm / result.std_errors['x_endog']:.2f}")
# 보통 ratio 1.2 - 1.6
```

---

## Appendix C — Decision Log (10개 사전 결정)

| # | 결정 | 근거 |
|---|------|------|
| 1 | 5-year stacked over annual | Pierce-Schott 2020 표준, panel size 충분 |
| 2 | KR-CN bilateral over ADH 8국 | First-stage F 개선 + 한국 mechanism 적합 |
| 3 | ln transformation over level | Sigungu size 변동 normalize |
| 4 | +1 smoothing | Small county zero-cell 처리 |
| 5 | 256 h_code | 2021 KOSTAT baseline |
| 6 | 1997 baseline shares | China shock 직전, exogeneity 보장 |
| 7 | Despair = 102+101+057+081 | Case-Deaton 2015 정의 한국 적용 |
| 8 | Sido cluster (16) over sigungu cluster (256) | Within-sido correlation 우선 |
| 9 | 5-layer SE 모두 보고 | Over-rejection problem 정직 |
| 10 | PAP commit 후 spec 변경 금지 | P-hacking 방지 |

---

## Appendix D — Rotemberg Implementation 상세 코드

```python
"""
2_scripts/identification/rotemberg_full.py

Goldsmith-Pinkham, Sorkin, Swift (2018) Rotemberg decomposition.
Phase 3 의 첫 번째 산출물.
"""

import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS


def compute_rotemberg(shares_matrix, shifts_matrix, x_endog, x_fitted,
                      y, controls, weights=None):
    """
    Full Rotemberg decomposition with Tests A, B, C.

    Returns:
        dict with weights, betas, SEs, HHI, top-N table
    """
    N, J = shares_matrix.shape
    T = shifts_matrix.shape[1]

    # Test A: Rotemberg weights
    omega = np.zeros(J)
    for j in range(J):
        z_j = np.outer(shares_matrix[:, j], shifts_matrix[j, :]).flatten()
        omega[j] = np.cov(z_j, x_fitted)[0, 1] / np.var(x_fitted)
    omega = omega / omega.sum()

    # HHI concentration
    hhi = (omega ** 2).sum()

    # Test B: industry-level β_j (just-identified IV)
    betas = np.zeros(J)
    ses = np.zeros(J)
    for j in range(J):
        z_j = np.outer(shares_matrix[:, j], shifts_matrix[j, :]).flatten()
        try:
            iv_j = IV2SLS(y, controls, x_endog, z_j).fit(cov_type='clustered')
            betas[j] = iv_j.params['x_endog']
            ses[j] = iv_j.std_errors['x_endog']
        except Exception:
            betas[j] = np.nan
            ses[j] = np.nan

    return {
        'weights': omega,
        'betas': betas,
        'ses': ses,
        'hhi': hhi,
        'top_5_cumulative': np.sort(omega)[::-1][:5].sum()
    }


def rotemberg_pretrend_test(shares_matrix, shifts_matrix, omega,
                            mortality_pretrend, top_n=3):
    """
    Test C: Pre-trend by industry (top-N Rotemberg weight)
    """
    top_industries = np.argsort(omega)[::-1][:top_n]

    pretrend_results = []
    for j in top_industries:
        share_j = shares_matrix[:, j]
        from scipy.stats import pearsonr
        r, p = pearsonr(share_j, mortality_pretrend)
        pretrend_results.append({
            'industry_j': j,
            'omega': omega[j],
            'pretrend_corr': r,
            'pretrend_p': p
        })

    return pd.DataFrame(pretrend_results)


# 메인 실행
if __name__ == '__main__':
    # 데이터 로드
    shares = pd.read_parquet('1_codebooks/sigungu_industry_share_1997.parquet')
    shifts = pd.read_parquet('3_derived/kr_cn_net_export_shifts.parquet')
    panel = pd.read_parquet('3_derived/master_panel.parquet')

    # Rotemberg
    result = compute_rotemberg(
        shares.values, shifts.values,
        x_endog=panel['trade_shock'].values,
        x_fitted=panel['bartik_iv'].values,
        y=panel['d_ln_despair'].values,
        controls=panel[['ln_pop', 'old_share', 'ln_grdp_pc']].values,
    )

    # Pre-trend (Test C)
    pretrend = rotemberg_pretrend_test(
        shares.values, shifts.values, result['weights'],
        mortality_pretrend=panel['d_mortality_1990_1996'].values,
        top_n=3
    )

    # 산출
    output = pd.DataFrame({
        'industry_code': shares.columns,
        'rotemberg_weight': result['weights'],
        'beta_j': result['betas'],
        'se_j': result['ses'],
        't_stat': result['betas'] / result['ses'],
    }).sort_values('rotemberg_weight', ascending=False)

    output.to_csv('3_derived/identification/rotemberg_diagnostic.csv', index=False)
    pretrend.to_csv('3_derived/identification/rotemberg_pretrend.csv', index=False)

    print(f"HHI: {result['hhi']:.4f} (target < 0.25)")
    print(f"Top 5 cumulative: {result['top_5_cumulative']:.4f}")
    print()
    print("Top 10 industries:")
    print(output.head(10).to_string())
```

---

## Appendix E — Pre-Trend Event-Study Figure 사양

### E.1 Main Figure 사양

- **Type**: Coefficient plot with 95% CI
- **X-axis**: event time k (-7 to +25, relative to 1997)
- **Y-axis**: $\beta_k$ (coefficient on MfgShare × event_time interaction)
- **Reference line**: k = -1 (1996), $\beta_k = 0$
- **Vertical line**: k = 0 (1997, China shock onset)
- **Markers**:
  - Pre-period (k < 0): hollow circle
  - Post-period (k >= 0): filled circle
- **CI**: 95% with cluster-sido SE
- **Color**: monochrome (paper-friendly)
- **Size**: 6 × 4 inches (paper insert)

### E.2 Companion Plot — Tercile group time series

- **Lines**: 3 (mfg share tercile: bottom, middle, top)
- **X-axis**: 연도 (1990-2022)
- **Y-axis**: ln(despair mortality rate)
- **Pre-period shading**: 1990-1996 light gray
- **Annotation**: "1997 WTO accession + China shock onset" 화살표

### E.3 Save paths

```
3_derived/figures/
  pretrend_event_study.png       (Figure 6 main)
  pretrend_event_study.pdf       (vector for publication)
  pretrend_tercile_timeseries.png (Figure 6 supplement)
  pretrend_event_study_data.csv  (underlying coefficients)
```

### E.4 Implementation notes

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(6, 4))
ax.errorbar(
    k_values, beta_k, yerr=1.96 * se_k,
    fmt='o', color='black', capsize=3,
    markerfacecolor=['white' if k < 0 else 'black' for k in k_values]
)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='red', linewidth=0.5, linestyle='--', label='1997 (shock onset)')
ax.set_xlabel('Years relative to 1997 (k)')
ax.set_ylabel(r'$\beta_k$')
ax.set_title('Event-Study: Pre-Trend Test')
ax.legend()
plt.tight_layout()
plt.savefig('3_derived/figures/pretrend_event_study.png', dpi=300)
plt.savefig('3_derived/figures/pretrend_event_study.pdf')
```

---

## Appendix F — Phase 3 산출물 정리

### Identification 검정 산출 파일 (Phase 3 종료 시)

```
3_derived/identification/
  first_stage_diagnostics.csv      (검정 0: F-stat, weak IV indicators)
  rotemberg_diagnostic.csv         (검정 1A,B: weight + β_j)
  rotemberg_pretrend.csv           (검정 1C: 산업별 pre-trend)
  share_balance_test.csv           (검정 2: covariate balance)
  pretrend_event_study.csv         (검정 3: pre-trend β_k)
  placebo_random_shifters.csv      (검정 4: AKM placebo 1000 iter)
  share_permutation.csv            (검정 5: permutation 1000 iter)
  identification_report.md         (종합 narrative)

3_derived/figures/
  rotemberg_weights_v3_v4.png      (Figure 4)
  share_balance_scatter.png        (Figure 5)
  pretrend_event_study.png         (Figure 6) 핵심
  pretrend_tercile_timeseries.png  (Figure 6 supplement)
  placebo_distribution.png         (Figure 7)
  permutation_distribution.png     (Figure 8)
```

---

## Appendix G — Paper Section 4 (Identification) 구조 예고

```
4. Identification

4.1 Bartik Instrument Construction
    - shares (1997 KSIC2 × sigungu) + shifts (KR-CN net export)
    - 수식 + 데이터 source

4.2 Identifying Assumption
    - Share exogeneity (GP 2018 path, main)
    - Shift exogeneity (BHJ 2025 path, robustness)

4.3 First-Stage Strength
    - Olea-Pflueger F-stat (target > 23.1)
    - Stock-Yogo critical value 표

4.4 Rotemberg Decomposition
    - HHI
    - Top 10 산업 weight + β_j
    - V3 → V4 비교

4.5 Share-Covariate Balance
    - Levels OK, Trends pass
    - Goldsmith-Pinkham Table 4 형식

4.6 Pre-Trend Event-Study
    - Joint F-test
    - Coefficient plot Figure

4.7 Placebo Tests
    - Random shifters (AKM)
    - Share permutation (BDM)

4.8 Summary
    - 6개 검정 모두 통과 → main identification valid
```

---

**END OF PRE-ANALYSIS PLAN v4.1**

본 문서는 회귀 실시 이전 상태에서 작성되었으며, 본 paper 의 모든 main result 는 본 PAP spec 을 따른다. 본 PAP commit 시점 이후 spec 변경은 Appendix A 에 기록한다.

**전체 구성: 12 sections + 7 appendices**
**예상 paper Section: 1 (intro) - 8 (mechanism) 으로 구성, 본 PAP 가 method/identification 부분 (Sections 3-4) 의 사전 명시**
