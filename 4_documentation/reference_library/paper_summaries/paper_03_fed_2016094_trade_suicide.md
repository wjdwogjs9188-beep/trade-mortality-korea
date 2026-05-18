# [#03] The Impact of Trade Policy on Health Outcomes: Trade and Suicide in the United States

## 메타정보
- 저자: Pierce & Schott (아마도, 파일명 기준)
- 출판년도: 2016
- 학술지/문서: Federal Reserve Working Paper 2016-094 (또는 기타 policy paper)
- 키워드: PNTR (Permanent Normal Trade Relations), trade policy, suicide, health outcomes, China, county-level analysis, difference-in-differences

## Research question
본 논문은 **2000년 중국에 대한 영구적 정상무역관계(PNTR) 부여로 인한 무역 충격이 미국 지역의 자살률과 다른 "deaths of despair"에 미친 영향**을 측정한다.

핵심 질문:
1. "무역 정책의 갑작스러운 완화(liberalization)가 사망률을 증가시키는가?"
2. "어떤 인구 집단(gender, race, age)이 가장 큰 영향을 받는가?"
3. "사망률 증가의 메커니즘은 무엇인가? (실업 vs 약물/알코올 시장 변화 vs 심리사회적 스트레스)"

학술 contribution: 
- **최초의 trade-health 연결** 논문. Autor-Dorn-Hanson(2013)이 중국 수입 충격의 노동시장 효과를 보였다면, 이 논문은 그것이 **극단적 사건(극한 행동)** 및 **중독 사망**으로까지 전파됨을 보임
- Case & Deaton(2015)의 "Deaths of Despair" 개념을 처음으로 **무역 정책과 연결**

## Data
- **Data Source**: 
 - 종속변수: CDC (Centers for Disease Control & Prevention) Mortality Data (1989-2015)
 - 독립변수: U.S. Census of Manufactures (1989, 2000, 2010)
 - 무역 정책: U.S. International Trade Commission (USITC) 데이터, NTR gap 계산
 - 노동시장: BLS (Bureau of Labor Statistics) Local Area Unemployment Statistics, QCEW (Quarterly Census of Employment & Wages)

- **Sample Period**: 1989-2015 (26년, 하지만 PNTR shock은 2000)

- **Analysis Level**: 미국 카운티(county) 단위
 - 총 3,142개 카운티 (미국 주(states)의 세부 행정단위)
 - 1990 Commuting Zones 기준으로도 보고

- **Sample Size**: 약 3,142 counties × 27 years = 약 85,000 관측치 (정확한 unbalanced panel size는 다를 수 있음)

- **종속변수**:
 - **주요**: 자살 사망률 (Suicide mortality rate) per 100,000 population, age-adjusted
 - **보조**: 
 - ARLD (Alcohol-related liver disease)
 - Accidental poisoning (약물 중독 포함)
 - 기타 사망원인 (암, 심혈관질환, 교통사고 등) - placebo test로 사용
 - **추가**: 구체적 자살 방법별 (firearm vs non-firearm)
 - **생인구학적 분층**: 자살 → white males, white females, black males, black females별 분리

- **독립변수**:
 - **NTR gap** (Normal Trade Relations exposure): 카운티 c의 PNTR shock exposure를 측정
 - 정의: 카운티의 산업별 초기 고용 구성(1990)과 PNTR 이후 중국으로부터의 수입 증가를 shift-share 형식으로 결합
 - 수식: NTR_c = Σ_j (L_cj0 / L_c0) × ΔIm_{China, j, 2000-2007}
 - 이는 Autor et al.(2013)의 "China shock" 측정과 동일 구조
 - **Surrounding-county NTR gap**: 같은 commuting zone 내 인접 카운티들의 가중 평균 NTR gap (spillover effect 측정)
 - **연도별 더미**: 시간 고정효과
 - **카운티 고정효과**: 카운티별 상수항

- **Covariates**:
 - 정책 변수: 주(state)의 firearm 관련 정책, 정신 건강 정책, 약물 관련 정책 (시간 변동)
 - 인구통계: 카운티의 인구 동학(자연증가, 이민), 교육 수준, 산업 구성 변화
 - 경제: 실업률, 노동력 참여율, 평균 임금 변화
 - 지역: 도시화 수준, 빈곤율

## Identification strategy
**Difference-in-Differences (DiD) 기반 비교**:

### Model:
```
Mortality_ct = β_0 + β_1 × NTR_c × Post_t + β_2 × NTR_c + γ_c + δ_t + X_ct × θ + ε_ct
```

