# [#01] The Rise of the East and the Far East: German Labor Markets and Trade Integration

## 메타정보
- 저자: Dauth, W., Findeisen, S., Suedekum, J.
- 출판년도: 2014
- 학술지: Journals of Economic Literature (JEL Classification: F16, J31, R11)
- Working Paper: CESifo, December 2013
- 키워드: trade integration, China, Eastern Europe, labor market displacement, shift-share IV, manufacturing employment, regional economics

## Research question
본 연구는 **독일 지역 노동시장이 중국과 동유럽의 경제적 부상으로부터 받은 영향을 계량화**하는 것을 목표로 한다. 핵심 질문은 "무역 통합(trade integration)이 지역 고용, 임금, 그리고 구조적 조정(structural adjustment)에 미치는 인과적 영향은 무엇인가?"이다.

학술 contribution: 저자들은 Autor-Dorn-Hanson(2013, 이하 ADH)의 미국 중국 수입 충격 연구를 독일 사례로 확장하며, 특히 **미국과 반대되는 결과**를 발견한다—독일은 수출 기회 증가로부터 대규모 고용 순이득을 경험했다. 이는 산업별 노동력 특성, 기술 역량, 그리고 무역 파트너 구성의 차이를 강조한다.

## Data
- **Data Source**: 독일 연방 고용청(German Federal Employment Agency, IAB), 센서스 자료(Census data), 산업별 무역 통계(UNSD Comtrade)
- **Sample Period**: 1988-2008 (20년 패널, 10년 변화량 단위로 분석)
- **Analysis Level**: 독일 행정지역(German administrative regions) 단위. 논문은 약 **328개 지역(Arbeitsagenturbezirke)**을 사용하며, 노동시장 지역(labor market areas)과 광역 지역(greater labor market areas)으로도 분석
- **Sample Size**: 약 2,000~3,200 지역-시기 관측치 (지역 수 × 시간 주기)
- **종속변수**:
 - 주요: 제조업 고용 변화 (% of working-age population), 10년 단위 변화
 - 보조: 임금 변화, 비제조업 고용, 구조적 조정 지표
- **독립변수**:
 - Import exposure (Δ Import Exp): 지역 i의 제조업 수입 충격
 - Formula: Σ_j (E_ijt / E_jt) × ΔIm_jt
 - 분자: 산업 j의 독일 수입 증가량
 - 분모: 지역의 산업별 초기 고용 구성(lagged sectoral employment shares)
 - Export exposure (Δ Export Exp): 지역 i의 수출 기회 증가
 - 유사 구조, 단 기타국가의 동유럽/중국 수출 기회 측정
 - Covariates: 산업별 초기 고용 구성, 지역 고정효과, 시간 고정효과, 광역 지역 더미

## Identification strategy
**Shift-share IV (Instrumental Variable)** 전략 사용:

- **IV #1 (Import exposure)**: 다른 선진국(미국, 일본, 캐나다, 오스트리아)의 동유럽/중국 수입 증가를 독일의 산업 구성에 적용
 - Logic: 다른 나라의 수입 증가는 동유럽의 부상이 **글로벌 충격**임을 나타내며, 독일 특수 충격과 독립적
 - 이를 통해 측정 오류와 역인과성(reverse causality) 제거

- **IV #2 (Export exposure)**: 동유럽/중국이 기타 국가로부터 수입하는 증가량을 독일의 산업 구성에 적용
 - Logic: 동유럽의 수입 수요 증가는 독일의 특수한 경제 충격과 무관하게 **글로벌 수요 충격**을 반영
 - 역인과성 완전히 배제: 독일의 실제 수출이 아닌 "potential" 수출 기회만 측정

- **First-stage**: OLS로 실제 독일 노출(LHS)을 IV(RHS)에 회귀하면 강한 상관관계 확인 (F-statistic 제시되지는 않으나 본문에서 "strong correlation" 언급)

