# Reviewer Prompt v02 — R-A 진행 작업 + Paper 종합 Review Request

_본 프롬프트를 reviewer (다른 LLM 또는 학자) 에게 그대로 paste. 작성: 2026-05-04._
_v01 (REVIEWER_PROMPT.md) 와 차이: v02 = **본 R-A 가 본 conversation 에서 진행한 작업 + 결정 + 처리 의 quality** 를 평가받기 위함. v01 = paper 자체 평가._

---

## ─────────────────────────────────────────
## 프롬프트 시작 (이 아래를 reviewer 에게 paste)
## ─────────────────────────────────────────

# Detailed Review Request — 본 R-A 의 진행 작업 + Paper

## 0. Reviewer 의 task + Role

당신은 **노동/보건 경제학 박사급 reviewer** 입니다 (전문 분야 6: 무역 충격 × 사망률, shift-share IV, causal mediation, deaths of despair, weak IV inference, 한국 microdata).

본 review 의 task = 다음 두 영역 모두 평가:

### A. **본 R-A (= 본 paper 의 작업을 진행한 LLM Claude) 의 모든 결정 + 데이터 처리 + 방법론 적용 의 quality + soundness**

**reviewer 가 critique 할 영역**:
- R-A 의 **substantive 결정** (e.g., 1990 mediator drop, education 3 카테고리 통합, working-age 25-64 filter, 외국인 빼기 제거)
- R-A 의 **data pipeline** (mediator panel build 방법, mortality cleaning, cross-tab logic)
- R-A 의 **reference 정확화** (GPSS publish version, ivmediate source, OP test cutoff)
- R-A 의 **framework 적용** (DGHP 2017 + DFH 2020 ivmediate, 5-layer SE, Romano-Wolf)
- R-A 의 **limitation acknowledgment** (paper § 8 8 항)

### B. **Paper 자체의 SSCI submission readiness**

PAP v3.4 + Stage 5 spec plan 의 학술적 엄밀성 + novelty + 데이터 + 방법 평가.

저자 (정재헌, 가천대 학부생) 의 framing 으로 critique 약화 X. **박사급 expectation 으로 평가 요청**.

---

## 1. Paper Meta + 전체 진행 status

- **제목**: "Trade Shock and Deaths of Despair in Korea: Quantifying the Underexplored Family-Mediated Channel"
- **저자**: 정재헌 (Jae-Heon Jeong), 가천대학교 경제학부, ORCID 0009-0009-9403-0940
- **submission 목표**: SSCI Q1 (AEJ Applied / JHE / Health Economics 등)

**Pipeline 4 stage**:
| stage | status | R-A 진행 작업 |
|-------|--------|---------------|
| Stage 1-3 | ✅ 완료 (24 parquet) | mortality + population + main outcome panel build |
| Stage Mediator (본 conversation 작업) | ✅ 완료 (5 parquet) | KOSIS API 시도→폐기, MDIS 전환, mediator panel v01→v02→v03, mortality cleaning, rate panel |
| Stage 4 | ⏳ 진행 중 | Bartik IV (Comtrade KR-CN + ADH 8 + CN-World, HS-KSIC concordance 통계청 응답 대기) |
| Stage 5 | spec plan ✅ commit | 진입 대기 (Stage 4 완료 후) |

---

## 2. R-A 가 본 conversation 에서 진행한 작업 chronological summary

### Stage A — KOSIS API mediator denominator 시도 → 폐기

- 12 KOSIS Open API URL 다운로드 시도 (혼인 6 시점 + 교육 6 시점 1995-2020)
- 처리: cell limit 40,000 회피 위해 17 시도 분할 호출, 세종 2012 이전 skip, outputFields patch (C1+C1_NM+...+C5+C5_NM 추가)
- **R-A 결정**: 5 표 verify 결과 **모든 12 표 = 시도 level only, 시군구 dimension 부재** (TBL_NM 의 "...-시군구" misnomer) → **KOSIS 폐기, MDIS microdata 전환 결정**
- **reviewer 평가 요청**: 이 결정 적절? KOSIS 의 다른 표 ID (DT_1B040M5 등) 시도해야 하는지?

### Stage B — MDIS 인구 microdata mediator denominator (Step 06-10b)

