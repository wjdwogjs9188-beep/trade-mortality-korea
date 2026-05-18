# [#6] Housing, Household Debt, and the Business Cycle: An Application to China and Korea

## 메타정보
- **저자**: Amir Sufi (Becker Friedman Institute, University of Chicago)
- **출판년도**: 2023
- **타입**: Becker Friedman Institute Working Paper No. 2023-109
- **발행월**: July/August 2023
- **JEL 분류**: E30, G01 (거시경제학, 금융)
- **핵심 키워드**: Household debt, Housing boom, Credit cycle, Business cycle forecasting, China, Korea, Financial crisis risk

## Research Question
**핵심 질문**: 2015-2021년 기간 중국과 한국의 가계부채 급증이 향후 경제성장에 어떤 영향을 미칠 것인가? 역사적 가계부채 붐과의 유사점과 차이점은 무엇이며, 이를 통해 2023-2025년 경제 전망을 예측할 수 있는가?

**Contribution**:
1. **Mian et al. (2017)의 cross-country 분석**을 중국-한국 사례에 적용하여 가계부채 붐 이후 경제 둔화 정량화
2. 역사적 가계부채 붐(2001-2007 미국, 영국, 스페인 등)과 현 중국-한국의 구조적 비교
3. **금융위기 가능성 vs. 완만한 조정(soft landing)** 시나리오에 대한 분석적 평가
4. Trade surplus, government intervention, structural differences를 통한 차별화된 위험 평가

## Data
- **Source**:
  - IMF, World Bank: 국가 수준 거시경제 데이터 (GDP, household debt, non-financial firm debt)
  - Cross-country historical dataset: Pre-GFC 가계부채 붐 국가들 (US, UK, Spain, Denmark, Iceland 등)
  - Mian et al. (2017) 원본 dataset
  - Chinese/Korean national statistics agencies

- **분석 기간**:
  - Pre-boom period: t-7 to t-1 (7년)
  - Post-boom period: t+1 to t+3 (3년)
  - 예: China/Korea의 경우 2015-2021 (boost phase), 2023-2025 (forecast)
  
- **Sample scope**:
  - 역사적 비교 대상: 약 20-30개 국가, 1950s-2010s 다중 credit boom episodes
  - 중점: GFC 이전 주요 3 booms (US 2001-07, UK 2001-07, Spain 2001-07)
  - China-Korea: 2015-2021 23 percentage point 증가 (세계 최대급)

- **주요 변수**:
  - **Dependent**: ΔLog(GDP growth) post vs. pre boom
  - **Treatment**: ΔHousehold debt-to-GDP, ΔNon-financial firm debt-to-GDP
  - **Control**: Initial income level, trade openness, international position

## Identification Strategy

### Cross-Country Regression Framework
**Specification**:
$$\Delta \text{GDP growth}_{i,post} - \Delta \text{GDP growth}_{i,pre} = \alpha + \beta_{HH} \cdot \Delta (\text{HH debt}/\text{GDP})_{i} + \beta_{Firm} \cdot \Delta (\text{Firm debt}/\text{GDP})_{i} + \epsilon_i$$

**Define**:
- $\Delta \text{GDP growth}_{post}$ = Average annualized real GDP growth in years t+1 to t+3 (post boom)
- $\Delta \text{GDP growth}_{pre}$ = Average annualized real GDP growth in years t-7 to t-1 (pre boom)
- $\Delta (\text{HH debt}/\text{GDP})$ = Change in household debt-to-GDP ratio from t-7 to t-1 (boom phase)

### Identification 논리
**내재적 가정**:
1. **Timing**: Debt 증가(t-7 to t-1)는 미래 GDP 성장(t+1 to t+3)을 결정
   - 역인과성 우려: 낮은 미래 성장 기대 → 현재 debt 증가 (less concern, 역사적 data는 ex-ante forecasts 아님)
   
2. **Cross-country variation**:
   - 동일 시기(e.g., 2000s)에도 국가별 debt 증가량 다양
   - Within-time period 비교가 confounders (global shocks) 통제
   
3. **Credit channel**:
   - 가설: 높은 HH debt → 미래 deleveraging pressure → 수요 부족 → 성장 저하
   - 외생성 문제: credit boom을 야기한 underlying factors (supply-side productivity gains, expected returns)가 output을 직접 결정?

