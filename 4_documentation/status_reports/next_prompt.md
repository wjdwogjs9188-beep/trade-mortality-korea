# Phase 2-A 사망률 panel build — Claude Code 작업 prompt

## 입력
- 0_raw/mortality_kostat/사망사료 정리/*.csv (27년, cp949 인코딩, 1997-2023)
- 1_codebooks/sigungu_crosswalk.csv (year × raw_code → h_code, 6,723 rows)
- 0_raw/kosis_population/population_combined.csv (시군구 × year × C2 sex × C3 age → 인구, 516,750 rows)
- 1_codebooks/kosis_104_to_icd10.yaml (outcome groups)

## 처리 단계

### Step 2A-1: 사망 raw 적재
- 27개 csv 파일 모두 read (cp949 → utf-8)
- 컬럼: 사망자주소행정구역시도코드, 사망자주소행정구역시군구코드, 사망원인_104항목분류코드, 성별, 연령 등
- 1997-2022: raw_code = sido(2) + sgg(3) zfill → 5자리
- 2023: sgg 자체가 5자리

### Step 2A-2: crosswalk join → h_code
- (year, raw_code) → h_code, h_name, sido_code, sido_name 추가
- 매칭률 27년 모두 100% (이미 검증됨)

### Step 2A-3: outcome 매핑
1_codebooks/kosis_104_to_icd10.yaml 참고:
- despair_total: 코드 102 + 101 + 057 + 081
- cardiovascular: 067-070
- cancer: 027-048
- respiratory: 073-078
- external_other: 097-104 minus 102

각 사망 record 에 outcome group 컬럼 추가 (multiple group 가능, dummy 변수 형태).

### Step 2A-4: 사망 카운트
h_code × year × outcome × age_5yr × sex 단위로 group_by + count

### Step 2A-5: 인구 panel join
- KOSIS 인구 panel 의 시군구 (C1 5자리)
- 9개 시 합계 코드 (수원시, 성남시 등) 제외
- (h_code, year, age_5yr, sex) 키로 join

연령 매핑:
- 사망 raw: 1세 단위
- KOSIS 인구: 5세 단위
- → 사망 raw 의 age 를 5세 bin 으로 묶어서 join

### Step 2A-6: 사망률 계산
mortality_rate = (사망 / 인구) × 100,000

### Step 2A-7: 산출
- 3_derived/mortality_panel.parquet
- 3_derived/mortality_panel.csv (큰 파일이면 옵션)
- schema:
  h_code, year, outcome_group, age_5yr, sex, deaths, population, mortality_rate

## 검증

### 검증 1: 사망자 합 보존
raw count 총합 == panel sum of deaths (delta=0 확인)

### 검증 2: KOSTAT 102 자살 cross-check (이미 known)
- 2010: 15566
- 2011: 15906
- 2015: 13513
- 2019: 13799

panel sum 으로 동일하게 나오는지

### 검증 3: 한국 자살률 시계열 plot
- 1997-2023 전국 자살률 (per 100k)
- 1997 IMF 위기 후 급등 → 2003 정점 → 2010s 감소 패턴 확인

### 검증 4: 시군구별 자살률 분포 sanity
- 광역시 vs 도 차이
- 노인 인구 비율 높은 곳 자살률 높은가

## 산출 보고서

3_derived/mortality_panel_validation.md 에:
- 검증 4가지 결과
- 시계열 plot
- KOSTAT cross-check 표
- 사용자 spot-check 안내

## reference

- 5_logs/methodology_notes/case_deaton_2015_notes.md (deaths of despair 정의)
- 5_logs/methodology_notes/finkelstein_nafta_2026_notes.md (β_m vs β_n framework)
- 1_codebooks/kosis_104_to_icd10.yaml (outcome 코드)

## 진행

먼저 1년치 (2010) 만 처리해서 결과 보여주기.
사용자 검토 후 OK 면 27년 전체 진행.

## 주의

- raw 데이터 절대 수정 X (read-only)
- 한글 인코딩 주의 (cp949 → utf-8 변환)
- 9개 시 합계 코드 (수원시, 성남시, 안양시, 고양시, 청주시(33010, 33040), 전주시, 포항시, 통합창원시) 제외
- pre-2012 세종 (29) sido 매핑은 연기군 retroactive (Phase 1-A 결정)
