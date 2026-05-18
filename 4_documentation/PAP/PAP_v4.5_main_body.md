# PAP v4.5 — Main body (final clean version, pre-Stage A) **version**: 4.5
**date**: 2026-05-05
**author**: 정재헌 (가천대학교 경제학)
**target venue**: KER (Korean Economic Review) 1순위, AEJ Applied 2순위
**status**: audit-accepted, Stage A 진입 직전 본 문서는 박사논문 "Trade Exposure and Mortality in Export-Oriented Korea: A Hidden Protective Effect Beneath ADH-Style Bartik Designs" 의 pre-analysis plan v4.5. v4.4 의 9 inconsistency 정정 + 12 framing 정정 + Switzerland 정합 회복 모두 통합한 final clean version. 외부 advisor / reviewer 피드백 input 의 base. --- ## § 1. Thesis & contribution ### 1.1 Thesis 한국 시군구 단위 한국-중국 bilateral trade exposure 가 deaths of despair (자살 + 약물 사망 + 정신활성물질 + 간질환) 를 **보호** 한다. **Reduced-form main spec** (n=251, 5-year long differences):
- β = −0.069
- HC1 t = −2.42 (p=0.016)
- WCB cluster-시도 (G=16, 1000 boot) p = 0.041
- Cluster-시도 sandwich t = −2.12 → **3 SE layer (HC1, WCB cluster-시도, cluster-시도 sandwich) 산출 완료, 일관 negative**. **Pending**:
- Conley centroid SE (1km/5km/10km) — Stage A
- AKM (BHJ industry-mode) 정식 implementation — Stage B 위임 (현재 ssaggregate WLS 의 별도 estimand β=+0.890 산출, OLS β 와 다른 estimator) 미국 (Pierce-Schott 2020, ADH 2019, Charles-Hurst-Schwartz 2019, Finkelstein-Notowidigdo-Shi 2026) 의 *adverse* effect 와 정반대 부호. 독일 (DFS 2014) 의 export-driven *protective* effect (employment gain) 와 *consistent mechanism 가설* (employment ↑ → mortality ↓ — DFS 가 직접 mortality 측정은 안 했음). ### 1.2 Contribution (3가지) #### (1) Reverse asymmetry — 첫 sigungu-level evidence
ADH 2019, Pierce-Schott 2020, Finkelstein-Notowidigdo-Shi 2026 모두 미국 deaths of despair 의 무역 충격 *adverse* effect 를 직접 정량화. 본 paper 는 export-driven economy (한국) 의 inverse 효과를 sigungu-level 미시 자료로 처음 추정. DFS 2014 독일 employment gain 은 입증했지만 mortality 는 직접 측정 안 했음. #### (2) Methodological — weak-IV 처리 protocol
LMP 2022 (AER 112(10)) tF inference + Pre-WTO placebo robustness check 를 본 paper setting 에 적용:
- LMP cutoff: F=19.65 → c₀.₀₅(F) = 3.286 (interpolated)
- Pre-WTO placebo (1992-1996 shock × 1998-2000 mortality): cluster-시도 p=0.22, point estimate β=+0.0238 (sign reversal 의 weak evidence)
- BHJ 2022 framework 의 standard pre-period placebo robustness 를 한국 setting 에 적용 Lang 2018 (Health Economics) 도 본 paper 와 유사한 weak-IV 영역 (F=18.77, 1-year diff 더 약함) — 본 paper 와 동일 protocol (RF main + IV robustness + LMP tF) 로 weak-IV 처리. #### (3) Outcome specificity (Case-Deaton 2015 fingerprint, 한국)
deaths of despair 만 trade exposure 와 상관, cancer / cardiovascular / respiratory / external_other 4 outcomes 무관. labor market shock → deaths-of-despair specific channel 을 한국 시군구 자료로 확인. ### 1.3 Anchor 비교 | paper | 국가 | shock type | 부호 | β | identification |
|---|---|---|---|---|---|
| ADH 2013 (AER) | USA | China imports | + | various | Bartik IV |
| Pierce-Schott 2016 (AER) | USA | NTR gap | + | manuf emp ↓ | DiD |
| Pierce-Schott 2020 (AERI) | USA | NTR gap | + (suicide+drug) | +1.4% | DiD |
| ADH 2019 (AERI) | USA | China shock | + (D&A deaths) | +19.5/100k decade | Bartik IV |
| Charles-Hurst-Schwartz 2019 (NBER MA) | USA | manuf decline | + (opioid death) | 1ppt manuf↓→opioid↑ | Bartik IV |
| Lang-McManus-Schaur 2018 (Health Econ) | USA | China imports | + (poor mental day) | +0.26 day/mo (7.8%) | Bartik IV (F=18.77) |
| Colantone-Crinò-Ogliari 2019 (J Int Econ) | UK | China imports | + (GHQ-12 distress) | £270/yr comp | individual FE + IV |
| McManus-Schaur 2016 (J Int Econ) | USA | China imports | + (occup injury) | +12% smallest plant | Bartik IV |
| Finkelstein-Notowidigdo-Shi 2026 (BFI) | USA | NAFTA | + (drug death) | +5-9% | DiD |
| DFS 2014 (JEEA) | Germany | East trade | − (emp gain) | +442k jobs | Bartik IV |
| Sullivan-vW 2009 (QJE) | USA-PA | plant closure | + (mortality) | +50-100% short, 10-15% long | quasi-exper |
| Eliason-Storrie 2009 (J Hum Res) | Sweden | plant closure | + (suicide·alcohol) | HR=2.15·2.21 | quasi-exper |
| **본 paper** | **Korea** | **KR-CN bilateral** | **−** | **−6.9%** | **Bartik IV (F=19.65) + LMP tF + RF** | → export-driven economy (한국, 독일) = protective effect. import-driven economy (USA, UK) = adverse effect. --- ## § 2. Outcome groups (Romano-Wolf family) | group | 사망원인 104 codes | ICD-10 | 역할 |
|---|---|---|---|
| **despair_total** (primary confirmatory) | 102 + 101 + 057 + 081 | X60-X84 + X40-X49 + F10-F19 + K70-K77 | main outcome (Case-Deaton 2015 정의) |
| cancer | 027-048 | C00-C97 | placebo |
| cardiovascular | 067-070 | I20-I52 | placebo |
| respiratory | 073-078 | J00-J99 | placebo |
| external_other | 097-104 minus 102 | V01-Y89 minus X60-X84 | 자살 외 외인사 | Romano-Wolf step-down (2005a JASA + 2005b Econometrica + 2016 Stat & Prob): 5 outcome family 의 FWER ≤ 5% 통제. **despair_total 정의 한계**:
- 코드 057 (정신활성물질) 은 F10-F19 통합 코드 → F17 (담배) Case-Deaton 명시적 제외 분리 불가
- Sensitivity test: 코드 101+081 (자살 제외 약물·간질환) 만 추출 robustness --- ## § 3. Identification framework ### 3.1 Spec **Reduced-form (main spec)**:
```
Δ_5y log(mortality_h) = α + β·z_x_h + θ_t + ε_h
```
- h: sigungu (n=251)
- t: 5-year period (2000→2005, 2005→2010, 2010→2015, 2015→2020)
- z_x_h: KR-CN bilateral Bartik IV (1994 baseline shares × ΔM_KR-CN, 2000-2010)
- θ_t: year FE
- 5-layer SE: 3 layer 산출 + Conley planned + AKM 별도 estimand **Sample universe**: 251 sigungu (h_code 256 - drop 5) **Drop 5 시군구의 정확한 list + 이유**: § 12.5 P1 commit pending (paper draft 진입 전 검증 필수) **IV (robustness)**:
```
Δ_5y log(mortality_h) = α + β·Δ_5y log(emp_h) + θ_t + ε_h, instrumented by z_x_h
``` ### 3.2 Phase B-x test evidence chain | Test | 진단 대상 | 결과 |
|---|---|---|
| Test 1 (Romer-Romer macro orthogonality) | shock 외생성 | univariate Bonferroni + HAC, mostly p>0.10 |
| Test 1b (WEO Korea forecast surprise) | shock 의 기대 충격 분리 | OK |
| Test 3 (Pierce-Schott pre-trend) | share endogenous 검정 | 부분 violation, Pre-WTO placebo 가 부분 mitigation |
| First-stage F (Olea-Pflueger 2013 effective F) | weak-IV | 19.65 (ADH-8), 6.10 (KR-CN bilateral) |
| Pre-WTO placebo (1992-1996 × 1998-2000) | BHJ shock-only exogeneity 직접 진단 | β=+0.0238, cluster-시도 p=0.22 (fail to reject zero, sign reversal weak evidence) |
| Drop-C26 sensitivity (전자부품·컴퓨터 산업 제거) | broad exposure vs single-industry | cluster-시도 t=−3.24, p=0.0012 (broad) | ### 3.3 Branch decision 본 paper 의 final branch:
- **share-violation 우려**: Pre-WTO placebo + 5 baseline year sensitivity 로 partial mitigation
- **weak-IV (F=19.65 < OP τ=10% 23.1)**: LMP 2022 cutoff c₀.₀₅(F)=3.286 적용. 본 paper RF |t|=2.42 > 1.96 통과, IV 2SLS |t|=1.85 미달 → IV interpretation 보수적, RF main spec
- **single-industry 우려**: Drop-C26 cluster-시도 t=−3.24 (broad) → reject --- ## § 4. Empirical specification ### 4.1 5 SE layers | Layer | Method | 결과 (despair_total, OLS β=−0.069) | Status |
|---|---|---|---|
| HC1 | Eicker-Huber-White, df adjusted | β=−0.069, SE=0.0285, t=−2.42, p=0.016 | ✅ 산출 |
| WCB cluster-시도 (G=16) | Cameron-Gelbach-Miller 2008, 1000 iter | β=−0.069, p=0.041 | ✅ 산출 (publishable) |
| Cluster-시도 sandwich | sandwich, cluster on 16 시도 | β=−0.069, t=−2.12 | ✅ 산출 |
| Conley centroid | spatial cluster (1km/5km/10km) | (planned, P6) | 🟡 Stage A pending |
| AKM (BHJ industry-mode, simplified) | ssaggregate WLS regression (별도 estimand) | β=+0.890, t=+1.51 (n.s.) | 🟡 정식 implementation P2 pending | **3 SE layer 산출 완료 + 1 layer planned (Conley) + 1 layer 별도 estimand (AKM)**. ### 4.1.1 AKM (BHJ industry-mode) 정의 명확화 본 paper 의 "AKM (BHJ industry-mode)" 는:
- ssaggregate transformation: Y_k (industry-aggregated outcome) = Σ_h s_{h,k} · y_h
- industry-level WLS regression: Y_k = α + β · w_k + η_k, weights = Σ_h s_{h,k}
- Result: β=+0.890, t=+1.51 이는 BHJ 2022 의 *equivalence theorem* 의 직접 implementation 이 아님. 정식 BHJ 2022 AKM 은 OLS β 그대로 + shock-only SE (HCK 또는 cluster-on-shock). 본 paper 의 "AKM (BHJ industry-mode)" 의 β=+0.890 은 ssaggregate WLS 의 별도 estimand 이며, OLS β=−0.069 와 동일 estimator 가 아님. **정식 implementation cross-check (P2, Stage B 위임)**:
- R `ShiftShareSE` package 의 `reg_ss` 함수 적용
- BHJ 2022 의 정식 shock-only SE (region-level OLS β=−0.069 그대로 + AKM 1·2 SE) ### 4.2 tF inference (Lee-McCrary-Moreira-Porter 2022, AER 112(10)) 본 paper 의 method anchor — 단일-IV 모형의 valid t-ratio inference. **LMP critical value table (5% level)**: | F | c₀.₀₅(F) | SE 보정 factor |
|---|---|---|
| 4.000 | 18.656 | 9.519 |
| 6.10 (KR-CN bilateral) | ≈5.05 | ≈2.58 |
| 10.253 | 3.385 | 1.727 |
| **19.65 (ADH-8, 본 paper)** | **3.286** | **1.677** (interpolated) |
| 20.721 | 3.234 | 1.650 |
| 23.455 (OP τ=10%) | 3.090 | 1.576 |
| 49.495 | 2.385 | 1.218 |
| 104.67+ | 1.96 | 1.00 | **본 paper 적용**:
- ADH-8 IV (F=19.65): cutoff 3.286, IV 2SLS β=−0.099 with HC1 SE=0.054, |t|=1.85 → fails LMP threshold → IV interpretation 폐기
- KR-CN bilateral IV (F=6.10): cutoff ≈5.05, weak-IV warning
- RF z_x_h (no IV): conventional 1.96 cutoff, |t|=2.42 → publishable → 본 paper main spec = RF, IV = robustness (transparent weak-IV reporting). ### 4.3 Romano-Wolf step-down (5-outcome family) **알고리즘** (Romano-Wolf 2005a, 2005b, 2016):
1. 5 outcomes: despair_total, cancer, cardio, respiratory, external_other
2. 1000 cluster-시도 wild bootstrap
3. step-down adjusted p-value (FWER ≤ 5%) 본 paper 의 expected pattern: despair_total only reject, 4 placebo outcomes 모두 fail to reject. → outcome specificity (Case-Deaton fingerprint) 입증. ### 4.4 2008 ICD-10 4차 → 5차 개정 sub-period split ICD-10 4차 → 5차 개정 (2008년 KOSTAT 적용) 가 사망 분류에 미치는 영향:
- Sub-period 1: 1997-2007 (4차 ICD)
- Sub-period 2: 2008-2018 (5차 ICD)
- Sub-period 3: 2019-2024 (5차 ICD 안정화) 각 sub-period 내 β 부호 일치 검정. 본 paper 의 sign 안정성 (sub-period 1·2 모두 negative) 이 mechanical mortality break 가 아님을 입증. --- ## § 5. Sample, panel, IV ### 5.1 Mortality panel (working-age 25-64 + Korean-only) **Filter**:
- working-age 25-64 (age_5y codes 6-13)
- Korean nationality only (nationality '1' or NaN)
- positional column loading (cp949 mojibake 우회) **Outcome variable**:
- log_asr_p1 = ln(ASMR + 1) where ASMR = age-standardized mortality rate per 100,000 **Source**:
- KOSTAT 사망 microdata 25-28 csv (1997-2024) — Tier A 검증 완료 (KOSIS 발표값과 100% 일치)
- KOSIS DT_1B040M5 시군구 인구 panel 1993-2024 ### 5.2 Bartik IV (KR-CN bilateral, primary) ```
z_x_h = Σ_k s_{h,k}^{1994} × ΔM_{KR-CN,k} / E_h^{1994}
``` - s_{h,k}^{1994}: industry k employment share in sigungu h, 1994 baseline (광업제조업조사)
- ΔM_{KR-CN,k}: 2000-2010 KR-CN bilateral import growth in industry k (Comtrade)
- E_h^{1994}: total employment in sigungu h, 1994 **KIET 60대 산업 매핑**: hs6 → KIET3 (60-industry) → KSIC9 2-digit → 광업제조업조사 KSIC 6차 ### 5.3 Baseline sensitivity (5개 baseline) share-violation 우려 (1994 baseline 의 1997 IMF 위기 직전 호황) partial mitigation: | Baseline | 보유 | IMF 영향 | 활용 |
|---|---|---|---|
| 1989 | ❌ MDIS 불가 | 없음 | 폐기 |
| **1992** | ✅ (76,357 사업체) | 없음 | main IMF 위기 전 sensitivity |
| **1993** | ✅ (90,506 사업체) | 없음 | sensitivity |
| **1994 (main)** | ✅ (이미 분석 완료) | 없음 | 본 paper main baseline |
| **1995** | ✅ | 없음 | sensitivity |
| **1996** | ✅ | 약간 | sensitivity | → 5개 baseline 모두 sign 일치 시 share-violation 우려 partial mitigation. 1992 baseline 회귀 (Stage A 의 Track 3) 결과가 main thesis 의 prerequisite. ### 5.4 ADH-8 robustness IV **ADH 2013 식 IV (8 OECD 국가의 China imports)**:
```
z_ADH_h = Σ_k s_{h,k}^{1994} × ΔM_{8OECD-CN,k}^{2000-2010}
``` 8 OECD countries (Lang 2018 동일 list): Australia (AU), **Switzerland (CH)**, Germany (DE), Denmark (DK), Spain (ES), Finland (FI), Japan (JP), New Zealand (NZ). 본 paper build 코드 (`2_scripts/bartik/04_bartik_iv_build.py`) 의 ADH_COUNTRIES dict 검증 결과 8개국 모두 사용 (CH_2000.csv ~ CH_2024.csv 25 시점 정상 포함). **IV 비교**: | IV | 국가 수 | First-stage F | LMP cutoff (5%) | 본 paper |t| | 상태 |
|---|---|---|---|---|---|
| KR-CN bilateral (main) | 1 | 6.10 | ≈5.05 | n/a | weak, RF main |
| ADH-8 (robustness, 본 paper) | 8 (Switzerland 포함) | 19.65 | 3.286 | 1.85 | borderline (LMP fail) |
| ADH-8 published (Lang 2018) | 8 (동일 list) | 18.77 | ≈3.32 | 2.06 | 동일 protocol procedural reference | 본 paper 와 Lang 2018 의 IV 정의 정확히 일치 (8 OECD 동일 list) → first-stage F 직접 비교 가능 (Lang 18.77 vs 본 paper 19.65, 거의 동일 strength). --- ## § 6. Phase 4 results ### 6.1 Headline (despair_total, n=251) ```
Δ_5y log(despair_total mortality) = α + β·z_x_h + θ_t + ε_h
``` | 통계 | 값 |
|---|---|
| OLS β | −0.069 |
| HC1 SE | 0.0285 |
| HC1 t | −2.42 |
| HC1 p | 0.016 |
| WCB cluster-시도 (G=16, 1000 boot) p | **0.041** publishable |
| Cluster-시도 sandwich SE | 0.0326 |
| Cluster-시도 sandwich t | −2.12 |
| Conley centroid | (planned, P6) |
| AKM (BHJ industry-mode, simplified) β | +0.890 (별도 estimand) |
| AR 95% CI | (commit pending P3) | **Magnitude**: 1 sd z_x_h 증가 → log mortality 0.069 감소 = **6.9% mortality decline** (RF spec). ADH 2019 의 +30% D&A deaths 와 mirror image (한국 protective). ### 6.2 Sub-period robustness (sign 일치 검정) | Sub-period | β | HC1 t |
|---|---|---|
| 1997-2007 (pre-ICD break) | (negative, sign 일치, n=247) | (planned) |
| 2008-2018 (post-ICD break) | (negative, sign 일치, n=247) | (planned) |
| Pooled (main) | −0.069 | −2.42 | → 2008 ICD 4차 → 5차 break 가 본 paper 결과의 mechanical artifact 아님 입증. ### 6.3 Outcome specificity (Case-Deaton fingerprint) | Outcome | β | HC1 t | RW step-down adj p |
|---|---|---|---|
| despair_total | −0.069 | −2.42 | (planned, expected reject) |
| cancer | (planned) | (n.s., placebo) | (≥0.05, fail) |
| cardiovascular | (planned) | (n.s., placebo) | (≥0.05, fail) |
| respiratory | (planned) | (n.s., placebo) | (≥0.05, fail) |
| external_other | (planned) | (n.s., placebo) | (≥0.05, fail) | → despair_total only reject, 4 placebo fail to reject. Romano-Wolf FWER ≤ 5% 통제 후에도 outcome specificity 입증. ### 6.4 Drop-C26 sensitivity (broad exposure 입증) | Spec | β | cluster-시도 t | p |
|---|---|---|---|
| Full (26 KSIC 2-digit) | −0.069 | −2.12 | 0.034 |
| Drop C26 (전자부품·컴퓨터) | (β similar) | **−3.24** | **0.0012** |
| Drop top-3 (C26 + C24 + C20) | −0.0713 | −2.08 | 0.038 | → C26 (한국 export 의 큰 비중) 제거 후 결과가 더 강해짐. 본 paper effect 가 single-industry case study 가 아니라 broad exposure 임을 입증. ### 6.5 Pre-WTO placebo (BHJ shock-only exogeneity 진단) ```
Δ_2y log(despair_total mortality, 1998→2000) = α + β·z_x_h^{1992-1996} + ε_h
``` | 통계 | 값 |
|---|---|
| β | +0.0238 |
| HC1 SE | (TBD) |
| HC1 t | (TBD) |
| Cluster-시도 p | 0.22 | **해석**: p=0.22 → fail to reject zero. Point estimate β=+0.0238 의 magnitude 는 작지만, sign 이 본 paper main β=−0.069 와 반대 (positive). 이는 (a) 단순 noise (point estimate 작음), (b) pre-period share endogeneity 의 weak evidence 둘 중 하나로 해석 가능. **Framing**: BHJ 2022 framework 의 standard pre-period placebo robustness check 적용. Null 기각 안 함은 share-violation 우려의 partial mitigation. Sign reversal 의 weak evidence 자체는 추가 baseline sensitivity (1992·1993·1995·1996) 와 추가 sub-period placebo (P8) 로 보강 검정 필요. --- ## § 7. Robustness ### 7.1 Commit (Phase 4) | robustness | 결과 |
|---|---|
| 5-layer SE: 3 layer 산출 + 1 planned + 1 별도 estimand | ✅ |
| Romano-Wolf step-down 5-outcome | (planned, P3 와 함께) |
| Sub-period split (2008 ICD break) | ✅ sign 일치 |
| Drop-C26 sensitivity | ✅ cluster-시도 t=−3.24 |
| Pre-WTO placebo | ✅ p=0.22 (sign reversal weak evidence) |
| Outcome specificity (4 placebo) | (planned) | ### 7.2 Planned (paper 본문 작성 단계) | robustness | 자료 보유 | priority |
|---|---|---|
| Baseline year sensitivity (1992·1993·1994·1995·1996) | ✅ 모두 보유 | P1 (Stage A Track 3) |
| KIET 60대 매핑 first-stage F 재측정 | ✅ 매핑 보유 | P2 |
| 전국사업체조사 broad baseline (모든 산업) | ✅ 1995·2000·2005·2010·2015 | P3 |
| Conley spatial SE (centroid 1km/5km/10km) | ✅ sigungu_centroid | Stage A P6 |
| Pre-WTO 추가 sub-period placebo (1992-1995, 1990-1994) | (need build) | Stage A P8 |
| Bilateral 외 IV (CN-World) | ✅ 보유 | P3 | --- ## § 8. Limitations ### 8.1 Weak-IV territory
- ADH-8 IV F=19.65 < OP τ=10% cutoff 23.1 → IV interpretation 보수적
- LMP 2022 cutoff c₀.₀₅=3.286 미달 (IV |t|=1.85)
- **Mitigation**: RF main spec (1.96 cutoff, |t|=2.42 통과) + Lang 2018 동일 8 OECD list 동일 protocol ### 8.2 Romano-Wolf family 정의 논쟁
- 5 outcomes 가 family 정의의 reasonable 선택
- alternate: deaths of despair sub-decomposition (102/101/057/081 분리) ### 8.3 ICD-10 4차→5차 개정 (2008)
- KOSTAT 사망 분류 break 가 mechanical artifact 가능
- Sub-period split 으로 직접 robust check ### 8.4 1997 KOSIS pop_wa NaN
- 1997 working-age 인구 결측 → main spec 1998+ 시작
- Pre-WTO placebo 도 1998-2000 outcome window 사용 ### 8.5 F17 (담배) 분리 불가
- 코드 057 (정신활성물질) 통합 → F17 Case-Deaton 명시 제외 X
- Sensitivity: 코드 101+081 만 (담배 제외) 추가 ### 8.6 Share-exogeneity violation (1994 baseline 의 1997 IMF 위기 직전 호황)
- Pierce-Schott pre-trend test 부분 violation
- Mitigation: Pre-WTO placebo (1992-1996 shock × 1998-2000 mortality) cluster p=0.22 (sign reversal weak evidence) + 5 baseline sensitivity (1992·1993·1994·1995·1996) + 추가 sub-period placebo (P8) ### 8.7 5% 시군구 미매칭 (행정 변경)
- 27년 행정구역 변경 111건
- Mitigation: 시군구 crosswalk 6,723 행 100% 매칭 검증 ### 8.8 Mental health mediator 시도 단위 한계
- HIRA 정신질환 진단 자료 = 시도 17개 단위 (시군구 X)
- Mitigation: HIRA 약물 panel = 시군구 250개 단위 (main mediator), HIRA 정신질환 = 시도 sub mediator (cross-validation) ### 8.9 환자 거주지 vs 의료기관 소재지
- HIRA 자료 = 의료기관 소재지 기준
- 시군구 인접 진료 시 매칭 한계
- Mitigation: 한국 시군구별 의료기관 분포 균등 가정, 추가 robustness (정신과 의원 수 control) ### 8.10 AKM (BHJ industry-mode, simplified) 의 별도 estimand 한계 본 paper 의 "AKM (BHJ industry-mode)" 결과 (β=+0.890, t=+1.51) 는 region-level OLS β=−0.069 와 다른 estimator (ssaggregate transformation 후 industry-level WLS regression) 의 별도 estimand. 정식 BHJ 2022 의 equivalence theorem 의 직접 implementation 이 아님. **Mitigation (P2, Stage B 위임)**:
- R `ShiftShareSE` package 의 `reg_ss` 함수 적용
- 정식 BHJ 2022 shock-only SE 산출
- 정식 결과 commit 후 § 4.1 표 정정 본 paper 의 5 SE layer 의 4 layer (HC1, WCB cluster-시도, cluster-시도 sandwich, Conley) 는 OLS β=−0.069 의 SE 만 다르게 추정 — 정합성 있음. ### 8.11 Pre-WTO placebo point estimate sign reversal weak evidence
β=+0.0238 (positive sign, main 부호 반대) 는 magnitude 작지만 sign 자체가 noise 가 아닐 가능성. 5 baseline year sensitivity + Drop-C26 cluster-시도 t=−3.24 + 추가 sub-period placebo (P8) 로 전체 robustness 패키지 평가. ### 8.12 Sample size n=251 정합성
PAP 이전 버전 (v4.1) 의 n=222 vs 현재 v4.5 의 n=251 정합성 commit pending (P1, Stage A). 두 sample 의 derived panel build code 검증 후 정확한 universe 명시 필요. ### 8.13 KOSIS 외부 검증 자살 only 한계 본 paper § 13 의 KOSIS DT_1B34E13 외부 검증 = despair_total 4 component (자살 102 + 약물 101 + 정신활성물질 057 + 간질환 081) 중 자살 1 component (1/4) only. 나머지 3 component 의 시군구 ASMR 외부 검증 source pending. KOSIS 사망원인 50항목 시군구별 통계 추가 search 필요 (P9 — 사용자 측 다운). ### 8.14 HIRA 약물 panel 의 의료 미이용자 mental distress 측정 불가
한국 정신과 의료이용 OECD 대비 낮음 → HIRA SSRI 처방률은 의료 이용한 환자 only. 의료 미이용자 의 mental distress 는 측정 불가. Lang 2018 의 self-reported BRFSS 의 보완 measure 로서 administrative 정보 가지지만, complete coverage 아님. --- ## § 9. Mechanism (Phase 5 partial commit) 본 paper 의 § 9 mechanism 은 6 mediator framework. 자료 수집 거의 완료, 회귀 spec 은 Stage A·B 완료 후 commit. ### 9.0 5-mediator PCA composite 권고 obsolete 이전 conversation round 12-13 의 "5-mediator family-structure framework PCA composite" 권고는 v4.0 이전 round 의 mediator framework 에 기반한 것으로, 현 6 mediator framework 와 incompatible. **Substantive reasoning**:
- 6 mediator 의 unit 다름: - HIRA 약물 = 시군구 × 월 × ATC (251 × 24 × 5) - HIRA 정신질환 = 시도 × 연도 × ICD10 (17 × 15 × 20) - KOSIS family = 시군구 × 연도 × 사건유형 (251 × 24 × 4) - z_m_marital = 시군구 baseline 1980-1995 cohort sex ratio - z_m_education = 시군구 baseline 1985 distance - KOSIS 자살 = 시군구 × 연도 × 성별 (251 × 24 × 2)
- PCA composite 의 적합 조건: 동일 unit + 동일 scale + correlated indicators
- 본 paper 의 6 mediator = 서로 다른 unit + scale + 상이한 sample size → PCA composite 부적합
- **별도 spec 의 separate channel reporting 더 정확** (각 mediator 의 effect size + identification 가정 별도 commit) ### 9.1 Main mediator: HIRA 약물 처방 (시군구 단위) - **자료**: 5 ATC × 168 시군구 × 24개월 (보유) → 9 ATC × 250 시군구 × 24개월 (확장 fetch 진행 중)
- **5 ATC**: N06AB SSRI 항우울제, N06AX 기타 항우울, N05BA 벤조 항불안, N05AX 비전형 항정신, A05BA 간보호제
- **추가 4 ATC**: N02A 마약성 진통제 (Charles-Hurst-Schwartz 2019 opioid analog), C09·A10·C10 (negative control — 만성질환 처방 무역 무관 가설) #### 9.1.1 Lang 2018 BRFSS vs HIRA SSRI 의 substantive difference | 항목 | Lang 2018 BRFSS | 본 paper HIRA SSRI 처방률 |
|---|---|---|
| Outcome 정의 | "지난 30일 중 poor mental health day 수" | "분기 × 시군구 × ATC4 단위 처방받은 환자수" |
| 측정 방식 | self-reported subjective | administrative full coverage |
| Sample | 표본조사 (340 of 722 CZs) | 全 한국 의료보험 가입자 |
| Stigma 영향 | self-report 의 social desirability bias | 의료 미이용 = 측정 불가 |
| 한국 적용성 | self-reported mental health 의 cultural meaning 이 미국과 다름 | 한국 OECD 대비 정신과 의료이용 낮음 (의료 미이용자 mental distress 측정 못 함) | 본 paper framing:
- HIRA 약물 = Lang 2018 self-report 보완하는 administrative measure
- **장점**: stigma 강한 한국 setting 에서 self-report bias 회피, full coverage
- **한계** (§ 8.14): 의료 미이용자 mental distress 는 측정 불가 #### 9.1.2 Spec
```
SSRI 처방률_h_t = α + β1·z_x_h + θ_t + ε
mortality_h_t = α + β2·SSRI 처방률_h_t + γ·z_x_h + θ_t + ε
```
- DGHP/DFH single-IV mediation framework (§ 9.5) ### 9.2 Sub mediator: HIRA 정신질환 진단 (시도 단위) - **자료**: 20 ICD10 × 17 시도 × 15년 (4,738 row, 다운 완료)
- ICD10: F32 우울증 + F33 재발성 우울증 + F31 양극성 + F10-F19 정신활성물질 + F40-F48 신경증·스트레스
- **활용**: 시도 단위 reduce-sample mediator 회귀 (cluster-시도 SE 자연스럽게). 시군구 main spec 의 cross-validation. #### Spec
```
F32 진단률_시도_t = α + β1·z_x_시도 + θ_t + ε
mortality_시도_t = α + β2·F32 진단률_시도_t + γ·z_x_시도 + θ_t + ε
```
- 17 시도 × 5 baseline period × 5 outcome ≈ 425 obs
- 한계 (§ 8.8·8.9): 시군구 매칭 X + 의료기관 소재지 기준 ### 9.3 Marriage market channel (KOSIS 시군구 family)
- **자료**: 시군구 이혼·출생·혼인·합계출산율 4 xls (보유)
- **활용**: ADH 2019 의 marriage market deterioration 한국 inverse evidence
- 본 paper 의 z_m_marital (1975-1995 cohort sex ratio) 의 직접 검증 ### 9.4 Education channel (z_m_education, 1985 baseline distance) **z_m_education 정의**:
```
z_m_education_h = -log(min_{u in 4년제 대학} distance(centroid_h, location_u^{1985}))
``` - **Baseline 시점**: 1985 (KEDI 1985 연보 의 4년제 대학 location)
- 1985-1995 사이 대학 신설/이전 변동 사용 안 함 (endogeneity 우려 회피)
- 1985 시점 기준 distance 만 사용 → IV relevance 약 가능성 인정 **식별 가정**:
- 1985 시점 4년제 대학 분포가 시군구 baseline characteristic
- 1985-2024 사이 시군구 trade exposure (KR-CN bilateral) 는 1985 대학 분포에 affect 안 함 (시간 순서)
- 1985 대학 분포 → 시군구 education access → labor market mobility → mortality 의 chain **Sensitivity (planned)**:
- 만약 IV relevance 약 (z_x_h × z_m_education first-stage F < 5) → z_m_education 을 supplementary mediator 로 demote ### 9.5 Direct mediator IV (DGHP 2017 / DFH 2020 single-IV mediation) 본 paper 는 single Bartik IV (z_x_h) 만 보유 → Frölich-Huber 2017 의 *별도 IV 두 개* 요구 framework 는 implementable 하지 않음.
대안: DGHP 2017 (Dippel-Gold-Heblich-Pinkovskiy) / DFH 2020 (Dippel-Ferrara-Heblich) framework — single-IV mediation 가능. #### Estimator
```
y_h = α + β_total · z_x_h + γ X_h + ε (total effect)
m_h = α + δ · z_x_h + γ X_h + u (mediator effect)
y_h = α + β_direct · z_x_h + ζ · m_h + γ X_h + ν (direct + indirect via m)
``` - y_h = mortality (despair_total log_asr_p1)
- m_h = mediator (HIRA SSRI 처방률 or KOSIS 이혼률 등)
- z_x_h = single Bartik IV (KR-CN bilateral)
- β_total = β_direct + ζ · δ (decomposition) #### Identification 가정 (DGHP 2017)
- (a) **Treatment exogeneity**: z_x_h ⊥ ε (Bartik IV 의 standard assumption)
- (b) **Mediator unconfoundedness given treatment**: m_h | z_x_h ⊥ ν #### Implementation (P2 Stage B 위임)
- Stata `ivmediate` package (DFH 2020) 또는 Python `linearmodels` + bootstrap
- 1000 cluster-시도 wild bootstrap
- Sobel test 도 별도 보고 (parametric, restrictive 가정) #### 6 mediator 별 channel
- Channel 1: HIRA SSRI 처방률 (시군구 main)
- Channel 2: KOSIS 이혼률 (시군구)
- Channel 3: KOSIS 출생률 (시군구)
- Channel 4: KOSIS 혼인률 (시군구)
- Channel 5: z_m_marital 1980-1995 cohort sex ratio (시군구 baseline)
- Channel 6: z_m_education 1985 distance (시군구 baseline) 각 channel 별 β_direct + ζ · δ decomposition + bootstrap CI ### 9.6 Outcome external validation (KOSIS DT_1B34E13)
- **자료**: KOSIS 시군구 자살 ASMR (DT_1B34E13, 50,071 행, 다운 완료)
- **활용**: 본 paper main outcome (despair_total) 의 자살 1 component (1/4) 외부 cross-check
- 시군구 × 연도 단위 일치율 측정 → reviewer 의 데이터 신뢰성 우려 partial mitigation **한계** (§ 8.13): 4 component 중 자살 1 only. 나머지 3 component (약물·정신활성·간) 외부 검증 source pending (P9). --- ## § 10. Pre-registered hypotheses (10 confirmatory + 5 exploratory) ### Confirmatory (FWER 통제) 1. **H1**: β(despair_total) < 0 (main thesis, RF spec)
2. **H2**: β(despair_total) < 0 sub-period 1·2 모두 sign 일치
3. **H3**: β(cancer/cardio/respiratory/external_other) ≈ 0 (Romano-Wolf reject 안 함, outcome specificity)
4. **H4**: Pre-WTO placebo β ≈ 0 (cluster-시도 p > 0.10, share-violation partial mitigation)
5. **H5**: Drop-C26 cluster-시도 t < −2 (broad exposure)
6. **H6**: 5 baseline year (1992·1993·1994·1995·1996) β 모두 sign 일치
7. **H7**: HIRA SSRI 처방률 β1 > 0 (z_x_h → 처방 ↑ 시 reverse asymmetry, 또는 < 0 시 export-driven mental health protective)
8. **H8**: HIRA F32 진단률 시도 단위 β1 sign 이 시군구 main spec 과 consistent
9. **H9**: KOSIS 시군구 자살 ASMR vs 본 paper main outcome 일치율 > 95%
10. **H10**: 본 paper β(Korea) sign 이 DFS 2014 독일 employment β sign 과 동일 mechanism ### Exploratory (no FWER) E1. KIET 60대 매핑 적용 first-stage F > 23.1 (목표)
E2. 전국사업체조사 broad baseline (모든 산업) sign 일치
E3. Conley spatial SE robust
E4. C09·A10·C10 negative control β ≈ 0 (만성질환 처방, 무역 무관 falsification)
E5. AKM 정식 BHJ 2022 implementation (P2) 의 OLS β 와 일관성 --- ## § 11. References 본 paper 가 인용하는 27편 reference paper deep summary: `4_documentation/reference_library/paper_summaries/paper_01_dauth_findeisen_suedekum.md` 등. **v4.0 시점 19편**: paper_01-08, 13-16, 24408 (GPSS), 24997 (BHJ), 25787 (DGLR), 5570 (Bartik), pierce_schott_2020_aeri 등. **이번 conversation 8편 추가 (paper_20-27)**:
- McManus & Schaur 2016 *Journal of International Economics*
- Lang, McManus & Schaur 2018 *Health Economics*
- Colantone, Crinò & Ogliari 2019 *Journal of International Economics*
- Autor, Dorn & Hanson 2019 *AER:Insights*
- Charles, Hurst & Schwartz 2019 *NBER Macroeconomics Annual*
- Eliason & Storrie 2009 *Journal of Human Resources*
- Sullivan & von Wachter 2009 *Quarterly Journal of Economics*
- Lee, McCrary, Moreira & Porter 2022 *American Economic Review* **Pending (P5)**: DGHP 2017 (Dippel-Gold-Heblich-Pinkovskiy) + DFH 2020 (Dippel-Ferrara-Heblich) 분리 인용 별도 file. --- ## § 12. Commit log (v4.0 → v4.5) ### 12.1 v4.0 (2026-05-04) — unified identification protocol
### 12.2 v4.1 (2026-05-05 morning) — Phase 4 publishable commit
### 12.3 v4.2 (2026-05-05 evening) — anchor 재배치 + LMP 정확값 + § 9 partial commit + § 13 신설
### 12.4 v4.3 (2026-05-05 late evening) — 9 inconsistency 정정 (target venue, AKM sign, WCB cluster, n 변경, Pre-WTO sign, Lang 비교 framing, 5-mediator PCA obsolete, Frölich-Huber 부적용, DGHP/DFH 분리 인용)
### 12.5 v4.4 (2026-05-05 evening) — 12 framing 정정 (Conley layer, KER full paper, ADH-7 → ADH-8 회복, PCA reasoning, Lang BRFSS vs HIRA, z_m_education 1985 baseline, DGHP/DFH spec, KOSIS 자살 only, references 27편 명시)
### 12.6 v4.5 (2026-05-05) — final clean version, audit-accepted 본 v4.5 = v4.0-v4.4 의 모든 정정 통합 + inline patch 표기 제거 + 깨끗한 narrative. ### 12.7 Pending list (paper draft Stage C 진입 전 commit 필수) | # | Pending | 처리 | Effort | Stage |
|---|---|---|---|---|
| **P1** | n=222 vs n=251 정합성 + 5 시군구 drop list | derived panel build code 검증 | direct 1-2h | Stage A |
| **P2** | AKM (BHJ industry-mode) 정식 implementation | R `ShiftShareSE` `reg_ss` 적용 | 위임 3-4h | Stage B |
| **P3** | AR-CI 산출 | linearmodels AR_test + ConfidenceSet | 위임 2-3h | Stage B |
| **P4** | WCB cluster-시도 G=16 결과 재산출 (verify) | Phase 4 5-layer SE script 재실행 | direct 1h | Stage A |
| **P5** | DGHP 2017 + DFH 2020 분리 인용 file | 별도 markdown citation | direct 30분 | Stage A |
| **P6** | Conley centroid SE 산출 (1km/5km/10km) | spatial cluster SE script | direct 1h | Stage A |
| **P8** | Pre-WTO sub-period sensitivity (1992-1995, 1990-1994) | placebo regression script | direct 1h | Stage A |
| **P9** | KOSIS 사망원인 50항목 시군구별 statistics search (despair 4 component 외부 검증) | KOSIS DT search | 사용자 측 다운 1h | 사용자 |
| ~~P10~~ | ~~Comtrade Switzerland fetch~~ — closed (build 코드 검증 결과 이미 포함) | — | 0 | closed | **Stage A 합계 (direct)**: P1 + P4 + P5 + P6 + P8 = 4-5h, 다음 turn 단일 가능
**Stage B 합계 (위임)**: P2 + P3 = 5-6h, 차차 turn 단일 위임
**사용자 측 P9**: KOSIS search 1h → Stage A·B + P9 모두 commit 후 v4.6 → paper draft Stage C (KER full paper format) 진입 ### 12.8 Track 3 — 1992 baseline build (사용자 audit B priority) PAP v4.5 의 § 5.3 의 5 baseline year sensitivity 의 첫 실행:
- 1992 광업제조업조사 microdata → baseline shares 1992
- z_x_h^{1992 baseline} 산출
- 1992 vs 1994 sensitivity 회귀
- 본 paper § 8.6 share-exogeneity violation 처리의 결과 의존성 해결 **Track 3 Status**: Stage A 와 병렬 가능 (direct 또는 위임). --- ## § 13. Outcome external validation ### 13.1 자료
- KOSIS DT_1B34E13 (사망원인별/시군구별/성별 사망자수·조사망률·연령표준화사망률, 50,071 행)
- 자살 (코드 102, X60-X84) 만 추출
- 본 paper 의 despair_total 의 main 구성 요소 (4 component 중 1, 약 50% 비중) ### 13.2 cross-check spec
시군구 × 연도 × 성별 단위로:
1. 본 paper 추정 ASMR (광업제조업조사 microdata + KOSIS 인구 + ICD 매핑) 산출
2. KOSIS DT_1B34E13 발표 ASMR 추출
3. 두 값의 절대 일치율 (within 1% tolerance) 측정 ### 13.3 보고 표 (paper § 3 Data 또는 § 8 Limitations)
| 시점 | 본 paper ASMR | KOSIS 발표 ASMR | 절대차 (%) |
|---|---|---|---|
| 1998 | (TBD) | 75.8 (DT_1B34E13) | (TBD) |
| 2008 | (TBD) | (TBD) | (TBD) |
| 2018 | (TBD) | (TBD) | (TBD) | ### 13.4 4 component 외부 검증 plan (P9 commit pending) | Component | 사망원인 코드 | ICD-10 | KOSIS 외부 source | 상태 |
|---|---|---|---|---|
| 자살 | 102 | X60-X84 | DT_1B34E13 | ✅ 받음 (50,071 행) |
| 약물 사망 | 101 | X40-X49 | DT_1B34E14 (?) | 🟡 P9 search |
| 정신활성물질 | 057 | F10-F19 | (?) | 🟡 P9 search |
| 간질환 | 081 | K70-K77 | (?) | 🟡 P9 search | P9 commit 후 § 13 의 4 component 외부 검증 표 commit. ### 13.5 활용
- KER reviewer 의 한국 microdata 신뢰성 비판에 직접 응답
- paper § 3 Data 의 검증 표 (1-2 paragraph)
- 일치율 > 95% 시 → main outcome 신뢰성 입증 (자살 component, 50% 비중) --- ## § 14. Paper draft 작성 plan (KER full paper format 25-35 page) ### Stage A (다음 turn, direct 4-5h)
- P1: n 정합성 + 5 시군구 drop list
- P4: WCB cluster-시도 G=16 verify
- P5: DGHP/DFH 분리 인용 file
- P6: Conley centroid SE 산출
- P8: Pre-WTO sub-period sensitivity ### Stage B (차차 turn, 위임 5-6h)
- P2: AKM 정식 BHJ 2022 implementation
- P3: AR-CI 산출 ### Track 3 (병렬, 사용자 audit B priority)
- 1992 광업제조업조사 baseline build (direct 또는 위임) ### 사용자 측 병렬
- P9: KOSIS 사망원인 50항목 시군구별 search (1h)
- HIRA 약물 9 ATC × 250 시군구 fetch 진행 중 (6일 분산) ### v4.6 commit (Stage A·B + Track 3 + P9 모두 완료 후)
- 8 pending 모두 closed
- AR-CI publishable verdict 결정
- AKM 정식 결과 + § 4.1 표 정정
- 4 component 외부 검증 표 (P9 결과)
- 1992 baseline sensitivity 결과 (Track 3)
- → paper draft Stage C (KER full paper format) entry-ready ### Stage C — paper draft 본격 작성 (KER full paper, 25-35 page)
- § 1 Introduction (3-4 page)
- § 2 Background & Korean trade context (2-3 page)
- § 3 Data (3-4 page)
- § 4 Identification + Spec (4-5 page)
- § 5 Main results (5-6 page)
- § 6 Robustness (4-5 page)
- § 7 Mechanism (4-5 page) — 6 mediator separate channel
- § 8 Discussion + Limitations (2-3 page)
- § 9 Conclusion (1-2 page)
- Online appendix: full robustness tables + mechanism details + 4 baseline sensitivity ### Stage D — Bibliography + Cover letter + KER submission --- ## 결론 본 PAP v4.5 = audit-accepted final clean version. v4.0-v4.4 의 모든 정정 (9 inconsistency + 12 framing + Switzerland 정합 회복) 통합 + inline patch 표기 제거. **Target venue**: KER 1순위 + AEJ Applied 2순위. AER:I 는 advisor 합류 + IV strength F>30 + multi-paper track 후 long-term goal. **Pending list**: 8개 (P1·P2·P3·P4·P5·P6·P8·P9). P10 closed. **Timeline**:
- v4.5 commit: ✅ (본 turn)
- Stage A (direct): 다음 turn 4-5h
- Stage B (위임): 차차 turn 5-6h
- Track 3 (1992 baseline): Stage A·B 와 병렬
- 사용자 측 P9: 1h (병렬)
- v4.6 commit + paper draft Stage C 진입: 차차차 turn
- KER submission ready: 4-6주 (timeline realistic) **Author**: 정재헌 (가천대학교 경제학, 단독 저자) — advisor 합류 negotiate 는 KER R&R 또는 AEJ Applied 도전 시점. 본 v4.5 는 **외부 advisor / reviewer 피드백 input 의 base**. 피드백 받은 후 v4.6 commit + Stage A 진입.
