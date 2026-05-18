"""문서 변환기 GUI — PDF/DOCX/XLSX/XLS/MD 상호 변환.

지원 모드:
 1. PDF → DOCX (pdf2docx)
 2. DOCX → MD (mammoth)
 3. PDF → MD (chained: pdf2docx → mammoth)
 4. XLSX → MD (pandas + openpyxl, 모든 시트를 markdown 표로)
 5. XLS → MD (pandas + xlrd<2.0 또는 사용자가.xlsx로 변환 권장)

기능:
 - 단일/다수/폴더 파일 선택
 - 출력 폴더 지정 (선택)
 - 페이지 범위 (PDF 모드 한정)
 - 덮어쓰기 옵션
 - 진행률 / 실시간 로그

실행:
 python 2_scripts/utils/pdf_to_docx_gui.py
 또는 PDF_to_DOCX.bat 더블클릭

라이브러리:
 - tkinter (Python 표준)
 - pdf2docx (pip install pdf2docx==0.5.8)
 - mammoth (pip install mammoth==1.8.0)
 - pandas (이미 requirements.txt 포함)
 - openpyxl (이미 포함,.xlsx 용)
 - xlrd (이미 포함;.xls 는 xlrd<2.0 필요)
"""
import sys
import tempfile
import threading
from pathlib import Path

try:
 import tkinter as tk
 from tkinter import filedialog, ttk, messagebox, scrolledtext
except ImportError:
 print("tkinter 미설치 — Anaconda는 기본 포함이라 거의 발생 안 함")
 sys.exit(1)

# ───────────────────────── 모드 정의 ─────────────────────────
MODES = {
 "pdf2docx": {"in_ext": ".pdf", "out_ext": ".docx", "label": "PDF → DOCX",
 "lib": "pdf2docx", "page_range": True},
 "docx2md": {"in_ext": ".docx", "out_ext": ".md", "label": "DOCX → MD",
 "lib": "mammoth", "page_range": False},
 "pdf2md": {"in_ext": ".pdf", "out_ext": ".md", "label": "PDF → MD",
 "lib": "both", "page_range": True},
 "xlsx2md": {"in_ext": ".xlsx", "out_ext": ".md", "label": "XLSX → MD",
 "lib": "pandas", "page_range": False},
 "xls2md": {"in_ext": ".xls", "out_ext": ".md", "label": "XLS → MD",
 "lib": "pandas", "page_range": False},
}

# XLSX→MD 옵션
XLSX_MAX_ROWS_PER_SHEET = 5000 # 너무 큰 시트는 잘림 (변경 가능)

def check_lib(name: str) -> bool:
 try:
 __import__(name)
 return True
 except ImportError:
 return False

# ───────────────────────── 변환 함수 ─────────────────────────
def convert_pdf_to_docx(pdf: Path, out: Path, start: int = 0, end: int | None = None):
 from pdf2docx import Converter
 out.parent.mkdir(parents=True, exist_ok=True)
 cv = Converter(str(pdf))
 try:
 kwargs = {}
 if start: kwargs["start"] = start
 if end is not None: kwargs["end"] = end
 cv.convert(str(out), **kwargs)
 finally:
 cv.close

def convert_docx_to_md(docx: Path, out: Path):
 """mammoth 로 DOCX → Markdown."""
 import mammoth
 out.parent.mkdir(parents=True, exist_ok=True)
 with open(docx, "rb") as f:
 result = mammoth.convert_to_markdown(f)
 out.write_text(result.value, encoding="utf-8")
 return result.messages # 변환 경고 (헤딩 매핑 등)

def convert_pdf_to_md(pdf: Path, out: Path, start: int = 0, end: int | None = None):
 """PDF → 임시 DOCX → MD."""
 with tempfile.TemporaryDirectory as td:
 tmp_docx = Path(td) / (pdf.stem + ".docx")
 convert_pdf_to_docx(pdf, tmp_docx, start, end)
 return convert_docx_to_md(tmp_docx, out)

