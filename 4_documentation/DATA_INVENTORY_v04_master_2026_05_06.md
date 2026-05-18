# Data Inventory v04 — Trade × Mortality Korea (2026-05-06)

**Author**: R-A
**Cross-reference**: PAP v4.5 § 3 (Data Sources), paper draft v01 § 3 (Data)
**Prior versions**: v01-v03 (2026-05-05). v04 reflects post-Track 2/3 + Phase 2-B + paper draft state.

---

## 1. 전체 데이터 규모 종합

**총 raw data**: ~10.5 GB (trade_mortality_korea/0_raw)
**총 processed**: ~110 MB (trade_mortality_korea/3_derived)
**총 logs + paper**: ~1 MB

---

## 2. 0_raw 폴더 카테고리별 inventory

### 2.1 사망 데이터 (mortality, KOSTAT)

| Folder | Size | Files | Status | Coverage |
|--------|------|-------|--------|----------|
| `mortality_kostat/` | **462 MB** | 41 csv | ✅ complete | 1997-2024, 28 annual files + supplementary |
| `kostat_mortality_aggregated/` | 39 MB | aggregated csv | ✅ | KOSTAT 발표값 cross-check |

→ 본 paper main outcome data. Working-age 25-64 + Korean nationality + 5 outcome group 처리 완료.

### 2.2 인구·경제 panel (KOSIS·ECOS)

| Folder | Size | Files | Status |
|--------|------|-------|--------|
| `kosis_population/` | **495 MB** | 11 csv | ✅ 286 sigungu × 1993-2023, 31년 |
| `kosis_business_survey/` | **1.6 GB** | 38 csv | ✅ 광업·제조업조사 1989-2024 |
| `kosis_industry_summary/` | 1.4 MB | csv | ✅ 광공업통계 요약 |
| `kosis_marriage_education/` | 76 MB | csv | ✅ M3 family mediator |
| `kosis_family_mediators/` | 18 MB | csv | ✅ 출생·혼인·이혼 |
| `kosis_welfare_recipients/` | 27 MB | csv | ✅ 복지수급자 |
| `kosis_foreign_residents/` | 21 MB | csv | ✅ 외국인 시군구 분포 |
| `kosis_medical_infra/` | 19 MB | csv | ✅ 의료기관 인프라 |
| `kosis_housing/` | 12 KB | csv | ✅ 주택 통계 |
| `kosis_birth_sex_ratio/` | 4 KB | csv | ✅ M4 mediator support |
| `kosis_religion/` | 4 KB | csv | ✅ 종교 분포 |

→ ECOS 거시 통계는 별도 (ecos_macro 35 MB, ecos_household_credit 3.7 MB, ecos_delinquency 6.7 MB).

### 2.3 무역 데이터 (UN Comtrade)

| Folder | Size | Files | Status | Notes |
|--------|------|-------|--------|-------|
| `comtrade_adh_china/` | **706 MB** | **201 csv** | ✅ ADH-8 8 country × 2000-2024 25 year |
| `comtrade_korea_china/` | **68 MB** | 61 csv | ✅ KR ↔ CN bilateral 2000-2024 |
| `comtrade_china_world/` | 39 MB | 26 csv | ✅ CN → World aggregate |

→ ADH-8 = Australia, Switzerland, Germany, Denmark, Spain, Finland, Japan, New Zealand. 본 paper Bartik IV instrument 의 source.

### 2.4 산업 분류 + crosswalk

| Folder | Size | Status |
|--------|------|--------|
| `hs_ksic_concordance/` | 2.1 MB | ✅ KIET 60 sector + KSIC 9차 매핑 |
| `hs_isic4_concordance/` | 1.5 MB | ✅ HS6 → ISIC4 alternate |
| `crosswalks/` | 12 MB | ✅ 시군구 변경 + KSIC 변환 |

### 2.5 HIRA (Mediator M1 + M2)

| Folder | Size | Status | Coverage |
|--------|------|--------|----------|
| `hira_drug/` (paper folder) | 36 MB | 🟡 fetch 진행 중 | 17.2% (9,500 / 55,080 calls) |
| `hira_quarterly/` | 87 MB | ✅ KOSIS HIRA quarterly aggregate (2009-2025) |
| `hira_medical_institutions/` | 21 MB | ✅ M2 의료기관 분포 |

