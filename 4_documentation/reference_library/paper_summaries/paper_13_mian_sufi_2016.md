# [#13] Household Debt and Business Cycles Worldwide

## 메타정보
- **저자**: Atif Mian (Princeton University), Amir Sufi (University of Chicago Booth), Emil Verner (Princeton University)
- **년도**: 2016
- **학술지**: *American Economic Review*, Vol. 106 (cross-country macro-finance journal)
- **분류**: Household debt × Business cycles × Global macroeconomy

---

## Research Question

Is there a systematic empirical relation between household debt and business cycles across advanced economies? Does an increase in household debt predict lower GDP growth in the medium run? What are the mechanisms: credit demand shocks vs. credit supply shocks? Is there a global household debt cycle that amplifies recessions?

---

## Data

**Sample**: Unbalanced panel of 30 mostly advanced countries, 1960-2012
- Advanced economies: US, UK, Euro zone, Canada, Japan, Australia, etc.
- Emerging markets: Korea, Mexico, Turkey, Hong Kong, Singapore, Indonesia, Thailand, etc.
- Notable exclusions: China, India, South Africa (decomposed credit series only post-2006)

**Credit Data**:
- Source: Bank for International Settlements (BIS) "Long series on total credit to the non-financial sectors"
- Definitions:
 - **Household debt to GDP** ($d^{HH}_{it} = \frac{D^{HH}_{it}}{Y_{it}}$): Outstanding residential mortgages + consumer credit
 - **Non-financial firm debt to GDP** ($d^F_{it} = \frac{D^F_{it}}{Y_{it}}$): Outstanding credit to non-financial corporations
- Concept: Total credit (loans + bonds) from domestic + foreign banks + non-bank institutions
- Coverage: Broader than bank lending only; includes securitized lending
- Time series: Average 30 years per country (23 years after differencing to 3-year changes)

**Macroeconomic Data**:
- Real GDP (log), consumption (durable, non-durable, services), investment
- Trade: Exports, imports, net exports, current account
- Labor market: Unemployment rate
- Financial: House prices, interest rate spreads (mortgage-sovereign)
- Expectations: IMF World Economic Outlook & OECD Economic Outlook forecasts (1972-2012)

**Sample Statistics** (Table I):
- Total private debt growth: +3.11 pp/year average
- Household debt volatility: σ(∆d^{HH}) moderate; firm debt: ~2× household volatility
- GDP growth volatility: Baseline for comparison (consumption/investment/imports 2.8-3.6× more volatile)

**Observations**: >900 country-years; Full panel (balanced) for VAR: 30 countries average

---

## Identification Strategy

### Core Design: VAR + Local Projections for Dynamic Identification

**VAR Specification** (Section III.A):

$$\mathbf{A}\mathbf{Y}_{it} = \mathbf{a}_i + \sum^p_{j=1} \boldsymbol{\alpha}_j \mathbf{Y}_{it-j} + \boldsymbol{\epsilon}_{it}$$

where:
- $\mathbf{Y}_{it} = (y_{it}, d^F_{it}, d^{HH}_{it})$ — log real GDP, firm debt/GDP, household debt/GDP
- $\mathbf{a}_i$ — country fixed effects
- $p=5$ lags (C criterion)
- Debt normalized by **one-year lagged GDP** to avoid capturing GDP innovations in debt equations
- Reduced form: $\mathbf{Y}_{it} = \mathbf{c}_i + \sum^p_{j=1} \boldsymbol{\delta}_j \mathbf{Y}_{it-j} + \mathbf{u}_{it}$

**Identification**: Cholesky decomposition (GDP ordered first → firm debt → household debt)
- Interpretation: Causal ordering reflects policy/market determination
- Robustness: Results robust to alternative orderings (not sensitive to ordering)

**Bias Correction**: Iterative bootstrap procedure for Nickell bias from country FE + lagged dependent variables
- Expected bias small (average T=25 years), confirmed by negligible bias-corrected vs. OLS difference

**Confidence Intervals**: Wild bootstrap (resamples cross-sections of residuals) → accounts for contemporaneous cross-country correlation

### Single-Equation Estimation (Section III.C)

