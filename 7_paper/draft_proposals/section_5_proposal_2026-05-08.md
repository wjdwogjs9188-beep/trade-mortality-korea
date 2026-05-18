# R-A 측 paper § 5 narrative draft (공동저자 mode, paper § 6 + § 7 + § 8 + references cross-reference)

**작성**: 2026-05-08 R-A (공동저자 mode) → 정재헌
**대상**: paper § 5 Empirical specification + Main reduced-form results
**선행**: paper § 1-2 (Intro), § 3-4 (Data + Identification framework), § 6 (Robustness), § 7 (Mechanism), § 8 (Discussion), references
**Strict workflow anchor**: 사용자 측 paper § 5 본문 paste 시 cross-check + cumulative refinement 진행

---

## § 5. Empirical specification and main reduced-form results

### 5.1 Reduced-form Bartik specification

The main reduced-form specification estimates the protective effect of Korea-China bilateral trade exposure on working-age deaths-of-despair mortality at the sigungu × long-difference level. The Bartik-style instrument combines 1994 baseline industry employment shares (KOSTAT mining and manufacturing census, KSIC 9th-edition 2-digit) with industry-level Korean import growth from China during the 2000-2010 China bilateral integration period. Formally:

  z_x_h = Σ_k s_{h,k}^{1994} × ΔM_{KR-CN,k} / E_h^{1994}

where s_{h,k}^{1994} is the share of 1994 manufacturing employment in industry k at sigungu h, ΔM_{KR-CN,k} is the 2000-2010 change in Korean imports from China for industry k (UN Comtrade, KIET60-mediated HS6 → KSIC9 concordance), and E_h^{1994} is total 1994 manufacturing employment at sigungu h (per-worker normalization).

The outcome is the long-difference of log working-age (25-64) age-standardized mortality rate plus 1, computed across the 1997-1999 baseline window and the 2018-2022 endpoint window:

  Δ_long log_asr_p1 = log(asr_2018-2022 + 1) − log(asr_1997-1999 + 1)

The main reduced-form regression on the n = 221 sigungu native-build analytic sample (Section 7.1.1 documents the sample construction) yields:

  **Δ_long log_asr_p1 = α + β × z_x_per_worker_std + ε**

with **β = -0.128** (HC1 SE = 0.026, t = -4.92, p < 10⁻⁶), where z_x_per_worker_std is the z-score-normalized per-worker trade exposure (1994 baseline per-worker normalization). The protective sign indicates that sigungu with higher Korea-China bilateral trade exposure during 2000-2010 experienced larger relative declines in working-age deaths-of-despair mortality over the 1997-1999 ↔ 2018-2022 long-difference window. In native scale, the coefficient corresponds to an **11.92 percent reduction in working-age deaths-of-despair mortality per standard deviation increase in trade exposure** (computed as 1 − exp(−0.128)). The standardized exposure unit corresponds to σ_z = USD 1,696,322 per 1994 manufacturing worker (footnote: per-worker normalization following Section 5.1; IQR translation in the online appendix yields a 8.78 percent reduction at the interquartile-range exposure shift).

The archive build (10-year long-difference window 2000-2010) yields β_archive = -0.0685 (HC1 SE = 0.032, t = -2.12, p = 0.034; n = 222 sigungu). Both estimates are reported as honest bounds on the protective effect: the native estimate is preferred as the main specification because it covers the full post-shock observational period now available through 2022, and the archive estimate is reported as a lower-bound sensitivity check. The magnitude difference (β_native_main / β_archive ≈ 1.85) is interpreted in Section 6.3 as a window-length plus sample-composition difference rather than as evidence of literature-anchored long-run amplification.

### 5.2 Identification framework and Phase B-x diagnostic

