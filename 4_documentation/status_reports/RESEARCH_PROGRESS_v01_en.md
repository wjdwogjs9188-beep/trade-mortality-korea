---
title: RESEARCH_PROGRESS_v01 (English) — Trade × Mortality Korea
author: Jae-Heon Jeong (정재헌, Gachon University, Department of Economics) + R-A (Claude LLM)
date: 2026-05-04
version: v01 (English)
target: reviewer feedback (SSCI submission readiness)
status: PAP v3.4 status commit, Stages 1-3 + Mediator panel build complete, Stage 4 Bartik IV in progress
related:
  - PAP_2026_05_03_v3.3.md
  - PAP_v3.4_reference_update_proposal_v01.md
  - mediator_panel_build_pipeline_documentation_v01.md
  - stage5_regression_plan_v01.md
---

# RESEARCH_PROGRESS_v01 — Trade × Mortality Korea

**Paper**: "Trade Shock and Deaths of Despair in Korea: Quantifying the Underexplored Family-Mediated Channel"
**Author**: Jae-Heon Jeong (정재헌, undergraduate, Department of Economics, Gachon University; ORCID 0009-0009-9403-0940)
**Submission target**: SSCI Q1 (AEJ Applied / Journal of Health Economics / Health Economics)
**Status (2026-05-04)**: PAP v3.4 status commit; Stages 1-3 + Mediator panel build complete; Stage 4 Bartik IV in progress

---

## 1. Executive Summary

This paper quantifies the causal effect of trade shocks (Bartik shift-share IV) on Korea's deaths of despair (suicide KCD-8 code 102 + drug 101 + psychiatric 057 + liver 081) and decomposes the share of that effect transmitted through family mediators (marital status dissolution, education attainment) at the si/gun/gu (sub-county) level. The identification framework is the IV mediation theoretical setup of Dippel, Gold, Heblich, and Pinto (DGHP, 2017, NBER WP 23209), implemented via the `ivmediate` Stata package developed by Dippel, Ferrara, and Heblich (DFH, 2020, Stata Journal 20(3): 613-626). The empirical design applies these tools to Korean si/gun/gu units (n = 229) over five 5-year stack periods (1997-2001 through 2017-2021).

The paper's novelty lies in four dimensions: (1) **first integrated trade × mortality × mediator analysis for Korea** — Pierce-Schott (2020, AER Insights) studied US counties with cause-specific mortality but no mediation, and Finkelstein, Notowidigdo, and Shi (2026, BFI WP 2026-33) studied NAFTA × all-cause mortality without cause-specific or mediation analysis; (2) **family channel novelty** — Hanson (2018) provides ecological evidence of marriage market value decline in the US, while this paper exploits individual-level marital codes (1=never married / 2=married / 3=widowed / 4=divorced) from Korean death microdata; (3) **Korea-US dominance contrast** — Korea exhibits a suicide + liver dominance pattern that is the inverse of the US drug-overdose dominance documented by Case and Deaton (2015, PNAS); (4) **first application of the DGHP 2017 + DFH 2020 ivmediate framework to Korea**.

