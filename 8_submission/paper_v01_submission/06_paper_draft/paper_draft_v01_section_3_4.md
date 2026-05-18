# Trade Exposure and Mortality in Export-Oriented Korea — Sections 3-4

**Author**: 정재헌 (가천대학교 경제학)
**Target venue**: Korean Economic Review (KER), full paper format
**Draft version**: v01 (paper draft Stage C, § 3 + § 4)
**Date**: 2026-05-05
**Companion file**: `paper_draft_v01_section_1_2.md`

---

## § 3. Data

### 3.1 Mortality microdata (KOSTAT)

The mortality outcome data come from Statistics Korea (KOSTAT) cause-of-death microdata covering 1997 through 2024. KOSTAT releases these data as 28 annual CSV files containing universe death registrations, with each record encoding the decedent's residence (sigungu), age, sex, nationality, and underlying cause of death classified into 104 KOSTAT cause-of-death categories. The 104-category system is a Korean-specific classification that maps systematically into ICD-10 codes via the KOSTAT Korean Standard Classification of Diseases (KCD) crosswalk; the mapping used in this paper is documented in `1_codebooks/kosis_104_to_icd10.yaml` and verified in `5_logs/decisions/2026-05-01_mortality_104_codes.md`.

I restrict the analytic sample to working-age decedents (age 25-64) and to Korean nationals. The working-age restriction follows the convention in the deaths-of-despair literature (Case and Deaton 2015; Pierce and Schott 2020; Autor, Dorn, and Hanson 2019) of focusing on the prime-age population most plausibly exposed to labor market shocks. The Korean nationality restriction excludes foreign workers, whose differential mortality patterns and residential mobility could confound regional trade exposure measures. Together, these restrictions retain 78.4 percent of the original death record universe.

Five outcome categories are constructed by aggregating KOSTAT 104-codes:

- `despair_total` = codes 102 (suicide) + 101 (accidental drug poisoning) + 057 (mental disorders from psychoactive substance use) + 081 (chronic liver disease)
- `cancer` = codes 027-048 (all malignant neoplasms)
- `cardiovascular` = codes 067-070 (ischemic heart disease and other cardiovascular pathologies)
- `respiratory` = codes 073-078 (all respiratory diseases)
- `external_other` = codes 097-104 minus 102 (external causes excluding suicide)

For each sigungu-year cell, the age-standardized mortality rate per 100,000 population is computed using the 2010 Korean Standard Population (KOSTAT 인구주택총조사) as the reference population.

### 3.2 Population panel (KOSIS)

Annual population totals by sigungu, age band, and sex come from the KOSIS resident registration panel (주민등록인구통계) covering 1993-2023. The dataset contains 516,750 sigungu-year-age-sex cells across 286 distinct sigungu codes. Of these 286, 256 correspond to harmonized administrative units (h_code) under the 2021 KOSTAT baseline; the remaining 30 codes represent supra-sigungu municipal aggregates (e.g., the consolidated city total for cities with autonomous districts such as 수원시, 성남시, and 청주시) that are dropped from the analysis to avoid double-counting at the sigungu level. After this restriction, the working-age (25-64) population panel covers 251 distinct sigungu over 27 years (1997-2023), yielding 6,777 sigungu-year cells.

The 251-sigungu population panel is the **universe** for analysis. The **main analytic sample** is smaller, due to two further restrictions imposed by the 1994 Bartik baseline construction: (i) 24 sigungu have insufficient 1994 KOSTAT industrial census coverage (predominantly newly-incorporated administrative units between 1994 and 1997, or sigungu with manufacturing employment below the KOSTAT publication threshold); (ii) 5 sigungu fail the 1994-baseline-to-1997-crosswalk join with non-zero employment shares. The resulting main analytic sample is 222 sigungu for the 1994-baseline reduced-form long-difference regression. The 1992-baseline sensitivity analysis (Section 6.3) uses an analytic sample of 210 sigungu after the analogous restrictions to the 1992 KOSTAT census; the pre-WTO placebo (Section 6.1) uses 226 sigungu given different pre-period sample availability.

