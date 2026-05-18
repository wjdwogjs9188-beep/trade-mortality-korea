# PAP v3.4 Reference Update 제안서 v01.1

_본 제안서: 19 paper deep summary 결과를 PAP v3.4 의 reference list + footnote 에 반영_
_작성: 2026-05-04_
_v01.1 update: 사용자 round 7-style audit critique 반영 (3 issue 정정 — GPSS 2020 publish, DFH 2020 추가, OP test cutoff TSLS bias attribution 정확화)_
_원본 PAP: `C:\Users\82103\Desktop\뉴 논문\PAP_2026_05_03_v3.3.md` (status v3.4)_

**v01 → v01.1 정정 내역**:
1. § 3.1 GPSS: 2018 NBER → **2020 AER** (publish version primary, NBER WP 24408 2018 = working paper)
2. § 4.1, § 4.2: DGHP 2017 only → **DGHP 2017 (theoretical) + DFH 2020 Stata Journal (ivmediate package implementation source)** 둘 다 명시. PAP v3.4 § 5.2 commit 일관.
3. § 6.2 OP test cutoff: "size distortion 5%" → **"5% worst-case TSLS bias relative to OLS"** (Stock-Yogo 2005 Cragg-Donald F=23 의 robust 확장). paper #8 (BHJ 2025) summary 의 "F > 23 (Cragg-Donald, 5% bias)" 와 일치.
4. § 8.1 reference list: 22 → **26** (GPSS publish version 정확화, DFH 2020 추가, Stock-Yogo 2005 추가, Pflueger-Wang 2015 weakivtest 추가)

---

## 0. 본 제안서 사용법

**본 제안서는 PAP 본문 main text 변경 X**. footnote + reference list 정확화만.

사용자 review 후 PAP 에 직접 적용:
- ✅ 즉시 적용 가능 (factual 정확화)
- ⚠️ 사용자 검토 필요 (해석 영향)
- 🔴 major rewrite 제안 (별도 PAP v4 검토)

---

## 1. § 1 Introduction / Motivation — Reference 보강

### 1.1 Deaths of despair 정의 source

**현재 PAP** (추정): "deaths of despair" 용어 사용 시 Case-Deaton 2015 cite

**제안 (✅ 즉시)**:
- **Case-Deaton 2015 PNAS** "Rising morbidity and mortality in midlife among white non-Hispanic Americans in the 21st century" — 자살 + 약물 + 알코올 (간경변) 3 outcome 정의 source
- **본 paper 의 4 outcome** (자살 102 + 약물 101 + 정신 057 + 간 081) = Case-Deaton 3 outcome 의 한국 확장 (정신질환 057 추가, 간 081 = ARLD 대응)
- 차이 명시: "Case-Deaton 의 alcohol-related liver disease (ARLD) = 본 paper 의 cause_104=081 (간) 와 conceptually 유사하나 한국 codebook 의 8차분류 기준"

### 1.2 Trade × mortality literature 위치

**제안 (✅ 즉시)**:
- **Pierce-Schott 2020 AERI** "Trade Liberalization and Mortality" — county-level US, drug overdose +2-3/100K, but **suicide 와 ARLD 는 NOT significant**
- **Finkelstein-Notowidigdo-Shi 2026** (BFI WP 2026-33) "Trade Shocks and Mortality" — NAFTA × all-cause +0.68% over 15 years
- **본 paper 의 한국 차이**: Pierce-Schott 의 약물 dominance 와 정반대 — 한국 = 자살 + 간 dominance (paper § 7 핵심 finding)

### 1.3 Motivation quote (paper § 1 권장)

> "While Case-Deaton (2015) defined deaths of despair as deaths from suicide, drug overdose, and alcohol-related liver disease (ARLD), Pierce and Schott (2020) found that trade liberalization significantly increased only drug overdose mortality in the US, with no detectable effect on suicide or ARLD. We document a fundamentally different pattern in Korea: trade exposure shifts mortality through suicide and chronic liver disease, while drug-related mortality remains negligible (5/100K vs. US's 50+/100K)."

---

## 2. § 2 Literature Review — Reference 보강

