"""
Step 3 — h_code 통합 매핑 빌드

Inputs:
  3_derived/sigungu/step1_codebook_old.csv     (1981-2021 long format)
  3_derived/sigungu/step2_raw_sigungu_by_year.csv  (raw mortality codes 1997-2023)
  3_derived/sigungu/step3c_codebook_2023.csv   (KOSTAT 2023 codebook)

Output:
  3_derived/sigungu/step3_h_code_mapping.csv
    columns: year, raw_code, h_code, h_name, sido_code, sido_name, event_note

h_code definition:
  Stable 5-digit administrative ID derived from the 2021 KOSTAT baseline (262 entries).
  - For each (year, raw_code), h_code is the corresponding 2021 entity.
  - Mergers/renames before 2021: PRE2021_REMAP (manual, based on KOSTAT codebook + 행정안전부 history).
  - 2023 changes (군위 cross-sido transfer + name normalization + 군 +200 renumber): handled below.

Coverage: 1997-2023 (27 years). Pre-1997 omitted (no mortality raw data).
"""
from __future__ import annotations
import sys
import io
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
DERIVED = ROOT / "3_derived" / "sigungu"
CB_OLD = DERIVED / "step1_codebook_old.csv"
RAW = DERIVED / "step2_raw_sigungu_by_year.csv"
CB23 = DERIVED / "step3c_codebook_2023.csv"
OUT = DERIVED / "step3_h_code_mapping.csv"
UNMATCHED_OUT = DERIVED / "step3_unmatched.csv"

