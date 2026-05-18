# [#14] Trade Liberalization and Mortality: Evidence from US Counties

## 메타정보
- **저자**: Justin R. Pierce (Federal Reserve Board) & Peter K. Schott (Yale School of Management, NBER)
- **년도**: 2020
- **학술지**: *AER: Insights*, Vol. 2(1), pp. 47-64
- **DOI**: 10.1257/aeri.20180396
- **분류**: Trade policy × Mortality (deaths of despair)

---

## Research Question

How does exogenous trade liberalization affect mortality from "deaths of despair" (drug overdoses, suicide, alcohol-related liver disease)? Can a large, plausibly exogenous economic shock to local labor markets drive increases in fatal outcomes?

---

## Data

**Source & Coverage**:
- Mortality data: CDC National Center for Health Statistics (proprietary microdata from all US death certificates, 1990-2013)
- Population estimates: NCI Surveillance, Epidemiology, and End Results (SEER) Program
- Labor market data: US Bureau of Labor Statistics
- Disability data: Social Security Administration

**Geographic Unit**: US counties (3,122 counties)

**Time Period**: 1990-2013 (sample period), with 1990 baseline for industrial exposure calculation

**Key Outcomes**:
- Age-adjusted mortality rates (per 100,000) by county-year-demographics (age, gender, race)
- Drug overdose deaths (baseline average: 5 per 100,000 in 2000)
- Suicide deaths (average: 10 per 100,000)
- Alcohol-related liver disease (ARLD) deaths (average: 4 per 100,000)
- Deaths of despair combined (average: 20 per 100,000)

**Demographics**: Deaths stratified by gender (M/F) and race (White, Black, American Indian, Asian)

**Sample Size**: 74,924 observations across 3,122 counties; R² = 0.41-0.65

---

## Identification Strategy: PNTR Shock as Quasi-Experiment

### The Trade Policy Change (PNTR)
- **Event**: October 2000 - US Congress granted **Permanent Normal Trade Relations (PNTR)** status to China
- **Pre-PNTR reality**: China's low normal trade relations (NTR) tariff rates required annual Congressional renewal; annual uncertainty created disincentive for US-China trade
- **Post-PNTR reality**: Permanent status eliminates need for renewals; effectively increases import competition from China post-2001 WTO accession

### Causal Instrument: NTR Gap
**Definition**:
$$\text{NTR Gap}_j = \text{NonNTR Rate}_j - \text{NTR Rate}_j$$

where $j$ indexes SIC industry (4-digit), rates from 1999 (Feenstra-Romalis-Schott 2002)

**Interpretation**: 
- Larger NTR gap = greater potential tariff increase faced by industry pre-PNTR = larger trade liberalization post-PNTR
- Mean NTR gap: 30 percentage points; SD: 18 pp; IQR: 2.2 to 10.5 pp

**Why exogenous**:
- 79% of variation in NTR gap due to non-NTR rates set in **1930** (Smoot-Hawley Tariff Act) → predates any post-2000 economic outcomes
- <1% variation due to NTR rates → rules out reverse causality
- No pre-PNTR relationship between NTR gaps and mortality/employment trends (parallel trends assumption validated)

### County-Level Exposure
$$\text{NTR Gap}_c = \sum_j \frac{L^{1990}_{jc}}{L^{1990}_c} \text{NTR Gap}_j$$

Employment-share-weighted average NTR gap of industries active in county $c$ using 1990 employment shares; mean: 7.2%, SD: 6.5%

### Identification Specification: Generalized DID

$$\text{DeathRate}_{ct} = \sum_t \theta_t \mathbf{1}\{year=t\} \times \text{NTR Gap}_c + \beta \mathbf{X}_{ct} + \sum_t \gamma_t \mathbf{1}\{year=t\} \times \mathbf{X}_c + \delta_c + \delta_t + \varepsilon_{ct}$$

where:
- LHS: Age-adjusted death rate (cause-specific) for county $c$, year $t$
- Key terms: $\theta_t$ coefficients capture differential mortality trends by NTR gap before/after policy change
- $\mathbf{X}_{ct}$: time-varying controls (US import tariffs, MFA exposure)
- $\mathbf{X}_c$: time-invariant 1990 county attributes (median income, college share, veteran share, foreign-born share, manufacturing share) + Chinese policy changes (tariffs, subsidies)
- $\delta_c$, $\delta_t$: county and year fixed effects
- Clustering: state level (conservative)
- Weights: population (1990)

---

## Empirical Specification & Estimation

**Specification**: Fully-flexible DID with year-NTR gap interactions
- Full set of year dummies (omitting 1990 as reference)
- Captures time path of PNTR impact from 1991-2013
- Allows testing for pre-trends (1990-2000 should be zero/flat) and post-policy effects (2001-2013)

**Standard Errors**: State-level clustering (allows within-state correlation across counties and cross-county contemporaneous shocks)

**Estimation Method**: OLS with population weighting

