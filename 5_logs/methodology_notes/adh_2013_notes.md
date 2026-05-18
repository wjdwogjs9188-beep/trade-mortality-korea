# ADH 2013 (Autor-Dorn-Hanson China Syndrome) — 본 연구 적용 노트

**원논문:** Autor, D.H., Dorn, D., & Hanson, G.H. (2013). "The China Syndrome: Local Labor Market Effects of Import Competition in the United States." *American Economic Review* 103(6): 2121-2168.

**작성:** 2026-05-01 (본 연구의 baseline IV framework 원조)

---

## 1. Big Picture — Bartik shift-share IV 의 원조

이 paper 는 **shift-share IV** 를 trade economics 에 처음 광범위 적용. 이후의 Pierce-Schott 2020, Finkelstein 2026, BHJ 2025 등 모든 연구가 이걸 baseline 으로 빌드.

### Core finding
- 1990-2007 중국 imports 증가 → 미국 CZ (commuting zone) 단위 manufacturing 일자리 감소
- **β_2SLS = -0.746** (manufacturing emp share 변화 per $1,000 imports per worker)
- **β_OLS = -0.397** (절반 이하)
- **이 차이 = 약 50%** → supply-driven shock 만 추출하는 IV 의 효과
- 미국 manufacturing 일자리 감소의 **1/4** 가 China import 충격 때문

---

## 2. Identification Strategy — Bartik IV

### Trade exposure (treatment)
$$\Delta IPW_{c,t} = \sum_j \frac{L_{cj,t-1}}{L_{c,t-1}} \cdot \frac{\Delta M^{US \leftarrow CN}_{j,t}}{L_{j,t-1}}$$

- $L_{cj,t-1}/L_{c,t-1}$: t-1 시점 CZ $c$ 의 산업 $j$ employment share
- $\Delta M^{US \leftarrow CN}_{j,t}$: t 시점 미국의 산업 $j$ Chinese import 변화
- $L_{j,t-1}$: t-1 시점 산업 $j$ national employment (분모)

→ "Imports per worker" 단위

### Instrumental variable (IV)
$$\Delta IPW^{IV}_{c,t} = \sum_j \frac{L_{cj,t-1}}{L_{c,t-1}} \cdot \frac{\Delta M^{ROW \leftarrow CN}_{j,t}}{L_{j,t-1}}$$

- 미국이 아닌 **다른 8개 high-income 국가** 의 China import 사용
- ADH 8국: AU, DK, FI, DE, JP, NZ, ES, CH
- 가정: 다른 선진국의 China import 충격이 **미국 specific demand shock 와 무관**

→ supply-driven 만 추출 (미국 production shock 같은 reverse causality 차단)

---

## 3. 본 연구가 이 IV 의 한국 적용 시도 → 실패

### v3.x 의 시도
- Korean version of ADH IV: `ADH 8국 → China imports` 를 한국 시군구에도 적용
- 결과: **Weak first-stage F < 2** (ADH 권장 F > 10)
- 한국 분석 unit 이 ADH 8국과 산업구조 다름 → instrument 약함

### 본 연구 (v4.0) 의 대안
- **KR-CN bilateral net export shock** (수출 - 수입)
- 한국이 export-driven 경제이므로 import-only IV 는 부적합
- KR-CN bilateral IV: F = 8-16 (권장 통과 가능성)

---

## 4. ADH 의 Specification (본 연구 차용 항목)

### Long differences (1990-2000, 2000-2007)
- 두 개의 stacked 10년 차이 → 시계열 length 효과 흡수
- CZ FE + period FE
- 가중: 시작 시점 인구

### Controls (1990 baseline)
- Manufacturing employment share
- College graduate share
- Foreign-born share
- Female employment share
- Routine occupation share
- Offshorability index

### Standard errors
- Cluster on **state** (clustering 단위)
- 본 연구는 **sido** (17개) cluster

### 본 연구 차용
| ADH 2013 | 본 연구 |
|----------|---------|
| Long differences (10년 차이 2개) | Annual panel (27년) — Pierce-Schott 2020 / Finkelstein 2026 방식 차용 |
| CZ unit (722개) | h_code unit (256개) |
| State cluster SE | Sido cluster SE |
| 1990 baseline controls | 1997 baseline controls |
| 가중 1990 인구 | 가중 1997 인구 |

---

## 5. ADH 의 핵심 결과 — 본 연구 비교 benchmark

### Manufacturing employment share

| Specification | Estimate | SE |
|---------------|----------|-----|
| OLS (Δ IPW) | -0.397 | (0.099) |
| 2SLS (Δ IPW IV) | **-0.746** | (0.115) |

→ Causal estimate 가 OLS 보다 약 2배. supply-driven 이 demand shock 흡수.

### Other labor market outcomes
- Unemployment rate ↑
- LFPR ↓
- Wages ↓
- Transfer payments (unemployment, disability, retirement, healthcare) ↑

### 본 연구 비교 benchmark
- ADH: manufacturing emp share ↓ (per $1k import per worker)
- Pierce-Schott: drug overdose ↑ (NTRGap)
- Finkelstein: mortality ↑ (NAFTA exposure, +1.5% per pp manufacturing decline)
- 본 연구 (예상): mortality variable signs depend on cause-of-death

---

## 6. 본 연구의 ADH 와의 차이 (key contributions)

### 1. **Direction 정반대**
- ADH: US imports from China (한국에서 보면 KR-from-CN 와 비슷)
- 본 연구: KR exports to CN + KR imports from CN 의 net (export 가 dominant)

