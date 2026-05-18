# Case-Deaton 2015 (PNAS) — 본 연구 적용 노트

**원논문:** Case, A. & Deaton, A. (2015). "Rising morbidity and mortality in midlife among white non-Hispanic Americans in the 21st century." *Proceedings of the National Academy of Sciences* 112(49): 15078-15083.

**작성:** 2026-05-01 (본 연구의 outcome 변수 정의의 직접 근거)

---

## 1. Big Picture — Deaths of Despair 의 정의 원조

이 paper 는 **"deaths of despair"** 라는 용어와 outcome 정의의 표준. 본 연구의 outcome group `despair_total` (코드 102 + 101 + 057 + 081) 의 학술적 근거가 바로 여기에서 나옴.

### Core finding

> 1999-2013 미국 **45-54세 백인 non-Hispanic** 의 사망률 **연간 0.5% 증가** (다른 부유국은 -2% 계속 감소)
> 다른 인종 (흑인·히스패닉) 과 노인 (65+) 은 계속 감소

→ **20세기 후반의 mortality decline 추세를 뒤집은 사건**. OECD 다른 어느 나라에도 없음.

### Cause of reversal

세 가지 사인이 dominant:
1. **Drug & alcohol poisoning** (의도적·불의·미상)
2. **Suicide**
3. **Chronic liver diseases and cirrhosis**

→ **이 셋이 "deaths of despair"** 의 정의

추가:
- 모든 education 그룹에서 증가
- **저학력 그룹** 에서 가장 큰 증가
- 자가보고 정신건강·만성통증·일상생활 능력 저하 동반

---

## 2. Outcome 변수 정의 (본 연구 채택)

### Case-Deaton 2015 의 정확한 정의
| 사인 | ICD-10 | 본 연구 코드 |
|------|--------|--------------|
| Drug poisoning (accidental + intent undetermined) | X40-X44, Y10-Y14 | 코드 101 (X40-X49) + 057 (F10-F19) |
| Alcohol poisoning | X45, Y15 | 코드 057 의 알코올 부분 |
| Suicide | X60-X84, Y87.0 | **코드 102** ⭐ |
| Chronic liver disease & cirrhosis | K70 (alcoholic), K73-K74 | 코드 081 (간 질환 통합) |

### 본 연구의 한국 매핑 (이미 1_codebooks/kosis_104_to_icd10.yaml 에 정의)
```yaml
despair_total:
 - 102 # 자살 (X60-X84)
 - 101 # 약물 중독 (X40-X49)
 - 057 # 정신활성물질 (F10-F19)
 - 081 # 간 질환 (K70-K77)
```

### 본 연구의 한계 — F17 담배 처리

Case-Deaton **명시적 제외**: tobacco-related deaths
한국 microdata 한계: 코드 057 안에 F10-F19 통합 → F17 (담배) 분리 불가

→ paper 의 limitation 으로 명시:
- Main: 코드 102 + 101 + 057 + 081 (담배 포함)
- Sensitivity: 코드 101 + 081 만 (담배 제외) → 비교

---

## 3. Mechanism — Case-Deaton 의 가설

### 1. Opioid epidemic (1996+ Oxycontin)
- 1996 Oxycontin 출시 → 처방 increasingly available
- 처방 약물 → 헤로인 substitution
- "epidemic of pain" 처방·복용 패턴 변화

### 2. 누적된 사회경제적 disadvantage (Case-Deaton 2017)
- **저학력 (HS or less)** 그룹의 cumulative disadvantage
- 직업 prospect 악화 + 임금 정체 + 결혼 시장 약화 + 사회적 자본 감소

### 3. 정신건강·만성통증·약물의존 cycle
- 자가보고 정신건강 declining
- 만성통증 increasing
- 일상생활 능력 declining
- 약물의존 + 통증 + 정신건강 → 사망

---

## 4. 본 연구 (Trade × Mortality Korea) 적용

### A. Outcome 정의의 학술적 근거

본 연구의 5가지 outcome group:
```
despair_total = 102 + 101 + 057 + 081 ← Case-Deaton 정의 ⭐
cardiovascular = 067-070
cancer = 027-048
respiratory = 073-078
external_other = 097-104 minus 102
```

`despair_total` 이 **Case-Deaton 2015 정의의 한국판** 임을 paper 에 명시.

### B. 한국 vs 미국 비교 — 본 연구의 contribution

| Case-Deaton 미국 | 한국 (예상) |
|-----------------|------------|
| 1999+ midlife 백인 mortality ↑ | 한국 자살률 1997 IMF 위기 후 OECD top |
| Drug overdose dominant (Oxycontin) | **자살 dominant** (102) — 약물 약함 |
| Alcoholic liver disease 증가 | 한국 간질환 (081) 통합 — 알코올 분리 어려움 |
| Suicide 부차적 (US) | **Suicide main outcome** (Korea) ⭐ |
| 백인 working-age | 한국은 race split 없음 (homogeneous) |
| 저학력 그룹 affected | 한국 자영업·제조업 직군 비교 |

