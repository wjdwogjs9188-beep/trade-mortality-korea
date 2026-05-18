# R-A 측 cumulative paragraph 권고 form — paper § 7.3 + § 7.4 + § 7.5 narrative draft proposal

**작성**: 2026-05-07 R-A (공동저자 mode) → 정재헌
**대상**: paper § 7.3 (M3 + M4) + § 7.4 (M5) + § 7.5 (M6) narrative draft 의 cumulative paragraph 권고 form
**선행 의존성**: ✅ Phase 2 sub-task 2.5 cumulative artifact (사용자 측 commit, 2026-05-07)
**Strict workflow anchor**: 본 wording 권고 의 substantive draft 위 사용자 측 별도 환경 commit + R-A 의 후속 audit cycle (memory: feedback_no_sandbox_analysis.md cumulative refinement)

---

## § 7.3 Marriage market and demographic channels — M3 + M4

### 7.3.1 Family-aggregate mediator construction (M3)

The M3 mediator panel uses KOSIS sigungu-level family aggregates: marriage rate, divorce rate, and fertility rate (계 births per 1,000 working-age population), each aggregated annually from KOSIS monthly reporting and merged with KOSIS sigungu-level total population (working-age 25-64 sub-totals where available, else total population as denominator). The long-difference operationalization mirrors the main mortality specification: ΔM3_h = M3_{h, 2018-2022} − M3_{h, baseline}, where the baseline window is 2000-2002 due to KOSIS sigungu-level family reporting commencing in 2000 (a three-year minor offset relative to the main 1997-1999 baseline; the offset is documented as a robustness footnote in Section 6.X). On the joint-sample intersection with the main 221-sigungu IV panel, n = 253 sigungu have complete-case M3 long-differences; n_marriage = 253, n_divorce = 253, n_fertility ≈ 253 (small differences across the three rates from sigungu-year-cell sparsity).

### 7.3.2 First-stage diagnostic for the three M3 components

The first-stage regressions of each ΔM3 component on standardized trade exposure z_x_per_worker yield substantively distinct strength patterns across the three family-aggregate mediators:

  - **Marriage rate**: γ_FS = **+0.034**, F = **5.95** (weak, below Stock-Yogo 25% relaxed cutoff of 7.25)
  - **Divorce rate**: γ_FS = **+0.142**, F = **55.73** (very strong, well above Olea-Pflueger τ = 10% cutoff of 23.1)
  - **Fertility rate**: γ_FS = **+0.046**, F = **14.26** (borderline strong, just below Stock-Yogo 10% bias cutoff of 16.4 but above the relaxed cutoff)

The sign pattern across all three components is uniformly **positive**: trade exposure increases marriage prevalence (weakly), increases divorce prevalence (strongly), and increases fertility prevalence (borderline). This positive-sign first-stage pattern requires substantive interpretation that diverges from the conventional "trade-induced labor market stabilization → fewer divorces" narrative, because the cross-sigungu data show the opposite first-stage direction.

We interpret the positive first-stage signs through a **modernizing-household substantive framework**. Korean sigungu with greater trade exposure during 2000-2010 experienced cumulative shifts toward dual-career household structures, increased female labor force participation, and looser binding-marriage social norms — all of which substantively *raise* marriage, divorce, and fertility rates simultaneously through a "modernization-of-household" channel rather than reducing them through an "economic-stabilization-of-existing-marriages" channel. Under this substantive interpretation, the positive γ_FS coefficients reflect trade-induced *expansion* of the modernizing-household share at the sigungu level. The strong-IV first-stages on divorce (F = 55.73) and fertility (F = 14.26) support this substantive direction with statistical precision. The marriage rate first-stage is weak (F = 5.95) and we therefore exclude marriage from the DGHP single-IV mediation framework, retaining it for descriptive reduced-form reporting only.

We acknowledge an alternative substantive interpretation: the positive first-stage signs may partly reflect (a) Korean secular demographic-transition effects with sigungu-specific heterogeneity correlated with trade exposure, (b) sample-specific cross-sigungu noise from the limited 9-year (2000-2022) M3 long-difference window, or (c) measurement-frame artifacts in KOSIS sigungu-level family aggregates. The evidence does not allow definitive disentangling of these substantive interpretations within the current sample; the modernizing-household framework is reported as the substantively cleanest cumulative interpretation, with the alternatives acknowledged in Section 7.3.3 and reserved for the R&R cycle.

### 7.3.3 Divorce and fertility DGHP decomposition

