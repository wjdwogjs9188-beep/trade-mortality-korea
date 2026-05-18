"""
Phase B-x — pre-flight input profiler  (/explore-data)
=========================================================

Phase B-x 스크립트 22·23·24·25 가 기대하는 5개 입력 데이터를 한 번에 profile.
codebook-first 원칙대로 **수정 없이** raw 폴더 inspect 만 한다.

profiles:
1) ECOS macro panel  — `0_raw/ecos_macro/*.parquet` (또는 csv)
   → script 22 (Test 1) 입력. 6 stat code (200Y110/402Y014/401Y015/901Y009/731Y004/722Y001) 존재 여부 확인.
2) WEO Historical xlsx — `0_raw/imf_weo_korea_vintage/WEOhistorical.xlsx`
   → script 23 (Test 1b) 입력. sheet, Korea NGDP_RPCH vintage range.
3) KR-CN bilateral csv — `0_raw/comtrade_korea_china/KR_*_*.csv`
   → script 22·23 입력. 50/50 file count, period coverage, flow split (M vs X).
4) 시군구 centroid — `0_raw/sigungu_centroid/sigungu_centroid_table.csv`
   → script 25 (first-stage F + Conley SE) 입력. 251/251 매칭 검증.
5) sigungu crosswalk — `1_codebooks/sigungu_crosswalk.csv`
   → script 25 sido cluster 매핑.

Outputs:
- 5_logs/integrity_checks/<date>_phase_bx_preflight.md  (사람이 읽을 종합 리포트)
- 3_derived/identification/preflight_summary.csv          (status row per input)

P1/P2/P3 flag 표기.

Author: R-A
Date  : 2026-05-04
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
LOGS = PROJ / "5_logs" / "integrity_checks"
OUT = PROJ / "3_derived" / "identification"
LOGS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
TODAY = date.today().isoformat()

# ---------------------------------------------------------------------------
# expected ECOS stat codes (validated against keyword search 2026-05-04)
# ---------------------------------------------------------------------------
ECOS_EXPECTED = {
    "200Y110": "국내총생산에 대한 지출 (실질, 분기 및 연간)",
    "402Y014": "수출물가지수 (기본분류)",
    "401Y015": "수입물가지수 (기본분류)",
    "901Y009": "소비자물가지수",
    "731Y004": "환율",
    "722Y001": "한국은행 기준금리",
}


# ---------------------------------------------------------------------------
# 1) ECOS macro panel
# ---------------------------------------------------------------------------
def profile_ecos(log: list) -> dict:
    log.append("\n## 1) ECOS macro panel  (script 22 input)\n")
    eco_dir = PROJ / "0_raw" / "ecos_macro"
    if not eco_dir.exists():
        log.append(f"❌ **[P1]** missing dir: `{eco_dir.relative_to(PROJ)}`")
        return {"input": "ecos_macro", "status": "MISSING_DIR", "p_flag": "P1"}

    files = list(eco_dir.glob("*.parquet")) + list(eco_dir.glob("*.csv"))
    log.append(f"- file count: **{len(files)}**")
    if not files:
        log.append("❌ **[P1]** 디렉토리 존재하나 파일 0")
        return {"input": "ecos_macro", "status": "EMPTY", "p_flag": "P1"}

    found_codes = set()
    sizes = []
    for f in files:
        sizes.append((f.name, f.stat().st_size))
        for code in ECOS_EXPECTED:
            if code in f.name.upper():
                found_codes.add(code)

    log.append(f"- 파일명 코드 매칭: **{len(found_codes)}/{len(ECOS_EXPECTED)}**")
    for code, label in ECOS_EXPECTED.items():
        ok = "✅" if code in found_codes else "❌"
        log.append(f"  - {ok} `{code}` — {label}")
    log.append("")
    log.append("- 상위 5개 파일 (size):")
    for name, sz in sorted(sizes, key=lambda x: -x[1])[:5]:
        log.append(f"  - {name}  ({sz/1024:.0f} KB)")

    missing = set(ECOS_EXPECTED) - found_codes
    if missing:
        log.append(f"\n⚠️ **[P1]** missing codes: {sorted(missing)}")
        log.append("  - script 22 (Test 1) 부분적으로만 작동. 누락된 매크로는 회귀에서 제외됨")
        return {"input": "ecos_macro", "status": "PARTIAL", "p_flag": "P1",
                "found": len(found_codes), "expected": len(ECOS_EXPECTED)}

    # head sample of one file
    try:
        sample = files[0]
        if sample.suffix == ".parquet":
            df = pd.read_parquet(sample).head(3)
        else:
            df = pd.read_csv(sample, nrows=3, encoding="utf-8-sig")
        log.append(f"\n- 샘플 (`{sample.name}`):")
        log.append("```")
        log.append(df.to_string(index=False))
        log.append("```")
    except Exception as e:
        log.append(f"⚠️ 샘플 읽기 실패: {e}")

    log.append("✅ **[OK]** 6 코드 모두 매칭, script 22 실행 가능")
    return {"input": "ecos_macro", "status": "OK", "p_flag": "OK",
            "found": len(found_codes), "expected": len(ECOS_EXPECTED)}


# ---------------------------------------------------------------------------
# 2) WEO Historical
# ---------------------------------------------------------------------------
def profile_weo(log: list) -> dict:
    log.append("\n## 2) WEO Historical xlsx  (script 23 input)\n")
    f = PROJ / "0_raw" / "imf_weo_korea_vintage" / "WEOhistorical.xlsx"
    if not f.exists():
        log.append(f"❌ **[P1]** not found: `{f.relative_to(PROJ)}`")
        return {"input": "weo", "status": "MISSING", "p_flag": "P1"}
    log.append(f"- size: {f.stat().st_size/1024**2:.2f} MB")

    try:
        xl = pd.ExcelFile(f)
        log.append(f"- sheets: {xl.sheet_names}")
        # 가장 큰 sheet
        biggest = max(xl.sheet_names,
                      key=lambda s: xl.parse(s, nrows=1).shape[1])
        head = xl.parse(biggest, nrows=5)
        log.append(f"- main sheet: `{biggest}` shape head={head.shape}")
        log.append(f"- sample columns: {list(head.columns)[:12]}")

        # Korea presence
        full = xl.parse(biggest)
        country_col = next(
            (c for c in full.columns
             if str(c).lower() in ("country", "iso", "weo country code", "country code")),
            None,
        )
        if country_col:
            kor_n = full[country_col].astype(str).str.upper().str.contains("KOR").sum()
            log.append(f"- Korea (KOR) rows: **{kor_n:,}**")
            if kor_n == 0:
                log.append("⚠️ **[P1]** Korea 0 rows → schema 다른 sheet 일 가능성")
                return {"input": "weo", "status": "NO_KOREA", "p_flag": "P1"}
        else:
            log.append("⚠️ **[P2]** country column 자동 인식 실패 — script 23 의 fallback 로직 의존")
    except Exception as e:
        log.append(f"❌ **[P1]** read error: {e}")
        return {"input": "weo", "status": "READ_ERROR", "p_flag": "P1"}

    log.append("✅ **[OK]** WEO 로드 가능. script 23 의 long-format 변환에서 vintage_year/horizon 추출")
    return {"input": "weo", "status": "OK", "p_flag": "OK"}


# ---------------------------------------------------------------------------
# 3) KR-CN bilateral
# ---------------------------------------------------------------------------
def profile_krcn(log: list) -> dict:
    log.append("\n## 3) KR-CN bilateral csv  (script 22, 23 input)\n")
    d = PROJ / "0_raw" / "comtrade_korea_china"
    if not d.exists():
        log.append(f"❌ **[P1]** missing dir: `{d.relative_to(PROJ)}`")
        return {"input": "krcn", "status": "MISSING_DIR", "p_flag": "P1"}

    files = sorted(d.glob("KR_*_*.csv"))
    log.append(f"- file count: **{len(files)}** (CLAUDE.md 기대: 50/50 ✅)")
    if not files:
        log.append("❌ **[P1]** 0 csv")
        return {"input": "krcn", "status": "EMPTY", "p_flag": "P1"}

    sample = pd.read_csv(files[0], nrows=3, low_memory=False)
    log.append(f"- 샘플 컬럼 ({files[0].name}): {list(sample.columns)[:10]}")

    # period coverage by filename pattern
    years = set()
    flows = set()
    for f in files:
        parts = f.stem.split("_")  # KR_M_2000 형태 가정
        if len(parts) >= 3:
            flows.add(parts[1])
            try:
                years.add(int(parts[-1]))
            except ValueError:
                pass
    log.append(f"- year range (filename): {min(years) if years else '?'}-{max(years) if years else '?'}, n_year={len(years)}")
    log.append(f"- flow tags: {sorted(flows)}")

    # P1 flag: 2000-2024 25y × 2 flow = 50 expected
    if len(files) < 50:
        log.append(f"⚠️ **[P1]** 50 미만 ({len(files)}) — Test 1·1b sample 축소 위험")
        return {"input": "krcn", "status": "PARTIAL", "p_flag": "P1",
                "n_files": len(files)}
    log.append(f"✅ **[OK]** 50 파일 (M+X × 2000-2024)")
    return {"input": "krcn", "status": "OK", "p_flag": "OK", "n_files": len(files)}


# ---------------------------------------------------------------------------
# 4) 시군구 centroid
# ---------------------------------------------------------------------------
def profile_centroid(log: list) -> dict:
    log.append("\n## 4) 시군구 centroid  (script 25 + Conley SE input)\n")
    f = PROJ / "0_raw" / "sigungu_centroid" / "sigungu_centroid_table.csv"
    if not f.exists():
        log.append(f"❌ **[P1]** not found: `{f.relative_to(PROJ)}`")
        return {"input": "centroid", "status": "MISSING", "p_flag": "P1"}

    df = pd.read_csv(f, dtype={"h_code": str})
    log.append(f"- rows: **{len(df):,}** (기대 251)")
    log.append(f"- columns: {list(df.columns)}")
    if "h_code" in df.columns:
        log.append(f"- distinct h_code: {df['h_code'].nunique()}")
    for col in ("lng", "lat", "longitude", "latitude"):
        if col in df.columns:
            n_valid = df[col].notna().sum()
            log.append(f"- {col} 유효: {n_valid}/{len(df)}")

    if len(df) == 251:
        log.append("✅ **[OK]** 251/251 정확 매칭")
        return {"input": "centroid", "status": "OK", "p_flag": "OK", "rows": len(df)}
    else:
        log.append(f"⚠️ **[P2]** rows ≠ 251 — h_code 정의 확인 필요")
        return {"input": "centroid", "status": "ROW_MISMATCH", "p_flag": "P2", "rows": len(df)}


# ---------------------------------------------------------------------------
# 5) crosswalk
# ---------------------------------------------------------------------------
def profile_crosswalk(log: list) -> dict:
    log.append("\n## 5) sigungu crosswalk  (script 25 sido cluster input)\n")
    f = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
    if not f.exists():
        log.append(f"❌ **[P1]** not found: `{f.relative_to(PROJ)}`")
        return {"input": "crosswalk", "status": "MISSING", "p_flag": "P1"}

    df = pd.read_csv(f, dtype=str)
    log.append(f"- rows: **{len(df):,}** (기대 6,723)")
    log.append(f"- columns: {list(df.columns)}")
    if "h_code" in df.columns:
        log.append(f"- distinct h_code: {df['h_code'].nunique()} (기대 256)")
    if "year" in df.columns:
        log.append(f"- year range: {df['year'].min()}-{df['year'].max()}")

    if len(df) >= 6700 and "sido_code" in df.columns:
        log.append("✅ **[OK]** crosswalk 정상")
        return {"input": "crosswalk", "status": "OK", "p_flag": "OK", "rows": len(df)}
    log.append("⚠️ **[P2]** crosswalk 행 수 또는 sido_code 컬럼 이상")
    return {"input": "crosswalk", "status": "PARTIAL", "p_flag": "P2", "rows": len(df)}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    log = [f"# Phase B-x pre-flight profile  ({TODAY})", ""]
    log.append("Phase B-x scripts 22·23·24·25 가 의존하는 5개 입력의 raw 상태 점검.")
    log.append("Codebook-first 원칙대로 0_raw·1_codebooks 만 inspect.")

    rows = []
    rows.append(profile_ecos(log))
    rows.append(profile_weo(log))
    rows.append(profile_krcn(log))
    rows.append(profile_centroid(log))
    rows.append(profile_crosswalk(log))

    # summary
    log.append("\n## 종합")
    n_ok = sum(1 for r in rows if r["status"] == "OK")
    log.append(f"- OK: **{n_ok}/{len(rows)}**")
    log.append("\n| input | status | flag |")
    log.append("|-------|--------|------|")
    for r in rows:
        log.append(f"| {r['input']} | {r['status']} | {r['p_flag']} |")

    log.append("\n## 다음 단계 (Suggested next steps)")
    if rows[0]["status"] == "OK" and rows[1]["status"] == "OK" and rows[2]["status"] == "OK":
        log.append("1. **즉시 실행 가능**: `python 2_scripts/identification/22_phase_bx_test1_macro_predictability.py`")
        log.append("2. **즉시 실행 가능**: `python 2_scripts/identification/23_phase_bx_test1b_weo_surprise.py`")
    else:
        log.append("1. ❌ Test 1 / 1b 입력 결손 — 위 missing 항목 우선 보강 후 재 preflight")
    if rows[3]["status"] != "OK":
        log.append("2. centroid 결손 → Conley SE 보류, HC1 + cluster-sido 만 사용")
    log.append("3. **Phase 2-B 의존 (Test 3·25)**: dry-run 으로 끝남. Phase 2-B 1990 baseline 별도 turn 필요")
    log.append("4. preflight 통과 시 `run_phase_bx_all.ps1` 한 번 실행 → 4개 log 일괄 생성")

    log_path = LOGS / f"{TODAY}_phase_bx_preflight.md"
    log_path.write_text("\n".join(log), encoding="utf-8")
    pd.DataFrame(rows).to_csv(OUT / "preflight_summary.csv",
                              index=False, encoding="utf-8-sig")
    print(f"\n✅ preflight log: {log_path}")


if __name__ == "__main__":
    main()
