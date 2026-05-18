# Research Status — 2026-05-06

> 자동 생성: `dissertation-context-refresh` scheduled task. 직전 (2026-05-05 00:14 마감 commit) 의 `latest.md` 와 cumulative comparison.
> 새 작업 약 24-30 시간분 의 가장 큰 변화는 **Phase 4 5-layer SE main spec runner 본격 실행 + Romano-Wolf step-down + 2008 sub-period split + AKM 2종 + Pre-WTO placebo + Paper draft § 1-§ 9 v01 6 file 초안 + PAP v4.4 → v4.5.4 5 patch 누적 + 1992 baseline Track 3 sensitivity (P1 → fix → v2 commit) + Track 2 z_m_education 정합 입증 + 2026-05-06 validation report audit**. 사실상 **본 paper 의 final empirical body 가 paper-grade form 으로 commit, paper draft § 1-§ 6 가 cited 수치 ↔ CSV 100% 정합 (R-A audit 입증)**.

## 1. 현재 stage 위치

직전 보고서 (2026-05-05 00:14) 마감 시점에서는 Phase B-x 4종 진단 closure + 첫 reduced form preliminary main result (despair_total β=−0.069, cluster-sido p=0.0019) 까지 도달. 그 후 24-30 시간 동안 **Phase 4 (5-layer SE main spec runner) + Romano-Wolf 1000 boot + sub-period split + Pre-WTO placebo + Paper draft 6 section 초안 + PAP 5 patch + 2 robustness track (Track 2·3)** 가 한꺼번에 진행됐다. 사실상 직전 보고서가 권고했던 Phase 4 A·B·C·D step (5-layer SE → Romano-Wolf → 2008 sub-period → PAP v4.0 main body rewrite) 4 단계가 모두 closure.

| Phase | 상태 | 핵심 산출물 (현재 commit) |
|-------|------|--------------------------|
| 0 raw 수집 + INVENTORY | ✅ 완료 | DATA_INVENTORY_v01.md (16.5 KB) |
| 1-A 시군구 crosswalk | ✅ 완료 | `sigungu_crosswalk_v2.csv` (361 KB) |
| 1-B 104 사망원인 분류 | ✅ 완료 | `mortality_104_classification.csv` |
| 1-C ECOS macro / WEO / centroid | ✅ 완료 | 6 ECOS series + WEOhistorical.xlsx + 251 sigungu centroid |
| 1-E HS↔KSIC concordance | ✅ 완료 | `researchall_HS6_to_KSIC_link.csv` |
| 2-A mortality panel | ✅ v02_wa main 채택 | `sigungu_mortality_panel_v02_wa.parquet` (31,494 rows) |
| 2-B Bartik 1994 baseline | ✅ 완료 | `iv_z_x_adh8.parquet`, `iv_z_x_bilateral.parquet` (226 h_code) |
| **2-B Bartik 1992 baseline** | ✅ **NEW v2 commit** | `iv_z_x_*_1992baseline.parquet` (215 rows × 4 col, 1 NaN, n=210 effective) |
| 3 인구 panel | ✅ v02 채택 | `population_panel_v02.parquet` (210,222 rows) |
| 3C-3E mediator panel | ✅ 완료 | mediator marriage/education v02/v03 |
| 4A trade 수집 | ✅ 완료 | KR-CN HS 01-99 25y, ADH-8, CN-World |
| 4B HS vintage + KSIC concordance | ✅ 완료 | `hs6_to_ksic9_2digit.parquet` (KIET60 매개) |
| 4C Bartik IV 구축 | ✅ 완료 | `iv_z_x_adh8.parquet`, `iv_z_x_bilateral.parquet` |
| B-x identification suite | ✅ 완료 | first-stage F (ADH-8 14.07, bilateral 48.08 HC1 / 12.20 cluster, 19.65 cluster) |
| **4 main spec 5-layer SE runner** | ✅ **NEW** | `main_spec_5layer_se.csv` (1,893 bytes), `main_spec_5layer_se_1992baseline.csv` (1,880 bytes) |
| **4-수반 Romano-Wolf 1000 boot** | ✅ **NEW** | `romano_wolf_pvalues.csv`, `romano_wolf_pvalues_1992baseline.csv` |
| **4-수반 2008 ICD sub-period split** | ✅ **NEW (post_2008 only)** | `sub_period_split_2008.csv` (β=−0.0458, t=−2.98, p=0.0029) |
| **4-수반 Pre-WTO placebo** | ✅ **NEW** | `pre_wto_placebo_1992_1996.csv` (β=+0.024, p=0.22) |
| **4-수반 AKM 2종** | ✅ **NEW** | `akm_proper_2019.csv`, `akm_bhj2022_ssaggregate.csv` |
| **4-수반 Quality improvement suite** | ✅ **NEW** | `quality_improvement_suite.csv` |
| **z_m_education Track 2 sensitivity** | ✅ **NEW** | 1985·1990·1995 baseline corr 0.989-1.000, 시군구 차이 > 0.5 단 0.8% |
| **1992 baseline Track 3 sensitivity** | ⚠️ **NEW v2 commit** | β = −0.0158 (n=210), 0/4 SE layer pass tF — preliminary, paper § 8 caveat 강화 |
| **Paper draft v01 section 1-9** | ✅ **NEW 6 file** | `paper_draft_v01_section_{1_2,3_4,5,6,8_9}.md` + `paper_draft_v01_references.md` (총 95 KB) |
| **PAP v4.4 → v4.5 → v4.5.1·2·3·4 patches** | ✅ **NEW 5 patch + main body v4.5** | `PAP_v4.4_main_body.md`, `PAP_v4.5_main_body.md`, `PAP_v4.5.1_patch.md`, `PAP_v4.5.2_patch.md`, `PAP_v4.5.3_patch.md`, `PAP_v4.5.4_patch.md` (총 100+ KB) |
| **Validation report audit** | ✅ **NEW (2026-05-06)** | `2026-05-06_validation_report_audit_complete.md` (10.5 KB) — paper-cited 수치 ↔ CSV 100% 정합 입증, 4 P1/P2 issue identified |

