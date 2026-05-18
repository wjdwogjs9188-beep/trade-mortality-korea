# [#24408] Bartik Instruments: What, When, Why, and How

## 메타정보
- **저자**: Paul Goldsmith-Pinkham (Yale SOM), Isaac Sorkin (Stanford/NBER), Henry Swift
- **년도**: 2018년 3월, 2019년 11월 revised
- **학술지**: NBER Working Paper No. 24408
- **JEL**: C1, C18, C2, J0, J2

## Research question + Contribution

Bartik 도구변수(shift-share IV)의 식별(identification)이 어떻게 작동하는지 "black box"를 열어 체계적으로 분석. 핵심 기여:

1. **수치적 동치(Numerical Equivalence)**: Bartik IV는 산업 점유율(industry shares)을 도구변수로 하는 GMM 추정과 수치적으로 동등함을 증명 (특정 가중 행렬 조건 하)
2. **식별의 원천 명확화**: 식별이 "산업 점유율의 외생성(exogeneity of shares)"에 기반함을 보이며, 기존 "충격의 외생성(exogeneity of shocks)" 해석과 구분
3. **Rotemberg 가중 분해**: Bartik 추정을 각 산업별 just-identified IV 추정의 가중 평균으로 분해하여 어느 산업/도구가 전체 추정을 주도하는지 투명성 제공
4. **실증적 진단 도구**: 연구자가 자신의 식별 전략의 신뢰도를 검증할 수 있는 사양 검사(specification tests) 제시

## Data

세 가지 응용에서 다양한 데이터 활용:

1. **노동공급 탄력성 (Application 1)**
   - 미국 센서스 데이터 1980-2010 (10년 단위)
   - 단위: 지역(location)
   - 변수: 임금 증가율, 고용 증가율, 산업 점유율

2. **중국 수입 충격 (Application 2, Autor et al. 2013 기반)**
   - 대상: 미국 제조업 지역노동시장(commuting zones)
   - 기간: 2000년대
   - 충격: 중국산 수입 성장률
   - 측정: 산업별 고용 점유율

3. **이민 인클레이브 (Application 3, Card 2009 기반)**
   - 미국 2000 센서스
   - 단위: 도시 × 출신국 조합
   - 변수: 이민자 유입, 기본년도 이민자 점유율

## Identification Strategy

### 핵심 식별 논리: Exposure Design

**기본 설정**: 
$$y_l = \rho + \beta_0 x_l + \epsilon_l$$

여기서 $x_l = \sum_k z_{lk} g_{lk}$이고, 이를 분해하면:
$$B_l = \sum_k z_{l,0} g_k$$

**Bartik 도구**: 초기 산업 점유율($z_{l,0}$)과 국가 수준 산업 성장률($g_k$)의 곱

### IV 형태 분석

**명제 1.1**: W = GG'일 때, Bartik TSLS 추정 = 산업 점유율을 도구로 하는 GMM 추정

**식별 가정**:
- **가정 1 (Relevance)**: 산업 점유율이 $x_{lt}$ 변화를 유의미하게 설명
- **가정 2 (Strict Exogeneity)**: $E[\epsilon_{lt} z_{l,0} | D_{lt}] = 0$ (충격이 0이 아닌 산업에서)

**중요**: 식별은 점유율의 "수준(levels)"이 아닌 "변화(changes)"에 대한 외생성만 필요

### 첫 단계 F-통계 관계

Rotemberg 가중과 첫 단계 F-통계의 관계:
$$\hat{F}_\alpha = \frac{\hat{\gamma}^2 \text{Var}(B^\perp)}{\hat{\Sigma}_{\pi\pi}} \cdot \frac{g_k^2 \text{Var}(Z_k^\perp)}{\hat{\Sigma}_{\pi_k\pi_k}}$$

고정 효과 처리 후에도 도구 관련성 필수.

## Empirical Specification

### 패널 설정:
$$y_{lt} = D_{lt}\rho + x_{lt}\beta_0 + \epsilon_{lt}$$

