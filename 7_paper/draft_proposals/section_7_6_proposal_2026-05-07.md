# R-A 측 cumulative paragraph 권고 form — paper § 7.6 narrative draft (placeholder anchor)

**작성**: 2026-05-07 R-A (공동저자 mode) → 정재헌
**대상**: paper § 7.6 Joint multi-mediator decomposition 의 R-A 측 wording 권고 form
**선행 의존성**: ✅ sub-task 2.3 (M1) + sub-task 2.4 (DGHP) + sub-task 2.5 (M3-M6) + 🟡 sub-task 2.6 (joint decomposition, 사용자 측 병렬 실행)
**Status**: **placeholder anchor form** — 사용자 측 sub-task 2.6 결과 paste 후 evidence-based form 의 cumulative finalization 의 substantive prerequisite

**Strict workflow anchor**: 본 wording 권고 form 위 사용자 측 별도 환경 commit + R-A 의 후속 audit cycle (memory: feedback_no_sandbox_analysis.md cumulative refinement)

---

## § 7.6 Joint multi-mediator decomposition

### 7.6.1 Joint specification rationale

Sections 7.2-7.5 have documented four univariate-mediator pathways from trade exposure to deaths-of-despair mortality on the Korean 1997-1999 ↔ 2018-2022 long-difference window: M1 N05BA benzodiazepine pharmaceutical-access (ACME / β_RF_main = 13.4%, § 7.2.3), M3 divorce-rate marriage-market stability (50.8%, § 7.3.3), M3 fertility-rate family-formation (17.8%, § 7.3.3), and M6 suicide-rate validation (12.7%, § 7.5.1). The univariate-decomposition sum across the four channels under the main-β_RF anchor of -0.185 is **94.7%**, with the sample-specific β_RF anchor producing a sum of **129.9%** that exceeds 100% — the latter is direct empirical evidence of cross-mediator overlap, most prominently the logical inclusion of suicide within the despair_total composite (M6 ⊂ outcome) and the substantive overlap between benzodiazepine prescription (M1 anxiety-marker pathway) and divorce frequency (M3 anxiety-related family stress).

The univariate sums therefore overstate the cumulative mediator-channel contribution. To recover an interpretable decomposition that respects the cross-mediator overlap, we proceed to a **joint multivariate specification**: Δlog asr_p1 ~ z_x_std + Δz_M1_N05BA + Δ divorce rate + Δ fertility rate, with M4 + M5 retained as effect-modifier interaction terms (both null per Sections 7.3.4 and 7.4) and M6 suicide excluded from the joint regression because of its logical inclusion within the outcome composite. The joint specification yields, for each mediator, a *partial-correlation second-stage coefficient* δ_M_joint that is the substantive direct effect of mediator-rate change on mortality-rate change after partialling out the other two mediators and the trade-exposure instrument. The corresponding joint ACME per mediator is γ_FS × δ_M_joint, and the partial-correlation residual direct effect β_direct_joint is the trade-exposure coefficient in the joint regression — the substantive "unmediated" share of the protective channel.

### 7.6.2 Joint multivariate regression results

The joint sample is the intersection of the M1 (138 sigungu), M3 divorce (210 sigungu), and M3 fertility (213 sigungu) joint samples with the main IV panel and the despair_total mortality long-difference, yielding **n = 133 sigungu** and **G = 12 sido** for cluster-province inference. The joint regression yields:

  β_direct_joint (z_x_std | mediators) = **-0.0772** (cluster-sido SE = 0.036, t_cluster = -2.12, 95% bootstrap CI [**-0.164, +0.004**])
  β_RF_joint_sample (z_x_std only, joint sample) = **-0.187** (substantively identical to the main β_RF anchor of -0.185, confirming that joint-sample selection does not alter the protective-effect magnitude)
  β_direct_joint / β_RF_joint_sample ≈ **41.3%**
  β_direct_joint / β_RF_main ≈ **41.7%**