def _df_to_md_table(df) -> str:
 """pandas DataFrame → markdown 표 (tabulate 의존성 없음).

 셀 안의 |, 줄바꿈은 escape.
 """
 if df.empty:
 return "_(빈 시트)_\n"
 headers = [str(c) for c in df.columns]
 sep = ["---"] * len(headers)
 lines = [
 "| " + " | ".join(headers) + " |",
 "| " + " | ".join(sep) + " |",
 ]
 for _, row in df.iterrows:
 cells = 
 for v in row:
 if v is None:
 s = ""
 else:
 s = str(v).replace("|", "\\|").replace("\n", "<br>").replace("\r", "")
 cells.append(s)
 lines.append("| " + " | ".join(cells) + " |")
 return "\n".join(lines) + "\n"

def convert_xlsx_to_md(xlsx: Path, out: Path, max_rows: int = XLSX_MAX_ROWS_PER_SHEET):
 """xlsx/xls 모든 시트를 markdown 표로. 시트별 ## 헤딩 분리.

.xls 의 경우 pandas 가 적절한 엔진 자동 선택 (xlrd 1.2.0 필요).
 """
 import pandas as pd
 out.parent.mkdir(parents=True, exist_ok=True)

 # 모든 시트 읽기 (셀 값은 string으로 — 숫자 포맷 손실 방지)
 sheets = pd.read_excel(xlsx, sheet_name=None, dtype=object)

 parts = 
 parts.append(f"# {xlsx.name}\n")
 parts.append(f"_원본 엑셀 시트 수: {len(sheets)}_\n")
 parts.append("")

 for sheet_name, df in sheets.items:
 parts.append(f"\n## Sheet: {sheet_name}\n")
 nrow, ncol = df.shape
 parts.append(f"_(rows: {nrow}, cols: {ncol})_\n")

 # 빈 셀 정리
 df = df.where(df.notna, "")

 # 너무 큰 시트 자르기 + 표시
 if nrow > max_rows:
 parts.append(f"\n⚠️ {nrow}행 중 처음 {max_rows}행만 표시 (`max_rows={max_rows}` 설정)\n")
 df = df.head(max_rows)

 parts.append("")
 parts.append(_df_to_md_table(df))

 out.write_text("\n".join(parts), encoding="utf-8")
 return # warning messages slot (interface 호환)

def convert_xls_to_md(xls: Path, out: Path, max_rows: int = XLSX_MAX_ROWS_PER_SHEET):
 """알리아스 — pandas read_excel 이.xls 도 처리."""
 return convert_xlsx_to_md(xls, out, max_rows)