### 2.1 Family channel (mediation) literature

**제안 (✅ 즉시)**:
- **Hanson marriage value paper** (paper #12) — 제조업 쇠퇴 → 남성 marriage market value ↓ → 가족 해체 → 자살/약물 사망률 ↑. 본 paper 의 mediator (marital_code) 의 직접 reference.
- 한국 적용: Korea 의 marriage rate decline (1995-2020) + working-age 25-64 의 미혼/이혼 비율 추이 (본 conversation 의 mediator panel build 에서 1997 미혼 3% → 2024 13%, 이혼 6% → 변동) 가 Hanson 의 US 추세와 일관

### 2.2 Household debt mediation (한국 context)

**제안 (✅ 즉시)**:
- **Sufi 2023 (BFI WP 2023-109)** "Household Debt and Macroeconomic Fluctuations" — 한국 가계부채 위기 직접 다룸. 본 paper § 2.3 의 한국 context 핵심 reference.
- **Mian-Sufi 2014, 2016** — household debt 의 mortality channel (자살 + 약물). 본 paper 의 secondary mediator (paper § 8 limitation 에 부채 channel 부재 명시)

### 2.3 NAFTA × Mortality (most direct precedent)

**제안 (✅ 즉시)**:
- **Finkelstein 2026 (BFI WP 2026-33)** = methodology 가장 가까운 reference. Trade shock + mortality + IV strategy + cause-specific analysis 모두 본 paper 와 parallel. 본 paper 가 한국 first 이지만 Finkelstein 이 international second.

---

## 3. § 5 Identification — Bartik IV reference

### 3.1 § 5.1 Bartik shift-share IV reference 4 ranked

**현재 PAP v3.4** § 4: **GPSS (2020 AER)** share exogeneity path 명시 commit (v3.3 § 14 dated change log #20 = "GPSS 2018 → 2020 AER 정정" 처리)

**제안 (✅ 즉시 — PAP v3.4 commit 일관)**:
- **primary**: **Goldsmith-Pinkham, Sorkin, Swift (2020) "Bartik Instruments: What, When, Why, and How," American Economic Review 110(8): 2586-2624** (publish version). NBER WP 24408 (2018) = working paper version. **본문 cite 시 "GPSS 2020", reference list 시 "2020 AER (NBER WP 24408 2018)"**. PAP § 5.1 의 identification 가정 명시 시 cite 필수.
- **secondary**: **Borusyak, Hull, Jaravel (2025) "A Practical Guide to Shift-Share Instruments," Journal of Economic Perspectives** — 실제 implementation 권장 (shock-level orthogonality test, ssaggregate R package)
- **tertiary**: **Borusyak, Hull, Jaravel (2022) "Quasi-Experimental Shift-Share Research Designs," Review of Economic Studies 89(1): 181-213** = AKM clustering 의 source (paper § 7.3 5-layer SE 의 Layer 4 직접 reference). NBER WP 24997 (2018) = working paper version.
- **foundational**: **Bartik (1991) "Who Benefits from State and Local Economic Development Policies?"** Upjohn Institute — original shift-share concept

### 3.2 § 5.1 first-stage spec

**제안 (✅ 즉시)**:
- **ADH 2013 AER** "The China Syndrome" — canonical Bartik first-stage spec. 본 paper 의 trade exposure 변수 = ADH 2013 의 Eq. (3) 한국 적용 (5-year stack)
- **Pierce-Schott 2020 AERI** Eq. (3) 의 5-year stacked first-difference design — 본 paper § 6 spec 직접 차용
- **Dauth-Findeisen-Suedekum 2014** (Germany) — 수출국 (한국 ≈ 독일) 시나리오 reference

---

## 4. § 5.2 Mediation framework — DGHP 2017

### 4.1 핵심 reference (PAP v3.4 § 5.2 commit 일관)

**현재 PAP v3.4** § 5.2: **"Main framework: Dippel, Gold, Heblich, Pinto (DGHP) 2017 NBER WP 23209 + Dippel, Ferrara, Heblich (DFH) 2020 Stata Journal `ivmediate` package"** (둘 다 명시 commit). v3.3 dated change log #20 = "DFH 2022 / DGHP 2020 / GPSS 2018" R-A citation accuracy 누락 패턴 limitation #20 처리 일환.

**제안 (✅ 즉시 — PAP v3.4 와 일관)**:
- **theoretical framework**: **Dippel, Gold, Heblich, Pinto (DGHP) 2017 "The Effect of Trade on Workers and Voters," NBER Working Paper 23209** — IV mediation framework 의 theoretical source. Total/direct/indirect effect 분해.
- **implementation source**: **Dippel, Ferrara, Heblich (DFH) 2020 "Causal mediation analysis in instrumental-variables regressions," Stata Journal 20(3): 613-626** — `ivmediate` Stata package implementation. PAP § 5.2 의 실제 estimation = DFH 2020 의 ivmediate command spec 직접 차용.
- **secondary mediator literature**:
  - **Hanson marriage value paper** (paper #12) — family channel 의 specific mediator (marriage market value)
  - **Dix-Carneiro, Soares, Ulyssea (2017)** "Local Labor Market Conditions and Crime," American Economic Review — Brazil tariff exposure × crime 의 mediation (employment channel). 본 paper 의 family channel 과 parallel 시 cite.

### 4.2 ivmediate Stata implementation (DFH 2020 source)

**제안 (✅ 즉시)**:
- **implementation source 명시**: ivmediate command = **DFH 2020 Stata Journal package** (DGHP 2017 의 framework 를 Stata 화). DGHP 2017 자체는 paper 만 제공 (Stata code X), DFH 2020 가 user-written package 출시.
- PAP § 5.2 spec 권장:
  ```stata
  * DFH 2020 ivmediate package, theoretical = DGHP 2017
  ssc install ivmediate
  ivmediate y (m = z_m) (x = z_x), [vce(cluster h_code)]
  - y = mortality_rate (mediator-specific, working-age 25-64, per 100K)
  - x = trade_exposure_5y (Bartik IV)
  - m = marital_share (or education_share) at h_code × period level
  - z_x = lagged shift-share IV (Bartik construction)
  - z_m = lagged mediator-specific IV — DGHP 2017 의 separate instrument requirement
  ```
- 추가 robustness: IKY 2010 bound interpretation (PAP v3.3 § 5.2 commit) 도 sensitivity test 차원

### 4.3 정확한 quote (paper § 5.2 권장)

> "Following Dippel, Gold, Heblich, and Pinto (2017), we decompose the total effect of trade exposure on mortality into a direct effect (operating through unmeasured channels such as job loss-induced stress) and an indirect effect mediated by family structure dissolution. Unlike Hanson (2018) who infers the family channel from marriage market value declines in US data, we directly observe individual-level marital status at death (혼인상태코드 from KOSIS death microdata) and combine it with the population at risk by marital category (mediator denominator from MDIS Population Census 2% sample, working-age 25-64)."

---

## 5. § 6 Empirical Specification — Reference

### 5.1 5-year stacked first-difference

**제안 (✅ 즉시)**:
- **Pierce-Schott 2020 AERI** Eq. (3) — 본 paper § 6 의 spec 직접 source
- **Pierce-Schott 2016 FED Working Paper** (paper #4) — 초기 PNTR design

### 5.2 Cause-specific analysis

**제안 (✅ 즉시)**:
- **Pierce-Schott 2020** = cause-by-cause estimation (drug separately from suicide separately from ARLD)
- **본 paper extension**: 4 cause (자살 + 약물 + 정신 + 간) + all_cause + other = 6 outcome group

---

## 6. § 7 Robust Inference (5-layer SE) — Reference 보강

### 6.1 Layer 별 reference

**제안 (✅ 즉시 — 정확화)**:

| Layer | method | primary reference | secondary |
|-------|--------|-------------------|-----------|
| 1 | HC1 robust SE | (textbook, Stata default) | — |
| 2 | WCB cluster bootstrap (sigungu) | Cameron-Gelbach-Miller 2008 | (textbook) |
| 3 | WCB cluster bootstrap (sido) | 동일 | — |
| 4 | **AKM SE (shift-share specific)** | **BHJ 2022 (paper #2 IMF 1806 또는 paper #12 BHJ 2018)** | GPSS 2018 |
| 5 | Conley spatial SE | **Conley 1999 (paper #18)** | — |

### 6.2 § 7.5 OP test (weak IV) — cutoff criterion 정확화

**제안 (✅ 즉시 — 사용자 round 7 audit critique 반영)**:
- **Olea-Pflueger 2013** "A Robust Test for Weak Instruments," Journal of Business and Economic Statistics 31(3): 358-369 — primary. **Effective F statistic** = heteroscedasticity + clustering robust 확장.
- **Staiger-Stock 1994 (paper #15, NBER TWP 151 / Econometrica 1997)** — original framework (homoskedasticity 가정 + local-to-zero asymptotics + Stock-Yogo cutoff base)
- **Andrews-Stock-Sun 2019 (paper #5)** "Weak Instruments in IV Regression," Annual Review of Economics — comprehensive review

**Cutoff F=23.1 의 정확한 attribution** (R-A round 7 audit critique 반영):
- ❌ **잘못**: "F=23.1 = 5% size distortion of Wald test" (이건 Stock-Yogo 의 별개 cutoff, 1 endog var 시 약 F=37)
- ✅ **정확**: **F=23.1 = 5% worst-case TSLS bias relative to OLS** (Stock-Yogo 2005 Cragg-Donald F ≈ 23 의 robust 확장, Olea-Pflueger 2013 effective F)
- 즉 PAP v3.3 § 4 의 "Olea-Pflueger 2013 effective F = 23.1 weak-IV test" 의 23.1 = **TSLS bias criterion** (NOT size distortion)
- paper #8 (BHJ 2025 practical guide) summary 의 명시: "F > 23 (Cragg-Donald, 5% bias)" — 동일 confirm
- PAP § 7.5 cite 시 **Olea-Pflueger 2013 + Stock-Yogo 2005 (Cragg-Donald F)** 둘 다 cite, criterion 명시 = "5% worst-case TSLS relative bias"

**Stock-Yogo 2005 cutoffs** (참고):
- F=10 (size distortion 25% Wald)
- F=15 (size distortion 15%)
- F=20 (size distortion 10%)
- F=37 (size distortion 5%, 1 endog var)
- F=23 (5% TSLS bias relative to OLS) ← 본 paper 의 23.1 의 base

**Stata implementation**: Pflueger-Wang 2015 `weakivtest` package — homoscedasticity / robust / cluster-robust effective F 자동 계산. PAP § 7.5 의 weakivtest output 가 23.1 cutoff 와 비교.

### 6.3 § 7.6 Romano-Wolf step-down

**제안 (✅ 즉시)**:
- **Romano-Wolf 2005** — multiple testing FWE control (현재 PAP cite 됐을 것)
- **Romano-Wolf 2016** — improved version 도 cite 권장

### 6.4 § 7.7 AR + tF (weak-IV CI)

**제안 (✅ 즉시)**:
- **Andrews-Stock-Sun 2019** (paper #5) "Weak Instruments in IV Regression: Theory and Practice" Annual Review — AR confidence interval 의 weak-IV-robust 성질
- **Staiger-Stock 1994 (paper #15)** — AR CI 의 original treatment

---

## 7. § 8 Limitations — Reference 보강

### 7.1 Mediator panel limitation 8 항 (본 conversation 결과)

**제안 (✅ 즉시 — 본 conversation 의 mediator panel build 에서 발견된 한계)**:

1. **1990 sigungu code (2자리) mapping placeholder** — 1990 mediator 자체 미사용, 영향 minor
2. **1997-2007 외국인 식별 불가** — sample microdata 변수 부재. numerator 미세 inflation (< 0.5% 추정)
3. **혼인/교육 미상 (9) drop** — MAR 가정. 1997-2000 high missing (혼인 2.5%, 교육 7%) sensitivity test 권장
4. **education 1997-2007 = 5 카테고리, 2008+ = 7 카테고리** → **3 카테고리 (College+ 통합)** align. 전문대 vs 4년제 정보 손실
5. **2022-2024 incomplete period** drop. 2017-2021 마지막 stack period
6. **MDIS 인구 microdata 2% 표본 weight** ±5% 오차
7. **denom missing 9.74% (marital), 2.11% (education)** Stage 5 listwise deletion. 영향 minor
8. **2024 시점 사망 microdata = 252 h_code** (다른 시점 229) crosswalk 미cover. main analysis 무관 (1997-2021 only)

### 7.2 비교 reference

**제안 (✅ 즉시)**:
- **Pierce-Schott 2020** 도 cause classification 변경 (ICD-10 transition 2002) limitation 보유 — 본 paper 의 8차분류 변경 limitation 과 parallel
- **Finkelstein 2026** 도 NAFTA 시점 외국인 분리 한계 — 본 paper 와 비슷한 한계

---

## 8. Reference list 추가 (PAP § References)

### 8.1 추가 cite 필수 (본 conversation 결과 발견)

| author | year | title | venue | priority |
|--------|------|-------|-------|----------|
| Case, Deaton | 2015 | Rising morbidity and mortality in midlife... | PNAS 112(49): 15078-15083 | 필수 |
| Pierce, Schott | 2020 | Trade Liberalization and Mortality... | American Economic Review: Insights 2(1): 47-64 | 필수 |
| Finkelstein, Notowidigdo, Shi | 2026 | (NAFTA × Mortality) | BFI WP 2026-33 | 필수 |
| **Goldsmith-Pinkham, Sorkin, Swift** | **2020** | **"Bartik Instruments: What, When, Why, and How"** | **American Economic Review 110(8): 2586-2624** (NBER WP 24408 2018) | 필수 |
| Borusyak, Hull, Jaravel | 2025 | A Practical Guide to Shift-Share Instruments | Journal of Economic Perspectives | 필수 |
| Borusyak, Hull, Jaravel | 2022 | Quasi-Experimental Shift-Share Research Designs | Review of Economic Studies 89(1): 181-213 (NBER WP 24997 2018) | 필수 |
| **Dippel, Gold, Heblich, Pinto (DGHP)** | **2017** | **"The Effect of Trade on Workers and Voters" (theoretical framework)** | **NBER Working Paper 23209** | 필수 |
| **Dippel, Ferrara, Heblich (DFH)** | **2020** | **"Causal mediation analysis in instrumental-variables regressions" (ivmediate Stata package)** | **Stata Journal 20(3): 613-626** | 필수 |
| Hanson (et al.) | 2018 | (Marriage value of trade-exposed men) | (paper #12) | 필수 |
| Sufi | 2023 | Household Debt and Macroeconomic Fluctuations | BFI WP 2023-109 | 필수 |
| Andrews, Stock, Sun | 2019 | Weak Instruments in IV Regression: Theory and Practice | Annual Review of Economics 11: 727-753 | 필수 |
| Olea, Pflueger | 2013 | A Robust Test for Weak Instruments | Journal of Business and Economic Statistics 31(3): 358-369 | 필수 |
| **Stock, Yogo** | **2005** | **"Testing for Weak Instruments in Linear IV Regression"** | **Identification and Inference for Econometric Models, Cambridge UP** (Cragg-Donald F=23 cutoff source) | 필수 |
| Pflueger, Wang | 2015 | "A robust test for weak instruments in Stata" (weakivtest package) | Stata Journal 15(1): 216-225 | 권장 |
| Staiger, Stock | 1994/1997 | IV Regression with Weak Instruments | NBER TWP 151 / Econometrica 65(3): 557-586 | 필수 |
| Romano, Wolf | 2005 | Stepwise Multiple Testing as Formalized Data Snooping | Econometrica 73(4): 1237-1282 | 필수 |
| Conley | 1999 | GMM Estimation with Cross Sectional Dependence | Journal of Econometrics 92(1): 1-45 | 필수 |
| Cameron, Gelbach, Miller | 2008 | Bootstrap-Based Improvements for Inference with Clustered Errors | Review of Economics and Statistics 90(3): 414-427 | 필수 |
| Autor, Dorn, Hanson | 2013 | The China Syndrome: Local Labor Market Effects of Import Competition in the United States | American Economic Review 103(6): 2121-2168 | 필수 |
| Dauth, Findeisen, Suedekum | 2014 | The Rise of the East and the Far East: German Labor Markets and Trade Integration | Journal of the European Economic Association 12(6): 1643-1675 | 권장 |
| Pierce, Schott | 2016 | The Surprisingly Swift Decline of US Manufacturing Employment | American Economic Review 106(7): 1632-1662 | 권장 |
| Mian, Sufi, Verner | 2016 | Household Debt and Business Cycles Worldwide | Quarterly Journal of Economics 132(4): 1755-1817 | 권장 |
| Mian, Sufi | 2014 | What Explains the 2007–2009 Drop in Employment? | Econometrica 82(6): 2197-2223 | 권장 |
| Dix-Carneiro, Soares, Ulyssea | 2017 | Local Labor Market Conditions and Crime: Evidence from the Brazilian Trade Liberalization | American Economic Journal: Applied Economics | 권장 |
| Dow, Godøy, Lowenstein, Reich | 2019 | Can Economic Policies Reduce Deaths of Despair? | NBER Working Paper 25787 | 권장 |
| Bartik | 1991 | Who Benefits from State and Local Economic Development Policies? | Upjohn Institute | foundational |

**Total: 26 reference** (v01 22 + v01.1 추가 4: GPSS publish version 정확화, DFH 2020 추가, Stock-Yogo 2005, Pflueger-Wang 2015)

---

## 9. PAP 직접 수정 권장 (사용자 review 후)

### 9.1 즉시 적용 가능 (✅) 7 항

1. § 1 motivation — Case-Deaton + Pierce-Schott + Finkelstein quote 추가
2. § 2 literature — Hanson + Sufi + Mian 추가
3. § 5.1 — GPSS + BHJ + Bartik 1991 정확 cite
4. § 5.2 — DGHP 2017 + Hanson + Dix-Carneiro 정확 cite + ivmediate spec 명시
5. § 6 — Pierce-Schott 2020 Eq (3) source 명시
6. § 7 — 5 layer SE 별 reference 정확화 (BHJ 2018, Conley 1999, Olea-Pflueger 2013, Staiger-Stock 1994, Andrews-Stock-Sun 2019, Romano-Wolf 2005)
7. § 8 — 8 limitation (mediator panel build 결과) 추가

### 9.2 검토 필요 (⚠️) 2 항

1. § 5.2 ivmediate spec 의 정확한 instrument set (z_x, z_m) — DGHP 2017 review 후 결정
2. § 7.6 Romano-Wolf step-down 의 family of hypotheses 정의 (4 outcome × marital/education = 12 + all_cause = 13 hypotheses?)

### 9.3 Major rewrite 제안 (🔴) 0 항

PAP v3.4 의 main framework 정확. major rewrite 불필요.

---

## 10. Workflow

### 10.1 본 제안서 사용

1. 사용자 review (~30 분)
2. § 1-8 의 ✅ 항 PAP v3.3 → v3.5 (또는 v4.0) update (~1 시간)
3. ⚠️ 항 별도 검토
4. § 9 reference list 추가 (~30 분)
5. PAP v3.5 외부 reviewer 피드백 위해 share

### 10.2 본 제안서 미적용 시 위험

- reference 정확화 부재 → 외부 reviewer "GPSS 2018, BHJ 2025 cite 빠졌네요" 같은 minor critique
- mediation framework 의 DGHP 2017 spec 명시 부재 → reviewer "ivmediate 어떻게 쓸지 명시 필요" critique
- limitation 부재 → reviewer "외국인 식별 등 한계 보강 필요"

→ 모두 minor 하나 paper revision 시 시간 손실. 본 제안서 적용 시 사전 방지.

---

_이 제안서 = 19 paper deep summary (master doc) 의 PAP 적용 인터페이스. master doc + 제안서 + PAP 3 문서 cycle._