$$\Delta^3 y_{it+3} = \alpha_i + \beta^{HH} \Delta^3 d^{HH}_{it-1} + \beta^F \Delta^3 d^F_{it-1} + \mathbf{X}^r_{it} \boldsymbol{\Gamma} + \epsilon_{it}$$

where:
- LHS: 3-year change in log GDP from time $t$ to $t+3$ (medium-run growth)
- RHS: 3-year change in debt-to-GDP from $t-4$ to $t-1$ (lagged by 1 year for forecaster knowledge)
- $\Delta^3$ = 3-year cumulative change (motivation: VAR impulse response shows household debt shocks persist 3-4 years)
- Controls: $\mathbf{X}^r_{it}$ = lagged GDP growth (3 lags), country FE
- Standard errors: Dually clustered on country and year (accounts for within-country serial correlation + cross-country contemporaneous shocks)

**Why 3-year horizon?**
- VAR impulse response (Figure 1, left panel): household debt shock peaks at year 3, then reverts
- Justification in VAR: First time formally justified in VAR setting (citing King 1994, Jordà et al. 2014a)

### Key Coefficient of Interest
$$\beta^{HH} = \text{Effect on 3-year GDP growth of 1-unit increase in household debt-to-GDP}$$

**Baseline estimate** (Table III, Col. 4): $\hat{\beta}^{HH} = -0.33$ (s.e. = 0.077, p<0.01)

**Magnitude**: One standard deviation increase in ∆³d^{HH} (= 6.2 pp) → **-2.1 pp lower GDP growth** over next 3 years
- Substantial effect (~20% of average GDP growth of 3%)

---

## Main Findings

### Finding 1: Full Dynamic Relation (VAR)

**Impulse Response Analysis** (Figure 1):
1. **Household debt shock response to itself** (left panel): 
 - Initial shock → 3-4 year boom in household debt → peak at year 3
 - Subsequent reversion to initial level by year 5-7
 - Dynamics: Household credit cycle lasts ~7 years peak-to-trough

2. **GDP response to household debt shock** (middle panel):
 - **Years 0-3**: GDP boost (positive elasticity) → temporary expansion during boom
 - **Years 3-6**: GDP contraction (negative effect, labeled "Effect A" in figure)
 - **Years 6-10**: Further GDP decline (labeled "Effect B") → long-run lower level
 - **Focal window**: Year 3-6 (medium-run) = -0.42 log point response
 - Interpretation: Credit-driven consumption boom temporarily raises output; subsequent bust depresses growth

3. **Firm debt shock response** (right panel):
 - **Contrast**: Immediate negative GDP response (no consumption boom phase)
 - Firm debt effect more immediate, smaller, reverts by year 5
 - **Test for distinctness**: Wald test rejects $\beta^{HH} = \beta^F$ (p<0.01)

**Robustness (Jordá Local Projections, Figure 2)**:
- Baseline: Baseline impulse response (top-left) confirms VAR findings
- With time trend: No substantial change to dynamic pattern
- Excluding Great Recession (2006-2012): Boom-bust pattern remains, though long-run level effect disappears
- First differences specification: Similar results; medium-run effect (year 3-6) always negative at 1% level

**Conclusion**: Household debt expansion → temporary output boost → sustained decline in medium-run growth

### Finding 2: Predictability in Single-Equation Framework

**Table III Results** (baseline = Column 4):

| Specification | β^{HH} | β^F | N | R² | Test (β^{HH} = β^F) |
|---|---|---|---|---|---|
| Total private debt | -0.119** | — | 695 | 0.087 | — |
| Household only | **-0.366**|| -0.0978 | 695 | 0.123 | **p=0.003** |
| + lagged GDP | -0.325** | -0.052 | 695 | 0.131 | p=0.007 |
| + gov debt | -0.340** | -0.024 | 695 | 0.128 | p=0.003 |
| + net foreign debt | -0.192* | -0.050 | 636 | 0.168 | p=0.007 |

Key observations:
- **Household debt** coefficient: consistently negative, -0.33 to -0.37 (1% sig)
- **Firm debt** coefficient: near zero, -0.02 to -0.10 (not sig or weakly sig)
- **Test**: β^{HH} ≠ β^F in all cases (p<0.01 in most)
- **Magnitude**: IQR shock (6.2 pp) → 2.1 pp lower growth (standardized effect)

