# Trade Exposure and Mortality in Export-Oriented Korea — Submission Package v01

**Author**: 정재헌 (가천대학교 경제학)
**Target venue**: Korean Economic Review (KER), full paper format
**Package date**: 2026-05-06
**Package version**: v01 (paper draft Stage C, post-Round 29 verification)

---

## Package Contents

This submission package contains the paper draft, regression outputs, panel data, codebooks, and audit logs needed for external review of the Trade × Mortality Korea paper. Reviewers should be able to (i) read the paper draft, (ii) verify cited statistics against the regression CSV files, and (iii) trace any panel-level claim back to the source data.

```
paper_v01_submission/
├── README.md                 (this file — start here)
├── DATA_DICTIONARY.md        (column-level specification for all parquet/csv)
├── 01_mortality/             (1 file, ~700 KB)
├── 02_bartik_iv/             (11 files, ~180 KB)
├── 03_mediators/             (5 files, ~3.2 MB)
├── 04_regression_results/    (10 files, ~6 KB)
├── 05_codebooks/             (6 files, ~365 KB)
├── 06_paper_draft/           (7 files, ~110 KB)
└── 07_audit_logs/            (7 files, ~32 KB)

Total: 47 files, ~5 MB
```

---

## Reading order

1. **`06_paper_draft/paper_draft_v01_section_1_2.md`** — Introduction and Background. Establishes the comparative framework (US/UK adverse vs Germany/Korea protective trade-mortality relationship) and motivates the protective-sign hypothesis for Korea.

2. **`06_paper_draft/paper_draft_v01_section_3_4.md`** — Data and Identification. Section 3.2 contains **Table A: Sample Universe Cascade**, which documents the 9 sample sizes (256/251/226/222/218/215/210/206/198) used in different analytic specifications. Section 4 specifies the Bartik IV construction and the BHJ shock-only / GPSS share-path identification framework.

3. **`06_paper_draft/paper_draft_v01_section_5.md`** — Main Empirical Results. Reports β = -0.0685 (HC1 t = -2.12, p = 0.034; cluster-province t = -3.11, p = 0.0019; AKM industry-mode t = -3.65) for the deaths-of-despair composite, with outcome specificity and post-2008 sub-period results.

4. **`06_paper_draft/paper_draft_v01_section_6.md`** — Robustness. Pre-WTO placebo, drop-C26, baseline year sensitivity (1992 attenuation honest disclosure), z_m_education baseline stability, outcome family alternative definitions, and Year FE specification.

5. **`06_paper_draft/paper_draft_v01_section_8_9.md`** — Discussion + Conclusion. Limitations (statistical inference, baseline year sensitivity, generalizability, mechanism precision) and the comparative trade-mortality framework.

6. **`06_paper_draft/paper_draft_v01_references.md`** — 39 academic + 8 institutional references.

7. **`06_paper_draft/DATA_INVENTORY_v04_master_2026_05_06.md`** — Full data inventory (raw, processed, regression outputs).

---

## Section 7 (Mechanism analysis) status

Section 7 is **deferred** to a future revision. The mechanism analysis will use the Dippel, Gold, Heblich, and Pinto (2017) single-IV mediation framework with five active mediators (M1 HIRA pharmaceutical prescription, M3 KOSIS family aggregates, M4 z_m_marital MDIS 1990 cohort sex ratios, M5 z_m_education KEDI 1985 university distance, M6 KOSTAT suicide rates). The HIRA pharmaceutical panel (M1) is in active data collection (~17 percent complete as of package date); the four non-HIRA mediator panels (M3-M6) are constructed and included in `03_mediators/`.

---

## Verifying cited statistics against regression CSV

The paper draft cites specific statistics from the regression outputs. Reviewers can verify these against `04_regression_results/`:

| Paper text | CSV file | Column |
|------------|----------|--------|
| § 5.1 main β = -0.0685, HC1 t = -2.12, p = 0.034 | `main_spec_5layer_se.csv` | despair_total row |
| § 5.1 cluster-province t = -3.11 | `main_spec_5layer_se.csv` | t_cluster_sido |
| § 5.1 AKM industry-mode t = -3.65 | `main_spec_5layer_se.csv` | t_AKM |
| § 5.3 Romano-Wolf p_RW = 0.317 | `romano_wolf_pvalues.csv` | despair_total row |
| § 5.4 post-2008 β = -0.0897, t = -4.28, p < 0.0001 | `sub_period_split_2008.csv` | post_2008 row |
| § 6.1 placebo β = +0.0238, p = 0.31 | `pre_wto_placebo_1992_1996.csv` | one-row table |
| § 6.2 drop-C26 β = -0.0756, t = -2.26 | `quality_improvement_suite.csv` | Drop-C26 row |
| § 6.3 1992 baseline β = -0.0158, p = 0.52 | `main_spec_5layer_se_1992baseline.csv` | despair_total row |
| § 6.3 1992 post-2008 β = -0.0458, p = 0.003 | `sub_period_split_2008_1992baseline.csv` | post_2008 row |

---

## Key datasets

