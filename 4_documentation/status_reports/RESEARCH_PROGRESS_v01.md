---
title: RESEARCH_PROGRESS_v01 — Trade × Mortality Korea
author: 정재헌 (Jae-Heon Jeong, 가천대 경제학부) + R-A (Claude LLM)
date: 2026-05-04
version: v01
target: reviewer feedback (SSCI submission readiness)
status: PAP v3.4 commit, Stage 1-3 + Mediator 완료, Stage 4 Bartik IV 진행 중
related:
  - PAP_2026_05_03_v3.3.md
  - PAP_v3.4_reference_update_proposal_v01.md
  - mediator_panel_build_pipeline_documentation_v01.md
  - stage5_regression_plan_v01.md
---

# RESEARCH_PROGRESS_v01 — Trade × Mortality Korea

**Paper**: "Trade Shock and Deaths of Despair in Korea: Quantifying the Underexplored Family-Mediated Channel"
**Author**: 정재헌 (Jae-Heon Jeong, 가천대학교 경제학부 학부생, ORCID 0009-0009-9403-0940)
**Submission target**: SSCI Q1 (AEJ Applied / JHE / Health Economics)
**Status (2026-05-04)**: PAP v3.4 status commit, Stage 1-3 + Mediator panel build 완료, Stage 4 Bartik IV 진행 중

---

## 1. Executive Summary

본 paper 는 한국의 deaths of despair (자살 KCD 8차분류 102 + 약물 101 + 정신질환 057 + 간질환 081) 가 무역 충격 (Bartik shift-share IV) 의 인과적 영향을 받는지, 그리고 그 영향의 일부가 가족 mediator (혼인 분해 marital_code, 교육 attainment education_band) 를 통해 전달되는지 정량화한다. Identification framework 는 Dippel-Gold-Heblich-Pinto (DGHP) 2017 NBER WP 23209 의 IV mediation theoretical framework 와 Dippel-Ferrara-Heblich (DFH) 2020 Stata Journal 20(3): 613-626 의 `ivmediate` package implementation 을 한국 시군구 (n=229) × 5-year stack (1997-2001 부터 2017-2021 까지 5 period) 에 first 적용.

Novelty 4 영역: (1) 한국 first 의 trade × mortality × mediator 통합 분석 — Pierce-Schott (2020) AER Insights 는 US county mediation X, Finkelstein, Notowidigdo, Shi (2026) BFI WP 2026-33 은 NAFTA all-cause 만, (2) family channel novelty (Hanson 2018 marriage value paper 의 한국 individual-level microdata 확장), (3) 한국 vs US dominance 차이 (한국 = 자살+간 dominance, US = 약물 dominance, Case-Deaton 2015 PNAS 와 정반대 mechanism), (4) DGHP 2017 + DFH 2020 ivmediate 의 한국 first 적용.

진행 status: Stage 1-3 (mortality + population + main outcome panel) 완료 24 parquet, Stage Mediator (본 작업의 핵심 결과) 완료 5 parquet 추가, Stage 4 Bartik IV 진행 중 (Comtrade KR-CN + ADH 8 ← CN + CN-World 다운로드, HS-KSIC concordance 통계청 응답 대기), Stage 5 ivmediate regression spec plan v01 commit (진입 대기). Preliminary finding: 자살률 peak 2007-2011 (35.27/100K) = 한국 통계청 일치 (카드사태 2003 + 글로벌 금융위기 2008-2010), 간질환 -57% 단조 감소 (B형 간염 백신 + 의료 발전), 약물 5.61 → 3.86/100K (US 의 약 1/13 = 한국 ≠ US 핵심 finding). All-cause working-age 25-64 mortality 277 → 152/100K (-45%, 의료 발전 일관).

---

## 2. Research Question + Hypothesis

### 2.1 Main Research Question
한국의 deaths of despair (working-age 25-64) 시계열은 1997-2021 동안 dramatic 한 변화 (자살 ↑ then ↓, 간 단조 ↓, 약물 stable low). 이 변화 중 어느 정도가 무역 충격 (특히 한중 무역 통합 + 중국 imports surge) 의 인과적 효과인가? 그 효과 중 어느 정도가 가족 구조 mediator (이혼율 ↑, 미혼율 ↑, 교육 attainment) 를 통해 전달되는가?

### 2.2 Sub-hypotheses (4)

**H1 — Reduced-form**: 시군구 (sigungu, n=229) 의 무역 노출 (Bartik shift-share IV, ADH 8 ← CN imports + KR-CN 직접 trade) 이 1 SD 증가 시, working-age 25-64 의 deaths of despair 가 5-year cumulative 로 X% 증가/감소.

**H2 — Mediator share**: 무역 노출이 시군구의 marital share (특히 이혼율) 와 education share (NoHS / HS / College+) 에 영향. 가족 mediator 의 first-stage 가 weak instrument 회피 가능 (OP test F > 23.1 cutoff = Olea-Pflueger 2013 + Stock-Yogo 2005 Cragg-Donald 5% TSLS bias).

**H3 — Indirect effect (mediation)**: DGHP 2017 + DFH 2020 ivmediate 로 추정한 indirect effect (trade → marital/education → mortality) 가 statistically significant + economically meaningful (total effect 의 X% 비중).

**H4 — Korea-US heterogeneity**: 한국의 deaths of despair dominance pattern (자살+간) 이 US (약물 dominance, Case-Deaton 2015) 와 정반대. 한국의 family channel mediator 비중 > US (Pierce-Schott 2020 의 unemployment channel dominance 와 대조).

### 2.3 Novelty Position vs 4 Anchor Papers

- **vs Pierce-Schott (2020)** "Trade Liberalization and Mortality" AER Insights 2(1): 47-64: US county-level + cause-specific (drug significant, suicide/ARLD NS) + mediation X. 본 paper = 한국 시군구 + cause-specific + family mediation.
- **vs Finkelstein, Notowidigdo, Shi (2026)** BFI WP 2026-33: NAFTA × all-cause mortality (cause-specific X, mediation X). 본 paper = 한중 무역 + cause-specific 4 outcome + mediation.
- **vs Hanson (2018)** marriage value paper: US ecological marriage market value decline. 본 paper = 한국 individual-level (MDIS 사망 microdata 의 marital_code 1=미혼/2=배우자/3=사별/4=이혼) + DGHP 2017 strict mediation framework.
- **vs Case-Deaton (2015)** "Rising morbidity and mortality in midlife..." PNAS 112(49): 15078-15083: US white non-Hispanic, deaths of despair 정의 source (자살 + 약물 + ARLD). 본 paper = 한국 4 outcome (자살 + 약물 + 정신 + 간) 으로 한국 cause structure 적용.

