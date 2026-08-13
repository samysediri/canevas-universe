"""Self-location O1 test: how surprising is a recent birth year after weighting by births?

Data source at run time:
Our World in Data grapher, sourced from UN World Population Prospects 2024.
This test intentionally restricts the quantitative calculation to 1950-2023,
the directly covered period of the annual-birth dataset. It does NOT extrapolate
through all of human history.

The user's birth year is used only as the observation being evaluated, not to
choose the data range or model.
"""
from urllib.request import Request, urlopen
from io import StringIO
import csv

URL='https://ourworldindata.org/grapher/annual-number-of-births-by-world-region.csv?v=1&csvType=full&useColumnShortNames=false'
OBS_YEAR=1992
WINDOW=5
TECH_THRESHOLDS=[1950,1970,1980,1990]


def fetch_rows():
    req=Request(URL,headers={'User-Agent':'Canevas self-location research/1.0'})
    text=urlopen(req,timeout=30).read().decode('utf-8')
    rows=list(csv.DictReader(StringIO(text)))
    if not rows: raise RuntimeError('No data returned.')
    # identify the numeric indicator column robustly
    fixed={'Entity','Code','Year'}
    valcols=[c for c in rows[0].keys() if c not in fixed]
    if len(valcols)!=1:
        # choose first column with a parseable value in World rows
        pick=None
        for c in valcols:
            for r in rows:
                if r.get('Entity')=='World':
                    try: float(r[c]); pick=c; break
                    except Exception: pass
            if pick: break
        if not pick: raise RuntimeError(f'Could not identify birth column: {valcols}')
        value_col=pick
    else:
        value_col=valcols[0]
    world=[]
    for r in rows:
        if r.get('Entity')!='World': continue
        y=int(r['Year'])
        try: b=float(r[value_col])
        except Exception: continue
        world.append((y,b))
    world.sort()
    return world,value_col


def probability_window(data, lo, hi, cond_lo=None):
    d=[(y,b) for y,b in data if (cond_lo is None or y>=cond_lo)]
    total=sum(b for _,b in d)
    hit=sum(b for y,b in d if lo<=y<=hi)
    return hit/total if total>0 else float('nan')


def birth_cdf(data, year, cond_lo=None):
    d=[(y,b) for y,b in data if (cond_lo is None or y>=cond_lo)]
    total=sum(b for _,b in d)
    return sum(b for y,b in d if y<=year)/total if total>0 else float('nan')


def run():
    data,col=fetch_rows()
    ymin,ymax=data[0][0],data[-1][0]
    if not (ymin<=OBS_YEAR<=ymax): raise RuntimeError('Observed year outside dataset.')
    years=[y for y,_ in data]
    n_years=len(years)
    lo=max(ymin,OBS_YEAR-WINDOW); hi=min(ymax,OBS_YEAR+WINDOW)

    # M0: uniform calendar year over same measured interval.
    p_uniform=(hi-lo+1)/n_years
    # M1: sample a random birth from UN-covered interval.
    p_birth=probability_window(data,lo,hi)
    cdf_birth=birth_cdf(data,OBS_YEAR)
    bobs=dict(data)[OBS_YEAR]
    bavg=sum(b for _,b in data)/len(data)
    rank_share=bobs/sum(b for _,b in data)

    print('CANEVAS SELF-LOCATION O1 — BIRTH-DENSITY TEST v1')
    print('==================================================')
    print(f'Data source column: {col}')
    print(f'Quantitative domain: {ymin}-{ymax} only (no prehistoric extrapolation)')
    print(f'Observed birth year evaluated: {OBS_YEAR}')
    print(f'Observed-year births: {bobs:,.0f}')
    print(f'Mean annual births over domain: {bavg:,.0f}')
    print()
    print(f'M0 uniform-calendar P(year within ±{WINDOW}) = {p_uniform:.6f}')
    print(f'M1 birth-weighted   P(year within ±{WINDOW}) = {p_birth:.6f}')
    print(f'Birth-weighted CDF through {OBS_YEAR} = {cdf_birth:.6f}')
    print(f'Share of all 1950-2023 births occurring in {OBS_YEAR} alone = {rank_share:.6f}')
    print()
    print('TECHNOLOGY-CONDITIONING SENSITIVITY (hard year cutoffs; diagnostic only):')
    for t in TECH_THRESHOLDS:
        if t>OBS_YEAR: continue
        p=probability_window(data,lo,hi,cond_lo=t)
        c=birth_cdf(data,OBS_YEAR,cond_lo=t)
        print(f'condition birth year >= {t}: P(±{WINDOW})={p:.6f}; CDF(obs)={c:.6f}')
    print()
    ratio=p_birth/p_uniform if p_uniform>0 else float('nan')
    print(f'Population-density correction factor M1/M0 for ±{WINDOW}-year window = {ratio:.4f}x')
    print()
    print('INTERPRETATION LOCK:')
    print('- This directly tests only the UN-covered 1950-2023 interval.')
    print('- A hard technology cutoff is a sensitivity diagnostic, not a model of technological consciousness.')
    print('- If recent birth timing becomes ordinary after birth weighting/conditioning, the raw "why now?" intuition is selection-biased.')
    print('- This says nothing by itself about Doomsday rank O2, which is a separate self-location problem.')
    print('- No cutoff may be selected post hoc because it makes the observation look special or ordinary.')
    print('\nFINISHED SELF-LOCATION O1 v1')

if __name__=='__main__':
    run()
