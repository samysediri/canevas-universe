"""Canevas v0.13 — predeclared distinguishability experiment.

This experiment does NOT derive P(U) from the philosophical axioms.
It tests one additional candidate hypothesis: parameter-space volume should be
weighted by how rapidly a fixed set of cosmological observables changes.

To avoid using our observed parameter values to tune the metric, the observable
vector and numerical regularisation below are fixed before results are examined.
This is exploratory, not evidence for Canevas by itself.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION="0.13"
OUT=Path(__file__).resolve().parent/"results"; OUT.mkdir(exist_ok=True)
h_ref=.674; Om=.315; Ob=.0493; wm=Om*h_ref**2; wb_obs=Ob*h_ref**2
zeta_obs=(wm-wb_obs)/wb_obs; OL=1-Om; wL_obs=OL*h_ref**2
As=2.10e-9; ns=.965; YHe=.245
# Dimensionless positive coordinates. Observed values are included only for later
# evaluation, not for defining metric weights.
zgrid=np.unique(np.sort(np.r_[np.logspace(np.log10(2.5),np.log10(15),31),zeta_obs]))
lgrid=np.unique(np.sort(np.r_[np.logspace(-1, np.log10(6.0),31),1.0]))
# Fixed observable vector: log matter power at 8 k values x z=(0,2,6), plus
# log H(z) at the same epochs. Equal standardised weight per observable.
ks=np.logspace(-2,0.7,8); zs=[0.,2.,6.]

def features(zeta,lr):
    wb=wm/(1+zeta); wc=wm-wb; wL=wL_obs*lr; h=np.sqrt(wm+wL)
    c=Class()
    try:
        c.set({'output':'mPk','h':float(h),'omega_b':float(wb),'omega_cdm':float(wc),'A_s':As,'n_s':ns,'YHe':YHe,'P_k_max_1/Mpc':6.,'z_max_pk':6.5})
        c.compute(); f=[]
        for z in zs:
            for k in ks: f.append(np.log(max(c.pk(float(k),z),1e-300)))
            # dimensionless H relative to 100 km/s/Mpc
            f.append(np.log(np.sqrt(wm*(1+z)**3+wL)))
        return np.asarray(f),None
    except Exception as e: return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass

def curve(grid,fixed,which):
    raw=[]
    for i,x in enumerate(grid,1):
        print(f'{which} [{i}/{len(grid)}] {x:.6g}',end=' ... ',flush=True)
        f,e=features(x,fixed) if which=='zeta' else features(fixed,x)
        print('OK' if f is not None else 'REJECTED')
        raw.append((x,f,e))
    ok=[r for r in raw if r[1] is not None]
    x=np.array([r[0] for r in ok]); F=np.vstack([r[1] for r in ok])
    # Standardise observables across the predeclared scan so units/components do
    # not dominate merely by numerical scale. This choice is itself a hypothesis.
    scale=np.std(F,axis=0); scale=np.where(scale>1e-10,scale,1.)
    Q=F/scale
    u=np.log(x); dQ=np.gradient(Q,u,axis=0)
    speed=np.sqrt(np.sum(dQ*dQ,axis=1)) # ds/dlog(parameter)
    # Compare candidate invariant volume to log-flat baseline.
    density_u=speed
    norm=np.trapezoid(density_u,u); p=density_u/norm
    c=np.r_[0,np.cumsum(.5*(p[:-1]+p[1:])*np.diff(u))]; c/=c[-1]
    obs=zeta_obs if which=='zeta' else 1.
    cdf=float(np.interp(np.log(obs),u,c)); med=float(np.exp(np.interp(.5,c,u)))
    return x,speed,cdf,med,raw

def run():
    print('CANEVAS v0.13 — DISTINGUISHABILITY CANDIDATE (NO ANTHROPIC SCORE)')
    print('Metric definition frozen before result inspection.\n')
    xz,sz,cz,mz,rz=curve(zgrid,1.,'zeta')
    xl,sl,cl,ml,rl=curve(lgrid,zeta_obs,'lambda')
    with (OUT/'v013_distinguishability.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['parameter','value','ds_dlogparam'])
        for x,s in zip(xz,sz): w.writerow(['zeta',x,s])
        for x,s in zip(xl,sl): w.writerow(['lambda_ratio',x,s])
    text=f'''CANEVAS v{VERSION} — DISTINGUISHABILITY CANDIDATE\n==================================================\nThis is a test of an added measure hypothesis, NOT a derivation from the Canevas axioms.\nNo anthropic/complexity score is included in this run.\n\nzeta observed = {zeta_obs:.6f}\nzeta distinguishability CDF at observed = {cz:.6f}\nzeta distinguishability median = {mz:.6f}\n\nLambda observed ratio = 1\nLambda distinguishability CDF at observed = {cl:.6f}\nLambda distinguishability median = {ml:.6f}\n\nInterpretation guardrails:\n- Near 0.5 CDF means typical only under this candidate metric and finite scan.\n- A good match does not validate the philosophical axioms.\n- Strong dependence on observable choice or scan bounds falsifies robustness of this candidate.\n'''
    (OUT/'v013_distinguishability_summary.txt').write_text(text,encoding='utf8'); print('\n'+text+'\nFINISHED v0.13')
if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
