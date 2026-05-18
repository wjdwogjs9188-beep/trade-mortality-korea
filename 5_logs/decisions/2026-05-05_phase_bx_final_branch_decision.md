# Phase B-x FINAL Branch Decision **date**: 2026-05-05
**author**: **status**: **final** (Phase 2-A 후 Test 3 보강 가능) ## 결과 chain (전체 진단) | 검정 | 결과 | 판정 |
|------|------|------|
| Test 1 v1 (saturated) | Joint F=130, p<0.0001 | saturation 인공물 의심 |
| Test 1 v2 (univariate Bonferroni) | 2/6 sig (GDP, 수입가) | 수입가 VIF=27.9 → multicollinearity 의심 |
| Test 1 v3 (drop 수입가) | **1/5 sig (GDP only)** | year FE 가 흡수 가능 |
| Test 1b (WEO surprise) | 0/2 sig (β≈0, p=0.74) | **shock-orthogonality PASS** |
| **First-stage F (ADH-8)** | F(HC1)=14.07, F(cluster)=12.20 | **weak-IV** |
| **First-stage F (bilateral)** | **F(HC1)=48.08, F(cluster)=19.65** | **strong by HC1, borderline by cluster** | ## Final spec **Main: A.ii — KR-CN bilateral primary** ```
Specification: Δ_5y log(mortality_h) = α + β · z_x_h^{KR-CN} + γ · X_h + δ_t + ε_h z_x_h^{KR-CN} = (1/E_{h,1994}) · Σ_k s_{h,k,1994} · ΔM_{KR-CN, k, 2000-2010} Conditions: - year FE mandatory (Test 1 결정) - tF inference mandatory (cluster-sido F=19.65 < 23.1) - 5-layer SE: HC1 + cluster-sido + WCB-sigungu + AKM (BHJ 2022) + Conley - X_h = pre-period mortality trend + sigungu controls Robustness: - ADH-8 Bartik (weak F → reported as supplementary) - winsorize z_x at p1/p99 - 1994 baseline → 1999/2004 baseline vintages - Romano-Wolf reduced-form (10 confirmatory hypotheses)
``` ## 9-branch matrix 매핑 | 분기점 | 결과 | 적용 branch |
|--------|------|-------------|
| Test 1 macro orthogonality | conditional pass (year FE 흡수) | A 계열 살아남음 |
| Test 1b WEO shock | full pass | A 계열 confirm |
| First-stage F ADH-8 | weak (F<23.1) | A.i 격하 |
| First-stage F bilateral | HC1 strong, cluster borderline | **A.ii** 선택 + tF 의무화 |
| Test 3 pre-trend | pending Phase 2-A | future check | ## Pending (Phase 2-A 후) 1. **Phase 2-A 사망률 panel** build (5 outcome groups × 251 시군구 × 27y)
2. **Test 3 재실행** (script 24) — Phase 2-A 후 입력 가능
3. **Reduced-form** — Δlog mortality ~ z_x_h^{KR-CN} 직접
4. **Winsorize sensitivity** — z_x p1/p99
5. **Wild cluster bootstrap** — 15 sido cluster 의 작은 수 보정
6. **Romano-Wolf step-down** — 10 confirmatory family ## Anchor - ADH (2013 AER): Bartik IV with 4-digit SIC, F^eff ~ 60-80 (USA)
- Pierce-Schott (2020 AERI): NTR gap shock, USA F > 100
- Sufi-Korea (2023 BFI WP): bilateral CN exposure for Korean 시군구, Korea-specific framework
- Olea-Pflueger (2013): F^eff cutoff 23.1 (5% TSLS bias robust)
- Lee-Moreira-McCrary-Porter (2022): tF inference for borderline IV
- Cameron-Gelbach-Miller (2008): cluster wild bootstrap when clusters < 30
