# Meta Prompt — 연구 상황 설명 문서 작성 Instruction

_본 프롬프트를 다른 LLM (또는 본 R-A) 에 paste → 산출 = "RESEARCH_PROGRESS_v01.md" 문서 (~10,000 단어, reviewer 에게 share 용)._
_작성: 2026-05-04. v01/v02 와 차이: v01/v02 = reviewer 가 직접 받는 prompt. **v03 = LLM 이 받아서 연구 상황 설명 문서를 산출** 하는 instruction._

---

## ─────────────────────────────────────────
## 메타 프롬프트 시작 (이 아래를 LLM 에게 paste)
## ─────────────────────────────────────────

# 연구 상황 자세한 설명 문서 작성 Task

## 0. 당신의 Role + Task

당신은 본 연구의 **technical ghostwriter / progress documentor**. 다음 두 input 을 활용해 박사급 학자 reviewer 가 1-3 시간 review 후 detailed structured feedback 작성 가능한 수준의 **self-contained 연구 상황 설명 문서** 를 산출.

### Input
1. **연구 폴더 access**: `C:\Users\82103\Downloads\trade_mortality_korea\` (50+ folder, 1000+ file, 24 parquet, 70+ script, 60+ md)
2. **본 메타 프롬프트의 § 2-7** (연구 context, 작성 구성, 원칙, 산출 형식)

### Output
- 단일 markdown 파일: `RESEARCH_PROGRESS_v01.md` (~10,000 단어, ~30 페이지)
- 폴더 root 에 저장
- reviewer 가 standalone 으로 본 연구의 가설/데이터/방법/진행/결과/한계 모두 정확 파악 가능

---

## 1. 연구 Meta (LLM 이 알아야 할 background)

### 1.1 Paper meta
- **제목**: "Trade Shock and Deaths of Despair in Korea: Quantifying the Underexplored Family-Mediated Channel"
- **저자**: 정재헌 (Jae-Heon Jeong), 가천대학교 경제학부 학부생 (단독 저자, SSCI 지향)
- **현재 status**: PAP v3.4 status commit, Stage 1-3 + Mediator 완료, Stage 4 Bartik IV 진행 중

### 1.2 핵심 가설
> 한국의 deaths of despair (자살 102 + 약물 101 + 정신 057 + 간 081, KCD 8차분류) 는 무역 충격 (Bartik shift-share IV) 의 인과적 영향을 받음. 그 영향의 일부는 가족 mediator (혼인 분해 marital_code, 교육 attainment education_band) 를 통해 전달됨. (DGHP 2017 + DFH 2020 ivmediate framework)

### 1.3 Novelty 4 영역
1. 한국 first of Trade × Mortality × Mediator 통합 분석
2. Family channel novelty (Hanson 2018 의 한국 individual-level 확장)
3. 한국 vs US dominance 차이 (한국 = 자살+간, US = 약물)
4. DGHP 2017 + DFH 2020 ivmediate 의 한국 first 적용

---

## 2. 작성할 RESEARCH_PROGRESS 문서의 권장 구성 (15 sections)

각 section 의 분량 + 내용 필수 항목:

### § 1 Executive Summary (300 단어)
- 핵심 가설 1 paragraph
- Novelty 4 영역 1 paragraph
- 진행 status (Stage 1-3 완료, Stage 4 진행, Stage 5 spec ready)
- 핵심 preliminary finding (deaths of despair 시계열 + 한국 vs US)

### § 2 Research Question + Hypothesis (500 단어)
- Main question + 4 sub-hypothesis
- Novelty position vs Pierce-Schott 2020 (US, mediation X), Finkelstein 2026 (NAFTA, all-cause만), Hanson 2018 (US ecological), Case-Deaton 2015 (US deaths of despair 정의 source)
- 한국 setting 의 unique 측면 (working-age 25-64, OECD 최고 자살률, 약물 매우 낮음)

### § 3 Literature Position (800 단어)
- Tier 1 reference (10): 각 1-2 문장 + 본 paper 와의 connection
- Tier 2 reference (5): brief
- Tier 3 reference (4): mention
- 본 paper 가 fill 하는 gap 명시

### § 4 Data Sources (1500 단어)
6 source 각 paragraph 1 개:
1. **MDIS 사망원인통계 microdata** (1997-2024, 28 시점, individual death) — sgguCd, 사망연령5세, 혼인, 교육, cause_104. 사용자 신청.
2. **MDIS 인구주택총조사 2% 표본 microdata** (1990-2020, 7 시점, individual) — sgguCd, 성, 연령, 혼인, 교육, 가중값. 사용자 신청.
3. **Comtrade Bartik IV** (1995-2024, HS6 trade) — KR-CN bilateral + ADH 8 ← CN + CN-World. 진행 중.
4. **KOSIS API mediator** — 시군구 부재 발견, 폐기.
5. **HIRA 약물 처방** (2010-2019, 시군구 × 월 × ATC4) — 정신과 mediator sensitivity, post-2010 only.
6. **ECOS 가계부채** (2003-2024, sido) — household debt sensitivity (Sufi 2023 channel).

### § 5 Data Pipeline (1500 단어)

**Stage 1-3 main outcome panel** (이미 commit):
- mortality 28 시점 raw → cleaning → component decomposition 10 outcome group
- 분구 시군구 합산 (sigungu_crosswalk_v2: 안산 31090, 용인 31190)
- 외국인 빼기 제거 (panel v01 자체가 한국인 only KOSIS DT_1B040M5 와 -0.35% 차이)
- 산출: `mortality_rate_panel_v02_1.parquet` (123,660 rows, 229 h_code)

**Stage Mediator** (본 conversation 작업 결과):
- KOSIS API 시도 → 시군구 부재 발견 → MDIS 전환
- MDIS 인구 microdata 7 시점 cross-tab → mediator denominator
- 1990 drop, working-age 25-64 filter, education 4 → 3 카테고리
- mortality 28 시점 cleaning (position-based parse, 외국인 drop)
- mortality × mediator cross-tab → numerator
- 5-year stack period × census year 매핑 → rate panel
- 산출 5 parquet (위 § 4 참조)

**Stage 4 Bartik IV** (진행 중):
- Comtrade KR-CN + ADH 8 (AU/DK/FI/DE/JP/NZ/ES/CH) ← CN + CN-World
- HS-KSIC concordance (통계청 응답 대기)
- HS 28-97 manufacturing focus (ADH 표준)

**Stage 5 regression** (spec ready, 진입 대기):
- ivmediate (DGHP 2017 + DFH 2020) Stata implementation
- 5-layer SE + Romano-Wolf

### § 6 Identification Strategy (1000 단어)

**§ 5.1 Bartik shift-share IV** (PAP § 5):
- 핵심 spec equation
- GPSS 2020 share exogeneity vs BHJ 2022 shock-level orthogonality
- ADH 8 ← CN imports + KR-CN 직접 trade
- HS-KSIC concordance (통계청 응답 대기)

**§ 5.2 Mediation** (DGHP 2017 + DFH 2020):
- ivmediate Stata package spec (theoretical framework + implementation source 둘 다)
- Direct/indirect/total effect 분해
- z_x (lagged shift-share) + z_m (mediator-specific IV, 후보 진단 중)

**§ 6 Empirical spec**:
- 5-year stacked first-difference (Pierce-Schott 2020 Eq. 3)
- 5 stack period: 1997-2001, ..., 2017-2021

**§ 7 5-layer SE + weak IV**:
- HC1 + WCB-sigungu (n=229) + WCB-sido (n=16) + AKM (BHJ 2022) + Conley
- OP test F=23.1 cutoff (5% TSLS bias relative to OLS, NOT size distortion)
- AR + tF (Andrews-Stock-Sun 2019)
- Romano-Wolf step-down (4 outcome × 2 mediator dim = 8, + all_cause = 9?)

### § 7 Empirical Findings — Preliminary (1000 단어)

**Deaths of despair 시계열** (working-age 25-64, /100K annual):
| period | drug | liver | psych | suicide |
|--------|------|-------|-------|---------|
| 1 (1997-2001) | 5.61 | **44.17** | 13.29 | 23.23 |
| 2 (2002-2006) | 4.01 | 34.26 | 10.62 | 28.26 |
| 3 (2007-2011) | 3.81 | 26.44 | 9.85 | **35.27** |
| 4 (2012-2016) | 3.85 | 22.69 | 8.93 | 32.89 |
| 5 (2017-2021) | 3.86 | 19.05 | 9.66 | 29.61 |

**Historical 검증**:
- ✅ 자살 peak 2007-2011 = 한국 통계청 일치 (카드사태 2003 + 글로벌 금융위기 2008-2010)
- ✅ 간질환 -57% 단조 감소 (B형 간염 백신 + 의료 발전)
- ✅ 약물 매우 낮음 (US 의 1/10) → **한국 ≠ US 핵심 finding**
- ✅ all_cause 277 → 152 / 100K (-45%)

**Mediator-specific rate panel** (h_code × period × sex × age × marital × cause × rate):
- 187,379 rows (marital), 171,811 rows (education)
- Stage 5 ivmediate input ready

### § 8 Limitations 8 항 (1000 단어)

각 limitation 의 origin + impact + mitigation:
1. 1990 sigungu code (2자리) mapping placeholder — 1990 mediator 미사용, minor
2. 1997-2007 외국인 식별 불가 (변수 부재) — < 0.5% inflation 추정
3. 혼인/교육 미상 (코드 9) drop — MAR 가정, sensitivity test 권장
4. Education 1997-2007 5 → 2008+ 7 카테고리 → 3 통합 align — 정보 손실
5. 2022-2024 incomplete period drop — 5-year stack 미완성
6. MDIS 2% 표본 weight ±5% 오차
7. denom missing 9.74% (marital) — 67 h_code 진단 미완
8. 2024 시점 252 h_code (sigungu_crosswalk 미cover) — main analysis 1997-2021 무관

### § 9 Pending Issues 4 항 (500 단어)
1. Stage 4 Comtrade + HS-KSIC concordance (통계청 응답 대기)
2. denom missing 67 h_code 진단
3. Stata 환경 verify (가천대 + 7 package)
4. PAP v3.4 → v3.5 update (reference proposal v01.1 적용)

### § 10 R-A Decisions Log 16 항 (1000 단어)
각 결정의 reasoning + alternative + chose 이유:
1. KOSIS 폐기 → MDIS 전환
2. 1990 mediator drop
3. age 25-64 filter
4. Education 3 카테고리 통합
5. Position-based parse (column rename fail 후)
6. 외국인 "2" 만 drop (NaN/빈 keep)
7. 혼인 9 drop
8. 교육 9 drop
9. Education align 3 카테고리
10. 5-year stack period
11. Rate formula (annual per 100K)
12. 6 cause group (deaths of despair 4 + other + all_cause)
13. denom missing listwise deletion (vs imputation)
14. GPSS 2020 publish primary
15. DGHP 2017 + DFH 2020 둘 다 cite
16. OP test F=23.1 = TSLS bias (NOT size distortion)

### § 11 Issue Resolution Log 7 항 (500 단어)
1. KOSIS 시군구 부재 → MDIS 전환
2. 1997-2007 column rename fail → position-based parse
3. national_code NaN → 외국인만 drop
4. 1990 sigungu 2자리 → drop
5. denom missing 9.74% → listwise deletion
6. Reference v01 inconsistency → v01.1 정정
7. PAP § 14 dated change log mismatch → 정정

### § 12 Reference Library Summary (500 단어)
- 19 paper deep summaries 종합 + Tier A/B/C
- PAP § 별 reference 매핑 table
- Citation strategy

### § 13 Output Inventory (500 단어)
- 24 derived parquet (mortality, population, mediator panel, rate panel)
- 70+ scripts (data_collection, build_panel, sigungu_crosswalk, verify)
- 60+ documentation (PAP, reference, summaries, status, pipeline)
- 폴더 구조 (4_documentation/ 7 sub-folder)

### § 14 Future Work + Timeline (500 단어)
- Stage 4 Comtrade 완료 (통계청 응답 후 1-2 주)
- Stage 5 ivmediate regression 진입 (Stata 환경 verify 후)
- Robustness check (HIRA T3-T4, Romano-Wolf, 5-layer SE)
- Paper 작성 (Stage 5 결과 후, 1-2 개월)
- SSCI submission target (AEJ Applied / JHE / Health Economics)
- 단독 학부생 first-author SSCI publish 가능성 평가

### § 15 Appendix (500 단어)
- 핵심 panel structure (mediator_specific_rate_v01 의 column + dimension)
- 5 stack period × mediator census 매핑 table
- ivmediate Stata code sketch
- 4 figure (deaths of despair 시계열, suicide by marital, mediator-specific rate by marital, ATC4 by year)

---

## 3. 작성 원칙 5 가지 (필수 enforce)

### 3.1 Self-contained
- 본 paper 의 prior conversation context 없이도 reviewer 가 이해 가능
- 모든 abbreviation 첫 사용 시 expansion (예: "MDIS (Microdata Integrated Service, 통계청 마이크로데이터 통합서비스)")
- 모든 reference 첫 cite 시 full citation (저자, 년, 학술지)

### 3.2 Quantitative
- 수치 + table 명시 (정성적 narrative 만 X)
- 각 panel 의 row count, h_code count, 시점 range, dimension cardinality 명시
- 각 finding 의 magnitude (예: "자살 peak 35.27/100K", "약물 5.61 → 3.86 -31%")
- statistical significance 미산출 시 명시 ("Stage 5 진입 후 산출")

### 3.3 Reproducible
- 모든 작업의 file path 명시 (`3_derived/mortality/mediator_specific_marital_rate_v01.parquet`)
- 모든 script path 명시 (`2_scripts/data_collection/12_mediator_specific_mortality_rate.py`)
- 모든 결정의 reasoning + commit 시점 명시
- 모든 데이터의 source + 신청 history

### 3.4 Honest
- limitation 8 항 명시 (over-promise X)
- pending 4 항 명시 (uncertainty 솔직히)
- R-A 의 4 회 재시도 history (Stage 11a) 명시 (failure transparent)
- single-author 학부생 publish 어려움 명시

### 3.5 Citation Accurate
- PAP v3.3 § 14 dated change log + reference proposal v01.1 의 commit 일관
- GPSS 2020 AER (NBER 24408 working) — publish primary
- DGHP 2017 NBER 23209 + DFH 2020 Stata Journal 20(3) — 둘 다 cite
- OP test F=23.1 = 5% TSLS bias (Stock-Yogo Cragg-Donald F=23 robust 확장, Olea-Pflueger 2013) NOT size distortion

---

## 4. 작성 도구 + 접근

연구 폴더 read 후 작성:
- 4 핵심 첨부 (PAP v3.4, reference proposal v01.1, mediator pipeline doc, Stage 5 plan) 사전 read
- 19 paper deep summaries (Tier A 우선) 참조
- 24 parquet 의 핵심 column + row count verify (Read tool 또는 pandas)
- REVIEWER_GUIDE.md + REVIEWER_FEEDBACK_TEMPLATE.md 와 cross-reference

---

## 5. 작성 후 deliver

### 산출 파일
- `C:\Users\82103\Downloads\trade_mortality_korea\RESEARCH_PROGRESS_v01.md`
- ~10,000 단어 (~30 페이지 markdown)

### 검증 항목
- 15 sections 모두 cover (체크리스트)
- 작성 원칙 5 가지 enforce (self-contained / quantitative / reproducible / honest / citation accurate)
- LLM context window 의 5-10% (LLM input 적정)

### Reviewer 가 받을 것 (본 RESEARCH_PROGRESS 와 함께 share)
1. 본 RESEARCH_PROGRESS_v01.md (10,000 단어)
2. 4 핵심 첨부:
   - `4_documentation/PAP/PAP_2026_05_03_v3.3.md` (PAP v3.4 본문, ~30p)
   - `4_documentation/PAP/PAP_v3.4_reference_update_proposal_v01.md` (reference v01.1, ~15p)
   - `4_documentation/pipeline_docs/mediator_panel_build_pipeline_documentation_v01.md` (~25p)
   - `4_documentation/stage_plans/stage5_regression_plan_v01.md` (~30p)
3. 보조 (관심 paper 만):
   - 19 paper deep summaries
   - Reference library master (14,500 단어)
   - Validation reports

### Reviewer 가 산출할 것
- detailed structured feedback (P1/P2/P3 tagged, NEXT_STEP_PROMPT 첨부)
- 1-3 시간 review 후 작성 가능

---

## 6. Output Format Specification

### Markdown 구조
```markdown
# RESEARCH_PROGRESS_v01 — Trade × Mortality Korea

