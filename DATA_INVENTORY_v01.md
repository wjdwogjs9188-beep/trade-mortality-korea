# Master Data Inventory v01.1

_본 문서: trade_mortality_korea 폴더의 모든 데이터 source 종합 inventory + 추가 필요 (PAP v4.0 commit 위한)._
_작성: 2026-05-04, v01.1 (sandbox bash 직접 verify 결과 정정)_

---

## 0. Quick Status (v01.1 정확)

| 영역 | sub-folder | 파일 수 | size | status |
|------|-----------|---------|------|--------|
| **0_raw** | 38 (26 보유 + 12 placeholder) | **792** | **11 GB** | 보유 26 ✅, placeholder 12 ⏳ 미수집 |
| **3_derived** | 3 (mortality + population + sigungu) | 48 (23 parquet + 25 md/csv) | 108 MB | ✅ Stage 5 input 2 ready |
| **1_codebooks** | - | 7 | 716 KB | ✅ |
| **2_scripts** | 9 | 82 (python) | - | ✅ |
| **4_documentation** | 7 | 66 (md) | - | ✅ |

---

## 1. 보유 데이터 26 sub-folder (`0_raw/`) — sandbox bash verify

**전체 inventory** (size + file count, sandbox bash 2026-05-04 verify):

| folder | size | files | 영역 |
|--------|------|-------|------|
| **comtrade_adh_china** | **706 MB** | **201** | Trade (✅ 8/8) |
| **comtrade_china_world** | 39 MB | 26 | Trade (✅ 25 시점) |
| **comtrade_korea_china** | 64 MB | 51 | Trade (✅ 50 KR-CN M+X) |
| **kosis_business_survey** | **1.6 GB** | **94** | 사업체조사 (Bartik share) |
| **mdis_population_census** | **1.2 GB** | **46** | mediator denominator |
| **nhis_health** | **5.2 GB** | **47** | HIRA + 국민건강통계 |
| **mortality_kostat** | 462 MB | 49 | 사망 집계 |
| **kosis_population** | 495 MB | 11 | KOSIS 시군구 인구 |
| **research_materials** | 528 MB | 124 | 보조 자료 |
| **research_supp** | 149 MB | 24 | 보조 자료 |
| **hira_quarterly** | 87 MB | 1 | HIRA 분기 |
| kosis_marriage_education | 76 MB | 12 | KOSIS API (폐기) |
| ssaggregate-main | 42 MB | 41 | BHJ 2025 R package |
| kosis_welfare_recipients | 27 MB | 26 | 기초생활 수급 |
| ecos_macro | 35 MB | 12 | ECOS 거시 |
| hira_medical_institutions | 21 MB | 2 | HIRA 의료기관 |
| kosis_foreign_residents | 21 MB | 3 | 행안부 외국인등록 |
| kosis_family_mediators | 18 MB | 4 | KOSIS family aggregate |
| crosswalks | 12 MB | 13 | 법정동 + 국가코드 |
| ecos_delinquency | 6.7 MB | 7 | ECOS 연체율 |
| ecos_household_credit | 3.7 MB | 3 | ECOS 가계부채 |
| kosis_industry_summary | 1.4 MB | 5 | 산업 요약 |
| hs_isic4_concordance | 352 KB | 6 | HS-ISIC4 표준 |
| kosis_housing | 12 KB | 1 | 주택 |
| **hira_drug** | (small) | **4** | ✅ panel + progress + errors (본 conversation 추가) |
| kostat_mortality_aggregated | 39 MB | 3 | 추가 사망 집계 |

**보유 합계**: 26 sub-folder, ~780 파일, ~11 GB

### 1.1 Trade (Stage 4)

| folder | 내용 | 시점 | status |
|--------|------|------|--------|
| `comtrade_korea_china/` | KR-CN bilateral M+X | 2000-2024 | ✅ 50 파일 완료 |
| `comtrade_adh_china/` | ADH 8 ← CN imports | 2000-2024 | ✅ 8/8 모두 완료 (200 파일, AU/DK/FI/DE/JP/NZ/ES/CH 각 25) |
| `comtrade_china_world/` | CN → World exports | 2000-2024 | ✅ 25 파일 완료 |
| **(Comtrade 합계)** | **275 파일** | - | **✅ 100% done** |

