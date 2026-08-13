"""Canevas v0.21 — boundary-sensitivity autopsy for zeta distinguishability.

Purpose: test whether the apparent centering of the observed dark-matter/baryon
ratio is mainly induced by finite scan bounds. No anthropic weighting and no
retuning to improve agreement.

The CLASS observable family is kept the same as the previous distinguishability
work: log P(k,z) at 8 k values for z=(0,2,6), plus log H(z). The metric density
along zeta is the Euclidean speed dF/dlog(zeta).

We first compute one broad zeta curve, then re-normalize the SAME metric density
on a predeclared family of truncated subdomains. If the inferred median and CDF
at zeta_obs move strongly with these bounds, the earlier centering is boundary-
driven rather than an interior prediction.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.21'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)

h=.674; Om=.315; Ob=.0493
wm=Om*h*h; wb_obs=Ob*h*h; zeta_obs=(Om-Ob)/Ob
wL=(1-Om)*h*h; As=2.10e-9; ns=.965; YHe=.245
ks=np.logspace(-2,0.7,8); zs=[0.,2.,6.]

# Broad diagnostic grid. CLASS may reject some low-zeta points; rejected values
# are never interpolated and are simply absent from all subdomain calculations.
ZETA=np.unique(np.sort(np.r_[np.logspace(np.log10(0.8),np.log10(80.0),90),zeta_obs]))

# PREDECLARED bound families, chosen before this run's results are seen.
LOWER_CUTS=[2.5,3.0,4.0,5.0]
UPPER_CUTS=[10.0,15.0,25.0,40.0,80.0]


def features(zeta):
    wb=wm/(1+zeta); wc=wm-wb
    c=Class()
    try:
        c.set({'output':'mPk','h':h,'omega_b':float(wb),'omega_cdm':float(wc),
               'A_s':As,'n_s':ns,'YHe':YHe,'P_k_max_1/Mpc':6.,'z_max_pk':6.5})
        c.compute(); f=[]
        for z in zs:
            for k in ks: f.append(np.log(max(c.pk(float(k),float(z)),1e-300)))
            f.append(np.log(max(c.Hubble(float(z)),1e-300)))
        return np.asarray(f),None
    except Exception as e:
        return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass


def summarize(x,speed,lo,hi):
    m=(x>=lo)&(x<=hi)&np.isfinite(speed)
    xx=x[m]; ss=np.maximum(speed[m],0)
    if len(xx)<5: return None
    u=np.log(xx)
    norm=np.trapezoid(ss,u)
    if not np.isfinite(norm) or norm<=0: return None
    p=ss/norm
    area=.5*(p[:-1]+p[1:])*np.diff(u)
    c=np.r_[0,np.cumsum(area)]; c/=c[-1]
    median=float(np.exp(np.interp(.5,c,u)))
    cdf=float(np.interp(np.log(zeta_obs),u,c,left=0.0,right=1.0))
    q16=float(np.exp(np.interp(.16,c,u))); q84=float(np.exp(np.interp(.84,c,u)))
    return len(xx),float(xx.min()),float(xx.max()),median,cdf,q16,q84


def run():
    print('='*72)
    print(f' CANEVAS v{VERSION} — ZETA BOUNDARY-SENSITIVITY TEST')
    print('='*72)
    print('No anthropic score; no bound is chosen after seeing its result.\n')

    xs=[]; Fs=[]; rejects=[]
    for i,z in enumerate(ZETA,1):
        print(f'[{i:2d}/{len(ZETA)}] zeta={z:.7g}',end=' ... ',flush=True)
        f,e=features(float(z))
        if f is None:
            print('REJECTED'); rejects.append((z,e)); continue
        print('OK'); xs.append(z); Fs.append(f)
    if len(xs)<10: raise RuntimeError('Too few valid zeta cosmologies.')

    x=np.asarray(xs); F=np.vstack(Fs); u=np.log(x)
    dF=np.gradient(F,u,axis=0)
    speed=np.sqrt(np.sum(dF*dF,axis=1))

    rows=[]
    for lo in LOWER_CUTS:
        for hi in UPPER_CUTS:
            if hi<=lo or not (lo<zeta_obs<hi):
                continue
            r=summarize(x,speed,lo,hi)
            if r is None: continue
            n,xmin,xmax,med,cdf,q16,q84=r
            rows.append((lo,hi,n,xmin,xmax,med,cdf,q16,q84))
            print(f'[{lo:4.1f},{hi:5.1f}] median={med:8.4f}  CDF(obs)={cdf:7.4f}  16-84=[{q16:.4f},{q84:.4f}]')

    meds=np.array([r[5] for r in rows]); cdfs=np.array([r[6] for r in rows])
    log_mid=np.array([0.5*(np.log(r[0])+np.log(r[1])) for r in rows])
    corr=float(np.corrcoef(log_mid,np.log(meds))[0,1]) if len(rows)>2 else np.nan

    with (OUT/'v021_zeta_curve.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','metric_speed_per_dlogzeta'])
        for z,s in zip(x,speed): w.writerow([z,s])
    with (OUT/'v021_bound_variants.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['requested_lo','requested_hi','n_valid','actual_min','actual_max','median','cdf_at_observed','q16','q84']); w.writerows(rows)

    text=f'''CANEVAS v{VERSION} — BOUNDARY-SENSITIVITY SUMMARY
====================================================
Observed zeta = {zeta_obs:.8f}
Valid CLASS zeta range = [{x.min():.8f}, {x.max():.8f}]
Rejected scan points = {len(rejects)}
Predeclared subdomains evaluated = {len(rows)}

Median across subdomains = {np.median(meds):.8f}
Median range across subdomains = [{np.min(meds):.8f}, {np.max(meds):.8f}]
CDF(obs) median across subdomains = {np.median(cdfs):.8f}
CDF(obs) range across subdomains = [{np.min(cdfs):.8f}, {np.max(cdfs):.8f}]
Correlation(log geometric-domain-center, log inferred median) = {corr:.8f}

PREDECLARED READING:
- Strong median movement with the bounds supports a truncation/boundary explanation.
- Stable median near observed zeta across widely different bounds would preserve an interior-selection puzzle.
- No subdomain may be selected as the preferred one because it matches observation.
- This diagnostic cannot rescue the distinguishability-as-probability hypothesis after v0.19.
'''
    (OUT/'v021_boundary_summary.txt').write_text(text,encoding='utf8')
    print('\n'+text+'\nFINISHED v0.21')

if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