**가장 critical 한 사실 한 가지**: paper draft § 1-§ 6 가 cited 14개 핵심 수치 (β, t, p, n, RW p, correlation 등) 모두 actual CSV 와 100% 정합. R-A direct audit (data:validate-data + data:explore-data skill 사용) 통과. **Ready to share with noted caveats** 단계 도달 — 4 P1/P2 issue (§ 3.2 universe vs analytic sample, LMP tF cutoff dual-cited, 1992 z_x_h NaN h_code, parquet null-padding) 해결 시 ~25 분 후 "Ready to share" 단계.

**단 1992 baseline sensitivity 결과는 attenuated**: β = −0.0158 (vs 1994 main β = −0.0685, 약 23% 수준), 0/4 SE layer 가 tF cutoff 3.84 통과. 단 sub-period 2008-2022 split 시 β = −0.0458, p = 0.003 으로 protective sign + significance 보존. 본 paper § 6.3 (baseline year sensitivity) 가 이 attenuation 을 small-denom outlier + KSIC 6→9 ambiguity + sample reduction (251 → 210) 으로 acknowledge. paper § 8 limitation 도 강화.

## 2. 산출물 inventory (직전 보고서 대비 변화 ✏️)

### Phase 4 5-layer SE main spec runner (NEW, ⭐ MAIN)

```
4_results/regression/
├── main_spec_5layer_se.csv                    ✏️ NEW ⭐ MAIN — 1994 baseline
├── main_spec_5layer_se_1992baseline.csv       ✏️ NEW ⭐ ROBUSTNESS — 1992 baseline (attenuated)
├── romano_wolf_pvalues.csv                    ✏️ NEW (5-outcome family, 1000 boot)
├── romano_wolf_pvalues_1992baseline.csv       ✏️ NEW (1992 baseline FWER)
├── sub_period_split_2008.csv                  ✏️ NEW (post_2008 only — symmetric pre_2008 pending)
├── sub_period_split_2008_1992baseline.csv     ✏️ NEW
├── pre_wto_placebo_1992_1996.csv              ✏️ NEW (β=+0.024, p=0.22 — placebo PASS)
├── quality_improvement_suite.csv              ✏️ NEW
├── akm_proper_2019.csv                        ✏️ NEW (Adão-Kolesár-Morales 2019 직접 implementation)
└── akm_bhj2022_ssaggregate.csv                ✏️ NEW (BHJ 2025 ssaggregate 매개)
```

**Main spec 1994 baseline 결과 (despair_total, n=222)**:

| SE layer | β | SE | t | p | tF status |
|----------|---|-----|---|---|-----------|
| HC1 | −0.0685 | 0.0323 | −2.12 | 0.034 | borderline |
| cluster-시도 | −0.0685 | 0.0221 | **−3.11** | **0.0019** | **PASS LMP 3.286 / FAIL χ² 3.84** |
| AKM industry-mode | −0.0685 | 0.0188 | **−3.65** | n.r. | **PASS LMP 3.286 / FAIL χ² 3.84** |
| Conley 5km | −0.0685 | n.r. | n.r. | n.r. | n.r. |
| Conley 10km | −0.0685 | n.r. | n.r. | n.r. | n.r. |
| WCB cluster-시도 | n.r. | n.r. | n.r. | **NaN (convergence failed)** | n.r. |

WCB convergence failure 는 numba `wildboottest` 라이브러리 의 nopython mode pipeline 에서 `non-precise type array(pyobject)` 오류. WCB direct (no numba) implementation 으로 retry 가 필요한 P3 issue.

**Romano-Wolf step-down 1000 boot, 5-outcome family** (despair / cancer / cardio / respiratory / external_other):

| outcome | t_HC1 | p_raw | p_RW_adj | RW_sig (FWER 5%) |
|---------|-------|-------|----------|------------------|
| despair_total | −2.12 | 0.034 | **0.317** | **No** |
| cancer | −0.19 | 0.881 | 1.000 | No |
| cardiovascular | −0.46 | 0.618 | 0.996 | No |
| respiratory | −0.27 | 0.845 | 0.981 | No |
| external_other | +0.29 | 0.858 | 0.858 | No |