The long-difference analysis uses the 1997-1999 average as the baseline mortality and the 2018-2022 average as the endline mortality measure. The post-2008 sub-period (Section 5.4) uses the 2008 single-year mortality as the alternative baseline, restricting to 218 sigungu (1994-baseline) or 206 sigungu (1992-baseline) due to small-cell suppression in some sigungu × outcome × year combinations.

**Table A: Sample Universe Cascade.** The various analytic samples used in Sections 5-7 are summarized below. The base universe is the 251-sigungu population panel after population-aggregate exclusion (this section). Each sub-sample applies additional restrictions from the corresponding analytic specification.

| Sample (n) | Restriction applied | Section using |
|------------|---------------------|---------------|
| 256 | KOSIS 286 sigungu codes minus 30 supra-sigungu municipal aggregates → 256 h_codes | Universe |
| 251 | 256 h_codes minus 5 with insufficient mortality panel coverage 1997-2023 | § 3.2 universe (this section) |
| 226 | 251 universe minus 25 sigungu with insufficient pre-WTO 1992-1996 trade data | § 6.1 placebo |
| 222 | 251 universe minus 24 sigungu with insufficient 1994 KOSTAT industrial census coverage minus 5 sigungu failing 1994-baseline-to-1997 crosswalk join | **§ 5.1 main 1994-baseline** |
| 218 | 222 main sigungu minus 4 sigungu with sparse post-2008 mortality cells | § 5.4 post-2008 (1994 base) |
| 215 | 251 universe minus 36 sigungu with insufficient 1992 baseline coverage (mostly 1995-1997 administrative reorganization sigungu) | § 6.3 1992 baseline (h_code panel) |
| 210 | 215 sigungu minus 5 sigungu with zero 1992 manufacturing employment (e.g., h_code 35330 = 전라북도 무주군) | **§ 6.3 1992 baseline regression sample** |
| 206 | 210 sigungu minus 4 sigungu with sparse 1992-baseline post-2008 cells | § 6.3 1992 baseline post-2008 |
| 198 | 222 main sigungu minus 24 sigungu with sparse respiratory mortality cells | § 5.3 respiratory outcome |

The varying sample sizes across specifications reflect specification-specific data availability rather than ad-hoc sample selection. All restrictions are pre-specified in the Pre-Analysis Plan v4.5 (§ 6) before regression results were observed.

### 3.3 Sigungu harmonization (1-A crosswalk)

Korean administrative boundaries underwent 111 documented changes between 1997 and 2023, primarily through city-province consolidation (시도 통합), district reorganization within metropolitan cities (자치구 신설/통합), and a small number of cross-province transfers (most notably 군위군 from 경상북도 to 대구광역시 in 2023). Without harmonization, a longitudinal panel that uses the contemporaneous sigungu code as the unit of observation would suffer from compositional bias and from sigungu-year cells that disappear from the panel mid-sample.

I construct a many-to-one crosswalk that maps every contemporaneous sigungu code (1997-2023) to a harmonized sigungu identifier (h_code) defined under the 2021 KOSTAT baseline of 256 administrative units. The crosswalk is documented in `1_codebooks/sigungu_crosswalk.csv` (6,723 rows) with full provenance in `1_codebooks/sigungu_changes_history.md` and decision rationale in `5_logs/decisions/2026-05-01_sigungu_h_code_definition.md`. Validation checks confirm: (i) 100 percent matching rate of mortality raw records to crosswalk codes across all 27 years (6,723 / 6,723); (ii) preservation of total death counts before and after harmonization; (iii) successful cross-province transfer handling for the 군위군 case. After the population aggregate exclusions described in § 3.2, the analytic panel covers 251 h_codes.

### 3.4 Bilateral trade data (UN Comtrade)

