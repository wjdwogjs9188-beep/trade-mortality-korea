# Panel 구축 작업 문서

## 무역 충격, 가족 해체, 그리고 절망사: 한국의 숨은 메커니즘

**작성 목적:** Raw 데이터에서 분석 가능한 master panel까지 구축하는 전체 단계를 정리한 작업 매뉴얼이다. 본인이 panel 작업할 때 step-by-step으로 따라할 수 있도록 작성한다. Paper 본문에는 들어가지 않으며 online appendix 또는 replication package의 base가 된다.

**작업 환경 가정:** Python 3.10 이상, pandas, numpy, pyreadstat, openpyxl 등 표준 데이터 처리 라이브러리. R은 ssaggregate 패키지 사용 시에만.

**전체 작업 시간 추정:** 약 4-6주 (full-time 작업 기준). 가장 큰 시간 소요는 시군구 crosswalk 작업과 KSIC-HS6 변환이다.

---

## 1. 작업 폴더 구조 설계

### 1.1 권장 폴더 구조

작업 시작 전에 폴더 구조를 정리한다. 모든 작업이 일관된 구조에서 진행되어야 후속 작업이 매끄럽다.

권장 구조는 다음과 같다.

`raw/` 폴더는 원본 raw 데이터를 보관한다. 이 폴더는 절대 수정하지 않는다. 어떤 처리도 하지 않은 원본 그대로 유지한다. 본인이 가지고 있는 `mortality_kostat/`, `kosis_population/`, `comtrade_korea_china/`, `comtrade_china_world/`, `comtrade_adh_china/`, `ecos_macro/`, `ecos_delinquency/`, `industry_census/`, `research_supp/`, `research_materials/` 등을 모두 이 raw 폴더 아래에 그대로 둔다.

`processed/` 폴더는 raw 데이터를 처리한 중간 산출물을 보관한다. 각 raw 데이터 source별로 하위 폴더를 만든다. 예를 들어 `processed/mortality/`, `processed/population/`, `processed/comtrade/`, `processed/industry_census/`, `processed/family_structure/` 등으로 분리한다.

`crosswalks/` 폴더는 작업 중 만드는 매핑 자료를 보관한다. 시군구 crosswalk, KSIC 분류 변환, KSIC-HS6 매핑, 사인 분류 매핑 등이다.

`panel/` 폴더는 최종 master panel을 보관한다. Reduced form 분석용 시군구 × 연도 panel, 매개 분석용 panel, demographic 분석용 시군구 × 연도 × 성 × 연령 panel 등 분석 용도별로 panel 파일을 만든다.

`code/` 폴더는 작업 코드를 보관한다. 각 단계별로 스크립트를 분리한다. `01_mortality_panel.py`, `02_population_panel.py`, `03_industry_shares.py`, `04_comtrade_shocks.py`, `05_bartik_iv.py`, `06_family_mediators.py`, `07_master_merge.py` 같은 식으로 numbering한다.

`logs/` 폴더는 각 단계의 실행 결과 로그를 보관한다. 어떤 처리가 어떤 시점에 진행됐는지, 어떤 결정을 했는지 기록한다.

`docs/` 폴더는 panel 구축 관련 문서를 보관한다. 본 작업 문서, 변수 정의 사전, 결정 사항 로그 등이다.

이 구조는 paper의 replication package 표준에도 부합한다. SSCI 저널 submission 시 reviewer가 reproducibility를 확인할 수 있는 구조로 정리되어 있어야 한다.

### 1.2 파일 명명 규칙

파일 명명은 다음 규칙을 따른다.

소스별 처리 산출물은 `{source}_{description}_{version}.csv` 형식으로 명명한다. 예를 들어 사망 panel의 첫 버전은 `mortality_panel_v01.csv`로 저장한다. 버전을 명시하면 작업 중 수정 사항을 추적할 수 있다.

연도별 raw 파일을 결합한 산출물은 `{source}_{start_year}_{end_year}.csv` 형식으로 명명한다. 예를 들어 27년치 사망 microdata를 결합한 파일은 `mortality_microdata_1997_2023.csv`로 저장한다.

