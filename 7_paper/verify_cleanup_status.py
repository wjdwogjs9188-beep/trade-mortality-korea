"""
Paper v02 cleanup status verifier
==================================
Trade × Mortality Korea — Path A unification verify script

본 script 는 paper 4 file 의 cleanup commit 결과의 정합 status 를 직접 검증.
사용자가 직접 실행해서 (1) archive leftover 잔존 영역 식별 + (2) native build target value 정합 verify
+ (3) β/SE = t arithmetic verify + (4) 미적용 영역 list 산출 가능.

Usage:
    cd C:\\Users\\82103\\Downloads\\trade_mortality_korea\\7_paper
    python verify_cleanup_status.py

Output:
    - stdout: archive leftover line list + native target line list + arithmetic verify result
    - cleanup_verify_report.md: 통합 report

Author: Claude (공동저자 mode, 2026-05-06)
"""

import re
import math
import csv
from pathlib import Path

PAPER_DIR = Path(__file__).parent
PAPER_FILES = [
    "paper_draft_v01_section_1_2.md",
    "paper_draft_v01_section_5.md",
    "paper_draft_v01_section_6.md",
    "paper_draft_v01_section_8_9.md",
]

# ============================================================
# Path A target values (cleanup commit 후 target state)
# ============================================================
PATH_A_TARGETS = {
    "main_beta_native": "-0.127",
    "main_beta_archive_robustness": "-0.0685",  # robustness footnote 영역 보존 가능
    "main_n_native": "221",
    "main_n_archive_robustness": "222",
    "respiratory_n_native": "219",
    "respiratory_n_archive": "198",
    "long_difference_window": "1997-1999 to 2018-2022 (또는 1997-1999 ↔ 2018-2022)",
    "trade_volume_window": "2000-2010 integration period",
    "percent_reduction_native": "11.92 percent (또는 -11.9 percent)",
    "percent_reduction_archive": "6.85 percent (사용 금지, native 통일)",
    "cluster_t_native": "-4.02",
    "cluster_t_archive": "-3.11",
    "akm_t_native": "-4.92 (또는 -4.93)",
    "akm_t_archive": "-3.65",
    "p_wcr_native": "<0.0001",
    "p_rw_native": "0.0161",
    "p_rw_archive_inhouse": "0.317",
    "placebo_beta_native": "-0.123",
    "placebo_beta_archive": "+0.0238 (또는 +0.024)",
    "placebo_t_native": "-3.50",
    "baseline_1992_beta_native": "-0.0640",
    "baseline_1992_beta_archive": "-0.0158",
    "baseline_1992_n_native": "209",
    "baseline_1992_n_archive": "210",
    "attenuation_factor": "50.4 percent",
    "long_run_amplification_ratio": "1.85 (또는 1.854)",
}

# ============================================================
# Archive leftover patterns (cleanup 진행 시 모두 사라져야 함)
# ============================================================
ARCHIVE_LEFTOVER_PATTERNS = {
    "main_beta_archive_in_main_context": [
        r"β_main\s*=\s*-?0[.,]0685",
        r"β\s*=\s*-?0[.,]0685(?!.*archive)(?!.*sensitivity)(?!.*robustness)",
        r"main\s+β\s*=\s*-?0[.,]0685",
        r"deaths-of-despair\s+coefficient\s*\(\s*-?0[.,]0685\s*\)",
    ],
    "main_n_archive_in_main_context": [
        r"n\s*=\s*222\s+main",
        r"222\s+sigungu\s+main",
        r"222\s+districts(?!.*archive)",
    ],
    "long_difference_window_archive": [
        r"From\s+2000\s+to\s+2010—the\s+long-difference\s+period",
        r"2000\s+to\s+2010—the\s+long-difference",
    ],
    "percent_reduction_archive": [
        r"-?6[.,]85\s+percent\s+(?:reduction|mortality\s+decline)",
        r"-?6[.,]9\s+percent\s+mortality\s+decline",
    ],
    "placebo_beta_archive_main": [
        r"β_placebo\s*=\s*\+?0[.,]0238",
        r"β_placebo\s*=\s*\+?0[.,]024(?!\d)",
        r"placebo\s+coefficient\s+is\s+\+0[.,]024",
    ],
    "baseline_1992_beta_archive": [
        r"β_1992\s*=\s*-?0[.,]0158",
    ],
    "baseline_1992_n_archive": [
        r"n\s*=\s*210\s*;",
        r"210\s+sigungu\s+vs\s+222",
    ],
    "p_rw_archive_only": [
        r"p_RW\s*=\s*0[.,]317(?!.*earlier|.*in-house|.*standard\s+backend)",
    ],
    "akm_t_archive_in_main": [
        r"AKM\s+industry-mode\s+estimator\s*\(\s*t\s*=\s*-?3[.,]65\s*\)",
        r"cluster-on-industry-mode\s*=\s*3[.,]65",
    ],
    "cluster_t_archive_in_main": [
        r"cluster-province\s+sandwich\s*\(\s*t\s*=\s*-?3[.,]11\s*\)",
        r"cluster-province\s*=\s*3[.,]11",
    ],
}

