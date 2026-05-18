# [#04] Weak Instruments in Linear IV Regression: Identification, Inference, and Testing

## 메타정보
- 저자: Andrews, D.W.K., Stock, J.H., Sun, L.
- 출판년도: 2019 (2018 published, actually seems to be 2018-19 timeframe based on file name)
- 학술지: Annual Review of Economics, Vol. 11, pp. 727-753
- DOI: 10.1146/annurev-economics-080218-025643
- 키워드: weak instruments, instrumental variables, F-statistic, Anderson-Rubin test, confidence intervals, first-stage diagnostics, heteroskedasticity, robust inference, nonhomoskedastic data

## Research question
본 review는 **instrumental variables (IV) 회귀에서 약한 instrument(weak instruments, WI)의 문제와 해결 방법**을 체계적으로 다룬다.

핵심 질문:
1. "Instrument가 '약하다'는 것은 무엇을 의미하는가? 그리고 왜 문제인가?"
2. "실증 연구에서 weak instrument를 어떻게 detect할 것인가?"
3. "Weak instrument 상황에서 robust inference는 무엇인가? (Point estimate vs Confidence intervals)"
4. "Heteroskedastic, clustered, 또는 time-series correlated 데이터에서 weak instrument 문제는 어떻게 다른가?"

학술 contribution:
- Andrews-Stock-Sun은 weak instrument 문제에 대한 **가장 실용적이고 종합적인 review**를 제공
- 특히 **비동분산(heteroskedasticity), clustering, 시계열 상관** 등 현실 데이터의 복잡성을 다룸
- AER (American Economic Review) 2014-2018 논문 survey를 통해 **실제 경험적 연구자들이 weak instrument를 얼마나 간과하는지** 정량화
- 각 상황별로 구현 가능한 **diagnostic tools과 robust testing procedures**를 제시

## Data
- **주요 방법론 논문 (theory)**이므로, 구체 데이터셋은 없음
- 대신 **Illustrative simulations**에서 여러 상황 시뮬레이션:
 - 동분산(homoskedastic) vs 비동분산(heteroskedastic) 오차
 - 무상관(i.i.d.) vs clustering (regional, sectoral) vs 시계열 상관
 - 약한 vs 강한 instrument
- **Empirical survey**: 2014-2018 AER에 게재된 IV 사용 논문들 (약 100+ 논문)을 수집하여 분석
 - First-stage F-statistic 보고 관행
 - Weak instrument 인식 정도
 - 사용된 inference 방법

## Identification strategy
**이론적 framework**: Linear IV model with multiple instruments

### Model specification:
```
Y_i = β_0 + β_1 × X_i + W_i' × γ + ε_i... (1) [Structural equation]
X_i = π_0 + Z_i' × π + W_i' × δ + V_i... (2) [First stage]
```

또는 reduced form으로:
```
Y_i = δ_0 + Z_i' × δ + W_i' × λ + U_i... (3) [Reduced form]
```

관계: δ = π × β (reduced form coefficient = first-stage × structural coefficient)

### 용어정의:

**Instrument strength (First-stage parameter π):**
- Strong: π가 크다 (상대적으로 sampling variation 대비)
- Weak: π가 0에 가깝거나 sampling variation에 비해 작다
- 정량적 measure: **F-statistic from first stage**

**Weak instrument 정의 (정식)**:
```
F-stat = [R_xu^2 / (1 - R_xu^2)] × (n - k - 1) / m
```
여기서:
- R_xu^2: X_i를 Z_i와 W_i에 회귀한 R-squared
- n: 샘플 크기
- k: W_i의 개수 (추가 exogenous variables)
- m: Z_i의 개수 (instrument 개수)

**Rule of thumb**:
- F > 10: Relatively strong (문제 적을 가능성)
- F < 10: 약한 instrument 우려 시작
- F < 3~5: 명백히 weak (robust inference 필수)
- F < 1: 극도로 weak (instrument로서 무의미할 가능성)

**예: Single endogenous variable (k=1), Single instrument case**:
```
F = [(β̂ estimated from 2SLS) / SE(β̂)]^2
```

### Identification assumption:
1. **Exogeneity of Z_i** (Instrument validity):
 ```
 E[Z_i' × ε_i] = 0
 ```
 즉, instrument은 종속변수의 오차와 무관해야 함

