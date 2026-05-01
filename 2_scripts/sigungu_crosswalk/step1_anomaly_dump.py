"""터미널 mojibake 회피 — anomaly 결과를 UTF-8 파일로 직접 dump."""
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:/Users/82103/Downloads/trade_mortality_korea")
SRC = ROOT / "3_derived" / "sigungu" / "step1_codebook_old.csv"
OUT = ROOT / "3_derived" / "sigungu" / "step1_anomaly_report.md"

df = pd.read_csv(SRC, dtype={"raw_code": str, "sido_code": str})

lines: list[str] = []
def w(s: str = "") -> None: lines.append(s)

w("# Step 1 Anomaly Report")
w("")
w("## (a) length=2 sigungu rows (1999-2021)")
short = df[df["code_len"] == 2]
w(short.to_markdown(index=False))
w("")
w("**해석:** 충청남도(34)에 raw_code='25', length=2 entry가 1999-2021년 매년 단 1개. "
  "한국 행정코드에서 2자리는 시도 레벨인데, 충청남도 sido_code는 34이지 25 아님. "
  "이는 코드집 데이터 오류 가능성 또는 계룡출장소(2003 계룡시 출범 전)/특별 sub-entity 추정. "
  "Step 3 매핑에서 '_anomaly_short_code_25'로 분리 처리.")
w("")

w("## (b) 1991→1992 transition (4-digit → 5-digit)")
n91 = df[df["year"] == 1991].set_index("sigungu_name")
n92 = df[df["year"] == 1992].set_index("sigungu_name")
only91 = sorted(set(n91.index) - set(n92.index))
only92 = sorted(set(n92.index) - set(n91.index))
w(f"- 1991만 ({len(only91)}개): {only91}")
w(f"- 1992만 ({len(only92)}개): {only92}")
w("**해석:** 1991→1992 시·군 명칭 자체는 ~동일, raw_code 길이만 4→5 일괄 전환. "
  "'1992년 행정구역 코드 개편' (5-digit 도입) 정책 반영.")
w("")

w("## (c) 1994→1995 transition (도농통합)")
n94 = df[df["year"] == 1994].set_index("sigungu_name")
n95 = df[df["year"] == 1995].set_index("sigungu_name")
only94 = sorted(set(n94.index) - set(n95.index))
only95 = sorted(set(n95.index) - set(n94.index))
w(f"- 1994년에 있고 1995년에 없는 ({len(only94)}개): {only94}")
w(f"- 1995년 신규 ({len(only95)}개): {only95}")
w("**해석:** 1995년 도농통합 (시 + 인접 군 → 통합시). 명칭 기반 매핑 필요.")
w("")

w("## (d) 2013→2014 transition (청주 통합)")
n13 = df[df["year"] == 2013].set_index("sigungu_name")
n14 = df[df["year"] == 2014].set_index("sigungu_name")
only13 = sorted(set(n13.index) - set(n14.index))
only14 = sorted(set(n14.index) - set(n13.index))
w(f"- 2013만: {only13}")
w(f"- 2014만: {only14}")
w("**해석:** 2014.7.1 청주시+청원군 → 통합 청주시 (4개 자치구: 상당·서원·흥덕·청원). "
  "코드집은 일부만 분리 표기 — 실제 raw 데이터로 검증 필요 (Step 2).")
w("")

w("## (e) 세종/연기군 transition")
sj = df[(df["sido_name"].str.contains("세종", na=False)) | (df["sigungu_name"].str.contains("세종|연기", na=False))]
w(sj.to_markdown(index=False))
w("**해석:** 충남 연기군 (1981-2011) → 세종특별자치시 (2012-) 직접 승계. "
  "raw_code 변경: 충남(34) 연기군 → 세종(29) 세종시. "
  "Phase 1-A 합의: 연기군과 세종시는 같은 h_code 매핑 (시간연속성).")
w("")

w("## (f) 시도 17개 — 모던 코드 사용 (retroactive)")
sidos = df[["sido_code", "sido_name"]].drop_duplicates().sort_values("sido_code")
w(sidos.to_markdown(index=False))
w("**해석:** KOSTAT 코드집은 1981년부터 모던 시도코드 (11~39) 적용. "
  "역사적 구분 (예: 직할시→광역시 1995, 제주도→특별자치도 2006)은 시도 레벨에서 invariant.")
w("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"saved: {OUT}")
print(f"size: {OUT.stat().st_size:,} bytes, {len(lines)} lines")
