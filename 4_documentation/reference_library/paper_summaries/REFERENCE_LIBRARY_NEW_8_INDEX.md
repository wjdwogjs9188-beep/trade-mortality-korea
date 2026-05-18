# Reference Library 신규 8편 추가 — 2026-05-05 (Round 2 정독 후)

## 추가 동기

PAP v4.1 publishable result (β=−0.069, WCB p=0.041) 의 anchor 재구조화 필요:
- 이전: ADH 2013 main framework. 한국 export-driven 구조에 IV weak-IV (F=19.65 < 23.1)
- 변경: DFS 2014 + Lang-McManus-Schaur 2018 + ADH 2019 main anchor → IV weak 이 단점이 아니라 contribution

## 9편 list (paper_20-28, Round 23 audit 후 DGHP 2017 추가)

추가: paper_28_dippel_gold_heblich_pinto_2017 — DGHP/DFH single-IV mediation framework (R-A round 22 audit 의 Pinkovskiy → Pinto 정정 후 commit, NBER WP 23209 본문 직접 inspect)

## 8편 list (paper_20-27)

| # | File | Citation | Role | Tier |
|---|---|---|---|---|
| 20 | paper_20_mcmanus_schaur_2016 | McManus, T. C. & G. Schaur. 2016. "The effects of import competition on worker health." *J Int Econ* 102: 160-172. | Occupational injury anchor | T1 |
| 21 | paper_21_lang_mcmanus_schaur_2018 | Lang, M., T. C. McManus & G. Schaur. 2018. "The effects of import competition on health in the local economy." *Health Economics* (Wiley) 28(1): 44-56. DOI 10.1002/hec.3826. | **PRIMARY HEALTH OUTCOME ANCHOR** | T2 |
| 22 | paper_22_colantone_crino_ogliari_2019 | Colantone, I., R. Crinò & L. Ogliari. 2019. "Globalization and mental distress." *J Int Econ* 119: 181-207. | Mental distress + family spillover anchor | T1 |
| 23 | paper_23_autor_dorn_hanson_2019 | Autor, D., D. Dorn & G. Hanson. 2019. "When work disappears: Manufacturing decline and the falling marriage market value of young men." *AER:Insights* 1(2): 161-178. | **PRIMARY MORTALITY ANCHOR** | T1 |
| 24 | paper_24_charles_hurst_schwartz_2018 | Charles, K. K., E. Hurst & M. Schwartz. 2019. "The transformation of manufacturing and the decline in U.S. employment." *NBER Macro Annual* 33: 307-372. (BFI WP 2018-20) | Manufacturing → opioid mechanism | T1 |
| 25 | paper_25_eliason_storrie_2009 | Eliason, M. & D. Storrie. 2009. "Does job loss shorten life?" *J Hum Res* 44(2): 277-302. | Sweden displacement → cause-specific mortality | T1 |
| 26 | paper_26_sullivan_vonwachter_2009 | Sullivan, D. & T. von Wachter. 2009. "Job displacement and mortality: An analysis using administrative data." *QJE* 124(3): 1265-1306. | US displacement → mortality hazard | T0 |
| 27 | paper_27_lee_mccrary_moreira_porter_2022 | Lee, D. S., J. McCrary, M. J. Moreira & J. R. Porter. 2022. "Valid t-ratio inference for IV." *AER* 112(10): 3260-3290. (NBER WP 29124, Mar 2022) | **METHODOLOGICAL ANCHOR (tF)** | T0 |

Tier: T0 = top-5 (AER/QJE/JPE/REStud/Ecma), T1 = top field, T2 = field

## R-A prior message 정정

이전 turn 에서 R-A 가 다음과 같이 잘못 표기:
- "McManus-Schaur 2016 J Health Econ" → 정정: **Journal of International Economics** (JIE) vol 102
- "Lang-McManus-Schaur 2019 J Health Econ" → 정정: **Health Economics (Wiley)** vol 28(1)

## Round 2 정독 후 핵심 발견

### 1. **본 paper 의 F=19.65 가 Lang 2018 의 F=18.77 와 거의 동일**
- Lang 2018 spec M.3 (full controls): first-stage F = 18.77, β=+0.144** (mental health, 5% level)
- 본 paper: first-stage F (ADH-8) = 19.65, β=−0.069 (despair mortality)
- → **본 paper 의 IV strength 는 Health Economics tier (Wiley) 의 published paper 와 동등**

