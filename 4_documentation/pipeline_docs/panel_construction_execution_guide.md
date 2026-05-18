# Panel 구축 실행 가이드

## 무역 충격, 가족 해체, 그리고 절망사: 한국의 숨은 메커니즘

**작성 목적:** Panel 구축 작업을 실제로 수행할 때 step-by-step으로 따라할 수 있는 실행 매뉴얼이다. 이전에 만든 `panel_construction_working_doc.md`가 작업의 큰 그림이라면, 이 문서는 매일의 코드 작업과 의사결정을 어떻게 할지의 실용 가이드다.

**작업 환경:** Python 3.10+, Jupyter notebook 또는 IDE, Git 사용 권장.
**필수 라이브러리:** pandas, numpy, pyarrow, openpyxl, xlrd, statsmodels, linearmodels, matplotlib.

---

## 1. 시작 전 환경 준비

작업을 시작하기 전에 환경을 정리하는 것이 첫 단계다. 일주일 정도 시간을 들여 다음 작업을 마치면 이후 작업이 매끄럽게 진행된다.

먼저 작업 폴더를 만든다. 본인 컴퓨터의 적절한 위치에 paper 작업 폴더를 만든다. 폴더 이름은 `family_disruption_paper` 또는 본인이 기억하기 쉬운 이름으로 한다. 이 폴더 안에 raw, processed, crosswalks, panel, code, logs, docs 일곱 개 하위 폴더를 만든다.

다음으로 가지고 있는 raw 데이터를 raw 폴더로 옮긴다. 현재 `/mnt/user-data/uploads/`에 있는 모든 데이터(`mortality_kostat`, `kosis_population`, `comtrade_korea_china`, `comtrade_china_world`, `comtrade_adh_china`, `ecos_macro`, `ecos_delinquency`, `industry_census`, `research_supp`, `research_materials`, `ssaggregate-main`)를 본인 작업 폴더의 raw 폴더 아래에 그대로 복사한다. raw 폴더는 절대 수정하지 않는 원본 보관소다.

다음으로 Git 저장소를 초기화한다. 작업 폴더에서 `git init`을 실행하고 `.gitignore` 파일을 만든다. `.gitignore`에 `raw/`, `processed/`, `panel/`, `*.csv`, `*.parquet`, `*.xlsx`, `*.xls`, `__pycache__/`, `.ipynb_checkpoints/`, `*.log`을 추가한다. Raw 데이터와 중간 산출물은 git에 올리지 않고, 코드와 문서만 버전 관리한다.

다음으로 Python 가상환경을 만든다. `python -m venv venv`로 가상환경을 만들고 활성화한 후 필수 라이브러리를 설치한다. 이렇게 하면 다른 프로젝트와 라이브러리 충돌이 없다.

다음으로 첫 코드 파일을 만든다. `code/00_setup.py` 파일을 만들어서 모든 후속 코드에서 공유할 path와 상수를 정의한다. RAW_DIR, PROCESSED_DIR, CROSSWALK_DIR, PANEL_DIR 같은 변수와 BASELINE_YEAR=1997, BASELINE_NUM_SIGUNGU=256, ANALYSIS_START=1997, ANALYSIS_END=2023 같은 상수를 정의한다. 이걸 매 스크립트 시작에서 import해서 일관성을 유지한다.

마지막으로 작업 일지 파일을 만든다. `docs/work_log.md` 파일을 만들어서 매일 또는 매주 본인이 무엇을 했는지 기록한다. 의사결정이 어떻게 진행됐는지, 어떤 문제를 만나서 어떻게 해결했는지 짧게 적는다. 이 일지가 paper 작성 시 큰 도움이 된다.

여기까지가 작업 시작 전 환경 준비다. 약 2-3일 소요된다.

---

## 2. Stage 1: 시군구 Crosswalk 구축

### 2.1 작업 목적과 마음가짐

이 작업은 panel 구축의 가장 첫 단계이자 가장 까다로운 단계다. 이걸 제대로 안 하면 모든 후속 panel이 시군구 매핑 inconsistency를 가진다. 시간이 들더라도 정확하게 해야 한다. 약 1주일을 잡고 진행한다.

### 2.2 첫 번째 작업 — 행정구역 변경 사례 조사

먼저 분석 기간(1997-2023) 동안 발생한 모든 시군구 변경 사례를 정리한다. KOSIS 또는 통계청 사이트에서 행정구역 변천사 자료를 받는다. 검색어는 "행정구역 변천사", "시군구 통합 분리"다. 행정안전부에서 발표하는 자료가 가장 정확하다.

