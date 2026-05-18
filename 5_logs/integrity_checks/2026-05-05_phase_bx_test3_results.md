# Phase B-x Test 3 — Pierce-Schott pre-trend exogeneity
_2026-05-05_

- pre-period mortality rows 1997-1999: **3,592**
- after filter outcome_group=despair_total: **723**
- using rate column: `log_asr_p1` (zero-safe)
- pivot columns: ['h_code', 1997, 1998, 1999]
- pre-trend panel n=241 (window 1997-1999, 2-year change)
- baseline manufacturing_emp_1994: 226 h_code
- bilateral exposure (using `z_x_per_worker`): 226 h_code
- final panel rows: **226**
- regression panel after dropna: 226

## OLS: pre_trend (1997→1999) ~ log(manufacturing_emp_1994) + bilateral_exposure_2000_2010
```
================================================================================================
 coef std err z P>|z| [0.025 0.975]
------------------------------------------------------------------------------------------------
const 5.7625 0.219 26.269 0.000 5.333 6.192
log_manufacturing_emp_1994 -0.1911 0.024 -8.087 0.000 -0.237 -0.145
bilateral_exposure_2000_2010 -2.264e-08 2.25e-08 -1.008 0.313 -6.67e-08 2.14e-08
================================================================================================
```
- p (log_manufacturing_emp_1994): 0.0000
- p (bilateral_exposure_2000_2010): 0.3134

- joint F p-value: **0.0000**
- ❌ p < 0.05 → share-exogeneity 위반 → A.iii branch (instrument 변경 또는 narrow window)

- ✅ panel saved: `3_derived\identification\test3_pretrend_panel.csv`