- **Exclusion restriction**: 다른 나라 수입/수출의 변화가 독일 노동시장 결과에 직접 영향을 미치지 않는다고 가정. 이는 독일이 작은 개방경제이며 다른 나라의 대동유럽 무역이 독일 임금이나 고용에 직접 충격을 주지 않는다는 가정에 기초

- **Parallel trends**: DiD 타입은 아니지만, 지역 고정효과와 시간 고정효과 사용으로 지역별 상수적 특성과 시간 공통 트렌드 제거

## Empirical specification
**주요 방정식** (Equation 3):
```
ΔY_it = β_0 + β_1·Δ(Import exp.)_D←EAST + β_2·Δ(Export exp.)_D←EAST + β_3·X_i0 + τ_t + λ_i + ε_it
```
여기서:
- ΔY_it: 지역 i에서 시기 t-1에서 t 사이의 변수 변화 (제조업 고용 비율, 임금 등)
- Δ(Import exp.): 지역의 수입 노출 변화
- Δ(Export exp.): 지역의 수출 노출 변화 (로그 단위로도 사용)
- X_i0: 초기 통제변수 (1988년 산업별 고용 구성)
- τ_t: 시간 고정효과
- λ_i: 지역 고정효과
- ε_it: 오차항

**표준오차**: 50개 광역 노동시장 지역(greater labor market areas)으로 clustering

**통제변수**:
- 산업별 초기 고용 비중 (tradable vs non-tradable 분리)
- 자동차 산업 초기 비중 (별도 계수)
- 지역 고정효과 (328개 지역)
- 시간 고정효과 (1988-1998, 1998-2008)
- 광역 지역 더미 (North, South, West, East Germany)

## Main findings

### Manufacturing employment 효과 (Table 1, Column 5 - Full specification):
- **Import exposure coefficient**: -0.23 (약 2-3%)
 - 의미: 1 € 천 증가 → 고용 비율 약 0.23 p.p. 감소 (working-age population 기준)
 - 통계적 유의성: 5% 유의 (standard error ≈ 0.11, 약 -0.23/-0.11 ≈ 2.1)
 - 경제적 크기: 제조업 고용 절대 비율의 약 1-2% 감소

- **Export exposure coefficient**: +0.40 (약 40-50%)
 - 의미: 1 € 천 수출 기회 증가 → 고용 비율 약 0.40 p.p. 증가
 - 통계적 유의성: 1% 유의
 - 경제적 크기: 제조업 고용의 약 2-3% 증가

### 순효과 (Net effect):
저자들은 1988-2008 기간 동안:
- 동유럽과의 수출 기회 증가의 순영향 > 수입 충격의 부정적 영향
- **총 442,000 풀타임 일자리(full-time equivalent jobs) 순 증가**를 계산 (지역 가중 합산)
- 이는 독일 제조업 고용의 약 13% 규모 (당시 약 330만 명)

### 중국 vs 동유럽 분리 효과 (Table 3):
- **Eastern Europe**: 순 수출 효과 매우 강함. 높은 이중 무역(two-way trade) 특성으로 인해 상호 이득 실현
 - Net export coefficient: ~+0.60
 - 고용 효과: 양수 (독일이 동유럽으로부터 중간재 수입 후 가공·수출)

- **China**: 상대적으로 약한 순 수출 효과, 더 큰 순 수입 충격
 - Net import coefficient: ~-0.50
 - 하지만 절대 규모는 작음 (초기 중국 무역량이 작았고, 대부분 1998-2008 시기)

## Robustness

1. **Sample 분할**:
 - 시간 주기 분리 (1988-1998 vs 1998-2008): 후기(1998-2008)에 효과 훨씬 큼. 이는 중국의 부상 시점과 일치
 - 지역 제외: 가장 무역 의존적인 3개 지역(Groß-Gerau, Fürth, Ulm) 제외 → 결과 매우 안정적

2. **IV 강건성** (Appendix Table A.5):
 - 동유럽 vs 중국 instrument 별도로 사용 → 결과 일관성
 - Leave-one-out approach: 각 국가 IV 제외 후 재추정 → 순위 순서만 바뀌고 크기 유지

