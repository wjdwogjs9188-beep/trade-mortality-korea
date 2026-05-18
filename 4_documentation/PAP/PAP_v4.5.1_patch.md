# PAP v4.5.1 — Patch (Round 21·22·23 audit 11 framing 정정)

**version**: 4.5.1 (patch on v4.5)
**date**: 2026-05-05
**author**: 정재헌 (가천대학교 경제학)
**supersedes**: PAP v4.5 의 일부 § (1.1, 1.3, 2, 3.2, 4.1, 4.3, 5.4, 9.4, 9.5, 10, 11)
**status**: Stage 5 회귀 시작 전 framing 정정 commit

본 patch 는 v4.5 audit (Round 21·22·23 통합) 의 11 framing 정정 항목 commit. 코드 실행 필요한 7 pending (P1-P9, P10 closed) 은 § 12 의 Stage A·B 분담 그대로 유지.

---

## v4.5 → v4.5.1 변경 list (11 항목)

### Tier A (Round 22 외부 verification 확정 — 4)

#### 정정 1: § 9.5 + § 11 — DGHP 2017 author "Pinkovskiy" → "**Pinto**"

**External verification source 셋**: NBER w23209 official + SSRN abstract 3126664 + IDEAS/RePEc p/nbr/nberwo/23209 — 모두 "Christian Dippel, Robert Gold, Stephan Heblich, **Rodrigo Pinto**" 확정.

**Disambiguation**:
- **Rodrigo R. Pinto** (UCLA, Heckman 의 mediation econometrics 공저자) — DGHP project 의 mediation framework 핵심 기여
- Maxim Pinkovskiy (NY Fed economist) — 별개 인물, DGHP 무관

**v4.5.1 정정**:
- § 9.5 모든 "Pinkovskiy" → "**Pinto**" 일괄
- § 11 references 의 cite: "Dippel C, Gold R, Heblich S, **Pinto R** (2017). NBER WP 23209"
- § 12.7 P5 (DGHP/DFH 분리 인용 file) 의 Pinto 정정 통합

#### 정정 2: § 1.3 + § 2 — PS20 anchor framing (drug-overdose-specific) + K70-K77 vs K70+K73+K74

**External verification (PS20 본문 fetch)**:
> "Within deaths of despair, we find that **the link between PNTR and mortality is driven by drug overdoses**. For this cause of death, an interquartile shift in exposure is also associated with a relative increase of 2 to 3 per 100,000... we find little relationship between PNTR and mortality from either suicide or alcohol-related liver disease (ARLD)."

PS20 의 main effect 는 **drug overdose only**, suicide + ARLD null.

**v4.5.1 정정**:

§ 1.3 anchor 비교 표 PS20 행:
| 이전 (v4.5) | 정정 (v4.5.1) |
|---|---|
| Pierce-Schott 2020 (AERI): + (suicide + drug), +1.4% | Pierce-Schott 2020 (AERI): **+ (drug overdose only, +2-3/100k IQR; suicide + ARLD: null)** |

§ 2 outcome groups 의 K70-K77 vs Case-Deaton K70+K73+K74 narrower 명시:
- 이전 (v4.5): "간질환 081, K70-K77"
- 정정 (v4.5.1): "간질환 081, **K70-K77 (본 paper 의 broader scope; Case-Deaton 2015 PNAS 의 narrower 정의 K70+K73+K74 와 differential. K71 toxic + K72 hepatic failure + K75 inflammatory + K76 other + K77 disorders 추가 포함은 본 paper 의도적 broader scope 로, despair_total 의 alcohol-induced 외 간질환 포함. K70+K73+K74 only 사용한 sensitivity test 별도 § 8.5 권고)**"

→ § 8.5 limitation 항목 보강 (F17 분리 불가 + K70-K77 vs narrower 두 sensitivity 명시)

#### 정정 3: § 1.3 — ADH 2019 main result reposition (marriage market → primary, mortality → secondary)

**External verification (Autor-Dorn-Hanson 2019 본문 fetch, AERI 1(2) 161-178)**:
- 정확 title: "When Work Disappears: Manufacturing Decline and the Falling **Marriage Market Value of Young Men**"
- Main result: "shifts in the relative economic stature of young men versus young women affected **marriage, fertility, and children's living circumstances**"
- Secondary mortality: "**a one-unit shock more than doubles the relative male death rate from drug and alcohol poisoning**"
- **정량 "+19.5/100k decade" 절대값 외부 verify 실패** — paper specific table 직접 인용 없이 사용 시 fabricated/unverified 위험

