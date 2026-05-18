"""ECOS 거시·지역 컨트롤 변수 일괄 수집 (옵션 1: 광범위).

수집 대상:
 A. 지역 거시 (시도 레벨, 본 연구 cluster·controls)
 - 200Y003: 지역내총생산(GRDP), 시도, 연
 - 132Y001: 산업별 대출금 (예금은행, 지역별, 전산업), 분기
 - 132Y003: 산업별 대출금 (예금은행, 지역별, 용도별), 분기
 - 301Y015: 지역별 경상수지, 연

 B. 전국 거시 (시계열, macro shock controls)
 - 722Y001: 한국은행 기준금리, 월
 - 731Y001: 주요국 통화별 환율 (USD, CNY 등), 월
 - 036Y002: 통화량 (M1, M2, Lf), 월
 - 901Y009: 소비자물가지수 (CPI), 월

 C. 무역 (전국, Comtrade 보완)
 - 403Y001: 국가별 수출, 월
 - 403Y002: 국가별 수입, 월

본 연구 사용:
 - GRDP·산업별대출 → 시도 fixed effects 또는 컨트롤
 - 환율·금리·CPI → 거시 충격 통제
 - 국가별 수출입 → 한국 무역 IV 보강

저장 위치: 0_raw/ecos_macro/
"""
import sys
import time
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR
from lib.ecos_api import search_statistic, list_items, search_table_by_keyword

OUT_DIR = RAW_DIR / "ecos_macro"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ───────────────────────── 통계표 정의 (수정 완료 2026-05-01) ─────────────────────────
# (stat_code, cycle, start, end, name)
#
# 주의:
# - GRDP는 ECOS에 없음 (KOSIS에서 별도 다운)
# - 132Y001/132Y003 시작 = 2008 Q1
# - 731Y004 = 월별 환율 (731Y001 은 일별)
# - 161Y006 = M2 평잔 원계열, 161Y001 = M1 평잔 계절조정
TABLES_A_REGIONAL = [
 # 132Y001/003: cycle Q 는 API에 0행, cycle A 만 사용 가능 (확인 2026-05-01)
 ("132Y001", "A", "2008", "2024", "산업별대출금_예금은행_지역별_전산업"),
 ("132Y003", "A", "2008", "2024", "산업별대출금_예금은행_지역별_용도별"),
 ("301Y015", "A", "2000", "2024", "지역별_경상수지"),
]

TABLES_B_NATIONAL = [
 ("722Y001", "M", "200001", "202412", "한국은행_기준금리"),
 ("731Y004", "M", "200001", "202412", "환율_주요국통화별_월"),
 ("161Y001", "M", "200001", "202412", "M1_협의통화_평잔_계절조정"),
 ("161Y006", "M", "200001", "202412", "M2_광의통화_평잔_원계열"),
 ("102Y002", "M", "200001", "202412", "본원통화_평잔_원계열"),
 ("901Y009", "M", "200001", "202412", "CPI_소비자물가지수"),
]

TABLES_C_TRADE = [
 ("403Y001", "M", "200001", "202412", "국가별_수출"),
 ("403Y002", "M", "200001", "202412", "국가별_수입"),
]

ALL_TABLES = TABLES_A_REGIONAL + TABLES_B_NATIONAL + TABLES_C_TRADE

def safe_filename(s: str) -> str:
 """Windows-safe filename. 한글은 그대로, 특수문자만 변환."""
 return s.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")

def download_one(stat_code: str, cycle: str, start: str, end: str, name: str) -> dict:
 """단일 통계표 다운 → CSV 저장. 결과 메타 dict 반환."""
 fn = f"{stat_code}_{cycle}_{start}_{end}_{safe_filename(name)}.csv"
 out = OUT_DIR / fn
 print(f"\n--- {stat_code} ({name}) [{cycle}] {start}-{end} ---")
 if out.exists:
 n_existing = sum(1 for _ in open(out, "r", encoding="utf-8-sig", errors="replace")) - 1
 if n_existing > 0:
 print(f" ⏭ 이미 존재 ({n_existing} 행) — skip")
 return {"stat_code": stat_code, "name": name, "rows": n_existing,
 "status": "exists", "file": str(out.name)}

 try:
 df = search_statistic(stat_code, cycle, start, end)
 if df.empty:
 print(f" ⚠️ 0 행 — 통계표 ID·기간·cycle 확인 필요")
 return {"stat_code": stat_code, "name": name, "rows": 0,
 "status": "empty", "file": ""}
 df.to_csv(out, index=False, encoding="utf-8-sig")
 print(f" ✅ {len(df):,} 행 → {out.name}")
 return {"stat_code": stat_code, "name": name, "rows": len(df),
 "status": "ok", "file": str(out.name)}
 except Exception as e:
 print(f" ❌ 실패: {e}")
 return {"stat_code": stat_code, "name": name, "rows": 0,
 "status": f"error: {str(e)[:100]}", "file": ""}

def main:
 print("=" * 70)
 print("ECOS 거시·지역 컨트롤 변수 일괄 수집")
 print("=" * 70)
 print(f"\n총 통계표 수: {len(ALL_TABLES)} 개")
 print(f" A. 지역 거시: {len(TABLES_A_REGIONAL)} 개")
 print(f" B. 전국 거시: {len(TABLES_B_NATIONAL)} 개")
 print(f" C. 무역: {len(TABLES_C_TRADE)} 개")
 print(f"\n저장 위치: {OUT_DIR}")
 print(f"ECOS 일일 한도: 10,000 호출 (충분)\n")

 answer = input("진행하시겠습니까? (yes / no): ").strip.lower
 if answer not in ("yes", "y"):
 print("중단.")
 return

 t0 = time.time
 results = 

 for group_name, group_tables in [
 ("A. 지역 거시", TABLES_A_REGIONAL),
 ("B. 전국 거시", TABLES_B_NATIONAL),
 ("C. 무역", TABLES_C_TRADE),
 ]:
 print(f"\n{'=' * 50}")
 print(f" {group_name}")
 print(f"{'=' * 50}")
 for tbl in group_tables:
 results.append(download_one(*tbl))
 time.sleep(0.3)

 # 결과 요약 + manifest 저장
 df_results = pd.DataFrame(results)
 manifest = OUT_DIR / "_manifest.csv"
 df_results.to_csv(manifest, index=False, encoding="utf-8-sig")

 elapsed = time.time - t0
 print(f"\n{'=' * 70}")
 print(f" 완료 — 총 {elapsed/60:.1f} 분")
 print(f"{'=' * 70}")
 print(f"\n결과 요약:")
 print(df_results[["stat_code", "name", "rows", "status"]].to_string(index=False))

 ok = (df_results["status"] == "ok").sum
 fail = (df_results["status"].str.startswith("error")).sum
 empty = (df_results["status"] == "empty").sum
 skip = (df_results["status"] == "exists").sum
 print(f"\n✅ ok: {ok}, ⏭ skip: {skip}, ⚠️ empty: {empty}, ❌ error: {fail}")
 print(f"\nManifest: {manifest}")

 if empty > 0 or fail > 0:
 print(f"\n⚠️ empty/error 통계표는 ID나 cycle이 잘못됐을 수 있어.")
 print(f" 다음으로 확인: python -c \"from lib.ecos_api import search_table_by_keyword; print(search_table_by_keyword('환율'))\"")

if __name__ == "__main__":
 main
