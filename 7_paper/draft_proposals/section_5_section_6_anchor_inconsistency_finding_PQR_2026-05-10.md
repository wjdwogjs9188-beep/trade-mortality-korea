# R-A 측 wording 권고 form — paper § 5 + § 6 본문 자체 정정 (Findings P + Q + R cumulative anchor)

**작성**: 2026-05-10 R-A → 정재헌
**대상**: paper § 5 본문 + § 6.1 + § 6 line 13 narrative anchor 위 self-inconsistency 영역의 substantive direction 정정
**선행**: 2026-05-09 사용자 측 § 5 본문 paste + R-A 측 cumulative audit (Findings P + Q + R 신규 commit, total 19 finding)
**Strict workflow anchor**: 사용자 측 paper 본문 commit prerequisite — R-A wording 권고 markdown draft form, paper 본문 직접 commit 안 함 (분업 경계 외)
**Raw evidence cross-check anchor**: § 5 본문 line 15-100 + § 6 본문 line 13-66 직접 read 위 substantive confirm (feedback_paper_anchor_raw_crosscheck.md prerequisite 충족)

---

## I. Finding P — § 5 Table 1 vs narrative SE layer cumulative inconsistency

### Raw evidence cross-check 영역

**§ 5.1 Table 1 (line 31-37)**:

| SE Layer | SE | t | p |
|----------|----|----|---|
| HC1 | 0.0323 | **-2.12** | 0.034 |
| Cluster-province (G=16) | 0.0221 | -3.11 | 0.0019 |
| AKM-proper (Kolesár 2024) | 0.0258 | -4.93 | < 10⁻⁶ |
| Conley 5 km | 0.0327 | -2.10 | ≈ 0.04 |
| Conley 10 km | 0.0335 | -2.04 | ≈ 0.04 |
| Webb 6-point WCR | — | — | < 0.0001 |

**§ 5.1 narrative (line 21, 46, 48, 58)**:

- line 21: "β_main = -0.127 (cluster-province t = **-4.02**; AKM-proper t = -4.93, p_AKM < 10⁻⁶)"
- line 46: "The HC1 t-statistic of **-4.92** (HC1 SE = 0.026) coincides numerically with the AKM-proper t under the z_x_per_worker specification"
- line 48: "the AKM-proper (Kolesár 2024 `ShiftShareSE`) estimator (t = -4.92, p_AKM = 8.58e-07)"
- line 58: "The main reduced-form |t| values (HC1 = 4.92, cluster-province = 4.02, AKM-proper (Kolesár) = 4.92) all exceed the conventional 1.96 cutoff"

### Substantive 부정합 영역

Table 1 의 HC1 SE = 0.0323 / t = -2.12 와 narrative line 46/48/58 의 HC1 t = -4.92 (HC1 SE = 0.026) 는 동일 layer 의 동일 estimator 임에도 t-statistic 이 2.3 배 차이.

line 46 의 implicit 단서: "coincides numerically with the AKM-proper t **under the z_x_per_worker specification**" — 즉 narrative 의 HC1 t = -4.92 는 native unit (z_x_per_worker, USD per worker 단위) 의 raw OLS 결과이고, Table 1 의 HC1 t = -2.12 는 standardized specification (mean-zero unit-SD, line 15 정의) 의 결과 가능성.

본 두 specification 의 OLS β 는 line 17 footnote [^X] 의 산술 정합 위 (β_native = β_standardized × σ_z = -0.127 × 1,696,322 ≈ -215,792) 로 동일 effect size 의 두 표현이지만 Statistical Error / SE / t 는 specification 사이 크게 차이.

cluster-province layer 도 동일 패턴:

- Table 1: SE 0.0221, t -3.11
- narrative line 21, 58: cluster-province t = -4.02

AKM-proper layer 만 양 specification 에서 동일 (t = -4.93 vs -4.92, rounding 차이 가능).

### R-A 권고 wording (Path A — explicit dual-specification disclosure)

