"""
Quick probe — KOSTAT 사망 microdata 의 진짜 컬럼명 + 첫 row.
"""
import sys
from pathlib import Path
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
RAW = PROJ / "0_raw" / "mortality_kostat" / "사망사료 정리"
OUT = PROJ / "5_logs" / "integrity_checks" / "2026-05-05_kostat_mortality_schema_probe.md"
OUT.parent.mkdir(parents=True, exist_ok=True)

log = ["# KOSTAT 사망 microdata schema probe\n"]

# 첫 파일 (1997)
files = sorted(RAW.glob("*.csv"))
for f in [files[0], files[len(files)//2], files[-1]]:
 log.append(f"\n## {f.name}")
 for enc in ("cp949", "euc-kr", "utf-8-sig"):
 try:
 df = pd.read_csv(f, encoding=enc, dtype=str, nrows=3, low_memory=False)
 log.append(f"- encoding: `{enc}`")
 log.append(f"- shape: {df.shape}")
 log.append("- columns:")
 log.append("```")
 for i, c in enumerate(df.columns):
 log.append(f" [{i:3d}] {repr(c)}")
 log.append("```")
 log.append("- 첫 3 row:")
 log.append("```")
 log.append(df.head(3).to_string)
 log.append("```")
 break
 except (UnicodeDecodeError, UnicodeError):
 continue

OUT.write_text("\n".join(log), encoding="utf-8")
print(f"[OK] {OUT}")