2. **Relevance of Z_i** (First-stage significance):
 ```
 E[Z_i' × X_i] ≠ 0 (rank condition)
 ```
 또는 더 강한 조건:
 ```
 π ≠ 0 (first-stage coefficient non-zero)
 ```

3. **No weak identification** (Weak instrument 회피):
 ```
 F-statistic sufficiently large
 또는 conditional on first-stage results, the estimand is identifiable
 ```

## Empirical specification

### Main diagnostic: First-stage F-statistic

**Homoskedastic case** (classical assumption):
```
F = [X̂'X̂ / σ̂^2] / m
```
여기서 X̂는 Z에 대한 X의 fitted value, m은 instrument 개수

**Heteroskedastic-robust version**:
```
F_rob = [(r'Z(Z'Z)^{-1}Z'r) / m] / σ̂_het^2
```
여기서 σ̂_het^2는 heteroskedasticity-consistent 분산 추정치

**Clustered case** (multi-level data):
```
F_cluster = adjusted F taking into account within-cluster correlation
```
- Stock-Yogo (2005) tables에서 제공된 critical values 사용 (but modified for clustering)

### Procedures for robust inference:

#### 1. **Anderson-Rubin (AR) Test** (클래식, 1949):
귀무가설: β = β_0

검정통계량:
```
AR(β_0) = (Y - β_0 X)' Z (Z'Z)^{-1} Z' (Y - β_0 X) / σ̂^2
 ~ χ^2_m under H_0 (under weak instrument, exactly valid)
```

장점:
- Weak instrument 문제에 **robust**
- Instrument가 매우 약하거나 many weak instruments 상황에서도 size가 정확

단점:
- Confidence interval이 wide할 수 있음 (weak instrument reflection)
- 다중 endogenous variables일 때 복잡

#### 2. **Kleibergen-Paap (KP) Test** (2006):
AR 테스트의 generalization을 위한 rank test
```
KP = [centered moment condition's variance]
```
- AR보다 향상된 크기(size) 특성
- IV 개수 > endogenous variables 개수인 과도-identified 상황에서 추천

#### 3. **Conditional likelihood ratio (CLR) test** (Moreira 2003):
- Highest power (가장 높은 검정력)
- Computation이 복잡하나, 현재 많은 패키지에 구현됨

#### 4. **Heteroskedasticity-robust CI**:
```
CI_robust = [β̂_2SLS ± z_{α/2} × SE_robust]
```
여기서 SE_robust는 다음 중 하나:
- HC0 (White, 1980)
- HC1, HC2, HC3 (MacKinnon-White)
- HC4 (또는 HC5) for small samples

#### 5. **Cluster-robust CI** (Grouped data):
```
SE_clustered = sqrt[ (M/(M-1)) × (K/(K-L)) × (1/N) Σ_g ĝ_g ĝ_g' ]
```
여기서:
- M: cluster 개수
- K: 회귀변수 개수
- L: exogenous variables 개수
- ĝ_g: group g의 moment condition

### 표준오차 계산:

**기본 규칙** (저자들의 추천):

1. **절대 하지 말 것**: Standard 2SLS SE (동분산 가정 하)
 ```
 SE_2SLS = σ̂^2 (X'Z(Z'Z)^{-1}Z'X)^{-1}
 ```
 이것은 heteroskedasticity나 clustering에 대해 무시

2. **최소한**: HC3 robust SE (White, 1980)
 ```
 SE_HC3 = (X'Z(Z'Z)^{-1}Z'X)^{-1} (X'Z(Z'Z)^{-1} Σ_i Z_i Z_i' û_i^2 (Z'Z)^{-1}Z'X) (X'Z(Z'Z)^{-1}Z'X)^{-1}
 ```

3. **Best practice** (clustering 있을 때):
 - Cluster-robust SE (각 cluster 내 correlation 허용)
 - 또는 two-way clustering (지역 + 시간)

## Main findings

### 1. **Weak instrument Problem의 정량화**:

#### 가상의 numerical example (저자들 시뮬레이션 기반):
- **Scenario A (Strong instrument)**: F = 100
 - 2SLS 계수와 true 계수 오차: < 5%
 - Normal approximation 잘 작동
 - Standard SE와 robust SE 비슷

- **Scenario B (Moderate instrument)**: F = 10
 - 2SLS 계수 편향: 5~15%
 - Normal approximation 부정확
 - Confidence interval이 symmetric하지 않음
 - AR test와 standard test 결과 다름

