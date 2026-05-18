# 정합성 검증 보고서

**시각:** 2026-05-01 07:43:36

## 종합

- ✅ 통과: **50**
- 🟡 경고: **0**
- 🔴 critical: **0**
- 합계: 50

## 결론

🟢 **모든 검증 통과 — 본 연구 데이터 무결성 보장됨**

## ✅ 통과 (50)

- 폴더: 0_raw
- 폴더: 0_raw/mortality_kostat
- 폴더: 0_raw/industry_census
- 폴더: 0_raw/kosis_population
- 폴더: 0_raw/ecos_macro
- 폴더: 0_raw/ecos_delinquency
- 폴더: 0_raw/comtrade_adh_china
- 폴더: 0_raw/comtrade_korea_china
- 폴더: 0_raw/comtrade_china_world
- 폴더: 0_raw/ssaggregate-main
- 폴더: 0_raw/research_supp
- 폴더: 0_raw/research_materials
- 폴더: 1_codebooks
- 폴더: 2_scripts
- 폴더: 2_scripts/lib
- 폴더: 2_scripts/data_collection
- 폴더: 2_scripts/sigungu_crosswalk
- 폴더: 3_derived
- 폴더: 5_logs/decisions
- 폴더: .git
- 파일: CLAUDE.md
- 파일: .env
- 파일: .gitignore
- 파일: requirements.txt
- 파일: 1_codebooks/sigungu_crosswalk.csv
- 파일: 1_codebooks/sigungu_changes_history.md
- 파일: 1_codebooks/kosis_104_to_icd10.yaml
- 파일: 1_codebooks/mortality_104_classification.csv
- 파일: 0_raw/kosis_population/population_combined.csv
- 파일: 3_derived/raw_inventory.csv
- 사망 microdata 파일: 27 (기대 27)
- 산업 microdata: 31 (기대 31)
- ECOS macro: 11 (기대 11)
- ECOS delinquency: 5 (기대 5)
- Comtrade KR-CN: 51 (기대 51 = 50 data + 1 log)
- Comtrade ADH 8국: 169 (기대 168, 35개 추가 예정)
- crosswalk rows: 6,723
- h_code 수: 256
- (year,raw)→h_code 1:1: 다중 매핑 0건
- 사망 ↔ crosswalk 매칭: 6723/6723 (누락 0)
- 인구 panel rows: 516,750
- 인구 시군구: 286
- 1993 전국 인구: 44,752,156
- Comtrade truncated: 0개 (0이어야 정상)
- CLAUDE.md ECOS 16개 일관: ECOS16: True, ECOS13(stale): False
- CLAUDE.md 사망 27년 일관: 27년: True, 28년(stale): False
- Phase 1 헤더: 1-A/C/D/E 완료 표시
- .env gitignored: .env 라인 존재
- git history API 키 노출: 0개 노출
- git commit 수: 1개
