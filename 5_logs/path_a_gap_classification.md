# Path A Gap Re-Classification: Revised Unification Status **Date**: 2026-05-06 **Scope**: 4 paper draft files (§ 1-2, § 5, § 6, § 8-9) **Methodology**: Context-aware reading + 3-category framework (TRUE_GAP / LEGITIMATE_ROBUSTNESS / AMBIGUOUS) --- ## Summary Counts | Category | Count | Per-File |
|----------|-------|----------|
| **A_TRUE_GAP** | **6** | § 1-2: 1, § 5: 5, § 6: 1, § 8-9: 0 |
| **B_LEGITIMATE_ROBUSTNESS** | **11** | § 1-2: 1, § 5: 3, § 6: 4, § 8-9: 3 |
| **C_AMBIGUOUS** | **1** | § 1-2: 0, § 5: 0, § 6: 1, § 8-9: 0 |
| **TOTAL** | **18** | — | ### Revised Completion Status - **FALSE POSITIVES (LEGITIMATE)**: 11 of 18 references (61%) are properly contextualized as archive build robustness or supporting narrative—should NOT be touched
- **TRUE CLEANUP GAPS**: 6 references (33%) require mechanical β=-0.0685 → β=-0.127 updates
- **AMBIGUOUS**: 1 reference (6%) needs context judgment **Revised TRUE completion %**: 49% × (6/18) = **16.3% actual cleanup need** (not 49% of all references) --- ## A. TRUE_GAP List (6 cleanup actions, priority order) ### Priority 1 (Highest visibility — main text) **1. § 5, line 42** — "The OLS point estimate β = -0.0685 is invariant..."
- **File**: `paper_draft_v01_section_5.md`, line 42
- **Current text**: "The OLS point estimate β = -0.0685 is invariant across the standard error layers by construction (SE layers affect inference but not the OLS coefficient)"
- **Issue**: § 5.1 context shows this is ARCHIVE build discussion (Table 1 rows below claim main β=-0.127). Transition text incorrectly generalizes archive coefficient as "the" OLS point estimate
- **Fix**: Replace "-0.0685" with "-0.127" OR clarify this is sub-section on archive-build robustness layer
- **Recommendation**: REPLACE with "-0.127"; this section should document MN inference layer table ### Priority 2 (Explicit main specification claim) **2. § 5, line 56** — "This paper proceeds with the reduced-form coefficient β_main = -0.0685 as the preferred specification"
- **File**: `paper_draft_v01_section_5.md`, line 56
- **Current text**: "This paper proceeds with the reduced-form coefficient β_main = -0.0685 as the preferred specification, following the convention..."
- **Issue**: DIRECT contradiction of Path A. Section 5.1 (line 19) clearly states β_main = -0.127. This line appears to be legacy Path B wording
- **Fix**: Replace "-0.0685" with "-0.127" AND update supporting text to acknowledge weak-IV context but recommit to reduced-form inference
- **Recommendation**: REPLACE & REWRITE introductory sentence to match Path A decision ### Priority 3 (Outcome specificity claim) **3. § 5, line 76** — "The deaths-of-despair coefficient (-0.0685) is the largest in absolute magnitude..."
- **File**: `paper_draft_v01_section_5.md`, line 76
- **Current text**: "The deaths-of-despair coefficient (-0.0685) is the largest in absolute magnitude among the five outcomes. Cancer (β = -0.005), cardiovascular (β = -0.013)..."
- **Issue**: Repeats archive coefficient as if it were the outcome-specificity main result. Table 2 (line 68) reports β=-0.127 for despair_total. This is mechanical copy-paste from archive build
- **Fix**: Replace all four β values in this paragraph with Path A native estimates
- **Recommendation**: REPLACE "-0.0685" with "-0.127" AND update cancer/cardiovascular/respiratory/external coefficients from Path A Table 2 ### Priority 4 (Section intro) **4. § 6, line 13** — "This section reports six classes of robustness checks for the main reduced-form estimate β = -0.0685"
- **File**: `paper_draft_v01_section_6.md`, line 13
- **Current text**: "This section reports six classes of robustness checks for the main reduced-form estimate β = -0.0685 (HC1 t = -2.12, p = 0.034)"
- **Issue**: § 6 is explicitly ROBUSTNESS section. Intro conflates "robustness checks FOR the main estimate" with "checks ON archive build". The HC1 t=-2.12 and p=0.034 correspond to archive build, not main. Path A main would yield HC1 t > -4.0 (much larger)
- **Fix**: Clarify that § 6 reports robustness to the MN β=-0.127, with HC1 t and p-values updated accordingly
- **Recommendation**: REWRITE section intro to reference main estimate correctly and update inference layer p-values ### Priority 5 (Main specification period) **5. § 1_2, line 36** — "From 2000 to 2010—the long-difference period of this paper"
- **File**: `paper_draft_v01_section_1_2.md`, line 36
- **Current text**: "From 2000 to 2010—the long-difference period of this paper—Korean imports from China grew from approximately USD 12.8 billion..."
- **Issue**: Describes 2000-2010 as "the long-difference period of this paper" but Path A main outcome period is 1997-1999 BASE to 2018-2022 ENDPOINT (25 years, not 10). The 2000-2010 window is the SHOCK identification period (Bartik construction), not the main outcome measurement window
- **Fix**: Replace text to clarify: "2000-2010" = shock activation window; "1997-2022" = main outcome long-difference
- **Recommendation**: REWRITE to separate shock window from outcome window language ### Priority 6 (HC1 inference layer) **6. § 5, line 31** — Table 1 HC1 row "| HC1 (heteroskedasticity-robust) | 0.0323 | -2.12 | 0.034 |"
- **File**: `paper_draft_v01_section_5.md`, line 31 (Table 1 HC1 row)
- **Current text**: "| HC1 (heteroskedasticity-robust) | 0.0323 | -2.12 | 0.034 |"
- **Issue**: HC1 SE=0.0323, t=-2.12 are inconsistent with β=-0.127 (would imply SE ≈ 0.031, but t would be -4.1, not -2.12). This HC1 row documents ARCHIVE build. Main β=-0.127 should have comparable HC1 SE but much larger |t|
- **Fix**: Recalculate HC1 standard error and t-statistic for β=-0.127; update Table 1 HC1 row
- **Recommendation**: REPLACE with correct HC1 values OR clarify this row is archive-only robustness table --- ## B. LEGITIMATE_ROBUSTNESS List (11 items — DO NOT TOUCH) These references properly cite the archive build as a sensitivity layer, robustness check, or comparative context. No cleanup needed: 1. **§ 1_2, line 56** — "1994-baseline Bartik exposure measure" — baseline construction explanatory text
2. **§ 1_2, line 44** — "I use the 1994 KOSTAT industrial census" — methodological choice explanation
3. **§ 5, line 19** — "β_main = -0.127 (cluster-province t = -4.02)" — MN estimate correctly cited
4. **§ 5, line 25** — "Replacing the 2000-2010 China bilateral exposure with 1995-2001 pre-WTO bilateral exposure" — pre-WTO placebo specification (legitimate falsification test)
5. **§ 5, line 25** — "β_placebo = +0.0238" — archive build placebo result (correctly flagged as sensitivity)
6. **§ 6, line 31** — "β_dropC26 = -0.0756 (HC1 SE = 0.0335, t = -2.26)" — robustness result on archive specification (correct context)
7. **§ 6, line 41** — "1994 vs 1993 ρ ≈ 0.97... expected pattern... within ±1.5 pp of main β = -0.0685" — baseline sensitivity justification (archive bounds correctly set)
8. **§ 6, line 47** — "β_1992 = -0.0158 (HC1 SE = 0.0246)" — baseline sensitivity result (properly contextualized attenuation)
9. **§ 8_9, line 15** — "The Korean estimate of -6.85 percent reduction" — percentage form interpretation of main effect
10. **§ 8_9, line 35** — "The 1992-baseline alternative specification yields β = -0.016" — limitations section (archive weakness properly disclosed)
11. **§ 8_9, line 51** — "β = -0.127 in log-rate units" — conclusion statement (MN estimate correctly cited) --- ## C. AMBIGUOUS List (1 item — context judgment needed) **1. § 6, line 88** — "0.0897 vs 0.0685 in absolute terms"
- **Text**: "...with the same protective sign as the main estimate and a magnitude approximately 31 percent larger (0.0897 vs 0.0685 in absolute terms)."
- **Context**: Section 5.4 reports post-2008 sub-period: β_post-2008 = -0.0897. The line compares this to 0.0685. This could mean: - **(Interpretation A)**: Compares post-2008 native (-0.0897) to archive build period estimate (-0.0685) — legitimate robustness - **(Interpretation B)**: Treats -0.0685 as the full-period main and reports post-2008 as 31% larger — TRUE GAP
- **Judgment**: LIKELY LEGITIMATE. Read full § 5.4 context: line 86 establishes β_post-2008 = -0.0897 as the sub-period result. The comparison to -0.0685 appears to be against the *archive build's full-period estimate* (not the main -0.127), used to show the sub-period strengthens the effect. Recommend reading full § 5.4 to confirm this is intended as sub-period robustness (LEGITIMATE) vs archive comparison (TRUE_GAP). --- ## Revised Unification Status ### Before Re-Classification (49% gaps reported)
- Assumed 49% of 66 references were "NEEDS_CLEANUP" or "⚠️"
- Implied ~32 references needed β=-0.0685 → β=-0.127 updates ### After Re-Classification (Path A native gap count)
- **6 TRUE_GAP** mechanical cleanup items (§ 5 concentrated: lines 31, 42, 56, 76)
- **11 LEGITIMATE** robustness citations (§ 1-2, § 5, § 6, § 8-9 all contain proper archive references)
- **1 AMBIGUOUS** (needs context read of § 5.4 full paragraph) ### Practical Completion
- **Actual unification needed**: 6 targeted changes (not 49% of all references)
- **Estimated time**: ~90 minutes (bulk in Table 1 HC1 recalculation + § 5 line 56 rewrite)
- **Risk of false-positive cleanup**: HIGH (11/18 = 61% are legitimate and must be preserved) --- ## Top 8 Specific Cleanup Actions (Priority Order) 1. **§ 5, line 56** — Replace "β_main = -0.0685" with "β_main = -0.127" + rewrite intro paragraph
2. **§ 6, line 13** — Rewrite section intro: clarify § 6 is robustness TO main β=-0.127; update HC1 t and p-values
3. **§ 5, line 76** — Replace "-0.0685" with "-0.127"; update all four outcome coefficients from Table 2 Path A native
4. **§ 5, line 31** — Recalculate and replace HC1 row in Table 1 (SE and t-statistic for β=-0.127)
5. **§ 5, line 42** — Clarify or replace "β = -0.0685" with "β = -0.127" in SE-layer discussion
6. **§ 1_2, line 36** — Rewrite 2000-2010 context sentence to separate shock window from outcome window
7. **§ 6, line 88** — Read full § 5.4 context; if archive comparison intended, add footnote clarifying sub-period vs archive
8. **AUDIT**: Full-text search for remaining "0.0685" hits in § 3-4 (not examined here) to catch any spillover mislabeling --- ## Key False Positives (Examples of What NOT to Change) - § 6 line 41 "±1.5 pp of main β = -0.0685" — this is deliberate archive robustness bound; preserve
- § 6 line 47 "β_1992 = -0.0158" — alternative baseline result; preserve as robustness weakness
- § 5 line 25 "β_placebo = +0.0238" — pre-WTO falsification test; preserve with current sign
- § 8_9 line 15 "-6.85 percent" — percentage restatement of main; preserve --- ## Recommendation **Do NOT execute blanket find-replace on -0.0685 → -0.127.** The 6 TRUE_GAP items are concentrated in § 5 (5 of 6 items) with one § 6 section intro. Surgical edits with context verification (especially Table 1 HC1 recalculation) will reduce false-positive risk. Archive build robustness citations are **intentional and correct** — they document Path A's commitment to reporting sensitivity checks alongside the main native estimate.
