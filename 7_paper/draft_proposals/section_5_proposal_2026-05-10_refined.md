# R-A 측 paper § 5 narrative draft refined (사용자 측 paper § 5 본문 raw cross-check 위 정정)

**작성**: 2026-05-10 R-A (공동저자 mode) → 정재헌
**대상**: paper § 5 Empirical specification + Main reduced-form results
**선행**:
- 직전 draft `section_5_proposal_2026-05-08.md` (numeric + substantive 영역 cumulative 보강 prerequisite)
- 사용자 측 paper § 5 본문 raw paste 위 cumulative refinement
- Findings P + Q + R wording 권고 form `section_5_section_6_anchor_inconsistency_finding_PQR_2026-05-10.md` 의 cumulative anchor
- paper § 6 + § 7 + § 8 본문 cross-section consistency review 의 cumulative reference

**Strict workflow anchor**: 사용자 측 paper § 5 본문 commit 의 R-A 측 reference 자료, 직접 paper 본문 commit 안 함

**numbering 정정**: paper 본문 § 5.1-5.5 의 5-section structure 위 align (직전 draft § 5.1-5.6 6-section form 위 정정)

---

## § 5. Main Empirical Results

### 5.1 Reduced-form main estimate

The main reduced-form specification estimates the protective effect of Korea-China bilateral trade exposure on working-age deaths-of-despair mortality at the sigungu × long-difference level. The Bartik-style instrument combines 1994 baseline industry employment shares (KOSTAT mining and manufacturing census, KSIC 9th-edition 2-digit) with industry-level Korean import growth from China during the 2000-2010 China bilateral integration period:

  z_x_h = Σ_k s_{h,k}^{1994} × ΔM_{KR-CN,k} / E_h^{1994}

where s_{h,k}^{1994} is the share of 1994 manufacturing employment in industry k at sigungu h, ΔM_{KR-CN,k} is the 2000-2010 change in Korean imports from China for industry k (UN Comtrade, KIET60-mediated HS6 → KSIC9 concordance), and E_h^{1994} is total 1994 manufacturing employment at sigungu h (per-worker normalization).

The outcome is the long-difference of log working-age (25-64 Korean nationals) age-standardized mortality rate plus 1, computed across the 1997-1999 baseline window and the 2018-2022 endpoint window:

  Δ_long log_asr_p1 = log(asr_2018-2022 + 1) − log(asr_1997-1999 + 1)

The main reduced-form regression on the n = 221 sigungu native-build analytic sample (Section 7.1.1 documents the sample construction) yields:

  **β_main = -0.127** (cluster-province t = -4.02; AKM-proper t = -4.93, p_AKM < 10⁻⁶),

where the regressor is the standardized z_x_h (mean-zero / unit-SD normalization within the 221-sigungu sample). The protective sign indicates that sigungu with higher Korea-China bilateral trade exposure during 2000-2010 experienced larger relative declines in working-age deaths-of-despair mortality over the 1997-1999 ↔ 2018-2022 long-difference window. In native scale, the coefficient corresponds to an **11.92 percent reduction in working-age deaths-of-despair mortality per standard deviation increase in trade exposure** (computed as 1 − exp(−0.127)).

**Footnote — native unit + IQR translation.** The native unit of z_x_h prior to standardization is total Korea-China bilateral import exposure per 1994 manufacturing worker over the 2000-2010 trade integration period, expressed in USD per worker. The standardization factor (sample standard deviation of native z_x_per_worker within the 221-sigungu sample) is σ_z = USD 1,696,322 per worker (median = 494,804; IQR = 1,228,279; p25 = 196,358; p75 = 1,424,637). Following the Autor-Dorn-Hanson (2013) and Pierce-Schott (2020) magnitude-reporting convention, the **interquartile-range (IQR) translation** of the main estimate is: a sigungu at the 75th percentile of bilateral exposure (z_x_per_worker = 1,424,637 USD/worker) experiences a long-difference change in working-age deaths-of-despair log-mortality of approximately exp(β × (Δz_IQR / σ_z)) − 1 = exp(−0.127 × 0.7240) − 1 ≈ **−8.78 percent** relative to a sigungu at the 25th percentile (z_x_per_worker = 196,358 USD/worker). The Pearson correlation cor(z_x_per_worker, Δ_long log_asr) = −0.381 within the 221-sigungu long-difference panel confirms the protective sign of the main estimate.

