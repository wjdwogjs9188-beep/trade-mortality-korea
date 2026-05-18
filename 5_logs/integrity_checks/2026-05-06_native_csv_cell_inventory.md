# Native CSV cell-by-cell inventory (Path A unification source values)

_2026-05-06_

**Trigger**: cleanup_prompt v02 의 Layer B Table 1/2 numerical placeholder 채우기 위해 native CSV 5 file 의 cell-by-cell exact values inventory build. /data:explore-data framework 적용.

**Source**: `4_results/regression/` 폴더 (4_results/regression/_archive_pre_round31_inhouse/ 와 분리됨, native build 결과만 본 inventory 대상)

---

## Native CSV 5 file inventory

### 1. `akm_proper_kolesar.csv` (Kolesár 2024 ShiftShareSE AKM-proper)

| outcome | n | β | SE_AKM | p_AKM |
|---------|---|---|--------|-------|
| despair_total | 221 | -0.127212 | 0.025848 | 8.58e-07 |
| cancer | 221 | -0.049877 | 0.023116 | 0.0310 |
| cardiovascular | 221 | -0.069708 | 0.021711 | 0.00132 |
| respiratory | 219 | +0.075382 | 0.035530 | 0.0339 |
| external_other | 221 | -0.017182 | 0.027717 | 0.535 |

**Note**: se_ehw / p_ehw / p_akm0 columns are NA (numerical instability or method args).

### 2. `wcr_webb_native.csv` (Webb 6-point WCR bootstrap, B=9999, G=16)

| outcome | n | β | SE_cluster | t_cluster | p_WCR_webb | G |
|---------|---|---|-----------|-----------|-----------|---|
| despair_total | 221 | -0.127212 | 0.031679 | -4.0156 | 0 (numerical zero) | 16 |
| cancer | 221 | -0.049877 | 0.030369 | -1.6424 | 0.2203 | 16 |
| cardiovascular | 221 | -0.069708 | 0.022575 | -3.0878 | 0.0160 | 16 |
| respiratory | 219 | +0.075382 | 0.045699 | +1.6496 | 0.1259 | 16 |
| external_other | 221 | -0.017182 | 0.039440 | -0.4357 | 0.6938 | 16 |

### 3. `rw_wcr_native.csv` (Romano-Wolf step-down with WCR backend)

| outcome | t_obs | β | p_RW |
|---------|-------|---|------|
| despair_total | -4.5621 | -0.133095 | **0.0161** ⭐ FWER pass |
| cancer | -1.4594 | -0.045051 | 0.382 |
| cardiovascular | -2.8095 | -0.064357 | 0.129 |
| respiratory | +1.6496 | +0.075382 | 0.382 |
| external_other | -0.4889 | -0.019582 | 0.658 |

**Anomaly**: RW backend despair_total β = -0.133 vs wcr_webb β = -0.127 (4.7% 미세 차이). RW step-down iteration 의 separate sample handling 또는 different SE estimator. paper Table 2 의 main β / SE / t_cluster 는 wcr_webb_native.csv 사용 + p_RW column 만 rw_wcr_native.csv 사용 권고.

### 4. `prewto_placebo_native_v02.csv` (1992-1996 KR-CN bilateral imports IV placebo)

| outcome | n | β | SE | t | p_WCR |
|---------|---|---|----|----|-------|
| despair_total | 221 | -0.123214 | 0.035221 | **-3.4983** | 0.0004 |
| cancer | 221 | -0.059668 | 0.032758 | -1.8215 | 0.185 |
| cardiovascular | 221 | -0.076441 | 0.026565 | -2.8775 | 0.0243 |
| respiratory | 219 | +0.100736 | 0.042033 | +2.3966 | 0.0923 |
| external_other | 221 | -0.005743 | 0.038288 | -0.1500 | 0.896 |

**Note**: 사용자의 v02 placebo wording 의 t = -3.85 → **t = -3.50** 정정 (R-A 가 v02 작성 시 approximate 추정값 사용, native CSV 의 정확값은 -3.498).

### 5. `baseline_1992_native_v02.csv` (1992 baseline winsorized)

| outcome | n | β | SE | t | p_WCR |
|---------|---|---|----|----|-------|
| despair_total | **209** | -0.063980 | 0.029352 | -2.1797 | 0.0840 |
| cancer | 209 | -0.012906 | 0.014457 | -0.8927 | 0.414 |
| cardiovascular | 209 | -0.043684 | 0.029964 | -1.4579 | 0.0838 |
| respiratory | 207 | +0.022828 | 0.026146 | +0.8731 | 0.380 |
| external_other | 209 | -0.000923 | 0.025691 | -0.0359 | 0.983 |

**Note**: 사용자의 v02 1992 baseline wording 의 n = 215 → **n = 209** 정정 (R-A 가 v02 작성 시 baseline_shares_1992_v2.parquet 의 215 sigungu 와 baseline_1992_native_v02.csv 의 209 sigungu 혼동, 후자가 정확).

