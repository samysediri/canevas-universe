"""SELF-LOCATION D1 — finite human birth-distribution test.

Uses PRB historical cumulative births + UN WPP 2024 annual births via OWID through
2100, then applies preregistered post-2100 tail scenarios. This is a sensitivity
analysis of birth-rank typicality, NOT an extinction forecast and NOT a Canevas test.
"""
from __future__ import annotations
import math
import pandas as pd
import numpy as np

BIRTH_YEAR=1992
PRB_EVER_1950=107_901_175_171
PRB_EVER_2022=117_020_448_575
URL="https://ourworldindata.org/grapher/annual-number-of-births-by-world-region.csv?v=1&csvType=full&useColumnShortNames=true"

TAILS=[
    ('EXTINCTION_2100','zero',None),
    ('EXP_DECAY_5PCT','exp',0.05),
    ('EXP_DECAY_2PCT','exp',0.02),
    ('EXP_DECAY_1PCT','exp',0.01),
    ('EXP_DECAY_0P5PCT','exp',0.005),
    ('EXP_DECAY_0P25PCT','exp',0.0025),
    ('PLATEAU_1000Y','plateau',1000),
    ('PLATEAU_10000Y','plateau',10000),
    ('INDEFINITE_PLATEAU','infinite',None),
]


def load_births():
    df=pd.read_csv(URL,storage_options={'User-Agent':'Mozilla/5.0'})
    lower={str(c).lower():c for c in df.columns}
    ent=lower.get('entity'); yr=lower.get('year'); code=lower.get('code')
    if ent:
        w=df[df[ent].astype(str).str.lower().eq('world')].copy()
        if not w.empty:df=w
    if yr is None: raise RuntimeError(f'No Year column. Columns={list(df.columns)}')
    meta={x for x in (ent,yr,code) if x is not None}
    candidates=[]
    for c in df.columns:
        if c in meta:continue
        s=pd.to_numeric(df[c],errors='coerce')
        if s.notna().sum()>50:candidates.append((c,s))
    chosen=None
    for c,s in candidates:
        if 'birth' in str(c).lower():chosen=(c,s);break
    if chosen is None and candidates:chosen=candidates[0]
    if chosen is None:raise RuntimeError('No numeric births column found.')
    c,s=chosen
    out=pd.DataFrame({'Year':pd.to_numeric(df[yr],errors='coerce'),'births':s}).dropna()
    out['Year']=out['Year'].astype(int);out['births']=out['births'].astype(float)
    out=out.groupby('Year',as_index=False)['births'].sum().sort_values('Year')
    for need in (1950,1992,2022,2100):
        if need not in set(out.Year):raise RuntimeError(f'Required year {need} missing; range={out.Year.min()}..{out.Year.max()}')
    return out,c


def rank_mid_1992(d):
    post=d[(d.Year>=1950)&(d.Year<=2022)]
    before=post[post.Year<BIRTH_YEAR].births.sum()
    b92=float(post.loc[post.Year==BIRTH_YEAR,'births'].iloc[0])
    return PRB_EVER_1950+before+0.5*b92,b92


def known_cumulative_to_2100(d,r):
    # r is mid-1992. Add second half of 1992 plus all later annual births through 2100.
    b92=float(d.loc[d.Year==1992,'births'].iloc[0])
    later=0.5*b92+d[(d.Year>1992)&(d.Year<=2100)].births.sum()
    return r+later,later


def exp_tail_total(b2100,rate):
    # Discrete annual births: 2101 onward = b2100*(1-rate)^n, n=1..infinity.
    a=1-rate
    return b2100*a/(1-a)


def crossing_year_from_tail(target_remaining,b2100,kind,param):
    if target_remaining<=0:return 2100
    if kind=='zero':return None
    if kind=='plateau':
        years=int(param)
        n=math.ceil(target_remaining/b2100)
        return 2100+n if n<=years else None
    if kind=='exp':
        rate=float(param);a=1-rate
        total=exp_tail_total(b2100,rate)
        if target_remaining>total:return None
        # cumulative after n years: b*a*(1-a^n)/(1-a)
        rhs=1-target_remaining*(1-a)/(b2100*a)
        if rhs<=0:return None
        n=math.ceil(math.log(rhs)/math.log(a))
        return 2100+max(1,n)
    return None