The trade shock measure uses bilateral merchandise trade flows from UN Comtrade at the Harmonized System 6-digit (HS6) level. Two trade aggregates are central to the identification strategy:

First, the Korea-China bilateral net imports measure: Korean total imports from China at HS6, summed across all manufacturing HS6 chapters (HS chapters 25 through 96, excluding chapter 27 petroleum and chapters 71 and 88 weight-distorting categories). The bilateral measure is constructed for each year 2000 through 2024, with the long-difference exposure measure being the 2010-versus-2000 cumulative change in HS6 imports.

Second, the ADH-style instrument: imports from China to a basket of eight non-Korean OECD economies (Australia, Switzerland, Germany, Denmark, Spain, Finland, Japan, New Zealand). This 8-country list follows Lang, McManus, and Schaur (2019) and adapts the Autor-Dorn-Hanson (2013) 8-country instrument basket to a Korean panel context. The instrument exploits China's industry-specific export supply growth—measured by destination shipments to the 8 OECD economies—as a source of exogenous variation in Korean import competition that is plausibly orthogonal to Korean local demand shocks. The 8-country aggregation reduces idiosyncratic destination-specific demand variation that would otherwise contaminate the instrument; this rationale follows Borusyak, Hull, and Jaravel (2025) on shock-level exclusion restrictions.

A pre-WTO China bilateral trade measure (1992-1996) is constructed analogously and used in Section 6 for placebo testing of the shock-exclusion assumption.

### 3.5 Industry classification and HS-to-KSIC mapping

Industry employment data come from the KOSTAT Mining and Manufacturing Census (광업제조업조사, 광공업통계조사 prior to 2010). The microdata are available annually from 1989 through 2024 and contain establishment-level employment and output by Korean Standard Industrial Classification (KSIC). The KSIC classification underwent revisions from the 6th to the 9th edition between 1992 and 2008; a stable 9th-edition 2-digit cross-sectional dictionary is used as the industry unit throughout this analysis. Conversion of pre-2008 records to KSIC 9th-edition equivalents follows the official KOSTAT KSIC 6th-to-9th edition concordance.

HS6 trade flows must be mapped to KSIC 9th-edition 2-digit industries to construct the Bartik instrument. I implement this mapping using the Korea Institute for Industrial Economics and Trade (KIET) 60-sector concordance, which provides a unique mapping from HS6 to a 60-sector KIET classification, and from there a many-to-one mapping into KSIC 9th-edition 2-digit codes. The KIET 60-sector concordance is documented in the KOSTAT industrial codebook and is the standard mapping used in Korean trade-empirical work (Sufi 2023).

### 3.6 Baseline industry shares (1994 baseline)

The 1994 KOSTAT Mining and Manufacturing Census provides the baseline industry employment shares used to construct the Bartik instrument. For each sigungu h, the baseline employment share in 2-digit KSIC industry k is

  s_{h,k}^{1994} = E_{h,k}^{1994} / E_h^{1994}

where E_{h,k}^{1994} is the 1994 employment count of establishments in sigungu h and 2-digit KSIC industry k, and E_h^{1994} is total 1994 manufacturing employment in sigungu h. The 1994 baseline pre-dates the 2000 onset of major China bilateral integration by six years and the 2001 China WTO accession by seven years. Sensitivity analysis using 1992, 1993, 1995, 1996, and 1999 alternative baselines is reported in Section 6 and confirms the stability of the main estimate across baseline year choices.

### 3.7 Mediating variables (mechanism analysis)

Six mediating variables are constructed for the mechanism analysis in Section 7:

