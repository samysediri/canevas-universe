"""CANEVAS 2.0 M2 — BLIND TIME-INTEGRATED ZETA MEASURE v1

PREREGISTERED BEFORE OUTPUT.

Purpose
-------
M1 showed that the historical preferred zeta is strongly epoch-dependent. M2 asks
whether a simple independently declared time-integrated measure yields a stable
zeta preference WITHOUT using the observed zeta to choose epochs or weights.

This is a methodological bridge, not new astrophysical evidence: it reuses the
already-seen v0.10 sensitivity table. Therefore M2 may validate a measure recipe
for future blind simulations, but it may NOT count as empirical confirmation of
Canevas or as a blind prediction of zeta.

Frozen measure
--------------
For each model row, combine its five available epochs z={10,8,6,4,2} using cosmic
proper-time interval weights from a fixed flat LCDM background (Omega_m=0.3,
Omega_L=0.7). Each tabulated epoch represents its Voronoi cell in scale factor a,
with outer boundaries halfway in a to the nearest tabulated point and clipped to
z=12 and z=0. This choice is declared before output and is independent of the
observed zeta.

Within each epoch we only possess the historical row-level summaries peak_zeta and
observed_over_peak, not the full W(zeta) curve. Thus M2 can time-integrate peak
locations as a weighted geometric mean and audit robustness, but cannot reconstruct
a genuine integrated posterior. That limitation is part of the verdict.
"""
from pathlib import Path
import csv, math, statistics

PATH=Path('results/v010_sensitivity_summary.csv')
EPOCHS=[10.0,8.0,6.0,4.0,2.0]
OM=0.3; OL=0.7
ZHI=12.0; ZLO=0.0


def a_of_z(z): return 1.0/(1.0+z)
def E_of_a(a): return math.sqrt(OM/a**3 + OL)
def dt_da(a): return 1.0/(a*E_of_a(a))  # common H0^-1 cancels

def integrate(f,lo,hi,n=20000):
    if n%2: n+=1
    h=(hi-lo)/n
    s=f(lo)+f(hi)
    for i in range(1,n): s+=(4 if i%2 else 2)*f(lo+i*h)
    return s*h/3

# Voronoi cells in scale factor, because a is monotonic and avoids arbitrary equal-z bins.
a_pts=sorted((a_of_z(z),z) for z in EPOCHS)
a_min=a_of_z(ZHI); a_max=a_of_z(ZLO)
bounds=[a_min]
for i in range(len(a_pts)-1): bounds.append(0.5*(a_pts[i][0]+a_pts[i+1][0]))
bounds.append(a_max)
weights={}
for i,(a,z) in enumerate(a_pts): weights[z]=integrate(dt_da,bounds[i],bounds[i+1])
norm=sum(weights.values()); weights={z:w/norm for z,w in weights.items()}

rows=[]
with PATH.open(encoding='utf-8') as f:
    for r in csv.DictReader(f): rows.append(r)

# infer model identity from every column except epoch and output summaries
exclude={'z','peak_zeta','observed_over_peak'}
keycols=[c for c in rows[0].keys() if c not in exclude]
groups={}
for r in rows:
    key=tuple(r[c] for c in keycols)
    groups.setdefault(key,{})[float(r['z'])]=float(r['peak_zeta'])

integrated=[]; incomplete=0
for key,d in groups.items():
    if not all(z in d for z in EPOCHS): incomplete+=1; continue
    # weighted geometric mean is appropriate for a positive scale parameter spanning factors
    logpeak=sum(weights[z]*math.log(d[z]) for z in EPOCHS)
    integrated.append(math.exp(logpeak))


def quantile(xs,p):
    a=sorted(xs); x=(len(a)-1)*p; i=int(math.floor(x)); j=int(math.ceil(x))
    return a[i] if i==j else a[i]*(j-x)+a[j]*(x-i)

print('='*82)
print('CANEVAS 2.0 M2 — BLIND TIME-INTEGRATED ZETA MEASURE v1')
print('='*82)
print('OBSERVED ZETA IS NOT USED OR PRINTED IN THIS TEST.\n')
print('Frozen proper-time weights:')
for z in sorted(weights,reverse=True): print(f' z={z:4.1f} weight={weights[z]:.8f}')
print(f'complete model trajectories = {len(integrated)}  incomplete = {incomplete}')

med=statistics.median(integrated); q16=quantile(integrated,.16); q84=quantile(integrated,.84)
spread=q84/q16
# leave-one-epoch-out using the SAME physical weights renormalized, purely robustness audit
loo=[]
for drop in EPOCHS:
    ww={z:w for z,w in weights.items() if z!=drop}; nn=sum(ww.values()); ww={z:w/nn for z,w in ww.items()}
    vals=[]
    for key,d in groups.items():
        if not all(z in d for z in EPOCHS): continue
        vals.append(math.exp(sum(ww[z]*math.log(d[z]) for z in ww)))
    loo.append((drop,statistics.median(vals)))

loo_factor=max(v for _,v in loo)/min(v for _,v in loo)
print('\nTIME-INTEGRATED PEAK ENSEMBLE')
print(f'median = {med:.8f}')
print(f'16-84 = [{q16:.8f}, {q84:.8f}]')
print(f'84/16 spread factor = {spread:.8f}')
print('\nLEAVE-ONE-EPOCH-OUT')
for z,v in loo: print(f'drop z={z:4.1f}: median={v:.8f}')
print(f'LOO median spread factor = {loo_factor:.8f}')

# preregistered methodological criterion only; no comparison to observed zeta.
if len(integrated)>=40 and loo_factor<=1.5:
    verdict='TIME_INTEGRATED_MEASURE_RECIPE_STABLE_ENOUGH_FOR_FUTURE_BLIND_TEST'
else:
    verdict='TIME_INTEGRATED_MEASURE_RECIPE_NOT_STABLE_ENOUGH_FOR_FUTURE_BLIND_TEST'

print('\nC2-M2 SUMMARY')
print(f'time_integrated_peak_median = {med:.8f}')
print(f'time_integrated_peak_q16 = {q16:.8f}')
print(f'time_integrated_peak_q84 = {q84:.8f}')
print(f'leave_one_epoch_spread_factor = {loo_factor:.8f}')
print(f'C2-M2 METHODOLOGICAL VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- Observed zeta was not used to select weights, epochs, thresholds, or verdict.')
print('- M2 reuses historical data and therefore cannot count as new empirical evidence or a blind zeta prediction.')
print('- Proper-time weighting is one explicit physical convention, not a uniquely derived observer measure.')
print('- Weighted peak locations are not equivalent to integrating full likelihood/posterior curves.')
print('- If stable, this recipe may be frozen for a NEW simulation that outputs full W(zeta,t) before observed zeta is revealed.')
print('- If unstable, do not retune weights under M2; design a separately motivated M3 instead.')
print('\nFINISHED C2-M2 — DO NOT RETUNE AFTER OUTPUT')