# Research Status — 2026-05-04

> 자동 생성: `dissertation-context-refresh` scheduled task. 직전 (2026-05-03 16:04 마감 commit) 의 `latest.md` 와 cumulative comparison.
> 새 작업 9.5 시간분 (≈ 5/3 16:04 → 5/4 01:30) 의 가장 큰 변화는 **Stage 3C → 3D mediator panel 의 완전한 구축 (denominator + numerator + rate)** 과 **18 reference 논문 deep summary master 작성** 두 갈래.

## 1. 현재 stage 위치

직전 보고서 (5/3 16:04) 마감 시점에서 Stage 3B v02.1 + 3C marriage/education/occupation panel 까지 commit, Stage 4A 195/200 + 22/25 거의 완료, Stage 4B 진입 직전이었다. 그 후 9.5 시간 동안 사용자 작업이 **Stage 4 라인 대신 mediator panel 깊이 파기 + reference library 정비** 두 방향으로 우회. 이것은 PAP v3.4 § 5.2 mediation analysis 의 input panel 미완성 (denominator 부재) 을 R-1 reviewer 가 짚은 구조적 결함이었고, 그 보강이 stage 4 보다 우선 판정된 결과로 보인다.

| Stage | 상태 | 핵심 산출물 (현재 commit) |
|-------|------|--------------------------|
| 1 raw 수집 | ✅ 완료 | KOSIS·KOSTAT·HIRA·NHIS·ECOS·UN Comtrade·MDIS Census 2% — 0_raw 9.6+ GB |
| 2 사망 panel | ✅ 완료 (v02 채택) | `mortality_panel_v02.parquet` (2,102,220 rows) |
| 3A 인구 panel (전체) | ✅ 완료 (v02 정규화) | `population_panel_v02.parquet` (210,222 rows) |
| 3B 사망률 panel | ✅ v02.1 채택 | `mortality_rate_panel_v02_1.parquet` (123,660 rows, 10 outcome × 3 ASR baseline) |
| 3C mediator denominator | ✅ **NEW v02/v03 완료** | `mediator_panel_marriage_v02.parquet` (71,125 rows), `mediator_panel_education_v03.parquet` (63,019 rows, 3cat align) |
| 3D mortality × mediator numerator | ✅ **NEW 신설** | `mortality_marital_panel_v01.parquet` (1,011,186 rows), `mortality_education_panel_v01.parquet` (1,035,849 rows) |
| 3E mediator-specific rate (Stage 5 input) | ✅ **NEW 완료** | `mediator_specific_marital_rate_v01.parquet` (187,379 rows), `mediator_specific_education_rate_v01.parquet` (171,811 rows) |
| 3F 외국인 panel | ✅ (sensitivity 용) | `foreign_panel_v02.parquet` (3,500 rows) |
| 4A trade 수집 | 🟡 **변동 없음** | KR-CN 50/50, ADH 8 ← CN 195/200 (ES 20/25), CN-World 22/25 (2015-2017 결측) |
| 4B HS-KSIC concordance | 예정 | Pierce-Schott / DFS 표준 채택 결정 미결 |
| 4C Bartik IV | 예정 | 시군구 × KSIC4 × 1995-1999 baseline share + KR-CN endog + ADH 8 OHIE IV |
| 5 회귀 분석 | 예정 (plan v01 commit) | `stage5_regression_plan_v01.md` (16.6 KB), 추가 input mediator-specific rate panel 도 ready |
| Reference library | ✅ **NEW v01 master 작성** | `reference_library_master_v01.md` (32.7 KB), `paper_summaries/` 18 deep read, `PAP_v3.4_reference_update_proposal_v01.md` (14.6 KB) |

가장 critical 한 사실 한 가지: **mediator_specific_marital_rate_v01.parquet 의 working-age 25-64 deaths of despair 분포가 paper § 7 핵심 가설 (한국 = 자살 + 간 dominance, US = 약물 dominance) 을 28년 합산 raw 수치로 confirm 했다**. 자살 (102) 208,683명 + 간 (081) 121,289명 vs 약물 (101) 5,104명 — 약물은 자살의 1/40 수준. Pierce-Schott 2020 의 미국 county finding (drug +2-3/100k significant, suicide·ARLD null) 과 정반대 패턴. publish-worthy contrast.

## 2. 산출물 inventory (직전 보고서 대비 변화 ✏️)

