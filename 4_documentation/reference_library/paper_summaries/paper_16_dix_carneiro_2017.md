# [#16] Economic Shocks and Crime: Evidence from the Brazilian Trade Liberalization

## 메타정보
- **저자**: Rafael Dix-Carneiro (Duke University), Rodrigo R. Soares (Columbia University), Gabriel Ulyssea (Pontifical Catholic University, Rio de Janeiro)
- **년도**: 2017 (working paper 23400, dated)
- **출판**: NBER Working Paper No. 23400
- **분류**: Trade liberalization × Crime (homicides)

---

## Research Question

How does trade-induced economic shocks affect violent crime? Can regional variation in tariff reductions from Brazil's 1990s liberalization identify causal effects of labor market conditions on homicide rates? What are the transmission mechanisms (employment, earnings, public goods provision, inequality)?

---

## Data

**Crime Data**:
- Source: DATASUS (Brazilian Department of Informatics), health system records of homicides
- Coverage: All Brazilian micro-regions (minimally comparable areas), 1991-2010
- Unit: Regional homicide rates (deaths per 100,000 population)
- Strength: Health system records (DATASUS) provide consistent coverage across regions/time; homicides more reliably reported than less serious crimes in developing countries

**Trade/Tariff Data**:
- Source: Brazilian tariff schedule, 1991-1995 (liberalization period)
- Coverage: SIC/CNAE industry classifications with tariff rates
- Key metric: Regional Tariff Change (RTC_r) = weighted average tariff reduction by region's sectoral composition

**Labor Market Data**:
- Source: Brazilian Census (1991, 2000, 2010) for employment/earnings
- Unit: Micro-region employment rates, earnings levels
- Coverage: 1991-2000 (medium-run) and 1991-2010 (long-run)

**Other Mechanisms**:
- Public safety personnel: State-level police/security staff
- Inequality: Gini coefficient (regional)
- Education: High school dropout rates
- Age composition of population

**Sample Size**: Micro-regions (smaller geographic aggregates than states), 1991-2010
- Short-run window (1991-2000): 9 years post-liberalization
- Long-run window (1991-2010): Full 19 years

---

## Identification Strategy

### The Trade Shock: Brazil's 1990s Tariff Liberalization

**Context**:
- 1990: Brazil begins trade liberalization; bilateral trade agreements phase in
- 1991-1995: Average tariff reductions of 10-30 percentage points across sectors
- Post-1995: Tariffs remain approximately constant (one-and-for-all shock structure)

**Quasi-experiment**: Regional variation in exposure to tariff cuts based on sectoral specialization

### Instrumental Variable: Regional Tariff Change (RTC)

$$\text{RTC}_r = \sum_j \frac{E^{1991}_{rj}}{E^{1991}_r} \left( \tau^{pre}_{j} - \tau^{post}_{j} \right)$$

where:
- $r$ = micro-region
- $j$ = 4-digit CNAE industry classification
- $E^{1991}_{rj}$ = 1991 employment in industry $j$ within region $r$ (pre-shock)
- $\tau^{pre}_j$, $\tau^{post}_j$ = tariff rates before/after liberalization (pre-1990, post-1995)

**Interpretation**:
- Larger RTC (more negative) = greater tariff reduction exposure = larger labor market shock
- Example: RTC of -0.1 log points (90th to 10th percentile) = 10% tariff reduction

**Exogeneity**:
- 1991 employment shares → pre-determined (shock occurs 1991-1995)
- Regional sectoral specialization in 1991 plausibly unaffected by future tariff policy
- Parallel trends assumption: Crime rate changes unrelated to RTC pre-1990

### Empirical Specification: Dynamic DID with Stacked Periods

$$\log(CR_{r,t}) = \alpha + \theta_t + RTC_r \times \beta_t + \mathbf{X}_r \times \gamma_t + \varepsilon_{r,t}$$

where:
- LHS: Log crime rate in region $r$ at year $t$
- $\theta_t$ = time period effects
- $RTC_r \times \beta_t$ = region-period interaction (heterogeneous treatment effect by time period)
- $\mathbf{X}_r$ = region controls (sectoral composition)
- Stacking: Combine 1991-2000 and 2000-2010 changes; control for state-period fixed effects
- Clustering: Meso-region level (allows spatial correlation across micro-regions)

**Baseline Specification**: 
- Stacked period-pairs (1991-2000, 2000-2010)
- State-period fixed effects
- Region controls for sectoral composition

---

## Main Findings

### Primary Result: Trade Liberalization Increases Crime (Medium-Run)