수집한 자료를 기반으로 `crosswalks/sigungu_changes_log.md` 파일을 만든다. 각 변경 사례를 다음 형식으로 적는다. 변경 일자, 변경 전 시군구 (시도 코드 + 시군구 코드 + 이름), 변경 후 시군구 (시도 코드 + 시군구 코드 + 이름), 변경 유형 (통합/분리/명칭변경/승격/이동), 비고. 약 30-40개 사례가 나올 것이다.

핵심 사례를 미리 알려준다. 2010년 마산-창원-진해 통합, 2014년 청주-청원 통합, 2003년 김포 시 승격, 2014년 여주 시 승격, 2013년 세종특별자치시 신설(공주시·연기군 일부 분리), 1995년 광주광역시 광산구 편입 이전 등이다. 이 사례들이 가장 큰 변경이다.

### 2.3 두 번째 작업 — Baseline 결정과 매핑 원칙 수립

Baseline은 2021년 KOSTAT 행정구역 기준 256개 시군구로 정한다. 이미 PAP에서 결정된 사항이다. 다만 매핑 원칙을 명시적으로 수립한다.

매핑 원칙은 다음과 같다. 통합 사례는 historical 시군구 여러 개가 baseline 시군구 하나에 매핑된다. 예를 들어 마산시(historical), 창원시(historical), 진해시(historical) 모두가 통합 창원시(baseline)에 매핑된다. 분리 사례는 historical 시군구 하나가 baseline 시군구 여러 개에 매핑된다. 이 경우 인구 분포 또는 면적 비율로 가중치를 준다. 분석 기간 안에는 큰 분리 사례가 세종시 정도이므로 처리가 비교적 단순하다. 명칭 변경은 같은 baseline 시군구로 매핑된다. 승격(군 → 시)도 같은 baseline 시군구로 매핑된다.

세종시 처리는 별도로 정한다. 2012년 7월 출범했고, 그 이전에는 충청남도 연기군과 공주시 일부였다. 본 paper의 분석에서 두 가지 옵션이 있다. 첫째는 세종시를 baseline에 포함시키되 2012년 이전 데이터는 historical 연기군 데이터를 사용하는 것이다. 둘째는 세종시를 분석에서 제외하는 것이다. Sample size를 위해 첫째 옵션을 권장한다.

### 2.4 세 번째 작업 — Crosswalk 매핑표 작성

`crosswalks/sigungu_crosswalk.csv` 파일을 만든다. 컬럼은 year, historical_sido_code, historical_sigungu_code, historical_name, baseline_sigungu_code, baseline_name, mapping_weight, mapping_notes로 구성한다.

mapping_weight는 분리 사례에서 사용한다. 예를 들어 historical 연기군이 세종시(baseline)에 1.0으로 매핑되고, historical 공주시 일부가 세종시(baseline)에 0.05로(공주시 면적의 5% 정도) 매핑되고 동시에 baseline 공주시에 0.95로 매핑되는 식이다. 통합과 명칭 변경은 weight 1.0이다.

매핑표는 약 27년 × 256 baseline + 변경 사례 = 약 7천 row 정도 된다. Excel이나 Python에서 작성한 후 CSV로 저장한다.

### 2.5 네 번째 작업 — 매핑 검증

매핑 검증은 Python 스크립트로 수행한다. `code/01_sigungu_crosswalk_validation.py` 파일을 만든다. 검증 항목은 세 가지다.

첫째, 모든 historical 시군구가 baseline에 매핑되는지 확인한다. 매핑 안 된 historical 시군구가 있으면 누락이다. KOSIS 인구 panel에서 historical 시군구 코드 목록을 가져와서 crosswalk에 다 들어있는지 확인한다.

둘째, 매핑 weight 합이 일관된지 확인한다. 각 historical 시군구의 mapping_weight 합이 1.0이어야 한다 (모든 인구가 어딘가로 가야 함). 분리 사례에서 weight 합이 1.0이 아니면 매핑 오류다.

셋째, 인구 검증을 한다. 각 baseline 시군구의 historical 시군구들을 합쳤을 때 인구 합계가 통계청 발표 인구와 일치하는지 확인한다. 예를 들어 2009년 통합 창원시(baseline)의 인구는 2009년 historical 마산시 + 창원시 + 진해시의 인구 합과 같아야 한다. 차이가 1% 이하면 통과로 본다.

검증 결과를 `crosswalks/validation_report.md`에 기록한다. 어떤 항목이 통과했는지, 어떤 부분에서 오차가 있는지 적는다.

