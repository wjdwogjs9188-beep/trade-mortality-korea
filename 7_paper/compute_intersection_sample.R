# Standalone R script — 221 main ∩ 167 HIRA intersection sample + main spec 재산출
# ===================================================================================
# 본 script 는 paper § 7 mediator analysis 의 sample mismatch 영역의 substantive verify.
# main spec n=221 (1994 baseline + 1997-1999 ↔ 2018-2022 long-difference) 과
# HIRA mediator n=167 (sgguCdNm name-based crosswalk) 의 intersection 위에서
# main reduced-form Bartik 재산출 → selection bias direct verify.
#
# Output:
#   - intersection sigungu n
#   - β_intersection + HC1 SE + cluster SE + t + p
#   - β_intersection vs β_full (β = -0.127212) 비교 → selection bias 영역 평가
#   - paper § 7 entry paragraph 의 placeholder 채울 numerical values
#
# Usage:
#   setwd("C:/Users/82103/Downloads/trade_mortality_korea/7_paper")
#   source("compute_intersection_sample.R")
#
# Author: Claude (공동저자 mode, 2026-05-07)

PROJ <- "C:/Users/82103/Downloads/trade_mortality_korea"
DATA_PKG <- file.path(PROJ, "8_submission/paper_v01_submission")
HIRA_CW  <- file.path(PROJ, "1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv")

cat("[Stage 0] Environment\n")
suppressPackageStartupMessages({
  library(arrow); library(dplyr); library(tidyr); library(sandwich)
})

# ============================================================
# Stage 1 — Build main long-difference panel (n=221, despair)
# ============================================================
cat("\n[Stage 1] Build main long-difference panel\n")
mortality <- arrow::read_parquet(file.path(DATA_PKG, "01_mortality/sigungu_mortality_panel_v02_wa.parquet"))
iv_main   <- arrow::read_parquet(file.path(DATA_PKG, "02_bartik_iv/iv_z_x_bilateral.parquet"))

mortality$mort_rate <- mortality$deaths / pmax(mortality$pop_wa, 1)
mortality$log_mort  <- log(mortality$mort_rate + 1e-6)

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

panel <- build_panel_ld(mortality, 1997:1999, 2018:2022, iv_main)
panel_despair <- panel[panel$outcome_group == "despair_total", ]
panel_despair$z_x_std <- as.numeric(scale(panel_despair$z_x_per_worker))

main_h_codes <- unique(panel_despair$h_code)
cat(sprintf("  main sample: n = %d sigungu\n", length(main_h_codes)))

# ============================================================
# Stage 2 — HIRA crosswalk load + 167 mapped h_code list
# ============================================================
cat("\n[Stage 2] HIRA crosswalk load\n")
hira_cw <- read.csv(HIRA_CW, stringsAsFactors = FALSE, fileEncoding = "UTF-8")
cat(sprintf("  HIRA crosswalk rows: %d\n", nrow(hira_cw)))
cat(sprintf("  HIRA crosswalk columns: %s\n", paste(colnames(hira_cw), collapse = ", ")))

# h_code column 식별 (가능 한 column name: h_code, hcode, mapped_h_code 등)
hcode_col <- intersect(colnames(hira_cw), c("h_code", "hcode", "mapped_h_code", "matched_h_code"))[1]
if (is.na(hcode_col) || length(hcode_col) == 0) {
  cat("  ⚠️  h_code column not found by standard names. Inspecting first row:\n")
  cat(sprintf("    %s\n", paste(head(hira_cw, 1), collapse = " | ")))
  stop("Manual column identification needed — adjust hcode_col.")
}
cat(sprintf("  Using h_code column: '%s'\n", hcode_col))

hira_h_codes <- as.character(unique(hira_cw[[hcode_col]]))
hira_h_codes <- hira_h_codes[!is.na(hira_h_codes) & hira_h_codes != "" & hira_h_codes != "NA"]
cat(sprintf("  HIRA mapped h_codes: n = %d unique\n", length(hira_h_codes)))

# ============================================================
# Stage 3 — 221 main ∩ 167 HIRA intersection
# ============================================================
cat("\n[Stage 3] Intersection sample\n")
main_h_codes_str <- as.character(main_h_codes)
intersection_h_codes <- intersect(main_h_codes_str, hira_h_codes)
n_intersection <- length(intersection_h_codes)
n_only_main    <- length(setdiff(main_h_codes_str, hira_h_codes))
n_only_hira    <- length(setdiff(hira_h_codes, main_h_codes_str))

cat(sprintf("  Main only (in 221, NOT in HIRA): n = %d sigungu\n", n_only_main))
cat(sprintf("  HIRA only (in 167, NOT in 221 main): n = %d sigungu\n", n_only_hira))
cat(sprintf("  Intersection (221 ∩ 167): n = %d sigungu\n", n_intersection))
cat(sprintf("  Coverage: %d / %d = %.1f%% of main 221 sample retained in HIRA mediator analysis\n",
            n_intersection, length(main_h_codes_str), 100 * n_intersection / length(main_h_codes_str)))

# ============================================================
# Stage 4 — main spec 재산출 on intersection sample
# ============================================================
cat("\n[Stage 4] Main reduced-form Bartik on intersection sample\n")
panel_intersection <- panel_despair[as.character(panel_despair$h_code) %in% intersection_h_codes, ]
cat(sprintf("  panel_intersection rows: %d\n", nrow(panel_intersection)))

