# 🔄 Conversation Hand-off — Trade × Mortality Korea

_본 문서: 본 conversation 의 마지막 commit. 다음 conversation 의 **단일 entry point**._
_작성: 2026-05-04, 정재헌 (Jae-Heon Jeong) + R-A (Claude LLM)_

---

## 0. 다음 Conversation 첫 prompt (사용자 paste 용)

```
Trade × Mortality Korea 연구 다시 시작.

본 conversation 이전의 마지막 status:
- PAP v4.0 unified identification protocol commit 직전
- Stage 1-3 + Mediator panel 완료 (24 parquet)
- Stage 4 Comtrade 100% 완료 (275 파일), HS-KSIC concordance 통계청 응답 대기
- z_x + z_m 두 instrument framework 채택 (DGHP 2017 + DFH 2020 ivmediate)
- Phase B-m 데이터 12 source 중 P1 6 미수집 (placeholder 폴더 신설 완료)

진입 전 read 권장:
1. C:\Users\82103\Downloads\trade_mortality_korea\HANDOFF.md (본 문서)
2. C:\Users\82103\Downloads\trade_mortality_korea\DATA_INVENTORY_v01.md
3. C:\Users\82103\Downloads\trade_mortality_korea\4_documentation\PAP\PAP_v4.0_unified_identification_protocol.md

오늘 진행할 task: [사용자가 명시]
```

---

## 1. 현재 Status — 한 눈 보기

### Stage Status

| Stage | status | 다음 step |
|-------|--------|-----------|
| Stage 1-3 main outcome panel | ✅ 완료 (123,660 rows, 229 h_code) | - |
| Stage Mediator | ✅ 완료 (5 parquet, 본 conversation 작업) | - |
| Stage 4 Bartik IV | ✅ Comtrade 275 파일, ⏳ HS-KSIC concordance 대기 | 통계청 응답 |
| Stage 5 ivmediate regression | spec ready (v4.0), ⏳ 진입 대기 | Stage 4 + Phase B-m + B-SI 완료 후 |

### Stage 5 진입 선결조건 (8 항, PAP v4.0 § 5)

| # | 항목 | status |
|---|------|--------|
| 1 | z_x first-stage F ≥ 10 (ADH-8 또는 bilateral) | ⏳ Stage 4 완료 후 |
| 2 | z_m_marital first-stage F ≥ 10 | ⏳ Phase B-m 데이터 수집 후 |
| 3 | z_m_education first-stage F ≥ 10 | ⏳ 동일 |
| 4 | z_x ⊥ z_m correlation < 0.3 | ⏳ |
| 5 | z_m ⊥ mortality residual ≈ 0 (Test 4) | ⏳ |
| 6 | z_m pre-trend test PASS (Test 5) | ⏳ |
| 7 | denom missing 67 h_code 진단 | ⏳ R-A pending |
| 8 | KR-CN bilateral IV exclusion (Test 1/1b/2/3) | ⏳ ECOS + WEO 데이터 후 |

---

## 2. 본 Conversation 의 핵심 변화

### Before (PAP v3.4)
- Mediation = paper main contribution (한국 first DGHP/DFH ivmediate)
- z_x (Bartik IV) 만 protocol 화, **z_m 미정의** (식별 black hole)
- 학부생 단독 저자 SSCI Q1 push

### After (PAP v4.0)
- **z_x + z_m 두 instrument framework** 명시 (A1-A4 + Sequential Ignorability)
- z_m 후보 commit:
  - **z_m_marital = 시군구 출생 성비 cohort lag** (Park-Cho 1995, Edlund-Lee 2009 외생성)
  - **z_m_education = distance-to-college** (Bound-Jaeger 1996, Currie-Moretti 2003)
- **Joint pre-commit decision tree (12+ branch)** — post-hoc IV switching 금지
- 본문 contribution = **조건부**:
  - Best case (z_x A × z_m αm): mediation main (paper § 5.2)
  - Worst case (z_m γm 또는 A4 reject): reduced-form main, mediation = appendix only
- → 학술 honest, SSCI Q1 target 동일 유지

---

## 3. 데이터 Status (DATA_INVENTORY_v01.md 참조)

### 보유 데이터 (✅, 26 sub-folder, 11 GB)

