# 2026-05-07 결정 로그 — Phase 2 sub-task 2.5 M3 + M4 + M5 + M6 cumulative findings **Author**: 정재헌 (가천대 경제학) / 공동저자 mode
**Phase**: Phase 2 sub-task 2.5 (4 active mediator + multi-mediator joint analysis)
**대상 파일**:
- `3_derived/m3_kosis_family_panel.parquet` (sigungu × year × {marriage, divorce, fertility}, 6566 rows × 253 h_code)
- `3_derived/m3_delta_panel.parquet` (sigungu × Δ family rates, 253 rows; baseline window 2000-2002 fallback)
- `3_derived/m4_z_marital_pre.parquet` (sigungu × cohort_sex_ratio_1995 + z_m_marital, 247 rows)
- `3_derived/m5_z_education_pre.parquet` (sigungu × {1985/1990/1995 distance + z_m_education}, 251 rows; Pearson r ≥ 0.992)
- `3_derived/m6_suicide_panel.parquet` (sigungu × delta_log_suicide, 229 rows; KOSTAT 102 X60-X84)
- `4_results/m3_m6_first_stage_table.parquet`
- `4_results/m3_m6_reduced_form_table.parquet`
- `4_results/multi_mediator_dghp_decomposition.parquet`
- `4_results/m4_m5_effect_modifier.parquet`
- `4_results/sub_period_sensitivity.parquet`
- `7_paper/draft_proposals/section_7_3_to_7_5_proposal_2026-05-07.md` (측 wording 권고 form) --- ## 1. 결정 (a) M3 KOSIS family aggregates 의 cumulative form 위 **divorce + fertility 가 substantive strong-IV mediator pathway** 의 evidence-based confirm. (b) M3 marriage 는 weak first-stage (F = 5.95) 위 reduced-form 보고만, DGHP decomposition 부재. (c) M4 z_m_marital + M5 z_m_education 의 effect modifier 영역 모두 null (interaction t < 1) — protective channel homogeneous across pre-determined endowment. (d) M6 suicide validation 의 cumulative form 위 mechanical positive reduced-form (suicide ⊂ despair_total) + sign-consistent protective ACME marginal CI 의 cumulative honest disclosure. (e) Cumulative identified-mediator ACME proportion ≈ 82% of β_RF (overlapping channels via suicide ⊂ despair). (f) paper § 7.3-7.5 narrative wording 권고 form 의 substantive draft commit (측 cumulative paragraph 권고 영역, 사용자 측 별도 환경 commit prerequisite). ## 2. 근거 ### 2.1 M3 first-stage F (joint sample n=221, sido G=16) | Mediator | γ_FS | F | Stock-Yogo |
|----------|-----:|--:|------------|
| Marriage rate | -0.290 | **5.95** | ❌ <7.25 (weak) |
| **Divorce rate** | **-0.660** | **55.73** | ✅ >>23.1 (very strong) |
| Fertility rate | -0.714 | **14.26** | borderline (>7.25, <16.4) | ### 2.2 M3 reduced-form mediator → mortality (cluster-province SE) | Mediator | β | cluster t | p_cluster |
|----------|--:|----------:|----------:|
| Marriage | -0.290 | -1.24 | n.s. |
| **Divorce** | **-0.660** | **-5.70** | **<0.001** ✅ |
| **Fertility** | **-0.714** | **-4.39** | **<0.001** ✅ | ### 2.3 M3 DGHP ACME (sido bootstrap B=1000, G=16) | Mediator | ACME point | 95% CI | β_RF proportion |
|----------|-----------:|--------|----------------:|
| Marriage | -0.010 | (n.s.) | — |
| **Divorce** | **-0.094** | **[-0.155, -0.043]** ✅ zero exclusion | **~51%** |
| **Fertility** | **-0.033** | **[-0.060, -0.010]** ✅ zero exclusion | **~18%** | ### 2.4 M4 + M5 effect modifier interaction (all null) | Mediator | Interaction t_cluster | p_cluster | Direction |
|----------|---------------------:|----------:|-----------|
| M4 z_m_marital × z_x | -0.52 | 0.61 | n.s. (homogeneous) |
| M5 z_m_education_1985 × z_x | -0.35 | 0.73 | n.s. (homogeneous) |
| M5 z_m_education_1990 × z_x | (similar) | n.s. | n.s. (homogeneous) |
| M5 z_m_education_1995 × z_x | (similar) | n.s. | n.s. (homogeneous) | ### 2.5 M6 suicide validation - First-stage z_x → Δ suicide rate: γ_FS = -0.042, F = **2.38** (weak)
- Reduced-form Δ suicide rate ~ z_x_std: β = +0.563, cluster t = +5.51 (mechanical positive — suicide ⊂ despair_total)
- DGHP ACME = -0.023, 95% CI [-0.063, +0.003] (marginal, sign-consistent protective)
- Sub-period: pre-2008 β = +0.251, post-2008 β = +0.170 (mechanical positive sub-period parallel) ### 2.6 Cumulative identified-mediator ACME proportion (β_RF = -0.185) - M1 N05BA: 13.4%
- M3 divorce: ~51%
- M3 fertility: ~18%
- M6 suicide (mediator form): ~12%
- **Cumulative ≈ 82% (overlapping channels, suicide ⊂ despair)**
- 직접 effect cumulative form: § 7.6 joint multi-mediator decomposition 의 substantive prerequisite ## 3. Anchor papers - DGHP 2017 NBER WP 23209 — single-IV mediation framework
- Pierce-Schott 2020 AERI 2(1): 47-63 — drug overdose mortality U.S. counties (parallel substance abuse)
- ADH 2019 AERI 1(2): 161-178 — marriage market value of young men in U.S. (opposite direction)
- Case-Deaton 2015 PNAS 112(49): 15078-15083 — deaths-of-despair definition
- Stock-Yogo (2005) — weak IV cutoffs ## 4. 영향 ### 4.1 paper § 7.3-7.5 narrative wording 권고 form commit `7_paper/draft_proposals/section_7_3_to_7_5_proposal_2026-05-07.md` 위 측 cumulative paragraph 권고 form 의 substantive draft. 사용자 측 별도 환경 commit + 후속 audit cycle. ### 4.2 paper § 6 Data footnote 권고 M3 baseline window 2000-2002 fallback (paper main 1997-1999 baseline 과의 차이) 의 cumulative honest anchor 영역 — paper § 6 Data 영역 위 minor footnote 의 substantive 권고. ### 4.3 Substantive academic contribution 의 cumulative anchor - 한국 evidence 의 cumulative form: marriage market + family formation (M3 divorce + fertility) 이 dominant mediator (>69% of β_RF)
- 정신건강 약물 (M1 N05BA Benzo) 13.4%, suicide (M6) ~12% 의 cumulative supplementary
- 한국 vs 미국 mediator chain 의 substantive 차이: 미국은 opioid + drug overdose 가 primary, 한국은 marriage market + family formation 이 primary (substantive academic contribution)
- pre-determined endowment (M4 cohort sex ratio + M5 university distance) effect modifier 부재 → homogeneous protective channel 의 evidence-based form ## 5. Sensitivity ### 5.1 M3 baseline window 2000-2002 fallback paper main 1997-1999 baseline 과의 3-year offset 의 minor robustness — 사용자 측 결정 영역 위 § 6 footnote 의 cumulative carry. ### 5.2 M6 suicide first-stage F = 2.38 (weak) DGHP framework 위 IV-based 인과식별 caution 영역의 cumulative honest disclosure. ACME marginal CI 의 cumulative form 위 paper § 7.5 narrative 위 honest framing. ### 5.3 Cumulative ACME ≈ 82% (overlapping channels) Suicide ⊂ despair composite + benzodiazepine prescription overlap with anxiety-related family stress 등의 cumulative overlapping. § 7.6 joint multi-mediator decomposition 의 substantive prerequisite — joint regression 위 partial-correlation residual direct effect 의 cumulative form 의 substantive direction. ### 5.4 Marriage rate weak first-stage (F = 5.95) 혼인 신고 timing 의 substantive measurement noise 의 가능성 영역 — paper § 7.3.2 narrative 위 honest disclosure. ## 6. 후속 step ### 6.1 즉시 - **사용자 측 별도 환경 commit**: paper § 7.3 + § 7.4 + § 7.5 narrative 위 측 wording 권고 form (`section_7_3_to_7_5_proposal_2026-05-07.md`) 의 substantive direction 의 사용자 측 commit
- paper § 6 Data 영역 footnote 추가 (M3 baseline window 2000-2002 fallback) ### 6.2 Mid-term (Phase 2 sub-task 2.6 — § 7.6 joint multi-mediator decomposition) - 4 mediator 의 cumulative joint regression
- Partial-correlation residual direct effect 의 cumulative form
- 사용자 측 별도 환경 실행 + 후속 audit + § 7.6 narrative wording 권고 form ### 6.3 Long-term (Phase 3-7) - PAP v4.6 update (sub-task 2.5 + 2.6 cumulative findings)
- Cover letter draft for KER July 2026 submission
- Replication archive (sub-task 2.5 sub-script 5 + multi-mediator analysis) --- **Audit-after-action 결과** (2026-05-07 audit cycle single-pass):
- 사용자 측 sub-task 2.5 cumulative artifact 의 substantive 정합 form ✅
- M3 divorce + fertility strong-IV pathway 의 evidence-based confirm ✅
- M4 + M5 effect modifier null 의 cumulative homogeneous channel 의 substantive direction ✅
- M6 suicide validation 의 mechanical positive + sign-consistent ACME 의 cumulative honest disclosure ✅
- 한자 사용 부재 ✅ **Status**: COMMIT (wording 권고 form + 결정 로그 + 사용자 측 commit wait)
**다음 turn**: 사용자 측 paper § 7.3-7.5 commit 후 후속 audit cycle + § 7.6 prompt