최종 master panel은 `master_panel_{level}_{date}.csv` 형식으로 명명한다. 예를 들어 시군구 × 연도 panel은 `master_panel_sigungu_year_20260601.csv`로 저장한다. 날짜를 포함하면 panel 업데이트 추적이 쉽다.

모든 파일은 UTF-8 인코딩으로 저장한다. cp949로 받은 raw 데이터는 처리 단계에서 UTF-8로 변환해서 저장한다.

---

## 2. Stage 1: 시군구 Crosswalk 구축

### 2.1 작업 목적

시군구 crosswalk은 분석 기간(1997-2023) 동안 변경된 시군구 행정구역을 일관된 baseline으로 매핑하는 매핑표다. 이 작업이 panel 구축의 가장 first 단계다. 모든 후속 panel(사망, 인구, 산업, 매개변수)이 일관된 시군구 코드로 정리되어야 한다.

### 2.2 시군구 변경 사례

분석 기간 동안 발생한 주요 시군구 변경 사례를 정리한다.

2010년 7월 마산시, 창원시, 진해시가 통합 창원시로 합쳐졌다. 2014년 7월 청주시와 청원군이 통합 청주시로 합쳐졌다. 2014년 7월 여주군이 여주시로 승격되었다. 2003년 김포군이 김포시로 승격되었다. 그 외에도 시군구 명칭 변경, 읍면동 통합 등 작은 변경이 다수 있다.

KOSTAT는 매년 시군구 행정구역 변경 사항을 발표하는데, 통계청 사이트에서 행정구역 변천사 자료를 받을 수 있다. 이를 기반으로 일관된 crosswalk을 만든다.

### 2.3 작업 단계

먼저 baseline을 결정한다. 본 paper는 2021년 KOSTAT 행정구역 기준 256개 시군구를 baseline으로 한다. 2021년이 적합한 이유는 분석 기간(1997-2023)의 중후반에 위치해서 통합과 분리의 영향이 안정화된 시점이기 때문이다.

다음으로 crosswalk 매핑표를 만든다. 매핑표는 두 컬럼으로 구성된다. 첫 컬럼은 historical_sigungu_code(연도별 시군구 코드)다. 둘째 컬럼은 baseline_sigungu_code(2021년 baseline에서의 시군구 코드)다. 한 historical 시군구가 baseline의 한 시군구로 매핑되거나, 통합된 경우 여러 historical 시군구가 한 baseline 시군구로 매핑된다.

특수 케이스를 처리한다. 통합 사례(마산-창원-진해 → 통합 창원시)는 historical 코드 세 개가 baseline 코드 한 개로 매핑되도록 한다. 분리 사례는 더 까다로운데, 시군구 분리 후 인구 분포에 따라 가중 평균하거나 분리 이전 시점에서 통합된 단위로 처리한다. 본 paper의 분석 기간에는 큰 분리 사례가 없으므로 간단히 처리할 수 있다.

매핑 검증을 한다. Crosswalk 매핑 후 baseline 코드별 historical 코드의 합계가 통계청 발표 인구와 일치하는지 확인한다. 불일치가 있으면 매핑을 수정한다.

### 2.4 결과 산출물

`crosswalks/sigungu_crosswalk.csv` 파일에 매핑표를 저장한다. 컬럼은 year, historical_sido_code, historical_sigungu_code, baseline_sigungu_code다. 분석 기간 1997-2023년 모든 연도에 대해 historical 코드를 baseline 코드로 매핑한다.

문서로 매핑 결정의 정당화를 정리한다. `docs/sigungu_crosswalk_documentation.md`에 baseline 선택 이유, 통합/분리 사례 처리 방법, 인구 검증 결과를 기록한다.

### 2.5 시간 추정

이 단계에 약 1주일이 소요된다. 시군구 변경 사례 조사에 2-3일, 매핑표 작성에 2-3일, 검증과 문서화에 1-2일이다. KOSTAT 자료 수집과 매핑 작성이 가장 시간이 든다.

---

## 3. Stage 2: 사망 Panel 구축

### 3.1 작업 목적

KOSTAT 사망 microdata 27개 CSV(1997-2023)를 결합하고, baseline 시군구로 매핑하고, outcome group별 사망률을 계산해서 panel을 만든다.

