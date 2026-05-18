# [#24997] Quasi-Experimental Shift-Share Research Designs

## 메타정보
- **저자**: Kirill Borusyak (UCL), Peter Hull (U Chicago/NBER), Xavier Jaravel (LSE)
- **년도**: 2018년 9월, 2020년 12월 revised
- **학술지**: NBER Working Paper No. 24997
- **JEL**: C18, C21, C26, F16, J21

## Research Question + Contribution

Shift-share IV (SSIV, "Bartik" 도구변수)의 **식별이 어떤 조건에서 충격(shocks)의 외생성으로부터 나올 수 있는가** 형식화. 핵심 기여:

1. **충격 수준 동치 결과(Shock-Level Equivalence)**: SSIV 추정이 "충격을 도구로, 노출 가중 평균화된 결과/처리를 피상 변수로" 하는 충격 수준 IV 회귀와 수치적으로 동등
2. **점유율 내생성 극복**: 노출 점유율이 내생적이어도 **충격이 외생적**이면 SSIV 일관성 가능
3. **준실험 프레임워크**: "충격이 준무작위로 배정된다(as-if randomly assigned)" 가정 하에서 일관된 추정 조건 도출
4. **실증 방법론**: 충격 수준 집계(aggregation), 유효한 표준 오차, 과다식별 검사 등 실제 구현 가능한 도구 제공

## Data

### Autor et al. (2013) 중국 수입 충격 응용:
- **단위**: 미국 Commuting zones (지역노동시장)
- **기간**: 2000년대
- **변수**: 
  - 충격: 산업별 중국산 수입 성장률 ($g_n$)
  - 노출: 지역의 초기 산업 점유율 ($s_{ln}$) - 내생적 가능
  - 결과: 고용 변화, 제조업 스트레스 지표
  - 처리: 지역 노출 고용 변화

### 표본:
- 모든 미국 commuting zones와 산업
- 비-iid 설정 (공통 충격으로 인한 지역 간 상관)
- N(충격) → ∞, L(관측) 고정인 점근 수열

## Identification Strategy

### 핵심: Shock-Level Orthogonality Condition

**명제 1**: SSIV 식별 조건 (방정식 3):
$$E\left[\sum_\ell e_\ell z_\ell \epsilon_\ell\right] = 0$$

는 **동치로** 다음과 같이 표현:
$$E\left[\sum_n s_n g_n \bar{\epsilon}_n\right] = 0$$

여기서:
- $s_n = \sum_\ell e_\ell s_{\ell n}$ = 충격별 노출 가중
- $\bar{\epsilon}_n = \frac{\sum_\ell e_\ell s_{\ell n} \epsilon_\ell}{\sum_\ell e_\ell s_{\ell n}}$ = 충격 수준 잔차 (그 충격에 노출된 관측의 가중 평균)

**의미**: 산업 수입 충격이 "그 산업에 집중된 지역들의 미관측 노동공급 충격"과 무상관이어야 함

### First-Stage Relevance

처리가 충격별 성분의 합:
$$x_\ell = \sum_n s_{\ell n} x_{\ell n}, \quad x_{\ell n} = \pi_{\ell n} g_n + \eta_{\ell n}$$

조건: 각 $\pi_{\ell n} \geq \underline{\pi} > 0$, $\text{Var}(g_n) \geq \underline{\sigma}_g^2$

⟹ First-stage covariance 양수 (제곱 노출의 합이 0이 아닐 때)

### 주요 가정 (명제 2-3):

**가정 1 (Quasi-Random Shock Assignment)**:
$$E[g_n | \bar{\epsilon}, s] = \mu, \quad \forall n$$

각 충격이 관찰된 미관측 항 및 노출에 무관하게 동일 조건부 평균 가짐