# ----------------------------------------------------------------------
# Manual remap: pre-2021 raw_codes that disappeared / merged / renumbered
# Source: step1_codebook_old.csv anomaly listing + 행안부 sigungu 변천사
# Each entry: raw_code → (h_code, h_name, h_sido_code, h_sido_name, event_note)
# h_* fields = 2021-baseline successor entity
# ----------------------------------------------------------------------
PRE2021_REMAP: dict[int, tuple[int, str, int, str, str]] = {
    # 인천 남구 → 미추홀구 (2018.7.1 개칭) — 23030 → 23090 으로 코드 변경
    23030: (23090, "미추홀구(남구)", 23, "인천광역시", "2018.7.1 남구→미추홀구 개칭, 코드 23030→23090"),
    # 부천시 분구 폐지 (2016.7.4) — 31051/31052/31053 → 31050 통합
    31051: (31050, "부천시", 31, "경기도", "2016.7.4 부천시 일반구(원미/소사/오정) 폐지 → 31050 통합"),
    31052: (31050, "부천시", 31, "경기도", "2016.7.4 부천시 일반구(원미/소사/오정) 폐지 → 31050 통합"),
    31053: (31050, "부천시", 31, "경기도", "2016.7.4 부천시 일반구(원미/소사/오정) 폐지 → 31050 통합"),
    # 고양 일산구 → 일산동/서구 분구 (2005.5.16) — 31102 → 31103/31104. 분구이므로 부모 31100(고양시)로 매핑
    31102: (31100, "고양시", 31, "경기도", "2005.5.16 일산구 → 일산동/서구 분구. 부모 고양시(31100)로 매핑"),
    # 양주군 → 양주시 승격 (2003.10.19)
    31310: (31260, "양주시", 31, "경기도", "2003.10.19 양주군 → 양주시 승격, 코드 31310→31260"),
    # 여주군 → 여주시 승격 (2013.9.23)
    31320: (31280, "여주시", 31, "경기도", "2013.9.23 여주군 → 여주시 승격, 코드 31320→31280"),
    # 화성군 → 화성시 승격 (2001.3.21)
    31330: (31240, "화성시", 31, "경기도", "2001.3.21 화성군 → 화성시 승격, 코드 31330→31240"),
    # 광주군 → 광주시 승격 (2001.3.21)
    31340: (31250, "광주시", 31, "경기도", "2001.3.21 광주군 → 광주시 승격, 코드 31340→31250"),
    # 포천군 → 포천시 승격 (2003.10.19)
    31360: (31270, "포천시", 31, "경기도", "2003.10.19 포천군 → 포천시 승격, 코드 31360→31270"),
    # 안성군 → 안성시 승격 (1998.4.1) — 1997만 등재
    31390: (31220, "안성시", 31, "경기도", "1998.4.1 안성군 → 안성시 승격, 코드 31390→31220"),
    # 김포군 → 김포시 승격 (1998.4.1)
    31400: (31230, "김포시", 31, "경기도", "1998.4.1 김포군 → 김포시 승격, 코드 31400→31230"),
    # 청주시(통합 전) + 청원군 → 통합청주시 (2014.7.1)
    33010: (33040, "통합청주시", 33, "충청북도", "2014.7.1 청주시(舊)+청원군 → 통합청주시, 코드 33010→33040"),
    33310: (33040, "통합청주시", 33, "충청북도", "2014.7.1 청원군 → 통합청주시 흡수, 코드 33310→33040"),
    # 구 청주 산하 일반구 (1995-2014) — 통합 청주의 새 일반구 코드로 매핑
    # 33011 상당구(舊) → 33041 상당구(통합 후); 33012 흥덕구(舊) → 33043 흥덕구(통합 후)
    33011: (33041, "상당구", 33, "충청북도", "2014.7.1 통합청주시 출범, 상당구 코드 33011→33041"),
    33012: (33043, "흥덕구", 33, "충청북도", "2014.7.1 통합청주시 출범, 흥덕구 코드 33012→33043"),
    # 연기군 → 세종특별자치시 편입 (2012.7.1) — sido 변경
    34320: (29010, "세종특별자치시", 29, "세종특별자치시", "2012.7.1 충남 연기군 → 세종특별자치시 편입, 코드 34320→29010 (sido 변경)"),
    # 당진군 → 당진시 승격 (2012.1.1)
    34390: (34080, "당진시", 34, "충청남도", "2012.1.1 당진군 → 당진시 승격, 코드 34390→34080"),
    # 계룡출장소 → 계룡시 승격 (2003.9.19)
    34400: (34070, "계룡시", 34, "충청남도", "2003.9.19 계룡출장소 → 계룡시 승격, 코드 34400→34070"),
    # 효자출장소 (전북) — 1996-1997만 잠시 분리, 전주시(35010) 소속
    35013: (35010, "전주시", 35, "전라북도", "1996-1997 효자출장소(전주 효자) 잠시 코드 부여, 전주시(35010)로 통합"),
    # 여수시(舊) + 여천시 + 여천군 통합 → 여수시 (1998.4.1) — 36050 여천시, 36340 여천군 → 36020 여수시
    36050: (36020, "여수시", 36, "전라남도", "1998.4.1 여수시(舊)+여천시+여천군 → 통합여수시, 코드 36050→36020"),
    36340: (36020, "여수시", 36, "전라남도", "1998.4.1 여천군 → 통합여수시 흡수, 코드 36340→36020"),
    # 창원시(舊) + 마산시 + 진해시 → 통합창원시 (2010.7.1)
    38010: (38110, "통합창원시", 38, "경상남도", "2010.7.1 창원(舊)+마산+진해 → 통합창원시, 코드 38010→38110"),
    38020: (38110, "통합창원시", 38, "경상남도", "2010.7.1 마산시 → 통합창원시, 코드 38020→38110"),
    38040: (38110, "통합창원시", 38, "경상남도", "2010.7.1 진해시 → 통합창원시, 코드 38040→38110"),
    # 마산시 일반구 합포/회원 (1995-2000): 2000.12 마산 일반구 폐지, 2010 통합창원 후 마산합포구/마산회원구로 부활
    38021: (38113, "마산합포구", 38, "경상남도", "1995-2000 마산 합포구 → 2010.7.1 통합창원시 마산합포구로 코드 변경 38021→38113"),
    38022: (38114, "마산회원구", 38, "경상남도", "1995-2000 마산 회원구 → 2010.7.1 통합창원시 마산회원구로 코드 변경 38022→38114"),
    # 북제주군 + 제주시 → 제주시; 남제주군 + 서귀포시 → 서귀포시 (2006.7.1, 제주특별자치도 출범)
    39310: (39010, "제주시", 39, "제주특별자치도", "2006.7.1 제주특별자치도 출범, 북제주군 → 제주시 통합, 코드 39310→39010"),
    39320: (39020, "서귀포시", 39, "제주특별자치도", "2006.7.1 제주특별자치도 출범, 남제주군 → 서귀포시 통합, 코드 39320→39020"),
}

