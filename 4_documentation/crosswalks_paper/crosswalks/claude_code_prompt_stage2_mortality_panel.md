# Claude Code Prompt — Stage 2 사망 Panel Build (v3)

## 작업 목적

KOSTAT 27개 cp949 사망 microdata CSV (1997-2023) 를 결합하고, sigungu_crosswalk_v2 의 229 baseline h_code 로 매핑하고, mortality_104_classification 의 5 outcome group 으로 분류한 후, 시군구 × 연도 × 성 × 5세 연령 × outcome panel 을 산출한다. 본 paper 의 종속변수 base panel 이 된다.

본 단계는 **deaths count 산출까지**. 사망률 (per 100,000) + 연령 표준화 + 로그 변환은 Stage 3 (인구 panel) 결합 후 별도 단계에서 처리.

## 입력 파일

1. **`0_raw/mortality_kostat/사망사료 정리/`** — 27개 CSV (1997-2023)
   - 인코딩 cp949, 1행 = 1 사망 record (microdata)
   - 18개 컬럼: 사망연도, 신고연도/월/일, 사망자주소행정구역시도코드 (2자리), 사망자주소행정구역시군구코드 (3자리), 사망연월일, 사망시, 사망장소코드, 사망자직업분류코드, 사망자혼인상태코드, 교육정도코드, 성별코드, 사망연령5세단위코드, 사망자국적구분코드, 사망자이전국적코드, 사망원인_104항목분류코드, 사망원인_57항목분류코드
   - 시기에 따라 컬럼명 미세 차이 가능 (KOSTAT 파일설계서 참고)

2. **`1_codebooks/sigungu_crosswalk_v2.csv`** — 229 baseline h_code 매핑
   - 컬럼: year, raw_code, h_code, h_name, sido_code, sido_name, event_note (또는 유사)
   - 자치구 32개가 11개 parent 시로 collapse 된 v2

3. **`1_codebooks/mortality_104_classification.csv`** — 사인 분류 코드북
   - 컬럼: cause_104 (정수 1-104), label_kr, label_en, category

4. **(참고) `0_raw/mortality_kostat/(수정_보건복지) 파일설계서_*.xlsx` 2개** — 컬럼 정의서 (2000-2007용, 2008-2009용)

## 출력 파일

1. **`processed/mortality/mortality_panel_v01.parquet`** — 메인 산출물
   - 컬럼: h_code, h_name, year, sex_code, age_5yr_code, outcome_group, deaths
   - 예상 row 수: 약 229 시군구 × 27년 × 2 성 × 17 연령bin × 5 outcome ≈ 1,050,000 (0 cell 포함)
   - 0 cell 도 explicit row (deaths=0)

2. **`processed/mortality/mortality_microdata_combined.parquet`** — 27년 결합 microdata (검증용)
   - 표준화된 컬럼명 + baseline h_code 매핑 + outcome_group 부여
   - 약 7-8M rows

3. **`processed/mortality/unmatched_mortality.parquet`** — 매핑 실패 record (검증용)

4. **`processed/mortality/mortality_panel_validation.md`** — 진단 보고서

## 처리 단계

### Step 1: 27 CSV 결합 + 컬럼 표준화

- glob 으로 27개 파일 경로 가져오기
- 각 파일을 `pd.read_csv(encoding='cp949', dtype=str)` 로 읽기 (모든 컬럼 string 으로, leading zero 보존)
- 파일명에서 연도 추출 (예: `1997_사망_연간자료_B형_*.csv` → year=1997)
- 컬럼명 영문 표준화 (mapping dictionary):
  - `사망자주소행정구역시도코드` → `sido_code`
  - `사망자주소행정구역시군구코드` → `sigungu_code_3digit`
  - `성별코드` → `sex_code`
  - `사망연령5세단위코드` → `age_5yr_code`
  - `사망원인_104항목분류코드` → `cause_104`
  - `사망원인_57항목분류코드` → `cause_57`
  - `사망연월일` → `death_date`
  - `사망장소코드` → `death_place_code`
  - `사망자직업분류코드` → `occupation_code`
  - `사망자혼인상태코드` → `marriage_status_code`
  - `교육정도코드` → `education_code`
- 27개 파일 결합 후 `mortality_microdata_combined.parquet` 저장 (utf-8)

### Step 2: raw_code 생성 + sigungu_crosswalk_v2 매핑