### 3.2 작업 단계

먼저 raw CSV 파일을 결합한다. `mortality_kostat/사망사료 정리/` 폴더의 27개 파일을 cp949 인코딩으로 읽어서 하나의 dataframe으로 결합한다. Python에서 pandas로 처리하면 된다. 각 파일을 읽을 때 인코딩 오류가 발생할 수 있으므로 errors='replace' 옵션을 사용한다.

다음으로 컬럼명을 표준화한다. 27개 파일의 컬럼명이 시기에 따라 다를 수 있다. KOSTAT 파일설계서(가지고 있는 `(수정_보건복지) 파일설계서_..._B형.xlsx`)를 참고해서 일관된 영문 컬럼명으로 변환한다. 예를 들어 사망자주소행정구역시도코드는 sido_code, 사망자주소행정구역시군구코드는 sigungu_code, 사망원인_104항목분류코드는 cause_104로 변환한다.

다음으로 시군구 코드를 baseline으로 매핑한다. Stage 1에서 만든 crosswalk을 사용해서 각 record의 historical sigungu code를 baseline sigungu code로 변환한다. 매핑 실패한 record(예: 외국 거주자, 미상)는 별도로 처리한다.

다음으로 outcome group을 정의한다. cause_104 코드를 5개 outcome group으로 매핑한다. 절망사는 코드 102, 101, 057, 081의 합이다. 심혈관계는 067-070, 암은 027-048, 호흡기는 073-078, 외인사 기타는 097-104에서 102를 제외한다. 각 record에 outcome group dummy 5개를 추가한다.

다음으로 사망률을 계산한다. 시군구 × 연도 × 성 × 5세 연령 × outcome group으로 groupby해서 사망자 수를 합산한다. 그 다음 Stage 3에서 만든 인구 panel과 merge해서 인구 분모를 가져온다. 사망률은 사망자 수를 인구로 나눠서 인구 10만명당으로 표현한다.

다음으로 연령 표준화 사망률을 계산한다. 2000년 한국 인구를 표준 인구로 사용해서 직접 표준화 방법으로 연령보정 사망률을 계산한다. 표준화는 시군구 × 연도 × 성 × outcome group 단위로 수행한다.

다음으로 로그 변환을 적용한다. ln(rate + 1)로 변환한 변수를 추가한다. +1 smoothing은 0 사망 cell을 처리하기 위한 것이다.

### 3.3 결측치 처리

작은 시군구의 0 사망 cell은 별도로 표시한다. 0 사망 cell의 비율을 시군구별, outcome group별로 계산해서 robustness 분석 시 참고한다.

매핑 실패 record는 별도 dataframe으로 보관한다. 분석에서 제외하지만 데이터 quality 평가에 사용한다.

### 3.4 결과 산출물

`processed/mortality/mortality_panel_v01.csv` 파일에 사망 panel을 저장한다. 컬럼은 baseline_sigungu_code, year, sex, age_group, outcome_group, deaths, population, mortality_rate, age_adjusted_rate, log_rate다.

`logs/mortality_panel_log.txt`에 처리 과정의 로그를 기록한다. 각 연도별 record 수, 매핑 실패 비율, 0 cell 비율 등이다.

### 3.5 시간 추정

이 단계에 약 1주일이 소요된다. CSV 결합과 컬럼 표준화에 2일, 시군구 매핑에 1-2일, outcome group 정의와 사망률 계산에 2-3일이다. 검증과 디버깅에 추가 시간이 든다.

---

## 4. Stage 3: 인구 Panel 구축

### 4.1 작업 목적

KOSIS 인구 panel을 baseline 시군구로 매핑하고 사망률 계산의 분모로 사용할 panel을 만든다.

### 4.2 작업 단계

`kosis_population/population_combined.csv`를 읽는다. 이미 시군구 × 성 × 5세 연령 × 연도 panel로 정리되어 있다.

시군구 코드를 baseline으로 매핑한다. KOSIS 인구 panel의 C1 코드는 5자리 시군구 코드다. Stage 1 crosswalk으로 baseline 코드로 변환한다.

