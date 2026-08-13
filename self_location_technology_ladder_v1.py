"""Canevas — full-history technology-ladder self-location test v1.

Purpose
-------
Quantify how concentrated human births are after a set of independently chosen
historical information/technology milestones. This does NOT say that a person
born after a milestone personally had access to it; it only characterizes the
historical environment into which births occurred.

Methodological guardrails
-------------------------
- Milestone dates are declared here before looking at the output.
- No milestone is selected afterward because it makes 1992 look special.
- Ancient cumulative births are estimated only from coarse PRB benchmark totals.
- Post-1950 annual births use UN WPP 2024 via Our World in Data.
- This is a self-location diagnostic, not evidence for Canevas by itself.
"""
import pandas as pd
import numpy as np

BIRTH_YEAR=1992
PRB_TOTAL_2022=117_020_448_575

# PRB 2022 cumulative-ever-born benchmarks. Negative years are BCE.
PRB=np.array([
    [-50000, 7_856_100_002],
    [-8000, 8_993_889_771],
    [1, 55_019_222_125],
    [1200, 81_610_565_125],
    [1650, 94_392_567_578],
    [1750, 97_564_499_091],
    [1850, 101_610_739_100],
    [1900, 104_510_976_956],
    [1950, 107_901_175_171],
],dtype=float)

# Independently chosen historical milestones. Dates are approximate and serve as
# sensitivity landmarks, not claims of a unique boundary of 'technology'.
MILESTONES=[
    ('writing', -3200, 'earliest known writing systems, approximate'),
    ('printing_press', 1450, 'European movable-type printing, approximate'),
    ('scientific_revolution', 1543, 'Copernicus publication landmark'),
    ('electric_power_age', 1882, 'early commercial central electric power landmark'),
    ('electronic_computing', 1945, 'general-purpose electronic computing era landmark'),
    ('world_wide_web', 1991, 'public Web era landmark'),
    ('conversational_genAI', 2022, 'mass public conversational generative-AI era landmark'),
]

URL='https://ourworldindata.org/grapher/annual-number-of-births-by-world-region.csv?v=1&csvType=full&useColumnShortNames=true'

def load_births():
    df=pd.read_csv(URL,storage_options={'User-Agent':'Mozilla/5.0'})
    # normalize schema
    lower={str(c).lower():c for c in df.columns}
    ycol=lower.get('year')
    ecol=lower.get('entity')
    if ycol is None: raise RuntimeError(f'No year column. Columns={list(df.columns)}')
    if ecol is not None:
        w=df[df[ecol].astype(str).str.lower().eq('world')].copy()
        if not w.empty: df=w
    meta={c for k,c in lower.items() if k in ('entity','code','year')}
    candidates=[]
    for c in df.columns:
        if c in meta: continue
        s=pd.to_numeric(df[c],errors='coerce')
        if s.notna().sum()>=10: candidates.append((c,s))
    chosen=None
    for c,s in candidates:
        if 'birth' in str(c).lower(): chosen=(c,s); break
    if chosen is None and candidates: chosen=candidates[0]
    if chosen is None: raise RuntimeError('No births column found.')
    c,s=chosen
    out=pd.DataFrame({'year':pd.to_numeric(df[ycol],errors='coerce'),'births':s}).dropna()
    out['year']=out['year'].astype(int); out['births']=out['births'].astype(float)
    out=out.groupby('year',as_index=False).births.sum()
    return out,c

def ancient_cumulative(year):
    """Coarse interpolation between PRB cumulative benchmarks.

    Linear interpolation in cumulative births is intentionally simple. We also
    report that these ancient estimates are low precision; the test is about
    orders of magnitude, not exact dates.
    """
    xs=PRB[:,0]; ys=PRB[:,1]
    if year<=xs[0]: return ys[0]
    if year>=xs[-1]: return ys[-1]
    return float(np.interp(year,xs,ys))

def cumulative_at(year,births):
    if year<1950:
        return ancient_cumulative(year)
    base=107_901_175_171.0
    add=births[(births.year>=1950)&(births.year<year)].births.sum()
    return base+float(add)

def main():
    births,col=load_births()
    if BIRTH_YEAR not in set(births.year): raise RuntimeError('1992 unavailable in births data.')
    print('='*78)
    print(' CANEVAS SELF-LOCATION — FULL-HISTORY TECHNOLOGY LADDER v1')
    print('='*78)
    print(f'Birth year = {BIRTH_YEAR}')
    print(f'Birth source = UN WPP 2024 via OWID; data column = {col}')
    print(f'PRB estimated total births through 2022 = {PRB_TOTAL_2022:,}\n')

    print('MILESTONE RESULTS:')
    rows=[]
    for name,year,note in MILESTONES:
        cum=cumulative_at(year,births)
        after=max(PRB_TOTAL_2022-cum,0.0)
        share=after/PRB_TOTAL_2022
        born_after=BIRTH_YEAR>=year
        rows.append((name,year,share,born_after))
        ys=f'{abs(year)} BCE' if year<0 else str(year)
        print(f'{name:24s} {ys:>9s}  share of all births AFTER milestone = {share:9.6f}  1992-after? {born_after}')
        print(f'  note: {note}')

    # Position of 1992 within each milestone-defined post-milestone birth class,
    # only where 1992 occurs after the milestone.
    cum1992=cumulative_at(BIRTH_YEAR,births)+0.5*float(births.loc[births.year==BIRTH_YEAR,'births'].iloc[0])
    print('\n1992 POSITION WITHIN ELIGIBLE POST-MILESTONE BIRTH CLASSES:')
    for name,year,share,born_after in rows:
        if not born_after:
            print(f'{name:24s} not applicable: 1992 precedes milestone')
            continue
        start=cumulative_at(year,births)
        denom=PRB_TOTAL_2022-start
        p=(cum1992-start)/denom if denom>0 else np.nan
        print(f'{name:24s} percentile of 1992 within births after milestone = {p:.6f}')

    print('\nINTERPRETATION LOCK:')
    print('- A tiny post-milestone birth share means that environment is historically recent among all births.')
    print('- It does NOT imply that a 1992 person personally had access to that technology at birth.')
    print('- If conditioning on a milestone makes 1992 ordinary, that supports a selection-effect explanation.')
    print('- Ancient milestone shares are coarse because PRB prehistoric/historical totals are reconstructed.')
    print('- These milestones do not define a unique reference class and are not derived from Canevas axioms.')
    print('- No milestone may be declared the preferred one after seeing which result looks most striking.')
    print('\nFINISHED TECHNOLOGY LADDER v1')

if __name__=='__main__': main()
