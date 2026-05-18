# Phase 4 — 5-layer SE main spec final
_2026-05-05_

- spec: Δ log_asr+1 (rate_h, 2000→2010) ~ z_x_h^{KR-CN, std}
- 5 outcomes × 5 SE layers + tF inference + Romano-Wolf 1000 boot

- mortality: (31494, 8), IV: (226, 4), centroid: 251
- baseline industry mode: 226 h_codes, 17 distinct industries
  - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m  def get_denom(self):
      <source elided>
        # R to c++ gives good speed improvements
[1m        @njit(parallel = self.parallel)
[0m        [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## despair_total (n=222)
- β (std) = -0.0685, R² = 0.043
- HC1: SE=0.0323, t=-2.12, p=0.0340
- cluster-sido: SE=0.0221, t=-3.11, p=0.0019
- AKM (industry-mode cluster): SE=0.0188, t=-3.65
- Conley 5km: SE=0.0326, t=-2.10
- Conley 10km: SE=0.0335, t=-2.04
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
  - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m  def get_denom(self):
      <source elided>
        # R to c++ gives good speed improvements
[1m        @njit(parallel = self.parallel)
[0m        [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## cancer (n=222)
- β (std) = -0.0050, R² = 0.000
- HC1: SE=0.0264, t=-0.19, p=0.8502
- cluster-sido: SE=0.0333, t=-0.15, p=0.8811
- AKM (industry-mode cluster): SE=0.0132, t=-0.38
- Conley 5km: SE=0.0263, t=-0.19
- Conley 10km: SE=0.0262, t=-0.19
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
  - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m  def get_denom(self):
      <source elided>
        # R to c++ gives good speed improvements
[1m        @njit(parallel = self.parallel)
[0m        [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## cardiovascular (n=222)
- β (std) = -0.0129, R² = 0.001
- HC1: SE=0.0284, t=-0.46, p=0.6488
- cluster-sido: SE=0.0259, t=-0.50, p=0.6181
- AKM (industry-mode cluster): SE=0.0172, t=-0.75
- Conley 5km: SE=0.0284, t=-0.46
- Conley 10km: SE=0.0288, t=-0.45
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
  - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m  def get_denom(self):
      <source elided>
        # R to c++ gives good speed improvements
[1m        @njit(parallel = self.parallel)
[0m        [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## respiratory (n=198)
- β (std) = -0.0118, R² = 0.000
- HC1: SE=0.0439, t=-0.27, p=0.7889
- cluster-sido: SE=0.0602, t=-0.20, p=0.8452
- AKM (industry-mode cluster): SE=0.0199, t=-0.59
- Conley 5km: SE=0.0439, t=-0.27
- Conley 10km: SE=0.0451, t=-0.26
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
  - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m  def get_denom(self):
      <source elided>
        # R to c++ gives good speed improvements
[1m        @njit(parallel = self.parallel)
[0m        [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## external_other (n=222)
- β (std) = +0.0135, R² = 0.002
- HC1: SE=0.0468, t=+0.29, p=0.7727
- cluster-sido: SE=0.0758, t=+0.18, p=0.8584
- AKM (industry-mode cluster): SE=0.0124, t=+1.09
- Conley 5km: SE=0.0468, t=+0.29
- Conley 10km: SE=0.0470, t=+0.29
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers

- saved: `4_results/regression/main_spec_5layer_se.csv`

## Romano-Wolf step-down (1000 boot, family of 5 outcomes)
```
       outcome     t_HC1    p_raw  p_RW_adj  RW_sig
 despair_total -2.120511 0.033963     0.317   False
        cancer -0.188915 0.850160     1.000   False
cardiovascular -0.455480 0.648764     0.996   False
   respiratory -0.267771 0.788875     1.000   False
external_other  0.288900 0.772658     0.999   False
```
- saved: `4_results/regression/romano_wolf_pvalues.csv`

## 2008 ICD-10 sub-period split (despair_total)
- post_2008 (2008-2022): N=218, β=-0.0897, t=-4.28, p=0.0000
- saved: `4_results/regression/sub_period_split_2008.csv`

## Final inference (despair_total)
- tF cutoff = 3.84 (Phase B-x F=19.65)
- SE layers passing tF: **0/4** (none)
- Romano-Wolf adj p (despair) = 0.3170
- ❌ no SE layer passes tF cutoff → preliminary only, paper § 8 caveat 강화