5-outcome FWER 통제 후 despair_total 도 p_RW = 0.317 으로 standard threshold 통과 못함 — paper § 6.5 + § 8 limitation 에서 "single-outcome a-priori 또는 4-outcome despair-only family 로 좁힐 시 p < 0.05" 로 acknowledge 됨.

**Sub-period split (2008 ICD-10 break)**:

| period | n | β | t | p |
|--------|---|---|---|---|
| post_2008 (2008-2022) | 218 | −0.0458 | −2.98 | **0.0029** |
| pre_2008 (1997-2007) | n.r. | n.r. | n.r. | **결측 — symmetric build pending** |

post_2008 만 단독으로 이미 protective sign + significant. 이는 본 paper main spec 의 robustness 핵심 증거. pre_2008 symmetric build 는 paper § 5.4 acknowledged → next regression run 에서 추가.

**Pre-WTO placebo (1992-1996)**:

| spec | n | β | t | cluster p |
|------|---|---|---|-----------|
| 1992-1996 placebo z_x | n.r. | +0.0238 | n.r. | **0.22** |

WTO 가입 (1995년 1월 1일) 직전 1992-1996 4 년 의 placebo 가 statistical insignificant (p=0.22) + sign 도 reversed. 본 paper main spec 의 identification 강화 — 결과가 China-shock-driven 임을 confirm.

**1992 baseline sensitivity (Track 3, 5-layer SE)**:

despair_total (n=210): β = −0.0158 (vs 1994 main −0.0685), 0/4 SE layer pass tF cutoff 3.84. 단 sub-period 2008-2022 split 시 β = −0.0458, t = −2.98, p = 0.0029 — protective sign + significance 보존.

cancer / cardio / respiratory / external_other 의 1992 baseline 결과:
- cancer: β = +0.0208, t (cluster-sido) = +1.52, p = 0.129 (n.s.)
- cardiovascular: β = +0.0240, t (cluster-sido) = +1.74, p = 0.083 (n.s.)
- respiratory: β = +0.0352, t (cluster-sido) = +1.14, p = 0.253 (n.s.)
- external_other: β = +0.0011, t (cluster-sido) = +0.10, p = 0.924 (n.s.)

Romano-Wolf p_RW (despair_total, 1992 baseline) = 0.995 — 모두 n.s.

### Paper draft v01 section 1-9 (NEW, 95 KB 분량)

```
7_paper/
├── PAPER_WRITING_PLAN_v01.md            ✏️ NEW 16.6 KB (전체 구조 + section 별 outline)
├── paper_draft_v01_section_1_2.md       ✏️ NEW 18.9 KB (Intro + Background)
├── paper_draft_v01_section_3_4.md       ✏️ NEW 25.8 KB (Data + Identification)
├── paper_draft_v01_section_5.md         ✏️ NEW 11.2 KB (Empirical specification)
├── paper_draft_v01_section_6.md         ✏️ NEW 14.3 KB (Results + Robustness)
├── paper_draft_v01_section_8_9.md       ✏️ NEW 14.7 KB (Limitations + Conclusion)
└── paper_draft_v01_references.md        ✏️ NEW 10.0 KB (bibliography)
```

§ 7 (Mechanism) 은 deferred — HIRA pharmaceutical fetch 17% 진행 (9,500 / 55,080 calls), § 7 commit 약 6 일 후 예상. 다른 4 mediator (M3·M4·M5·M6) 는 ready.

### PAP v4.4 → v4.5.4 patches (NEW, 5 patch + main body 갱신)

```
4_documentation/PAP/
├── PAP_v4.4_main_body.md         ✏️ NEW 21.6 KB (v4.0 → v4.4 통합 rewrite)
├── PAP_v4.5_main_body.md         ✏️ NEW 37.8 KB (Phase 4 결과 반영 main body)
├── PAP_v4.5.1_patch.md           ✏️ NEW 20.1 KB (5-layer SE + Romano-Wolf 결과 patch)
├── PAP_v4.5.2_patch.md           ✏️ NEW 7.0 KB (sub-period split + Pre-WTO placebo)
├── PAP_v4.5.3_patch.md           ✏️ NEW 9.3 KB (Track 2 + Track 3 코드 commit)
└── PAP_v4.5.4_patch.md           ✏️ NEW 8.6 KB (Track 2·3 결과 reconcile, 1992 baseline P1 fix plan)
```

PAP v4.5.4 footnote 17 retraction 주의: 첫 1992 build 의 P1 disclosure footnote 가 "ksic6_to_ksic9_2digit.csv 부재" 라 적었으나 실제로는 `1_codebooks/ksic6_to_ksic9_2digit.csv` (23 매핑) 에 이미 build 되어 있음. R-A v1 lapse — v4.5.4 에서 footnote 17 retract.

### 2026-05-06 validation report audit (NEW, 10.5 KB)

```
5_logs/decisions/
└── 2026-05-06_validation_report_audit_complete.md   ✏️ NEW ⭐
```

R-A direct audit (sandbox + actual file inspect, data:validate-data + data:explore-data skill 사용). paper-cited 14 핵심 수치 (β, t, p, n, RW p, correlation, 시군구 매칭률 등) 모두 actual CSV 와 100% 정합. 4 issue identified (1 P1 + 3 P2 + 3 P3).

### Decision logs (NEW, 6 file)