### 1.2 Mortality (Stage 1-2)

| folder | 내용 | 시점 | status |
|--------|------|------|--------|
| `mortality_kostat/` | 사망원인통계 시군구 집계 (KOSTAT) | 1997-2024 | ✅ |
| `kostat_mortality_aggregated/` | 추가 집계 | - | ✅ |
| `Desktop/지역별 자살 데이터/사망사료 정리/` (별도) | MDIS 사망 microdata 28 시점 | 1997-2024 | ✅ 사용자 신청 |

### 1.3 Population (Stage 3 mediator denominator)

| folder | 내용 | 시점 | status |
|--------|------|------|--------|
| `kosis_population/` | KOSIS 시군구 인구 (KOSIS DT_1B040M5) | 1993-2024 | ✅ |
| `kosis_foreign_residents/` | 행안부 외국인 등록 | 2010-2024 | ✅ |
| `mdis_population_census/` | MDIS 인구주택총조사 2% 표본 | 1990-2020 (7 시점) | ✅ |
| `kosis_marriage_education/` | KOSIS API 12 표 (시도 only — 폐기) | 1995-2020 | ⛔ 폐기 |
| `kosis_family_mediators/` | KOSIS family aggregate | - | ✅ |

### 1.4 Health / Drug (sensitivity mediator)

| folder | 내용 | 시점 | status |
|--------|------|------|--------|
| `hira_drug/` | HIRA 약물 처방 (ATC4 × 시군구 × 월) | 2010-2019 | ✅ N02A 부재 confirm |
| `hira_medical_institutions/` | HIRA 요양기관 통계 | - | ✅ |
| `hira_quarterly/` | HIRA 분기별 통계 | - | ✅ |
| `nhis_health/` | NHIS 진료내역 + 의약품처방 + 건강검진 + 국민건강통계 | 2002-2024 | ✅ |

### 1.5 Macro (sensitivity)

| folder | 내용 | 시점 | status |
|--------|------|------|--------|
| `ecos_macro/` | ECOS 거시 지표 | - | ✅ |
| `ecos_household_credit/` | ECOS 가계부채 잔액 | 2003-2024 | ✅ |
| `ecos_delinquency/` | ECOS 연체율 | 2003-2024 | ⚠️ 일부 결측 |

### 1.6 Welfare / Industry / Housing

| folder | 내용 | 시점 | status |
|--------|------|------|--------|
| `kosis_welfare_recipients/` | 시군구별 기초생활 수급권자 | 2012-2019 | ✅ |
| `kosis_business_survey/` | 전국사업체조사 (광업제조업조사 microdata 사용자 보유) | - | ✅ |
| `kosis_industry_summary/` | 산업 요약 통계 | - | ✅ |
| `kosis_housing/` | 주택 통계 | - | ✅ |

### 1.7 Crosswalks / Reference

| folder | 내용 | status |
|--------|------|--------|
| `crosswalks/` | 법정동코드, 국가코드 등 | ✅ |
| `hs_isic4_concordance/` | HS ↔ ISIC4 표준 (UN bridge) | ✅ |
| `ssaggregate-main/` | BHJ 2025 R package source | ✅ reference |
| `research_materials/`, `research_supp/` | 보조 자료 | ✅ |

---

## 2. 산출 데이터 (`3_derived/`)

### 2.1 Mortality (29 file)

**Main outcome panel (Stage 1-3)**:
- `mortality_microdata_combined.parquet` (54 MB, 28 시점 raw 통합)
- `mortality_panel_v01.parquet` → `v02.parquet` → `v02_marriage/education/occupation.parquet`
- **`mortality_rate_panel_v02_1.parquet`** (6.8 MB, 123,660 rows, **main analysis panel**)

**Stage Mediator (본 conversation 작업)**:
- `mortality_microdata_cleaned_v01.parquet` (19 MB, 7.4M rows)
- `mortality_marital_panel_v01.parquet` (1.6 MB, 1.0M rows)
- `mortality_education_panel_v01.parquet` (1.6 MB, 1.0M rows)
- **`mediator_specific_marital_rate_v01.parquet`** (1.5 MB, 187K rows, **Stage 5 input**)
- **`mediator_specific_education_rate_v01.parquet`** (1.5 MB, 172K rows, **Stage 5 input**)

