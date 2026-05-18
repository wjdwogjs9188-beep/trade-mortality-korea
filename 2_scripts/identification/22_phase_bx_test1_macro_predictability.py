"""
Phase B-x Test 1 — Romer-Romer style macro predictability.

PAP v4.0 § 2.2 spec:
  ΔM_t^{KR←CN} = α + Σ_j β_j · KR_macro_realized_{t-j} + γ·X + ε_t

H0: β_j = 0 ∀ j (모든 macro 변수)
p > 0.10 → bilateral shock 외생성 신호
p < 0.05 → bilateral validity 약화 → C.ii branch 진입 위험

Macro 변수 (모두 ECOS 보유):
  1. 200Y110 분기 GDP 성장률
  2. 402Y014 수출물가지수 총지수
  3. 401Y015 수입물가지수 총지수
  4. 901Y009 CPI
  5. 731Y004 KRW/USD 환율
  6. 722Y001 BoK 기준금리

bilateral shock = KR-CN bilateral imports + exports change (5-year stack 또는 분기)

산출:
  5_logs/integrity_checks/<date>_phase_bx_test1_results.md
  3_derived/identification/test1_macro_predictability.csv
"""
from __future__ import annotations
import sys, glob
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import RAW_DIR, DERIVED_DIR, LOGS_DIR

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ECOS_DIR = RAW_DIR / "ecos_macro_extra"
ECOS_BASE = RAW_DIR / "ecos_macro"
TRADE_DIR = RAW_DIR / "comtrade_korea_china"
OUT_DIR = DERIVED_DIR / "identification"
LOG = LOGS_DIR / "integrity_checks" / f"{datetime.now():%Y-%m-%d}_phase_bx_test1_results.md"


def load_ecos_series(stat_code: str, base_dir: Path = None) -> pd.DataFrame:
    """ECOS 시리즈 로드 — base + extra 둘 다 검색."""
    candidates = []
    for d in [base_dir or ECOS_BASE, ECOS_DIR]:
        if d.exists():
            candidates.extend(d.glob(f"{stat_code}_*.csv"))
    if not candidates:
        raise FileNotFoundError(f"ECOS {stat_code} 파일 없음")
    df = pd.read_csv(candidates[0], encoding='utf-8-sig')
    return df


def parse_period_column(df, period_col='TIME', cycle='Q'):
    """ECOS TIME 컬럼 → datetime."""
    df[period_col] = df[period_col].astype(str)
    if cycle == 'Q':
        # "2000Q1" → 2000-03-31
        df['date'] = pd.to_datetime(df[period_col].str.replace('Q', ''), format='%Y%m', errors='coerce')
    elif cycle == 'M':
        # "200001" → 2000-01-31
        df['date'] = pd.to_datetime(df[period_col], format='%Y%m', errors='coerce')
    elif cycle == 'A':
        df['date'] = pd.to_datetime(df[period_col], format='%Y', errors='coerce')
    return df


def aggregate_macro_yearly(df, value_col='DATA_VALUE', date_col='date'):
    """월·분기 → 연도 평균."""
    df['year'] = df[date_col].dt.year
    return df.groupby('year')[value_col].mean().reset_index()


def compute_log_change(df, value_col='DATA_VALUE', period=5):
    """N-period log change."""
    df = df.sort_values('year').copy()
    df[f'log_{value_col}'] = np.log(df[value_col].replace(0, np.nan))
    df[f'd{period}_log_{value_col}'] = df[f'log_{value_col}'].diff(period)
    return df