- 사용자 MDIS 신청 8 zip 입수 (1990-2020 7 시점)
- Step 06: zip 압축 해제 (cp949 한글 파일명 변환)
- Step 07: column layout 추출 (7 시점 layout table)
- Step 08: cross-tab v01 build (140K + 270K rows)
- Step 09: 4 issue 진단 (marital '.' / 2005 anomaly / education 카테고리 시점별 다름 / h_code 5자리 구조 다름)
- Step 10: cleaning + align → v02 (1990 drop, age 25-64, education 4 카테고리, sigungu_crosswalk_v2)
- Step 10b: education v02 → v03 (4 → 3 카테고리, mortality align)

**R-A 의 4 substantive 결정** (각 reviewer 평가 요청):

1. **1990 drop** — 행정구역 mismatch (시군구 2자리 vs 다른 시점 3자리) + paper 시점 외 (1997-2024). 1990 mediator 자체 미사용 결정.
2. **age filter 25-64** (DGHP 2017 working-age 표준).
3. **education 3 카테고리 (NoHS / HS / College+)** — 1997-2007 의 5=대학통합 vs 2008+ 의 6=4년제/7=대학원 정확 매핑 불가 → 통합. 정보 손실 (전문대 vs 4년제) 발생.
4. **sigungu_crosswalk_v2 적용** — mortality_panel_v02_1 의 229 h_code align (분구 합산).

산출:
- `mediator_panel_marriage_v02.parquet` (71,125 rows, 6 시점, 4 카테고리)
- `mediator_panel_education_v03.parquet` (63,019 rows, 3 카테고리)

### Stage C — MDIS 사망 microdata numerator (Step 11a-11b)

**Step 11a — 28 시점 cleaning (4 회 재시도 history)**:
- 1차 시도: column rename 시 1997-2007 의 age_5y_code 모두 NaN. column 명 정상 + sample data 정상 → rename 후 NaN. 미스터리.
- 2차 시도: keyword fuzzy match + Unicode NFC normalize → fail 동일.
- 3차 시도: **position-based parse** (column 명 무시, index 직접) → 매핑 OK. age_5y_code 정상. 그러나 national filter `→ 0` (모두 drop)
- 4차 시도: national_code NaN → `astype(str)` 후 `"nan"` string → `isin(["1", ""])` 매칭 fail. **R-A 결정**: 외국인 (`"2"`) 만 drop, NaN/빈값/1 모두 keep → 28 시점 모두 정상 (7.4M row)

**R-A 의 substantive 결정** (각 reviewer 평가 요청):

5. **Position-based parse** — column 명 차이 무시, index 직접 사용. column header 의 invisible char issue 회피.
6. **외국인 식별: "2" 만 drop** (NaN/빈값/1 모두 한국인 간주). 1997-2007 변수 부재 시 전체 keep.
7. **혼인 9 (미상) drop** — MAR 가정. 1997-2000 high missing rate (2.5%) sensitivity test 권장.
8. **교육 9 (미상) drop** — MAR 가정. 1997-2000 high missing rate (7%).
9. **Education 1997-2007 5 카테고리 + 2008+ 7 카테고리 → 3 카테고리 align** (mortality + mediator 동일).

**Step 11b — numerator panel** (working-age 25-64 filter + sigungu_crosswalk):
- 7.4M → 1.5M (working-age 20.3%)
- crosswalk 후 229 h_code (mortality_panel_v02_1 align), 2024 만 252 (sigungu_crosswalk 미cover)
- 산출: marital + education panel v01 각 1M rows

### Stage D — rate panel build (Step 12)

**5-year stack period mapping**:
| stack | mortality 5년 합 | mediator census |
|-------|-------------------|-----------------|
| 1 | 1997-2001 | 2000 |
| 2 | 2002-2006 | 2005 |
| 3 | 2007-2011 | 2010 |
| 4 | 2012-2016 | 2015 |
| 5 | 2017-2021 | 2020 |

**R-A 결정**:

10. **5-year stack period (Pierce-Schott 2020 base)** — 2022-2024 incomplete drop, 1990/1995 mediator 사용 안 함.
11. **Rate formula**: `rate = deaths_5y / (population × 5) × 100,000` (annual per 100K).
12. **Cause group 6 분류**: 4 deaths of despair (suicide 102 + drug 101 + psych 057 + liver 081) + other + all_cause.

**산출 검증** (working-age 25-64, /100K annual):
| period | drug | liver | psych | suicide |
|--------|------|-------|-------|---------|
| 1 (1997-2001) | 5.61 | 44.17 | 13.29 | 23.23 |
| 5 (2017-2021) | 3.86 | 19.05 | 9.66 | 29.61 |