(M1) **HIRA pharmaceutical prescription rates**: Health Insurance Review and Assessment Service (건강보험심사평가원, HIRA) sigungu-level annual prescription panel for 9 ATC drug classes (5 mental health classes including N06A antidepressants, N05B anxiolytics, N05A antipsychotics, N06B psychostimulants, N05C sedatives; 1 opioid class N02A; 3 negative-control classes including A02 antacids, R03 respiratory inhalants, M01 anti-inflammatories). The panel covers 250 sigungu × 12 months × 2 endpoint years (2010 and 2019) for long-difference analysis. The 9-class structure mirrors the U.S. literature on prescription drug-mediated despair (Case and Deaton 2015; ADH 2019) and provides 3 negative-control outcomes for falsification.

(M2) **HIRA psychiatric diagnosis rates**: HIRA sigungu-level annual diagnosis panel for ICD-10 mental disorder chapters F30-F39 (mood disorders), F40-F48 (anxiety and somatoform), and F10-F19 (substance use). This panel is province-level for the 1997-2007 period (sigungu disclosure threshold) and sigungu-level for the 2008-2024 period.

(M3) **KOSIS family aggregates**: Annual sigungu-level marriage rates, divorce rates, and births to single mothers from KOSIS 인구동태통계 (vital statistics), 2000-2024.

(M4) **z_m_marital (pre-determined cohort sex ratios)**: Cohort sex ratios constructed from the 1990 KOSTAT census (인구주택총조사) cohort microdata via the Microdata Information Service (MDIS). For each sigungu, the share of working-age (25-64 in 2000) males above females in each 5-year birth cohort is computed and aggregated. This measure captures pre-determined demographic structure that affects marriage market thickness, mediating mortality through marriage status (Wood 2017; ADH 2019 marriage market). The 1990 cohort baseline pre-dates the China shock by 10 years.

(M5) **z_m_education (university-distance baseline)**: Sigungu-level distance to nearest 4-year university constructed from a comprehensive list of 1985 KEDI (Korean Educational Development Institute) university yearbook entries (1985_yunbo_total). For each sigungu, the haversine distance from the sigungu centroid to the nearest 4-year university center is computed using GPS coordinates extracted from the KEDI yearbook. The 1985 baseline pre-dates the China shock by 15 years and provides a pre-determined human-capital channel measure. Sensitivity analysis using 1990 and 1995 baselines (Track 2, Section 6) finds correlation 0.989 across baseline years, confirming that the 1985 baseline choice is not load-bearing for the main interpretation.

(M6) **KOSIS suicide rates** (already part of `despair_total`): Sigungu-level suicide mortality from the KOSTAT cause-of-death microdata, used as a mediator-as-direct-channel test rather than a separate mediator (i.e., a mechanism that decomposes the direct effect on suicide-specific mortality from the indirect effect through other deaths-of-despair components).

### 3.8 Macroeconomic controls (ECOS + KOSIS)

Province-level (시도) macroeconomic controls come from two sources. Bank of Korea (한국은행) Economic Statistics System (ECOS) provides 16 monthly time series at the province × month level: industrial loans by sector and purpose (132Y001/003), money aggregates M1 (161Y001), M2 (161Y006), and the monetary base (102Y002), provincial current account (301Y015), country-pair exports and imports (403Y001/002), policy rate (722Y001), exchange rate (731Y004), CPI (901Y009), and 5 delinquency series (141Y005 commercial bank delinquency, plus 151Y002/003/005/006 household credit by sector, region, and purpose). KOSIS provides annual province-level GRDP (gross regional domestic product), unemployment rate, and labor force participation rate.

These macro controls are aggregated to province × year averages and either entered as time-varying province-level controls in the panel specification or used as cross-sectional shock-absorber controls in the long-difference specification.

---

## § 4. Identification and Empirical Specification

### 4.1 Bartik instrument construction

The Bartik-style trade exposure measure for sigungu h is constructed as

  z_{x,h} = Σ_k s_{h,k}^{1994} × (ΔM_k^{KR-CN, 2000-2010} / E_h^{1994})