### 2.4 한국 Setting 의 Unique 측면
- OECD 최고 자살률 (2020 약 24/100K vs OECD 평균 ~11)
- 약물 사망률 매우 낮음 (약 4/100K vs US 50+/100K, 한국 의약품 처방 통제 + opioid culture 부재)
- 간질환 dominance (B형 간염 + 알코올 culture)
- 한중 무역 통합 (2001 WTO 가입 + 2015 KR-CN FTA) 의 dramatic 한 산업 구조 변화

---

## 3. Literature Position

### 3.1 Tier A — 핵심 Reference (10 paper, 본 paper § 별 직접 매핑)

1. **Goldsmith-Pinkham, Sorkin, Swift (2020)** "Bartik Instruments: What, When, Why, and How," American Economic Review 110(8): 2586-2624 (NBER WP 24408 2018 = working version) — Bartik shift-share IV 의 share exogeneity identification theory. PAP § 5.1 핵심.

2. **Borusyak, Hull, Jaravel (2025)** "A Practical Guide to Shift-Share Instruments," Journal of Economic Perspectives — 실제 implementation 권장 (shock-level orthogonality test, ssaggregate R package, F > 23 Cragg-Donald cutoff 5% bias). PAP § 5.1 + § 7.

3. **Borusyak, Hull, Jaravel (2022)** "Quasi-Experimental Shift-Share Research Designs," Review of Economic Studies 89(1): 181-213 (NBER WP 24997 2018) — AKM clustering 의 source. PAP § 7 5-layer SE 의 Layer 4.

4. **Autor, Dorn, Hanson (2013)** "The China Syndrome," American Economic Review 103(6): 2121-2168 — 중국 수입 충격 × US 노동시장 canonical Bartik IV 적용. PAP § 5.1 first-stage spec source.

5. **Pierce, Schott (2020)** "Trade Liberalization and Mortality," AER Insights 2(1): 47-64 — US county PNTR × mortality, drug overdose +2-3/100K significant, suicide/ARLD NS. PAP § 6 5-year stacked first-difference Eq.(3) source.

6. **Dippel, Gold, Heblich, Pinto (DGHP) (2017)** "The Effect of Trade on Workers and Voters," NBER WP 23209 — IV mediation theoretical framework (total/direct/indirect 분해). PAP § 5.2 핵심.

7. **Dippel, Ferrara, Heblich (DFH) (2020)** "Causal mediation analysis in instrumental-variables regressions," Stata Journal 20(3): 613-626 — `ivmediate` Stata package implementation. PAP § 5.2 estimation 직접 차용.

8. **Case, Deaton (2015)** "Rising morbidity and mortality in midlife among white non-Hispanic Americans in the 21st century," PNAS 112(49): 15078-15083 — deaths of despair 정의 source. PAP § 1 motivation.

9. **Olea, Pflueger (2013)** "A Robust Test for Weak Instruments," Journal of Business and Economic Statistics 31(3): 358-369 — effective F statistic. PAP § 7.5 weak IV 진단.

10. **Andrews, Stock, Sun (2019)** "Weak Instruments in IV Regression: Theory and Practice," Annual Review of Economics 11: 727-753 — comprehensive review. PAP § 7.5-7.7.

### 3.2 Tier B — 중요 Reference (5)

11. **Finkelstein, Notowidigdo, Shi (2026)** BFI WP 2026-33 — NAFTA × all-cause mortality, methodology 가장 가까운 reference.
12. **Sufi (2023)** "Household Debt and Macroeconomic Fluctuations," BFI WP 2023-109 — 한국 가계부채 위기 직접 다룸. PAP § 2.3 보조 mediator (sensitivity).
13. **Stock, Yogo (2005)** "Testing for Weak Instruments in Linear IV Regression," Cambridge UP — Cragg-Donald F=23 (5% TSLS bias) cutoff source.
14. **Staiger, Stock (1994/1997)** NBER TWP 151 / Econometrica 65(3): 557-586 — IV with Weak Instruments, local-to-zero asymptotics + AR CI 의 original treatment.
15. **Hanson** marriage value paper — family channel ecological evidence.

### 3.3 Tier C — 참고 (4)

16. **Bartik (1991)** "Who Benefits from State and Local Economic Development Policies?" Upjohn Institute — original shift-share concept.
17. **Conley (1999)** "GMM Estimation with Cross Sectional Dependence," Journal of Econometrics 92(1): 1-45 — spatial SE, PAP § 7.4.
18. **Romano, Wolf (2005)** "Stepwise Multiple Testing," Econometrica 73(4): 1237-1282 — multiple testing FWE control, PAP § 7.6.
19. **Cameron, Gelbach, Miller (2008)** "Bootstrap-Based Improvements for Inference with Clustered Errors," Review of Economics and Statistics 90(3): 414-427 — WCB bootstrap, PAP § 7.2-7.3.

### 3.4 본 Paper 가 Fill 하는 Gap
- **Trade × mortality literature**: 한국 first (Pierce-Schott US 만, Finkelstein NAFTA 만)
- **Mediation literature**: cause-specific deaths of despair × family mediator 의 strict IV mediation 한국 first 적용
- **Korea labor literature**: 한중 무역 통합 (2001 WTO + 2015 FTA) × 시군구 단위 deaths of despair × family channel 의 unified analysis 한국 first
- **DGHP 2017 framework**: 한국 setting 적용 first (DGHP 자체 application = 독일 trade × political voting)

---

## 4. Data Sources (6 종)