**Robustness Checks** (Table 4 / Figure 4):
1. Geographic aggregation: Replicate at CUMA level (PUMA-adjusted, 950 areas)
2. Medicaid expansion controls (2001-2008 expansions in NY, ME, AZ + Romneycare MA 2006 + Oregon 2008)
3. State opioid-law restrictiveness (2006-2012 count of opioid regulatory categories from Meara et al. 2016)
4. State-year fixed effects (very conservative; absorbs much NTR variation)
5. Other causes of death (cancer, respiratory diseases) as placebo tests

---

## Main Findings

### Primary Result: Drug Overdoses Driven by Trade Shock

**Figure 1, Panel A (Drug Overdose)**:
- **Pre-PNTR (1991-2000)**: 95% CI bands centered at zero, flat trajectory → no pre-existing differential trend
- **Post-PNTR (2001-2013)**: Step change up; significant positive effect emerging after 2001
- **Magnitude**: Interquartile shift in NTR gap (8.3 pp) associated with **2-3 additional deaths per 100,000** per year post-PNTR
 - 2000 baseline drug overdose rate: 5 per 100,000 → effect is **40-60% of baseline**
 - Statistically significant at conventional levels

**Other Deaths of Despair** (Figure 1, Panels B-C, D):
- **Suicide**: No significant relationship with PNTR (p-value not significant)
- **ARLD**: No significant relationship with PNTR (p-value not significant)
- **Combined Deaths of Despair**: Statistically significant (driven entirely by drug overdoses)

### Heterogeneity by Demographics

**Figure 2 (Gender × Race)**:
- **White males** (Panel A): Strong positive PNTR effect on drug overdose mortality
- **White females** (Panel E): Positive effect but smaller in magnitude than males
- **Black males** (Panel B), **Black females** (Panel F): No significant effect
- **American Indian** (Panels C, G), **Asian** (Panels D, H): No significant effects (large SEs)

**Explanation for white concentration**:
- Whites = 84% of manufacturing workforce (vs. 82% of general population); overrepresented especially in high-wage occupations (managerial, professional)
- Larger earning losses post-job displacement → greater economic stress
- Psychosocial stress from status loss may amplify mortality impact

### Heterogeneity by Age

**Figure 3 (Working-age population, ages 20-64)**:
- Strongest PNTR effect in ages 20-54 (Panels A-G)
- Weaker effects in 55-64 age groups (Panels H-I)
- Pattern consistent with labor market mechanism (worker displacement from trade shock)

---

## Robustness

**All robustness checks yield similar or slightly larger point estimates**:

1. **CUMA aggregation** (950 larger geographic units): Results very similar to county-level analysis (Figures A.6-A.8, online appendix)
2. **Medicaid expansion controls** (Figure 4, Panel B): Minimal impact on PNTR coefficient
3. **State opioid-law controls** (Figure 4, Panel C): Minimal impact on PNTR coefficient
4. **State-year FE** (Figure 4, Panel D): Upward shift still visible but standard errors inflate; very conservative specification
5. **Other causes of death** (Figure A.3, online appendix): No PNTR relationship with internal causes (cancer, respiratory, etc.) → inconsistent with general health/health-care access channel; supports labor market specificity
6. **Pre-sample balance**: NTR gaps unrelated to 1990 mortality/employment levels (validates exogeneity claim)

---

## Heterogeneity

### By Geography (CUMAs vs. Counties)
- County-level: Point estimates stable
- CUMA-level (larger areas): Results very similar

### By Exchange Rate Regime
- Not explicitly tested in main text but implied by geographic variation

### By Time
- Effects emerge post-2001 (WTO accession deadline)
- Persist through 2013 (unlike cyclical unemployment effects which revert)
- Lag structure: Effect visible immediately post-policy but grows over time (cumulative trauma mechanism?)

---

## Mechanism: Labor Market Deterioration

### Channels Tested

**Labor Market Outcomes** (Figure 5):
1. **Unemployment rate** (Panel A): 
 - IQR NTR gap increase → +1 to +2 percentage point increase in unemployment
 - Effect centered ~zero pre-2000, diverges post-2001

2. **Labor force participation** (Panel B):
 - IQR increase → -1 to -2 pp decline in LFPR
 - Large standard errors; effect less precisely estimated than unemployment

3. **Disability transfer take-up** (Panels C-D):
 - Log disability transfers: +0.1-0.2 log points
 - Log disabled workers: +0.02-0.06 log points
 - Effect post-2000; hampered by data unavailability pre-1999

### Proposed Mechanism Chain
Trade shock → **Unemployment + wage loss** → **Disability application** → **Opioid prescription** (painkillers for disability-related pain) → **Drug overdose death**

**Supporting evidence**:
- Cite Quinones (2015, *Dreamland*): Documentation of opioid pill mills in Rust Belt exploiting disability recipients for "monthly government disability check as solution to unemployment"
- OxyContin introduced 1996 → availability pre-dated PNTR shock, allowing supply to respond to demand shock
- Authors note workers displaced from manufacturing earn 8-12% lower wages when reemployed in other sectors (Ebenstein et al. 2014)
- Psychological stress from status loss (esp. in white male populations) may amplify mortality (Cutler-Deaton-Lleras-Muney 2006)

