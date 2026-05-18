"""
Phase 2-A — 2010 mortality panel build (single-year prototype).

Inputs:
- 0_raw/mortality_kostat/사망사료 정리/2010_사망_연간자료_B형_*.csv (cp949)
- 1_codebooks/sigungu_crosswalk.csv  (year × raw_code → h_code)
- 0_raw/kosis_population/population_combined.csv  (sigungu × sex × age × year → 인구)
- 1_codebooks/kosis_104_to_icd10.yaml  (outcome groups)

Output:
- 3_derived/mortality_panel_2010.parquet
- 3_derived/mortality_panel_2010.csv
- 3_derived/mortality_panel_2010_validation.md

Schema:
  h_code, year, outcome_group, age_5yr, sex, deaths, population, mortality_rate
"""
import sys
import io
from pathlib import Path
import pandas as pd
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parents[2]
RAW_MORT = ROOT / '0_raw' / 'mortality_kostat' / '사망사료 정리' / '2010_사망_연간자료_B형_20260410_98266.csv'
XW_PATH = ROOT / '1_codebooks' / 'sigungu_crosswalk.csv'
POP_PATH = ROOT / '0_raw' / 'kosis_population' / 'population_combined.csv'
YAML_PATH = ROOT / '1_codebooks' / 'kosis_104_to_icd10.yaml'
OUT_DIR = ROOT / '3_derived'
OUT_DIR.mkdir(exist_ok=True)

YEAR = 2010

# -------------------------------------------------------------------
# Mortality 5-year age code → KOSIS C3 age bin
# (verified from 파일설계서_1997 코드정보 sheet, rows 79-99)
#  1 = 0세,  2 = 1-4세,  3 = 5-9세,  4 = 10-14세,  5 = 15-19세,
#  6 = 20-24,  7 = 25-29,  8 = 30-34,  9 = 35-39,  10 = 40-44,
#  11 = 45-49,  12 = 50-54,  13 = 55-59,  14 = 60-64,  15 = 65-69,
#  16 = 70-74,  17 = 75-79,  18 = 80-84,  19 = 85-89,  20 = 90세이상,  99 = 미상
# Combine to KOSIS bins (bin 1+2 → 0-4; bin 18+19+20 → 80+)
# -------------------------------------------------------------------
MORT_AGE_TO_KOSIS = {
    '1':  '020',  # 0세 → KOSIS 0-4
    '2':  '020',  # 1-4 → KOSIS 0-4
    '3':  '050',
    '4':  '070',
    '5':  '100',
    '6':  '120',
    '7':  '130',
    '8':  '150',
    '9':  '160',
    '10': '180',
    '11': '190',
    '12': '210',
    '13': '230',
    '14': '260',
    '15': '280',
    '16': '310',
    '17': '330',
    '18': '340',  # 80-84 → 80+
    '19': '340',  # 85-89 → 80+
    '20': '340',  # 90+   → 80+
    '99': 'UNK',
}

# Outcome groups per CLAUDE.md / next_prompt.md
OUTCOMES = {
    'despair_total':  ['102', '101', '057', '081'],
    'cardiovascular': ['067', '068', '069', '070'],
    'cancer':         [f'{c:03d}' for c in range(27, 49)],
    'respiratory':    [f'{c:03d}' for c in range(73, 79)],
    'external_other': [f'{c:03d}' for c in list(range(97, 105)) if c != 102],
    'all_cause':      [f'{c:03d}' for c in range(1, 105)],   # 합계용
}


def load_mortality(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding='cp949', dtype=str)
    print(f'[mortality] read {len(df):,} rows')
    df['raw_code'] = df['사망자주소행정구역시도코드'].str.zfill(2) + \
                     df['사망자주소행정구역시군구코드'].str.zfill(3)
    df['age_kosis'] = df['사망연령5세단위코드'].map(MORT_AGE_TO_KOSIS)
    df['sex'] = df['성별코드']
    df['code104'] = df['사망원인_104항목분류코드']
    df['year'] = YEAR
    return df[['year', 'raw_code', 'age_kosis', 'sex', 'code104']]


def join_crosswalk(df: pd.DataFrame, xw: pd.DataFrame) -> pd.DataFrame:
    xw_y = xw[xw['year'].astype(int) == YEAR][['raw_code', 'h_code', 'h_name', 'sido_code', 'sido_name']]
    out = df.merge(xw_y, on='raw_code', how='left')
    miss = out['h_code'].isna().sum()
    print(f'[crosswalk] match {len(out) - miss:,}/{len(out):,}  ({(1 - miss/len(out))*100:.2f}%)')
    if miss:
        bad = out[out['h_code'].isna()]['raw_code'].value_counts().head(10)
        print('  unmatched sample:', bad.to_dict())
    return out


