"""Canevas — O1 full-history self-location test v1.

Goal
----
Estimate how late a 1992 birth lies among *all Homo sapiens births*, using:
- PRB cumulative-ever-born benchmark at 1950 and 2022;
- annual UN/OWID world births for 1950 onward.

This avoids inventing annual prehistoric precision. The prehistoric contribution
enters only through PRB's cumulative benchmark, whose uncertainty is explicitly
reported in the interpretation.

This is a self-location diagnostic, not evidence for Canevas by itself.
"""
import io
import urllib.request
import pandas as pd

BIRTH_YEAR = 1992
WINDOW = 5

# PRB 2022 table, "How Many People Have Ever Lived on Earth?"
PRB_EVER_1950 = 107_901_175_171
PRB_EVER_2022 = 117_020_448_575
PRB_START_YEAR = -190000  # approximate modern-Homo-sapiens benchmark used by PRB

# OWID grapher: annual births, UN WPP. The script discovers the numeric column.
URLS = [
    "https://ourworldindata.org/grapher/births.csv?tab=table&country=~OWID_WRL",
    "https://ourworldindata.org/grapher/annual-number-of-births-by-world-region.csv?country=~OWID_WRL",
]

def load_births():
    last=None
    for url in URLS:
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                raw=r.read()
            df=pd.read_csv(io.BytesIO(raw))
            if 'Entity' in df.columns:
                df=df[df['Entity'].astype(str).str.lower().eq('world')]
            nums=[c for c in df.columns if c not in ('Entity','Code','Year')]
            if not nums: continue
            col=nums[0]
            out=df[['Year',col]].dropna().rename(columns={col:'births'})
            out['Year']=out['Year'].astype(int)
            out['births']=out['births'].astype(float)
            if 1950 in set(out.Year) and BIRTH_YEAR in set(out.Year): return out, url
        except Exception as e: last=e
    raise RuntimeError(f'Could not download OWID/UN births data: {last}')

def main():
    df,url=load_births()
    # Use 1950..2022 so denominator matches PRB's 2022 total.
    d=df[(df.Year>=1950)&(df.Year<=2022)].copy()
    if BIRTH_YEAR not in set(d.Year): raise RuntimeError('Birth year unavailable.')

    # Anchor PRB cumulative at the start of 1950. Add annual UN births through year.
    births_1950_to_before = d[d.Year < BIRTH_YEAR].births.sum()
    births_in_year = float(d.loc[d.Year==BIRTH_YEAR,'births'].iloc[0])
    # Mid-year rank is a less arbitrary point estimate than beginning/end of year.
    rank_mid = PRB_EVER_1950 + births_1950_to_before + 0.5*births_in_year
    percentile = rank_mid / PRB_EVER_2022
    later_fraction = 1-percentile

    lo=BIRTH_YEAR-WINDOW; hi=BIRTH_YEAR+WINDOW
    window_births=d[(d.Year>=lo)&(d.Year<=hi)].births.sum()
    p_window_all=window_births/PRB_EVER_2022

    post1950_births=d.births.sum()
    post1950_share=post1950_births/PRB_EVER_2022
    post1990_births=d[d.Year>=1990].births.sum()
    post1990_share=post1990_births/PRB_EVER_2022

    # Calendar-time straw comparison only: exact years are not a meaningful
    # observer measure, but it quantifies the naive "tiny slice of species age" intuition.
    span_years=2022-PRB_START_YEAR+1
    calendar_window_share=(2*WINDOW+1)/span_years

    print('='*72)
    print(' CANEVAS SELF-LOCATION O1 — FULL HOMO SAPIENS HISTORY v1')
    print('='*72)
    print('Observed birth year:',BIRTH_YEAR)
    print('Annual-birth source:',url)
    print(f'PRB cumulative ever born by 1950 = {PRB_EVER_1950:,}')
    print(f'PRB cumulative ever born by 2022 = {PRB_EVER_2022:,}')
    print(f'UN/OWID births in {BIRTH_YEAR} = {births_in_year:,.0f}')
    print()
    print('BIRTH-RANK RESULT (main result):')
    print(f'approx cumulative rank at middle of {BIRTH_YEAR} = {rank_mid:,.0f}')
    print(f'percentile among all births through 2022 = {percentile:.6f}')
    print(f'fraction of all births occurring AFTER mid-{BIRTH_YEAR} = {later_fraction:.6f}')
    print()
    print('WINDOW RESULT:')
    print(f'share of all Homo-sapiens births in {lo}-{hi} = {p_window_all:.6f}')
    print(f'share of all births in 1950-2022 = {post1950_share:.6f}')
    print(f'share of all births in 1990-2022 = {post1990_share:.6f}')
    print()
    print('CALENDAR-TIME STRAW MODEL:')
    print(f'share of ~190,000 BCE..2022 calendar years in the {lo}-{hi} window = {calendar_window_share:.8f}')
    print('This calendar-time number is NOT a serious self-location probability.')
    print()
    print('INTERPRETATION LOCK:')
    print('- If birth-rank percentile is high, a 1992 birth is genuinely late among human births.')
    print('- That does NOT by itself make it anomalous: birth sampling naturally weights populous eras.')
    print('- Exact prehistory is highly uncertain; PRB calls its 117-billion estimate semi-scientific.')
    print('- Technology is a separate conditioning problem and is NOT inferred from these birth counts.')
    print('- No self-location rule (SSA/SIA/reference class) is derived here.')
    print()
    print('FINISHED O1 FULL-HISTORY v1')

if __name__=='__main__': main()