### Psychosocial Channel
- Job loss among high-tenure workers in high-wage manufacturing → loss of status + income → depression, substance abuse
- White workers face greatest earning losses due to sectoral specialization
- Female effects smaller (less wage loss, less status loss?)

### Alternative Mechanisms Ruled Out
- **General health access**: No effect on non-despair causes of death (cancer, respiratory) → suggests outcome-specific channel, not general health insurance loss
- **Drug supply**: Controlled for state opioid laws (Meara et al. 2016) → small effect on PNTR coefficient; opioid availability likely necessary but not sufficient condition

---

## 본 paper와의 connection

**Your PAP v3.4 mapping**:

### Identification Strategy Parallel
- **Your approach**: 5-year stacked first-difference DID (following Pierce-Schott 2020 exactly)
 - "Section 6. Identification" → directly maps to Pierce-Schott structure
 - County-level analysis with time-invariant instrument → same as PNTR
 - Your IV: sectoral Bartik + lagged exposure (analogous to NTR gap)

### Trade Shock Context
- Pierce-Schott = PNTR 2000 (import shock)
- Your paper = 무역충격 × 사망률 Korea (homemade likely)
- Both use quasi-experimental variation in trade exposure to identify causal effects

### Mortality Outcomes
- P-S: Deaths of despair (OD, suicide, ARLD)
- You: 9종 주요 사망원인 (pending clarification on codes)
- Both emphasize labor market mechanism as transmission

### Key Technical Notes for Your Paper
1. **Clustering**: P-S uses state-level clustering (conservative) → you use county & year dual clustering (more general)
2. **Weighting**: P-S population-weights (standard) → check your approach
3. **Robustness on controls**: P-S includes policy covariates (MFA exposure, Medicaid) → consider analogous Korean policy variables (health insurance reform dates?)
4. **Non-linearity test**: P-S doesn't test, but your § 7 should test asymmetry (trade expansion vs. contraction)

### Five-Year Stacked First-Difference
- P-S doesn't explicitly state 5-year horizon, but uses 3-year changes (∆y_{t+3})
- Your use of 5-year stacking justified by Korean 무역 cycle dynamics

---

## Quality Assessment (Lesson 3개)

### Lesson 1: Causal Identification via Historical Tariff Variation
**Strength**: Using 1930 tariff schedule (Smoot-Hawley) as instrument for 2000+ policy shock is elegant and near-dispositive for exogeneity. 79% of NTR gap variation from pre-determined non-NTR rates eliminates reverse causality.

**Applicability to your work**: Analogy in Korea?
- If your trade IV based on historical sectoral specialization (pre-1990s) + subsequent tariff schedule changes, similar logic applies
- Validates use of Bartik-style shifters with lagged exposure

### Lesson 2: Heterogeneous Treatment Effects by Demographic Groups
**Strength**: Disaggregation by race/gender reveals **concentrated impact on white males** — not mechanical, but economically motivated (manufacturing specialization + status loss sensitivity). Adds credibility to labor market mechanism.

**Applicability**: 
- For Korea: analogous stratification by education level (manufacturing vs. service jobs) or regional concentration (Honam/Yeongnam manufacturing regions) could isolate mechanisms
- Validates PAP § 5.2 heterogeneity framework

### Lesson 3: Careful Control for Confounding Policy Changes
**Strength**: Explicit controls for Medicaid expansions, opioid laws, Chinese policy changes, MFA phase-out → robustness to unobserved concurrent shocks. State-year FE as ultra-conservative check confirms direction (though loses power).

**Applicability**:
- For Korea: 건강보험료 changes, 산업정책 shifts, 최저임금 changes during your sample period → must be controlled
- Validate with state-year (or 도/year) FE as robustness check
- Beware of "absorbing too much variation" trade-off (P-S shows precision loss with state-year FE)

---

## 추가 기술 노트

### Mortality Data Quality
- CDC death certificate microdata provides high-quality cause-of-death coding (ICD-10 compatible)
- Authors note drug overdose deaths have higher scrutiny → less misclassification than other causes
- Age-adjusted rates using 2000 US population standards (enables cross-time comparison)

### Population Weighting Justification
- Small counties have noisier death counts → population weighting reduces influence of outliers
- Justification: policy impact more salient in higher-population areas where economic scale matters

### Parallel Trends Assumption
- Figure 1 (pre-2000) shows flat, zero-centered confidence intervals → visual validation of PT
- Strengthens credibility of post-2000 divergence as causal PNTR effect

---

## Word Count
**2,150 words**

---

## References (for your paper)

Pierce, J.R., & Schott, P.K. (2020). Trade Liberalization and Mortality: Evidence from US Counties. *AER: Insights*, 2(1), 47-64.

—Additional citations embedded:
- Case, A., & Deaton, A. (2015, 2017) — Deaths of despair literature foundation
- Autor, D., Dorn, D., & Hanson, G. (2013) — China import shock labor market effects
- Quinones, S. (2015) — Opioid supply mechanism narrative