**Cross-country heterogeneity** (Figure A5):
- Coefficient negative for 24/30 countries
- Only Turkey: significantly positive
- Cross-country mean: -0.36; precision-weighted: -0.40

### Finding 3: Interest Rate Spreads & Credit Supply Shocks (Section V)

**Proxy SVAR Analysis** (Tables VI-VII):

**First Stage (Table VI)**: Mortgage-Sovereign Spread as Instrument
- Residualized MS spread → negative coefficient on household debt residuals (-0.341, p<0.05)
- Low MS spread indicator → positive coefficient (0.689, p<0.05)
- F-stat: 11.4 → strong instrument

**Interpretation**: 
- Low interest spreads → increased household borrowing (credit supply effect)
- Contrast with credit demand: demand shock should increase spreads (higher demand for credit)
- Evidence: Low spreads predict debt booms → credit supply shock dominant

**Eurozone & 2000s Boom Case Studies** (Table VII):
- Sovereign spread convergence (1996-1999): Drove household debt surge 2002-2007
- IV estimates: ∆d^{HH} → larger negative GDP growth effect when instrumented by spreads
- Magnitude: 2SLS coefficient = -0.222 to -0.347 (vs. OLS = -0.17), confirming credit supply mechanism

### Finding 4: Forecasting Errors (Table VIII)

**Specification**: 
$$\text{Forecast Error}_{t+h|t} = \alpha + \beta^{HH} \Delta^3 d^{HH}_{it-1} + \gamma^F \Delta^3 d^F_{it-1} + \epsilon$$

where forecast error = (actual GDP − forecast made in year $t$ for year $t+h$)

**Results**:
- **IMF 1-year forecast error**: β^{HH} = -0.060 to -0.31 (p<0.01)
- **OECD 1-year forecast error**: β^{HH} = -0.070 (p<0.01)
- **Firm debt**: no significant forecast error (β^F ≈ 0)

**Interpretation**: 
- Household debt booms predict overoptimistic IMF/OECD growth forecasts
- Forecasters have information on debt growth (observable) but systematically under-weight its medium-run negative implications
- Evidence of biased expectations by professionals (not just households)

### Finding 5: Labor Market Slack (Table X)

**Unemployment Prediction**:
$$\Delta^3 u_{it+3} = \alpha_i + \beta^{HH} \Delta^3 d^{HH}_{it-1} + \beta^F \Delta^3 d^F_{it-1} + \gamma_j \Delta^3 u_{it-j} + \varepsilon$$

**Results** (Column 1):
- β^{HH} = +0.132 (s.e. = 0.038, p<0.01)
- Interpretation: Household debt boom → +1.3 pp unemployment rise over 3 years (per 1-unit debt increase)
- IQR effect (6.2 pp) → +0.82 pp unemployment (substantial)
- Non-linearity: Fixed ER regimes (β^{HH} = 0.264) > intermediate > floating (β^{HH} = -0.016)
- Interpretation: Nominal rigidities amplify unemployment effects in fixed exchange rate regimes

### Finding 6: Global Household Debt Cycle (Section IX)

**Cross-country Spillover Channel**:

$$\Delta^3 y_{it+3} = \alpha + \beta^{global} \Delta^3 \bar{d}^{HH}_{t} + \text{Controls}$$

where $\bar{d}^{HH}_{t} = \sum_i \Delta^3 d^{HH}_{it}$ = global household debt change

**Key Result**:
- Countries with household debt cycles **more correlated with global cycle** experience **sharper GDP declines**
- Mechanism: When many countries simultaneously deleverage, external offset via net exports disappears
- Countries can boost NX when trading partners strong, but not when all deleveraging simultaneously

**Trade Channel**:
- During household debt booms: imports of consumption goods rise (NX declines)
- Countries with high global debt correlation: cannot boost NX → larger growth decline
- Table XII shows global coefficient > individual country coefficients

**Great Recession Prediction**:
- Pre-crisis household debt surge (2000-2006): Large increase in global dHH
- Regression model using pre-2006 data alone: Predicts accurately the 2007-2012 collapse
- "The severity of the Great Recession should not have been surprising given the large increase in global household debt that preceded it"