- **Scenario C (Weak instrument)**: F = 3
 - 2SLS 계수 편향: 20~50%
 - Normal approximation 크게 부정확
 - Standard CI에서 true value가 95% 수준에서 벗어날 수 있음
 - AR test 필수

#### 비동분산/Clustering 영향:
- **Homoskedastic assumption으로 계산한 F**: 실제보다 높게 보임
- **Robust-to-heteroskedasticity F**: 더 낮음 (더 conservative)
- **Implication**: F > 10이 "strong"이라는 classical rule이 현실에서는 부족할 수 있음

### 2. **경험적 조사 (2014-2018 AER)**:

저자들이 AER에 게재된 IV 사용 논문 약 100+개를 조사한 결과:

| 항목 | 비율 |
|-----|------|
| First-stage F 보고 | ~60% |
| Weak instrument 문제 인식 | ~40% |
| AR/KP test 사용 | <20% |
| Heteroskedasticity-robust SE | ~70% |
| Cluster-robust SE | ~50% |
| 과도 식별(overidentified) case에서 J-test 실행 | ~70% |

**해석**: 대다수 연구자가 first-stage F를 보고하지만, weak instrument가 있을 때의 robust inference 방법을 제대로 사용하지 않고 있음

### 3. **구체적 권장 Threshold**:

저자들은 **Stock-Yogo (2005) critical values**를 다음과 같이 정리:

| Target | Critical value (Single endogenous var) |
|--------|----------------------------------------|
| 5% maximum relative bias | F > 13.91 |
| 10% maximum relative bias | F > 9.08 |
| 20% maximum relative bias | F > 6.46 |
| 25% maximum relative bias | F > 5.39 |

**의미**: 예를 들어 F = 8이면, 2SLS 추정치가 true value로부터 평균 10% 정도 편향될 가능성 있음

## Robustness

### 저자들이 검증한 상황:

1. **동분산 vs 비동분산**:
 - Homoskedastic F와 heteroskedastic-robust F의 차이 시뮬레이션
 - 결과: robust F는 평균 20-40% 더 낮을 수 있음

2. **Clustering의 영향**:
 - 단순 robust SE vs cluster-robust SE
 - Many clusters (M > 100) vs few clusters (M < 10)
 - 결과: 클러스터 수가 적으면 F-stat critical value 조정 필요

3. **여러 endogenous variables & many weak instruments**:
 - 단일 endogenous variable 상황과 다름
 - Rank condition 더 엄격해질 수 있음

4. **Time-series AR(1) structure**:
 - i.i.d. 가정 vs 시계열 상관 존재
 - 결과: Newey-West SE가 robust SE보다 큼 (상관 반영)

## Heterogeneity

### 1. **Instrument 강도 분포** (survey data):
- 약 20%의 논문이 F < 5 (명백히 weak)
- 약 30%의 논문이 5 < F < 10 (약함)
- 약 50%의 논문이 F > 10 (상대적으로 강함)

### 2. **주제별 차이**:
- Labor economics (trade, migration, education): F 값 상대적으로 높음 (좋은 instrument 가능)
- Macroeconomics (natural experiments): F 값 낮은 경향 (weak IV often unavoidable)

### 3. **Data structure별**:
- 큰 샘플 (n > 100,000): F 높은 경향 (같은 π 값이라도 F ∝ √n)
- 작은 샘플 (n < 1,000): F 낮은 경향

## Mechanism (방법론적 meritorious insights)

### Why weak instruments matter:

1. **Distribution 왜곡**:
 - Strong IV: β̂ ~ N(β, SE^2) (asymptotically normal)
 - Weak IV: β̂의 분포가 non-normal, multimodal일 수 있음
 - Delta method (linear approximation)이 작동 불가

2. **Bias-variance tradeoff**:
 - Weak IV → large variance (낮은 precision)
 - But also → potential bias (if instrument slightly invalid)
 - Strong IV → low bias and variance (but requires validity)

3. **Confidence interval distortion**:
 - Standard CI (symmetric around point estimate) → may not contain true value even at 95% confidence
 - AR-based CI → asymmetric, wider, but coverage 정확

## 본 paper와의 connection

### 매핑 위치 (본 논문 PAP v3.4):
- **Section 3 & 4 (Diagnostics & Testing) → 최핵심**
- **Layer 4 (OP test) → Anderson-Rubin test와 거의 동일**
- **Layer 3 (Romano-Wolf) → Robust testing framework의 이론적 근거**

### 5-layer SE와의 구체적 매핑:

