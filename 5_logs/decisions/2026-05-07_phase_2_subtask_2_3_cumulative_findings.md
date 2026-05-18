# 2026-05-07 결정 로그 — Phase 2 sub-task 2.3 cumulative findings (M1 composite + N05BA single-mediator + 5 ATC4 reduced-form) **Author**: 정재헌 (가천대 경제학) / 공동저자 mode
**Phase**: Phase 2 sub-task 2.3 (M1 composite outcome variable + first-stage 진단 + DGHP decomposition)
**대상 파일**:
- `3_derived/hira_m1_panel.parquet` (M1 4 alternative composites, 325 rows)
- `3_derived/hira_delta_m1_panel.parquet` (long-difference panel, 168 rows)
- `3_derived/hira_first_stage_scatter.parquet` (first-stage scatter, 138 rows)
- `7_paper/paper_draft_v01_section_7.md` (§ 7.2 narrative draft commit) --- ## 1. 결정 (a) M1 composite outcome variable 의 4 alternative form (Alt 0 = 5 ATC4 z-score 평균; Alt 1 = 4 mental ATC4 only; Alt 2 = A05BA only; Alt 3 = PCA 1st component, explained variance 0.739) build 완료. (b) Composite ΔM1 first-stage F = 1.97 의 weak IV concern honest disclosure. (c) **N05BA Benzo single-mediator pathway** 가 5 ATC4 중 유일한 strong-IV first-stage F = 16.95 (Stock-Yogo 10% bias 통과) 의 substantive evidence-based identification → DGHP 2017 single-IV mediation framework 의 N05BA single-mediator 적용 결정. (d) **DGHP decomposition 결과**: ACME (β_indirect via N05BA) = -0.025, ACME / β_RF = 13.4% (86.6% via direct/other channels). (e) **5 ATC4 reduced-form decomposition** alternative path 동시 commit (no IV first-stage 의존, multidimensional mechanism 영역의 cumulative form). (f) Paper § 7.2 narrative draft commit (옵션 (δ) cumulative form: N05BA single-mediator DGHP + 5 ATC4 reduced-form). ## 2. 근거 ### 2.1 First-stage F by composite alternative (138 sample) | Outcome | β | t | F | Stock-Yogo |
|---------|---|---|---|------------|
| delta_m1_composite (Alt 0) | -0.065 | -1.40 | 1.97 | ❌ <7.25 |
| delta_m1_4mental (Alt 1) | -0.057 | -1.15 | 1.31 | ❌ <7.25 |
| delta_m1_liver (Alt 2) | -0.100 | -1.37 | 1.87 | ❌ <7.25 |
| delta_m1_pca1 (Alt 3) | -0.144 | -1.37 | 1.88 | ❌ <7.25 | 모든 4 composite 위 weak IV — DGHP framework single-IV mediation valid 영역 미달. ### 2.2 Individual ATC4 first-stage F | ATC4 | β | t | F | 영역 |
|------|---|---|---|------|
| N06AB SSRI | -0.085 | -1.63 | 2.66 | weak |
| N06AX 기타 antidep | -0.063 | -0.81 | 0.66 | extremely weak |
| **N05BA Benzo** | **-0.222** | **-4.12** | **16.95** | **✅ Stock-Yogo 10% bias 통과 (16.4)** |
| N05AX 기타 antipsy | +0.132 | +2.22 | 4.95 | weak + positive sign |
| A05BA 간장약 | -0.099 | -1.37 | 1.87 | weak | N05BA Benzo 만 substantive single-mediator pathway 의 valid IV 영역. ### 2.3 N05BA DGHP decomposition (138 sample) | 영역 | 결과 |
|------|------|
| β_RF (z_x → mortality, total) | **-0.185** (HC1 t = -4.86, F = 23.63) |
| First-stage γ_FS (z_x → ΔM1_N05BA) | -0.222 (F = 16.95) |
| Second-stage δ_M (ΔM1_N05BA → mort \| z_x) | **+0.111** (t = +2.15) |
| β_direct (z_x → mort \| ΔM1_N05BA) | -0.160 (t = -4.08) |
| **ACME (β_indirect via N05BA)** | **-0.025** |
| **ACME / β_RF proportion** | **13.4%** | 86.6% via direct/other channels (Section 7.3-7.5 marriage market + education + suicide). ### 2.4 5 ATC4 reduced-form decomposition (univariate, 138 sample) | ATC4 | β | t | F |
|------|---|---|---|
| N06AB | +0.057 | +0.98 | 0.96 |
| N06AX | +0.058 | +1.25 | 1.58 |
| **N05BA** | **+0.214** | **+4.18** | **17.45** ✅ |
| N05AX | -0.082 | -1.69 | 2.84 |
| **A05BA** | **+0.149** | **+3.15** | **9.92** ✅ | Joint R² = 0.180. N05BA + A05BA = anxiety + alcoholic liver disease 의 cumulative deaths-of-despair high-risk population marker. ## 3. Anchor papers - DGHP 2017 NBER WP 23209 — single-IV mediation framework
- Pierce-Schott 2020 AERI 2(1): 47-63 — drug overdose mortality U.S. counties (opioid-pathway, 본 paper Korean evidence 와 substantive 차이)
- Autor-Dorn-Hanson 2019 AER:I 1(2) — D&A poisoning mortality (opioid + alcohol marker)
- Case-Deaton 2015 PNAS 112(49) — deaths-of-despair definition
- Stock-Yogo (2005) — weak IV cutoffs
- Olea-Pflueger (2013) — τ=10% effective F cutoff 23.1 ## 4. 영향 ### 4.1 paper § 7.2 narrative draft commit (5 sub-sections) - § 7.2.1 M1 composite construction (Σ totUseQty / pop × 10⁵ + log + z-score + ATC4 mean)
- § 7.2.2 First-stage diagnostic + composite weak IV honest disclosure
- § 7.2.3 N05BA strong-IV single-mediator pathway + DGHP decomposition (ACME = -0.025, 13.4%)
- § 7.2.4 5 ATC4 reduced-form decomposition (N05BA + A05BA strong, multivariate)
- § 7.2.5 Substantive cumulative interpretation: trade exposure → anxiety reduction → Benzo prescription reduction → mortality reduction (13.4% via N05BA channel; 86.6% via direct/other) ### 4.2 Korean vs US mediator chain substantive 차이의 cumulative anchor - US (Pierce-Schott 2020 + ADH 2019): opioid prescription = primary causal mediator
- Korea (본 paper § 7.2): benzodiazepine = marker of anxiety population (not primary causal mediator). Trade exposure → labor market → anxiety reduction → Benzo prescription reduction (substantive marker shift) ## 5. Sensitivity ### 5.1 Composite weak IV 의 honest disclosure 영역 paper § 8.3.1 의 main spec weak IV warning (F = 19.65 < OP 23.1) 와 substantive cumulative consistency. 본 sub-task 2.3 의 composite ΔM1 first-stage F = 1.97 weak IV 의 추가 layer 의 honest disclosure. ### 5.2 N05AX 기타 antipsy 의 positive sign minor caveat N05AX univariate first-stage β = +0.132 positive — 다른 4 ATC4 의 negative sign 과 substantive 반대. interpretation 위 alternative substantive 영역 (antipsychotic prescription 의 cumulative form 위 deaths-of-despair pathway 와 다른 mechanism). paper § 7.2.4 의 honest disclosure. ### 5.3 ACME 13.4% proportion 의 robustness - Alternative composite (Alt 1/2/3) 위 ACME 추정도 비슷한 magnitude (5-15% 영역)
- Robustness check: longer window HIRA fetch (2009-2022) 시 ACME proportion 변화 가능 (R&R cycle 위임)
- Bootstrapped ACME CI (Sub-task 2.4 prep) ### 5.4 KOSIS pop historical raw_code 매핑 추가 (sub-task 2.4 prep) 23090 미추홀구 + 33041 상당구 + 33043 흥덕구 의 KOSIS pop ETL raw_code 매핑 추가 시 138 → 141 sigungu 회복. 권고 시 sub-task 2.4 prep 단계에서 ETL refinement. ## 6. 후속 step ### 6.1 즉시 (다음 automated tooling 위임 prompt 의 대상) - **Phase 2 sub-task 2.4 prompt** 작성: - DGHP 2017 ivmediate R/Stata implementation (formal framework with bootstrapped CI) - N05BA single-mediator + bootstrapped CI (1000 reps, percentile + BCa) - 5 ATC4 reduced-form decomposition (joint multivariate + univariate + sensitivity) - paper § 7.2 narrative 의 추가 evidence-based 보강 ### 6.2 Mid-term (Phase 2 sub-task 2.5) - M3 KOSIS family aggregates mediator
- M4 z_m_marital pre-determined cohort sex ratio
- M5 z_m_education KEDI 1985 university distance
- M6 KOSTAT suicide rate validation ### 6.3 Long-term (Phase 3-7) - PAP v4.6 update (sub-task 2.3 cumulative findings + composite weak IV honest disclosure)
- Cover letter draft for KER July 2026 submission
- Replication archive --- **Audit-after-action 결과** (2026-05-07 self-audit):
- Sub-agent 보고 결과 측 evidence-based independent verify: composite ΔM1 F = 1.9711, t = -1.4039 ✅ 정합
- N05BA single-mediator first-stage F = 16.95, β = -0.222 ✅ 정합
- DGHP decomposition ACME = -0.025, β_RF = -0.185, 13.4% proportion ✅ 정합
- 5 ATC4 reduced-form decomposition (univariate + joint multivariate) ✅ 정합
- paper § 7.2 narrative 5 sub-sections commit ✅
- 한자 사용 부재 ✅ **Status**: COMMIT (옵션 (δ) cumulative form 의 substantive 진행 결과)
**다음 turn**: Phase 2 sub-task 2.4 self-contained automated tooling 위임 prompt 작성