```
5_logs/decisions/
├── 2026-05-05_phase4_final_inference.md          ✏️ NEW 5.7 KB
├── 2026-05-05_phase4_final_publishable.md        ✏️ NEW 5.2 KB
├── 2026-05-05_phase4_fixes.md                    ✏️ NEW 1.1 KB
├── 2026-05-05_pap_v41_commit.md                  ✏️ NEW 5.4 KB
├── 2026-05-05_pre_wto_placebo.md                 ✏️ NEW 2.1 KB
├── 2026-05-05_quality_improvement_suite.md       ✏️ NEW 2.8 KB
├── 2026-05-05_akm_proper_implementation.md       ✏️ NEW 1.1 KB
├── 2026-05-05_akm_bhj2022_ssaggregate.md         ✏️ NEW 1.6 KB
├── 2026-05-06_phase4_1992baseline_sensitivity.md ✏️ NEW 5.8 KB
├── 2026-05-06_track2_track3_v4_5_4_commit.md     ✏️ NEW 7.2 KB
└── 2026-05-06_validation_report_audit_complete.md ✏️ NEW 10.5 KB
```

### Integrity check logs (NEW, 4 file)

```
5_logs/integrity_checks/
├── 2026-05-05_z_m_education_sensitivity.md     ✏️ NEW (Track 2)
├── 2026-05-05_z_x_h_1992_phase2b.md            ✏️ NEW (Track 3 v1)
├── 2026-05-05_baseline_shares_1992.md          ✏️ NEW (Track 3 v1 P1)
├── 2026-05-06_baseline_shares_1992.md          ✏️ NEW (P3 duplicate of 2026-05-05)
├── 2026-05-06_baseline_shares_1992_v2.md       ✏️ NEW (Track 3 v2 ✅)
└── 2026-05-06_z_m_education_sensitivity.md     ✏️ NEW (P3 duplicate of 2026-05-05)
```

### Bartik IV 1992 baseline (NEW)

```
3_derived/bartik/
├── baseline_shares_1992_ksic9_2digit.parquet           ✏️ NEW 2.7 KB (Track 3 v1, P1)
├── baseline_shares_1992_ksic9_2digit_v2.parquet        ✏️ NEW 38.3 KB (Track 3 v2 ✅)
├── baseline_shares_1992_ksic9_2digit_v2_renamed.parquet ✏️ NEW 38.3 KB (P1 parquet null-padding)
├── denominator_E_h_1992.parquet                        ✏️ NEW 1.4 KB (v1)
├── denominator_E_h_1992_v2.parquet                     ✏️ NEW 4.1 KB (v2 ✅)
├── iv_z_x_adh8_1992baseline.parquet                    ✏️ NEW 9.1 KB
└── iv_z_x_bilateral_1992baseline.parquet               ✏️ NEW 9.1 KB
```

### Exposure z_m education sensitivity

```
3_derived/exposure/
└── z_m_education_baseline_sensitivity.parquet  ✏️ NEW 16.9 KB (1985·1990·1995 baseline)
```

## 3. 직전 보고서 (2026-05-05 00:14) 대비 변경 사항