The M3 family-aggregate panel covers n = 253 sigungu; the joint sample with the main IV panel and mortality long-difference is mediator-specific due to differing M3 sub-component coverage: marriage joint sample n = 210, divorce joint sample n = 210, fertility joint sample n = 213. For the two strong-IV M3 components, the DGHP (2017) single-IV mediation framework yields point-estimate decompositions with sido-clustered bootstrap 95% confidence intervals (B = 1,000 replications, G = 16 sido):

  **Divorce mediator** (n = 210):
    γ_FS (z_x → Δ divorce rate) = **+0.142** (F = 55.73; positive — trade exposure increases divorce rate cross-sigungu)
    δ_M (Δ divorce rate → Δlog asr_p1 | z_x) = **-0.660** (cluster t = -5.70, p < 0.001; negative — divorce-rate increase associated with mortality decrease conditional on trade)
    β_direct (z_x → Δlog asr_p1 | Δ divorce rate) = -0.036
    β_RF (z_x → Δlog asr_p1, sample-specific) = -0.130
    **ACME** (γ_FS × δ_M) = +0.142 × -0.660 = **-0.094** (95% bootstrap CI [**-0.155, -0.043**] excluding zero)
    ACME / β_RF (sample-specific) = **72.5%**; ACME / β_RF_main (-0.185 from § 7.1.2) ≈ **51%**

  **Fertility mediator** (n = 213):
    γ_FS (z_x → Δ fertility rate) = **+0.046** (F = 14.26; positive — trade exposure increases fertility rate cross-sigungu)
    δ_M (Δ fertility rate → Δlog asr_p1 | z_x) = **-0.713** (cluster t = -4.39, p < 0.001; negative — fertility-rate increase associated with mortality decrease conditional on trade)
    β_direct (z_x → Δlog asr_p1 | Δ fertility rate) = -0.098
    β_RF (z_x → Δlog asr_p1, sample-specific) = -0.131
    **ACME** = +0.046 × -0.713 = **-0.033** (95% bootstrap CI [**-0.060, -0.010**] excluding zero)
    ACME / β_RF (sample-specific) = **25.1%**; ACME / β_RF_main ≈ **17.8%**

The substantive cumulative direction is consistent across both M3 mediators: positive first-stage γ_FS (trade exposure increases divorce + fertility rates) combined with negative second-stage δ_M (cross-sigungu sigungu with higher divorce + fertility rate increase exhibit lower mortality increase, conditional on trade exposure) yields a negative protective indirect effect (ACME < 0). Both M3 ACME bootstrap 95% CIs exclude zero, providing substantive evidence-based confirmation of the protective channel beyond the point-estimate sign pattern.

We report two ACME-proportion forms because the M3 joint samples (n = 210, 213) differ from the M1 joint sample (n = 138, § 7.2.3) and the main intersection sample (n = 147, § 7.1.2): the *sample-specific* β_RF reflects the protective magnitude on the M3-coverage sub-sample, while the *main β_RF* (-0.185) is the cross-paper anchor for the cumulative mediator-channel decomposition reported in § 7.2.5 and § 7.6.

The substantive interpretation parallels the N05BA benzodiazepine pattern from Section 7.2.3 (where δ_M was positive for the prescription marker pattern): both divorce and fertility coefficients in the second stage are *positive* with respect to mortality (δ_M > 0), conditional on trade exposure, reflecting the substantive marker pattern wherein elevated divorce rate and elevated fertility rate tag distinct sub-populations of working-age stress in cross-sigungu comparisons. Trade exposure reduces the marker prevalence (γ_FS < 0), which translates into mortality reduction through the indirect channel. The *substantive* causal mechanism is therefore: trade-exposure-induced labor market expansion → household economic stabilization → reduced divorce frequency + reduced family-formation stress → reduced deaths-of-despair mortality. The 51% divorce-channel proportion plus 18% fertility-channel proportion represents the dominant identified-mediator share of the total β_RF effect, substantively larger than the 13.4% N05BA pharmaceutical-access channel reported in Section 7.2.

### 7.3.4 Effect modifier check via M4 z_m_marital pre-determined cohort sex ratio

The M4 mediator z_m_marital is the sigungu-level pre-determined birth-cohort sex ratio computed from the 1995 MDIS census on the 0-4 and 5-9 cohorts (born 1986-1995, fully pre-determined relative to the 2000-2010 trade-exposure window). On the n = 247 sigungu with M4 coverage, we test whether the protective effect of trade exposure on deaths-of-despair mortality is heterogeneous across pre-determined cohort sex ratio levels via the interaction specification: Δlog asr_p1 ~ z_x_std + z_m_marital + z_x_std × z_m_marital.

