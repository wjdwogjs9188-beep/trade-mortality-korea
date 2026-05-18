# 데이터 수집 Protocol — PAP v3.2 spec 요구사항 기반 (2026-05-03)

**작성**: Claude (R-A) 분석 + 정재헌 사용자 PC 다운로드 protocol
**목적**: PAP v3.2 의 모든 spec 결정에 필요한 데이터의 specific source + 메뉴 path + 다운로드 protocol
**우선순위**: Tier A (Stage 5 시작 전 필수) > Tier B (병행 가능) > Tier C (paper draft 단계)

---

## Tier A — Critical (Stage 5 시작 전 필수)

### A.1 의료 인프라 데이터 ⭐ Spec-level

**필요 이유**: PAP v3.2 § 5.1 H1.3 의 naive vs **controlled** spec 비교 — manufacturing region = better medical infrastructure → faster B-hep treatment → liver mortality decline 의 alternative explanation 차단. § 4.4 #3 share-covariate balance test 에 의료 인프라 변수 명시 포함.

#### A.1.1 시군구 의료기관 수 (종별)

**Source**: KOSIS 또는 HIRA 보건의료빅데이터

**KOSIS path** (1차 시도):
```
https://kosis.kr → 검색창 "의료기관"
→ 주제별통계 → 보건·복지 → 보건의료자원
→ 표 후보:
   - DT_YB1201 "의료기관" (orgId=711)
   - DT_11001N_2013_A042 "의료기관 및 병상수" (orgId=110, 보건복지부)
```

**확인 항목** (R-A protocol § 7.3 specific quote):
- 시군구 단위 panel 가용 여부 (시도만이면 fallback 필요)
- 시계열 시작 연도 (1995-1999 baseline 가용성)
- 종별 분리 (종합병원·병원·의원·요양병원 etc.)

**HIRA path** (2차 시도, KOSIS 가용 안 시):
```
https://opendata.hira.or.kr → 의료자원 통계
→ "지역별 요양기관 현황"
→ 시군구 × 종별 다운로드
```

**예상 가용성**: 2008년 이후 시군구 panel 완전. **1995-1999 baseline 은 광역시도 단위 down-aggregate fallback 필요 가능성 큼**.

**Fallback**: 1995-1999 baseline 광역시도 단위만 가용 시 → § 4 controls 의 의료 인프라 baseline 을 광역시도 fixed effect 로 처리 + 2000-2023 panel 만 시군구 단위 control.

#### A.1.2 KCDC B형간염 vaccination 시군구 panel

**Source**: KCDC 질병관리청 예방접종통계 또는 KDCA 감염병관리과

**경로**:
```
https://www.kdca.go.kr → 정책정보 → 감염병관리 → 예방접종
→ "예방접종등록정보" 또는 "예방접종 현황 통계"
또는
KOSIS → 검색창 "B형간염 예방접종"
```

**확인 항목**:
- 시군구 panel 가용 여부 (**부재 가능성 매우 큼**)
- 시계열 시작 연도 (1995년 국가 접종 시작)
- 0세·1세·청소년 등 연령별 접종률

**예상 가용성**: **시군구 panel 가능성 낮음**. 광역시도 단위 fallback 또는 NHIS 일반건강검진 (B형간염 보유율) 광역시도 panel 사용.

**Fallback (정확)**:
1. NHIS 국민건강보험공단 일반건강검진 결과 → 광역시도 별 B형간염 보유율 panel
2. 또는 의료기관 수 (A.1.1) 에 흡수시키고 vaccination 별도 control 제외

#### A.1.3 HIRA 항바이러스제 처방률

**Source**: HIRA 의약품 처방 통계 ATC J05A (항바이러스제, 2000년대 도입)

**경로**:
```
https://opendata.hira.or.kr → 의약품통계 → 진료비통계
→ ATC 코드별 시군구 처방 통계
또는
HIRA "처방 의약품 사용량" 통계
```