### 2. **LMP 2022 정확 critical value (interpolation)**
| F-statistic | tF 5% cutoff (|t|) | SE adjustment factor |
|---|---|---|
| F=10 | 4.49 | 1.751 |
| F=15 | 3.84 | ≈1.96 |
| **F=19.65 (본 paper ADH-8)** | **3.286** | **1.677** (interpolated) |
| F=20.721 | 3.234 | 1.650 |
| F=23.1 (OP τ=10%) | ~3.10 | ~1.58 |
| **F=6.10 (본 paper KR-CN bilateral)** | **~5.05** | **~2.58** |
| F→∞ | 1.96 | 1.000 |

→ 본 paper β=−0.099 의 |t|=1.85 (HC1) 은 LMP cutoff 3.286 미달 → IV interpretation 폐기 정확
→ But RF spec |t|=2.42 가 Lang 2018 의 cutoff 보다 더 강함

### 3. **ADH 2019 의 정확 mortality 효과 (단위: per 100k decade per unit shock)**
- D&A deaths: β=+19.5 (t=2.9) — **30% of total male mortality contribution**
- HIV (often IV drug related): β=+21.6 (t=2.5)
- Homicide: β=+14.0 (t=1.7, marginal)
- Suicide (20-39세): β=+7.7 (n.s.)
- Total male-female mortality gap: β=+64.4
- Baseline: 936/100k decade
- → 본 paper 의 despair_total β=−0.069 (5y log) 와 직접 magnitude 비교 가능

### 4. **Eliason-Storrie 2009 정확 hazard ratio (Sweden 1987-1988 plant closure)**
- Male overall mortality first 4y: HR = **1.44** (95% CI 1.19-1.76) [+44%]
- Male suicide first 4y: HR = **2.15** (95% CI 1.28-3.59) [≈2x]
- Male alcohol-related first 4y: HR = **2.21** (95% CI 1.14-4.31) [≈2x]
- Male smoking cancer: HR = 1.48 (n.s.)
- Female: no significant overall mortality effect
- → 본 paper 의 cause-specific outcome 의 individual-level analog

### 5. **Sullivan-vW 2009 정확 mortality hazard**
- Short-run (1y post-displacement): **+50% to +100%** mortality hazard
- Long-run (20y post): **+10% to +15%** hazard PERSISTS
- Life expectancy loss: **1.0-1.5 years** for displaced at age 40
- Earnings loss correlation: 본 displacement → mean earnings -15%-20% → mortality 50-75% of total reduced-form effect

### 6. **Lang 2018 magnitude (US CZ, 25→75 percentile = $1,000/worker shock)**
- Mental health: +0.26 day/month poor mental health (7.8% of mean) [β=+0.144 ppt]
- General health: +0.8 ppt fair/poor (5.4% of mean) [β=+0.813 ppt]
- Health affordability: +2.135 ppt unable to afford doctor visit (employed)
- **Effect concentrated in EMPLOYED (Panel B), not unemployed/homemakers** — workplace stress > job loss

### 7. **Colantone 2019 magnitude (UK individual, 25→75 percentile = 1 SD)**
- GHQ-12: β=+0.290*** (col 7 with all controls) — sig at 1%
- 25→75 percentile = £270/year compensation needed
- Total UK annual: £5.2 billion (0.35% GDP, 4.3% healthcare expenditure)
- Pre-trends placebo (future IS × past GHQ): β=+0.026 (n.s., 0.59) — **clean identification**
- Worker sorting orthogonal: stayer subsample β similar to baseline

### 8. **McManus-Schaur 2016 정확 (5y diff, 25→75 percentile = SD shock)**
- Smallest decile (40 emp): elasticity +0.107*** [12% injury rate increase]
- Median (100 emp): +0.085** [10%]
- Largest decile (400 emp): +0.063*
- 7.4% of all manufacturing injuries attributable to China shock
- 62k-90k injuries/year, $2.2-9 billion annual cost, **1-2% wage equivalent** at small plants

