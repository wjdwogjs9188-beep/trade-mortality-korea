# Reviewer Prompt — Detailed Paper Feedback Request

_본 프롬프트를 reviewer (다른 LLM 또는 학자) 에게 그대로 paste 후 첨부 4 문서 함께 share. 작성: 2026-05-04._
_첨부 권장 문서:_
1. `4_documentation/PAP/PAP_2026_05_03_v3.3.md` (PAP v3.4 본문)
2. `4_documentation/PAP/PAP_v3.4_reference_update_proposal_v01.md` (reference 정정 v01.1)
3. `4_documentation/pipeline_docs/mediator_panel_build_pipeline_documentation_v01.md` (본 conversation 작업 결과)
4. `4_documentation/stage_plans/stage5_regression_plan_v01.md` (다음 phase spec)

---

## ─────────────────────────────────────────
## 프롬프트 시작 (이 아래를 reviewer 에게 paste)
## ─────────────────────────────────────────

# Detailed Feedback Request — Trade × Mortality Korea SSCI Paper

## 0. Reviewer Role 설정

당신은 **노동/보건 경제학 박사급 reviewer** 입니다. 다음 분야 expert:
- 무역 충격 × 사망률 (Pierce-Schott 2020, Finkelstein 2026, Autor-Dorn-Hanson 2013)
- Shift-share IV identification (Goldsmith-Pinkham-Sorkin-Swift 2020 AER, Borusyak-Hull-Jaravel 2022 RES + 2025 JEP)
- Causal mediation analysis (Dippel-Gold-Heblich-Pinto 2017 + Dippel-Ferrara-Heblich 2020 ivmediate)
- Deaths of despair literature (Case-Deaton 2015 PNAS)
- Weak IV inference (Olea-Pflueger 2013, Andrews-Stock-Sun 2019 Annual Review)
- 한국 microdata (KOSIS, MDIS, HIRA) 처리 경험 우대

당신의 task: 본 paper 의 **PAP v3.4 + 진행 상황 + 데이터 + 방법론** 검토 후 **SSCI 단독 저자 submission 가능 수준 reach** 위한 **detailed structured feedback** 제공.

저자 = 정재헌 (가천대 경제학부 학부생). 박사급 paper 작성에 필요한 일체의 critique 환영 (저자가 학부생이라는 점이 critique 약화 사유 X — 오히려 박사급 expectation 으로 평가 요청).

---

## 1. Paper Meta

- **제목**: "Trade Shock and Deaths of Despair in Korea: Quantifying the Underexplored Family-Mediated Channel"
- **저자**: 정재헌 (Jae-Heon Jeong), 가천대학교 경제학부, ORCID 0009-0009-9403-0940
- **submission 목표**: SSCI Q1 (American Economic Journal: Applied / Journal of Health Economics / Health Economics 등)
- **현재 status**:
  - ✅ Stage 1-3 (mortality + population + mediator panel build) **완료** (24 parquet)
  - ⏳ Stage 4 (Bartik IV trade exposure, Comtrade + HS-KSIC concordance) **진행 중**
  - ✅ Stage 5 spec plan v01 **commit**, Stage 4 완료 후 진입 대기
  - ✅ PAP v3.4 status commit (PAP_2026_05_03_v3.3.md, status v3.4 명시)
  - ✅ Reference library 19 paper deep summaries 완료 (각 1500-2700 단어)
  - ✅ Reference proposal v01.1 (3 issue 정정 후) — PAP v3.5 update 대기

---

## 2. 핵심 가설 + Novelty Position

### 2.1 핵심 가설

> **한국의 deaths of despair (자살 102 + 약물 101 + 정신 057 + 간 081, KCD 8차분류) 는 무역 충격 (Bartik shift-share IV) 의 인과적 영향을 받음. 그 영향의 일부는 가족 mediator (혼인 분해 marital_code, 교육 attainment education_band) 를 통해 전달됨.**