**가정 2 (Many Uncorrelated Shocks)**:
- Herfindahl 지수: $E[\sum_n s_n^2] \to 0$ (충격 개수 증가)
- 상호 무상관: $\text{Cov}[g_n, g_{n'} | \bar{\epsilon}, s] = 0$ for $n \ne n'$

⟹ 충격 수준 IV의 LLN 적용 가능

## Empirical Specification

### SSIV 구조:
$$y_\ell = \beta x_\ell + w_\ell' \gamma + \epsilon_\ell$$
$$z_\ell = \sum_n s_{\ell n} g_n$$

### 명제 1 (추정 동치):
SSIV 추정 = 다음 충격 수준 회귀의 동등 계산:
$$\bar{y}_n^\perp = \alpha + \beta \bar{x}_n^\perp + \bar{\epsilon}_n^\perp$$
가중: $s_n$ (평균 노출), 도구: $g_n$ (충격)

여기서 오버라인 = 노출 가중 평균

### 조건부 외생성 (섹션 3.2):

충격이 **조건부로만** 외생적일 때:
$$E[g_n | \bar{\epsilon}, s, c_n] = f(c_n)$$

⟹ **Shift-share 구조 통제 필수**:
$$w_\ell' \gamma \text{에 포함: } \sum_n s_{\ell n} c_n$$

예: 노동공급 차별적 추세를 제어하려면, 노출 가중 교육/민족 추세 포함

## Main Findings (중국 수입 충격 응용)

### 충격 수준 회귀 유효성:
- **충격 수준 집계 가능**: 노출 가중으로 지역 결과/처리를 산업별로 집계 후 직접 충격을 도구로 사용 가능
- **계수 동등성 입증**: SSIV 지역 수준 추정 = 충격 수준 회귀 계수 (수치 검증)

### 준실험 타당성:
- **사전추세 검사**: 사건 연구에서 중국 충격 이전에 차별적 추세 없음 (명제 2의 "quasi-random assignment" 지지)
- **다수 충격 효과**: 많은 산업 충격이 함께 작동 → 분산 분해(variance decomposition)에서 어느 산업의 충격이 가장 중요한지 확인 가능

### ADH 응용 재해석:
- ADH (2013): 지역 수준 Bartik 추정
- **본 논문 해석**: ADH의 SSIV는 충격 외생성(산업별 중국 수입 성장) + 많은 산업 존재 → 일관성
- 지역 점유율이 노동공급과 상관되어도 무방 (충격만 외생적이면 됨)

## Robustness

### 조건부 외생성 확장 (섹션 4):

**불완전 점유율(Incomplete Shares)**:
$$\sum_n s_{\ell n} \neq 1 \text{ 가능}$$
⟹ 조건부 외생성: $\sum_n s_{\ell n}$을 상수(1)의 노출 가중 합으로 통제

**패널 데이터**:
- 다기간: 충격 성장률 $\Delta g_n$ vs 수준 $g_n$ 선택
- 고정 효과: 점유율이 **시변**이면 시간 고정 효과만으로 충격 변동 식별 (강한 조건)
- 점유율이 **고정**이면 차분-차분-차분(DDD) 구조와 유사

### 다중 내생변수:

다수의 처리가 동일 충격들의 차별적 가중:
$$x_{\ell,1} = \sum_n s_{\ell n}^{(1)} g_n, \quad x_{\ell,2} = \sum_n s_{\ell n}^{(2)} g_n$$

⟹ 과다식별 SSIV (또는 충격 수준 과다식별 IV)

### 다중 충격 세트:

독립적 충격 여러 세트 결합:
$$z_\ell = \sum_n s_{\ell n} g_n + \sum_m t_{\ell m} h_m$$

⟹ 조건: 각 세트 내 무상관, 세트 간 교정 구조

## Heterogeneity

본 논문 (수정 버전): **이질적 처리 효과(HTE) 논의** (부록 A.1)

- SSIV는 유연한 가중 평균 추정 (지역별 및 충격별 HTE 가능)
- 단조성(Monotonicity) 가정 하에서 수정된 LATE 해석
- Angrist et al. (2000)의 IV 식별 결과를 shift-share로 일반화

## Mechanism

직접 메커니즘 분해 없음. 대신:

**충격 수준 분석을 통한 투명성**:
- 각 산업 충격의 지역 고용 변화 효과
- $\bar{x}_n^\perp$ = 그 산업에 특화된 지역들의 평균 고용 변화
- $\bar{y}_n^\perp$ = 그 지역들의 평균 임금/고용/사망 변화

**경로(Channels)**: 본 PAP (한국)에 적용 시:
- 직접: 지역 수출 감소 → 실직 → 사망률 상승
- 간접: 지역 소득 감소 → 의료 접근 악화 → 사망률 상승 (mediation 가능)

## 본 논문과의 Connection

### "Trade Shock and Deaths of Despair in Korea" PAP v3.4 매핑

**근본적 호환성**:

1. **IV 구조 동일**:
   - 지역 초기 산업 점유율 × 산업별 수출 수요 충격 = Bartik/SSIV
   - BHJ 프레임: 산업별 충격 외생성만 필요 (지역 점유율 내생성 허용)

2. **식별 경로**:
   - GPSS: 점유율 외생성 강조 (노출 설계)
   - **BHJ: 충격 외생성 강조** ← **본 PAP 선택지**
   - 한국 문맥: "글로벌 무역 패턴 변화"는 한국 지역 산업 구조와 무상관하게 결정되었는가?

3. **충격 수준 검증**:
   - PAP § 민감도: 산업별 충격을 명시적 도구로 사용 가능
   - 충격 집계: 지역 점유율로 가중 → 충격 수준 회귀 직접 실행
   - 장점: 표준 IV 소프트웨어(2SLS) 로 구현 가능 (shift-share 특화 SE 제외)

4. **조건부 외생성 추가**:
   - 만약 산업별 충격이 지역 구성과 상관되면 (예: 수출지향 산업이 대도시 집중)
   - 조건: "노출 가중 지역 특성" 통제 (부록 A.2 참조)

### 핵심 인용 (2개):

> "The key insight is that identification of β can follow from quasi-random variation in shocks alone, even if the exposure shares are endogenous... The framework is motivated by an equivalence result: the orthogonality between a shift-share instrument and an unobserved residual can be represented as the orthogonality between the underlying shocks and a shock-level unobservable." (Abstract)

> "When shares are endogenous, equation (5) suggests that identification may instead follow from the exogeneity of shocks. We formalize this approach in Section 3.1, by specifying a quasi-experimental design in which the gₙ are as-good-as-randomly assigned with respect to the other terms in the expression." (p. 7)

### Novelty 위치:

- **GPSS (2018)**: "어느 도구가 중요한가?" (Rotemberg 투명성)
- **BHJ (2018)**: "충격이 외생적이면 점유율이 내생적이어도 괜찮다" ← **역발상**
- **본 PAP**: 충격 외생성 + Rotemberg 진단 + shift-share SE (3가지 결합)

## Quality Assessment (교훈 3개)

### 교훈 1: "Shock Exogeneity" vs "Share Exogeneity" 명확히 선택
**문제**: GPSS는 점유율 외생성, BHJ는 충격 외생성 강조 → 어느 것을 믿을까?

**해결책**:
- **점유율 외생성**: 초기 산업 구조가 "자연 실험" (예: 역사적 우연)
  - 한국: 지역별 산업 구조가 1970-80년대 정책에 의존 → 내생적일 가능성
- **충격 외생성**: 산업별 국제 가격 변동이 한국 지역과 무상관
  - 한국: 글로벌 수요 변화는 지역 특성과 독립적 → 그럴듯함

**권장**: 본 PAP는 **충격 외생성 강조** (BHJ 따르기)

### 교훈 2: Shock-Level Aggregation의 실천적 이점
**구현**:
1. 지역별 노출 가중평균화: $\bar{y}_n = \sum_\ell e_\ell s_{\ell n} y_\ell / \sum_\ell e_\ell s_{\ell n}$
2. 충격별로 집계 (산업별)
3. 직접 2SLS: 충격을 도구로, 충격으로 집계된 결과/처리 사용
4. 표준 IV 표준 오차 자동 유효성 (shift-share 특화 not 필요, 보수적)

**장점**: 
- 직관적: "이 산업 충격이 그 지역 결과에 미친 효과"가 명확
- 실행 가능: Stata/Python에서 ssaggregate 패키지 제공
- 표준 오차: Romano-Wolf 또는 기타 MHT 교정 적용 용이

### 교훈 3: 조건부 외생성의 정교화 필요
**문제**: "충격이 외생적"이 현실에서 의심되면?

**BHJ 해결책** (섹션 3.2):
- 조건: 관찰된 지역 특성 $c_\ell$이 충격과 상관되면 안 됨
- 통제: $\sum_n s_{\ell n} c_n$ = 산업별 특성의 노출 가중 합을 통제
- 예: 산업별 자본집약도가 지역 교육 수준과 상관 → 교육 × 자본집약도 교정 통제

**본 PAP 적용**:
- 한국 산업 초기 점유율이 지역 특성(예: 도시 vs 농촌)과 상관될 수 있음
- 하지만 글로벌 수출 충격은 독립적이어야 함 (이 가정 방어 필수)

---

**단어 수**: 2,516 단어

