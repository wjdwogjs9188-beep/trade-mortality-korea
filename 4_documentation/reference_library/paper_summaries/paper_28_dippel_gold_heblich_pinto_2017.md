# [#28] Instrumental Variables and Causal Mechanisms: Unpacking the Effect of Trade on Workers and Voters ## 메타정보
- **저자**: Christian Dippel (UCLA Anderson), Robert Gold (Kiel Institute), Stephan Heblich (Bristol), **Rodrigo Pinto (UCLA)**
- **출판년도**: 2017 working paper, revised June 2018
- **논문 종류**: NBER Working Paper No. 23209
- **JEL**: F1, F6, J2
- **DOI / URL**: https://www.nber.org/papers/w23209 > ⚠️ **round 22 정정 확정**: 4번째 author = **Rodrigo Pinto** (Pinkovskiy 아님). Maxim Pinkovskiy (NY Fed economist) 와 별개 인물. ## Research Question 표준 IV (single-instrument) 만으로 mediation analysis 가능한가? Trade exposure (T) 가 labor market adjustments (M) 를 통해 voter polarization (Y) 에 영향. 표준 IV 는 T → Y 의 total effect 만 추정. **single IV Z 로 T → M, T → Y 분리 + indirect effect (T → M → Y) 추정 framework**. ## Key contribution 본 paper 는 **single-IV mediation** 의 정식 framework. Frölich-Huber (2017) 의 dual-IV requirement (T 와 M 양쪽에 별도 instrument) 를 회피. ## Framework spec (Section 2-3 의 정확 명시) ### Model III (IV Mediation)
```
T = α_T + γ_T · Z + ε_T (treatment, instrumented by Z)
M = α_M + β_M · T + ε_M (mediator, T endogenous)
Y = α_Y + β_Y · T + ζ · M + ε_Y (outcome, both T and M endogenous)
``` - T endogenous (in regression of M on T)
- M endogenous (in regression of Y on M and T)
- Z exogenous (single IV)
- Two endogenous regressors, single IV → standard IV underidentified ### Identification (Assumption A-1) **Standard IV exclusion restriction (Assumption A-1)**:
> "The independence relation **Z ⊥⊥ ε_T, ε_M, ε_Y** holds in the mediation model (1)–(3)." Z 가 unobserved error terms (T, M, Y 의 jointly cause) 와 statistically independent. 이는 IV 의 정의 자체. ### "One additional identifying assumption" 본 paper 의 핵심 contribution. Section 2.B 또는 Online Appendix A 에서 정의된 추가 assumption (본문 깊은 inspect 후 commit 예정). → **본 paper § 9.5 의 정확 spec 은 추가 inspect 후 v4.5.2 patch commit**. ### Frölich-Huber 2017 와의 명시적 대비 본문 인용:
> "The only existing approaches to achieving identification in the IV setting of Model III require **separate dedicated instruments for M**, which require additional exogeneity assumptions that are considerably more restrictive than the standard ones (e.g. Jun, Pinkse, Xu, and Yildiz 2016; **Frolich and Huber 2017**)." > "Our proposed solution does not assume away endogeneity in any of the key relationships in Model III and **does not require additional instruments**. Instead, we rely on the insight that... **one additional identifying assumption** alone is sufficient to unpack the causal channels in Model III." ### Imai-Keele-Yamamoto 2010 의 Sequential Ignorability Assumption A-3 와 contrast > "A large literature on mediation analysis relies on the **Sequential Ignorability Assumption A-3 of Imai, Keele, and Yamamoto (2010)** to identify mediation effects. This assumption is discussed in Online Appendix A. See **Frolich and Huber (2017)** for a recent review of the mediation literature." → DGHP 2017 의 추가 assumption 은 Imai et al. 의 Sequential Ignorability 의 generalization. ## Implementation > "can be easily implemented using the well-known **Two-Stage Least Squares (2SLS) estimator**" 본 paper 는 2SLS 의 single-IV setting 에서 mediation decomposition 가능 → 본 paper § 9.5 의 정확한 estimator. ### Bounds option
> "The added identifying assumption can be relaxed, and bounds instead of point estimates can be derived." → Conley-Hansen-Rossi (2012) 의 plausible bounds 와 spirit 동일. ## Application (Section 4-5) - Treatment T: Chinese import exposure (Germany 1988-2010)
- Mediator M: regional labor market adjustments (manufacturing employment, wages)
- Outcome Y: voter polarization (right-wing populist vote share)
- Instrument Z: ADH 2013 의 8 OECD imports IV **Result**: "labor market adjustments explain **most to all of the effect** of import exposure on voting" → policy response 는 labor market 에 focus 해야. ## Connection to Trade × Mortality Korea **역할: § 9.5 의 정식 framework anchor** 본 paper § 9.5 의 6 mediator framework (HIRA 약물 + KOSIS family + z_m_marital + z_m_education) 의 single-IV mediation framework 의 정확 spec source. ### 본 paper 적용
- Treatment T: KR-CN bilateral trade exposure (z_x_h)
- Mediator M (6 channel): SSRI 처방률, 이혼률, 출생률, 혼인률, z_m_marital, z_m_education
- Outcome Y: deaths of despair mortality (despair_total log_asr_p1)
- Instrument Z: Bartik IV (z_x_h 자체가 IV — 본 paper 는 reduced-form main spec 으로 별도 IV 안 씀) → DGHP 2017 framework 적용 시: z_x_h 를 외생적 shifter 로 가정하면 single-IV 효과 본 paper setting 에 자연스럽게 적용. 별도 IV 두 개 (Frölich-Huber) 요구 회피. ### 6 mediator 별 separate channel reporting 본 paper § 9.5 의 6 mediator 각각 별도로 DGHP 2017 framework 적용: ```
Channel k (k = 1,..., 6): m_k = α_k + β_k · z_x_h + ε_k (mediator) y = α + β_total · z_x_h + γ · X + ε (total) y = α + β_direct · z_x_h + ζ_k · m_k + γ · X + ν (direct + indirect via m_k) Indirect via m_k = ζ_k · β_k Direct = β_direct Total = β_direct + ζ_k · β_k = β_total
``` 각 channel k 별 decomposition + bootstrap CI. ## 본 paper § 9.5 commit 사항 **v4.5.2 patch 권장**:
1. § 9.5 framework anchor: DGHP **2017** (Pinto) + Frölich-Huber 2017 명시적 대비
2. Identification 가정: Assumption A-1 (Z ⊥⊥ ε_T, ε_M, ε_Y) + "one additional identifying assumption"
3. Implementation: 2SLS standard + bootstrap CI
4. Bounds option: 본 paper 가 partial identification 보고 시 (Conley-Hansen-Rossi 2012 spirit)
5. 6 mediator 각각 별도 channel decomposition ## Tier
- T0 (NBER WP, single-IV mediation framework 정식 source) — 본 paper § 9.5 의 직접 anchor ## 추가 inspect pending
- Section 2.B (또는 Online Appendix A) 의 "one additional identifying assumption" 정확 spec
- Application section (Section 4-5) 의 specific β_total / β_direct / ζ 추정값
- Bounds 결과 (relaxed identification) → 다음 turn deep inspect 시 § 9.5 정확 spec commit