성과 연령 코드를 표준화한다. 성별 코드 0(계), 1(남), 2(여)와 5세 연령 bin 코드를 일관된 형식으로 변환한다. Outcome panel의 성별, 연령 분류와 일치시킨다.

연령 그룹을 만든다. Paper 분석에서 사용할 연령 그룹(working-age 25-54, 청년 15-24, 장년 55-64, 노년 65+)으로 5세 bin을 재분류한다.

### 4.3 결과 산출물

`processed/population/population_panel_v01.csv` 파일에 인구 panel을 저장한다. 컬럼은 baseline_sigungu_code, year, sex, age_5yr, age_group, population이다.

### 4.4 시간 추정

이 단계는 약 2-3일 소요된다. KOSIS 인구 데이터가 이미 정리된 형태라 작업이 비교적 간단하다.

---

## 5. Stage 4: 산업 Census와 Baseline Shares 구축

### 5.1 작업 목적

1997년 산업 census로 시군구별 KSIC 산업 비중을 계산한다. 이는 Bartik IV의 baseline shares가 된다.

### 5.2 작업 단계

먼저 1997년 산업 census 파일을 읽는다. `industry_census/1997_연간자료_*.csv` 파일을 cp949 인코딩으로 읽는다. 파일 크기가 195MB로 크니 chunk 단위로 처리한다.

KSIC 산업 분류를 표준화한다. 1997년 데이터는 KSIC 8차 분류를 사용한다. 가지고 있는 KSIC crosswalk(`research_supp/ksic_crosswalk_8_to_9.csv`, `9_to_10.csv`, `10_to_11.csv`)를 단계적으로 적용해서 일관된 KSIC 11차 2자리 분류로 변환한다.

시군구별 산업 비중을 계산한다. 시군구 c × 산업 j 종사자 수를 시군구 c 전체 종사자 수로 나눠서 비중 $s_{cj,1997}$을 계산한다. 비제조업 산업도 포함하지만 무역 충격에는 0으로 처리한다.

Robustness용 추가 baseline shares를 만든다. 1990년과 2000년 산업 census로도 같은 절차로 baseline shares를 계산해서 robustness 분석에 활용한다.

### 5.3 결과 산출물

`processed/industry_census/baseline_shares_1997.csv`에 1997년 baseline shares를 저장한다. 컬럼은 baseline_sigungu_code, ksic_2digit, share, employment, total_employment다.

`processed/industry_census/baseline_shares_1990.csv`와 `baseline_shares_2000.csv`도 robustness용으로 저장한다.

### 5.4 시간 추정

이 단계에 약 1-2주일이 소요된다. 1997년 census 파일 처리에 3-4일, KSIC 변환에 3-4일, 검증에 2-3일이다. KSIC 변환이 까다로워서 시간이 든다.

---

## 6. Stage 5: Comtrade 데이터와 무역 충격 계산

### 6.1 작업 목적

Comtrade 데이터에서 산업별 무역 충격 $g_{j,t}$를 계산한다.

### 6.2 KSIC-HS6 매핑

먼저 KSIC와 HS6의 매핑을 만든다. 가지고 있는 자료에는 KSIC-ISIC4 연계표, CPC21-HS2012, CPC21-ISIC4 변환표가 있다. 직접 매핑이 없으므로 단계적으로 변환한다.

매핑 단계는 KSIC 2자리 → ISIC4 2자리 → CPC21 → HS2012 → HS6이다. 각 단계에서 일대다 또는 다대일 매핑이 발생할 수 있으므로 가중치 처리가 필요하다.

대안으로 통계청 또는 UN Statistics Division 사이트에서 KSIC-HS 직접 매핑이 공개된 자료가 있는지 추가 확인한다. 직접 매핑이 있으면 단계적 변환의 정보 손실을 피할 수 있다.

### 6.3 KR-CN Bilateral 무역 충격 계산

`comtrade_korea_china/` 폴더의 50개 CSV(2000-2024)를 결합한다. 각 파일은 한국과 중국 간 양자 무역(수출과 수입)을 HS6 product 단위로 기록한다.