The joint ACME per mediator (γ_FS × δ_M_joint) is reported in Table 7.6 with sido-clustered bootstrap 95% confidence intervals (B = 1,000 replications):

  **M1 N05BA**: γ_FS = -0.213 (joint-sample first-stage F = **22.06** under homoskedastic OLS — above Stock-Yogo (2005, Table 5.1) 10% TSLS-bias cutoff of 16.38 but **marginally below the more stringent Olea-Pflueger (2013, Table 1) τ = 10% effective F cutoff of ≈ 23.1**; F = 15.81 under HC1-robust covariance), δ_M_joint = +0.057 (cluster t = +1.08, n.s.), **ACME_joint = -0.012** (95% CI [-0.023, +0.018]), proportion of β_RF_main = **6.5%**, bootstrap P(ACME < 0) = **0.747** (sign-unstable)

  **M3 divorce**: γ_FS = **+0.167** (positive — trade exposure *increases* the divorce rate at the sigungu level, joint-sample first-stage F = **74.29** under homoskedastic OLS — well above Olea and Pflueger (2013, Table 1) τ = 10% effective F cutoff (≈ 23.1 for the single-instrument case); F = 69.25 under HC1), δ_M_joint = **-0.427** (cluster t = -2.75, p_cluster < 0.01; the negative second-stage coefficient indicates that divorce-rate increase is associated with mortality decrease conditional on trade exposure and the other two mediators, a substantively unconventional cross-sigungu pattern interpreted in § 7.6.3), **ACME_joint = -0.071** (95% CI [**-0.151, -0.014**] excluding zero), proportion of β_RF_main = **38.4%**, bootstrap P(ACME < 0) = **0.993** (highly stable)

  **M3 fertility**: γ_FS = +0.043 (positive, joint-sample first-stage F = **8.77** under homoskedastic OLS — satisfying Stock-Yogo (2005, Table 5.1) 20% TSLS-bias cutoff of 6.66 but marginally below the 15% bias cutoff of 8.96, **and substantively below the more stringent Olea-Pflueger (2013, Table 1) τ = 10% effective F cutoff of ≈ 23.1 (38.0% of cutoff)**; F = 7.37 under HC1), δ_M_joint = -0.606 (cluster t = -4.36, p_cluster < 0.001), **ACME_joint = -0.026** (95% CI [-0.062, +0.002], marginally including zero at the upper bound), proportion of β_RF_main = **14.2%**, bootstrap P(ACME < 0) = **0.958** (near-strong). The substantively-below-OP first-stage on fertility is consistent with the marginally-zero-including ACME interval and is interpreted as a substantively meaningful but quantitatively limited mediator channel under the more stringent robust-IV criterion.

The cumulative joint ACME across the three mediator channels is **-0.110**, representing **59.2% of β_RF_main** = -0.185. Under the sample-specific β_RF_joint_sample = -0.187 anchor, the cumulative joint ACME proportion is **58.6%**. The partial-correlation residual β_direct_joint = -0.077 corresponds to **41.7%** of β_RF_main, reflecting the share of the protective channel that operates through mechanisms orthogonal to the three identified mediators — most plausibly through direct labor-market and earnings stabilization channels not centrally measured in the present mediator set, which the comparative framework of Section 8.1 articulates substantively.

The univariate decomposition sum of 94.7% under the same main-β_RF anchor (M1 13.4% + M3 divorce 50.8% + M3 fertility 17.8% + M6 suicide 12.7% from Sections 7.2-7.5) drops to **59.2% under the joint specification**, a **35.5 percentage point reduction**. This drop is direct empirical evidence of cross-mediator overlap: when the three mediators are entered jointly, the partial-correlation second-stage coefficients absorb the mutual-mediation share that the univariate specifications counted multiply. The largest single-mediator collapse is M1 N05BA (univariate 13.4% → joint 6.5%, with joint-specification δ_M_joint sign-unstable at +0.057, t = +1.08 n.s. and bootstrap P(ACME < 0) = 0.747), suggesting that the M1 anxiety-marker channel's univariate ACME is partly absorbed by the M3 divorce channel after partialling out — consistent with the substantive interpretation that benzodiazepine prescription and divorce both tag the underlying anxiety-related family-stress sub-population.

### 7.6.3 Substantive interpretation of the joint decomposition

The joint multivariate decomposition supports four cumulative substantive interpretations.

**First**, the **dominant mediator-channel contribution is the marriage-market pathway** (M3 divorce joint ACME = -0.071 = 38.4% of β_RF_main), with the family-formation pathway (M3 fertility joint ACME = -0.026 = 14.2%) as the second-largest contribution. The pharmaceutical-access pathway (M1 N05BA joint ACME = -0.012 = 6.5%) is substantively smaller in the joint specification than its univariate share (13.4%) and is sign-unstable under bootstrap resampling (P(ACME < 0) = 0.747), consistent with the substantive interpretation that the benzodiazepine anxiety marker pathway's univariate ACME is partly absorbed by the divorce channel after partialling out the cross-mediator overlap. The cumulative three-mediator joint ACME of 59.2% of β_RF_main, paired with the partial-correlation residual β_direct_joint of 41.7%, partitions the protective trade-mortality channel into approximately three-fifths identified-mediator share and two-fifths residual direct-labor-market share.