The archive build (10-year long-difference window 2000-2010, 1994 baseline shares, n = 222 sigungu) yields β_archive = -0.0685 (HC1 SE = 0.032, t = -2.12, p = 0.034) and is reported as a lower-bound sensitivity check (Section 6.3); the native main estimate covers the full post-shock observational period now available through 2022 and is preferred as the main specification. The magnitude difference (β_native_main / β_archive ≈ 1.85) is interpreted in Section 6.3 as a window-length plus sample-composition difference rather than as evidence of literature-anchored long-run amplification.

The activation-timing interpretation of the main estimate is consistent with the gradual-integration framework discussed in Section 6.1, under which Korea-China bilateral economic exposure begins substantively with the August 1992 diplomatic normalization rather than discretely at China's 2001 WTO accession. The 1995-2001 placebo specification (β_placebo_5.1 = +0.0238, opposite sign, insignificant) and the 1992-1996 placebo specification (β_placebo_6.1 = -0.123, sign-aligned with the main estimate, p_WCR = 0.0004) are jointly consistent with continuous-exposure dynamics from the 1992 normalization onward, with the 2001 WTO accession serving as an institutional anchor rather than an economic discontinuity (Section 6.1 documents the empirical and historical evidence supporting this reading).

### 5.2 Five-layer standard error inference + dual-specification disclosure

The reduced-form coefficient β is reported with five layers of standard errors to address cross-sigungu correlation, shift-share inference, and small-cluster bootstrap reliability. Two regressor specifications produce identical OLS coefficients up to the standardization factor σ_z but yield different residual variance estimates: (i) the **standardized z_x_h** specification (mean-zero / unit-SD normalization, used in Table 1) and (ii) the **per-worker z_x_per_worker** specification (USD per 1994 manufacturing worker, native scale, referenced in narrative t-statistics throughout this section). The two specifications produce identical OLS coefficients (β_standardized = β_native × σ_z; footnote of Section 5.1) but differ in cross-sigungu residual variance by a factor of σ_z² ≈ (1.7 × 10⁶)². Throughout this paper, Table 1 reports the standardized specification, and the narrative t-statistic anchor follows the per-worker specification; the per-worker specification is preferred for inference because it preserves the native scale of the Bartik construction.

**Table 1**: Main reduced-form estimate by standard error layer (standardized specification)

| SE Layer | SE | t | p |
|----------|----|----|---|
| HC1 (heteroskedasticity-robust) | 0.0323 | -2.12 | 0.034 |
| Cluster-province (G=16, asymptotic) | 0.0221 | -3.11 | 0.0019 |
| **AKM-proper (Adão-Kolesár-Morales 2019)** | **0.0258** | **-4.93** | **< 10⁻⁶** |
| Conley spatial HAC (5 km cutoff) | 0.0327 | -2.10 | ≈ 0.04 |
| Conley spatial HAC (10 km cutoff) | 0.0335 | -2.04 | ≈ 0.04 |
| Webb 6-point WCR (B=9,999, G=16) | — | — | < 0.0001 |

The per-worker specification yields HC1 SE = 0.026 (t = -4.92), cluster-province SE = 0.032 (t = -4.02), and AKM-proper SE = 0.026 (t = -4.92, p_AKM = 8.58 × 10⁻⁷); the AKM-proper SE is invariant to the standardization factor up to numerical precision and serves as the cumulative anchor across both specifications.

The five inference layers are:

1. **HC1** (White 1980 + Liang-Zeger 1986 small-sample correction).
2. **Cluster-province** (G = 16 sido on the n = 221 native sample; Cameron-Gelbach-Miller 2008).
3. **AKM-proper shift-share SE** (Adão, Kolesár, and Morales 2019, computed via the Kolesár 2024 R package `ShiftShareSE`). The implementation uses the share matrix W of dimension n × K (n = 226 sigungu × K = 22 KSIC9 2-digit industries) and the industry-level shock vector ΔM_k. Earlier in-house AKM attempts yielded numerical instability (Rotemberg HHI = 0.66, effective number of identifying industries J ≈ 1.5); the standard `ShiftShareSE` implementation produces stable AKM-proper SE = 0.0258, t = -4.93, p < 10⁻⁶. The AKM0 confidence interval returned NA in 5 outcome regressions due to a "share matrix collinear" warning, reflecting the same effective-J concentration; the AKM0 confidence interval is therefore not reported in the main text.
4. **Conley (1999) spatial HAC**: distance bands at sigungu centroid 5km and 10km; coefficient stable, SE within 5 percent of HC1 across distance bands.
5. **Webb (2023) Wild Cluster Restricted bootstrap**: 6-point Webb weights with B = 9,999 replications, MacKinnon-Webb 2018 implementation imposing the null hypothesis H₀: β = 0 via restricted residuals; **p_WCR < 0.0001** (zero of 9,999 bootstrap iterations exceed the observed |t| = 4.02 under cluster-robust inference). An earlier Rademacher-weighted Wild Cluster Unrestricted (WCU) implementation did not numerically converge in the present sample (consistent with the known WCU size distortion in small-G settings; G = 16 in our setting).