**Magnitude** (baseline specification):
- Regional Tariff Change of **-0.1 log point** (equivalent to 90th to 10th percentile shift) 
- → Relative increase in crime rate of **0.38 log point** (= **46% increase**)
- Five years after liberalization is complete (1995 → 2000)

**Dynamics**:
- Short-run (1991-2000): Strong, statistically significant effect
- Long-run (1991-2010): Effect vanishes/reverts → Medium-run shock, not permanent

**Robustness**:
- State-period FE specification: Coefficient **increases by >50%** when controlling for state-specific time-varying characteristics
  - Interpretation: Some high-tariff-reduction states had other crime-reducing policies → initial negative bias
  - Corrected estimate: Even larger crime-increasing effect

**Pre-trends**: No significant relationship between RTC and crime changes pre-1990 (validates parallel trends assumption)

### Mechanism: Labor Market Conditions Account for 75-93% of Crime Effect

**Bounds Estimation**:
- Authors construct algebraic upper/lower bounds on effect of employment on crime
- Range: Employment effects account for **75-93%** of total trade-shock effect on crime
- Remaining variation: Other channels (public goods, inequality, etc.)

**Mediation Analysis Framework**:
$$\text{Total Effect} = \text{Direct (Labor Market)} + \text{Indirect (Other Channels)}$$

Lower bound on labor market contribution: 75%
Upper bound: 93%

**Competing Mechanisms (Section 5.2)**:
1. **Public safety personnel** (police): Reduces crime, but cannot fully offset labor market effect
2. **Inequality** (Gini coefficient): Increases crime through wage/employment losses
3. **Public goods provision**: Partially offsets crime-increasing effect
4. **Education** (high school dropouts): Increases with tariff exposure but weak independent crime effect

**Conclusion**: Labor market is dominant channel; other mechanisms matter but smaller

---

## Identification Assumptions & Validation

### Parallel Trends
- Visual inspection (Figure shows pre-1990 relationship between RTC and crime changes ≈ 0)
- Statistically validated: Pre-period coefficients not significant

### Regional Sectoral Composition as Instrument
- 1991 employment shares reflect pre-existing (pre-shock) specialization
- Exogenous to future tariff policy
- Substantial variation across regions (standard deviation in RTC reported)

### Dynamic Specification Justification
- Tariff liberalization: Once-and-for-all event (1991-1995)
- Allows empirical characterization of crime dynamics post-shock
- Can distinguish medium-run (1991-2000) from long-run (1991-2010) effects

---

## Heterogeneity

### Geographic (Region-Level)
- Brazil's micro-regions show heterogeneous responses to tariff shocks
- High variance in both RTC exposure and crime rate changes (visible in Figure 2 distributions)
- Some regions specialize heavily in import-competing sectors → larger employment shock
- Others diversified → smaller crime response

### Temporal
- **Short-run (1991-2000)**: Strongest effect (0.38 log point per -0.1 log point RTC)
- **Long-run (1991-2010)**: Effect attenuates/disappears
- Interpretation: Adjustment friction fades; workers re-allocate out of import-competing sectors

### By Mechanism
- **Employment channel**: 75-93% of total effect
- **Other channels**: Residual 7-25%
  - Public safety (minimal independent effect)
  - Inequality (contributes but secondary)
  - Education (weak independent effect)

---

## Robustness

### Specification Checks
1. **State-period FE**: Coefficient increases >50%; remains significant
2. **Pre-period validity**: Pre-1990 RTC-crime relationship ≈ 0 (validates exogeneity)
3. **Stacking periods**: Combines 1991-2000 and 2000-2010 with state-period FE controls
4. **Clustering**: Meso-region level to account for spatial correlation

### Alternative Mechanisms
- Tested public safety, inequality, education in horse-race specifications
- Employment dominates (Table 7 results)

### Data Quality
- DATASUS homicides: Most reliable crime measure in developing-country context
- Underreporting non-random, but systematic → can measure changes
- Validates focus on homicides as proxy for overall crime

---

## 본 paper와의 connection

### Identification Parallel
- **Your approach**: Sectoral Bartik instrument + lagged exposure (5-year stacked first-difference)
- **D-S approach**: Regional tariff change (RTC) + 1991 employment weighting (stacked 1991-2000 and 2000-2010)
- **Similarity**: Both exploit regional sectoral specialization × exogenous tariff variation for identification
- **Key difference**: You use Bartik shift-share logic; D-S use direct tariff schedule

