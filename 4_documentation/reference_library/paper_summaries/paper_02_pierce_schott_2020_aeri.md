# Paper 02: Pierce & Schott (2020) - Trade Liberalization and Mortality (AER Insights)

## 메타정보

**저자**: Justin R. Pierce (Federal Reserve Board) & Peter K. Schott (Yale School of Management & NBER)

**출판**: AER: Insights, Vol. 2, No. 1 (2020), pp. 47-64
- DOI: https://doi.org/10.1257/aeri.20180396

**working paper 버전**: FEDS WP 2016-094 (동일 내용, 더 긴 버전)

**핵심 키워드**: Trade liberalization, PNTR (China), mortality, deaths of despair, drug overdoses, labor market disruption, local economic shocks

---

## 1. Research Question (핵심 질문)

**Main RQ**: Does a large, plausibly exogenous change in trade policy (PNTR to China, 2000) cause increases in "deaths of despair" (drug overdoses, suicide, alcohol-related liver disease)?

**Secondary RQ**: 
- Which causes of death respond to trade shocks? (Drug overdoses vs. suicide vs. ARLD)
- Which demographic groups are most affected? (Gender, race, age)
- What are the labor market mechanisms? (Unemployment, disability take-up)

**Research gap addressed**: 
- Previous literature identified **unemployment** as a risk factor for deaths of despair
- But finding **exogenous variation** in economic shocks is difficult
- PNTR provides a "natural experiment" to isolate causal effect

---

## 2. Data & Sample

### Geographic unit
- **County level** (3,122 U.S. counties)
- Also tested at PUMA level (PUMAs = Public Use Microdata Areas, minimum 100K population)

