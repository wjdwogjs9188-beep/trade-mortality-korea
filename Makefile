# Makefile — 전체 파이프라인 한 번에 재현
# 사용: make all, make clean, make panel, etc.

PYTHON := python3
SCRIPTS := 2_scripts
DERIVED := 3_derived
RESULTS := 4_results
LOGS := 5_logs

.PHONY: all clean panel iv regress robust paper help

all: paper

# Phase 0: raw extract + inventory
$(DERIVED)/raw_inventory.csv: 0_raw/
	$(PYTHON) $(SCRIPTS)/00_extract_zips.py
	$(PYTHON) $(SCRIPTS)/00_build_inventory.py

# Phase 2: panels
$(DERIVED)/mortality_panel.parquet: 0_raw/지역별\ 자살\ 데이터/ 1_codebooks/icd10_to_cause.yaml
	$(PYTHON) $(SCRIPTS)/01_build_mortality_panel.py

$(DERIVED)/population_panel.parquet: 0_raw/연구\ 자료/
	$(PYTHON) $(SCRIPTS)/02_build_population_panel.py

$(DERIVED)/asmr_panel.parquet: $(DERIVED)/mortality_panel.parquet $(DERIVED)/population_panel.parquet
	$(PYTHON) $(SCRIPTS)/03_compute_asmr.py

$(DERIVED)/industry_panel.parquet: 0_raw/산업\ 비중\ 데이터/
	$(PYTHON) $(SCRIPTS)/04_build_industry_panel.py

$(DERIVED)/trade_panel.parquet: 0_raw/연구\ 자료/
	$(PYTHON) $(SCRIPTS)/05_build_trade_data.py

panel: $(DERIVED)/asmr_panel.parquet $(DERIVED)/industry_panel.parquet $(DERIVED)/trade_panel.parquet

# Phase 3: Bartik IV
$(DERIVED)/bartik_iv.parquet: $(DERIVED)/industry_panel.parquet $(DERIVED)/trade_panel.parquet
	$(PYTHON) $(SCRIPTS)/06_build_bartik_iv.py

iv: $(DERIVED)/bartik_iv.parquet

# Phase 4: 회귀
$(DERIVED)/analysis_panel.parquet: $(DERIVED)/asmr_panel.parquet $(DERIVED)/bartik_iv.parquet
	$(PYTHON) $(SCRIPTS)/07_build_controls.py

$(RESULTS)/regression_log.csv: $(DERIVED)/analysis_panel.parquet
	$(PYTHON) $(SCRIPTS)/08_run_regressions.py

regress: $(RESULTS)/regression_log.csv

# Phase 6: Robustness
$(RESULTS)/robustness_log.csv: $(DERIVED)/analysis_panel.parquet
	$(PYTHON) $(SCRIPTS)/09_robustness.py

robust: $(RESULTS)/robustness_log.csv

# Phase 7: 표/그림
$(RESULTS)/tables/main.tex: $(RESULTS)/regression_log.csv
	$(PYTHON) $(SCRIPTS)/10_make_tables.py

$(RESULTS)/figures/fig1.pdf: $(RESULTS)/regression_log.csv
	$(PYTHON) $(SCRIPTS)/11_make_figures.py

paper: $(RESULTS)/tables/main.tex $(RESULTS)/figures/fig1.pdf

# 정리
clean:
	rm -rf $(DERIVED)/*.parquet
	rm -rf $(RESULTS)/tables/*.tex $(RESULTS)/figures/*.pdf
	@echo "Cleaned derived data and results. Raw and logs preserved."

clean-all: clean
	rm -rf $(LOGS)/pipeline_runs/*
	@echo "Also cleaned logs."

help:
	@echo "Targets:"
	@echo "  make all       — 전체 파이프라인"
	@echo "  make panel     — panel 데이터까지"
	@echo "  make iv        — Bartik IV 까지"
	@echo "  make regress   — 회귀 까지"
	@echo "  make robust    — robustness 까지"
	@echo "  make paper     — 표/그림"
	@echo "  make clean     — derived/results 삭제"
	@echo "  make clean-all — 위 + logs 삭제"