| 우선 활용 | folder | size | 용도 |
|-----------|--------|------|------|
| 🔴 1 | `kosis_business_survey/` | **1.6 GB** (94 file) | Stage 4 Bartik first-stage 의 산업별 시군구 share |
| 🔴 2 | `comtrade_*/` | 275 파일 (KR-CN 50 + ADH 200 + CN-World 25) | Bartik IV shock |
| 🔴 3 | `mdis_population_census/` | 1.2 GB | mediator denominator (사용 완료) |
| 🔴 4 | `Desktop/지역별 자살 데이터/` | 사용자 별도 | mortality microdata (사용 완료) |
| 🟡 | `hira_drug/` | 4 파일 | post-2010 sensitivity mediator |
| 🟡 | `ecos_household_credit/`, `ecos_delinquency/` | small | Sufi 2023 household debt sensitivity |

### 미수집 데이터 (⏳, 12 placeholder 폴더 신설 완료)

🔴 **P1 6 source** (Stage 5 entry 차단, ~10 시간):

| # | folder | 다운로드 link |
|---|--------|---------------|
| 1 | `kosis_birth_sex_ratio/` | https://kosis.kr → 인구·가구 → 출생 (DT_1B81A21) |
| 2 | `edu_university_list_1990/` | https://kess.kedi.re.kr → 고등교육 → 학교현황 |
| 3 | `sigungu_centroid/` | https://github.com/southkorea/southkorea-maps (GeoJSON) |
| 4 | `ecos_macro_extra/` | https://ecos.bok.or.kr (200Y007/401Y014/015) |
| 5 | `imf_weo_korea_vintage/` | https://www.imf.org/.../world-economic-outlook-databases |
| 6 | `hs_ksic_concordance/` | https://kssc.kostat.go.kr (통계청 응답 대기) |

🟡 **P2 3 source** (SI 통제 변수): kosis_religion, kosis_medical_infra, nec_election

🟢 **P3 3 source** (z_m backup): mma_conscription, elis_marriage_subsidy, moe_university_quota

---

## 4. ⚠️ Pending Critical Issues 6

| # | issue | severity | action |
|---|-------|----------|--------|
| 1 | HS-KSIC concordance 통계청 응답 | 🔴 | 통계청 follow-up |
| 2 | z_m 후보 데이터 6 source 수집 (P1) | 🔴 | 사용자 다운로드 ~10h |
| 3 | denom missing 67 h_code 진단 | 🟡 | Claude Code 위임 ~1h |
| 4 | Stata 환경 verify (가천대 + 7 package) | 🟡 | ~30m |
| 5 | research_materials/2%_표본_인구 vs mdis_population_census 의 1990/2010 batch 차이 분석 (md5 다름 confirm) | 🟢 | ~30m, 다음 conversation |
| 6 | PAP v3.4 → v4.0 commit (본문 + footnote) | 🟢 | R-A 직접 ~3h |

---

## 5. ⚠️ R-A oversight 회피 (본 conversation lesson)

본 conversation 에서 R-A 가 한 mistake (**다음 conversation 에서 반복 회피**):

### 5.1 mortality 11a column rename 4 회 재시도 (Stage Mediator)
- 1997-2007 의 column 명 invisible char issue 진정 root cause 미확정
- Position-based parse (column index 직접) 로 우회
- → **lesson**: column rename fail 시 즉시 position-based fallback (4 회 재시도 X)

### 5.2 데이터 삭제 권고 md5 verify 안 함
- research_materials/2%_표본_인구... = mdis_population_census 와 size 같다고 ~600 MB "중복" 삭제 권고
- 사용자 critique 후 md5 verify → 1990/2010 다른 batch 발견
- → **lesson**: 삭제 권고 전 md5sum 또는 column hash verify 필수 (memory: `feedback_data_deletion_md5_verify.md` saved)

### 5.3 PAP § 14 dated change log 미참조 (reference proposal v01)
- GPSS 2018 → 2020 AER, DGHP+DFH 둘 다, OP test 23.1 = TSLS bias (NOT size distortion)
- 사용자 round 7 audit critique 후 v01.1 정정
- → **lesson**: PAP § 14 verification commit 사전 확인 후 reference 작성

### 5.4 Stage Reference 작성 시 1 paper 만 deep read (sub-agent 효율 핑계)
- 5 sub-agent parallel 호출 후 19/20 paper 모두 deep read 강제
- → **lesson**: sub-agent 에 명확 instruction (skip 시 fail) + 토큰 효율 핑계 거부

### 5.5 v3.6 z_m draft 작성 (R-A) 후 v4.0 (외부) 의 superior version 등장
- R-A v3.6 = 종교 + 대학 시설 밀도 (학술 외생성 변호 약함)
- v4.0 = 출생 성비 + distance-to-college (Park-Cho 1995, Bound-Jaeger 1996 강력 reference)
- → **lesson**: 외부 reviewer / colleague 의 outside critique 우선 채택 (R-A first attempt 가 항상 best 아님)

