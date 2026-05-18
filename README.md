# Trade × Mortality Korea

**Author:** 정재헌 (Jae-Heon Jeong)
**Affiliation:** Department of Economics, Gachon University
**ORCID:** 0009-0009-9403-0940

Replication package for **"Trade Integration, Family Formation, and the 'Korean'
Deaths of Despair: Evidence from Sigungu-Level Bilateral Exposure."**

---

## Research question

For an export-oriented economy such as Korea, what is the causal effect of
bilateral trade exposure to China on sigungu-level (county-equivalent)
mortality? Identification uses a Bartik shift-share instrument built from 1994
manufacturing employment shares interacted with Korea-China bilateral import
growth. Outcomes follow the Case-Deaton (2015) deaths-of-despair construction
adapted to working-age (25-64) Korean nationals.

See [METHODOLOGY.md](METHODOLOGY.md) for the full specification and
[DATA_SOURCES.md](DATA_SOURCES.md) for raw data provenance.

---

## Repository layout

```
trade_mortality_korea/
├── 1_codebooks/             variable definitions (ICD-10, KSIC, sigungu)
├── 2_scripts/               Python pipeline + run/ orchestrators (.ps1)
│   ├── bartik/              Bartik IV construction (baseline 1994 shares)
│   ├── build_panel/         mortality / population / mediator panels
│   ├── crosswalks/          KSIC ↔ HS6 mapping
│   ├── data_collection/     Comtrade, KOSIS, HIRA fetchers
│   ├── identification/      identification diagnostics + reduced-form spec
│   ├── lib/                 shared modules (io, log, icd10, validate)
│   ├── mechanism/           DGHP mediator decomposition
│   ├── mortality/           ICD-10 ↔ outcome group mappings
│   ├── sigungu_crosswalk/   1997-2023 sigungu h_code build
│   ├── run/                 PowerShell orchestrators (Windows)
│   ├── utils/               misc helpers
│   └── verify/              schema + integrity checks
├── 3_derived/sigungu/       derived sigungu codebooks (CSV outputs)
├── 4_documentation/         crosswalk diagnostics
└── 4_results/regression/    reduced-form coefficient + SE tables
```

Raw data (`0_raw/`) is not redistributed — see DATA_SOURCES.md for retrieval
instructions per source.

---

## Quick start

```bash
pip install -r requirements.txt

# Unix / WSL
make all

# Windows
powershell -File 2_scripts/run/run_phase_data_collection_v02.ps1
```

Individual Makefile targets: `make inventory`, `sigungu`, `panels`, `bartik`,
`regress` (see `make help`).

---

## Methodological principles

1. `0_raw/` is read-only — all transformations write to `3_derived/`.
2. Cause-of-death classification maps from ICD-10 raw directly; KOSIS
   104-category codes are used as a reference layer only.
3. Every panel passes a KOSTAT cross-check before being committed to disk.
4. Variable definitions live in `1_codebooks/` (YAML / CSV) — no hard-coding
   inside scripts.
5. All regressions report a 5-layer SE: HC1, cluster-sido, AKM (industry-mode),
   Conley (centroid 1/5/10 km), and weak-IV-robust tF inference.

---

## Citation

If you use this code or any derived codebook, please cite the working paper
(see project page) and the underlying data sources listed in DATA_SOURCES.md.