### 2.6 시간 추정과 어려움

이 단계 전체에 약 1주일이 든다. 행정구역 조사에 2일, 매핑표 작성에 2-3일, 검증과 디버깅에 1-2일이다. 가장 큰 어려움은 통계청과 행정안전부의 시군구 코드가 다를 수 있다는 점이다. KOSIS는 5자리 코드(시도 2자리 + 시군구 3자리)를 쓰는데, KOSTAT 사망 microdata도 비슷한 구조이지만 정확히 같은지 확인이 필요하다. 만약 다르면 추가 매핑이 필요하다.

---

## 3. Stage 2: 사망 Panel 구축

### 3.1 작업 시작 전 점검

Stage 1이 완료되어야 Stage 2를 시작할 수 있다. `crosswalks/sigungu_crosswalk.csv`가 만들어져 있어야 한다. 만약 아직 없다면 Stage 1을 먼저 마친다.

### 3.2 첫 번째 작업 — 27개 CSV 결합

`code/02_mortality_combine.py` 파일을 만든다. raw 폴더의 `mortality_kostat/사망사료 정리/` 안에 있는 27개 CSV를 모두 읽어서 하나의 dataframe으로 결합한다.

핵심 코드 흐름은 이렇다. glob으로 27개 파일 경로를 모두 가져온다. 각 파일을 pandas read_csv로 읽되 encoding은 cp949로 지정한다. encoding 오류가 발생하면 errors='replace' 옵션을 추가한다. 모든 파일을 읽은 후 pandas concat으로 결합한다.

주의할 점은 컬럼명이 시기에 따라 다를 수 있다는 점이다. 가지고 있는 KOSTAT 파일설계서 두 개(2000-2007용, 2008-2009용)를 참고해서 컬럼명을 비교한다. 컬럼명이 다르면 일관된 영문 컬럼명으로 rename한다. 예를 들어 `사망자주소행정구역시도코드`는 `sido_code`로, `사망자주소행정구역시군구코드`는 `sigungu_code_orig`로, `사망원인_104항목분류코드`는 `cause_104`로 변경한다.

각 record의 사망 연도가 명시되어 있는지 확인한다. 각 파일이 한 연도의 데이터이니 파일명에서 연도를 추출해서 `year` 컬럼으로 추가한다.

결합한 dataframe을 `processed/mortality/mortality_microdata_1997_2023.parquet` 파일로 저장한다. parquet 형식이 CSV보다 훨씬 빠르고 용량이 작다.

### 3.3 두 번째 작업 — 시군구 매핑

`code/03_mortality_map_sigungu.py` 파일을 만든다. 결합된 사망 microdata에 baseline 시군구 코드를 추가한다.

코드 흐름은 이렇다. mortality_microdata와 sigungu_crosswalk을 병합한다. 병합 키는 (sido_code, sigungu_code_orig, year)이다. 병합 결과로 baseline_sigungu_code가 추가된다.

매핑 실패 record를 별도로 처리한다. 외국인 거주자, 미상 시군구, 또는 crosswalk에 없는 시군구가 매핑 실패한다. 이런 record를 별도 dataframe으로 빼내고 비율을 계산한다. 매핑 실패율이 1% 이하면 정상이다. 만약 더 높으면 crosswalk에 누락이 있을 수 있으므로 Stage 1을 다시 검토한다.

### 3.4 세 번째 작업 — Outcome Group 정의

`code/04_mortality_outcome_groups.py` 파일을 만든다. KOSTAT 104분류 코드를 5개 outcome group으로 분류한다.

먼저 outcome group 정의 dictionary를 만든다. despair는 [102, 101, 057, 081], cardiovascular는 [067, 068, 069, 070], cancer는 list(range(27, 49)), respiratory는 [073, 074, 075, 076, 077, 078], external_other는 list(range(97, 105))에서 102를 제외한 것이다.

각 record에 outcome group을 매핑한다. cause_104 코드가 어느 group에 속하는지 확인해서 새 컬럼 outcome_group을 추가한다. 한 record가 여러 group에 속할 수는 없다.

다음으로 group별 사망자 수를 계산한다. (baseline_sigungu_code, year, sex, age_5yr, outcome_group)으로 groupby한 후 record 수를 세서 deaths 컬럼을 만든다. 결과는 시군구 × 연도 × 성 × 5세 연령 × outcome group panel이다. cell 수는 약 256 × 27 × 2 × 17 × 5 ≈ 117만이지만 0 cell이 많아 실제 row 수는 더 적다.