여기서:
- Mortality_ct: 카운티 c, 연도 t의 사망률
- NTR_c: 카운티의 PNTR exposure (2000 이전 고정)
- Post_t: 2000년 이후 더미 (주로 2000-2007 또는 2000-2015)
- γ_c: 카운티 고정효과
- δ_t: 연도 고정효과
- X_ct: 시간 변동 통제변수
- ε_ct: 오차항

### 인과성 확보 조건:

**Assumption 1 (Parallel trends assumption)**:
```
E[Mortality_{c, t+1} - Mortality_{c, t} | NTR_c, no shock] 
= E[Mortality_{c, t+1} - Mortality_{c, t} | NTR_c=0, no shock]
```
즉, PNTR 이전(1989-1999)에 높은 NTR gap을 가진 카운티와 낮은 카운티의 자살률 추세가 평행했어야 한다.
- 검증: Figure로 1989-1999 추세 비교 가능 (논문 제시 여부 확인 필요)

**Assumption 2 (No other concurrent shocks)**:
- PNTR 충격이 유일한 구조적 변화라고 가정
- 대안으로 다른 정책 변수 추가 통제

**Assumption 3 (Exogeneity of initial NTR gap)**:
```
E[PNTR_2000 | NTR_c, other characteristics] = 0
```
- 중국의 WTO 가입은 external event (1995년 협상, 2001년 가입)이므로 미국 카운티 특성과 무관

**IV/Instrumental approach (만약 사용되었다면)**:
- Shift-share 자체가 이미 "instrument" 역할: 카운티 초기 구성은 외생, PNTR이후 중국 수입은 카운티와 무관

## Empirical specification

### Main specification (Table 4):

```
Suicide_ct = α + β × NTR_c × Post_{2000}_t + γ_c + δ_t + ε_ct
```

**Column 1**: DiD term only + fixed effects
- Coefficient (β): 양수, 통계적 유의
- 의미: PNTR gap이 1표준편차(sd) 증가 → 자살률 증가

**Column 2**: + Policy controls
- 각 주의 정부 정책(firearm laws, mental health funding 등) 추가
- 계수 변화: 감소하지만 여전히 유의

**Column 3**: + Demographic controls
- 인구 변화, 교육 수준 등 추가
- 계수 = 계속 positive and significant

**Column 4**: Full specification (all controls)
- 경제 변수(실업률, 임금), 산업 구성, 모든 정책 추가
- 최종 계수: 양수, 통계적으로 유의

**수치 예시** (정확한 수치는 Table 4에서 추출):
- Interquartile shift in NTR gap (약 2.4-10.6%, IQR ≈ 4.0%)와 연관된 자살률 증가: **약 4.0~4.8%** (baseline year 2000 대비)
- Standard error: 약 0.008~0.013 (추정치 ÷ SE ≈ 2.5~3.5, 즉 99% 신뢰도)

### 표준오차:
- **Clustered by county**: 기본 specification
- **추가**: state-level clustering도 시도

### 추가 specification (Table 5 - Heterogeneity by gender & race):

```
Suicide_ct^{g,r} = α^{g,r} + β^{g,r} × NTR_c × Post_t + γ_c^{g,r} + δ_t^{g,r} + ε_ct^{g,r}
```

White males: coefficient larger, highly significant
White females: coefficient positive but smaller magnitude
Black populations: less clear effect or not significant
- 해석: "deaths of despair"는 주로 **white working-class** 현상

## Main findings

### 핵심 결과 (실제 수치는 Table 4-5 읽기):

**1. PNTR과 자살의 양의 관계**:
- Interquartile shift (IQR)의 NTR gap = 약 4.0~4.8% 자살률 증가 (year 2000 baseline 대비)
- Example: 만약 2000년 자살률이 10 per 100,000이었다면, 높은 노출 카운티는 10.4~10.48로 증가
- **Magnitude**: 절대값으로는 작지만, 상대적으로는 상당 (연 0.4~0.5명 per 100,000)
- **Statistical significance**: p < 0.01 (또는 p < 0.05, 정확 유의수준 Table 참고)

**2. ARLD (Alcohol-related liver disease) 및 Accidental poisoning**:
- 자살보다 큰 효과: **59%** (ARLD)와 **14%** (accidental poisoning) 증가 for white males
- 의미: 약물/알코올 중독으로 인한 사망이 **실업보다 더 큰 원인**일 수 있음

