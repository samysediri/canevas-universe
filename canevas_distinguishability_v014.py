"""Canevas v0.14 — robustness attack on distinguishability measure.

Purpose
-------
Stress-test the striking v0.13 result without tuning toward the observed universe.
The central methodological fix is to remove scan-dependent standardisation.
We use derivatives of log-observables with respect to log-parameters, which are
already dimensionless. We then repeat the calculation across predeclared
observable subsets and scan-window trims.

This remains an added measure hypothesis, not a derivation from Canevas axioms.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.14'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
h_ref=.674; Om=.315; Ob=.0493; wm=Om*h_ref**2; wb_obs=Ob*h_ref**2
zeta_obs=(wm-wb_obs)/wb_obs; OL=1-Om; wL_obs=OL*h_ref**2
As=2.10e-9; ns=.965; YHe=.245
zgrid=np.unique(np.sort(np.r_[np.logspace(np.log10(2.0),np.log10(20.0),45),zeta_obs]))
lgrid=np.unique(np.sort(np.r_[np.logspace(np.log10(.05),np.log10(6.0),45),1.0]))
# Superset of observables computed once.
ks=np.logspace(-2,0.7,10); zs=[0.,1.,2.,4.,6.]


def features(zeta,lr):
    wb=wm/(1+zeta); wc=wm-wb; wL=wL_obs*lr; h=np.sqrt(wm+wL)
    c=Class()
    try:
        c.set({'output':'mPk','h':float(h),'omega_b':float(wb),'omega_cdm':float(wc),'A_s':As,'n_s':ns,'YHe':YHe,'P_k_max_1/Mpc':6.,'z_max_pk':6.5})
        c.compute(); vals=[]; labels=[]
        for z in zs:
            for k in ks:
                vals.append(np.log(max(c.pk(float(k),z),1e-300))); labels.append(f'pk_z{z:g}_k{k:.5g}')
            vals.append(np.log(np.sqrt(wm*(1+z)**3+wL))); labels.append(f'H_z{z:g}')
        return np.asarray(vals),labels,None
    except Exception as e:
        return None,None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass


def scan(grid,fixed,which):
    feats=[]; good=[]; labels=None
    for i,x in enumerate(grid,1):
        print(f'{which} [{i}/{len(grid)}] {x:.6g}',end=' ... ',flush=True)
        f,l,e=features(x,fixed) if which=='zeta' else features(fixed,x)
        if f is None:
            print('REJECTED'); continue
        print('OK'); good.append(x); feats.append(f); labels=l
    return np.asarray(good),np.vstack(feats),labels


def metric_summary(x,F,labels,which,variant,trim=None):
    # Select predeclared observable subsets.
    if variant=='P_all': mask=np.array([lab.startswith('pk_') for lab in labels])
    elif variant=='H_all': mask=np.array([lab.startswith('H_') for lab in labels])
    elif variant=='PplusH_all': mask=np.ones(len(labels),dtype=bool)
    elif variant=='P_late': mask=np.array([lab.startswith('pk_') and any(f'z{z:g}_' in lab for z in [0.,1.,2.]) for lab in labels])
    elif variant=='P_early': mask=np.array([lab.startswith('pk_') and any(f'z{z:g}_' in lab for z in [4.,6.]) for lab in labels])
    elif variant=='P_large_scales':
        mask=[]
        for lab in labels:
            if not lab.startswith('pk_'): mask.append(False); continue
            kval=float(lab.split('_k')[1]); mask.append(kval<=0.25)
        mask=np.array(mask)
    elif variant=='P_small_scales':
        mask=[]
        for lab in labels:
            if not lab.startswith('pk_'): mask.append(False); continue
            kval=float(lab.split('_k')[1]); mask.append(kval>=0.25)
        mask=np.array(mask)
    else: raise ValueError(variant)

    xx=x.copy(); QQ=F[:,mask].copy()
    if trim is not None:
        lo,hi=trim; m=(xx>=lo)&(xx<=hi); xx=xx[m]; QQ=QQ[m]
    u=np.log(xx)
    # No scan-dependent standardization: log-observable derivatives are dimensionless.
    dQ=np.gradient(QQ,u,axis=0)
    speed=np.sqrt(np.sum(dQ*dQ,axis=1))
    norm=np.trapezoid(speed,u)
    p=speed/norm
    c=np.r_[0,np.cumsum(.5*(p[:-1]+p[1:])*np.diff(u))]; c/=c[-1]
    obs=zeta_obs if which=='zeta' else 1.
    if not (xx.min()<=obs<=xx.max()): return None
    cdf=float(np.interp(np.log(obs),u,c)); med=float(np.exp(np.interp(.5,c,u)))
    return {'parameter':which,'variant':variant,'trim':str(trim),'cdf_at_observed':cdf,'median':med,'nobs':int(mask.sum()),'xmin':float(xx.min()),'xmax':float(xx.max())}


def run():
    print('CANEVAS v0.14 — ROBUSTNESS ATTACK ON DISTINGUISHABILITY')
    print('No scan-dependent feature standardisation.\n')
    xz,Fz,labels=scan(zgrid,1.,'zeta')
    xl,Fl,_=scan(lgrid,zeta_obs,'lambda')
    variants=['P_all','H_all','PplusH_all','P_late','P_early','P_large_scales','P_small_scales']
    ztrims=[None,(2.5,15.),(3.,12.)]
    ltrims=[None,(.1,5.),(.15,4.)]
    rows=[]
    for v in variants:
        for t in ztrims:
            r=metric_summary(xz,Fz,labels,'zeta',v,t)
            if r: rows.append(r)
        for t in ltrims:
            r=metric_summary(xl,Fl,labels,'lambda',v,t)
            if r: rows.append(r)
    with (OUT/'v014_distinguishability_robustness.csv').open('w',newline='',encoding='utf8') as f:
        fields=['parameter','variant','trim','cdf_at_observed','median','nobs','xmin','xmax']; w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    lines=[f'CANEVAS v{VERSION} — DISTINGUISHABILITY ROBUSTNESS','='*56]
    for par in ['zeta','lambda']:
        rr=[r for r in rows if r['parameter']==par]; c=np.array([r['cdf_at_observed'] for r in rr]); m=np.array([r['median'] for r in rr])
        lines += ['',par.upper(),f'variants = {len(rr)}',f'CDF median = {np.median(c):.6f}',f'CDF 10-90% = [{np.percentile(c,10):.6f}, {np.percentile(c,90):.6f}]',f'median(parameter) median = {np.median(m):.6f}',f'fraction with observed CDF in [0.25,0.75] = {np.mean((c>=.25)&(c<=.75)):.6f}',f'fraction with observed CDF in [0.10,0.90] = {np.mean((c>=.10)&(c<=.90)):.6f}']
    lines += ['', 'GUARDRAILS:', '- v0.13 exact match is not considered robust unless it survives these variants.', '- H-only is a deliberately harsh alternative and may probe a different physical notion of distinguishability.', '- Scan-window sensitivity remains a failure mode if CDFs move strongly under trims.', '- No anthropic score is used here.']
    text='\n'.join(lines); (OUT/'v014_distinguishability_robustness_summary.txt').write_text(text,encoding='utf8'); print('\n'+text+'\nFINISHED v0.14')
if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