이 panel을 `processed/mortality/mortality_deaths_panel.parquet`로 저장한다.

### 3.5 네 번째 작업 — 인구 분모 결합과 사망률 계산

먼저 Stage 3 (인구 panel)을 마친 후 이 작업을 한다. 즉 Stage 2의 마지막 단계는 Stage 3 완료 후로 미룬다. 이 순서로 작업하면 코드가 자연스럽다.

### 3.6 시간 추정

Stage 2 전체에 약 5-7일이 든다. CSV 결합에 1-2일, 시군구 매핑에 1-2일, outcome group 정의에 1-2일이다. 가장 큰 변수는 컬럼명 표준화와 인코딩 오류 처리다.

---

## 4. Stage 3: 인구 Panel 구축

### 4.1 첫 번째 작업 — KOSIS 인구 데이터 처리

`code/05_population_panel.py` 파일을 만든다. raw 폴더의 `kosis_population/population_combined.csv`를 읽는다. 이미 정리된 panel이라 처리가 비교적 간단하다.

코드 흐름은 이렇다. read_csv로 파일을 읽고 컬럼명을 영문으로 변경한다. C1은 sigungu_code_orig, C2는 sex_code, C3는 age_5yr_code로 rename한다. 성별 코드 (0=계, 1=남, 2=여)와 연령 코드를 일관된 형식으로 정리한다.

다음으로 시군구 매핑을 한다. sigungu_crosswalk과 병합해서 baseline_sigungu_code를 추가한다. 매핑 후 (baseline_sigungu_code, year, sex_code, age_5yr_code)로 groupby해서 인구 합계를 계산한다. 통합 사례에서 historical 시군구 여러 개의 인구가 baseline 시군구 하나에 합쳐진다.

### 4.2 두 번째 작업 — 연령 그룹 재분류

`code/06_population_age_groups.py` 파일을 만든다. 5세 연령 bin을 paper 분석에 사용할 연령 그룹으로 재분류한다.

연령 그룹 정의는 다음과 같다. youth는 15-24세 (5세 bin 040, 050), working_age는 25-54세 (5세 bin 060, 070, 080, 090, 100, 110), middle_age는 55-64세 (5세 bin 120, 130), elderly는 65+ (5세 bin 140, 150, 160 등). 0-14세는 본 paper 분석에서 제외한다 (절망사 분석은 성인 대상).

age_group 컬럼을 추가한다. age_5yr_code를 위 정의에 따라 매핑한다.

### 4.3 세 번째 작업 — Stage 2 사망률 완성

이제 Stage 2의 마지막 단계를 진행한다. `code/07_mortality_rates.py` 파일을 만든다. mortality_deaths_panel과 population_panel을 병합한다. 병합 키는 (baseline_sigungu_code, year, sex_code, age_5yr_code)이다.

병합 후 사망률을 계산한다. mortality_rate = deaths / population × 100,000 이다. 인구 0인 cell은 결측치 처리한다.

연령 표준화 사망률 계산은 별도 함수로 작성한다. 2000년 한국 인구의 5세 bin별 분포를 표준 인구로 정의한다. 시군구 × 연도 × 성 × outcome group으로 groupby한 후 5세 bin별 사망률에 표준 인구 가중치를 곱해서 합산한다. 이게 직접 표준화 방법이다.

로그 변환을 적용한다. log_mortality_rate = ln(mortality_rate + 1) 이다.

최종 panel을 `processed/mortality/mortality_panel_final.parquet`로 저장한다. 컬럼은 baseline_sigungu_code, year, sex_code, age_group, outcome_group, deaths, population, mortality_rate, age_adjusted_rate, log_mortality_rate다.

### 4.4 시간 추정

Stage 3 전체에 약 3-4일이 든다. 인구 panel 처리는 빠르지만 사망률 결합과 표준화 계산이 시간이 든다.

---

## 5. Stage 4: 산업 Census와 Baseline Shares

### 5.1 첫 번째 작업 — 1997년 산업 Census 처리

`code/08_industry_shares.py` 파일을 만든다. raw 폴더의 `industry_census/` 안에 있는 1997년 산업 census 파일을 읽는다. 파일 크기가 195MB로 크니 chunk 단위 처리를 고려한다.

읽기는 read_csv with encoding='cp949'와 chunksize=100000으로 한다. 각 chunk를 처리하면서 시군구 × KSIC 산업별 종사자 수를 집계한다.

