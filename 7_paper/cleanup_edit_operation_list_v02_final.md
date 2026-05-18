# Cleanup Edit Operation List — Path A unification (v02 stack final)

_2026-05-06 R-A 직접 작성 (sub-agent file 작성 실패 후 R-A 가 paper 4 file direct read 로 작성)_

**대상**: paper 4 file (§ 1·2 / § 5 / § 6 / § 8·9)
**적용 method**: mechanical find-and-replace + paragraph reverse + footnote insertion
**reference**: cleanup_prompt v02 + v02.1 + v02.2 + v02.3 의 4 patch stack 통합

---

## R-A spot-check verified actual state (cleanup 진행 전 baseline)

| 영역 | 현재 paper 본문 | Path A target | gap status |
|------|---------------|--------------|-----------|
| § 1.2 line 16 main β=-0.127 + cluster/AKM/WCR/RW | native build 정합 | target 정합 | ✅ ALREADY_PATH_A |
| § 1.2 line 16 placebo +0.024 | archive standardized leftover | -0.123 (native CSV) | 🔴 TRUE_GAP |
| § 1.2 line 22 "-6.9 percent" | archive scale | -11.92 percent (native) | 🔴 TRUE_GAP |
| § 1.2 line 36 "From 2000 to 2010—the long-difference period" | window context confusion | trade volume window vs long-difference window 분리 | 🔴 TRUE_GAP |
| § 5.3 Table 2 line 69-70 cancer/cardio | native build (-0.050, -0.070) 정합 | target 정합 | ✅ ALREADY_PATH_A |
| § 6.1 line 21 placebo +0.0238 | archive standardized leftover | -0.123 (native v02 CSV) | 🔴 TRUE_GAP (sign flip) |
| § 6.3 line 47 β_1992=-0.0158, n=210 | archive 또는 별도 spec | -0.0640, n=209 (native v02 CSV) | 🔴 TRUE_GAP (4× magnitude 차이) |

---

## § 1.2 (paper_draft_v01_section_1_2.md) — 3 edit operation

### Op #1 — Line 16 placebo β reverse (TRUE_GAP)

**Find**:
```
the placebo coefficient is +0.024 with the opposite sign of the main estimate and is statistically null
```

**Replace**:
```
the placebo coefficient is -0.123 (cluster-province t = -3.50, p_WCR = 0.0004), with sign aligned to the main estimate; we report this honestly as a placebo failure under the strict pre-WTO activation-timing interpretation and discuss the alternative gradual-integration interpretation in Section 6.1
```

**Reason**: Path A 채택 후 placebo source 가 archive (standardized +0.024) 에서 native v02 CSV (β=-0.123) 로 변경. sign flip + magnitude + interpretation reframe.

### Op #2 — Line 22 percent reduction reverse (TRUE_GAP)

**Find**:
```
The Korean estimate of -6.9 percent mortality decline per standard deviation trade exposure
```

**Replace**:
```
The Korean estimate of -11.92 percent mortality decline per standard deviation trade exposure (computed as 1 − exp(−0.127) under the log-rate specification)
```

**Reason**: archive scale (-6.9%) → native scale (-11.92%) 로 정정. exp 변환 footnote 형식 inline 통합.

### Op #3 — Line 36 long-difference window separation (TRUE_GAP)

**Find**:
```
From 2000 to 2010—the long-difference period of this paper—Korean imports from China grew from approximately USD 12.8 billion to USD 71.6 billion, while Korean exports to China grew from USD 18.5 billion to USD 116.8 billion (UN Comtrade, KOSTAT).
```

**Replace**:
```
The bilateral trade volume between Korea and China grew dramatically over the 2000-2010 integration period — Korean imports from China expanded from approximately USD 12.8 billion to USD 71.6 billion, while Korean exports to China grew from USD 18.5 billion to USD 116.8 billion (UN Comtrade, KOSTAT). To capture the long-run mortality response to this bilateral integration, this paper adopts a long-difference research design with a 21-year window — using 1997-1999 (3-year average) as the pre-integration baseline and 2018-2022 (5-year average) as the post-integration endpoint period. This window length encompasses the full bilateral trade scale-up of 2000-2010 plus the subsequent decade of long-run cumulative mortality response, and is anchored on the 1994 industrial census for the share-weighted Bartik exposure measure.
```

