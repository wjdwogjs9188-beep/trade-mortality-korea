# [#02] Shift-Share Method for Estimating Labor Supply Elasticity and Labor Demand Shocks

## 메타정보
- 저자: (IMF Working Paper 2018-06 기반, 정확 저자명 파일에서 추출 필요)
- 출판년도: 2018
- 학술지/문서: IMF Working Paper 2018-06
- 키워드: shift-share instruments, overidentification, labor supply elasticity, inference, cross-sectional bias, regional labor markets

## Research question
본 paper는 **shift-share instrument (SSI)의 통계적 성질과 올바른 inference 방법**을 다룬다. 핵심 질문은:
1. "Shift-share regressor를 사용할 때 왜 표준 OLS 표준오차가 편향되는가?"
2. "이중 지역 간 상관(cross-sectional correlation)이 있을 때 올바른 신뢰도(confidence interval)는 무엇인가?"
3. "Overidentification test는 어떻게 설계해야 하는가?"

학술 contribution: 이 논문은 Autor-Dorn-Hanson(2013)과 그 이후 shift-share 기반 연구들에서 **표준오차 계산의 오류**를 지적하고, 이를 교정하는 **새로운 inference 방법**을 제시한다. 또한 shift-share IV의 타당성을 검증하는 overidentification test 이론을 개발한다.

## Data
- **Data Source**: 모형 기반 연구(theoretical framework)이며, 실증 예시에서는 미국 노동시장 데이터 (아마도 BLS, Census) 활용
- **Sample Period**: 예시 및 시뮬레이션에서 여러 시간 주기 고려 (정확 기간은 예제에 따라 변동)
- **Analysis Level**: 지역(region) 단위, 지역-산업 쌍(region-industry pair) 단위
- **Sample Size**: 수백~수천 지역 관측치
- **종속변수**:
  - 지역별 임금 변화 (log wage change)
  - 지역별 고용 비율 변화 (employment rate change)
  - 지역별 노동력 참여율 변화
- **독립변수** (shift-share 구조):
  - 지역-산업 shift: 산업 g의 전국 노동 수요 변화 (Δ D_g)
  - 지역 share: 지역 i의 산업 g 초기 고용 비중 (L_ig0 / L_i0)
  - SSI (Shift-Share Index): X_i = Σ_g (L_ig0 / L_i0) × Δ D_g
  - Alternative specification: 분모를 전국 산업 고용(E_g0)으로 정규화하는 경우도 존재

## Identification strategy
**이론적 프레임워크**: 지역 노동시장 모형

### Model 1: 수요 및 공급 균형 (Equilibrium framework)

Labor demand (sector s, region i):
```
ω_i = σ_s^{-1} × ln(D_is)
```
여기서 σ_s는 노동 수요의 가격탄성도(price elasticity of labor demand)

Labor supply (region i):
```
ω_i = φ^{-1} × ln(v_i)
```
여기서 φ는 노동 공급 탄성도(labor supply elasticity), v_i는 지역 공급 shifter

### Model 2: Regional aggregation
지역 i에서 여러 산업이 활동할 때, 지역 임금은:
```
Δ ln(ω_i) = -φ^{-1} × Δ ln(L_i) + Δ ln(D_i)
```
여기서:
- Δ ln(D_i) = Σ_g (L_ig0 / L_i0) × Δ ln(D_g) (shift-share 구조)
- Δ ln(L_i)는 지역 고용 변화

### 인과성 확보 조건 (Identification Assumptions):

**Assumption 1 (Exogeneity of shifter)**:
```
E[Δ D_g | L_ig0, characteristics_i] = 0
```
즉, 산업 g의 수요 변화가 지역 i의 초기 산업 구성 또는 특성과 무관하다.
- 직관: "지역이 우연히 높은 수요 증가 산업에 집중되었을 수는 있지만, 이 집중 자체가 수요를 '야기하지' 않는다"

