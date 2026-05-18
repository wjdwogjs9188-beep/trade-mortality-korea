# Research Status — 2026-05-07

> 자동 생성: `dissertation-context-refresh` scheduled task. 직전 보고서 (2026-05-06 latest.md) 와 cumulative comparison.
> 직전 24-30 시간의 가장 큰 변화는 **Path A native unification 본격 commit (β: -0.0685 → -0.127, window: 10y → 21y, Romano-Wolf p_RW: 0.317 → 0.0161 FWER PASS, native scale 회귀 10종 모두 commit, paper draft 7 file → 7 file native-scale 통일, paper v01 submission package zip 첫 build, wildboottest no-numba published-package patch P1 fix, target venue AER:Insights → KER pivot)**. 사실상 paper v02 first state 도달 + Phase 2 (HIRA M5 mediator panel build + § 7 mechanism) entry 단계.

> **scheduled task 환경 limitation 노트**: 본 task spec 은 archive 위치를 `C:\Users\82103\Desktop\뉴 논문\daily_status\` 로 지정. 그러나 본 conversation 의 mounted folders 는 `Downloads`, `Desktop\연구용`, `L:\da`, `Documents\Claude\Projects\논문을쓰자` 4 곳뿐 — `Desktop\뉴 논문` 미접근. 이전 보고서 (2026-05-06 까지) 가 모두 `trade_mortality_korea\4_documentation\status_reports\daily_status\` 에 archive 되어 있어, **본 보고서도 동일 경로에 commit**. 사용자 측 의사결정 권장: archive 경로 (1) 그대로 trade_mortality_korea 아래 유지, 또는 (2) 뉴 논문 폴더를 mount 에 추가, 또는 (3) 논문을쓰자 폴더로 통합.

> **본 보고서 본체 archive 위치**: `archive/2026/05/research_status_2026-05-07.md` (총 19 KB, 7 section + Source-of-truth files inventory).

## 핵심 요약

### A. Path A native unification (가장 critical)

archive scale (β=-0.0685, window 2000-2010 10-year long-difference) → **native scale (β=-0.127, window 1997-1999 ↔ 2018-2022 21-year long-difference)**. 1.854 amplification ratio = paper § 6.X 별도 sub-section 의 substantive contribution (Sullivan-Von Wachter + Eliason-Storrie + Case-Deaton + Pierce-Schott 4 reference anchor 위에서 long-run effect amplification 의 substantive evidence).

### B. Inference framework FWER PASS

| metric | archive (5/6 latest.md) | native (5/7) |
|--------|------------------------|--------------|
| despair_total β | -0.0685 | **-0.127** |
| HC1 t | -2.12 | **-4.92** |
| cluster-province t | -3.11 | **-4.02** |
| AKM-proper t | -3.65 | **-4.92** (numerical coincidence with HC1) |
| WCR Webb 6-point bootstrap p | NaN (numba error) | **<0.0001** (9,999 boot, 0 reject) |
| Romano-Wolf p_RW (5-outcome FWER) | 0.317 (n.s.) | **0.0161** ⭐FWER PASS⭐ |
| 1992 baseline robustness β | -0.0158 | **-0.0640** (50.4% attenuation) |
| Pre-WTO placebo β | +0.024 (placebo PASS) | -0.123 (sign flip → "gradual integration" interpretation) |
| Drop-C26 cluster t | (보강) | **-3.24, p=0.0012** |

### C. Paper draft v01 native unified — 7 file

| File | size | 변경 사항 |
|------|------|-----------|
| paper_draft_v01_section_1_2.md | 19.7 KB | NATIVE UNIFIED |
| paper_draft_v01_section_3_4.md | 31.3 KB | **NEW** (Data + Identification, native unified) |
| paper_draft_v01_section_5.md | 27.7 KB | NATIVE UNIFIED + Footnote X (σ_z = 1,696,322 USD/worker, IQR translation -8.78%) |
| paper_draft_v01_section_6.md | 22.6 KB | NATIVE UNIFIED + § 6.X 1.854 ratio sub-section |
| paper_draft_v01_section_7.md | 8.3 KB | **NEW** (Mechanism placeholder, HIRA fetch deferred) |
| paper_draft_v01_section_8_9.md | 17.7 KB | NATIVE UNIFIED |
| paper_draft_v01_references.md | 11.0 KB | DOI 추가 + Pierce-Schott pagination 정정 |

verify_cleanup_status.py 결과: 13/13 native target PASS + 8/8 arithmetic verify PASS.

### D. paper_v01_submission package (NEW, 첫 zip build, 5/6 06:48)

`8_submission/paper_v01_submission.zip` 3.5 MB + `paper_v01_submission/` 7 sub-folder (01_mortality, 02_bartik_iv, 03_mediators, 04_regression_results, 05_codebooks, 06_paper_draft, 07_audit_logs) + DATA_DICTIONARY.md (9.4 KB) + README.md (9.6 KB). **KER submission 준비 단계**.

### E. P1 issues 모두 closure (직전 보고서 2개 P1 → 0개)

- **WCB cluster-시도 numba pipeline error** ✅ (published wildboottest 0.3.2 no-numba patch, `wcb_webb_native.csv` + `wcr_webb_native.csv` p_WCR < 0.0001)
- **LMP tF cutoff dual-cited (3.286 vs 3.84)** ✅ (3.286 정확값 통일, paper § 5.3 commit)

### F. target venue pivot — AER:Insights → KER

2026-05-06 16:10 사용자 commit (`논문을쓰자/status_report_phase2_entry.md`). KER (Korean Economic Review) 7월 submission target. paper format short → full. 정재헌 single author.

### G. Phase 2 entry 권고 (HIRA M5 mediator panel build + § 7 mechanism)

`status_report_phase2_entry.md` 명시 5-stage workflow:

| sub-task | 작업량 | 상태 |
|---------|-------|------|
| 2.1 HIRA sgguCd → h_code crosswalk | 1-2h | ✅ 완료 (`1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv`) |
| 2.2 sigungu × year × ATC4 panel ETL | 2-3 일 | 🟡 R-A 측 script 작성 + 사용자 측 execution |
| 2.3 M5 outcome variable build | 1-2 일 | 🟡 pending |
| 2.4 ivmediate framework (DGHP 2017) | 5-7 일 | 🟡 pending |
| 2.5 § 7 mechanism narrative + 4 layer honest disclosure | 2-3 일 | 🟡 pending |

5 ATC4 grouping (사용자 commit Option 3): N06AB SSRI + N06AX 기타 antidepressants + N05BA Benzodiazepines + N05AX 기타 antipsychotics + A05BA Liver therapy. 4 honest limitation disclosure layer (2010-2019 unit inconsistency / 168/250 sigungu coverage / N02A 부재 / cross-mediator decomposition abandoned).

## 다음 작업 priority (요약)

1. **paper § 7 (Mechanism) 완성** — Phase 2 sub-task 2.2-2.5 (2-3 주)
2. **KER submission package final review** — paper_v01_submission zip 검토 (2-3 일)
3. **WCB published-package patch verify** — 5-layer SE 5번째 layer cross-check (1 회)
4. **Pre_2008 symmetric build (P3.2)** — ~30 분
5. **Phase B-m identification (z_m mediator instruments)** — 5-7 일
6. **BHJ 2025 effective number of shocks** — paper § 5.2 robustness ~30 분
7. (deferred) **Bartik baseline robustness 5 vintage** — 1993·1995·1996·1999 추가 ~2-3h
8. (deferred) **외부 데이터 추가** — KOSIS 자살률 외부 검증, GRDP, ELIS 결혼지원금

## Outstanding risk

### [P1] HIRA M5 mediator panel 의 168/250 sigungu coverage (24% sigungu 부재)

main spec 1994 baseline 의 221 sigungu 중 ~53 sigungu 가 HIRA panel 부재 — Phase 2 sub-task 2.2 진행 시 sample mismatch 의 substantive 문제. 사용자 commit Option 3 (5 ATC4 single composite) 위에서 진행. paper § 7 의 4 honest limitation disclosure 의 첫 layer.

### [P2] N02A (오피오이드) 부재 — Korea-US substantive 차이

HIRA OpenAPI rate limit 위에서 acquisition 중단. 단 Korea 의 minimal opioid prescription evidence 가 US 와 fundamental 차이 — paper § 7 의 substantive backing. forward-looking footnote.

### [P2] target venue pivot 의 documentation align

5/5 evening RESEARCH_STATUS_2026_05_05_evening.md 는 여전히 AER:Insights primary 명시, 5/6 16:10 status_report_phase2_entry.md 는 KER. PAPER_WRITING_PLAN_v01.md 의 target venue 영역 KER 으로 update + paper format 8-12 page → full paper format update 권장 → R-A 다음 turn PAPER_WRITING_PLAN_v02 commit.

### [P2] Romano-Wolf 5-outcome family pre-specification 정합

despair p_RW = 0.0161 FWER PASS — 단 KER referee potential criticism = "outcome family 가 post-hoc 선택" — pre-specification (PAP v4.5.4) 에서 5-outcome family 명시 commit verify 필요.

### [P2] Test 3 share violation (직전 P2 동일)

1997-1999 pre-trend × 1994 manufacturing share β=-0.191, p<0.0001. BHJ 2022/2025 framework (shock-only exogeneity) 의존 명시 + Test 1b WEO surprise PASS (β=-0.05, p=0.74) secondary evidence.

### [P3] pre_2008 symmetric build 결측 / Mortality WA panel NaN 11.4% / F17 담배 제외 불가 (직전 P3 동일, 변경 없음)

### [P3] § 3.2 Sample Attrition Table A.1·A.2 INSERT 위치 + post-2008 native R wrapper 실행 결정 (status_report_phase2_entry.md carry-over)

---

**상세 본문**: [archive/2026/05/research_status_2026-05-07.md](archive/2026/05/research_status_2026-05-07.md) (19 KB, 7 section + Source-of-truth inventory)

**메모리 신규 entry 권장 4종** (사용자 승인 후 다음 conversation 적용):
1. `project_paper_v02_first_state.md` (project) — final headline number stable fact
2. `project_target_venue_ker.md` (project) — AER:Insights → KER pivot
3. `project_phase_2_entry_hira_m5.md` (project) — Phase 2 sub-task list + 5 ATC4 + 4 honest layer
4. `feedback_path_a_native_unification.md` (feedback) — native-first principle + IQR translation footnote 필수