- `raw_code = sido_code.zfill(2) + sigungu_code_3digit.zfill(3)` (5자리 string)
- sigungu_crosswalk_v2 와 (year, raw_code) 키로 left join → h_code, h_name 추가
- **외국 거주자 / 미상 분리**: sido_code='99' 또는 sigungu_code='999' 또는 unmapped raw_code 인 record 를 별도 dataframe (`unmatched_mortality.parquet`) 으로 분리
- 분리 후 국내 거주자 record 만 다음 step 으로 진행

### Step 3: cause_104 → 5 outcome group 매핑

#### dtype 통일 (필수)

KOSTAT raw 의 cause_104 는 `dtype=str` 로 읽혀 zero-padded 3-digit string ("057", "081", "102" 등) 형식. mortality_104_classification.csv 의 cause_104 는 정수 1-104. 매핑 전에 **classification.csv 의 정수를 `.astype(str).str.zfill(3)` 적용하여 "001"-"104" string 으로 변환**한 후 KOSTAT raw 와 join. 매핑 직전 양쪽 dtype + 형식 sample 5개 print 로 검증.

#### 5 outcome group 정의 (mutually exclusive 보장)

```
despair_total  : cause_104 ∈ {"102", "101", "057", "081"}
                   (자살, 유독성물질 중독, 정신활성물질, 만성 간질환)
cardiovascular : cause_104 ∈ {"067", "068", "069", "070"}
cancer         : cause_104 ∈ {"027", "028", ..., "048"}  # 27-48 zero-padded
respiratory    : cause_104 ∈ {"073", "074", "075", "076", "077", "078"}
external_other : cause_104 ∈ {"097", "098", "099", "100", "103", "104"}
                   # 97-104 에서 자살 (102) + 유독성물질 중독 (101) 모두 제외
                   # 둘 다 despair_total 에 이미 포함되므로 mutual exclusivity 보장
```

각 record 에 `outcome_group` 컬럼 추가. **한 record 가 정확히 하나의 group 에만 속함** (mutually exclusive). 5 group 어디에도 안 속하는 record 는 `outcome_group = "other"` 로 표시 (분석 제외, 검증용 보존).

### Step 4: panel aggregation

- `(h_code, year, sex_code, age_5yr_code, outcome_group)` 으로 groupby + size() → `deaths` 컬럼
- panel skeleton 만들기:
  - 229 h_codes × 27년 × {1, 2} sex × age_5yr_code (실제 unique 값 기준) × {despair, cardiovascular, cancer, respiratory, external_other} 5 outcome
  - 모든 cell 포함 (0 cell 도 explicit row)
  - panel skeleton 과 actual deaths 를 left join, NaN → 0
- `mortality_panel_v01.parquet` 저장

### Step 5: 검증 (7가지)

다음 7가지 검증 + `mortality_panel_validation.md` 에 기록.

#### 검증 1 — 전체 사망자 합 보존

input microdata 의 row 수 == output panel 의 deaths 합. drop 된 record (외국 거주자 + 미상 + "other" 는 panel 에서 제외) 만 차이. 정확한 숫자 보고.

#### 검증 2 — Mutual exclusivity (필수, FAIL 시 즉시 중단)

각 record 가 정확히 하나의 outcome_group 에만 속함. 중복 record 0개 확인. 1개라도 중복이면 outcome_group 정의에 logic error → 즉시 보고 + 작업 중단.

#### 검증 3 — 연도별 coverage

1997-2023 모든 27년에 대해 deaths > 0 인 cell 존재. 어느 연도라도 deaths 합이 0 또는 비정상적으로 작으면 보고.

#### 검증 4 — Sigungu 매핑 실패율 (외국 거주자 분리)

외국 거주자 (sido_code='99' 또는 sigungu_code='999' 또는 unmapped raw_code) + 미상 record 를 별도 분리 후 **국내 거주자 기준 매핑 실패율** 계산.
- < 1% 합격
- 1-3% marginal (paper limitation 명시)
- > 3% critical (재검토)

외국 거주자 비율도 별도 보고 (한국에서 사망한 외국인은 매년 1-2% 가능).

#### 검증 5 — KOSTAT 공식 통계 cross-check (4개 연도 자살)

KOSTAT 사망원인통계 연간 발표 자료 기준 자살자 수와 panel 의 sex/age aggregate 합 비교:

| 연도 | 공식 자살자 수 | panel sum | diff (%) | PASS / FAIL |
|---|---|---|---|---|
| 2010 | ~15,566 | ? | ? | |
| 2011 | ~15,906 | ? | ? | |
| 2015 | ~13,513 | ? | ? | |
| 2019 | ~13,799 | ? | ? | |