**Reason**: trade volume integration period (2000-2010) ↔ long-difference research design window (1997-1999 ↔ 2018-2022) 의 두 시기 분리 명시. 사용자 audit 의 권고 영역.

---

## § 5 (paper_draft_v01_section_5.md) — Table 2 정합 ✅ + narrative archive leftover

### Op #4 — § 5.3 Romano-Wolf paragraph (TRUE_GAP, 사용자 측 추가 read 필요)

사용자 측 § 5.3 narrative paragraph 의 cancer / cardiovascular inline reference 가 archive 결과 (-0.005 / -0.013) 일 가능성. R-A 가 § 5.3 narrative paragraph 의 actual state 미read — 사용자 측 grep 권고:

```bash
grep -n "cancer.*-0\.005\|cardiovascular.*-0\.013\|cardio.*-0\.013" 7_paper/paper_draft_v01_section_5.md
```

발견 시 native build 결과 (cancer -0.050, cardio -0.070) 로 정정.

### Op #5 — § 5.1 line 14 unit interpretation (TRUE_GAP, optional Footnote X 추가)

paper 본문에 standardized 1-SD interpretation main + native unit footnote 추가 권고. cleanup_prompt v02.1 Patch #2 wording 적용:

> "The regressor of interest is the standardized 1994-baseline Bartik exposure measure z_x_h ... β = -0.127 ... 11.92 percent ... [Footnote X: native unit interpretation + σ_z value 사용자 측 R console 1 line]"

### Op #6 — § 5.1 line 44 WCB→AKM 방어선 honest disclose (INSERT)

cleanup_prompt v02.1 Patch #2 wording 적용:

> "The Webb (2023) 6-point Wild Cluster Restricted bootstrap (WCR; B = 9,999) yields p_WCR < 0.0001. We note that bootstrap inference can be subject to known size distortions in small-G settings (G = 16; Cameron-Gelbach-Miller 2008; Webb 2014); we therefore adopt the AKM (2019) shift-share standard error via the Kolesár (2024) `ShiftShareSE` R package as our primary defense against shift-share-induced inference distortions and report the WCR result as a sensitivity check in Section 5.3 Table 2 and the online appendix."

---

## § 6 (paper_draft_v01_section_6.md) — 3 critical paragraph reverse + footnote insertion

### Op #7 — § 6.1 line 21 placebo paragraph 전체 reverse (TRUE_GAP, sign flip)

**Find** (paragraph approximately around line 19-25):
```
β_placebo = +0.0238 (HC1 SE = 0.0233, t = +1.02, p = 0.31; cluster-province SE = 0.0194, p = 0.22)
```