### Outcome: Mortality vs. Crime
- **D-S**: Homicides (crime outcome)
- **You**: 9 causes of death (mortality outcome)
- **Parallel**: Both reflect labor market stress transmission (though different manifestations)

### Mechanism Framework
- **D-S Section 5.2**: Mediation bounds (labor market 75-93% of total effect)
- **Your PAP § 5.2**: ivmediate/mediation analysis with 5-layer SE
- **Key overlap**: Both decompose total trade effect into labor channel + other channels
- **Your advantage**: Richer mechanism set (health insurance, disability, substance abuse vs. D-S inequality/police)

### Dynamic Specification
- **D-S**: Stacked 1991-2000 vs. 1991-2010 to show medium-run vs. long-run dynamics
- **Your approach**: 5-year stacking to capture medium-run effects (closer to D-S short-run window)
- **Implication**: You should also test long-run (10-15 year) robustness to check persistence

### Heterogeneity Testing
- **D-S**: Mainly regional (implicit through residuals)
- **Your § 7**: Should include heterogeneity by demographics (age, gender) and region analogously

### Causal Ordering
- **D-S**: RTC → Employment → Earnings → (Inequality + Police) → Crime
- **Your hypothesis**: Trade shock → Unemployment → (Disability application + Opioid access) → Deaths of despair
- **Both**: Labor market is causal common cause

---

## Quality Assessment (Lesson 3개)

### Lesson 1: Dynamic Effects & Shock Persistence
**Strength**: By stacking multiple periods (1991-2000, 2000-2010) and allowing separate coefficients, authors show effect is **medium-run, not permanent**. Crime increases post-shock but normalizes after adjustment period (~15 years).

**Applicability to your work**:
- Your 5-year stacking likely captures medium-run effects
- **Recommendation**: Extend analysis to 10-15 year window to test if mortality effects are temporary or persistent (unlike crime, mortality effects may be permanent due to chronic disease/psychological scarring)
- Validates PAP design but suggests need for long-run robustness check

### Lesson 2: Bounds on Mediation (When Direct Mechanism Unobserved)
**Strength**: When employment effects on crime cannot be directly estimated (simultaneity, measurement error), authors construct **algebraic bounds** (75-93% of effect via labor channel). Partially identifies mechanism without perfect data.

**Applicability**:
- For Korea: If you cannot directly observe worker-level displacement from trade, regional employment changes provide lower-bound mechanism effect
- Complements ivmediate approach with semi-parametric bounds
- Reduces reliance on specific functional form assumptions

### Lesson 3: Sectoral Specialization as Identification (Bartik-style IV)
**Strength**: Regional sectoral composition (1991 employment shares) × industry-level tariffs = plausibly exogenous source of variation. Avoids endogeneity from feedback of economic outcomes to policy.

**Applicability**:
- Directly analogous to Borusyak et al. (2025) practical guide on shift-share instruments
- Pre-determined weights (1991) ensure exogeneity
- Validates your use of Bartik shifter; suggests checking that your weights are truly pre-determined (not adjusted for business cycles)
- Documentation: Ensure replication can verify 1991 weights are unchanged by subsequent outcomes

---

## 추가 기술 노트

### Crime Data as Outcome
- Homicides = most reliably measured crime in developing countries (less subject to reporting variation)
- Health system data (DATASUS) provides administrative count (not survey-based)
- Enables long time series (1991-2010) with consistent coding

### Regional Definition
- Micro-regions ≈ minimally comparable areas (analogous to US county analogs)
- Comparability validated across Census waves (1991, 2000, 2010)
- Larger than municipalities; smaller than states

### Stacking Methodology
- Combine 1991-2000 and 2000-2010 period pairs
- Control for state-period FE to absorb state-specific trends
- Standard errors clustered at meso-region to allow spatial correlation

### Bounds on Mediation
- Not full mediation analysis (which requires strong assumptions on error term independence)
- **Conservative approach**: Bounds do not depend on correct functional form or full system specification
- **Trade-off**: Less precise than full mediation analysis but more robust to model misspecification

---

## Word Count
**2,080 words**

---

## References

Dix-Carneiro, R., Soares, R.R., & Ulyssea, G. (2017). Economic Shocks and Crime: Evidence from the Brazilian Trade Liberalization. *NBER Working Paper* No. 23400.

—Key citations embedded:
- Dix-Carneiro & Kovak (2015a, 2015b) — Labor market response to same trade shock
- Soares (2004) — Crime measurement in developing countries
- Fajnzylber et al. (2002), Bourguignon et al. (2003) — Inequality-crime link
- Levitt (1997), Jacob & Lefgren (2003) — Police/public goods → crime