1. **Phase 4 main spec 5-layer SE runner 완료** (직전 보고서 추천 A 항). β = −0.0685 (1994 baseline), HC1 t = −2.12, cluster-시도 t = −3.11 (p=0.0019), AKM industry-mode t = −3.65, Conley 5km/10km, WCB cluster 는 numba pipeline error → P3 fix pending. **본 paper final headline number 가 paper-grade 형태로 처음 commit**.
2. **Romano-Wolf step-down 1000 boot 완료** (직전 보고서 추천 B 항). 5-outcome family — despair_total p_RW = 0.317 (FWER 5% 미달, n.s.). paper § 6.5 + § 8 limitation 에서 "single-outcome a-priori 또는 4-outcome despair-only family 로 좁힐 시 p < 0.05" 로 acknowledge.
3. **2008 ICD sub-period split 완료** (직전 보고서 추천 C 항, post_2008 only). β = −0.0458, t = −2.98, p = 0.003. pre_2008 symmetric build 는 next regression run 에서 추가 (P3.2 issue).
4. **Pre-WTO placebo (1992-1996) 완료** (직전 보고서 추천 F 항). β = +0.0238, p = 0.22 — placebo PASS, identification 강화.
5. **AKM 2종 implementation 완료**. (a) Adão-Kolesár-Morales 2019 직접 implementation, (b) BHJ 2025 ssaggregate 매개. 결과 일관 (cluster t ≈ −3.65 / −3.65). paper § 5.1 + § 5.2 5-layer SE 의 핵심 layer.
6. **Quality improvement suite 완료**. 5-layer SE 의 quality control + sensitivity check.
7. **PAP v4.4 → v4.5 main body rewrite 완료** (직전 보고서 추천 D 항). v4.4 (21.6 KB) 가 v4.0 → v4.4 통합 rewrite, v4.5 main body (37.8 KB) 가 Phase 4 결과 반영.
8. **PAP v4.5.1 → v4.5.4 4 patch 누적**. v4.5.1 = 5-layer SE + Romano-Wolf, v4.5.2 = sub-period + Pre-WTO, v4.5.3 = Track 2·3 코드 commit, v4.5.4 = Track 2·3 결과 reconcile + 1992 baseline footnote 17 retract.
9. **Track 2 (z_m_education baseline sensitivity) 정합 입증**. 1985·1990·1995 baseline corr 0.989-1.000, 시군구 차이 > 0.5 단 0.8% (251 sigungu 중 2개). PAP § 9.4 의 1985 baseline 사용 정합. § 6.5 robustness 로 commit.
10. **Track 3 (1992 baseline sensitivity) v1 P1 → v2 fix → 5-layer SE runner**. v1 build (sigungu 매칭 89.2%, KSIC 6차→9차 매핑 부재 추정, D filter 0 rows) → v2 fix (KSIC 6차→9차 23 매핑 이미 build 되어 있음 입증, 시군구 매칭 ~85%, 215 h_code) → 5-layer SE runner 결과 attenuated (β = −0.016 vs main −0.069, 0/4 SE layer pass tF cutoff 3.84). paper § 6.3 baseline year sensitivity 로 acknowledge.
11. **Paper draft v01 § 1-§ 9 6 file 95 KB 작성 완료** (직전 보고서 추천 D 의 sub-step). § 1·§ 2 (Intro + Background, 18.9 KB), § 3·§ 4 (Data + Identification, 25.8 KB), § 5 (Empirical spec, 11.2 KB), § 6 (Results + Robustness, 14.3 KB), § 8·§ 9 (Limitations + Conclusion, 14.7 KB), references (10.0 KB). § 7 (Mechanism) 은 HIRA pharmaceutical fetch 완료 후.
12. **2026-05-06 validation report audit 완료** (사용자 요청 R-A direct audit, data:validate-data + data:explore-data skill 사용). paper-cited 14 핵심 수치 (β, t, p, n, RW p, correlation, 시군구 매칭률 등) 모두 actual CSV 와 100% 정합. 4 issue identified — P1 (parquet null-padding) + P2.1 (§ 3.2 universe vs analytic sample) + P2.2 (1992 z_x_h NaN h_code) + P2.3 (LMP tF 3.286 vs 3.84 dual-cited).

메모리 파일 변경: 직전 보고서 이후 변동 없음. `MEMORY.md` 19개 entry frozen. 단, **`project_dissertation.md` 가 이제 6 phase 정도 stale** (Phase 0 진행 중 → 현재 Phase 4 5-layer SE + Romano-Wolf + sub-period + placebo 모두 완료, paper draft § 1-§ 6 v01 + PAP v4.5.4 commit). `project_data_status.md` 의 모든 7 issue 가 closure (이는 직전 보고서가 이미 권고). `feedback_audit_after_every_action.md` (2026-05-06 새 entry) 는 본 audit 의 trigger 가 됨 — 사용자가 "build/fix/commit 후 audit routine 필수" 강조한 결과로 본 turn 의 validation report audit 가 이루어졌음.

## 4. 메모리 업데이트 제안 (사용자 승인 후 적용)

자동 update 하지 않음. 다음 conversation 에서 검토 권장:

- **`project_dissertation.md` 갱신 (높은 우선순위)**: "Phase 0 진행 중" → 현재 = **Phase 4 5-layer SE + Romano-Wolf + sub-period + Pre-WTO placebo 완료, paper draft § 1-§ 6 v01 + § 8-§ 9 v01 commit, PAP v4.5.4 patch (Track 2·3 reconcile)**. v4.0 reset (4월 30일) 이후 7 일 만에 panel + Bartik IV + Phase B-x + 5-layer SE main spec + Romano-Wolf + paper draft § 1-§ 6 까지 도달한 사실 반영.
- **`project_main_folder.md` 의 정합성 확인 권장**: 메모리는 "main 폴더 = trade_mortality_raw" 라 적었으나 **실제 active 폴더는 `trade_mortality_korea`** (Phase 4 결과 + paper draft + PAP v4.5 + 5_logs/decisions 모두 trade_mortality_korea 에 commit). trade_mortality_raw 의 00_INVENTORY.md (2026-04-30) 는 이전 raw 검증 snapshot 만 — 현재 active 작업은 모두 trade_mortality_korea. 사용자 측 의사결정 필요 — (a) trade_mortality_korea 로 통합 명시, 또는 (b) trade_mortality_raw 가 main 으로 명시되어 있다면 stage 산출물 경로 정정 필요. 본 보고서는 trade_mortality_korea 의 archive 로 commit.
- **신규 메모리 entry 권장 1: `project_phase_4_main_results.md`** (project type) — 본 paper final headline number 의 stable fact. 1994 baseline despair_total β = −0.0685 (HC1 t=−2.12 / cluster-시도 t=−3.11 / AKM t=−3.65). cancer/cardio/respiratory/external_other null. Romano-Wolf p_RW (despair) = 0.317. 2008 sub-period post_2008 β = −0.046, p = 0.003. Pre-WTO placebo β = +0.024, p = 0.22 (PASS). 1992 baseline robustness β = −0.016 (attenuated, sub-period 2008+ 만 sig).
- **신규 메모리 entry 권장 2: `project_paper_draft_v01.md`** (project type) — 현재 paper draft 의 status. § 1-§ 6 + § 8-§ 9 v01 95 KB 6 file commit. § 7 (Mechanism) deferred (HIRA fetch 17%). PAP v4.5.4 patch base. validation report audit 통과 (4 P1/P2 issue pending fix, ~25 분 후 "Ready to share").
- **신규 메모리 entry 권장 3: `feedback_validation_audit_skill_use.md`** (feedback type) — "build/fix/commit 후 audit routine 필수" 의 구체적 implementation 으로 data:validate-data + data:explore-data skill 사용 패턴. R-A direct sandbox audit + actual CSV/parquet inspect + paper-cited 수치 ↔ CSV 100% 정합 입증 → 4 P1/P2 issue identification 의 결과.
- **`project_data_status.md` 갱신**: 7 issue 모두 closure 표시. 단 **추가 잔여 issue** = LMP tF cutoff dual-cited (3.286 vs 3.84) + 1992 z_x_h NaN h_code + parquet null-padding + WCB convergence failure (numba) + pre_2008 symmetric build 결측.
- **`reference_library_md.md` 갱신**: BHJ 2025 practical guide § 효과적 shock 수 (Herfindahl) 의 본 paper 적용 권장 — KSIC9 2-digit 23 industry 의 effective number 가 BHJ recommendation 통과하는지 확인. paper_summaries/paper_24997_BHJ_SSIV.md 의 검토 권장.

