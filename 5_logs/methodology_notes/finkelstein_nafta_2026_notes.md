# Finkelstein-Notowidigdo-Shi 2026 NAFTA — 본 연구 적용 노트

**원논문:** Finkelstein, A., Notowidigdo, M.J., & Shi, S. (2026). "Trading Goods for Lives: NAFTA's Mortality Impacts and Implications." *BFI Working Paper 2026-33*.

**작성:** 2026-05-01 (본 연구의 가장 직접적인 비교·확장 framework)

---

## 1. Big Picture — 본 연구의 가장 중요한 reference

이 paper 는 **Pierce-Schott 2020 + ADH 2013 + Sullivan-von Wachter 2009 + Ruhm 2016** 결과를 **하나의 framework** 로 통합. 본 연구의 narrative 와 직접 연결.

### Core finding

> **무역 충격으로 인한 manufacturing 일자리 감소 → 사망률 증가**
> **그러나 비-manufacturing 일자리 감소 (recession 등) → 사망률 감소**
>
> → 같은 EPOP 감소라도 **manufacturing 인지 아닌지에 따라 mortality 영향 부호가 다름**

이게 **paradox 해결 framework**. 본 연구의 v3.x "기타 심장질환 보호효과" 와 직접 연결될 수 있음.

---

## 2. Identification Strategy — NAFTA Vulnerability Index

### Industry-level Mexican RCA + tariff
$$\text{RCA}_j = \frac{x^{MEX}_{j,1990} / x^{ROW}_{j,1990}}{\sum_i x^{MEX}_{i,1990} / \sum_i x^{ROW}_{i,1990}}$$

- $x^{MEX}_{j,1990}$: Mexico's 1990 exports of industry $j$ to non-US countries
- $x^{ROW}_{j,1990}$: Rest of world's exports of industry $j$ to non-Mexico countries

→ "Mexico has comparative advantage in industry $j$"

### Area-level vulnerability
$$\tilde{V}_c = \sum_j \frac{L^{1980}_{cj}}{L^{1980}_c} \cdot \widetilde{\text{RCA}}_j \cdot \tau^{1990}_j$$

- $L^{1980}_{cj}/L^{1980}_c$: 1980 industry $j$ employment share in CZ $c$ (pre-NAFTA baseline)
- $\widetilde{\text{RCA}}_j = \text{RCA}_j / \overline{\text{RCA}}_j$: normalized
- $\tau^{1990}_j$: 1990 US tariff on Mexican imports of $j$

### Scaled vulnerability
$$V_c = \frac{\tilde{V}_c}{\mathbb{E}[\tilde{V}_c | c \in Q_4] - \mathbb{E}[\tilde{V}_c | c \in Q_1]}$$

→ 1 unit = top quartile vs bottom quartile shift.

### Event study DID
$$y_{ct} = \beta_t [V_c \times \mathbb{1}(\text{Year}_t)] + \alpha_c + \tau_t + X_{ct}\phi + \epsilon_{ct}$$

- $\alpha_c$: CZ FE (722 CZs)
- $\tau_t$: year FE
- $X_{ct}$: Census region × year + demographic clusters × year
- 가중: 1990 CZ population
- SE: cluster on local area

**Bartik shift-share interpretation:** lagged 1980 employment shares assumed exogenous (Goldsmith-Pinkham 2020). Identifying assumption = parallel trends, testable via pre-1994 $\beta_t$.

---

## 3. Key Results — 본 연구가 직접 비교할 숫자

### Main NAFTA effect (1994-2008, 15년)

```
NAFTA top vs bottom quartile vulnerability:
  → +1.9% age-adjusted mortality (SE = 0.54)

Average CZ vulnerability = 0.35:
  → NAFTA increased mortality by 0.68% on average over 15년
```

**NAFTA welfare gain (Caliendo-Parro 2015) 보다 큰 사망 비용** = welfare-erasing effect.

### Heterogeneity

- **Working-age men** 영향 가장 큼
- **All age × sex groups** 어느 정도 영향
- 80% of NAFTA-induced EPOP decline = manufacturing (manufacturing 은 1993 employment 의 19%만)

### Manufacturing vs Non-manufacturing dichotomy ⭐⭐⭐

```
Specification:
  log(mortality) = β_m × ΔEPOP_M + β_n × ΔEPOP_N + α_c + τ_t

Results:
  β_m ≈ -1.5%  (1pp manufacturing 감소 → +1.5% mortality)
  β_n ≈ +0.5%  (1pp non-manufacturing 감소 → -0.5% mortality)

→ 부호 반대! 통계적으로 다름
→ 같은 magnitude EPOP 감소도 어디서 오느냐에 따라 mortality 영향 정반대
```

