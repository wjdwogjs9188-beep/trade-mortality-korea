"""문서 변환 CLI — PDF/DOCX/XLSX/XLS/MD 상호 변환.

지원 모드:
  pdf2docx  : PDF  → DOCX
  docx2md   : DOCX → MD
  pdf2md    : PDF  → MD  (pdf2docx → mammoth chained)
  xlsx2md   : XLSX → MD  (모든 시트를 markdown 표로)
  xls2md    : XLS  → MD  (xlrd<2.0 필요)

사용법:
  # 단일 파일 (모드 자동 감지)
  python pdf_to_docx.py input.pdf                  # → input.docx
  python pdf_to_docx.py input.docx                 # → input.md
  python pdf_to_docx.py input.xlsx                 # → input.md
  python pdf_to_docx.py input.pdf --to md          # → input.md (체인)

  # 출력 경로 지정
  python pdf_to_docx.py input.pdf -o output.docx
  python pdf_to_docx.py input.xlsx -o codebook.md

  # 디렉토리 batch
  python pdf_to_docx.py /path/to/pdfs/             # 모든 PDF → DOCX
  python pdf_to_docx.py /path/to/xlsx/             # 모든 XLSX → MD
  python pdf_to_docx.py /path/to/pdfs/ --to md     # PDF → MD (체인)

  # 페이지 범위 (PDF 입력 한정)
  python pdf_to_docx.py input.pdf --start 70 --end 130

라이브러리:
  pip install pdf2docx==0.5.8 mammoth==1.8.0 pandas openpyxl xlrd
"""
import argparse
import sys
import tempfile
from pathlib import Path


def convert_pdf_to_docx(pdf: Path, out: Path, start: int = 0, end: int | None = None):
    try:
        from pdf2docx import Converter
    except ImportError:
        print("❌ pdf2docx 미설치. pip install pdf2docx==0.5.8")
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv = Converter(str(pdf))
    try:
        kwargs = {}
        if start: kwargs["start"] = start
        if end is not None: kwargs["end"] = end
        cv.convert(str(out), **kwargs)
    finally:
        cv.close()


def convert_docx_to_md(docx: Path, out: Path):
    try:
        import mammoth
    except ImportError:
        print("❌ mammoth 미설치. pip install mammoth==1.8.0")
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(docx, "rb") as f:
        result = mammoth.convert_to_markdown(f)
    out.write_text(result.value, encoding="utf-8")
    return result.messages


def convert_pdf_to_md(pdf: Path, out: Path, start: int = 0, end: int | None = None):
    """체인: PDF → 임시 DOCX → MD."""
    with tempfile.TemporaryDirectory() as td:
        tmp_docx = Path(td) / (pdf.stem + ".docx")
        convert_pdf_to_docx(pdf, tmp_docx, start, end)
        return convert_docx_to_md(tmp_docx, out)


def _df_to_md_table(df) -> str:
    """tabulate 의존 없는 DataFrame → markdown 표."""
    if df.empty:
        return "_(빈 시트)_\n"
    headers = [str(c) for c in df.columns]
    sep = ["---"] * len(headers)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for _, row in df.iterrows():
        cells = []
        for v in row:
            s = "" if v is None else str(v).replace("|", "\\|").replace("\n", "<br>").replace("\r", "")
            cells.append(s)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def convert_xlsx_to_md(xlsx: Path, out: Path, max_rows: int = 5000):
    """xlsx/xls 모든 시트 → markdown 표 (시트별 ## 헤딩)."""
    try:
        import pandas as pd
    except ImportError:
        print("❌ pandas 미설치. pip install pandas openpyxl xlrd")
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheets = pd.read_excel(xlsx, sheet_name=None, dtype=object)

    parts = [f"# {xlsx.name}\n", f"_원본 시트 수: {len(sheets)}_\n", ""]
    for name, df in sheets.items():
        parts.append(f"\n## Sheet: {name}\n")
        nrow, ncol = df.shape
        parts.append(f"_(rows: {nrow}, cols: {ncol})_\n")
        df = df.where(df.notna(), "")
        if nrow > max_rows:
            parts.append(f"\n⚠️ {nrow}행 중 처음 {max_rows}행만 표시\n")
            df = df.head(max_rows)
        parts.append("")
        parts.append(_df_to_md_table(df))
    out.write_text("\n".join(parts), encoding="utf-8")
    return []


# .xls 도 같은 함수로 (pandas 가 엔진 자동 선택)
convert_xls_to_md = convert_xlsx_to_md


# ───────────────────────── 모드 라우팅 ─────────────────────────
def detect_mode(in_ext: str, target: str | None) -> str:
    """입력 확장자 + --to 플래그로 모드 결정."""
    in_ext = in_ext.lower()
    if target:
        target = target.lower().lstrip(".")
        if in_ext == ".pdf"  and target == "docx": return "pdf2docx"
        if in_ext == ".pdf"  and target == "md":   return "pdf2md"
        if in_ext == ".docx" and target == "md":   return "docx2md"
        if in_ext == ".xlsx" and target == "md":   return "xlsx2md"
        if in_ext == ".xls"  and target == "md":   return "xls2md"
        raise ValueError(f"지원하지 않는 변환: {in_ext} → {target}")
    # 기본 (--to 없음): 자동 감지
    if in_ext == ".pdf":  return "pdf2docx"
    if in_ext == ".docx": return "docx2md"
    if in_ext == ".xlsx": return "xlsx2md"
    if in_ext == ".xls":  return "xls2md"
    raise ValueError(f"지원하지 않는 입력: {in_ext}")