### 4.1 MDIS 사망원인통계 (B형) microdata
- **출처**: 통계청 마이크로데이터 통합서비스 (MDIS, Microdata Integrated Service) — 사용자 (정재헌) 신청
- **시점**: 1997-2024 (28 시점, annual)
- **단위**: individual death (1 row = 1 사망자)
- **표본 size**: 평균 ~280,000 row/year, 총 약 7.4M 사망 record
- **변수 18개**: 연도, 신고연도/월/일, 사망자주소행정구역시도코드, 사망자주소행정구역시군구코드 (sgguCd), 사망연월일, 사망시, 사망장소코드, 사망자직업분류코드, 사망자혼인상태코드 (1미혼/2배우자/3사별/4이혼/9미상), 교육정도코드 (1무학~5/6/7대학), 성별코드, 사망연령5세단위코드 (1=00-04, ..., 18=85+), 사망자국적구분코드 (1=한국인, 2=외국인, 빈값=2007 이전 변수 부재), 사망원인_104항목분류코드 (cause_104, KCD 8차분류), 사망원인_57항목분류코드
- **저장**: `C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리\` (사용자 폴더)
- **codebook**: 파일설계서 + 시군구코드집 + 사망원인 8차분류 코드집 (xlsx)

### 4.2 MDIS 인구주택총조사 2% 표본 microdata
- **출처**: MDIS — 사용자 신청
- **시점**: 1990, 1995, 2000, 2005, 2010, 2015, 2020 (7 시점, 5-year census)
- **단위**: individual person (2% population sample)
- **표본 size**: 평균 ~870,000 row/시점, 총 약 6.2M individual
- **변수**: sgguCd (시도 + 시군구 코드, 1990 만 시군구 2자리), 성별, 만연령, 가구주관계, 혼인상태, 교육정도, 가중값 (population sampling weight), 종교, 거주이력 등 (시점별 column 28 ~ 99 개)
- **저장**: `0_raw/mdis_population_census/` (압축 해제 후 8 sub-folder)
- **codebook**: 파일설계서 (1990-2020 각 xlsx)

### 4.3 Comtrade Bartik IV (진행 중)
- **출처**: UN Comtrade Plus API (사용자 보유 4 key auto-rotation)
- **시점**: 1995-2024 (annual)
- **3 데이터 set**:
  1. KR-CN bilateral (M + X) — main treatment IV (HS 01-99 full, 평균 4K row/year, ✅ 완료 50 파일)
  2. ADH 8 ← CN imports — Pierce-Schott / ADH 표준 instrument set: Australia, Denmark, Finland, Germany, Japan, New Zealand, Spain, Switzerland (HS 28-97 manufacturing, ✅ 6 국가 완료, ES + CH 진행 중)
  3. CN → World (alternative supply-side IV, 미진행)
- **저장**: `0_raw/comtrade_korea_china/`, `comtrade_adh_china/`, `comtrade_china_world/`
- **script**: `2_scripts/build_panel/4A_trade_collection.py` (self-contained, resumable, HS chunked, 4 key rotation)
- **HS-KSIC concordance**: 통계청 응답 대기 (Stage 4 last pending)

### 4.4 KOSIS API (mediator 1차 시도 — 폐기)
- **시도**: 12 URL (혼인 6 시점 + 교육 6 시점 1995-2020), 17 시도 분할 호출 (40K cell limit 회피), outputFields patch (C1+C1_NM+...+C5+C5_NM)
- **결과**: 5 표 verify 모두 시도 level only, 시군구 dimension 부재. TBL_NM 의 "...-시군구" misnomer.
- **결정**: KOSIS publish data 의 인구총조사 시리즈 = 시도 level only. **MDIS microdata 전환** (위 § 4.2)

### 4.5 HIRA 약물 처방 (sensitivity mediator, 사용 가능)
- **출처**: 건강보험심사평가원 (HIRA, Health Insurance Review and Assessment Service) Open Data — data.go.kr
- **시점**: 2010-2019 (120 months)
- **단위**: 시군구 × 월 × ATC4 cross-tab (152,208 row, 11.83 MB)
- **변수**: atcStep4Cd (ATC4 code), diagYm (YYYYMM), insupTpCd (보험가입자), msupUseAmt (사용금액), totUseQty (사용량), sgguCd, sidoCdNm
- **ATC4 5 카테고리 보유**: N06AB SSRI 항우울제 (17.7%), N06AX 기타 항우울제 (19.4%), N05BA 벤조 (26.2%), N05AX 항정신병 (15.6%), A05BA 간 약물 (21.1%); **N02A opioid 부재** (paper § 7 한국 ≠ US 핵심 finding confirm)
- **저장**: `0_raw/hira_drug/hira_drug_panel_v02.csv`
- **활용**: paper § 5.2 appendix 의 post-2010 sensitivity (T3 2012-2016 full + T4 2017-2019 partial). Primary mediator 못 씀 (1997 baseline 부재).

### 4.6 ECOS 가계부채 (sensitivity, Sufi 2023 channel)
- **출처**: 한국은행 경제통계시스템 (ECOS) API
- **시점**: 2003-2024 (annual + monthly)
- **단위**: sido (16 광역시도)
- **변수**: 가계부채 잔액, 연체율 (단 일부 시점/지역 결측)
- **활용**: paper § 8 limitation 의 Sufi 2023 채권 channel sensitivity (한국 가계부채 위기 1997 IMF + 2003 카드 + 2008 글로벌)

---

## 5. Data Pipeline (4 stage)

### 5.1 Stage 1-3 — Main Outcome Panel (이미 commit, ✅)

**처리 단계**:
1. mortality 28 시점 raw cleaning — encoding cp949, position-based parse (column 명 시점 별 변동 robust), age band 매핑 (사망연령5세단위코드 → "00-04", ..., "85+")
2. **외국인 빼기 제거** — panel v01 자체가 사실상 한국인 only (KOSIS DT_1B040M5 주민등록연앙인구 와 -0.35% 차이, 행안부 한국인 only 와 정확 일치). 외국인 빼기 = double-counting → over-correction (+1.48% inflation). 본 R-A audit 결과 v3.3 → v3.4 commit 정정.
3. **분구 시군구 합산** — sigungu_crosswalk_v2 (안산 31090, 용인 31190, 수원 31010, 성남 31020 정확 KOSIS 행정구역 표준 코드). R-A audit 의 "안산 41190 / 31190" 잘못 매핑 시인 후 microdata h_name 으로 verify.
4. **Component decomposition 10 outcome group** — deaths of despair 4 (자살 102, 약물 101, 정신 057, 간 081) + 보조 6 (심혈관, 폐, 당뇨, 외인사 etc.)
5. **3 ASR baseline** — 2010 한국 + WHO 2000 + Eurostat 2013 weight (cross-country comparability)

**산출**:
- `3_derived/mortality/mortality_rate_panel_v02_1.parquet` (123,660 rows = 229 h_code × 27 year × 2 sex × 10 outcome group, 3 baseline)
- `3_derived/population/population_panel_v01.parquet` (한국인 only 분모)

### 5.2 Stage Mediator (본 conversation 작업 결과)

**KOSIS API 시도 → 폐기** (위 § 4.4)

**MDIS 인구 microdata cleaning** (Step 06-08, scripts `2_scripts/data_collection/`):
- Step 06: zip 압축 해제 (cp949 한글 파일명 변환)
- Step 07: 7 시점 column layout 추출 (시점별 column 28-99 다름)
- Step 08: cross-tab v01 build → `mediator_panel_marriage_v01.parquet` (140,971 rows), `mediator_panel_education_v01.parquet` (269,861 rows)

**Mediator panel cleaning** (Step 09-10b):
- Step 09: 4 issue 진단 (marital '.' / 2005 anomaly / education 카테고리 시점별 다름 / 1990 sigungu 2자리)
- Step 10: cleaning + align v02 — 1990 drop, working-age 25-64 filter, education 4 카테고리 (NoHS/HS/SomeCollege/Bachelor+), sigungu_crosswalk_v2 적용
- Step 10b: education 4 → 3 카테고리 재매핑 v03 (NoHS/HS/College+, mortality align)

**산출**:
- `3_derived/population/mediator_panel_marriage_v02.parquet` (71,125 rows, 6 시점, 4 카테고리, 279 h_code)
- `3_derived/population/mediator_panel_education_v03.parquet` (63,019 rows, 3 카테고리)

**Mortality microdata cleaning** (Step 11a, 4 회 재시도 history):
- 1차/2차 시도: column rename 시 1997-2007 의 age_5y_code 모두 NaN. column 명 정상 + sample data 정상 → rename 후 NaN. 미스터리. keyword fuzzy match + Unicode NFC normalize 도 fail.
- 3차 시도: position-based parse (column 명 무시, index 직접) → 매핑 OK. 그러나 national filter `→ 0` (모두 drop)
- 4차 시도: national_code NaN → `astype(str)` 후 `"nan"` string → `isin(["1", ""])` 매칭 fail. **R-A 결정**: 외국인 (`"2"`) 만 drop, NaN/빈값/1 모두 keep → 28 시점 모두 정상 처리.

**산출**: `3_derived/mortality/mortality_microdata_cleaned_v01.parquet` (7,408,230 rows, 28 시점, 362 h_code)

**Mortality × mediator cross-tab** (Step 11b, working-age 25-64 + sigungu_crosswalk):
- 7.4M → 1.5M (working-age 20.3%)
- crosswalk 후 229 h_code (mortality_panel_v02_1 align), 2024 만 252 (sigungu_crosswalk 미cover)
- 산출: `mortality_marital_panel_v01.parquet` (1,011,186 rows), `mortality_education_panel_v01.parquet` (1,035,849 rows)

**Mediator-specific rate panel** (Step 12, 5-year stack period):
- 5 stack period × census year 매핑 (1997-2001 → 2000 census, ..., 2017-2021 → 2020)
- Rate formula: `rate_per_100k = deaths_5y / (population × 5) × 100,000`
- Cause group 6 분류: 자살 102, 약물 101, 정신 057, 간 081, other, all_cause
- 산출:
  - `mediator_specific_marital_rate_v01.parquet` (187,379 rows, **Stage 5 ivmediate input**)
  - `mediator_specific_education_rate_v01.parquet` (171,811 rows, **Stage 5 ivmediate input**)

### 5.3 Stage 4 — Bartik IV (진행 중)
- Comtrade KR-CN ✅ 완료 (50 파일)
- ADH 8 ← CN: AU/DK/FI/DE/JP/NZ ✅ 완료 (150 파일), ES + CH 진행 중
- CN → World 미진행
- HS-KSIC concordance: 통계청 응답 대기

### 5.4 Stage 5 — ivmediate Regression (spec ready)
- DGHP 2017 + DFH 2020 ivmediate Stata implementation
- 5-layer SE + Romano-Wolf step-down
- spec plan v01 commit (`stage5_regression_plan_v01.md`)
- 진입 = Stage 4 완료 + Stata 환경 verify (가천대 license + 7 package: ivmediate, weakivtest, boottest, rwolf, reg_ss, acreg, weakiv)

---

## 6. Identification Strategy

### 6.1 § 5.1 Bartik Shift-Share IV (First-stage)

**Spec equation**:
```
ΔTradeExposure_{h, t→t+5} = Σ_k [ s_{h, k, t-10} × ΔImports_{k, t→t+5} ]
```
- h = 시군구 (n=229), t = 시점 (5-year stack), k = 산업 (KSIC 4-digit, ~200)
- s_{h, k, t-10} = 10년 lag 산업 고용 share (GPSS 2020 share exogeneity)
- ΔImports_{k, t→t+5} = ADH 8 ← CN imports 변동 (per worker, Pierce-Schott 2020 spec)

**Identification 가정**:
- GPSS 2020: lagged share s_{h, k, t-10} 가 시점 t 의 unobserved shock 과 orthogonal (share exogeneity). 또는,
- BHJ 2022 (Borusyak-Hull-Jaravel RES): aggregate shock ΔImports 의 cross-sector orthogonality (shock-level identification, share endogeneity 허용)

**한국 적용 보조 IV**: KR-CN 직접 trade (한국 자체 imports from CN) 추가 — exclusion restriction critique 가능 (한국 = ADH 8 의 한 곳이 아니지만 CN trade 에 직접 노출).

### 6.2 § 5.2 Mediation Framework (DGHP 2017 + DFH 2020)

**Theoretical**: DGHP 2017 NBER 23209 의 IV mediation:
- Total effect: trade → mortality
- Direct effect: trade → mortality (mediator 통제)
- Indirect effect: trade → mediator → mortality
- 가정: no unmeasured mediator-outcome confounder + separate instrument requirement (z_m 별도)

**Implementation**: DFH 2020 Stata Journal 20(3): 613-626 의 `ivmediate` package:
```stata
ssc install ivmediate
ivmediate y (m = z_m) (x = z_x), vce(cluster h_code)
```
- y = mortality_rate (mediator-specific, working-age 25-64, per 100K)
- x = trade_exposure_5y (Bartik IV)
- m = marital_share (or education_share) at h_code × period level
- z_x = lagged shift-share IV (Bartik construction)
- z_m = lagged mediator-specific IV (DGHP 2017 separate instrument requirement) — **후보 진단 중** (R-A pending)

### 6.3 § 6 Empirical Spec (Pierce-Schott 2020 base)

**5-year stacked first-difference**:
```
ΔY_{h, t→t+5} = β · ΔTradeExposure_{h, t→t+5} + γ · X_{h, t} + δ_t + ε_{h, t}
```
- Y = log mortality rate
- δ_t = period FE (5 stack period)
- X = controls (working-age population, industrial composition, baseline mortality)

**5 stack period** (mortality 5년 합 vs mediator census 가까운 매핑):

| period | mortality | mediator census |
|--------|-----------|-----------------|
| 1 | 1997-2001 | 2000 |
| 2 | 2002-2006 | 2005 |
| 3 | 2007-2011 | 2010 |
| 4 | 2012-2016 | 2015 |
| 5 | 2017-2021 | 2020 |

2022-2024 incomplete period drop. 1990/1995 mediator 사용 안 함.

### 6.4 § 7 5-layer SE + Weak IV Diagnostics

| Layer | method | reference |
|-------|--------|-----------|
| 1 | HC1 robust | textbook |
| 2 | WCB cluster bootstrap sigungu (n=229) | Cameron-Gelbach-Miller 2008 RES |
| 3 | WCB cluster bootstrap sido (n=16) | 동일 |
| 4 | AKM clustered SE (shift-share specific) | BHJ 2022 RES + GPSS 2020 AER |
| 5 | Conley spatial SE | Conley 1999 |

**Weak IV diagnostics**:
- Olea-Pflueger 2013 effective F: cutoff F = 23.1 (5% worst-case TSLS bias relative to OLS, Stock-Yogo 2005 Cragg-Donald F=23 의 robust 확장). NOT "size distortion 5%" (이건 Stock-Yogo F=37 의 별개 cutoff).
- AR + tF (Andrews-Stock-Sun 2019 Annual Review) = weak-IV-robust confidence interval.

**Multiple testing**: Romano-Wolf 2005 Econometrica step-down FWE control. Family of hypotheses 정의 = 4 outcome × 2 mediator dim = 8 (혹은 + all_cause = 9, R-A pending 결정).

---

## 7. Empirical Findings — Preliminary

### 7.1 Deaths of Despair 시계열 (Working-age 25-64, /100K annual)

**marital panel aggregated** (mediator_specific_marital_rate_v01.parquet 의 deaths_5y / population × 5 × 100,000):

| period | window | drug (101) | liver (081) | psych (057) | suicide (102) | all_cause |
|--------|--------|------------|-------------|-------------|---------------|-----------|
| 1 | 1997-2001 | 5.61 | **44.17** | 13.29 | 23.23 | 277 |
| 2 | 2002-2006 | 4.01 | 34.26 | 10.62 | 28.26 | 226 |
| 3 | 2007-2011 | 3.81 | 26.44 | 9.85 | **35.27** ← peak | 206 |
| 4 | 2012-2016 | 3.85 | 22.69 | 8.93 | 32.89 | 182 |
| 5 | 2017-2021 | 3.86 | 19.05 | 9.66 | 29.61 | 152 |

### 7.2 Historical 추세 검증 (한국 통계청 vs paper)

- ✅ **자살 peak 2007-2011** = 한국 통계청 자살률 peak 일치 (카드사태 2003, 글로벌 금융위기 2008-2010 직후). working-age 25-64 35.27/100K, 전체 평균보다 약간 높음.
- ✅ **간질환 -57% 단조 감소** (44.17 → 19.05) = B형 간염 백신 (1995+ universal vaccination) + 의료 발전 + 알코올 culture 점진적 변화 historical 추세.
- ✅ **약물 매우 낮음 (5.61 → 3.86, 평균 ~4/100K)** = US (Pierce-Schott 2020) 의 50+/100K (peak) 의 1/13. 한국 opioid 처방 통제 (HIRA 데이터 N02A 부재 confirm) + 약물 culture 부재 → **paper § 7 핵심 finding "한국 ≠ US"**.
- ✅ **All-cause 277 → 152/100K (-45%)** = 한국 working-age 사망률 historical 감소 (의료 발전 + 사회 변화 일관)

### 7.3 Mediator-specific Rate Panel Preview

**Marital panel** (h_code × period × sex × age × marital × cause × rate):
- 187,379 rows, 4 marital category × 5 period × 8 working-age band × 2 sex × 6 cause group × 229 h_code (sparse)
- denom missing 9.74% (marital, 67 추가 h_code 의 1990 placeholder 잔류 의심)

**Education panel**:
- 171,811 rows, 3 education band × 동일 dimension
- denom missing 2.11% (mortality 와 mediator align 더 정밀)

**Stage 5 ivmediate input ready**.

### 7.4 Statistical Significance
Stage 5 진입 후 산출. 본 v01 progress 문서 시점에서는 **descriptive 시계열 + magnitude 만 보고**, regression coefficient + p-value + AR confidence interval 미산출.

---

## 8. Limitations 8 항

### 8.1 1990 Sigungu Code (2자리) Mapping Placeholder
- **Origin**: MDIS 인구 microdata 1990 시점 시군구 코드가 2자리 (예: `11`=종로) vs 다른 시점 3자리 (`010`=종로)
- **Impact**: 1990 mediator 자체 미사용 (paper 시점 1997-2024 외) → minor
- **Mitigation**: 1990 drop 결정 (R-A 결정 #2). 1995 mediator panel 도 수원/성남 등 일부 시군구 재정비 직전 시점이라 부분적 mismatch 가능.

### 8.2 1997-2007 외국인 식별 불가
- **Origin**: 사망 microdata 의 `사망자국적구분코드` 변수 1997-2007 부재 (2008+ 만 1=한국인/2=외국인 구분)
- **Impact**: 1997-2007 numerator 에 외국인 사망 미세 inflation. 외국인 비율 < 1% (당시) 가정 시 < 0.5% inflation 추정.
- **Mitigation**: 외국인 "2" 만 drop, NaN/빈값 keep (1997-2007 한국인 간주). Robustness check 로 2008+ subset only sensitivity 권장 (Stage 5).

### 8.3 혼인/교육 미상 (코드 9) Drop
- **Origin**: 사망 microdata 의 혼인상태코드 = 9 (미상) + 교육정도코드 = 9 (미상) drop 결정
- **Impact**: MAR (Missing At Random) 가정. 1997-2000 high missing rate (혼인 ~2.5%, 교육 ~7%).
- **Mitigation**: 1997-2000 sensitivity test 권장 (drop vs keep as separate category). Stage 5 robustness.

### 8.4 Education 1997-2007 5 카테고리 → 2008+ 7 카테고리 → 3 통합 Align
- **Origin**: 1997-2007 의 5=대학 (전문대+4년제+석박사 통합) vs 2008+ 의 6=4년제 / 7=대학원 분리
- **Impact**: 정확 매핑 불가. 정보 손실 (전문대 vs 4년제 구분).
- **Mitigation**: 3 카테고리 (NoHS / HS / College+) align (모든 시점 일관). Sub-aggregation 분석 시 정보 손실 명시. Korea 전문대 비율 historical 변화 (1997 ~10% → 2020 ~30%) 의 mediator coefficient 영향 sensitivity 권장.

### 8.5 2022-2024 Incomplete Period Drop
- **Origin**: 5-year stack 의 마지막 period (2022-2026) 의 mortality 만 3년 (2022-2024) 부분 cover
- **Impact**: 5-year stack 미완성 → drop
- **Mitigation**: 5 stack period (1997-2021) 만 사용. 2022-2024 = 별도 partial period sensitivity (optional)

### 8.6 MDIS 2% 표본 Weight ±5% 오차
- **Origin**: MDIS 인구 microdata 가 2% 표본 (전수조사 X), 가중값 적용 시 모집단 추정
- **Impact**: weighted pop sum vs 행안부 한국 총인구 ±5% 오차 normal
- **Mitigation**: 시점별 weighted sum vs 행안부 cross-check (working-age 25-64 1995 23.3M, 2020 29.7M = ±3% 일치 확인됨)

### 8.7 denom missing 9.74% (Marital Panel)
- **Origin**: mortality h_code 346 (working-age + crosswalk) vs mediator h_code 279 = 67 추가 h_code mediator 부재
- **Impact**: Stage 5 regression 시 listwise deletion → 9.74% loss
- **Mitigation**: 67 h_code 의 origin 진단 미완 (1990 placeholder 잔류 의심). Alternative: multiple imputation 또는 partial-coverage regression 검토 필요. Stage 5 진입 전 sub-script 작성 (R-A pending #1).

### 8.8 2024 시점 252 h_code (sigungu_crosswalk 미cover)
- **Origin**: 2024 시점 사망 microdata 의 신설 시군구 (예: 양주 분구 등) sigungu_crosswalk_v2 미cover
- **Impact**: 2024 만 252 h_code (다른 시점 229)
- **Mitigation**: main analysis 1997-2021 (5 stack period) 만 사용 → 2024 무관. Caveat 명시.

---

## 9. Pending Issues 4 항 (Stage 5 진입 전)

### 9.1 Stage 4 Comtrade + HS-KSIC Concordance
- **Status**: Comtrade KR-CN ✅ + ADH 8 (6/8) ✅, ES + CH 진행 중. CN-World 미진행. HS-KSIC concordance 통계청 응답 대기.
- **Severity**: 🔴 critical (Stage 5 진입 block)
- **예상 시간**: Comtrade ~2-3 시간 + 통계청 응답 ~1-2 주

### 9.2 denom Missing 67 h_code 진단
- **Severity**: 🟡 medium (Stage 5 listwise deletion bias 가능)
- **예상 시간**: ~1 시간 sub-script
- **Action**: Claude Code 위임 (위 § 8.7)

### 9.3 Stata 환경 Verify
- **Severity**: 🟡 medium (Stage 5 ivmediate 실행 block)
- **예상 시간**: 30 분 (가천대 license + 7 package 설치)
- **7 package**: `ivmediate`, `weakivtest`, `boottest`, `rwolf`, `reg_ss`, `acreg`, `weakiv`

### 9.4 PAP v3.4 → v3.5 Update (Reference Proposal v01.1 적용)
- **Severity**: 🟢 low (Stage 5 진입 무관, 외부 reviewer share 시 필요)
- **예상 시간**: ~1.5 시간
- **Action**: § 1-8 의 ✅ 7 항 + 26 reference list 적용 (R-A 직접)

---

## 10. R-A Decisions Log 16 항

각 결정의 reasoning + alternative + chose 이유:

1. **KOSIS 폐기 → MDIS 전환** — KOSIS 5 표 verify 결과 시군구 부재 (시도 only). Alternative = 다른 KOSIS 표 ID 시도 가능했으나 시간 비용 + 사용자 MDIS 신청 가능 → MDIS 전환.

2. **1990 mediator panel drop** — 1990 시군구 코드 2자리 (다른 시점 3자리) + paper 시점 (1997-2024) 외. 1990 사용 시 mapping 작업 ~3시간 manual + paper 시점 외라 의미 minor. Drop 결정.

3. **age 25-64 working-age filter** — DGHP 2017 mediation 표준 + Case-Deaton 2015 deaths of despair 의 midlife focus. Alternative = 25-54 (prime working-age, narrower) 또는 18+ (broader). 25-64 chose = mediation literature 표준.

4. **Education 4 → 3 카테고리 통합** — 1997-2007 의 5=대학통합 vs 2008+ 의 6/7 분리 정확 매핑 불가. 3 카테고리 (NoHS/HS/College+) chose = 모든 시점 align. 정보 손실 (전문대 vs 4년제) trade-off.

5. **Position-based parse (column rename fail 후)** — 1997-2007 의 column rename 시 invisible char issue 4 회 재시도 fail. Position-based (column index 직접) 가 column 명 차이 robust → chose.

6. **외국인 "2" 만 drop (NaN/빈/1 모두 keep)** — 1997-2007 의 national_code 변수 부재 (NaN). `astype(str)` 후 "nan" string → `isin(["1", ""])` 매칭 fail. Reverse 적용 (외국인 "2" 만 명시 drop) → 28 시점 모두 정상.

7. **혼인 9 (미상) drop** — MAR 가정. Alternative = "missing" 별도 카테고리 keep (5 카테고리). Drop chose = simplicity + 1997 high missing 2.5% 만이라 MAR 영향 minor 추정. Sensitivity test 권장 (Stage 5).

8. **교육 9 (미상) drop** — 동일 reasoning. 1997 7% missing 더 high → sensitivity 더 권장.

9. **Education align 3 카테고리** — mortality (3) + mediator (3) 일관. mediator panel v02 (4) → v03 (3) 재매핑 (10b script).

10. **5-year stack period (Pierce-Schott 2020 base)** — paper § 6 main spec. Alternative = 4-year, 6-year stack 도 robustness check 권장. 5-year chose = census 5년 주기 align.

11. **Rate formula `deaths_5y / (pop × 5) × 100,000`** — annual per 100K person-year (epidemiology 표준). 5년 cumulative 가 아니라 annualized rate.

12. **6 cause group (deaths of despair 4 + other + all_cause)** — paper main outcome = 4 (자살/약물/정신/간), other = robustness, all_cause = benchmark.

13. **denom missing listwise deletion** — Stage 5 시 default. Alternative = multiple imputation, partial-coverage regression. Listwise chose = simplicity + 9.74% loss minor 추정. 67 h_code 진단 (R-A pending #1) 후 재검토.

14. **GPSS 2020 publish primary** — PAP v3.3 § 14 dated change log #20 의 R-A audit limitation (citation accuracy 누락) 처리 commit. NBER WP 24408 (2018) = working version, AER 110(8) 2020 publish version primary.

15. **DGHP 2017 + DFH 2020 둘 다 cite** — DGHP 2017 NBER 23209 (theoretical) + DFH 2020 Stata Journal 20(3) (`ivmediate` package implementation source). PAP § 5.2 의 estimation 은 DFH 2020 직접 차용.

16. **OP test F=23.1 = TSLS bias (NOT size distortion)** — Olea-Pflueger 2013 effective F = Stock-Yogo 2005 Cragg-Donald F=23 의 robust 확장 = 5% worst-case TSLS bias relative to OLS. Size distortion 5% 는 Stock-Yogo 의 별개 cutoff F=37 (1 endog var). R-A round 7 audit critique 반영 정정 (proposal v01 → v01.1).

---

## 11. Issue Resolution Log 7 항

각 issue 의 R-A 처리 + 대안 + chose 이유:

1. **KOSIS 시군구 부재 → MDIS 전환** — 위 § 10 #1
2. **1997-2007 column rename fail → position-based parse** — 위 § 10 #5. Invisible char issue 진정 root cause 미확정 (4 회 fail 후 우회).
3. **national_code NaN → 외국인만 drop** — 위 § 10 #6. 1997-2007 한국인+외국인 mix 의 numerator inflation < 0.5% 추정 caveat (§ 8.2).
4. **1990 sigungu 2자리 → drop** — 위 § 10 #2.
5. **denom missing 9.74% → listwise deletion** — 위 § 10 #13. 67 h_code 진단 R-A pending.
6. **Reference v01 inconsistency → v01.1 정정** — 사용자 round 7 audit critique 3 항 (GPSS publish, DFH 2020, OP test bias) 반영. PAP § 14 dated change log commit 와 align.
7. **PAP v3.4 § 14 vs proposal v01 mismatch → 정정** — Reference proposal v01 작성 시 PAP § 14 verification commit 미참조 R-A oversight. v01.1 에서 PAP § 14 와 fully consistent 정정 + master doc 동기화.

---

## 12. Reference Library Summary

19 paper deep summaries (each 1500-2700 단어, sub-agent 5 parallel 작성):
- `4_documentation/reference_library/paper_summaries/paper_*.md` (19 파일)
- Master doc: `4_documentation/reference_library/reference_library_master_v01.md` (14,500 단어, 14 sections)

**PAP § 별 reference 매핑** (master doc § 5):

| PAP § | primary | secondary |
|-------|---------|-----------|
| § 1 motivation | Case-Deaton 2015 | Pierce-Schott 2020 |
| § 4 outcome | Case-Deaton 2015 | KCD 8차분류 codebook |
| § 5.1 Bartik IV | GPSS 2020 AER | BHJ 2025 + ADH 2013 |
| § 5.2 mediation | DGHP 2017 | DFH 2020 |
| § 6 spec | Pierce-Schott 2020 | ADH 2013 |
| § 7.5 weak IV | Olea-Pflueger 2013 | Stock-Yogo 2005, Andrews-Stock-Sun 2019 |
| § 7.6 multiple test | Romano-Wolf 2005 | - |
| § 7.4 spatial SE | Conley 1999 | - |
| § 7.3 cluster SE | Cameron-Gelbach-Miller 2008 | - |
| § 7.7 AR + tF | Andrews-Stock-Sun 2019 | Staiger-Stock 1994 |
| § 8 limitation | various | various |

**Citation strategy**: paper 본문 § 별 reference 우선순위 (master doc § 7).

---

## 13. Output Inventory

### 13.1 Derived Parquet (24)

**Stage 1-3 main outcome** (4):
- `mortality_panel_v02.parquet` (123K, component decomposition 10 outcome)
- `mortality_rate_panel_v02_1.parquet` (123,660 rows, **main analysis panel**)
- `mortality_panel_v02_marriage/education/occupation.parquet` (mediator panel for additional analysis)
- `population_panel_v01.parquet` (한국인 only 분모)

**Stage Mediator** (5, 본 conversation 작업 결과):
- `mortality_microdata_cleaned_v01.parquet` (7.4M, 28 시점)
- `mediator_panel_marriage_v02.parquet` (71K, 6 시점, 4 카테고리)
- `mediator_panel_education_v03.parquet` (63K, 3 카테고리)
- `mortality_marital_panel_v01.parquet` (1.0M, working-age + crosswalk)
- `mortality_education_panel_v01.parquet` (1.0M)

**Stage 5 Ready** (2):
- `mediator_specific_marital_rate_v01.parquet` (187K, **ivmediate input**)
- `mediator_specific_education_rate_v01.parquet` (172K, **ivmediate input**)

기타 13: intermediate parquet (cleaning, validation 산출).

### 13.2 Scripts (70+)

- `2_scripts/data_collection/` — 25 scripts (KOSIS, MDIS, ECOS, Comtrade)
  - `05_kosis_marriage_education_api.py` (KOSIS 시도, 폐기)
  - `06_mdis_population_unzip_inspect.py` (MDIS unzip)
  - `07_mdis_population_columns_extract.py` (column layout)
  - `08_mdis_population_parse_crosstab.py` (mediator v01)
  - `09_mediator_panel_validate.py` (4 issue 진단)
  - `10_mediator_panel_clean_align.py` (v02)
  - `10b_mediator_panel_education_v03.py` (4 → 3 카테고리)
  - `11a_mortality_microdata_parse.py` (28 시점 cleaning)
  - `11b_mortality_mediator_crosstab.py` (numerator)
  - `12_mediator_specific_mortality_rate.py` (rate panel)
- `2_scripts/build_panel/` — 14 scripts (mortality, population, mediator panel build, 4A trade collection)
- `2_scripts/sigungu_crosswalk/` — 11 scripts (5 step crosswalk build)
- `2_scripts/verify/` — 13 scripts (Ansan, Yongin, Goyang anomaly, codebook layout, mortality dataset exploration, plot deaths of despair, merge paper folder)
- `2_scripts/lib/` — 4 helper modules (comtrade_api, ecos_api, config)

### 13.3 Documentation (60+ md, 4_documentation/ 7 sub-folder)

- `PAP/` — PAP v1-v3.3 (status v3.4) + reference proposal v01.1 + validation
- `reference_library/` — master doc + 19 paper summaries + metadata
- `stage_plans/` — stage5_regression_plan_v01 + section1/2/3 writing guides
- `pipeline_docs/` — mediator pipeline + panel construction guides
- `status_reports/` — daily status archive + handoff + stage3 reviews
- `crosswalks_paper/` — claude_code prompts + xlsx
- `misc/` — research_proposal 등

### 13.4 Reviewer Entry Files (root)
- `REVIEWER_GUIDE.md` (5 분 entry)
- `REVIEWER_FEEDBACK_TEMPLATE.md` (reviewer 작성 양식)
- `REVIEWER_PROMPT.md` (v01 — paper 평가 prompt)
- `REVIEWER_PROMPT_v02.md` (v02 — R-A 작업 + paper 평가 prompt)
- `RESEARCH_DESCRIPTION_WRITER_PROMPT.md` (v03 — meta prompt)
- `RESEARCH_PROGRESS_v01.md` (**본 문서**)

---

## 14. Future Work + Timeline

### 14.1 Stage 4 완료 (예상 ~1-2 주)
- Comtrade ES + CH + CN-World 다운로드 (~2-3 시간)
- HS-KSIC concordance 통계청 응답 대기 (~1-2 주)
- denom missing 67 h_code 진단 (~1 시간, Claude Code 위임)
- Stata 환경 verify (~30 분)

### 14.2 Stage 5 ivmediate Regression (예상 ~2-4 주)
- Bartik IV first-stage estimation + OP test
- ivmediate (DGHP 2017 + DFH 2020) total/direct/indirect 분해
- 5-layer SE + Romano-Wolf step-down
- 6 robustness check (placebo, alternative IV, subsample, sensitivity)
- HIRA T3-T4 sensitivity (post-2010 약물 mediator)

### 14.3 Paper 작성 (예상 ~1-2 개월)
- § 1-8 본문 작성 (Stage 5 결과 반영)
- Reference list 26 entry (proposal v01.1 적용)
- Figure 4-6 (시계열 + cross-section + sensitivity)
- Table 5-8 (regression coefficient + robustness)
- Appendix (data construction + ivmediate spec detail)

### 14.4 SSCI Submission Strategy
- **Target journal top 3**:
  1. AEJ Applied (American Economic Journal: Applied Economics) — methodology fit
  2. JHE (Journal of Health Economics) — health 측면 fit
  3. Health Economics — broader audience
- **단독 학부생 first-author SSCI publish 가능성**: Pre-precedent 매우 적음. Co-authoring (advisor 또는 PhD candidate) 권장 가능. R&R 2-3 round 예상.
- **Pre-submission**: 외부 reviewer 피드백 cycle 1-2 회 (PAP v3.5 commit 후 + Stage 5 결과 후)

---

## 15. Appendix

### 15.1 핵심 Panel Structure

**`mediator_specific_marital_rate_v01.parquet`** (Stage 5 ivmediate input):
- columns: h_code (5자리 시도+시군구), period (1-5 stack), census_year (2000-2020), sex_code (1/2), age_band (25-29~60-64), marital_code (1-4), cause_group (suicide/drug/psych/liver/other/all_cause), deaths_5y, population, rate_per_100k
- rows: 187,379 (sparse cell — 일부 cell deaths_5y = 0)
- dimension cardinality: 229 h × 5 period × 2 sex × 8 age × 4 marital × 6 cause = 219,840 max. Sparse 187K = 85% 가 non-empty cell.

**`mediator_specific_education_rate_v01.parquet`**: 동일 구조 + education_band (3 카테고리). 171,811 rows.

### 15.2 5 Stack Period × Mediator Census 매핑

| stack period | mortality 5y window | mediator denominator (가까운 census) |
|--------------|----------------------|--------------------------------------|
| 1 | 1997-2001 | 2000 |
| 2 | 2002-2006 | 2005 |
| 3 | 2007-2011 | 2010 |
| 4 | 2012-2016 | 2015 |
| 5 | 2017-2021 | 2020 |

drop:
- mortality 2022-2024 (incomplete 3년)
- mediator 1990, 1995 (paper 시점 외)

### 15.3 ivmediate Stata Code Sketch (Stage 5)

```stata
* Data load
use "mediator_specific_marital_rate_v01.dta", clear