(주: paper 본문에 등장하는 수치는 **1.5% / 0.5%**. 이전 메모리에 있던 "1.4 / 1.1" 보다 더 큰 격차. 정확한 값은 paper main table 참조)

### Trade vs Recession 대조

| Shock | EPOP 감소 | mortality |
|-------|---------|-----------|
| **NAFTA** (1994+) | manufacturing dominant | +1.5% |
| **China Shock** (ADH) | manufacturing dominant | +1.5% (NAFTA 와 동일) |
| **Great Recession** (2008-2009) | non-manufacturing dominant | -0.5% (mortality ↓) |

→ Ruhm (2000)의 경기침체 → 사망 감소 paradox 와 ADH 의 무역충격 → 사망 증가 가 **manufacturing 비중 차이** 로 통합 설명됨.

---

## 4. 본 연구 (Trade × Mortality Korea) 직접 적용

### A. 본 연구의 핵심 가설 (Finkelstein 2026 framework 기반)

**한국의 export-driven 무역 (특히 對중국 중간재) → manufacturing 일자리 변동 → 사망률에 미치는 부호?**

가설들:
1. 한국은 export 가 양 (+) 이므로 manufacturing 일자리 안 줄어듦 → mortality protective effect (Finkelstein β_m 와 같은 메커니즘이지만 부호 반대 = export increase → 일자리 ↑ → 사망 ↓)
2. 한국 자영업율 25% 가 buffer → non-manufacturing 영향이 클 수 있음 → β_n 직접 적용
3. Net export 가 양 인데 일부 industry 는 import shock → 부분적 manufacturing 감소 → 부분적 mortality ↑

→ 본 연구는 **export 충격의 reverse direction**으로 Finkelstein framework 적용.

### B. 본 연구 specification (Finkelstein 차용)

```
ln(MortRate)_{ct} = β_t × [V^{KR-CN}_c × 1{Year_t}] + α_c + τ_t + X_{ct}φ + ε_{ct}
```

**한국 vulnerability index:**
$$V^{KR-CN}_c = \sum_j \frac{L^{1997}_{cj}}{L^{1997}_c} \cdot \frac{\Delta X^{KR \to CN}_j - \Delta M^{KR \leftarrow CN}_j}{1990 \text{ employment}}$$

- $L^{1997}_{cj}$: 1997 시군구 c의 산업 j 고용 (KOSIS 산업 microdata 31년치)
- $\Delta X^{KR \to CN}_j$: KSIC j 의 한국→중국 수출 변화 (Comtrade 50개 KR-CN bilateral)
- $\Delta M^{KR \leftarrow CN}_j$: KSIC j 의 한국←중국 수입 변화

→ Net exposure = 수출 - 수입 (수출 양이면 protective, 수입 양이면 negative)

### C. 본 연구의 핵심 robustness — Finkelstein β_m vs β_n decomposition

**제조업 (KSIC C) vs 비-제조업 별도 IV**:

```
ln(MortRate)_{ct} = β_m × ΔEPOP^M_{ct} + β_n × ΔEPOP^N_{ct} + α_c + τ_t + ε_{ct}

IV: KR-CN bilateral IV split by KSIC C (manufacturing) vs others
```

**기대 결과 (한국 케이스)**:
- 한국은 export-driven → manufacturing EPOP 안 줄어들거나 증가 → mortality protective effect
- v3.x "기타 심장질환 -3.8% 보호효과" 가 이 channel 일 가능성

→ Finkelstein 의 β_m (manufacturing decline → mortality ↑) 의 **거울상 (manufacturing increase → mortality ↓)** 가 본 연구의 main contribution.

### D. Finkelstein 2026 와 본 연구의 차이

| 항목 | Finkelstein 2026 | 본 연구 |
|------|------------------|---------|
| 국가 | US | 한국 |
| 충격 | NAFTA (Mexico import) | KR-CN trade (export-driven) |
| 직접 충격 방향 | manufacturing 감소 | manufacturing 안정/증가 |
| Outcome 예상 | mortality 증가 | mortality 보호효과 |
| 자영업 buffer | 미고려 | 한국 specific (25%) |
| 자살 | 부차적 | **main outcome** (Korea OECD top) |
| 기간 | 1986-2008 (NAFTA) | 1997-2023 (Korea-China) |
| 단위 | CZ (722) | h_code (256) |

### E. 본 연구의 paper narrative — Finkelstein 활용