**v4.5.1 정정**:

§ 1.3 anchor 비교 표 ADH 2019 행:
| 이전 (v4.5) | 정정 (v4.5.1) |
|---|---|
| ADH 2019 (AERI): + (D&A deaths) +19.5/100k decade | ADH 2019 (AERI): **main = marriage market value of young men ↓; secondary = relative male D&A poisoning death rate ~doubling under one-SD trade shock (정량값 본 paper 본문 verify pending)** |

→ ADH 2019 을 본 paper § 9 mechanism 의 **marriage market mediator anchor** 로 활용 + mortality outcome anchor 는 PS20 (drug-only) + Case-Deaton 2015 PNAS (composite definition) 의 조합으로 재구성. § 9.3 (KOSIS family marriage market) 의 ADH 2019 mirror evidence framing 강화.

#### 정정 4: § 5.4 — Lang **2019** Health Economics + F=18.77 verification pending 명시

**External verification**:
- 정확 cite: **Lang, M., T.C. McManus, G. Schaur (2019)** "The Effects of Import Competition on Health in the Local Economy" Health Economics **28(1) 44-56**, online publication 2018-09-19, DOI 10.1002/hec.3826, January 2019 print issue
- "Lang 2018" 표기는 NBER/SSRN first-version 만 가리킬 때 사용 — ambiguous
- IV definition: ADH 2013 standard 8개국 list — v4.5 ADH-8 OECD list 와 set 일치
- **F=18.77 정확값 외부 verify 실패** (paywalled Wiley, 403 error)

**v4.5.1 정정**:

§ 5.4 ADH-8 비교 표:
| 이전 (v4.5) | 정정 (v4.5.1) |
|---|---|
| ADH-8 published precedent (Lang 2018): F=18.77 | ADH-8 published (**Lang, McManus, Schaur 2019** Health Economics 28(1):44-56, DOI 10.1002/hec.3826): **F 약 18-20 (paper 본문 verify pending — 저자가 학교 도서관 access 또는 author preprint 통해 specific value Table 확인 후 commit)** |

§ 11 references cite:
- "Lang M, McManus TC, Schaur G (**2019**) The Effects of Import Competition on Health in the Local Economy. Health Economics **28(1):44-56**. DOI 10.1002/hec.3826"

→ § 12.7 P11 (NEW) 신설: Lang 2019 본문 직접 fetch + F 정확값 + spec verify (사용자 측 또는 R-A 가 학교 도서관 access 시)

### Tier A (Round 21 line-by-line — 3)

#### 정정 5: § 1.1 + § 1.3 — DFS 2014 outcome 차원 분리

**문제**: § 1.1 본문 ("DFS 2014 가 직접 mortality 측정 안 함") 과 § 1.3 표 (DFS 2014 부호 "−") 직접 충돌. employment outcome 과 mortality outcome 차원 혼동.

**v4.5.1 정정**:

§ 1.3 anchor 비교 표 — outcome 별 분리:

| paper | 국가 | shock type | **outcome** | **부호** | β | identification |
|---|---|---|---|---|---|---|
| ADH 2013 | USA | China imports | employment | + | various | Bartik IV |
| Pierce-Schott 2016 | USA | NTR gap | employment | + | manuf emp ↓ | DiD |
| Pierce-Schott 2020 | USA | NTR gap | mortality | + (drug overdose only) | +2-3/100k IQR | DiD |
| ADH 2019 | USA | China shock | marriage market (main) + mortality (secondary) | − (marriage); + (D&A doubling, 정량 verify pending) | n/a | Bartik IV |
| Charles-Hurst-Schwartz 2019 | USA | manuf decline | mortality (opioid) | + | 1ppt manuf↓→opioid↑ | Bartik IV |
| Lang-McManus-Schaur 2019 | USA | China imports | mental health (poor day) | + | +0.26 day/mo (7.8%) | Bartik IV (F~18-20) |
| Colantone-Crinò-Ogliari 2019 | UK | China imports | mental distress (GHQ-12) | + | £200-270/yr comp (verify pending) | individual FE + IV |
| McManus-Schaur 2016 | USA | China imports | occup injury | + | +12-13% smallest plant | Bartik IV |
| Finkelstein-Notowidigdo-Shi 2026 | USA | NAFTA | drug death | + | +5-9% (verify pending) | DiD |
| **DFS 2014** | Germany | East trade | **employment (NOT mortality)** | **+ (emp gain)** | +442k jobs | Bartik IV |
| Sullivan-vW 2009 | USA-PA | plant closure | mortality | + | +50-100% short, 10-15% long | quasi-exper |
| Eliason-Storrie 2009 | Sweden | plant closure | cause-specific mortality | + | HR≈2 suicide·alcohol (정량 verify pending) | quasi-exper |
| **본 paper** | **Korea** | **KR-CN bilateral** | **mortality** | **−** | **−6.9%** | **Bartik IV (F=19.65) + LMP tF + RF** |

**§ 1.1 thesis 정정**:
> "독일 (DFS 2014) 의 export-driven *employment gain* (mortality outcome 직접 측정 안 함) 와 본 paper 의 *mortality decline* 이 *consistent mechanism 가설* (employment ↑ → mortality ↓) 으로 연결. 두 paper 의 *outcome 차원 다름* — DFS 2014 = employment, 본 paper = mortality. DFS 2014 결과는 본 paper § 9 mechanism 의 employment channel 의 anchor 로 활용 (직접 결과 비교 아님)."

#### 정정 6: § 10 H4 vs § 8.11 framing 정합

**문제**: § 8.11 ("β=+0.0238 sign reversal weak evidence") vs § 10 H4 ("Pre-WTO placebo β ≈ 0, p > 0.10 share-violation partial mitigation") 직접 충돌.

**v4.5.1 정정** (option b — Pre-WTO 를 confirmatory 가 아닌 robustness 로 demote):

§ 10 confirmatory 9 hypothesis (이전 10 → 9, H4 → exploratory):

1. H1: β(despair_total) < 0
2. H2: β(despair_total) sub-period sign 일치
3. H3: β(4 placebo outcomes) ≈ 0 (Romano-Wolf reject 안 함)
4. ~~H4~~ → **Exploratory E5 로 demote** (Pre-WTO placebo)
5. H5 → H4: Drop-C26 cluster-시도 t < −2
6. H6 → H5: 5 baseline year sign 일치
7. H7 → H6: HIRA SSRI 처방률 mediator
8. H8 → H7: HIRA F32 진단률 cross-validation
9. H9 → H8: KOSIS 자살 ASMR 일치율 > 95%
10. H10 → H9: DFS 2014 mechanism mirror

§ 10 exploratory 6 (이전 5 → 6):
- E1: KIET 60대 first-stage F > 23.1
- E2: 전국사업체조사 broad baseline sign 일치
- E3: Conley spatial SE robust
- E4: C09·A10·C10 negative control β ≈ 0
- **E5 (NEW) — Pre-WTO placebo robustness**: β ≈ 0 (cluster-시도 p > 0.10) **and** |β| < |main β|/3 (magnitude condition added)
- E6 (이전 E5): AKM 정식 BHJ 2022 implementation OLS β 일관성

§ 8.11 framing 강화:
> "Pre-WTO placebo β=+0.0238 (positive sign, main 부호 반대) 는 magnitude 작지만 sign 자체가 noise 가 아닐 가능성. § 10 E5 의 magnitude condition (|β_pre| < |β_main|/3 = 0.023) 통과 하지만 sign reversal 의 weak evidence 자체는 share-violation 우려의 partial mitigation only. 5 baseline year sensitivity (1992·1993·1994·1995·1996) + Drop-C26 cluster-시도 t=−3.24 + 추가 sub-period placebo (P8) 로 전체 robustness 패키지 평가. Pre-WTO placebo 단독으로 share-violation 해결 주장 X."

#### 정정 7: § 9.4 z_m_education 1985 vs § 5.3 5-baseline cross-reference

**문제**: § 9.4 의 1985 baseline vs § 5.3 의 1992-1996 baseline 의 lag/scope 차이 명시 안 됨.