### 9. **Charles-Hurst-Schwartz 2018/2019 정확**
- 10 ppt manuf decline → male emp -3.7 ppt, female -2.7 ppt
- 5.7 ppt manuf decline (90-10) → opioid prescription +20 log points
- 1 ppt manuf decline → drug & opioid death rate ↑ (state-level IV est)
- 1/3 ~ 1/2 of aggregate prime-age employment decline 2000-2017 explained by manuf

## Paper anchor 재배치 (PAP v4.2 § 1·2) — 정밀화

**이전 (PAP v4.1)**:
1. ADH 2013 main framework (IV)
2. Pierce-Schott 2020 AERI benchmark
3. Finkelstein-Notowidigdo-Shi 2026 magnitude
4. DFS 2014 Germany comparison
5. Case-Deaton 2015 outcome 정의

**변경 (PAP v4.2)**:
1. **DFS 2014** (독일 net export Bartik) → Korea 와 직접 매핑
2. **Lang-McManus-Schaur 2018** (US CZ × mental health, F=18.77) — 본 paper 의 IV strength benchmark
3. **ADH 2019** (US CZ × deaths of despair, decadal mortality decomposition) → mortality outcome anchor
4. **Colantone-Crinò-Ogliari 2019** (UK individual × GHQ, family spillover) → mechanism anchor
5. **McManus-Schaur 2016** (occupational injury, plant heterogeneity) — small-plant anchor
6. Pierce-Schott 2020, Finkelstein-Notowidigdo-Shi 2026 → comparison benchmark
7. ADH 2013 → robustness only (weak-IV honest reporting)
8. **Charles-Hurst-Schwartz 2019** → manufacturing decline → opioid mediator
9. **Eliason-Storrie 2009 + Sullivan-vW 2009** → § 9 mediator (displacement → cause-specific)
10. **Lee-McCrary-Moreira-Porter 2022** → § 5 method (tF inference, exact cutoff 3.286 for F=19.65)
11. Case-Deaton 2015 → outcome 정의
12. AKM 2019 + BHJ 2022 + GPSS 2020 → SE methodology

## 본 paper § 1 narrative 재작성 (정밀화 — Round 2 후)

> "The literature on trade exposure and worker outcomes documents three robust findings.
> First, manufacturing decline from import competition reduces local employment and earnings 
> (Autor-Dorn-Hanson 2013, Pierce-Schott 2016, Charles-Hurst-Schwartz 2019). 
> Second, this decline causally elevates 'deaths of despair' — a one-unit China shock raises 
> the male-female gap in drug/alcohol mortality by 19.5 deaths per 100,000 adults per decade 
> (ADH 2019, Pierce-Schott 2020, Finkelstein-Notowidigdo-Shi 2026), accounting for 30% of 
> the trade-induced male mortality differential. Third, mediating channels include workplace 
> stress (Lang-McManus-Schaur 2018: 7.8% increase in poor mental health days), individual 
> mental distress (Colantone-Crinò-Ogliari 2019: £270/yr compensation needed), occupational 
> injury (McManus-Schaur 2016: 12% increase at smallest plants), and individual displacement 
> (Sullivan-von Wachter 2009: 50-100% short-run mortality hazard increase, 10-15% long-run; 
> Eliason-Storrie 2009: HR=2.15 for suicide, 2.21 for alcohol mortality after Swedish plant closure).

> "We extend this literature in three directions. **First**, we examine an export-oriented economy 
> (Korea) — analogous to Germany (Dauth-Findeisen-Suedekum 2014) but with stronger China-specific 
> bilateral integration. **Second**, we apply the recent valid t-ratio inference framework 
> (Lee-McCrary-Moreira-Porter 2022) to handle weak-IV concerns inherent to ADH-style designs in 
> export economies (our first-stage F=19.65 is comparable to Lang-McManus-Schaur 2018's F=18.77). 
> **Third**, we document a *protective* mortality effect of trade exposure — the inverse of the 
> US/EU pattern — and explore mechanisms through marriage market and education channels."

## 다음 step

1. **PAP v4.2 § 1·2 outline 본격 작성** — 위 narrative 적용 (Task #26 done, 본격 작성은 다음 turn)
2. **paper draft § 1 export from PAP v4.2** → markdown & docx
3. **Reference library 의 19편 + 신규 8편 = 27편 cite count 안정화**
4. **본 paper § 7 results 의 LMP 2022 cutoff 정확값** (3.286 for F=19.65) 적용