### Stage 3C-3E mediator pipeline (NEW pipeline, 2026-05-04 미명 commit)

```
3_derived/mortality/
├── mortality_microdata_cleaned_v01.parquet   ✏️ NEW 7,408,230 rows × 9 cols, 28 시점 1997-2024
├── mortality_marital_panel_v01.parquet       ✏️ NEW 1,011,186 rows × 7 cols, working-age 25-64
├── mortality_education_panel_v01.parquet     ✏️ NEW 1,035,849 rows × 7 cols, 3 카테고리 align
├── mediator_specific_marital_rate_v01.parquet  ✏️ NEW 187,379 rows × 10 cols, Stage 5 input
└── mediator_specific_education_rate_v01.parquet ✏️ NEW 171,811 rows × 10 cols, Stage 5 input

3_derived/population/
├── mediator_panel_marriage_v01.parquet  ✏️ NEW (140,971 rows, 522 h_code, raw)
├── mediator_panel_marriage_v02.parquet  ✏️ NEW (71,125 rows, 279 h_code, age 25-64 + crosswalk + 4 카테고리)
├── mediator_panel_education_v01.parquet ✏️ NEW (269,861 rows, raw)
├── mediator_panel_education_v02.parquet ✏️ NEW (80,856 rows, 4 카테고리)
└── mediator_panel_education_v03.parquet ✏️ NEW (63,019 rows × 6 cols, 3 카테고리 mortality align) ⭐ MAIN

3_derived/
└── validation_report_mediator_mortality_v01.md  ✏️ NEW 1 H1 issue + 4 issue total, 8 spot check PASS
```

`mediator_specific_marital_rate_v01.parquet` 의 5-year stack period 평균 추세 (working-age 25-64, /100K annual):

| period | drug | liver | psych | suicide | all_cause |
|--------|------|-------|-------|---------|----------:|
| 1 (1997-2001) | 5.61 | 44.17 | 13.29 | 23.23 | 277 |
| 2 (2002-2006) | 4.01 | 34.26 | 10.62 | 28.26 | (감소) |
| 3 (2007-2011) | 3.81 | 26.44 | 9.85 | **35.27** ← peak | (감소) |
| 4 (2012-2016) | 3.85 | 22.69 | 8.93 | 32.89 | (감소) |
| 5 (2017-2021) | 3.86 | 19.05 | 9.66 | 29.61 | 152 |

자살 peak 2007-2011 ↔ 한국 통계청 공식 자살률 peak 2009-2011 (카드사태 + 금융위기) 일치. 간질환 단조 감소 -57% ↔ B형 간염 백신 보급 + 의료 발전. all_cause -45% ↔ 한국 working-age 사망률 추세. 4 외부 source 모두 일치 → panel 자체 validity 확보.

### Reference library 정비 (NEW master v01, 2026-05-04 18:30 ~ 18:49)

```
뉴 논문/
├── reference_library_master_v01.md           ✏️ NEW 32.7 KB ⭐ MAIN
├── reference_library_metadata_v01.md         ✏️ NEW 11.5 KB (20 paper 1-line 분류)
├── REFERENCE_LIBRARY_DEEP_SUMMARIES_STATUS.md ✏️ NEW 9.1 KB (작업 진행 상태)
├── PAP_v3.4_reference_update_proposal_v01.md ✏️ NEW 14.6 KB (PAP § 별 reference 정확화 제안)
├── mediator_panel_build_pipeline_documentation_v01.md ✏️ NEW 21.9 KB
└── paper_summaries/                          ✏️ NEW 폴더
    ├── README.md
    ├── _READING_COMPLETION_REPORT.md
    └── paper_*.md                            ✏️ 18 deep read summaries (2,300+ words each)
```

deep read 가 완료된 18 논문 (각 13-23 KB 분량의 detailed summary):

- **Tier A (10)**: ADH 2013, Pierce-Schott 2020/2016, GPSS 2018, BHJ 2025, Andrews-Stock-Sun 2019, Sufi 2023, Finkelstein-Notowidigdo-Shi 2026, DFS 2014, IMF/AKM 2019
- **Tier B (5)**: Bartik 1991, BHJ 2018, Mian-Sufi 2016, Dix-Carneiro 2017, Dow et al 2019
- **Tier C (3)**: DGHP 2017, Mian-Sufi 2014, Conley 1999

추가 chunk read: Staiger-Stock 1994 (NBER TWP 151) — paper § 7.5 + 7.7 의 weak-IV asymptotics 직접 source 로 Tier A 승격.