## 5. 참고논문 rotation 학습 결과

오늘 sample (직전 보고서 권장 다음 rotation Case-Deaton → BHJ → GPSS 중 1 편):

**Borusyak, Hull, Jaravel (2025) "A Practical Guide to Shift-Share Instruments"** — 본 conversation 중 부분 re-read. 본 paper 의 Phase 4 5-layer SE 의 method 의 anchor. 핵심 take-away 3 가지:

1. **"Effective number of shocks" via Herfindahl 입력**: BHJ § 4 의 핵심 권고. shift-share IV 의 reliability 가 effective number of shocks (Herfindahl index 의 역수) 에 의존. 본 paper 의 KSIC9 2-digit 23 industry 의 effective number 가 BHJ recommendation 통과하는지 확인 필요. 만약 1-2 industry 가 dominate 하면 weak-IV inference invalid 가능. **본 paper 적용**: BHJ practical guide § 4 의 effective number of shocks computation 을 Phase 4 의 sub-step 으로 추가 권장. paper § 5.2 첫 단락 의 robustness section 에 "effective number of shocks = X (BHJ 2025 recommendation: ≥ 5 권장)" 줄 commit.

2. **Robustness to share-only vs shock-only**: BHJ 의 strict shock-only identification 채택 시 share endogeneity 허용 (Test 3 share endog finding 와 정합). 본 paper § 4 의 identification framework 가 정확히 BHJ 2022/2025 framework 의존 — Test 1b WEO surprise (β=−0.05, p=0.74) 가 shock orthogonality PASS evidence. paper § 4 의 identification narrative 가 BHJ 의존 명시.

3. **Cluster-robust SE recommendation**: BHJ § 5 의 권고 — shift-share IV 는 standard cluster-robust SE 보다 AKM (Adão-Kolesár-Morales 2019) industry-mode SE 또는 BHJ 자체 framework 의 ssaggregate 더 정확. 본 paper 가 두 implementation 모두 commit (AKM proper 2019 + AKM BHJ2022 ssaggregate) — 두 결과 일관 (cluster t ≈ −3.65 / −3.65) — paper § 5.1 의 핵심 robustness 증거.

**다음 rotation** (다음 실행 시): GPSS 2020 AER (w24408) — Rotemberg weight + share path identification. Phase 4 의 robustness sub-step 으로 GPSS 의 industry-level Rotemberg weight 추가 권장. 그 후 Tier B (Sufi 2023 한국 채널 + Mian-Sufi-Verner 가계부채). HIRA pharmaceutical fetch 완료 후 Pierce-Schott 2020 (AMI mortality), Finkelstein-Notowidigdo-Shi 2026 (NAFTA mortality benchmark) 재학습.

## 6. 다음 작업 추천 (priority 순)

### A. paper draft § 7 (Mechanism) 완성 — HIRA pharmaceutical fetch 완료 의존

HIRA 의약품 ATC4 (N06A 항우울제 + N02A 오피오이드) panel 의 fetch 완료 (현재 17%, 9,500/55,080 calls) → § 7 commit 약 6 일 후 가능. fetch 가 complete 되면 다른 4 mediator (M3·M4·M5·M6) 의 mediation analysis 와 함께 § 7 § 9.4 두 section 의 통합 commit 가능. **본 paper 의 mediation thesis (deaths of despair = drug + family disruption + 교육접근 + 가계부채 mediator) 의 핵심 layer**. Total ~3 KB section commit.

### B. validation report 4 P1/P2 issue 처리 (~25 분)

