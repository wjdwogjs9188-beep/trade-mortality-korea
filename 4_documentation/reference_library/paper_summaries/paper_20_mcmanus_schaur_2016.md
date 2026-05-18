# [#20] The Effects of Import Competition on Worker Health ## 메타정보
- **저자**: T. Clay McManus (Xavier), Georg Schaur (Tennessee)
- **출판년도**: 2016
- **학술지**: **Journal of International Economics** vol 102: 160-172
- **DOI**: 10.1016/j.jinteco.2016.06.005
- **JEL 분류**: F16, F66, J81, J32, L60 > ⚠️ prior message 정정: "J Health Econ" 표기 오류. 정답은 **Journal of International Economics (JIE)**. ## Research Question
중국 수입 충격이 미국 manufacturing plant 의 **occupational injury rate** 에 미치는 영향.
가설: 작은 plant 일수록 외부 경쟁에 vulnerable → injury 상승. ## Data
- US Manufacturing plant-level injury data (BLS Survey of Occupational Injuries and Illnesses, SOII)
- Chinese import value (UN Comtrade), 1996-2007
- Plant-industry-year panel ## Identification
- ADH 2013 IV (다른 OECD 국가의 China 수입 = exogenous component)
- 2SLS, plant size interaction
- First-stage F: 1-year diff 약함, 2+년 diff F > 10 통과 ## Spec
```
Δlog(InjRate)_ij = β1·log(M_china)_j + β2·log(M_china)_j × log(L)_ij + β3·log(L)_ij + τ_j + θ_t + ε
```
β1+β2·log(L) = plant size 별 marginal effect ## Main Result
- 5-year diff: 가장 작은 plant decile (40 employees) elasticity ≈ +0.107 (p<0.01)
- Median (100 employees) ≈ +0.085 (p<0.05)
- Largest decile (400 employees): not sig
- Magnitude: 25→75 percentile 산업 수입 증가 → 작은 plant injury rate +12 ppt (1995-2007 중 7.4% 가 China shock 귀속)
- 1-2% wage equivalent welfare loss ## Connection to Trade × Mortality Korea
**역할: secondary anchor, mediator (occupational health → mortality channel)** - **본 paper 와 다른 점**: occupational injury (non-fatal, work injury) — 본 paper 의 deaths of despair 와는 outcome 다름
- **본 paper 와 같은 점**: - China shock × local labor market × health - ADH IV 2013 동일 framework - Small plant heterogeneity 발견 (본 paper 의 시군구 heterogeneity 비교 가능)
- **본 paper § 9 mechanism 에 활용**: - "occupational stress → mental health → suicide" 의 첫 link 의 micro evidence - 한국에서 직접 부가가치 노출 증가 산업 (부품제조 등) 이 occupational stress 통한 mortality channel 로 작동 가설 ## 본 paper § 1 인용 안 (예시)
> "Trade exposure affects health via multiple channels: occupational injury (McManus and Schaur 2016), > mental distress (Colantone et al. 2019; Lang et al. 2019), and mortality (Pierce and Schott 2020; > Finkelstein et al. 2026). This paper documents..."