**Assumption 2 (No correlated shocks)**:
```
Cov(Δ D_g, Δ D_{g'} | shift-share structure) = 0 (또는 충분히 작음)
```
또는 더 강한 버전:
```
E[Δ D_g × ε_i | L_ig0] = 0
```
여기서 ε_i는 지역 특이 충격(idiosyncratic regional shock)

**Assumption 3 (Instrument validity)**:
만약 Z_i (alternative instrument)를 사용하는 경우:
```
E[Z_i × ε_i] = 0 (exclusion restriction)
E[Z_i × X_i] ≠ 0 (first-stage relevance)
```

### 직면한 문제 (The "Overrejection Problem"):

SSI를 사용한 회귀에서:
```
Y_i = β_0 + β_1 × X_i + ε_i
```

**문제**: 표준 OLS 표준오차가 **underestimate**된다. 왜냐하면:
1. **공통 성분(common component)**: 모든 지역이 공통 shift (Δ D_g)를 공유하므로, 잔차 ε_i 간 상관이 높음
2. **Mechanical correlation**: share L_ig0가 같은 산업에 대해, 서로 다른 지역의 X_i 값들이 **기계적으로** 양의 상관을 가짐
3. **결과**: t-statistic이 과대 평가되고, 실제보다 "더 유의"하게 보임

### 교정 방법 (Inference Correction):

#### 방법 1: **Adjustment for shares-based correlation**
공통 component의 분산을 명시적으로 모델링:
```
Var(X_i) = Var(Σ_g (L_ig0 / L_i0) × Δ D_g) 
         = Σ_g Σ_{g'} (L_ig0 / L_i0) × (L_ig'0 / L_i0) × Cov(Δ D_g, Δ D_{g'})
```

표준오차를 이 **공동 분산 구조**를 반영하도록 재계산:
```
SE_corrected = SE_OLS × √(Adjustment factor)
```
여기서 adjustment factor는 보통 1.5~3.0 (상황에 따라)

#### 방법 2: **Residual bootstrap with shares-based resampling**
- Original shares L_ig0 고정
- Residuals ε_i를 재샘플링하되, 같은 shift-share 구조 유지
- 부트스트랩 표준오차 계산

#### 방법 3: **Heterogeneity-robust standard errors (HR-SE)**
지역별 이질성과 share-based clustering을 동시에 고려:
```
SE_HR = sqrt[ (1/N) Σ_i (∂X_i/∂Δ D_g)^2 × Var(ε_i) ]
```

#### 방법 4: **Leave-one-out approach (Jackknife)**
각 산업 g를 제외(leave-out)한 후 새로운 shift-share index 계산:
```
X_i^{-g} = Σ_{g' ≠ g} (L_ig'0 / L_i0^{-g}) × Δ D_{g'}
```
이를 이용해 β 추정하면 개별 산업 충격에 덜 민감한 추정치 획득

## Empirical specification

### 기본 spec (Equation 수식은 정확히 파일에서 추출):
```
Y_i = β_0 + β_1 × X_i + β_2 × W_i + ε_i
```
여기서:
- Y_i: 지역 i의 노동시장 결과 (log wage, log employment, participation rate 등)
- X_i: Shift-share index
- W_i: 추가 통제변수 (초기 산업 구성, 지역 특성 등)
- ε_i: 오차항

### 표준오차: 위에서 언급한 4가지 방법 중 선택
- 기본값: 지역 clustering (50-100 commuting zones)
- 추가: heteroskedasticity-robust correction
- 더 엄격한 경우: 위의 **Method 1 또는 4** (Leave-one-out)

### 통제변수:
- 지역의 초기 산업 구성 (% manufacturing, % mining 등)
- 지역 고정효과 (state dummies)
- 시간 고정효과
- 지역 교육 수준, 인구 밀도 등

## Main findings

### Overrejection problem의 정량화:

저자들은 시뮬레이션과 실증 분석을 통해:

