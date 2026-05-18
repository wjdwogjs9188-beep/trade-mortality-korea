"""뉴 논문 폴더 → trade_mortality_korea/4_documentation/ 정리 통합.

분류 logic:
 - PAP_*.md, *reference_*.md, pap_*.md → 4_documentation/pre-analysis plan/
 - reference_library_*.md, REFERENCE_LIBRARY_*.md, paper_summaries/ → 4_documentation/reference_library/
 - stage*_plan*.md, stage*_for_review*.md, section*_writing*.md → 4_documentation/stage_plans/
 - panel_construction_*.md, mediator_panel_*.md, *pipeline*.md → 4_documentation/pipeline_docs/
 - daily_status/, status_for_review_*.md, handoff_*.md, data_collection_protocol_*.md → 4_documentation/status_reports/
 - crosswalks/ → 4_documentation/crosswalks_paper/ (0_raw/crosswalks 와 별개)
 - 기타 → 4_documentation/misc/

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\verify\\merge_paper_folder.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

SRC = Path(r"C:\Users\82103\Desktop\뉴 논문")
DST_ROOT = Path(r"C:\Users\82103\Downloads\trade_mortality_korea\4_documentation")

# Sub-folder 별 매칭 rule (filename keyword)
RULES = [
 ("pre-analysis plan", lambda name: (
 name.startswith("PAP_") or name.startswith("pap_") or
 name.startswith("PAP_v3.4_reference") or name == "research_proposal.md"
)),
 ("reference_library", lambda name: (
 name.startswith("reference_library_") or
 name.startswith("REFERENCE_LIBRARY_") or
 name == "paper_summaries" # 폴더
)),
 ("stage_plans", lambda name: (
 name.startswith("stage") and ("plan" in name or "regression" in name)
 or name.startswith("section") and "writing" in name
)),
 ("pipeline_docs", lambda name: (
 "pipeline" in name or
 name.startswith("panel_construction") or
 name.startswith("mediator_panel") or
 name == "raw_data_inventory.md"
)),
 ("status_reports", lambda name: (
 name.startswith("status_for_review") or
 name.startswith("stage") and "for_review" in name or
 name.startswith("handoff_") or
 name.startswith("data_collection_protocol") or
 name == "daily_status" # 폴더
)),
 ("crosswalks_paper", lambda name: name == "crosswalks"), # 폴더
]

def classify(name: str) -> str:
 """파일/폴더 명 → sub-folder 결정."""
 for sub, rule in RULES:
 if rule(name):
 return sub
 return "misc"

def main -> int:
 print("=" * 70)
 print("뉴 논문 → trade_mortality_korea/4_documentation/ 정리 통합")
 print("=" * 70)
 print(f" source: {SRC}")
 print(f" destination: {DST_ROOT}")

 # Sub-folder 생성
 sub_folders = ["pre-analysis plan", "reference_library", "stage_plans",
 "pipeline_docs", "status_reports",
 "crosswalks_paper", "misc"]
 for sub in sub_folders:
 (DST_ROOT / sub).mkdir(parents=True, exist_ok=True)
 print(f"\n[mkdir] {len(sub_folders)} sub-folders created")

 # 분류 + 이동 (top-level 만, sub-folder 그대로 keep)
 moved = {sub: for sub in sub_folders}
 skipped = 

 for item in sorted(SRC.iterdir):
 sub = classify(item.name)
 target = DST_ROOT / sub / item.name

 if target.exists:
 skipped.append(f"{item.name} (이미 존재)")
 continue

 try:
 if item.is_dir:
 shutil.copytree(item, target)
 # 원본 삭제 안 함 (사용자 verify 후 수동 삭제)
 moved[sub].append(f"{item.name}/ (폴더 + 하위 모두)")
 else:
 shutil.copy2(item, target)
 moved[sub].append(item.name)
 except Exception as e:
 skipped.append(f"{item.name} ({type(e).__name__}: {e})")

 # 보고
 print(f"\n[result]")
 total = 0
 for sub, files in moved.items:
 if files:
 print(f"\n [{sub}] {len(files)} 항목:")
 for f in files:
 print(f" {f}")
 total += len(files)

 if skipped:
 print(f"\n [skipped] {len(skipped)}:")
 for s in skipped:
 print(f" {s}")

 print(f"\n총 {total} 항목 이동 (copy, 원본 보존)")
 print(f"\n다음 step (사용자 verify 후 수동):")
 print(f" 1. {DST_ROOT} 의 분류 결과 검토")
 print(f" 2. 누락/잘못 분류 수정")
 print(f" 3. 원본 폴더 ({SRC}) 삭제 (PowerShell: Remove-Item -Recurse '{SRC}')")
 print("=" * 70)

 return 0

if __name__ == "__main__":
 import sys
 sys.exit(main)