---

## Heterogeneity & Non-Linearity

### By Exchange Rate Regime (Table IX)

**Fixed ER regimes** (β^{HH} = -0.534**):
- Largest negative effect on growth
- Household debt booms incompatible with zero interest-rate bound

**Intermediate regimes** (β^{HH} = -0.311**):
- Moderate effect
- Some monetary flexibility partially offsets

**Freely floating** (β^{HH} = -0.067):
- Smallest effect (not sig)
- Flexible monetary policy + depreciation can boost exports

**Interpretation**: Nominal rigidities (wage stickiness, ZLB) amplify medium-run recessionary effect

### Non-Linearity (Table IX, Col. 1)

**Positive debt changes**:
- β^{HH,+} = -0.436** (for ∆d^{HH} > 0)
- Strong recessionary effect of debt booms

**Negative debt changes**:
- β^{HH,-} = +0.066 (for ∆d^{HH} ≤ 0)
- **No positive effect** of debt reduction on growth (asymmetry!)
- Interpretation: Consistent with downward wage/interest-rate rigidities (Schmitt-Grohé & Uribe 2016)

### By Developed vs. Emerging Economies (Table IV)

**Developed economies** (β^{HH} = -0.37**):
- Larger household debt effect

**Emerging markets** (β^{HH} = -0.24**):
- Smaller but still significant effect
- Difference marginally significant (p≈0.08)

---

## Robustness

### Specification Checks (Table IV, Panel A)

| Robustness Check | β^{HH} | Note |
|---|---|---|
| Non-overlapping years | -0.32** | Excludes overlapping 3-year windows |
| Arellano-Bond GMM | -0.32** | Addresses Nickell bias directly |
| No country FE | -0.31** | Within-country variation not driving |
| Panel moving blocks bootstrap | -0.33** (t=-4.02) | Conservative SE; sig maintained |
| + Time trend | -0.23** | Reduces est. by 1/3; still sig |
| + Year FE | -0.21** | Over-controlling per authors; still sig |
| Alternative debt normalization | -0.30** | Normalized by initial GDP; robust |

**Conclusion**: Core result stable across specifications; magnitude slightly reduced with time trend/YFE

### Sample Robustness (Table IV, Panel B)

| Period | β^{HH} | Notes |
|---|---|---|
| Developed economies | -0.37** | Larger effect |
| Emerging economies | -0.24** | Smaller but sig |
| Pre-1995 | -0.29** | Before Great Moderation |
| Pre-2006 | -0.22** | Excludes Great Recession |
| Pre-2006 + YFE | -0.16** | Reduced but robust |

**Key takeaway**: Pre-Great Recession data alone shows weaker effect, suggesting debt-growth link partially driven by 2007-2012 experience (but effect present across eras)

---

## 본 paper와의 connection

### Identification & Mechanism Framework
- **Mian et al. (2016)**: VAR + local projections (dynamic, multi-period)
- **Your approach**: 5-year stacked first-difference DID (static/medium-run focus)
- **Overlap**: Both document medium-run (3-6 year) deterioration in outcomes post-shock

### Transmission Channels
- **Mian**: Credit supply (low spreads), forecaster bias, ZLB/nominal rigidities, consumption collapse, trade spillovers
- **Your framework** (PAP § 5): Labor market (unemployment/disability), opioid supply, health insurance, health care access
- **Complementarity**: Mian identifies *where* growth declines; you identify *how mortality increases* (mechanisms diverge)

### Global Dimension
- **Mian Section IX**: Global household debt cycle predicts severity of global recession
- **Your setting**: Likely one-country (Korea) or potentially multi-country (regional trade shocks within EA)
- **Lesson**: If testing global spillovers, check whether Korea's export partners' import demand effects matter (general equilibrium)

### Heterogeneity by Monetary Regime
- **Mian Table IX**: Fixed ER regimes show -0.534 (large), floating show -0.067 (small)
- **Your application**: Korea historically managed float/peg → intermediate regime
- **Implication**: Your effect size should be between Mian's extremes; controllable via ER regime interaction

