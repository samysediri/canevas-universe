"""Canevas v0.23 — physically defined maturation-window test.

Purpose
-------
Replace arbitrary redshift windows with a simple physical clock.  A parcel of
baryonic matter is counted only after it first enters an atomic-cooling halo and
has then had a fixed maturation delay tau.  The delay is varied over a
predeclared family (0, 0.5, 1, 2, 4 Gyr).  No observed zeta enters the score.

This is still a toy astrophysical proxy, not a derivation from the Canevas
axioms and not a realistic star-formation/metallicity model.

Predeclared interpretation
--------------------------
- Boundary maxima do not count as a finite physical selection.
- Interior peaks that move by > factor 2 across delay variants are fragile.
- No delay may be selected post hoc because it matches observed zeta.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.23'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)

h=0.674; Omega_m=0.315; Omega_b_obs=0.0493
omega_m=Omega_m*h*h; Omega_L=1-Omega_m
zeta_obs=(Omega_m-Omega_b_obs)/Omega_b_obs
A_s=2.10e-9; n_s=0.965; YHe=0.245

ZETA=np.unique(np.sort(np.r_[np.logspace(np.log10(1.5),np.log10(25.0),39),zeta_obs]))
# Dense cosmic history; no special epoch selected from observed zeta.
Z=np.array([20.,16.,14.,12.,10.,8.,7.,6.,5.,4.,3.,2.,1.5,1.,0.7,0.5,0.3,0.1,0.0])
DELAYS_GYR=[0.0,0.5,1.0,2.0,4.0]

k=np.logspace(-4,np.log10(40.0),700)
M=np.logspace(7,14.5,300); lnM=np.log(M)
rho_m=Omega_m*2.775e11
G=6.67430e-8; kB=1.380649e-16; mp=1.6726219e-24
Msun=1.98847e33; Mpc=3.0856776e24; mu=0.59
H0_cgs=100*h*1e5/Mpc
SEC_PER_GYR=3.15576e16

def Ez(z): return np.sqrt(Omega_m*(1+z)**3+Omega_L)
def dt_dz_abs(z): return 1/((1+z)*H0_cgs*Ez(z))

def cosmic_time_gyr(z):
    # Exact flat matter+Lambda age formula, radiation neglected consistently
    # with this late-time toy model.
    a=1/(1+z)
    pref=2/(3*H0_cgs*np.sqrt(Omega_L))
    return pref*np.arcsinh(np.sqrt(Omega_L/Omega_m)*a**1.5)/SEC_PER_GYR

def R_from_M(m): return (m/((4*np.pi/3)*rho_m))**(1/3)
R=R_from_M(M)

def Wtop(x):
    out=np.ones_like(x); q=np.abs(x)>1e-5
    y=x[q]; out[q]=3*(np.sin(y)-y*np.cos(y))/y**3
    out[~q]=1-x[~q]**2/10
    return out

def sigma_M(kh,Ph):
    lnk=np.log(kh); base=kh**3*Ph/(2*np.pi**2)*np.gradient(lnk)
    X=R[:,None]*kh[None,:]
    return np.sqrt(np.maximum((Wtop(X)**2)@base,0))

def st_mass_fraction(sig):
    dc=1.686; A=0.3222; a=0.707; p=0.3
    s=np.maximum(sig,1e-30); nu=dc/s
    f=A*np.sqrt(2*a/np.pi)*nu*(1+(1/(a*nu**2))**p)*np.exp(-a*nu**2/2)
    dlninv=np.gradient(np.log(1/s),lnM)
    return np.maximum(f*dlninv,0)

def atomic_cooling_mass(z):
    T=1e4; H=H0_cgs*Ez(z); rho_c=3*H**2/(8*np.pi*G); rho_v=200*rho_c
    C=(mu*mp*G/(2*kB))*(4*np.pi*rho_v/3)**(1/3)
    Mcgs=(T/C)**1.5
    return (Mcgs/Msun)*h

def class_history(zeta):
    wb=omega_m/(1+zeta); wc=omega_m-wb
    c=Class()
    try:
        c.set({'output':'mPk','h':h,'omega_b':float(wb),'omega_cdm':float(wc),
               'A_s':A_s,'n_s':n_s,'YHe':YHe,'P_k_max_1/Mpc':40.,
               'z_max_pk':float(Z.max()+0.5)})
        c.compute(); fcoll=[]
        for z in Z:
            P=np.array([c.pk(float(ki),float(z)) for ki in k])
            kh=k/h; Ph=P*h**3
            frac=st_mass_fraction(sigma_M(kh,Ph))
            mask=M>=atomic_cooling_mass(float(z))
            val=float(np.trapezoid(frac[mask],lnM[mask])) if np.count_nonzero(mask)>1 else 0.0
            fcoll.append(min(max(val,0.0),1.0))
        return np.asarray(fcoll),None
    except Exception as e:
        return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass

def maturation_score(zeta,fcoll,tau_gyr):
    # Sort forward in cosmic time.  Count only *newly collapsed* mass, avoiding
    # repeatedly crediting the same baryons at every epoch.
    t=np.array([cosmic_time_gyr(float(z)) for z in Z])
    o=np.argsort(t); t=t[o]; f=np.asarray(fcoll)[o]
    # Positive increments in collapse fraction are interpreted as newly entering
    # eligible atomic-cooling halos. Negative numerical/merger excursions do not
    # create negative observers and are clipped to zero.
    df=np.r_[max(f[0],0.0), np.maximum(np.diff(f),0.0)]
    t0=float(t.max())
    mature_time=np.maximum(t0-t-tau_gyr,0.0)
    fb=1/(1+zeta)
    # Baryonic mass newly made eligible times the amount of post-delay cosmic
    # time available. Units are arbitrary; only relative zeta dependence matters.
    return float(fb*np.sum(df*mature_time))

def run():
    print('='*76)
    print(f' CANEVAS v{VERSION} — PHYSICAL MATURATION-CLOCK TEST')
    print('='*76)
    print(f'{len(ZETA)} zeta cosmologies; delays = {DELAYS_GYR} Gyr')
    print('Observed zeta is reporting-only.\n')

    data={}; errors=[]
    for i,zeta in enumerate(ZETA,1):
        print(f'[{i:2d}/{len(ZETA)}] zeta={zeta:.7f}',end=' ... ',flush=True)
        f,e=class_history(float(zeta))
        if f is None:
            print('REJECTED'); errors.append((zeta,e)); continue
        print('OK'); data[float(zeta)]=f
    if len(data)<8: raise RuntimeError('Too few valid CLASS cosmologies.')

    valid=np.array(sorted(data.keys())); rows=[]; summaries=[]; interior=[]
    for tau in DELAYS_GYR:
        scores=np.array([maturation_score(z,data[z],tau) for z in valid])
        im=int(np.nanargmax(scores)); peak=float(valid[im]); mx=float(scores[im])
        boundary=(im==0 or im==len(valid)-1)
        if not boundary: interior.append(peak)
        obs=float(np.interp(np.log(zeta_obs),np.log(valid),scores)) if valid.min()<=zeta_obs<=valid.max() else np.nan
        ratio=obs/mx if mx>0 and np.isfinite(obs) else np.nan
        summaries.append((tau,peak,boundary,ratio))
        print(f'delay={tau:4.1f} Gyr  peak={peak:.6f}  {"BOUNDARY" if boundary else "INTERIOR"}  obs/peak={ratio:.6f}')
        for z,s in zip(valid,scores): rows.append((tau,z,s))

    if len(interior)>=2:
        spread=max(interior)/min(interior)
        verdict='ROBUST' if spread<=2 else 'FRAGILE'
    elif len(interior)==1:
        spread=np.nan; verdict='INSUFFICIENT_INTERIOR_VARIANTS'
    else:
        spread=np.nan; verdict='NO_INTERIOR_OPTIMUM'

    with (OUT/'v023_maturation_scores.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['delay_Gyr','zeta','matured_baryon_time_score']); w.writerows(rows)
    with (OUT/'v023_rejections.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','error']); w.writerows(errors)

    lines=[f'CANEVAS v{VERSION} — PHYSICAL MATURATION SUMMARY','='*55,
           'No distinguishability measure. No anthropic score. No observed-zeta tuning.',
           'Temporal weighting is generated by a physical maturation delay, not a chosen redshift window.',
           f'Observed zeta (reporting only) = {zeta_obs:.8f}',
           f'Valid CLASS zeta range = [{valid.min():.8f}, {valid.max():.8f}]',
           f'CLASS rejected zeta points = {len(errors)}','']
    for tau,peak,boundary,ratio in summaries:
        lines.append(f'delay={tau:.1f} Gyr: peak={peak:.8f}; status={"BOUNDARY" if boundary else "INTERIOR"}; observed/peak={ratio:.8f}')
    lines += ['',f'Interior-peak spread factor = {spread}',f'PREDECLARED MATURATION VERDICT = {verdict}','',
              'INTERPRETATION LOCK:',
              '- A delay producing agreement cannot be selected post hoc.',
              '- Boundary maxima are not finite-selection evidence.',
              '- Stable interior peaks support only this physical compromise proxy, not Canevas.',
              '- Strong delay dependence means the optimum is not uniquely selected by this clock.']
    text='\n'.join(lines)+'\n'
    (OUT/'v023_maturation_summary.txt').write_text(text,encoding='utf8')
    print('\n'+text+'\nFINISHED v0.23')

if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