flowCode 컬럼으로 수출(X)과 수입(M)을 분리한다. 각 HS6 product × 연도별로 수출액과 수입액을 정리한다.

HS6를 KSIC2로 매핑해서 산업별 무역 합계를 계산한다. 산업 j × 연도 t의 한국 → 중국 수출액 $X_{j,t}$, 중국 → 한국 수출액(한국 입장에서 수입) $M_{j,t}$를 계산한다.

Net export를 계산한다. $\text{NetExport}_{j,t} = X_{j,t} - M_{j,t}$다.

무역 충격을 계산한다. 1997년 또는 5년 전 대비 변화로 측정한다. $g_{j,t} = \Delta \ln(\text{NetExport}_{j,t})$다. Net export가 음수인 경우 부호와 절댓값을 따로 처리한다(예: signed log transformation).

### 6.4 ADH 8국 무역 충격 계산 (Robustness)

`comtrade_adh_china/` 폴더에서 8개국(호주, 스위스, 독일, 덴마크, 스페인, 핀란드, 일본, 뉴질랜드)의 대중국 수입을 처리한다.

8국의 산업별 대중국 수입을 합산해서 ADH 8국 대중국 수입 $M^{ADH}_{j,t}$를 계산한다.

스페인과 독일의 누락 연도는 명시적으로 다룬다. 스페인은 2004년 이후 거의 전체가 누락이고, 독일은 2019, 2021-2024년 누락이다. 두 가지 처리 방법이 있다. 하나는 누락 국가를 빼고 6국 또는 7국 IV로 가는 것이다. 다른 하나는 interpolation으로 누락치를 메우는 것이다. 본 paper는 첫째 방법을 main으로 하고 둘째 방법을 robustness로 사용한다.

### 6.5 결과 산출물

`processed/comtrade/krcn_shocks.csv`에 KR-CN bilateral 무역 충격을 저장한다. 컬럼은 ksic_2digit, year, exports, imports, net_export, log_change_net_export다.

`processed/comtrade/adh_shocks.csv`에 ADH 8국 무역 충격을 저장한다. 컬럼은 ksic_2digit, year, total_imports, log_change_imports다.

### 6.6 시간 추정

이 단계에 약 1-2주일이 소요된다. KSIC-HS6 매핑이 가장 시간이 많이 든다. KR-CN과 ADH 데이터 처리에 각 3-4일이다.

---

## 7. Stage 6: Bartik IV 계산

### 7.1 작업 목적

Stage 4에서 만든 baseline shares와 Stage 5에서 만든 무역 충격을 결합해서 시군구 × 연도 Bartik IV를 계산한다.

### 7.2 작업 단계

먼저 baseline shares panel과 무역 충격 panel을 산업 코드로 결합한다. 각 시군구 c × 연도 t × 산업 j cell에서 비중 $s_{cj,1997}$과 충격 $g_{j,t}$를 만난다.

시군구 c × 연도 t의 Bartik IV를 계산한다. 산업 j에 대해 비중과 충격의 곱을 합산한다.

$$\text{Bartik}_{c,t} = \sum_{j} s_{cj,1997} \cdot g_{j,t}$$

KR-CN main IV와 ADH robustness IV를 따로 계산한다.

5-year stacked first-difference를 위해 5년 period 구분을 만든다. 1997-2002, 2002-2007, 2007-2012, 2012-2017, 2017-2022의 5개 period다. 각 period의 시작과 끝 시점의 Bartik IV 차이를 계산한다.

### 7.3 결과 산출물

`processed/bartik/bartik_iv_annual.csv`에 연간 Bartik IV를 저장한다. 컬럼은 baseline_sigungu_code, year, bartik_krcn, bartik_adh다.

`processed/bartik/bartik_iv_5year.csv`에 5년 stacked Bartik IV를 저장한다. 컬럼은 baseline_sigungu_code, period, delta_bartik_krcn, delta_bartik_adh다.

### 7.4 시간 추정

이 단계에 약 3-5일이 소요된다. Stage 4와 5의 결과가 정리되어 있으면 결합 작업은 비교적 간단하다.

---

## 8. Stage 7: 가족 구조 매개변수 Panel 구축

### 8.1 작업 목적