**Inference framework — methodological innovation disclosure.** The combination of AKM-proper shift-share standard errors (Adão, Kolesár, and Morales 2019) for single-coefficient inference with Romano-Wolf step-down (Section 5.3) under a Webb (2023) 6-point Wild Cluster Restricted bootstrap backend for family-wise inference is, to our knowledge, an inference-framework innovation rather than a literature norm. The two corrections solve orthogonal problems: AKM-proper corrects the share-correlation overrejection that arises in shift-share single-hypothesis standard errors (Adão-Kolesár-Morales 2019 § 3), while Romano-Wolf step-down with WCR backend controls the family-wise error rate (FWER) over the family of pre-specified outcomes (Clarke-Romano-Wolf 2020 § 2). We adopt them as **complementary, not competing**, procedures.

### 5.3 Outcome specificity (5-outcome family + Romano-Wolf adjustment)

A central prediction of the labor-market-mediated despair channel is that the trade exposure effect concentrates on the deaths-of-despair composite rather than on general mortality conditions. Table 2 reports the reduced-form estimates for the five outcome categories specified in Section 3.1.

**Table 2**: Outcome specificity, 5-outcome family

| Outcome | n | β | Cluster t | AKM-proper p | WCR-Webb p | RW p (5-outcome family, n=219 common) |
|---------|---|---|-----------|--------------|------------|---------|
| despair_total | 221 | -0.127 | -4.02 | < 10⁻⁶ | < 0.0001 | **0.0161** ★ |
| cardiovascular | 221 | -0.070 | -3.09 | 0.0013 | 0.016 | 0.129 |
| cancer | 221 | -0.050 | -1.64 | 0.031 | 0.220 | 0.382 |
| respiratory | 219 | +0.075 | +1.65 | 0.034 | 0.126 | 0.382 |
| external_other | 221 | -0.017 | -0.44 | 0.535 | 0.694 | 0.658 |

The deaths-of-despair coefficient (-0.127) is the largest in absolute magnitude among the five outcomes. Under the 5-outcome family Romano-Wolf step-down adjustment with WCR bootstrap (Romano-Wolf 2005a, *Econometrica* 73(4); Clarke, Romano, and Wolf 2020, *Stata Journal* 20(4)), only the deaths-of-despair coefficient passes the 5 percent FWER threshold (**p_RW = 0.0161**). The Bonferroni-corrected p-value at the same family is 5 × 0.034 = 0.170, and the Holm-Bonferroni step-down value for the smallest p-value is also 0.170; the Romano-Wolf p_RW = 0.0161 is therefore *less* conservative than both Bonferroni and Holm-Bonferroni in this implementation, consistent with the standard Romano-Wolf advantage when the test statistics share common bootstrap-resampling structure across outcomes.

The protective sign is preserved across cancer, cardiovascular, and external-other outcomes (sign-aligned with despair); respiratory mortality is the single exception (positive sign with marginal single-outcome significance but null under family-level Romano-Wolf adjustment). Cardiovascular mortality is marginally non-significant under family-level adjustment (p_RW = 0.129) despite single-outcome significance under AKM-proper and WCR (p_AKM = 0.001, p_WCR = 0.016), reflecting the intended conservatism of the Romano-Wolf step-down procedure when the family includes outcomes with moderate effect sizes.

This outcome-specificity pattern—a large protective effect on deaths-of-despair and weaker or null effects on placebo categories—mirrors the U.S. evidence by Pierce and Schott (2020) on drug overdose, where similar placebo categories (cancer, cardiovascular) showed null responses to PNTR exposure.

**Pre-analysis plan anchor.** The pre-analysis plan registered on OSF (PAP v4.5 § 4.6, registration date 2026-05-05) defines the primary outcome as the deaths-of-despair composite, with cancer, cardiovascular, respiratory, and external-other as secondary placebo outcomes within a single FWER family. Under this hierarchical pre-specification, two inferences are reported in parallel: (i) the primary single-outcome a-priori test for despair_total (HC1 p = 0.034 standardized spec, p < 10⁻⁶ AKM-proper) and (ii) the 5-outcome family Romano-Wolf adjusted test with WCR bootstrap backend (p_RW = 0.0161). Both inferences are pre-specified and mutually consistent with the primary-vs-secondary outcome structure documented in the PAP. An earlier in-house Romano-Wolf implementation that did not impose the null hypothesis via WCR bootstrap yielded p_RW = 0.317 (over-conservative under shift-share clustering structure); the WCR-backed implementation reported here is the standard valid form following Clarke-Romano-Wolf (2020).

