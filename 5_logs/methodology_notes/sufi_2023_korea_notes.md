# Sufi 2023 BFI (Korea + China) — 본 연구 적용 노트

**원논문:** Sufi, A. (2023). "Housing, Household Debt, and the Business Cycle: An Application to China and Korea." *BFI Working Paper 2023-109*.

**작성:** 2026-05-01 (본 연구의 한국 거시 backdrop + Phase 2-C 컨트롤 설계)

---

## 1. Big Picture — 한국 거시 backdrop 의 핵심 reference

이 paper 는 **Mian-Sufi-Verner credit-driven household demand channel** 의 한국·중국 적용. 본 연구의 거시 컨트롤 변수 (가계대출, 연체율) 의 학술적 정당성 + 한국 specific 통찰.

### Core thesis

> **가계부채 medium-run 증가 → boom-bust pattern**
> "credit-driven household demand channel" (Mian-Sufi 2018)
> 
> 한국 + 중국 (2015-2021): 23pp household debt-to-GDP 증가
> → 미국/영국 2001-2007 boom 과 비슷한 magnitude
> → 미래 consumer spending 약화 예상

---

## 2. 한국 specific 발견

### 한국 가계부채 boom (2015-2021)
- 23 percentage points 증가 (debt-to-GDP)
- 미국/영국 2001-2007 (Great Recession 직전) 와 비슷한 크기
- 부동산 가격 boom 동반

### 한국의 risk 평가
| 항목 | 평가 |
|------|------|
| 금융위기 risk | 낮음 (currrent account 흑자) |
| Banking system | 안정적 |
| **Consumer spending** | **약화 예상** (debt overhang) |
| 부동산 시장 | downturn 진행 중 |

### 본 연구 panel 기간 와의 일치
- Sufi 2023 분석 기간: 2015-2021 (한국 가계부채 boom)
- 본 연구 panel: 1997-2023
- → 본 연구의 panel **마지막 8년** 이 가계부채 boom 시기와 정확히 겹침
- → Phase 4 회귀에서 **가계대출 control** 의 중요성 직접 정당화

---

## 3. 본 연구 (Trade × Mortality Korea) 적용

### A. Phase 2-C 거시 컨트롤 변수의 학술적 근거

본 연구의 ECOS 16개 통계표 중 가계부채 관련 5개:
```
141Y005 — 예금은행 지역별 연체율 (시도, 월)
151Y002 — 가계대출 (업권별)
151Y003 — 예금은행 지역별 가계대출 잔액
151Y005 — 가계대출 (용도별)
151Y006 — 비은행 지역별 가계대출
```

**Sufi 2023 의 channel 직접 차용:**
- 가계부채 ↑ → 일정 시점 후 consumer spending ↓ (Mian-Sufi-Verner 2017)
- 본 연구: 무역 충격 + 가계부채 → 사망률에 영향 (interaction)

### B. 본 연구의 추가 hypothesis

**Trade × Household debt interaction:**
- 무역 충격이 **고가계부채 지역** 에서 더 강한 mortality 영향
- 가계부채 stress + 일자리 감소 → "doubled down" mental health/economic stress

**Specification 추가:**
```
ln(MortRate)_{ct} = β_1 × Bartik_c + β_2 × HHDebt_{ct} 
 + β_3 × (Bartik_c × HHDebt_{ct})
 + α_c + τ_t + X_{ct}φ + ε
```

→ β_3 가 유의 → "Sufi channel" 확인

### C. 본 연구의 Korea-specific narrative

**Sufi 2023 의 발견 + 본 연구 contribution:**

```
1. 한국 가계부채 boom (2015-2021) — Sufi 2023 documents
2. 동시기 한국 자살률 (102) trend — 본 연구 documents
3. Trade shock × HHDebt interaction — 본 연구 newly tests
4. Mechanism: 무역 + 부채 → 정신건강 → 자살
```

→ Sufi 2023 + Pierce-Schott 2020 + Finkelstein 2026 의 **세 framework 통합**.

### D. Phase 2-C 거시 컨트롤 panel 설계

**시도 단위 panel** (17 sido × 17년):
- 가계대출 잔액 (151Y003)
- 연체율 (141Y005)
- → broadcast to 시군구 (자치구가 같은 sido 내)