---

## 6. Workflow 메모리 (다음 conversation 에서 적용)

memory `feedback_workflow_claude_code_division.md` 기반:

| Role | 담당 |
|------|------|
| **Claude Code (별도 IDE)** | substantive 코딩 — pandas pipeline, panel build, validation script |
| **R-A (본 conversation)** | orchestration only — Claude Code prompt 작성, log 검토, 사용자 명령 제공 |
| **사용자 (정재헌)** | messenger — Claude Code 실행 + log paste, R-A 명령 실행 + 결과 paste |

**R-A 직접 (script 작성 X)**:
- file copy (sandbox bash)
- inventory check
- documentation 작성 (.md)
- validation report

**Claude Code 위임 (R-A 가 prompt 만)**:
- panel build (multi-step pandas)
- raw parsing (encoding, position-based)
- cross-tab + merge
- 복잡 statistical script

---

## 7. 핵심 산출물 Inventory (다음 conversation read 권장)

### 7.1 Top priority (entry 시 5 분 read)
- **HANDOFF.md** (본 문서, root)
- **DATA_INVENTORY_v01.md** (root, data status)

### 7.2 Paper framework (Stage 5 spec)
- **PAP v4.0** (`4_documentation/PAP/PAP_v4.0_unified_identification_protocol.md`) — 최신 protocol (z_x + z_m + SI)
- PAP v3.4 status commit (`4_documentation/PAP/PAP_2026_05_03_v3.3.md`) — 본문
- Reference proposal v01.1 (`4_documentation/PAP/PAP_v3.4_reference_update_proposal_v01.md`) — reference 정확화
- Stage 5 plan (`4_documentation/stage_plans/stage5_regression_plan_v01.md`) — regression spec

### 7.3 본 conversation 의 작업 종합
- Mediator pipeline doc (`4_documentation/pipeline_docs/mediator_panel_build_pipeline_documentation_v01.md`)
- Reference library master (`4_documentation/reference_library/reference_library_master_v01.md`, 14,500 단어)
- 19 paper deep summaries (`4_documentation/reference_library/paper_summaries/`)

### 7.4 Reviewer entry pipeline
- REVIEWER_GUIDE.md (5분 entry)
- REVIEWER_FEEDBACK_TEMPLATE.md
- REVIEWER_PROMPT.md / REVIEWER_PROMPT_v02.md / RESEARCH_DESCRIPTION_WRITER_PROMPT.md
- RESEARCH_PROGRESS_v01.md (한국어, 10K)
- RESEARCH_PROGRESS_v01_en.md (English, 10K)

### 7.5 데이터 (Stage 5 input)
- `mediator_specific_marital_rate_v01.parquet` (187K rows, ivmediate input)
- `mediator_specific_education_rate_v01.parquet` (172K rows)
- `mortality_rate_panel_v02_1.parquet` (123,660 rows, main outcome)

---

## 8. 다음 Conversation 의 우선순위 작업 (사용자 결정)

### Path A — 데이터 수집 우선 (~10 시간 사용자 작업)
1. KOSIS 출생성비 (P1.1, 2h) ← **가장 critical**
2. 시군구 centroid GeoJSON (P1.3, 30m)
3. ECOS 신규 시리즈 (P1.4, 1h)
4. 1990 4년제 대학 list (P1.2, 3h)
5. IMF WEO Korea vintage (P1.5, 2h)
6. HS-KSIC concordance (통계청 응답 대기)

### Path B — Documentation 우선 (R-A 작업 ~5 시간)
1. PAP v3.4 → v4.0 commit (본문 + footnote, ~3h)
2. v4.0 § 9 사용자 review 체크리스트 6 항 결정 + 반영
3. Reference list 26 entry 적용 (proposal v01.1 의 7 항)
4. Limitation 8 항 paper § 8 추가

### Path C — Substantive 분석 (Claude Code 위임 ~7 시간)
1. denom missing 67 h_code 진단
2. HIRA T3-T4 sensitivity panel build (post-2010)
3. research_materials vs mdis 의 1990/2010 batch 차이 분석
4. ksic_business_survey (1.6 GB) initial exploration

### Path D — 외부 Review pipeline (사용자 작업)
1. RESEARCH_PROGRESS_v01_en.md + 4 첨부 → reviewer share
2. Reviewer feedback 받음 → NEXT_STEP_PROMPT 본 R-A 에 paste

---

## 9. 정리 — 모든 메모리 (next conversation 적용)

`MEMORY.md` 의 feedback 7 항 (모두 next conversation 자동 적용):