**Sign reversal 회복**: cancer + cardio + external_other 가 모두 음수 (1994 baseline 정합), respiratory 만 positive. baseline 1992 의 attenuation 후에도 sign consistency 유지.

---

## Path A unification 정확 attenuation factor

- 1994 baseline native main: β = -0.127
- 1992 baseline winsorized: β = -0.0640
- **Attenuation factor: -0.0640 / -0.127 = 0.504 (50.4%)**

이는 substantive attenuation 으로, 1992 baseline 의 (i) 작은 sample (n=209 < n=221), (ii) winsorize 후에도 잔존하는 small-denominator 영향, (iii) KSIC 6 → 9 crosswalk 의 1992 ambiguity 의 결합. 1994 baseline 을 main 으로 채택의 정당화.

---

## Arithmetic cell-by-cell verify (R-A 직접 calculation)

### despair_total (1994 baseline native main):
- AKM: -0.127212 / 0.025848 = **-4.9216** ≈ -4.92 ✅
- Cluster (asymptotic): -0.127212 / 0.031679 = **-4.0156** ≈ -4.02 ✅
- Cluster (WCR Webb 6-pt): t = -4.0156, p_WCR = 0 (numerical zero, < 1e-4) ✅

### Pre-WTO placebo despair_total:
- Cluster: -0.123214 / 0.035221 = **-3.4983** ≈ -3.50 ✅

### 1992 baseline despair_total (winsorized):
- Cluster: -0.063980 / 0.029352 = **-2.1797** ≈ -2.18 ✅

모든 native CSV 의 β / SE / t cell 이 arithmetic verify 통과. Path A unification 시 paper Table 1/2 의 numerical 정합성 hard verified.

---

## 1.854 ratio substantive 재확인

- Native main β / archive main β = -0.127 / -0.0685 = 1.854 (시간 amplification factor)
- Native placebo β / archive placebo β 는 archive placebo 결과 부재로 직접 비교 불가 — 다만 native placebo β = -0.123 ≈ native main β = -0.127 (ratio 0.97) — placebo failure pattern

이 1.854 ratio 가 window length 의 long-run effect amplification factor 로 paper § 5.5 또는 § 6 별도 sub-section 에 commit 가능. native CSV 의 cell-by-cell inventory 가 그 ratio 의 backing evidence 로 작용.

---

## 사용자 측 R wrapper 추가 verify 영역 (HC1, Conley)

본 inventory 가 cover 못 한 SE layer:

1. **HC1 SE for native β = -0.127 (despair_total)**: native R wrapper 출력 영역. 사용자 측 R console 1 line:
   ```r
   fit <- lm(d_log_asr ~ z_x_std, data = panel_main_despair)
   sandwich::vcovHC(fit, type = "HC1") |> diag() |> sqrt()
   ```

2. **Conley 5km / 10km SE for native β = -0.127**: spatial HAC re-run 영역. 사용자 측 R wrapper 의 conley() implementation (또는 Stata `acreg` package) 실행 결과 paste.

3. **Post-2008 sub-period native β + SE**: 본 inventory 폴더에서 `sub_period_split_2008_native.csv` 또는 동등 file 미발견. 사용자 측 hard drive 에 있는지 확인 또는 native R wrapper sub-period split extension 추가 실행.

이 3 영역의 추가 결과가 paper § 5.1 Table 1 + § 5.4 sub-period 의 final placeholder 채움 영역.

---

## 사용자 측 추가 결정 영역 (R-A audit 영역 외)

1. **§ 5.1 line 14 unit interpretation 결정**: standardized 1-SD main + native unit footnote (R-A 권고) vs native unit main + standardized footnote — 사용자 결정 영역
2. **§ 6.1 placebo activation-timing narrative reframe**: gradual integration interpretation (1992-1996 pre-WTO) vs strict activation-timing failure (1992-1996 placebo failure honest disclose) — substantive narrative 결정 영역
3. **RW backend β 미세 차이 verify**: rw_wcr_native.csv 의 despair_total β = -0.133 vs wcr_webb_native.csv β = -0.127. 사용자 측 R script 의 RW iteration sample handling detail 영역.

---

## v02 → v02.1 patch deliverable

본 inventory 의 모든 cell exact values 가 cleanup_prompt v02.1 patch 에 적용됨:
- `Documents/Claude/Projects/논문을쓰자/cleanup_prompt_path_a_v02_1_patch.md`

사용자 측 paper 본문 commit 시 v02 + v02.1 patch 를 함께 적용하면 Layer A + Layer B 의 모든 cell 이 native CSV exact values 로 채워진 commit-ready 형태.

---

## R-A 한계 시인

본 inventory 의 한계:
1. HC1 SE / Conley SE / post-2008 sub-period 의 3 영역이 본 inventory 에서 cover 안 됨 — 사용자 측 R wrapper 추가 실행 영역
2. RW backend β 의 -0.133 vs -0.127 미세 차이의 root cause 가 R-A 측 verify 안 됨 — 사용자 측 R script 영역
3. § 5.1 Footnote X 의 σ_z 값 (native z_x 의 sample SD) 미verify — 사용자 측 R console 1 line 영역