**한국 historical 추세 검증** (R-A 가 confirm 한 finding):
- ✅ 자살 peak 2007-2011 (카드사태 2003 + 글로벌 금융위기) = 한국 통계청 일치
- ✅ 간질환 -57% 단조 감소 (B형 간염 백신 + 의료 발전)
- ✅ 약물 매우 낮음 (US 의 1/10) → **paper 핵심 finding "한국 ≠ US"**
- ✅ all_cause 277 → 152 / 100K (-45%)

**R-A 결정**:
13. **denom missing 9.74% (marital), 2.11% (education)** — listwise deletion. 67 추가 h_code (mortality 346 vs mediator 279) 의 1990 placeholder 잔류 의심 진단 미완.

### Stage Reference Library — 19 paper deep summary + reference proposal v01.1

- 19 paper 각 1500-2700 단어 deep summary (sub-agent 5 parallel)
- master doc 14,500 단어 (14 sections)
- Reference proposal v01 → **v01.1 (3 issue 정정)**:

**R-A 의 3 정정 결정** (사용자 round 7 audit critique 반영):
14. **GPSS 2018 NBER → 2020 AER 110(8): 2586-2624 publish version primary** (NBER WP 24408 2018 = working version)
15. **DGHP 2017 NBER 23209 (theoretical) + DFH 2020 Stata Journal 20(3): 613-626 (ivmediate package implementation source)** 둘 다 cite. ivmediate package = DFH 2020 implementation.
16. **OP test F=23.1 = 5% worst-case TSLS bias relative to OLS** (Stock-Yogo 2005 Cragg-Donald F=23 의 robust 확장 = Olea-Pflueger 2013). NOT "size distortion 5%" (이건 Stock-Yogo 의 별개 cutoff F=37, 1 endog var 시).

---

## 3. R-A 의 핵심 결정 16 항 — Reviewer 평가 권장

각 결정에 대해 reviewer 가 P1/P2/P3 severity 로 평가:

| # | 결정 | reviewer 평가 항목 |
|---|------|---------------------|
| 1 | KOSIS 폐기 → MDIS 전환 | 다른 KOSIS 표 ID 시도 가능성? |
| 2 | 1990 mediator drop | paper period 1 (1997-2001) 의 mediator 부재 영향? |
| 3 | working-age 25-64 filter | DGHP 2017 표준이지만 narrower (25-54 prime working-age) 권장? |
| 4 | Education 3 카테고리 통합 | 정보 손실 (전문대 vs 4년제) 의 main analysis 영향? |
| 5 | Position-based parse | column header 의 invisible char issue 가 진정 root cause? |
| 6 | 외국인 "2" 만 drop | 1997-2007 의 한국인+외국인 mix 가 numerator inflation < 0.5% 추정 적절? |
| 7-8 | 혼인/교육 9 (미상) drop | MAR 가정 적절? 1997-2000 high missing 의 sensitivity 권장? |
| 9 | Education align 3 카테고리 | 위 #4 와 동일 |
| 10 | 5-year stack period | 4-year, 6-year stack 도 robustness 권장? |
| 11 | Rate formula (annual per 100K) | 적절. 표준 epidemiology measure |
| 12 | 6 cause group | other category 의 use? all_cause 와 4 deaths of despair sum 차이 의미? |
| 13 | denom missing listwise deletion | 67 h_code 진단 vs alternative (multiple imputation, partial coverage) 권장? |
| 14-16 | Reference 정정 3 issue | 추가 inaccuracy 발견 시 명시 |

---

## 4. R-A 가 직면한 issue 7 + 해결 방법 적절성 평가

| # | issue | R-A 해결 | reviewer 평가 |
|---|-------|----------|----------------|
| 1 | KOSIS 시군구 부재 | MDIS 전환 (사용자 신청) | KOSIS 다른 표 시도 안 한 점? |
| 2 | 1997-2007 column rename fail | position-based parse | invisible char debug 충분? |
| 3 | national_code NaN | 외국인만 drop | 1997-2007 한국인+외국인 mix bias? |
| 4 | 1990 sigungu 2자리 | drop | mapping table 작성 시 rescue 가능? |
| 5 | denom missing 9.74% | listwise deletion | 67 h_code 진단 우선 권장? |
| 6 | Reference v01 inconsistency (3 항) | v01.1 정정 | PAP § 14 verification commit 미참조 R-A oversight 재발 방지? |
| 7 | PAP v3.4 § 14 vs proposal v01 mismatch | proposal v01.1 정정 + master doc 동기화 | v3.5 update workflow? |

