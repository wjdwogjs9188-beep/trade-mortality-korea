# Dauth-Findeisen-Suedekum 2014 (German East-trade) — 본 연구 적용 노트

**원논문:** Dauth, W., Findeisen, S., & Suedekum, J. (2014). "The Rise of the East and the Far East: German Labor Markets and Trade Integration." *Journal of the European Economic Association* 12(6): 1643-1675.
(working paper version: DICE Discussion Paper No. 127, December 2013)

**작성:** 2026-05-01 (한국과 가장 비슷한 export-driven 케이스)

---

## 1. Big Picture — 본 연구의 가장 직접적 mirror case

이 paper 는 **export-driven 경제 (독일) 가 무역 충격에 어떻게 반응하는지** 의 가장 명확한 분석. 한국이 export-driven 이라는 특성이 정확히 일치 → **본 연구의 가장 직접적 비교 framework**.

### Core finding (놀라운 결과)

> 1988-2008 독일이 "the East" (중국 + 동유럽) 와 무역 통합 → **+442,000 일자리 순증가**
>
> Mechanism:
> - **Import shock** (수입 경쟁 산업) → 일자리 감소 (ADH-style)
> - **Export shock** (수출 기회) → 일자리 증가 ← 더 큼
> - **Net: 일자리 증가** ⭐
>
> 흥미로운 점: 거의 **동유럽** 효과 (중국 효과는 작음)

→ ADH (미국) 와 정반대 결과. 같은 China shock 인데 독일은 protective.

---

## 2. Identification Strategy — Two-Way Bartik IV

### Import exposure (ADH 차용)
$$\Delta(\text{Import exp.})^{EAST}_{it} = \sum_j \frac{E_{ijt}}{E_{jt}} \cdot \frac{\Delta Im^{D \leftarrow EAST}_{jt}}{E_{it}}$$

- $E_{ijt}/E_{jt}$: 독일 region $i$ 의 산업 $j$ 노출 share
- $\Delta Im^{D \leftarrow EAST}_{jt}$: 독일의 산업 $j$ Eastern import 변화
- $E_{it}$: region $i$ employment

### Export exposure (DFS 의 contribution)
$$\Delta(\text{Export exp.})^{EAST}_{it} = \sum_j \frac{E_{ijt}}{E_{jt}} \cdot \frac{\Delta Ex^{D \to EAST}_{jt}}{E_{it}}$$

→ Symmetric to imports, but using exports.

### Instrumental variable (ADH-style)
- Other high-income countries 의 trade flows 사용
- Reverse causality 차단 (독일 specific shock 와 무관)

### Specification
```
Δ y_{it} = β_M × Δ(Import exp.)_{it} + β_X × Δ(Export exp.)_{it} 
         + α_i + τ_t + X_{it}φ + ε_{it}
```

- $y_{it}$: manufacturing emp share, unemployment, etc.
- 가중: 1988 region population
- Cluster SE: state level

---

## 3. Key Results — Import vs Export 분리

### Manufacturing employment

| Spec | Import effect | Export effect | Net |
|------|---------------|---------------|-----|
| ADH (US, 2013) | β_M = -0.746 (significant) | (analyzed only as "exposure") | Manufacturing ↓ |
| DFS (Germany, 2014) | **β_M < 0 (significant)** | **β_X > 0 (significant, larger)** | **Manufacturing ↑** |

→ ADH 의 "import-only" 가 실은 **net effect of imports + exports**. 미국은 import dominant, 독일은 export dominant → 정반대 결과.

### Aggregate impact
- 442,000 net additional jobs (1988-2008)
- 거의 전부 **Eastern Europe** 효과 (중국 효과는 작음)
- 동유럽 = "natural trading partner" (지리적 + 1989 베를린 장벽 후 통합)

### Sectoral breakdown
- **Import-competing sectors** (textiles, toys, office equipment): 일자리 감소
- **Export sectors** (자동차, 기계, 의료기기): 일자리 증가
- 후자가 magnitude 더 큼

---

## 4. 본 연구 (Trade × Mortality Korea) 적용 — 가장 중요한 reference