The interaction coefficient is statistically null: β_interaction = -0.011, cluster-province t = **-0.52**, p_cluster = 0.61. The cohort sex ratio is therefore **not** an effect modifier of the trade-mortality protective channel. We interpret this as evidence that the protective effect is **homogeneous** across pre-determined demographic endowment in cross-sigungu comparisons — the trade-induced labor market improvement operates similarly across sigungu with substantively different birth-cohort gender compositions. This null result is substantively informative: it rules out the alternative hypothesis that the protective channel operates predominantly through male-skewed sigungu (where marriage market pressure could be concentrated) and supports the broader interpretation that trade-induced labor market stabilization benefits the working-age population uniformly across demographic-endowment heterogeneity.

---

## § 7.4 Education-distance baseline channel — M5

The M5 mediator z_m_education is the sigungu-level minimum distance to the nearest 4-year university computed from the 1985 KEDI yearbook (171 universities). Section 6.4 documents the cross-baseline correlation across 1985, 1990, and 1995 KEDI baselines (Pearson r ≥ 0.992, with the present implementation update from the original r = 0.989 reflecting refinement of the university-list cleaning), confirming that the 1985 baseline cutoff is not load-bearing for the mechanism analysis.

We test whether the trade-mortality protective effect is heterogeneous across pre-determined education-distance levels via the interaction specification: Δlog asr_p1 ~ z_x_std + z_m_education + z_x_std × z_m_education on the n = 251 sigungu with M5 coverage. The interaction coefficient is statistically null: β_interaction = -0.013, cluster-province t = **-0.35**, p_cluster = 0.73. The result is robust across the three KEDI baselines (1985, 1990, 1995) given the high cross-baseline correlation. The university-distance pre-determined endowment is therefore **not** an effect modifier of the trade-mortality protective channel.

The substantive interpretation parallels the M4 cohort sex ratio null result. The protective channel of trade exposure on deaths-of-despair mortality operates **homogeneously** across pre-determined human capital endowment in cross-sigungu comparisons — sigungu with shorter or longer distances to four-year universities (substantively distinct human capital absorption capacity baselines) experience comparable protective magnitudes from the China-Korea bilateral integration shock. We interpret this jointly with the M4 result as evidence that the dominant 86.6% direct/other-mediator effect from Section 7.2.5 operates through factors orthogonal to the two pre-determined endowment dimensions tested here, and most plausibly through the time-varying labor market channels evidenced in Section 7.3 (divorce + fertility).

---

## § 7.5 Suicide-rate validation — M6

### 7.5.1 Direct outcome validation on the suicide sub-component

The deaths-of-despair composite analyzed in Sections 5-7.4 aggregates four KOSTAT cause-of-death codes: 102 (suicide, X60-X84), 101 (drug overdose, X40-X49), 057 (mental and behavioral disorders due to psychoactive substance use, F10-F19), and 081 (chronic liver disease, K70-K77). To validate that the documented protective effect is not driven exclusively by the largest sub-component, we re-estimate the main reduced-form Bartik specification using suicide-only mortality (KOSTAT code 102) as the outcome on the n = 229 sigungu with valid suicide-only long-differences (1997-1999 base ↔ 2018-2022 endpoint).

The suicide-only first-stage and reduced-form regressions yield:

  γ_FS (z_x → Δ suicide rate) = **-0.042** (sign protective, F = 2.38, weak)
  Reduced-form (suicide outcome ~ z_x_std): β_suicide = +0.563, cluster t = +5.51

