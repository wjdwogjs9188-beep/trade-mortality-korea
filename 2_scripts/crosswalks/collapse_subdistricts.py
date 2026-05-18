"""Collapse 일반시 자치구 children → parent 시 in sigungu crosswalk.

Input  : 1_codebooks/sigungu_crosswalk.csv  (250-256 h_codes)
Output : 1_codebooks/sigungu_crosswalk_v2.csv
         1_codebooks/child_to_parent_mapping.csv
         1_codebooks/crosswalk_merge_report.md

Rationale
---------
The KOSTAT 2021 baseline crosswalk preserves 일반시 자치구 (수원 장안구 등) as
distinct h_codes. For panel analysis (5-year stacked first-difference) this
breaks balance because pre-divide years exist only at the parent (시) level.
Collapsing children → parent yields a balanced 1997-2023 panel.

광역시 자치구 (서울/부산/...)는 collapse 대상이 아니다. 이미 KOSTAT 표준 단위.
일반시 자치구만 그 시(parent) 단위로 통합한다.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "1_codebooks" / "sigungu_crosswalk.csv"
OUT_CSV = REPO / "1_codebooks" / "sigungu_crosswalk_v2.csv"
OUT_MAP = REPO / "1_codebooks" / "child_to_parent_mapping.csv"
OUT_REPORT = REPO / "1_codebooks" / "crosswalk_merge_report.md"

# child h_code -> (parent h_code, parent h_name)
# Derived from inspection of sigungu_crosswalk.csv (sub_units check) and
# sigungu_changes_history.md. Only 일반시 자치구. 광역시 자치구는 제외.
COLLAPSE_MAP: dict[str, tuple[str, str]] = {
    # 수원시 (parent NEW — never appears as h_code in v1)
    "31011": ("31010", "수원시"),
    "31012": ("31010", "수원시"),
    "31013": ("31010", "수원시"),
    "31014": ("31010", "수원시"),
    # 성남시 (NEW)
    "31021": ("31020", "성남시"),
    "31022": ("31020", "성남시"),
    "31023": ("31020", "성남시"),
    # 안양시 (NEW)
    "31041": ("31040", "안양시"),
    "31042": ("31040", "안양시"),
    # 안산시 (existing)
    "31091": ("31090", "안산시"),
    "31092": ("31090", "안산시"),
    # 고양시 (existing)
    "31101": ("31100", "고양시"),
    "31103": ("31100", "고양시"),
    "31104": ("31100", "고양시"),
    # 용인시 (existing)
    "31191": ("31190", "용인시"),
    "31192": ("31190", "용인시"),
    "31193": ("31190", "용인시"),
    # 통합청주시 (existing)
    "33041": ("33040", "통합청주시"),
    "33042": ("33040", "통합청주시"),
    "33043": ("33040", "통합청주시"),
    "33044": ("33040", "통합청주시"),
    # 천안시 (existing)
    "34011": ("34010", "천안시"),
    "34012": ("34010", "천안시"),
    # 전주시 (NEW)
    "35011": ("35010", "전주시"),
    "35012": ("35010", "전주시"),
    # 포항시 (NEW)
    "37011": ("37010", "포항시"),
    "37012": ("37010", "포항시"),
    # 통합창원시 (existing)
    "38111": ("38110", "통합창원시"),
    "38112": ("38110", "통합창원시"),
    "38113": ("38110", "통합창원시"),
    "38114": ("38110", "통합창원시"),
    "38115": ("38110", "통합창원시"),
}


def main() -> None:
    df = pd.read_csv(SRC, dtype=str, encoding="utf-8")
    df["event_note"] = df["event_note"].fillna("")
    n_rows_in = len(df)
    n_h_in = df["h_code"].nunique()
    n_raw_in = df["raw_code"].nunique()

    # --- collapse ---
    is_child = df["h_code"].isin(COLLAPSE_MAP)
    n_child_rows = int(is_child.sum())

    df2 = df.copy()
    df2.loc[is_child, "h_name"] = df2.loc[is_child, "h_code"].map(
        lambda c: COLLAPSE_MAP[c][1]
    )
    df2.loc[is_child, "h_code"] = df2.loc[is_child, "h_code"].map(
        lambda c: COLLAPSE_MAP[c][0]
    )
    # Annotate event_note for collapsed rows (preserve any existing note)
    new_note = "subdistrict_collapsed_to_parent_2026-05-02"
    def _merge_note(s: str) -> str:
        s = (s or "").strip()
        return f"{s}; {new_note}" if s else new_note
    df2.loc[is_child, "event_note"] = df2.loc[is_child, "event_note"].apply(_merge_note)

    # --- validation ---
    n_h_out = df2["h_code"].nunique()
    n_raw_out = df2["raw_code"].nunique()

    val: dict[str, tuple[bool, str]] = {}

    # V1: row count preserved
    val["V1 row count preserved"] = (
        len(df2) == n_rows_in,
        f"in={n_rows_in} out={len(df2)}",
    )
    # V2: every raw_code preserved (no drops)
    val["V2 raw_code preserved (no drops)"] = (
        n_raw_out == n_raw_in,
        f"in={n_raw_in} out={n_raw_out}",
    )
    # V3: distinct h_code reduced exactly as expected
    children_dropped = set(COLLAPSE_MAP) & set(df["h_code"])
    parents_existing = {p for c, (p, _) in COLLAPSE_MAP.items() if p in set(df["h_code"])}
    parents_new = {p for c, (p, _) in COLLAPSE_MAP.items() if p not in set(df["h_code"])}
    expected_delta = -len(children_dropped) + len(parents_new)
    val["V3 h_code count delta matches expected"] = (
        n_h_out - n_h_in == expected_delta,
        f"in={n_h_in} out={n_h_out} delta={n_h_out-n_h_in} expected={expected_delta} "
        f"(children={len(children_dropped)} new_parents={len(parents_new)})",
    )
    # V4: every collapsed parent appears in all 27 years
    years_full = set(df["year"].unique())
    parents_targets = {p for _, (p, _) in COLLAPSE_MAP.items()}
    bad_parents = []
    for p in sorted(parents_targets):
        years_present = set(df2[df2["h_code"] == p]["year"].unique())
        if years_present != years_full:
            missing = sorted(years_full - years_present)
            bad_parents.append(f"{p}={missing}")
    val["V4 collapsed parents balanced over all years"] = (
        len(bad_parents) == 0,
        f"missing_year_parents={bad_parents}" if bad_parents else "all 11 parents 1997-2023",
    )
    # V5: 광역시 자치구 untouched (sample check on 11230 강남구)
    seoul_gangnam_before = df[(df["h_code"] == "11230")][["raw_code", "h_code", "h_name"]].drop_duplicates()
    seoul_gangnam_after = df2[(df2["h_code"] == "11230")][["raw_code", "h_code", "h_name"]].drop_duplicates()
    val["V5 광역시 자치구 untouched (강남구 spot)"] = (
        seoul_gangnam_before.equals(seoul_gangnam_after),
        f"identical={seoul_gangnam_before.equals(seoul_gangnam_after)}",
    )
    # V5b: 광역시 자치구 universal — ensure no h_code in sido 11/21/22/23/24/25/26 was touched
    metro_sidos = {"11", "21", "22", "23", "24", "25", "26"}
    metro_before = df[df["sido_code"].isin(metro_sidos)].sort_values(["year", "raw_code"]).reset_index(drop=True)
    metro_after = df2[df2["sido_code"].isin(metro_sidos)].sort_values(["year", "raw_code"]).reset_index(drop=True)
    val["V5b 광역시 rows fully unchanged"] = (
        metro_before.equals(metro_after),
        f"all 7 metro sidos rows identical={metro_before.equals(metro_after)}",
    )
    # V6: 세종 (29110/29010) untouched
    sejong_before = df[df["sido_code"] == "29"].sort_values(["year", "raw_code"]).reset_index(drop=True)
    sejong_after = df2[df2["sido_code"] == "29"].sort_values(["year", "raw_code"]).reset_index(drop=True)
    val["V6 세종 untouched"] = (
        sejong_before.equals(sejong_after),
        f"identical={sejong_before.equals(sejong_after)}",
    )

    all_pass = all(v[0] for v in val.values())

    # --- spot checks ---
    spot_checks = [
        ("31101", "31100", "고양 덕양구 → 고양시"),
        ("38111", "38110", "창원 의창구 → 통합창원시"),
        ("38113", "38110", "창원 마산합포구 → 통합창원시"),
        ("33041", "33040", "청주 상당구 → 통합청주시"),
        ("37011", "37010", "포항 남구 → 포항시"),
        ("11230", "11230", "서울 강남구 → 변경 없음 (광역시 자치구)"),
        ("21090", "21090", "부산 해운대구 → 변경 없음 (광역시 자치구)"),
    ]
    spot_results = []
    for src_h, exp_parent, label in spot_checks:
        # Pick a row in df where h_code==src_h (any year), look up post-collapse h_code
        rows_pre = df[df["h_code"] == src_h]
        if len(rows_pre) == 0:
            spot_results.append((label, src_h, "NOT FOUND in v1", "?", False))
            continue
        rows_post = df2[(df2["raw_code"].isin(rows_pre["raw_code"])) & (df2["year"].isin(rows_pre["year"]))]
        # raw_code in v1 == raw_code in v2 (only h_code/h_name change), so use raw_code as key
        sample_raw = rows_pre.iloc[0]["raw_code"]
        sample_year = rows_pre.iloc[0]["year"]
        post = df2[(df2["raw_code"] == sample_raw) & (df2["year"] == sample_year)]
        post_h = post.iloc[0]["h_code"] if len(post) > 0 else "?"
        ok = post_h == exp_parent
        spot_results.append((label, src_h, exp_parent, post_h, ok))

    # --- write outputs ---
    df2.to_csv(OUT_CSV, index=False, encoding="utf-8")

    map_rows = []
    for child, (parent, pname) in sorted(COLLAPSE_MAP.items()):
        cn = df[df["h_code"] == child]["h_name"].iloc[0] if (df["h_code"] == child).any() else "?"
        map_rows.append({
            "child_h_code": child,
            "child_h_name": cn,
            "parent_h_code": parent,
            "parent_h_name": pname,
            "parent_was_new": parent in parents_new,
        })
    pd.DataFrame(map_rows).to_csv(OUT_MAP, index=False, encoding="utf-8")

    # --- write report ---
    lines: list[str] = []
    lines.append("# Crosswalk Merge Report — 일반시 자치구 → Parent 시 collapse")
    lines.append("")
    lines.append(f"- Generated: 2026-05-02")
    lines.append(f"- Source: `1_codebooks/sigungu_crosswalk.csv`")
    lines.append(f"- Output: `1_codebooks/sigungu_crosswalk_v2.csv`")
    lines.append(f"- Mapping table: `1_codebooks/child_to_parent_mapping.csv`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| metric | before | after | delta |")
    lines.append(f"|---|---:|---:|---:|")
    lines.append(f"| total rows | {n_rows_in:,} | {len(df2):,} | {len(df2)-n_rows_in:+d} |")
    lines.append(f"| distinct h_code | {n_h_in} | {n_h_out} | {n_h_out-n_h_in:+d} |")
    lines.append(f"| distinct raw_code | {n_raw_in:,} | {n_raw_out:,} | {n_raw_out-n_raw_in:+d} |")
    lines.append(f"| child rows reassigned | — | {n_child_rows:,} | — |")
    lines.append("")
    lines.append("## Collapse policy")
    lines.append("")
    lines.append("- **Collapsed**: 일반시 자치구 (광역시 외) — children sharing a parent 시 prefix.")
    lines.append("- **Untouched**: 광역시 자치구 (sido 11/21/22/23/24/25/26), 세종, 강원/충남/전남/제주 일반시.")
    lines.append("- 새 parent h_code 5건 (수원 31010, 성남 31020, 안양 31040, 전주 35010, 포항 37010) — pre-collapse 에는 raw_code 로도, h_code 로도 등장하지 않음 → child raw_code 이 parent h_code 로 합쳐지면서 신규 도입.")
    lines.append("- 기존 parent h_code 6건 (안산 31090, 고양 31100, 용인 31190, 청주 33040, 천안 34010, 창원 38110) — 이미 v1 에 존재하나 일부 연도만 커버 → collapse 후 27 년 전체 커버.")
    lines.append("")
    lines.append("## Child → parent mapping (32 children, 11 parents)")
    lines.append("")
    lines.append("| child h_code | child name | parent h_code | parent name | parent was new |")
    lines.append("|---:|---|---:|---|:---:|")
    for r in map_rows:
        nw = "✓" if r["parent_was_new"] else ""
        lines.append(f"| {r['child_h_code']} | {r['child_h_name']} | {r['parent_h_code']} | {r['parent_h_name']} | {nw} |")
    lines.append("")
    lines.append("## Validation")
    lines.append("")
    lines.append("| check | result | detail |")
    lines.append("|---|:---:|---|")
    for k, (ok, detail) in val.items():
        mark = "PASS" if ok else "**FAIL**"
        lines.append(f"| {k} | {mark} | {detail} |")
    lines.append("")
    lines.append(f"**Overall**: {'ALL PASS' if all_pass else '**FAIL — DO NOT ADOPT**'}")
    lines.append("")
    lines.append("## Spot checks")
    lines.append("")
    lines.append("| label | source h_code | expected | actual | result |")
    lines.append("|---|---:|---:|---:|:---:|")
    for label, src, exp, got, ok in spot_results:
        mark = "PASS" if ok else "**FAIL**"
        lines.append(f"| {label} | {src} | {exp} | {got} | {mark} |")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("1. raw_code 는 **건드리지 않음**. h_code 와 h_name 만 child → parent 로 재할당. event_note 에 `subdistrict_collapsed_to_parent_2026-05-02` 추가.")
    lines.append("2. mapping_weight 컬럼은 v1 에 없음 (모든 매핑 1:1). 추후 필요시 별도 추가.")
    lines.append("3. 통합창원시 38110 의 마산합포/마산회원구 (38113/38114) 는 1997-2009 에도 raw 38021/38022 로 등장 → collapse 후 raw 38010 (창원 舊), 38020 (마산), 38040 (진해), 38021/38022 (마산 자치구) 모두 h_code 38110 로 합산됨. 통합창원시 = 창원+마산+진해 전 영역으로 해석 일관.")
    lines.append("4. 통합청주시 33040 의 raw 33310 (청원군, 1997-2013) 도 기존부터 33040 으로 매핑되어 있어 그대로 유지. collapse 후 청주시 = 상당+서원+흥덕+청원 전 영역.")
    lines.append("5. **다음 panel build (사망/인구/산업) 에서는 이 v2 crosswalk + child_to_parent_mapping.csv 를 함께 적용**해야 KOSTAT raw 의 자치구 단위 record 가 parent 시 단위로 올바르게 합산됨.")
    lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    # --- console print ---
    print(f"[in ] rows={n_rows_in:,}  h_code={n_h_in}  raw_code={n_raw_in:,}")
    print(f"[out] rows={len(df2):,}  h_code={n_h_out}  raw_code={n_raw_out:,}")
    print(f"[delta] h_code={n_h_out-n_h_in:+d} (children dropped={len(children_dropped)}, new parents={len(parents_new)})")
    print(f"[child rows reassigned] {n_child_rows:,}")
    print()
    print("Validation:")
    for k, (ok, detail) in val.items():
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {k}: {detail}")
    print()
    print("Spot checks:")
    for label, src, exp, got, ok in spot_results:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {label}: src={src} expected={exp} got={got}")
    print()
    print(f"Wrote: {OUT_CSV.relative_to(REPO)}")
    print(f"Wrote: {OUT_MAP.relative_to(REPO)}")
    print(f"Wrote: {OUT_REPORT.relative_to(REPO)}")

    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
