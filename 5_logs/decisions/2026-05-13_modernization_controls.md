# Path B Phase 2 — Modernization confound robustness (sido FE + urbanization)
_Date: 2026-05-13_

## Summary
Long-difference of log working-age despair-mortality regressed on standardized Bartik trade exposure, with the cascade adding sido FE and Δ_urbanization (long-difference log population density, 1997-1999 pop / 2007 area baseline → 2018-2022 pop / 2018-2022 area endpoint).

Analytic sample (with Δ_urbanization joinable): n = 213.
Sido FE: 16-17 dummies (drop_first=True; baseline = lowest sido_code).

### Cascade
| Spec | β | HC1 SE | Cluster-Sido SE | AR 95% CI | Attenuation vs β_main |
|------|--:|------:|----------------:|-----------|----------------------:|
| Spec 0 (z_x_std) | -0.1297 | 0.0263 | 0.0327 | [-0.2077, -0.0897] | 100.0% (anchor) |
| Spec 1 (+ sido FE) | -0.0635 | 0.0198 | 0.0189 | [-0.1175, -0.0315] | 49.0% |
| Spec 2 (+ sido FE + Δ_urbanization) | -0.0706 | 0.0204 | 0.0179 | [-0.1266, -0.0386] | 54.4% |

**Verdict**: PARTIAL CONFOUND — substantive attenuation (50% ≤ β_full < 70% × β_main)

### Data-limitation honest disclosure
- Area baseline = 2007 KOSIS 지적통계 (closest to mortality-baseline 1997-1999; 7-12 year gap).
 Areas are nearly time-invariant within sigungu (cross-sectional variation dominates),
 so the 2007 anchor is a substantive proxy for 1994/1997 baseline urbanization levels.
- Dual-career household share, domestic violence reporting, healthcare infrastructure
 density: **not available** at sigungu × pre-2015 vintage with sufficient long-difference
 scope. These three controls are deferred to the R&R cycle and disclosed in § 8.3.3.

Output CSV: `4_results/regression/modernization_robustness_cascade.csv`
Density panel: `3_derived/modernization_controls/sigungu_density_panel.parquet`