KOSIS 산업 census 컬럼을 확인한다. 보통 시도, 시군구, KSIC 산업분류 코드, 사업체 수, 종사자 수가 들어있다. 컬럼명이 한글이니 영문으로 rename한다.

KSIC 분류 표준화를 한다. 1997년 데이터는 KSIC 8차 분류이니 가지고 있는 KSIC crosswalk(`research_supp/ksic_crosswalk_8_to_9.csv`, `9_to_10.csv`, `10_to_11.csv`)를 단계적으로 적용해서 KSIC 11차 2자리 분류로 변환한다.

KSIC 11차 2자리 제조업 코드는 약 24개다. 코드 10번대(농림어업)와 30번대 후반 이상(서비스업)은 제외하고 10-33번대(제조업)만 사용한다.

### 5.2 두 번째 작업 — Baseline Shares 계산

시군구 × KSIC 산업별 종사자 수를 (baseline_sigungu_code, ksic2)로 정리한다. 시군구 매핑은 sigungu_crosswalk으로 baseline에 맞춘다.

각 시군구의 baseline shares를 계산한다. share = (시군구 × 산업의 종사자 수) / (시군구의 전체 종사자 수) 이다. 합이 1이 되어야 한다.

비제조업도 포함시킨다. 비제조업의 share는 1 - 제조업 share 합이다. 비제조업은 단일 카테고리로 묶어도 되고 세분해도 된다. 본 paper에서는 단일 카테고리(non_manufacturing)로 묶는다.

`processed/industry_census/baseline_shares_1997.parquet` 파일에 저장한다. 컬럼은 baseline_sigungu_code, ksic2, employment, total_employment, share다.

### 5.3 세 번째 작업 — Robustness용 Baseline Shares

1990년과 2000년 산업 census 파일이 있는지 raw 폴더에서 확인한다. 가지고 있는 industry_census 폴더는 1994-2010년이라 1990년이 없을 수 있다. 1990년이 없으면 1994년을 가장 이른 baseline으로 사용한다.

1994년과 2000년 baseline shares도 같은 절차로 계산해서 robustness용으로 저장한다.

### 5.4 시간 추정

Stage 4에 약 1-2주일이 든다. 1997 census 파일 처리에 3-4일, KSIC 변환에 3-4일, 검증에 2-3일이다. KSIC 변환이 가장 까다롭다.

---

## 6. Stage 5: Comtrade 데이터와 무역 충격

### 6.1 KSIC-HS6 매핑 작업

`code/09_ksic_hs6_mapping.py` 파일을 만든다. 가장 까다로운 단계다.

먼저 통계청 또는 UN Statistics Division 사이트에서 KSIC-HS 직접 매핑이 공개되어 있는지 확인한다. 검색어는 "KSIC HS classification mapping" 또는 "한국표준산업분류 HS 연계표"다. 통계청 홈페이지의 한국표준산업분류 자료실에 있을 가능성이 있다.

직접 매핑이 없으면 단계적 변환을 한다. 가지고 있는 자료는 KSIC11-ISIC4 (`research_materials/8.한국표준산업분류 제11차-국제표준산업분류 제4차 연계표.xlsx`), CPC21-HS2012 (`cpc21-hs2012.txt`), CPC21-ISIC4 (`cpc21-isic4.txt`)다.

단계적 변환 로직은 이렇다. KSIC2 → ISIC4 (직접 매핑) → CPC21 (CPC-ISIC4 역매핑) → HS2012 (CPC-HS2012 직접 매핑) → HS6 (HS2012의 6자리). 각 단계에서 일대다 매핑이 발생할 수 있으므로 가중치 처리가 필요하다. 가중치는 일단 균등 분할(equal split)로 시작한다.

매핑 결과를 `crosswalks/ksic2_to_hs6.csv`에 저장한다. 컬럼은 ksic2, hs6, weight다.

### 6.2 KR-CN Bilateral 무역 충격 계산

`code/10_comtrade_krcn.py` 파일을 만든다. raw 폴더의 `comtrade_korea_china/`에 있는 50개 CSV를 결합한다.

flowCode로 수출(X)과 수입(M)을 분리한다. KR이 reporter이고 CN이 partner인 경우 flowCode X는 한국 → 중국 수출, flowCode M은 중국 → 한국 수출(한국 입장에서 수입)이다. 두 flow를 다 포함한 panel을 만든다.

HS6를 KSIC2로 매핑한다. ksic2_to_hs6 crosswalk을 사용해서 각 HS6 product line을 KSIC2 산업으로 변환한다. 일대다 매핑이면 가중치로 분배한다.

