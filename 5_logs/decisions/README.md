# decisions/ — 본 paper 의 commit 결정 archive

_총 14 file. 시간순 + 주제별 grouping_

본 폴더의 file 은 paper 본문의 모든 substantive 결정 (working-age, A.ii main, year FE 의무, tF 의무, 5-layer SE, AKM-proper, Romano-Wolf 등) 의 source. 한 file 당 결정 1건 + 근거 + anchor + 영향 + sensitivity + 후속 step 6-section 형식.

---

## 시간순 14 file

### 2026-05-01 (Phase 1 codebook commit)

| file | 결정 |
|------|------|
| `2026-05-01_mortality_104_codes.md` | KOSIS 사망 microdata 104 항목 → outcome group 매핑 commit. 029 식도암 / 069 기타심장 / 102 자살 식별. v3.x mislabel (069 alcohol 오기) 정정 |
| `2026-05-01_sigungu_h_code_definition.md` | 256 h_code (KOSTAT 2021 baseline) commit. crosswalk 6,723 rows, 1997-2023 매칭률 100% |

### 2026-05-04 (Phase B-x identification diagnostic)

| file | 결정 |
|------|------|
| `2026-05-04_phase_bx_test1_test1b_branch_decision.md` | Test 1 (Romer-Romer macro orthogonality) + Test 1b (WEO surprise) branch 1차 결정 |

### 2026-05-05 (Phase B-x final + Phase 2 + Phase 4 publishable)

| file | 결정 |
|------|------|
| `2026-05-05_phase_bx_final_branch_decision.md` | Phase B-x 진단 9-branch matrix → A.ii main commit (univariate Bonferroni HAC pass) |
| `2026-05-05_mortality_panel_policy.md` | working-age 25-64 + Korean-only 정책 commit |
| `2026-05-05_first_reduced_form_main_result.md` | β=-0.0685 standardized first result commit. n=222 main, n=198 respiratory |
| `2026-05-05_p1_clear_for_phase4.md` | P1 finding clear → Phase 4 entry commit |
| `2026-05-05_phase4_final_inference.md` | Phase 4 5-layer SE final inference commit |
| `2026-05-05_phase4_fixes.md` | Phase 4 numerical / convergence fix commit |
| `2026-05-05_phase4_final_publishable.md` | β=-0.069, WCB p=0.041, sub-period sign 일치 ⭐ publishable 상태 도달 |
| `2026-05-05_pap_v41_commit.md` | PAP v4.1 commit (Phase 4 결과 반영) |
| `2026-05-05_akm_proper_implementation.md` | AKM-proper Kolesár ShiftShareSE 채택 commit |
| `2026-05-05_akm_bhj2022_ssaggregate.md` | BHJ ssaggregate shock-only path commit |
| `2026-05-05_quality_improvement_suite.md` | 7-source published packages (ShiftShareSE / ssaggregate / fwildclusterboot / wildrwolf / rwolf2 / st0611 / wildboottest) 통합 commit |
| `2026-05-05_pre_wto_placebo.md` | Pre-WTO IV placebo (1992-1996 KR-CN imports) commit. share violation audit |

### 2026-05-06 (Track 2/3 + 1992 sensitivity + audit)

| file | 결정 |
|------|------|
| `2026-05-06_track2_track3_v4_5_4_commit.md` | Track 2/3 (placebo + 1992 baseline) v4.5.4 commit |
| `2026-05-06_phase4_1992baseline_sensitivity.md` | 1992 baseline winsorized sensitivity commit |
| `2026-05-06_validation_report_audit_complete.md` | validation audit complete commit (사용자 측) |

---

## 주제별 grouping

### A. Sample universe (4 file)
- `2026-05-01_sigungu_h_code_definition.md` — 256 h_code
- `2026-05-01_mortality_104_codes.md` — 104 → 5 outcome group
- `2026-05-05_mortality_panel_policy.md` — working-age + Korean-only
- `2026-05-05_first_reduced_form_main_result.md` — n=222/198 sample 진입

### B. Identification (3 file)
- `2026-05-04_phase_bx_test1_test1b_branch_decision.md`
- `2026-05-05_phase_bx_final_branch_decision.md` — A.ii main
- `2026-05-05_pre_wto_placebo.md`

### C. Inference (5 file)
- `2026-05-05_phase4_final_inference.md` — 5-layer SE
- `2026-05-05_phase4_fixes.md` — convergence fix
- `2026-05-05_phase4_final_publishable.md` — publishable 상태
- `2026-05-05_akm_proper_implementation.md` — AKM-proper
- `2026-05-05_akm_bhj2022_ssaggregate.md` — ssaggregate

### D. Robustness (3 file)
- `2026-05-05_quality_improvement_suite.md` — 7-source packages
- `2026-05-06_track2_track3_v4_5_4_commit.md` — Track 2/3
- `2026-05-06_phase4_1992baseline_sensitivity.md` — 1992 baseline

### E. PAP commit (1 file)
- `2026-05-05_pap_v41_commit.md`

### F. Audit complete (1 file)
- `2026-05-06_validation_report_audit_complete.md`

---

## 가장 최신 publishable state

`2026-05-05_phase4_final_publishable.md` + `2026-05-06_validation_report_audit_complete.md` 가 본 paper 의 가장 최근 publishable + audit-complete commit. reset 시 이 둘을 우선 read.