### 2.2 Novelty 4 영역

1. **한국 first** of Trade × Mortality × Mediator 통합 분석:
   - Pierce-Schott 2020 = US county-level, mortality cause-specific만 (mediation X)
   - Finkelstein 2026 NAFTA = all-cause mortality만 (cause-specific X, mediation X)
   - 본 paper = cause-specific 4 outcome + family channel mediation, 한국 시군구 first

2. **Family channel novelty** (DGHP 2017 + DFH 2020 framework 의 한국 first 적용):
   - Hanson (2018) marriage value paper = US marriage market value decline 의 ecological evidence 만
   - 본 paper = MDIS 사망 microdata 의 individual-level marital_code (1미혼/2배우자/3사별/4이혼) × cause cross-tab + MDIS 인구 census 의 working-age 25-64 marital share denominator → DGHP 2017 strict mediation 의 mediator-specific mortality rate 직접 산출

3. **한국 vs US dominance 차이** (paper 핵심 finding):
   - 한국 deaths of despair (working-age 25-64, 5-year stack 2017-2021): 자살 29.6/100K + 간 19.0 + 정신 9.7 + 약물 3.9
   - US (Pierce-Schott 2020): 약물 dominance (50+/100K peak), 자살 14, 간 NS
   - → 한국 = **자살 + 간 dominance**, 약물 매우 낮음 (US 의 약 1/13). Case-Deaton 2015 의 미국 narrative 와 정반대 mechanism 가설 필요

4. **DGHP 2017 + DFH 2020 ivmediate** (Stata Journal 20(3): 613-626) 의 한국 first 적용

### 2.3 한국 deaths of despair 시계열 (사용자 보유 데이터로 직접 산출, working-age 25-64, /100K annual)

| period | 시점 | drug | liver | psych | suicide |
|--------|------|------|-------|-------|---------|
| 1 | 1997-2001 | 5.61 | **44.17** | 13.29 | 23.23 |
| 2 | 2002-2006 | 4.01 | 34.26 | 10.62 | 28.26 |
| 3 | 2007-2011 | 3.81 | 26.44 | 9.85 | **35.27** ← peak |
| 4 | 2012-2016 | 3.85 | 22.69 | 8.93 | 32.89 |
| 5 | 2017-2021 | 3.86 | 19.05 | 9.66 | 29.61 |

검증:
- ✅ 자살 peak 2007-2011 = 한국 통계청 자살률 peak 일치 (카드사태 2003 + 글로벌 금융위기 2008-2010 직후)
- ✅ 간질환 -57% 단조 감소 = B형 간염 백신 + 의료 발전 historical 추세
- ✅ 약물 매우 낮음 (US 의 1/10) = paper § 7 "한국 ≠ US" 핵심 finding
- ✅ all_cause 277 → 152 / 100K (-45%) = 한국 working-age 사망률 historical 감소 추세

---

## 3. 데이터 + 방법론 detailed

### 3.1 Data sources (4 종)

| source | 시점 | 단위 | 변수 | status |
|--------|------|------|------|--------|
| KOSIS API (mediator denominator 1차 시도) | 1995-2020 | 시군구 detail 부재 발견 → 폐기 | marriage / education aggregate | 폐기 |
| MDIS 인구주택총조사 2% 표본 microdata | 1990-2020 (7 시점) | 시군구 individual | sgguCd, 성, 연령, 혼인, 교육, 가중값 | ✅ 사용 |
| MDIS 사망원인통계 (B형) microdata | 1997-2024 (28 시점) | individual death | sgguCd, 사망연령5세, 혼인, 교육, cause_104 | ✅ 사용 |
| KITA + KOSIS 무역 (Bartik IV) | 1995-2024 | HS6 trade flow | KR-CN, ADH 8 (AU/DK/FI/DE/JP/NZ/ES/CH) ← CN, CN-World | ⏳ Comtrade 진행 |
| HIRA 약물 처방 (sensitivity mediator) | 2010-2019 (120 months) | 시군구 × 월 × ATC4 | N06AB SSRI / N06AX 항우울 / N05BA 벤조 / N05AX 항정신병 / A05BA 간 / N02A 부재 | ✅ 사용 (post-2010 sensitivity only) |
| ECOS (가계부채 sensitivity) | 2003-2024 | sido | 가계부채/연체율 | ✅ |