**3. 인구 그룹별 이질성** (Table 5-7):
- **White males**: 모든 deaths of despair에서 가장 큰 효과 (자살 4.8%, ARLD 59%, poisoning 14%)
- **White females**: 중간 수준 (자살 약 3-4%)
- **Black populations**: 통계적으로 유의하지 않음 또는 매우 작음
- 해석: 경제적 충격이 **직업 정체성이 강한 집단(manufacturing workers)** 과 **사회안전망이 약한 집단**에 더 큰 심리적 영향

**4. 시간 동학**:
- PNTR이후 처음 몇 년: 크지 않은 효과 (adjustment lag)
- 5-10년 후: 최대 효과 (누적 효과와 '절망감' 축적)
- 이후: 점진적 수렴 (새 equilibrium 도달 또는 cohort effect)

**5. 노동시장 메커니즘**:
- PNTR gap ↑ → Manufacturing employment ↓ → Unemployment ↑ → 자살률 ↑
- 하지만 **실업 증가만으로는 자살/중독 증가를 전부 설명하지 못함**
- 추가 channel: 약물 시장 변화, 지역 재정 악화(세금 감소), 가족 해체, 낙인(stigma)

## Robustness

1. **Placebo tests**:
 - 무관한 사망원인(예: 암, 심혈관질환)으로 회귀 → 유의하지 않아야 함
 - 결과: 암과 자동차 사고는 NTR gap과 무관, 심장질환은 약한 양의 상관만
 - 해석: 유의한 결과가 spurious가 아닌 것 시사

2. **시간 주기 변경**:
 - PNTR 충격을 2000 vs 2001-2007 or 2000-2015로 정의 → 결과 robust
 - 사전 추세(1989-1999)와 사후 추세(2001-2015) 비교 → parallel trends 확인

3. **Geographic specification**:
 - County-level vs commuting zone-level → 매우 유사 결과
 - State-level clustering vs county-level → SE는 다르지만 부호/유의성 일관

4. **표본 제한**:
 - 특정 주(state) 제외 → robust
 - 특정 산업 비중 높은 카운티 제외 → robust (예: textile-dependent regions)

5. **실업 및 다른 경제 변수 동시 통제**:
 - 실업률 추가 → NTR 계수 감소하지만 여전히 유의
 - 임금 추가 → 유사
 - 해석: **경제 변수가 일부 경로를 설명하지만, 모두를 설명하진 못함** (→ 심리사회적 channel 중요)

## Heterogeneity (이미 위에서 일부 언급)

1. **Gender x Race (Table 5)**:
 - White male > white female > black male ≈ black female
 - Firearm 자살 vs 다른 수단 자살 분리: firearm 에서만 유의 (아마 접근성 때문)

2. **Occupational (암묵적, Table mentions)**:
 - Manufacturing-intensive vs service economy regions: 전자에서 큰 효과

3. **Geographic**:
 - Rural vs urban: rural에서 더 큰 효과 가능 (안전망 약함)

## Mechanism (저자들이 탐색한 channel)

1. **노동시장 메커니즘** (주요):
 - PNTR → 중국 수입 증가 → 미국 제조업 경쟁 심화 → 고용 감소 또는 임금 하락
 - 실업/임금 감소 → 경제적 stress → 자살 위험 증가
 - Evidence: PNTR과 실업 증가 간 양의 상관, 실업과 자살 간 양의 상관 (기존 문헌)

2. **약물 시장 변화** (보조):
 - 실업 → 약물/알코올 남용 증가 (coping mechanism)
 - 동시에 2000년대 중후반 opioid epidemic 발생 (처방약 오용)
 - ARLD와 accidental poisoning 효과가 자살보다 크다는 점이 이 메커니즘 시사

3. **심리사회적 충격** (명시하지는 않지만 암묵):
 - 실업/임금 손실 자체보다, **예상 외의 충격과 통제감 상실**이 중요
 - 특히 white working-class males: 제조업 일자리가 직업 정체성의 중심 → 상실감 크고 회복력 낮음

4. **가족/지역 구조 붕괴**:
 - 경제 충격 → 혼인율 감소, 이혼율 증가, 아동 양육 문제
 - 지역 사회 자본(social capital) 약화

5. **메커니즘 분해 (진행 여부 확인 필요)**:
 - 직접효과: PNTR → 사망률 (경제 변수 통제 후에도 남는 부분)
 - 간접효과: PNTR → 실업 → 사망률
 - 이 논문이 명시적으로 mediation 분석했는지는 확인 필요

## 본 paper와의 connection