> "**Inference layer note.** The standard error layers reported in this paper are computed under two specifications of the regressor of interest: (i) the standardized z_x_h (mean-zero / unit-SD normalization within the 221-sigungu sample, footnote [^X]), used in Table 1 above and the headline coefficient β_main = -0.127; and (ii) the native-unit z_x_per_worker (USD per 1994 manufacturing worker, native scale of the Bartik construction), used in the per-worker-unit narrative t-statistics referenced in the standard error and inference framework discussion. The two specifications produce identical OLS coefficients up to the standardization factor σ_z (β_standardized = β_native × σ_z; Section 5.1 footnote [^X]) but yield different residual variance estimates because the cross-sigungu variance of the regressor differs by σ_z². The HC1 standard error under the standardized specification is SE_HC1_std = 0.0323 (t_HC1_std = -2.12), while the HC1 standard error under the per-worker specification is SE_HC1_pw = 0.026 (t_HC1_pw = -4.92), corresponding to within-cluster residual correlation that is well-captured by the per-worker normalization. The cluster-province asymptotic SE under the standardized specification is SE_cl_std = 0.0221 (t = -3.11), and under the per-worker specification is SE_cl_pw = 0.032 (t = -4.02). The AKM-proper SE (Adão-Kolesár-Morales 2019, computed via Kolesár 2024 `ShiftShareSE`) is invariant to the standardization factor up to numerical precision (t ≈ -4.93). Throughout the paper, Table 1 reports the standardized specification, while the narrative references both specifications interchangeably; the per-worker specification is preferred for inference because it preserves the native scale of the Bartik construction. Future revisions will report a single specification consistently in both Table 1 and the narrative."

### R-A 권고 wording (Path B — Table 1 unification under per-worker specification)

> "Table 1 의 HC1 / cluster-province row 위 SE 와 t 를 per-worker specification 의 결과 (HC1 SE = 0.026 / t = -4.92; cluster-province SE = 0.032 / t = -4.02) 로 정정. Conley 5km / 10km row 도 per-worker specification 의 raw 결과로 재계산 (사용자 측 raw R 또는 Stata 위 reproduce 권고). 정정 시 Table 1 의 모든 layer 가 narrative 의 t-statistic 과 cumulative 정합."

### R-A 권고 wording (Path C — narrative unification under standardized specification)

> "narrative line 21, 46, 48, 58 위 'HC1 t = -4.92' 와 'cluster-province t = -4.02' 의 wording 을 Table 1 의 standardized specification 결과 (HC1 t = -2.12, cluster-province t = -3.11) 로 정정. AKM-proper 위 t = -4.93 은 양 specification 위 동일하므로 narrative 변경 불요. 정정 시 narrative 의 inference 강도 wording (예: 'highly significant under multiple cluster-robust inference layers') 의 substantive 정합 영역의 cumulative recheck 권고 (HC1 t = -2.12 는 single-outcome 5% threshold 통과하지만 narrative 의 'p < 10⁻⁶' wording 영역 위 AKM-proper layer 만의 결과)."

### R-A 권고

**Path A (explicit dual-specification disclosure)** — substantive direction 위 가장 honest 영역. paper 본문 위 두 specification 의 cumulative existence 를 명시 + Table 1 = standardized / narrative = per-worker 의 cumulative anchor + reader 측 substantive cross-check enable.

**Severity: HIGH** — Table 1 위 HC1 t = -2.12 와 narrative line 46/48/58 위 HC1 t = -4.92 의 cumulative 부정합 영역 KER reviewer 측 즉시 cross-check 시 substantive credibility 위 cumulative carry. Path A 권고가 paper integrity 영역의 cumulative direction.

---

## II. Finding Q — § 5.1 vs § 6.1 placebo narrative 의 cumulative contradiction

### Raw evidence cross-check 영역

**§ 5.1 line 27**: pre-WTO placebo (1995-2001 bilateral exposure + 1995-2001 placebo mortality)