# ============================================================
# Native build target patterns (cleanup 후 commit 되어 있어야 함)
# ============================================================
NATIVE_TARGET_PATTERNS = {
    "main_beta_native": r"β\s*=\s*-?0[.,]127|β_main\s*=\s*-?0[.,]127",
    "main_n_native": r"n\s*=\s*221|221\s+(?:districts|sigungu|main)",
    "long_difference_native_window": r"1997-1999\s*(?:↔|to|base.*?endpoint).*?2018-2022",
    "percent_reduction_native": r"-?11[.,]9\d?\s+percent",
    "cluster_t_native": r"cluster-province\s*(?:asymptotic\s*)?(?:\(?\s*)?t\s*=\s*-?4[.,]02",
    "akm_t_native": r"AKM-proper.*?t\s*=\s*-?4[.,]9[2-3]",
    "p_wcr_native": r"p_WCR\s*<\s*0[.,]0001",
    "p_rw_native": r"p_RW\s*=\s*0[.,]0161",
    "placebo_beta_native": r"β_placebo\s*=\s*-?0[.,]123",
    "baseline_1992_beta_native": r"β_1992\s*=\s*-?0[.,]0640",
    "baseline_1992_n_native": r"n\s*=\s*209",
    "attenuation_factor": r"50[.,]4\s*percent|attenuation\s+factor.*?50[.,]4",
    "amplification_ratio": r"1[.,]8(?:5|54)|β.*?ratio.*?1[.,]85",
}


def grep_file(filepath, pattern):
    """Return list of (line_num, line) tuples matching the pattern."""
    matches = []
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if re.search(pattern, line):
                matches.append((i, line.rstrip()))
    return matches


def verify_archive_leftover():
    """Find archive leftover lines (cleanup 후 0개여야 함)."""
    print("=" * 70)
    print("ARCHIVE LEFTOVER CHECK (must be 0 in main context)")
    print("=" * 70)
    findings = {}
    for category, patterns in ARCHIVE_LEFTOVER_PATTERNS.items():
        findings[category] = []
        for pattern in patterns:
            for fname in PAPER_FILES:
                fpath = PAPER_DIR / fname
                if not fpath.exists():
                    continue
                hits = grep_file(fpath, pattern)
                for line_num, line in hits:
                    findings[category].append({
                        "file": fname,
                        "line": line_num,
                        "pattern": pattern,
                        "context": line[:200],
                    })
    total_leftover = sum(len(v) for v in findings.values())
    if total_leftover == 0:
        print("\n✅ Archive leftover ZERO — all 정합")
    else:
        print(f"\n⚠️  Archive leftover {total_leftover} hit(s) found:")
        for category, hits in findings.items():
            if hits:
                print(f"\n  [{category}]")
                for h in hits:
                    print(f"    {h['file']}:{h['line']}  →  {h['context'][:120]}")
    return findings


def verify_native_target():
    """Verify native build target patterns are present."""
    print("\n" + "=" * 70)
    print("NATIVE BUILD TARGET CHECK (presence verify)")
    print("=" * 70)
    findings = {}
    for label, pattern in NATIVE_TARGET_PATTERNS.items():
        findings[label] = []
        for fname in PAPER_FILES:
            fpath = PAPER_DIR / fname
            if not fpath.exists():
                continue
            hits = grep_file(fpath, pattern)
            for line_num, line in hits:
                findings[label].append({
                    "file": fname,
                    "line": line_num,
                })
    print()
    for label, hits in findings.items():
        status = "✅" if hits else "❌ NOT FOUND"
        files = ", ".join(f"{h['file']}:{h['line']}" for h in hits[:3])
        more = f" (+{len(hits)-3} more)" if len(hits) > 3 else ""
        print(f"  {status}  {label:35}  {files}{more}")
    return findings


