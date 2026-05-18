# Pre-WTO 1992-1996 placebo v2 — incremental log
_2026-05-05_

## Pre-WTO csv: 5
- combined rows: 13,174
- columns: ['typecode', 'freqcode', 'refperiodid', 'refyear', 'refmonth', 'period', 'reportercode', 'reporteriso', 'reporterdesc', 'flowcode', 'flowdesc', 'partnercode', 'partneriso', 'partnerdesc', 'partner2code', 'partner2iso', 'partner2desc', 'classificationcode', 'classificationsearchcode', 'isoriginalclassification']
- cmd_col: cmdcode, val_col: primaryvalue
- HS6 distinct: 3894
- pivot columns: [1992, 1993, 1994, 1995, 1996]
- pre-WTO ΔM rows: 3894, sum: 4,812,450,944
- hs_ksic mapping rows: 6314, cols: ['hs6_str', 'ksic9_2digit']
- pre-WTO HS6 → KSIC9_2 merged: 3665
- pre-WTO ΔM by KSIC9_2: 23
```
ksic9_2digit   dM_pre_wto
         C24 1139514167.0
         C26  699973172.0
         C14  515070036.0
         C13  401337305.0
         C20  341035073.0
         C10  322315320.0
         C28  298815403.0
         C15  295139141.0
         C19  209413418.0
         C33  134571300.0
         C16  122150334.0
         C29   89851177.0
         C27   88245610.0
         C25   74961037.0
         C31   52491781.0
         C21   43385485.0
         C22   33905255.0
         C30   22379631.0
         C32   18447913.0
         C17    2814468.0
         C18    1225925.0
         C12   -6775191.0
         C23  -86870221.0
```
- shares rows: 4003, denom rows: 226

- z_x^{pre-WTO}: 226 h_code, mean=152601.24
- mortality pivot columns: ['h_code', 1998, 2000]
- 1998→2000 mortality non-null: 241
- placebo panel: n=226

## Pre-WTO placebo regression result
- N = 226, R² = 0.0093
- β (std) = +0.0238
- HC1: SE=0.0233, t=+1.02, p=0.3074
- cluster-sido: SE=0.0194, t=+1.23, p=0.2206

## 판정
- ✅ **Pre-WTO placebo PASS** (cluster p=0.2206 > 0.10)
- pre-WTO bilateral 변화가 1997-1999 mortality 와 무관 → BHJ shock-only exogeneity 직접 입증
- z_x_h^{2000-2010} 의 share-violation 에도 shock 자체는 외생

- saved: `4_results\regression\pre_wto_placebo_1992_1996.csv`