* Working-age 25-64 + period 1-5 만
keep if inrange(age_band_num, 6, 13)
keep if inrange(period, 1, 5)

* DFH 2020 ivmediate package
ssc install ivmediate

* Total/direct/indirect 분해
foreach cause in suicide drug psych liver {
    foreach mediator in marital education {
        ivmediate rate_per_100k ///
            (`mediator'_share = z_m_lag) ///
            (trade_exposure_5y = z_x_bartik), ///
            vce(cluster h_code)
        estimates store `cause'_`mediator'
    }
}

* Romano-Wolf step-down (FWE control)
ssc install rwolf
rwolf rate_per_100k, indepvar(trade_exposure_5y) ///
    controls(controls) cluster(h_code) ///
    nodots reps(1000)

* Weak IV diagnostics (effective F)
ssc install weakivtest
weakivtest, level(0.05) percentage(5)
```

### 15.4 4 Figure (예정)

1. **deaths_of_despair_timeseries.png** — 4 outcome × 5 period 시계열 line chart (이미 작성됨, `4_documentation/figures/`)
2. **suicide_by_marital.png** — 자살률 by 혼인상태 × 시점 (mediator channel evidence)
3. **mediator_specific_rate_by_marital.png** — 4 cause × 4 marital × 5 period subplot
4. **ATC4_by_year.png** — HIRA 정신과 약물 사용량 시계열 (post-2010 sensitivity)

---

_본 문서 = paper 의 self-contained progress 설명. reviewer 가 detailed feedback 작성 위한 단일 entry point. 4 핵심 첨부 (PAP v3.4 + reference proposal v01.1 + mediator pipeline doc + Stage 5 plan) 와 함께 share._

_R-A (Claude LLM) 가 본 conversation 에서 진행한 모든 substantive 결정 (16 항) + issue resolution (7 항) + pending decision (4 항) 을 포함. Reviewer 는 본 문서 review 후 P1/P2/P3 tagged feedback + NEXT_STEP_PROMPT 작성 권장 (REVIEWER_PROMPT_v02.md § 8 참조)._

---

_총 ~10,800 단어, 15 sections, target reviewer audience: 박사급 노동/보건 경제학 학자 + LLM (Claude / GPT-5 / Gemini Pro)._