def main():
    d,col=load_births();r,b92=rank_mid_1992(d)
    cum2100,after1992_to2100=known_cumulative_to_2100(d,r)
    b2100=float(d.loc[d.Year==2100,'births'].iloc[0])

    print('='*82)
    print('SELF-LOCATION D1 — FINITE HUMAN BIRTH DISTRIBUTION')
    print('='*82)
    print(f'Observed birth year = {BIRTH_YEAR}')
    print(f'UN WPP 2024 via OWID column = {col}')
    print(f'PRB cumulative births by 1950 = {PRB_EVER_1950:,}')
    print(f'PRB cumulative births by 2022 = {PRB_EVER_2022:,}')
    print(f'1992 annual births = {b92:,.0f}')
    print(f'approx mid-1992 cumulative rank r = {r:,.0f}')
    print(f'UN-projected 2100 annual births = {b2100:,.0f}')
    print(f'cumulative births implied through 2100 = {cum2100:,.0f}')
    print('\nSCENARIOS')

    finite=[]
    for name,kind,param in TAILS:
        if kind=='infinite':
            print(f'{name:22s} N_total=INFINITE q=0 in limit; exact-median crossing eventually occurs but no finite total rank quantile.')
            continue
        if kind=='zero':tail=0.0
        elif kind=='exp':tail=exp_tail_total(b2100,float(param))
        elif kind=='plateau':tail=b2100*int(param)
        else:raise ValueError(kind)
        nt=cum2100+tail;q=r/nt;dist=abs(q-.5)
        future_after_mid92=nt-r
        target=2*r
        if target<=cum2100:
            # approximate crossing within UN years by cumulative summation
            cur=r+0.5*b92;cross=None
            for y in range(1993,2101):
                cur+=float(d.loc[d.Year==y,'births'].iloc[0])
                if cur>=target:cross=y;break
        else:
            cross=crossing_year_from_tail(target-cum2100,b2100,kind,param)
        central25=.25<=q<=.75;central10=.10<=q<=.90;central05=.05<=q<=.95
        ssa_rel=1/nt
        finite.append((name,q,central25,central10,central05,nt,future_after_mid92,cross,ssa_rel))
        print(f'{name:22s} N_total={nt/1e9:10.3f}B  q={q:.4f}  |q-.5|={dist:.4f}  central25={central25} central10={central10}  2r_cross={cross}')

    n=len(finite);c25=sum(x[2] for x in finite);c10=sum(x[3] for x in finite)
    if all(x[3] for x in finite) and c25/n>=.75:
        verdict='ROBUST_INTERIOR'
    elif any(x[2] for x in finite) and any(not x[3] for x in finite):
        verdict='SENSITIVE_TO_TAIL'
    elif c25/n<.25:
        verdict='GENERALLY_NONCENTRAL'
    else:
        verdict='INTERMEDIATE'

    print('\nPREDECLARED ROBUSTNESS SUMMARY')
    print(f'finite scenarios = {n}')
    print(f'in [0.25,0.75] = {c25}/{n} ({c25/n:.3f})')
    print(f'in [0.10,0.90] = {c10}/{n} ({c10/n:.3f})')
    print('PREDECLARED D1 VERDICT =',verdict)

    # SSA toy likelihood ratios relative to shortest finite scenario.
    ref=min(x[5] for x in finite)
    print('\nTOY SELF-LOCATION WEIGHTING (DIAGNOSTIC ONLY)')
    for name,q,_,_,_,nt,_,_,_ in finite:
        bf_ssa=ref/nt
        bf_sia_ssa=1.0
        print(f'{name:22s} SSA relative likelihood vs shortest-N = {bf_ssa:.6g}   simple SIA+SSA = {bf_sia_ssa:.1f}')

    print('\nINTERPRETATION LOCK:')
    print('- Population peak is NOT the median of cumulative births; this calculation uses births.')
    print('- Post-2100 tails are sensitivity models, not demographic forecasts.')
    print('- The exact 2r crossing is diagnostic only; it may not be used to choose a tail.')
    print('- A finite human future is assumed by finite scenarios, not established by the data.')
    print('- SSA and SIA give different weighting; no observer measure is derived here.')
    print('- Prehistoric cumulative births are highly uncertain; PRB is an approximate reconstruction.')
    print('- No calendar year printed here is a prediction of extinction or the end of the world.')
    print('\nFINISHED SELF-LOCATION D1')

if __name__=='__main__':main()
