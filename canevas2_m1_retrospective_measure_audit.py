"""CANEvas 2.0 M1 — RETROSPECTIVE MEASURE AUDIT

IMPORTANT: this is deliberately POST-HOC. The v0.10 data have already been seen.
M1 can diagnose dependence on epoch/weighting but can never count as new evidence.

Input: results/v010_sensitivity_summary.csv
Primary question: how strongly does the historical preferred zeta depend on which
cosmic epoch receives weight?
"""
from pathlib import Path
import csv, math, statistics

PATH=Path('results/v010_sensitivity_summary.csv')
OBS=5.389452


def median(xs): return statistics.median(xs)
def q(xs,p):
    a=sorted(xs)
    if not a: return float('nan')
    x=(len(a)-1)*p; i=int(math.floor(x)); j=int(math.ceil(x))
    if i==j: return a[i]
    return a[i]*(j-x)+a[j]*(x-i)

rows=[]
with PATH.open(encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append({
            'z':float(r['z']),
            'peak':float(r['peak_zeta']),
            'support':float(r['observed_over_peak']),
        })

epochs=sorted(set(r['z'] for r in rows), reverse=True)
print('='*80)
print('CANEVAS 2.0 M1 — RETROSPECTIVE ZETA MEASURE AUDIT')
print('='*80)
print('POST-HOC DIAGNOSTIC ONLY. THIS OUTPUT CANNOT COUNT AS NEW EVIDENCE.\n')

per={}
for z in epochs:
    rr=[r for r in rows if r['z']==z]
    peaks=[r['peak'] for r in rr]; sup=[r['support'] for r in rr]
    per[z]={
        'n':len(rr),'med':median(peaks),'q16':q(peaks,.16),'q84':q(peaks,.84),
        'supmed':median(sup),'f75':sum(x>=.75 for x in sup)/len(sup),
        'f90':sum(x>=.90 for x in sup)/len(sup)
    }
    d=per[z]
    print(f"z={z:4.1f} n={d['n']:3d} peak_med={d['med']:.4f} 16-84=[{d['q16']:.4f},{d['q84']:.4f}] support_med={d['supmed']:.4f} f>=.75={d['f75']:.3f} f>=.90={d['f90']:.3f}")

meds=[per[z]['med'] for z in epochs]
epoch_spread=max(meds)/min(meds)

print('\nLEAVE-ONE-EPOCH-OUT')
loo=[]
for drop in epochs:
    rr=[r for r in rows if r['z']!=drop]
    peaks=[r['peak'] for r in rr]; sup=[r['support'] for r in rr]
    m=median(peaks); f75=sum(x>=.75 for x in sup)/len(sup)
    loo.append((drop,m,f75))
    print(f'drop z={drop:4.1f}: pooled_peak_med={m:.4f} pooled_f_support>=.75={f75:.4f}')

full_med=median([r['peak'] for r in rows])
full_f75=sum(r['support']>=.75 for r in rows)/len(rows)
loo_spread=max(x[1] for x in loo)/min(x[1] for x in loo)

# Purely diagnostic classification. Because data were already known, neither branch
# can be interpreted as confirmation/refutation of Canevas.
if epoch_spread>2.0:
    verdict='HISTORICAL_ZETA_PREFERENCE_STRONGLY_EPOCH_MEASURE_DEPENDENT'
else:
    verdict='HISTORICAL_ZETA_PREFERENCE_MODERATELY_EPOCH_STABLE'

print('\nC2-M1 SUMMARY')
print(f'full pooled peak median = {full_med:.6f}')
print(f'full fraction support>=0.75 = {full_f75:.6f}')
print(f'across-epoch median-peak spread factor = {epoch_spread:.6f}')
print(f'leave-one-epoch pooled-median spread factor = {loo_spread:.6f}')
print(f'C2-M1 DIAGNOSTIC VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- M1 is post-hoc and cannot supply new evidence.')
print('- A pooled historical median is not a prediction unless epoch/time weighting is independently derived.')
print('- Proximity of observed zeta at any one epoch may not be used to select that epoch.')
print('- The purpose of M1 is to specify what C2-M2 must solve: a physical time-integrated measure frozen before new output.')
print('- No thresholds or epoch subsets may be retuned under the M1 label.')
print('\nFINISHED C2-M1')