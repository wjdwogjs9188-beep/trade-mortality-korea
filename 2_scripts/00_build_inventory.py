"""0_raw/ 모든 파일의 INVENTORY.csv 생성.

각 파일에 대해 기록:
 path, size, md5, encoding, ext, rows, cols (csv/xlsx 만), first_3_lines

목적:
 1. 어떤 raw가 있는지 한 표에서 확인
 2. md5 → 변경 감지 (raw가 수정되면 자동으로 알아챔)
 3. 인코딩 자동 감지 (cp949 vs utf-8-sig 등)
"""
import sys
import hashlib
from pathlib import Path
import csv

sys.path.insert(0, str(Path(__file__).resolve.parents[0]))
from lib.config import RAW_DIR, DERIVED_DIR

def md5(p: Path, max_bytes: int = 50 * 1024 * 1024) -> str:
 """파일 md5. 50MB 이상은 첫 50MB만 (속도)."""
 h = hashlib.md5
 n = 0
 with open(p, "rb") as f:
 while True:
 chunk = f.read(1024 * 1024)
 if not chunk: break
 h.update(chunk)
 n += len(chunk)
 if n >= max_bytes: break
 return h.hexdigest + (f":first{max_bytes}" if n >= max_bytes else "")

def detect_encoding(p: Path) -> str:
 """csv/txt 파일 인코딩 감지."""
 try:
 import chardet
 with open(p, "rb") as f:
 raw = f.read(20000)
 det = chardet.detect(raw)
 return f"{det['encoding']}({det['confidence']:.0%})"
 except Exception as e:
 return f"err: {e}"

def csv_shape(p: Path, encoding: str) -> tuple[int, int]:
 """csv 행수 + 컬럼수 (빠르게)."""
 enc = encoding.split("(")[0]
 try:
 with open(p, "r", encoding=enc, errors="replace") as f:
 reader = csv.reader(f)
 try:
 header = next(reader)
 except StopIteration:
 return 0, 0
 n_cols = len(header)
 n_rows = sum(1 for _ in reader) + 1
 return n_rows, n_cols
 except Exception:
 return -1, -1

def first_3_lines(p: Path, encoding: str) -> str:
 """첫 3줄 (긴 줄은 200자로 자름)."""
 enc = encoding.split("(")[0]
 try:
 lines = 
 with open(p, "r", encoding=enc, errors="replace") as f:
 for _ in range(3):
 line = f.readline.rstrip[:200]
 lines.append(line)
 return " | ".join(lines)
 except Exception:
 return ""

def walk(root: Path, follow_symlinks: bool = True):
 """root 아래 모든 파일 (symlink follow)."""
 for entry in root.iterdir:
 if entry.is_dir:
 yield from walk(entry, follow_symlinks)
 elif entry.is_file:
 yield entry

def main:
 rows = 
 print(f"Walking {RAW_DIR}...")
 for p in walk(RAW_DIR):
 rel = str(p.relative_to(RAW_DIR))
 try:
 size = p.stat.st_size
 except OSError:
 size = -1

 ext = p.suffix.lower
 record = {
 "path": rel,
 "size_bytes": size,
 "size_human": f"{size/1024/1024:.1f}M" if size > 1e6 else f"{size/1024:.0f}K" if size > 1024 else f"{size}B",
 "ext": ext,
 "md5": "",
 "encoding": "",
 "rows": "",
 "cols": "",
 "first_3_lines": "",
 }

 # md5 (symlink follow OK)
 if size > 0 and size < 200 * 1024 * 1024:
 try:
 record["md5"] = md5(p)
 except OSError as e:
 record["md5"] = f"err: {e}"

 # CSV/TXT 만 인코딩 + 행/열 감지
 if ext in {".csv", ".txt"}:
 enc = detect_encoding(p)
 record["encoding"] = enc
 if size < 100 * 1024 * 1024: # 100MB 미만만 행 카운트
 r, c = csv_shape(p, enc)
 record["rows"] = r
 record["cols"] = c
 record["first_3_lines"] = first_3_lines(p, enc)
 # XLSX 는 행/열만 (여기선 생략, 추후 별도)

 rows.append(record)
 if len(rows) % 50 == 0:
 print(f" {len(rows)} files...")

 # csv 저장
 DERIVED_DIR.mkdir(parents=True, exist_ok=True)
 out = DERIVED_DIR / "raw_inventory.csv"
 with open(out, "w", encoding="utf-8-sig", newline="") as f:
 writer = csv.DictWriter(f, fieldnames=list(rows[0].keys))
 writer.writeheader
 writer.writerows(rows)

 print(f"\n✅ {len(rows):,} 파일 inventory 저장: {out}")
 # summary
 by_ext = {}
 for r in rows:
 by_ext[r["ext"]] = by_ext.get(r["ext"], 0) + 1
 print("\n확장자별:")
 for ext, n in sorted(by_ext.items, key=lambda x: -x[1])[:10]:
 print(f" {ext or '(no ext)':10s} {n:>5}")

if __name__ == "__main__":
 main