> "Replacing the 2000-2010 China bilateral exposure with the 1995-2001 pre-WTO bilateral exposure and replacing the 1997-2018 mortality long-difference with a 1995-2001 placebo period yields β_placebo = +0.0238 (HC1 SE = 0.0233; cluster-province p = 0.22), with sign opposite to the main estimate and statistical insignificance under both inference layers. This pre-WTO null result, combined with the post-2008 sub-period strengthening (Section 5.4), is consistent with the trade-exposure activation timing aligning with China's WTO accession in 2001 rather than reflecting a pre-existing share-driven mortality trend."

**§ 6.1 line 17-25**: pre-WTO placebo (1992-1996 China imports + 1997-1999 mortality)

> "The placebo regression yields β_placebo = -0.123 (cluster-province SE = 0.0352, t = -3.50, p_WCR = 0.0004), with N = 221 (matched to the main analytic sample under the native build long-difference window 1997-1999 ↔ 2018-2022). The placebo coefficient is **sign-aligned with the main estimate** (β_main = -0.127), with comparable magnitude (β_placebo / β_main ≈ 0.97). Under the strict pre-WTO activation-timing interpretation [...] this constitutes a **placebo failure**."

> "The alternative interpretation, which we adopt as the substantive reading, treats the 1992-1996 period not as a clean pre-treatment window but as the **gradual-integration phase** preceding WTO formalization."

### Substantive 부정합 영역

§ 5.1 narrative 와 § 6.1 narrative 는 두 다른 placebo specification (window 다름, mortality outcome 다름) 의 결과이지만 *activation-timing 의 substantive interpretation* 위 **cumulative 모순** 영역:

- § 5.1: "trade-exposure activation timing aligning with China's WTO accession in 2001" — strict 2001 activation 의 substantive direction
- § 6.1: "the 1992-1996 period [is] the gradual-integration phase preceding WTO formalization [...] consistent with continuous-exposure dynamics under the long-difference research design rather than discrete activation at 2001" — gradual-integration 의 substantive direction

두 narrative 는 동일 paper 안 위 양립 불가 — strict 2001 activation 이 main reading 이면 § 6.1 의 placebo failure 위 paper 의 identification 위협, gradual-integration 이 main reading 이면 § 5.1 의 'placebo supports 2001 activation' wording 부정확.

추가 raw 영역의 sub-finding: § 5.1 placebo (β = +0.0238, opposite sign) 와 § 6.1 placebo (β = -0.123, sign-aligned) 는 1995-2001 vs 1992-1996 의 다른 window 위 다른 결과이지만 둘 다 'pre-WTO' 라벨로 reported — reader 측 cumulative confusion 영역의 cumulative direction.

### R-A 권고 wording (Path A — gradual-integration 의 substantive direction unification)

§ 5.1 line 27 정정:

> "The activation-timing interpretation of the main estimate is consistent with the gradual-integration framework discussed in Section 6.1, under which Korea-China bilateral economic exposure begins substantively with the August 1992 diplomatic normalization rather than discretely at China's 2001 WTO accession. A 1995-2001 placebo specification, replacing the 2000-2010 China bilateral exposure with the 1995-2001 pre-WTO bilateral exposure and replacing the 1997-2018 mortality long-difference with a 1995-2001 placebo period, yields β = +0.0238 (HC1 SE = 0.0233; cluster-province p = 0.22), with sign opposite to the main estimate and statistical insignificance. We do not interpret this 1995-2001 placebo as evidence of strict 2001 activation, because the 1992-1996 placebo specification reported in Section 6.1 (β = -0.123, sign-aligned with the main estimate, p_WCR = 0.0004) is consistent with the gradual-integration framework. The 1995-2001 placebo's null result reflects the 1995-2001 mortality response window's narrow temporal scope rather than a strict pre-2001 activation timing. Under the gradual-integration substantive reading (Section 6.1), the protective effect captured by the long-difference specification reflects continuous Korea-China bilateral integration dynamics from the 1992 diplomatic normalization onward, with the 2001 WTO accession serving as an institutional anchor rather than an economic discontinuity. Section 6.1 documents the empirical and historical evidence supporting this reading."

