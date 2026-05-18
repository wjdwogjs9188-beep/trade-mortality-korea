"""Phase 2 sub-task 2.5a -- M3 KOSIS family aggregates ETL.

Reads 4 KOSIS sigungu raw files:
  - 시군구 혼인.xls (SpreadsheetML XML, EUC-KR)
  - 시군구 이혼.xls (SpreadsheetML XML, EUC-KR)
  - 시군구 출생아.xls (SpreadsheetML XML, EUC-KR)
  - 시군구_합계출산율.xlsx (binary xlsx)

Builds sigungu x year panel of marriage / divorce / fertility, then computes
long-difference 1997-1999 baseline vs 2018-2022 endpoint (mirror main spec).
Marriage/divorce/birth raw is monthly counts -> aggregate to annual then
convert to rates per 1000 working-age population. Fertility rate (TFR) is
already an annual rate.
"""
import io
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from lxml import etree

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
M3_RAW = PROJ / "0_raw" / "kosis_family_mediators"
DERIVED = PROJ / "3_derived"
DERIVED.mkdir(exist_ok=True)

NS = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}

SIDO_SUFFIXES = ("특별시", "광역시", "특별자치시", "특별자치도", "도")


def parse_spreadsheetml(fp: Path) -> pd.DataFrame:
    """Parse Excel 2003 SpreadsheetML XML (EUC-KR) -> long DataFrame.

    Returns DataFrame with columns: ['sido_name', 'sigungu_name', 'year', 'month', 'value'].
    """
    raw = fp.read_bytes()
    text = raw.decode("cp949")
    text = re.sub(r'encoding="EUC-KR"', 'encoding="utf-8"', text)
    parser = etree.XMLParser(recover=True)
    tree = etree.fromstring(text.encode("utf-8"), parser=parser)
    ws_list = tree.findall(".//ss:Worksheet", NS)
    if not ws_list:
        raise RuntimeError(f"No worksheets in {fp.name}")
    ws = ws_list[0]
    rows = ws.findall(".//ss:Row", NS)
    grid: list[list[str | None]] = []
    for r in rows:
        cells = r.findall("ss:Cell", NS)
        vals: list[str | None] = []
        for c in cells:
            idx_attr = c.get("{urn:schemas-microsoft-com:office:spreadsheet}Index")
            if idx_attr is not None:
                target = int(idx_attr) - 1
                while len(vals) < target:
                    vals.append(None)
            d = c.find("ss:Data", NS)
            vals.append(d.text if d is not None else None)
        grid.append(vals)

    header = grid[1]
    data_rows = grid[2:]
    period_cols = []
    for j, h in enumerate(header):
        if h is None:
            continue
        s = str(h).strip()
        m = re.match(r"^(\d{4})\.(\d{1,2})", s)
        if m:
            period_cols.append((j, int(m.group(1)), int(m.group(2))))
            continue
        m2 = re.match(r"^(\d{4})\b", s)
        if m2:
            period_cols.append((j, int(m2.group(1)), 0))

    long_rows = []
    current_sido = None
    for row in data_rows:
        if not row:
            continue
        name = row[0]
        if name is None:
            continue
        nm = str(name).strip()
        item = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ""
        if nm in ("전국", "전국합계", "전국 합계"):
            continue
        if any(nm.endswith(s) for s in SIDO_SUFFIXES):
            current_sido = nm
            continue
        for j, yr, mo in period_cols:
            v = row[j] if j < len(row) else None
            if v is None or str(v).strip() in ("", "-", "X", "..."):
                continue
            try:
                num = float(str(v).replace(",", ""))
            except Exception:
                continue
            long_rows.append(
                {
                    "sido_name": current_sido,
                    "sigungu_name": nm,
                    "item": item,
                    "year": yr,
                    "month": mo,
                    "value": num,
                }
            )
    return pd.DataFrame(long_rows)


def parse_xlsx_tfr(fp: Path) -> pd.DataFrame:
    """Parse 시군구_합계출산율.xlsx (year x {births, TFR} pairs)."""
    df = pd.read_excel(fp, header=None, engine="openpyxl")
    year_row = df.iloc[0].astype(str)
    label_row = df.iloc[1].astype(str)
    long_rows = []
    current_sido = None
    for ri in range(2, len(df)):
        nm = df.iloc[ri, 0]
        if pd.isna(nm):
            continue
        nm = str(nm).strip()
        if nm in ("전국", "전국합계", "전국 합계", "계"):
            continue
        if any(nm.endswith(s) for s in SIDO_SUFFIXES):
            current_sido = nm
            continue
        for ci in range(1, df.shape[1]):
            yr_s = year_row.iloc[ci]
            lab = label_row.iloc[ci]
            m = re.match(r"^(\d{4})", str(yr_s))
            if not m:
                continue
            yr = int(m.group(1))
            if "합계출산율" not in str(lab):
                continue
            v = df.iloc[ri, ci]
            if pd.isna(v):
                continue
            try:
                num = float(v)
            except Exception:
                continue
            long_rows.append(
                {"sido_name": current_sido, "sigungu_name": nm, "year": yr, "tfr": num}
            )
    return pd.DataFrame(long_rows)


