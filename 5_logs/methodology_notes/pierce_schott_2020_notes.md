# Pierce-Schott 2020 (AER:Insights) — 본 연구 적용 노트

**원논문:** Pierce, J.R. & Schott, P.K. (2020). "Trade Liberalization and Mortality: Evidence from US Counties." *AER: Insights* 2(1): 47-64.

**작성:** 2026-05-01 (본 연구 Phase 5 mechanism + Phase 4 baseline 비교용)

---

## 1. Research Question

> 미국이 중국에 PNTR (Permanent Normal Trade Relations, 2000) 부여 → 무역 자유화 충격이 county 단위 사망률에 영향?

**Outcome:** Deaths of despair (Case-Deaton 2015 정의)
- Drug overdose
- Suicide
- ARLD (Alcohol-related liver disease)

**핵심 finding:** **drug overdose** 만 통계적으로 유의 ↑, suicide·ARLD 는 효과 없음.

---

## 2. Identification Strategy — NTR Gap

### 정의
$$\text{NTRGap}_j = \text{NonNTRRate}_j - \text{NTRRate}_j$$

- NonNTRRate: Smoot-Hawley 1930 관세율 (PNTR 통과 전 가능했던 인상폭)
- NTRRate: 실제 적용된 낮은 관세율
- Industry $j$ 의 PNTR exposure = "관세 인상 위협 크기"

### County-level exposure
$$\text{NTRGap}_c = \sum_j \frac{L^{1990}_{jc}}{L^{1990}_c} \cdot \text{NTRGap}_j$$

→ 1990년 (정책 10년 전) employment share 가중평균.

### Identifying assumption
- Non-NTR rates 는 1930년에 fixed → 2000년 산업 동향과 무관
- 79% variation 이 non-NTR 변동에서 나옴 → reverse causality 가능성 거의 없음

### DID specification
$$\text{DeathRate}_{ct} = \sum_t \theta_t \mathbb{1}\{year=t\} \times \text{NTRGap}_c + \beta X_{ct} + \sum_t \gamma_t \mathbb{1}\{year=t\} \times X_c + \delta_c + \delta_t + \varepsilon_{ct}$$

- $\delta_c$: county FE
- $\delta_t$: year FE
- $X_{ct}$: time-varying (US import NTR tariff, MFA exposure)
- $X_c$: 1990 county attributes (income, college share, manufacturing share, foreign-born share, veteran share, China policy variables)
- 가중: 1990 인구
- SE: state cluster

---

## 3. Key Results

### Magnitude
- IQR shift in NTRGap (8.3 percentage points) → **2-3 deaths/100k 증가** (drug overdose)
- 2000년 county 평균 drug overdose rate = 5/100k → **상대적 +40-60%**

### Heterogeneity
- **백인** 만 효과 (다른 인종 X)
- **20-54세** 작업연령 강함
- **남성 > 여성** (manufacturing 의 male skew 때문)

### No effect
- Suicide ❌
- ARLD ❌
- Cancer, respiratory 등 internal causes ❌

---

## 4. Robustness 체크

1. **CUMA aggregation** (PUMAs, min 100k 인구) → 결과 동일
2. **Medicaid expansion** dummies → 결과 동일
3. **Opioid 법규제** controls → 결과 동일
4. **State-year FE** (가장 conservative) → SE 커지지만 직관 동일
5. **Other internal causes 16개** → 효과 없음 (placebo 통과)

---

## 5. Mechanisms (Section IV)

### Labor market deterioration
- IQR NTRGap → 실업률 +1-2pp ↑
- LFPR -1-2pp ↓ (정책 후)
- Disability transfer 증가
- Disabled workers 증가

### Disability + Opioid 연결
- 1996 Oxycontin 출시 + 2000 PNTR 동시
- 일자리 잃은 사람들이 disability 신청 → opioid 처방 → 중독·사망

> "Quinones (2015): 'Waves of people sought disability as a way to survive as jobs departed... an economic coping strategy'"

---

## 6. 본 연구 (Trade × Mortality Korea) 에 적용

### A. 직접 비교 항목

| Pierce-Schott 2020 | 본 연구 |
|--------------------|---------|
| US, county 단위 | Korea, h_code (시군구) 단위 |
| PNTR (2000) NTR Gap | KR-CN bilateral (수입-수출) net exposure |
| 1990-2013 panel | 1997-2023 panel |
| Drug overdose 효과 | 본 연구 코드 101 (drug poisoning), 057 (substance use), 081 (간 질환) 비교 |
| Suicide 효과 없음 | 본 연구 코드 102 — Korea suicide rate 가 OECD 최고 → 효과 다를 가능성 |
| ARLD 효과 없음 | 본 연구 코드 081 비교 |
| Manufacturing 백인 남성 | 본 연구 sex × age subgroup 별 분석 — 한국 자영업율 25% 특이 |

### B. 본 연구가 Pierce-Schott 와 다른 이유