**확인 항목**:
- ATC4 J05A (항바이러스제 직접) 또는 J05AB / J05AF (인터페론, nucleoside analogue) 분리
- 시군구 panel 가용 여부
- 시계열 시작 연도 (2000년대 도입 → 2002 또는 2005 시작 가능)

**가용성**: HIRA 가 ATC4 시군구 panel 일반적으로 가용 (이전 가이드 K9 의 "지역별 진료 정보" 와 통합).

**Fallback**: 시군구 panel 부재 시 광역시도 down-aggregate.

#### A.1.4 추가 의료 인프라 변수 (선택)

- **HIRA 의료급여 진료 통계** ICD F10 (알코올 사용장애), F20-F29, F32-F33: 이전 KOSIS_collection_guide.md K9 에 명시. 가족 mediator + drug/psych mortality mechanism 의 control.
- **인구 천명당 의사 수**: KOSIS DT_1YL20981 (시도/시·군·구).

---

### A.2 외국인 비율 시군구 panel ⭐ Spec-level

**필요 이유**: PAP v3.2 § 4.5 measurement error robustness — 외국인 비율 시군구 heterogeneity × manufacturing 비중 상관 → measurement error × treatment 상관 차단. § 5.4 외국인 비율 high vs low group separate estimation.

**Source**: KOSIS 외국인등록인구

**경로**:
```
https://kosis.kr → 검색창 "외국인등록인구"
→ 주제별통계 → 인구·가구 → 외국인등록인구통계
→ 표 후보:
   - 1B040A26 "행정구역별 외국인주민현황"
   - 또는 행정안전부 "지방자치단체 외국인주민 현황"
```

**확인 항목**:
- 시군구 panel 가용성 (보통 가용)
- 시계열 시작 연도 (한국 외국인 통계 1990년대 후반-2000년대 초)
- 국적별 분리 (전체 외국인 + 중국·일본·동남아 등)

**예상 가용성**: 시군구 panel 가용. 시계열 1995-1999 baseline 은 데이터 적을 가능성.

**Fallback**: 1995-1999 baseline 결측 시 2000년 baseline 으로 대체.

---

### A.3 시군구 × KSIC 4-digit 산업 비중 panel ⭐ Bartik IV core

**필요 이유**: PAP v3.2 § 4.2 Bartik shift-share IV 의 core 변수. baseline industry shares (1995-1999) × shift (KR-CN trade exposure) → Δ_trade.

**Source**: KOSIS 사업체조사 (전국사업체조사) 또는 통계청 인구주택총조사

**경로**:
```
https://kosis.kr → 검색창 "사업체조사"
→ 주제별통계 → 산업·기업 → 전국사업체조사
→ "시·군·구별 산업분류별 사업체수 및 종사자수"
```

**확인 항목**:
- 시군구 × KSIC 4-digit (~200 산업) 종사자 수 panel
- 시계열: 1994-1999 baseline + 2000-2023 panel
- 시군구 단위 가용성 (보통 가용)

**예상 가용성**: 사업체조사는 시군구 단위 KSIC 4-digit 가용. 시계열 1994 부터 시작 가능.

**KSIC version 주의**:
- 1994-2007: KSIC 8차 개정
- 2008-2017: KSIC 9차 개정
- 2017+: KSIC 10차 개정 (현재)
- **시계열 통일을 위해 KSIC version concordance 필요** (KOSIS 가 자동 통일 또는 별도 처리)

**Fallback**: KSIC 4-digit 부재 시 KSIC 2-digit 또는 KSIC 3-digit 사용 (PAP § 12 down-aggregate option).

---

### A.4 KSIC-HS6 Concordance ⭐ Bartik IV core

**필요 이유**: PAP v3.2 § 4.2 — 시군구 산업 비중 (KSIC) × 무역 변화 (HS6) 결합용.

**현재 상태**:
- ✅ `hs6_to_ksic5_crosswalk.csv` (research_handoff_complete) 이미 존재 — **KSIC 5-digit** version
- ⚠️ PAP v3.2 commit = **KSIC 4-digit**
- 차이: KSIC5 → KSIC4 down-aggregate 가능 (앞 4자리 추출). 정보 손실 minimal.

