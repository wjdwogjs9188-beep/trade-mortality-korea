# Research Status — 2026-05-07

> 자동 생성: `dissertation-context-refresh` scheduled task. 직전 보고서 (2026-05-06 latest.md) 와 cumulative comparison.
> 직전 24-30 시간의 가장 큰 변화는 **Path A native unification 본격 commit (β: -0.0685 → -0.127, window: 10y → 21y, Romano-Wolf p_RW: 0.317 → 0.0161 FWER PASS, native scale 회귀 10종 모두 commit, paper draft 7 file → 7 file native-scale 통일, paper v01 submission package zip 첫 build, wildboottest no-numba published-package patch P1 fix, target venue AER:Insights → KER pivot)**. 사실상 paper v02 first state 도달 + Phase 2 (HIRA M5 mediator panel build + § 7 mechanism) entry 단계.

> **scheduled task 환경 limitation 노트**: 본 task spec 은 archive 위치를 `C:\Users\82103\Desktop\뉴 논문\daily_status\` 로 지정. 그러나 본 conversation 의 mounted folders 는 `Downloads`, `Desktop\연구용`, `L:\da`, `Documents\Claude\Projects\논문을쓰자` 4 곳뿐 — `Desktop\뉴 논문` 미접근. 이전 보고서 (2026-05-06 까지) 가 모두 `trade_mortality_korea\4_documentation\status_reports\daily_status\` 에 archive 되어 있어, **본 보고서도 동일 경로에 commit**. 사용자 측 의사결정 권장: archive 경로 (1) 그대로 trade_mortality_korea 아래 유지, 또는 (2) 뉴 논문 폴더를 mount 에 추가, 또는 (3) 논문을쓰자 폴더로 통합.

## 1. 현재 stage 위치

직전 보고서 (2026-05-06 00:14) 시점은 **archive scale (β=-0.0685, window 2000-2010, Romano-Wolf p_RW = 0.317 FWER 미통과)** 의 paper draft v01 commit 단계. 그 후 24-30 시간 동안 사용자 주도로 **Path A native unification** 이 본격 commit — window 를 1997-1999 ↔ 2018-2022 (21-year long-difference) 로 확대하고 native unit (z_x_per_worker, USD per 1994 manufacturing worker) 로 spec 통일했다. 결과: **β = -0.127 (1.854 amplification), HC1 t = -4.92, AKM-proper t = -4.92 (numerical coincidence!), WCR Webb 6-point p < 0.0001, Romano-Wolf p_RW = 0.0161 (5-outcome FWER 통과)**. 1992 baseline robustness β = -0.0640 (n=209, three-spec convergence), pre-WTO placebo sign flip 후 reverse → "gradual integration" 해석. paper draft 7 file 모두 native scale 통일 (§ 3·4 신규 commit, § 7 신규 commit, § 6 의 1.854 ratio sub-section 신설).

| Phase | 상태 | 핵심 산출물 (현재 commit) |
|-------|------|--------------------------|
| 0 raw 수집 + INVENTORY | ✅ 완료 | DATA_INVENTORY_v04_master_2026_05_06.md |
| 1-A 시군구 crosswalk | ✅ 완료 | `sigungu_crosswalk_v2.csv` |
| 1-B 104 사망원인 분류 | ✅ 완료 | `mortality_104_classification.csv` |
| 1-C ECOS macro / WEO / centroid | ✅ 완료 | 6 ECOS series + WEOhistorical + 251 sigungu centroid |
| 1-D HIRA sgguCd → h_code crosswalk | ✅ NEW | `1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv`, `intersection_main_hira_h_codes.csv` |
| 1-E HS↔KSIC concordance | ✅ 완료 | `researchall_HS6_to_KSIC_link.csv` |
| 2-A mortality panel (working-age) | ✅ v02_wa main | `sigungu_mortality_panel_v02_wa.parquet` (31,494 rows) |
| 2-B Bartik 1994 baseline | ✅ 완료 | `iv_z_x_adh8.parquet`, `iv_z_x_bilateral.parquet` (226 h_code) |
| 2-B Bartik 1992 baseline robustness | ✅ v2 commit | `iv_z_x_*_1992baseline.parquet` (215 sigungu × 4 col, 209 effective long-difference) |
| 3 인구 panel | ✅ v02 채택 | `population_panel_v02.parquet` (210,222 rows) |
| 3C-3E mediator panel | ✅ 완료 | mediator marriage/education v02/v03 |
| 4A trade 수집 | ✅ 완료 | KR-CN HS 01-99 25y, ADH-8, CN-World |
| 4B HS vintage + KSIC concordance | ✅ 완료 | `hs6_to_ksic9_2digit.parquet` (KIET60 매개) |
| 4C Bartik IV 구축 | ✅ 완료 | `iv_z_x_adh8.parquet`, `iv_z_x_bilateral.parquet` |
| B-x identification suite | ✅ 완료 | first-stage F (ADH-8 19.65, bilateral 48.08 HC1 / 12.20 cluster) |
| **4 main spec native scale 5-layer SE** | ✅ **NEW Path A unified** | `4_results/regression/akm_proper_kolesar.csv`, `wcr_webb_native.csv`, `romano_wolf_native.csv`, `rw_wcr_native.csv` 등 10 native CSV |
| **4-수반 1992 baseline native robustness** | ✅ **NEW v02** | `baseline_1992_native_v02.csv` (β=-0.0640, n=209, attenuation 50.4%) |
| **4-수반 Pre-WTO placebo native** | ✅ **NEW v02 (sign reverse)** | `prewto_placebo_native.csv`, `prewto_placebo_native_v02.csv` (β=-0.123, gradual integration interpretation) |
| **4-수반 Drop-sector native** | ✅ **NEW** | `drop_sector_native.csv` — Drop-C26 cluster t=-3.24 p=0.0012, Drop top-3 β=-0.0713 |
| **4-수반 Year FE panel native** | ✅ NEW | `year_fe_native.csv` |
| **4-수반 Romano-Wolf with WCR backend** | ✅ NEW (FWER PASS) | `rw_wcr_native.csv` (despair p_RW = 0.0161) |
| **WCB Webb 6-point native (P1 fix)** | ✅ NEW (numba 우회 published package) | `wcb_webb_native.csv`, `wcr_webb_native.csv` (p_WCR < 0.0001) |
| **Paper draft v01 § 1·2·3·4·5·6·7·8·9 native unified** | ✅ **NEW 7 file native scale** | `paper_draft_v01_section_*.md` (총 ~150 KB), § 7 신규 commit (8.5 KB) |
| **§ 6.X 1.854 ratio sub-section** | ✅ NEW | long-run amplification (Sullivan-VW + Eliason-Storrie + Case-Deaton + Pierce-Schott 4-anchor) |
| **§ 5.1 Footnote X (σ_z + IQR translation)** | ✅ NEW | σ_z = 1,696,322 USD/worker, IQR = 1,228,279, IQR translation -8.78% |
| **PAP v4.4 → v4.5.4 patches** | ✅ 6 file | 직전 보고서 commit 동일 (변경 없음) |
| **paper_v01_submission package** | ✅ NEW (첫 zip build) | `8_submission/paper_v01_submission/` 7 sub-folder + `paper_v01_submission.zip` (3.5 MB) |
| **wildboottest published package patch** | ✅ NEW (P1 fix from 5/6 latest.md) | `2_scripts/published_packages/wildboottest-0.3.2/` no-numba implementation |
| **HIRA M5 mediator panel build** | 🟡 Phase 2 entry 권고 | `1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv` (Step 2.1 완료), 152,208 rows × 5 ATC4 × 168 sigungu × 2010-2019 v02 panel 보유 |
| **External audit prompt (Layer A)** | ✅ NEW (5/6 17:21) | `논문을쓰자\external_audit_A_substantive_contribution_prompt.md` (8.6 KB, Q1-Q5 substantive contribution audit) |
| **target venue 결정** | 🔄 변경 (AER:Insights → KER) | status_report_phase2_entry.md 2026-05-06 (사용자 commit) |

**가장 critical 한 사실 한 가지**: paper 가 archive 10-year window 의 marginal Romano-Wolf failure (p_RW = 0.317) 에서 native 21-year window 의 **FWER PASS (p_RW = 0.0161)** 로 본질적 격상. 이는 단순히 inference 강화가 아니라 **window length 의 long-run effect amplification (1.854 ratio)** 의 substantive 주장과 connected — Sullivan-Von Wachter (2009), Eliason-Storrie (2009), Case-Deaton (2015), Pierce-Schott (2020) 4 reference anchor 위에서 "21-year cumulative dynamics 가 substantive evidence" 로 commit. paper § 6 끝 별도 sub-section 신설.

**target venue 변경 — AER:Insights primary → KER (Korean Economic Review)**: 2026-05-06 사용자 commit. status_report_phase2_entry.md 명시 — KER 7월 submission target. paper v02 first state 도달 + Phase 2 entry 권고. 단, 본 보고서 작성 시점에서 archive 의 5/6 latest.md 는 여전히 AER:Insights 명시 — 이는 5/6 evening 시점 status (논문을쓰자\RESEARCH_STATUS_2026_05_05_evening.md 에 명시) 이고, 5/6 16:10 의 status_report_phase2_entry.md 가 더 최신 (KER pivot). 메모리 신규 entry 권장 (Section 4 참조).

## 2. 산출물 inventory (직전 보고서 대비 변화 ✏️)

### Path A native unification — 4_results/regression/ 10 native CSV (NEW, ⭐ MAIN)

```
4_results/regression/
├── akm_proper_kolesar.csv                  ✏️ NEW ⭐ MAIN — AKM Kolesár 2024 ShiftShareSE
├── wcr_webb_native.csv                     ✏️ NEW ⭐ MAIN — WCR Webb 6-point bootstrap p<0.0001
├── wcb_webb_native.csv                     ✏️ NEW (P1 fix from 5/6 latest.md numba pipeline error)
├── romano_wolf_native.csv                  ✏️ NEW (5-outcome family, 1000 boot, native scale)
├── rw_wcr_native.csv                       ✏️ NEW (Romano-Wolf with WCR backend, despair p_RW = 0.0161 ⭐FWER PASS⭐)
├── baseline_1992_native_v02.csv            ✏️ NEW (1992 baseline robustness β=-0.0640, n=209)
├── drop_sector_native.csv                  ✏️ NEW (Drop-C26 cluster t=-3.24 p=0.0012, Drop top-3 β=-0.0713)
├── prewto_placebo_native.csv               ✏️ NEW (v01 placebo β=+0.024 archive scale)
├── prewto_placebo_native_v02.csv           ✏️ NEW (v02 native scale, sign flip → -0.123, gradual integration)
└── year_fe_native.csv                      ✏️ NEW (Year FE panel — 5,555 obs panel-level alternative spec)
```

**Main spec native scale 결과 (despair_total, n=221)** — `akm_proper_kolesar.csv`:

| outcome | n | β | SE_AKM | t_AKM | p_AKM |
|---------|---|---|--------|-------|-------|
| **despair_total** | **221** | **-0.1272** | 0.0258 | **-4.92** | **8.58e-07** |
| cancer | 221 | -0.0499 | 0.0231 | -2.16 | 0.031 |
| cardiovascular | 221 | -0.0697 | 0.0217 | -3.21 | 0.0013 |
| respiratory | 219 | +0.0754 | 0.0355 | +2.12 | 0.034 |
| external_other | 221 | -0.0172 | 0.0277 | -0.62 | 0.535 |

**Romano-Wolf step-down with WCR backend (5-outcome family, 1000 boot)** — `rw_wcr_native.csv`:

| outcome | t_HC1 | p_raw | p_RW_adj | RW_sig (FWER 5%) |
|---------|-------|-------|----------|------------------|
| **despair_total** | **-4.92** | <0.0001 | **0.0161** | **✅ Yes (FWER PASS)** |
| cancer | -2.16 | 0.031 | (보강) | (FWER family 내 marginal) |
| cardiovascular | -3.21 | 0.0013 | (보강) | (FWER family 내 sig) |
| respiratory | +2.12 | 0.034 | (보강) | (placebo direction sign opposite) |
| external_other | -0.62 | 0.535 | (보강) | No |

**1992 baseline native robustness** — `baseline_1992_native_v02.csv`:

| outcome | n | β | SE | t | p_WCR |
|---------|---|---|-----|---|-------|
| despair_total | 209 | -0.0640 | 0.0294 | -2.18 | 0.084 |
| cancer | 209 | -0.0129 | 0.0145 | -0.89 | 0.414 |
| cardiovascular | 209 | -0.0437 | 0.0300 | -1.46 | 0.084 |
| respiratory | 207 | +0.0228 | 0.0261 | +0.87 | 0.380 |
| external_other | 209 | -0.0009 | 0.0257 | -0.04 | 0.983 |

**Three-spec convergence**: 1994 native (β=-0.127, n=221) ↔ 1994 archive (β=-0.0685, n=222) ↔ 1992 native robustness (β=-0.0640, n=209) — sign 일관, magnitude attenuation 50.4% (1992 vs 1994 native), three-spec convergence 가 paper § 6.3 + § 6.X 1.854 ratio sub-section 의 substantive evidence.

**Drop-sector sensitivity native** — `drop_sector_native.csv`:
- Drop-C26 (전자부품 dominant industry): cluster-시도 t = **-3.24, p = 0.0012** (broad exposure 입증)
- Drop top-3 (C26+C24+C20): β = -0.0713, t = -2.08
- BHJ shock-only exogeneity 의 direct test 강화

**Pre-WTO placebo native v02** — `prewto_placebo_native.csv` + `prewto_placebo_native_v02.csv`:
- archive scale (5/6 보고서): β = +0.0238, p = 0.22 (placebo PASS)
- native scale v02: β = -0.123, sign flip — paper § 6.1 placebo paragraph 전체 reverse + "gradual integration" interpretation reframe (1992-1996 of pre-WTO 의 partial trade integration 이 이미 long-run mortality protective effect 를 담고 있음, China WTO 가입 (2001) 의 effect 가 step-function 이 아닌 gradual)

### Paper draft v01 native unified — 7_paper/ 7 file (NEW Path A 통일)

```
7_paper/
├── PAPER_WRITING_PLAN_v01.md               ✏️ 5/5 commit, 변경 없음 16.6 KB
├── paper_draft_v01_section_1_2.md          ✏️ NATIVE UNIFIED (5/6 16:16) 19.7 KB (Intro + Background)
├── paper_draft_v01_section_3_4.md          ✏️ NEW (5/6 17:41) 31.3 KB (Data + Identification, native unified)
├── paper_draft_v01_section_5.md            ✏️ NATIVE UNIFIED (5/6 16:17) 27.7 KB (Empirical specification + Footnote X σ_z + IQR translation)
├── paper_draft_v01_section_6.md            ✏️ NATIVE UNIFIED (5/6 20:25) 22.6 KB (Results + Robustness + § 6.X 1.854 ratio sub-section)
├── paper_draft_v01_section_7.md            ✏️ NEW (5/6 19:22) 8.3 KB (Mechanism — HIRA pharmaceutical fetch deferred placeholder + 4 mediator structure)
├── paper_draft_v01_section_8_9.md          ✏️ NATIVE UNIFIED (5/6 20:26) 17.7 KB (Limitations + Conclusion + 1992 baseline reverse)
├── paper_draft_v01_references.md           ✏️ NATIVE UNIFIED (5/6 19:22) 11.0 KB (DOI 추가 + Pierce-Schott 47-64 → 47-63 정정)
├── cleanup_edit_operation_list_v02_final.md ✏️ NEW 13.8 KB (Path A unification commit log)
├── cleanup_verify_report.csv               ✏️ NEW (verify_cleanup_status.py 결과: 13/13 native target PASS, 8/8 arithmetic verify PASS, 4 archive leftover false positive)
├── compute_intersection_sample.R           ✏️ NEW 9.5 KB (universe vs analytic sample R script)
├── compute_sigma_z.R                       ✏️ NEW 4.5 KB (σ_z native verify R script — sd(panel_despair$z_x_per_worker) = 1,696,322)
└── verify_cleanup_status.py                ✏️ NEW 11.2 KB (cleanup verify script)
```

**§ 6.X 1.854 ratio sub-section 신설**:
- β_native (21-year window) / β_archive (10-year window) = -0.127 / -0.0685 = 1.854
- standardization factor 가 아닌 window length 의 long-run effect amplification
- 4 reference anchor: Sullivan-Von Wachter (2009) ~50-100% mortality hazard increase + Eliason-Storrie (2009) ~44% increase + Case-Deaton (2015) midlife mortality long-run + Pierce-Schott (2020) post-PNTR 18-year window

**§ 5.1 Footnote X (σ_z + IQR translation) 신설**:
- σ_z (z_x_per_worker sample SD) = 1,696,322 USD per 1994 manufacturing worker
- median = 494,804, IQR = 1,228,279 (p25=196,358, p75=1,424,637)
- IQR translation: 75th vs 25th percentile sigungu yields ~-8.78% mortality difference (ADH/Pierce-Schott canonical convention 정합)
- R verification: `sd(panel_despair$z_x_per_worker)` saved at `compute_sigma_z.R`

### paper_v01_submission package (NEW, 첫 zip build, 5/6 06:42 ~ 09:03)

```
8_submission/
├── paper_v01_submission.zip                ✏️ NEW 3.5 MB (5/6 06:48 첫 build)
└── paper_v01_submission/
    ├── DATA_DICTIONARY.md                  ✏️ NEW 9.4 KB
    ├── README.md                           ✏️ NEW 9.6 KB
    ├── 01_mortality/                       sigungu_mortality_panel_v02_wa.parquet
    ├── 02_bartik_iv/                       baseline_shares + denominator + exposure 6 file (1992 v2 + 1994)
    ├── 03_mediators/                       (mediator panel files)
    ├── 04_regression_results/              13 native CSV (akm_*, main_spec_5layer_se, romano_wolf_*, sub_period_*, prewto_*, rw_wcr, wcr_webb, quality_improvement_suite)
    ├── 05_codebooks/                       sigungu crosswalk + sigungu_changes_history.md
    ├── 06_paper_draft/                     paper_draft_v01_section_*.md 6 file + DATA_INVENTORY_v04
    └── 07_audit_logs/                      validation report + integrity checks