# ───────────────────────── GUI ─────────────────────────
class DocConverterApp:
 def __init__(self, root: tk.Tk):
 self.root = root
 self.root.title("문서 변환기 (PDF / DOCX / XLSX / XLS / MD)")
 self.root.geometry("820x720")
 self.root.minsize(680, 600)

 self.files: list[Path] = 
 self.out_dir: Path | None = None
 self.is_running = False
 self.mode_var = tk.StringVar(value="pdf2docx")

 self._build_ui
 self._on_mode_change # 초기 상태 반영

 def _build_ui(self):
 pad = {"padx": 10, "pady": 6}

 # ───── 모드 선택 ─────
 frame_mode = ttk.LabelFrame(self.root, text="1. 변환 모드", padding=10)
 frame_mode.pack(fill="x", **pad)

 # 5개 모드 → 한 줄에 다 안 들어가서 grid 로 배치
 for i, (key, m) in enumerate(MODES.items):
 r, c = divmod(i, 3)
 ttk.Radiobutton(frame_mode, text=m["label"],
 variable=self.mode_var, value=key,
 command=self._on_mode_change).grid(
 row=r, column=c, sticky="w", padx=10, pady=2)

 # ───── 입력 파일 ─────
 frame_in = ttk.LabelFrame(self.root, text="2. 입력 파일 선택", padding=10)
 frame_in.pack(fill="x", **pad)

 btn_row = ttk.Frame(frame_in)
 btn_row.pack(fill="x")

 self.btn_files = ttk.Button(btn_row, text="📄 파일 선택",
 command=self.pick_files)
 self.btn_files.pack(side="left", padx=(0, 6))

 ttk.Button(btn_row, text="📁 폴더 선택 (안의 모든 파일)",
 command=self.pick_folder).pack(side="left", padx=(0, 6))
 ttk.Button(btn_row, text="🗑 초기화",
 command=self.clear_files).pack(side="left")

 self.files_listbox = tk.Listbox(frame_in, height=8)
 self.files_listbox.pack(fill="both", expand=True, pady=(8, 0))

 # ───── 출력 폴더 ─────
 frame_out = ttk.LabelFrame(self.root, text="3. 출력 폴더 (선택)", padding=10)
 frame_out.pack(fill="x", **pad)

 out_row = ttk.Frame(frame_out)
 out_row.pack(fill="x")

 self.out_var = tk.StringVar(value="(입력 파일과 같은 위치)")
 ttk.Label(out_row, textvariable=self.out_var, foreground="#444",
 width=70, anchor="w").pack(side="left", fill="x", expand=True)
 ttk.Button(out_row, text="📁 폴더 선택",
 command=self.pick_out_dir).pack(side="left", padx=(6, 0))
 ttk.Button(out_row, text="↺",
 command=self.reset_out_dir, width=3).pack(side="left", padx=(4, 0))

 # ───── 옵션 ─────
 frame_opt = ttk.LabelFrame(self.root, text="4. 옵션", padding=10)
 frame_opt.pack(fill="x", **pad)

 opt_row = ttk.Frame(frame_opt)
 opt_row.pack(fill="x")

 self.start_lbl = ttk.Label(opt_row, text="시작 페이지 (0부터):")
 self.start_lbl.grid(row=0, column=0, sticky="w")
 self.start_var = tk.StringVar
 self.start_entry = ttk.Entry(opt_row, textvariable=self.start_var, width=10)
 self.start_entry.grid(row=0, column=1, padx=6)

 self.end_lbl = ttk.Label(opt_row, text="끝 페이지 (exclusive):")
 self.end_lbl.grid(row=0, column=2, sticky="w", padx=(20, 0))
 self.end_var = tk.StringVar
 self.end_entry = ttk.Entry(opt_row, textvariable=self.end_var, width=10)
 self.end_entry.grid(row=0, column=3, padx=6)

 self.overwrite_var = tk.BooleanVar(value=False)
 ttk.Checkbutton(opt_row, text="기존 출력 파일 덮어쓰기",
 variable=self.overwrite_var).grid(row=1, column=0, columnspan=2,
 sticky="w", pady=(8, 0))

 self.page_hint = ttk.Label(frame_opt,
 text="(페이지 비우면 전체 변환. PDF 입력 모드에서만 적용.)",
 foreground="#666", font=("", 9))
 self.page_hint.pack(anchor="w", pady=(6, 0))

 # ───── 변환 버튼 ─────
 frame_run = ttk.Frame(self.root)
 frame_run.pack(fill="x", **pad)

 self.run_btn = ttk.Button(frame_run, text="▶ 변환 시작",
 command=self.start_convert)
 self.run_btn.pack(side="left")

 self.progress = ttk.Progressbar(frame_run, mode="determinate")
 self.progress.pack(side="left", fill="x", expand=True, padx=(10, 0))

 # ───── 로그 ─────
 frame_log = ttk.LabelFrame(self.root, text="진행 상황", padding=10)
 frame_log.pack(fill="both", expand=True, **pad)

 self.log = scrolledtext.ScrolledText(frame_log, height=10, wrap="word")
 self.log.pack(fill="both", expand=True)

 self.log_msg("문서 변환기 준비 완료.")
 self._check_libs

 def _check_libs(self):
 missing = 
 if not check_lib("pdf2docx"):
 missing.append("pdf2docx (PDF→DOCX 모드용)")
 if not check_lib("mammoth"):
 missing.append("mammoth (DOCX→MD 모드용)")
 if not check_lib("pandas"):
 missing.append("pandas (XLSX/XLS→MD 모드용)")
 if not check_lib("openpyxl"):
 missing.append("openpyxl (XLSX→MD 모드용)")
 if missing:
 self.log_msg("⚠️ 설치 필요:")
 for m in missing:
 self.log_msg(f" {m}")
 self.log_msg(" 한꺼번에: pip install pdf2docx==0.5.8 mammoth==1.8.0 pandas openpyxl xlrd")

 # ───── 모드 변경시 옵션 활성화 토글 ─────
 def _on_mode_change(self):
 mode = self.mode_var.get
 m = MODES[mode]
 # 페이지 옵션은 PDF 입력일 때만
 state = "normal" if m["page_range"] else "disabled"
 self.start_entry.config(state=state)
 self.end_entry.config(state=state)

 # 버튼 라벨 업데이트
 self.btn_files.config(text=f"📄 {m['in_ext'].upper} 파일 선택")

 # 파일 목록 검증 (모드에 안 맞는 건 제거)
 valid_ext = m["in_ext"]
 before = len(self.files)
 self.files = [p for p in self.files if p.suffix.lower == valid_ext]
 if before!= len(self.files):
 self.log_msg(f" 모드 변경으로 {before - len(self.files)}개 파일 제거 (확장자 불일치)")
 self._refresh_files

 # ───── 파일 선택 ─────
 def _current_ext(self) -> str:
 return MODES[self.mode_var.get]["in_ext"]

 def pick_files(self):
 ext = self._current_ext
 ftypes = [(f"{ext.upper} 파일", f"*{ext}"), ("모든 파일", "*.*")]
 paths = filedialog.askopenfilenames(
 title=f"변환할 {ext.upper} 파일 선택", filetypes=ftypes,
)
 if not paths: return
 for p in paths:
 self.files.append(Path(p))
 self._refresh_files

 def pick_folder(self):
 ext = self._current_ext
 d = filedialog.askdirectory(title=f"{ext.upper} 들어있는 폴더 선택")
 if not d: return
 files = sorted(Path(d).glob(f"*{ext}"))
 if not files:
 messagebox.showinfo("결과", f"{d}\n안에 {ext.upper} 없음")
 return
 for p in files:
 self.files.append(p)
 self._refresh_files

 def clear_files(self):
 self.files.clear
 self._refresh_files

 def _refresh_files(self):
 self.files_listbox.delete(0, "end")
 seen = set
 unique = 
 for p in self.files:
 ap = str(p.resolve)
 if ap not in seen:
 seen.add(ap)
 unique.append(p)
 self.files = unique
 for p in self.files:
 self.files_listbox.insert("end", str(p))
 self.log_msg(f"선택된 파일: {len(self.files)} 개")

 # ───── 출력 폴더 ─────
 def pick_out_dir(self):
 d = filedialog.askdirectory(title="출력 저장할 폴더 선택")
 if not d: return
 self.out_dir = Path(d)
 self.out_var.set(str(self.out_dir))

 def reset_out_dir(self):
 self.out_dir = None
 self.out_var.set("(입력 파일과 같은 위치)")

 # ───── 변환 ─────
 def start_convert(self):
 if self.is_running:
 messagebox.showwarning("진행 중", "변환이 이미 진행 중입니다.")
 return
 if not self.files:
 messagebox.showwarning("입력 없음", "변환할 파일을 선택하세요.")
 return

 mode = self.mode_var.get
 m = MODES[mode]

 # 라이브러리 체크
 if mode == "pdf2docx" and not check_lib("pdf2docx"):
 messagebox.showerror("라이브러리 없음", "pdf2docx 미설치.\npip install pdf2docx==0.5.8")
 return
 if mode == "docx2md" and not check_lib("mammoth"):
 messagebox.showerror("라이브러리 없음", "mammoth 미설치.\npip install mammoth==1.8.0")
 return
 if mode == "pdf2md" and (not check_lib("pdf2docx") or not check_lib("mammoth")):
 messagebox.showerror("라이브러리 없음",
 "PDF→MD는 둘 다 필요.\npip install pdf2docx==0.5.8 mammoth==1.8.0")
 return
 if mode in ("xlsx2md", "xls2md") and not check_lib("pandas"):
 messagebox.showerror("라이브러리 없음",
 "pandas 미설치.\npip install pandas openpyxl xlrd")
 return
 if mode == "xlsx2md" and not check_lib("openpyxl"):
 messagebox.showerror("라이브러리 없음",
 "openpyxl 미설치.\npip install openpyxl")
 return

 # 옵션
 try:
 start = int(self.start_var.get) if self.start_var.get.strip else 0
 end = int(self.end_var.get) if self.end_var.get.strip else None
 except ValueError:
 messagebox.showerror("입력 오류", "페이지는 정수여야 합니다.")
 return

 overwrite = self.overwrite_var.get
 out_ext = m["out_ext"]

 # thread 실행
 self.is_running = True
 self.run_btn.config(state="disabled", text="변환 중...")
 self.progress["value"] = 0
 self.progress["maximum"] = len(self.files)

 t = threading.Thread(target=self._convert_all,
 args=(mode, out_ext, start, end, overwrite),
 daemon=True)
 t.start

 def _convert_all(self, mode: str, out_ext: str,
 start: int, end: int | None, overwrite: bool):
 ok = fail = skip = 0
 for i, src in enumerate(self.files):
 self.log_msg(f"[{i+1}/{len(self.files)}] {src.name}")
 try:
 if self.out_dir:
 out = self.out_dir / (src.stem + out_ext)
 else:
 out = src.with_suffix(out_ext)

 if out.exists and not overwrite:
 self.log_msg(f" ⏭ 이미 존재 — skip")
 skip += 1
 continue

 if mode == "pdf2docx":
 convert_pdf_to_docx(src, out, start, end)
 elif mode == "docx2md":
 msgs = convert_docx_to_md(src, out)
 for msg in msgs[:3]: # 첫 3개 경고만
 self.log_msg(f" note: {msg.message}")
 elif mode == "pdf2md":
 msgs = convert_pdf_to_md(src, out, start, end)
 for msg in msgs[:3]:
 self.log_msg(f" note: {msg.message}")
 elif mode == "xlsx2md":
 convert_xlsx_to_md(src, out)
 elif mode == "xls2md":
 convert_xls_to_md(src, out)

 self.log_msg(f" ✅ → {out}")
 ok += 1
 except Exception as e:
 self.log_msg(f" ❌ 실패: {e}")
 fail += 1

 self.progress["value"] = i + 1
 self.root.update_idletasks

 self.log_msg("")
 self.log_msg("=" * 50)
 self.log_msg(f"완료: 성공 {ok}, 실패 {fail}, skip {skip}")
 self.log_msg("=" * 50)

 self.is_running = False
 self.run_btn.config(state="normal", text="▶ 변환 시작")

 if ok > 0:
 messagebox.showinfo("완료", f"변환 완료\n성공: {ok}\n실패: {fail}\nskip: {skip}")

 def log_msg(self, msg: str):
 self.log.insert("end", msg + "\n")
 self.log.see("end")

def main:
 root = tk.Tk
 try:
 from ctypes import windll
 windll.shcore.SetProcessDpiAwareness(1)
 except Exception:
 pass
 app = DocConverterApp(root)
 root.mainloop

if __name__ == "__main__":
 main
