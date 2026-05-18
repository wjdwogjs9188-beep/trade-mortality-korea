# Verified Citations — Track 1 본문 직접 inspect (2026-05-05) 본 paper PAP v4.5.1 의 citation 정확성을 paper PDF 본문 직접 inspect 결과 commit. direct text extraction (pdftotext) 으로 verify 한 specific values. --- ## ✅ Verified — v4.5.1 정확값 일치 ### 1. Lang, McManus, Schaur (2019) Health Economics 28(1):44-56 **Verified value**: First-stage F = **18.77** (Table 2, M.3 spec full controls) 본문 발췌:
> "ΔIPW OTH_i... Wk. instrument F stat... 50.76 / 35.95 / **18.77**" → v4.5.1 § 5.4 의 "Lang 2019 F=18.77 published" framing 정확 ✅ ### 2. Pierce-Schott (2020) AERI 2(1):47-64 **Verified framing**: Drug overdose only (suicide + ARLD null) 본문 발췌:
> "an interquartile shift in counties' exposure to PNTR is associated with a relative increase in mortality from overall deaths of despair of **2 to 3 per 100,000**"
> "Within deaths of despair, **the link between PNTR and mortality is driven by drug overdoses**. For this cause of death, an interquartile shift in exposure is also associated with a relative increase of **2 to 3 per 100,000**, a sizable share of the **5 per 100,000 average death rate**"
> "we find **little relationship between PNTR and mortality from either suicide or alcohol-related liver disease (ARLD)**" → v4.5.1 § 1.3 + § 2 정정 framing 정확 ✅ ### 3. Autor, Dorn, Hanson (2019) AERI 1(2):161-178 **Verified value**: D&A point estimate **19.5** (t=2.9) per 100,000 adults per decade 본문 발췌 (Panel B, column 4):
> "The point estimate of **19.5 (t = 2.9)** accounts for **30 percent** of the total contribution of trade shocks to differential male mortality."
> Background mortality rate: 936/100k decade Main result framing:
> "differential and economically large rise in male mortality from drug and alcohol poisoning, HIV/DS, and homicide"
> Title focus: marriage market value of young men → v4.5.1 § 1.3 정정 framing (main = marriage market, secondary = D&A mortality +19.5/100k) 정확 ✅ ### 4. Dippel, Gold, Heblich, Pinto (2017) NBER WP 23209 **Verified citation**: 4번째 author = **Pinto** (Pinkovskiy 아님) **Verified framework spec**:
- Title: "Instrumental Variables and Causal Mechanisms: Unpacking the Effect of Trade on Workers and Voters"
- JEL: F1, F6, J2
- Single-IV mediation: T (treatment), M (mediator), Y (outcome), Z (instrument for T)
- **Assumption A-1**: Z ⊥⊥ T, M, Y (standard IV exclusion restriction generalization)
- 2SLS implementation
- **Frölich-Huber 2017 와의 명시적 대비**: F-H 2017 require "separate dedicated instruments for M, which require additional exogeneity assumptions that are considerably more restrictive"
- Imai-Keele-Yamamoto (2010) 의 Sequential Ignorability Assumption A-3 와 contrast (DGHP 의 single-IV 가 더 generalized) → v4.5.1 § 9.5 의 "DGHP/DFH single-IV mediation, Frölich-Huber 부적용" framing 정확 ✅ ### 5. Eliason, Storrie (2009) Journal of Human Resources 44(2):277-302 **Verified values**:
- Overall male first 4y mortality: HR = **1.44** (95% CI 1.19-1.76)
- **Suicide first 4y**: HR = **2.15** (95% CI 1.28-3.59)
- **Alcohol-related first 4y**: HR = **2.21** (95% CI 1.14-4.31)
- Female: 영향 작거나 not significant → v4.5.1 § 1.3 의 "HR=2.15·2.21 (suicide·alcohol)" 정확 ✅ ### 6. Colantone, Crinò, Ogliari (2019) Journal of International Economics 119:181-207 **Verified value**: **£270/yr** monetary compensation (final published) 본문 발췌:
> "a worker employed in the industry at the 75th percentile [vs 25th] would need a **yearly monetary compensation of £270** to make up for her greater utility loss" → v4.5.1 § 1.3 의 "£270/yr" 정확 ✅ (working paper £200 → published £270) ### 7. McManus, Schaur (2016) Journal of International Economics 102:160-172 **Verified values**:
- Abstract: "injury risk increases by **13%** at the smallest establishments"
- Specific table: "Moving an industry from the 25th to the 75th percentile of Chinese import growth increases injury rates by about **12%** at the smallest decile of plants in the industry and **10%** at the median"
- Welfare equivalent: 1-2% wage reduction → v4.5.1 § 1.3 의 "+12% smallest plant" 정확 (paper Table 1 specific decile estimate) ✅ --- ## ⚠️ Citation 정정 필요 (Finkelstein 2026) ### 8. Finkelstein, Notowidigdo, Shi (2026) BFI WP 2026-33 (또는 NBER WP 34855) **Title**: "Trading Goods for Lives: NAFTA's Mortality Impacts and Implications" **Verified main result** (Abstract):
> "In the 15 years post-NAFTA, an area with average NAFTA exposure experienced an increase in **annual, age-adjusted mortality of 0.68 percent (standard error = 0.19)**" **v4.5.1 의 표기 정정**:
- 이전 (v4.5 + v4.5.1): "+5-9% drug death magnitude (verify pending)"
- **정정 (v4.5.2)**: "+**0.68% age-adjusted mortality** (15 years post-NAFTA, SE 0.19), all-cause not drug-specific" 본 paper 의 main estimate 는 all-cause age-adjusted mortality (0.68%) 이며, "drug death +5-9%" 는 misattribution. drug death 분리 estimate 가 paper 본문에 별도 있는지는 추가 inspect 필요 (Tables 4-5 등). 추가 finding:
> "Mortality increases appear across all broad age by sex groups, but are particularly pronounced among working-age men"
> "declines in local area manufacturing employment increase mortality, while declines in local area non-manufacturing employment decrease mortality" → 본 paper § 1.3 anchor 비교 표 의 Finkelstein row 정정: "+0.68% age-adjusted mortality (15y post-NAFTA), particularly working-age men, all-cause not drug-specific" --- ## Track 4 — P1 sample universe 진단 ### Phase 4 main spec script (`30_phase4_main_spec_5layer.py`) **Source**:
- Mortality: `sigungu_mortality_panel_v02_wa.parquet` (working-age 25-64, Korean-only)
- IV: `iv_z_x_bilateral.parquet` (KR-CN bilateral z_x_h)
- Centroid: `sigungu_centroid_table.csv`
- Crosswalk: `sigungu_crosswalk.csv` **Spec**:
- 5 outcome groups (despair_total + 4 placebo)
- per-outcome pivot_table (h_code × year × log_asr_p1)
- **per-outcome 별 다른 sample size 가능** (Romano-Wolf step-down 의 "different sample sizes allowed") ### n=222 vs n=251 의 진단 → **per-outcome 별 sample size 차이 가능성**: despair_total = 251, cancer = 다른 n, etc. v4.1 의 n=222 는 특정 outcome 의 sample size 일 가능성. v4.5.1 의 n=251 은 despair_total 의 universe. **P1 정확 commit (paper draft 시점)**:
- main spec table 의 outcome 별 정확한 n 명시
- 256 (총 h_code) → 251 (despair_total) drop 5 시군구의 구체 list (paper draft Stage C 에서 출력)
- v4.1 의 n=222 가 어느 outcome 의 sample 인지 derived panel build code 검증 후 commit ### P1 status per-outcome sample 차이 is `known issue` from script structure. Paper draft Stage C 에서 outcome 별 n 표 commit 시 자연스럽게 해결. → § 8.12 limitation 의 "n=222 vs n=251 정합성 pending" framing 그대로 유지. paper draft 시점에 outcome 별 정확한 n 표 commit. --- ## 결론 **Tier A·B 8/9 paper verified**:
- 1-7: v4.5.1 framing 정확 (Lang, PS20, ADH 2019, DGHP, Eliason, Colantone, McManus)
- 8 (Finkelstein): magnitude 표기 정정 필요 (drug-specific +5-9% → all-cause +0.68%) **Sullivan 2009**: abstract 의 50-100% short / 10-15% long / 1.0-1.5y life expectancy loss 정확값 — 이미 v4.5.1 정확. **v4.5.2 patch 항목 (다음 step)**:
- Finkelstein 2026 magnitude 정정: +5-9% drug death → +0.68% all-cause age-adjusted
- 나머지 7편 verified 표기 (no further change) **Author**: 직접 본문 inspect (PDF 9개 본 paper 폴더 보유)
**Date**: 2026-05-05