**Validation reports** (15 md): break_audit, sigungu_collapse, mediator_panel_audit, hira_drug_exploration, etc.

### 2.2 Population (10 file)

- `population_panel_v01.parquet` (한국인 only, 분모, 626 KB)
- `population_panel_v02.parquet` (1.5 MB)
- `foreign_panel_v02.parquet` (외국인 별도)
- `mediator_panel_marriage_v01/v02.parquet` (376 KB / 198 KB)
- `mediator_panel_education_v01/v02/v03.parquet` (651 KB / 209 KB / 172 KB; **v03 = mortality align 3 카테고리**)

### 2.3 Sigungu (3 file)
- step1_anomaly_log/report + codebook_old

---

## 3. 추가 필요 데이터 12 source (PAP v4.0 commit 위한)

**모두 placeholder 폴더 `0_raw/` 안에 신설 완료** (이번 conversation).

### 3.1 🔴 P1 Critical (Stage 5 entry 차단, 6 source) — 모두 placeholder 폴더 0 파일 verify

| # | folder | 파일 수 | 내용 | source / link | 시간 |
|---|--------|---------|------|---------------|------|
| 1 | `kosis_birth_sex_ratio/` | **0** | KOSIS 시군구별 출생 성비 1980-1995 (z_m_marital) | https://kosis.kr → 인구·가구 → 출생 (DT_1B81A21) | ~2h |
| 2 | `edu_university_list_1990/` | **0** | 1990 4년제 대학 list (z_m_education distance) | https://kess.kedi.re.kr 또는 https://www.schoolinfo.go.kr | ~3h |
| 3 | `sigungu_centroid/` | **0** | 시군구 centroid 좌표 | https://www.juso.go.kr 또는 https://github.com/southkorea/southkorea-maps | 30m |
| 4 | `ecos_macro_extra/` | **0** | ECOS 200Y007, 401Y014, 401Y015 (Test 1) | https://ecos.bok.or.kr | ~1h |
| 5 | `imf_weo_korea_vintage/` | **0** | IMF WEO Korea forecast vintage (Test 1b) | https://www.imf.org/.../world-economic-outlook-databases | ~2h |
| 6 | `hs_ksic_concordance/` | **0** | HS6 ↔ KSIC 4-digit 매핑 (Stage 4 Bartik) | https://kssc.kostat.go.kr → 분류 변환 (통계청 응답 대기) | ~1h |

**P1 합계**: ~10 시간 (1-2 작업일).

### 3.2 🟡 P2 Important (SI 통제 변수, 3 source) — 모두 0 파일 verify

