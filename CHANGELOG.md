# Changelog

All notable changes to this project. Dates in ISO 8601 (YYYY-MM-DD).

## [1.0.0] — 2026-05-18

Initial public release accompanying the manuscript
**"Trade Integration, Family Formation, and the 'Korean' Deaths of Despair:
Evidence from Sigungu-Level Bilateral Exposure."**

### Included
- Codebooks (`1_codebooks/`) — sigungu crosswalk 1997-2023, KSIC6→KSIC9 mapping,
  104 mortality cause classification, HIRA sgguCd→h_code crosswalk
- Build pipeline (`2_scripts/`) — Bartik IV construction, mortality / population /
  mediator panels, KSIC↔HS6 crosswalks, identification diagnostics, mortality
  rate computation, verification utilities
- Derived codebooks (`3_derived/sigungu/`) — h_code mapping outputs
- Reduced-form regression results (`4_results/regression/`) —
  main 5-layer SE specification, Romano-Wolf, robustness cascades, placebo,
  rotemberg weights
- Crosswalks documentation (`4_documentation/crosswalks_paper/`) — KIET60 ↔
  HS6 ↔ KSIC mapping diagnostics
