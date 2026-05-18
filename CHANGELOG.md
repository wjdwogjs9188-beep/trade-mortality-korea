# Changelog

이 프로젝트의 모든 주요 변경사항을 기록합니다. 날짜는 ISO 8601 (YYYY-MM-DD) 형식.

---

## [Unreleased]

## [Phase 1-A: sigungu crosswalk] — 2026-05-01

### Added
- `1_codebooks/sigungu_crosswalk.csv` — 1997-2023 27년치 (year × raw_code → h_code) 통합 매핑, 6,723 rows, 100% 매칭
- `1_codebooks/sigungu_changes_history.md` — 행정 변경 이벤트 111건 표
- `3_derived/sigungu/step3c_codebook_2023.csv` — KOSTAT 2023 파일설계서에서 261개 시군구 추출
- `3_derived/sigungu/step3_h_code_mapping.csv` + `step3_unmatched.csv` (0건)
- `3_derived/sigungu/step4_validation_report.md` — 5/5 검증 통과
- `2_scripts/sigungu_crosswalk/step3c_extract_2023_codebook.py`
- `2_scripts/sigungu_crosswalk/step3_build_h_code.py`
- `2_scripts/sigungu_crosswalk/step4_validate.py`
- `2_scripts/sigungu_crosswalk/step5_finalize.py`
- `5_logs/decisions/2026-05-01_sigungu_h_code_definition.md` — h_code 정책 + 검증 결과

### Decisions
- h_code = 2021 KOSTAT baseline (262 entries) 채택 (2014 통합 기준에서 수정)
- 2023 cross-sido 군위군 (경북→대구): h_code 37310 유지, sido_code 만 22로 변경
- 2023 raw_code +200 군 일괄 renumber: within-sido 명칭 매칭으로 흡수 (256건)
- 5개 special case (군위, 미추홀구, 세종, 통합청주시, 통합창원시): 명시적 REMAP_2023
- pre-2021 합병/승격/개칭 29건 PRE2021_REMAP (창원/청주/세종/제주/여수/김포/안성/화성/광주/포천/양주/여주/당진/계룡 등)
- 폐기: 자동 ordered pairing → KOSTAT 공식 codebook 우선

### Validation
- 매칭률: 27년 모두 100% (6,723/6,723)
- 사망자 합 보존: 27년 모두 delta=0
- 시도 coverage: 17 시도 (panel-consistent)
- 군위 transfer: pre=경북 / 2023=대구 검증

## [Phase 0] — 2026-05-01

### Added
- 프로젝트 폴더 구조 (`trade_mortality_korea/`)
- 메타 문서: README.md, METHODOLOGY.md, CHANGELOG.md, DATA_SOURCES.md
- requirements.txt, Makefile,.gitignore
- 5개 zip 파일 → `0_raw/` 압축 해제
 - 지역별 자살 데이터 (사망 microdata 28년 + 시군구코드집 24개 + ICD 코드집)
 - 산업 비중 데이터 (사업체조사 31년 + 조사·파일설계서 53개)
 - 연구 자료 (Census 2% + 27 paper + 복지 + 미국 무역 + crosswalk)
 - 연구용 (KSIC 연계표 + KOSIS 시군구 + HIRA 분기별 + 추가 raw)
 - ssaggregate-main (BHJ R 패키지)
- INVENTORY.csv 자동 생성 (모든 raw 파일의 md5/행수/컬럼/인코딩)
- git 초기화 + 첫 commit

### Decisions
- ICD-10 raw 직접 추출 (KOSIS 104항목 코드 신뢰 X) — 이전 v3.x mislabel 문제 대응
- Korea-China bilateral IV 우선 사용 (ADH 8-country weak in Korea)
- 5-layer SE 동시 보고 정책

---

## [Pre-reset history] (참고)

### v3.8 (2026-04-30)
- "Hidden Protective Effect" narrative
- bartik_v2 reduced form β=−0.041
- 변수 mislabel 의심 → reset 결정

### v3.0-v3.9 (2026-03 ~ 2026-04)
- 9 Bartik spec 비교 + bartik_v2 선정
- AKM SE, Rotemberg, Conley 추가
- China-World alternative IV
- Self-employment control 추가

### v1.0-v2.0 (2026-02 ~ 2026-03)
- 초기 시군구 panel 구축
- ADH 8-country IV → weak 발견
- Korea-China bilateral 도입

## 2026-05-04 (v4.1) — 데이터 보강 + 폴더 정리

### 데이터 추가
- BACI HS92 1995-2011 (17 csv, 3.9 GB) → `4_trade/raw/baci/`
- WITS HS6→ISIC Rev3 4-digit + Rev2 (5,703 codes) → `0_raw/hs_isic4_concordance/WITS_*.csv`
- KIET 60-industry HS-KSIC (P1.6 우회 후보, granularity 부족 — robustness 만)
- **researchall HS6↔KSIC10 매핑 (6,351 rows, 415 manuf KSIC) — P1.6 SOLVED ⭐** → `0_raw/hs_ksic_concordance/researchall_HS6_to_KSIC_link.csv`
- KSIC chain (8→9→10→11) 통합 lookup (1,361 rows) → `3_derived/sigungu/ksic_chain_lookup.csv`
- IMF WEO Historical (1990-2022 vintage) → `0_raw/imf_weo_korea_vintage/WEOhistorical.xlsx`
- 시군구 centroid (KOSTAT 2018, 251 rows) → `0_raw/sigungu_centroid/`
- ECOS 200Y110 (분기 GDP 실질, 2,100 rows) + 402Y014 (수출물가 총지수) + 401Y015 (수입물가 총지수) — Test 1 macro variable
- KOSIS 보건의료 4 시리즈 (보건기관 이용률 + 인플루엔자 접종률 + 일반건강검진 정상B/질환의심) → `0_raw/kosis_medical_infra/`
- **MDIS 인구주택총조사 1975/1980/1985/1990/1995 (5 census, 220 MB, 3.8M rows) — z_m_marital instrument 핵심 데이터** ⭐⭐ → `0_raw/mdis_population_census/2pct_1975_1995/`

### Protocol commit
- **PAP v4.0 unified identification protocol** (z_x + z_m + Sequential Ignorability + Joint decision tree) ⭐
- v3.5 (z_x only) + v3.6 z_m draft → archive

### 폴더 정리 (root → sub-folder)
- REVIEWER 5 문서 → `4_documentation/reviewer/`
- RESEARCH_PROGRESS 2 + next_prompt → `4_documentation/status_reports/`
- 실행 스크립트 6 (.bat,.ps1) → `2_scripts/run/`
- PAP 7 archive 버전 → `4_documentation/PAP/archive/`
- inventory csv → `4_documentation/pipeline_docs/`
- root: 9 파일만 유지 (메타 entry)