### 3.2 Pipeline (3 stage)

**Stage 1-3 (main outcome panel)**:
- mortality 28 시점 raw → cleaning (외국인 빼기 제거, panel v01 = 한국인 only KOSIS DT_1B040M5 와 -0.35% 차이)
- 분구 시군구 합산 (sigungu_crosswalk_v2, 안산 31090 / 용인 31190 정확 코드)
- component decomposition 10 outcome group (4 deaths of despair + 6 보조)
- 3 ASR baseline (2010 한국 / WHO 2000 / Eurostat 2013)
- 산출: `mortality_rate_panel_v02_1.parquet` (123,660 rows, 229 h_code)

**Stage Mediator (본 paper conversation 작업 결과)**:
- MDIS 인구 microdata 7 시점 cross-tab → mediator denominator panel
- 1990 drop (행정구역 mismatch + paper 시점 외)
- working-age 25-64 filter (DGHP 2017 mediation 표준)
- education 4 → 3 카테고리 (NoHS / HS / College+, mortality align)
- mortality 28 시점 cleaning (position-based parse, 외국인 drop)
- mortality × mediator cross-tab (working-age + sigungu_crosswalk)
- 5-year stack period × mediator census 가까운 매핑 → mediator-specific rate panel

산출 5 parquet:
- `mediator_panel_marriage_v02.parquet` (71,125 rows, 6 시점, 4 카테고리)
- `mediator_panel_education_v03.parquet` (63,019 rows, 3 카테고리)
- `mortality_marital_panel_v01.parquet` (1,011,186 rows, working-age 25-64 + crosswalk)
- `mortality_education_panel_v01.parquet` (1,035,849 rows)
- `mediator_specific_marital_rate_v01.parquet` (187,379 rows, **Stage 5 input**)
- `mediator_specific_education_rate_v01.parquet` (171,811 rows, **Stage 5 input**)

### 3.3 Identification (Stage 5 spec, paper § 5)

**§ 5.1 Bartik shift-share IV (first-stage)**:
```
ΔTradeExposure_{h, t} = Σ_k (s_{h,k,t-10} × ΔImports_{k,t})
```
- s_{h,k,t-10} = 시군구 h 의 산업 k 고용 share (10년 lag, GPSS 2020 share exogeneity)
- ΔImports_{k,t} = ADH 8 of CN imports (Pierce-Schott 2020 spec, 한국 KR-CN 도 추가)
- HS-KSIC concordance (통계청 응답 대기)

**§ 5.2 Mediation (DGHP 2017 + DFH 2020)**:
```stata
ssc install ivmediate
ivmediate y (m = z_m) (x = z_x), vce(cluster h_code)
- y = mediator-specific mortality rate (mediator_specific_*_rate_v01.parquet 의 cell)
- x = trade exposure (Bartik IV)
- m = marital_share (or education_share) at h_code × period level
- z_x = lagged shift-share IV
- z_m = lagged mediator-specific IV (DGHP 2017 의 separate instrument requirement)
```

**§ 6 Empirical spec**: 5-year stacked first-difference (Pierce-Schott 2020 Eq. 3 base):
```
ΔY_{h, t→t+5} = β · ΔX_{h, t→t+5} + γ · controls + ε
```

