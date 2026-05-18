# Phase 4 — 5-layer SE main spec final
_2026-05-06_

- spec: Δ log_asr+1 (rate_h, 2000→2010) ~ z_x_h^{KR-CN, std}
- 5 outcomes × 5 SE layers + tF inference + Romano-Wolf 1000 boot

- mortality: (31494, 8), IV: (215, 4), centroid: 251
- baseline industry mode: 214 h_codes, 18 distinct industries
 - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m def get_denom(self):
 <source elided>
 # R to c++ gives good speed improvements
[1m @njit(parallel = self.parallel)
[0m [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## despair_total (n=210)
- β (std) = -0.0158, R² = 0.002
- HC1: SE=0.0246, t=-0.64, p=0.5198
- cluster-sido: SE=0.0345, t=-0.46, p=0.6467
- AKM (industry-mode cluster): SE=0.0305, t=-0.52
- Conley 5km: SE=0.0247, t=-0.64
- Conley 10km: SE=0.0254, t=-0.62
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
 - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m def get_denom(self):
 <source elided>
 # R to c++ gives good speed improvements
[1m @njit(parallel = self.parallel)
[0m [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## cancer (n=210)
- β (std) = +0.0208, R² = 0.007
- HC1: SE=0.0132, t=+1.58, p=0.1137
- cluster-sido: SE=0.0137, t=+1.52, p=0.1291
- AKM (industry-mode cluster): SE=0.0114, t=+1.83
- Conley 5km: SE=0.0128, t=+1.63
- Conley 10km: SE=0.0129, t=+1.62
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
 - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m def get_denom(self):
 <source elided>
 # R to c++ gives good speed improvements
[1m @njit(parallel = self.parallel)
[0m [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## cardiovascular (n=210)
- β (std) = +0.0240, R² = 0.004
- HC1: SE=0.0124, t=+1.94, p=0.0529
- cluster-sido: SE=0.0138, t=+1.74, p=0.0827
- AKM (industry-mode cluster): SE=0.0122, t=+1.97
- Conley 5km: SE=0.0122, t=+1.96
- Conley 10km: SE=0.0123, t=+1.95
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
 - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m def get_denom(self):
 <source elided>
 # R to c++ gives good speed improvements
[1m @njit(parallel = self.parallel)
[0m [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## respiratory (n=187)
- β (std) = +0.0352, R² = 0.004
- HC1: SE=0.0386, t=+0.91, p=0.3618
- cluster-sido: SE=0.0308, t=+1.14, p=0.2529
- AKM (industry-mode cluster): SE=0.0249, t=+1.41
- Conley 5km: SE=0.0391, t=+0.90
- Conley 10km: SE=0.0393, t=+0.89
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers
 - WCB error: Failed in nopython mode pipeline (step: nopython frontend)
[1m[1m[1mnon-precise type array(pyobject, 1d, C)[0m
[0m[1mDuring: typing of argument at C:\Users\82103\anaconda3\Lib\site-packages\wildboottest\wildboottest.py (533)[0m
[1m
File "..\..\..\..\anaconda3\Lib\site-packages\wildboottest\wildboottest.py", line 533:[0m
[1m def get_denom(self):
 <source elided>
 # R to c++ gives good speed improvements
[1m @njit(parallel = self.parallel)
[0m [1m^[0m[0m

[0m[1mDuring: Pass nopython_type_inference[0m

## external_other (n=210)
- β (std) = +0.0011, R² = 0.000
- HC1: SE=0.0200, t=+0.06, p=0.9557
- cluster-sido: SE=0.0117, t=+0.10, p=0.9242
- AKM (industry-mode cluster): SE=0.0088, t=+0.13
- Conley 5km: SE=0.0199, t=+0.06
- Conley 10km: SE=0.0201, t=+0.06
- tF cutoff (F=19.65): |t| > 3.84
- tF pass count: 0/4 SE layers

- saved: `4_results/regression/main_spec_5layer_se_1992baseline.csv`

## Romano-Wolf step-down (1000 boot, family of 5 outcomes)
```
 outcome t_HC1 p_raw p_RW_adj RW_sig
 despair_total -0.643730 0.519751 0.995 False
 cancer 1.581809 0.113693 0.799 False
cardiovascular 1.935643 0.052911 0.654 False
 respiratory 0.911951 0.361794 0.981 False
external_other 0.055566 0.955687 1.000 False
```
- saved: `4_results/regression/romano_wolf_pvalues_1992baseline.csv`

## 2008 ICD-10 sub-period split (despair_total)
- post_2008 (2008-2022): N=206, β=-0.0458, t=-2.98, p=0.0029
- saved: `4_results/regression/sub_period_split_2008_1992baseline.csv`

## Final inference (despair_total)
- tF cutoff = 3.84 (Phase B-x F=19.65)
- SE layers passing tF: **0/4** (none)
- Romano-Wolf adj p (despair) = 0.9950
- ❌ no SE layer passes tF cutoff → preliminary only, paper § 8 caveat 강화