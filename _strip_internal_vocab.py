"""
Strip internal-only vocabulary from the public repo:
  - PAP v4.0 / v4.5.x references → 'pre-analysis plan' (section refs preserved)
  - v4.0 reset / v3.x mislabel → public phrasing
  - Phase B-x → identification diagnostic
Keeps generic Phase 1/2/3, Stage 1/2/3, and file path _v01/_v02 suffixes.

Walks every text file (skipping binaries), applies substitutions, prints
a diff summary, then commits + pushes on confirmation.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")

# Substitution rules — order matters (more specific first)
SUBS = [
    # PAP with section ref → drop PAP version label, keep §
    (re.compile(rb"PAP\s*v\d+(?:\.\d+)*\s*\xc2\xa7"), b"\xc2\xa7"),  # § = 0xc2 0xa7 UTF-8
    (re.compile(rb"PAP\s*v\d+(?:\.\d+)*\s*\xc2\xa6"), b"\xc2\xa6"),  # alt §
    # PAP version without section
    (re.compile(rb"PAP\s*v\d+(?:\.\d+)*", re.IGNORECASE), b"pre-analysis plan"),
    # Standalone "PAP" with word boundaries
    (re.compile(rb"\bPAP\b"), b"pre-analysis plan"),
    # Internal milestones
    (re.compile(rb"v4\.0\s+reset", re.IGNORECASE), b"project reset"),
    (re.compile(rb"\bv3\.x\s+mislabel", re.IGNORECASE), b"earlier version mapping error"),
    (re.compile(rb"\bv3\.x\b", re.IGNORECASE), b"earlier version"),
    (re.compile(rb"\bv4\.0\b"), b"1.0"),
    # Phase B-x diagnostic suite
    (re.compile(rb"Phase\s*B-?x", re.IGNORECASE), b"identification diagnostic"),
]

BINARY_EXT = {".png",".jpg",".jpeg",".gif",".webp",".pdf",".zip",".gz",".tar",".7z",".rar",
              ".xlsx",".xls",".docx",".doc",".pptx",".ppt",".parquet",".pkl",".npy",".npz",
              ".db",".sqlite",".sqlite3",".exe",".dll",".so",".dylib",".bin",
              ".woff",".woff2",".ttf",".otf",".eot",".mp3",".mp4",".wav",".avi",".mov"}

# Files we should NOT modify (filenames themselves contain phase_bx etc, but
# our regex skips lowercase phase_bx, so this is precautionary)
SKIP_FILES = set()


def should_skip(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXT:
        return True
    rel = str(path.relative_to(REPO))
    if rel in SKIP_FILES:
        return True
    if ".git" in rel.split(os.sep):
        return True
    if rel.startswith("_"):  # our own utility scripts
        return True
    return False


def run(args, **kw):
    kw.setdefault("cwd", str(REPO))
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    kw.setdefault("encoding", "utf-8")
    proc = subprocess.run(args, **kw)
    return proc


def main():
    os.chdir(REPO)
    print("[1] Scanning git-tracked files only (avoids 0_raw/ junction)...")

    # Use git ls-files -z (null-delimited, Korean-safe) to get tracked files
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=str(REPO), capture_output=True,
    )
    raw = proc.stdout
    tracked_rels = [p.decode("utf-8", errors="replace")
                    for p in raw.rstrip(b"\x00").split(b"\x00") if p]
    print(f"  {len(tracked_rels)} tracked files")

    changes = {}
    for rel in tracked_rels:
        path = REPO / rel
        if not path.exists() or not path.is_file():
            continue
        if path.suffix.lower() in BINARY_EXT:
            continue
        if rel.startswith("_") or "/_" in rel.replace("\\", "/"):
            continue
        try:
            data = path.read_bytes()
        except Exception:
            continue
        new_data = data
        per_pattern = []
        for pat, repl in SUBS:
            new_data, n = pat.subn(repl, new_data)
            if n:
                per_pattern.append((pat.pattern.decode("utf-8", errors="replace"), n))
        if new_data != data:
            changes[rel] = (per_pattern, new_data, path)

    if not changes:
        print("  Nothing to change — already clean.")
        return

    print(f"\n[2] Files to modify: {len(changes)}")
    total_edits = 0
    for rel, (per_pattern, _, _) in sorted(changes.items(), key=lambda x: -sum(n for _, n in x[1][0])):
        n_total = sum(n for _, n in per_pattern)
        total_edits += n_total
        breakdown = ", ".join(f"{n}×({p[:30]})" for p, n in per_pattern)
        print(f"  {n_total:>3}  {rel}  [{breakdown}]")
    print(f"\n  Total edits across {len(changes)} files: {total_edits}")

    ans = input("\nApply changes locally? (y/N) ").strip().lower()
    if ans != "y":
        print("Cancelled.")
        return

    print(f"\n[3] Writing files...")
    for rel, (_, new_data, path) in changes.items():
        path.write_bytes(new_data)
    print(f"  {len(changes)} files updated.")

    print(f"\n[4] Staging + commit...")
    run(["git", "add", "-A"])
    msg = "Standardize internal nomenclature for public release"
    proc = run(["git", "commit", "-m", msg])
    print(proc.stdout or proc.stderr)

    ans = input("\nPush to origin/main? (y/N) ").strip().lower()
    if ans != "y":
        print("Local commit done. Push skipped.")
        return

    proc = subprocess.run(["git", "push", "origin", "main"],
                          cwd=str(REPO), text=True, encoding="utf-8")
    print("Done.")


if __name__ == "__main__":
    main()