fit_int <- lm(d_log_asr ~ z_x_std, data = panel_intersection)
beta_int <- coef(fit_int)[2]

# HC1 SE
vcov_hc1 <- sandwich::vcovHC(fit_int, type = "HC1")
se_hc1   <- sqrt(diag(vcov_hc1))[2]
t_hc1    <- beta_int / se_hc1

# Cluster-province SE (G = number of unique sido)
cluster_id <- panel_intersection$sido_code
G <- length(unique(cluster_id))
N <- nrow(panel_intersection); K <- 2
X <- model.matrix(fit_int)
resid_int <- residuals(fit_int)
unique_clusters <- unique(cluster_id)
bread <- solve(crossprod(X)); meat <- matrix(0, K, K)
for (c in unique_clusters) {
  idx <- which(cluster_id == c)
  Xc <- X[idx, , drop = FALSE]; rc <- resid_int[idx]
  s_c <- crossprod(Xc, rc); meat <- meat + tcrossprod(s_c)
}
G_factor <- (G / (G - 1)) * ((N - 1) / (N - K))
vcov_cluster <- bread %*% meat %*% bread * G_factor
se_cluster <- sqrt(diag(vcov_cluster))[2]
t_cluster  <- beta_int / se_cluster

p_hc1     <- 2 * pt(-abs(t_hc1), df = N - K)
p_cluster <- 2 * pt(-abs(t_cluster), df = G - 1)

cat(sprintf("  β_intersection = %.6f\n", beta_int))
cat(sprintf("  HC1 SE = %.6f, t = %.4f, p ≈ %.4f\n", se_hc1, t_hc1, p_hc1))
cat(sprintf("  Cluster-province (G=%d) SE = %.6f, t = %.4f, p ≈ %.4f\n",
            G, se_cluster, t_cluster, p_cluster))

# ============================================================
# Stage 5 — Selection bias direct verify
# ============================================================
cat("\n[Stage 5] Selection bias direct verify (intersection vs full sample)\n")
# Full sample main spec (re-run for direct comparison)
fit_full <- lm(d_log_asr ~ z_x_std, data = panel_despair)
beta_full <- coef(fit_full)[2]
vcov_hc1_full <- sandwich::vcovHC(fit_full, type = "HC1")
se_hc1_full <- sqrt(diag(vcov_hc1_full))[2]

cat(sprintf("  Full sample (n=%d):     β = %.6f, HC1 SE = %.6f\n",
            nrow(panel_despair), beta_full, se_hc1_full))
cat(sprintf("  Intersection (n=%d):    β = %.6f, HC1 SE = %.6f\n",
            nrow(panel_intersection), beta_int, se_hc1))
cat(sprintf("  Δβ = β_int - β_full = %.6f\n", beta_int - beta_full))
cat(sprintf("  ratio β_int / β_full = %.4f\n", beta_int / beta_full))
cat(sprintf("  selection bias evidence: |Δβ| / SE_full = %.4f\n",
            abs(beta_int - beta_full) / se_hc1_full))

# ============================================================
# Stage 6 — sido distribution of main_only_53 (어느 시도 missing?)
# ============================================================
cat("\n[Stage 6] Missing sigungu sido distribution (main 221 - intersection)\n")
main_only <- setdiff(main_h_codes_str, hira_h_codes)
sido_dist <- table(substr(main_only, 1, 2))
sido_names <- c(
  "11" = "서울특별시", "21" = "부산광역시", "22" = "대구광역시", "23" = "인천광역시",
  "24" = "광주광역시", "25" = "대전광역시", "26" = "울산광역시", "29" = "세종특별자치시",
  "31" = "경기도",     "32" = "강원도",     "33" = "충청북도",   "34" = "충청남도",
  "35" = "전라북도",   "36" = "전라남도",   "37" = "경상북도",   "38" = "경상남도",
  "39" = "제주특별자치도"
)
cat(sprintf("  Missing sigungu (main 221 - intersection %d): n = %d\n",
            n_intersection, length(main_only)))
for (sd in names(sort(sido_dist, decreasing = TRUE))) {
  cat(sprintf("    %s (%s): %d sigungu\n",
              sd, sido_names[sd], sido_dist[sd]))
}

# ============================================================
# Stage 7 — Save intersection h_code list
# ============================================================
out_file <- file.path(PROJ, "1_codebooks/intersection_main_hira_h_codes.csv")
intersection_df <- data.frame(
  h_code = intersection_h_codes,
  in_main_221 = TRUE,
  in_hira_167 = TRUE
)
write.csv(intersection_df, out_file, row.names = FALSE, fileEncoding = "UTF-8")
cat(sprintf("\n[Stage 7] Saved intersection list: %s (n = %d)\n",
            out_file, n_intersection))

cat("\n=== Intersection sample + main spec 재산출 complete ===\n")
cat("Paper § 7 entry paragraph placeholder values:\n")
cat(sprintf("  n_intersection      = %d\n", nrow(panel_intersection)))
cat(sprintf("  β_intersection      = %.4f\n", beta_int))
cat(sprintf("  HC1 t_intersection  = %.2f\n", t_hc1))
cat(sprintf("  HC1 SE_intersection = %.4f\n", se_hc1))
cat(sprintf("  β_full vs β_int     = %.4f vs %.4f (Δ = %.4f)\n",
            beta_full, beta_int, beta_int - beta_full))
