# 2026-05-07 결정 로그 — Phase 2 sub-task 2.6 joint multi-mediator decomposition + γ_FS / δ_M sign 영역의 fundamental 정정 + 5번째 trust violation **Author**: 정재헌 (가천대 경제학) / 공동저자 mode
**Phase**: Phase 2 sub-task 2.6 (joint multi-mediator decomposition + partial-correlation residual)
**대상 파일**:
- `4_results/joint_multimediator_decomposition.parquet` (3 mediator joint ACME, 4902 bytes)
- `4_results/joint_multimediator_partial_residual.parquet` (1000-rep bootstrap, 100,045 bytes)
- `2_scripts/build_panel/2_6_joint_multimediator.py` (Python ETL)
- `2_scripts/build_panel/run_subtask_2_6.ps1` (PowerShell wrapper)
- `7_paper/draft_proposals/section_7_3_to_7_5_proposal_2026-05-07.md` (γ_FS sign 영역의 fundamental 정정)
- `7_paper/draft_proposals/section_7_6_proposal_2026-05-07.md` (specific number cumulative refinement)
- `memory/feedback_subagent_label_ambiguity.md` (5번째 trust violation case) --- ## 1. 결정 (a) Joint multi-mediator decomposition (M1 + M3 divorce + M3 fertility, n = 133, G = 12) 의 cumulative substantive 영역의 evidence-based maximum form 도달. (b) **γ_FS / δ_M sign 영역의 fundamental 정정**: sub-task 2.5 의 보고 위 substantive label ambiguity 의 cumulative form (β = -0.660 = δ_M, NOT γ_FS) 의 evidence-based 정정 — actual γ_FS = +0.142 / +0.046 (positive), δ_M = -0.660 / -0.713 (negative), ACME = γ_FS × δ_M = -0.094 / -0.033 (산술적 정합 ✅). (c) Modernizing-household alternative interpretation 의 cumulative substantive direction 의 paper § 7.3.2 narrative 위 commit (positive γ_FS = trade-induced expansion of modernizing-household share). (d) M1 N05BA univariate 13.4% → joint 6.5% collapse of standalone causal role 의 evidence-based finding (anxiety marker NOT primary causal mediator). (e) Cumulative joint ACME 59.2% / partial-correlation residual β_direct_joint 41.7% 의 cumulative substantive direction 의 maximum form 도달. (f) 5번째 trust violation case 의 cumulative honest disclosure + memory commit. ## 2. 근거 ### 2.1 Joint specification (n=133, G=12) | Mediator | γ_FS (joint) | F_FS | δ_M_joint | t_clu | ACME_joint | prop_main | bootstrap CI | P(<0) |
|----------|------------:|-----:|---------:|------:|-----------:|----------:|-------------|------:|
| M1 N05BA | -0.213 | 15.81 | +0.057 | +1.08 (n.s.) | -0.012 | 6.5% | [-0.023, +0.018] | 0.747 ⚠️ |
| **M3 divorce** | **+0.167** | **69.25** | **-0.427** | **-2.75** | **-0.071** | **38.4%** | [-0.151, -0.014] excl. zero ✅ | **0.993** |
| M3 fertility | +0.043 | 7.37 | -0.606 | -4.36 | -0.026 | 14.2% | [-0.062, +0.002] | 0.958 | - β_direct_joint = -0.0772, cluster t = -2.12, 95% CI [-0.164, +0.004] (marginal upper bound)
- β_RF_joint_sample = -0.187 (≈ main β_RF -0.185, no sample-selection 영향)
- Cumulative joint ACME = -0.110 = **59.2%** of β_RF_main
- partial-correlation residual β_direct_joint / β_RF_main = **41.7%**
- Univariate sum 94.7% → joint 59.2% = **35.5pp drop = overlap evidence** ### 2.2 γ_FS / δ_M sign 영역의 fundamental 정정 | Mediator | 보고 위 cumulative form (label ambiguity) | actual evidence-based form (multi_mediator_dghp_decomposition.parquet column) |
|----------|---------------------------------------------------|----------------------------------------------------------------------------|
| Marriage | "γ_FS = -0.290, F = 5.95" | γ_FS = **+0.034**, F_FS = 5.95, δ_M = **-0.290** |
| **Divorce** | "γ_FS = -0.660, F = 55.73" | γ_FS = **+0.142**, F_FS = 55.73, δ_M = **-0.660** |
| **Fertility** | "γ_FS = -0.714, F = 14.26" | γ_FS = **+0.046**, F_FS = 14.26, δ_M = **-0.713** |
| Suicide | "γ = -0.042, F = 2.38" | γ_FS = -0.042 (correct), δ_M = +0.563 | **Substantive 정정 영역**:
- Trade exposure → divorce ↑ (γ_FS = +0.142), divorce ↑ → mortality ↓ | z_x (δ_M = -0.660), ACME = -0.094 protective ✅
- Trade exposure → fertility ↑ (γ_FS = +0.046), fertility ↑ → mortality ↓ | z_x (δ_M = -0.713), ACME = -0.033 protective ✅ ### 2.3 Modernizing-household alternative interpretation paper § 7.3.2 narrative 의 substantive direction 위 trade exposure 가 modernizing-household share 확대 → divorce + fertility 증가 (positive γ_FS) → cross-sigungu mortality 감소 (negative δ_M) 의 cumulative form. 직전 markdown draft 의 narrative ("trade-induced labor market stabilization → fewer divorces") 의 substantive direction 의 cumulative reverse 영역의 fundamental 정정. ### 2.4 M1 N05BA univariate vs joint collapse | 영역 | univariate | joint |
|------|-----------:|------:|
| ACME proportion of β_RF_main | 13.4% | **6.5%** |
| δ_M sign | +0.111 (significant) | +0.057 (n.s.) |
| Bootstrap P(ACME < 0) | (univariate stable) | **0.747** ⚠️ unstable | **Substantive 함의**: M1 anxiety marker channel 의 univariate ACME 가 M3 divorce channel 에 cumulative 흡수 — benzodiazepine prescription + divorce 가 동일한 anxiety-related family-stress 영역 의 cumulative tag. paper § 7.2.5 의 "marker NOT primary causal mediator" framing 의 cumulative consistency 의 evidence-based confirm. ## 3. Anchor papers - DGHP 2017 NBER WP 23209 — single-IV mediation framework
- Pierce-Schott 2020 + ADH 2019 — U.S. opioid-pathway substantive 차이
- Case-Deaton 2015 PNAS — deaths-of-despair definition
- Stock-Yogo (2005) — weak IV cutoffs ## 4. 영향 ### 4.1 paper § 7.3-7.5 markdown draft 의 fundamental 정정 `section_7_3_to_7_5_proposal_2026-05-07.md` 의 cumulative refinement:
- § 7.3.2 first-stage γ_FS sign 영역의 fundamental 정정 (-0.290/-0.660/-0.714 → +0.034/+0.142/+0.046)
- § 7.3.2 substantive interpretation 의 cumulative refinement (modernizing-household alternative framework)
- § 7.3.3 DGHP decomposition 위 γ_FS / δ_M dual notation 의 명시적 anchor ### 4.2 paper § 7.6 markdown draft 의 specific number commit `section_7_6_proposal_2026-05-07.md` 의 cumulative refinement:
- Joint sample n = 133, G = 12 의 명시적 anchor
- β_direct_joint = -0.0772 (CI [-0.164, +0.004]) + 41.7% partial-correlation residual
- M1 collapse + M3 divorce dominant + 35.5pp overlap evidence
- δ_M < 0 의 modernizing-household alternative interpretation 의 cumulative substantive direction ### 4.3 5번째 trust violation case 의 memory commit `memory/feedback_subagent_label_ambiguity.md` 의 cumulative anchor + MEMORY.md update. ## 5. Sensitivity ### 5.1 δ_M < 0 의 substantive interpretation 의 3 alternative (a) Modernizing-household marker (권고 main interpretation)
(b) Korean secular demographic-transition + sigungu-specific heterogeneity correlated with trade exposure
(c) Sample-specific cross-sigungu noise (9-year M3 long-difference window 의 limited cumulative form) R&R cycle 위임 영역: sigungu-level controls (urbanization + dual-career + domestic violence reporting) 의 cumulative carry. ### 5.2 M1 N05BA collapse 의 cumulative substantive direction joint specification 위 M1 standalone causal role 의 collapse → § 7.2.5 narrative ("marker NOT primary causal mediator") 의 cumulative consistency 의 evidence-based form. paper § 7.2.5 narrative 의 cumulative carry 의 정통 form. ## 6. 후속 step ### 6.1 즉시 - 사용자 측 paper § 7.3-7.5 commit (측 cumulative refinement form 의 substantive direction 위 사용자 측 별도 환경 commit)
- 사용자 측 paper § 7.6 commit (측 cumulative refinement form 의 substantive direction 위 사용자 측 별도 환경 commit)
- 사용자 측 § 6 footnote commit (M3 baseline 2000-2002 fallback) ### 6.2 Mid-term (Phase 3 — paper finalization) - paper § 7.1-7.6 cumulative consistency review (audit cycle)
- paper § 5 + § 6 + § 8 cross-section consistency review
- paper § 1-2 abstract + introduction 의 cumulative finalization ### 6.3 Long-term (Phase 4-7) - PAP v4.6 update
- Cover letter draft for KER July 2026
- Replication archive (sub-task 2.2-2.6 cumulative form) --- **Audit-after-action 결과** (2026-05-07 audit cycle):
- Sub-task 2.6 cumulative artifact 의 evidence-based 정합 form ✅
- γ_FS / δ_M sign 영역의 fundamental 정정 ✅
- ACME = γ_FS × δ_M 산술적 정합 ✅ (M1 -0.012 + M3 divorce -0.071 + M3 fertility -0.026 + M6 suicide -0.023)
- Modernizing-household alternative interpretation cumulative direction commit ✅
- 5번째 trust violation case memory commit ✅
- 한자 사용 부재 ✅ **Status**: COMMIT (γ_FS / δ_M sign 정정 + joint specification + memory + draft 정정 cumulative form)
**다음 turn**: 사용자 측 paper § 7.3-7.5 + § 7.6 commit + 후속 audit cycle (paper § 7.1-7.6 cumulative consistency review)