**HIRA drug fetch 진행도** (raw 폴더 별도):
- panel rows accumulated: **46,015 / ~266,500 expected** (17.3%)
- 9 ATC × 250 sigungu × 12 month × 2 endpoint year = 55,080 calls
- 5/9 ATC complete (5 mental drugs), 4/9 pending (1 opioid + 3 negative control)
- 44/250 sigungu coverage (current daily fetch 진행)
- Daily quota 9,500 → 약 5-6 days remaining for full panel

### 2.6 MDIS (z_m_marital + 인구주택총조사)

| Folder | Size | Status |
|--------|------|--------|
| `mdis_population_census/` | **1.5 GB** | ✅ 1990 census 16 csv (M4 z_m_marital baseline) |

### 2.7 KEDI (z_m_education baseline)

| Folder | Size | Status |
|--------|------|--------|
| `1985_yunbo_total/` | **186 MB** | ✅ KEDI 1985 yearbook (171 universities baseline) |
| `1990_yunbo_total/` | 20 MB | ✅ 1990 yearbook (175 universities) |
| `1995_yunbo_total/` | 57 MB | ✅ 1995 yearbook (175 universities) |
| `edu_university_list_1990/` | 88 KB | ✅ 보조 list |
| `moe_university_quota/` | 4 KB | ✅ 입학 정원 |

→ Track 2 z_m_education baseline sensitivity 정합 입증 (1985 vs 1990 corr=0.989).

### 2.8 NHIS Health (Mediator support)

| Folder | Size | Status |
|--------|------|--------|
| `nhis_health/` | **5.2 GB** | ✅ 30 csv (M2 정신질환 alternative source — 본 paper 미사용) |

### 2.9 보조 source

| Folder | Size | Notes |
|--------|------|-------|
| `imf_weo_korea_vintage/` | 8.6 MB | Phase B-x Test 1b WEO surprise |
| `sigungu_centroid/` | 380 KB | Conley spatial HAC + z_m_education haversine |
| `ssaggregate-main/` | 42 MB | BHJ R package |
| `ecos_macro_extra/` | 528 KB | 보조 거시 |
| `mma_conscription/` | 4 KB | 군 입영 (mediator support) |
| `nec_election/` | 4 KB | 선거 결과 (보조) |
| `elis_marriage_subsidy/` | 4 KB | 결혼지원금 (mediator support) |
| `research_supp/` | 0 | 비어있음 |
| `research_materials/` | 528 MB | reference paper PDF + supporting docs |

---

## 3. 1_codebooks (codebook + crosswalks)

| File | Size | Status |
|------|------|--------|
| `sigungu_crosswalk.csv` | 331 KB | ✅ 6,723 rows, 256 h_code 2021 baseline |
| `sigungu_crosswalk_v2.csv` | 361 KB | ✅ Phase 1-A v2 |
| `sigungu_changes_history.md` | 17 KB | ✅ 111 changes 1997-2023 |
| `mortality_104_classification.csv` | 8.4 KB | ✅ KOSTAT 104 cause-of-death codes |
| `kosis_104_to_icd10.yaml` | 6.6 KB | ✅ outcome group mapping |
| `ksic6_to_ksic9_2digit.csv` | 268 B | ✅ 23 mappings (D15→C10 등) |
| `child_to_parent_mapping.csv` | 1.4 KB | ✅ KOSIS aggregation |
| `crosswalk_merge_report.md` | 5.2 KB | ✅ merge audit |

---

## 4. 3_derived (processed panels + Bartik build)

### 4.1 Bartik IV outputs

| File | Size | Status |
|------|------|--------|
| `baseline_shares_1992_ksic9_2digit_v2.parquet` | 38 KB | ✅ 215 h_code × 22 KSIC9 (Track 3 v2) |
| `baseline_shares_1992_ksic9_2digit_v2_renamed.parquet` | 38 KB | ✅ regression input (NaN drop, 214 h_code) |
| `baseline_shares_1994_ksic9_2digit.parquet` | 47 KB | ✅ main 1994 baseline (251 h_code × 23 KSIC9) |
| `baseline_shares_1994_all_industries.parquet` | 256 KB | ✅ all KSIC9 (manufacturing + non) |
| `baseline_shares_1994_manufacturing.parquet` | 84 KB | ✅ manufacturing only |
| `denominator_E_h_1992_v2.parquet` | 4 KB | ✅ |
| `denominator_E_h_1994.parquet` | 4 KB | ✅ |
| `exposure_adh8_2000_2010.parquet` | 3.5 KB | ✅ ΔM_ADH8 by KSIC9 |
| `exposure_bilateral_2000_2010.parquet` | 3.5 KB | ✅ ΔM_KR-CN by KSIC9 |
| `iv_z_x_adh8.parquet` | 9.4 KB | ✅ z_x_h ADH-8 (1994 baseline, n=251) |
| `iv_z_x_bilateral.parquet` | 9.4 KB | ✅ z_x_h KR-CN (1994 baseline, n=251) |
| `iv_z_x_adh8_1992baseline.parquet` | TBD | ✅ Phase 2-B (215 h_code, NaN=1) |
| `iv_z_x_bilateral_1992baseline.parquet` | TBD | ✅ Phase 2-B (215 h_code, NaN=1) |
| `hs6_to_ksic9_2digit.parquet` | 38 KB | ✅ HS6 → KSIC9 매핑 |

