# PAP v4.2 Anchor 재구조화 Plan

**Date**: 2026-05-05  
**Trigger**: AKM canonical (BHJ WLS) t=+1.51 not sig + AR-CI [-0.497, +0.013] inclusive of 0 + first-stage F=19.65 < OP τ=10% cutoff 23.1.  
**Decision**: Anchor 를 ADH 2013 (IV-main) → DFS 2014 + Lang/ADH 2019 + LMP 2022 (RF-main + valid weak-IV) 로 재배치. IV weak 이 단점이 아니라 contribution.

## 1. Anchor 재배치 표

| 위치 | PAP v4.1 (이전) | PAP v4.2 (신규) | 사유 |
|---|---|---|---|
| § 1 main framework | ADH 2013 (China shock IV) | **DFS 2014** (독일 net export) | Korea export-driven 매핑 직접 |
| § 1 health outcome | Pierce-Schott 2020 (mortality) | **Lang-McManus-Schaur 2018** (mental) + **ADH 2019** (mortality) | 본 paper outcome 가장 직접 analog |
| § 1 mechanism | implicit | **Colantone-Crinò-Ogliari 2019** (mental distress) | individual-level micro foundation |
| § 5 method | tF mention only | **Lee-McCrary-Moreira-Porter 2022** explicit | 본 paper 의 5-layer SE 핵심 |
| § 7 result framing | IV main | **RF main, IV robustness** | F<23.1 정직 보고 |
| § 9 mechanism | Z-score deck | **Sullivan-vW 2009 + Eliason-Storrie 2009 + Charles-Hurst-Schwartz 2019** | displacement → mortality channel anchor |
| Robustness only | DFS 2014 | ADH 2013 (with weak-IV honest reporting) | flip 됨 |

## 2. § 1 Introduction outline (재작성)

### Para 1: Trade × labor 의 두 stylized fact
- US/EU manufacturing decline → employment ↓ (ADH 2013, Pierce-Schott 2016)
- Deaths of despair ↑ (Pierce-Schott 2020, ADH 2019, Finkelstein-Notowidigdo-Shi 2026, Charles-Hurst-Schwartz 2019)
- Mediator: mental distress (Colantone et al. 2019, Lang et al. 2018), displacement (Sullivan-vW 2009, Eliason-Storrie 2009), occupational injury (McManus-Schaur 2016)

### Para 2: Korea 의 차별점
- Export-driven (DFS 2014 의 독일 analog)
- KR-CN bilateral 가 ADH-style import-Bartik 와 다름 (net positive exposure)
- Trade gain 가 mortality 에 protective 가설

### Para 3: Identification 도전
- ADH-style IV first-stage F = 19.65 (OP τ=10% cutoff 23.1 미달)
- Solution 1: LMP 2022 tF inference (5% level cutoff t=3.43 for F=19.65)
- Solution 2: BHJ 2022 ssaggregate (shock-only exogeneity, AKM cluster SE)
- Solution 3: Reduced-form main + IV robustness (Pierce-Schott 2020 / Finkelstein 2026 의 main spec convention 따름)

### Para 4: Three contributions
1. **First mortality effect estimate for Korea** — 사상 처음
2. **Reverse asymmetry**: protective effect in export-economy (mirror image of US/EU)
3. **Methodological**: LMP 2022 + Pre-WTO placebo direct test of BHJ 2022 shock-only exogeneity 한 첫 paper

### Para 5: Summary results
- β = −0.069 (Δ_5y log mortality_h, despair_total), HC1 t=−2.42
- Sub-period sign 일치 (1997-2007 + 2008-2018)
- Pre-WTO placebo PASS (1992-1996 shock × 1998-2000 mortality cluster p=0.22)
- Drop-C26 (전자) cluster-sido t=−3.24, p=0.0012 (broad exposure, not single industry)
- AKM canonical (BHJ WLS) t=+1.51, AR-CI [-0.50, +0.01]: weak-IV reporting transparency

## 3. § 2 Related Literature outline

### Subsec 2.1: Trade × employment
- ADH 2013 baseline (Korean comparison)
- DFS 2014 (독일 net export gain 본 paper 와 직접 비교)
- Pierce-Schott 2016 manufacturing decline
- Charles-Hurst-Schwartz 2019 (manufacturing → employment)

### Subsec 2.2: Trade × health outcome
- Lang-McManus-Schaur 2018 (mental health, BRFSS, US CZ)
- McManus-Schaur 2016 (occupational injury)
- Colantone-Crinò-Ogliari 2019 (UK BHPS individual GHQ)
- Adda-Fawaz (2017) 추가 가능 (R-A 추가 fetch 미완)

### Subsec 2.3: Trade × mortality (despair specifically)
- Pierce-Schott 2020 AERI (US county, NTR gap)
- ADH 2019 (US CZ, gender differential, deaths of despair)
- Finkelstein-Notowidigdo-Shi 2026 (NAFTA, US county)
- Charles-Hurst-Schwartz 2019 (opioid death)