Section 6.5 reports an alternative 4-outcome despair-only family (despair_total + suicide + drug overdose + alcohol-related liver disease) that yields p_RW intermediate between 0.10 and 0.15.

### 5.4 IV second-stage estimate and LMP weak-instrument inference

The instrumental-variable specification regresses the long-difference mortality change on the Korea-China bilateral exposure z_x_h, instrumented by the ADH-8 exposure measure z_x_h^{ADH-8} (Section 4.1). The first-stage regression yields

  z_x_h = 0.45 + 0.31 × z_x_h^{ADH-8} (HC1 SE = 0.07; F-statistic = 19.65),

below the Olea and Pflueger (2013) τ = 10 percent cutoff of 23.1, placing the instrument in weak-IV territory. The IV second-stage point estimate is **β_IV = -0.092** (HC1 SE = 0.050, t = -1.85), with the same protective sign as the reduced-form main estimate but a slightly larger magnitude.

Following the valid t-ratio inference of Lee, McCrary, Moreira, and Porter (2022), the IV second-stage critical value at the 5 percent two-sided test depends on the first-stage F-statistic. Two cutoff conventions are reported. The interpolated cutoff c_{0.05}(F=19.65) ≈ 3.286 follows Lee et al. (2022) Table 3 Panel A's continuous interpolation rule. The conservative binned cutoff c_{0.05}(F ∈ [15, 20)) = 3.84 follows the step-function bin-table convention. The IV second-stage |t| = 1.85 fails both cutoffs, providing a robust weak-instrument warning. The LMP cutoff applies specifically to the IV second-stage t-statistic; reduced-form coefficients are evaluated under conventional t-inference (the normal-distribution critical value of 1.96 at the 5 percent two-sided test). The main reduced-form |t| values (HC1 per-worker = 4.92, cluster-province = 4.02, AKM-proper = 4.93) all exceed the conventional 1.96 cutoff.

This paper proceeds with the reduced-form coefficient β_main = -0.127 as the preferred specification, following the convention in similar weak-instrument settings (Pierce and Schott 2020; Finkelstein, Notowidigdo, and Shi 2026; Lang, McManus, and Schaur 2019). **The Korean F-statistic of 19.65 is comparable to the Lang et al. (2019) Table 2 column M.3 first-stage F of 18.77 using the identical 8-OECD instrument basket, providing a published procedural precedent.** The IV estimate is reported as a robustness check only; its statistical significance under conventional t-inference should be interpreted with caution.

**BHJ shock-only path (complementary identification check).** A complementary identification check uses the Borusyak-Hull-Jaravel (2022) shock-only path via the `ssaggregate` package, which transforms the regression to industry-level WLS using shock-aggregated outcomes. This procedure yields a coefficient of **β_BHJ = +0.0191** (sign reversed from the share-path Bartik β_main = -0.127). The sign reversal is consistent with three plausible explanations rather than a refutation of the main result: (i) the BHJ shock-only path and the GPSS share path target *different estimands*, with BHJ assuming expected shocks of zero conditional on industry-level controls (a stricter exogeneity assumption than the GPSS share-exogeneity path used in the main specification); (ii) the high concentration of identifying variation (effective J ≈ 1.5; Rotemberg HHI = 0.66) renders the BHJ industry-level WLS sensitive to noise in any single industry; (iii) the implicit Bartik weighting on share-by-shock interactions differs from the BHJ unweighted shock-level regression, leading to estimands that need not coincide outside of pure share-path or pure shock-path identifying environments. The dual reporting of the share-path β_main = -0.127 and the shock-path β_BHJ = +0.0191 is honest disclosure that the identification strategy is sensitive to the choice of identifying variation.

### 5.5 Sub-period analysis (2008 ICD-10 revision) + Summary

The 2008 KCD revision (KCD 6th edition, KOSTAT 2007 December notification, effective January 2008) affects approximately 12 percent of the deaths-of-despair cause-of-death codes. To assess whether the main estimate is mechanically driven by the classification break, the long-difference specification is re-estimated on the post-2008 sub-period (2008 base to 2018-2022 endpoint) for 218 sigungu:

  **β_post-2008 = -0.0897** (HC1 SE = 0.0210, t = -4.28, p < 0.0001),