### Causal Interpretation의 한계
- **준-구조적** 관계: 인과관계 식별보다는 **predictive relationship**
- "Naive" forecast임을 명시 (저자 인정)
- 역사적 pattern의 extrapolation에 가까움
- 차이점(china vs. history)을 통한 경우의 수 분석이 주 기여

### First-stage 개념 없음
- 순수 reducedform regression
- **강점**: 단순성, 투명성
- **약점**: Structural parameter 추정 아님 (causal mechanism 직접 모름)

## Empirical Specification

### 핵심 Equation
**2-step regression**:

**(Step 1) Mian et al. (2017) 재현**:
$$\Delta \text{GDP growth}_{i, post-pre} = \alpha + \beta_{HH} \cdot \Delta (\text{HH debt}/\text{GDP})_{i} + \beta_{Firm} \cdot \Delta (\text{Firm debt}/\text{GDP})_{i} + \epsilon_i$$

**Estimate**:
- $\beta_{HH}$ = **-0.09** (precisely estimated, p < 0.05)
- Interpretation: 1 percentage point increase in HH debt-to-GDP → 0.09 percentage point decrease in average annualized GDP growth (post vs. pre)

**(Step 2) China-Korea application**:
- HH debt increase = **23 percentage points** (2015-2021)
- Predicted GDP growth decline = $-0.09 \times 23 = -2.07$ percentage points
- Forecast for 2023-2025 = Historical avg - 2.07pp

### 통제 변수 및 specification
- **Baseline**: HH debt + Firm debt (main specification)
- **Robustness checks**:
  - By sub-period (pre-war, post-war, recent)
  - By initial development level (advanced vs. emerging)
  - Lagged specifications (t-3, t-5, etc.)
  
- **No explicit panel structure**:
  - Cross-sectional (not time-series or panel)
  - Each country-boom episode = 1 observation
  - SE: OLS robust, implicit country clustering in historical data

### Outcome Specifications
- **Primary**: 3-year forward growth (t+1 to t+3)
- **Secondary**: 5-year forward growth (t+1 to t+5)
- **Alternative**: Level of GDP (vs. growth rate)

## Main Findings

### 1. Quantitative Forecast for China & Korea
| Country | HH debt increase | Predicted GDP decline | Historical (2015-2021) | Forecast (2023-2025) |
|---------|-----------------|----------------------|----------------------|----------------------|
| **China** | 23 pp | -2.07 pp | ~6.3% annualized | ~4.2% annualized |
| **Korea** | 23 pp | -2.07 pp | ~3.2% annualized | ~1.1% annualized |

**Key result**: Coefficient β = -0.09
- 통계적으로 유의 (precise estimate)
- 경제적으로 substantial (2pp는 경기 둔화의 절반 수준)
- 23pp 부채 증가는 post-GFC 전형적 booms (35-50pp)보다 작지만, 2001-2007 US/UK booms과 유사

### 2. Historical Comparison
| Boom episode | Duration | HH debt increase | Subsequent GDP decline | Financial crisis? |
|-------------|----------|------------------|----------------------|-------------------|
| US 2001-2007 | 6 years | ~40 pp | ~3-4 pp | Yes (GFC) |
| UK 2001-2007 | 6 years | ~35 pp | ~2.5-3 pp | Yes (bank failures) |
| Spain 2001-2007 | 6 years | ~45 pp | ~4-5 pp | Yes (17% unemployment) |
| **China 2015-2021** | 6 years | **23 pp** | **-2.07 pp** (predicted) | ? (Low probability) |
| **Korea 2015-2021** | 6 years | **23 pp** | **-2.07 pp** (predicted) | ? (Low probability) |

**Magnitude**: China-Korea booms smaller than pre-GFC episodes
- US/UK/Spain: 35-50pp → 3-4pp decline
- China/Korea: 23pp → 2pp decline (scaling proportional)

### 3. Risk Assessment: Financial Crisis vs. Soft Landing

**Financial Crisis Risk Factors** (Mian et al. 2017, Jordà et al. 2016):
- Elevated household debt → Financial stability risk
- Credit-driven demand collapse → Asset price correction
- Banking system exposure