### `01_mortality/sigungu_mortality_panel_v02_wa.parquet`
Working-age (25-64) Korean nationality death panel. 31,494 cells (sigungu × year × outcome_group). 1997-2024 coverage. Source: KOSTAT 사망 microdata 28 csv. See `05_codebooks/mortality_104_classification.csv` for cause-of-death code definitions.

### `02_bartik_iv/baseline_shares_1994_ksic9_2digit.parquet`
1994 KOSTAT industrial census baseline employment shares for Bartik IV construction. 4,003 cells (h_code × KSIC9_2digit). 251 sigungu × 23 KSIC9 industries. Source: KOSTAT 광업·제조업조사 1994.

### `02_bartik_iv/iv_z_x_bilateral.parquet`
Korea-China bilateral Bartik IV (z_x_h^KR-CN). 226 sigungu (after exposure normalization). Per-worker normalized to total 1994 manufacturing employment. Source: combination of `baseline_shares_1994_ksic9_2digit.parquet` and `exposure_bilateral_2000_2010.parquet`.

### `02_bartik_iv/baseline_shares_1992_ksic9_2digit_v2.parquet`
1992 baseline shares (sensitivity analysis). 215 h_code × 22 KSIC9. KSIC 6th-edition codes converted via the 23-row crosswalk in `05_codebooks/ksic6_to_ksic9_2digit.csv`. Note: 1992 baseline yields attenuated regression result (β = -0.0158, p = 0.52); see paper § 6.3 for honest disclosure of three contributing factors (sample reduction, small-denominator outliers, KSIC crosswalk ambiguity).

### `03_mediators/z_m_education_baseline_sensitivity.parquet`
Track 2 z_m_education sensitivity panel. 251 sigungu × 3 KEDI baselines (1985, 1990, 1995). Cross-baseline correlation ≥ 0.989; stability confirmed for paper § 6.4 narrative.

---

## Audit logs (07_audit_logs/)

The `07_audit_logs/` folder contains seven critical decision and integrity-check logs:

- `2026-05-06_validation_report_audit_complete.md` — Full validation report for the paper draft (post-Round 26 audit, identifies P1·P2·P3 issues and resolution status)
- `2026-05-06_track2_track3_v4_5_4_commit.md` — Track 2 (z_m_education baseline) + Track 3 (1992 baseline shares) commit log
- `2026-05-05_phase_bx_final_branch_decision.md` — A.ii branch commit (BHJ shock-only path + GPSS share-path joint diagnostic, weak-IV warning)
- `2026-05-05_phase4_final_publishable.md` — Phase 4 main spec final publishable result
- `2026-05-06_baseline_shares_1992_v2.md` — Track 3 v2 build integrity check (3 bug fixes documented)
- `2026-05-06_z_m_education_sensitivity.md` — Track 2 integrity check (cross-baseline correlation 0.989)
- `2026-05-05_z_x_h_1992_phase2b.md` — Phase 2-B z_x_h^1992 build (cross-validation against 1994 baseline)

---

## Open issues (transparent disclosure)

Per Round 29 verification (2026-05-06), the paper has the following acknowledged open issues:

**P1 (publication-blocking, addressing in revision):**
1. **Romano-Wolf common-sample re-implementation**: The current implementation uses outcome-specific sample sizes (despair/cancer/cardio/external = 222; respiratory = 198). A common-sample re-implementation (n=198) is in progress.
2. **WCB cluster-province alternative implementation**: The Cameron-Gelbach-Miller Rademacher implementation did not numerically converge with G=16. A Webb (2023) 6-point weighted re-implementation using the `fwildclusterboot` R package is in progress.
3. **Pre-2008 sub-period regression**: Section 5.4 reports the post-2008 sub-period only. The symmetric pre-2008 sub-period (1997-1999 base → 2007 endpoint) is in build.

**P2 (paper polish, paywalled access):**
4. **Lee et al. (2022) Table 3 Panel A interpolation**: The IV second-stage critical value c_{0.05}(F=19.65) = 3.286 is interpolated from the LMP 2022 table; the precise interpolation procedure is documented in the online appendix when accessible.
5. **Lang et al. (2019) Table 2 column M.3 first-stage F = 18.77**: Cited as procedural precedent; verification via paper PDF access pending.

These items are tracked in `07_audit_logs/2026-05-06_validation_report_audit_complete.md`.

---

## Reading instructions for reviewers

1. Read README (this file) for orientation.
2. Read `DATA_DICTIONARY.md` for column-level specification.
3. Read paper draft sections in numerical order: § 1-2, § 3-4, § 5, § 6, § 8-9, References.
4. For any cited statistic, verify against the corresponding `04_regression_results/*.csv` file (see verification table above).
5. For any panel-level claim, trace back to the parquet file in `01_mortality/`, `02_bartik_iv/`, or `03_mediators/`.
6. For methodological choices (working-age 25-64 restriction, Korean nationality filter, 1994 baseline, A.ii branch decision), see `07_audit_logs/`.

---

## Contact

For questions or feedback on this draft, please contact:
- 정재헌 (jaeheon.jeong, 가천대학교 경제학)

The paper is a single-author submission for KER full paper format (target venue), with AEJ Applied as a secondary target venue and AER:I as a long-term aspiration.
