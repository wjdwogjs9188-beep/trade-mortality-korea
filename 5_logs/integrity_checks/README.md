# integrity_checks/ — build 진단·검증 archive _총 36 file. phase 별 grouping. build script 의 시행착오 lessons 가 여기 archive_ 본 폴더는 build pipeline 의 schema probe, validation, sensitivity test 결과 archive. v01→v02→v03 시행착오 lessons (mortality mojibake 우회, baseline col 14 식별, KIET60 매개 매핑 등) 가 file 안에 포함. --- ## Phase 별 grouping (37 file) ### Phase 0 — initial integrity (1 file) | file | 내용 |
|------|------|
| `2026-05-01_0743_integrity_check.md` | Phase 0 initial 5 zip 추출 + 폴더 구조 정합 check | ### Phase B-x — identification diagnostic (8 file) | file | 내용 |
|------|------|
| `2026-05-04_phase_bx_preflight.md` | Phase B-x 진단 preflight |
| `2026-05-04_phase_bx_test1_results.md` | Test 1 saturated Romer-Romer |
| `2026-05-04_phase_bx_test1_v2_results.md` | Test 1 v2 univariate Bonferroni HAC VIF |
| `2026-05-04_phase_bx_test1_v3_results.md` | Test 1 v3 수입가 drop |
| `2026-05-04_phase_bx_test1b_results.md` | Test 1b WEO forecast surprise |
| `2026-05-04_phase_bx_test3_dryrun.md` | Test 3 Pierce-Schott pre-trend dry-run |
| `2026-05-04_phase_bx_first_stage_f_dryrun.md` | first-stage F dry-run |
| `2026-05-05_phase_bx_first_stage_f.md` | first-stage F final ADH-8 vs bilateral |
| `2026-05-05_phase_bx_test3_dryrun.md` | Test 3 dry-run 재실행 |
| `2026-05-05_phase_bx_test3_results.md` | Test 3 final | ### Phase 2-A — mortality panel build (5 file) | file | 내용 |
|------|------|
| `2026-05-05_kostat_mortality_schema_probe.md` | KOSTAT 사망 microdata schema probe (cp949 mojibake 식별) |
| `2026-05-05_mortality_panel_v02_wa_validation.md` | mortality panel v02 working-age build (v1) |
| `2026-05-05_mortality_panel_v02_wa_validation_v2.md` | v2 (positional column 우회 시도) |
| `2026-05-05_mortality_panel_v02_wa_validation_v3.md` | ⭐ v3 positional column 최종 (256 h_code, 31,494 rows, 1997-2022) |
| `2026-05-05_population_join_fix.md` | KOSIS 인구 panel join fix (C1 raw_code + C3_NM age band) |
| `2026-05-05_v02_wa_verification.md` | v02 wa verification |
| `2026-05-05_v02_wa_verification_R-A.md` | 측 verification | ### Phase 2-B — Bartik IV build (8 file) | file | 내용 |
|------|------|
| `2026-05-05_business_survey_1994_schema.md` | 광업제조업조사 1994 schema probe (col 식별) |
| `2026-05-05_business_survey_1994_schema_v2.md` | v2 (col 14 = 종사자 확정) |
| `2026-05-05_baseline_shares_1994_validation.md` | ⭐ 1994 baseline shares 검증 (226 h_code, 9,739 cells, 95.2% match) |
| `2026-05-05_business_survey_2000_2010_schema.md` | 2000-2010 광업제조업조사 schema |
| `2026-05-05_employment_change_2000_2010.md` | 2000-2010 employment change build |
| `2026-05-05_employment_change_2000_2010_v2.md` | v2 |
| `2026-05-05_kiet60_mapping_inspect.md` | KIET 60-sector 매개 HS6→KSIC 매핑 inspect |
| `2026-05-05_kiet60_mapping_v2.md` | v2 매핑 |
| `2026-05-05_bartik_iv_build.md` | Bartik IV (z_x_h) 최종 build | ### Phase 2-B (1992 sensitivity) — 1992 baseline (4 file) | file | 내용 |
|------|------|
| `2026-05-05_baseline_shares_1992.md` | 1992 baseline 1차 build |
| `2026-05-05_z_x_h_1992_phase2b.md` | z_x_h 1992 vintage |
| `2026-05-06_baseline_shares_1992.md` | 1992 v1 (col 11 자영업주만 사용 bug) |
| `2026-05-06_baseline_shares_1992_v2.md` | ⭐ 1992 v2 (col 30 종사자수합계 fix, 215 h_code, 3,237 cells, 85.3% match) | ### Phase 3 — first reduced form (1 file) | file | 내용 |
|------|------|
| `2026-05-05_first_reduced_form.md` | ⭐ 첫 reduced form 5 outcome × 5-layer SE preliminary. n=222/222/222/198/222, β=-0.0685 (despair) main result | ### Phase 5 — mediator z_m (3 file) | file | 내용 |
|------|------|
| `2026-05-05_nhis_schema_probe.md` | NHIS schema probe (HIRA mediator 후보) |
| `2026-05-05_z_m_education_sensitivity.md` | z_m education distance sensitivity |
| `2026-05-06_z_m_education_sensitivity.md` | v2 sensitivity | ### Phase A.1 — sample attrition audit (1 file, 진행 중) | file | 내용 |
|------|------|
| `sample_attrition_audit_template_v01.md` | ⭐ 9-단계 cascade audit template (작성 2026-05-06). Step 1·3·7 verified, Step 2·5·6·8·9·10 사용자 build log 필요 | ### Phase cleanup — Path A unification audit cycle (1 file, 2026-05-06 신규) | file | 내용 |
|------|------|
| `2026-05-06_path_a_3stage_audit_cycle.md` | ⭐ 3-stage audit cycle (/data:explore-data → /data:analyze → /data:validate-data) 결과 archive. Stage 1 49% → Stage 2 16.3% → Stage 3 hard data inconsistency 식별 progression. cleanup_prompt v01 → v02 update trigger. Layer A (narrative reverse) + Layer B (Table numerical re-population) 두 layer 분리 | --- ## ⭐ 핵심 mark file (reset 또는 audit 시 우선 read) 1. `2026-05-05_mortality_panel_v02_wa_validation_v3.md` — mortality panel v3 (256 h_code 최종)
2. `2026-05-05_baseline_shares_1994_validation.md` — 1994 baseline (226 h_code)
3. `2026-05-06_baseline_shares_1992_v2.md` — 1992 baseline (215 h_code)
4. `2026-05-05_first_reduced_form.md` — n=222/198 sample cascade ground truth
5. `sample_attrition_audit_template_v01.md` — 9-단계 cascade audit 진행 중 --- ## v01→v02→v03 시행착오 lessons (reset 시 다시 발견 필요한 함정) | 시행착오 | file path | 함정 |
|---------|----------|------|
| mortality cp949 mojibake | `2026-05-05_kostat_mortality_schema_probe.md` | header 한글 깨짐 → positional column loading 우회 발견 |
| 1994 baseline col 식별 | `2026-05-05_business_survey_1994_schema.md` v2 | col 14 (종사자) vs col 11 (자영업주) 식별. anchor 1995 통계연감 290만 ≈ col 14 합 256만 |
| KSIC 6→9 crosswalk file 부재 오인 | `2026-05-06_baseline_shares_1992_v2.md` | 1_codebooks/ksic6_to_ksic9_2digit.csv 100% match |
| KIET60 매개 매핑 | `2026-05-05_kiet60_mapping_inspect.md` v2 | HS6→KSIC9_2 직접 매핑 부재 → KIET 60-sector 매개 |
| 1992 col 30 vs col 14 | `2026-05-06_baseline_shares_1992_v2.md` | 1992 schema 는 col 30 = 종사자수합계 (1994 schema 와 다름) | reset 시 위 시행착오 4-5건이 반복 risk.