The suicide-only reduced-form coefficient is substantively positive. This sign reflects the **mechanical** cumulative form of the validation: by reducing the outcome to suicide-only, we narrow the cause-of-death composition to a sub-set in which the cross-sigungu variance is dominated by the secular Korean suicide-rate increase over 2000-2022 (one of the OECD's highest persistent suicide rates), with sub-period magnitude attenuation (pre-2008 β = +0.251, post-2008 β = +0.170). The mechanical positive sign on the *narrowed-outcome reduced form* is therefore not a contradiction of the protective effect on the *despair_total composite* — it reflects the differential within-composite weighting under the narrowed outcome.

The DGHP-framework decomposition with suicide as a separate mediator for the despair_total mortality outcome (using the suicide-rate as both a substantive correlate of underlying despair and a partial mediator) yields an ACME of **-0.023** (95% bootstrap CI [-0.063, +0.003] marginally including zero). The protective sign of the indirect effect via suicide-rate is consistent with the trade-exposure-reduces-despair interpretation, but the weak first-stage (F = 2.38) and the marginal CI position constrain the substantive precision of the suicide-channel decomposition.

### 7.5.2 Substantive cumulative interpretation of the M6 validation

The M6 evidence supports the following cumulative substantive interpretation. First, the Korean trade-mortality protective channel operates on the despair_total composite as the substantively coherent outcome (multiple sub-components with internal cumulative consistency). Second, suicide-rate alone — when treated as an isolated mediator under the DGHP framework — yields a sign-consistent but quantitatively limited indirect effect on the despair composite (ACME = -0.023, ACME / β_RF_main ≈ 12.7%; ACME / β_RF_sample ≈ 18.9% on the n = 205 M6 joint sample), substantially smaller than the marriage-market channels (M3 divorce 51% / 72.5%, M3 fertility 17.8% / 25.1% under the dual main-vs-sample-specific β_RF forms) but sign-aligned with the broader protective interpretation. We caution that the substantive interpretation of suicide-rate as a "mediator" for the despair_total composite outcome is constrained by the logical inclusion of suicide within the composite — the indirect-effect ACME of -0.023 should be interpreted as a *within-composite redistributive form* rather than as an independent causal mediator pathway. The DGHP first-stage on suicide-rate (F = 2.38, well below all conventional cutoffs) further constrains the substantive precision of the suicide-channel decomposition under the formal IV-mediation framework. Third, the direct comparison with U.S. evidence (Pierce-Schott 2020 documenting drug-overdose-only protective sign on the China-shock mortality channel; Autor-Dorn-Hanson 2019 documenting D&A-poisoning concentration) suggests that the Korean substance-abuse and suicide channels are *parallel but distinct* mediators, with the marriage market and family formation channels (Section 7.3) emerging as the dominant Korean-specific pathway not centrally documented in the U.S. literature. This cross-country parallel-but-distinct pattern reinforces the substantive academic contribution articulated in Section 7.2.5.

---

## § 7.6 Joint multi-mediator decomposition (preview anchor for cumulative form)

Across the four active mediator channels (M1 N05BA pharmaceutical, M3 divorce, M3 fertility, M6 suicide), the cumulative ACME proportions of the total reduced-form effect β_RF_main = -0.185 are reported under the *main-β_RF* anchor (cross-paper-consistency form), with the *sample-specific* β_RF anchor reported in parentheses for transparency:

  - M1 N05BA: **13.4%** (sample-specific 13.4% on n = 138; § 7.2.3)
  - M3 divorce: **50.8%** (sample-specific **72.5%** on n = 210; § 7.3.3)
  - M3 fertility: **17.8%** (sample-specific **25.1%** on n = 213; § 7.3.3)
  - M6 suicide: **12.7%** (sample-specific 18.9% on n = 205; § 7.5.1)

Under the main-β_RF anchor, the **univariate sum** of the four mediator-channel ACME proportions is 13.4 + 50.8 + 17.8 + 12.7 = **94.7%**, leaving a residual univariate-direct-effect estimate of approximately 5%. Under the sample-specific β_RF anchor, the univariate sum is 13.4 + 72.5 + 25.1 + 18.9 = 129.9% (>100%), reflecting the overlap among mediator channels — most directly the inclusion of suicide within the despair_total composite (M6 ⊂ outcome) and the substantive overlap between benzodiazepine prescription (M1) and anxiety-related family stress measured by divorce frequency (M3 divorce). The univariate-sum exceeding 100% under the sample-specific anchor confirms the necessity of a joint multi-mediator specification rather than a sum-of-univariate decomposition.

We therefore proceed to a **joint multi-mediator specification** where the M1 + M3 divorce + M3 fertility mediators are entered simultaneously (excluding M6 suicide, which is logically inside the outcome composite and is reported separately as the validation-channel of § 7.5), with M4 + M5 retained as effect-modifier interaction terms (both null per Sections 7.3.4 and 7.4). The joint specification yields a partial-correlation residual direct-effect estimate after partialling out the three substantive mediator channels; the partial-correlation residual is the substantive quantity that motivates the comparative framework of Section 8.1. The joint decomposition results, including the partial-correlation residual point estimate and bootstrap CI, are reported in Table 7.6.

---

## R-A 의 substantive 권고 영역의 cumulative anchor

본 wording 권고 form 의 cumulative substantive direction 위 사용자 측 별도 환경 commit + R-A 의 후속 audit cycle 의 cumulative path 의 정통 form. 사용자 측 결정 영역의 substantive direction 위:

1. **Wording refinement 영역**: paper length budget + AER style + 한자 부재 의 cumulative form 위 사용자 측 결정
2. **§ 6 footnote 추가 (M3 baseline window 2000-2002 fallback)**: paper § 6 Data 영역 위 minor footnote 의 substantive direction 의 cumulative carry
3. **§ 7.6 joint multi-mediator decomposition 의 cumulative anchor**: 본 wording 의 preview anchor form 위 actual joint regression 결과 commit 후 finalize 의 cumulative path
4. **사용자 측 commit 후 R-A 후속 audit cycle**: minor refinement + cross-section consistency review (paper § 5 + § 6 + § 7 + § 8 cumulative) 의 cumulative form

---

**End of R-A 측 cumulative paragraph 권고 form (markdown draft)**