def explode_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for grp, codes in OUTCOMES.items():
        sub = df[df['code104'].isin(codes)].copy()
        sub['outcome_group'] = grp
        rows.append(sub)
    return pd.concat(rows, ignore_index=True)


def load_population(path: Path, xw: pd.DataFrame) -> pd.DataFrame:
    pop = pd.read_csv(path, dtype=str)
    pop = pop[pop['year'].astype(int) == YEAR].copy()
    pop['population'] = pop['population'].astype(float)
    print(f'[pop] {YEAR} rows: {len(pop):,}')

    # only keep 5-digit C1 (sigungu) rows that map via crosswalk
    pop = pop[pop['C1'].str.len() == 5]
    xw_y = xw[xw['year'].astype(int) == YEAR][['raw_code', 'h_code']]
    pop = pop.merge(xw_y, left_on='C1', right_on='raw_code', how='inner')
    print(f'[pop] after xw filter: {len(pop):,}')

    # only sex 1/2, age != '000' (drop totals)
    pop = pop[(pop['C2'].isin(['1', '2'])) & (pop['C3'] != '000')]

    # collapse 80+ alternate bins (340 = 80+; 360/380/410/430/440 are finer; 370 = 85+)
    # rule: if year has 340 use 340; if not, derive by summing 360+380+410+430+440 (or 340 + 370 etc.)
    # for 2010: 340 IS present → drop the finer 80+ alternates to avoid double counting
    drop_80_finer = ['360', '380', '410', '430', '440', '370']
    pop = pop[~pop['C3'].isin(drop_80_finer)].copy()

    pop = pop.rename(columns={'C2': 'sex', 'C3': 'age_kosis'})
    agg = pop.groupby(['h_code', 'sex', 'age_kosis'], as_index=False)['population'].sum()
    return agg