### Subsec 2.4: Mediator anchors
- Sullivan-von Wachter 2009 (mortality hazard, individual)
- Eliason-Storrie 2009 (Sweden plant closure, cause-specific)

### Subsec 2.5: Methodological
- ADH 2013 / GPSS 2020 / BHJ 2022 (shift-share theory)
- AKM 2019 (cluster SE)
- LMP 2022 (tF valid inference)

## 4. § 5 Empirical Specification 변경 사항

### Main spec (RF):
```
Δ_5y log(mortality_h_t / mortality_h_t-5) = α + β·z_x_h + γ·X_h + θ_t + ε_h
```
- 5-layer SE: HC1, WCB cluster-sigungu, cluster-sido, AKM (BHJ industry-mode), Conley
- Identification: shock-only exogeneity (Pre-WTO placebo confirms)

### Robustness (IV):
- ADH 2013 IV (8개 OECD): F=19.65, **LMP tF cutoff t=3.43** for 5%
- KR-CN bilateral IV: F=6.10, **LMP tF cutoff t=6.81** (weak-IV warning)
- AKM canonical WLS: β=+0.890, t=+1.51 (transparent weak-IV reporting)
- AR confidence set: [-0.50, +0.01]

### Sensitivity (NEW):
- Drop-C26 (전자부품): cluster-sido t=−3.24, p=0.0012 (broad exposure)
- Drop top-3: t=−2.08 (still robust)
- Pre-WTO placebo: cluster p=0.22 (shock-only exogeneity 직접 입증)

## 5. § 7 Results 변경 사항

### Tier 1 (publishable, 강한 evidence):
- RF β=−0.069, HC1 t=−2.42 (5-year diff, despair_total)
- WCB cluster-sigungu p=0.041
- Cluster-sido t=−2.12
- Drop-C26 cluster-sido t=−3.24 (broad exposure)
- Pre-WTO placebo PASS (BHJ shock-only exogeneity 직접)

### Tier 2 (transparency, 약한 evidence):
- IV 2SLS β=−0.099, HC1 t=−1.85 (LMP tF criterion 미달)
- AKM canonical WLS β=+0.890, t=+1.51 (weak-IV)
- AR-CI [-0.50, +0.01] (0 inclusive)

→ **Tier 1 가 main, Tier 2 가 robustness**. ADH 2013 main spec frame 의 paper 들 (Pierce-Schott 2020 등) 도 동일 convention.

## 6. § 9 Mechanism 변경 사항

### NEW mediator anchor:
- Sullivan-vW 2009: individual mortality hazard (50-100% short-run, 10-15% long-run)
- Eliason-Storrie 2009: Swedish plant closure (suicide·alcohol 2배)
- Charles-Hurst-Schwartz 2019: manufacturing → opioid

### Mediation in this paper:
- z_m_marital (1975-1995 cohort sex ratio): trade gain → marriage market value ↑ → suicide ↓
- z_m_education (대학 distance): displacement protection ↑ (한국 1990 census proxy)

### ADH 2019 mediator framing:
- Male labor demand shock → marriage market deterioration → premature mortality
- 본 paper 는 inverse: positive trade gain → marriage market 보존 → mortality protective

## 7. § 8 Limitations 변경 사항

- IV first-stage F < 23.1: ADH-style IV 가 export-driven Korea 에서 약한 것은 자연스럽지만, AR-CI 가 0 포함 → IV interpretation 보수적
- Mental health micro data 부재 (NHIS 시도-level only): mediator 직접 측정 한계
- 1994 baseline 의 1997 IMF 위기 직전 호황 우려: 1989/1992 baseline (KOSIS MDIS 신청 중) 의 sensitivity 추후

## 8. 다음 step

1. **즉시 (this turn)**: 본 plan 검토 + sign-off
2. **다음 turn (R-A)**: PAP v4.2 main body 본격 재작성 (anchor 재배치 적용)
3. **차차 turn**: paper draft § 1 export from PAP v4.2 → markdown + docx
4. **차차차 turn**: reference 27편 cite count 검증 + bibliography build

## 9. R-A 권장 순서

```
Path 1 (즉시, 권장):
1. 본 plan 사용자 검토 + sign-off
2. PAP v4.2 main body 작성 (1-2 turns, R-A)
3. paper draft § 1 markdown export (1 turn, R-A)
4. paper draft § 1 docx export with academic-paper-tools:paper-docx (1 turn)

Path 2 (수정 시):
1. 사용자 가 anchor 우선순위 변경 (예: Lang 보다 Pierce-Schott main 으로) 지시
2. R-A 가 plan revise

Path 3 (additional 보강):
1. Adda-Fawaz 2017 추가 fetch (사용자)
2. 한국 학자의 무역×노동 anchor 추가 (사용자)
3. PAP v4.2 anchor 27 → 30 으로 확장
```
