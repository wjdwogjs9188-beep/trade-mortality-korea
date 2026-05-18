"""
Phase 1.1 — 시군구 centroid 좌표 수집.

소스: https://github.com/southkorea/southkorea-maps (KOSTAT 2018 행정경계)
방법: GeoJSON 다운로드 → shapely centroid 계산 → CSV 출력 (h_code × name × lat × lon)

산출:
 0_raw/sigungu_centroid/skorea_sigungu_2018_geo_simple.json
 0_raw/sigungu_centroid/sigungu_centroid_table.csv

검증: 229+ h_code 모두 valid lat/lon
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR, LOGS_DIR

import requests

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")
 sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = RAW_DIR / "sigungu_centroid"
LOG = LOGS_DIR / "data_collection" / f"{datetime.now:%Y-%m-%d}_phase1_centroid.md"

# 후보 URL (failover)
URLS = [
 "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea_municipalities_geo_simple.json",
 "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_municipalities_geo_simple.json",
]

GEOJSON_FILE = OUT_DIR / "skorea_sigungu_2018_geo_simple.json"
TABLE_FILE = OUT_DIR / "sigungu_centroid_table.csv"

def download -> bytes | None:
 for url in URLS:
 print(f" fetching {url}")
 try:
 r = requests.get(url, timeout=60)
 r.raise_for_status
 return r.content
 except requests.exceptions.RequestException as e:
 print(f" [fail] {e}")
 return None

def polygon_centroid(coords) -> tuple[float, float]:
 """단순 polygon centroid (외부 ring 만 사용, area-weighted)"""
 # GeoJSON polygon: coords = [[lng, lat], [lng, lat],...]
 # 다중 polygon (MultiPolygon) 시 첫 polygon 만 사용 — Korean 행정경계는 거의 단일 polygon
 if not coords:
 return float("nan"), float("nan")
 # MultiPolygon 의 경우: coords = [[ [[ring1]], [[ring2]] ],...]
 # Polygon 의 경우: coords = [ [[ring1]], [[ring2]] ]
 # ring1 만 사용
 if isinstance(coords[0][0][0], (int, float)):
 # Polygon
 ring = coords[0]
 else:
 # MultiPolygon — 가장 큰 polygon 사용
 biggest = max(coords, key=lambda p: len(p[0]))
 ring = biggest[0]

 # Shoelace centroid
 n = len(ring)
 area2 = 0.0
 cx = 0.0
 cy = 0.0
 for i in range(n - 1):
 x0, y0 = ring[i]
 x1, y1 = ring[i + 1]
 cross = x0 * y1 - x1 * y0
 area2 += cross
 cx += (x0 + x1) * cross
 cy += (y0 + y1) * cross
 if area2 == 0:
 # Degenerate: arithmetic mean
 xs = [p[0] for p in ring]
 ys = [p[1] for p in ring]
 return sum(xs) / len(xs), sum(ys) / len(ys)
 cx /= 3 * area2
 cy /= 3 * area2
 return cx, cy # (lng, lat)

def main -> int:
 OUT_DIR.mkdir(parents=True, exist_ok=True)
 LOG.parent.mkdir(parents=True, exist_ok=True)

 if GEOJSON_FILE.exists:
 print(f"[skip] {GEOJSON_FILE} already exists")
 with GEOJSON_FILE.open("rb") as f:
 content = f.read
 else:
 content = download
 if content is None:
 err = "[ERROR] GeoJSON download fail. URLs:\n" + "\n".join(f" - {u}" for u in URLS)
 print(err)
 LOG.write_text(f"# Phase 1.1 — 시군구 centroid ❌\n\n{err}\n", encoding="utf-8")
 return 1
 GEOJSON_FILE.write_bytes(content)
 print(f"[OK] downloaded {len(content):,} bytes -> {GEOJSON_FILE}")

 geo = json.loads(content)
 features = geo.get("features",)
 print(f"[parse] {len(features):,} features")

 # CSV: h_code, name, lng, lat
 rows = 
 for f in features:
 props = f.get("properties", {})
 # KOSTAT 2018 의 properties 키 후보: code, SIG_CD, name, NAME_2 등
 h_code = (
 props.get("code")
 or props.get("SIG_CD")
 or props.get("ADM_CD")
 or props.get("CTPRVN_CD")
 or ""
)
 name = (
 props.get("name")
 or props.get("SIG_KOR_NM")
 or props.get("NAME_2")
 or props.get("SIG_ENG_NM")
 or ""
)
 geom = f.get("geometry", {})
 coords = geom.get("coordinates",)
 lng, lat = polygon_centroid(coords)
 rows.append({"h_code": str(h_code), "name": name, "lng": lng, "lat": lat,
 "geom_type": geom.get("type", "")})

 import csv
 with TABLE_FILE.open("w", encoding="utf-8-sig", newline="") as f:
 writer = csv.DictWriter(f, fieldnames=["h_code", "name", "lng", "lat", "geom_type"])
 writer.writeheader
 writer.writerows(rows)

 n_total = len(rows)
 n_with_code = sum(1 for r in rows if r["h_code"])
 n_with_xy = sum(1 for r in rows if r["lng"] == r["lng"] and r["lat"] == r["lat"]) # NaN check

 msg = (
 f"# Phase 1.1 — 시군구 centroid ✅\n\n"
 f"- GeoJSON: `{GEOJSON_FILE}` ({len(content):,} bytes)\n"
 f"- 출력 CSV: `{TABLE_FILE}` ({n_total} rows)\n"
 f"- h_code 보유: {n_with_code}/{n_total}\n"
 f"- 유효 lng/lat: {n_with_xy}/{n_total}\n"
 f"- timestamp: {datetime.now.isoformat}\n"
)
 print(f"\n{msg}")
 LOG.write_text(msg, encoding="utf-8")
 return 0

if __name__ == "__main__":
 sys.exit(main)
