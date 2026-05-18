"""
Phase 2-B Step 6b — 2000·2010 schema probe (다른 schema 진단)
============================================================== 1994: 15 cols, headerless
2000: 107 cols — 다른 schema
2010: 111 cols — 다른 schema (KSIC 9차, C 326k rows) 각 year 의 컬럼명 + 시도/시군구/KSIC/종사자 후보 식별. 산출:
- 5_logs/integrity_checks/<date>_business_survey_2000_2010_schema.md Author: Date: 2026-05-04
"""
from __future__ import annotations import sys
from datetime import date
from pathlib import Path import pandas as pd PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
RAW = PROJ / "0_raw" / "kosis_business_survey" / "microdata_1994_2024"
LOGS = PROJ / "5_logs" / "integrity_checks"
LOGS.mkdir(parents=True, exist_ok=True)
TODAY = date.today.isoformat if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace") KEYWORDS = { "sido": ["시도", "광역", "행정구역_시도", "sido"], "sigungu": ["시군구", "구시군", "행정구역_시군", "sigungu", "sgg"], "addr": ["주소", "소재지", "지역"], "ksic": ["산업", "KSIC", "업종", "산업분류", "산업코드"], "employee": ["종사자", "종업원", "근로자", "고용", "인원"], "weight": ["가중치", "weight", "wt"],
} def probe(year: int, log: list) -> None: files = sorted(RAW.glob(f"{year}*.csv")) if not files: log.append(f"\n## {year}: ❌ no file") return f = files[0] log.append(f"\n## {year}: `{f.name}` ({f.stat.st_size/1024**2:.1f} MB)") # try with header (default) + cp949 for enc in ("cp949", "utf-8-sig"): try: df = pd.read_csv(f, encoding=enc, dtype=str, nrows=5, low_memory=False) log.append(f"- encoding: {enc}, header read shape: {df.shape}") break except (UnicodeDecodeError, UnicodeError): continue log.append(f"\n### Columns ({len(df.columns)}):") log.append("```") for i, c in enumerate(df.columns): log.append(f" [{i:3d}] {c}") log.append("```") log.append("\n### Keyword 매칭") cols_str = [str(c) for c in df.columns] for cat, keys in KEYWORDS.items: matched = [(i, c) for i, c in enumerate(cols_str) if any(k in c for k in keys)] if matched: log.append(f"- **{cat}**: {matched[:8]}") else: log.append(f"- {cat}: (none)") log.append("\n### 첫 3 row × 첫 20 col") log.append("```") log.append(df.iloc[:3,:20].to_string(index=False)) log.append("```") def main -> None: log = [f"# Phase 2-B Step 6b — 2000·2010 광업제조업조사 schema\n_{TODAY}_\n"] probe(2000, log) probe(2010, log) out = LOGS / f"{TODAY}_business_survey_2000_2010_schema.md" out.write_text("\n".join(log), encoding="utf-8") print(f"[OK] {out}") if __name__ == "__main__": main
