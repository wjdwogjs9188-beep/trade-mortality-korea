# [#23] When Work Disappears: Manufacturing Decline and the Falling Marriage Market Value of Young Men

## 메타정보
- **저자**: David Autor (MIT), David Dorn (Zürich/CEPR), Gordon Hanson (UCSD/NBER)
- **출판년도**: 2019
- **학술지**: **American Economic Review: Insights** vol 1(2): 161-178
- **DOI**: 10.1257/aeri.20180010
- **JEL**: F16, J12, J13, J16, J23, J31, L60

## Research Question
무역 충격의 gender-specific labor demand 효과가 **결혼·출산·premature mortality** 에 미치는 영향. Becker household specialization model 의 trade shock test.

## Data
- US 722 commuting zones, 1990-2014
- Trade shock measure: ADH 2013 IV + gender-specific industry composition
- Outcomes: marriage rate, fertility rate, single-parent household, 20-39세 mortality (CDC certificate)

## Identification
ADH 2013 IV + male-female differential 분해:
```
ΔY_male - ΔY_female = α + β·(ΔIPW_male - ΔIPW_female) + γX + ε
```
Male-specific shock 측정 → 동일 CZ 내 male vs female mortality gap 변화

## Main Result
- Trade shock differentially male employment ↓ ($ earnings ↓ for young adult males)
- Marriage rate ↓ (trade-impacted CZs)
- Fertility ↓
- **Premature male mortality ↑** (esp. 20-39세 working-age)
- D&A (drug & alcohol) deaths: **+19.5 per 100k decade** (t=2.9) per unit trade shock — 30% of total male mortality contribution
- Single-mother household share ↑

## Connection to Trade × Mortality Korea
**역할: TIER A ANCHOR — gender × deaths of despair connection**

본 paper 와 거의 동일한 outcome (deaths of despair, 자살·약물·알코올 등 working-age mortality):
- ADH 2019 의 D&A 사망률 효과 = 본 paper 의 despair_total outcome 와 직접 매핑
- ADH 2019 의 marriage market mediation = 본 paper 의 z_m_marital (1975-1995 cohort sex ratio) anchor
- ADH 2019 의 male-specific framing = 본 paper 의 working-age 25-64 male 분리 가능

## 본 paper 의 PAP v4.2 reframing
- **ADH 2019 가 본 paper 의 가장 직접적인 anchor** (mortality outcome + ADH IV + working-age)
- **차별화**: 한국은 export-driven (D&A 사망률 ↓ 가 자연스럽게 예측됨, ADH 2019 의 mirror image)
- **paper § 1 narrative**:
 > "Autor, Dorn, and Hanson (2019) document that trade-induced manufacturing decline raises 
 > working-age male mortality from drug and alcohol causes in the US. We examine the inverse 
 > question: does trade-induced manufacturing growth in an export-oriented economy reduce mortality?"

## 본 paper § 9 mechanism (marriage market) 에 활용
- ADH 2019 의 marriage market deterioration = z_m_marital anchor (Phase B 의 mediator IV)
- Frölich-Huber 2017 ivmediate 의 외생적 mediator IV 로 z_m_marital 사용 가능

## Tier
- AER:Insights (top-5 의 short paper venue) — 본 paper publication 시 main anchor