1. **한국은 export-driven** (vs 미국 import-shock)
   → Korea-China bilateral net exposure 가 더 적합
   → 효과 방향 (단순 음 vs 양) 가설 다를 수 있음

2. **한국의 자영업 buffer**
   → 미국 manufacturing 일자리 잃으면 disability 로 갔지만,
   → 한국은 자영업 (편의점·음식점) 으로 흡수 → 사망 효과 약화 가능성

3. **Drug overdose vs Suicide**
   → 미국: opioid epidemic (Oxycontin 1996+)
   → 한국: opioid 처방 매우 제한적, 자살이 dominant deaths of despair
   → **본 연구 main outcome 은 자살 (102)**, drug 보다.

4. **Pierce-Schott "기타 심장질환" placebo**
   → 본 연구 v3.x 에서 "기타 심장질환 (069 = I26-I51) -3.8% 보호효과"
   → Pierce-Schott 는 internal causes 0 효과 (placebo 통과)
   → 본 연구 발견은 **PSc 와 다른 conclusion** = 한국 export 충격의 cardiovascular 보호 효과 가능성
   → **paper main contribution** 으로 강조

### C. 본 연구의 specification 설계 (PSc 차용)

```
ln(MortRate)_{ct} = θ_t × Bartik_c + β_t × X_c + δ_c + δ_t + ε_ct
```

- `Bartik_c` = 1997 시군구 employment share weighted KR-CN net export shock
- `δ_c` = h_code FE (256개)
- `δ_t` = year FE (27개)
- `X_c` = 1997 baseline controls (인구·자영업율·산업구조·고령화)
- 가중: 1997 인구
- SE: sido cluster (PSc 의 state cluster 와 동일 logic, 17개 sido)

### D. 본 연구의 추가 robustness (PSc 차용)

1. **CUMA 비슷** — 광역 단위 aggregation (시 단위 합산) — robustness check
2. **Other causes placebo** — 본 연구도 cancer/respiratory 등 placebo
3. **Pre-trend** — 2000 이전 KR-CN trade 가 mortality 에 영향 없는지
4. **State-year FE** (한국: sido-year FE) — 가장 conservative
5. **HIRA 약물 처방** (Phase 5 mechanism) → Pierce-Schott 가 못 본 직접 mechanism

### E. paper 인용 시점

Pierce-Schott 2020 인용 위치:
- **Introduction**: 미국 사례 motivation
- **Section 2 (Identification)**: NTR Gap 과 본 연구 Bartik 차이 설명
- **Section 4 (Results)**: 한국 자살 효과 vs 미국 drug 효과 대조
- **Section 5 (Mechanism)**: HIRA 데이터로 PSc 가 못 한 직접 mechanism 검증
- **Section 6 (Conclusion)**: 본 연구의 "Hidden Protective Effect" 가 PSc 의 사망률 ↑ 와 다른 이유 (export-driven)

---

## 7. 핵심 인용구 (paper draft 시 사용)

> "We find that counties more exposed to the change in US trade policy exhibit relative increases in deaths of despair... the link between PNTR and mortality is driven by drug overdoses." (PSc 2020, p.47)

> "Our contribution to this literature is to exploit a plausibly exogenous change in policy for identification." (p.49)

> "By contrast, we do not find an association between PNTR and drug overdose deaths for males or females of other races." (p.51)

> "While our findings do not provide an assessment of the overall welfare impact of this liberalization, they do offer a broader understanding of the distributional implications of trade." (p.59)

---

## 8. 본 연구의 narrative 차별화

**Pierce-Schott:** "미국 무역자유화 → 백인 working-age 약물중독 사망 ↑"

**본 연구:** "한국 export-driven 무역구조 → 일부 사망 outcome 보호효과 (heart diseases I26-I51), 자살은 다른 mechanism"

→ 직접 mirror 가 아니라 **complement / contrast** 관계.

본 연구의 contribution:
1. ADH-style import shock 외에 **export-driven 한국 케이스**
2. **자살** main outcome (Korea OECD top)
3. **Hidden protective effect** (cardiovascular)
4. **HIRA mechanism 직접 검증** (PSc 가 prescription data 없어 못 한 부분)

---

## 9. Phase 4 회귀 시 reference 사용

| 본 연구 specification | Pierce-Schott 와 동일/차이 |
|-----------------------|------------------------|
| DID with year × IV interactions | ✅ 동일 |
| h_code (county) FE + year FE | ✅ 동일 |
| 1997 baseline controls × year | ✅ 동일 |
| 가중 1997 인구 | ✅ 동일 |
| Sido (state) cluster SE | ✅ 동일 |
| 5-layer SE (HC1, cluster, AKM, Conley, AR+tF) | ⭐ 본 연구 차별화 |
| Multiple causes (despair, cardio, cancer 등) | ⭐ 본 연구 확장 |
| HIRA 약물 mechanism | ⭐ 본 연구 추가 |