def verify_arithmetic():
    """β/SE = t arithmetic verify on Table 1 + Table 2 native values."""
    print("\n" + "=" * 70)
    print("ARITHMETIC VERIFY (β/SE = t)")
    print("=" * 70)
    rows = [
        # (label, beta, se, t_expected, tolerance)
        ("Table 1 cluster-province", -0.127212, 0.031679, -4.02, 0.05),
        ("Table 1 AKM-proper Kolesár", -0.127212, 0.025848, -4.92, 0.05),
        ("Table 2 cancer cluster", -0.049877, 0.030369, -1.64, 0.05),
        ("Table 2 cardio cluster", -0.069708, 0.022575, -3.09, 0.05),
        ("Table 2 respiratory cluster", 0.075382, 0.045699, 1.65, 0.05),
        ("Table 2 ext_other cluster", -0.017182, 0.039440, -0.44, 0.05),
        ("§ 6.1 placebo cluster", -0.123214, 0.035221, -3.50, 0.05),
        ("§ 6.3 1992 baseline cluster", -0.063980, 0.029352, -2.18, 0.05),
    ]
    print(f"{'Label':40} {'β':>12} {'SE':>10} {'t (calc)':>10} {'t (paper)':>10} {'OK':>4}")
    for label, beta, se, t_expected, tol in rows:
        t_calc = beta / se
        ok = abs(t_calc - t_expected) < tol
        status = "✅" if ok else "⚠️"
        print(f"{label:40} {beta:>12.6f} {se:>10.6f} {t_calc:>10.4f} {t_expected:>10.2f} {status:>4}")
    print()
    print("  percent reduction verify: 1 - exp(-0.127) = ", end="")
    print(f"{1 - math.exp(-0.127):.6f} (= {(1-math.exp(-0.127))*100:.2f}%)")
    print(f"  attenuation factor: -0.0640 / -0.127 = {(-0.0640)/(-0.127):.4f} (= {((-0.0640)/(-0.127))*100:.1f}%)")
    print(f"  amplification ratio: -0.127 / -0.0685 = {(-0.127)/(-0.0685):.4f}")


def verify_unapplied():
    """미적용 영역 list (사용자 측 commit 또는 추가 R-A 진행 영역)."""
    print("\n" + "=" * 70)
    print("UNAPPLIED 영역 (사용자 결정 또는 추가 commit 필요)")
    print("=" * 70)
    unapplied = [
        ("§ 5.1 line 14 Footnote X", "σ_z native unit value 사용자 측 R console verify",
         "사용자 측 R 1 line: sd(panel$z_x[is.finite(panel$z_x)])"),
        ("§ 5.1 HC1 t native", "HC1 SE / t native value verify",
         "사용자 측 R: sandwich::vcovHC(fit, type='HC1') |> diag() |> sqrt()"),
        ("§ 3.2 Sample Attrition Table A.1·A.2", "INSERT location 결정",
         "별도 file (paper_draft_v01_section_3_4.md) 또는 § 3 본문에 INSERT"),
        ("§ 6.X sensitivity bound footnote", "별도 footnote vs § 6.3 통합 paragraph 결정",
         "현재 § 6.3 끝에 통합 commit, 사용자 결정 영역"),
    ]
    for label, desc, action in unapplied:
        print(f"\n  📋 {label}")
        print(f"      desc:   {desc}")
        print(f"      action: {action}")


def main():
    print("\n" + "=" * 70)
    print("Paper v02 Cleanup Status Verify (Path A unification)")
    print(f"  Working dir: {PAPER_DIR}")
    print(f"  Paper files: {len(PAPER_FILES)} files")
    print("=" * 70)
    leftover = verify_archive_leftover()
    targets = verify_native_target()
    verify_arithmetic()
    verify_unapplied()

    # CSV report
    report_path = PAPER_DIR / "cleanup_verify_report.csv"
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "file", "line", "pattern", "context"])
        for category, hits in leftover.items():
            for h in hits:
                w.writerow([category, h["file"], h["line"], h["pattern"], h["context"]])
    print(f"\n📄 CSV report saved: {report_path}")
    print("\n" + "=" * 70)
    print("Verify complete. Review archive leftover above; 0 hit = clean Path A unification.")
    print("=" * 70)


if __name__ == "__main__":
    main()