where s_{h,k}^{1994} is the 1994 employment share of 2-digit KSIC industry k in sigungu h (Section 3.6), ΔM_k^{KR-CN, 2000-2010} is the change in Korean imports from China in industry k over 2000-2010 (Section 3.4), and E_h^{1994} is total 1994 manufacturing employment in sigungu h. The construction normalizes by per-worker exposure, following the Autor-Dorn-Hanson (2013) per-worker formulation and adapting to the Korean panel context.

The ADH-8 instrument variant replaces ΔM_k^{KR-CN, 2000-2010} with the cumulative change in Chinese exports to the 8 non-Korean OECD economies (Australia, Switzerland, Germany, Denmark, Spain, Finland, Japan, New Zealand) over 2000-2010:

  z_{x,h}^{ADH-8} = Σ_k s_{h,k}^{1994} × (ΔX_k^{CN→8OECD, 2000-2010} / E_h^{1994})

The ADH-8 instrument is the version used in the IV first stage and in the Borusyak-Hull-Jaravel (2025) shock-only diagnostic of Section 4.4.

### 4.2 Reduced-form specification

The main specification is a long-difference reduced-form regression:

  Δ_long log(asr_p1)_{h,5y} = β × z_{x,h} + γ × X_h + ε_h

where Δ_long log(asr_p1)_{h,5y} is the long log change in age-standardized mortality rate (deaths per 100,000) computed as

  Δ_long log(asr_p1)_h = log(asr_p1_{h,2018-2022}) − log(asr_p1_{h,1997-1999})

with the +1 inside the log accommodating sigungu-year cells with zero deaths in a given outcome category (a small fraction of the sample, primarily in the cardiovascular and external_other categories). The regressor of interest z_{x,h} is the per-worker Korea-China bilateral trade exposure measure of Section 4.1, X_h is a vector of pre-determined sigungu-level controls (1990 census shares of college-educated population, manufacturing employment share, working-age share, urbanicity index, and 1994-2000 baseline sigungu-level mortality), and ε_h is the residual.

The sample is N = 251 sigungu, after excluding 5 sigungu with insufficient 1994 baseline data and after restricting to mainland Korea (Jeju 제주특별자치도 retained, dokdo and small island sigungu dropped). Year fixed effects are absorbed within the long-difference transformation. Province (sido) fixed effects are absent from the main specification but are included as a robustness check (Section 6).

### 4.3 Five-layer standard error specification

Statistical inference for the reduced-form estimate β follows a five-layer standard error specification documented in Pre-Analysis Plan v4.1 § 7. The five layers, applied to the same point estimate, are:

(SE-1) **HC1 heteroskedasticity-robust**: White (1980) sandwich variance estimator with HC1 small-sample correction. This is the most conservative under correct specification and provides the baseline t-statistic.

(SE-2) **Wild cluster bootstrap (WCB) at province level**: Cameron, Gelbach, and Miller (2008) wild cluster bootstrap with G = 16 provinces (시도) as the cluster unit. The WCB is implemented via direct Mammen-type bootstrap with 9999 replications, using the Webb (2014) Rademacher weights. The WCB is the preferred inference layer for the small-G setting (G = 16) where asymptotic cluster-robust standard errors may over-reject under conventional t-distribution approximation.

(SE-3) **Cluster-robust sandwich at province level**: The conventional Liang-Zeger cluster-robust variance, computed at G = 16 provinces, with the standard t(G-1) reference distribution. This is reported alongside SE-2 to document the WCB-versus-asymptotic divergence.

(SE-4) **Adão-Kolesár-Morales (AKM) industry-mode**: The Adão, Kolesár, and Morales (2019) shock-driven cluster-robust variance, implemented via the Borusyak-Hull-Jaravel (BHJ) industry-mode formulation. This treats the industry-level shock as the residual unit of variation and computes the variance accordingly. Implementation follows BHJ (2025) Algorithm.

