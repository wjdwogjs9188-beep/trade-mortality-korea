# Phase B-x diagnostics — Handoff (2026-05-04)

## 작성된 스크립트

| # | Test | File | 데이터 의존성 | 즉시 실행 |
|---|------|------|---------------|-----------|
| 22 | Test 1 — Romer-Romer macro predictability | `2_scripts/identification/22_phase_bx_test1_macro_predictability.py` | `0_raw/ecos_macro/*.parquet` (Phase 1-C ✅) + `0_raw/comtrade_korea_china/*.csv` (50/50 ✅) | ✅ |
| 23 | Test 1b — WEO forecast surprise | `2_scripts/identification/23_phase_bx_test1b_weo_surprise.py` | `0_raw/imf_weo_korea_vintage/WEOhistorical.xlsx` (Phase 0 ✅) + KR-CN bilateral | ✅ |
| 24 | Test 3 — Pierce-Schott pre-trend | `2_scripts/identification/24_phase_bx_test3_pierce_schott_pretrend.py` | Phase 2-A mortality panel + Phase 2-B baseline shares 1990 + exposure 2000-2010 | ⏸ Phase 2 후 |
| 25 | First-stage F (z_x ADH-8 vs bilateral) | `2_scripts/identification/25_phase_bx_first_stage_f.py` | Phase 2-B 출력 + centroid (✅) | ⏸ Phase 2 후 |

## 실행 방법

```powershell
cd C:\Users\82103\Downloads\trade_mortality_korea
powershell -ExecutionPolicy Bypass -File 2_scripts\identification\run_phase_bx_all.ps1
```

Test 24·25 는 dry-run mode 로 끝남 (Phase 2-B 출력이 없으면 missing 표시 + skip).

## 데이터 inventory check (2026-05-04 업로드 기준)

| 항목 | 상태 | 비고 |
|------|------|------|
| 시군구 centroid | ✅ 251/251 | `0_raw/sigungu_centroid/sigungu_centroid_table.csv` — Conley SE 준비 완료 |
| WEO Historical | ✅ 8.98 MB | Test 1b 입력 |
| ECOS keyword search | ✅ 834 stat | 정확한 코드 확정: 200Y110/402Y014/401Y015/901Y009/731Y004/722Y001 |
| ECOS Test 1 macro fetch (v03) | ❌ 실패 | v03 은 잘못된 코드 (200Y007/200Y011/200Y001/401Y014) 사용. **무시 가능** — script 22 는 Phase 1-C 완료한 `0_raw/ecos_macro/` 기존 파일을 읽음 |
| KR-CN bilateral 50/50 | ✅ | 2000-2024 25년 |

## 다음 우선순위 (사용자 측 실행)

1. **`run_phase_bx_all.ps1` 실행** → Test 1 + 1b 실제 결과 산출
2. 결과 log (`5_logs/integrity_checks/2026-05-04_phase_bx_test1*.md`) 확인 후 R-A 에 공유
3. p-value 결과에 따라:
   - Test 1, 1b 모두 p > 0.10 → A.i / A.ii branch 살아있음
   - Test 1 또는 1b p < 0.05 → C.ii branch (macro-driven 의심) 검토 필요

## Phase 2-B (1990 baseline Bartik) 다음 dedicated turn 필수

Test 3·25 는 1990 산업 baseline shares 가 필요. 현재 광업제조업조사 1994
microdata KSIC 4-digit extraction 미수행 — 별도 세션 (~3h 작업) 필요.

## 미완 — 별도 turn

- PAP v3.4 main body → v4.0 patches 통합 rewrite (~3h)
- Phase 2-A mortality panel build (despair_total/cancer/cardio/respiratory/external_other 5개 outcome group × 251 시군구 × 27년)
- Phase 2-B Bartik 1990 baseline + exposure 2000-2010
- Phase B-m Tests 4·5·6 (z_m 외생성: 인구이동·결혼시장·교육접근)
- Phase B-SI ρ-sensitivity ±0.5 구현 (ivmediate Stata)