### C. 본 연구의 narrative — Case-Deaton 차용 + 변형

**Case-Deaton:** "미국 백인 노동계층의 누적 disadvantage → deaths of despair 증가"

**본 연구:** "한국 export-driven 무역구조 → manufacturing 안정 → deaths of despair (특히 자살) 의 protective effect 또는 무영향"

→ **direction 정반대** 가설:
- 한국 self-employed buffer
- 한국 export-driven manufacturing 안정성
- 한국 자살이 다른 mechanism (사회적 압력, 정신건강 인프라 부족)

### D. 한국 자살 (102) 의 특수성

**OECD 자살률 통계:**
- 한국 자살률: 2010 33.5/100k, 2020 25.7/100k
- 미국 자살률: 14/100k (2020)
- 한국이 OECD 1-2위 지속

**원인 (한국 specific):**
- IMF 위기 (1997) 후 자살률 급등
- 노인 빈곤 (OECD 최고)
- 사회 압력 (학업·직장)
- 정신건강 인프라 부족

→ 본 연구의 **"trade shock 이 한국 자살에 미치는 효과"** 는 미국과 다른 mechanism 으로 해석.

### E. 본 연구의 paper narrative 위치

**Section 1 (Introduction):**
- Case-Deaton 2015 → Pierce-Schott 2020 → Finkelstein 2026 흐름
- "deaths of despair" 가 미국 phenomenon → 한국 적용 의의

**Section 2 (Background):**
- Korea 자살률 OECD top 의 역사
- 한국 deaths of despair 정의의 한계 (F17 등)
- IMF 위기 (1997) → 자살률 급등 (Phase 4 의 1997 baseline 의 의미)

**Section 4 (Main Results):**
- 자살 (102) 효과 → Case-Deaton 의 미국 자살 mortality 증가 와 비교
- Drug-related (101 + 057) → Pierce-Schott / Case-Deaton 비교
- 알코올성 간질환 (081) → Case-Deaton 의 ARLD 비교

**Section 7 (Discussion):**
- 한국 deaths of despair = 미국과 다른 channel
- "Hidden protective effect" framework

---

## 5. 핵심 인용구

> "The increase in midlife mortality of US white non-Hispanics... was largely accounted for by increasing death rates from drug and alcohol poisonings, suicide, and chronic liver diseases and cirrhosis." (Abstract)

> "Although all education groups saw increases in mortality from suicide and poisonings, and an overall increase in external cause mortality, those with less education saw the most marked increases." (Abstract)

> "From 1978 to 1998, the mortality rate for US whites aged 45–54 fell by 2% per year on average... After 1998, US white non-Hispanic mortality rose by half a percent a year. No other rich country saw a similar turnaround." (Section: Midlife Mortality)

> "The increased availability of opioid prescriptions for pain that began in the late 1990s has been widely noted, as has the associated mortality... For each prescription painkiller death in 2008, there were 10 treatment admissions for abuse, 32 emergency department visits..." (Discussion)

---

## 6. 본 연구의 outcome group 검증

본 연구가 수집한 데이터로 **한국 deaths of despair 시계열** 그릴 수 있는지:

```python
# Phase 2-A 의 출력 mortality_panel 에서:
df_panel.groupby("year")[
 ["mort_102_suicide", "mort_101_drug", "mort_057_substance", "mort_081_liver"]
].mean.plot
```

기대:
- 1997 IMF 위기 후 자살률 급등
- 2003-2010 자살률 정점
- 2010-2020 자살률 점차 감소 (정부 개입)
- 약물·간질환은 미국보다 훨씬 낮을 것

→ 이 시계열이 Case-Deaton 의 미국 그래프 (Figure 1) 와 직접 비교 가능. paper 에 그림 1로 사용.

---

## 7. 다음 단계 메모

1. Phase 2-A 사망률 panel 빌드 시 **outcome group별 시계열 그림** 우선 생성
2. **자살 (102) 시계열** 1997-2023 → KOSTAT 공식과 비교 (이미 4년치 검증됨)
3. **광역시 vs 도** 자살률 차이 → 본 연구의 heterogeneity 의 첫 결과
4. paper Figure 1 = 한국 deaths of despair 시계열 (Case-Deaton Fig.1 mirror)

---

## 8. Case-Deaton 후속 paper

추후 read 가치:
- **Case-Deaton 2017** (Brookings Papers): "cumulative disadvantage" 가설
- **Case-Deaton 2020 book** "Deaths of Despair and the Future of Capitalism": 종합본
- **Case-Deaton 2021 PNAS**: COVID 후 추가 deaths

본 연구의 narrative 가 Case-Deaton 의 framework 를 한국 export-driven 컨텍스트로 변형 → **본 연구의 international perspective contribution**.