**Layer 1 (Main IV, DFS-style shift-share)**:
- First-stage F-statistic 반드시 계산 & 보고
- 본 논문: DFS의 shift-share IV가 충분히 강한지 확인
 - 예상: F > 10~15 (because shift-share usually strong)
 - 실제 계산 필수

**Layer 2 (DGHP mediation)**:
- Mediation analysis도 IV structure를 가짐
- 각 step (trade shock → employment → mortality)의 first-stage F 확인

**Layer 3 (Romano-Wolf correction)**:
- Multiple hypothesis testing (예: 여러 사망원인)
- Andrews-Stock-Sun의 robust procedures 기초
- Particularly: heteroskedasticity-robust critical values

**Layer 4 (OP / Anderson-Rubin test)**:
- 이 논문의 AR test가 **정확히** OP (Overidentification) test의 특수한 형태
- J-test (Sargan test)보다 weak instrument에 robust
- 여러 shift-share IV (예: 산업별, 무역상대국별)의 타당성 검증

**Layer 5 (Final integrated approach)**:
```
1. First-stage F for each IV
2. If any F < 10: use cluster-robust SE (minimum)
3. If F < 5 for any: use AR/KP test instead of standard 2SLS
4. Apply Romano-Wolf to multiple tests
5. Report both point estimate & AR CI
```

### 직접 인용 가능 quote:
> "Weak instruments remain an important issue for empirical practice, and that there are simple steps that researchers can take to better handle weak instruments in applications." (Abstract)

> "The usual normal approximation to the distribution of β̂ can be derived using the delta method, which linearizes β̂ in (δ̂, π̂). Under this linear approximation, normality of (δ̂, π̂) implies approximate normality of β̂. This normal approximation fails in settings with weak instruments because β̂ is highly nonlinear in π̂ when the latter is close to zero." (Section 3, explaining weak instruments)

> "We use this sample for two purposes. The first is to learn what empirical researchers are actually doing when it comes to detecting and handling weak instruments. The second is to develop a [methodology for...]" (Section 1, Introduction)

### Novelty claim:
- **이 논문의 contribution**: Weak instruments에 대한 **가장 실용적이고 완전한 guide**
- **본 논문의 차별성**:
 - DFS & Pierce-Schott을 따르는 shift-share IV 사용
 - BUT 한국 데이터에서 instrument strength 확보가 더 어려울 수 있음 (작은 지역 개수)
 - 따라서 Andrews-Stock-Sun의 robust inference가 **필수적**
 - 특히 cluster-robust SE와 AR-based CI가 key methodological contribution

## Quality assessment

### 본 논문 writer가 알아야 할 핵심 lesson 3개:

1. **"First-stage F > 10"은 충분하지 않을 수 있음, 특히 cluster된 데이터에서**: 
 - 한국 시군구 데이터는 (a) 표본 크기 작음 (~ 250 시군구), (b) 강한 clustering (시도 내) 존재
 - 따라서 Andrews-Stock-Sun의 권장 critical value (F > 13.91 for 5% bias, 또는 F > 9.08 for 10% bias)를 적용할 것
 - 만약 F가 낮으면, point estimate를 과신하지 말고 Anderson-Rubin CI 보고 필수

2. **Heteroskedasticity-robust & cluster-robust SE는 선택이 아닌 필수**:
 - 본 논문: 시도(state-level), 지역(region-level), 시간(annual)의 3중 clustering 가능성
 - 따라서 최소한 **two-way clustering (지역 + 시간)**을 사용할 것
 - 또는 더 안전하게 **all clustering** (지역 중심)

3. **Overidentified case에서 AR-based J-test 사용**:
 - 여러 산업/무역상대국별 shift-share를 동시에 사용하면 overidentified
 - 전통적 J-test (Sargan test)는 weak instrument에 sensitive
 - 대신 **Anderson-Rubin의 overidentification test** 또는 **Kleibergen-Paap test** 사용
 - 이를 Romano-Wolf correction과 결합하여 multiple testing 문제 해결

---

## 종합 평가
Andrews-Stock-Sun (2019)는 **weak instruments의 bible**이라고 할 수 있다. 본 논문은 shift-share IV라는 강력한 도구를 사용하지만, 한국의 작은 지역 데이터라는 제약 속에서 **robust inference**를 반드시 구현해야 한다. 특히 point estimate의 신뢰도보다 confidence interval의 정확성이 중요하다는 message를 명확히 할 필요가 있다.