**§ 7 5-layer SE** (over-engineering 여부 critique 환영):
1. HC1 (textbook, baseline)
2. WCB cluster bootstrap sigungu (n=229) — Cameron-Gelbach-Miller 2008
3. WCB cluster bootstrap sido (n=16)
4. AKM clustered SE (BHJ 2022 RES = shift-share specific)
5. Conley spatial SE (Conley 1999)

**Weak-IV diagnostics**:
- OP test effective F = **23.1 cutoff (5% worst-case TSLS bias relative to OLS)** (Olea-Pflueger 2013, Stock-Yogo 2005 Cragg-Donald F=23 의 robust 확장)
- AR + tF (Andrews-Stock-Sun 2019)

**Multiple testing**: Romano-Wolf 2005 step-down (4 outcome × 2 mediator dim = 8 hypotheses + all_cause = 9?)

---

## 4. Pending issue 4 (Stage 5 진입 전)

| issue | severity | 처리 시간 |
|-------|----------|-----------|
| Stage 4 Comtrade + HS-KSIC concordance | 🔴 critical | 통계청 응답 대기 (~수주) |
| denom missing 9.74% (marital panel) — 67 추가 h_code 진단 (1990 placeholder 잔류 의심) | 🟡 medium | ~1 시간 |
| Stata 환경 verify (가천대 license + 7 package: ivmediate, weakivtest, boottest, rwolf, reg_ss, acreg, weakiv) | 🟡 medium | ~30 분 |
| PAP v3.4 → v3.5 update (reference proposal v01.1 의 ✅ 7 항 + 26 entry reference list 적용) | 🟢 low | ~1.5 시간 |

---

## 5. Limitation 8 항 (paper § 8 추가 권장, 본 conversation 발견)

1. **1990 sigungu code (2자리) mapping placeholder** — 1990 mediator 자체 미사용 (paper 시점 외), 영향 minor
2. **1997-2007 외국인 식별 불가** (사망 microdata `사망자국적구분코드` 변수 부재) → numerator 미세 inflation (< 0.5% 추정)
3. **혼인/교육 미상 (코드 9) drop** → MAR 가정. 1997-2000 high missing rate (혼인 2.5%, 교육 7%) sensitivity test 권장
4. **Education 1997-2007 = 5 카테고리 (대학 통합), 2008+ = 7 카테고리** → **3 카테고리 (College+ 통합)** align. 전문대 vs 4년제 정보 손실
5. **2022-2024 incomplete period** drop (3년만, 5-year stack 의 마지막 period 부재)
6. **MDIS 인구 microdata 2% 표본 weight** 적용 — weighted pop sum vs 행안부 한국 총인구 ±5% 오차 normal
7. **denom missing 9.74% (marital panel)** — 67 추가 h_code 진단 미완. Stage 5 listwise deletion 시 minor bias
8. **2024 시점 사망 microdata 252 h_code** (다른 시점 229) — sigungu_crosswalk_v2 미cover. main analysis 1997-2021 무관

---

## 6. Reference 정정 결과 (v01 → v01.1, 3 issue 처리 완료)

PAP v3.3 § 14 dated change log 의 commit 과 reference proposal v01 사이 inconsistency 3 항 정정:

1. **GPSS 2018 NBER → 2020 AER 110(8): 2586-2624** (publish version primary; NBER WP 24408 2018 = working version)
2. **DGHP 2017 NBER 23209 (theoretical) + DFH 2020 Stata Journal 20(3): 613-626 (ivmediate package implementation source)** 둘 다 cite. PAP § 5.2 commit 일관
3. **OP test F=23.1 = 5% worst-case TSLS bias relative to OLS** (Stock-Yogo 2005 Cragg-Donald F=23 의 robust 확장). NOT "size distortion 5%" (이건 Stock-Yogo 의 별개 cutoff F=37, 1 endog var 시)

Reference list 22 → 26 entry (publish version 정확화 + DFH 2020 + Stock-Yogo 2005 + Pflueger-Wang 2015 weakivtest 추가)

---