**Section 1 (Introduction)**:
- Pierce-Schott 2020 + ADH 2013 + Finkelstein 2026 결과 정리
- "manufacturing decline → mortality 증가" 가 미국 패턴
- 본 연구: 한국의 reverse direction (export-driven manufacturing increase)

**Section 2 (Background)**:
- Korea-China 무역구조 (한국이 중간재 export, 중국이 final goods)
- Finkelstein framework 적용 가능성

**Section 3 (Methodology)**:
- KR-CN bilateral IV (Comtrade 50개)
- Finkelstein β_m, β_n decomposition 적용
- 5-layer SE (HC1, cluster-sido, AKM, Conley, AR+tF)

**Section 4 (Main Results)**:
- 자살 (102) — 한국 OECD top, main outcome
- 심혈관 (067-070) — Finkelstein β_m 의 거울상 검증
- Deaths of despair total

**Section 5 (Mechanism)**:
- Finkelstein 가 못 한 직접 mechanism: HIRA 약물 처방 panel
- 자영업 buffer (한국 specific)

**Section 6 (Heterogeneity)**:
- Manufacturing vs Non-manufacturing decomposition (Finkelstein 직접 차용)
- 광역시 vs 도, 자영업율 splits

---

## 5. 본 연구의 contribution 강조

기존 연구들과 비교:
- Pierce-Schott 2020: PNTR → drug overdose ↑ (백인 working-age)
- ADH 2013: China Shock → manufacturing 일자리 ↓
- Finkelstein 2026: NAFTA → manufacturing decline → mortality ↑ (β_m 양)
- Sullivan-von Wachter 2009: plant closing → mortality ↑ (개인 단위)
- Ruhm 2000: recession → mortality ↓ (β_n 음)

**본 연구의 unique contribution:**
1. **Korea-China bilateral IV** (export-driven, opposite direction of US Mexico/China shock)
2. **Hidden protective effect** — Finkelstein β_m 의 거울상 검증
3. **Korea-specific 자영업 buffer**
4. **HIRA mechanism** — 직접 약물 처방 panel
5. **Suicide as main outcome** — Korea 자살률 OECD top

→ paper "Hidden Protective Effect Beneath ADH-Style Bartik Designs" 의 motivation 이 Finkelstein 2026 framework 와 정확히 일치.

---

## 6. 핵심 인용구

> "We estimate that a 1 percentage point trade-induced decline in area EPOP from either NAFTA or exposure to trade from China increases age-adjusted mortality by the same magnitude (about 1.5 percent); ... but are of opposite sign and statistically distinguishable from our estimates that a 1 percentage point recession-induced area EPOP decline *reduces* mortality by about 0.5 percent." (Abstract)

> "Local area declines in manufacturing employment increase mortality, while local area declines in non-manufacturing employment *decrease* mortality." (Introduction)

> "These findings suggest that the sign and magnitude of any mortality impacts of future economic shocks likely depends critically on how much these shocks affect the manufacturing sector relative to non-manufacturing sectors." (Conclusion)

---

## 7. 본 연구의 specification 채택

**Phase 4 main 회귀 시 Finkelstein 2026 의 다음 specification 직접 차용:**

1. **Event study DID** with year × IV interactions
2. **CZ FE + year FE** (본 연구: h_code FE + year FE)
3. **Demographic clusters × year** (본 연구: 1997 baseline 자영업율·산업구조 × year)
4. **Cluster SE on local area** (본 연구: sido cluster)
5. **Manufacturing vs Non-manufacturing decomposition** (Finkelstein 의 핵심 contribution)
6. **β_m / β_n 별도 IV** for Korea-China shock + Great Recession (한국 IMF 1997, COVID 2020 recession 비교)

**예상 paper title 보강:**
- 현재: "Trade Exposure and Mortality in Export-Oriented Korea: A Hidden Protective Effect Beneath ADH-Style Bartik Designs"
- 강화 안: "...A Hidden Protective Effect Through Manufacturing Stabilization in Korea-China Trade" — Finkelstein framework 직접 명시

---

## 8. 다음 단계 메모

1. Finkelstein 의 정확한 specification 표 (Table 2-3) 확인 — Phase 4 시 직접 비교
2. Manufacturing EPOP 정의 (CBP/SEER 데이터) → 한국 산업 microdata 의 KSIC C 매핑
3. β_m vs β_n IV 방식 — Great Recession 같은 한국 recession 변수 (IMF 1997, 2008, COVID) 사용 가능성
4. Welfare analysis (Section 4) — 본 연구도 Caliendo-Parro 같은 trade welfare 비교