def build_name_to_hcode(xw: pd.DataFrame) -> dict:
    """sido_name + sigungu_name -> h_code (latest mapping)."""
    latest = xw.sort_values("year").drop_duplicates(["sido_name", "h_name"], keep="last")
    lookup = {}
    for _, r in latest.iterrows():
        lookup[(str(r["sido_name"]).strip(), str(r["h_name"]).strip())] = int(r["h_code"])
    # Also build sigungu-only fallback (only if name unique)
    name_counts = xw.drop_duplicates(["h_code"])["h_name"].value_counts()
    unique_names = set(name_counts[name_counts == 1].index)
    return lookup, unique_names


def attach_hcode(df: pd.DataFrame, lookup: dict, unique_names: set, xw: pd.DataFrame) -> pd.DataFrame:
    name_only = (
        xw.drop_duplicates(["h_code"]).set_index("h_name")["h_code"].to_dict()
    )

    def lk(row):
        key = (str(row["sido_name"]).strip() if row["sido_name"] else "", str(row["sigungu_name"]).strip())
        if key in lookup:
            return lookup[key]
        if row["sigungu_name"] in unique_names:
            return name_only.get(row["sigungu_name"])
        # Try without sido (might match via name_only if name happens to be unique anyway)
        return None

    df = df.copy()
    df["h_code"] = df.apply(lk, axis=1)
    return df