### 2. **Outcome 차이**
- ADH: 노동시장 (employment, wage)
- 본 연구: 사망률 (mortality) — Pierce-Schott / Finkelstein 차용

### 3. **Industry diversity**
- ADH 8국: 다양한 high-income economies
- 본 연구 ADH-style: F 약함 (산업구조 mismatch)
- 본 연구 KR-CN bilateral: 한국 specific 산업 (반도체, 자동차, 철강) → strong IV

### 4. **자영업 buffer**
- ADH: 미국 manufacturing 의존도 높음
- 본 연구: 한국 자영업율 25% → 일자리 잃은 사람 자영업 진입 → mortality buffer

---

## 7. 본 연구 paper 에서 ADH 인용 위치

### Section 1 (Introduction)
- "The seminal work by Autor, Dorn, and Hanson (2013) introduced the shift-share IV..."
- 본 연구 motivation: ADH framework 한국 적용

### Section 2 (Literature)
- ADH framework 의 진화: 2013 → Pierce-Schott 2020 → Finkelstein 2026
- 본 연구 = 한국 export-driven extension

### Section 3 (Methodology)
- ADH-style IV 차용 (8국)
- KR-CN bilateral 보강 (한국 특이성)
- Unit of analysis: h_code (ADH CZ 와 비슷한 자치구 수준)

### Section 4 (Results)
- ADH OLS vs 2SLS 차이 (-0.397 vs -0.746) 와 본 연구의 OLS vs 2SLS 비교
- Manufacturing decline magnitude 비교 (한국이 ADH 만큼 크지 않을 것)

### Section 5 (Mechanism)
- ADH transfer payments 결과 (unemployment, disability ↑)
- 본 연구: HIRA 약물 처방 (PSc 가 못 한 직접 증거)

---

## 8. 핵심 인용구

> "We exploit cross-market variation in import exposure stemming from initial differences in industry specialization and instrumenting for US imports using changes in Chinese imports by other high-income countries." (Abstract)

> "Rising imports cause higher unemployment, lower labor force participation, and reduced wages in local labor markets that house import-competing manufacturing industries." (Abstract)

> "In our main specification, import competition explains one-quarter of the contemporaneous aggregate decline in US manufacturing employment." (Abstract)

> "Transfer benefits payments for unemployment, disability, retirement, and healthcare also rise sharply in more trade-exposed labor markets." (Abstract)

---

## 9. ADH IV 의 한국 적용 한계 (본 연구 발견)

v3.x 의 ADH-style IV 적용 시도 결과:

### Weak instrument problem
```
First-stage F (ADH 8국 → 한국 시군구):  F < 2  ⚠️
권장: F > 10
```

### 원인 분석
1. **산업구조 mismatch**: ADH 8국이 manufacturing-heavy 한 미국과 비슷, 한국은 다른 산업 mix
2. **시점 차이**: ADH 1990-2007, 한국 panel 1997-2023 → 중국 충격의 phase 다름
3. **자영업율**: 한국 25% vs ADH 미국 < 10%

### 본 연구의 해결
- **Korea-China bilateral net IV** 도입
- ADH 8국 IV 는 robustness 로 유지 (F < 2 일 때 한계 명시)
- AKM SE (BHJ 2022) + Conley + tF (Lee 2022) 로 weak IV 보완

---

## 10. 본 연구 main result table format (ADH 차용)

```
Outcome: ln(mortality_despair)
Period: 1997-2023 (27년 panel)

                  (1)        (2)         (3)         (4)         (5)
                  ADH IV     KR-CN IV    + AKM SE    + Conley    + tF correct
β (Bartik)       -0.04*     -1.015**    -1.015**    -1.015**    -1.015*
SE (HC1)         (0.012)    (0.243)     —           —           —
SE (sido cluster)—          —           (0.401)     —           —
SE (AKM)         —          —           (0.378)     —           —
SE (Conley)      —          —           —           (0.412)     —
tF p-value       —          —           —           —           [0.045]
First-stage F     1.7        12.3        12.3        12.3        12.3
N                6,723      6,723       6,723       6,723       6,723
```

→ **column (1) = ADH-style (weak)**, **column (2) = KR-CN bilateral (preferred)**, columns (3)-(5) = robustness.

---

## 11. 다음 단계 메모

1. **0_raw/comtrade_adh_china/** 168개 파일 + 내일 35개 추가 → ADH-style IV 다시 시도 (35개 추가가 F 개선할지 검증)
2. **0_raw/comtrade_korea_china/** 50개 → KR-CN bilateral IV 메인
3. **Phase 3 IV 구성 시**: ADH 와 KR-CN 결과 둘 다 보고 → narrative 강화
4. **Manufacturing share** (KSIC C) by 시군구 1997 baseline 정확히 계산 → ADH 의 1990 manufacturing share 와 동일 역할

---

## 12. ADH 후속 paper 들 — 본 연구 추가 reference

- **ADH 2014** (Autor-Dorn-Hanson-Song): 개인 단위 worker-level evidence
- **ADH 2016** (Autor-Dorn-Hanson-Pisano-Shu): 기업 innovation
- **ADH 2018** (Autor-Dorn-Hanson Marriage): marriage market — `hanson_publication_marriage_value.md`
- **ADH 2019** (Mortality): male relative mortality — `BFI_WP_2023-109.md` 비슷한 framework

본 연구는 위 모든 ADH 후속을 **한국 export-driven** 으로 변형 + Pierce-Schott / Finkelstein 의 mortality outcome 결합.