# ----------------------------------------------------------------------
# 2023 special cases — name normalization + cross-sido 군위 transfer
# Maps 2023 raw_code → (h_code, h_name, h_sido_code, h_sido_name, event_note)
# ----------------------------------------------------------------------
REMAP_2023: dict[int, tuple[int, str, int, str, str]] = {
    # 군위군 경북 → 대구 편입 (2023.7.1). h_code 는 경북 시절 코드 유지(stable panel ID)
    22520: (37310, "군위군", 22, "대구광역시", "2023.7.1 경북 군위군 → 대구 편입, raw_code 37310→22520. h_code 37310 유지(panel stable), sido_code 만 22로 변경"),
    # 인천 남구 → 미추홀구 — 2023 codebook 에선 '미추홀구' (괄호 제거), 2021 codebook 은 '미추홀구(남구)'
    23090: (23090, "미추홀구(남구)", 23, "인천광역시", "2018.7.1 남구→미추홀구 개칭. 코드 23090 동일, 2023 codebook에서 '(남구)' 표기 제거"),
    # 세종 — 2021: '세종시', 2023: '세종특별자치시'. 동일 entity.
    29010: (29010, "세종특별자치시", 29, "세종특별자치시", "2012.7.1 출범. 2023 codebook에서 정식명칭 '세종특별자치시' 표기"),
    # 통합청주시 — 2023 codebook 부모 코드 33040 (실제 사망 raw 데이터엔 미사용; 33041-33044 sub-구만 사용)
    33040: (33040, "통합청주시", 33, "충청북도", "2014.7.1 통합. 2023 codebook 부모코드 33040 (실데이터엔 33041-33044 sub-구만 사용)"),
    # 통합창원시 — 동일
    38110: (38110, "통합창원시", 38, "경상남도", "2010.7.1 통합. 2023 codebook 부모코드 38110 (실데이터엔 38111-38115 sub-구만 사용)"),
}

# ----------------------------------------------------------------------
# 2023 sido name update — 강원도 → 강원특별자치도 (2023.6.11)
# Used as sido_name override for 2023 only (does not change sido_code)
# ----------------------------------------------------------------------
SIDO_NAME_2023 = {
    32: "강원특별자치도",  # 2023.6.11 강원도→강원특별자치도
    35: "전라북도",  # (실제 전라북도→전북특별자치도 변경은 2024.1.18; 2023년은 전라북도 유지)
    39: "제주특별자치도",
}


def normalize_sigungu_name(name: str) -> str:
    """Strip parenthetical aliases for matching. e.g. '미추홀구(남구)' → '미추홀구'."""
    if name is None:
        return ""
    s = str(name).strip()
    if "(" in s:
        s = s.split("(")[0].strip()
    return s


