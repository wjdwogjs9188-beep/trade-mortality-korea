# Reviewer Feedback Template

**Reviewer 정보**:
- 이름: ________________________
- 소속: ________________________
- 검토 시점: ________________________
- 검토 시간 투자: ________________ 시간

---

## 0. Overall Assessment

체크 (해당 1):
- [ ] **Ready to publish (SSCI submission 가능)** — 학술적 엄밀성 + novelty + 데이터 모두 충분
- [ ] **Major revision before publish** — 핵심 framework 또는 데이터 issue 보완 필요
- [ ] **Minor revision** — refining 만 필요, 기본 framework + finding 견고
- [ ] **Stage 5 진입 후 재평가** — 현재 Stage 4 미완 상태로 평가 보류

자유 코멘트 (overall):
```
[reviewer 자유 작성]
```

---

## 1. Methodology Review

### 1.1 Identification (PAP § 5)

**Bartik shift-share IV (PAP § 5.1)**:
- Identification 가정 명시 충분? (share exogeneity vs shock exogeneity, GPSS 2020 framework)
- First-stage spec 의 weak IV 진단 (OP test F=23.1) 적절?
- ADH 2013 + Pierce-Schott 2020 의 한국 적용 spec 정합성?

코멘트:
```
[reviewer]
```

**DGHP 2017 + DFH 2020 mediation (PAP § 5.2)**:
- ivmediate Stata package spec 적절? (theoretical framework + implementation source 모두 cite)
- Direct/indirect effect 분해의 instrument set (z_x, z_m) 정합성?
- Family channel mediator (혼인 + 교육) 의 한국 first 적용 contribution claim 충분?

코멘트:
```
[reviewer]
```

### 1.2 Empirical Spec (PAP § 6)

**5-year stacked first-difference (Pierce-Schott 2020 base)**:
- period 매핑 (1997-2001 → 2000 census, ..., 2017-2021 → 2020) timing 가정 적절?
- 2022-2024 incomplete period drop reasoning 충분?

코멘트:
```
[reviewer]
```

### 1.3 5-layer SE (PAP § 7)

| Layer | method | reference | over-engineering? |
|-------|--------|-----------|-------------------|
| 1 | HC1 | textbook | [reviewer 평가] |
| 2 | WCB-sigungu (229) | Cameron-Gelbach-Miller 2008 | |
| 3 | WCB-sido (16) | 동일 | |
| 4 | AKM | BHJ 2022 + GPSS 2020 | |
| 5 | Conley | Conley 1999 | |
| 6 | OP test (F=23.1) | Olea-Pflueger 2013 + Stock-Yogo 2005 | |
| 7 | AR + tF | Andrews-Stock-Sun 2019 + Staiger-Stock 1994 | |

전체 5-7 layer 의 over-engineering 여부:
```
[reviewer]
```

### 1.4 Romano-Wolf step-down (PAP § 7.6)

Family of hypotheses 정의:
- 옵션 A: 4 outcome (자살 + 약물 + 정신 + 간) only = 4 hypotheses
- 옵션 B: 4 outcome × 2 mediator dim (marital + education) = 8 hypotheses
- 옵션 C: 옵션 B + all_cause = 9 hypotheses

권장 옵션 + 이유:
```
[reviewer]
```

---

## 2. Data Quality Review

### 2.1 Mediator Panel

**Education 3 카테고리** (NoHS / HS / College+):
- 1997-2007 의 5=대학통합 vs 2008+ 의 6=4년제/7=대학원 매핑 적절?
- 정보 손실 (전문대 vs 4년제) 의 main analysis 영향?

코멘트:
```
[reviewer]
```

**denom missing 9.74% (marital panel)**:
- 67 h_code (mortality 346 - mediator 279) 의 origin 진단 권장?
- Stage 5 listwise deletion 의 bias direction?

코멘트:
```
[reviewer]
```

### 2.2 Mortality Microdata

**1997-2007 외국인 식별 불가** (변수 부재):
- Numerator 미세 inflation (< 0.5% 추정) 의 main result 영향?
- Caveat 추가 위치 (PAP § 8) 적절?