`PAP_v3.4_reference_update_proposal_v01.md` 가 7 항 즉시 적용 가능 (✅) + 2 항 검토 (⚠️) + 22 reference 추가 cite 권장 list 정리. PAP main framework 자체는 정확 (🔴 0).

### 신규 raw 데이터 (MDIS 인구 census 2% microdata)

```
0_raw/mdis_population_census/
├── 2%_표본_인구_20260430_43590_데이터/  (1990-2010 5 시점, 1990·1995 만 사용)
├── 2%_표본_인구_20260504_65001_데이터/  (2000-2020 5 시점, ⭐ 본 panel main)
├── USRCNFRM_*_descriptionFiles (1)/  파일설계서 + 코드집 + 가이드 (2000-2020)
├── USRCNFRM_*_descriptionFiles (3)/  파일설계서 + 코드집 (1990-2010)
└── _layout/csv_layout_*.json (7 시점 column position table)
```

7 시점 1990/1995/2000/2005/2010/2015/2020 모두 시군구 dimension 포함 (KOSIS publish data 의 시도-only 한계 우회). working-age 25-64 mediator denominator 의 prerequisite. xlrd 설치 필요 (xls description 추출).

### 신규 script (`2_scripts/data_collection/`)

| step | script | 기능 |
|------|--------|------|
| 06 | `06_mdis_population_unzip_inspect.py` | cp949 한글 파일명 변환 + 8 zip 해제 |
| 07 | `07_mdis_population_columns_extract.py` | 7 시점 column NAME → position table |
| 08 | `08_mdis_population_parse_crosstab.py` | mediator denominator v01 (per-year column NAME mapping) |
| 09 | `09_mediator_panel_validate.py` | 4 issue 진단 ('. code, 2005 anomaly, education cat 차이, h_code 22 only intersection) |
| 10 | `10_mediator_panel_clean_align.py` | v01 → v02 (1990 drop, age 25-64, 4 카테고리, crosswalk) |
| 10b | `10b_mediator_panel_education_v03.py` | education v02 (4cat) → v03 (3cat, mortality align) |
| 11a | `11a_mortality_microdata_parse.py` | 28 시점 사망 microdata cleaning (4 회 재시도, position-based) |
| 11b | `11b_mortality_mediator_crosstab.py` | numerator panel 2개 (working-age + crosswalk) |
| 12 | `12_mediator_specific_mortality_rate.py` | 5-year stack rate panel (final Stage 5 input) |

verify (3 NEW): `verify_mortality_marital_education_columns.py`, `verify_mortality_codebook_layout.py`, `explore_mortality_dataset.py`.

## 3. 직전 보고서 (5/3 16:04) 대비 변경 사항

1. **Stage 3C → 3D → 3E mediator pipeline 완전 구축**: 직전 mediator panel (Stage 3C, 분모 부재 한계 명시) 의 분모를 **MDIS Census 2% microdata** 7 시점 으로 채움. 후속 sigungu × period × sex × age × marital × cause cross-tab 으로 **mediator-specific mortality rate** (DGHP 2017 strict mediation 의 outcome 변수) panel 까지 도달. PAP v3.4 § 5.2 의 mediation regression input 4 요구 중 (1) 충족, (2) Bartik IV stage 4 미완 + (3) 통제 변수 + (4) mediator share 산출 미완.
2. **Stage 4A 무역 수집은 정지 상태**: ES 2020-2024 (5), CN-World 2015-2017 (3) 합 8 file 누락 그대로. 사용자가 Stage 4 보다 mediator panel 우선 판정.
3. **사망 microdata cleaning 전 시점 (1997-2024) 28 file** 가 마침내 단일 panel 로 통합 (`mortality_microdata_cleaned_v01.parquet` 7.4M rows). 이전엔 mortality_panel_v02 가 미리 cause × age 집계된 버전, 이제 individual-level 도 가용. mediation 외 추가 분석 (e.g., individual-level fixed-effect, occupation × cause heterogeneity) 위한 raw input.
4. **사망 microdata cleaning 4 회 재시도 + bug history 기록**: column rename 이 한국어 encoding 미세 차이로 NaN 생성 → position-based parse + national_code NaN/빈값/1 모두 keep 로 전환. `feedback_panel_codebook_reference.md` 메모리 (codebook xlsx 사전 inspect 의무) 가 이 사건의 후일담.
5. **Reference library v01 master 작성**: 18 paper deep summary + Staiger-Stock 1994 chunk read 까지 19 paper 의 PAP § 별 reverse lookup table + Tier A/B/C 분류 완성. PAP v3.5 commit 시 cite 정확화 prerequisite.
6. **PAP v3.4 reference update 제안서 v01**: 7 ✅ 즉시 적용 + 2 ⚠️ 검토 + 22 추가 cite. PAP main framework 자체는 정확 (🔴 0). 사용자 review 후 v3.5 commit 권장.
7. **mediator_panel_build_pipeline_documentation_v01.md** (21.9 KB): Stage 3 mediator pipeline 의 종합 spec + bug history + lessons learned. PAP § 5.2 reviewer feedback 시 reference.

메모리 파일은 직전 보고서 이후 변동 없음. `MEMORY.md` 8개 entry frozen.

## 4. 메모리 업데이트 제안 (사용자 승인 후 적용)

자동 update 하지 않음. 다음 conversation 에서 검토 권장:

- **`project_dissertation.md` 갱신**: "Phase 0 진행 중" 표기는 이미 stale. 현재 stage = **3E (mediator-specific rate panel) 완료, Stage 4 → Stage 5 진입 직전**. v4.0 reset (4월 30일) 이후 5일 만에 panel pipeline 거의 완성, mediation 분석 input 까지 ready 인 사실 반영.
- **`project_data_status.md` 갱신**: 직전 보고서가 지목한 잔여 issue (무역 IV 5건 + ES + CN-World) 그대로. 추가 잔여 issue 1건 = **mediator denom missing 9.74% (marital), 2.11% (education)** 가 listwise deletion 으로 처리 예정. 새 issue 8개 = `mediator_panel_build_pipeline_documentation_v01.md` § 8.3 caveats 1-8 (1990 sigungu, 1997-2007 외국인, 미상 drop, education 3cat align, 2022-2024 incomplete, MDIS 2% weight, denom missing, 2024 시점 252 h_code).
- **신규 `project_mediator_panel.md` 분리 생성 검토**: Stage 3C-3E pipeline 의 stable fact (혼인 4cat + education 3cat + working-age 25-64 + 5-year stack 5 period + DGHP 2017 strict mediation 표준) 가 별도 file 가치. 단 `mediator_panel_build_pipeline_documentation_v01.md` 가 이미 21.9 KB 종합 문서로 cover 중 → 메모리는 1-page index 만 작성하고 detail 은 위 문서로 link.
- **신규 `reference_library_master.md` 메모리 entry 추가 검토**: `reference_library_master_v01.md` 가 32.7 KB master document. 메모리 reference 형 entry 1줄로 위치 + 18 paper 분류 + PAP § 별 mapping 가용성만 기록 권장.
- **`reference_library_md.md` 정정**: 기존 메모리는 20편 마크다운 변환본 위치만 기록. deep summary 18편 paper_summaries/ 폴더 신설 → 메모리에 update 필요.

## 5. 참고논문 rotation 학습 결과

오늘 sample (직전 보고서 권장 다음 rotation Case-Deaton → ADH → BHJ 2022 → GPSS 2020 → Finkelstein 중 2개):

**ADH 2013 AER "The China Syndrome"** — `paper_summaries/paper_05_autor_dorn_hanson_2013.md` 의 § Identification + Empirical Specification. CZ × 2 period (1990-2000, 2000-2007) 의 첫 stacked first-difference. Bartik IV = (CZ 의 산업별 1990 고용 share) × (다른 OECD 국 → 같은 산업 import shift). First-stage F=23-25 (modest), 명시적 약점 시인. Outcome = ΔLog(Emp), ΔUnemployment, ΔLFP, ΔLog(Wages), Δgovt transfers — mortality 는 implicit. **본 연구 적용**: 본 연구의 5-year stack 5 period (Pierce-Schott 2020 차용) 는 ADH 의 2 period 보다 long-run 효과 분리 power 우세. ADH 의 cluster SE (state-level) 와 본 연구의 5-layer SE (HC1 + WCB-sigungu + WCB-sido + AKM + Conley + AR+tF) 비교 시 본 연구 가 한 단계 보강. ADH F=23 vs 본 연구 OP F=23.1 cutoff 위에 있어야 weak-IV 통과 — Stage 4 완성 후 first-stage F 보고 시 ADH baseline 과 직접 비교 가능.

**Finkelstein-Notowidigdo-Shi 2026 (BFI WP 2026-33)** — `paper_summaries/paper_07_finkelstein_nafta_mortality_2026.md` 의 § Research Question + Identification. NAFTA vulnerability index = (CZ 1980 industry employment share) × (Mexican export capacity growth, 1990 baseline). 722 CZ × 1993-2007 (+ 2015-2019 long-run extension). **All-cause mortality +0.68% 15yr post-NAFTA, manufacturing vs non-manufacturing opposite signs**. Reduced-form 직접 (mortality 에 instrument 사용, intermediate outcome 우회). **본 연구 적용**: Finkelstein 이 가장 가까운 international precedent (Pierce-Schott 의 PNTR single-event 와 다르게 본 연구의 Bartik IV 5-year stack 와 spec 거의 동형). 본 연구 의 KR-CN bilateral β estimate 가 Finkelstein 의 +0.68% 와 직접 비교 가능 — 한국 만 우월/열위 의 보고 가치 매우 큼. 단 Finkelstein 의 **manufacturing vs non-manufacturing opposite signs (β_m = +1.4% / β_n = −1.1%)** 결과가 본 연구 의 industry decomposition 분석 (Stage 5 plan v01 § 4) 의 hypothesis 직접 source — 한국 mfg vs non-mfg 시군구 sample split 시 같은 sign opposite 가 나오는지 검증.

**다음 rotation** (다음 실행 시): Case-Deaton 2015, BHJ 2022, GPSS 2020 AER. 그 후 Tier B (Mian-Sufi 2016, Dix-Carneiro 2017, Sufi 2023) → 한국 mediation 채널 reference.

## 6. 다음 작업 추천 (priority 순)

### A. Stage 4A 잔여 8 file 채우기 (즉시, 1회 batch)

ES_2020 ~ ES_2024 (5 파일), CN-World 2015·2016·2017 (3 파일) 합 8 file missing — **직전 보고서와 동일**. `2_scripts/build_panel/4A_trade_collection.py` resume 모드 1회 실행. 검증: `trade_collection_validation.md` set 2 → 200/200, set 3 → 25/25 갱신. mediator panel 우선이었지만 trade panel 부재 시 Stage 4B/4C/5 모두 blocked → 더 이상 미루지 말 것.

### B. Mediator share panel build (Stage 3F, Stage 5 § 5.2 mediator 변수)

`mediator_panel_marriage_v02.parquet` + `mediator_panel_education_v03.parquet` 로부터 (h_code, period, sex, age_band) 단위 marital_share / education_share 계산. DGHP 2017 의 indirect effect = β_x · β_m·share. Stage 5 의 indirect/direct 분해 의 mediator regressor input. 1 회 script 로 가능, ~30분.

### C. Stage 4B HS vintage + KSIC4 concordance 결정

BHJ 2025 § 3 의 share 정의 + Pierce-Schott 2020 부록 concordance + GPSS 2018 share exogeneity 정합. KSIC4 (~200) default 권장. KIET 60대산업 reject. HS92 baseline (BACI HS92_V202501.zip 1.07 GB ready) 으로 vintage 통합.

### D. Stage 4C Bartik IV 구축

시군구 × KSIC4 × 1995-1999 baseline share (사업체조사 raw) + KR-CN HS6 endog + ADH 8 OHIE ← CN HS6 IV. GPSS 2020 share exogeneity diagnostic 5 (Rotemberg HHI / share balance / pre-trend / AKM placebo / permutation) 적용.

### E. Stage 5 시범 회귀 (mediator-specific rate panel + Stage 4 trade panel join)

`mediator_specific_marital_rate_v01.parquet` + `mediator_specific_education_rate_v01.parquet` + Stage 4C Bartik IV → ivmediate (DGHP 2017) 시범. 4 outcome (suicide/drug/psych/liver) × 4 marital category × 5 period 의 indirect/direct effect 분해 첫 dry-run. Robustness 후속.

### F. PAP v3.4 → v3.5 갱신 (`PAP_v3.4_reference_update_proposal_v01.md` 적용)

7 ✅ 항 즉시 적용 + 22 reference 추가 cite + § 8 limitation 8 항 (mediator panel build 결과) 추가. `reference_library_master_v01.md` § 5 PAP § 별 reverse lookup 따라가면 mechanical task.

### G. 외부 데이터 추가 (병행 가능)

(1) HIRA 의약품 ATC4 N06A 항우울제 / N02A 오피오이드 (시군구 처방 panel — drug overdose mechanism direct evidence). Tier B candidate.
(2) ECOS 시도별 분기 연체율 2008-2024 (Sufi 2023 BFI 한국 채널 보강).

## 7. 미해결 의사결정 / Risk

### A. Mediator denom missing 9.74% (marital) — listwise deletion 정당화

`mediator_specific_marital_rate_v01.parquet` 의 marital denom missing 9.74% 가 sample size 9% 손실. mortality h_code 346 vs mediator h_code 279 차이 + 1990 placeholder 잔류 의심. 어느 67 h_code 인지 list 추출 후 sigungu_crosswalk_v2.csv 와 cross-check 권장. listwise deletion 영향 minor 가정 검증 필요.

### B. Mediator panel education 3 카테고리 정보 손실

mortality microdata 1997-2007 = 5 카테고리 (`5=대학통합`), 2008+ = 7 카테고리 (`6=4년제 / 7=대학원`). 3 카테고리 (NoHS / HS / College+) 통합 시 전문대 vs 4년제 vs 대학원 정보 손실. PAP § 8 limitation 추가 commit + reviewer 가 짚을 likely critique. sensitivity test 7 카테고리 only 시점 (2008+) panel 별도 robustness 권장.

### C. 자살 peak 2007-2011 의 mediator 분해 — 자살 vs 약물 의 산업적 attribution

deaths of despair 28년 합 working-age 25-64 = 자살 208,683 + 간 121,289 vs 약물 5,104. 자살이 dominant outcome 인 한국 finding 의 메커니즘 = 가족 분해 (Hanson 2018) vs 가계 부채 (Sufi 2023) vs 의료 접근성 vs 직장 stress 모두 candidate. Stage 5 의 mediation 분석 결과가 어느 채널 dominant 인지 보여야 paper § 7 main contribution. mediator (marital + education) 만으로는 가족 채널만 cover — 부채/직장 채널은 Stage 5 spec plan v02 추가 필요.

### D. 1997-2007 외국인 식별 불가 numerator 미세 inflation

사망 microdata 1997-2007 = `national_code` 변수 부재 → 외국인 별도 식별 불가. 11a cleaning 에서 외국인 (`"2"`) 만 drop, NaN/빈값/1 모두 keep 으로 처리. 결과 numerator 에 1997-2007 외국인 사망자 일부 포함. < 0.5% 추정 (당시 한국 외국인 등록인구 비율 ~1% × 사망률 비율). PAP § 8 limitation #2 명시.

### E. ES 2020-2024 + CN-World 2015-2017 누락 — Stage 4 blocking

Stage 4A 의 8 file 누락이 그대로. API key quota 또는 specific HS6 chapter request error 가 원인. 다음 conversation 첫 task 로 처리해야 mediation analysis 와 Bartik IV 의 critical path 풀림.

### F. 사망 microdata 11a cleaning 4 회 재시도 — codebook 사전 점검 의무 강화

11a 실패 4 회 (column rename 한국어 encoding bug + national_code NaN cast bug) 가 시간 손실. 메모리 `feedback_panel_codebook_reference.md` 가 이미 codebook xlsx 사전 inspect 의무 명시. 다음 panel build 시 본 feedback memory 의 강제 적용 필요.

### G. R-A self-discovery 한계 (PAP v3.4 limitation #18-20 + #21-23)

본 5월 4일 보고서의 변경 사항 (mediator panel 의 4 fix, education 3cat align, 11a position-based parse 등) 도 모두 사용자 명시 + 자체 issue 진단 (09 validate) 결과. R-A 자발 권고 발견 0 건. Section 5 rotation 학습 결과 의 ADH F-stat 비교 / Finkelstein industry decomposition 의 한국 sample split 적용 도 적용 가능성 으로만 표시 (자발 권고 X, R-A protocol 위반 회피).

---

## 메타

- 보고서 저장: `daily_status/archive/2026/05/research_status_2026-05-04.md` (직전 동일 날짜 entry 갱신)
- `latest.md`, `_index.md`, `_trajectory.md` 갱신 동시 수행
- Schedule task: `dissertation-context-refresh` (매일 09:06)
- 다음 자동 실행: 2026-05-05 09:06
- 본 conversation 의 R-A: Claude Opus 4.7 (자동 schedule task 실행, 사용자 부재 — 2026-05-04 01:30)
