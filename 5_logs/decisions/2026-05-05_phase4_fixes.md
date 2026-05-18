# Phase 4 fixes — WCB direct + pre_2008 diagnosis
_2026-05-05_

## WCB-sido direct bootstrap (1000 boot)
- N = 222, sido clusters = 16
- baseline cluster-sido: β=-0.0685, t=-3.11, p=0.0019
- **WCB-sido p (1000 boot)**: 0.0410
- ✅ WCB significant — small-cluster correction 후에도 유의

## pre_2008 sub-period diagnosis (despair_total)
- pre_2008 rows: 2657
- year distribution: {np.int64(1997): 241, np.int64(1998): 241, np.int64(1999): 241, np.int64(2000): 241, np.int64(2001): 239, np.int64(2002): 240, np.int64(2003): 241, np.int64(2004): 241, np.int64(2005): 244, np.int64(2006): 244, np.int64(2007): 244}
- pop_wa NaN by year: {np.int64(1997): 241}
- log_asr_p1 NaN by year: {np.int64(1997): 241}
- window 1998-2007: N=222, β=-0.0511, t=-1.19, p=0.2355
- window 2000-2007: N=222, β=-0.0599, t=-2.00, p=0.0455
- window 1999-2007: N=222, β=-0.0557, t=-1.47, p=0.1414
- window 1997-2007: pivot 컬럼 부재

## 종합
- WCB-sido 가 전통 cluster-sido 보다 SE inflate → small-cluster (15) 영향 정량
- pre_2008 결과 (위 windows) → ICD artifact 검증