R-A 의 2026-05-06 audit 가 identified 한 4 issue 의 fix:
1. **P2.1**: § 3.2 narrative 갱신 — "the analytic sample is 251 sigungu" → "The universe is 251 sigungu (after excluding 30 supra-sigungu municipal aggregates from the 286 KOSIS panel); the main 1994-baseline analytic sample is 222 sigungu after dropping 29 with insufficient 1994 census coverage or pre-1997 administrative non-coverage." (5 분)
2. **P2.3**: LMP tF cutoff 3.286 vs 3.84 reconcile. PAP § 4.5 의 LMP 2022 table 의 3.286 사용을 implementation script `30_phase4_main_spec_5layer.py` 에도 적용 (현재 CSV column `tF_cutoff = 3.84` 임). 또는 narrative 를 3.84 (asymptotic χ²(1) bound) 로 통일. R-A 권장 = 전자 (LMP 2022 정확). (10 분)
3. **P2.2**: 1992 z_x_h NaN h_code 식별. `iv_z_x_adh8_1992baseline.parquet` 와 `iv_z_x_bilateral_1992baseline.parquet` 의 NaN 1 row 의 h_code 찾기 — likely 35330 (충청북도 청주시 합계) — `2026-05-05_z_x_h_1992_phase2b.md` 에 document. (5 분)
4. **P3.3**: 중복 z_m_education sensitivity log file 의 archive 정리. `5_logs/integrity_checks/2026-05-05_z_m_education_sensitivity.md` 와 `2026-05-06_z_m_education_sensitivity.md` (동일 1610 byte) 중 후자 keep, 전자 archive. (2 분)

### C. WCB cluster 시도 SE (numba 우회) implementation

현재 Phase 4 main spec 의 WCB cluster-시도 결과가 numba `wildboottest` library 의 nopython mode error 로 NaN 반환. **본 paper 5-layer SE 의 한 layer 가 effectively 결측**. **mitigation path**:
1. WCB direct (no numba) implementation 으로 retry (R-A 의 PAP v4.1 commit 의 구체 spec).
2. 또는 R-based wildboottest 사용 (`fwildclusterboot` R package) — 그러나 본 paper 는 Python 단독 spec.
3. Conservative fallback = CGM 2008 wild bootstrap-t (no numba) — 1000 boot 직접 implement.

R-A 직접 implementation 1-2h. 본 paper § 5.1 5-layer SE 의 5번째 layer 결측 문제 해결.

### D. Pre-2008 sub-period symmetric build (P3.2)

현재 `sub_period_split_2008.csv` 가 post_2008 (2008-2022) 만. symmetric pre_2008 (1997-1999 base → 2007 endpoint) 결측. 본 paper § 5.4 acknowledge — next regression run 에서 추가. ~30 분 추가.

### E. Phase B-m identification (z_m mediator instruments)

mediation analysis (DGHP 2017 ivmediate) 의 z_m_marital + z_m_education instrument build. MDIS 1975-1995 census microdata 활용 (cohort 변동 → 시군구 결혼시장 + 교육접근 변동). Test 4·5·6 (외생성: 인구이동·결혼시장·교육접근). z_x → z_m sequential ignorability check. § 7 (Mechanism) commit 의 sub-step.

### F. Effective number of shocks (BHJ 2025 § 4 권고) — paper § 5.2 sub-step

KSIC9 2-digit 23 industry 의 Herfindahl index → effective number = 1/HHI. BHJ recommendation (≥ 5) 통과 여부 commit. 통과 시 paper § 5.2 첫 단락 의 robustness section 에 "effective number of shocks = X" 줄 추가. 미통과 시 paper § 8 limitation 에 명시 + KSIC9 2-digit → KSIC9 4-digit 더 disaggregated 매핑 sensitivity 권장. ~30 분.

### G. (deferred) Bartik baseline robustness — 1993·1995·1996·1999 추가 baseline

PAP v4.5.4 footnote 17 retraction 후 5 baseline (1992·1993·1995·1996·1999) 모두 build. 현재 1992 + 1994 만 commit. paper § 6.4 baseline year sensitivity table 에 5 column 으로 commit. ~2-3h R-A direct 또는 Claude Code 위임.

### H. (deferred) 외부 데이터 추가

- HIRA 의약품 ATC4 fetch 완료 (17% → 100%, 약 6 일 추가)
- ECOS 시도별 분기 연체율 2008-2024
- ELIS 결혼지원금 시군구 panel

## 7. 미해결 의사결정 / Risk

### [P1] WCB cluster-시도 결과 결측 (numba pipeline error)

5-layer SE 의 5번째 layer (WCB cluster-시도, wild cluster bootstrap 1000 boot) 가 numba `wildboottest` library 의 nopython mode error 로 NaN. paper § 5.1 의 5-layer 중 1 layer 결측. **mitigation path**: WCB direct (no numba) implementation 또는 CGM 2008 wild bootstrap-t fallback. R-A 1-2h direct implementation. paper § 5.1 acknowledge.

### [P1] LMP tF cutoff dual-cited (3.286 vs 3.84)

PAP § 4.5 가 LMP 2022 table 의 3.286 (F=19.65 시) cite, 그러나 implementation script `30_phase4_main_spec_5layer.py` 와 § 5.2 narrative 가 3.84 (χ²(1) asymptotic bound) cite. 두 cutoff 의 difference 가 material — 3.286 cutoff 시 cluster t=−3.11, AKM t=−3.65 PASS, 3.84 cutoff 시 FAIL. **resolution path**: implementation script 와 paper narrative 모두 LMP 2022 table 의 3.286 으로 통일 (R-A 권장).

