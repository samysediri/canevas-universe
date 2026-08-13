"""Canevas — O1 full-history self-location test v1.3."""
import pandas as pd

BIRTH_YEAR=1992
WINDOW=5
PRB_EVER_1950=107_901_175_171
PRB_EVER_2022=117_020_448_575
PRB_START_YEAR=-190000
URL="https://ourworldindata.org/grapher/annual-number-of-births-by-world-region.csv?v=1&csvType=full&useColumnShortNames=true"

def load_births():
    try:
        df=pd.read_csv(URL,storage_options={'User-Agent':'Mozilla/5.0'})
    except Exception as e:
        raise RuntimeError(f'Could not download OWID/UN births data: {e}')

    # Normalize schema names because OWID exports may use Entity/Year or entity/year.
    lower={str(c).lower():c for c in df.columns}
    entity_col=lower.get('entity')
    year_col=lower.get('year')
    code_col=lower.get('code')

    if entity_col is not None:
        world=df[df[entity_col].astype(str).str.lower().eq('world')].copy()
        if not world.empty:
            df=world

    if year_col is None:
        raise RuntimeError(f'No year column found. Columns={list(df.columns)}')

    meta={c for c in (entity_col,code_col,year_col) if c is not None}
    candidates=[]
    for c in df.columns:
        if c in meta:
            continue
        s=pd.to_numeric(df[c],errors='coerce')
        if s.notna().sum()>=10:
            candidates.append((c,s))
    if not candidates:
        raise RuntimeError(f'No numeric births column found. Columns={list(df.columns)}')

    chosen=None
    for c,s in candidates:
        if 'birth' in str(c).lower():
            chosen=(c,s); break
    if chosen is None:
        chosen=candidates[0]
    col,series=chosen

    out=pd.DataFrame({'Year':pd.to_numeric(df[year_col],errors='coerce'),'births':series}).dropna()
    out['Year']=out['Year'].astype(int)
    out['births']=out['births'].astype(float)
    out=out.groupby('Year',as_index=False)['births'].sum()

    years=set(out.Year)
    if 1950 not in years or BIRTH_YEAR not in years:
        raise RuntimeError(f'Required years missing from OWID data. Range={out.Year.min()}..{out.Year.max()}, column={col}')
    return out,col

def main():
    d,col=load_births(); d=d[(d.Year>=1950)&(d.Year<=2022)].copy()
    births_before=d[d.Year<BIRTH_YEAR].births.sum()
    births_year=float(d.loc[d.Year==BIRTH_YEAR,'births'].iloc[0])
    rank_mid=PRB_EVER_1950+births_before+0.5*births_year
    percentile=rank_mid/PRB_EVER_2022
    later=1-percentile
    lo=BIRTH_YEAR-WINDOW; hi=BIRTH_YEAR+WINDOW
    pwin=d[(d.Year>=lo)&(d.Year<=hi)].births.sum()/PRB_EVER_2022
    post1950=d.births.sum()/PRB_EVER_2022
    post1990=d[d.Year>=1990].births.sum()/PRB_EVER_2022
    span=2022-PRB_START_YEAR+1
    cal=(2*WINDOW+1)/span
    print('='*72)
    print(' CANEVAS SELF-LOCATION O1 — FULL HOMO SAPIENS HISTORY v1.3')
    print('='*72)
    print(f'Observed birth year = {BIRTH_YEAR}')
    print(f'Source = UN WPP 2024 via Our World in Data; data column = {col}')
    print(f'PRB cumulative ever born by 1950 = {PRB_EVER_1950:,}')
    print(f'PRB cumulative ever born by 2022 = {PRB_EVER_2022:,}')
    print(f'UN/OWID births in {BIRTH_YEAR} = {births_year:,.0f}')
    print('\nBIRTH-RANK RESULT:')
    print(f'approx cumulative rank at middle of {BIRTH_YEAR} = {rank_mid:,.0f}')
    print(f'percentile among all births through 2022 = {percentile:.6f}')
    print(f'fraction of all births AFTER mid-{BIRTH_YEAR} = {later:.6f}')
    print('\nWINDOW RESULT:')
    print(f'share of all Homo-sapiens births in {lo}-{hi} = {pwin:.6f}')
    print(f'share of all births in 1950-2022 = {post1950:.6f}')
    print(f'share of all births in 1990-2022 = {post1990:.6f}')
    print('\nCALENDAR-TIME STRAW MODEL:')
    print(f'share of ~190,000 BCE..2022 calendar years in {lo}-{hi} = {cal:.8f}')
    print('This calendar-time number is NOT a serious self-location probability.')
    print('\nINTERPRETATION LOCK:')
    print('- High birth-rank percentile means 1992 is late among estimated human births.')
    print('- It does NOT by itself imply an anomaly; populous eras contain more births.')
    print('- Prehistoric cumulative births are highly uncertain; PRB is an order-of-magnitude reconstruction.')
    print('- Technology remains a separate conditioning problem.')
    print('- No SSA/SIA/reference-class rule is derived here.')
    print('\nFINISHED O1 FULL-HISTORY v1.3')

if __name__=='__main__': main()