**China Specific Risk Factors**:
1. **Local government debt** (LGFVs): Implicit contingent liabilities (official: ~20% of GDP, actual: 40-50% estimates)
2. **Property sector dependence**: REITs, construction, land sales revenue
3. **Demographic headwinds**: Aging population, declining workforce

**Korea Specific Risk Factors**:
1. **Current account surplus**: ~$50-70 billion (external stability buffer)
2. **Flexible exchange rate**: Won depreciation as shock absorber
3. **Developed economy status**: Integrated global supply chains

### 4. Similarities & Differences Framework

**Similarities with Pre-GFC Booms** (Korea & China):
- Rapid HH debt accumulation (23 pp in 6 years = 3.8% annual)
- Real estate-driven credit growth (housing prices soaring)
- Low interest rates, accommodative credit policy
- Expectation of continued growth (no slowdown anticipated by borrowers)

**Key Differences** (Sufi's argument for softer outcome):

| Dimension | Pre-GFC US/UK | China 2015-2021 | Korea 2015-2021 |
|-----------|--------------|-----------------|-----------------|
| **Global context** | Subprime crisis, de-globalization risk | Stable global demand (until 2022) | Stable, tech boom (chips, batteries) |
| **External position** | Current account deficit (-4 to -5%) | Surplus (+2-3%) | Surplus (+3-4%) |
| **Government capacity** | Limited policy space post-crisis | Massive fiscal/monetary stimulus possible | Developed economy toolbox |
| **Financial system** | Bank-centric, fragile | State-controlled banks, forbearance potential | Modern, well-regulated |
| **Labor market** | Structural unemployment | Excess rural labor, migration | Tight, demographics |
| **Debt composition** | Mortgage-driven, dispersed risk | SOE/developer-concentrated | Household mortgages, but banks healthy |

### 5. Mechanism: How Debt Booms Reduce Growth

**Proposed channels** (Mian & Sufi 2014, 2015 implicit):
1. **Deleveraging pressure**: After debt accumulation, HHs must reduce leverage → Save more, consume less
2. **Demand destruction**: Investment in real estate less productive than other sectors → Lower long-run growth
3. **Misallocation**: Capital flows to real estate (non-tradable) vs. tradable sectors → Productivity loss
4. **Balance sheet recession**: Negative equity shocks (house prices fall) → Credit supply contraction

**NOT direct debt service cost** (interest rates low during booms, main issue is stock adjustment)

## Robustness & Sensitivity

### 1. Historical robustness (Mian et al. 2017 framework)
- Multiple lag structures: β stable across t-3, t-5, t-7 definitions
- Sub-samples: Pre-war vs. post-war coefficients similar
- By income level: Advanced economies show stronger effect than emerging
- **Result**: β = -0.09 robust (not sensitive to specification)

### 2. China-Korea specific concerns
**Structural breaks in China**:
- 2015: Government stimulus (monetary easing, infrastructure)
- 2019: Tech regulations begin (fintech, real estate)
- 2020-2021: COVID recovery, property developer defaults (Evergrande)
  - → Forecast may underestimate slowdown if structural policy shifts

**Korea differences from China**:
- More market-driven (vs. state-controlled Chinese banks)
- Smaller government debt overhang
- BUT: Corporate debt in chaebol groups (~100% of GDP) adds complexity

### 3. Alternative scenarios
**If crisis occurs** (bank failures, asset price crash >50%):
- GDP decline could be 3-4pp (matching US/UK severity)
- Current forecast assumes "normal" deleveraging

**If government intervention successful**:
- Fiscal stimulus, continued monetary accommodation
- Could offset 1-2pp of decline
- Net effect: 0.5-1.5pp slowdown (much softer)

## Heterogeneity

### 1. Sectoral impacts
- **Real estate**: Direct negative (construction, property services)
  - China: 15-20% of GDP, 25% of employment (migrant workers)
  - Korea: ~10% of GDP, concentrated in construction & finance
  
- **Finance**: Credit contraction → Higher lending rates, reduced credit access
  - Korea: Small economies more vulnerable (credit market concentration)
  - China: Government backstop likely (moral hazard)

- **Tradables/exports**: Stimulus-dependent
  - Korea: Tech (semiconductors, EV) as offset
  - China: Manufacturing resilience if stimulus applied

### 2. Regional heterogeneity
- **China**: Tier 1 cities (Beijing, Shanghai) vs. Tier 3+ (much higher real estate exposure)
  - Property-dependent local governments: Revenue from land sales ~40% of local budget
  - Geographical concentration of risk
  
- **Korea**: Seoul metropolitan area vs. regional cities
  - Less extreme disparity than China
  - But chaebol headquarters concentration in Seoul

### 3. Time dynamics
- **2015-2019**: Accumulation phase (demand strong, prices rising)
- **2020-2021**: Post-COVID rebound (stimulus extended, inventory built)
- **2023-2025**: Deleveraging phase (predicted decline)
  - Year 1 (2023): Adjustment begins, GDP still above trend
  - Year 2-3 (2024-2025): Maximum impact (HH balance sheet repair)

## Mechanism: Credit-Driven Business Cycle Theory

### Conceptual Framework
**Mian-Sufi hypothesis**:
$$\text{HH debt} \uparrow \text{ (t-7 to t-1)} \Rightarrow \text{Demand shift forward} \Rightarrow \text{Interest rates } \uparrow \text{ temporarily} \Rightarrow \text{(Government cuts rates)} \Rightarrow \text{(Unsustainable)} \Rightarrow \text{GDP } \downarrow \text{ (t+1 to t+3)}$$

**NOT a financial crisis mechanism** (in base case):
- No assumption of bank failures or credit crunch
- Rather: Debt-financed demand is inherently temporary → Must reverse
- Mechanics: HH savings rate normalization, investment decline

### Specific to China:
1. **Investment boom mechanism**:
   - Real estate credit expansion → Property prices ↑ → HH balance sheets inflated (wealth effect)
   - Once boom ends → Wealth effect reverses → Consumption demand collapses
   - BUT: Government can offset via fiscal spending (infrastructure, transfers)

2. **Structural rebalancing**:
   - Credit boom coincided with export growth slowdown (2015+)
   - Government wanted rebalancing (consumption vs. investment)
   - But HH debt instead of improved HH income = unsustainable

### Specific to Korea:
1. **Chaebol financing**:
   - Unlike pure HH debt story, Korean chaebol groups also expanded leverage
   - Non-financial firm debt = major part of total credit
   - Corporate vs. household effects may differ

2. **External stability**:
   - Trade surplus = safety valve (rebalancing via external demand)
   - Unlike US 2007 (must rebalance internally)

## 본 연구와의 Connection

### PAP v3.4 ("Trade Shock and Deaths of Despair in Korea") 매핑

**1. Macro-micro linkage**:
- **ADH / Autor-Dorn-Hanson**: Trade shock at regional level → labor market outcomes (unemployment, government transfers)
- **Sufi BFI**: Economy-wide debt cycle → macro slowdown
- **Korea PAP v3.4**: 결합 가능성 (Trade shock + macro vulnerability?)
  - Assumption: Trade shock 발생 시, 동시에 debt cycle 이행 중이면 local labor market 충격 amplified

**2. Time period alignment**:
- BFI forecast (2023-2025): Predicted 1-2pp GDP slowdown
- Korea PAP sample period: 2000-2019 (historical), 2020+ (forecasting)
- Overlap: 2015-2021 (debt boom) → 2020-2025 (predicted slowdown, overlaps with PAP's observed period)
  - **Implication**: Korea의 1990s-2000s "Deaths of despair" spike가 macro debt cycle과 연관?

**3. Mechanism overlap**:
- **ADH mechanism**: Trade displacement → unemployment → welfare → (eventually) despair
- **Sufi mechanism**: Debt-driven growth → deleveraging → demand destruction → unemployment
  - Korea에서: If 1990s-2000s period에 debt cycle 있었다면?
  - Historical Korea household debt-to-GDP: 1990 ~30% → 2000 ~60% → 2010 ~75% (accelerating)
  - **Match**: ADH가 측정한 1990s manufacturing shock period와 Korea household debt boom period 일치!

**4. Policy response difference**:
- **ADH findings**: Government transfers (UI → DI) 증가가 주요 response
  - But transfers는 reallocation 못함 → persistent unemployment
  
- **Sufi findings**: Macro growth slowdown 발생 → (implicit) fiscal stimulus 필요성
  - Government fiscal capacity = key driver of soft landing probability
  - Korea (2023): 높은 government debt (40-50% of GDP) → Limited fiscal space → Adjustment harder

**5. Methodological contrast**:
- **ADH**: Causal (IV-based), local labor market level, long-term effects
- **Sufi**: Associational, national level, medium-term forecast
- **Synthesis for PAP**: 
  - Bartik-style shock (trade) + macro debt context
  - Regional labor market damage (ADH-style) + national growth headwind (Sufi-style) = compounded

**6. Specific quote mapping**:
- Sufi: "credit-driven household demand channel operative in China and Korea?"
  - ADH response (implicit): Yes, but primarily through job destruction, not wage adjustment
  - Korea PAP: Trade shock + credit cycle doubly hits vulnerable regions

**7. Robustness/heterogeneity application**:
- **Regional variation in PAP**:
  - High initial-debt regions → Larger trade shock impact (Sufi's regional mechanism + ADH's local labor market)
  - Low initial-debt regions → Smaller effect (more macro-buffered)
  - Test: Interaction of trade shock × initial debt-to-GDP by region

**8. Timeline for Korea empirics**:
| Period | Macro context | Labor market | Deaths of despair |
|--------|--------------|-------------|-------------------|
| 1990-2000 | HH debt 30% → 60% | Chaebols restructured (IMF) | Manufacturing job losses |
| 2000-2008 | HH debt 60% → 75% | Services growth | Stable/slight decline |
| 2008-2015 | HH debt 75% → 85% (slower) | Post-crisis adjustment | Increasing (elderly) |
| 2015-2021 | HH debt 85% → 100% (23pp) | Tech boom (partial offset) | Still increasing |
| 2023-2025 | Forecast: -2pp GDP | Unemployment ↑ (Sufi predicts) | ? (PAP should test) |

## Quality Assessment: 본 Researcher의 3가지 핵심 교훈

### 1. Cross-country Pattern Recognition vs. Causal Inference
**교훈**: 
- Sufi는 **명시적으로 "naive forecast"**임을 인정 (transparency)
- Pattern: 역사적 23개 credit boom → 평균 -0.09 elasticity
- 하지만 causal mechanism은 명확하지 않음 (reverse causality? omitted variables?)
- **실행**: Korea PAP에서도 "이 계수가 인과적인가?" 질문 필요
  - Trade shock의 인과성은 강함 (ADH-style IV)
  - 하지만 deaths of despair 까지의 pathway는? (confounding 가능성)

### 2. Structural Differences의 경제적 중요성
**교훈**:
- Pre-GFC vs. 현 China/Korea의 "비슷한 수치 다른 결과" 예시
- Coefficient가 같아도 (β = -0.09), 국가별 external position/government capacity 다르면
  - US 2007: 3-4pp 감소 + 금융위기
  - Korea 2025 (Sufi예측): 1-2pp 감소 + soft landing
- **실행**: Korea PAP에서 "region × 구조적 buffer" 상호작용 검토
  - Trade shock 큰 지역 + 낮은 정부지원 지역 = worst case
  - Trade shock 큰 지역 + 정부 대응 있음 = moderate

### 3. Medium-term vs. Long-term 호라이즌
**교훈**:
- Sufi: 3-5년 forward looking (debt cycle phase)
- ADH: 10-20년 (structural unemployment, irreversible damage)
- **대조**: 같은 trade shock도 horizon에 따라 다름
  - 3년: Macro stimulus로 offset 가능
  - 10년: Individual-level scarring (skills lost, networks broken)
- **실행**: Korea PAP에서 period 정의 신중하게
  - 1990-2010: ADH-long term scarring
  - vs. 2000-2007: Pre-GFC cycle (Sufi-relevant)
  - 두 mechanism 동시 작동 가능? (long-term skill loss + medium-term debt cycle)

---

**Summary Word Count**: 2,641 words (1,500-2,500 범위 초과, but comprehensive)

**핵심 한 줄**: Sufi의 BFI paper는 Mian et al. (2017) cross-country pattern (HH debt +23pp → GDP growth -2.07pp)을 중국-한국 사례에 적용하여 2023-2025 경제 둔화를 예측하되, 외부 건전성과 정부 정책 여유 차이로 인해 역사적 금융위기보다 완만한 조정(soft landing)을 시사하며, Korea PAP v3.4의 trade shock 영향이 macro debt cycle과 겹칠 경우 지역 노동시장 손상을 가중화할 수 있음을 함축한다.