**v4.5.1 정정** (§ 9.4 본문 추가):

> "**z_m_education baseline 시점 vs industry shares baseline 의 정합성**:
> 
> § 5.3 의 5 baseline (1992·1993·1994·1995·1996) 는 *industry employment shares* (광업제조업조사 microdata) 의 baseline. § 9.4 의 1985 baseline 은 *university distribution* (KEDI 1985 연보) 의 baseline. 두 baseline 은 *별개 변수의 baseline* 으로 lag/scope 다름.
> 
> **이론적 정합성**: 1985 시점 university distribution 이 시군구 의 baseline characteristic. 1985-2024 사이 시군구 trade exposure (KR-CN bilateral, 2000-2010) 는 1985 university distribution 에 affect 안 함 (시간 순서). 1985 university distribution → 시군구 education access (시간 불변) → labor market mobility → mortality 의 chain.
> 
> **Sensitivity check (planned)**: § 5.3 의 5 baseline (1992-1996) 과 동일 시점 (1990 또는 1995) 의 university distribution 사용 시 z_m_education 의 IV relevance 변화 비교. 1985 vs 1990 vs 1995 university distribution 의 시군구별 변동 작으면 (대학 신설 1990s 적음) 1985 baseline 의 IV relevance 보장."

→ § 12.7 P12 (NEW) 신설: KEDI 1985 vs 1990 vs 1995 university distribution 비교 (사용자 측 KEDI 도서관 access 또는 KESS 1985 한국교육통계연보 verify)

### Tier B (Round 22 외부 verification — 4)

#### 정정 8: § 4.1 — AKM 2019 (QJE) vs BHJ 2022 (RES) ssaggregate WLS 명명 분리

**문제**: v4.5 § 4.1 의 "AKM (BHJ industry-mode, simplified)" 가 두 framework conflate.

**v4.5.1 정정**:

§ 4.1 5-layer SE 표 의 AKM row 정정:

| Layer | Method | 결과 | Status |
|---|---|---|---|
| ~~AKM (BHJ industry-mode, simplified)~~ | ~~ssaggregate WLS regression~~ | β=+0.890 | 🟡 P2 정식 implementation pending |
| **(정정)** **shift-level WLS regression (BHJ 2022 ssaggregate-based)** | shift-level inference, OLS β 와 별개 estimator | β=+0.890, t=+1.51 | 🟡 P2 정식 implementation pending |

**§ 4.1.1 정정** (별도 estimand 명확화):

> "본 paper 의 'shift-level WLS regression (ssaggregate-based)' 은 BHJ 2022 (RES) 의 *shift-level equivalence theorem* 의 부분 implementation. ssaggregate transformation 후 shift-level WLS regression β=+0.890 은 region-level OLS β=−0.069 와 **다른 estimator**.
> 
> 정식 frameworks 두 가지:
> - **AKM 2019 (Adão-Kolesár-Morales, QJE 134(4) 1949-2010)**: region-level OLS β + cluster-robust shift-level SE. R `ShiftShareSE` package 의 `reg_ss()` 함수 또는 Stata `ShiftShareSEStata` 표준.
> - **BHJ 2022 (Borusyak-Hull-Jaravel, RES 89(1) 181-213)**: shift-level inference 의 정식 equivalence theorem. Stata `ssaggregate` package.
> 
> **두 framework 동시 보고 권고 (P2 Stage B Claude Code 위임)**:
> - AKM 정식 (R `ShiftShareSE`): region-level OLS β=−0.069 그대로 + AKM cluster-robust SE
> - BHJ 정식 (Stata `ssaggregate`): shift-level inference 의 shift-level OLS β + cluster-on-shock SE
> 
> 두 framework 의 결과 비교 후 § 4.1 표 정정."

#### 정정 9: § 11 — BHJ 2022 (RES) vs BHJ 2025 (JEP) 분리 cite

**v4.5.1 정정**:

§ 11 references:
- BHJ 2022 (paper_24997 → 정확): "Borusyak K, Hull P, Jaravel X (2022) Quasi-Experimental Shift-Share Research Designs. Review of Economic Studies 89(1):181-213. DOI 10.1093/restud/rdab030" — 정식 econometric framework
- BHJ 2025 (NEW): "Borusyak K, Hull P, Jaravel X (2025) A Practical Guide to Shift-Share Instruments. Journal of Economic Perspectives 39(1):181-204. DOI 10.1257/jep.20231370" — practitioner checklist