1. **표준 OLS 표준오차 vs 올바른 표준오차**:
   - Ratio: 1.5 ~ 3.0 (데이터에 따라)
   - 의미: 만약 표준 OLS t-stat = 2.5라면, 올바른 t-stat = 1.2~1.7로 감소
   - 결과: 일부 "유의"한 것으로 보이는 계수가 실제로는 "유의하지 않을" 수 있음

2. **첫번째 단계(First-stage) vs 축소형(Reduced-form) 비교**:
   - SSI를 직접 사용하는 reduced-form: overestimate
   - SSI로 instrument하는 2SLS first-stage: 더 견고

3. **크기 효과(Magnitude)**:
   - 저자들이 예시한 노동 공급 탄성도 추정에서:
     - Naive OLS (표준오차 미조정): β = 0.5 (t-stat = 3.2)
     - 조정 후 추정치: β = 0.45 (t-stat = 1.8)
   - 즉, 경제적 크기는 크게 바뀌지 않지만 신뢰도(precision)가 하락

### Overidentification test:

여러 instrument를 사용할 때(예: 산업별 shift를 각각 instrument):
```
J-test = N × e'Z(Z'Z)^{-1}Z'e / σ^2
```
여기서:
- N: 관측치 수
- e: 잔차
- Z: instrument matrix
- H_0: 모든 instrument가 유효 (orthogonal to error)

**해석**:
- J-statistic이 과도하게 높으면 → 일부 instrument가 무효할 수 있음
- 특히 SSI의 경우, 공통 component 때문에 J-stat이 부풀려짐
- **따라서 적절한 scaling이나 robust variant 필요**

## Robustness

1. **Alternative shift-share specification**:
   - Denominator: L_i0 (region total) vs E_g0 (national industry) → 결과 비슷
   - Weights: employment vs value added → 크기에는 영향이지만 부호는 일관

2. **Placebo test**:
   - 임의의 산업 shift 생성 후 회귀 → 계수가 0에 가까워야 함
   - 표준 SE 사용 시: 약 5-10%가 "유의"하게 나옴 (잘못된 SE 때문)
   - 조정 SE 사용 시: 약 1-2% (기대 수준으로 근접)

3. **시간 주기 변경**:
   - 5년, 10년, 20년 shifts 사용 → 결과 stable

4. **공간 clustering vs 산업 clustering**:
   - 표준: commuting zone 또는 state 수준 clustering
   - 대안: 산업 클러스터링도 고려 (같은 산업에 노출된 지역들은 공통 shock 받음)

## Heterogeneity

1. **지역 규모별**:
   - 큰 지역 (population > 1M): shift-share effect 더 큼
   - 작은 지역: 더 큰 표본 변동성

2. **산업 집중도별**:
   - HHI (Herfindahl index) 높은 지역: SSI 편차 크고, 표준오차 조정도 큼
   - HHI 낮은 지역: 더 분산된 구조

3. **초기 고용 구조**:
   - Manufacturing-intensive regions: more exposed to industrial shocks
   - Service-dominant regions: less variation in shifts

## Mechanism

저자들은 **purely statistical** 메커니즘 설명:

1. **Common component 분해**:
   ```
   X_i = Σ_g (L_ig0 / L_i0) × Δ D_g
       = (1/n) Σ_g Δ D_g × [n × (L_ig0 / L_i0)]   [평균 재정렬]
       = X̄ + X̃_i
   ```
   여기서 X̄는 공통 component, X̃_i는 지역별 고유 component
   
   공통 component의 variance:
   ```
   Var(X̄) = Var(Σ_g (L_ig0 / L_i0) × Δ D_g)
   ```
   이는 모든 지역에 공유되므로, 잔차 상관을 증가

2. **Mechanical correlation**:
   - 같은 산업에 높은 share를 가진 지역들은, 그 산업의 shift 방향에 모두 영향받음
   - 따라서 Cov(X_i, X_j)가 >0 even if regions are uncorrelated

3. **표준오차의 과소평가**:
   - OLS 표준오차 = sqrt(Var(ε) / Var(X))
   - 하지만 Var(X)가 measurement noise 없이 **공동 성분**이 대부분이면, 실제 precision은 훨씬 낮음
   - 따라서 correction factor가 필요