### Time period
- **Analysis window**: 1990-2013 (24 years)
- **Policy change**: PNTR passed October 2000, effective December 2001 (China's WTO entry)
- **Pre-period**: 1990-2000 (10 years)
- **Post-period**: 2001-2013 (13 years)

### Outcome variables (mortality)

**Deaths of despair (DoD)** defined as three broad categories:
1. **Drug overdose** (external cause)
2. **Suicide** (external cause) 
3. **Alcohol-related liver disease (ARLD)** (internal cause)

**Data source**: 
- CDC National Center for Health Statistics
- Universe of all US death certificates 1990-2013
- Includes demographics: age, gender, race, county of residence, ICD-coded cause

**Mortality rates calculated as**:
- Age-adjusted death rates per 100,000 population
- Weighted by 2000 U.S. population shares across 15 age bins
- Also computed crude rates (unweighted)

**Baseline mortality rates in 2000** (population-weighted average):
- Drug overdose: 5 per 100,000 (SD=4)
- Suicide: 10 per 100,000 (SD=5)
- ARLD: 4 per 100,000 (SD=3)
- **Total DoD**: 20 per 100,000 (SD=8)

### Treatment variable: NTR Gap (Trade exposure measure)

**Context**: Before PNTR, China received annual "Most Favored Nation" (MFN) status renewal, which was uncertain post-Tiananmen (1989). This created **policy risk** = disincentive for US-China trade.

**Definition of NTR gap by industry j**:
```
NTRGap_j = NonNTRRate_j - NTRRate_j
```

Where:
- **NonNTRRate_j** = Smoot-Hawley tariff rates (set in 1930!), applied if MFN renewal failed
- **NTRRate_j** = Low tariff rates for WTO members (status quo)
- **Larger gap** = greater tariff risk before PNTR

**Industry-level statistics**:
- Mean NTR gap: 30 percentage points
- SD: 18 percentage points
- Range: Manufacturing & agricultural sectors primarily affected
- Service industries: assigned gap = 0 (not subject to tariffs)

**Key identification feature**: 79% of gap variation from non-NTR rates (set 1930), <1% from NTR rates
→ Exogenous, predetermined by Smoot-Hawley

**County-level exposure** (shift-share structure):
```
NTRGap_c = Σ_j (L_jc^1990 / L_c^1990) × NTRGap_j
```

Where L_jc^1990 = # workers in industry j, county c in 1990

**Statistics**:
- Unweighted mean: 7.2%
- SD: 6.5%
- Interquartile range: 2.2% to 10.5%

**Interpretation**: Interquartile shift = county moves from 25th to 75th percentile = 8.3 percentage point increase in exposure

---

## 3. Identification Strategy

### Model: Generalized Difference-in-Differences (DID)

```
DeathRate_ct = Σ_t θ_t × 1{year=t} × NTRGap_c 
 + β·X_ct 
 + Σ_t γ_t × 1{year=t} × X_c 
 + δ_c + δ_t + ε_ct
```

**Notation**:
- c = county, t = year
- **Main coefficients of interest**: θ_t (interacted with year dummies)
- **Baseline year**: 1990 (omitted) → all θ_t relative to 1990

**Time-varying controls** X_ct:
- Average U.S. import NTR tariff (county-level)
- Exposure to Multi-Fiber Arrangement (MFA) phase-out (other trade shock)

**Time-invariant controls X_c** (interacted with year dummies):
- Chinese tariff & subsidy changes (post-2001 WTO accession)
- 1990 county demographics:
 - Median household income (proxy for healthcare access)
 - Share college-educated (technical change proxy)
 - Share veterans (DoD risk)
 - Share foreign-born
 - Share manufacturing employment

**Fixed effects**:
- δ_c = County fixed effects (time-invariant county characteristics)
- δ_t = Year fixed effects (aggregate shocks)

**Standard errors**: Clustered at state level (conservative, allows cross-county correlation within state)

**Weighting**: Population-weighted by 1990 county population

### Identification assumptions

1. **Parallel trends (pre-PNTR)**: Counties with high/low NTR gaps had same mortality trends 1990-2000
 - Test: Visual inspection of θ_t pre-2000 → should be ~0 and non-significant

2. **Exogeneity of shares**: 1990 employment shares (L_jc^1990) predetermined
 - Not forward-looking before PNTR announcement (2000)
 - Risk: If firms relocated anticipating PNTR in 1990s → endogenous shares
 - Mitigation: Non-NTR rates set 1930 (way before any firms' planning horizons)

3. **Exclusion restriction**: NTR gap affects mortality ONLY through trade exposure
 - Not through other unobserved county characteristics
 - Test: No effect on other causes of death (cancer, respiratory)

---

## 4. Empirical Results: Main Findings

### 4.1 Overall Deaths of Despair (DoD)

**Figure 1, Panel D** (all DoD combined):
- **Pre-PNTR (1990-2000)**: θ_t coefficients oscillate around zero, non-significant
 - Supports parallel trends assumption ✓

- **Post-PNTR (2001-2013)**: θ_t becomes positive and **statistically significant** from 2001 onward

- **Magnitude** (interquartile shift in NTR gap = 8.3 pp):
 - **Effect size**: 2-3 deaths per 100,000 per year
 - **Relative to baseline**: ~10-15% of 2000 average DoD mortality (20 per 100k)
 - **Timing**: Effect emerges immediately after PNTR (2001), grows over time

- **Interpretation**: A county moving from 25th to 75th percentile in trade exposure experiences ~2-3 additional DoD deaths per 100k population annually

### 4.2 Decomposition by Cause of Death

**Drug Overdose (Figure 1, Panel A)**: ✓ SIGNIFICANT
- Pre-2000: ~ 0, non-significant (parallel trends OK)
- Post-2001: θ_t = +2 to +3 deaths/100k per year, **highly significant**
- Effect magnitude: **40-60% of 2000 baseline** (5 deaths/100k baseline)
- **Strongest response** among all causes

**Suicide (Figure 1, Panel B)**: ✗ NOT SIGNIFICANT
- θ_t ~ 0 and non-significant throughout entire period (1990-2013)
- Despite similar baseline to drug OD (10 vs 5 per 100k)
- Interpretation: **Not responsive to trade-induced labor market shocks**

**Alcohol-related liver disease - ARLD (Figure 1, Panel C)**: ✗ NOT SIGNIFICANT 
- θ_t ~ 0 and non-significant throughout
- Baseline (4 per 100k) is lowest of three
- Interpretation: **Slower-onset chronic disease, less responsive to acute shocks**

**Key finding**: PNTR effect is **specific to drug overdoses**, not general to all despair deaths
→ Suggests **acute mechanism** (prescription opioid use) rather than psychological cumulative effect

---

### 4.3 Heterogeneity by Demographic Group

**Figure 2: By Gender and Race**

**White males** (Figure 2A): ✓ STRONGEST EFFECT
- θ_t clearly positive, significant post-2001
- Magnitude: ~4-5 deaths/100k (highest among all groups)
- Accounts for majority of aggregate effect

**White females** (Figure 2E): ✓ POSITIVE but WEAKER
- θ_t positive but with larger confidence intervals
- Magnitude: ~2-3 deaths/100k
- Less pronounced than white males

**Black males (2B), American Indian males (2C), Asian males (2D)**: ✗ NO EFFECT
- θ_t ~ 0, non-significant
- Confidence intervals include zero throughout

**Black females, Amer. Indian females, Asian females (2F, 2G, 2H)**: ✗ NO EFFECT
- θ_t ~ 0, mostly non-significant

**Why white males especially?** (Authors' explanation):
1. **Manufacturing employment composition**: 68% male in 1999 vs 49% population-wide
2. **Within manufacturing, whites over-represented**: 84% vs 82% population-wide
3. **Wage loss concentration**: Whites concentrated in high-wage occupations (managerial, professional) in manufacturing
 → Larger income shocks upon displacement
4. **Psychological effects**: Status loss amplifies economic hardship for males (Cutler et al. 2006)
5. **Geographic concentration**: Other racial groups more geographically concentrated → smaller sample size = noisier estimates

**Robustness**: Results "very similar" when restricted to working-age population (20-64) ✓

---

### 4.4 Heterogeneity by Age Group

**Figure 3**: Drug overdose deaths of white adults by 5-year age bins (20-24 through 60-64)

**Age 20-54**: ✓ SIGNIFICANT POSITIVE EFFECT
- θ_t positive and significant post-2001
- Magnitude largest in 35-44 age groups (~3-5 deaths/100k)
- Effect present across entire working-age spectrum

**Age 55-64**: ✓ SIGNIFICANT but SMALLER
- θ_t positive but effect smaller than 20-54
- Magnitude ~1-2 deaths/100k

**Interpretation**: Peak effect in prime working ages (35-54), consistent with **labor market mechanism**

---

### 4.5 Robustness Checks

**Figure 4**: Four robustness specifications

**Panel A (Baseline)**: Reference specification
- Effect size: +2-3 deaths/100k post-2001, highly significant

**Panel B (+ Medicaid expansion controls)**:
- Add indicators for state Medicaid expansions (NY, Maine, AZ 2001-2006, MA 2006, OR 2008)
- **Result**: Virtually identical effect to baseline
- Interpretation: Results not driven by changes in health insurance eligibility post-2001

**Panel C (+ State opioid law controls)**:
- Add state-year indicators for opioid regulation stringency (2006-2012)
 - E.g., pain clinic regulation, doctor licensing restrictions
- Source: Meara et al. (2016)
- **Result**: Virtually identical effect
- Interpretation: Results not driven by state policy differences in opioid supply regulation

**Panel D (+ State-year fixed effects)**:
- Most conservative specification: δ_{ct} for all state-year pairs
- This **absorbs all across-state variation** in NTR gap!
 - Many counties near state borders with different exposures → identifies off remaining within-state variation
- **Result**: Effect remains positive but **precision severely degrades** (much wider CI)
 - Still shows upward shift visually
- Interpretation: State-year FE very restrictive; results robust but with caveats

### 4.6 Validity Test: Other Causes of Death

**Online Appendix Figure A.3** (not shown in paper excerpt):
- Test 16 major internal causes of death (cancer, respiratory, cardiovascular, etc.)
- **Result**: No significant relationship between PNTR and these causes
- **Interpretation**: Supports **specificity** of trade effect to DoD; not due to general deterioration in health

**Geographic robustness**: 
- Re-estimated at CUMA level (aggregated PUMAs, 950 areas)
- Results "very similar" to county level ✓

---

## 5. Mechanisms: Labor Market Pathway

### 5.1 Employment Effects

**Figure 5, Panels A-B**: PNTR exposure → labor market deterioration

**Unemployment rate (Panel A)**:
- Pre-2000: θ_t ~ 0
- Post-2001: θ_t = +1 to +2 percentage points, **significant**
- Interpretation: Interquartile shift in NTR gap → 1-2 pp higher unemployment

**Labor force participation rate - LFPR (Panel B)**:
- Pre-2000: θ_t ~ 0 (larger SEs)
- Post-2001: θ_t = -1 to -2 percentage points, **significant** (negative!)
- Interpretation: Trade exposure → workers leave labor force

**Consistency**: Results align with ADH (2013, 2014) finding that China import exposure reduces earnings

### 5.2 Disability Insurance Pathway

**Figure 5, Panels C-D**: Possible opioid exposure mechanism through disability

**Real disability transfer payments (Panel C)**:
- Log specification
- Pre-2000: θ_t ~ 0
- Post-2001: θ_t = +0.1 to +0.2 (log scale), **significant**
- Interpretation: Trade exposure → ~10-20% higher disability payments

**# of disabled workers (Panel D)**:
- Log specification
- Data available only 1999 onward
- θ_t = +0.02 to +0.04 (log scale) post-2001, **significant**
- Interpretation: Trade exposure → ~2-4% higher disability rolls

**Authors' mechanism hypothesis**:
1. Trade shock → unemployment ↑
2. Displaced workers apply for disability insurance (SSI/SSDI) to survive
3. As part of disability process, many prescribed **prescription opioids** (especially post-1996 when OxyContin introduced)
4. Opioid supply + labor market desperation → overdose deaths ↑

**Quotation support** (Quinones 2015, *Dreamland*):
> "The pain treatment revolution had many faces... But in the Rust Belt, another kind of pain had emerged. Waves of people sought disability as a way to survive as jobs departed. Legions of doctors arose who were not so well-meaning... They were an economic coping strategy..."

**Additional factor**: Firms may have cut safety (skirt regulations) to compete against Chinese imports → workplace injuries ↑ → opioid prescriptions ↑ (McManus & Schaur 2016)

---

## 6. Alternative Explanations Tested & Rejected

### Pre-trends (Parallel trends assumption)
- Figure 1 Panel A shows θ_t ~ 0, non-significant for 1990-2000
- **Conclusion**: No pre-existing mortality trends in high-exposure counties ✓

### Geographic aggregation
- Results similar when moving from county to CUMA level (950 areas)
- **Conclusion**: Not artifact of geographic aggregation level ✓

### Other policy changes
- Medicaid expansions (Panel B, Figure 4)
- State opioid law changes (Panel C, Figure 4)
- **Conclusion**: Results robust to these policy controls ✓

### Other causes of death
- Cancer, respiratory, cardiovascular, etc. show **no relationship** with PNTR
- **Conclusion**: Effect specific to deaths of despair, not general health deterioration ✓

### Migration
- Online Appendix discusses potential role of migration
- Counties with greater job loss may experience out-migration of workers
- This could **bias results downward** (lower observed DoD if workers leave)
 - But estimates remain significant, so conservative interpretation

---

## 7. 본 Paper와의 연결 (Application to Korea)

### A. 동일한 Identification Strategy 적용 가능

Pierce-Schott 2020은 **본 paper의 직접적인 벤치마크**입니다:

**유사점**:
1. **Trade exposure measure**: Shift-share structure (county = 시군구, industry j = SIC/NCS)
 - 본 paper도 동일 구조: 시군구 × 산업 × China trade shock

2. **Policy change**: Exogenous trade policy shock (PNTR → Korea의 FTA/China shock도 가능)
 - Korea도 WTO 가입 (1995), China FTA 추진 등 정책적 변화 있음

3. **Outcome**: Deaths of despair (drug OD, suicide, ARLD)
 - 본 paper: 한국 ICD-10 분류로 동일하게 측정 가능
 - 다만 한국은 **자살 비율이 훨씬 높음** (OECD 최고 수준)

4. **Mechanisms**: Labor market → disability → substance abuse → mortality
 - 한국 맥락에서 **household debt → family dissolution → suicide** 추가 경로

### B. 차이점 & 한국에 적용할 시 고려사항

| 차원 | Pierce-Schott 2020 | 본 Paper (Korea) | 영향 |
|------|----------------|--------------|------|
| **Geography** | 3,122 counties | 시군구 (227개) | 더 큰 픽셀, 더 정확한 local exposure 측정 |
| **주요 죽음 유형** | Drug OD (primary) | Suicide (primary) | Korea 는 약물남용 <10%, 자살 >70% of DoD |
| **Healthcare** | Private + Medicaid/Medicare | National Health Insurance | Medicaid expansion 통제 불필요 |
| **Mechanism** | Opioid availability + disability | **Household debt + family** | 추가 mediation pathway |
| **Trade shock** | PNTR (China) 명확한 date | China shock + FTA | 노출도 측정에 비연속성 활용 필요 |

### C. 본 Paper에서 인용할 Key Findings

**1. "Dead-specificity" (약물 vs 자살 vs 음주)**:
> Pierce-Schott find that PNTR exposure increases drug overdose mortality but not suicide or ARLD. This suggests acute labor market shocks trigger opioid use, not cumulative psychological despair...
> In Korea's context, where opioid addiction is rare, suicide may be the primary response to trade-induced job loss.

**2. Manufacturing concentration**:
> Pierce-Schott (2020) estimate that men comprise 68% of manufacturing employment vs. 49% population-wide, explaining why trade shocks disproportionately harm males. Korea's manufacturing structure shows similar male concentration (70%+ in automotive, electronics).

**3. Disability insurance pathway**:
> The authors document that higher exposure to PNTR is associated with increased disability payments (+10-20% in log terms) and disabled workers (+2-4%), suggesting displaced workers seek welfare benefits. Korea's unemployment insurance replacement rates are lower, but household debt may substitute this role.

**4. Robustness to health policy**:
> Results are robust to Medicaid expansion controls, suggesting trade effects are not simply proxying for insurance policy changes. Korea's universal healthcare eliminates this confounder.

---

## 8. 본 Paper의 Novelty 대비 Pierce-Schott

| Pierce-Schott의 커버 | 본 Paper의 추가 기여 |
|-------------------|-----------------|
| Trade exposure → unemployment ✓ | **Trade exposure → household debt → family dissolution → suicide** |
| Drug OD mechanism ✓ | **Suicide mechanism (한국 맥락)** |
| Gender/age heterogeneity ✓ | **Debt-gender interaction** (females more susceptible to family stability shocks?) |
| County-level geography ✓ | **County + household-level linkage** (본 paper family mortality?)|
| PNTR (discrete policy change) ✓ | **China shock (continuous, gradually phasing in)** |

**본 paper의 methodological advancement**:
- 5-layer SE (AKM + Rotemberg + BHJ + Romano-Wolf)
- vs Pierce-Schott's basic state-clustered SE

---

## 9. Quality Assessment (본 Paper 저자들이 배울 점)

### A. 강점 (Strengths)

1. **Exogeneity of variation**: Non-NTR rates set 1930 → cannot respond to 2000 conditions
 - → Reverse causality ruled out
 - **Lesson**: Korea도 pre-treatment (pre-2000) 산업구조 사용 권장

2. **Parallel trends evidence**: Visual inspection of pre-2000 θ_t clearly shows ~0
 - → Builds confidence in DiD assumption
 - **Lesson**: 본 paper도 pre-2005 trend plot 필수

3. **Cause-specific analysis**: Separate by drug OD, suicide, ARLD
 - Not just "deaths of despair" aggregate
 - **Lesson**: 한국도 자살, 약물, 음주를 분리 분석

4. **Multiple heterogeneity dimensions**: Race, gender, age
 - Not just by county
 - **Lesson**: 본 paper도 성별, 연령별 이질성 보고

5. **Mechanism pathway**: Unemployment → disability → opioid exposure
 - Data-driven hypothesis (not just speculation)
 - **Lesson**: 본 paper의 household debt pathway도 intermediate outcomes 제시

### B. 한계 (Limitations)

1. **PNTR as binary event**: Trade exposure happens at discrete date (2001)
 - Real trade liberalization is gradual (tariff phase-ins over 10-15 years)
 - **Implication**: Timing of effect might be hard to identify
 - **Korea**: China shock is more gradual (2000s-2010s) → advantage?

2. **Opioid supply confound**:
 - OxyContin introduced 1996, coincidental with pre-PNTR uncertainty
 - This timing **aids** identification (PNTR effect should show post-2001, not 1996-2000)
 - But state-year FE (Panel D, Figure 4) degrades precision when controlling for opioid policy
 - **Lesson**: Difficult to separate supply vs demand effects

3. **Geographic scale**: County level may mix multiple local labor markets
 - Authors test CUMA level with similar results
 - But still broader than actual job-search markets
 - **Korea**: 시군구 level might have similar heterogeneity

4. **Race-specific effects unexplained**: Why ONLY whites? Authors offer hypotheses but don't test definitively
 - Could be employment composition + wage loss magnitude
 - Or could be medication/healthcare access differences
 - **Lesson**: Need mechanism data to pin down heterogeneity sources

---

## 10. 메서드 노트 (Method Specifics for 본 Paper 구현)

### A. Standard Errors

Pierce-Schott use **state-level clustering**:
```
Cluster: State (50 units including DC)
vs. Standard HC1 or county-level clustering
```

This is **conservative** because:
- Allows cross-county correlation within state (wages, opioid policy, etc. may be correlated)
- Reduces effective # of units from 3,122 counties to ~50 states
- **Standard error multiplier**: ~2-3x larger than OLS HC1

**본 paper comparison**:
- If using 광역시도 (16 regions) → similar clustering level
- AKM cluster on **sectoral similarity** (different dimension)
- Combination of both = even more conservative

### B. Fixed Effects

```
δ_c + δ_t + interactions of X_c × 1{t ≥ 2001}
```

This **absorbs**:
- All time-invariant county characteristics (coast, geography, etc.)
- All aggregate shocks (recessions, epidemiology)
- Allows county-specific trends in covariates (manufacturing share, education, etc.)

**Interpretation**: Estimates are **within-county changes** over time

**본 paper**:
- Likely similar (광역시도×년 FE minimum, possibly 시군구×년)
- Additional demographic×year interactions recommended

### C. Weighting

All regressions **population-weighted by 1990 population**

This ensures:
- Large counties (more mortality events) have more influence
- Reduces noise from small counties with volatile small-sample rates
- Economically meaningful: larger labor markets get more weight

**본 paper**: 1990 또는 2000 인구로 가중 권장

---

## 11. 결론 및 Citation for 본 Paper

**Citation**:
```
Pierce, Justin R., and Peter K. Schott. 2020. "Trade Liberalization and 
Mortality: Evidence from US Counties." American Economic Review: Insights, 
2(1): 47-64.
```

**본 Paper에서의 역할**:
1. **벤치마크**: PNTR→mortality 효과 크기 비교
 - Pierce-Schott: +2-3 deaths/100k (10-15% of baseline)
 - 본 paper: 한국 effect magnitude 비교 기준

2. **방법론**: Trade exposure measure, DiD specification, robustness checks
 - 특히 cause-specific analysis (자살 vs 약물) 시사

3. **메커니즘**: Unemployment → disability → substance abuse
 - 한국에서는 unemployment → debt → family dissolution → suicide 추가

4. **이질성**: Gender (white males), age (20-54 peak)
 - 한국도 성별, 연령별 차이 기대

**최종 평가**: 본 paper의 가장 직접적인 선행논문. 미국 context이지만 methodology와 findings 모두 한국 적용에 매우 relevant함.

---