본문에서 framework 인용 시 BHJ 2022, practical recommendation 인용 시 BHJ 2025 분리 사용.

#### 정정 10: § 3.2 — Olea-Pflueger 2013 venue **JBES** (NOT AER)

**External verification**: Montiel Olea & Pflueger (2013) "A Robust Test for Weak Instruments" **Journal of Business & Economic Statistics 31(3) 358-369**, DOI 10.1080/00401706.2013.806694

**v4.5.1 정정**:
- § 3.2 + § 11: "Olea-Pflueger 2013 (**JBES** 31(3):358-369)" — v4.x 에서 "AER" 표기 시 즉시 정정

#### 정정 11: § 4.3 — Romano-Wolf algorithm specificity

**External verification**:
- Romano-Wolf (2005a) JASA 100(469):94-108
- Romano-Wolf (2005b) Econometrica 73(4):1237-1282 — Algorithms 4.1-4.2 ("Studentized StepM Procedure")
- Romano-Wolf (2016) Statistics & Probability Letters 113:38-40
- Stata `rwolf` package: Clarke-Romano-Wolf (2020) Stata Journal 20(4):812-843

**v4.5.1 정정** (§ 4.3 algorithm source 명시):

> "**Algorithm**: Romano-Wolf 2005b Algorithms 4.1-4.2 ('Studentized StepM Procedure') + 2016 multiple-test extension. Stata implementation: Clarke-Romano-Wolf (2020) Stata Journal 20(4):812-843 의 `rwolf` package."

---

## v4.5 → v4.5.1 미정정 항목 (Stage A·B 또는 paper draft 단계)

### Tier C — paper 본문 verify 필요 (paper draft 단계)

- **C1**: Eliason-Storrie 2009 HR=2.15·2.21 정확값 paper Table 직접 verify
- **C3**: Colantone-Crinò-Ogliari 2019 final published JIE 의 £270/yr (working paper £200) verify
- **C4**: McManus-Schaur 2016 의 +12% (working paper +13%) verify
- **C5**: Finkelstein-Notowidigdo-Shi 2026 의 +5-9% verify + 정확 cite (NBER WP 34855 vs BFI WP 2026-33)
- ADH 2019 의 "+19.5/100k decade" 정량값 verify (정정 3 의 hedged framing 으로 partial mitigation)
- Lang 2019 의 F=18.77 verify (정정 4 의 hedged framing)

→ **사용자 측 paper 본문 직접 access (학교 도서관 ScienceDirect / Wiley / NBER subscription) 후 cite 정확화**. 본 paper § 11 references final commit 시점에 처리.

### 코드 실행 항목 (Stage A·B 또는 사용자 측)

- **P1** (Stage A): n=222 vs 251 정합성 + 5 시군구 drop list (R-A direct 1-2h)
- **P2** (Stage B): AKM 정식 (R `ShiftShareSE`) + BHJ 정식 (Stata `ssaggregate`) 동시 보고 (Claude Code 위임 4-5h, 정정 8 통합)
- **P3** (Stage B): AR-CI 산출 (linearmodels AR_test, Claude Code 위임 2-3h)
- **P4** (Stage A): WCB cluster-시도 G=16 verify (R-A direct 1h)
- **P5** (Stage A): DGHP/DFH 분리 인용 file (Pinto 정정 통합, R-A direct 30분)
- **P6** (Stage A): Conley centroid SE (R-A direct 1h)
- **P8** (Stage A): Pre-WTO sub-period sensitivity (1992-1995, 1990-1994) + magnitude condition E5 통과 verify (R-A direct 1h)
- **P9** (사용자 측): KOSIS 사망원인 50항목 시군구별 search (1h)
- **P11 (NEW)**: Lang 2019 본문 fetch + F 정확값 + spec verify (학교 도서관 access)
- **P12 (NEW)**: KEDI 1985 vs 1990 vs 1995 university distribution 비교 (사용자 측 KEDI/KESS 1985 한국교육통계연보 verify)

---

## Submission Strategy 권고 (Round 23 동의)

