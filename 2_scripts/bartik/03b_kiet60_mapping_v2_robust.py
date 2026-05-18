"""
Phase 2-B Step 5a-2 — KIET60 mapping v2: robust 매칭 시도
============================================================ v1 결과: 컬럼 자동 인식 실패 + KSIC 6차 (baseline) ↔ 9차 (KIET 매핑) mismatch. 전략: 여러 aggregation level 시도하여 가장 viable 한 것을 선택. Level options:
- KIET 1레벨 (I0~I5, ~6 categories): coarse, robust to KSIC 차수
- KIET 2레벨 (I31, I32,..., ~10 categories): 산업특성별
- KIET 3레벨 (I3101,..., 60 categories): ADH 4-digit SIC 와 비슷 precision
- KSIC 2-digit (D17, D18,..., 24 categories): 6→9차 numeric shift 표준화 후 사용 KSIC 6→9차 핵심 변경 (KOSTAT 발행 연계표 일부):
- D (제조업) → C (제조업) — 모든 letter 변경
- D17 섬유 → C13 섬유
- D18 의복 → C14 의복
- D19 가죽 → C15 가죽
- D20 목재 → C16 목재
- D21 펄프 → C17 펄프
- D22 출판 → C18 인쇄
- D23 코크스 → C19 코크스
- D24 화학 → C20 화학
- D25 고무 → C22 고무
- D26 비금속광물 → C23 비금속
- D27 1차금속 → C24 1차금속
- D28 조립금속 → C25 금속가공
- D29 일반기계 → C29 기계
- D30 사무기기 → C28 의료광학 일부
- D31 전기기기 → C28 전기장비
- D32 영상통신 → C26 전자
- D33 의료정밀 → C27 의료정밀
- D34 자동차 → C30 자동차
- D35 기타운송 → C31 기타운송
- D36 가구 → C32 가구 산출:
- `5_logs/integrity_checks/<date>_kiet60_mapping_v2.md`
- `1_codebooks/ksic6_to_ksic9_2digit.csv` (manual crosswalk)
- `3_derived/bartik/baseline_shares_1994_kiet60_via_ksic2.parquet` (시도) Author: Date: 2026-05-04
"""
from __future__ import annotations import sys
import re
from datetime import date
from pathlib import Path import numpy as np
import pandas as pd PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
CONC = PROJ / "0_raw" / "hs_ksic_concordance"
BARTIK = PROJ / "3_derived" / "bartik"
CODEBOOKS = PROJ / "1_codebooks"
LOGS = PROJ / "5_logs" / "integrity_checks"
BARTIK.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
TODAY = date.today.isoformat if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace") # KSIC 6차 → 9차 manual crosswalk at 2-digit level
# (D=제조업 알파벳 → C, 일부 numeric shift)
# Source: KOSTAT 2007년 9차 개정 한국표준산업분류 부속표 (manually transcribed)
KSIC6_TO_KSIC9 = { "D15": "C10", # 음식료품 "D16": "C12", # 담배 "D17": "C13", # 섬유 "D18": "C14", # 의복·모피 "D19": "C15", # 가죽·신발 "D20": "C16", # 목재 "D21": "C17", # 펄프·종이 "D22": "C18", # 인쇄·출판 "D23": "C19", # 코크스·석탄·석유정제 "D24": "C20", # 화학 "D25": "C22", # 고무·플라스틱 "D26": "C23", # 비금속광물 "D27": "C24", # 1차금속 "D28": "C25", # 조립금속 "D29": "C29", # 일반기계 "D30": "C28", # 사무·계산·회계용기계 → 전기장비/일부 "D31": "C28", # 기타전기기계 "D32": "C26", # 영상·음향·통신 → 전자부품 "D33": "C27", # 의료·정밀·광학 "D34": "C30", # 자동차 "D35": "C31", # 기타 운송장비 "D36": "C32", # 가구·기타 "D37": "C33", # 재활용 "C10": "B05", # 광업: 석탄 "C11": "B06", # 광업: 원유·천연가스 "C12": "B07", # 광업: 비철금속 "C13": "B08", # 광업: 토석 "C14": "B08", # 광업: 기타
} def parse_ksic_lead(text: str) -> str | None: """'C21 의료용...' → 'C21'""" if pd.isna(text): return None s = str(text).strip m = re.match(r"^([A-Z]\d{1,4})\s", s) return m.group(1) if m else None def main -> None: log = [f"# Phase 2-B Step 5a-2 — KIET60 mapping v2 (robust)\n_{TODAY}_\n"] # 1) save manual crosswalk cw_df = pd.DataFrame([{"ksic6": k, "ksic9": v} for k, v in KSIC6_TO_KSIC9.items]) cw_path = CODEBOOKS / "ksic6_to_ksic9_2digit.csv" cw_df.to_csv(cw_path, index=False, encoding="utf-8-sig") log.append(f"## KSIC 6차 → 9차 manual crosswalk\n- saved: `{cw_path.relative_to(PROJ)}` ({len(cw_df)} mappings)\n") # 2) load KIET60 ↔ KSIC mapping f = CONC / "KIET60_to_KSIC_v2.xlsx" df = pd.read_excel(f, sheet_name="연계표") log.append(f"## KIET60_to_KSIC_v2 inspection") log.append(f"- shape: {df.shape}") log.append(f"- columns: {list(df.columns)}\n") # parse KSIC 9차 leading code ksic9_col = "표준산업분류 9차" df["ksic9_lead"] = df[ksic9_col].apply(parse_ksic_lead) df["ksic9_2digit"] = df["ksic9_lead"].astype(str).str[:3] # C21, C26, etc. log.append(f"- KSIC 9차 leading code 파싱 결과:") log.append(f" - non-null: {df['ksic9_lead'].notna.sum}/{len(df)}") log.append(f" - distinct 2-digit: {df['ksic9_2digit'].nunique}") log.append(f" - top: {df['ksic9_2digit'].value_counts.head(15).to_dict}") # KIET 3레벨 코드도 추출 df["kiet3"] = df["3레벨"].astype(str).str.extract(r"(I\d{4})")[0] df["kiet2"] = df["2레벨"].astype(str).str.extract(r"(I\d{2,3})")[0] df["kiet1"] = df["1레벨"].astype(str).str.extract(r"(I\d)")[0] log.append(f"\n- KIET 코드 추출:") log.append(f" - kiet1 distinct: {df['kiet1'].dropna.nunique}") log.append(f" - kiet2 distinct: {df['kiet2'].dropna.nunique}") log.append(f" - kiet3 distinct: {df['kiet3'].dropna.nunique}") # 3) baseline shares load bs = pd.read_parquet(BARTIK / "baseline_shares_1994_manufacturing.parquet") log.append(f"\n## baseline_shares_1994_manufacturing") log.append(f"- rows: {len(bs):,}, distinct KSIC4 (6차): {bs['ksic4'].nunique}") # KSIC 6차 4-char → 9차 2-digit 변환 bs["ksic6_2digit"] = bs["ksic4"].str[:3] # D17, D18,... bs["ksic9_2digit"] = bs["ksic6_2digit"].map(KSIC6_TO_KSIC9) n_mapped = bs["ksic9_2digit"].notna.sum log.append(f"- KSIC 6차 → 9차 (2-digit) 변환률: **{n_mapped:,}/{len(bs):,}** ({n_mapped/len(bs):.1%})") unmapped = bs.loc[bs["ksic9_2digit"].isna, "ksic6_2digit"].value_counts.head(5).to_dict log.append(f"- 미매핑 6차 2-digit top 5: {unmapped}") # 4) KSIC9 2-digit → KIET 3레벨 (or 2레벨) 매핑 # KIET mapping: ksic9_2digit (C21, C26,...) → kiet3 (I3101,...) but many KSIC2 → multiple KIET3 # 따라서 시군구 baseline 을 KSIC9 2-digit 으로 합한 후, KIET 2레벨 (산업그룹) 까지만 # build KSIC9 2-digit → KIET 1/2 레벨 mapping (가장 부유한 industry group 선택) grp = df.groupby("ksic9_2digit").agg({ "kiet1": lambda x: x.dropna.mode.iloc[0] if x.dropna.any else np.nan, "kiet2": lambda x: x.dropna.mode.iloc[0] if x.dropna.any else np.nan, }).reset_index log.append(f"\n## KSIC9 2-digit → KIET 그룹 매핑 (mode 기준)") log.append("```") log.append(grp.to_string(index=False)) log.append("```") # 5) baseline → KSIC9 2-digit aggregate bs_agg2 = (bs.dropna(subset=["ksic9_2digit"]).groupby(["h_code", "ksic9_2digit"])["employment"].sum.reset_index) h_total = bs_agg2.groupby("h_code")["employment"].sum.rename("h_total") bs_agg2 = bs_agg2.merge(h_total, on="h_code") bs_agg2["share"] = bs_agg2["employment"] / bs_agg2["h_total"].replace(0, np.nan) out_path = BARTIK / "baseline_shares_1994_ksic9_2digit.parquet" bs_agg2.to_parquet(out_path, index=False) log.append(f"\n- saved: `{out_path.relative_to(PROJ)}`") log.append(f"- rows: {len(bs_agg2):,}, distinct h_code: {bs_agg2['h_code'].nunique}, distinct KSIC9 2-digit: {bs_agg2['ksic9_2digit'].nunique}") # 6) HS6 ↔ KIET60 inspect log.append(f"\n## HS6 ↔ KIET60 매핑 (Comtrade input 준비)") fhs = CONC / "KIET60_to_HS6.xlsx" dfhs = pd.read_excel(fhs) log.append(f"- shape: {dfhs.shape}") log.append(f"- HS code 길이 distribution: {dfhs['hsc'].astype(str).str.len.value_counts.to_dict}") log.append(f"- 레벨1코드 distinct: {dfhs['레벨1코드'].nunique}") log.append(f"- 레벨2코드 distinct: {dfhs['레벨2코드'].nunique}") log.append(f"- 레벨3코드 distinct: {dfhs['레벨3코드'].nunique}") log.append(f"- 레벨1코드 distribution: {dfhs['레벨1코드'].value_counts.to_dict}") # 7) decision summary log.append("\n## 결정 사항 (다음 step 입력)") if n_mapped / len(bs) > 0.95: log.append(f"- ✅ KSIC 6→9 (2-digit) 변환률 {n_mapped/len(bs):.1%} → **KSIC9 2-digit 단위 Bartik 진행 권장**") log.append("- baseline: `baseline_shares_1994_ksic9_2digit.parquet` (h × KSIC9 2-digit)") log.append("- next: HS6 → KSIC9 2-digit 매핑으로 Comtrade 집계 (또는 KIET 2레벨 매개)") else: log.append(f"- ⚠️ KSIC 6→9 변환률 {n_mapped/len(bs):.1%} — 추가 crosswalk 필요") log.append("\n- aggregation level 옵션:") log.append(" - **KSIC9 2-digit (~24 industries)**: ADH 4-digit SIC 보다 coarse 하지만 robust ← 권장") log.append(" - KIET 3레벨 (~60 industries): ADH 와 동급 precision but KSIC 9차 4-digit 까지 변환 필요 (별도 turn)") log.append(" - KIET 2레벨 (~10 industries): too coarse, robustness only") out = LOGS / f"{TODAY}_kiet60_mapping_v2.md" out.write_text("\n".join(log), encoding="utf-8") print(f"[OK] {out}") if __name__ == "__main__": main