_작성: YYYY-MM-DD_
_저자: 정재헌 (가천대 학부) + R-A (Claude LLM)_
_status: PAP v3.4 commit, Stage 1-3 + Mediator 완료, Stage 4 진행_

---

## 1. Executive Summary
[300 단어]

## 2. Research Question + Hypothesis
[500 단어]

[... 15 sections]

## 15. Appendix
[500 단어]

---

_본 문서 = paper 의 self-contained progress 설명. reviewer 가 detailed feedback 작성 위한 단일 entry point._
```

### Quality check (작성 후 self-check)
- [ ] 15 sections 모두 cover
- [ ] Total word count 9,000-11,000 (target 10,000)
- [ ] 모든 abbreviation expansion 첫 사용 시
- [ ] 모든 file path 명시 (parquet, script, md)
- [ ] 모든 reference full citation 첫 cite 시
- [ ] PAP § 14 dated change log + reference proposal v01.1 와 일관
- [ ] limitation 8 항 + pending 4 항 모두 명시
- [ ] R-A decisions 16 항 + issue resolution 7 항 모두 명시
- [ ] 한국어 위주 (사용자 preference) + 영어 reference / quote / table

---

## 7. 작성 metadata

작성 후 산출 파일 frontmatter:
```yaml
---
title: RESEARCH_PROGRESS_v01 — Trade × Mortality Korea
author: 정재헌 (가천대 학부) + R-A (Claude LLM)
date: YYYY-MM-DD
version: v01
target: reviewer feedback (SSCI submission readiness)
status: PAP v3.4 commit, Stage 1-3 + Mediator 완료, Stage 4 진행
related:
  - PAP_2026_05_03_v3.3.md
  - PAP_v3.4_reference_update_proposal_v01.md
  - mediator_panel_build_pipeline_documentation_v01.md
  - stage5_regression_plan_v01.md
---
```

---

## ─────────────────────────────────────────
## 메타 프롬프트 끝
## ─────────────────────────────────────────

_본 v03 메타 프롬프트는 v01/v02 와 차이 = LLM 이 받아서 "RESEARCH_PROGRESS_v01.md" 산출. 그 산출 문서를 reviewer 에게 share → reviewer 가 detailed feedback 작성._

_사용 흐름:_
1. _본 메타 프롬프트 LLM 에게 paste → LLM 이 RESEARCH_PROGRESS_v01.md 산출 (~1-2 시간 작업)_
2. _RESEARCH_PROGRESS_v01.md + 4 핵심 첨부 → reviewer share_
3. _Reviewer feedback (P1/P2/P3 + NEXT_STEP_PROMPT) → 본 R-A 에게 paste → 다음 step 진행_
