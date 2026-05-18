# 2026-05-01 — Sigungu h_code 정의 결정 ## 배경 본 연구 (Trade × Mortality Korea) 는 1997-2023 KOSTAT 사망 microdata 를 sigungu(시군구) 레벨로 패널화. 27년 사이 한국 시군구 행정구역은: - 9개 도농통합/광역시 승격 (2003-2014)
- 1개 광역자치단체 신설 (세종 2012.7.1)
- 1개 시군 cross-sido 편입 (군위군 경북→대구 2023.7.1)
- 6건 일반구 분구·폐지 (1995-2016)
- 5건 명칭 변경 (남구→미추홀구 2018, 강원도→강원특별자치도 2023 등) 다년간 panel 회귀를 위해 **stable identifier (h_code)** 가 필요. ## 결정 ### 1. h_code = 2021 KOSTAT baseline (262 entries) 기준 - 2021년 KOSTAT 시군구 codebook (sigungu 5-digit code) 을 reference set.
- 모든 raw_code 는 2021 시점의 successor entity 의 코드로 매핑.
- 사유: 2018+ 코드가 2010+ 통합 결과를 모두 반영한 안정 상태 (4년 연속 262 entries 동일). ### 2. 사전 2021 raw_code 매핑 (29건) `step3_build_h_code.py::PRE2021_REMAP` 참조. 주요: | 이벤트 | 합병/승격일 | raw_code 변경 |
|--------|-------------|---------------|
| 통합창원시 출범 | 2010.7.1 | 38010+38020+38040 → 38110 |
| 통합청주시 출범 | 2014.7.1 | 33010+33310 → 33040 |
| 통합여수시 출범 | 1998.4.1 | 36050+36340 → 36020 |
| 제주특별자치도 출범 | 2006.7.1 | 39310→39010, 39320→39020 |
| 부천시 일반구 폐지 | 2016.7.4 | 31051/31052/31053 → 31050 |
| 세종특별자치시 출범 | 2012.7.1 | 34320 (연기군) → 29010 |
| 도농통합 시 승격 | 1998-2013 | 31330→31240 (화성), 31320→31280 (여주) 등 8건 | ### 3. 2022 = 2021 forward-fill 2022 KOSTAT codebook 미보유. step3a 검증 결과 2022 raw_code 100% = 2021 raw_code → 그대로 사용. ### 4. 2023 — KOSTAT 별도 codebook + 5개 special case - **소스**: `0_raw/mortality_kostat/usrcnfrm/파일설계서(공공용)_사망원인통계_사망연간자료B형(제공)_2023(코드집포함).xlsx`, sheet `코드정보`, 항목명 `사망자주소행정구역시군구코드` (261 entries).
- **bulk match**: within-sido sigungu 명칭 join → 256 entries 매칭 (군 코드는 2023 부터 +200 일괄 renumber, 예: 38400→38600 합천군).
- **5 special cases** (`step3_build_h_code.py::REMAP_2023`): 1. 군위군 22520 (대구) → h_code 37310 유지 (panel stable), sido_code 만 22. 2. 미추홀구 23090 — 2021 codebook 의 `'미추홀구(남구)'` vs 2023 codebook 의 `'미추홀구'` (괄호 정규화). 3. 세종특별자치시 29010 — 2021 `'세종시'` vs 2023 `'세종특별자치시'`. 4. 통합청주시 33040 — 2021 codebook 부모 코드 (실데이터엔 33041-33044 sub-구만 존재). 5. 통합창원시 38110 — 동일 (실데이터엔 38111-38115 sub-구만 존재).
- **2023 sido name override**: 32 강원도 → 강원특별자치도 (2023.6.11). ### 5. 폐기된 대안 - **자동 ordered pairing** (군 코드 sorted-by-rank join): 군 +200 renumber 단순 케이스엔 동작하나 군위 cross-sido / 명칭 변경 case 에서 잘못 매핑. 명시적 KOSTAT codebook 우선 (현재 결정).
- **2014년 통합 기준** (CLAUDE.md 초기 권장 228 시군구): 2018+ baseline (262 entries) 이 후속 이벤트 (남구→미추홀구 2018) 반영. 2021 채택. ## 검증 결과 (`step4_validation_report.md`) | 검증 | 결과 |
|------|------|
| (a) 연도별 매칭률 | ✅ 27년 모두 100% (6,723/6,723 rows) |
| (b) 사망자 합계 보존 | ✅ 27년 모두 delta=0 (raw → h_code 합 무손실) |
| (c) 시도 coverage | ✅ 1997-2023 17 시도 (panel-consistent retroactive 세종 매핑 포함) |
| (d) h_code 카운트 | ✅ 모든 연도 ≤ 262 (1997: 241, 2021+: 250-256) |
| (e) 군위 transfer | ✅ pre-2023: sido=37 경북, 2023: sido=22 대구, h_code=37310 유지 | ### 군위 transfer spot check (raw 사망 합계) | year | 대구(22) | 경북(37) | 군위(22520) raw |
|------|---------:|---------:|----------------:|
| 2022 | 17,592 | 27,840 | — |
| 2023 | 12,239 | 18,784 | 335 | (대구 합엔 군위 335 포함, 경북 합엔 군위 제외 — 정상) ## 산출물 - `1_codebooks/sigungu_crosswalk.csv` — final mapping (year × raw_code → h_code/h_name/sido_code/sido_name/event_note), 6,723 rows
- `1_codebooks/sigungu_changes_history.md` — 358 event rows, 행정 변경 이력 표
- `3_derived/sigungu/step3c_codebook_2023.csv` — 261 rows (2023 KOSTAT 추출)
- `3_derived/sigungu/step3_h_code_mapping.csv` — 동일 내용 derived 사본
- `3_derived/sigungu/step3_unmatched.csv` — 0 rows (전부 매칭됨)
- `3_derived/sigungu/step4_validation_report.md` — 5/5 통과
- `2_scripts/sigungu_crosswalk/step3c_extract_2023_codebook.py`
- `2_scripts/sigungu_crosswalk/step3_build_h_code.py`
- `2_scripts/sigungu_crosswalk/step4_validate.py`
- `2_scripts/sigungu_crosswalk/step5_finalize.py` ## 한계 및 후속 과제 1. **연기군→세종 retroactive 매핑**: 1997-2011 연기군 사망 → h_sido=29 (세종). Panel consistent 하나 "1997년 세종" 이라는 비역사적 표기 발생. 시도 시계열 분석 시 주석 필요.
2. **통합청주시(33040)/통합창원시(38110) 부모코드**: 2023 codebook 에 등재되었으나 실데이터엔 sub-구 코드만 사용. crosswalk 에 매핑 행은 있으나 raw 데이터 join 시 NULL.
3. **2024년 데이터 미수집**: 2024.1.18 전라북도 → 전북특별자치도 변경 반영 필요 시 본 crosswalk 확장.
4. **인구 합 정합성 cross-check 미수행**: KOSIS 시군구 인구 데이터 (별도 다운 필요) 와 합산해서 raw → h_code aggregation 시 인구 보존 여부 점검은 후속 단계 (mortality rate 계산 시 동시 수행). --- *Author: (Opus 4.7) + 정재헌*
*Date: 2026-05-01*