### A. 한국과 독일의 닮은꼴

| 특성 | 독일 (DFS 2014) | 한국 (본 연구) |
|------|----------------|-----------------|
| 무역 구조 | Export-driven | Export-driven |
| China trade balance | Imports < Exports (deficit small) | Net export 양 (한국은 흑자) |
| Manufacturing 비중 | 높음 (1988+) | 높음 (1997+) |
| 주요 export 산업 | 자동차, 기계, 전자 | 반도체, 자동차, 화학 |
| 거리·관계 | EU + Eastern Europe (지리·정치) | 동아시아 + 중국 (지리·문화) |

→ 한국은 **독일의 동아시아 버전**. DFS 의 framework 가 가장 직접 적용 가능.

### B. 본 연구의 specification — DFS 차용

**Import-Export 분리 IV** (DFS 의 가장 큰 contribution):

```
ln(MortRate)_{ct} = β_M × ImportExp_{ct} + β_X × ExportExp_{ct}
                  + α_c + τ_t + X_{ct}φ + ε
```

본 연구 한국 데이터:
- $\Delta M^{KR \leftarrow CN}_{j,t}$: 한국 산업별 중국 imports (Comtrade KR-CN bilateral 50 files)
- $\Delta X^{KR \to CN}_{j,t}$: 한국 산업별 중국 exports (Comtrade KR-CN)

→ **β_M (import effect on mortality)**: 미국·독일 import 효과 비교
→ **β_X (export effect on mortality)**: 새로운 contribution (DFS 가 employment 만 본 것을 mortality 로 확장)

### C. 본 연구 가설 (DFS framework 기반)

**Manufacturing employment level 의 mortality 영향:**
1. **β_M > 0 (import 충격이 mortality ↑)**: ADH/Pierce-Schott/Finkelstein 차용
2. **β_X < 0 (export 기회가 mortality ↓)**: DFS 의 employment gain 의 health spillover
3. **Net effect**: 한국이 export-dominant (DFS 처럼) → **net protective effect** ⭐

→ v3.x 의 "Hidden protective effect" 가 정확히 이 mechanism 으로 해석됨.

### D. 본 연구의 narrative — DFS 직접 차용

**기존 ADH/Pierce-Schott narrative:**
"Trade shock → employment ↓ → mortality ↑"

**DFS narrative:**
"Trade shock 에 import 와 export 둘 다 있음. 미국은 import dominant 라 employment ↓, 독일은 export dominant 라 employment ↑."

**본 연구의 narrative (DFS 확장):**
"DFS 가 독일에서 employment 영향만 봤지만, 본 연구는 **mortality outcome 으로 확장**.
한국 export-driven 무역구조 → β_X > 0 로 mortality 보호효과.
따라서 한국 = DFS 의 mortality version"

→ paper title 강화 안:
> "Trade Exposure and Mortality in Export-Oriented Korea: A Hidden Protective Effect Beneath ADH-Style Bartik Designs — A German-Style Export Channel for Health Outcomes"

### E. 본 연구의 robustness (DFS 차용)

DFS 의 robustness checks:
1. **Eastern Europe vs China 분리**: 독일은 동유럽 효과 main
   → 본 연구: **중국 import vs export 분리** 효과 비교 (Comtrade KR-CN 50 files 활용)
2. **Industry sub-classification**: 자동차 vs 텍스타일 등
   → 본 연구: KSIC 산업별 robustness
3. **Individual worker-level analysis**: panel of workers
   → 본 연구는 시군구 단위만 (개인 단위 mortality data 없음, KOSTAT microdata limit)

---

## 5. 핵심 인용구

> "We find that the rise of 'the East' in the world economy caused substantial job losses in German regions specialized in import-competing industries, both in manufacturing and beyond. Regions specialized in export-oriented industries, however, experienced even stronger employment gains and lower unemployment." (Abstract)

> "In the aggregate, we estimate that this trade integration has caused some 442,000 additional jobs in the economy and contributed to retaining the manufacturing sector in Germany." (Abstract)