1. **panel build / 매핑 시 codebook 사전 참고 필수** — raw 폴더의 파일설계서/시군구코드집/8차분류 등 사전 inspect
2. **workflow — Claude Code 가 코딩, R-A 가 orchestration, 사용자가 실행**
3. **my paper 피드백 모드** — P1/P2/P3 분류, over-critic 금지, NEXT_STEP_PROMPT 첨부
4. **박사논문 skill·plugin 운용** — phase 별 자동 활용 매핑
5. **데이터 삭제 권고 시 md5 verify 필수** ← **본 conversation 에서 추가**
6. **skill 활용 범위 — 본 학술 분석에 적합한 것만** — product-tracking/bigdata/box/productivity 무관
7. **paper 기존 메모리** — 104 codebook, ICD-10 F10-F19, reference library 20편 등

---

## 10. 폴더 구조 종합 (다음 conversation entry)

```
trade_mortality_korea/
├── HANDOFF.md                              ← 본 문서 (단일 entry)
├── DATA_INVENTORY_v01.md                   ← 데이터 status
├── README.md                               (project overview)
├── REVIEWER_GUIDE.md                       (reviewer entry)
├── REVIEWER_FEEDBACK_TEMPLATE.md
├── REVIEWER_PROMPT.md / REVIEWER_PROMPT_v02.md / RESEARCH_DESCRIPTION_WRITER_PROMPT.md
├── RESEARCH_PROGRESS_v01.md / _en.md       (한국어 + English 10K)
│
├── 0_raw/                                  (38 sub-folder, 792 file, 11 GB)
│   ├── 26 보유 (Stage 1-3 + Mediator + Comtrade 100%)
│   └── 12 placeholder (P1 6 + P2 3 + P3 3, 미수집)
│
├── 1_codebooks/                            (7 file)
├── 2_scripts/                              (82 python, 9 sub-folder)
├── 3_derived/                              (48 file, 23 parquet)
└── 4_documentation/                        (66 md, 7 sub-folder)
    ├── PAP/                                ← PAP v1-v3.4 + reference proposal + **v4.0** ← 핵심
    ├── reference_library/                  (master + 19 paper summaries)
    ├── stage_plans/                        (Stage 5 regression plan)
    ├── pipeline_docs/                      (mediator pipeline)
    ├── status_reports/                     (daily status)
    ├── crosswalks_paper/
    └── misc/
```

---

## 11. 본 Conversation 의 Major Outputs (chronological)

1. ✅ KOSIS API 12 표 시도 → 시군구 부재 → MDIS 전환
2. ✅ MDIS 인구 microdata 7 시점 cleaning + mediator panel build (v01 → v02 → v03)
3. ✅ MDIS 사망 microdata 28 시점 cleaning (4 회 재시도, position-based parse, 외국인만 drop)
4. ✅ Mortality × mediator cross-tab (working-age 25-64 + sigungu_crosswalk)
5. ✅ 5-year stack rate panel (5 period × 6 cause × 4-3 mediator) — Stage 5 input ready
6. ✅ HIRA 약물 panel exploration (post-2010 sensitivity)
7. ✅ 19 paper deep summaries + reference library master (14,500 단어)
8. ✅ Reference proposal v01 → v01.1 (3 issue 정정: GPSS 2020, DGHP+DFH 둘 다, OP test TSLS bias)
9. ✅ Reviewer feedback P1-P3 받음 (z_m 부재 = 가장 critical)
10. ✅ R-A v3.6 z_m draft 작성
11. ✅ 외부 v4.0 unified identification protocol 채택 (R-A v3.6 supersede)
12. ✅ Folder cleanup (뉴 논문 → 4_documentation/, 7 sub-folder 정리)
13. ✅ Comtrade 4A 100% 완료 (KR-CN + ADH 8 + CN-World, 275 파일)
14. ✅ DATA_INVENTORY_v01.md (38 sub-folder, 792 file, 11 GB)
15. ✅ HANDOFF.md (본 문서, 다음 conversation entry)
16. ✅ Memory 7 feedback 저장 (md5 verify, skill scope, workflow, codebook reference, paper review mode 등)

---

_본 HANDOFF.md = 본 conversation 의 마지막 commit. 다음 conversation 첫 prompt 의 read 권장 순서:_
_1. HANDOFF.md (본 문서, 5 분)_
_2. DATA_INVENTORY_v01.md (3 분)_
_3. PAP v4.0 (15 분)_

_저자: 정재헌 (Jae-Heon Jeong) + R-A (Claude LLM)_
_작성: 2026-05-04, conversation hand-off 완료_