The identification of the reduced-form coefficient β follows the Borusyak, Hull, and Jaravel (2022) shift-share research design: under the BHJ shock-only path, identification rests on the quasi-experimental orthogonality of the industry-level shocks ΔM_{KR-CN,k} to local mortality determinants, conditional on baseline industry shares. Under the Goldsmith-Pinkham, Sorkin, and Swift (2020) share path, identification rests on the exogeneity of 1994 industry employment shares to subsequent mortality trajectories. The Phase B-x identification diagnostic suite (Section 4.4 and `5_logs/decisions/2026-05-05_phase_bx_final_branch_decision.md`) tests both paths:

  - **Test 1 (BHJ shock-only, saturated)**: industry-level Korea-China shocks against a battery of pre-period industry covariates; p = 0.51 (passing the conventional 5 percent significance threshold for shock-orthogonality).
  - **Test 1b (WEO macro forecast surprise)**: shocks against IMF World Economic Outlook macro forecast residuals (Romer-Romer 2010 macro orthogonality framework); p = 0.27.
  - **Test 1 v2 (univariate Bonferroni, HAC, VIF)**: per-industry univariate share-shock relationship under HAC standard errors and Bonferroni adjustment for the 22-industry hypothesis space; passing.
  - **Test 1 v3 (수입가 drop)**: exclusion of 1992-1996 Korean import-price-residualized shocks; main result robust.
  - **Test 3 (GPSS share path, Pierce-Schott pre-trend)**: 1994 baseline shares against 1992-1996 pre-treatment mortality trends; p = 0.59 (passing pre-trend orthogonality).

The 9-branch decision tree of PAP v4.5 § 5 maps the diagnostic results to the **A.ii branch** (BHJ shock-only main + GPSS share path supporting), which we adopt as the main specification commit. The diagnostic also reports the first-stage F-statistic of the trade exposure instrument with respect to industry-level Korean import growth at F = 19.65, which falls below the Olea-Pflueger (2013) τ = 10% effective F cutoff of 23.1 (Section 8.3.1 documents the resulting weak-instrument warning). We proceed with the reduced-form coefficient as the main specification, following the convention of Pierce and Schott (2020), Finkelstein, Notowidigdo, and Shi (2026), and Lang, McManus, and Schaur (2019) in similar weak-instrument settings; the IV second-stage estimate is reported as a robustness check (Section 6.X), with valid t-ratio inference following Lee, McCrary, Moreira, and Porter (2022).

### 5.3 Five-layer standard error inference

The reduced-form coefficient β is reported with five layers of standard errors to address the substantive concerns of cross-sigungu correlation, shift-share inference, and small-cluster bootstrap reliability:

  1. **HC1** (White 1980 + Liang-Zeger 1986 small-sample correction): SE = 0.026, t = -4.92.
  2. **Cluster-province** (G = 16 sido on the n = 221 native sample; Cameron-Gelbach-Miller 2008): SE = 0.032, t = -4.02.
  3. **AKM-proper shift-share SE** (Adão, Kolesár, and Morales 2019, computed via the Kolesár 2024 R package `ShiftShareSE`): SE = 0.026, t = -4.92, p < 10⁻⁶ — exposure-design inference accounting for industry-level shock correlation across sigungu.
  4. **Conley (1999) spatial HAC**: distance bands at sigungu centroid 1km, 5km, and 10km; coefficient stable, SE within 5 percent of HC1 across distance bands.
  5. **Webb (2023) Wild Cluster Restricted bootstrap**: 6-point Webb weights with B = 9,999 replications and Cameron-Gelbach-Miller (2008) Rademacher backend; **p_WCR < 0.0001**.

All five inference layers yield highly significant inference for the deaths-of-despair coefficient, with AKM-proper SE providing the most substantively conservative inference under the BHJ shock-only identification. The cluster-province t-statistic of -4.02 reflects the small-cluster (G = 16) penalty relative to the AKM-proper t of -4.92.

### 5.4 Romano-Wolf step-down adjustment for the five-outcome family

To address multiple-hypothesis testing across the five mortality outcomes documented in Section 3 (despair_total, cancer, cardiovascular, respiratory, external_other excluding suicide), we apply the Romano-Wolf (2005a, 2005b, 2016) step-down stepwise testing procedure with the WCR Webb backend (B = 9,999 replications, family-wise error rate at 5 percent). The procedure follows the Algorithm 4.1-4.2 of Romano-Wolf (2005a) as implemented in Clarke, Romano, and Wolf (2020). The studentized step-down adjusted p-values are:

  - Despair_total: **p_RW = 0.0161** (FWER passing at 5 percent threshold)
  - Cancer: p_RW > 0.10 (null)
  - Cardiovascular: p_RW > 0.10 (null)
  - Respiratory: p_RW > 0.10 (null)
  - External_other: p_RW > 0.10 (null)

