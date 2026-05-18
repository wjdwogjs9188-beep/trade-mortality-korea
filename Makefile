# Makefile — sequential pipeline reference for the panel build
# ============================================================
# For Windows users the canonical orchestrators are PowerShell scripts in
# 2_scripts/run/ (run_data_collection.ps1, run_phase_data_collection_v02.ps1,
# run_comtrade_pre_wto.ps1, run_crawl_hs_ksic_v01.ps1, run_kcue.ps1).
# This Makefile mirrors the build order for *nix / WSL environments.

PYTHON   := python
SCRIPTS  := 2_scripts
DERIVED  := 3_derived
RESULTS  := 4_results

.PHONY: all inventory sigungu panels bartik regress clean help

all: regress

# Phase 0 — raw inventory
inventory:
	$(PYTHON) $(SCRIPTS)/00_build_inventory.py

# Phase 1 — sigungu h_code crosswalk
sigungu:
	$(PYTHON) $(SCRIPTS)/sigungu_crosswalk/step3_build_h_code.py
	$(PYTHON) $(SCRIPTS)/sigungu_crosswalk/step4_validate.py
	$(PYTHON) $(SCRIPTS)/sigungu_crosswalk/step5_finalize.py

# Phase 2 — mortality / population / mediator panels
panels:
	$(PYTHON) $(SCRIPTS)/build_panel/2A_mortality_panel.py
	$(PYTHON) $(SCRIPTS)/build_panel/3A_population_panel.py
	$(PYTHON) $(SCRIPTS)/build_panel/3B_panel_v02.py
	$(PYTHON) $(SCRIPTS)/build_panel/3B_rate_v02_1.py
	$(PYTHON) $(SCRIPTS)/build_panel/3C_mediator_panel.py

# Phase 3 — Bartik IV (baseline 1994 shares, KIET60 mapping, Comtrade)
bartik:
	$(PYTHON) $(SCRIPTS)/bartik/02_build_baseline_shares_1994.py
	$(PYTHON) $(SCRIPTS)/bartik/03b_kiet60_mapping_v2_robust.py
	$(PYTHON) $(SCRIPTS)/bartik/04_bartik_iv_build.py

# Phase 4 — reduced-form regressions + Phase B-x diagnostics
# (see 2_scripts/identification/ for full diagnostic suite)
regress:
	$(PYTHON) $(SCRIPTS)/identification/reduced_form_5layer.py

clean:
	rm -rf $(DERIVED)/*.parquet $(RESULTS)/regression/*.csv
	@echo "Cleaned derived parquet and regression CSV."

help:
	@echo "Targets:"
	@echo "  make inventory  — Phase 0 raw inventory"
	@echo "  make sigungu    — Phase 1 sigungu h_code crosswalk"
	@echo "  make panels     — Phase 2 mortality / population / mediator"
	@echo "  make bartik     — Phase 3 Bartik IV build"
	@echo "  make regress    — Phase 4 reduced-form regressions"
	@echo "  make all        — full pipeline (inventory → regress)"
	@echo "  make clean      — remove derived parquet + regression csv"