가지고 있는 가족 구조 데이터를 시군구 × 연도 panel로 정리하고 추가로 KOSIS 인구주택총조사 데이터를 받는다.

### 8.2 작업 단계

먼저 시군구 출생, 혼인, 이혼 데이터를 처리한다. `research_supp/시군구 출생아.xls`, `시군구 혼인.xls`, `시군구 이혼.xls` 파일을 pandas로 읽는다. 각 파일은 시군구 × 연도 panel 형태로 정리되어 있다.

시군구 코드를 baseline으로 매핑한다. 인구 panel과 merge해서 인구 1000명당 비율을 계산한다. 결혼율 = 혼인 건수 / 인구 × 1000, 이혼율 = 이혼 건수 / 인구 × 1000, 출생률 = 출생아 수 / 인구 × 1000이다.

합계출산율을 처리한다. `시군구_출생아수__합계출산율_20260419183410.xlsx` 파일을 읽어서 시군구 × 연도 합계출산율 panel로 정리한다.

KOSIS 인구주택총조사 1인가구 비율을 추가 다운로드한다. KOSIS 사이트(kosis.kr)에서 인구주택총조사의 시군구 단위 결과를 받는다. 5년 간격(1995, 2000, 2005, 2010, 2015, 2020) 데이터다. 시군구 단위 1인가구 수와 전체 가구 수를 받아서 1인가구 비율을 계산한다.

5년 간격 데이터를 연간 panel로 변환한다. Linear interpolation으로 사이 연도의 값을 추정한다. 추정값임을 명시하기 위해 boolean 컬럼 imputed를 추가한다.

### 8.3 결과 산출물

`processed/family_structure/family_panel_v01.csv`에 가족 구조 panel을 저장한다. 컬럼은 baseline_sigungu_code, year, marriage_rate, divorce_rate, birth_rate, tfr, single_household_rate, single_household_imputed다.

### 8.4 시간 추정

이 단계에 약 1주일이 소요된다. 시군구 출생/혼인/이혼 처리에 2-3일, 인구주택총조사 추가 다운로드와 처리에 2-3일, interpolation과 검증에 1-2일이다.

---

## 9. Stage 8: 보조 매개변수와 통제변수 Panel 구축

### 9.1 작업 목적

노동시장, 가구 부채, 의료 인프라 보조 매개변수와 통제변수 panel을 구축한다.

### 9.2 노동시장 Panel

KOSIS에서 시군구 단위 실업률, 고용률, 경제활동참가율 데이터를 추가 다운로드한다. 학부생도 KOSIS 회원가입으로 받을 수 있다.

시군구 단위 통계는 2008년 이후만 안정적이므로 2008-2023년 panel만 만든다. baseline 시군구로 매핑해서 panel을 정리한다.

`processed/labor_market/labor_panel_v01.csv`에 저장한다. 컬럼은 baseline_sigungu_code, year, unemployment_rate, employment_rate, participation_rate다.

### 9.3 가구 부채 Panel

`ecos_delinquency/` 폴더의 5개 series를 처리한다. ECOS 데이터는 시도 단위(16개)이므로 시군구 panel이 아니라 시도 panel로 정리한다.

각 시군구를 시도로 매핑해서 시도 panel을 만든다. baseline_sigungu_code의 첫 2자리가 시도 코드다.

`processed/household_debt/debt_panel_v01.csv`에 저장한다. 컬럼은 sido_code, year, household_loan, delinquency_rate, household_loan_purpose다.

이 데이터는 시군구 분석에 직접 쓰지 못하는 한계를 명시적으로 인정한다.

### 9.4 의료 인프라 Panel

`research_supp/kosis_hira_quarterly_2009_2025.csv` 파일을 처리한다. 분기 단위 panel이므로 연간으로 aggregate한다(연 평균 또는 연말 값).

시군구별 인구 1000명당 의사 수를 계산한다. 16종 의료인력 중 의사, 정신과 관련 인력(레지던트, 전문의 등)을 분리해서 보관한다.

`processed/healthcare/hira_panel_v01.csv`에 저장한다. 컬럼은 baseline_sigungu_code, year, doctors_per_1k, total_medical_staff, mental_health_staff다.