**Source 검토**:

#### A.4.1 통계청 직접 매핑 응답

**경로**: 통계청 통계 표준 분류 담당 부서 또는 KOSIS 고객지원
**대기**: 1-2 주
**예상**: KSIC 4-digit 또는 5-digit level 매핑

#### A.4.2 한국은행 IO 380 fallback

**Source**: 한국은행 산업연관표 (Input-Output Table)

**경로**:
```
https://www.bok.or.kr → 통계 → 산업연관표
→ "산업연관표 부속표" → "기본부문분류표 (380부문)"
```

**Mapping**:
- IO 380 → KSIC 4-digit aggregate (한국은행 자체 매핑 제공)
- HS6 → IO 380 (한국은행 무역 통계 연계)

#### A.4.3 ISIC4 bridge fallback

**Source**: UN Statistics Division concordance + KOSIS

**경로**:
- ISIC4 → KSIC concordance: KOSIS 통계 표준 분류
- HS6 → ISIC4 concordance: WITS 또는 UN Comtrade

**현실적 선택**: A.4 통계청 응답 + A.4.2 한국은행 IO 380 둘 다 준비. 응답 빠른 쪽 채택.

---

### A.5 가족 구조 5 Mediator Panel ⭐ Mediation analysis

**필요 이유**: PAP v3.2 § 5.2 DFH 2020 mediation analysis. 5 mediator (이혼·결혼·출산·한부모·동거).

#### A.5.1 이혼율 / 결혼율

**Source**: KOSIS 인구동향조사

**경로**:
```
https://kosis.kr → 검색창 "이혼" 또는 "혼인"
→ 인구·가구 → 인구동향조사
→ "시·군·구별 인구동향" → "혼인 건수", "이혼 건수"
```

**확인 항목**:
- 시군구 panel 가용
- 시계열 1997-2023
- 천명당 율 vs 절대 건수

**예상 가용성**: 가용 (이전 K7 가이드 명시).

#### A.5.2 합계출산율

**Source**: KOSIS 출생통계

**경로**:
```
https://kosis.kr → 검색창 "합계출산율"
→ 인구·가구 → 출생통계
→ "시·군·구별 합계출산율" 또는 "시·군·구별 모(母)의 연령별 출생아수"
```

**확인 항목**:
- 시군구 panel 가용
- 시계열 1997-2023

#### A.5.3 한부모 가구 비율

**Source**: KOSIS 인구주택총조사 (5년 주기)

**경로**:
```
https://kosis.kr → 검색창 "한부모"
→ 인구·가구 → 인구주택총조사
→ "시·군·구별 가구원수별 한부모 가구"
```

**제약**: **5년 주기** (1995, 2000, 2005, 2010, 2015, 2020) — 매년 panel 불가.

**현재 상태**: ✅ `welfare_panel_2012_2019_clean_wide.csv` 에 일부 있음 (한부모 변수).

**Fallback**: 5년 시점 데이터를 5년 stack 의 baseline 으로 사용. Annual interpolation 회피.

#### A.5.4 동거 비율

**Source**: KOSIS 인구주택총조사 (5년 주기)

**경로**:
```
KOSIS → 인구주택총조사
→ "시·군·구별 미혼 동거 가구" 또는 "혼인상태별 인구"
```

**제약**: 동거 통계가 명시적 panel 없을 가능성. 미혼 비혼 가구 + 혼인상태 indirect 측정.

**Fallback**: 동거 변수 정확 측정 어려움 → 5 mediator 중 동거 제외하고 4 mediator (이혼·결혼·출산·한부모) 만 사용.

---

## Tier B — Major (Stage 4-5 병행)

### B.1 시군구 1인당 GRDP / 평균임금 / 고용 panel

**Source**: KOSIS 지역소득 + 사업체조사