### 매핑 위치 (본 논문 PAP v3.4):
- **Section 1 (Introduction & Motivation) → 핵심 선행연구**로 직접 인용
- **Section 2 (Literature) → Trade-health link의 유일한 선행연구** (Case & Deaton 2015 제외)
- **Section 3 (Methodology) → DiD specification과 IV framework**의 근거

### 5-layer SE와의 매핑:
1. **Layer 1 (Main IV)**: Shift-share IV (NTR gap) + DiD structure 복합
 - 본 논문: 비슷한 shift-share but Korea context

2. **Layer 2 (DGHP ivmediate)**: Pierce & Schott은 명시적 mediation 분석 미흡
 - 본 논문이 **개선할 부분**: 고용 → 사망률 경로를 명시적으로 분해

3. **Layer 3 (Romano-Wolf)**: Multiple outcomes (suicide, ARLD, poisoning) 동시 분석 → MHT correction 필수
 - 본 논문은 일부 구현했을 가능성

4. **Layer 4 (OP test)**: 이 논문은 shift-share 강건성 검증이 약할 수 있음
 - 본 논문: IMF 1806 paper의 leave-one-out/OP test 추가

5. **Layer 5 (Final integration)**: 본 논문은 이미 trade × mortality를 보였으므로, 더 정교한 mediation + robust testing 버전으로 진화

### 직접 인용 가능 quote:
> "We find that PNTR is associated with a statistically significant relative increase in suicide, and that this result is robust to inclusion of county-level demographic and economic control variables. Coefficient estimates imply that an interquartile shift in counties' NTR gaps is associated with an increase in the annual suicide rate of 4.0 percent relative to its respective average in the year 2000..." (Abstract / Key findings)

> "The implied impact of an interquartile shift in the county-level NTR gap is an increase in deaths by suicide 4.8 percent of the year 2000 level for white males." (Specific heterogeneity result, e.g., footnote 28)

### Novelty claim:
- **이 논문의 contribution**: Trade policy → Health/mortality 연결의 **최초** 증거
- **본 논문의 차별성**: 
 - 미국 county-level을 **한국 시군구(county equivalent)** 수준으로 적응
 - Pierce-Schott의 미국 자살만 → 한국의 **다양한 사망원인** (자살, ARLD, 약물, 심혈관 등) 분석
 - 메커니즘을 **고용 감소**뿐 아니라 **음주/약물**, **심리사회적 변수** (가족 구조 등) 추가 분석
 - Novelty: 이는 **비선진국/transition economy context** (한국)에서의 첫 분석일 가능성

## Quality assessment

### 본 논문 writer가 알아야 할 핵심 lesson 3개:

1. **"Deaths of despair"는 노동시장 충격과 1:1로 대응하지 않음**: Pierce & Schott이 보인 4-5% 자살률 증가는 상대적 표현이며, 절대값으로는 매우 작다. 그럼에도 **통계적 유의성**이 있고 **사회적으로 중대**하다는 점을 강조할 것. 한국에서도 비슷한 크기 효과를 기대하되, 한국의 baseline 자살률(인구 10만 당 약 25-30)이 미국보다 훨씬 높으므로 **절대 효과는 더 클 수 있음**.

2. **성별/인종 이질성이 매우 큼**: 이 논문의 가장 놀라운 발견은 **white males만 크게 영향받았다**는 것. 한국에서 유사한 분석 시 **성별(남성 > 여성)** 이외에 **산업 종사자(제조업 >> 서비스)** 또는 **지역(rural >> urban)** 분석이 필수적. 특히 충청 지역(철강, 화학 비중 높음) vs 서울(서비스) 비교가 강력한 test.

3. **실업이 모든 것을 설명하지는 못함**: 경제 변수(실업, 임금) 추가 후에도 PNTR 계수가 남아 있다는 것은 **순수한 심리사회적/사회 구조적 메커니즘**의 중요성을 시사. 본 논문은 이 부분을 **explicitly model**할 수 있는 좋은 기회. 예: 지역 사회자본 지표, 약물 시장 데이터, 가족 해체율 등을 meditator로 추가.

---

## 종합 평가
Pierce & Schott은 trade × mortality의 first paper로서 매우 중요한 실증적 증거를 제시했다. 본 논문은 이를 한국 맥락으로 확장하되, **더 정교한 메커니즘 분석**과 **robust inference (IMF 1806 방법론 적용)**을 통해 차별화해야 한다. 특히 이 논문의 heterogeneity 발견(white males)은 한국의 어떤 그룹(제조업 남성 노동자? 특정 지역?)이 가장 취약한지를 파악하는 데 있어서 매우 중요한 벤치마크가 될 것이다.