MODE_OUTEXT = {"pdf2docx": ".docx", "docx2md": ".md", "pdf2md": ".md",
               "xlsx2md": ".md", "xls2md": ".md"}
MODE_INEXT = {"pdf2docx": ".pdf", "docx2md": ".docx", "pdf2md": ".pdf",
              "xlsx2md": ".xlsx", "xls2md": ".xls"}


def convert_one(src: Path, out: Path, mode: str,
                start: int = 0, end: int | None = None) -> bool:
    print(f"  변환 [{mode}]: {src.name} → {out.name}")
    try:
        if mode == "pdf2docx":
            convert_pdf_to_docx(src, out, start, end)
        elif mode == "docx2md":
            msgs = convert_docx_to_md(src, out)
            for m in msgs[:3]:
                print(f"    note: {m.message}")
        elif mode == "pdf2md":
            msgs = convert_pdf_to_md(src, out, start, end)
            for m in msgs[:3]:
                print(f"    note: {m.message}")
        elif mode == "xlsx2md":
            convert_xlsx_to_md(src, out)
        elif mode == "xls2md":
            convert_xls_to_md(src, out)
    except Exception as e:
        print(f"  ❌ 실패: {e}")
        return False
    print(f"  ✅ {out}")
    return True


def main():
    p = argparse.ArgumentParser(description="문서 변환기 (PDF/DOCX/MD)")
    p.add_argument("input", help="입력 파일 또는 폴더")
    p.add_argument("-o", "--output", help="출력 파일 또는 폴더")
    p.add_argument("--to", choices=["docx", "md"],
                   help="출력 포맷 (입력 확장자에 따라 자동 결정 가능)")
    p.add_argument("--start", type=int, default=0, help="시작 페이지 (0-based, PDF 한정)")
    p.add_argument("--end", type=int, default=None, help="끝 페이지 (exclusive, PDF 한정)")
    p.add_argument("--overwrite", action="store_true", help="기존 출력 파일 덮어쓰기")
    args = p.parse_args()

    inp = Path(args.input).expanduser().resolve()

    # ───── 단일 파일 ─────
    if inp.is_file():
        try:
            mode = detect_mode(inp.suffix, args.to)
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)

        out_ext = MODE_OUTEXT[mode]
        out = Path(args.output).expanduser().resolve() if args.output else inp.with_suffix(out_ext)

        if out.exists() and not args.overwrite:
            print(f"⚠️ {out} 이미 존재. --overwrite 옵션으로 덮어쓰기.")
            sys.exit(1)

        ok = convert_one(inp, out, mode, args.start, args.end)
        sys.exit(0 if ok else 1)

    # ───── 디렉토리 ─────
    elif inp.is_dir():
        # 디렉토리 batch — 가장 흔한 확장자 기준으로 모드 결정
        pdfs  = sorted(inp.glob("*.pdf"))
        docxs = sorted(inp.glob("*.docx"))
        xlsxs = sorted(inp.glob("*.xlsx"))
        xlss  = sorted(inp.glob("*.xls"))

        if args.to == "md":
            # 다중 후보 → 우선순위: xlsx > docx > xls > pdf (체인 비용)
            if xlsxs:
                mode, files = "xlsx2md", xlsxs
            elif docxs:
                mode, files = "docx2md", docxs
            elif xlss:
                mode, files = "xls2md", xlss
            elif pdfs:
                mode, files = "pdf2md", pdfs
            else:
                print(f"⚠️ {inp} 에 변환 가능한 파일 없음")
                sys.exit(1)
        elif args.to == "docx":
            mode, files = "pdf2docx", pdfs
            if not files:
                print(f"⚠️ {inp} 에 PDF 없음")
                sys.exit(1)
        else:
            # 기본 (--to 없음): 가장 많은 확장자에 자동
            if pdfs:    mode, files = "pdf2docx", pdfs
            elif docxs: mode, files = "docx2md",  docxs
            elif xlsxs: mode, files = "xlsx2md",  xlsxs
            elif xlss:  mode, files = "xls2md",   xlss
            else:
                print(f"⚠️ {inp} 에 변환 가능한 파일 없음")
                sys.exit(1)

        out_ext = MODE_OUTEXT[mode]
        out_dir = Path(args.output).expanduser().resolve() if args.output else inp

        print(f"=== Batch [{mode}]: {len(files)} 개 파일 → {out_dir} ===\n")
        ok_count = 0
        for src in files:
            out = out_dir / (src.stem + out_ext)
            if out.exists() and not args.overwrite:
                print(f"  ⏭ skip (exists): {out.name}")
                continue
            if convert_one(src, out, mode, args.start, args.end):
                ok_count += 1

        print(f"\n✅ 완료: {ok_count}/{len(files)} 성공")
        sys.exit(0 if ok_count == len(files) else 1)
    else:
        print(f"❌ {inp} 파일도 폴더도 아님")
        sys.exit(1)


if __name__ == "__main__":
    main()