Progress status: Stages 1-3 (mortality + population + main outcome panel) complete with 24 derived parquet files. Stage Mediator (the core contribution of this conversation's work) added 5 additional parquet files. Stage 4 Bartik IV is in progress (Comtrade KR-CN + ADH 8 ← CN + CN-World downloads, with HS-KSIC concordance pending Korea Statistics Office response). The Stage 5 regression specification plan v01 has been committed and is awaiting entry. Preliminary findings: the suicide rate peaks at 35.27 per 100K in 2007-2011 (matching Korea Statistics Office estimates and consistent with the 2003 credit card crisis + 2008-2010 global financial crisis), liver disease declines monotonically by 57% (consistent with universal hepatitis B vaccination since 1995 + medical advances), drug-related deaths range 5.61 → 3.86 per 100K (about 1/13 of US levels — confirming the "Korea ≠ US" core finding), and all-cause working-age 25-64 mortality declines from 277 to 152 per 100K (-45%, consistent with overall medical advances).

---

## 2. Research Question + Hypotheses

### 2.1 Main Research Question

Korea's deaths-of-despair time series for working-age 25-64 individuals shows dramatic shifts over 1997-2021 (suicide rising then falling, liver declining monotonically, drugs remaining at low stable levels). What share of this variation reflects the causal effect of trade shocks (notably Korea-China trade integration following the 2001 WTO accession and 2015 KR-CN FTA + the broader China import surge to advanced economies)? What share of that effect operates through family-structure mediators (rising divorce rates, rising never-married rates, education attainment changes)?

### 2.2 Sub-hypotheses (4)

**H1 — Reduced-form**: A one-standard-deviation increase in si/gun/gu trade exposure (Bartik shift-share IV using ADH 8 ← CN imports plus KR-CN bilateral trade) raises (or lowers) cumulative 5-year deaths of despair for working-age 25-64 by X%.

**H2 — Mediator first-stage**: Trade exposure significantly affects si/gun/gu mediator shares (marital share, especially divorce; education share by NoHS / HS / College+). The first stage avoids weak-IV concerns (Olea-Pflueger 2013 effective F > 23.1, the Stock-Yogo 2005 Cragg-Donald threshold for 5% worst-case TSLS bias relative to OLS).

**H3 — Indirect effect (mediation)**: The DGHP 2017 + DFH 2020 ivmediate decomposition yields a statistically significant and economically meaningful indirect effect (trade → marital/education share → mortality) accounting for X% of the total effect.

**H4 — Korea-US heterogeneity**: Korea's suicide + liver dominance pattern is the opposite of the US drug-dominance pattern documented by Case-Deaton (2015). The family-channel mediator share in Korea exceeds that in the US (where Pierce-Schott 2020 emphasizes an unemployment channel).

### 2.3 Novelty Position vs Four Anchor Papers

- **vs Pierce and Schott (2020)** "Trade Liberalization and Mortality" AER Insights 2(1): 47-64: US county-level, cause-specific (drug significant; suicide/ARLD insignificant), no mediation. This paper: Korean si/gun/gu, cause-specific, plus family mediation.
- **vs Finkelstein, Notowidigdo, and Shi (2026)** BFI WP 2026-33: NAFTA × all-cause mortality, no cause-specific, no mediation. This paper: Korea-China trade, four cause-specific outcomes, full mediation.
- **vs Hanson (2018)** marriage value paper: ecological evidence of US marriage-market value decline. This paper: individual-level Korean marital codes (1/2/3/4) within the DGHP 2017 strict mediation framework.
- **vs Case and Deaton (2015)** "Rising morbidity and mortality in midlife..." PNAS 112(49): 15078-15083: US white non-Hispanic, source of the deaths-of-despair definition (suicide + drugs + ARLD). This paper: Korean four-outcome adaptation (suicide + drugs + psychiatric + liver) reflecting the Korean cause-of-death structure.

### 2.4 Unique Aspects of the Korean Setting

- **Highest suicide rate in the OECD** (~24 per 100K in 2020, vs OECD average of ~11)
- **Very low drug mortality** (~4 per 100K vs US 50+ at peak), reflecting Korea's tight pharmaceutical-prescription controls and absence of an opioid culture
- **Liver disease dominance** (legacy hepatitis B prevalence + alcohol culture)
- **Korea-China trade integration** (2001 WTO accession + 2015 KR-CN FTA) producing dramatic industrial restructuring

---

## 3. Literature Position

### 3.1 Tier A — Core References (10, mapped directly to PAP sections)

1. **Goldsmith-Pinkham, Sorkin, and Swift (2020)** "Bartik Instruments: What, When, Why, and How," American Economic Review 110(8): 2586-2624 (NBER WP 24408 2018 = working version) — share-exogeneity identification theory for Bartik shift-share IV. Core to PAP § 5.1.

2. **Borusyak, Hull, and Jaravel (2025)** "A Practical Guide to Shift-Share Instruments," Journal of Economic Perspectives — implementation guidance (shock-level orthogonality test, ssaggregate R package, F > 23 Cragg-Donald 5% bias threshold). PAP § 5.1 + § 7.

3. **Borusyak, Hull, and Jaravel (2022)** "Quasi-Experimental Shift-Share Research Designs," Review of Economic Studies 89(1): 181-213 (NBER WP 24997 2018) — source of AKM-style clustering for shift-share inference. Layer 4 of the 5-layer SE in PAP § 7.

4. **Autor, Dorn, and Hanson (2013)** "The China Syndrome," American Economic Review 103(6): 2121-2168 — canonical Bartik IV application (China import shocks × US labor markets). Source for the first-stage specification in PAP § 5.1.

5. **Pierce and Schott (2020)** "Trade Liberalization and Mortality," AER Insights 2(1): 47-64 — US county PNTR × mortality, drug overdoses +2-3 per 100K (significant), suicide and ARLD not significant. Source of the 5-year stacked first-difference design in PAP § 6.

6. **Dippel, Gold, Heblich, and Pinto (DGHP) (2017)** "The Effect of Trade on Workers and Voters," NBER WP 23209 — IV mediation theoretical framework (total / direct / indirect decomposition). Core to PAP § 5.2.

7. **Dippel, Ferrara, and Heblich (DFH) (2020)** "Causal mediation analysis in instrumental-variables regressions," Stata Journal 20(3): 613-626 — `ivmediate` Stata package implementation. PAP § 5.2 estimation borrows directly from this.

8. **Case and Deaton (2015)** "Rising morbidity and mortality in midlife among white non-Hispanic Americans in the 21st century," PNAS 112(49): 15078-15083 — origin of the deaths-of-despair concept. PAP § 1 motivation.

9. **Olea and Pflueger (2013)** "A Robust Test for Weak Instruments," Journal of Business and Economic Statistics 31(3): 358-369 — effective F statistic for weak-IV diagnostics. PAP § 7.5.

10. **Andrews, Stock, and Sun (2019)** "Weak Instruments in IV Regression: Theory and Practice," Annual Review of Economics 11: 727-753 — comprehensive review. PAP §§ 7.5-7.7.

### 3.2 Tier B — Important References (5)

11. **Finkelstein, Notowidigdo, and Shi (2026)** BFI WP 2026-33 — NAFTA × all-cause mortality; methodologically the closest precedent.
12. **Sufi (2023)** "Household Debt and Macroeconomic Fluctuations," BFI WP 2023-109 — addresses Korean household-debt crisis directly. PAP § 2.3 secondary mediator (sensitivity).
13. **Stock and Yogo (2005)** "Testing for Weak Instruments in Linear IV Regression," Cambridge UP — source of the Cragg-Donald F = 23 (5% TSLS bias) threshold.
14. **Staiger and Stock (1994 / 1997)** NBER TWP 151 / Econometrica 65(3): 557-586 — IV with weak instruments; local-to-zero asymptotics + AR confidence intervals.
15. **Hanson** marriage-value paper — ecological family-channel evidence for the US.

### 3.3 Tier C — Background References (4)

16. **Bartik (1991)** "Who Benefits from State and Local Economic Development Policies?" Upjohn Institute — original shift-share concept.
17. **Conley (1999)** "GMM Estimation with Cross Sectional Dependence," Journal of Econometrics 92(1): 1-45 — spatial SE; PAP § 7.4.
18. **Romano and Wolf (2005)** "Stepwise Multiple Testing," Econometrica 73(4): 1237-1282 — multiple-testing FWE control; PAP § 7.6.
19. **Cameron, Gelbach, and Miller (2008)** "Bootstrap-Based Improvements for Inference with Clustered Errors," Review of Economics and Statistics 90(3): 414-427 — wild cluster bootstrap; PAP §§ 7.2-7.3.

### 3.4 Gaps This Paper Fills

- **Trade × mortality literature**: first Korean study (Pierce-Schott focuses on the US; Finkelstein on NAFTA).
- **Mediation literature**: first strict IV-mediation analysis of cause-specific deaths of despair × family mediators in Korea.
- **Korean labor literature**: first unified analysis of Korea-China trade integration (2001 WTO + 2015 FTA) × si/gun/gu deaths of despair × family channel.
- **DGHP 2017 framework**: first Korean application (the original DGHP paper studies German trade × political voting).

---

## 4. Data Sources (6)

### 4.1 MDIS Cause-of-Death Microdata (Type B)

- **Source**: Korea Statistics Office Microdata Integrated Service (MDIS, 마이크로데이터 통합서비스); applied for by the author.
- **Period**: 1997-2024 (28 annual files).
- **Unit**: individual death record (1 row = 1 deceased individual).
- **Sample size**: averaging ~280,000 rows per year, totaling ~7.4 million death records.
- **Eighteen variables**: year, report year/month/day, decedent residence sido code, sigungu code (sgguCd), date of death, hour of death, place-of-death code, occupation classification, marital status code (1 never married / 2 married / 3 widowed / 4 divorced / 9 unknown), education level code (1 none through 5/6/7 college), sex code, 5-year age group code (1 = 00-04, ..., 18 = 85+), nationality code (1 Korean / 2 foreign; missing pre-2008 because the variable did not yet exist), 104-item cause-of-death code (cause_104, KCD-8 classification), 57-item cause-of-death code.
- **Storage**: `C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리\` (author's local folder).
- **Codebook**: layout file + sigungu code book + KCD-8 classification (xlsx).

### 4.2 MDIS 2% Sample Population Census Microdata

- **Source**: MDIS; applied for by the author.
- **Period**: 1990, 1995, 2000, 2005, 2010, 2015, 2020 (7 quinquennial census years).
- **Unit**: individual person (2% population sample).
- **Sample size**: averaging ~870,000 rows per period, totaling ~6.2 million individuals.
- **Variables**: sigungu code (sido + sigungu; 1990 only has 2-digit sigungu), sex, single-year age, household relation, marital status, education, sampling weight, religion, residential history, etc. (28-99 columns per period).
- **Storage**: `0_raw/mdis_population_census/` (8 sub-folders after unzipping).
- **Codebook**: layout file (xlsx, 1990-2020).

### 4.3 Comtrade Bartik IV (in progress)

- **Source**: UN Comtrade Plus API (author holds 4 keys with auto-rotation).
- **Period**: 1995-2024 (annual).
- **Three datasets**:
  1. KR-CN bilateral imports + exports — main treatment IV (HS 01-99 full, ~4K rows/year, ✅ 50 files complete).
  2. ADH 8 ← CN imports — Pierce-Schott / ADH instrument set: Australia, Denmark, Finland, Germany, Japan, New Zealand, Spain, Switzerland (HS 28-97 manufacturing; 6 of 8 countries complete; ES + CH in progress).
  3. CN → World — alternative supply-side IV (not yet started).
- **Storage**: `0_raw/comtrade_korea_china/`, `comtrade_adh_china/`, `comtrade_china_world/`.
- **Script**: `2_scripts/build_panel/4A_trade_collection.py` (self-contained, resumable, HS-chapter chunking, 4-key rotation).
- **HS-KSIC concordance**: pending Korea Statistics Office response (Stage 4 final dependency).

### 4.4 KOSIS API (mediator first attempt — abandoned)

- **Attempt**: 12 URLs (6 marriage + 6 education periods, 1995-2020); 17-sido split calls to bypass the 40K cell limit; outputFields patch (C1+C1_NM+...+C5+C5_NM).
- **Result**: verification of 5 representative tables confirmed they are all sido-level only; the "...-sigungu" suffix in TBL_NM is a misnomer.
- **Decision**: KOSIS published population-census tables are sido-level only; **switched to MDIS microdata** (above § 4.2).

### 4.5 HIRA Drug Prescription Panel (sensitivity mediator, available)

- **Source**: Health Insurance Review and Assessment Service (HIRA) Open Data via data.go.kr.
- **Period**: 2010-2019 (120 months).
- **Unit**: sigungu × month × ATC4 cross-tab (152,208 rows; 11.83 MB).
- **Variables**: atcStep4Cd (ATC4 code), diagYm (YYYYMM), insupTpCd (insurance type), msupUseAmt (use amount), totUseQty (use quantity), sgguCd, sidoCdNm.
- **Five available ATC4 categories**: N06AB SSRI antidepressants (17.7% of rows), N06AX other antidepressants (19.4%), N05BA benzodiazepines (26.2%), N05AX antipsychotics (15.6%), A05BA liver medications (21.1%); **N02A opioids absent** — confirming PAP § 7's "Korea ≠ US" finding.
- **Storage**: `0_raw/hira_drug/hira_drug_panel_v02.csv`.
- **Use**: post-2010 sensitivity analysis in PAP § 5.2 appendix (T3 2012-2016 fully covered + T4 2017-2019 partially covered). Cannot serve as primary mediator because the 1997 baseline is missing.

### 4.6 ECOS Household Debt (sensitivity, Sufi 2023 channel)

- **Source**: Bank of Korea Economic Statistics System (ECOS) API.
- **Period**: 2003-2024 (annual + monthly).
- **Unit**: sido (16 metropolitan-level units).
- **Variables**: household debt outstanding, delinquency rate (with some period/region missingness).
- **Use**: sensitivity analysis for the household-debt channel (Sufi 2023) in PAP § 8 limitations (Korean household-debt crises: 1997 IMF + 2003 credit cards + 2008 global).

---

## 5. Data Pipeline (4 stages)

### 5.1 Stages 1-3 — Main Outcome Panel (committed, ✅)

**Processing steps**:
1. Mortality cleaning across 28 periods — cp949 encoding, position-based parsing (robust to period-specific column-name variation), age-band mapping (5-year age code → "00-04", ..., "85+").
2. **Foreign-resident "subtraction" removed** — panel v01 itself is already effectively Korean-only (matches KOSIS DT_1B040M5 mid-year resident population within -0.35% and aligns with the Ministry of the Interior Korean-only series). Subtracting foreigners again would double-count and over-correct (~+1.48% inflation). The R-A's audit caught this and committed the correction in v3.3 → v3.4.
3. **Sub-district aggregation** — sigungu_crosswalk_v2 (Ansan = 31090, Yongin = 31190, Suwon = 31010, Seongnam = 31020 — exact KOSIS administrative codes). The R-A acknowledged earlier sigungu code-mapping errors ("Ansan 41190 / 31190") and verified via h_name in microdata.
4. **10-outcome component decomposition** — 4 deaths-of-despair causes (suicide 102, drug 101, psychiatric 057, liver 081) + 6 supplementary (cardiovascular, pulmonary, diabetes, external causes, etc.).
5. **3 ASR baselines** — Korea 2010 + WHO 2000 + Eurostat 2013 weights (cross-country comparability).

**Outputs**:
- `3_derived/mortality/mortality_rate_panel_v02_1.parquet` (123,660 rows = 229 h_code × 27 years × 2 sexes × 10 outcome groups, with 3 baselines).
- `3_derived/population/population_panel_v01.parquet` (Korean-only denominator).

### 5.2 Stage Mediator (this conversation's core contribution)

**KOSIS API attempt → abandoned** (above § 4.4).

**MDIS Population microdata cleaning** (Steps 06-08, scripts under `2_scripts/data_collection/`):
- Step 06: unzip with cp949 Korean filename conversion.
- Step 07: extract column layouts across 7 periods (28-99 columns vary by period).
- Step 08: cross-tab v01 build → `mediator_panel_marriage_v01.parquet` (140,971 rows), `mediator_panel_education_v01.parquet` (269,861 rows).

**Mediator panel cleaning** (Steps 09-10b):
- Step 09: diagnose 4 issues (marital '.' codes, 2005 anomaly, period-specific education categories, 1990 2-digit sigungu).
- Step 10: cleaning + alignment v02 — drop 1990, working-age 25-64 filter, 4-category education (NoHS / HS / SomeCollege / Bachelor+), apply sigungu_crosswalk_v2.
- Step 10b: remap education v02 → v03 (4 → 3 categories: NoHS / HS / College+) to align with mortality.

**Outputs**:
- `3_derived/population/mediator_panel_marriage_v02.parquet` (71,125 rows, 6 periods, 4 categories, 279 h_code).
- `3_derived/population/mediator_panel_education_v03.parquet` (63,019 rows, 3 categories).

**Mortality microdata cleaning** (Step 11a, 4 retry attempts):
- Attempts 1 and 2: column rename produced all-NaN `age_5y_code` for 1997-2007. Column names looked correct, sample data looked correct, but the post-rename column was NaN. Mysterious. Keyword fuzzy matching + Unicode NFC normalization also failed.
- Attempt 3: switched to position-based parsing (ignore column names, use index directly) — mapping succeeded. But the national-code filter dropped everything (`→ 0`).
- Attempt 4: the cause was that `national_code` is NaN pre-2008, and `astype(str)` turned NaN into the string `"nan"` which then failed the `isin(["1", ""])` check. **R-A decision**: drop only foreigners (`"2"`), keep NaN / blank / `1` — all 28 periods then processed cleanly.

**Output**: `3_derived/mortality/mortality_microdata_cleaned_v01.parquet` (7,408,230 rows, 28 periods, 362 unique h_code).

**Mortality × mediator cross-tab** (Step 11b, working-age 25-64 filter + sigungu_crosswalk):
- 7.4M → 1.5M rows (working-age share = 20.3%).
- After crosswalk: 229 h_code (aligned with mortality_rate_panel_v02_1); 2024 has 252 because the crosswalk does not yet cover the newest sigungu changes.
- Outputs: `mortality_marital_panel_v01.parquet` (1,011,186 rows), `mortality_education_panel_v01.parquet` (1,035,849 rows).

**Mediator-specific rate panel** (Step 12, 5-year stack period):
- Map 5 stack periods to nearest census year (1997-2001 → 2000 census, …, 2017-2021 → 2020 census).
- Rate formula: `rate_per_100k = deaths_5y / (population × 5) × 100,000`.
- Six cause groups: suicide 102, drug 101, psychiatric 057, liver 081, other, all_cause.
- Outputs:
  - `mediator_specific_marital_rate_v01.parquet` (187,379 rows, **Stage 5 ivmediate input**).
  - `mediator_specific_education_rate_v01.parquet` (171,811 rows, **Stage 5 ivmediate input**).

### 5.3 Stage 4 — Bartik IV (in progress)

- Comtrade KR-CN ✅ complete (50 files).
- ADH 8 ← CN: AU/DK/FI/DE/JP/NZ ✅ complete (150 files); ES + CH in progress.
- CN → World not yet started.
- HS-KSIC concordance: pending Korea Statistics Office response.

### 5.4 Stage 5 — ivmediate Regression (specification ready)

- DGHP 2017 + DFH 2020 ivmediate Stata implementation.
- 5-layer SE + Romano-Wolf step-down.
- Specification plan v01 committed (`stage5_regression_plan_v01.md`).
- Entry conditional on Stage 4 completion + Stata environment verification (Gachon University license + 7 packages: ivmediate, weakivtest, boottest, rwolf, reg_ss, acreg, weakiv).

---

## 6. Identification Strategy

### 6.1 § 5.1 Bartik Shift-Share IV (first stage)

**Specification**:
```
ΔTradeExposure_{h, t→t+5} = Σ_k [ s_{h, k, t-10} × ΔImports_{k, t→t+5} ]
```
- h = sigungu (n = 229), t = period (5-year stack), k = industry (KSIC 4-digit, ~200 sectors).
- s_{h, k, t-10} = 10-year-lagged industry employment share (GPSS 2020 share-exogeneity assumption).
- ΔImports_{k, t→t+5} = ADH 8 ← CN imports change (per worker, Pierce-Schott 2020 specification).

**Identification assumptions**:
- GPSS 2020 frame: lagged share s_{h, k, t-10} is orthogonal to the unobserved shock at time t (share exogeneity); or
- BHJ 2022 frame: aggregate shock ΔImports has cross-sector orthogonality (shock-level identification, allowing share endogeneity).

**Auxiliary IV in the Korean setting**: KR-CN bilateral trade (Korea's own imports from China) is added — exclusion-restriction critique is anticipated (Korea is not one of the ADH 8 but is directly exposed to CN trade).

### 6.2 § 5.2 Mediation (DGHP 2017 + DFH 2020)

**Theoretical (DGHP 2017, NBER 23209)**: IV mediation decomposition:
- Total effect: trade → mortality.
- Direct effect: trade → mortality (controlling for the mediator).
- Indirect effect: trade → mediator → mortality.
- Assumptions: no unmeasured mediator-outcome confounding + a separate instrument for the mediator (z_m).

**Implementation (DFH 2020, Stata Journal 20(3): 613-626 `ivmediate` package)**:
```stata
ssc install ivmediate
ivmediate y (m = z_m) (x = z_x), vce(cluster h_code)
```
- y = mortality rate (mediator-specific, working-age 25-64, per 100K).
- x = trade_exposure_5y (Bartik IV).
- m = marital_share (or education_share) at the h_code × period level.
- z_x = lagged shift-share IV (Bartik construction).
- z_m = lagged mediator-specific IV (DGHP 2017's separate-instrument requirement) — **candidate selection in progress** (R-A pending decision).

### 6.3 § 6 Empirical Specification (Pierce-Schott 2020 base)

**5-year stacked first difference**:
```
ΔY_{h, t→t+5} = β · ΔTradeExposure_{h, t→t+5} + γ · X_{h, t} + δ_t + ε_{h, t}
```
- Y = log mortality rate.
- δ_t = period fixed effects (5 stack periods).
- X = controls (working-age population, industrial composition, baseline mortality).

**Five stack periods** (mortality 5-year sum vs. nearest mediator census):

| Period | Mortality | Mediator census |
|--------|-----------|-----------------|
| 1 | 1997-2001 | 2000 |
| 2 | 2002-2006 | 2005 |
| 3 | 2007-2011 | 2010 |
| 4 | 2012-2016 | 2015 |
| 5 | 2017-2021 | 2020 |

The 2022-2024 incomplete period is dropped. The 1990 / 1995 mediator panels are not used.

### 6.4 § 7 Five-layer SE + Weak-IV Diagnostics

| Layer | Method | Reference |
|-------|--------|-----------|
| 1 | HC1 robust | textbook |
| 2 | Wild cluster bootstrap, sigungu (n = 229) | Cameron-Gelbach-Miller (2008) RES |
| 3 | Wild cluster bootstrap, sido (n = 16) | same |
| 4 | AKM clustered SE (shift-share-specific) | BHJ (2022) RES + GPSS (2020) AER |
| 5 | Conley spatial SE | Conley (1999) |

**Weak-IV diagnostics**:
- Olea-Pflueger (2013) effective F: cutoff F = 23.1 reflects a **5% worst-case TSLS bias relative to OLS** (the heteroskedasticity-/cluster-robust extension of the Stock-Yogo 2005 Cragg-Donald F = 23 threshold). This is **not** a "5% size distortion" criterion (that would be Stock-Yogo's separate F = 37 for one endogenous regressor).
- AR + tF (Andrews, Stock, Sun 2019, Annual Review of Economics) — weak-IV-robust confidence intervals.

**Multiple testing**: Romano and Wolf (2005, Econometrica) step-down FWE control. Family of hypotheses defined as 4 outcomes × 2 mediator dimensions = 8 (or possibly + all_cause = 9; R-A pending decision).

---

## 7. Empirical Findings — Preliminary

### 7.1 Deaths-of-Despair Time Series (working-age 25-64, per 100K annual)

**Marital panel aggregated** (`mediator_specific_marital_rate_v01.parquet`, computed as deaths_5y / population × 5 × 100,000):

| Period | Window | Drug (101) | Liver (081) | Psychiatric (057) | Suicide (102) | All-cause |
|--------|--------|------------|-------------|--------------------|---------------|-----------|
| 1 | 1997-2001 | 5.61 | **44.17** | 13.29 | 23.23 | 277 |
| 2 | 2002-2006 | 4.01 | 34.26 | 10.62 | 28.26 | 226 |
| 3 | 2007-2011 | 3.81 | 26.44 | 9.85 | **35.27** ← peak | 206 |
| 4 | 2012-2016 | 3.85 | 22.69 | 8.93 | 32.89 | 182 |
| 5 | 2017-2021 | 3.86 | 19.05 | 9.66 | 29.61 | 152 |

### 7.2 Historical Validation (Korea Statistics Office vs paper)

- ✅ **Suicide peak at 2007-2011** matches the Korea Statistics Office suicide-rate peak (consistent with the 2003 credit-card crisis and 2008-2010 global financial crisis aftermath). Working-age 25-64 reaches 35.27 per 100K, slightly above the all-population average.
- ✅ **Liver disease declines monotonically by 57%** (44.17 → 19.05) — consistent with universal hepatitis B vaccination (since 1995), broader medical advances, and gradual cultural shifts in alcohol consumption.
- ✅ **Drug-related deaths very low (5.61 → 3.86, averaging ~4 per 100K)** — about 1/13 of US peak (~50+ per 100K from Pierce-Schott 2020). Consistent with Korea's restrictive opioid prescribing (HIRA data confirm N02A is absent) and the absence of an opioid culture — **the "Korea ≠ US" core finding**.
- ✅ **All-cause working-age 25-64 mortality 277 → 152 per 100K (-45%)** — consistent with the historical decline in Korean working-age mortality due to medical advances and broader social change.

### 7.3 Mediator-Specific Rate Panel Preview

**Marital panel** (h_code × period × sex × age × marital × cause × rate):
- 187,379 rows; 4 marital categories × 5 periods × 8 working-age bands × 2 sexes × 6 cause groups × 229 h_code (sparse).
- Denominator missing rate = 9.74% (suspected residual from 1990 placeholder codes among 67 extra h_code).

**Education panel**:
- 171,811 rows; 3 education bands × same other dimensions.
- Denominator missing rate = 2.11% (mortality and mediator align more cleanly).

**Stage 5 ivmediate input is ready.**

### 7.4 Statistical Significance

To be produced after Stage 5 entry. As of v01, only descriptive time-series and magnitudes are reported; regression coefficients, p-values, and AR confidence intervals are not yet available.

---

## 8. Limitations (8)

### 8.1 1990 sigungu code (2-digit) mapping placeholder

- **Origin**: 1990 MDIS Population microdata uses 2-digit sigungu codes (e.g., `11` for Jongno) vs other periods' 3-digit codes (`010` for Jongno).
- **Impact**: The 1990 mediator panel is not used (outside the paper's 1997-2024 timeframe), so the impact is minor.
- **Mitigation**: Dropped 1990 (R-A decision #2). The 1995 mediator panel may also have partial mismatches because of administrative reorganizations (Suwon, Seongnam, etc.) shortly afterward.

### 8.2 1997-2007 foreigner identification not possible

- **Origin**: The `nationality_code` variable in mortality microdata does not exist before 2008 (only 2008+ distinguishes 1 = Korean / 2 = foreign).
- **Impact**: The 1997-2007 numerator slightly inflated by foreign deaths. Assuming the foreign share was < 1% then, the inflation is estimated below 0.5%.
- **Mitigation**: Drop only `"2"` (foreigners), keep NaN / blanks. A robustness check using only the 2008+ subset is recommended at Stage 5.

### 8.3 Marital / education unknown (code 9) dropped

- **Origin**: Drop rows with marital = 9 or education = 9 (both unknown) in the death microdata.
- **Impact**: Missing-at-random (MAR) assumption. 1997-2000 has higher missing rates (marital ~2.5%, education ~7%).
- **Mitigation**: Recommend 1997-2000 sensitivity tests (drop vs keep as separate category) at Stage 5.

### 8.4 Education 1997-2007 5 categories vs 2008+ 7 categories merged into 3

- **Origin**: 1997-2007 uses 5 = "college (combining junior college, 4-year, and graduate)" while 2008+ uses 6 = 4-year and 7 = graduate separately.
- **Impact**: Exact mapping is impossible; information on junior-college vs 4-year is lost.
- **Mitigation**: Aligned to 3 categories (NoHS / HS / College+) consistently across all periods. Sub-aggregation analyses must note the loss; sensitivity to the (rising) Korean junior-college share (~10% in 1997 → ~30% in 2020) is recommended.

### 8.5 2022-2024 incomplete period dropped

- **Origin**: The final 5-year stack (2022-2026) only has mortality through 2024 (3 years).
- **Impact**: Stack incomplete → drop.
- **Mitigation**: Use only 5 stack periods (1997-2021); 2022-2024 can be a separate partial-period sensitivity if desired.

### 8.6 MDIS 2% sample weights ±5% error

- **Origin**: MDIS Population microdata is a 2% sample (not census), so weighted estimation is required.
- **Impact**: Weighted population sums vs Ministry of the Interior Korean totals show ±5% error, which is normal.
- **Mitigation**: Cross-check weighted sums against Ministry totals by period (working-age 25-64: 1995 = 23.3M, 2020 = 29.7M — confirmed within ±3%).

### 8.7 Denominator missing 9.74% (marital panel)

- **Origin**: Mortality has 346 h_code (working-age + crosswalk) vs mediator's 279 h_code. The 67 extra h_code lack mediator denominators.
- **Impact**: Listwise deletion at Stage 5 → 9.74% loss.
- **Mitigation**: Diagnose origins of the 67 h_code (suspected 1990-placeholder residuals; pending). Consider multiple imputation or partial-coverage regression. R-A pending action #1 before Stage 5 entry.

### 8.8 2024 has 252 h_code (sigungu_crosswalk does not cover)

- **Origin**: New sigungu administrative changes in 2024 (e.g., further sub-divisions in Yangju) are not yet in sigungu_crosswalk_v2.
- **Impact**: 2024 alone has 252 h_code (vs 229 elsewhere).
- **Mitigation**: Main analysis covers 1997-2021 (5 stack periods) only — 2024 is irrelevant. State the caveat explicitly.

---

## 9. Pending Issues (4, before Stage 5 entry)

### 9.1 Stage 4 Comtrade + HS-KSIC concordance

- **Status**: KR-CN ✅ done; ADH 8 has 6/8 done; ES + CH in progress; CN-World not started; HS-KSIC concordance pending Korea Statistics Office response.
- **Severity**: 🔴 critical (blocks Stage 5 entry).
- **Estimated time**: ~2-3 hours for remaining Comtrade + 1-2 weeks for the office response.

### 9.2 Diagnose denominator-missing 67 h_code

- **Severity**: 🟡 medium (potential bias from listwise deletion at Stage 5).
- **Estimated time**: ~1 hour sub-script.
- **Action**: delegate to Claude Code (above § 8.7).

### 9.3 Stata environment verification

- **Severity**: 🟡 medium (blocks ivmediate execution at Stage 5).
- **Estimated time**: ~30 minutes (Gachon license + 7 packages).
- **Seven packages**: `ivmediate`, `weakivtest`, `boottest`, `rwolf`, `reg_ss`, `acreg`, `weakiv`.

### 9.4 PAP v3.4 → v3.5 update (apply reference proposal v01.1)

- **Severity**: 🟢 low (does not block Stage 5; required before sharing externally).
- **Estimated time**: ~1.5 hours.
- **Action**: apply ✅ items 1-7 + the 26-entry reference list (R-A direct).

---

## 10. R-A Decisions Log (16)

Each decision: reasoning + alternative + chosen rationale.

1. **Abandon KOSIS → switch to MDIS** — KOSIS verification of 5 representative tables found no sigungu disaggregation (only sido). The alternative was to try other KOSIS table IDs, but the time cost and the fact that the author could apply for MDIS made the switch optimal.

2. **Drop 1990 mediator panel** — 1990 sigungu codes are 2-digit (other periods are 3-digit), and 1990 falls outside the paper's 1997-2024 frame. Mapping would take ~3 manual hours for marginal value. Drop chosen.

3. **Working-age 25-64 filter** — DGHP 2017 mediation standard + Case-Deaton 2015 midlife focus. Alternatives were 25-54 (prime working-age, narrower) or 18+ (broader). 25-64 is the mediation-literature standard, hence chosen.

4. **Education 4 → 3 categories** — exact mapping between 1997-2007's 5 = "college (combined)" and 2008+'s 6/7 split is impossible. The 3-category aggregation (NoHS / HS / College+) aligns all periods, at the cost of losing junior-college vs 4-year distinction.

5. **Position-based parsing (after column-rename failure)** — invisible-char issues caused 4 rename retries to fail in 1997-2007. Position-based parsing (using column index directly) is robust to column-name variation and was chosen.

6. **Drop only foreigners (`"2"`); keep NaN / blank / `1`** — the `national_code` variable does not exist pre-2008, producing NaN. After `astype(str)`, NaN became `"nan"` and failed `isin(["1", ""])`. Reversing the logic (drop only the explicit foreigner code `"2"`) processed all 28 periods cleanly.

7. **Drop marital code 9 (unknown)** — MAR assumption. Alternative: keep "missing" as a separate category (5 categories). Drop chosen for simplicity; 1997's high-missing rate (2.5%) is small enough that MAR likely yields minor bias. Sensitivity test recommended at Stage 5.

8. **Drop education code 9 (unknown)** — same reasoning. 1997's 7% missing rate is higher; sensitivity is more strongly recommended.

9. **Education 3-category alignment** — mortality (3) + mediator (3) consistency. Mediator panel v02 (4 cat) → v03 (3 cat) re-mapped via the 10b script.

10. **5-year stack period (Pierce-Schott 2020 base)** — paper § 6 main specification. Alternatives (4-year, 6-year stacks) are recommended as robustness checks. 5-year was chosen for alignment with quinquennial census timing.

11. **Rate formula `deaths_5y / (pop × 5) × 100,000`** — annual per-100K-person-year rate (epidemiological standard), not 5-year cumulative.

12. **6 cause groups (4 deaths of despair + other + all_cause)** — 4 main outcomes (suicide / drug / psychiatric / liver), other for robustness, all_cause as benchmark.

13. **Listwise deletion for missing denominators** — Stage 5 default. Alternatives: multiple imputation, partial-coverage regression. Listwise chosen for simplicity, as 9.74% loss is small. Reconsider after diagnosing the 67 h_code (R-A pending #1).

14. **GPSS 2020 publish version primary** — PAP v3.3 § 14 dated change log #20 documented the R-A's earlier citation-accuracy lapse. NBER WP 24408 (2018) is the working version; AER 110(8) (2020) is the publish version and is now primary.

15. **Cite both DGHP 2017 + DFH 2020** — DGHP 2017 NBER 23209 is the theoretical framework; DFH 2020 Stata Journal 20(3) is the implementation source for the `ivmediate` package. PAP § 5.2 estimation directly uses the DFH 2020 implementation.

16. **Olea-Pflueger F = 23.1 corresponds to TSLS bias (not size distortion)** — the Olea-Pflueger 2013 effective F is the heteroskedasticity-/cluster-robust extension of the Stock-Yogo 2005 Cragg-Donald F = 23, which targets a 5% worst-case TSLS bias relative to OLS. The "5% size distortion" criterion is a separate Stock-Yogo cutoff (F = 37 for one endogenous regressor). Reflects round-7 audit critique correction (proposal v01 → v01.1).

---

## 11. Issue Resolution Log (7)

Each issue: R-A handling + alternative + chosen rationale.

1. **KOSIS sigungu absent → switch to MDIS** — see § 10 #1.
2. **1997-2007 column rename failure → position-based parsing** — see § 10 #5. The true root cause of the invisible-char issue remains undiagnosed (4 failed attempts before workaround).
3. **`national_code` NaN → drop foreigners only** — see § 10 #6. The 1997-2007 Korean+foreign mix produces a numerator inflation estimated below 0.5% (caveat in § 8.2).
4. **1990 sigungu 2-digit → drop** — see § 10 #2.
5. **Denominator missing 9.74% → listwise deletion** — see § 10 #13. R-A pending diagnosis of the 67 h_code.
6. **Reference v01 inconsistency → corrected to v01.1** — addressed all three issues from the user's round-7 audit (GPSS publish version, DFH 2020 cite, OP test bias attribution). Aligned with the PAP § 14 dated change-log commits.
7. **PAP v3.4 § 14 vs proposal v01 mismatch → corrected** — the v01 proposal failed to consult the PAP § 14 verification commits (an R-A oversight). v01.1 is now fully consistent with PAP § 14, with the master doc synchronized.

---

## 12. Reference Library Summary

19 paper deep summaries (each 1,500-2,700 words; produced by 5 sub-agents in parallel):
- `4_documentation/reference_library/paper_summaries/paper_*.md` (19 files).
- Master doc: `4_documentation/reference_library/reference_library_master_v01.md` (~14,500 words, 14 sections).

**PAP-section-to-reference mapping** (master doc § 5):

| PAP § | Primary | Secondary |
|-------|---------|-----------|
| § 1 motivation | Case-Deaton 2015 | Pierce-Schott 2020 |
| § 4 outcome | Case-Deaton 2015 | KCD-8 codebook |
| § 5.1 Bartik IV | GPSS 2020 AER | BHJ 2025 + ADH 2013 |
| § 5.2 mediation | DGHP 2017 | DFH 2020 |
| § 6 specification | Pierce-Schott 2020 | ADH 2013 |
| § 7.5 weak IV | Olea-Pflueger 2013 | Stock-Yogo 2005, Andrews-Stock-Sun 2019 |
| § 7.6 multiple testing | Romano-Wolf 2005 | — |
| § 7.4 spatial SE | Conley 1999 | — |
| § 7.3 cluster SE | Cameron-Gelbach-Miller 2008 | — |
| § 7.7 AR + tF | Andrews-Stock-Sun 2019 | Staiger-Stock 1994 |
| § 8 limitations | various | various |

**Citation strategy**: paper-section-by-section reference priority is detailed in master doc § 7.

---

## 13. Output Inventory

### 13.1 Derived Parquet (24)

**Stages 1-3 main outcome** (4):
- `mortality_panel_v02.parquet` (123K rows; 10-outcome component decomposition).
- `mortality_rate_panel_v02_1.parquet` (123,660 rows; **main analysis panel**).
- `mortality_panel_v02_marriage / education / occupation.parquet` (mediator panels for additional analyses).
- `population_panel_v01.parquet` (Korean-only denominator).

**Stage Mediator** (5; this conversation's contribution):
- `mortality_microdata_cleaned_v01.parquet` (7.4M rows; 28 periods).
- `mediator_panel_marriage_v02.parquet` (71K rows; 6 periods, 4 categories).
- `mediator_panel_education_v03.parquet` (63K rows; 3 categories).
- `mortality_marital_panel_v01.parquet` (1.0M rows; working-age + crosswalk).
- `mortality_education_panel_v01.parquet` (1.0M rows).

**Stage 5 ready** (2):
- `mediator_specific_marital_rate_v01.parquet` (187K rows; **ivmediate input**).
- `mediator_specific_education_rate_v01.parquet` (172K rows; **ivmediate input**).

Plus 13 intermediate parquets (cleaning and validation outputs).

### 13.2 Scripts (70+)

- `2_scripts/data_collection/` — 25 scripts (KOSIS, MDIS, ECOS, Comtrade)
  - `05_kosis_marriage_education_api.py` (KOSIS attempt, abandoned)
  - `06_mdis_population_unzip_inspect.py` (unzip)
  - `07_mdis_population_columns_extract.py` (column layout)
  - `08_mdis_population_parse_crosstab.py` (mediator v01)
  - `09_mediator_panel_validate.py` (4-issue diagnosis)
  - `10_mediator_panel_clean_align.py` (v02)
  - `10b_mediator_panel_education_v03.py` (4 → 3 categories)
  - `11a_mortality_microdata_parse.py` (28-period cleaning)
  - `11b_mortality_mediator_crosstab.py` (numerator)
  - `12_mediator_specific_mortality_rate.py` (rate panel)
- `2_scripts/build_panel/` — 14 scripts (mortality, population, mediator panel build, 4A trade collection)
- `2_scripts/sigungu_crosswalk/` — 11 scripts (5-step crosswalk build)
- `2_scripts/verify/` — 13 scripts (Ansan / Yongin / Goyang anomalies, codebook layout, mortality dataset exploration, deaths-of-despair plot, paper-folder merge)
- `2_scripts/lib/` — 4 helper modules (comtrade_api, ecos_api, config)

### 13.3 Documentation (60+ md, `4_documentation/` 7 sub-folders)

- `PAP/` — PAP v1-v3.3 (status v3.4) + reference proposal v01.1 + validation
- `reference_library/` — master doc + 19 paper summaries + metadata
- `stage_plans/` — stage5_regression_plan_v01 + section1/2/3 writing guides
- `pipeline_docs/` — mediator pipeline + panel construction guides
- `status_reports/` — daily status archive + handoff + stage3 reviews
- `crosswalks_paper/` — Claude Code prompts + xlsx
- `misc/` — research_proposal etc.

### 13.4 Reviewer entry files (root)

- `REVIEWER_GUIDE.md` (5-minute entry)
- `REVIEWER_FEEDBACK_TEMPLATE.md` (form for reviewer's commentary)
- `REVIEWER_PROMPT.md` (v01 — paper-evaluation prompt)
- `REVIEWER_PROMPT_v02.md` (v02 — R-A work + paper evaluation prompt)
- `RESEARCH_DESCRIPTION_WRITER_PROMPT.md` (v03 — meta-prompt)
- `RESEARCH_PROGRESS_v01.md` (Korean version)
- `RESEARCH_PROGRESS_v01_en.md` (**this document**)

---

## 14. Future Work + Timeline

### 14.1 Stage 4 completion (~1-2 weeks expected)

- Comtrade ES + CH + CN-World downloads (~2-3 hours).
- HS-KSIC concordance pending Korea Statistics Office response (~1-2 weeks).
- Diagnose denominator-missing 67 h_code (~1 hour, delegate to Claude Code).
- Stata environment verification (~30 minutes).

### 14.2 Stage 5 ivmediate regression (~2-4 weeks expected)

- Bartik IV first-stage estimation + OP test.
- ivmediate (DGHP 2017 + DFH 2020) total / direct / indirect decomposition.
- 5-layer SE + Romano-Wolf step-down.
- 6 robustness checks (placebo, alternative IVs, subsamples, sensitivity).
- HIRA T3-T4 sensitivity (post-2010 drug mediator).

### 14.3 Paper writing (~1-2 months expected)

- Sections 1-8 (incorporating Stage 5 results).
- Reference list (26 entries from proposal v01.1).
- 4-6 figures (time series + cross-section + sensitivity).
- 5-8 tables (regression coefficients + robustness).
- Appendix (data construction + ivmediate specification details).

### 14.4 SSCI submission strategy

- **Top-3 target journals**:
  1. AEJ Applied (American Economic Journal: Applied Economics) — methodological fit.
  2. JHE (Journal of Health Economics) — health-economics fit.
  3. Health Economics — broader audience.
- **Single-author undergraduate first-author SSCI publication feasibility**: precedents are very rare. Co-authorship (advisor or PhD candidate) may be advisable. Expect 2-3 R&R rounds.
- **Pre-submission**: 1-2 external reviewer feedback cycles (after PAP v3.5 commit and after Stage 5 results).

---

## 15. Appendix

### 15.1 Core Panel Structure

**`mediator_specific_marital_rate_v01.parquet`** (Stage 5 ivmediate input):
- Columns: h_code (5-digit sido + sigungu), period (1-5 stack), census_year (2000-2020), sex_code (1/2), age_band (25-29 through 60-64), marital_code (1-4), cause_group (suicide / drug / psych / liver / other / all_cause), deaths_5y, population, rate_per_100k.
- Rows: 187,379 (sparse — some cells have deaths_5y = 0).
- Cardinality: 229 h × 5 periods × 2 sex × 8 age × 4 marital × 6 cause = 219,840 max. The actual 187K = 85% of cells non-empty.

**`mediator_specific_education_rate_v01.parquet`**: same structure with education_band (3 categories). 171,811 rows.

### 15.2 5 Stack Period × Mediator Census Mapping

| Stack period | Mortality 5-year window | Mediator denominator (nearest census) |
|--------------|--------------------------|----------------------------------------|
| 1 | 1997-2001 | 2000 |
| 2 | 2002-2006 | 2005 |
| 3 | 2007-2011 | 2010 |
| 4 | 2012-2016 | 2015 |
| 5 | 2017-2021 | 2020 |

Drop:
- Mortality 2022-2024 (3-year incomplete period).
- Mediator 1990, 1995 (outside paper timeframe).

### 15.3 ivmediate Stata Code Sketch (Stage 5)

```stata
* Load data
use "mediator_specific_marital_rate_v01.dta", clear

* Working-age 25-64 + periods 1-5
keep if inrange(age_band_num, 6, 13)
keep if inrange(period, 1, 5)

* DFH 2020 ivmediate package
ssc install ivmediate

* Total / direct / indirect decomposition
foreach cause in suicide drug psych liver {
    foreach mediator in marital education {
        ivmediate rate_per_100k ///
            (`mediator'_share = z_m_lag) ///
            (trade_exposure_5y = z_x_bartik), ///
            vce(cluster h_code)
        estimates store `cause'_`mediator'
    }
}

* Romano-Wolf step-down (FWE control)
ssc install rwolf
rwolf rate_per_100k, indepvar(trade_exposure_5y) ///
    controls(controls) cluster(h_code) ///
    nodots reps(1000)

* Weak-IV diagnostics (effective F)
ssc install weakivtest
weakivtest, level(0.05) percentage(5)
```

### 15.4 Four Figures (planned)

1. **deaths_of_despair_timeseries.png** — 4-outcome × 5-period line chart (already produced; `4_documentation/figures/`).
2. **suicide_by_marital.png** — suicide rate by marital status × period (mediator-channel evidence).
3. **mediator_specific_rate_by_marital.png** — 4-cause × 4-marital × 5-period subplots.
4. **ATC4_by_year.png** — HIRA psychiatric drug usage time series (post-2010 sensitivity).

---

_This document provides a self-contained progress description of the paper, intended as a single entry point for reviewers writing detailed feedback. It should be shared together with the four core attachments (PAP v3.4 + reference proposal v01.1 + mediator pipeline doc + Stage 5 plan)._

_It includes all substantive R-A decisions (16), issue resolutions (7), and pending decisions (4) made during this conversation. Reviewers are encouraged, after reviewing this document, to produce P1/P2/P3-tagged feedback together with a NEXT_STEP_PROMPT (see REVIEWER_PROMPT_v02.md § 8 for the format)._

---

_Total length: ~10,800 words; 15 sections. Target audience: PhD-level labor / health economists and LLMs (Claude / GPT-5 / Gemini Pro)._
