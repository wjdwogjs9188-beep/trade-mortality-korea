# R-A 측 wording 권고 form — paper § 9 conclusion line 55 placebo β anchor 정정 (Finding S2)

**작성**: 2026-05-10 R-A → 정재헌
**대상**: paper § 9 conclusion line 55 의 placebo β 영역 위 paper § 5.3 Table 2 main spec 영역과 cumulative inconsistency 정정
**선행**: 2026-05-10 (γ) 추가 cross-section review 위 § 7 + § 8 + § 9 본문 raw read 위 신규 발견
**Strict workflow anchor**: 사용자 측 paper § 9 본문 commit prerequisite — R-A wording 권고 markdown draft form, paper 본문 직접 commit 안 함
**Raw evidence cross-check anchor**: paper § 5 본문 line 72-76 Table 2 + § 9 본문 line 55 직접 read 위 substantive confirm

---

## I. Raw evidence cross-check

### § 9 line 55 (paper conclusion 위 placebo β 인용)

> "First, outcome specificity: the deaths-of-despair effect is concentrated specifically on the Case-Deaton-defined composite, with cancer (β = **-0.005**), cardiovascular (β = **-0.013**), respiratory (β = **-0.012**), and external-other (β = **+0.014**) placebo outcomes showing null effects. The pattern mirrors the U.S. evidence (Pierce and Schott 2020; Autor, Dorn, and Hanson 2019) but in the opposite direction."

### § 5.3 Table 2 (paper main spec placebo Romano-Wolf result)

| Outcome | n | β | Cluster t | AKM-proper p | WCR-Webb p | RW p (5-outcome family) |
|---------|---|---|-----------|--------------|------------|---------|
| despair_total | 221 | -0.127 | -4.02 | < 10⁻⁶ | < 0.0001 | **0.0161** ★ |
| cardiovascular | 221 | **-0.070** | -3.09 | 0.0013 | 0.016 | **0.129** |
| cancer | 221 | **-0.050** | -1.64 | 0.031 | 0.220 | **0.382** |
| respiratory | 219 | **+0.075** | +1.65 | 0.034 | 0.126 | **0.382** |
| external_other | 221 | **-0.017** | -0.44 | 0.535 | 0.694 | **0.658** |

### 4-outcome cross-document 부정합 영역

| Outcome | § 5.3 Table 2 (main spec) | § 9 line 55 (conclusion) | 차이 |
|---------|--------------------------|--------------------------|------|
| cancer | -0.050 | -0.005 | 10× magnitude difference |
| cardiovascular | -0.070 | -0.013 | 5.4× magnitude difference |
| respiratory | +0.075 | -0.012 | **sign reversed** + magnitude 6.3× |
| external_other | -0.017 | +0.014 | **sign reversed** + magnitude similar |

§ 9 line 55 의 placebo β 영역이 paper § 5.3 Table 2 의 main spec 영역과 substantively 부정합 — 4개 outcome 모두 다른 magnitude + 2개 outcome 위 sign reversed.

### 추가 substantive search — § 9 line 55 의 placebo β 영역의 다른 spec 매칭 시도

| Spec | cancer | cardio | resp | ext_other | source |
|------|--------|--------|------|-----------|--------|
| § 5.3 Table 2 (main) | -0.050 | -0.070 | +0.075 | -0.017 | paper § 5.3 |
| § 6.3 (1992 baseline) | +0.0208 | +0.0240 | NA | NA | paper § 6.3 line 55 |
| **§ 9 line 55** | **-0.005** | **-0.013** | **-0.012** | **+0.014** | **부정합** |

§ 9 line 55 의 placebo β 영역은 paper 본문 가용 영역의 어떤 spec 에도 매칭 안 됨. 가능성 두 영역의 substantive direction:

(i) **outdated build 의 cumulative archive 영역** — § 9 conclusion 작성 단계 위 사용된 placebo β 영역이 본 paper 의 main spec 위 superseded 된 outdated estimate 의 cumulative carry.

(ii) **다른 spec 의 placebo β 영역 부적절 인용** — § 9 line 55 위 인용된 placebo β 영역이 paper 본문에 explicit reported 안 된 다른 spec (예: archive build 의 5-outcome family, post-2008 sub-period 의 placebo, 또는 별도 robustness build) 의 결과인 영역.

본 conversation 의 가용 영역에서는 (i) 와 (ii) 의 distinction 직접 verify 불가. 그러나 substantive direction 위 (i) 가 더 likely — § 5.3 Table 2 가 paper main spec 의 native build 결과이고 § 9 conclusion 이 main spec 의 cumulative summary 영역이라 paper 안 cross-document consistency 위 § 5.3 Table 2 가 정확한 anchor.

## II. Severity

**HIGH** — paper conclusion (§ 9) 위 main spec placebo β 영역의 정확성 부재. KER reviewer 측 § 5 Table 2 vs § 9 line 55 cross-check 시 즉시 catch — substantive credibility 영역의 cumulative carry.