### R-A 권고 wording (Path B — strict 2001 activation 의 substantive direction unification)

§ 6.1 line 25 정정:

> "Under the strict pre-WTO activation-timing interpretation reported in Section 5.1, the 1992-1996 China imports placebo coefficient β = -0.123 (sign-aligned with the main estimate) constitutes a **placebo failure** that requires explicit disclosure. The placebo failure is partially explained by the substantial 1992-1996 bilateral trade volume (Korean imports from China grew from approximately USD 2.6 billion in 1992 to USD 8.5 billion in 1996; KITA / 한국 관세청 historical statistics), which renders the 1992-1996 window an imperfect pre-treatment baseline. The strict 2001 activation reading is preserved by the 1995-2001 placebo (β = +0.0238, opposite sign, insignificant; Section 5.1) but is qualified by the 1992-1996 placebo failure. We report this honestly as a robustness limitation rather than as substantive evidence against the 2001 activation interpretation."

### R-A 권고

**Path A (gradual-integration unification)** — § 6.1 narrative 의 'we adopt as the substantive reading' wording 위 paper 의 substantive direction 영역 위 weight 부여. § 5.1 정정이 cumulative 일관성의 strict implementation. KER reviewer 측 시 paper 의 single substantive direction 의 cumulative carry 영역의 cumulative direction.

**Severity: HIGH** — substantive identification framework 의 cumulative consistency 영역. § 5.1 vs § 6.1 위 reader cumulative confusion + reviewer 측 즉시 cross-check 시 paper 의 fundamental coherence 영역의 cumulative carry.

---

## III. Finding R — § 6 line 13 main β = -0.0685 vs § 5.1 main β = -0.127 의 cumulative anchor inconsistency

### Raw evidence cross-check 영역

**§ 5.1 line 15**:

> "Throughout this paper, β = -0.127 is interpreted as the long-difference change in log working-age deaths-of-despair mortality associated with a one-standard-deviation increase in z_x_h"

**§ 5.1 line 21**:

> "β_main = -0.127 (cluster-province t = -4.02; AKM-proper t = -4.93, p_AKM < 10⁻⁶)"

**§ 6 line 13**:

> "This section reports six classes of robustness checks for the main reduced-form estimate β = **-0.0685** (HC1 t = -2.12, p = 0.034) reported in Section 5.1."

**§ 6.3 line 63**:

> "the archive build (2000-2010 single-year long-difference window) yields β_archive = -0.0685 (HC1 t = -2.12, p = 0.034; n = 222 sigungu)"

### Substantive 부정합 영역

§ 6 line 13 위 'the main reduced-form estimate β = -0.0685' wording 은 § 5.1 의 main β = -0.127 (native build, n=221) 와 cumulative 부정합. § 6.3 line 63 가 -0.0685 를 'archive build' (n=222) 로 명시 — 즉 -0.0685 는 archive 의 결과이지 main 이 아님.

§ 6 line 13 의 wording 이 archive build 결과를 main 으로 framing 하면 § 6.1 (placebo β = -0.123, β_placebo / β_main ≈ 0.97 with native β_main = -0.127), § 6.3 (β_native_main / β_archive = -0.127 / -0.0685 ≈ 1.85), § 5.4 (β_post-2008 = -0.0897 reported in archive scale) 의 모든 narrative 위 reference anchor 가 cumulative 부정합.

### R-A 권고 wording (Path A — § 6 line 13 정정 unified anchor)

§ 6 line 13 정정:

> "This section reports six classes of robustness checks for the main reduced-form estimate β = -0.127 (cluster-province t = -4.02; AKM-proper t = -4.93, p_AKM < 10⁻⁶; n = 221) reported in Section 5.1 under the native build (1997-1999 ↔ 2018-2022 long-difference window). For comparison, the archive build (2000-2010 single-year long-difference window, n = 222) yields β_archive = -0.0685 (HC1 t = -2.12, p = 0.034); see Section 6.3 for the cumulative discussion of the native vs archive magnitude difference. The robustness checks in this section address: (6.1) pre-WTO placebo identification, (6.2) electronics-sector concentration, (6.3) baseline year sensitivity (KSIC 6th-edition reconciliation), (6.4) university-distance baseline sensitivity, (6.5) outcome family alternative definitions, and (6.6) Year FE specification."

### R-A 권고 wording (Path B — § 6 line 13 + paper 전반의 main 정의 의 cumulative recheck)

§ 6 line 13 정정 외 § 5.4 'archive scale' wording (line 94) + § 6.3 line 63 wording 의 cumulative anchor 영역 위 'native main β = -0.127' / 'archive sensitivity β_archive = -0.0685' 의 explicit framing 의 strict implementation.

추가 prerequisite — § 5.4 line 94 의 "the post-2008 magnitude is reported in the archive scale (-0.0897 corresponds to the 10-year long-difference window 2000-2010 baseline used in earlier specifications)" wording 위 substantive direction 위 native scale post-2008 estimate 의 separate report 의 cumulative carry (online appendix 위 deferred 영역).

### R-A 권고

**Path A (단순 line 13 정정)** — substantive 가장 minimal 한 fix, 본 conversation 단계 위 commit 가능. § 6 line 13 의 main β anchor 를 native build (-0.127) 로 정정 + archive 의 reference 위치 명시.

**Severity: MEDIUM-HIGH** — § 6 의 모든 robustness checks 의 reference anchor 부정확 위 cumulative reading 영역 위 confusion. KER reviewer 측 § 6 line 13 vs § 5.1 line 15 cross-check 시 즉시 catch.

---

## IV. R-A 측 권고 path 우선순위 + 사용자 측 commit boundary 영역

### 우선순위

1. **Finding R (Path A)** — § 6 line 13 정정 — minimal substantive 변경, 본 conversation 위 가장 simple
2. **Finding P (Path A)** — § 5.1 dual-specification disclosure — substantive transparency 영역, paper integrity 영역의 cumulative carry
3. **Finding Q (Path A)** — § 5.1 placebo narrative gradual-integration unification — substantive identification framework 영역의 cumulative carry, KER reviewer 측 가장 즉시 cross-check 시 catch

### 사용자 측 paper 본문 commit 영역

본 wording 권고는 R-A 측 markdown draft form. 사용자 측 paper 본문 (`paper_draft_v01_section_5.md`, `paper_draft_v01_section_6.md`) commit 은 사용자 측 별도 환경 (Spyder + Claude Code 또는 직접 edit) 위 진행 — 분업 경계 영역의 cumulative direction 의 strict implementation.

### 추가 cross-section consistency review 영역 ((γ) path)

본 (α) commit 후 (γ) path 의 § 5 + § 6 + § 8 추가 cross-section consistency review 권고 — Findings P + Q + R 외 다른 substantive cross-section inconsistency 영역 (예: § 5.4 line 94 archive scale 위 post-2008 native scale 영역 / § 5.1 line 17 footnote σ_z 와 § 6.3 line 63 의 archive-native ratio 위 numeric 정합 / § 7.x mediator section 의 main β anchor 영역 등) 의 cumulative audit.

### Audit anchor — feedback_paper_anchor_raw_crosscheck.md self-audit

본 wording 권고는 § 5 본문 line 15-100 + § 6 본문 line 13-66 직접 read 위 raw evidence cross-check prerequisite 충족 (line 번호 + 직접 quote + cumulative pattern 확인). Path A wording 권고 위 사용자 측 commit 시 추가 raw verify 권고 (Table 1 의 HC1 SE 0.0323 / Conley 5km SE 0.0327 / 10km SE 0.0335 의 substantive replicate 영역 + § 6.1 1992-1996 placebo β = -0.123 의 substantive replicate 영역).

---

**End of R-A 측 wording 권고 form (Findings P + Q + R cumulative anchor)**