산업 j × 연도 t의 한국 → 중국 수출액 X_jt와 중국 → 한국 수출액 M_jt를 계산한다. Net export는 X_jt - M_jt다.

무역 충격 g_jt를 계산한다. main spec은 5년 변화로 g_jt = ln(NetExport_jt + 1) - ln(NetExport_{j,t-5} + 1)이다. Net export가 음수일 수 있으므로 signed log transformation 또는 +large constant로 처리한다.

`processed/comtrade/krcn_shocks_panel.parquet`에 저장한다.

### 6.3 ADH 8국 무역 충격 계산 (Robustness)

`code/11_comtrade_adh.py` 파일을 만든다. raw 폴더의 `comtrade_adh_china/`에 있는 176개 CSV를 결합한다. 8개국이 중국에서 수입한 데이터다.

8개국의 산업별 대중국 수입을 합산해서 ADH 8국 대중국 수입 M^ADH_jt를 계산한다.

스페인과 독일 누락 처리를 명시적으로 한다. 스페인은 2004년 이후 거의 누락이라 분석에서 제외한다. 독일은 2019, 2021-2024 누락이지만 다른 연도는 가용하므로 보간한다. main spec은 7개국(스페인 제외)으로 가고, robustness로 6개국(스페인, 독일 제외) 결과도 보고한다.

무역 충격은 5년 변화 ln(M^ADH_jt) - ln(M^ADH_{j,t-5})로 계산한다.

`processed/comtrade/adh_shocks_panel.parquet`에 저장한다.

### 6.4 시간 추정

Stage 5에 약 1-2주일이 든다. KSIC-HS6 매핑이 4-5일, KR-CN 처리가 2-3일, ADH 처리가 2-3일이다.

---

## 7. Stage 6: Bartik IV 계산

`code/12_bartik_iv.py` 파일을 만든다.

baseline_shares_1997과 무역 충격 panel을 ksic2 키로 결합한다. 시군구 c × 연도 t × 산업 j cell마다 share s_cj와 shock g_jt가 만난다.

시군구 c × 연도 t의 Bartik IV는 산업 j에 대한 (s_cj × g_jt)의 합이다. groupby (baseline_sigungu_code, year)로 sum 처리한다.

KR-CN main IV와 ADH robustness IV를 따로 계산해서 두 컬럼으로 저장한다.

5-year stacked IV도 계산한다. period 정의 (1997-2002, 2002-2007,...)에 따라 시작 시점과 끝 시점의 Bartik IV 차이를 구한다. delta_bartik_krcn, delta_bartik_adh 컬럼을 만든다.

`processed/bartik/bartik_iv_panel.parquet`에 저장한다.

이 단계에 약 2-3일이 든다.

---

## 8. Stage 7: 가족 구조 매개변수 Panel

### 8.1 첫 번째 작업 — 출생/혼인/이혼 처리

`code/13_family_structure.py` 파일을 만든다. raw 폴더의 `research_supp/시군구 출생아.xls`, `시군구 혼인.xls`, `시군구 이혼.xls` 파일을 처리한다.

xls 파일은 read_excel(engine='xlrd')로 읽는다. 각 파일은 시군구 × 연도 panel 구조다. 컬럼명을 표준화하고 시군구 코드를 baseline에 매핑한다.

인구 panel과 결합해서 비율을 계산한다. marriage_rate = 혼인 건수 / 인구 × 1000, divorce_rate = 이혼 건수 / 인구 × 1000, birth_rate = 출생아 수 / 인구 × 1000이다. 인구 분모는 이미 만든 population_panel을 사용한다.

### 8.2 두 번째 작업 — 합계출산율 처리

`research_supp/시군구_출생아수__합계출산율_*.xlsx` 파일을 처리한다. read_excel(engine='openpyxl')로 읽는다. 합계출산율 컬럼을 추출해서 baseline 시군구 매핑한다.

### 8.3 세 번째 작업 — KOSIS 인구주택총조사 추가 다운로드

KOSIS 사이트(kosis.kr)에 회원가입하고 인구주택총조사 데이터를 받는다. 검색어는 "인구주택총조사 시군구 1인가구"다. 5년 간격(1995, 2000, 2005, 2010, 2015, 2020) 시군구 단위 결과를 받는다. 1인가구 수와 전체 가구 수가 핵심 변수다.

다운로드한 파일을 raw 폴더의 새 하위 폴더 `kosis_household/`에 저장한다.

`code/14_household_panel.py` 파일을 만든다. 다운로드한 6개 시점의 데이터를 처리해서 시군구 × 5년시점 panel로 만든다. 시군구 매핑 후 1인가구 비율을 계산한다.