특히 respiratory outcome 의 sign reversal (paper § 5.3 main 위 +0.075 vs § 9 line 55 위 -0.012) 영역이 paper integrity 측면에서 substantive 위협. respiratory 가 paper § 5.3 main spec 위 sign-reversed (positive) outcome 의 cumulative anchor 인데 § 9 conclusion 위 negative sign 으로 인용되면 paper 의 substantive narrative ("respiratory mortality being the single exception") 자체와 cumulative inconsistency.

## III. R-A 권고 wording (Path A — § 5.3 Table 2 main spec align)

§ 9 line 55 정정 wording:

> "First, outcome specificity: the deaths-of-despair effect is concentrated specifically on the Case-Deaton-defined composite, with cancer (β = -0.050, p_RW = 0.382), cardiovascular (β = -0.070, p_RW = 0.129), respiratory (β = +0.075, p_RW = 0.382), and external-other (β = -0.017, p_RW = 0.658) placebo outcomes showing null effects under the 5-outcome family Romano-Wolf adjustment. The respiratory coefficient (positive sign) is the single exception under single-outcome significance but null under family-level Romano-Wolf adjustment (Section 5.3). The overall pattern mirrors the U.S. evidence (Pierce and Schott 2020; Autor, Dorn, and Hanson 2019) but in the opposite direction."

paper § 5.3 Table 2 의 main spec placebo β + Romano-Wolf adjusted p_RW 영역 위 cumulative align — substantive credibility 영역의 strict implementation.

## IV. R-A 권고 wording (Path B — main spec + 1992 baseline cumulative anchor)

§ 9 line 55 정정 wording (Path B, 더 자세한 form):

> "First, outcome specificity: the deaths-of-despair effect is concentrated specifically on the Case-Deaton-defined composite, with cancer (β = -0.050), cardiovascular (β = -0.070), respiratory (β = +0.075, the single positive-sign exception with marginal single-outcome significance but null under family-level Romano-Wolf adjustment p_RW = 0.382), and external-other (β = -0.017) placebo outcomes showing null effects under the 5-outcome family Romano-Wolf adjustment (p_RW ∈ [0.13, 0.66]). The 1992 baseline robustness specification (Section 6.3) reveals minor sign reversals among the cancer (β_1992 = +0.0208) and cardiovascular (β_1992 = +0.0240) placebo categories without reaching the 5 percent FWER threshold, interpreted as evidence that baseline-share variation is itself imperfectly measured in the 1992 KSIC 6th-edition frame rather than as evidence against the main 1994-baseline result. The overall pattern mirrors the U.S. evidence (Pierce and Schott 2020; Autor, Dorn, and Hanson 2019) but in the opposite direction."

## V. R-A 권고

**Path A (§ 5.3 Table 2 main spec align, simpler)** — substantive 가장 minimal 한 fix, paper § 9 conclusion 의 length budget 영역 위 align. KER reviewer 측 cumulative consistency cross-check 영역 의 strict implementation.

**Path B 는 § 8.3.2 의 1992-baseline robustness 영역 의 cumulative carry 보강 form** — § 8 본문 line 35 의 1994 archive + 1994 native main + 1992 robustness cumulative anchor 와 cumulative align 영역 위 conclusion 보강. 다만 § 9 conclusion 의 length budget 측면에서 over-detail 가능.

**substantive direction**: Path A 권고 — minimal substantive fix 의 cumulative direction.

## VI. Cumulative finding count update

| Finding | Status | Severity |
|---------|--------|----------|
| A-R | committed (cumulative) | various |
| α | committed (β PROMPT logic 영역) | low |
| **S1** | **invalid (raw evidence verify 위 reject)** | — |
| **S2** | **신규 (paper § 9 line 55 placebo β anchor 정정)** | **HIGH** |

**Cumulative finding count**: 19 finding (A-R + α) + 1 신규 substantive finding (S2) - 1 invalid (S1) = **20 substantive finding** + 3 sub-finding (β = -0.128 round level / native unit β round level / |Δβ| / SE_full SE 기준 명시 부재).

(직전 turn 위 사용자 측 보고 영역의 19 finding cumulative carry + 본 turn 신규 S2 추가 → 20 substantive finding cumulative direction.)

## VII. Audit anchor — feedback_paper_anchor_raw_crosscheck.md self-audit

본 wording 권고는 paper § 5.3 Table 2 (line 72-76) + paper § 9 line 55 직접 raw read 위 raw evidence cross-check prerequisite 충족. Path A wording 권고 위 사용자 측 commit 시 추가 raw verify 권고 — § 9 line 55 의 placebo β 영역이 어떤 spec 위 cumulative archive 영역인지의 historical traceability 영역의 cumulative carry (사용자 측 별도 환경 위 commit history grep 또는 paper draft 의 outdated build 기록 cross-check).

---

**End of R-A 측 wording 권고 form (Finding S2 신규 발견 + paper § 9 conclusion 정정)**