### 4.2 Mortality panels

| File | Size | Status |
|------|------|--------|
| `sigungu_mortality_panel_v02_wa.parquet` | 31,494 rows | ✅ Working-age 25-64 panel (1997-2024) |
| `mortality_panel_v02_education.parquet` | TBD | ✅ M5 mediator panel |
| `mortality_panel_v02_marriage.parquet` | TBD | ✅ M3·M4 mediator panel |
| `mortality_panel_v02_occupation.parquet` | TBD | ✅ 보조 mediator panel |
| `mortality_microdata_combined.parquet` | TBD | ✅ raw microdata 통합 |

### 4.3 Exposure (mediator)

| File | Size | Status |
|------|------|--------|
| `z_m_education_baseline_sensitivity.parquet` | 251 rows | ✅ Track 2 (1985·1990·1995 3 baseline) |
| `d5_log_employment_2000_2010.parquet` | TBD | ✅ Phase 2-B 의 LHS 변수 |
| `mediator_specific_education_rate_v01.parquet` | 1.5 MB | ✅ M5 처리 |

### 4.4 Identification (Phase B-x)

| Folder | Status |
|--------|--------|
| `3_derived/identification/` | ✅ Test 1·1b·3 + first-stage F 결과 |

---

## 5. 4_results (regression outputs)

| File | Size | Spec |
|------|------|------|
| `main_spec_5layer_se.csv` | 1.9 KB | ✅ 1994 main, 5 outcome × 5 SE layer |
| `main_spec_5layer_se_1992baseline.csv` | 1.9 KB | ✅ 1992 sensitivity, 5 outcome |
| `romano_wolf_pvalues.csv` | 360 B | ✅ 1994 main RW |
| `romano_wolf_pvalues_1992baseline.csv` | 361 B | ✅ 1992 RW |
| `sub_period_split_2008.csv` | 144 B | ✅ post-2008 only (pre-2008 미build) |
| `sub_period_split_2008_1992baseline.csv` | 145 B | ✅ post-2008 1992 |
| `pre_wto_placebo_1992_1996.csv` | 253 B | ✅ pre-WTO placebo |
| `quality_improvement_suite.csv` | 278 B | ✅ Drop-C26, Drop-top-3, AKM v4 canonical |
| `akm_proper_2019.csv` | 313 B | ✅ AKM proper 2019 |
| `akm_bhj2022_ssaggregate.csv` | 317 B | ✅ ssaggregate WLS (별도 estimand) |

---

## 6. 5_logs (decision logs + integrity checks)

