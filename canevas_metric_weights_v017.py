"""Canevas v0.17 — robustness of the joint distinguishability metric to W.

Goal
----
Test whether the v0.15.2 result depends strongly on how components of the
observable vector are weighted. CLASS is run once on the same 2D grid. Multiple
predeclared W choices are then evaluated on exactly the same valid cells.

This does NOT derive W from the Canevas axioms. It is a falsification-oriented
robustness test of a family of relational/distinguishability metrics.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.17'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
h_ref=.674; Om=.315; Ob=.0493; wm=Om*h_ref**2; wb_obs=Ob*h_ref**2
zeta_obs=(wm-wb_obs)/wb_obs; wL_obs=(1-Om)*h_ref**2
As=2.10e-9; ns=.965; YHe=.245
zgrid=np.unique(np.sort(np.r_[np.logspace(np.log10(2.5),np.log10(15),19),zeta_obs]))
lgrid=np.unique(np.sort(np.r_[np.logspace(np.log10(.1),np.log10(6.),19),1.0]))
ks=np.logspace(-2,0.7,8); zs=[0.,2.,6.]

# Feature layout per redshift: 8 log P(k) entries + 1 log H entry.
NPK=len(ks); BLOCK=NPK+1; NF=BLOCK*len(zs)
idx_pk=np.array([b*BLOCK+i for b in range(len(zs)) for i in range(NPK)],int)
idx_h=np.array([b*BLOCK+NPK for b in range(len(zs))],int)
idx_z={z:np.arange(b*BLOCK,(b+1)*BLOCK) for b,z in enumerate(zs)}
idx_pk_z={z:np.arange(b*BLOCK,b*BLOCK+NPK) for b,z in enumerate(zs)}
idx_lowk=np.array([b*BLOCK+i for b in range(len(zs)) for i in range(NPK//2)],int)
idx_highk=np.array([b*BLOCK+i for b in range(len(zs)) for i in range(NPK//2,NPK)],int)

def features(zeta,lr):
    wb=wm/(1+zeta); wc=wm-wb; wL=wL_obs*lr; h=float(np.sqrt(wm+wL))
    c=Class()
    try:
        c.set({'output':'mPk','h':h,'omega_b':float(wb),'omega_cdm':float(wc),
               'A_s':As,'n_s':ns,'YHe':YHe,'P_k_max_1/Mpc':6.,'z_max_pk':6.5})
        c.compute(); f=[]
        for z in zs:
            for k in ks: f.append(np.log(max(c.pk(float(k),z),1e-300)))
            f.append(np.log(np.sqrt(wm*(1+z)**3+wL)))
        return np.asarray(f,float),None
    except Exception as e:
        return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass

def diagW(indices,scale=1.0):
    w=np.zeros(NF); w[np.asarray(indices,int)]=scale
    return np.diag(w)

def weighted_cdf(values,weights,x):
    values=np.asarray(values); weights=np.asarray(weights); s=weights.sum()
    return float(weights[values<=x].sum()/s) if s>0 else np.nan

def weighted_median(values,weights):
    values=np.asarray(values); weights=np.asarray(weights); s=weights.sum()
    if s<=0:return np.nan
    o=np.argsort(values); v=values[o]; w=weights[o]; c=np.cumsum(w)
    return float(v[np.searchsorted(c,0.5*c[-1])])

def metric_stats(celldata,W):
    rows=[]
    for c in celldata:
        a,b=c['du'],c['dv']
        g11=float(a@W@a); g22=float(b@W@b); g12=float(a@W@b)
        det=g11*g22-g12*g12
        dens=float(np.sqrt(max(det,0.0)))
        mass=dens*c['area']
        rows.append((c,dens,mass))
    masses=np.array([r[2] for r in rows]); total=masses.sum()
    if not np.isfinite(total) or total<=1e-14:
        return None,'degenerate/zero metric volume'
    zc=np.array([r[0]['zc'] for r in rows]); lc=np.array([r[0]['lc'] for r in rows])
    cz=weighted_cdf(zc,masses,zeta_obs); cl=weighted_cdf(lc,masses,1.0)
    mz=weighted_median(zc,masses); ml=weighted_median(lc,masses)
    # Joint lower-density mass using observed-containing valid cell.
    obs=[r for r in rows if r[0]['contains_obs']]
    if obs:
        d0=obs[0][1]; joint=float(sum(m for _,d,m in rows if d<=d0)/total)
    else: joint=np.nan
    return {'cz':cz,'cl':cl,'mz':mz,'ml':ml,'joint':joint,'total':float(total)},None

def run():
    nz,nl=len(zgrid),len(lgrid); F=None; valid=np.zeros((nz,nl),bool); errors=[]
    total=nz*nl; n=0
    print(f'CANEVAS v{VERSION} — W ROBUSTNESS TEST')
    print('CLASS cosmologies are computed once; W variants are applied afterward.\n')
    for i,zeta in enumerate(zgrid):
        for j,lr in enumerate(lgrid):
            n+=1; print(f'[{n:3d}/{total}] zeta={zeta:.5g}, lambda={lr:.5g}',end=' ... ',flush=True)
            f,e=features(float(zeta),float(lr))
            if f is None:
                print('REJECTED'); errors.append((i,j,zeta,lr,e)); continue
            print('OK')
            if F is None:F=np.full((nz,nl,len(f)),np.nan)
            F[i,j]=f; valid[i,j]=True
    if F is None: raise RuntimeError('No valid CLASS points.')

    uz=np.log(zgrid); ul=np.log(lgrid); uo=np.log(zeta_obs); vo=0.0
    cells=[]
    for i in range(nz-1):
        for j in range(nl-1):
            if not (valid[i,j] and valid[i+1,j] and valid[i,j+1] and valid[i+1,j+1]):continue
            du0=uz[i+1]-uz[i]; dv0=ul[j+1]-ul[j]
            dFdu=((F[i+1,j]+F[i+1,j+1])-(F[i,j]+F[i,j+1]))/(2*du0)
            dFdv=((F[i,j+1]+F[i+1,j+1])-(F[i,j]+F[i+1,j]))/(2*dv0)
            cells.append({'du':dFdu,'dv':dFdv,'area':du0*dv0,
                          'zc':float(np.exp(.5*(uz[i]+uz[i+1]))),
                          'lc':float(np.exp(.5*(ul[j]+ul[j+1]))),
                          'contains_obs':bool(uz[i]<=uo<=uz[i+1] and ul[j]<=vo<=ul[j+1])})
    if not cells:raise RuntimeError('No fully valid cells.')

    # Predeclared W family. Subset variants use unit weights on selected features.
    variants={
      'identity_all':np.eye(NF),
      'pk_only':diagW(idx_pk),
      'z0_all':diagW(idx_z[0.]),
      'z2_all':diagW(idx_z[2.]),
      'z6_all':diagW(idx_z[6.]),
      'z0_pk_only':diagW(idx_pk_z[0.]),
      'z2_pk_only':diagW(idx_pk_z[2.]),
      'z6_pk_only':diagW(idx_pk_z[6.]),
      'low_k_pk':diagW(idx_lowk),
      'high_k_pk':diagW(idx_highk),
    }
    # Fixed epoch emphasis, still diagonal and independent of observed parameter location.
    for name,weights in {
        'late_emphasis':{0.:4.0,2.:2.0,6.:1.0},
        'early_emphasis':{0.:1.0,2.:2.0,6.:4.0},
    }.items():
        w=np.zeros(NF)
        for z,mult in weights.items():w[idx_z[z]]=mult
        variants[name]=np.diag(w)

    # Covariance-whitened alternative. This is explicitly scan-dependent and is
    # tested as a harsh alternative, not claimed as derived. Use valid grid points only.
    FV=F[valid]
    C=np.cov(FV,rowvar=False)
    ridge=1e-6*max(float(np.trace(C)/NF),1e-12)
    variants['covariance_whitened']=np.linalg.pinv(C+ridge*np.eye(NF),rcond=1e-10)

    results=[]
    for name,W in variants.items():
        s,err=metric_stats(cells,W)
        if s is None:
            print(f'{name:24s} DEGENERATE: {err}')
            results.append({'variant':name,'status':'degenerate','zeta_cdf':'','zeta_median':'','lambda_cdf':'','lambda_median':'','joint_low_density_mass':'','note':err})
        else:
            print(f"{name:24s} zetaCDF={s['cz']:.4f} lambdaCDF={s['cl']:.4f} joint={s['joint']:.4f}")
            results.append({'variant':name,'status':'ok','zeta_cdf':s['cz'],'zeta_median':s['mz'],'lambda_cdf':s['cl'],'lambda_median':s['ml'],'joint_low_density_mass':s['joint'],'note':''})

    with (OUT/'v017_weight_robustness.csv').open('w',newline='',encoding='utf8') as f:
        fields=list(results[0].keys()); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(results)
    ok=[r for r in results if r['status']=='ok']
    zc=np.array([float(r['zeta_cdf']) for r in ok]); lc=np.array([float(r['lambda_cdf']) for r in ok]); jc=np.array([float(r['joint_low_density_mass']) for r in ok if np.isfinite(float(r['joint_low_density_mass']))])
    def q(a,p):return float(np.quantile(a,p)) if len(a) else np.nan
    text=f'''CANEVAS v{VERSION} — METRIC-W ROBUSTNESS SUMMARY\n=================================================\nMetric family test; no anthropic score.\nCLASS grid points = {nz*nl}\nCLASS rejected points = {len(errors)}\nFully valid cells reused = {len(cells)} / {(nz-1)*(nl-1)}\nW variants declared = {len(results)}\nNondegenerate variants = {len(ok)}\n\nZETA observed = {zeta_obs:.6f}\nCDF median across W = {q(zc,.5):.6f}\nCDF 10-90% across W = [{q(zc,.1):.6f}, {q(zc,.9):.6f}]\nfraction W with zeta CDF in [0.25,0.75] = {np.mean((zc>=.25)&(zc<=.75)):.6f}\n\nLAMBDA observed ratio = 1\nCDF median across W = {q(lc,.5):.6f}\nCDF 10-90% across W = [{q(lc,.1):.6f}, {q(lc,.9):.6f}]\nfraction W with Lambda CDF in [0.10,0.90] = {np.mean((lc>=.10)&(lc<=.90)):.6f}\n\nJOINT observed-cell lower-density mass\nmedian across W = {q(jc,.5):.6f}\n10-90% across W = [{q(jc,.1):.6f}, {q(jc,.9):.6f}]\nfraction W with joint mass in [0.10,0.90] = {np.mean((jc>=.10)&(jc<=.90)):.6f}\n\nGUARDRAILS:\n- W is still not derived uniquely from Canevas axioms.\n- The covariance-whitened case is scan-dependent and is only a stress test.\n- Degenerate variants are reported, not repaired.\n- Results remain conditional on finite parameter bounds, CLASS validity, and the chosen observable family.\n'''
    (OUT/'v017_weight_robustness_summary.txt').write_text(text,encoding='utf8')
    print('\n'+text+'\nFINISHED v0.17')
if __name__=='__main__':
    try:run()
    except Exception:traceback.print_exc()