2009년 이전은 결측치 처리한다.

### 9.5 ECOS Macro 통제변수

`ecos_macro/` 폴더의 11개 series를 처리한다. 대부분 시간 변수(연간 또는 월간)이므로 연도 단위로 정리한다.

월간 시리즈는 연 평균 또는 연말 값으로 aggregate한다. 본 paper의 통제변수로 사용하는 시리즈는 901Y009 CPI(실질값 변환용), 731Y004 환율, 722Y001 기준금리, 161Y006 M2다.

`processed/macro_controls/macro_panel_v01.csv`에 저장한다. 컬럼은 year, cpi, exchange_rate_usd, base_rate, m2다.

### 9.6 GRDP Panel (추가 다운로드)

KOSIS에서 시군구 GRDP를 추가 다운로드한다. 1985년 이후 시군구 panel이 가용하다.

`processed/grdp/grdp_panel_v01.csv`에 저장한다. 컬럼은 baseline_sigungu_code, year, grdp, log_grdp_per_capita다.

### 9.7 시간 추정

이 단계 전체에 약 1-2주일이 소요된다. 각 source별 처리에 2-3일, 추가 다운로드에 1-2일이다.

---

## 10. Stage 9: Master Panel Merge

### 10.1 작업 목적

지금까지 만든 모든 panel을 baseline_sigungu_code와 year 키로 결합해서 분석용 master panel을 만든다.

### 10.2 작업 단계

먼저 기본 panel skeleton을 만든다. 256 시군구 × 27년의 모든 cell이 들어있는 base dataframe을 만든다. cell 수는 6,912다.

차례대로 다음 panel들을 left merge한다. mortality_panel(시군구 × 연도 × 성 × 연령 × outcome group), bartik_iv_annual, family_panel, labor_panel(2008년 이후), debt_panel(시도 단위로 broadcast), hira_panel(2009년 이후), macro_panel(year 키로만), grdp_panel.

Sex와 age를 group한 시군구 × 연도 panel을 별도로 만든다. Reduced form 분석에는 시군구 × 연도 단위로 집계한 panel이 필요하다.

5-year stacked first-difference를 위해 시군구 × period panel을 만든다. 5개 period(1997-2002, 2002-2007 등)별로 시작과 끝 시점의 변수 차이를 계산한다.

### 10.3 결측치 처리

merge 후 결측치 패턴을 분석한다. 어떤 변수가 어떤 시점에 결측치가 많은지 정리한다. 노동시장 변수는 2008년 이전 결측, HIRA는 2009년 이전 결측, 가구 부채는 2008년 이전 결측이다.

분석 시 결측치가 있는 cell을 제외할지, imputation할지를 변수별로 결정한다. Main specification은 1997-2023년 full sample이지만, 보조 매개변수 분석은 데이터가 가용한 시기로 제한한다.

### 10.4 결과 산출물

`panel/master_panel_sigungu_year_v01.csv`에 시군구 × 연도 master panel을 저장한다. 모든 변수가 들어있다.

`panel/master_panel_5year_stacked_v01.csv`에 5-year stacked panel을 저장한다.

`panel/master_panel_demographic_v01.csv`에 시군구 × 연도 × 성 × 연령 panel을 저장한다. Heterogeneity 분석용이다.

### 10.5 시간 추정

이 단계에 약 3-5일이 소요된다. Merge 자체는 빠르지만 결측치 처리와 검증이 시간이 든다.

---

## 11. Stage 10: 검증과 Descriptive Statistics

### 11.1 작업 목적

Master panel의 quality를 검증하고 paper의 Section 3에 들어갈 descriptive statistics를 계산한다.

### 11.2 작업 단계

먼저 panel structure를 검증한다. 모든 시군구가 모든 연도에 cell을 가지는지, missing cell의 패턴이 합리적인지 확인한다.

각 변수의 분포를 확인한다. 평균, 표준편차, 최소, 최대를 시군구 × 연도 단위로 계산한다. 이상치(outlier)를 확인하고 데이터 입력 오류 가능성을 검토한다.