> "Consistent with the US experience, we also find a negative *causal* effect of import exposure from the East... Yet, this negative impact is, on average, more than offset by a positive *causal* effect of export exposure, as the respective export oriented regions built up manufacturing employment as a result of the new market opportunities." (Section 1)

> "This is almost exclusively driven by the rise of Eastern Europe, not by China." (Abstract)

---

## 6. 본 연구 paper 의 DFS 인용 위치

### Section 1 (Introduction) — Top tier
- ADH 2013 → Pierce-Schott 2020 → Finkelstein 2026 (US sequence)
- **DFS 2014 (Germany) → 본 연구 (Korea)** = export-driven sequence
- **본 연구는 DFS 의 mortality 버전**

### Section 2 (Background)
- 한국 무역 history (1988+ 독일 East trade 와 유사 timing)
- 한국 export 산업의 성장 (1990 자동차, 2000 반도체)

### Section 3 (Methodology)
- DFS 의 import-export 분리 IV 직접 차용
- 본 연구 KR-CN bilateral 50 files = DFS 의 East trade 와 mirror

### Section 4 (Main Results)
- β_M, β_X 분리 표 (DFS Table 2 와 mirror)
- "Net protective effect" 직접 비교

### Section 6 (Discussion)
- 한국 vs 독일 = export-driven 의 mortality 보호효과 → globalization 의 distributional effect 재평가
- Pierce-Schott / Finkelstein 의 "trade kills" narrative 의 한계

---

## 7. 본 연구의 contribution clarified

**본 연구의 4가지 unique contribution:**

1. **DFS 의 mortality version** ⭐⭐⭐
   - DFS 가 employment 만 본 것을 mortality 로 확장
   - Export-driven 경제의 health protective effect 직접 검증

2. **Pierce-Schott 의 한국판 (with reverse direction)**
   - PSc 가 PNTR mortality 증가 → 본 연구는 KR-CN export → 보호효과
   - Mechanism 비교 (HIRA 약물 데이터 추가)

3. **Finkelstein 2026 framework 의 한국 적용**
   - β_m vs β_n decomposition
   - Manufacturing 안정성의 mortality 보호효과

4. **Sufi 2023 와 결합**
   - Trade × Household debt interaction
   - 한국 specific (가계부채 boom 동시기)

→ 본 연구가 **4개 framework 통합** 의 한국 케이스. 박사논문 contribution 분명.

---

## 8. DFS 후속 paper 들 (이미 md/ 에 있음)

- **dp10469.md** (DFS 2017 IZA): "Trade and Manufacturing Jobs in Germany" — 후속 update
- **dp11299.md** (DFS 2018 IZA): "Adjusting to Globalization in Germany" — adjustment 분석

이 둘도 추후 read 가치. 본 연구의 DFS reference 강화.

---

## 9. 다음 단계 메모

1. **Phase 3 IV 구성** 시 DFS 의 import-export 분리 specification 직접 차용
2. **Comtrade KR-CN bilateral** 50 files 가 DFS framework 에 정확히 맞음 (수출입 양방향)
3. **β_M, β_X 분리 표** 가 본 연구 main result
4. **Eastern Europe vs China 분리** 처럼, 본 연구는 **중국 vs 일본/대만/미국** 분리도 가능 (Comtrade ADH 8국 이용)

---

## 10. 본 연구 narrative 의 최종 정리

```
1990s-2000s globalization era 의 mortality 영향:

미국 (Pierce-Schott + Finkelstein + Case-Deaton):
  PNTR/NAFTA → manufacturing job loss → deaths of despair ↑
  특히 백인 working-age, drug overdose dominant

독일 (Dauth-Findeisen-Suedekum):
  East trade → employment net 증가 (+442k)
  Manufacturing 유지, mortality 영향 미연구

한국 (본 연구):
  KR-CN trade → employment 안정/증가 (export-driven)
  Mortality protective effect 가설
  자살 (102) main outcome (한국 OECD top)
  HIRA mechanism 직접 검증
  가계부채 (Sufi 2023) interaction
```

→ **본 연구가 globalization-mortality literature 의 가장 중요한 missing case (Korea)** 채움.