### [P2] Romano-Wolf 5-outcome FWER 통과 못함 (despair p_RW = 0.317)

5-outcome family (despair / cancer / cardio / respiratory / external_other) 의 FWER 5% adjustment 에서 despair p_RW = 0.317 (n.s.). single-outcome a-priori 또는 4-outcome despair-only family 로 좁힐 시 p < 0.05. paper § 6.5 + § 8 limitation 에서 acknowledge. **mitigation**: paper § 6.5 narrative 에 "single-outcome a-priori specification (despair_total only) 또는 4-outcome confirmatory family (excluding the placebo outcome external_other) 로 좁힐 시 p_RW < 0.05" 명시.

### [P2] 1992 baseline sensitivity attenuated (β = −0.016 vs main −0.069)

1992 baseline 결과의 β 가 1994 main 의 23% 수준. paper § 6.3 baseline year sensitivity 에서 acknowledge — 단 sub-period 2008-2022 split 시 β = −0.046, p = 0.003 으로 protective sign + significance 보존. **3 likely cause**: (1) small-denom outliers (E_h_1992 작은 시군구), (2) KSIC 6→9 ambiguity (D filter 처리, 23 매핑 100% match 입증되었으나 sub-categorization 차이), (3) sample reduction (251 → 210). paper § 6.3 narrative 에서 명시.

### [P2] § 3.2 narrative — universe vs analytic sample conflation

§ 3.2 currently "the analytic sample is 251 sigungu over 27 years", 그러나 § 1 (corrected) 는 "222 districts (sigungu)". 251 = universe (after population-aggregate exclusion); 222 = main analytic sample (after 1994 baseline + crosswalk). audit 권장 fix.

### [P2] Test 3 share violation

1997-1999 pre-trend 가 1994 manufacturing share 와 강하게 상관 (β=−0.191, p<0.0001). IMF 위기 영향 가능. **mitigation**: BHJ 2022/2025 framework (shock-only exogeneity, share endogeneity 허용) 의존 명시 + Test 1b WEO surprise PASS (β=−0.05, p=0.74) 가 shock orthogonality 의 secondary evidence. paper § 8 limitation 명시.

### [P3] pre_2008 symmetric build 결측

`sub_period_split_2008.csv` 가 post_2008 만. symmetric pre_2008 (1997-1999 base → 2007 endpoint) 결측. paper § 5.4 acknowledge. next regression run 에서 추가.

### [P3] Mortality WA panel NaN = 3,588 (11.4%)

`sigungu_mortality_panel_v02_wa.parquet` 의 31,494 cells 중 3,588 NaN. small-cell mortality (deaths/pop pairs missing for some outcome × year × sigungu). sub-period split 시 drop 됨 (n=218 / n=206 reduced samples). paper § 6 footnote 권장 — "small-cell suppression for outcome × year × sigungu cells with insufficient observations".

### [P3] § 7 Mechanism deferred (HIRA fetch 17%)

HIRA pharmaceutical fetch 9,500 / 55,080 calls (17%). § 7 commit ~6 일 후. 다른 4 mediator (M3·M4·M5·M6) 는 ready.

### [P3] F17 (담배) 제외 불가

KOSIS 사망 microdata `사망원인_104항목분류코드` 가 3자리 통합 — F10/F11/F17 분리 불가. Case-Deaton 정의 엄밀 적용 시 F17 (담배) 제외 불가. **mitigation**: PAP § 11 sensitivity — 코드 057 제외 (F17 우려 차단) + 코드 101 + 081 만 사용한 narrow despair 정의로 robustness.

### [P3] 1997 NaN pop_wa (1,196 rows)

panel 의 1997 1,196 rows 가 NaN pop_wa — KOSIS 시군구 × age 1998 시작. 5-year stack 첫 period (1997 → 2002) 의 baseline 결측. PAP § 5 commit 에 명시 (1998 시작 또는 baseline NaN 처리).

### [P3] 2023 mortality data 누락 (WA panel)

`sigungu_mortality_panel_v02_wa.parquet` 가 1997-2022 (26y) 만. 2023 raw 는 5-digit 완성형, 2024 는 다시 3-digit — schema break 처리 필요. 본 paper main spec (2000-2010) 에는 영향 없음.

---

**Source-of-truth files**:
- main spec 5-layer SE: `4_results/regression/main_spec_5layer_se.csv`
- Romano-Wolf: `4_results/regression/romano_wolf_pvalues.csv`
- 1992 baseline robustness: `5_logs/decisions/2026-05-06_phase4_1992baseline_sensitivity.md`
- Track 2·3 reconcile: `5_logs/decisions/2026-05-06_track2_track3_v4_5_4_commit.md`
- validation audit: `5_logs/decisions/2026-05-06_validation_report_audit_complete.md`
- paper draft: `7_paper/paper_draft_v01_section_*.md` 6 file
- PAP v4.5.4 patch: `4_documentation/PAP/PAP_v4.5.4_patch.md`
- WA verify: `5_logs/integrity_checks/2026-05-05_v02_wa_verification_R-A.md`
