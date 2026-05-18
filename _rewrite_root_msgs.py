"""
Rewrite root + Phase-tracking commits to remove internal versioning vocabulary.

Targets the two oldest commits whose messages still show internal phase /
version language (v4.0 reset, Phase 0, Phase 2-7 progress, etc.). These are
the last-commit message for .env.example and METHODOLOGY.md on GitHub.

Since these are root-area commits, every descendant gets a new hash too — but
all authors are already the user, so no Claude orphan will surface.
"""
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")

NEW_MESSAGES = {
    "6ca1f4a": "Initial repository scaffold and project documentation",
    "0613120": "Add core pipeline scripts and reference materials",
}


def run(args, **kw):
    kw.setdefault("cwd", str(REPO))
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    kw.setdefault("encoding", "utf-8")
    proc = subprocess.run(["git"] + args, **kw)
    if proc.returncode != 0:
        print(f"[!] git {' '.join(args)} failed:\n{proc.stderr}")
        raise SystemExit(proc.returncode)
    return proc.stdout


def main():
    os.chdir(REPO)
    branch = run(["rev-parse", "--abbrev-ref", "HEAD"]).strip()
    if branch != "main":
        print(f"[!] not on main"); sys.exit(1)
    head_before = run(["rev-parse", "HEAD"]).strip()

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"pre-root-msg-{ts}"
    run(["branch", backup])
    print(f"[1] Backup branch: {backup}")

    # Entire history oldest → newest
    commits = run(["rev-list", "--reverse", "HEAD"]).split()
    print(f"[2] Commits in full history: {len(commits)}")

    mapping = {}
    print(f"\n[3] Rewriting (all 12 will get new hashes — root rewrite cascades)...")
    for old in commits:
        old_short = old[:7]
        old_msg = run(["log", "-n", "1", "--format=%B", old]).rstrip("\n") + "\n"
        tree = run(["rev-parse", f"{old}^{{tree}}"]).strip()
        old_parents = run(["log", "-n", "1", "--format=%P", old]).strip().split()
        new_parents = [mapping.get(p, p) for p in old_parents]
        info = run([
            "log", "-n", "1",
            "--format=%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI",
            old,
        ])
        an, ae, ai, cn, ce, ci = info.rstrip("\n").split("\x00")

        new_msg = NEW_MESSAGES.get(old_short, old_msg.strip())
        changed = "*" if new_msg.strip() != old_msg.strip() else " "

        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": an, "GIT_AUTHOR_EMAIL": ae, "GIT_AUTHOR_DATE": ai,
            "GIT_COMMITTER_NAME": cn, "GIT_COMMITTER_EMAIL": ce, "GIT_COMMITTER_DATE": ci,
        })
        cmd = ["git", "commit-tree", tree]
        for p in new_parents:
            cmd += ["-p", p]
        cmd += ["-m", new_msg]

        proc = subprocess.run(cmd, cwd=str(REPO), env=env,
                              capture_output=True, text=True, encoding="utf-8")
        if proc.returncode != 0:
            print(f"[!] commit-tree failed for {old_short}: {proc.stderr}")
            sys.exit(1)
        new_sha = proc.stdout.strip()
        mapping[old] = new_sha
        print(f"  {changed} {old_short} → {new_sha[:7]}  {new_msg[:70]}")

    new_head = mapping[commits[-1]]
    run(["update-ref", "refs/heads/main", new_head, head_before])
    print(f"\n[4] Moved main: {head_before[:7]} → {new_head[:7]}")
    print("\n[5] New log (all 12):")
    print(run(["log", "--oneline"]))

    ans = input("\nForce-push to origin/main? (y/N) ").strip().lower()
    if ans != "y":
        print(f"Skipped. Rollback: git reset --hard {backup}"); return
    subprocess.run(["git", "push", "--force-with-lease", "origin", "main"],
                   cwd=str(REPO), text=True, encoding="utf-8")
    print(f"\nBackup: {backup}")
    print(f"Rollback: git reset --hard {backup} ; git push --force origin main")


if __name__ == "__main__":
    main()
