from pathlib import Path
import csv, math, traceback
import numpy as np
from classy import Class

VERSION='ZETA-T1'
OUTDIR=Path(__file__).resolve().parent/'results'; OUTDIR.mkdir(exist_ok=True)

h=0.674
Omega_m=0.315
omega_m=Omega_m*h*h
Omega_L=1.0-Omega_m
A_s=2.10e-9
n_s=0.965
YHe=0.245
zeta_obs=5.389452

G=6.67430e-8; kB=1.380649e-16; mp=1.6726219e-24
Msun=1.98847e33; Mpc=3.0856776e24; mu=0.59; delta_c=1.686
rho_m_phys=omega_m*2.775e11
Mgrid=np.logspace(7,15,320); lnM=np.log(Mgrid); dlnM=np.gradient(lnM)
kgrid=np.logspace(-4,np.log10(50.0),700)
redshifts=np.array([12.,10.,8.,6.,4.,3.,2.,1.,0.5,0.])
zeta_grid=np.unique(np.sort(np.append(np.logspace(np.log10(0.5),np.log10(30.0),49),1.0)))

def W(x):
    x=np.asarray(x); out=np.ones_like(x); m=np.abs(x)>1e-5; y=x[m]
    out[m]=3*(np.sin(y)-y*np.cos(y))/y**3; out[~m]=1-x[~m]**2/10
    return out

def sigma_M(Pk):
    lnk=np.log(kgrid); dlnk=np.gradient(lnk)
    base=kgrid**3*Pk/(2*np.pi**2)*dlnk
    X=Rgrid[:,None]*kgrid[None,:]
    return np.sqrt(np.maximum((W(X)**2)@base,0))

def hmf_ST(sig):
    A0,aa,p=0.3222,0.707,0.3
    s=np.maximum(sig,1e-30); nu=delta_c/s
    f=A0*np.sqrt(2*aa/np.pi)*nu*(1+(1/(aa*nu**2))**p)*np.exp(-aa*nu**2/2)
    deriv=np.gradient(np.log(1/s),lnM)
    return np.maximum(rho_m_phys/Mgrid*f*deriv,0)

def coolfunc(T):
    safe=np.maximum(np.asarray(T),1)
    line=1.2e-22*np.exp(-((np.log10(safe)-5.25)/0.75)**2)
    gate=1/(1+np.exp(-(np.log10(safe)-4.0)*20))
    brem=1.4e-27*np.sqrt(safe)
    return gate*line+brem

def H_cgs(z):
    return 100*h*np.sqrt(Omega_m*(1+z)**3+Omega_L)*1e5/Mpc

def rho_crit(z):
    H=H_cgs(z); return 3*H*H/(8*np.pi*G)

def cooling_eff(z,fb):
    Mcgs=Mgrid*Msun; rh=200*rho_crit(z)
    Rv=(3*Mcgs/(4*np.pi*rh))**(1/3); V=np.sqrt(G*Mcgs/Rv)
    T=mu*mp*V**2/(2*kB); tdyn=Rv/V; n=fb*rh/(mu*mp)
    tcool=1.5*kB*T/(np.maximum(n,1e-100)*np.maximum(coolfunc(T),1e-100))
    eff=1/(1+tcool/tdyn)
    return np.where(T>=1e4,eff,0.0)

def class_spectra(zeta):
    omega_b=omega_m/(1+zeta); omega_cdm=omega_m-omega_b
    params={'output':'mPk','h':h,'omega_b':omega_b,'omega_cdm':omega_cdm,
            'A_s':A_s,'n_s':n_s,'YHe':YHe,'P_k_max_1/Mpc':50.0,
            'z_max_pk':float(redshifts.max()+0.5)}
    c=Class()
    try:
        c.set(params); c.compute()
        spectra={float(z):np.array([c.pk(float(k),float(z)) for k in kgrid]) for z in redshifts}
        return spectra,omega_b,omega_cdm,None
    except Exception as e:
        return None,omega_b,omega_cdm,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try:c.struct_cleanup(); c.empty()
        except Exception:pass

def cosmic_time_grid_seconds():
    # integrate dt/dz from high z to each grid endpoint; only interval differences matter
    zfine=np.linspace(0,redshifts.max(),20000)
    integ=1/((1+zfine)*np.array([H_cgs(z) for z in zfine]))
    # t_since_bigbang proxy over finite z range: cumulative from zmax down
    # easier: compute lookback from 0 then reverse via interpolation
    dz=zfine[1]-zfine[0]
    cum=np.concatenate([[0],np.cumsum(0.5*(integ[:-1]+integ[1:])*dz)])
    lookback=np.interp(redshifts,zfine,cum)
    return -lookback  # monotonic increasing with cosmic time as z decreases after sort