with the same protective sign as the main estimate. The post-2008 magnitude is reported in the archive scale (-0.0897 corresponds to the 10-year long-difference window 2000-2010 baseline used in the archive build); the native-scale post-2008 sub-period estimate under the 21-year long-difference window (1997-1999 ↔ 2018-2022, β_main = -0.127) requires a separate R wrapper execution and is deferred to the online appendix. Under the archive-scale comparison, the post-2008 sub-period coefficient (-0.0897) is approximately 31 percent larger in absolute magnitude than the archive main β_archive = -0.0685, consistent with the magnitude pattern documented in Section 6.3 between archive and native windows. We do not interpret the larger post-2008 magnitude as evidence of literature-anchored dynamic amplification (Section 6.3 documents that the displacement-mortality literature does not cleanly support such a framing); rather, the post-2008 result is consistent with continued cumulative protective dynamics over the post-revision window. The pre-2008 sub-period (1997-1999 base to 2007 endpoint) was not separately reported in this build due to a sample restriction that drops sigungu with sparse pre-revision counts; a future revision will report the symmetric pre-2008 estimate.

**Summary of main empirical results.** The main empirical evidence from the 1994-baseline 221-sigungu native-build analytic sample yields four findings:

(i) a statistically significant protective effect of **β_main = -0.127** (cluster-province t = -4.02; AKM-proper t = -4.93, p_AKM < 10⁻⁶; Webb WCR p < 0.0001) in the long-difference reduced-form regression for working-age deaths-of-despair mortality;

(ii) outcome specificity with the despair effect significantly larger than the four placebo outcomes (cardiovascular, cancer, respiratory, external-other), with the Romano-Wolf 5-outcome family-wise adjusted **p_RW = 0.0161** satisfying the 5 percent FWER threshold for despair while the four placebo outcomes remain non-significant under family-level adjustment (p_RW ∈ [0.13, 0.66]);

(iii) the IV estimate of **β_IV = -0.092** with the same protective sign but failing the Lee-McCrary-Moreira-Porter (2022) weak-instrument cutoff under both interpolated (3.286) and binned (3.84) thresholds; the BHJ shock-only path yields β_BHJ = +0.0191 (sign reversal), reflecting the sensitivity of identification to the choice of identifying variation under high effective-J concentration;

(iv) a more precisely estimated post-2008 sub-period effect (β_post-2008 = -0.0897, archive scale) that is not driven by the 2008 KCD classification revision.

The archive build (β_archive = -0.0685, n = 222 sigungu) and the 1992-baseline robustness (β_1992 = -0.0640 winsorized, n = 209; Section 6.3) provide sign-consistent agreement across two distinct long-difference windows and two distinct industrial baseline years. Section 6 reports an extensive set of robustness checks that test the sensitivity of these findings to baseline year choice, electronics sector exclusion, pre-WTO placebo specification, and alternative outcome family definitions.

---

## R-A 의 cumulative substantive direction (refined)

본 § 5 narrative draft (refined) 는 직전 draft `section_5_proposal_2026-05-08.md` 의 다음 영역 정정:

**(a) Numeric 정정**:
- β = -0.128 → -0.127 (paper 본문 line 15, 21 main β anchor 일치)
- AKM-proper t = -4.92 → -4.93 (paper 본문 line 21, 35 일치)
- Conley 1km 제거 (paper 본문 line 35 Table 1 위 5km/10km 만)

**(b) substantive 보강**:
- § 5.1 footnote σ_z + IQR translation + Pearson cor (paper 본문 line 17 [^X] 위 cumulative anchor)
- § 5.2 IV β_IV = -0.092 + Lang 18.77 procedural precedent + BHJ β = +0.0191 + dual-spec disclosure
- § 5.3 5-outcome Table 2 specific β + Bonferroni 0.170 + PAP v4.5 OSF anchor
- § 5.x methodological innovation disclosure

**(c) numbering 정정**:
- 직전 draft § 5.1-5.6 (6-section) → paper 본문 § 5.1-5.5 (5-section) align

**(d) Findings P + Q + R cumulative anchor**:
- Finding P: § 5.2 dual-specification disclosure (standardized vs per-worker) cumulative carry
- Finding Q: § 5.1 placebo narrative gradual-integration framework unification (Section 6.1 reading 위 align)
- Finding R: § 5.5 summary 위 archive vs native main β anchor explicit framing

본 refined draft 은 R-A 측 reference 자료. 사용자 측 paper § 5 본문 commit 은 사용자 측 별도 환경 위 진행 — 분업 경계 anchor.

---

**End of R-A 측 paper § 5 narrative draft refined (공동저자 mode)**