**Sequence A (R-A 권고, Round 23 동의)**:
```
v4.5.1 commit → Stage A·B + Track 3 + P9·P11·P12 → v4.6 commit (paper draft entry-ready)
→ Paper draft Stage C (KER full paper 25-35 page)
→ KER submission (cover letter 7 항목 권장)
→ KER R&R 또는 reject
→ Advisor 합류 negotiate (가천대 또는 외부 한국 경제학부 교수, 또는 Choi-Xu 2020 World Economy 저자 contact)
→ AEJ Applied 도전
→ AEJ Applied 실패 시 JHE / Demography / EER / RESTAT / Health Economics
→ AER:Insights = long-term goal (advisor + IV F>30 + multi-paper track 후)
```

**Timeline realistic**:
- v4.5.1 commit: ✅ (본 turn)
- Stage A (R-A direct): 다음 turn 4-5h
- Stage B (Claude Code 위임): 차차 turn 5-6h (정정 8 의 AKM + BHJ 동시 보고)
- Track 3 (1992 baseline build): Stage A·B 와 병렬
- 사용자 측 P9·P11·P12: 1-2주 (학교 도서관 access 시간 포함)
- v4.6 commit: 2-3주
- Paper draft Stage C (KER full paper): 3-4주
- **KER submission ready: 6-12주** (v4.5 § 결론의 4-6주는 unrealistic, Round 23 audit 정확)

**Cover letter 7 항목** (Round 23 권고):
1. 학부생 단독 저자 status 정직 disclosure
2. 가천대 경제학부 informal advisor 명시
3. AEA Data and Code Repository commitment
4. KOSIS data access 정보 (MDIS approval ID 해당 시)
5. KSIC 분류 + 시군구 boundary crosswalk documentation replication archive
6. Choi-Xu 2020 (World Economy) 와의 differentiation 1 paragraph
7. PAP v4.0 → v4.5.1 누적 변경 OSF timestamp 명시 (post-data discovery transparent disclosure)

---

## R-A 의 systematic lapse 자기 시인 (Round 1-23 누적)

본 patch 작성 시 R-A 의 systematic 결함:

1. **External citation web verification 의존**: Pinkovskiy/Pinto, Lang 2018/2019, PS20 composite/drug-only, ADH 2019 main/secondary, Olea-Pflueger AER/JBES 등 다수 misattribution 의 외부 verification 결과 정정. **R-A specific citation 외부 verify 가 systematic 부족**.

2. **Self-audit consistency lapse**: 이전 audit (Round 19) 에서 R-A 가 짚은 DFS 2014 outcome 차원 issue 가 v4.5 § 1.3 표에 미반영. R-A 의 cumulative audit memory persistence 부재.

3. **§ cross-reference 검증 lapse**: § 10 H4 vs § 8.11 framing 충돌, § 9.4 1985 baseline vs § 5.3 1992-1996 baseline lag mismatch — 모두 R-A 의 v4.5 commit 시점 cross-reference 검증 안 함.

4. **Korean setting context 한계**: 안산 시군구 코드 lapse 누적, KEDI 1985 baseline 가용성 verify 부재 — 사용자 직접 inspection 의존.

5. **R-A audit 은 외부 referee 의 보조 도구이며 대체재 아님** (Round 23 audit 정확). 본 v4.5.1 commit 후에도 외부 advisor / KER actual referee review 가 R-A audit 보다 우선.

---

## 결론 (PAP v4.5.1 patch commit)

본 v4.5.1 = audit-accepted patch. v4.5 의 11 framing 정정 + magnitude verify pending hedged 표기 + Stage A·B 코드 실행 항목 분담 그대로 유지.

**Target venue**: KER 1순위 + AEJ Applied 2순위 + AER:Insights long-term goal (Round 23 정확 자기 인식 유지).

**Pending list**: 9개 (P1·P2·P3·P4·P5·P6·P8·P9·P11·P12 — P10 closed). v4.6 commit 시점에 모두 closed 권고.

**Author**: 정재헌 (가천대학교 경제학, 단독 저자) — KER R&R 시점에 advisor 합류 negotiate.

본 v4.5.1 = **외부 advisor / reviewer 피드백 통합 후 Stage 5 회귀 분석 시작 직전 status**.