**경로**:
```
KOSIS → 국민계정·지역계정 → 지역소득
→ "시·군·구별 지역내총생산" (가용성 unclear)
또는
→ 시도별만 가용 시 → "시·도별 1인당 지역내총생산" + 시군구 sub-aggregation
```

**가용성 우려**: 시군구 단위 GRDP 는 일부 광역시도 자치구만 가용 가능성. 시 단위는 광역시도 share 로 추정.

### B.2 주택가격 / 자가비율 panel

**현재 상태**: ✅ `Housing_Price_Panel_apt_sale_Yearly.csv` + `Monthly.csv` 이미 존재.

**확장**: 자가비율은 인구주택총조사 5년 주기.

### B.3 1990-1994 baseline shares sensitivity

**Source**: KOSIS 사업체조사 (A.3 와 동일, 시기만 다름)

**제약**: 1990-1993 사업체조사 panel 가용성 unclear. 1995 이후 가능성 큼.

**Fallback**: Pre-IMF baseline 가용 안 되면 § 4.4 robustness 제외 + paper limitation 명시.

### B.4 고용 panel (2008-2019 unemployment)

**현재 상태**: 이전 KOSIS_collection_guide K6 명시. 사용자가 이미 수집했을 수 있음 → research_handoff_complete 에 데이터 있는지 추가 점검 필요.

---

## Tier C — Minor (Paper Draft 단계)

### C.1 65+ Subgroup 분석

**현재 상태**: ✅ `mortality_rate_panel_v01.parquet` 에 17 age band 있음. 80+ aggregate 외에 65-69, 70-74, 75-79, 80+ 별도 추출 가능. 추가 데이터 수집 불필요.

### C.2 Stata Package 설치

**필요 환경**: 가천대 Stata license 확인 + 7 package 설치:
- `boottest` (Cameron-Gelbach-Miller 2008 + Roodman 2019)
- `weakivtest` (Pflueger-Wang 2015)
- `ivmediate` (DFH 2020)
- `rwolf` (Romano-Wolf 2005)
- `reg_ss` (BHJ 2022, Borusyak github)
- `acreg` (Conley SE)
- `weakiv` (AR + tF inference)

