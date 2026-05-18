# Reviewer Guide — Trade × Mortality Korea

**Paper**: "Trade Shock and Deaths of Despair in Korea: Quantifying the Underexplored Family-Mediated Channel"
**Author**: 정재헌 (Jae-Heon Jeong, 가천대 경제학부 학부생, SSCI 단독 저자 지향)
**Last update**: 2026-05-04
**PAP version**: v3.4 status commit, v3.5 update pending (reference proposal v01.1)

---

## 1. 5분 Reviewer 가이드

본 paper 의 핵심 가설:
> **한국의 deaths of despair (자살, 약물, 정신, 간) 는 무역 충격 (Bartik shift-share IV) 의 영향을 받음. 그 영향의 일부는 가족 mediator (혼인 분해, 교육 attainment) 를 통해 전달됨.**

**핵심 finding (한국 vs US 차이)**:
- 한국 = **자살 + 간** dominance (working-age 25-64 의 약 22% 사망)
- US (Pierce-Schott 2020) = 약물 dominance (한국 약물 사망률 = US 의 1/10)
- DGHP 2017 + DFH 2020 ivmediate framework 로 family channel 정량화 (paper § 5.2)

**현재 status**:
- ✅ Stage 1-3: mortality + population + mediator panel build 완료 (24 parquet)
- ⏳ Stage 4: Bartik IV (Comtrade 진행 중, HS-KSIC concordance 통계청 응답 대기)
- ✅ Stage 5 spec plan 완료 (PAP v3.4 commit), 진입 대기

---

## 2. Reviewer 가 어디 봐야 하는지

### A. 핵심 문서 4 개 (우선순위 順)

| 우선 | 문서 | 위치 | 분량 |
|------|------|------|------|
| 1 | **PAP v3.4** (status commit, 본문) | `4_documentation/PAP/PAP_2026_05_03_v3.3.md` | ~30p |
| 2 | **Reference update proposal v01.1** (3 issue 정정 후) | `4_documentation/PAP/PAP_v3.4_reference_update_proposal_v01.md` | ~15p |
| 3 | **Mediator panel pipeline doc** (본 conversation 결과) | `4_documentation/pipeline_docs/mediator_panel_build_pipeline_documentation_v01.md` | ~25p |
| 4 | **Stage 5 regression plan** (next phase) | `4_documentation/stage_plans/stage5_regression_plan_v01.md` | ~30p |

### B. 보조 문서

- **Reference library master** (19 paper deep summaries): `4_documentation/reference_library/reference_library_master_v01.md` (~30p)
- **각 paper 별 deep summary**: `4_documentation/reference_library/paper_summaries/` (19 md, 평균 2000 단어)
- **Validation reports**: `3_derived/validation_report_*.md`, `PAP_v3.4_reference_proposal_validation_v01_1.md`

---

## 3. 데이터 inventory

### 3.1 Raw data sources

| source | 시점 | 단위 | status | 위치 |
|--------|------|------|--------|------|
| KOSIS API (mediator) | 1995-2020 | 시도 only — 부재 발견 | 폐기 | `0_raw/kosis_marriage_education/` |
| MDIS 인구주택총조사 2% 표본 | 1990-2020 (7 시점) | 시군구 individual | ✅ | `0_raw/mdis_population_census/` |
| MDIS 사망원인통계 (B형) | 1997-2024 (28 시점) | individual death | ✅ | `Desktop/지역별 자살 데이터/사망사료 정리/` |
| Comtrade (Bartik IV) | 1995-2024 | HS6 trade flow | ⏳ | `0_raw/comtrade_*/` |
| ECOS (가계부채) | 2003-2024 | sido | ✅ | `0_raw/ecos_*/` |

### 3.2 Derived panels (24 parquet)

**Stage 3 main outcome**:
- `mortality_rate_panel_v02_1.parquet` — 123,660 rows, 229 h_code, **외국인 빼기 제거** (분모 한국인 only)
- `population_panel_v01.parquet` — 한국인 only

**Stage Mediator (본 conversation 작업)**:
- `mortality_microdata_cleaned_v01.parquet` (7.4M, 28 시점)
- `mediator_panel_marriage_v02.parquet` (71K, 6 시점, 4 카테고리)
- `mediator_panel_education_v03.parquet` (63K, **3 카테고리 — mortality align**)
- `mortality_marital_panel_v01.parquet` (1.0M, working-age 25-64 + sigungu_crosswalk)
- `mortality_education_panel_v01.parquet` (1.0M)
- **`mediator_specific_marital_rate_v01.parquet`** (187K, **Stage 5 regression input**)
- **`mediator_specific_education_rate_v01.parquet`** (172K, **Stage 5 input**)

---

## 4. 핵심 finding 시계열 (Working-age 25-64, /100K annual)

### Deaths of Despair 5 stack period 추세

