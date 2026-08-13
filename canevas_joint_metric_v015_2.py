"""Canevas v0.15.2 — joint 2D distinguishability on valid CLASS cells.

Same added metric hypothesis and observable vector as v0.15.
Numerical-rejection handling is now local and objective:
- a rectangular cell is used iff all four CLASS corner cosmologies are valid;
- cells touching rejected points are excluded;
- no rejected point is interpolated;
- valid distant cells are never discarded because of an unrelated rejection.

Probability summaries are discrete quadrature over valid cells in
(log zeta, log Lambda) space. They are conditional on this valid-cell domain.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.15.2'
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
    except Exception as e:
        return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass

def weighted_cdf(values,weights,x):
    values=np.asarray(values); weights=np.asarray(weights); s=weights.sum()
    return float(weights[values<=x].sum()/s) if s>0 else np.nan

def weighted_median(values,weights):
    values=np.asarray(values); weights=np.asarray(weights)
    o=np.argsort(values); v=values[o]; w=weights[o]; c=np.cumsum(w)
    return float(v[np.searchsorted(c,0.5*c[-1])])

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

    uz=np.log(zgrid); ul=np.log(lgrid)
    cells=[]
    for i in range(nz-1):
        for j in range(nl-1):
            if not (valid[i,j] and valid[i+1,j] and valid[i,j+1] and valid[i+1,j+1]):
                continue
            du=uz[i+1]-uz[i]; dv=ul[j+1]-ul[j]
            # Cell-centred derivatives from opposite-edge averages. This uses only
            # the four valid corners and is symmetric under swapping cell edges.
            dF_du=((F[i+1,j]+F[i+1,j+1])-(F[i,j]+F[i,j+1]))/(2*du)
            dF_dv=((F[i,j+1]+F[i+1,j+1])-(F[i,j]+F[i+1,j]))/(2*dv)
            g11=float(np.dot(dF_du,dF_du)); g22=float(np.dot(dF_dv,dF_dv)); g12=float(np.dot(dF_du,dF_dv))
            dens=float(np.sqrt(max(g11*g22-g12*g12,0.0)))
            area=du*dv; mass=dens*area
            uc=.5*(uz[i]+uz[i+1]); vc=.5*(ul[j]+ul[j+1])
            cells.append((i,j,uc,vc,dens,area,mass))
    if not cells: raise RuntimeError('No fully valid cells available.')

    masses=np.array([c[6] for c in cells]); total_mass=float(masses.sum())
    if total_mass<=0: raise RuntimeError('Metric volume is zero on valid cells.')
    zcent=np.exp(np.array([c[2] for c in cells])); lcent=np.exp(np.array([c[3] for c in cells]))
    cz=weighted_cdf(zcent,masses,zeta_obs); cl=weighted_cdf(lcent,masses,1.0)
    mz=weighted_median(zcent,masses); ml=weighted_median(lcent,masses)

    # Observed-cell density: locate the unique cell containing (zeta_obs,1), if valid.
    uo=np.log(zeta_obs); vo=0.0; obs_cell=None
    for c in cells:
        i,j=c[0],c[1]
        if uz[i] <= uo <= uz[i+1] and ul[j] <= vo <= ul[j+1]:
            obs_cell=c; break
    if obs_cell is not None:
        pobs=obs_cell[4]
        low_density_mass=float(sum(c[6] for c in cells if c[4] <= pobs)/total_mass)
        obs_cell_status='valid'
    else:
        pobs=np.nan; low_density_mass=np.nan; obs_cell_status='unavailable because observed-containing cell touches a rejected CLASS point'

    with (OUT/'v0152_joint_valid_cells.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta_center','lambda_center','metric_density','log_area','metric_mass'])
        for c in cells: w.writerow([np.exp(c[2]),np.exp(c[3]),c[4],c[5],c[6]])
    with (OUT/'v0152_rejections.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','lambda_ratio','error'])
        for _,_,z,l,e in errors: w.writerow([z,l,e])

    total_cells=(nz-1)*(nl-1); valid_cells=len(cells)
    text=f'''CANEVAS v{VERSION} — JOINT 2D DISTINGUISHABILITY\n==================================================\nSame metric/observables as v0.15; no anthropic score.\nOriginal CLASS grid = {nz} x {nl} = {nz*nl} points\nCLASS rejected points = {len(errors)}\nPotential rectangular cells = {total_cells}\nFully valid cells used = {valid_cells}\nValid-cell fraction = {valid_cells/total_cells:.6f}\nAll probabilities are conditional on the valid-cell domain.\n\nzeta observed = {zeta_obs:.6f}\nzeta marginal cell-mass CDF at observed = {cz:.6f}\nzeta marginal weighted median = {mz:.6f}\n\nLambda observed ratio = 1\nLambda marginal cell-mass CDF at observed = {cl:.6f}\nLambda marginal weighted median = {ml:.6f}\n\nObserved-containing cell status = {obs_cell_status}\nObserved-cell lower-density probability mass = {low_density_mass:.6f}\n(when available: near 0.5 is ordinary; near 0 or 1 more special; NOT a p-value.)\n\nGUARDRAILS:\n- No rejected cosmology is interpolated.\n- Only cells touching rejected points are excluded.\n- Metric remains an added hypothesis, not derived from Canevas axioms.\n- Result remains conditional on finite bounds and chosen observable vector.\n'''
    (OUT/'v0152_joint_metric_summary.txt').write_text(text,encoding='utf8'); print('\n'+text+'\nFINISHED v0.15.2')
if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