**Replace** (cleanup_prompt v02.3 Patch #1 wording):
```
β_placebo = -0.123 (HC1 SE = ...; cluster-province SE = 0.0352, t = -3.50, p_WCR = 0.0004) for the deaths-of-despair outcome. The sign aligned with the main estimate (β_main = -0.127) and the comparable magnitude (β_placebo / β_main ≈ 0.97) jointly indicate a placebo failure under the strict activation-timing interpretation. We discuss the alternative interpretation — that the gradual 1992-1996 Korea-China bilateral integration (preceding China's formal WTO accession in 2001) initiated economic exposure dynamics earlier than the 2001 institutional anchor — in this section's discussion below.
```

**Reason**: sign flip (+0.024 → -0.123) + paragraph 전체 reframe. activation-timing strict 해석 약화 + gradual integration interpretation reframe.

### Op #8 — § 6.3 line 47 1992 baseline paragraph 전체 reverse (TRUE_GAP, 4× magnitude)

**Find**:
```
β_1992 = -0.0158 (HC1 SE = 0.0246, t = -0.64, p = 0.52; n = 210; cluster-province SE = 0.0345, p = 0.65)
```

**Replace** (cleanup_prompt v02.2 Patch #2 + v02.3 wording):
```
β_1992 = -0.0640 (winsorized at 99% to remove small-denominator outliers; n = 209 sigungu after winsorize+filter; cluster-province SE = 0.0294, t = -2.18, p_WCR = 0.084), representing a substantial attenuation from the 1994-baseline main β = -0.127. The attenuation factor is approximately 50.4 percent (= -0.0640 / -0.127), reflecting (i) the smaller 1992-baseline sample due to insufficient KSIC 6→9 crosswalk coverage at the early Korean industrial transition period, (ii) winsorization of small-denominator outliers, and (iii) the residual ambiguity in 1992 baseline shares.
```

**Reason**: archive (-0.0158, n=210) → native v02 CSV (-0.0640, n=209) 로 reverse. 4× magnitude 차이 + attenuation factor 50.4% 정합.

### Op #9 — § 6.3 footnote 6 sigungu drop list (INSERT, cleanup_prompt v02.3 Patch #1)

§ 6.3 본문 또는 footnote 형태로 6 sigungu drop disclose 추가:

```
Footnote (§ 6.3 1992 baseline): The drop from 215 sigungu (1992 baseline shares matched with 1997 h_code crosswalk) to 209 sigungu (1992 baseline robustness regression sample for despair_total / cancer / cardiovascular / external_other) reflects the long-difference panel construction requirement — both 1997-1999 base period and 2018-2022 endpoint period mortality data must be present. Five sigungu lack 2018-2022 mortality records and thus drop from all four outcomes: h_code 31090 안산시 (경기도), 31190 용인시 (경기도), 33040 통합청주시 (충청북도), 34010 천안시 (충청남도), and 38110 통합창원시 (경상남도). One additional sigungu (h_code 34070 계룡시 (충청남도)) lacks respiratory-specific mortality data and drops from respiratory only (n=207). The 215 → 209 drop is not driven by the 99% winsorization of z_x outliers, which caps extreme values but preserves all 215 sigungu in the IV.
```

### Op #10 — § 6.X sensitivity bound footnote (INSERT, cleanup_prompt v02.3 Patch #1 sensitivity bound)

archive build sensitivity bound 의 separate footnote (사용자 audit 권고):

```
Footnote: As a sensitivity bound on the main estimate, the archive build (2000-2010 single-year long-difference window) yields β_archive = -0.0685 (HC1 t = -2.12, p = 0.034; n = 222 sigungu), which combined with the 1992-baseline robustness coefficient β_1992-baseline = -0.0640 (winsorized) demonstrates sign-consistent agreement across two distinct long-difference windows and two distinct industrial baseline years. This three-spec convergence reinforces the protective effect interpretation despite the magnitude attenuation under alternative specifications.
```

---

## § 5.5 또는 § 6 — 1.854 ratio sub-section (INSERT)

cleanup_prompt v02 Path A spec 의 1.854 ratio substantive 재해석 wording (사용자 측 § 5.5 또는 § 6 별도 sub-section 적용):

```
The 21-year long-difference window (1997-1999 → 2018-2022) yields a main coefficient β = -0.127, while a shorter 10-year long-difference window (2000-2010, single-year T0/T1) over the same baseline yields β = -0.0685 (sample n = 222). The ratio of approximately 1.85 between these two coefficients reflects the cumulative long-run amplification of the mortality response to bilateral trade exposure: while the 10-year window captures the contemporaneous and short-run mortality dynamics, the 21-year window additionally incorporates the slower-developing long-run cohort effects (occupational disability accumulation, intergenerational scarring, late-onset psychiatric responses to economic precarity) that take a decade or more to manifest in age-standardized mortality. This long-run amplification is consistent with the deaths-of-despair literature (Case-Deaton 2015; Pierce-Schott 2020 long-run window robustness) and with the labor-market scarring literature (Sullivan-Von Wachter 2009; Eliason-Storrie 2009) finding multi-decade persistence of trade-shock-induced unemployment effects.
```

---

## § 3.2 Sample Attrition Table (INSERT, audit point 16)

cleanup_prompt v02.3 Patch #2 의 layout 2 (1994 main + 1992 robustness 별도 cascade) 적용:

```
Table A.1: 1994-baseline (main) sample cascade
| Step | Stage | n |
|------|-------|---|
| 1 | mortality panel raw | 256 |
| 2 | long-difference d_log_panel (4 outcome) | 236 |
| 3 | long-difference d_log_panel (respiratory) | 211 |
| 4 | 1994 baseline shares | 226 |
| 5 | 4 outcome × 1994 baseline IV merge | 222 |
| 6 | respiratory × 1994 baseline IV merge | 198 |

Table A.2: 1992-baseline (robustness) sample cascade
| Step | Stage | n |
|------|-------|---|
| 1 | 1992 baseline shares (raw) | 215 |
| 2 | 1992 4-outcome regression sample | 209 |
| 3 | 1992 respiratory regression sample | 207 |
```

---

## § 8/9 (paper_draft_v01_section_8_9.md) — 사용자 측 추가 read 필요

사용자 측 § 8.3 limitations + § 9 conclusion 의 grep 영역:

```bash
grep -n "0\.0685\|0\.127\|n=222\|n = 222\|6\.9 percent\|11\.9 percent\|From 2000\|2000-2010" 7_paper/paper_draft_v01_section_8_9.md
```

발견된 line 의 archive leftover reference 가 native build target 으로 정합되도록 cleanup. cleanup_prompt v02 의 § 8.3.1 + § 9 wording 적용.

---

## Summary

**Total edit operations (R-A direct read 기반)**:
- § 1.2: 3 TRUE_GAP edits
- § 5: 1 confirmed Table 2 정합 + 3 추가 영역 (사용자 측 grep 권고)
- § 6: 3 critical paragraph reverse + 2 footnote insertion
- § 5.5/§ 6: 1 sub-section insert
- § 3.2: 1 Table insert (Sample Attrition cascade layout 2)
- § 8/9: 사용자 측 grep 영역 (R-A 미read)

**Estimated commit time**: 30-60 분 (mechanical paste + paragraph reverse)

---

## 사용자 측 commit 영역

1. § 1.2 의 3 edit (Op #1·#2·#3) — mechanical find-and-replace
2. § 5 의 narrative grep + cancer/cardio inline reference 정합 verify
3. § 5.1 line 14 Footnote X 추가 (σ_z native unit, R console 1 line verify)
4. § 5.1 line 44 WCB→AKM 방어선 wording (Op #6)
5. § 6.1 placebo paragraph 전체 reverse (Op #7) — sign flip + native -0.123
6. § 6.3 1992 baseline paragraph 전체 reverse (Op #8) + 6 sigungu drop footnote (Op #9)
7. § 6.X sensitivity bound footnote (Op #10)
8. § 5.5 또는 § 6 별도 sub-section: 1.854 ratio substantive disclose (INSERT)
9. § 3.2 Sample Attrition Table 의 layout 2 (Table A.1 + A.2 별도 cascade)
10. § 8/9 의 사용자 측 grep 후 archive leftover reverse

---

## R-A 한계 시인

1. § 5.3 narrative paragraph + § 8.9 의 archive leftover line 은 R-A 가 직접 read 안 함 — 사용자 측 grep 권고로 분리.
2. § 5.1 Footnote X 의 σ_z 정확 값은 사용자 측 R console 1 line verify 영역.
3. Op #7 (§ 6.1 placebo paragraph) 의 surrounding context (line 19-25) 의 정확 paragraph boundary 는 사용자 측 read 후 결정.
4. Op #8 (§ 6.3 1992 baseline) 의 surrounding context (line 45-55) 의 정확 paragraph boundary 도 사용자 측 결정.