**±2% 이내 일치** 합격 기준 (거주지 vs 사망지 기준, 외국인 포함 여부 등 source 정의 차이 감안).

#### 검증 6 — 연도별 사망자 패턴

한국 전체 사망자 수 시계열이 1997 (~24만) → 2010 (~26만) → 2020 (~30만) 증가 추세인지 확인. 연도별 합 plot 가능하면 보고서에 첨부.

#### 검증 7 — Cause_104 매핑 분포 detail

- 5 outcome group 별 record 수 + 비율
- "other" 그룹 record 수 + 비율
- "other" 그룹이 전체의 50% 이상이면 outcome group 정의 좁다는 신호 → 보고
- "other" 그룹의 cause_104 분포 상위 10개 (각 cause_104 의 record 수 + label_kr)

### Step 6: 산업 census + 인구 panel 과의 unit 일관성

future Stage 3 (인구 panel) + Stage 4 (산업 census) 와의 결합을 위한 unit 검증.

- **age_5yr_code 일관성 (필수)**: KOSTAT 사망 microdata 의 age_5yr_code unique 값 (보통 17개: 0-4, 5-9, ..., 80+, 미상 99) 을 KOSIS 인구 panel 의 5세 bin 코드 (000=계, 020=0-4세, 050=5-9세, ..., 340=80+) 와 비교. 두 source 의 형식이 다르면 매핑 dict 만들기 필요. 보고서에 양쪽 unique values + 매핑 가능성 명시.

- **sex_code 일관성**: KOSTAT (1=남, 2=여) vs KOSIS (1=남, 2=여, 0=계). 형식 일치 확인 + 분포 기록.

- **시군구 코드 형식 일관성 (필수)**: KOSTAT raw_code (sido 2자리 + sigungu 3자리 = 5자리) 가 KOSIS 인구 panel 의 시군구 코드 (C1, 5자리) 와 정확히 같은 format 인지 확인. KOSIS sample 시군구 코드 5개와 KOSTAT raw_code 5개 비교 print. 다르면 추가 매핑 필요 — 보고서에 명시.

## 주의 사항

1. **Raw 파일 read-only**. 27 cp949 CSV 절대 수정 X. 결합/표준화 산출물만 새로 저장.
2. **인코딩 일관성**. 모든 processed 파일은 utf-8.
3. **dtype string**. raw_code, cause_104 같은 ID 컬럼은 leading zero 보존 위해 모두 string 으로 처리. groupby 시 string 비교 정확.
4. **분구 자치구 자동 처리**. sigungu_crosswalk_v2 가 이미 자치구 raw_code → parent h_code 로 매핑되어 있어서 raw_code 31101 (덕양구) 가 자동으로 h_code 31100 (고양시) 에 들어감. 별도 처리 불필요.
5. **Validation 우선**. 7가지 검증 중 검증 2 (mutual exclusivity) 가 FAIL 이면 즉시 작업 중단 + 보고. 다른 검증 FAIL 시 commit 하지 말고 보고.

## 결과 검토 후 사용자 확인 필요

1. 27년 record 합 (예: 약 7-8M) 합리적인지
2. Mutual exclusivity 검증 PASS (중복 record 0개)
3. Sigungu 매핑 실패율 (외국 거주자 제외 후 < 1% 목표)
4. KOSTAT 자살률 cross-check 4개 연도 모두 ±2% 이내 일치
5. mortality_panel_v01.parquet 의 row 수 + 0 cell 비율 합리적인지
6. age_5yr_code unique values + 시군구 코드 형식 일관성 (Stage 3 결합 가능 여부)
7. "other" 그룹 비율 + 분포 상위 10개 (5 outcome group 정의의 적정성)

위 7개 OK 면 Stage 2 완료.

**Stage 2 산출물의 위상**: `mortality_panel_v01.parquet` 는 deaths count 까지 final. 사망률 (per 100,000) + 연령 표준화 + 로그 변환은 Stage 3 (인구 panel) 결합 후 별도 단계에서 처리. Stage 3 가 끝나야 본 paper 의 종속변수 (ln(despair mortality rate) 등) 가 완성.

**다음 step**: Stage 3 (인구 panel) → Stage 2 + 3 결합 (사망률 계산 + 연령표준화 + 로그변환) → Stage 7 (가족구조 mediator) → Stage 4 (산업 census KSIC2 baseline shares).

---

이 prompt 를 Claude Code 에 그대로 전달. 산출물은 `processed/mortality/` 폴더에 저장.