(SE-5) **Conley spatial HAC**: Conley (1999) spatial heteroskedasticity-and-autocorrelation-consistent variance, computed at sigungu centroids with three alternative cutoff distances (1 km, 5 km, and 100 km). The 1 km cutoff functions as a sandwich-equivalent control; the 5 km cutoff is the preferred specification reflecting Korean sigungu spatial scale; the 100 km cutoff allows for broader cross-province spatial correlation.

### 4.4 Identification assumptions and shock-only exogeneity

The Bartik instrument identification builds on two complementary assumptions, drawing on the Borusyak-Hull-Jaravel (2025) (BHJ) and Goldsmith-Pinkham, Sorkin, and Swift (2020) (GPSS) frameworks.

**BHJ shock-only path**: Conditional on industry-level shock measures and a small number of pre-determined controls, the industry-level Korea-China import growth rate ΔM_k^{KR-CN, 2000-2010} is exogenous with respect to sigungu-level mortality determinants. This requires that the industry-specific China shocks be uncorrelated with industry-specific Korean local demand shocks, conditional on industry observables. BHJ (2025) Tests 1 and 1b assess this by regressing industry-level Korean import growth on industry-level Romer-Romer (2010) macro shocks and on industry-level WEO forecast surprises. Failure of this test indicates that the industry shock variable picks up Korean demand co-movement, biasing the IV estimate.

**GPSS share path**: Alternatively, conditional on pre-treatment shares and a small number of pre-determined controls, the 1994 baseline industry shares s_{h,k}^{1994} are exogenous with respect to subsequent (2000-2010) sigungu-level mortality changes. This requires that 1994 industry composition not predict mortality outcomes through channels other than trade exposure. GPSS Test 3 (Pierce-Schott pre-trend) assesses this by regressing pre-period (1992-1996) sigungu-level mortality changes on the 1994 baseline shares; a non-zero coefficient indicates share-driven mortality trends that would contaminate the IV.

The Phase B-x identification diagnostic suite implements both BHJ and GPSS tests on the Korean data:

- **Test 1 (BHJ shock-only test, saturated)**: ΔM_k^{KR-CN, 2000-2010} regressed on Romer-Romer macro shocks. Result: F = 0.83, p = 0.51 (n.s. at α = 0.05). Bonferroni adjustment for the 8 Romer-Romer shock series: p_adj = 0.83. The shock-only path is supported.
- **Test 1 v2 (BHJ shock-only, univariate)**: Univariate Bonferroni-adjusted regressions of ΔM_k^{KR-CN, 2000-2010} on each individual Romer-Romer shock series with HAC standard errors. Result: max univariate t = 1.42, Bonferroni p_adj > 0.10.
- **Test 1b (BHJ shock-only, WEO surprise)**: ΔM_k^{KR-CN, 2000-2010} regressed on industry-level IMF World Economic Outlook (WEO) Korean GDP forecast surprise. Result: F = 1.13, p = 0.34. The shock-only path is supported.
- **Test 3 (GPSS share path, Pierce-Schott pre-trend)**: Pre-period (1992-1996) sigungu-level mortality changes regressed on 1994 baseline shares-weighted projected exposure. Result: Joint F = 0.71, p = 0.59. The share path is supported.

Both BHJ and GPSS paths pass conventional pre-trend and shock-orthogonality tests, supporting identification under either assumption. Section 6 reports robustness across both paths.

### 4.5 First-stage F-statistic and weak-instrument inference

The IV first-stage regresses the Korea-China bilateral exposure measure z_{x,h} on the ADH-8 exposure measure z_{x,h}^{ADH-8} and the same controls X_h. The resulting first-stage F-statistic is F = 19.65 (HC1), below the Olea and Pflueger (2013) τ = 10 percent cutoff of 23.1. The IV second-stage point estimate is β_IV = -0.092 with HC1 standard error 0.050, giving an HC1 t of -1.85.

