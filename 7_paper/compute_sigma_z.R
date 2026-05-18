# Standalone R script — σ_z (sample SD of native z_x) 산출
# =========================================================
# 본 script 는 paper § 5.1 Footnote X 의 native unit interpretation 의 σ_z 값 산출 용도.
# run_robustness_native_v02.R 의 panel build 영역을 추출 + sd() 만 산출.
#
# Usage:
#   Rscript compute_sigma_z.R
#
# Output (stdout):
#   σ_z (native z_x sample SD) for the despair_total long-difference panel
#   β_native = β_standardized × σ_z 변환 결과

PROJ <- "C:/Users/82103/Downloads/trade_mortality_korea"
DATA_PKG <- file.path(PROJ, "8_submission/paper_v01_submission")

cat("[Stage 0] Environment\n")
suppressPackageStartupMessages({
  library(arrow); library(dplyr); library(tidyr)
})

cat("\n[Stage 1] Data load\n")
mortality <- arrow::read_parquet(file.path(DATA_PKG, "01_mortality/sigungu_mortality_panel_v02_wa.parquet"))
iv_main   <- arrow::read_parquet(file.path(DATA_PKG, "02_bartik_iv/iv_z_x_bilateral.parquet"))

mortality$mort_rate <- mortality$deaths / pmax(mortality$pop_wa, 1)
mortality$log_mort  <- log(mortality$mort_rate + 1e-6)

cat("  mortality rows:", nrow(mortality), "\n")
cat("  iv_main rows:  ", nrow(iv_main), "\n")

# Build long-difference panel (1997-1999 base, 2018-2022 endpoint, despair_total)
build_panel_ld <- function(mort, base_yrs, end_yrs, iv_z) {
  mb <- mort %>% filter(year %in% base_yrs) %>% group_by(h_code, outcome_group) %>%
    summarise(b = mean(log_mort, na.rm = TRUE), .groups = "drop")
  me <- mort %>% filter(year %in% end_yrs) %>% group_by(h_code, outcome_group) %>%
    summarise(e = mean(log_mort, na.rm = TRUE), .groups = "drop")
  p <- mb %>% inner_join(me, by = c("h_code", "outcome_group")) %>%
    mutate(d_log_asr = e - b) %>% inner_join(iv_z, by = "h_code")
  p$sido_code <- substr(as.character(p$h_code), 1, 2)
  finite_z <- is.finite(p$z_x)
  p <- p[finite_z, ]
  p
}

cat("\n[Stage 2] Build despair_total panel (1997-1999 ↔ 2018-2022)\n")
panel <- build_panel_ld(mortality, 1997:1999, 2018:2022, iv_main)
panel_despair <- panel[panel$outcome_group == "despair_total", ]

cat("  panel_despair rows (n_sigungu):", nrow(panel_despair), "\n")

# CRITICAL FIX: paper main spec uses z_x_per_worker (denominator-normalized) 정합
#   raw z_x 는 sigungu size confounding 때문에 spurious +0.235 correlation
#   z_x_per_worker = z_x / E_h_1994 가 paper main spec 의 IV
# σ_z 산출 — z_x_per_worker 위에서
sigma_z <- sd(panel_despair$z_x_per_worker)
cat("\n[Stage 3] σ_z (native z_x_per_worker sample SD)\n")
cat(sprintf("  σ_z = %.6f (USD per 1994 manufacturing worker)\n", sigma_z))
cat(sprintf("  β_native = β_standardized × σ_z = -0.127212 × %.6f = %.6f\n",
            sigma_z, -0.127212 * sigma_z))

# z_x_per_worker range + percentiles
cat("\n[Stage 4] z_x_per_worker distribution (USD per 1994 worker)\n")
cat(sprintf("  min:    %.4f\n", min(panel_despair$z_x_per_worker)))
cat(sprintf("  p25:    %.4f\n", quantile(panel_despair$z_x_per_worker, 0.25)))
cat(sprintf("  median: %.4f\n", median(panel_despair$z_x_per_worker)))
cat(sprintf("  mean:   %.4f\n", mean(panel_despair$z_x_per_worker)))
cat(sprintf("  p75:    %.4f\n", quantile(panel_despair$z_x_per_worker, 0.75)))
cat(sprintf("  max:    %.4f\n", max(panel_despair$z_x_per_worker)))
cat(sprintf("  IQR:    %.4f (p75 - p25)\n",
            quantile(panel_despair$z_x_per_worker, 0.75) - quantile(panel_despair$z_x_per_worker, 0.25)))

# HC1 SE for native β (extra: paper § 5.1 line 54 HC1 t verify)
cat("\n[Stage 5] HC1 SE for despair_total (paper § 5.1 line 54 HC1 t verify)\n")
# z_x_per_worker 위에서 standardize
panel_despair$z_x_std <- as.numeric(scale(panel_despair$z_x_per_worker))
fit <- lm(d_log_asr ~ z_x_std, data = panel_despair)
cat(sprintf("  cor(z_x_per_worker, d_log_asr) = %.4f\n",
            cor(panel_despair$z_x_per_worker, panel_despair$d_log_asr)))

if (requireNamespace("sandwich", quietly = TRUE)) {
  vcov_hc1 <- sandwich::vcovHC(fit, type = "HC1")
  se_hc1 <- sqrt(diag(vcov_hc1))[2]  # z_x_std coef
  beta_std <- coef(fit)[2]
  t_hc1 <- beta_std / se_hc1
  cat(sprintf("  β_standardized = %.6f\n", beta_std))
  cat(sprintf("  HC1 SE = %.6f\n", se_hc1))
  cat(sprintf("  HC1 t  = %.4f\n", t_hc1))
  cat(sprintf("  HC1 p (2-sided) ≈ %.4f\n", 2 * pt(-abs(t_hc1), df = nrow(panel_despair) - 2)))
} else {
  cat("  sandwich package not installed; install with: install.packages('sandwich')\n")
}

cat("\n=== σ_z + HC1 SE 산출 complete ===\n")
cat("  paper § 5.1 Footnote X 에 σ_z paste\n")
cat("  paper § 5.1 line 54 HC1 t native value paste\n")