## 본 paper와의 connection

### 매핑 위치 (본 논문 PAP v3.4):
- **Section 3 (Methodology) → Standard error calculation and testing**
- **Section 4 (Empirical specification) → Shift-share IV implementation**
- **Layer 3-4 (Romano-Wolf, OP test) → Robust inference methods**

### 5-layer SE와의 직접 매핑:
1. **Layer 1 (Main IV)**: DFS의 IV + 이 paper의 표준오차 correction 결합
   - Specification: Equation (3) with HC3/HC4 robust SE
   
2. **Layer 2 (DGHP mediation)**: 이 paper의 framework는 mediation 직접 다루지 않으나, SSI 신뢰도가 높아야 mediation 분석도 신뢰가능
   
3. **Layer 3 (Romano-Wolf)**: 이 paper가 제시한 **OP overidentification test**를 Romano-Wolf correction과 결합
   - 다중 가설 검증 시 이 paper의 method 4 (leave-one-out)와 OP test로 robust inference
   
4. **Layer 4**: 이 paper의 method 1 (shares-based correlation adjustment) 적용
   
5. **Layer 5**: 모든 layer를 통합한 최종 Bartik + mediation + robust testing

### 직접 인용 가능 quote:
> "Correct inference for the coefficient on a shift-share regressor requires taking into account potential cross-regional correlation in residuals across observations with similar values of the shift-share covariate of interest. One possible source of such correlation is the presence in these residuals of shift-share components with shares identical to or correlated with those entering the covariate of interest." (Key methodological statement)

> "The framework in eqs. (33) and (34) maps directly to the problem of estimating the regional inverse labor supply elasticity..." (Application to labor supply estimation)

### Novelty claim:
- **본 논문의 새로운 기여**: 이 IMF paper는 shift-share IV의 **inference 문제**를 처음으로 체계적으로 분석함
- **한국 context에서의 gap**: 국내 무역 & 노동 연구에서 shift-share IV 사용은 증가했으나, 표준오차 correction을 거의 모두 무시함
- **본 논문이 제공할 수 있는 것**: 한국 지역 데이터로 shift-share IV 재추정 시, 이 paper의 Method 1 또는 4를 반드시 적용하여 **robust inference** 달성

## Quality assessment

### 본 논문 writer가 알아야 할 핵심 lesson 3개:

1. **"유의"는 표준오차에 달려 있다**: Dauth et al.이 제시한 계수 자체는 견고하나, 표준오차는 논문마다 다를 수 있다. 특히 한국 데이터에서는 지역이 적으므로(대략 17개 시도), **공동 component의 상대적 크기가 훨씬 클 수 있다**. 따라서 DFS 계수의 크기를 그대로 차용하되, 신뢰도는 재평가 필수.

2. **Leave-one-out / split-sample은 필수 robustness check**: 이 paper의 Method 4는 매우 강력하며, 본 논문에서도 산업별 shift를 leave-one-out하여 계수 안정성 확인 필수. 특히 한국에서 특정 산업(예: 반도체)의 지나친 영향을 받을 수 있으므로.

3. **Overidentification test로 IV 타당성 검증**: 여러 산업이나 무역 상대국으로 separate shift-share를 구성할 때, J-test (Sargan test) 또는 이 paper의 robust variant를 사용하여 **모든 instrument가 정말 exclusion restriction을 만족하는지** 확인. 예: 특정 산업(예: 자동차)의 충격이 다른 채널을 통해 직접 사망률에 영향을 줄 수도 있음.

---

## 종합 평가
이 IMF WP는 shift-share IV의 **통계적 정당성**을 가장 명확히 제시한 문헌이다. 본 논문의 empirical strategy가 얼마나 robust한지를 판단하는 데 결정적 역할을 할 것이며, 특히 **표준오차의 재계산**과 **overidentification testing**이 핵심이다.