def score_epoch(Pk,z,fb):
    sig=sigma_M(Pk); hmf=hmf_ST(sig); eff=cooling_eff(z,fb)
    return fb*np.sum(Mgrid*hmf*eff*dlnM)/rho_m_phys

Rgrid=(Mgrid/((4*np.pi/3)*rho_m_phys))**(1/3)

def main():
    print('='*78); print('CANEVAS + CLASS ZETA-T1 — TIME-INTEGRATED COOLING-BARYON SCORE'); print('='*78)
    print(f'fixed h={h}, Omega_m={Omega_m}, omega_m={omega_m:.8f}')
    print(f'zeta scan points={len(zeta_grid)} range=[{zeta_grid.min():.3f},{zeta_grid.max():.3f}]')
    print('Observed zeta is not used in score construction.\n')
    rows=[]; summaries=[]
    # cosmic time ordering: redshifts listed descending, t coordinate increasing
    t=-cosmic_time_grid_seconds()  # lookback positive; descending z means descending lookback? make explicit below
    # use actual age-like coordinate relative to z=12: t_age = max(lookback)-lookback
    lookback=t
    tage=np.max(lookback)-lookback
    for i,zeta in enumerate(zeta_grid,1):
        print(f'[{i:2d}/{len(zeta_grid)}] zeta={zeta:.6g}',end=' ... ',flush=True)
        sp,ob,oc,err=class_spectra(float(zeta))
        if sp is None:
            print('REJECTED'); summaries.append((zeta,np.nan,'rejected'))
            rows.append({'zeta':zeta,'z':'','omega_b':ob,'omega_cdm':oc,'fcool':'','status':'rejected','error':err})
            continue
        fb=ob/omega_m; vals=[]
        for z in redshifts:
            s=score_epoch(sp[float(z)],float(z),fb); vals.append(s)
            rows.append({'zeta':zeta,'z':z,'omega_b':ob,'omega_cdm':oc,'fcool':s,'status':'ok','error':''})
        vals=np.array(vals)
        order=np.argsort(tage); J=float(np.trapezoid(vals[order],tage[order]))
        summaries.append((zeta,J,'ok')); print('OK')
    with (OUTDIR/'zeta_t1_epoch_scores.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['zeta','z','omega_b','omega_cdm','fcool','status','error']); w.writeheader(); w.writerows(rows)
    valid=np.array([(z,s) for z,s,status in summaries if status=='ok' and np.isfinite(s)],float)
    if len(valid)<5: raise RuntimeError('Too few valid zeta points')
    x=valid[:,0]; J=valid[:,1]; o=np.argsort(x); x=x[o]; J=J[o]
    imax=int(np.argmax(J)); pred=float(x[imax]); boundary=(imax==0 or imax==len(x)-1)
    Jrel=J/np.max(J); obsrel=float(np.interp(zeta_obs,x,Jrel)) if x.min()<=zeta_obs<=x.max() else float('nan')
    dist=max(pred/zeta_obs,zeta_obs/pred)
    if boundary: verdict='BOUNDARY_NO_FINITE_SELECTION'
    elif dist<=1.25: verdict='CLOSE_NUMERICAL_OVERLAP'
    elif dist<=2.0: verdict='BROAD_ORDER_OVERLAP'
    else: verdict='NO_CLOSE_OVERLAP'
    with (OUTDIR/'zeta_t1_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['zeta','J','J_relative']);
        for a,b,c in zip(x,J,Jrel): w.writerow([a,b,c])
    print('\nPREDECLARED ZETA-T1 RESULT')
    print(f'zeta_pred = {pred:.6f}')
    print(f'peak_is_boundary = {boundary}')
    print(f'observed zeta reporting-only = {zeta_obs:.6f}')
    print(f'score_at_observed_over_peak = {obsrel:.6f}')
    print(f'multiplicative_distance_pred_vs_obs = {dist:.6f}x')
    print('PREDECLARED ZETA-T1 VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- This is one non-anthropic proxy: cooling-capable baryon-time, not life or consciousness.')
    print('- No epoch was selected after seeing observation.')
    print('- A numerical overlap is not proof of Canevas and requires preregistered robustness tests.')
    print('- A boundary/mismatch is retained and not repaired under T1.')
    print('\nFINISHED ZETA-T1 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    try: main()
    except Exception:
        traceback.print_exc(); raise