## 7. Reviewer Feedback 요청 7 영역 (각 영역 별 detailed critique 요청)

### 7.1 Methodology Review

**A. Identification (PAP § 5)**:
- Bartik shift-share IV identification 가정 적절성 (GPSS 2020 share exogeneity vs BHJ 2022 shock-level orthogonality 중 어느 framework 가 한국 setting 에 적합?)
- First-stage spec 의 weak IV 진단 (OP F=23.1 cutoff) 의 한국 시군구 단위 (n=229) sample size 에서 충분 power?
- ADH 8 ← CN imports 의 한국 적용 시 한국 자체 KR-CN 직접 trade 가 confounding 또는 violation of exclusion restriction 가능성?

**B. Mediation (PAP § 5.2 DGHP 2017 + DFH 2020 ivmediate)**:
- ivmediate spec 의 instrument set (z_x, z_m) 정합성 — DGHP 2017 의 separate instrument requirement 가 한국 setting 에 가능?
- z_m (mediator-specific IV) 으로 무엇을 사용할 것인가? (예: lagged mediator share? cohort 변동? 별도 instrument 의 source?)
- Direct/indirect/total effect 분해의 identification assumption (no unmeasured mediator-outcome confounder) 한국 setting violability?

**C. 5-layer SE (PAP § 7)**:
- 5 layer 가 over-engineering 여부 (HC1 → WCB-sigungu → WCB-sido → AKM → Conley → OP test → AR+tF)
- 각 layer 의 한국 시군구 단위 sample size (n=229) 에서 power vs precision trade-off
- Romano-Wolf step-down family of hypotheses 정의 권장 (4 outcome × 2 mediator dim = 8, + all_cause = 9, 또는 다른 grouping?)

### 7.2 Data Quality Review

**A. Mediator panel education 3 카테고리 통합** (NoHS / HS / College+):
- 1997-2007 의 5=대학통합 vs 2008+ 의 6=4년제/7=대학원 분리 매핑 정합성
- 정보 손실 (전문대 vs 4년제) 의 main analysis 영향 — Korea 전문대 비율 historical 변화 (1997 ~10% → 2020 ~30%) 가 mediator coefficient 에 영향?

**B. denom missing 9.74% (marital panel)**:
- 67 추가 h_code 의 1990 placeholder 잔류 의심 — Stage 5 listwise deletion 의 bias direction 이 trade exposure 의 OLS vs IV β 추정에 어떻게 작용?
- alternative: denom = 0 fill 후 (excludes group-period cells with 0 population), 또는 multiple imputation, 또는 partial-coverage regression 권장 여부

**C. 1997-2007 외국인 식별 불가**:
- numerator 미세 inflation (< 0.5%) 가 진정 minor 인지 (혹은 외국인 비율 지역 × 시점 heterogeneity 가 trade exposure 와 correlated 라 measurement error × treatment correlation)
- robustness check 로 2008+ subset only sensitivity 시 main result 안정성

### 7.3 Robustness

**A. Stage 5 spec plan v01 의 6 진단** (외에 추가 권장):
- placebo test (pre-1997 trade exposure 가 1997+ mortality predict?)
- alternative IV (KR-CN 만 vs ADH 8 ← CN 만 vs CN-World 만)
- subsample (manufacturing-heavy sigungu vs service-heavy)
- sensitivity to 5-year window definition (4-year, 6-year)

**B. HIRA 약물 mediator (post-2010 only sensitivity)**:
- T3 (2012-2016 full) + T4 (2017-2019 partial) sensitivity check 만 가능
- HIRA 정신과 약물 (N06AB+N06AX+N05BA+N05AX) 처방률 = mediator 추가 권장 여부
- HIRA N02A (opioid) 부재 = paper § 7 한국 ≠ US 가설 confirm — narrative 강화 가능

### 7.4 Novelty Position