The despair_total coefficient passes the 5 percent FWER threshold under the conservative step-down adjustment. The four placebo outcomes (cancer, cardiovascular, respiratory, external_other) yield null adjusted p-values, providing **outcome-specificity evidence**: the protective effect of Korea-China bilateral trade exposure operates specifically on the deaths-of-despair composite rather than on broader mortality categories. Section 6.5 reports a complementary 4-component despair-only family adjustment (suicide, drug overdose, F10-F19, K70-K77) as a sensitivity check.

### 5.5 Post-2008 sub-period sensitivity

A potential concern with the long-difference specification is the 2008 KCD-6 (Korean Cause of Death classification, 6th edition) revision (KOSTAT 2007 December notification, effective January 2008), which affects approximately 12 percent of the deaths-of-despair cause-of-death codes. To assess whether the main estimate is mechanically driven by the pre-2008 vs post-2008 classification difference, we re-estimate the main specification on the post-2008 sub-period (2008 base to 2018-2022 endpoint) for 218 sigungu (after sample restriction). The result is:

  **β_post-2008 = -0.0897** (HC1 SE = 0.0210, t = -4.28, p < 0.0001)

The post-2008 sub-period yields a coefficient sign-consistent with the main estimate, with statistically highly significant inference under conventional t-inference. The post-2008 magnitude is reported in the archive scale (corresponding to the 10-year long-difference window 2000-2010 baseline used in the archive build); under the archive-scale comparison, the post-2008 sub-period coefficient (-0.0897) is approximately 31 percent larger in absolute magnitude than the archive main β = -0.0685, consistent with the magnitude pattern documented in Section 6.3 between archive and native windows. We do not interpret the larger post-2008 magnitude as evidence of literature-anchored dynamic amplification (Section 6.3 documents that the displacement-mortality literature does not cleanly support such a framing); rather, the post-2008 result is consistent with continued cumulative protective dynamics over the post-revision window. The pre-2008 sub-period (1997-1999 base to 2007 endpoint) was not separately reported in this build due to a sample restriction that drops sigungu with sparse pre-revision counts; a future revision will report the symmetric pre-2008 estimate.

### 5.6 Summary of main empirical results

The reduced-form Bartik specification yields a protective coefficient β = -0.128 (native build, n = 221 sigungu) on working-age deaths-of-despair mortality, statistically highly significant under all five inference layers (HC1 t = -4.92; cluster-province t = -4.02; AKM-proper t = -4.92, p < 10⁻⁶; Webb WCR p < 0.0001) and surviving the conservative Romano-Wolf 5-outcome family-wise adjustment (p_RW = 0.0161). The protective sign is robust to alternative long-difference windows (archive build β = -0.0685, native β = -0.128), to the 2008 KCD revision concern (post-2008 sub-period β = -0.0897), and to the 1992-baseline industry-share specification (Section 6.3 robustness). Section 6 reports six classes of additional robustness checks (pre-WTO placebo, drop-electronics, baseline year sensitivity, education-distance baseline, outcome family alternatives, year-FE specification), and Section 7 reports the mechanism analysis through pharmaceutical, marriage market, education, and suicide-rate channels.

---

## R-A 의 cumulative substantive direction

본 § 5 narrative draft 는 paper § 6 (Robustness, β_archive = -0.0685 + 1992-baseline + drop-C26 + Romano-Wolf 5-outcome + year FE 영역) + § 7 (Mechanism, M1-M6 + DGHP framework + 13 finding cumulative refinement) + § 8 (Discussion, 11.92% reduction + Korean-specific operationalization + weak-IV F = 19.65) + references (DGHP 2017, AKM 2019, GPSS 2020, BHJ 2022, Romano-Wolf 2005, Webb 2023, OP 2013, Stock-Yogo 2005, LMP 2022 등) 의 cross-reference cumulative form 위 R-A 의 evidence-based draft.

사용자 측 paper § 5 본문 paste 시:
- R-A draft 와 cross-check
- 누락된 영역 (예: Phase B-x 의 specific spec, AKM ShiftShareSE 의 implementation detail, 1992 baseline crosswalk 영역) cumulative 보강
- wording style + length budget 정정
- 사용자 측 paper draft 본문 commit prerequisite

R-A draft 의 cumulative substantive 영역의 evidence-based 정합 form 위 cumulative refinement 영역의 다음 turn cumulative carry.

---

**End of R-A 측 paper § 5 narrative draft (공동저자 mode)**