### Mechanism Decomposition (Mediation Analysis)
- **Mian**: Spread channel (Table VII), forecast error (Table VIII), unemployment (Table X), non-linearity (Table IX)
- **Your § 5.2**: ivmediate + 5-layer SE (health insurance → disability → opioid → death)
- **Difference**: Mian tests channels sequentially; you build causal chain
- **Advantage**: Your causal chain structure more aligned with Pierce-Schott/D-S mediation frameworks

### Credit Supply vs. Demand Identification
- **Mian**: Uses spreads as instrument for credit supply shocks (Proxy SVAR, Table VI)
- **Your design**: Tariff shock likely exogenous to credit conditions (unlike household debt boom)
- **Implication**: Your trade IV naturally isolates supply/demand separation (trade ≠ credit demand per se)

---

## Quality Assessment (Lesson 3개)

### Lesson 1: Dynamic Effects Require Appropriate Time Horizon
**Strength**: Authors justify 3-year window via VAR impulse response analysis, showing household debt shocks persist 3-4 years. This moves beyond arbitrary choice to theory-driven selection.

**Applicability to your work**:
- VAR-justified horizon (3-4 years) vs. your 5-year stacking: slight difference but conceptually similar
- **Recommendation**: Verify 5-year choice against your own data dynamics (e.g., do trade shocks persist 5 years or decay faster in Korea?)
- Strengthens PAP credibility

### Lesson 2: Distinguish Household from Firm Debt Effects
**Strength**: Consistent negative household debt effect (β^{HH} ≈ -0.33), near-zero firm debt effect (β^F ≈ 0). Difference is **economically meaningful** (consumption boom mechanism for HH, no boom for firms) and statistically distinct (Wald tests p<0.01).

**Applicability**:
- Your trade shock likely affects both firm demand (export exposure) and household income (unemployment)
- **Recommendation**: Heterogeneity analysis by firm vs. household impacts could isolate channels
- Validates sectoral heterogeneity in your PAP (manufacturing more exposure than services)

### Lesson 3: Global Spillovers & Trade Channel
**Strength**: Section IX shows global debt synchronization amplifies recessions (countries can't export-led growth when all deleveraging). International trade linkages documented as spillover mechanism.

**Applicability**:
- **Critical for Korea**: As small open economy, global/regional demand shocks likely matter
- **Recommendation**: If regional trade data available, test whether your trade shock effect interacts with trading-partner import demand
- Extends identification from domestic labor market to GE trade channel

---

## 추가 기술 노트

### VAR Lag Selection
- Akaike Information Criterion (C) selects p=5
- Bias correction for dynamic panel (Nickell) via iterative bootstrap
- Minimum expected bias (T≈25 years >> 5 lags)

### Borrowing Constraints Interpretation
- BIS credit data: Total credit from all sources (banks, securities markets, non-bank institutions)
- Broader than bank lending; includes securitization, foreign borrowing
- Limitation: Cannot decompose between constrained vs. unconstrained households (Guerrieri & Lorenzoni 2015 mechanism)

### Monetary Policy Slack Channel
- Non-linearity & ER regime heterogeneity suggest ZLB/nominal rigidity as key amplifier
- References: Eggertsson & Krugman (2012), Korinek & Simsek (2016) on how debt booms amplify when monetary space constrained
- Implication: Korea's monetary autonomy during your sample period matters for effect size

### Consumption Channel Detail
- Table V confirms consumption (all types: nondurable, durable, services) rises during HH debt booms
- Imports of consumption goods rise; domestic production cannot meet demand
- Current account deterioration (NX declines) during boom; exports cannot offset during global bust

---

## Word Count
**2,320 words**

---

## References

Mian, A., Sufi, A., & Verner, E. (2016). Household Debt and Business Cycles Worldwide. *American Economic Review*, 106(7), 1755-1794.

—Key citations:
- Jordà, Schularick, Taylor (2014a, 2014b) — Credit growth & financial crises
- Case & Deaton (2015, 2017) — Deaths of despair (for your mortality connection)
- Schmitt-Grohé & Uribe (2016) — Fixed ER, downward wage rigidity, debt amplification
- Eggertsson & Krugman (2012) — Demand-driven recessions during deleveraging
- Guerrieri & Lorenzoni (2015) — Household borrowing constraints & demand externalities