| period | mortality 5y | drug | liver | psych | suicide |
|--------|--------------|------|-------|-------|---------|
| 1 | 1997-2001 | 5.61 | **44.17** | 13.29 | 23.23 |
| 2 | 2002-2006 | 4.01 | 34.26 | 10.62 | 28.26 |
| 3 | 2007-2011 | 3.81 | 26.44 | 9.85 | **35.27** |
| 4 | 2012-2016 | 3.85 | 22.69 | 8.93 | 32.89 |
| 5 | 2017-2021 | 3.86 | 19.05 | 9.66 | 29.61 |

**검증** (한국 통계청 vs paper):
- ✅ 자살 peak 2007-2011 (카드사태 2003 + 글로벌 금융위기 2008-2010)
- ✅ 간질환 -57% 단조 감소 (B형 간염 백신 + 의료 발전)
- ✅ 약물 매우 낮음 (US 의 1/10) — paper 핵심 finding (US ≠ Korea)
- ✅ all_cause 277 → 152 / 100K (-45%, 의료 발전)

---

## 5. Reviewer Feedback 요청 사항 (5 영역)

### 5.1 Methodology

1. **DGHP 2017 + DFH 2020 ivmediate spec** (PAP § 5.2): direct/indirect effect 분해의 instrument set 적절성
2. **5-year stack period mapping** (mortality 5년 합 vs mediator census year 가까운): timing 가정 적절성
3. **5-layer SE** (PAP § 7): HC1 + WCB-sigungu + WCB-sido + AKM (BHJ 2022) + Conley + AR+tF over-engineering 여부

### 5.2 Data Quality

1. **Mediator education 3 카테고리** (NoHS / HS / College+): 1997-2007 의 5=대학통합 vs 2008+ 의 6/7 분리 매핑 적절성
2. **denom missing 9.74% (marital)**: 67 추가 h_code 의 1990 placeholder 잔류 + Stage 5 listwise deletion bias
3. **2024 시점 252 h_code**: sigungu_crosswalk_v2 미cover. main analysis (1997-2021) 무관 caveat 충분 여부

### 5.3 Robustness

1. **Romano-Wolf step-down** family of hypotheses (4 outcome × 2 mediator dim = 8 + all_cause = 9?)
2. **OP test 23.1**: 5% TSLS bias relative to OLS criterion (NOT size distortion) 정확 attribution (reference proposal v01.1 정정)
3. **외국인 빼기 over-correction** (PAP § 8 #22): Stage 3B v02.1 의 -0.35% 차이 reasoning 의 sufficient 여부

### 5.4 Novelty Position

1. **한국 = 자살+간 vs US = 약물**: dominance 차이의 mechanism 가설 (paper § 7) sufficient narrative?
2. **Family channel** (Hanson 2018 marriage value 의 한국 확장) novelty position
3. **Mediator-specific rate panel** (DGHP 2017 의 한국 first 적용) contribution claim

### 5.5 Reference Citation Accuracy

본 conversation round 7 audit 에서 정정한 3 issue:
1. GPSS 2018 NBER → **2020 AER 110(8)** primary (NBER WP 24408 = working version)
2. DGHP 2017 NBER 23209 + **DFH 2020 Stata Journal 20(3)** (ivmediate package implementation source) 둘 다 cite
3. OP test F=23.1 = **5% worst-case TSLS bias** (NOT "size distortion 5%") — Stock-Yogo 2005 + Olea-Pflueger 2013

→ Reviewer 가 추가 inaccuracy 발견 시 명시 요청

---

## 6. Reviewer 의 다음 step (workflow)

1. **본 REVIEWER_GUIDE 5 분 read** (overview)
2. **PAP v3.4** read (~30 분, 핵심 framework)
3. **Mediator panel pipeline doc** read (~20 분, 본 conversation 결과)
4. **Reference proposal v01.1** read (~15 분, 3 issue 정정 detail)
5. **REVIEWER_FEEDBACK_TEMPLATE.md** 코멘트 작성 (1-2 시간) — 별도 파일
6. **시각화** 검토: `4_documentation/figures/deaths_of_despair_timeseries.png` (작성 중)

추가 필요 시:
- 19 paper summary 중 관심 paper read (각 1500-2700 단어)
- 24 derived parquet 중 관심 panel direct verify (Python pandas)

---

## 7. Pending issue 4 (Stage 5 진입 전)

| issue | severity | 처리 |
|-------|----------|------|
| Stage 4 Bartik IV (Comtrade + HS-KSIC concordance 미완) | 🔴 critical | 통계청 응답 대기 |
| denom missing 9.74% (marital) — 67 h_code 진단 | 🟡 medium | sub-script 작성 후 1 시간 |
| Stata 환경 verify (가천대 license + 7 package) | 🟡 medium | 30 분 |
| PAP v3.4 → v3.5 update (reference proposal v01.1 적용) | 🟢 low | 1.5 시간 |

본 4 항 완료 시 **Stage 5 mediation regression 즉시 진입 가능**.

---

_본 REVIEWER_GUIDE = paper 의 단일 entry point. 모든 documentation + data + script path 정리._
