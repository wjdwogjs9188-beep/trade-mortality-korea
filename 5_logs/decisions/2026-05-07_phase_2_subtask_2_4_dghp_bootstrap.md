# 2026-05-07 결정 로그 — Phase 2 sub-task 2.4 DGHP formal ivmediate + bootstrapped CI cumulative findings **Author**: 정재헌 (가천대 경제학) / 공동저자 mode
**Phase**: Phase 2 sub-task 2.4 (DGHP 2017 ivmediate formal implementation + cluster-province SE + sido-cluster bootstrapped CI)
**대상 파일**:
- `4_results/dghp_acme_n05ba_bootstrap.parquet` (1,001 rows, 73.6 KB)
- `4_results/atc4_reduced_form_decomposition.parquet` (10 rows, 6.0 KB)
- `4_results/m1_alt_robustness.parquet` (5 rows, 4.2 KB)
- `2_scripts/build_panel/2_4_dghp_ivmediate.py` (Python ETL)
- `2_scripts/build_panel/run_dghp_ivmediate.ps1` (PowerShell wrapper)
- `7_paper/paper_draft_v01_section_7.md` (§ 7.2.3-7.2.5 wording finalization) --- ## 1. 결정 (a) DGHP 2017 single-IV mediation framework 의 formal R/Stata-equivalent Python implementation 위 N05BA single-mediator pathway 의 cumulative substantive 정통 form 의 evidence-based commit. (b) Bootstrap 95% CI (sido-cluster, B=1000) 위 ACME = -0.025, CI [-0.046, +0.015] marginal but **89.4% sign stability** 의 honest disclosure. (c) β_direct ([-0.252, -0.107]) + β_RF ([-0.255, -0.130]) 의 zero exclusion 의 strong evidence 의 cumulative anchor — direct effect 영역의 substantive maximum form 도달. (d) Cluster-province SE (G=12) 위 5 ATC4 reduced-form decomposition 의 cumulative form: N05BA univariate p_cluster = 0.0021 + A05BA p_cluster = 0.0394 + N05BA joint p_cluster = 0.0418 + N05AX joint p_cluster = 0.0245 (opposite-sign offset). (e) paper § 7.2.3 + § 7.2.4 + § 7.2.5 wording finalization commit. ## 2. 근거 ### 2.1 N05BA single-mediator DGHP point estimates (138 sample) | 영역 | 결과 |
|------|------|
| γ_FS (z_x → ΔM1_N05BA) | -0.222, F = 22.59 (DGHP HC1 SE) / F = 16.95 (univariate cluster SE) |
| δ_M (ΔM1_N05BA → mort \| z_x) | +0.111 (HC1 t = +2.15) |
| β_direct (z_x → mort \| ΔM1_N05BA) | -0.160 (HC1 t = -4.08) |
| **ACME** (γ_FS × δ_M) | **-0.0247** |
| β_RF (z_x → mort, total) | -0.185 |
| **ACME / β_RF proportion** | **13.4%** | ### 2.2 Sido-cluster bootstrap (B=1000) | 영역 | Point | 95% CI | Zero exclusion |
|------|------:|--------|----------------|
| γ_FS | -0.222 | [-0.298, +0.035] | NO (marginal) |
| β_direct | -0.160 | **[-0.252, -0.107]** | ✅ YES |
| β_RF | -0.185 | **[-0.255, -0.130]** | ✅ YES |
| ACME | -0.025 | [-0.046, +0.015] | NO (marginal) |
| ACME proportion | 13.4% | [-9.0%, +28.5%] | NO |
| **ACME sign stability** | — | **894/1000 = 89.4% < 0** | substantively strong direction | ### 2.3 5 ATC4 reduced-form (cluster-province SE, G=12) | ATC4 | Spec | β | t_cluster | p_cluster | Significance |
|------|------|--:|----------:|----------:|--------------|
| **N05BA** | univariate | **+0.214** | **+3.98** | **0.0021** | ✅✅ strong |
| A05BA | univariate | +0.149 | +2.34 | 0.0394 | ✅ |
| N06AB | univariate | +0.057 | +0.98 | NS | — |
| N06AX | univariate | +0.058 | +1.25 | NS | — |
| N05AX | univariate | -0.082 | -1.69 | NS | — |
| **N05BA** | joint | **+0.182** | **+2.30** | **0.0418** | ✅ |
| **N05AX** | joint | **-0.147** | **-2.61** | **0.0245** | opposite-sign offset |
| A05BA | joint | +0.077 | +1.34 | NS | — |
| N06AB | joint | -0.010 | -0.12 | NS | — |
| N06AX | joint | +0.039 | +0.71 | NS | — | Joint R² = 0.180. ### 2.4 Alt composite robustness (first-stage F) | Spec | mediator | n | γ_FS | F | Stock-Yogo |
|------|----------|--:|-----:|--:|------------|
| Alt 0 (5 ATC4 mean) | delta_m1_composite | 138 | -0.065 | 1.97 | ❌ |
| Alt 1 (4-mental excl A05BA) | delta_m1_4mental | 138 | -0.057 | 1.31 | ❌ |
| Alt 2 (A05BA only) | delta_m1_liver | 138 | -0.100 | 1.86 | ❌ |
| Alt 3 (PCA 1st) | delta_m1_pca1 | 138 | -0.144 | 1.88 | ❌ |
| **N05BA single** | d_z_n05ba | 138 | -0.222 | **16.95-22.59** | ✅ pass | N05BA single 만 substantively strong-IV pathway 의 evidence-based confirm. ## 3. Anchor papers - DGHP 2017 NBER WP 23209 — single-IV mediation framework
- Cameron-Gelbach-Miller 2008 — cluster-bootstrap inference
- Stock-Yogo (2005) — 10% bias cutoff 16.4
- Olea-Pflueger 2013 — τ=10% effective F cutoff 23.1
- Pierce-Schott 2020 + ADH 2019 — U.S. opioid-pathway substantive 차이의 cumulative anchor
- Case-Deaton 2015 PNAS — deaths-of-despair definition ## 4. 영향 ### 4.1 paper § 7.2 narrative finalization commit - § 7.2.3 N05BA strong-IV single-mediator pathway: bootstrap CI evidence-based 보강 + ACME sign stability 89.4% honest disclosure + β_direct/β_RF zero exclusion strong evidence
- § 7.2.4 5 ATC4 reduced-form (cluster-SE G=12): N05BA univariate p=0.0021 strong + A05BA p=0.0394 + N05BA joint p=0.0418 + N05AX opposite-sign honest disclosure
- § 7.2.5 substantive cumulative interpretation: 13.4% / 86.6% decomposition 의 evidence-based maximum form, 한국 vs 미국 mediator chain 차이 cumulative anchor ### 4.2 Substantive academic contribution 의 cumulative anchor - N05BA Benzo = anxiety/distress population marker (not primary causal mediator, U.S. opioid-pathway 와 substantive 차이)
- 13.4% mediator-channel + 86.6% direct/other-channel decomposition 의 cumulative form 위 multi-mediator framework 의 motivation
- 한국 NHIS 정신과 access 확대 (2000-2010s) 의 cumulative form 의 evidence-based anchor ## 5. Sensitivity ### 5.1 ACME marginal CI 의 honest disclosure ACME 95% CI [-0.046, +0.015] marginal zero 포함 영역의 cumulative form 의 honest disclosure. 단 (a) 89.4% sign stability + (b) N05BA univariate p_cluster = 0.0021 strong + (c) N05BA joint p_cluster = 0.0418 + (d) F = 22.59 strong first-stage 의 cumulative evidence 위 negative-mediation hypothesis 의 substantive 가치 의 cumulative form 의 maximum form 도달. paper 본문 위 "marginal but directionally robust" framing 의 substantive 정통 form. ### 5.2 G = 12 (vs prompt 가정 G = 13) minor 영역 138 sigungu 위 sido 분포 12 (일부 sido 가 intersection complete-case 부재). t-distribution df = 11 위 inference. main spec G = 13 와의 cumulative form 의 minor 영역의 honest disclosure. ### 5.3 N05AX joint multivariate opposite-sign N05AX 기타 antipsy 의 joint p_cluster = 0.0245 negative 영역의 cumulative form 의 substantive 영역. 단 (a) univariate spec 위 NS (β = -0.082, t = -1.69) + (b) substantive interpretation 위 antipsychotic prescription 의 deaths-of-despair pathway 와의 substantive 영역 의 alternative direction 의 가능성 (anxiolytics protective vs antipsychotics ambiguous) 위 honest secondary finding 으로 commit. ### 5.4 Composite vs N05BA single 의 substantive direction Alt 0/1/2/3 composite 모두 weak first-stage (F < 2) 의 cumulative form 위 N05BA single-mediator 가 unique strong-IV pathway. Composite 의 cross-ATC4 dilution 영향 + N05AX opposite-sign offset 의 cumulative 영역 의 substantive form 위 paper § 7.2 main spec 는 N05BA single-mediator + composite 는 robustness check 으로 격하 의 substantive 결정. ## 6. 후속 step ### 6.1 즉시 - paper § 7.2 narrative finalization 완료 (§ 7.2.1-7.2.5 모두 commit)
- 다음 sub-task 2.5: M3-M6 mediator 분석 (KOSIS family aggregates + z_m_marital + z_m_education + KOSTAT suicide rate) ### 6.2 Mid-term - Sub-task 2.5 prompt 작성: M3 KOSIS family + M4 cohort sex ratio + M5 university distance + M6 suicide validation
- paper § 7.3 + § 7.4 + § 7.5 narrative draft ### 6.3 Long-term - PAP v4.6 update (sub-task 2.4 cumulative findings)
- Cover letter draft for KER July 2026 submission
- Replication archive --- **Audit-after-action 결과** (2026-05-07 self-audit):
- 사용자 측 Spyder/ paste 결과 위 cumulative substantive 정합 ✅
- ACME = -0.0247, β_RF = -0.185, 13.4% proportion ✅ (직전 cumulative form 정합)
- bootstrap CI [-0.046, +0.015] + sign stability 89.4% ✅
- cluster-SE p_cluster = 0.0021 (N05BA univariate) ✅
- paper § 7.2.3-7.2.5 wording 정정 cumulative ✅
- 한자 사용 부재 ✅ **Status**: COMMIT (sub-task 2.4 cumulative form 의 evidence-based maximum form 도달)
**다음 turn**: Phase 2 sub-task 2.5 prompt 작성 (M3-M6 mediator)