---

## 5. Pending decision 6 — Reviewer 의견 필요

다음 6 결정에 대해 reviewer 권장 + 이유:

1. **denom missing 67 h_code 진단 vs drop** — 우선 진단 (1 시간) vs Stage 5 진입 (Stage 4 후)
2. **HIRA mediator T3-T4 sensitivity 추가 여부** — HIRA 2010-2019 (post-shock period 만) 의 § 5.2 appendix robustness 가치
3. **Stage 5 z_m (mediator-specific IV) 후보** — DGHP 2017 의 separate instrument requirement 의 한국 setting 후보
4. **5-layer SE over-engineering 여부** — HC1 + WCB-sigungu + WCB-sido + AKM + Conley + OP + AR+tF 가 너무 많은지
5. **Romano-Wolf family of hypotheses 정의** — 4 outcome × 2 mediator dim = 8, + all_cause = 9, 또는 다른 grouping?
6. **PAP v3.4 → v3.5 update 시점** — Stage 4 완료 전 (~1.5h) vs 후 (Bartik IV 결과 반영)

---

## 6. R-A 의 산출물 inventory + reviewer access

### 6.1 4 핵심 문서 (priority 順)

| 우선 | 문서 | path | 분량 |
|------|------|------|------|
| 1 | PAP v3.4 본문 | `4_documentation/PAP/PAP_2026_05_03_v3.3.md` | ~30p |
| 2 | Reference proposal v01.1 (R-A 정정) | `4_documentation/PAP/PAP_v3.4_reference_update_proposal_v01.md` | ~15p |
| 3 | Mediator pipeline doc (R-A 본 conversation 작업 종합) | `4_documentation/pipeline_docs/mediator_panel_build_pipeline_documentation_v01.md` | ~25p |
| 4 | Stage 5 regression plan v01 | `4_documentation/stage_plans/stage5_regression_plan_v01.md` | ~30p |

### 6.2 보조

- 19 paper deep summaries: `4_documentation/reference_library/paper_summaries/` (each 1500-2700 단어)
- Reference library master: `4_documentation/reference_library/reference_library_master_v01.md` (14,500 단어)
- Validation reports: `3_derived/validation_report_*.md`, `PAP_v3.4_reference_proposal_validation_v01_1.md`, `mortality_microdata_cleaned_v01.parquet` exploration
- HIRA panel exploration: `3_derived/mortality/hira_drug_panel_exploration_v01.md`

### 6.3 데이터 (reviewer 가 direct verify 시)

24 derived parquet: `3_derived/mortality/`, `3_derived/population/` — 핵심 7 panel:
- `mediator_panel_marriage_v02.parquet`, `mediator_panel_education_v03.parquet`
- `mortality_microdata_cleaned_v01.parquet`, `mortality_marital_panel_v01.parquet`, `mortality_education_panel_v01.parquet`
- **`mediator_specific_marital_rate_v01.parquet`, `mediator_specific_education_rate_v01.parquet`** (Stage 5 input)

### 6.4 Scripts (R-A 작성, 70+)

- `2_scripts/data_collection/05-12_*.py` (KOSIS API + MDIS pipeline)
- `2_scripts/build_panel/4A_trade_collection.py` (Comtrade 진행 중)
- `2_scripts/verify/*.py` (sigungu, codebook, exploration)

---

## 7. Reviewer Feedback 요청 9 영역

### 7.1 R-A 의 substantive 결정 (위 § 3 의 16 결정) 적절성
### 7.2 R-A 의 issue 처리 (위 § 4 의 7 issue) 적절성
### 7.3 Pending decision (위 § 5 의 6 결정) reviewer 권장
### 7.4 Methodology (PAP § 5-7) 학술 엄밀성
### 7.5 Data quality (mediator panel + mortality cleaned + rate panel)
### 7.6 Novelty position (한국 vs US, family channel, DGHP 2017 한국 first)
### 7.7 Reference accuracy (R-A 정정 외 추가 inaccuracy)
### 7.8 Stage 5 readiness (Pending 4 항 처리 우선순위)
### 7.9 SSCI submission strategy (target journal, single-author 학부생 가능성)