**전국 시계열** (시간 변동):
- 기준금리 (722Y001)
- 환율 (731Y004)
- M2 (161Y006)
- CPI (901Y009)
- → 시간 fixed effects 안에 흡수, 또는 별도 시간변동 컨트롤

### E. Sufi 2023 인용 위치

**Section 2 (Background):**
- 한국 거시 환경 (가계부채 boom)
- Mian-Sufi-Verner 2017 channel
- 본 연구의 panel 기간 (1997-2023) 의 거시 사건 (1997 IMF, 2008 Recession, 2015+ 가계부채 boom, 2020 COVID)

**Section 5 (Mechanism):**
- Trade shock × HHDebt interaction 결과
- 가계부채 가 mortality channel 의 amplifier

**Section 7 (Discussion):**
- 미래 한국 mortality 전망 (Sufi 2023 의 weakening consumer spending 시나리오)

---

## 4. 핵심 인용구

> "China and South Korea both experienced substantial increases in household debt through 2021, and now both countries face a weakening economy." (Abstract)

> "On the positive side, neither country is at risk of a severe financial crisis... On the negative side, consumer spending in both countries could be quite weak in the years ahead." (Abstract)

> "The 23 percentage point rise in the household debt to GDP is smaller than some of the largest booms prior to the Great Recession, but the Chinese and Korean booms are comparable with the booms that occurred in the United States and United Kingdom from 2001 to 2007." (Section: Debt Booms)

---

## 5. 본 연구의 unique contribution (Sufi 2023 후속)

**Sufi 2023 의 한계:**
- 한국 거시 (aggregate) 만 분석
- 사망률·건강 outcome 미고려
- 시군구 단위 spatial heterogeneity 미사용

**본 연구의 확장:**
1. **시군구 단위** spatial heterogeneity (Sufi 의 macro 보다 정밀)
2. **Mortality outcome** (Sufi 가 못 한 health channel)
3. **Trade × HHDebt interaction** (Sufi 의 channel 연구를 microdata 로 확장)
4. **HIRA mechanism** (정신건강 약물 처방 → Sufi 의 macro 가 못 본 직접 mechanism)

---

## 6. 본 연구 paper 의 narrative 강화

### 기존 narrative
"무역 충격 → 한국 시군구 사망률 (Hidden protective effect 일 가능성)"

### Sufi 2023 결합 narrative
"무역 충격 + 가계부채 → 한국 시군구 사망률에 미치는 효과:
1. 무역 main effect: protective (export-driven)
2. 가계부채 main effect: detrimental (Sufi channel)
3. Interaction: 부채 high 지역에서 무역 보호효과 약화

→ 한국 정책 implication: 가계부채 관리가 trade-related health outcome 에 직접 영향"

→ paper 의 **policy relevance** 대폭 강화. 박사논문급 narrative.

---

## 7. 다음 단계 메모

1. **Phase 2-C 거시 컨트롤 panel** 빌드 시 ECOS 5개 가계부채 통계표를 sido level 로 정리
2. **Trade × HHDebt interaction** 항 추가 specification 준비
3. **Mian-Sufi-Verner 2017** (mian-s5.md) 다음에 read 권장 — 더 디테일한 channel 분석
4. **Phase 5 mechanism** 시 Sufi channel + Pierce-Schott opioid channel 비교

---

## 8. 본 연구 narrative 의 학술적 lineage

```
Trade shock 분석:
├── ADH 2013 (China shock baseline)
├── Pierce-Schott 2020 (PNTR mortality)
├── Finkelstein 2026 (NAFTA + general framework)
└── 본 연구 (Korea export-driven)

Deaths of despair:
├── Case-Deaton 2015 (정의)
├── Pierce-Schott 2020 (drug overdose)
└── 본 연구 (Korea suicide-dominant)

Household debt:
├── Mian-Sufi-Verner 2017 (channel)
├── Mian-Sufi 2018 (revised)
├── Sufi 2023 (Korea/China)
└── 본 연구 (sigungu-level interaction)

Methodology:
├── ADH 2013 → Goldsmith-Pinkham 2018 → BHJ 2022/2025
├── Adão-Kolesár-Morales 2019 (AKM SE)
├── Andrews-Stock-Sun 2019 (weak IV)
└── 본 연구 (5-layer SE 통합)
```

본 연구가 **4개 독립 literature 의 교차점** 에 위치. Contribution 분명.