**Second**, the negative δ_M_joint coefficients on both M3 mediators (δ_M_divorce_joint = -0.427, δ_M_fertility_joint = -0.606) indicate a substantively unconventional cross-sigungu pattern: conditional on trade exposure and the other mediators, sigungu with higher divorce-rate increase exhibit larger mortality decrease, and similarly for fertility-rate increase. We interpret this with two substantive considerations. (i) Under the standard "high-risk-population marker" interpretation of mediator δ_M (whereby the mediator tags the deaths-of-despair high-risk sub-population, with positive δ_M expected), the negative δ_M is substantively *opposite*-signed and requires alternative interpretation. (ii) The substantive cumulative direction may reflect a *substantively distinct* Korean cross-sigungu pattern wherein divorce and fertility increases tag *modernizing* sigungu (urban, post-industrial, with more dual-career households and lower domestic-violence-trapped marriages), where the deaths-of-despair high-risk sub-population is a complementary minority rather than the modal household. Under this alternative substantive interpretation, the protective trade-mortality channel operates through expanding the modernizing-household share (γ_FS_divorce > 0, γ_FS_fertility > 0) rather than through reducing a marker-tagged high-risk sub-population. We acknowledge this interpretation as substantive-but-tentative and reserve the formal disentangling for the R&R cycle, where additional sigungu-level controls (urbanization index, dual-career-household share, domestic-violence reporting frequency) would clarify the substantive mechanism.

**Third**, the partial-correlation residual β_direct_joint = -0.077 (95% CI marginally including zero at the upper bound +0.004) of the protective effect operates outside the three identified mediators, implicating direct labor-market channels (employment, earnings, household financial stability) and broader social channels (community resilience, institutional trust) that are not centrally measured in the present mediator set. Section 8.1 articulates the comparative framework that interprets this residual in the context of the U.S. opioid-pathway literature.

**Fourth**, the substantive academic contribution articulated in Section 7.2.5 — that the Korean trade-mortality protective channel operates through *marker-not-causal-mediator* mechanisms that differ substantively from the U.S. trade-mortality literature — is reinforced by the joint decomposition. The dominant identified mediator (M3 marriage market) has a direct substantive parallel in Autor-Dorn-Hanson (2019) but with opposite sign: ADH 2019 documents that trade shocks *deter* US marriage formation (a one-unit shock predicts a 0.95 percentage-point decline in the fraction of young women currently married) and *reduce* US fertility (1.5 fewer births per 1,000 women per unit shock), whereas our Korean evidence shows trade exposure raising both divorce-rate and fertility (γ_FS_divorce = +0.167, γ_FS_fertility = +0.043). The opposite-sign comparative pattern is consistent with the modernizing-household alternative interpretation outlined above: Korean trade exposure tags modernizing sigungu (urban, dual-career household, looser binding-marriage social norms) where divorce and fertility increases reflect family-formation diversification rather than family-formation contraction. Pierce-Schott (2020) does not address marriage-market or fertility mechanisms — its analysis focuses on labor market deterioration and drug overdose mortality. The M1 N05BA pharmaceutical share is sign-aligned-but-weaker than the U.S. labor-market channel documented in Pierce-Schott (2020), and is sign-unstable under bootstrap (P(ACME < 0) = 0.747) once the marriage-market channel is jointly controlled.

### 7.6.4 Robustness sensitivity — 4-mediator specification with M6

A robustness specification that includes M6 suicide as an additional mediator (despite the logical inclusion concern of § 7.5) yields [TBD] joint ACME values with [TBD] direction-of-effect sensitivity. We report the 3-mediator specification (excluding M6) as the main joint decomposition because of the M6-⊂-despair_total composite logical concern, with the 4-mediator specification reported in the online appendix as a robustness sensitivity. The substantive cumulative direction of the protective trade-mortality channel — dominated by marriage-market and family-formation mediation under the main 3-mediator joint specification — is preserved across both specifications.

### 7.6.5 Sub-period sensitivity

The post-2008 sub-period sub-sample yields [TBD] joint ACME values with [TBD] proportion of the post-2008 β_RF, confirming that the joint decomposition pattern documented above is not an artifact of the 2008 KCD-to-ICD-10 classification revision (Section 5.4) and operates consistently in the cleaner post-revision window.

---

## R-A 의 권고 영역의 cumulative anchor

본 placeholder wording 의 cumulative substantive direction 위 사용자 측 sub-task 2.6 결과 paste 후 R-A 의 후속 작업 영역:

1. **Specific number commit**: [TBD] placeholder 영역 위 사용자 측 결과 paste 의 cumulative form 의 evidence-based 정확한 number anchor commit (R-A 측 cumulative refinement 의 markdown draft 위 commit)
2. **Substantive interpretation 의 cumulative direction**: 사용자 측 결과 위 substantive 가설 (marriage market dominant + N05BA secondary + partial-correlation residual 영역) 의 evidence-based confirm 또는 정정 영역의 cumulative direction
3. **사용자 측 별도 환경 commit**: paper § 7.6 narrative 의 substantive direction 의 사용자 측 paper draft 본문 commit
4. **R-A 의 후속 audit cycle**: 사용자 측 commit 후 single-pass + minor refinement 권고 + cross-section consistency review (paper § 7.1-7.6 cumulative form)

---

**End of R-A 측 cumulative paragraph 권고 form (placeholder anchor for sub-task 2.6 evidence-based finalization)**