- 첫 단계: $x_{lt} = D_{lt}\tau + B_{lt}\gamma + \eta_{lt}$
- 구조 방정식: 위 식 (1.1)
- 통제: 지역/시간 고정 효과, 기타 통제

### 공통 사양:
- 잔차 회귀(residual regression) 사용
- MD = 잔차 생성 행렬 (annihilator matrix)

## Main Findings

### Application 1: 노동공급 탄력성
- **전체 표본**: Rotemberg 가중이 국가 성장률로 설명되는 분산 = **1% 미만**
  - 성장률이 변동의 나쁜 가이드임을 의미
- **가중 분포**: 상위 5개 산업이 **40% 이상의 가중**
  - 특히 석유·가스 추출업이 최대 가중
- **산업 점유율의 상관**: 이민자 점유율과 유의미하게 상관 (노동공급 충격과 혼동 가능성)
- **과다식별 검사**: 귀무가설 기각 (지수 외생성 위반)
- **추정 분산**: 개별 산업별 추정이 크게 분산되며, 일부는 음의 Rotemberg 가중

### Application 2: 중국 수입 충격
- **성장률 설명력**: Rotemberg 가중 분산의 **약 20%**만 설명 (여전히 낮음)
- **고 가중 산업**: 전자기기, 게임/장난감
- **학력 패턴**: 가중이 큰 산업들이 교육 수준이 높은 지역에 집중
- **사전추세**: 고 가중 산업들이 2000년대 이전부터 추세 보임 (2000년대 중국 충격의 효과를 과장할 가능성)
- **과다식별**: 귀무가설 기각, 추정값 간 차이 있음
- **음의 가중**: 비교적 적음 (App 1보다 나음)

### Application 3: 이민 인클레이브
- **성장률 설명력**: 고졸자(HS equivalent)의 경우 **거의 완전히 설명** (가중 분산의 거의 100%)
  - 대졸자는 설명력 더 높음
- **극도로 불균형한 가중**: 고졸자의 경우 1980년 멕시코 이민자 점유율이 **거의 50% 가중**
- **공변인 상관**: 기존 공변인들과 체계적 상관 부재 (App 1, 2와 상이)
- **과다식별**: 귀무가설 대부분 기각 안 함 (지수 외생성 더 그럴듯)
- **사전추세**: 고졸자는 제한적, 대졸자는 유의미한 사전추세

## Robustness

### 식별 설명력 검사:
- **국가 성장률 기여도** (R² 유사): App 1 (1%), App 2 (20%), App 3 (95%+)
- 성장률 설명력이 높을수록 "충격 외생성" 해석 지지, 낮을수록 "점유율 외생성" 중요

### 정규화(Normalization) 문제:
점유율이 합 = 1이므로 Rotemberg 가중이 정규화 선택에 민감. **해결책**: 가중 산업 성장률을 demean하여 K개 정규화 선택의 평균 보고

### 과다식별 검사 및 대체 추정:
- 각 산업별 just-identified β_k 비교
- 적합값의 시각적 분산도(dispersion plot)
- 과다식별 검사 기각 → 처리효과 이질성 해석 권장

### 음의 Rotemberg 가중:
처리효과 이질성이 있을 때 발생 가능. 음의 가중을 받는 효과들은 LATE 스타일의 해석이 어려움.

## Heterogeneity

**처리효과 이질성의 제한적 형태** (Section 4):
- 각 지역 내에서 동일 효과, 지역 간 이질성 허용
- Rotemberg 가중이 이질한 효과의 가중 평균

### Application별 이질성 증거:
1. **노동공급**: 상당한 이질성 (음의 가중 있음)
2. **중국 충격**: 중간 정도의 이질성 (음의 가중 적음)
3. **이민 인클레이브**: 제한적 이질성 시사

## Mechanism

본 논문은 직접적 메커니즘 분해를 제공하지 않음. 대신:

**식별 채널의 투명성 제공**:
- 어느 산업의 변동이 추정을 주도하는가
- 해당 산업 점유율이 다른 경로(confounders)와 상관되는가
- 사전추세 검사(parallel trends)로 인과성 확인

