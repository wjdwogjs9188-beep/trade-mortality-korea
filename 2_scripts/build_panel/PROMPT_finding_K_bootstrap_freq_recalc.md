# Sub-task 2.4 bootstrap raw recalculation — Finding K placeholder anchor (R-A 측 self-contained mini-prompt)

**작성**: 2026-05-08 R-A → 정재헌 → Spyder/Claude Code
**대상**: paper § 7.2.4 line 50 의 frequency 19.1% (F < 7.25) → 새 cutoff (F < 5.53) 의 raw recalculation
**선행**: ✅ sub-task 2.4 cumulative artifact (`4_results/dghp_acme_n05ba_bootstrap.parquet`, 1,001 rows)
**Strict workflow anchor**: R-A sandbox 위 substantive 분석 부재 (memory: feedback_no_sandbox_analysis.md). 사용자 측 Spyder 환경 위 직접 실행 + 결과 paste form.

---

## 1. 목적

Finding J 의 cumulative refinement 영역 위 paper § 7.2.4 line 50 의 frequency 영역 정정:

- 직전 wording: "19.1% 의 replications producing F < 7.25 (Stock-Yogo 25% relaxed cutoff)"
- 정정 후 wording: "[X%] of replications producing F < 5.53 (Stock-Yogo 25% TSLS-bias cutoff)"

X% 의 cumulative substantive 영역 위 sub-task 2.4 의 N05BA bootstrap 의 raw 분포 (1000 reps) 위 F < 5.53 의 frequency cumulative recalculation prerequisite.

---

## 2. Implementation script

`C:\Users\82103\Downloads\trade_mortality_korea\2_scripts\build_panel\finding_K_bootstrap_freq_recalc.py`

```python
"""Finding K — bootstrap F frequency recalculation (F < 5.53 under Stock-Yogo 25% TSLS-bias cutoff)."""
import pandas as pd
import numpy as np
from pathlib import Path

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
boot_path = PROJ / "4_results" / "dghp_acme_n05ba_bootstrap.parquet"

if not boot_path.exists():
    raise FileNotFoundError(f"Sub-task 2.4 bootstrap parquet 부재: {boot_path}")

boot = pd.read_parquet(boot_path)
print(f"Bootstrap rows (1 point + B reps): {len(boot)}")
print(f"Columns: {boot.columns.tolist()}")

# Find first-stage F column (sub-task 2.4 spec)
# Robust column identification: exact match 또는 prefix match
fs_F_col = None
for col in boot.columns:
    cl = col.lower()
    if cl == 'f_fs' or cl.startswith('f_first') or 'first_stage' in cl or cl == 'f_first_stage':
        fs_F_col = col
        break

if fs_F_col is None:
    print("[WARN] First-stage F column 직접 식별 불가. boot.columns 위 cumulative read 권고.")
    print(boot.head(3))
else:
    print(f"\nFirst-stage F column: {fs_F_col}")
    F_dist = boot.iloc[1:][fs_F_col]  # boot_id=0 은 point estimate
    print(f"\n  Bootstrap reps (excluding point): {len(F_dist)}")
    print(f"  F distribution percentiles: 2.5%={F_dist.quantile(0.025):.2f}, 50%={F_dist.median():.2f}, 97.5%={F_dist.quantile(0.975):.2f}")

    # Cumulative cutoff frequency
    cutoffs = {
        'Stock-Yogo 10% TSLS-bias (16.38)': 16.38,
        'Stock-Yogo 15% TSLS-bias (8.96)': 8.96,
        'Stock-Yogo 20% TSLS-bias (6.66)': 6.66,
        'Stock-Yogo 25% TSLS-bias (5.53)': 5.53,
        'Olea-Pflueger τ=10% (23.1)': 23.1,
    }
    print(f"\n  Cumulative bootstrap frequency P(F < cutoff):")
    for label, cutoff in cutoffs.items():
        freq = (F_dist < cutoff).mean()
        print(f"    {label:<40} {freq*100:.1f}%")
    
    print(f"\n  Finding K paper § 7.2.4 line 50 정정 영역의 substantive direction:")
    print(f"    이전 wording: 38.5% (F<16.4) + 19.1% (F<7.25) + 54.5% (F<23.1)")
    print(f"    정정 wording: {(F_dist<16.38).mean()*100:.1f}% (F<16.38) + {(F_dist<5.53).mean()*100:.1f}% (F<5.53) + {(F_dist<23.1).mean()*100:.1f}% (F<23.1)")
```

---

## 3. 검증 commit 형식

```markdown
## Finding K bootstrap frequency recalculation 완료

**Output**:
- console: F < {16.38, 8.96, 6.66, 5.53, 23.1} 위 cumulative frequency

**Verify 결과**:
- F < 16.38: ?% (이전 38.5% 와 정합 영역)
- F < 5.53: ?% (이전 19.1% (F<7.25) 의 cumulative 정정 영역)
- F < 23.1: ?% (이전 54.5% 와 정합 영역)

**다음 step**: paper § 7.2.4 line 50 의 [TBD] placeholder 의 cumulative refinement commit (사용자 측 별도 환경 commit 의 substantive direction).
```

---

## 4. 실행 명령

Spyder F5 또는 %runfile:
```
%runfile C:/Users/82103/Downloads/trade_mortality_korea/2_scripts/build_panel/finding_K_bootstrap_freq_recalc.py --wdir
```

---

**End of Finding K bootstrap frequency recalculation prompt**
