# 5_logs — 본 paper 의 결정·진단·방법론 archive index _2026-05-06 작성 (file 이동 없는 README index, navigability 회복용)_ 본 paper (Trade × Mortality Korea) 의 모든 결정 commit, build 진단, 방법론 note, data 수집 log 가 이 폴더 아래 archive 되어 있습니다. --- ## 폴더 구조 ```
5_logs/
├── README.md (이 file — 전체 index)
├── pre_analysis_plan.md (PAP v4.x 의 root copy)
├── my_execution_plan.md (사용자 작성 execution plan)
├── decisions/ (14 결정 commit log — paper 본문 결정의 source)
│ └── README.md
├── integrity_checks/ (36 build 진단·검증 file — script 시행착오 lessons)
│ └── README.md
├── methodology_notes/ (9 anchor paper deep summary — paper § 4 방법론 source)
│ └── README.md
└── data_collection/ (12 data fetch progress log — Phase 1 archive) └── README.md
``` --- ## 핵심 navigation | 의도 | 봐야 할 file |
|------|------------|
| 본 paper 의 commit 결정이 뭐인지 알고 싶다 | `decisions/README.md` → 시간순 14 file |
| build script 의 어느 단계가 검증됐는지 알고 싶다 | `integrity_checks/README.md` → phase 별 36 file |
| paper § 4 (Identification) 의 anchor reference 가 어디인지 | `methodology_notes/README.md` → 9 paper |
| Phase 1 data 수집의 어느 통계표를 받았는지 | `data_collection/README.md` → 12 fetch log |
| 본 paper 의 pre-analysis plan 자체 | `pre_analysis_plan.md` (5_logs/ root) | --- ## Cross-reference - paper 본문: `7_paper/paper_draft_v01_section_*.md`
- PAP version archive: `4_documentation/PAP/`
- daily status archive: `4_documentation/status_reports/daily_status/`
- raw data inventory: `4_documentation/pipeline_docs/raw_data_inventory.md`
- reference library: `4_documentation/reference_library/paper_summaries/` (19 deep summary)
- working memory: project root `CLAUDE.md`