5년 간격을 연간 panel로 변환한다. linear interpolation을 사용한다. scipy의 interp1d 또는 pandas의 interpolate 함수로 처리한다. 각 시군구별로 (1995, 2000, 2005, 2010, 2015, 2020) 점들을 잇고 사이 연도 값을 추정한다. boolean 컬럼 `imputed`를 추가해서 어느 cell이 추정값인지 표시한다.

### 8.4 결과 저장과 시간

family_panel을 `processed/family_structure/family_panel.parquet`에 저장한다. 컬럼은 baseline_sigungu_code, year, marriage_rate, divorce_rate, birth_rate, tfr, single_household_rate, single_household_imputed다.

Stage 7에 약 5-7일이 든다. 출생/혼인/이혼 처리에 2-3일, 합계출산율 처리에 1일, 인구주택총조사 다운로드와 처리에 2-3일이다.

---

## 9. Stage 8: 보조 매개변수와 통제변수

이 단계는 main paper의 robustness용이라 우선순위가 낮다. 시간이 부족하면 가족 구조 매개변수 분석을 먼저 끝내고 이 단계는 후순위로 미룬다.

### 9.1 노동시장 Panel

KOSIS 사이트에서 시군구 노동시장 panel을 추가 다운로드한다. 검색어는 "시군구 실업률 고용률"이다. 2008년 이후 가용하다.

`code/15_labor_market.py` 파일을 만든다. 다운로드한 파일을 처리해서 baseline 시군구 panel로 만든다.

### 9.2 ECOS 가계부채 Panel

`code/16_household_debt.py` 파일을 만든다. raw 폴더의 `ecos_delinquency/`에 있는 5개 series를 처리한다. 시도 단위 panel이라 시군구 매핑 시 시도 코드(baseline_sigungu_code의 첫 2자리)로 broadcast한다.

### 9.3 HIRA 의료인력 Panel

`code/17_hira_medical.py` 파일을 만든다. raw 폴더의 `research_supp/kosis_hira_quarterly_2009_2025.csv`를 처리한다. 분기 단위라 연간으로 aggregate(연 평균 또는 연말 값)한다.

### 9.4 ECOS Macro와 GRDP

`code/18_macro_controls.py` 파일을 만든다. raw 폴더의 `ecos_macro/`의 11개 series를 처리한다. 월간 또는 연간 시리즈를 연 단위로 정리한다.

GRDP는 KOSIS에서 추가 다운로드한다. 검색어는 "시군구 GRDP"다.

### 9.5 시간 추정

Stage 8 전체에 약 1주일이 든다. 각 source별 처리에 1-2일이다.

---

## 10. Stage 9: Master Panel Merge

`code/19_master_panel.py` 파일을 만든다.

먼저 panel skeleton을 만든다. 256 baseline 시군구 × 27년 = 6,912 cells의 base dataframe을 만든다. 모든 가능한 조합을 itertools.product로 생성한다.

차례로 left merge한다. mortality_panel_final → bartik_iv_panel → family_panel → labor_panel → debt_panel(시도 broadcast) → hira_panel → macro_panel → grdp_panel 순서로 결합한다.

merge 키는 (baseline_sigungu_code, year)다. 일부 panel은 (baseline_sigungu_code, year, sex, age_group) 구조이므로 reduced form 분석용 panel(시군구 × 연도)과 demographic 분석용 panel(시군구 × 연도 × 성 × 연령)을 따로 만든다.

5-year stacked panel도 만든다. period 정의에 따라 시작과 끝의 변수 차이를 계산한다. 5 period × 256 시군구 = 1,280 row가 된다.

세 가지 master panel을 저장한다. `panel/master_panel_sigungu_year.parquet` (시군구 × 연도, reduced form용), `panel/master_panel_5year_stacked.parquet` (5-year stacked, main spec용), `panel/master_panel_demographic.parquet` (시군구 × 연도 × 성 × 연령, hetero 분석용).

이 단계에 약 3-5일이 든다.

---

## 11. Stage 10: 검증과 Descriptive Statistics

`code/20_descriptive_statistics.py` 파일을 만든다.

먼저 panel structure 검증을 한다. cell 수, missing 비율, 변수별 분포를 확인한다. 이상치(outlier)를 발견하면 데이터 입력 오류 가능성을 검토한다.

주요 변수의 시간 추세 그래프를 그린다. 한국 평균값의 시간 추세가 직관과 일치하는지 확인한다. 예를 들어 합계출산율이 1997년부터 2023년까지 감소 추세인지, 절망사 사망률이 2000년대 초반에 정점인지 등이다.