def main() -> None:
    cb = pd.read_csv(CB_OLD)
    raw = pd.read_csv(RAW)
    cb23 = pd.read_csv(CB23)

    cb["raw_code"] = cb["raw_code"].astype(int)
    raw["raw_code"] = raw["raw_code"].astype(int)
    cb23["raw_code"] = cb23["raw_code"].astype(int)

    # 2021 baseline
    cb21 = cb[cb.year == 2021].copy()
    cb21["sigungu_name_norm"] = cb21["sigungu_name"].apply(normalize_sigungu_name)
    set21 = set(cb21["raw_code"].astype(int))

    # ------------------------------------------------------------------
    # Build (year, raw_code) -> h_code mapping for 1997-2022
    # ------------------------------------------------------------------
    rows: list[dict] = []
    unmatched: list[dict] = []

    for year in sorted(raw[raw.year <= 2022]["year"].unique()):
        sub = raw[raw.year == year][["raw_code"]].drop_duplicates()
        for rc in sub["raw_code"]:
            rc_int = int(rc)
            if rc_int in set21:
                # h_code = raw_code; lookup name from 2021 baseline
                row21 = cb21[cb21.raw_code == rc_int].iloc[0]
                rows.append({
                    "year": int(year),
                    "raw_code": rc_int,
                    "h_code": rc_int,
                    "h_name": row21["sigungu_name"],
                    "sido_code": int(row21["sido_code"]),
                    "sido_name": row21["sido_name"],
                    "event_note": "",
                })
            elif rc_int in PRE2021_REMAP:
                hc, hn, sc, sn, note = PRE2021_REMAP[rc_int]
                rows.append({
                    "year": int(year),
                    "raw_code": rc_int,
                    "h_code": hc,
                    "h_name": hn,
                    "sido_code": sc,
                    "sido_name": sn,
                    "event_note": note,
                })
            else:
                unmatched.append({"year": int(year), "raw_code": rc_int})

    # ------------------------------------------------------------------
    # Build (2023, raw_code) -> h_code via:
    #   1. REMAP_2023 special cases (5 entries)
    #   2. Within-sido name match (normalized) → 2021 h_code
    # ------------------------------------------------------------------
    raw_2023 = raw[raw.year == 2023][["raw_code"]].drop_duplicates()
    cb23_set = cb23[["sido_code", "raw_code", "sigungu_name"]].copy()
    cb23_set["sigungu_name_norm"] = cb23_set["sigungu_name"].apply(normalize_sigungu_name)

    # within-sido name match
    name_join = cb23_set.merge(
        cb21[["sido_code", "sigungu_name_norm", "raw_code", "sigungu_name", "sido_name"]].rename(
            columns={"raw_code": "h_code", "sigungu_name": "h_name", "sido_name": "h_sido_name"}
        ),
        on=["sido_code", "sigungu_name_norm"],
        how="left",
    )
    name_join_map: dict[int, tuple[int, str, int, str, str]] = {}
    for _, r in name_join.iterrows():
        rc = int(r["raw_code"])
        if rc in REMAP_2023:
            continue
        if pd.isna(r["h_code"]):
            continue
        hc = int(r["h_code"])
        # event note: "renumbered" if raw_code != h_code
        note = ""
        if rc != hc:
            note = f"2023 KOSTAT 코드집 raw_code 변경: {hc}(2021)→{rc}(2023). h_code 유지"
        name_join_map[rc] = (hc, r["h_name"], int(r["sido_code"]), r["h_sido_name"], note)

    # raw 2023 codes from death data
    for rc in sorted(raw_2023["raw_code"].astype(int)):
        if rc in REMAP_2023:
            hc, hn, sc, sn, note = REMAP_2023[rc]
            rows.append({
                "year": 2023, "raw_code": rc, "h_code": hc, "h_name": hn,
                "sido_code": sc, "sido_name": sn, "event_note": note,
            })
        elif rc in name_join_map:
            hc, hn, sc, sn, note = name_join_map[rc]
            # apply 2023 sido name override (e.g., 강원도 → 강원특별자치도)
            sn_final = SIDO_NAME_2023.get(sc, sn)
            rows.append({
                "year": 2023, "raw_code": rc, "h_code": hc, "h_name": hn,
                "sido_code": sc, "sido_name": sn_final, "event_note": note,
            })
        else:
            unmatched.append({"year": 2023, "raw_code": rc})

    out = pd.DataFrame(rows)
    out = out.sort_values(["year", "raw_code"]).reset_index(drop=True)
    out.to_csv(OUT, index=False, encoding="utf-8-sig")

    # Apply 2023 sido name override to all 2023 rows (including REMAP_2023 entries)
    mask23 = out["year"] == 2023
    for sc, sn in SIDO_NAME_2023.items():
        m = mask23 & (out["sido_code"] == sc)
        out.loc[m, "sido_name"] = sn
    out.to_csv(OUT, index=False, encoding="utf-8-sig")

    # Unmatched
    unm = pd.DataFrame(unmatched)
    if len(unm):
        unm.to_csv(UNMATCHED_OUT, index=False, encoding="utf-8-sig")
    else:
        # touch empty file with header
        pd.DataFrame(columns=["year", "raw_code"]).to_csv(UNMATCHED_OUT, index=False, encoding="utf-8-sig")

    # Report
    print(f"[step3] total mapping rows: {len(out)}")
    print(f"[step3] unmatched rows: {len(unm)}")
    print(f"[step3] year coverage: {sorted(out['year'].unique().tolist())}")
    print(f"[step3] distinct h_code: {out['h_code'].nunique()}")
    print(f"[step3] wrote: {OUT}")
    print(f"[step3] wrote: {UNMATCHED_OUT}")
    if len(unm):
        print("\n[step3] UNMATCHED preview:")
        print(unm.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