def main():
    print('=' * 70)
    print(f'Phase 2-A — mortality panel build for YEAR={YEAR}')
    print('=' * 70)

    xw = pd.read_csv(XW_PATH, dtype=str)
    print(f'[xw] {len(xw):,} rows, h_codes={xw["h_code"].nunique()}')

    mort = load_mortality(RAW_MORT)
    mort = join_crosswalk(mort, xw)

    # quick KOSTAT cross-check before further processing
    suicide_n = (mort['code104'] == '102').sum()
    print(f'[check] suicide (code 102) total: {suicide_n}  (expected 15566)')

    # outcome explode
    long = explode_outcomes(mort)
    print(f'[outcome] expanded rows: {len(long):,} (records can fall into multiple groups)')

    # drop rows with missing h_code or unknown age (separate count for unknown)
    drop_unk_age = (long['age_kosis'] == 'UNK').sum()
    print(f'[note] dropping {drop_unk_age:,} death records with unknown age (sex/age join not possible)')
    long = long[long['age_kosis'] != 'UNK'].copy()

    # death counts by (h_code, outcome, age_kosis, sex)
    deaths = long.groupby(
        ['h_code', 'outcome_group', 'age_kosis', 'sex'],
        as_index=False
    ).size().rename(columns={'size': 'deaths'})

    # population
    pop = load_population(POP_PATH, xw)
    print(f'[pop] aggregated to {len(pop):,} (h_code, sex, age) cells')

    # join
    panel = deaths.merge(pop, on=['h_code', 'sex', 'age_kosis'], how='left')
    panel['year'] = YEAR
    miss_pop = panel['population'].isna().sum()
    if miss_pop:
        print(f'[warn] {miss_pop} cells missing population — sample:')
        print(panel[panel['population'].isna()].head(10))

    # mortality rate per 100k
    panel['mortality_rate'] = panel['deaths'] / panel['population'] * 1e5

    # tidy + reorder
    panel = panel[['h_code', 'year', 'outcome_group', 'age_kosis', 'sex',
                   'deaths', 'population', 'mortality_rate']]
    panel = panel.sort_values(['outcome_group', 'h_code', 'sex', 'age_kosis']).reset_index(drop=True)

    # save
    out_pq = OUT_DIR / f'mortality_panel_{YEAR}.parquet'
    out_csv = OUT_DIR / f'mortality_panel_{YEAR}.csv'
    panel.to_parquet(out_pq, index=False)
    panel.to_csv(out_csv, index=False, encoding='utf-8-sig')
    print(f'[out] {out_pq}  ({len(panel):,} rows)')
    print(f'[out] {out_csv}')

    # ==================================================================
    # Validation
    # ==================================================================
    print('\n' + '=' * 70)
    print('VALIDATION')
    print('=' * 70)

    raw_total = len(mort)
    raw_known_age = (mort['age_kosis'] != 'UNK').sum()
    panel_dt = panel[panel['outcome_group'] == 'all_cause']['deaths'].sum()
    print(f'[V1] raw mortality records (with known age): {raw_known_age:,}')
    print(f'[V1] panel all_cause sum:                    {panel_dt:,.0f}')
    print(f'[V1] delta (should be 0):                    {raw_known_age - panel_dt:.0f}')

    # 102 자살 cross-check
    suicide_panel = panel[panel['outcome_group'] == 'despair_total']
    despair_sum = suicide_panel['deaths'].sum()
    suicide_only = (mort['code104'] == '102').sum()
    print(f'[V2] suicide (code 102) raw count:    {suicide_only}  (expected 15566)')
    print(f'[V2] despair_total panel sum (102+101+057+081): {despair_sum:.0f}')

    # National rate sanity
    nat_pop = pop['population'].sum()
    print(f'[V3] national pop (sum of disaggregated): {nat_pop:,.0f}')
    print(f'[V3] national suicide rate (per 100k):    {suicide_only / nat_pop * 1e5:.2f}')

    # Outcome breakdown
    print('\n[V4] outcome group breakdown (deaths):')
    print(panel.groupby('outcome_group')['deaths'].sum().to_string())

    # Save validation report
    rep = OUT_DIR / f'mortality_panel_{YEAR}_validation.md'
    with open(rep, 'w', encoding='utf-8') as f:
        f.write(f'# Phase 2-A — {YEAR} mortality panel validation\n\n')
        f.write(f'**Input**: `{RAW_MORT.name}` ({raw_total:,} raw rows)\n\n')
        f.write(f'**Output**: `mortality_panel_{YEAR}.parquet` ({len(panel):,} rows)\n\n')
        f.write('## V1 — death count conservation\n\n')
        f.write(f'- Raw records (known age): **{raw_known_age:,}**\n')
        f.write(f'- Panel `all_cause` sum:   **{panel_dt:,.0f}**\n')
        f.write(f'- Δ = **{raw_known_age - panel_dt:.0f}** (target: 0)\n')
        f.write(f'- Records dropped (unknown age): {drop_unk_age:,}\n\n')
        f.write('## V2 — KOSTAT 102 (suicide) cross-check\n\n')
        f.write('| metric | value | KOSTAT official |\n|---|---|---|\n')
        f.write(f'| Code 102 raw count | {suicide_only:,} | 15,566 |\n')
        f.write(f'| Match | {"100% PASS" if suicide_only == 15566 else "MISMATCH"} |  |\n\n')
        f.write('## V3 — national rate sanity\n\n')
        f.write(f'- Total disaggregated pop (KOSIS sum): {nat_pop:,.0f}\n')
        f.write(f'- National suicide rate per 100k: {suicide_only / nat_pop * 1e5:.2f}\n')
        f.write(f'- (KOSTAT 2010 공식 자살률 참고치: 31.2 per 100k. 본 panel은 5세-성별 disaggregated → top-down 비교는 주의.)\n\n')
        f.write('## V4 — outcome group totals\n\n')
        f.write('| outcome_group | deaths |\n|---|---|\n')
        for g, n in panel.groupby('outcome_group')['deaths'].sum().items():
            f.write(f'| {g} | {n:,.0f} |\n')
        f.write('\n## V5 — top-10 sigungu by all-cause deaths\n\n')
        ac = panel[panel['outcome_group'] == 'all_cause'].groupby('h_code')['deaths'].sum().sort_values(ascending=False).head(10)
        xw_names = xw[['h_code', 'h_name']].drop_duplicates().set_index('h_code')['h_name'].to_dict()
        f.write('| h_code | h_name | deaths |\n|---|---|---|\n')
        for h, n in ac.items():
            f.write(f'| {h} | {xw_names.get(h, "?")} | {n:,.0f} |\n')
        f.write('\n## V6 — schema head\n\n```\n')
        f.write(panel.head(20).to_string(index=False))
        f.write('\n```\n')
    print(f'\n[out] {rep}')


if __name__ == '__main__':
    main()