**Source**:
- SSC archive: 1, 2, 3, 4, 6, 7 (Stata 명령어 `ssc install boottest` 등)
- Author website: 5 `reg_ss` (https://github.com/borusyak/shift-share)

**Fallback**: Stata license 제약 시 R / Python alternative implementation:
- R: `ivreg`, `lfe`, `boot.kbet`, `mediation`
- Python: `linearmodels.iv`, `econml.iv`, `statsmodels`

### C.3 영문 학술 검수

**Service options**:
- AJE (American Journal Experts): ~$300-500
- Editage: ~$400-600
- Enago: ~$300-500
- 가천대 글로벌센터 또는 영문 학술 글쓰기 program

**Timeline**: paper draft 완성 (2026-08) 후 1-2주 검수 (2026-09).

---

## 다운로드 Protocol

### 회원가입 / API 키

| Source | 회원가입 | API key | 저장 위치 |
|--------|:--:|:--:|------|
| KOSIS | ✅ 필요 (무료) | ✅ 가능 (`KOSIS_API_KEY` 이미 .env 존재) | `0_raw/kosis_*/` |
| HIRA | ✅ 필요 (무료) | API 별도 신청 | `0_raw/hira_*/` |
| KCDC | 일부 무료 공개 | API 별도 | `0_raw/kcdc_*/` |
| 한국은행 ECOS | ✅ 필요 (무료) | ✅ (`ECOS_API_KEY` 이미 .env 존재) | `0_raw/ecos_*/` |
| 통계청 (KSIC concordance) | 별도 요청 | 이메일 응답 | `0_raw/ksic_concordance/` |

### 폴더 구조 권장

```
0_raw/
├── hira_medical_institutions/         # A.1.1
├── kcdc_vaccination/                  # A.1.2
├── hira_atc_j05a/                     # A.1.3
├── kosis_foreign_residents/           # A.2
├── kosis_business_survey_ksic/        # A.3
├── ksic_hs6_concordance/              # A.4
│   ├── hs6_to_ksic5_crosswalk.csv  (이미 존재, 복사)
│   └── statkorea_response.csv       (응답 시)
├── kosis_family_mediators/            # A.5
│   ├── marriage_divorce_2000_2023.csv
│   ├── fertility_2000_2023.csv
│   └── single_parent_5yr.csv
├── kosis_grdp_employment/             # B.1
└── stata_packages_install_log.txt     # C.2
```

### 다운로드 우선순위 (2026-05-04 부터 가용한 시간 기준)

**Day 1 (Tier A 핵심)**:
- A.3 사업체조사 KSIC 4-digit (가장 큰 데이터, 첫 다운로드)
- A.5.1 이혼·결혼 (KOSIS 가이드 K7)
- A.2 외국인등록 (KOSIS 검색)

**Day 2 (의료 인프라)**:
- A.1.1 HIRA 의료기관 수
- A.1.3 HIRA 항바이러스제 J05A
- A.1.2 KCDC vaccination (가용성 verify, 부재 시 fallback)

**Day 3 (가족 mediator + KSIC concordance)**:
- A.5.2 합계출산율
- A.5.3 한부모 (5년 주기, 일부 welfare_panel 활용)
- A.4 KSIC-HS6 concordance (이미 존재 + IO 380 추가 다운로드)

**Day 4-5 (Tier B + Stata 환경)**:
- B.1 GRDP / 고용
- B.3 1990-1994 baseline (가용 시)
- C.2 Stata 환경 verification

**Day 6-7 (verification + Stage 5 시작)**:
- 모든 다운로드 데이터 + PAP v3.2 spec mapping verify
- Stage 5 회귀 분석 시작

---

## 사용자 Action Items 요약

| # | Action | Time | 우선순위 |
|---|--------|------|:--:|
| 1 | KOSIS 회원가입 + API key 확인 (이미 보유) | 5분 | High |
| 2 | HIRA 회원가입 (opendata.hira.or.kr) | 5분 | High |
| 3 | KOSIS 사이트에서 위 path 별 데이터 다운로드 | 1-3시간 | High |
| 4 | HIRA 사이트에서 의료기관 + 의약품 다운로드 | 30-60분 | High |
| 5 | KCDC vaccination 가용성 verify + fallback 결정 | 30분 | High |
| 6 | 통계청 KSIC concordance 응답 follow-up | 이메일 | Medium |
| 7 | Stata license 확인 (가천대) + 7 package 설치 시도 | 1-2시간 | Medium |
| 8 | 한국은행 IO 380 다운로드 (KSIC concordance fallback) | 30분 | Medium |
| 9 | 다운로드 완료 후 R-A 에게 보고 + spec adjust | 다음 conversation | High |

---

## R-A 에게 보고할 specific quote (R-2 protocol § 7.3)

각 데이터 다운로드 후 다음 specific 정보를 R-A 에게 보고:

```
[데이터 ID] (예: A.1.1 HIRA 의료기관 수)
- 메뉴 path: 정확히 어디서 찾았는지
- 표 ID + 제목: KOSIS DT_xxx 또는 HIRA URL
- 시계열: 시작-끝 연도
- Panel granularity: 시도 / 시·군·구 / 자치구 분리 여부
- 변수 list: column 이름들
- 다운로드 형식: CSV / Excel / OpenAPI
- 행 수: 전체 row count
- 결측 패턴: 1995-1999 baseline 가용 / 부재 / 부분 가용
- 파일 위치: 사용자 PC 의 어느 폴더 + 파일명
```

이 정보 paste 받으면 R-A 가:
1. PAP v3.2 spec 과 정합성 verify
2. Spec adjust 필요 시 즉시 PAP update
3. Fallback 결정 (데이터 부재 시)

---

작성: Claude (R-A) + 정재헌, 2026-05-03
PAP v3.2 spec 요구사항 → 데이터 수집 protocol mapping