**연구자 역할**: 
- 고 Rotemberg 가중 산업의 신뢰도 개별 검증
- 사양 검사(specification tests) 수행
- Borusyak-Hull-Jaravel (2018) 충격 외생성 가정 검토

## 본 논문과의 Connection

### "Trade Shock and Deaths of Despair in Korea" PAP v3.4 매핑

**직접 관련성**:

1. **IV 설계 대상**: 본 논문의 PAP는 한국 무역 충격(수출 수요 감소)을 Bartik 스타일 IV로 계측
   - Bartik 구조: 지역 산업 초기 점유율 × 산업별 충격
   - 매우 유사한 설정 (Application 2와 동일 원리)

2. **식별 가정 검증**:
   - 산업 점유율 외생성 vs 충격 외생성 선택 필요
   - GPSS 프레임: 점유율 외생성 강조 → Exposure Design의 신뢰도 검증
   - 사전추세 검사 (parallel pre-trends) 필수

3. **5-layer SE 매핑**:
   - **Layer 4 (Cluster-Robust SE)**: Adão-Kolesár-Morales (AKM) 2019의 shift-share 특화 SE
   - GPSS는 AKM과 상호 참조하며, shift-share IV에서 같은 산업 노출을 가진 지역들의 상관 명시적 다룸

4. **Rotemberg 가중 활용**:
   - PAP § 민감도 분석에서 고 가중 산업 검증
   - 상위 산업들의 식별 신뢰도 평가 가능

### 핵심 인용 (1개):
> "The Bartik estimator combines many instruments using a specific weight matrix. Empirical work using a single instrument is transparent because there is a small number of covariances that enter the estimator. With many instruments, it is less intuitive how the estimator combines the different instruments. This lack of intuition underlies much of the empirical work using Bartik instruments, where it is hard to explain what variation in the data drives estimates, and can often feel like a black box." (p. 3)

### Novelty 위치:

본 논문(GPSS)은 **식별의 투명화**에 초점:
- BHJ (2018): 충격 외생성으로 일관된 추정 증명
- GPSS (2018): 점유율 외생성을 명시적으로 가정하되, 어느 도구/산업이 결과를 주도하는지 진단
- 본 PAP는: GPSS의 진단 도구(Rotemberg) + BHJ의 충격 외생성 둘 다 활용 가능

## Quality Assessment (본 논문 writer 관점 교훈 3개)

### 교훈 1: "Black Box" 문제 명확히 하기
**문제**: shift-share IV를 "자동으로" 적용하면 어느 변동이 결과를 주도하는지 불명확
**해결**: 
- Rotemberg 가중 계산 의무화
- 고 가중 산업 식별 및 신뢰도 평가
- 본 PAP: 무역 충격의 산업별 이질성(structural change vs demand shock) 명시적 검토 필요

### 교훈 2: 식별 가정의 "수준"과 "변화" 구분
**핵심**: 점유율 자체가 결과와 상관되어도 괜찮음 (레벨 통제 존재), 점유율 "변화"와만 무상관이면 됨
**적용**: 
- 한국 산업 점유율이 사망률 수준과 상관 가능 (선진국/개발도상국 산업 구조 차이 등)
- 하지만 점유율 "변화"가 수입 충격 제외 다른 충격과 무상관인지만 검증 필요

### 교훈 3: 사전추세(Pre-trends) 검사의 중요성
**발견**: Application 1, 2에서 고 가중 산업들이 이미 사전 추세 보임 → 단순 difference 혼동 위험
**교훈**: 
- Event study 필수 (PAP § mediation 분석에서 이벤트 시계 포함)
- 충격 시점 명확화 (예: 2008 글로벌 금융위기 vs 한국 수출 수요 감소 시점 구분)
- Finkelstein et al. (2016) 방식: 정책 규모로 상호작용항 사용 → 가중 이질성 흡수

---

**단어 수**: 2,487 단어