Cross-sectional variation을 확인한다. 시군구별 baseline 산업 비중 분포, Bartik IV 분포, 가족 구조 변수 분포를 본다.

Descriptive statistics 표를 만든다. paper Section 3에 들어갈 표 3개를 작성한다. Table 1은 데이터 출처와 분석 기간 정리, Table 2는 핵심 변수의 1997, 2010, 2020 시점 평균/표준편차/min/max, Table 3은 outcome group의 KOSTAT 코드 매핑이다.

표를 `docs/descriptive_tables.md`에 markdown 형식으로 저장한다.

검증 결과를 `docs/data_quality_report.md`에 보고서로 저장한다. 어떤 검증을 했는지, 어떤 결과가 나왔는지, 어떤 문제가 있었고 어떻게 처리했는지 적는다.

이 단계에 약 1주일이 든다.

---

## 12. 작업 중 마음가짐과 막혔을 때 대처

전체 작업이 약 6-8주 걸리는 큰 프로젝트다. 매주 progress가 눈에 보이지 않을 수 있고, 디버깅에 며칠씩 갈리는 단계가 있을 수 있다. 마음가짐 몇 가지를 짚는다.

먼저 매일 작업 일지를 쓴다. `docs/work_log.md`에 그날 무엇을 했는지, 어떤 문제를 만났는지, 어떻게 해결했는지 짧게 적는다. 한 줄도 좋다. 한 달 후 본인이 어떤 의사결정을 했는지 다시 확인할 때 큰 도움이 된다.

그리고 작은 단위로 commit한다. Git을 쓰니까 매일 또는 매번 작은 작업 후 commit한다. commit message에 무엇을 했는지 짧게 적는다. 나중에 코드를 되돌릴 때 유용하다.

검증을 매 단계마다 한다. 한 단계가 끝나면 결과 dataframe의 shape, 결측치 비율, 평균값 등을 확인한다. 이상하면 다음 단계로 넘어가지 말고 디버깅한다. 잘못된 데이터로 다음 단계 진행하면 디버깅이 더 어려워진다.

막혔을 때 대처는 이렇다. 한 시간 이상 같은 문제로 막히면 잠시 멈추고 다른 단계로 넘어간다. 머리를 쉬고 다시 돌아오면 해결책이 보일 때가 많다. 또는 짧게 정리해서 저에게 물어보세요. Conversation 안에서 같이 디버깅할 수 있어요.

특히 시군구 매핑에서 막힐 가능성이 높다. KOSIS, KOSTAT, 행정안전부의 시군구 코드 체계가 미세하게 다를 수 있고, 통합/분리/명칭변경이 복잡하게 얽힌 사례가 있을 수 있다. 이 부분은 시간을 충분히 들여서 정확히 한다.

KSIC-HS6 매핑도 까다로운 단계다. 직접 매핑이 없어서 단계적 변환을 해야 하고, 변환 정보 손실이 발생한다. 이 부분에서 막히면 통계청 자료실을 추가로 검색하거나 저에게 알려주세요.

---

## 13. 이 작업이 끝난 후 다음 단계

Panel 구축이 완료되면 paper 작업의 나머지 단계로 넘어간다. 다음 단계는 회귀 분석이다. 이때 추가로 필요한 문서가 회귀 분석 작업 매뉴얼이다. Reduced form 회귀, 매개 분석, 식별 진단(Rotemberg HHI, share-covariate balance, pre-trend, AKM SE, 5-layer 표준오차)을 어떻게 돌릴지의 step-by-step 절차다. Python linearmodels 라이브러리 사용법, R ssaggregate 패키지 사용법, 회귀 결과 해석 방법이 포함된다.

이 매뉴얼은 panel이 완성된 후 데이터를 본 다음 만드는 게 효율적이다. 데이터 실제 모습을 보고 어떤 spec이 적합한지 정한 후 작성한다.

또 paper 본문 Section 4-7 작성 가이드도 panel 구축 후 만든다. Section 4는 Identification Strategy, Section 5는 Reduced Form, Section 6은 Mediation Analysis, Section 7은 Robustness, Heterogeneity, Discussion이다. 결과를 본 후 작성하는 게 자연스럽다.

지금은 panel 구축에 집중한다. 작업 중 막히는 부분이 생기면 conversation에서 같이 풀어요.

---

**END OF PANEL CONSTRUCTION EXECUTION GUIDE v1.0**
