# Phase B-x — First-stage F (z_x: ADH-8 vs KR-CN bilateral)
_2026-05-05_

- cutoff: Stock-Yogo 5% TSLS bias robust = **23.1**
- 2 IV → tF inference (Lee-Moreira-McCrary-Porter 2022) on smaller F

## ADH-8: using `z_x_per_worker` as instrument

## ADH-8 first stage
- merged panel n=220
- N = 220
- β = +0.0000, R² = 0.187
- F (HC1) = **14.07**
- F (cluster-sido) = **12.20**
- ⚠️ min(F) ∈ [10, 23.1) → weak-IV territory, tF inference 필수

## bilateral: using `z_x_per_worker` as instrument

## bilateral first stage
- merged panel n=220
- N = 220
- β = +0.0000, R² = 0.226
- F (HC1) = **48.08**
- F (cluster-sido) = **19.65**
- ⚠️ min(F) ∈ [10, 23.1) → weak-IV territory, tF inference 필수

- ✅ saved: `3_derived\identification\first_stage_f_results.csv`

## Branch suggestion (PAP v4.0 § 5)
- → **A.ii main**: KR-CN bilateral primary (ADH-8 weak)