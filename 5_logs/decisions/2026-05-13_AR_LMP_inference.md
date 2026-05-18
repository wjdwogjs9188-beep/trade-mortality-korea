# Path B Phase 1 — Anderson-Rubin + LMP cumulative robustness
_Date: 2026-05-13_

## Summary
5 IV-inference areas of the manuscript receive cumulative weak-IV-robust treatment.

### Area 1 — Main IV β (validation IV, n=221)
- β_IV = -0.1003 (Wald HC1 SE = 0.0273)
- Wald 95% CI = [-0.1537, -0.0468]
- **AR 95% CI = [-0.1494, -0.0365]**
- First-stage F (manuscript-cited cluster-sido) = 19.65; LMP c_0.05(F) = 3.286
- IV t-stat = -3.68; LMP-valid? **YES**

### Area 2 — DGHP single-IV mediation
- **Area 2.1 — DGHP M1 N05BA (paper F=22.59)** (n=138): γ_FS=-0.2098 (F_paper=22.59, AR CI [-0.3097, -0.1099]); ACME=-0.0233 (AR CI [-0.0658, -0.0011]); LMP c=2.90, valid? YES
- **Area 2.2 — DGHP M3 divorce (paper F=55.73)** (n=210): γ_FS=+0.1449 (F_paper=55.73, AR CI [+0.1069, +0.1830]); ACME=-0.0957 (AR CI [-0.1506, -0.0532]); LMP c=2.00, valid? YES
- **Area 2.3 — DGHP M3 fertility (paper F=14.26)** (n=213): γ_FS=+0.0468 (F_paper=14.26, AR CI [+0.0225, +0.0710]); ACME=-0.0334 (AR CI [-0.0663, -0.0111]); LMP c=4.01, valid? NO
- **Area 2.4 — DGHP M3 marriage (paper F=5.95, very weak)** (n=210): γ_FS=+0.0342 (F_paper=5.95, AR CI [+0.0067, +0.0616]); ACME=-0.0099 (AR CI [-0.0355, -0.0000]); LMP c=6.28, valid? NO
- **Area 2.5 — DGHP M6 suicide (paper F=2.38, extremely weak)** (n=205): γ_FS=-0.0428 (F_paper=2.38, AR CI [-0.0972, +0.0116]); ACME=-0.0241 (AR CI [-0.0671, +0.0080]); LMP c=8.24, valid? NO

### Area 3 — Joint multi-mediator (n=133)
- **Joint multimediator (n=133) — M1 N05BA**: γ_FS=-0.2040 (F_paper=22.06); ACME_joint=-0.0115 (AR CI [-0.0427, +0.0082]); LMP c=3.01, valid? YES
- **Joint multimediator (n=133) — M3 divorce**: γ_FS=+0.1592 (F_paper=74.29); ACME_joint=-0.0680 (AR CI [-0.1307, -0.0231]); LMP c=1.99, valid? YES
- **Joint multimediator (n=133) — M3 fertility**: γ_FS=+0.0415 (F_paper=8.77); ACME_joint=-0.0252 (AR CI [-0.0671, -0.0032]); LMP c=5.28, valid? NO

### Cumulative interpretation
- LMP-valid count: **5 / 9** inference rows.
- AR CI consistency with sign: see CSV for area-by-area sign-zero comparison.
- Output CSV: `4_results/regression/AR_LMP_inference_cumulative.csv`