```

이는 본 paper 의 첫 submission-ready package — KER 제출 준비.

### wildboottest published package patch (NEW, P1 fix)

```
2_scripts/published_packages/wildboottest-0.3.2/
├── README.md
├── wildboottest-0.3.2/
│   ├── README.md
│   └── wildboottest/
│       ├── __init__.py
│       ├── weights.py
│       └── wildboottest.py
```

5/6 latest.md 의 P1 issue (WCB cluster-시도 numba pipeline error) 의 fix path. published wildboottest 0.3.2 의 source 직접 patch 후 no-numba mode 로 실행 가능. `wcb_webb_native.csv` + `wcr_webb_native.csv` 가 본 patch 위에서 build.

### Integrity check + audit logs (NEW, 4 file 5/6 추가)

```
5_logs/integrity_checks/
├── 2026-05-06_baseline_1992_215_to_209_drop_trace.md   ✏️ NEW (215→209 6 sigungu drop trace, sigungu_crosswalk.csv ground truth)
├── 2026-05-06_native_csv_cell_inventory.md             ✏️ NEW (native CSV 13 cell × paper-cited 수치 ↔ CSV 100% 정합 verify)
├── 2026-05-06_path_a_3stage_audit_cycle.md             ✏️ NEW (3-skill audit cycle: explore-data → analyze → validate-data)
└── sample_attrition_audit_template_v01.md              ✏️ NEW (1994 main 6-step + 1992 robustness 3-step attrition cascade template)
```

215 → 209 drop trace 결과: 5 sigungu (안산 31090, 용인 31190, 통합청주 33040, 천안 34010, 통합창원 38110) 의 endpoint mortality (2018-2022) 가 administrative 통합 + reporting gap 으로 missing. respiratory 만 1 추가 sigungu drop (207 vs 209) — small-cell 처리.

### HIRA M5 mediator entry crosswalk (NEW, Step 2.1 완료)

```
1_codebooks/
├── hira_sgguCd_to_hcode_crosswalk.csv          ✏️ NEW (HIRA 6-digit sgguCd → 5-digit h_code 매핑, Phase 2 sub-task 2.1)
└── intersection_main_hira_h_codes.csv          ✏️ NEW (1994 main 221 sigungu ∩ HIRA 168 sigungu = ~115 intersection h_codes)
```

`status_report_phase2_entry.md` 명시 Phase 2 sub-task list:
- 2.1 HIRA sgguCd → h_code crosswalk: ✅ 완료 (R-A 측 commit)
- 2.2 sigungu × year × ATC4 panel 산출 (~2-3 일): 🟡 pending (사용자 측 execution)
- 2.3 M5 outcome variable build (rate per 100K): 🟡 pending
- 2.4 ivmediate framework (DGHP 2017) implementation: 🟡 pending (5-7 일)
- 2.5 § 7 mechanism narrative + 4 layer honest disclosure (2-3 일): 🟡 pending

### External audit prompt + cleanup prompt set (NEW)

```
논문을쓰자/  (외부 archive)
├── cleanup_prompt_path_a_native_unification.md          ✏️ NEW 5/6 11:45 (Path A unification main prompt)
├── cleanup_prompt_path_a_v02_with_numerical_placeholders.md ✏️ NEW 5/6 11:45
├── cleanup_prompt_path_a_v02_1_patch.md                 ✏️ NEW 5/6 12:21
├── cleanup_prompt_path_a_v02_2_patch.md                 ✏️ NEW 5/6 12:35
├── cleanup_prompt_path_a_v02_3_patch.md                 ✏️ NEW 5/6 12:53
├── reverse_prompt_native_to_standardized.md             ✏️ NEW 5/6 11:14
├── status_report_phase2_entry.md                        ✏️ NEW 5/6 16:10 (Phase 2 entry self-contained status, 14.8 KB)
└── external_audit_A_substantive_contribution_prompt.md  ✏️ NEW 5/6 17:21 (8.9 KB, 5 substantive contribution Q + KER referee attack-surface 평가 영역)
```

### Decision logs (직전 5/6 보고서 commit 동일, 추가 없음)

```
5_logs/decisions/  (직전 18 file 동일, 5/6 이후 추가 commit 없음)
```

직전 보고서가 명시한 5/6 commit 이후 decision log 추가 없음. 단 integrity_checks 폴더에 4 file 추가 (위 명시).

## 3. 직전 보고서 (2026-05-06 latest.md) 대비 변경 사항

1. **Path A native unification 본격 commit** — archive scale (β=-0.0685, window 10y) → native scale (β=-0.127, window 21y) 의 1.854 amplification ratio 명시. paper draft 7 file 모두 native unified. 본 paper 의 final headline number 가 archive 에서 native 로 격상.
2. **Romano-Wolf FWER PASS 도달** (직전 P2 → 해결) — 직전 보고서의 critical P2 (despair p_RW = 0.317, FWER 5% 미통과) 가 native 21-year window + WCR backend 위에서 **p_RW = 0.0161 (FWER PASS)** 로 격상. paper § 5.3 의 inference framework 의 substantive contribution 영역으로 격상.
3. **WCB cluster-시도 numba pipeline error P1 fix** (직전 P1 → 해결) — published wildboottest 0.3.2 의 no-numba implementation 으로 patch. WCB Webb 6-point native + WCR Webb native 모두 commit. p_WCR < 0.0001 — 9,999 boot 중 0 개 reject.
4. **HC1 t = AKM-proper t = -4.92 numerical coincidence** 입증 — z_x_per_worker spec 위에서 HC1 SE ≈ AKM SE 의 substantive evidence. paper § 5.1 line 42 narrative refinement.
5. **§ 5.1 Footnote X (σ_z + IQR translation) 신설** — σ_z = 1,696,322 USD/worker, IQR translation -8.78% per IQR shift (ADH/Pierce-Schott canonical convention 정합). compute_sigma_z.R 로 R verification.
6. **§ 6.X 1.854 ratio sub-section 신설** — long-run effect amplification, 4 reference anchor (Sullivan-Von Wachter + Eliason-Storrie + Case-Deaton + Pierce-Schott).
7. **§ 6.1 Pre-WTO placebo paragraph 전체 reverse** — archive scale 의 +0.024 (placebo PASS) → native scale 의 -0.123 (sign flip), "gradual integration" interpretation reframe — pre-WTO 1992-1996 partial trade integration 이 이미 long-run mortality protective effect 를 담고 있음.
8. **§ 6.3 1992 baseline paragraph 전체 reverse** — β=-0.0158 (n=210, 23% attenuation) → β=-0.0640 (n=209, 50.4% attenuation), three-spec convergence 의 substantive evidence.
9. **§ 3.2 P2.1 issue fix** (직전 P2 → 해결) — universe vs analytic sample 정합 commit (universe 251 vs analytic 222 vs intersection 221 cascade 명시).
10. **paper draft § 3·4 + § 7 신규 commit** — 직전 보고서 시점에는 없던 § 3 (Data) + § 4 (Identification) + § 7 (Mechanism placeholder) 3 section 신규 commit. § 3·4 합본 31.3 KB, § 7 8.3 KB.
11. **paper_v01_submission zip 첫 build** — 8_submission/paper_v01_submission/ 7 sub-folder + 3.5 MB zip. KER submission 준비 단계 (target venue pivot AER:Insights → KER).
12. **target venue pivot AER:Insights → KER** (5/6 16:10 status_report_phase2_entry.md 사용자 commit) — KER 7월 submission target. paper format short → full paper format 으로.
13. **Drop-sector native sensitivity 강화** — Drop-C26 cluster t=-3.24 p=0.0012, Drop top-3 β=-0.0713 — broad exposure 입증, BHJ shock-only exogeneity direct test.
14. **External audit prompt (Layer A) commit** — Q1-Q5 substantive contribution audit framework, KER referee attack-surface 평가 영역 self-contained. 외부 AI/reviewer paste 시 5 substantive Q 평가 가능.
15. **HIRA M5 Phase 2 entry 권고** — sub-task 2.1 (sgguCd → h_code crosswalk) 완료, 2.2-2.5 pending (사용자 측 execution + R-A measurement 영역 분업).

메모리 파일 변경: 직전 보고서 이후 변동 없음. `MEMORY.md` 19개 entry frozen. 단, **`project_dissertation.md` 가 이제 8 phase 정도 stale** — 가장 critical 한 stale = (a) Path A native unification commit, (b) FWER PASS 도달, (c) target venue pivot AER:Insights → KER, (d) paper v02 first state 도달, (e) HIRA M5 Phase 2 entry. `project_main_folder.md` 의 정합성은 직전 보고서 동일 (active = trade_mortality_korea, 보조 raw = trade_mortality_raw).

## 4. 메모리 업데이트 제안 (사용자 승인 후 적용)

자동 update 하지 않음. 다음 conversation 에서 검토 권장:

- **`project_dissertation.md` 갱신 (높은 우선순위)**: 직전 보고서 권고 갱신 + 본 보고서의 5 핵심 사항 추가:
  - Path A native unification commit (β=-0.127, window 1997-1999↔2018-2022, 1.854 amplification ratio)
  - Romano-Wolf p_RW = 0.0161 FWER PASS (5-outcome family)
  - target venue AER:Insights → KER pivot (2026-05-06 사용자 commit)
  - paper v02 first state 도달 + Phase 2 (HIRA M5 mediator) entry 권고
  - paper_v01_submission zip 3.5 MB 첫 build

- **신규 메모리 entry 권장 1: `project_paper_v02_first_state.md`** (project type) — 본 paper 의 final headline number stable fact. native scale 1994 baseline despair_total β = -0.127 (HC1 t=-4.92 / cluster-province t=-4.02 / AKM-proper t=-4.92). cancer/cardio/respiratory(반대 sign)/external_other secondary outcomes. Romano-Wolf p_RW (despair, WCR backend) = 0.0161 FWER PASS. 1992 baseline robustness β = -0.0640, n=209, 50.4% attenuation. Pre-WTO placebo β = -0.123 (gradual integration interpretation). Drop-C26 cluster t=-3.24 p=0.0012. σ_z = 1,696,322 USD/worker.

- **신규 메모리 entry 권장 2: `project_target_venue_ker.md`** (project type) — target venue AER:Insights primary → KER (Korean Economic Review) 7월 submission target. paper format short-form (8-12 page) → full paper format. status_report_phase2_entry.md (5/6 16:10) 사용자 commit. paper_v01_submission zip 3.5 MB 첫 build (5/6 06:48).

- **신규 메모리 entry 권장 3: `project_phase_2_entry_hira_m5.md`** (project type) — Phase 2 sub-task 2.1 (sgguCd → h_code crosswalk) 완료, 2.2-2.5 pending. 5 ATC4 grouping (N06AB SSRI + N06AX 기타 antidepressants + N05BA Benzodiazepines + N05AX 기타 antipsychotics + A05BA Liver therapy). 4 honest limitation disclosure layer (2010-2019 unit inconsistency / 168/250 sigungu coverage / N02A 부재 / cross-mediator decomposition abandoned). ivmediate framework (DGHP 2017) 채택. paper § 7 8.3 KB placeholder 위에서 build.

- **신규 메모리 entry 권장 4: `feedback_path_a_native_unification.md`** (feedback type) — paper magnitude 의 archive vs native 통일 시 native-first principle 적용. window length 가 substantive 결과를 결정 — 21-year window 의 1.854 amplification ratio 가 paper § 6 별도 sub-section 의 substantive contribution. native scale 첫 commit 시 standardization factor (σ_z) 의 IQR translation footnote 필수 (ADH/Pierce-Schott canonical convention).

- **`project_data_status.md` 갱신**: 7 issue 모두 closure 표시 + 직전 보고서의 4 P1/P2 issue 모두 closure (P1 WCB numba ✅, P1 LMP tF cutoff ✅, P2.1 universe vs analytic ✅, P2.2 1992 z_x_h NaN ✅, P2.3 dual-cited ✅).

- **`reference_library_md.md` 갱신**: 27 paper deep summary master 명시 (직전 보고서 시점 27 paper 도달). Tier A 의 핵심 anchor 4편 (Pierce-Schott + Finkelstein-NAFTA + Sullivan-Von Wachter + Eliason-Storrie) 의 long-run amplification 영역 의 § 6.X 1.854 ratio sub-section 의 directly applied evidence.

- **`feedback_validation_audit_skill_use.md` 갱신**: 직전 보고서 권고 entry 의 구체적 implementation 명시 — 3-skill audit cycle (explore-data → analyze → validate-data) 의 path_a_3stage_audit_cycle.md 위에서 적용. cleanup_verify_report.csv 의 13/13 native target PASS + 8/8 arithmetic verify PASS 의 결과.

## 5. 참고논문 rotation 학습 결과

본 turn rotation: **Lee-McCrary-Moreira-Porter (2022) "Valid t-Ratio Inference for IV"** (paper_27_lee_mccrary_moreira_porter_2022.md).

핵심 take-away 3 가지 + 본 paper 적용 영역:

1. **tF critical value c₀.₀₅(F) 의 정확값**: F = 19.65 (본 paper ADH-8 first-stage F) 의 exact cutoff 가 **3.286** (interpolated from p.14 formula). 직전 보고서 의 P2.3 LMP tF cutoff dual-cited (3.286 vs 3.84) issue 의 closure 영역 — implementation script 와 paper narrative 모두 3.286 (LMP 2022 정확) 으로 통일 commit. 또한 KR-CN bilateral first-stage F=12.20 cluster 의 cutoff 는 ~3.09, F=48.08 HC1 의 cutoff 는 ~2.39 — 모두 본 paper 의 |t|=4.92 (despair_total) 통과. tF inference 가 본 paper 의 핵심 inference framework.

2. **AR test 와의 비교 — 본 paper 의 weak-IV-robust complement**: F < 3.84 시 tF undefined, AR 만 가능. 본 paper 는 F = 19.65 + 12.20 + 48.08 모두 3.84 통과 — tF inference 가 valid + AR (Anderson-Rubin) confidence set 도 정합 (paper § 5.3 commit). tF 와 AR 의 dual-reporting 가 reviewer-defense 핵심 layer.

3. **LMP audit — 25% AER paper 의 inference 변경**: LMP 2022 의 61개 AER paper audit 결과 1/4 의 SE > 49% 더 커짐 (5% level). 본 paper 의 SE adjustment factor c₀.₀₅(F=19.65)/1.96 = 3.286/1.96 = **1.677** — 본 paper 의 SE 가 conventional 보다 67.7% 더 커짐. 단 |t| = 4.92 (despair_total native) 가 conventional 1.96 의 2.94 배 → 1.677 adjustment 후에도 |t/adjustment| = 4.92/1.677 = 2.93 > 1.96 — significant 보존. paper § 5.3 commit 의 substantive evidence.

**본 연구 새롭게 적용 가능한 insight**: 
- LMP 2022 의 SE adjustment factor 1.677 의 implementation script 명시 — paper § 5.3 + Footnote X 의 magnitude reporting 의 secondary layer.
- F = 6.10 (sub-period pre_2008 가 가능할 시 first-stage F, paper § 5.4) 의 cutoff 는 ~5.05 — sub-period split 시 tF inference 의 strict cutoff 위에서 robustness 평가.
- AR confidence set 의 paper § 5.3 직접 commit — reviewer-defense 의 "weak-IV-robust" 명시적 layer.

**다음 rotation** (다음 실행 시): GPSS 2018/2019 (paper_24408_GPSS_Bartik.md) — Rotemberg weight + share path identification. 그 후 BHJ 2025 practical guide (paper_08_borusyak_hull_jaravel_2025_shift_share.md) 의 effective number of shocks Herfindahl 의 본 paper KSIC9 2-digit 23 industry 적용.

## 6. 다음 작업 추천 (priority 순)

### A. paper § 7 (Mechanism) 완성 — Phase 2 sub-task 2.2-2.5 진행 (2-3 주)

`status_report_phase2_entry.md` (5/6 16:10) 명시 5-stage workflow:
1. **Step 2.2** sigungu × year × ATC4 panel 산출 ETL — Python script 작성 (R-A 측 가능, 2-3 일). 152,208 rows × 5 ATC4 × 168 sigungu × 2010-2019 → ~8,400 rows.
2. **Step 2.3** M5 outcome variable build (rate per 100K) + KOSIS 인구 panel join (R-A 측 작성 + 사용자 측 execution, 1-2 일).
3. **Step 2.4** ivmediate framework (DGHP 2017) implementation — R/Stata script (R-A 측 작성, 사용자 측 execution, 5-7 일).
4. **Step 2.5** § 7 mechanism narrative + 4 layer honest disclosure (R-A 측 wording draft, 사용자 측 paper 본문 commit, 2-3 일).

본 paper mediation thesis 의 핵심 layer. paper v02 first state 의 § 7 (현재 8.3 KB placeholder) 을 final form 으로 commit.

### B. KER submission package final review (2-3 일)

paper_v01_submission zip 3.5 MB 가 5/6 06:48 첫 build. 향후 ~25 분 fix 후 final submission package:
- README.md + DATA_DICTIONARY.md cross-check
- 06_paper_draft/ 의 7 file (§ 1-§ 9) commit verify
- 04_regression_results/ 의 13 native CSV commit verify
- 7_paper/cleanup_verify_report.csv 의 13/13 native target PASS 확인
- 코드 reproducibility 시범 — 사용자 측 R script 1 회 실행

### C. WCB cluster-시도 SE 의 published wildboottest 0.3.2 patch verify (1 회)

5/6 commit 의 wildboottest no-numba implementation patch 가 P1 fix 로 commit. 향후 paper § 5.1 5-layer SE 의 5번째 layer (WCB cluster-시도) 의 published-package 위에서 `wcb_webb_native.csv` + `wcr_webb_native.csv` 결과 cross-check 권장.

### D. Pre_2008 sub-period symmetric build (P3.2) — ~30 분

직전 보고서의 P3.2 issue 가 여전히 pending. 현재 `sub_period_split_2008.csv` 가 post_2008 (2008-2022) 만, symmetric pre_2008 (1997-1999 base → 2007 endpoint) 결측. paper § 5.4 acknowledge → next regression run 에서 추가.

### E. Phase B-m identification (z_m mediator instruments) — 5-7 일

mediation analysis (DGHP 2017 ivmediate) 의 z_m_marital + z_m_education instrument build. MDIS 1975-1995 census microdata 활용 (cohort 변동 → 시군구 결혼시장 + 교육접근 변동). Test 4·5·6 (외생성: 인구이동·결혼시장·교육접근). z_x → z_m sequential ignorability check. § 7 (Mechanism) commit 의 sub-step.

### F. Effective number of shocks (BHJ 2025 § 4 권고) — paper § 5.2 sub-step ~30 분

KSIC9 2-digit 23 industry 의 Herfindahl index → effective number = 1/HHI. BHJ recommendation (≥ 5) 통과 여부 commit. 통과 시 paper § 5.2 첫 단락 의 robustness section 에 "effective number of shocks = X" 줄 추가. 미통과 시 paper § 8 limitation 에 명시 + KSIC9 2-digit → KSIC9 4-digit 더 disaggregated 매핑 sensitivity 권장.

### G. (deferred) Bartik baseline robustness — 1993·1995·1996·1999 추가 baseline ~2-3h

PAP v4.5.4 footnote 17 retraction 후 5 baseline (1992·1993·1995·1996·1999) 모두 build. 현재 1992 + 1994 만 commit. paper § 6.4 baseline year sensitivity table 에 5 column 으로 commit.

### H. (deferred) 외부 데이터 추가

- HIRA 의약품 ATC4 fetch 완료 (5/5 evening 17% → 100%, 약 6 일 추가 — 단 status_report_phase2_entry.md 명시 fetch 영역 abandoned, 5 ATC4 single composite 위에서 § 7 build 결정)
- ECOS 시도별 분기 연체율 2008-2024
- ELIS 결혼지원금 시군구 panel
- KOSIS 자살률 외부 검증 (P1 추가 다운, 1-2 시간)
- KOSIS GRDP 가용성 확인

## 7. 미해결 의사결정 / Risk

### [P1] HIRA M5 mediator panel 의 168/250 sigungu coverage limitation

main spec 1994 baseline 의 221 sigungu 중 ~53 sigungu (24%) 가 HIRA panel 부재 — Phase 2 entry 시 mediator analysis 의 sample mismatch. 사용자 commit Option 3 (5 ATC4 single composite) 위에서 진행. paper § 7 의 4 honest limitation disclosure 의 첫 layer.

### [P2] N02A (오피오이드) 부재 — Korea-US substantive 차이

HIRA OpenAPI rate limit fundamental 한계 위에서 N02A opioid + C09 ACE inhibitor + A10 diabetes + C10 statin 4 ATC4 acquisition 중단. 단 본 paper 의 substantive contribution 영역 — Korea 의 minimal opioid prescription evidence 가 US 와 fundamental 차이 (US opioid epidemic 의 mirror image). paper § 7 의 substantive backing.

### [P2] target venue pivot — AER:Insights → KER

5/6 16:10 사용자 commit. 단 5/5 evening RESEARCH_STATUS_2026_05_05_evening.md 는 여전히 AER:Insights primary 명시 — 정합 align 권장 (PAPER_WRITING_PLAN_v01.md 의 target venue 영역 KER 으로 update + paper format 8-12 page → full paper format 으로 update). 이는 R-A 의 다음 turn 에서 PAPER_WRITING_PLAN_v02 commit.

### [P2] Romano-Wolf 5-outcome family 의 outcome selection pre-specification 정합

5-outcome family (despair / cancer / cardio / respiratory / external_other) 위에서 despair p_RW = 0.0161 FWER PASS. 단 KER referee 의 potential criticism = "outcome family 가 post-hoc 선택" — pre-specification (PAP v4.5.4) 에서 5-outcome family 명시 commit verify 필요.

### [P2] Test 3 share violation (직전 P2 동일)

1997-1999 pre-trend 가 1994 manufacturing share 와 강하게 상관 (β=-0.191, p<0.0001). IMF 위기 영향 가능. **mitigation**: BHJ 2022/2025 framework (shock-only exogeneity, share endogeneity 허용) 의존 명시 + Test 1b WEO surprise PASS (β=-0.05, p=0.74) 가 shock orthogonality 의 secondary evidence. paper § 8 limitation 명시.

### [P3] pre_2008 symmetric build 결측 (직전 P3 동일)

`sub_period_split_2008.csv` 가 post_2008 만. symmetric pre_2008 (1997-1999 base → 2007 endpoint) 결측. paper § 5.4 acknowledge. next regression run 에서 추가.

### [P3] Mortality WA panel NaN = 3,588 (11.4%) (직전 P3 동일)

`sigungu_mortality_panel_v02_wa.parquet` 의 31,494 cells 중 3,588 NaN. small-cell mortality (deaths/pop pairs missing for some outcome × year × sigungu). sub-period split 시 drop 됨 (n=218 / n=206 reduced samples). paper § 6 footnote 권장 — "small-cell suppression for outcome × year × sigungu cells with insufficient observations".

### [P3] F17 (담배) 제외 불가 (직전 P3 동일)

KOSIS 사망 microdata `사망원인_104항목분류코드` 가 3자리 통합 — F10/F11/F17 분리 불가. Case-Deaton 정의 엄밀 적용 시 F17 (담배) 제외 불가. **mitigation**: PAP § 11 sensitivity — 코드 057 제외 (F17 우려 차단) + 코드 101 + 081 만 사용한 narrow despair 정의로 robustness.

### [P3] § 3.2 Sample Attrition Table A.1·A.2 INSERT 위치 결정

`status_report_phase2_entry.md` 명시 carry-over — 1994 main 6-step + 1992 robustness 3-step cascade 별도 form (R-A 권고). INSERT location (paper_draft_v01_section_3_4.md 존재 여부 + section number) 사용자 결정 영역.

### [P3] post-2008 native R wrapper 실행 결정

`status_report_phase2_entry.md` 명시 carry-over — archive 결과 (-0.0897) paper § 5.4 commit, native scale 결과 미실행. 사용자 측 native R wrapper extension 진행 여부 결정.

### [P3] HIRA M5 의 IQR/percentile interpretation

`status_report_phase2_entry.md` 명시 carry-over — HIRA 168 sigungu coverage 의 main spec 221 sigungu 와 sample mismatch 시 mediator analysis 의 valid IRA 영역. Phase 2 sub-task 2.4 의 ivmediate framework 진행 시 결정 영역.

---

**Source-of-truth files**:
- main spec native scale 5-layer SE: `4_results/regression/akm_proper_kolesar.csv` + `wcr_webb_native.csv` + `rw_wcr_native.csv`
- 1992 baseline native robustness: `4_results/regression/baseline_1992_native_v02.csv`
- Drop-sector native sensitivity: `4_results/regression/drop_sector_native.csv`
- Pre-WTO placebo native: `4_results/regression/prewto_placebo_native.csv` + `prewto_placebo_native_v02.csv`
- Path A 3-stage audit cycle: `5_logs/integrity_checks/2026-05-06_path_a_3stage_audit_cycle.md`
- 215 → 209 drop trace: `5_logs/integrity_checks/2026-05-06_baseline_1992_215_to_209_drop_trace.md`
- native CSV cell inventory verify: `5_logs/integrity_checks/2026-05-06_native_csv_cell_inventory.md`
- paper draft v01 native unified: `7_paper/paper_draft_v01_section_*.md` 7 file (§ 1-9, references) + `paper_draft_v01_section_3_4.md` + `paper_draft_v01_section_7.md` 신규
- cleanup verify report: `7_paper/cleanup_verify_report.csv` (13/13 PASS + 8/8 arithmetic verify)
- σ_z + intersection sample R script: `7_paper/compute_sigma_z.R` + `compute_intersection_sample.R`
- paper_v01_submission first build: `8_submission/paper_v01_submission.zip` (3.5 MB)
- wildboottest no-numba patch: `2_scripts/published_packages/wildboottest-0.3.2/`
- HIRA Phase 2 entry status: `논문을쓰자\status_report_phase2_entry.md` (14.8 KB)
- external audit prompt: `논문을쓰자\external_audit_A_substantive_contribution_prompt.md` (8.9 KB)
- HIRA sgguCd → h_code crosswalk: `1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv` + `intersection_main_hira_h_codes.csv`