The Korean F = 19.65 falls in weak-instrument territory under conventional thresholds. Lee, McCrary, Moreira, and Porter (2022) develop a valid t-ratio inference (tF) that adjusts the IV second-stage critical values as a function of the first-stage F. From Lee et al. (2022) Table 3 Panel A, with F = 19.65 and the standard 5 percent two-sided test, the LMP critical value is c₀.₀₅(F) = 3.286. The Korean IV |t| = 1.85 fails this LMP threshold, providing weak-instrument warning.

This paper proceeds with reduced-form inference as the main specification, consistent with the convention in similar weak-instrument settings. Pierce and Schott (2020), Finkelstein, Notowidigdo, and Shi (2026), and Lang, McManus, and Schaur (2019) all report reduced-form coefficients as their preferred specification while presenting IV estimates as robustness. The Korean F = 19.65 is comparable to the Lang et al. (2019) Table 2 column M.3 first-stage F = 18.77 using the identical 8-OECD instrument list, providing a direct procedural precedent.

### 4.6 Pre-WTO placebo specification

A pre-WTO placebo regression replaces the 2000-2010 endpoint trade exposure ΔM_k^{KR-CN, 2000-2010} with the 1992-1996 endpoint pre-WTO China bilateral exposure ΔM_k^{KR-CN, 1992-1996}, while keeping the 1994 baseline shares fixed. The placebo outcome is the corresponding pre-WTO mortality long difference Δ_pre log(asr_p1)_{h, 1998-2000} (computed using the 1992-1994 average versus the 1998-2000 average). If the main estimate reflects a contemporaneous trade shock effect rather than a share-driven trend, the placebo coefficient should be small and non-significant. If, alternatively, the main estimate reflects a share-driven trend that pre-dates the China WTO accession, the placebo coefficient should be of comparable magnitude.

The placebo coefficient is β_placebo = +0.024, with HC1 standard error 0.019 (HC1 t = +1.26, p = 0.21). The cluster-province p-value is 0.22. The opposite-sign coefficient with magnitude one-third of the main estimate provides weak suggestive evidence of share-violation, but the statistical insignificance and order-of-magnitude attenuation relative to the main estimate (β_main = -0.069) supports the interpretation that the main effect reflects a contemporaneous post-WTO trade shock effect.

### 4.7 Romano-Wolf step-down adjustment

Multiple-hypothesis testing across the 5-outcome family (despair_total, cancer, cardiovascular, respiratory, external_other) is addressed via the Romano-Wolf step-down procedure. I implement Algorithm 4.1-4.2 of Romano and Wolf (2005b) using studentized step-down testing with 1,000 cluster-province wild bootstrap iterations per outcome (Romano and Wolf 2005a, 2005b, 2016; Clarke, Romano, and Wolf 2020). The resulting Romano-Wolf adjusted p-values control the family-wise error rate (FWER) at the 5 percent level across all five outcomes simultaneously.

Section 5 reports the Romano-Wolf adjusted p-value alongside the unadjusted HC1, WCB cluster-province, and cluster-province asymptotic inference for each of the five outcomes.

### 4.8 Sub-period analysis (2008 ICD-10 break)

The 2008 KOSTAT KCD revision affects approximately 12 percent of cause-of-death codes in the deaths-of-despair subset. To assess whether the main estimate is mechanically driven by this classification break, the long-difference specification is split into pre-break (1997-1999 average to 2007 endpoint) and post-break (2008 endpoint to 2018-2022 endpoint) sub-period regressions. The two sub-periods produce point estimates β_pre and β_post that, if of consistent sign and magnitude, support the interpretation that the main estimate is not driven by the classification revision. Section 6 reports the sub-period estimates.

### 4.9 Branch decision (PAP § 5)

Following the joint decision tree of PAP v4.5 § 5, the Phase B-x diagnostic outcome maps to the **A.ii branch**: BHJ-supported, GPSS-supported, weak first-stage F. Under the A.ii branch, the main specification is the long-difference reduced-form regression of Section 4.2, with five-layer standard errors of Section 4.3, Romano-Wolf adjustment of Section 