**5_logs/decisions/** (10 logs since 2026-05-05):
- `2026-05-06_track2_track3_v4_5_4_commit.md` — Track 2 ✅ + Track 3 P1 fix
- `2026-05-06_phase4_1992baseline_sensitivity.md` — 1992 baseline regression
- `2026-05-06_validation_report_audit_complete.md` — Round 26 audit
- `2026-05-05_phase4_final_publishable.md` — Phase 4 main spec
- `2026-05-05_phase_bx_final_branch_decision.md` — A.ii branch commit
- `2026-05-05_phase4_final_inference.md` — 5-layer SE + tF + Romano-Wolf
- `2026-05-05_pre_wto_placebo.md` — placebo result
- `2026-05-05_quality_improvement_suite.md` — Drop-C26 + outlier
- `2026-05-05_p1_clear_for_phase4.md` — P1 clear
- `2026-05-05_phase4_fixes.md` — WCB convergence patch
- `2026-05-05_pap_v41_commit.md` — PAP v4.1 commit

**5_logs/integrity_checks/** (10 logs since 2026-05-05):
- `2026-05-06_baseline_shares_1992_v2.md` — Track 3 v2 audit
- `2026-05-06_z_m_education_sensitivity.md` — Track 2 audit
- `2026-05-05_z_x_h_1992_phase2b.md` — Phase 2-B z_x_h^1992 build
- `2026-05-05_v02_wa_verification.md` — mortality WA panel verify
- `2026-05-05_v02_wa_verification_R-A.md` — R-A audit
- `2026-05-05_population_join_fix.md` — population join fix
- `2026-05-05_phase_bx_test3_results.md` — Test 3 (Pierce-Schott pre-trend)
- `2026-05-05_phase_bx_test3_dryrun.md` — Test 3 dry-run

---

## 7. 7_paper (paper draft v01)

| File | Size | Status |
|------|------|--------|
| `paper_draft_v01_section_1_2.md` | 18.8 KB | ✅ Intro + Background |
| `paper_draft_v01_section_3_4.md` | 25.5 KB | ✅ Data + Identification (Sample Universe Master Table commit) |
| `paper_draft_v01_section_5.md` | 11.1 KB | ✅ Main Results (Round 26 P1·P2 fix) |
| `paper_draft_v01_section_6.md` | 14.1 KB | ✅ Robustness (Round 26 over-claim fix) |
| `paper_draft_v01_section_8_9.md` | 14.7 KB | ✅ Discussion + Conclusion |
| `paper_draft_v01_references.md` | 9.8 KB | ✅ 47 references (39 academic + 8 institutional) |
| § 7 Mechanism | DEFERRED | HIRA fetch ~5-6일 후 작성 |
| Online Appendix | next | 15-20p |

**Total paper draft**: ~94 KB (~26 pages KER format)

---

## 8. PAP versions (4_documentation/PAP/)

| Version | Size | Status |
|---------|------|--------|
| `PAP_v4.4_main_body.md` | 21.6 KB | superseded |
| `PAP_v4.5_main_body.md` | 37.8 KB | ✅ current main |
| `PAP_v4.5.1_patch.md` | 20.1 KB | ✅ Round 21·22·23 audit (11 framing 정정) |
| `PAP_v4.5.2_patch.md` | 7.0 KB | ✅ Track 1 verified citation |
| `PAP_v4.5.3_patch.md` | 9.3 KB | ✅ DGHP A-2 + Track 2/3 코드 commit |
| `PAP_v4.5.4_patch.md` | 8.6 KB | ✅ Track 2 정합 + Track 3 v2 + KSIC 6→9 footnote retract |

→ PAP v4.6 commit pending (WCB stale narrative + Sample Universe Master Table sync + Round 26 fix 통합).

---

## 9. 변경 사항 (v03 → v04, 2026-05-05 → 2026-05-06)

**추가된 데이터:**
- ✅ `baseline_shares_1992_ksic9_2digit_v2.parquet` (Track 3 v2)
- ✅ `baseline_shares_1992_ksic9_2digit_v2_renamed.parquet` (regression input)
- ✅ `denominator_E_h_1992_v2.parquet`
- ✅ `iv_z_x_adh8_1992baseline.parquet` + `iv_z_x_bilateral_1992baseline.parquet` (Phase 2-B)
- ✅ `z_m_education_baseline_sensitivity.parquet` (Track 2)
- ✅ `main_spec_5layer_se_1992baseline.csv` + `romano_wolf_pvalues_1992baseline.csv` + `sub_period_split_2008_1992baseline.csv`

**진행 상황:**
- HIRA drug fetch: 9.5K / 55K calls (17.3%)
- Paper draft: 9/10 sections committed (§ 7 Mechanism deferred)
- Round 26 audit: 7/16 fix applied (A1·A3·B1·B3·B4·C1·C2). A2 RW common-sample re-run pending. V1-V8 web verification pending.

**Pending data builds (next 6 days):**
- HIRA drug full panel completion (~5-6일)
- 1993·1995·1996 baseline shares (Track 4, R-A 다음 turn 작성 가능)
- Pre-2008 sub-period regression (sample restriction 처리 후)
- 1992 baseline outlier-trimmed sensitivity
- WCB alternative implementation (`fwildclusterboot`, `boottest`)

---

## 10. Outstanding Issues (priority)

**P1 (publication-blocking):**
- Romano-Wolf common-sample re-run (n=198 vs 222 inconsistency, A2)
- WCB convergence — alternative implementation 시도

**P2 (paper polish):**
- V1-V8 citation web verification (8 항목)
- Pre-2008 sub-period build
- 1993·1995·1996 baseline sensitivity

**P3 (HIRA dependent):**
- § 7 Mechanism (HIRA fetch 완료 후 ~5-6일)
- DGHP 2017 ivmediate framework 적용
