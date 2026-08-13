"""Canevas v0.15.1 — joint 2D distinguishability with objective handling of CLASS rejects.

Same metric/observables/domain as v0.15. If CLASS rejects any point, every zeta-row
and every Lambda-column containing at least one rejected point is removed before
computing derivatives. This uses only numerical validity, never the metric values.
No interpolation of rejected cosmologies is performed.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.15.1'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
h_ref=.674; Om=.315; Ob=.0493; wm=Om*h_ref**2; wb_obs=Ob*h_ref**2
zeta_obs=(wm-wb_obs)/wb_obs; wL_obs=(1-Om)*h_ref**2
As=2.10e-9; ns=.965; YHe=.245
zgrid=np.unique(np.sort(np.r_[np.logspace(np.log10(2.5),np.log10(15),19),zeta_obs]))
lgrid=np.unique(np.sort(np.r_[np.logspace(np.log10(.1),np.log10(6.),19),1.0]))
ks=np.logspace(-2,0.7,8); zs=[0.,2.,6.]

def features(zeta,lr):
    wb=wm/(1+zeta); wc=wm-wb; wL=wL_obs*lr; h=float(np.sqrt(wm+wL))
    c=Class()
    try:
        c.set({'output':'mPk','h':h,'omega_b':float(wb),'omega_cdm':float(wc),'A_s':As,'n_s':ns,'YHe':YHe,'P_k_max_1/Mpc':6.,'z_max_pk':6.5})
        c.compute(); f=[]
        for z in zs:
            for k in ks: f.append(np.log(max(c.pk(float(k),z),1e-300)))
            f.append(np.log(np.sqrt(wm*(1+z)**3+wL)))
        return np.asarray(f),None
    except Exception as e: return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass

def cdf_1d(u,p,uobs):
    p=np.maximum(p,0); n=np.trapezoid(p,u)
    if n<=0: return np.nan,np.nan
    p=p/n; area=.5*(p[:-1]+p[1:])*np.diff(u); c=np.r_[0,np.cumsum(area)]; c/=c[-1]
    return float(np.interp(uobs,u,c)),float(np.exp(np.interp(.5,c,u)))

def run():
    nz,nl=len(zgrid),len(lgrid); F=None; valid=np.zeros((nz,nl),bool); errors=[]
    total=nz*nl; n=0
    for i,zeta in enumerate(zgrid):
        for j,lr in enumerate(lgrid):
            n+=1; print(f'[{n:3d}/{total}] zeta={zeta:.5g}, lambda={lr:.5g}',end=' ... ',flush=True)
            f,e=features(float(zeta),float(lr))
            if f is None:
                print('REJECTED'); errors.append((i,j,zeta,lr,e)); continue
            print('OK')
            if F is None: F=np.full((nz,nl,len(f)),np.nan)
            F[i,j]=f; valid[i,j]=True
    if F is None: raise RuntimeError('No valid CLASS points.')

    bad_rows=np.where(~np.all(valid,axis=1))[0]
    bad_cols=np.where(~np.all(valid,axis=0))[0]
    keep_rows=np.array([i for i in range(nz) if i not in set(bad_rows)])
    keep_cols=np.array([j for j in range(nl) if j not in set(bad_cols)])
    if len(keep_rows)<3 or len(keep_cols)<3:
        raise RuntimeError('Too many rejected rows/columns for a stable 2D derivative grid.')

    zg=zgrid[keep_rows]; lg=lgrid[keep_cols]; FF=F[np.ix_(keep_rows,keep_cols,np.arange(F.shape[2]))]
    if not np.all(np.isfinite(FF)): raise RuntimeError('Reduced grid still contains invalid points.')

    uz=np.log(zg); ul=np.log(lg)
    dF_duz=np.gradient(FF,uz,axis=0); dF_dul=np.gradient(FF,ul,axis=1)
    g11=np.sum(dF_duz*dF_duz,axis=2); g22=np.sum(dF_dul*dF_dul,axis=2); g12=np.sum(dF_duz*dF_dul,axis=2)
    density=np.sqrt(np.maximum(g11*g22-g12*g12,0))
    norm=np.trapezoid(np.trapezoid(density,ul,axis=1),uz); P=density/norm
    pz=np.trapezoid(P,ul,axis=1); pl=np.trapezoid(P,uz,axis=0)
    cz,mz=cdf_1d(uz,pz,np.log(zeta_obs)); cl,ml=cdf_1d(ul,pl,0.0)

    row_at_obs=np.array([np.interp(np.log(zeta_obs),uz,P[:,j]) for j in range(len(lg))])
    pobs=float(np.interp(0.0,ul,row_at_obs))
    cell_mass=.25*(P[:-1,:-1]+P[1:,:-1]+P[:-1,1:]+P[1:,1:])*np.diff(uz)[:,None]*np.diff(ul)[None,:]
    cell_density=.25*(P[:-1,:-1]+P[1:,:-1]+P[:-1,1:]+P[1:,1:])
    low_density_mass=float(np.sum(cell_mass[cell_density<=pobs]))

    with (OUT/'v0151_joint_metric.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','lambda_ratio','density_per_dlogzeta_dloglambda'])
        for i,z in enumerate(zg):
            for j,l in enumerate(lg): w.writerow([z,l,density[i,j]])
    with (OUT/'v0151_rejections.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','lambda_ratio','error'])
        for _,_,z,l,e in errors: w.writerow([z,l,e])

    text=f'''CANEVAS v{VERSION} — JOINT 2D DISTINGUISHABILITY\n==================================================\nSame metric as v0.15; no anthropic score.\nOriginal grid = {nz} x {nl} = {nz*nl} points\nCLASS rejected points = {len(errors)}\nRows removed solely because of CLASS rejection = {len(bad_rows)}\nColumns removed solely because of CLASS rejection = {len(bad_cols)}\nReduced fully valid grid = {len(zg)} x {len(lg)} = {len(zg)*len(lg)} points\nReduced domain: zeta [{zg.min():.4f},{zg.max():.4f}], Lambda ratio [{lg.min():.4f},{lg.max():.4f}]\n\nzeta observed = {zeta_obs:.6f}\nzeta marginal CDF at observed = {cz:.6f}\nzeta marginal median = {mz:.6f}\n\nLambda observed ratio = 1\nLambda marginal CDF at observed = {cl:.6f}\nLambda marginal median = {ml:.6f}\n\nObserved-point lower-density probability mass = {low_density_mass:.6f}\n(near 0.5 is ordinary; near 0 or 1 is more special, but this is NOT a p-value.)\n\nGUARDRAILS:\n- Rejected points are never interpolated.\n- Row/column removal depends only on CLASS validity, not metric values.\n- Metric remains an added hypothesis, not a derivation from Canevas axioms.\n- Result remains conditional on finite bounds and observable vector.\n'''
    (OUT/'v0151_joint_metric_summary.txt').write_text(text,encoding='utf8'); print('\n'+text+'\nFINISHED v0.15.1')
if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