| # | folder | 파일 수 | 내용 | source / link | 시간 |
|---|--------|---------|------|---------------|------|
| 7 | `kosis_religion/` | **0** | 시군구 종교 분포 1995/2005/2015 (SI #2) | https://kosis.kr → 인구주택총조사 → 종교 (DT_1IN1502) | ~1h |
| 8 | `kosis_medical_infra/` | **0** | 시군구 의료 인프라 (의사/병상/정신과) (SI #3) | https://kosis.kr → 보건 → 의료기관 (DT_410S0001) / HIRA | ~1h |
| 9 | `nec_election/` | **0** | 시군구 선거 vote share (cultural conservatism, SI #1) | https://www.nec.go.kr → 선거통계시스템 | ~2h |

**P2 합계**: ~4 시간 (Stage 5 진입 전 필수 X, 병행 가능).

### 3.3 🟢 P3 Backup (z_m 후보 fail 시, 3 source) — 모두 0 파일 verify

| # | folder | 파일 수 | 내용 | source / link | 시간 |
|---|--------|---------|------|---------------|------|
| 10 | `mma_conscription/` | **0** | 시군구 군 복무 입대율 (z_m_marital backup) | https://www.mma.go.kr → 통계자료 (정보공개 청구 가능성) | ~3h + 1-2주 |
| 11 | `elis_marriage_subsidy/` | **0** | 지자체 결혼장려/출산장려 정책 timing (backup) | https://www.elis.go.kr (조례 시계열) | ~5h |
| 12 | `moe_university_quota/` | **0** | BK21 정원배분 시도별 시계열 (z_m_education backup) | https://www.moe.go.kr / https://www.nrf.re.kr | ~2h |

**P3 합계**: ~10 시간 (z_m 후보 fail 시만 진행).

---

## 4. 다음 Conversation Entry Point

### 4.1 즉시 진행 가능 (사용자)

이번 주말 (~3 시간):
1. **P1.1** KOSIS 출생성비 다운로드 (KOSIS_API_KEY 사용, 2h)
2. **P1.3** 시군구 centroid GeoJSON 다운로드 (GitHub, 30m)
3. **P1.4** ECOS 신규 시리즈 다운로드 (ECOS_API_KEY 사용, 1h)

다음 주 (~5 시간):
4. **P1.2** 1990 4년제 대학 list 수기 수집 + geocoding (3h)
5. **P1.5** IMF WEO Korea vintage 다운로드 (2h)

대기 중:
6. **P1.6** HS-KSIC concordance 통계청 응답 (1-2 주)

### 4.2 다음 Conversation 의 첫 prompt

다음 conversation 시작 시 R-A 에게 말하기:
> "Trade × Mortality Korea 연구 다시 시작. 본 conversation 마지막 status = PAP v4.0 commit 직전, Phase B-m 데이터 12 source 중 P1 6 수집 진행 중. trade_mortality_korea/DATA_INVENTORY_v01.md + REVIEWER_GUIDE.md + RESEARCH_PROGRESS_v01_en.md 참조."

### 4.3 다음 Conversation 의 첫 작업 후보

1. **데이터 수집 status 확인** (P1 6 source 중 어디까지 다운로드)
2. **P1 데이터 정리 + Phase B-m 진단 시작** (Claude Code 위임)
3. **PAP v3.4 → v4.0 commit** (R-A 직접, ~3 시간)
4. **Stage 5 진입 선결조건 8 항 점검** (v4.0 § 6 patch)
5. **Comtrade 4A 진행 monitor** (ES + CH + CN-World)

---

## 5. 핵심 reference 파일 (next conversation 진입 시 read 권장)

| 파일 | 위치 | 용도 |
|------|------|------|
| **본 문서** | `DATA_INVENTORY_v01.md` (root) | 데이터 status 종합 |
| RESEARCH_PROGRESS (English) | `RESEARCH_PROGRESS_v01_en.md` (root) | 연구 종합 (10K words) |
| RESEARCH_PROGRESS (Korean) | `RESEARCH_PROGRESS_v01.md` (root) | 동일 (한국어) |
| REVIEWER_GUIDE | `REVIEWER_GUIDE.md` (root) | reviewer entry |
| **PAP v4.0** | `4_documentation/PAP/PAP_v4.0_unified_identification_protocol.md` | **최신 protocol (z_x + z_m)** |
| PAP v3.4 (status commit) | `4_documentation/PAP/PAP_2026_05_03_v3.3.md` | 기존 PAP 본문 |
| Reference proposal v01.1 | `4_documentation/PAP/PAP_v3.4_reference_update_proposal_v01.md` | reference 정확화 |
| Stage 5 plan | `4_documentation/stage_plans/stage5_regression_plan_v01.md` | regression spec |
| Mediator pipeline doc | `4_documentation/pipeline_docs/mediator_panel_build_pipeline_documentation_v01.md` | 본 conversation 작업 종합 |
| Reference library master | `4_documentation/reference_library/reference_library_master_v01.md` | 19 paper deep summary |

---

## 6. 본 Conversation 의 주요 산출 (요약)

본 conversation 에서 진행한 것:
- ✅ KOSIS API 12 표 시도 → 시군구 부재 → 폐기
- ✅ MDIS 인구 microdata 7 시점 cleaning + mediator panel build (v01 → v02 → v03)
- ✅ MDIS 사망 microdata 28 시점 cleaning (4 회 재시도, position-based parse)
- ✅ Mortality × mediator cross-tab (working-age 25-64 + sigungu_crosswalk)
- ✅ 5-year stack rate panel (5 period × 6 cause × 4-3 mediator) — Stage 5 input ready
- ✅ HIRA 약물 panel exploration (post-2010 sensitivity)
- ✅ 19 paper deep summaries + reference library master + reference proposal v01.1
- ✅ Reviewer feedback 받음 (P1.A z_m 부재 등 5 critique) + v4.0 채택
- ✅ 데이터 정리 + 다음 conversation entry point commit (본 문서)

---

## 6.1 Cleanup 권고 (R-A 정정 2026-05-04)

### research_materials/2%_표본_인구_20260430_43590_데이터 vs mdis_population_census 동명 폴더

md5 verify 결과 (sandbox bash):

| 시점 | research_materials | mdis_population_census | md5 |
|------|--------------------|------------------------|-----|
| 1990 | 18 MB | **60 MB** | ❌ DIFFERENT (다른 batch) |
| 1995 | 53 MB | 53 MB | ✅ duplicate |
| 2000 | 89 MB | 89 MB | ✅ duplicate |
| 2005 | 101 MB | 101 MB | ✅ duplicate |
| 2010 | 106 MB | **136 MB** | ❌ DIFFERENT (다른 batch) |

**결론**: **삭제 X**. 1990, 2010 의 두 batch 가 다른 파일이라 통째 삭제 시 unique 데이터 손실.

**옵션 A (보존)**: 둘 다 keep, 11 GB 폴더에서 243 MB 절약 minor.
**옵션 B (선택 삭제)**: 3 duplicate (1995, 2000, 2005) 만 research_materials 에서 삭제 (~243 MB 절약), 1990/2010 unique 보존.
**옵션 C (분석 후 결정)**: 1990/2010 의 두 batch 차이 분석 후 main 결정. Stage Mediator 사용한 batch (mdis_population_census) 가 main 일 가능성 높음.

→ **다음 conversation 에서 결정** (지금 삭제 X).

---

## 7. 폴더 구조 종합

```
trade_mortality_korea/
├── 0_raw/                          (26 보유 + 12 placeholder = 38 sub-folder)
│   ├── 1.7  Trade        (3 folder, 6/9 진행)
│   ├── 1.2  Mortality    (2 folder + 사용자 별도 Desktop)
│   ├── 1.3  Population   (5 folder, KOSIS 폐기 1)
│   ├── 1.4  Health       (4 folder, ✅)
│   ├── 1.5  Macro        (3 folder, ⚠️ 1)
│   ├── 1.6  Welfare 등   (4 folder, ✅)
│   ├── 1.7  Reference    (4 folder, ✅)
│   └── ⏳   P1-P3 placeholder (12 folder, 미수집)
│
├── 1_codebooks/                    (7 file)
├── 2_scripts/                      (70+ scripts: data_collection 25, build_panel 14, sigungu 11, verify 13)
├── 3_derived/                      (39 file)
│   ├── mortality/                  (29 file, 9 parquet + 15 md + 5 misc)
│   ├── population/                 (10 file, 8 parquet + 2 md)
│   └── sigungu/                    (3 file)
│
└── 4_documentation/                (60+ md, 7 sub-folder)
    ├── PAP/                        (PAP v1-v3.4 + reference proposal + **v4.0**)
    ├── reference_library/          (master + 19 paper summaries)
    ├── stage_plans/                (Stage 5 + writing guides)
    ├── pipeline_docs/              (mediator + panel construction)
    ├── status_reports/             (daily status + handoff)
    ├── crosswalks_paper/           (claude code prompts)
    └── misc/                       (research_proposal)

root/
├── README.md                       (project overview)
├── REVIEWER_GUIDE.md               (5분 entry)
├── REVIEWER_FEEDBACK_TEMPLATE.md   (template)
├── REVIEWER_PROMPT.md              (v01 paper 평가)
├── REVIEWER_PROMPT_v02.md          (v02 R-A 작업 + paper)
├── RESEARCH_DESCRIPTION_WRITER_PROMPT.md  (v03 meta)
├── RESEARCH_PROGRESS_v01.md        (한국어 10K)
├── RESEARCH_PROGRESS_v01_en.md     (English 10K)
└── DATA_INVENTORY_v01.md           (본 문서)
```

---

_본 문서 = 본 conversation 의 마지막 commit. 다음 conversation 진입 시 entry point._
_저자: 정재헌 (Jae-Heon Jeong, 가천대 경제학부) + R-A (Claude LLM)_
_작성: 2026-05-04, conversation hand-off._
