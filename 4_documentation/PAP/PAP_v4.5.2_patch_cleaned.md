# PAP v4.5.2 — Patch (Track 1 verified citation + Finkelstein 정정 + DGHP commit) **version**: 4.5.2 (patch on v4.5.1)
**date**: 2026-05-05
**author**: 정재헌 (가천대학교 경제학)
**supersedes**: v4.5.1 의 § 1.3 anchor 표 + § 5.4 ADH-8 + § 9.5 DGHP/DFH framework
**status**: paper draft Stage C 진입 prerequisite 본 patch 는 v4.5.1 audit 의 11 framing 정정 commit 후, paper PDF 9 paper 본문 직접 inspect 결과 verified citation commit. 1편 magnitude 정정 (Finkelstein) + DGHP 2017 framework spec 정확화. --- ## v4.5.1 → v4.5.2 변경 (4 항목) ### 1. § 1.3 — Finkelstein 2026 magnitude 정정 본문 직접 verify (BFI WP 2026-33 abstract):
> "In the 15 years post-NAFTA, an area with average NAFTA exposure experienced an increase in annual, age-adjusted mortality of 0.68 percent (standard error = 0.19)" **정정 (v4.5.2)**: | 이전 (v4.5.1) | 정정 (v4.5.2) |
|---|---|
| Finkelstein-Notowidigdo-Shi 2026 (BFI WP): drug death +5-9% (verify pending) | Finkelstein-Notowidigdo-Shi 2026 (BFI WP 2026-33): all-cause age-adjusted mortality +0.68% (SE 0.19), 15 years post-NAFTA, particularly working-age men. Drug-specific decomposition: 본문 Tables 4-5 추가 inspect pending | v4.5.1 의 "+5-9% drug death" 표기는 misattribution. Finkelstein 2026 의 main result 는 all-cause age-adjusted mortality (0.68%) 이며, drug-specific decomposition 별도 inspect 후 v4.5.3 commit 가능. ### 2. § 1.3 — 나머지 8 paper verified citation 표기 본문 직접 inspect 후 v4.5.1 의 specific values 모두 verified: | Paper | v4.5.1 표기 | Verified status |
|---|---|---|
| Lang 2019 F=18.77 | "verify pending" | Table 2 M.3 spec verified |
| PS20 +2-3/100k IQR (drug only) | 정정 framing | Abstract verified |
| ADH 2019 +19.5/100k decade | "verify pending" | Panel B col 4 verified (t=2.9, 30% of total) |
| Eliason HR=2.15 (suicide), 2.21 (alcohol) | round 2 정독 | Table 2 verified |
| Colantone £270/yr | published 값 | Abstract verified (working paper £200 → published £270) |
| McManus +12% smallest plant | round 2 정독 | Specific decile estimate verified |
| Sullivan 50-100% short / 10-15% long | abstract | verified | → § 1.3 anchor 비교 표의 "verify pending" 표기 모두 제거 (Finkelstein 만 partial pending). ### 3. § 5.4 — Lang 2019 F=18.77 verified 본문 직접 verify:
> "ΔIPW OTH_i ... Wk. instrument F stat ... 50.76 / 35.95 / 18.77" → § 5.4 의 "F 약 18-20 (paper 본문 verify pending)" hedged 표기 제거. F=18.77 (Lang 2019 Table 2, M.3 spec full controls) 정확 commit. | 이전 (v4.5.1) | 정정 (v4.5.2) |
|---|---|
| ADH-8 published (Lang 2019 Health Economics 28(1):44-56): F 약 18-20 (paper 본문 verify pending) | ADH-8 published (Lang 2019 Health Economics 28(1):44-56, Table 2 col M.3): F = 18.77 (Wk. instrument F stat, full controls). 본 paper F=19.65 와 거의 동일 IV strength + 동일 8 OECD list (AU·CH·DE·DK·ES·FI·JP·NZ) | ### 4. § 9.5 — DGHP 2017 framework spec 정확화 (Pinto 정정 + Framework 정밀) 본문 직접 verify (NBER WP 23209): **§ 9.5 정정 (v4.5.2)**: > "**Single-IV mediation framework (Dippel-Gold-Heblich-Pinto 2017, NBER WP 23209)**:
> > 본 paper 는 single Bartik IV (z_x_h) 만 보유. Frölich-Huber 2017 의 dual-IV requirement (mediator 의 별도 instrument) 부적용. DGHP 2017 의 single-IV mediation framework 적용.
> > **Model spec**:
> ```
> T = α_T + γ_T · Z + ε_T (treatment, instrumented by Z)
> M = α_M + β_M · T + ε_M (mediator, T endogenous)
> Y = α_Y + β_Y · T + ζ · M + ε_Y (outcome, both T and M endogenous)
> ```
> > **Identification (Assumption A-1, NBER WP 23209 Section 2)**:
> > Z ⊥⊥ ε_T, ε_M, ε_Y
> > 즉 standard IV exclusion restriction 의 generalization (Z 가 outcome error 와도 independent).
> > **'One additional identifying assumption'** (DGHP 2017 의 핵심 contribution):
> Imai-Keele-Yamamoto (2010) 의 Sequential Ignorability Assumption A-3 의 generalization. 정확 spec 은 NBER WP 23209 Online Appendix A — 본 paper 의 § 9.5 deep inspect 시 commit (v4.5.3).
> > **Implementation**: Standard 2SLS estimator. Bootstrap CI (1000 cluster-시도 wild bootstrap).
> > **Bounds option** (DGHP 2017 의 추가 contribution): identifying assumption 을 relax 시 bounds 보고 가능 (Conley-Hansen-Rossi 2012 spirit).
> > **6 mediator 별 separate channel decomposition**:
> Channel k (k = 1, ..., 6): SSRI 처방률, 이혼률, 출생률, 혼인률, z_m_marital, z_m_education
> 각 channel 의 indirect effect = ζ_k · β_k, direct effect = β_direct, total = β_total" → § 11 references 의 cite 정확화:
- "Dippel C, Gold R, Heblich S, Pinto R (2017). Instrumental Variables and Causal Mechanisms: Unpacking the Effect of Trade on Workers and Voters. NBER Working Paper 23209. March 2017, Revised June 2018." --- ## v4.5.2 미정정 항목 (Track 2·3 + 추가 inspect) ### Track 2 — z_m_education 검증
- 사용자 제공 학교 list (대학교 + 전문대학 + 교육대학 + 산업대학 + 과학기술원) + universities_4year_pre1990_clean.csv (175 학교) parse
- 1985 / 1990 / 1995 sub-cohort 별 시군구 nearest distance 재계산
- v4.5.1 § 9.4 의 baseline 정합성 검증
- 다음 turn direct 처리 (사용자 학교 list parse + distance 재계산) ### Track 3 — 1992 광업제조업조사 baseline build
- 1992 microdata schema 확인 + KSIC 6차 → KSIC 9차 변환
- 1994 build 코드 (`04_bartik_iv_build.py`) 패턴 확장
- 1992 baseline shares build script 작성
- z_x_h^{1992} 산출 + 1992 vs 1994 sensitivity 회귀
- 다음 turn direct 처리 ### DGHP 2017 추가 inspect
- "One additional identifying assumption" 정확 spec (NBER WP 23209 Online Appendix A)
- Application section (Section 4-5) 의 β_total / β_direct / ζ 추정값
- Bounds 결과 (partial identification)
- 다음 turn direct 처리 ### Track 4 — P1 sample universe
- per-outcome 별 sample size 차이 (Romano-Wolf step-down 의 "different sample sizes allowed")
- v4.1 의 n=222 가 어느 outcome 의 sample 인지 derived panel build code 검증
- Paper draft Stage C 시점에 outcome 별 정확한 n 표 commit
- v4.5.2 § 8.12 limitation 표현 그대로 유지 --- ## 결론 (PAP v4.5.2 patch commit) 본 v4.5.2 = Track 1 verified citation + Finkelstein 정정 + DGHP framework 정확. 8/9 paper 정확값 verified, 1편 (Finkelstein) magnitude 정정. **Pending 사항** (v4.5.3 commit 시점):
1. Finkelstein drug-specific decomposition 추가 inspect (Tables 4-5)
2. DGHP "one additional identifying assumption" 정확 spec (Online Appendix A)
3. Track 2 (z_m_education) 검증 결과
4. Track 3 (1992 baseline) build 결과 **Author**: 정재헌 (가천대학교 경제학)
**Date**: 2026-05-05
**Verified by**: direct PDF inspect (paper 9개 본 paper 폴더 보유)