def aggregate_bilateral_yearly() -> pd.DataFrame:
    """KR-CN bilateral yearly aggregate (imports + exports)."""
    rows = []
    for f in sorted(TRADE_DIR.glob("KR_*_*.csv")):
        # Parse: KR_imp_from_CN_2000.csv 또는 KR_exp_to_CN_2000.csv
        parts = f.stem.split('_')
        if 'imp' in f.stem:
            direction = 'M'
        elif 'exp' in f.stem:
            direction = 'X'
        else:
            continue
        year = int(parts[-1])
        try:
            df = pd.read_csv(f, encoding='utf-8-sig', usecols=['primaryValue'], dtype={'primaryValue': float})
            total = df['primaryValue'].sum()
            rows.append({'year': year, 'direction': direction, 'value_usd': total})
        except Exception as e:
            print(f"  [skip] {f.name}: {e}")
    return pd.DataFrame(rows).pivot(index='year', columns='direction', values='value_usd').reset_index()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log = [f"# Phase B-x Test 1 — Macro predictability\n", f"_timestamp: {datetime.now().isoformat()}_\n\n"]

    # 1) bilateral shock 시계열
    print("[1] KR-CN bilateral 연도별 aggregate")
    bil = aggregate_bilateral_yearly()
    bil['net_X_M'] = bil.get('X', 0) - bil.get('M', 0)  # net export
    bil['total'] = bil.get('X', 0) + bil.get('M', 0)  # total trade
    bil['log_M'] = np.log(bil['M'].replace(0, np.nan))
    bil['log_X'] = np.log(bil['X'].replace(0, np.nan))
    bil['log_net'] = np.log(bil['total'].replace(0, np.nan))
    bil['d5_log_M'] = bil['log_M'].diff(5)
    bil['d5_log_X'] = bil['log_X'].diff(5)
    bil['d5_log_net'] = bil['log_net'].diff(5)
    print(f"  bilateral years: {bil['year'].min()} ~ {bil['year'].max()}, n={len(bil)}")
    log.append(f"## bilateral coverage\n- years {bil['year'].min()}-{bil['year'].max()}, n={len(bil)}\n\n")

    # 2) ECOS macro 변수 로드
    print("\n[2] ECOS macro 시리즈 로드")
    macro_specs = [
        ('200Y110', 'Q', '분기GDP_지출_실질'),
        ('402Y014', 'M', '수출물가지수'),
        ('401Y015', 'M', '수입물가지수'),
        ('901Y009', 'M', 'CPI'),
        ('731Y004', 'M', 'KRW_USD'),
        ('722Y001', 'M', 'BoK_rate'),
    ]
    macro_df = bil.copy()
    for stat, cycle, label in macro_specs:
        try:
            df = load_ecos_series(stat)
            df = parse_period_column(df, cycle=cycle)
            df = df[df[df.columns[df.columns.str.contains('TIME')][0]].notna()]
            yearly = aggregate_macro_yearly(df)
            yearly = yearly.rename(columns={'DATA_VALUE': f'macro_{label}'})
            yearly[f'log_macro_{label}'] = np.log(yearly[f'macro_{label}'].replace(0, np.nan))
            yearly[f'd5_log_macro_{label}'] = yearly[f'log_macro_{label}'].diff(5)
            macro_df = macro_df.merge(yearly, on='year', how='left')
            print(f"  ✅ {stat} ({label}): {len(yearly)} years")
        except Exception as e:
            print(f"  ❌ {stat} ({label}): {e}")
            log.append(f"- ❌ `{stat}` 로드 실패: {e}\n")

    # 3) Test 1 regression: bilateral d5_log_M ~ lagged macro changes
    print("\n[3] Test 1 회귀 — bilateral_M_change ~ lagged macro changes")
    macro_cols = [c for c in macro_df.columns if c.startswith('d5_log_macro_')]
    valid_cols = [c for c in macro_cols if macro_df[c].notna().sum() > 5]

    # lagged 1-period (5-year)
    for c in valid_cols:
        macro_df[f'{c}_lag1'] = macro_df[c].shift(1)

    # Y = d5_log_M (bilateral imports change)
    y_var = 'd5_log_M'
    x_vars = [f'{c}_lag1' for c in valid_cols]

    # OLS
    reg_data = macro_df[[y_var] + x_vars].dropna()
    print(f"  obs after dropna: {len(reg_data)}")

    if len(reg_data) < 5:
        print("  ⚠️ obs 부족 — bilateral 1995-1999 추가 호출 후 재시도 권장")
        log.append(f"\n## Test 1 ⚠️ obs 부족\n- regression obs: {len(reg_data)}\n")
        log.append(f"- 권장: Comtrade 1995-1999 추가 호출 (run_comtrade_pre_wto.ps1)\n")
    else:
        import statsmodels.api as sm
        X = sm.add_constant(reg_data[x_vars])
        y = reg_data[y_var]
        model = sm.OLS(y, X).fit(cov_type='HC1')
        print(model.summary())

        # F-test (joint significance)
        from scipy import stats as sp_stats
        # H0: 모든 lagged macro β = 0
        f_test = model.f_test(x_vars)
        print(f"\n  Joint F-test (H0: all lagged macro = 0)")
        print(f"  F = {f_test.fvalue:.3f}, p = {f_test.pvalue:.4f}")

        log.append(f"\n## Test 1 — bilateral M change ~ lagged macro\n\n")
        log.append(f"- obs: {len(reg_data)}\n")
        log.append(f"- macro variables: {x_vars}\n")
        log.append(f"- **Joint F-stat**: {f_test.fvalue:.3f}\n")
        log.append(f"- **Joint p-value**: {f_test.pvalue:.4f}\n")
        log.append(f"- **결정**:\n")
        if f_test.pvalue > 0.10:
            log.append(f"  - p > 0.10 → **bilateral shock 가 lagged macro 로 예측 *안 됨*** → 외생성 신호 ✅\n")
        elif f_test.pvalue > 0.05:
            log.append(f"  - 0.05 < p < 0.10 → borderline. 추가 검정 필요\n")
        else:
            log.append(f"  - p < 0.05 → **bilateral 외생성 의심** → C.ii branch 진입 위험\n")

        # 결과 csv
        coef_df = pd.DataFrame({
            'variable': model.params.index,
            'coef': model.params.values,
            'se': model.bse.values,
            'p': model.pvalues.values,
        })
        out_csv = OUT_DIR / 'test1_macro_predictability.csv'
        coef_df.to_csv(out_csv, index=False)
        print(f"\n[saved] {out_csv}")

    LOG.write_text("".join(log), encoding="utf-8")
    print(f"[log] {LOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