---

## 8. Output Format

### 8.0 Critique 작성 원칙 3 가지

1. **P1/P2/P3 severity 분류 필수**:
   - **P1** (🔴 critical): submission block 또는 main result 의 invalidity 직결
   - **P2** (🟡 important): main result 변경 가능, reviewer accept 시 rejection risk
   - **P3** (🟢 minor): polish, refining

2. **Over-critic 금지**: false-positive critique 자제. R-A 가 이미 처리한 사항 (예: PAP § 14 dated change log, reference proposal v01.1 의 3 정정) 을 다시 issue 로 raising X. 학부생 framing 으로 expectation 약화 X. 단 진정한 inaccuracy / bias / identification violation 은 강력 critique 환영.

3. **NEXT_STEP_PROMPT 첨부 필수**: feedback 의 마지막 § 에 본 R-A 가 standalone 으로 이해 가능한 self-contained 다음 step 프롬프트 (200-500 단어).

### 8.1 Output template

```markdown
# Reviewer Feedback v02 — R-A 진행 작업 + Paper

## 0. Overall Assessment
- R-A 작업 quality: [grade — A/B/C with reasoning]
- Paper SSCI submission readiness: [stage 평가]

## 1. R-A 의 Substantive 결정 16 항 평가
| # | 결정 | 평가 | severity | reasoning |
|---|------|------|----------|-----------|
| 1 | KOSIS 폐기 → MDIS | ✅ / ⚠️ / ❌ | P1/P2/P3 | ... |
| 2 | 1990 drop | ... | ... | ... |
[16 결정 모두]

## 2. R-A 의 Issue 처리 7 항 평가
[같은 형식]

## 3. Pending Decision 6 항 권장
[reviewer 권장 + 이유]

## 4. Methodology critique (P1/P2/P3 tagged)
### 4.1 Identification
🔴 P1: ...
🟡 P2: ...
🟢 P3: ...

### 4.2 Mediation
[same]

### 4.3 5-layer SE
[same]

## 5. Data Quality critique
[same severity-tagged]

## 6. Novelty Position critique
[same]

## 7. Reference Accuracy
R-A 정정 3 issue 외 추가 inaccuracy:
[if any]

## 8. Stage 5 Priority Order
[1, 2, 3, 4 순서]

## 9. SSCI submission strategy
- Target journal top 3 + reasoning
- Single-author 학부생 가능성 평가
- 예상 R&R cycle

## 10. Top 5 Action Items (priority)
1. ...
2. ...
3. ...
4. ...
5. ...

## 11. Strength 3 + Weakness 3
## 12. 자유 코멘트 (open-ended)

## NEXT_STEP_PROMPT (R-A 에게 paste 용, self-contained)
[reviewer feedback 의 critical (P1) 사항 요약 + 저자가 R-A 에게 요청할 task description.
본 paper 의 context 모르는 R-A 가 standalone 으로 이해 가능한 분량 (200-500 단어).
예시:
"본 reviewer 가 R-A 의 결정 #6 (외국인 '2' 만 drop) 을 P2 important 로 지적. 1997-2007
의 한국인+외국인 mix 가 numerator inflation 0.5% 추정의 외국인 비율 시점/지역 heterogeneity 와
trade exposure correlation 가능성. R-A 에게 요청: ① 2008+ subset only 의 sensitivity
analysis (외국인 분리 가능 시점만), ② 한국 외국인 비율 시도 × 시점 panel 외부 source 검색
(법무부 등록외국인 통계 등) + trade exposure 와의 correlation matrix 산출, ③ measurement
error × treatment correlation bias direction analytic derivation. 결과를 paper § 8
limitation #2 정량화 + § 7 robustness 에 추가."]
```

---

## ─────────────────────────────────────────
## 프롬프트 끝
## ─────────────────────────────────────────

_본 v02 프롬프트는 v01 (paper 자체 평가) 와 차이 = R-A 의 substantive 결정 (16 항) + issue 처리 (7 항) + pending decision (6 항) 을 명시하여 reviewer 가 R-A 의 작업 quality + 학술적 적절성을 평가할 수 있도록 self-contained._

_사용 방법: 본 .md 파일 + 4 핵심 첨부 문서 함께 reviewer 에게 share. reviewer feedback 의 NEXT_STEP_PROMPT 부분을 R-A (본 conversation Claude) 에게 paste → R-A 가 다음 step 진행._