코멘트:
```
[reviewer]
```

**Sigungu_crosswalk_v2 적용 후 229 h_code**:
- Mortality_panel_v02_1 와 align 정합성?
- 안산 31090 (R-A audit 정정) verify 충분?

코멘트:
```
[reviewer]
```

### 2.3 외국인 빼기 over-correction (PAP § 8 #22)

Stage 3B v02.1 의 -0.35% 차이 reasoning:
- panel v01 자체가 한국인 only (KOSIS DT_1B040M5 = 행안부 한국인 only -0.35% 차이)
- 외국인 빼기 = double-counting → over-correction (+1.48% inflation)
- v02.1 = 외국인 빼기 제거 = 정확

Reasoning sufficient?:
```
[reviewer]
```

---

## 3. Novelty Position

### 3.1 한국 = 자살 + 간 vs US = 약물 dominance

| outcome | 한국 (paper period 5) | US (Pierce-Schott 2020) |
|---------|----------------------|-------------------------|
| 자살 | 29.61 / 100K | 14 / 100K |
| 간질환 | 19.05 / 100K | (Pierce-Schott NS) |
| 약물 | 3.86 / 100K | 50+ / 100K (peak) |

Mechanism 가설:
- 한국 = stoic culture + 자살 stigma 낮음 + 알코올 culture (간)
- US = opioid epidemic + 가족 해체 channel

가설 narrative 충분:
```
[reviewer]
```

### 3.2 Family channel novelty

Hanson (2018) marriage value paper 의 한국 확장:
- Hanson = US marriage market value decline 의 ecological evidence
- 본 paper = individual-level death microdata 의 marital_code × cause cross-tab → mediator-specific rate
- DGHP 2017 + DFH 2020 ivmediate framework 한국 first 적용

Novelty claim 충분:
```
[reviewer]
```

---

## 4. Reference Citation Accuracy

### 4.1 본 conversation 정정 3 issue (reference proposal v01.1)

| issue | 정정 내용 |
|-------|----------|
| 1 | GPSS 2018 NBER → 2020 AER 110(8) primary |
| 2 | DGHP 2017 (theoretical) + DFH 2020 Stata Journal 20(3) (implementation) 둘 다 cite |
| 3 | OP test F=23.1 = 5% TSLS bias (NOT size distortion) |

추가 inaccuracy 발견 시 명시:
```
[reviewer]
```

### 4.2 Reference list 26 entry (proposal v01.1 § 8.1)

빠진 reference 또는 잘못된 attribution:
```
[reviewer]
```

---

## 5. Stage 5 Readiness

### 5.1 Pending 4 항

| pending | severity | 우선순위 |
|---------|----------|----------|
| Stage 4 Comtrade + HS-KSIC concordance | 🔴 critical | [reviewer 평가] |
| denom missing 67 h_code 진단 | 🟡 medium | |
| Stata 환경 verify (7 package) | 🟡 medium | |
| PAP v3.4 → v3.5 (reference proposal v01.1 적용) | 🟢 low | |

권장 처리 순서:
```
[reviewer]
```

### 5.2 Stage 5 진입 시 추가 권고

Stata implementation 시 주의사항 (예: ivmediate package version, weakivtest cutoff 정확화, rwolf seed 등):
```
[reviewer]
```

---

## 6. 자유 코멘트 (open-ended)

### 6.1 paper 의 강점 3 가지
1.
2.
3.

### 6.2 paper 의 약점 3 가지
1.
2.
3.

### 6.3 next 6 개월 priority 추천
1.
2.
3.

### 6.4 SSCI submission 시 적합 journal 추천
- 1순위:
- 2순위:
- 3순위:

---

## 7. Reviewer 서명 + 검토 완료일

- 검토 완료일: ________________
- Reviewer 서명: ________________
- 추가 follow-up 가능 여부: ________________

---

_본 template 작성 후 author (정재헌) 에게 전달. PAP v3.5 update 시 반영 사항 명시._