def main():
    print("[step1] parse 4 KOSIS family raw files")
    df_marr = parse_spreadsheetml(M3_RAW / "시군구 혼인.xls")
    df_div = parse_spreadsheetml(M3_RAW / "시군구 이혼.xls")
    df_birth = parse_spreadsheetml(M3_RAW / "시군구 출생아.xls")
    df_tfr = parse_xlsx_tfr(M3_RAW / "시군구_합계출산율.xlsx")
    print(f"  marriage long rows: {len(df_marr)}, year range: {df_marr['year'].min()}-{df_marr['year'].max()}")
    print(f"  divorce  long rows: {len(df_div)}, year range: {df_div['year'].min()}-{df_div['year'].max()}")
    print(f"  birth    long rows: {len(df_birth)}, year range: {df_birth['year'].min()}-{df_birth['year'].max()}")
    print(f"  tfr      long rows: {len(df_tfr)}, year range: {df_tfr['year'].min()}-{df_tfr['year'].max()}")

    print("\n[step2] aggregate monthly -> annual counts (filter to total/계 only)")
    # Marriage / divorce: 항목 == '혼인' / '이혼' (single item)
    marr_y = df_marr.groupby(["sido_name", "sigungu_name", "year"], as_index=False)["value"].sum()
    marr_y.rename(columns={"value": "marriages"}, inplace=True)
    div_y = df_div.groupby(["sido_name", "sigungu_name", "year"], as_index=False)["value"].sum()
    div_y.rename(columns={"value": "divorces"}, inplace=True)

    # Births: 항목 has '계[명]' / '남자[명]' / '여자[명]' -> filter to 계
    if not df_birth.empty:
        birth_total = df_birth[df_birth["item"].str.startswith("계", na=False)]
        if len(birth_total) == 0:
            # Fallback: if no '계' filter matched, use sum / 2 (male + female)
            print(f"  [warn] no '계' item in births; sample items: {df_birth['item'].unique()[:5]}")
            birth_total = df_birth
        birth_y = birth_total.groupby(["sido_name", "sigungu_name", "year"], as_index=False)["value"].sum()
        birth_y.rename(columns={"value": "births"}, inplace=True)
    else:
        birth_y = pd.DataFrame(columns=["sido_name", "sigungu_name", "year", "births"])

    print("\n[step3] attach h_code via crosswalk")
    xw = pd.read_csv(PROJ / "1_codebooks" / "sigungu_crosswalk.csv")
    lookup, unique_names = build_name_to_hcode(xw)
    marr_y = attach_hcode(marr_y, lookup, unique_names, xw)
    div_y = attach_hcode(div_y, lookup, unique_names, xw)
    birth_y = attach_hcode(birth_y, lookup, unique_names, xw)
    df_tfr = attach_hcode(df_tfr, lookup, unique_names, xw)

    for label, d in [("marr", marr_y), ("div", div_y), ("birth", birth_y), ("tfr", df_tfr)]:
        unmatched_n = d["h_code"].isna().sum()
        print(f"  {label}: matched {len(d) - unmatched_n} / {len(d)} (unmatched {unmatched_n})")
        if unmatched_n > 0:
            samp = d[d["h_code"].isna()][["sido_name", "sigungu_name"]].drop_duplicates().head(5)
            print(f"    sample unmatched: {samp.values.tolist()}")

    # Drop unmatched
    marr_y = marr_y.dropna(subset=["h_code"]).copy()
    div_y = div_y.dropna(subset=["h_code"]).copy()
    birth_y = birth_y.dropna(subset=["h_code"]).copy()
    df_tfr = df_tfr.dropna(subset=["h_code"]).copy()
    for d in (marr_y, div_y, birth_y, df_tfr):
        d["h_code"] = d["h_code"].astype(int)

    # h_code may have multiple entries (e.g., merged sigungu) -> sum within h_code+year
    marr_y = marr_y.groupby(["h_code", "year"], as_index=False)["marriages"].sum()
    div_y = div_y.groupby(["h_code", "year"], as_index=False)["divorces"].sum()
    birth_y = birth_y.groupby(["h_code", "year"], as_index=False)["births"].sum()
    df_tfr = df_tfr.groupby(["h_code", "year"], as_index=False)["tfr"].mean()

    print("\n[step4] merge population denominator")
    pop = pd.read_csv(PROJ / "0_raw" / "kosis_population" / "population_combined.csv")
    print(f"  pop columns: {pop.columns.tolist()}, shape: {pop.shape}")
    # Schema: C1=sigungu code (5-digit) or sido (2-digit) or 0 (전국), C2=sex (0/1/2), C3=age (0=계),
    # C3_NM = age band label.
    pop["C1"] = pop["C1"].astype(int)
    pop_sg = pop[(pop["C1"] >= 10000) & (pop["C2"] == 0) & (pop["C3"] == 0)].copy()
    pop_sg = pop_sg.rename(columns={"C1": "h_code"})
    pop_agg = pop_sg.groupby(["h_code", "year"], as_index=False)["population"].sum()
    pop_agg["h_code"] = pop_agg["h_code"].astype(int)
    print(f"  pop_agg rows: {len(pop_agg)}, h_code n: {pop_agg['h_code'].nunique()}")

    panel = (
        marr_y.merge(div_y, on=["h_code", "year"], how="outer")
        .merge(birth_y, on=["h_code", "year"], how="outer")
        .merge(df_tfr, on=["h_code", "year"], how="outer")
        .merge(pop_agg, on=["h_code", "year"], how="left")
    )
    panel["marriage_rate"] = panel["marriages"] / panel["population"] * 1000.0
    panel["divorce_rate"] = panel["divorces"] / panel["population"] * 1000.0
    panel["fertility_rate"] = panel["tfr"]

    panel = panel.sort_values(["h_code", "year"]).reset_index(drop=True)
    out_panel = DERIVED / "m3_kosis_family_panel.parquet"
    panel[
        [
            "h_code",
            "year",
            "marriages",
            "divorces",
            "births",
            "population",
            "marriage_rate",
            "divorce_rate",
            "fertility_rate",
        ]
    ].to_parquet(out_panel, index=False)
    print(f"  panel written: {out_panel.name} (rows={len(panel)}, h_code_n={panel['h_code'].nunique()})")

    print("\n[step5] long-difference 1997-1999 vs 2018-2022")
    base_yr = list(range(1997, 2000))
    end_yr = list(range(2018, 2023))
    if panel["year"].min() > 1999:
        # marriage/divorce data starts 2000; use 2000-2002 as baseline fallback
        base_yr = list(range(2000, 2003))
        print(f"  [note] data starts {panel['year'].min()} -> using baseline window {base_yr}")

    def long_diff(df, var):
        b = df[df["year"].isin(base_yr)].groupby("h_code")[var].mean().rename(f"{var}_b")
        e = df[df["year"].isin(end_yr)].groupby("h_code")[var].mean().rename(f"{var}_e")
        d = pd.concat([b, e], axis=1)
        d[f"delta_{var}"] = np.log(d[f"{var}_e"] + 1e-3) - np.log(d[f"{var}_b"] + 1e-3)
        return d.reset_index()

    delta_marr = long_diff(panel, "marriage_rate").rename(
        columns={"delta_marriage_rate": "delta_marriage"}
    )
    delta_div = long_diff(panel, "divorce_rate").rename(
        columns={"delta_divorce_rate": "delta_divorce"}
    )
    delta_fert = long_diff(panel, "fertility_rate").rename(
        columns={"delta_fertility_rate": "delta_fertility"}
    )

    delta = (
        delta_marr[["h_code", "delta_marriage"]]
        .merge(delta_div[["h_code", "delta_divorce"]], on="h_code", how="outer")
        .merge(delta_fert[["h_code", "delta_fertility"]], on="h_code", how="outer")
    )
    out_delta = DERIVED / "m3_delta_panel.parquet"
    delta.to_parquet(out_delta, index=False)
    print(f"  delta written: {out_delta.name} (rows={len(delta)})")
    print(f"  delta_marriage  describe: mean={delta['delta_marriage'].mean():+.4f}, std={delta['delta_marriage'].std():.4f}, n={delta['delta_marriage'].notna().sum()}")
    print(f"  delta_divorce   describe: mean={delta['delta_divorce'].mean():+.4f}, std={delta['delta_divorce'].std():.4f}, n={delta['delta_divorce'].notna().sum()}")
    print(f"  delta_fertility describe: mean={delta['delta_fertility'].mean():+.4f}, std={delta['delta_fertility'].std():.4f}, n={delta['delta_fertility'].notna().sum()}")
    print("\n=== M3 ETL complete ===")


if __name__ == "__main__":
    main()
