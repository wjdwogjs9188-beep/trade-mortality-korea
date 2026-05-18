"""
Consolidate cleaned PAP v4.5 main body + 4 patches into a single document for OSF upload.

Order:
  1. PAP_v4.5_main_body_cleaned.md
  2. PAP_v4.5.1_patch_cleaned.md
  3. PAP_v4.5.2_patch_cleaned.md
  4. PAP_v4.5.3_patch_cleaned.md
  5. PAP_v4.5.4_patch_cleaned.md

Output:
  PAP_v4.5_consolidated_cleaned.md  (single markdown)
  PAP_v4.5_consolidated_cleaned.docx (via pandoc)
  PAP_v4.5_consolidated_cleaned.pdf (via docx2pdf — Word COM, Malgun Gothic embedding)
"""

from pathlib import Path
import subprocess
import sys

PAP_DIR = Path(r"C:\Users\82103\Downloads\trade_mortality_korea\4_documentation\PAP")
OUTPUT_MD = PAP_DIR / "PAP_v4.5_consolidated_cleaned.md"
OUTPUT_DOCX = PAP_DIR / "PAP_v4.5_consolidated_cleaned.docx"
OUTPUT_PDF = PAP_DIR / "PAP_v4.5_consolidated_cleaned.pdf"

FILES_IN_ORDER = [
    "PAP_v4.5_main_body_cleaned.md",
    "PAP_v4.5.1_patch_cleaned.md",
    "PAP_v4.5.2_patch_cleaned.md",
    "PAP_v4.5.3_patch_cleaned.md",
    "PAP_v4.5.4_patch_cleaned.md",
]

HEADER = """# Pre-Analysis Plan v4.5 (Consolidated, Cleaned for OSF posting)

**Project**: Trade Integration, Family Formation, and the 'Korean' Deaths of Despair: Evidence from Sigungu-Level Bilateral Exposure

**Author**: Jaeheon Jung (정재헌), Department of Economics, Gachon University

**Pre-Analysis Plan version**: v4.5 (main body + 4 patches, consolidated)

**Internal frozen window**: 2026-05-05 20:52 KST (main body) to 2026-05-06 00:16 KST (final patch v4.5.4). All estimation work followed PAP completion.

**Public OSF posting date**: 2026-05-12

---

## Style cleanup note

This consolidated file reflects light copy-editing (removal of decorative special characters and stylistic phrases) applied 2026-05-12 to the originally-frozen 2026-05-05/06 source files. All analytical commitments — sample definitions, inference framework, outcome family, mediator framework, baseline year, identification protocol, and numerical specifications — are preserved verbatim from the original frozen versions. The original 5 source files are preserved in the replication archive at `4_documentation/PAP/` with their original mtime metadata. The cleaned consolidated file is suitable for OSF public posting; the original frozen sources remain the authoritative pre-registration documents.

---

## Consolidation note

This document concatenates the following 5 source files (cleaned versions) in the order in which patches were applied to the v4.5 main body:

1. PAP_v4.5_main_body_cleaned.md (cleaned from PAP_v4.5_main_body.md)
2. PAP_v4.5.1_patch_cleaned.md (cleaned from PAP_v4.5.1_patch.md)
3. PAP_v4.5.2_patch_cleaned.md (cleaned from PAP_v4.5.2_patch.md)
4. PAP_v4.5.3_patch_cleaned.md (cleaned from PAP_v4.5.3_patch.md)
5. PAP_v4.5.4_patch_cleaned.md (cleaned from PAP_v4.5.4_patch.md)

The original individual files are preserved in the replication archive at `4_documentation/PAP/` for traceability.

---

"""

def consolidate():
    parts = [HEADER]
    for fname in FILES_IN_ORDER:
        path = PAP_DIR / fname
        if not path.exists():
            print(f"[WARN] Missing: {path}")
            continue
        parts.append(f"\n\n---\n\n# Source: `{fname}`\n\n")
        parts.append(path.read_text(encoding="utf-8"))
    consolidated = "\n".join(parts)
    OUTPUT_MD.write_text(consolidated, encoding="utf-8")
    print(f"[OK] consolidated md: {OUTPUT_MD} ({len(consolidated):,} chars)")

def to_pdf():
    """Convert via pandoc + Word COM (docx2pdf) for Malgun Gothic East Asia rendering."""
    # First convert md -> docx via pandoc
    try:
        subprocess.run(
            ["pandoc", str(OUTPUT_MD), "--from", "markdown", "--to", "docx",
             "-o", str(OUTPUT_DOCX)],
            check=True, capture_output=True,
        )
        print(f"[OK] docx: {OUTPUT_DOCX}")
    except subprocess.CalledProcessError as e:
        print(f"[ERR] pandoc failed: {e.stderr.decode(errors='ignore')}")
        return
    except FileNotFoundError:
        print(f"[ERR] pandoc not found on PATH")
        return

    # Then docx -> pdf via Word COM
    try:
        from docx2pdf import convert
        convert(str(OUTPUT_DOCX), str(OUTPUT_PDF))
        print(f"[OK] pdf: {OUTPUT_PDF}")
    except Exception as e:
        print(f"[ERR] docx2pdf failed: {e}")
        print(f"      Use Word manually: open {OUTPUT_DOCX} → Save As PDF")

if __name__ == "__main__":
    consolidate()
    to_pdf()