3. **Specification**:
 - OLS (no IV) vs 2SLS 비교: OLS 계수가 더 크거나 작음 → endogeneity 방향에 따라 변함
 - 지역 더미 추가/제거: 계수 안정적
 - 로그 vs 수준(level) specification: 일관성 유지

4. **US ADH 비교**:
 - ADH 방법론 정확히 복제한 독일 버전과 비교
 - "China syndrome" effect는 미국보다 약하고 부호 상이 (독일은 순이득)

## Heterogeneity

1. **지역별 이질성** (경제 구조):
 - 초기 제조업 비중 높은 지역: 수출 효과 더 큼 (규모 효과)
 - 자동차 비중 높은 지역: 양의 수출 효과 상당함 (자동차 산업이 동유럽 공급망 중심)

2. **산업별 이질성**:
 - **이중 무역(Intra-industry two-way trade)이 높은 산업**: 긍정적 순효과
 - 자동차, 기계류, 화학 등
 - 독일은 중간재/부품을 동유럽에서 수입 → 조립·고부가가치 공정 수행 → 재수출
 - **일방적 수입 산업**: 부정적 효과 (섬유, 조립 의류)

3. **기술 수준**:
 - 고기술 산업: 양의 수출 효과 (기술 기반 경쟁력)
 - 저기술 산업: 음의 수입 효과 (경가격 경쟁)

## Mechanism

저자들이 명시적으로 분석한 channel:

1. **수직적 특화(Vertical specialization) / Global value chains (GVC)**:
 - 독일-동유럽 간 양방향 무역이 매우 높음 (correlat ion coefficient: -0.067 China vs EE imports → 거의 직교)
 - 독일은 **상위 가치사슬**에서 중간재 수입 → 가공 후 수출
 - 이는 고용과 임금 모두에 양의 효과

2. **산업 구조 차이**:
 - 독일: 자동차, 기계 중심 (수직 통합, 높은 가치사슬)
 - 미국: 저부가가치 최종재 경쟁 (중국과의 수평적 경쟁)

3. **노동시장 조정**:
 - Worker-level 분석(Section 6)에서: 영향받은 개인의 임금 손실은 있으나, 재고용율이 높음 (지역 수출 증가로 인한 새 일자리 흡수)

4. **Direct vs indirect effect 분리 없음**:
 - 저자들은 reduced-form 계수만 제시
 - 메커니즘은 이론적 설명과 서술적 증거(narrative evidence)에 의존

## 본 paper와의 connection

### 매핑 위치 (본 논문 "Trade Shock and Deaths of Despair in Korea" v3.4 PAP):
- **Section 2 (Literature Review) → Identification strategy**로 직접 인용 가능
- **Section 3 (Methodology) → Shift-share IV framework** 정의 및 구현 방법
- **Section 4 (Empirical specification) → Equation (1)-(3) 설계** 참고

### 5-layer SE와의 매핑:
1. **Layer 1 (Main IV specification)**: Dauth-Findeisen-Suedekum과 동일한 shift-share IV 구조
 - 한국 데이터: 지역 수입 노출 = Σ_j (L_ijt / L_jt) × ΔIm_jt
 - Instrument: 다른 국가의 대한국 수입 또는 한국의 제3국 수출

2. **Layer 2 (DGHP 2017 ivmediate)**: Dauth et al.의 mediation approach 확장
 - 직접효과(고용 → 사망률)와 간접효과(고용 → 음주/약물 → 사망률) 분해

3. **Layer 3 (Romano-Wolf correction)**: Multiple hypothesis testing 시 적용
 - Dauth et al.에서 여러 종속변수(제조업, 임금, 고용률) 동시 테스트

4. **Layer 4 (OP test - overidentification)**: IV 강건성
 - DFS의 "leave-one-out" 방식과 유사하게, 한국에서도 여러 instrument (무역 상대국별, 산업별) 검증

5. **Layer 5 (Bartik IV + mediation)**: Layer 1-4를 통합하여 사망률과의 인과성 확인