Trade shock과 mortality, family structure 변수의 시간 추세를 그래프로 그린다. 한국 평균값의 변화 패턴이 직관과 일치하는지 확인한다.

Cross-sectional variation을 확인한다. 시군구별 baseline 산업 비중의 분포, NTR Gap 분포, Bartik IV 분포를 본다.

### 11.3 Descriptive Statistics 표 만들기

Paper Section 3에 들어갈 표를 만든다.

Table 1은 데이터 출처와 분석 기간 정리다. 각 변수의 source, period, unit, observations를 표로 보여준다.

Table 2는 핵심 변수의 descriptive statistics다. 1997, 2010, 2020 세 시점의 시군구 단위 평균, 표준편차, 최소, 최대를 보여준다. 변수는 절망사 사망률, 결혼율, 이혼율, 출생률, 합계출산율, 1인가구 비율, KR-CN 무역 충격, 1997 baseline shares 분포 등이다.

Table 3은 outcome group의 KOSTAT 코드 매핑이다. 각 outcome group이 포함하는 사인 코드를 명시한다.

### 11.4 결과 산출물

`docs/descriptive_statistics_tables.md`에 세 개 표를 저장한다.

`docs/data_quality_report.md`에 검증 결과 보고서를 저장한다.

### 11.5 시간 추정

이 단계에 약 1주일이 소요된다. 검증과 표 작성에 시간이 든다.

---

## 12. 전체 작업 시간 종합

전체 panel 구축에 약 4-6주가 소요된다.

Stage 1 시군구 crosswalk이 1주일.
Stage 2 사망 panel이 1주일.
Stage 3 인구 panel이 2-3일.
Stage 4 산업 census와 baseline shares가 1-2주일.
Stage 5 Comtrade와 무역 충격이 1-2주일.
Stage 6 Bartik IV 계산이 3-5일.
Stage 7 가족 구조 매개변수 panel이 1주일.
Stage 8 보조 매개변수와 통제변수 panel이 1-2주일.
Stage 9 master panel merge가 3-5일.
Stage 10 검증과 descriptive statistics가 1주일.

본 paper의 6개월 timeline에서 첫 1.5-2개월이 panel 구축에 할당된다. 이 시간 안에 panel이 완성되지 않으면 분석 단계가 밀린다. 만약 일정이 빠듯해지면 보조 매개변수 panel(Stage 8)을 robustness 단계로 미루고, 가족 구조 매개변수와 reduced form 분석에 우선 집중한다.

---

## 13. 주요 결정 사항 로그

작업 중 결정한 사항을 다음 로그에 기록한다. Reproducibility와 future revision을 위해 필요하다.

baseline 시군구는 2021년 KOSTAT 기준 256개로 결정.

KSIC 분류는 11차 2자리(약 24개 제조업)로 결정.

Bartik IV main shifter는 KR-CN bilateral net export, robustness는 ADH 8국(스페인 제외 7국).

매개변수는 결혼율, 이혼율, 출생률, 합계출산율, 1인가구 비율 5개.

분석 기간은 1997-2023년, 5-year stacked period는 5개.

로그 변환은 ln(rate + 1) smoothing.

연령 표준화 사망률의 표준 인구는 2000년 한국 인구.

NHIS 데이터는 접근 불가로 paper limitation으로 명시.

---

## 14. 다음 단계

Panel 구축이 완료되면 다음 단계는 회귀 분석이다. 이는 별도의 작업 문서로 정리한다. 다음에 작성할 문서는 다음과 같다.

회귀 분석 작업 문서. Reduced form 회귀, 매개 분석, 식별 진단(Rotemberg HHI, share-covariate balance, pre-trend, AKM SE)의 step-by-step 절차를 정리한다. Python(linearmodels 라이브러리)과 R(ssaggregate 패키지)의 사용법을 포함한다.

다음 단계의 paper section 작성 가이드. Section 4(Identification Strategy), Section 5(Reduced Form), Section 6(Mediation Analysis)의 작성 가이드를 차례로 만든다.

이 문서들이 모이면 raw 데이터에서 paper submission까지의 전체 작업 매뉴얼이 완성된다.

---

**END OF PANEL CONSTRUCTION WORKING DOCUMENT v1.0**