**A. 한국 = 자살+간 vs US = 약물 dominance** mechanism 가설:
- 한국 stoic culture + 자살 stigma 낮음 + 알코올 culture (간) 가설 narrative 충분?
- alternative explanation: 한국 의료 access (전국민 건강보험) → opioid prescription 보수 + 간 disease 조기 발견 → 사망률 paradox?
- paper § 7 mechanism section 길이 + cite 권장

**B. Family channel (DGHP 2017 한국 first 적용) novelty**:
- Hanson 2018 marriage value paper 의 ecological evidence 와 본 paper 의 individual-level mediator-specific rate 의 차이가 contribution claim 으로 충분?
- 보조 mediator (교육) 의 contribution 약화 가능성 (혼인이 main, 교육은 보조?)

### 7.5 Reference Citation Accuracy

본 conversation 정정 3 issue (위 § 6) 외 추가 inaccuracy 발견 시 명시:
- 19 paper deep summary 의 attribution / year / venue 정확성
- PAP § References 26 entry 의 빠진/잘못된 cite
- 본 paper 가 cite 해야 하지만 누락 가능성 있는 reference (예: Romano-Wolf 2016 improved version, Cameron-Miller 2015 cluster-robust review 등)

### 7.6 Stage 5 Readiness

Pending 4 항 처리 우선순위 권장:
- Stage 4 Comtrade 완료 vs denom missing 진단 vs Stata 환경 vs PAP v3.5 update — 어느 순서?
- Stata implementation 시 주의사항 (ivmediate package version 호환성, weakivtest cutoff 정확화, rwolf seed reproducibility 등)
- 외부 reviewer 피드백 cycle 권장 시점 (PAP v3.5 commit 후 vs Stage 5 결과 후)

### 7.7 SSCI Submission Strategy

**A. Target journal 권장 (top 5)**:
- AEJ Applied / JHE / Health Economics / Journal of Public Economics / Demography
- 각 journal 의 typical paper length, methodology rigor expectation, mediation analysis 수용 여부

**B. Single-author 학부생 paper 의 SSCI accept 가능성**:
- 학부생 first/single-author SSCI publish precedent
- co-authoring 권장 여부 (advisor 또는 PhD candidate)
- 수정 cycle 예상 (R&R 2-3 round)

---

## 8. Output Format (reviewer 산출 형식)

### 8.0 Critique 작성 원칙 (3 가지 enforce)

1. **P1/P2/P3 severity 분류 필수** — 모든 issue 에 priority tag:
   - **P1** (🔴 critical): submission block 또는 main result 의 invalidity 직결
   - **P2** (🟡 important): main result 변경 가능, 또는 reviewer accept 시 rejection risk
   - **P3** (🟢 minor): polish, refining, 학문적 흠집은 아니나 보강 권장

2. **Over-critic 금지** — false-positive critique 자제:
   - 본 paper 가 이미 처리한 사항 (예: PAP § 14 dated change log 의 verification commit) 을 다시 issue 로 raising X
   - 학부생 framing 으로 expectation 약화 X (위 § 0 reviewer role 참조)
   - 단, 진정한 inaccuracy / bias / identification violation 은 강력 critique 환영

3. **다음 단계 프롬프트 첨부** — reviewer feedback 의 마지막 § 에 "본 feedback 을 받은 저자가 다음 step 진행 시 R-A (별도 LLM Claude) 에게 input 할 self-contained 프롬프트" 작성 권장. 형식:
   ```
   ## NEXT_STEP_PROMPT (저자가 R-A 에게 paste 용, self-contained)
   [reviewer feedback 의 critical 사항 요약 + 저자가 R-A 에게 요청할 task description, 본 paper 의 context 모르는 R-A 가 standalone 으로 이해 가능한 분량으로]
   ```

### 8.1 Output template

다음 형식으로 detailed feedback 제공 요청:

```markdown
# Reviewer Feedback — Trade × Mortality Korea PAP v3.4

## 0. Overall Assessment
- [ ] Ready for SSCI submission (minor revision)
- [ ] Major revision before submission
- [ ] Substantial rewrite required
- [ ] Conditional accept (Stage 4 완료 후 재평가)

## 1. Methodology — issue 별 (P1/P2/P3 severity tagged)
### 1.1 Identification
- 🔴 P1 [critical issue]: [description, why critical, fix recommendation]
- 🟡 P2 [important]: ...
- 🟢 P3 [minor]: ...

### 1.2 Mediation
[same severity-tagged]

### 1.3 SE strategy
[same]

## 2. Data Quality — issue 별
[same severity-tagged]

## 3. Robustness — recommendation
[priority-ranked list]

## 4. Novelty Position — strengthening
[concrete narrative recommendation]

## 5. Reference Accuracy — additional inaccuracy
[if any]

## 6. Stage 5 — priority order
[1, 2, 3, 4 순서]

## 7. SSCI submission — strategy
- Target journal top 3 + reasoning
- Single-author 가능성 평가
- 예상 R&R cycle

## 8. Top 5 Action Items (priority order, 본 paper 의 가장 critical 한 5 개)
1.
2.
3.
4.
5.

## 9. Strength 3 + Weakness 3
**Strength**:
1.
2.
3.

**Weakness**:
1.
2.
3.

## 10. 자유 코멘트 (open-ended)
[reviewer 가 추가하고 싶은 모든 코멘트]

## NEXT_STEP_PROMPT (저자가 R-A 에게 paste 용, self-contained)
[본 feedback 의 critical (P1) 사항 요약 + 저자가 R-A 에게 요청할 task description.
본 paper 의 context 모르는 R-A 가 standalone 으로 이해 가능한 분량 (200-500 단어).
예시:
"본 reviewer 가 § 5.2 의 mediation framework 의 z_m (mediator-specific instrument)
부재를 P1 critical 로 지적. DGHP 2017 의 separate instrument requirement 가 본 paper
의 한국 setting 에서 violated. 저자가 R-A 에게 요청: ① z_m 후보 list (lagged mediator
share + cohort 변동 + 별도 instrument source), ② 각 후보의 한국 setting 적용 가능성
+ exclusion restriction 평가, ③ ivmediate 의 alternative spec (예: structural model
without separate IV) 검토 + 추천."]
```

---

## 9. 첨부 4 문서 사용법

본 프롬프트 이해를 위해 다음 4 문서 함께 review 권장:

1. **PAP v3.4 본문** (`PAP_2026_05_03_v3.3.md`) — 핵심 framework + 14 sections + dated change log
2. **Reference proposal v01.1** (`PAP_v3.4_reference_update_proposal_v01.md`) — PAP § 5/7/8 reference 정확화 제안서
3. **Mediator pipeline doc** (`mediator_panel_build_pipeline_documentation_v01.md`) — 본 conversation 의 panel build 종합 (10 sections)
4. **Stage 5 regression plan** (`stage5_regression_plan_v01.md`) — 다음 phase spec (15 sections, ivmediate Stata code sketch)

**보조** (관심 있는 paper 만):
- 19 paper deep summaries (`paper_summaries/paper_*.md`, 각 1500-2700 단어)
- Reference library master (`reference_library_master_v01.md`, 14 sections, 14,500 단어)

---

## ─────────────────────────────────────────
## 프롬프트 끝
## ─────────────────────────────────────────

_본 프롬프트는 reviewer 가 본 paper 의 모든 context (가설 + 데이터 + 방법 + caveat + reference) 를 standalone 으로 파악할 수 있도록 self-contained. 위 4 첨부 문서 와 함께 share 시 reviewer 가 1-3 시간 review 후 detailed structured feedback 작성 가능._

_추가 질문 / 명확화 요청 시 본 paper 저자 (정재헌) 또는 본 conversation 의 R-A 에게 follow-up._
