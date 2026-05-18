# Stage 5 — Regression Analysis Plan v01 **작성**: 2026-05-03
**Stage 5 입력**: panel v02.1 (mortality_rate_panel_v02_1.parquet) + Stage 4 무역 + KSIC concordance + 가족 mediator
**Stage 5 산출**: paper Section 4-7 main result + robustness + mediation 결과
**Reference verified**: DGHP 2017 NBER 23209 + DFH 2020 Stata Journal + GPSS 2020 AER + OP 2013 + AKM 2019 + BHJ 2022 + Pierce-Schott 2020 + ADH 2013 + Romano-Wolf 2005 + CGM 2008 + Roodman et al 2019 --- ## § 1. Stage 5 Workflow Overview ```
1. Data preparation (panel merge) ├── mortality_rate_panel_v02.1 (분자, outcome_group 10 + 3 ASR baseline) ├── kosis_business_survey (분모 share, baseline 1995-1999) ├── comtrade_korea_china + comtrade_adh_china (trade shock + IV) ├── hs_isic4_concordance + ksic_version concordance (HS6 ↔ KSIC4) ├── kosis_family_mediators (mediator) ├── medical infrastructure controls (HIRA + KOSIS health indicators) └── 외국인등록 + macro controls (ECOS) + housing + welfare 등 2. Bartik IV construction ├── Industry shares (시군구 × KSIC4 × 1995-1999) ├── Trade shock (KR-CN HS6 → KSIC4 aggregation) └── IV (8 OHIE ← CN HS6 → KSIC4 aggregation) 3. First-stage regression + diagnostics ├── First-stage 2SLS (Δ5_trade_c,t ~ IV_c,t + X) ├── Olea-Pflueger 2013 effective F (`weakivtest`) ├── Rotemberg HHI (GPSS 2020 path) — 산업 집중도 ├── Share balance — baseline shares vs sigungu characteristics ├── Pre-trend — 1995-1999 outcome trend vs share ├── AKM placebo — random industry shock └── Permutation — random sigungu IV 4. Main 2SLS regression (4 main + 1 robustness + 2 placebo) ├── Suicide (component, H1.1, sign +) ├── Drug overdose (component, H1.2, uncertain) ├── Psych disorder (component, H1.2, uncertain) ├── Alcohol liver (component, H1.3, sign-uncertain) ├── Despair_total (robustness, original PAP main) ├── Cardiovascular (placebo, H1.4) └── Cancer (placebo, H1.4) 5. 5-layer SE (모든 회귀에 적용) ├── HC1 robust (default) ├── WCB-sigungu (229 cluster) — boottest ├── WCB-sido (16 cluster, secondary) — boottest ├── AKM SE (main inference) — reg_ss (BHJ 2022) ├── Conley spatial — acreg └── AR + tF (weak IV robust) — weakiv 6. Mediation analysis (DGHP 2017 + DFH 2020) ├── Mediator: 이혼율, 결혼율, 합계출산율, 한부모, (옵션 동거) ├── Estimation: 3 separate 2SLS (T→M, T→Y, Y→M|T) ├── Indirect = β_TM × γ_MY|T ├── Direct = β_TY − Indirect ├── Mediation share = Indirect / Total └── Sensitivity: ρ_TY robustness + IKY 2010 bound interpretation 7. Romano-Wolf step-down (multiple testing) ├── 4 main outcome (suicide/drug/psych/liver) × 5 mediator + 5 robustness └── Family-wise error rate 통제 (Stata `rwolf`) 8. Heterogeneity ├── Manufacturing intensity quartile (Q1-Q4) ├── Sex separate (남/여) └── 65+ sub-analysis (한국 OECD 1위 elderly suicide) 9. Robustness (10 항목) ├── Concordance (KSIC 4-digit main / IO 380 / ISIC4 bridge) ├── Baseline period (1995-1999 / 1990-1994 / 1998-2002) ├── Sample period (2000-2024 / 2002-2024 excluding pre-IMF) ├── Outcome (ln_asr+1 main / Poisson IV) ├── Standardization (KR2010 main / WHO2000 / Eurostat 2013) ├── 80+ aggregate vs 65+ subgroup ├── 외국인 빼기 (v02 sensitivity vs v02.1 main) ├── Stack count (5 stack Δ5+Δ4 main / 4 stack Δ5 only) ├── Medical infrastructure controls (naive vs controlled H1.3) └── Mediation framework (DGHP 2017 main vs IKY 2010 sensitivity) 10. Output formatting ├── Table 1 — Main result (suicide + drug + psych + liver + despair_total + cardio + cancer) ├── Table 2 — Mediation decomposition (5 mediator 별 indirect / direct / total) ├── Table 3 — Heterogeneity (manufacturing quartile × sex × 65+) ├── Table 4 — Robustness summary └── Figure 1-3 — ASR 시계열, first-stage scatter, mediation flowchart
``` --- ## § 2. Data Preparation Spec ### 2.1 Panel merge ```stata
* Stata pseudocode
use "panel/mortality_rate_panel_v02_1.dta", clear
* h_code, year, sex_code, outcome_group, deaths, population, asr_kr2010_per_100k, ln_asr_kr2010,... merge m:1 h_code year using "panel/trade_panel_long.dta"
* h_code, year, trade_shock, IV (Bartik 8 OHIE) merge m:1 h_code using "panel/baseline_industry_shares.dta"
* h_code, ksic4_share_1995, ksic4_share_1996,..., ksic4_share_1999 merge m:1 h_code year using "panel/family_mediators.dta"
* h_code, year, divorce_rate, marriage_rate, fertility_rate, single_parent_rate merge m:1 h_code year using "panel/medical_infrastructure.dta"
* h_code, year, n_general_hospital, n_clinic, vaccination_proxy,... merge m:1 h_code year using "panel/foreign_residents.dta"
* h_code, year, foreign_pop, foreign_share * 회귀용 5-year stacked first-difference
gen year_5yr = floor((year - 2000) / 5) * 5 + 2000
collapse (mean)..., by(h_code year_5yr sex_code outcome_group) * Δ5 outcome
xtset h_code year_5yr
gen d5_ln_asr = ln_asr_kr2010 - L.ln_asr_kr2010
gen d5_trade = trade_shock - L.trade_shock
gen d5_IV = IV - L.IV
``` ### 2.2 Stack 정의 (PAP § 4.2 commit) 5 stack: t = 2000, 2005, 2010, 2015, 2020 (4 Δ5 + 1 Δ4)
- Δ5 stacks: 2000-2005, 2005-2010, 2010-2015, 2015-2020 (4 stack)
- Δ4 stack: 2020-2024 (1 stack, partial)
- Sensitivity: 4 stack Δ5 only (2020-2024 제외) ### 2.3 Sample size - Main: 5 stack × 229 sigungu × 2 sex = **2,290 obs** (sex-stratified)
- 또는 sex-pooled: 5 × 229 = **1,145 obs** --- ## § 3. Bartik IV Construction ### 3.1 Industry shares (시군구 × KSIC4 × baseline 1995-1999) ```stata
use "kosis_business_survey/microdata_1995_1999.dta", clear
* 시도, 시군구, KSIC4, 종사자수
egen total_emp_h = total(employment), by(h_code)
egen emp_h_k = total(employment), by(h_code KSIC4)
gen share_h_k = emp_h_k / total_emp_h
collapse (mean) share_h_k, by(h_code KSIC4)
* baseline shares: ~229 sigungu × ~200 KSIC4 = ~45,800 cells
save "panel/baseline_industry_shares.dta", replace
``` ### 3.2 Trade shock (KR ← CN HS6 → KSIC4) ```stata
use "comtrade/korea_china_bilateral_HS6.dta", clear
* year, hs6, value_usd (KR import from CN)
merge m:m hs6 using "concordance/hs6_to_ksic4.dta" // Stage 4B 산출
collapse (sum) value_usd, by(year KSIC4)
gen d5_value = value_usd - L5.value_usd // 5-year change
``` ### 3.3 Bartik shock (시군구 × year) ```stata
* Δ5_trade_c,t = Σ_k (share_h_k) × (Δ5_value_k / total_emp_k_baseline)
joinby KSIC4 using "panel/baseline_industry_shares.dta"
gen contribution = share_h_k * d5_value / total_emp_k_baseline
collapse (sum) contribution, by(h_code year)
rename contribution trade_shock
save "panel/trade_panel.dta", replace
``` ### 3.4 IV (8 OHIE ← CN HS6 → KSIC4) ```stata
use "comtrade/eight_ctry_from_china_HS6.dta", clear
* year, country, hs6, value_usd
collapse (sum) value_usd, by(year hs6) // 8 OHIE 합산
* 동일 logic 으로 IV_c,t 계산
``` --- ## § 4. First-stage Regression + 6 Diagnostics ### 4.1 First-stage spec ```stata
reg d5_trade d5_IV X i.year_5yr i.sido, robust
* X: baseline manufacturing share, education, age structure, urbanization, 외국인 비율
* sido FE: 16 광역시도
* year FE: 5 stack
``` ### 4.2 OP 2013 effective F (PAP § 4.4 #1) ```stata
ssc install weakivtest
weakivtest, level(0.05) tau(0.10)
* 5% TSLS bias threshold = 23.1 (single endogenous + single IV)
``` **합격 기준**: F > 23.1 → strong IV. F < 23.1 → weak IV → AR+tF inference. ### 4.3 Rotemberg HHI (PAP § 4.4 #2) ```stata
ssc install bartik_weight // GPSS 2020 path
bartik_weight d5_trade d5_IV (share_h_k = ksic4_emp), z(d5_value_k)...
* HHI = Σ α_k^2 ≤ 0.20 (pass)
``` ### 4.4 Share balance (PAP § 4.4 #3) ```stata
* baseline industry shares vs sigungu characteristics
foreach k of varlist top_50_ksic4 { reg `k' baseline_manuf_share education_share age65_share urbanization med_infra test baseline_manuf_share education_share age65_share urbanization med_infra * H0: 모든 covariate uncorrelated (joint test)
}
``` ### 4.5 Pre-trend (PAP § 4.4 #4) ```stata
* 1995-1999 outcome (mortality) trend vs share
reg d_outcome_pre baseline_industry_shares, robust
* H0: pre-trend uncorrelated
``` ### 4.6 AKM placebo (PAP § 4.4 #5) ```stata
* random industry shock 1000 회 simulation → β 분포
* 실제 β 가 분포 외 → strong identification
``` ### 4.7 Permutation test (PAP § 4.4 #6) ```stata
* random sigungu IV 1000 회 → β 분포
* p-value (실제 β > distribution percentile)
``` --- ## § 5. Main 2SLS Regression (4 main + 1 robustness + 2 placebo) ### 5.1 Main spec ```stata
foreach outcome in suicide_102 drug_101 psych_057 liver_081 despair_total cardiovascular cancer { use "panel/main_panel.dta", clear keep if outcome_group == "`outcome'" ivregress 2sls d5_ln_asr (d5_trade = d5_IV) X i.year_5yr i.sido, robust estimates store main_`outcome' * 5-layer SE 적용 (§ 6 참조)
}
``` ### 5.2 Output coefficient + 5-layer SE 각 outcome 별 main coefficient + 5-layer CI 보고:
```
suicide_102: β = 0.45, SE_HC1 = 0.12, p < 0.001 WCB-sigungu CI: [0.18, 0.72] AKM SE = 0.15, p = 0.003 Conley CI: [0.20, 0.70] AR+tF CI: [0.15, 0.75]
``` --- ## § 6. 5-Layer SE Spec ### 6.1 HC1 robust (default) ```stata
ivregress 2sls..., robust
``` ### 6.2 WCB-sigungu (229 cluster) ```stata
ssc install boottest
boottest d5_trade, cluster(h_code) reps(9999) seed(20260503)
* 229 cluster → asymptotic valid (CGM 2008)
``` ### 6.3 WCB-sido (16 cluster, secondary) ```stata
boottest d5_trade, cluster(sido) reps(9999) seed(20260503)
* 16 cluster < 30 → small-cluster bias (1.3-1.5x over-rejection)
* WCB 가 small-cluster bias 부분 fix
``` ### 6.4 AKM SE (main inference, BHJ 2022) ```stata
* BHJ ssaggregate R package via Stata interop
* 또는 reg_ss (Borusyak github)
ssc install reg_ss // 또는 github 직접
reg_ss d5_trade..., shift(d5_value_k)
* J = ~200 KSIC4 → BHJ 2022 small-J inference 적용
``` ### 6.5 Conley spatial SE ```stata
ssc install acreg
acreg d5_ln_asr (d5_trade = d5_IV) X, latitude(lat) longitude(lon) dist(100)...
* 100km radius spatial correlation
``` ### 6.6 AR + tF (weak IV robust) ```stata
ssc install weakiv
weakiv ivregress 2sls d5_ln_asr (d5_trade = d5_IV) X
* AR test → robust to weak IV
``` --- ## § 7. Mediation Analysis (DGHP 2017 + DFH 2020) ### 7.1 Spec (PAP § 5.2) ```stata
ssc install ivmediate // DFH 2020 Stata Journal
foreach M in divorce_rate marriage_rate fertility_rate single_parent_rate { foreach Y in suicide_102 drug_101 psych_057 liver_081 { ivmediate `Y' (`M' = `M' L1.`M') (d5_trade = d5_IV) X, /// cluster(h_code) reps(1000) * indirect = β_TM × γ_MY|T * direct = β_TY - indirect * total = β_TY * mediation share = indirect / total }
}
``` ### 7.2 ρ_TY sensitivity (PAP § 5.2 honest framing) ```stata
* DFH framework 의 core assumption: ρ_TY = 0
* sensitivity: ρ_TY ∈ [-0.3, +0.3] 변동 시 indirect effect 변동 폭
``` ### 7.3 IKY 2010 bound interpretation (robustness) ```stata
ssc install medsem
* IKY framework 적용 (mediator endogeneity 가정)
* sequential ignorability bound 보고
``` --- ## § 8. Romano-Wolf Step-down ### 8.1 Spec ```stata
ssc install rwolf
rwolf suicide_102 drug_101 psych_057 liver_081 despair_total /// cardiovascular cancer respiratory external_other, /// indep(d5_trade) reps(1000) seed(20260503)
* family-wise error rate 통제 (Holm-Bonferroni 방식)
* p-value 조정 후 결과 보고
``` --- ## § 9. Heterogeneity ### 9.1 Manufacturing intensity quartile ```stata
* baseline manufacturing share quartile
xtile mfg_q = baseline_manuf_share, n(4)
foreach q in 1 2 3 4 { ivregress 2sls d5_ln_asr (d5_trade = d5_IV) X if mfg_q == `q' estimates store mfg_q`q'
}
``` ### 9.2 Sex separate ```stata
foreach s in 1 2 { // 1=male, 2=female ivregress 2sls d5_ln_asr (d5_trade = d5_IV) X if sex_code == `s' estimates store sex_`s'
}
``` ### 9.3 65+ sub-analysis ```stata
* 65+ aggregate ASR (panel v02.1 의 age band 14-17 만)
* age band 14: 60-64, 15: 65-69, 16: 70-74, 17: 75-79, 18_19_20: 80+
* 65+ = age band 15 + 16 + 17 + 18_19_20 (sum)
ivregress 2sls d5_ln_asr_65plus (d5_trade = d5_IV) X
``` --- ## § 10. Robustness (10 항목) (§ 1.9 list 참조 — 10 항목 별 spec) 각 항목 별:
- Main spec 의 변경 부분만 명시
- Coefficient + p-value 비교
- Main 결과와 일관성 (same sign + magnitude ±50% 이내) 확인 --- ## § 11. Output Formatting ### 11.1 Table 1 — Main Result | Outcome | β (Suicide H1.1) | SE_AKM | OP F | n |
|---------|-----------------:|-------:|-----:|---|
| Suicide | +0.45 | 0.15 | 25.3 | 2,290 |
| Drug | +0.18 | 0.10 | 25.3 | 2,290 |
| Psych | +0.12 | 0.08 | 25.3 | 2,290 |
| Liver | -0.32 | 0.18 | 25.3 | 2,290 |
| Despair_total | +0.15 | 0.12 | 25.3 | 2,290 |
| Cardiovascular | +0.02 | 0.08 | 25.3 | 2,290 |
| Cancer | -0.01 | 0.07 | 25.3 | 2,290 | (가상 결과 — 실제 Stage 5 회귀 후 채움) ### 11.2 Table 2 — Mediation Decomposition (5 mediator × 4 main outcome = 20 cells, indirect / direct / share) ### 11.3 Figure 1-3 - Figure 1: ASR 시계열 (1997-2023, 4 component + total)
- Figure 2: First-stage scatter (Δ5_IV vs Δ5_trade)
- Figure 3: Mediation flowchart (T → M → Y, β + share) --- ## § 12. Stata 환경 + Package 설치 (Stage 5 시작 직전) ### 12.1 가천대 Stata license 확인 ```bash
# 현재 사용 가능 license 확인
stata -e
. about
* edition: SE / MP / IC?
``` ### 12.2 7 package 설치 ```stata
ssc install boottest // CGM 2008 + Roodman et al 2019
ssc install weakivtest // Pflueger-Wang 2015
ssc install ivmediate // DFH 2020
ssc install rwolf // Romano-Wolf 2005
* reg_ss: github 직접 설치
* net install reg_ss, from("https://raw.githubusercontent.com/borusyak/shift-share/master/")
ssc install acreg // Conley 1999
ssc install weakiv // AR + tF inference
ssc install bartik_weight // GPSS 2020 Rotemberg HHI
``` ### 12.3 R / Python alternative (Stata license 제약 시) - R: `ivreg`, `lfe`, `boot.kbet`, `mediation`, `ssaggregate` (BHJ 2022 R package, 사용자 보유)
- Python: `linearmodels.iv`, `econml.iv`, `statsmodels` → Stage 5 시작 직전 환경 verify + alternative 결정. --- ## § 13. Stage 5 Timeline (예상) | 작업 | 시간 |
|---|---|
| § 12 환경 verify + package 설치 | 1-2 시간 |
| § 2 Data preparation | 2-3 일 |
| § 3 Bartik IV construction | 1-2 일 |
| § 4 First-stage + 6 diagnostics | 2-3 일 |
| § 5 Main 2SLS (7 outcome) | 2-3 일 |
| § 6 5-layer SE | 2-3 일 |
| § 7 Mediation (5 mediator × 4 outcome) | 3-4 일 |
| § 8 Romano-Wolf | 1 일 |
| § 9 Heterogeneity | 2 일 |
| § 10 Robustness (10 항목) | 1 주 |
| § 11 Output formatting | 1 주 |
| **Total** | **~3-4 주** (2026-06 중반) | --- ## § 14. Stage 5 진입 직전 prerequisite - [x] Panel v02.1 main analysis ready (mortality_rate_panel_v02_1.parquet)
- Stage 4B HS-KSIC concordance 완료 (통계청 응답 대기)
- Mediator rate 분모 수집 (KOSIS 다운로드 진행 중)
- Stata 환경 verify + 7 package 설치
- PAP v3.4 final commit (현재 상태) → 모든 prerequisite 완료 후 Stage 5 진입. --- ## § 15. Reference Verified (PAP v3.3 § 13) - ADH 2013 AER (Bartik IV 표준)
- Pierce-Schott 2020 AER:I (NTR gap DID, 5-year stacked spec)
- GPSS 2020 AER 110(8): 2586-2624 (share exogeneity)
- DGHP 2017 NBER WP 23209 (mediation framework)
- DFH 2020 Stata Journal 20(3): 613-626 (`ivmediate`)
- OP 2013 J Bus Econ Stat (effective F)
- BHJ 2022 RES (small-J inference)
- AKM 2019 QJE (shift-share SE)
- CGM 2008 RES (cluster bootstrap)
- Roodman et al 2019 Stata J (`boottest`)
- Romano-Wolf 2005 Econometrica (step-down)
- Conley 1999 J Econom (spatial SE)
- IKY 2010 Stat Sci (sensitivity bound) --- 작성: 정재헌 + 2026-05-03 Stage 5 spec plan v01 commit before Stage 4B + Stage 5 진입. 다음 update: Stage 4B concordance 완료 + 사용자 PC Stata 환경 verify 후 v02 update.