### 직접 인용 가능 quote:
> "To address this concern, we use an instrumental variable (IV) strategy that is close in spirit to the approach by ADH. To instrument German regional import exposure from the East, we construct the following variable for every German region i..." (p. 6, Section 2.1)

> "The logic of the instrumental variable (5) is similar. As the East rises in the world economy, this induces a demand shock for all countries since the East becomes a more attractive export destination not just for Germany. Using (5) as an instrument for (2) purges the impacts of unobservable shocks, and thus identifies the causal impact of the rise of export opportunities in the East on German local labor markets." (p. 7, Section 2.1)

### Novelty claim 및 본 논문과의 차이:
- **DFS 분석 대상**: 노동시장 결과 (고용, 임금, 구직 기간)
- **본 논문 확장**: 무역 충격 → 노동시장 악화 → **사망률 (특히 자살, 약물 중독사, 알코올 관련 사망)의 인과 연쇄**
- 본 논문이 cover하지 않는 영역: **건강/사망 결과까지의 전파 경로**, 특히 **심리사회적 메커니즘(psychological distress, despair, family dissolution)**

## Quality assessment

### 본 논문 writer가 알아야 할 핵심 lesson 3개:

1. **Shift-share IV는 강력하지만 가정이 중요**: DFS는 다른 선진국의 수입/수출을 이용하여 exclusion restriction을 달성하였다. 하지만 한국의 경우 세계 무역 대국(한국이 매우 개방적)이므로, 제3국의 수입 변화가 한국의 노동시장에 직접 영향을 미칠 가능성이 있다. **Borusyak et al. (2025) practical guide**를 반드시 참고하여 split-sample 또는 leave-one-out IV 검증 필수.

2. **이중 무역의 부호 반전 가능성**: DFS의 핵심 발견은 독일이 동유럽과의 이중 무역에서 **순이득**을 본 것이다. 한국도 베트남, 방글라데시 등과 유사한 공급망 관계를 가질 수 있으므로, 간단히 "무역 충격 = 부정적"이라는 가정을 버려야 한다. **수출 기회의 증가**와 **수입 경쟁의 증가**를 분리하여 분석할 필요가 있다.

3. **노동시장 메커니즘만으로는 부족**: DFS의 worker-level 분석(Section 6)에서도 재고용율이 높았으나, 본 논문은 **사망률 증가**라는 극단적 결과를 본다. 이는 단순 고용 손실을 넘어 **심리사회적 충격, 중독, 가족 해체** 등의 역할을 시사한다. 따라서 **직접 노동시장 통제 이외에 추가 메커니즘**을 탐색해야 함 (e.g., 지역 재정(fiscal) 악화, 범죄율, 약물 시장 등).

---

## 참고: Dauth et al. (2014) 주요 통계표

| 항목 | 값 |
|-----|-----|
| **분석 기간** | 1988-2008 (10년 차이로 분석) |
| **분석 대상 지역** | 독일 328개 지역 |
| **제조업 고용 감소 (전체)** | -4 p.p. (16% → 12% of working-age population) |
| **순 무역 효과 (추정)** | +442,000 jobs (= 무역 없었을 시 고용 더 감소) |
| **수입 충격 계수 (IV)** | -0.23 |
| **수출 효과 계수 (IV)** | +0.40 |
| **동유럽 수입 증가 (1988-2008)** | 800% |
| **중국 무역 증가 시기** | 주로 1998-2008 |
| **지역 간 기초 통계** | Mean NTR gap: 6.8%, SD: 4.8%, IQR: 2.4-10.6% |

---

## 종합 평가
DFS는 ADH 이후 가장 영향력 있는 trade-labor market 연구로, **shift-share IV의 정확한 구현**과 **이중 무역 메커니즘의 중요성**을 보여준다. 본 논문은 이 프레임워크를 건강/사망 결과로 확장하는 첫 시도가 되어야 하며, 특히 **직역(literal) 복제가 아닌 한국식 적응(contextualization)**이 필수적이다.
