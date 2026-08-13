"""Canevas v0.22 — physical-compromise test for zeta = rho_cdm/rho_b.

Purpose
-------
Return to the one mechanism in the project that can produce a genuine interior
optimum for physical reasons: more CDM accelerates structure formation, while
more baryons provide more ordinary matter that can cool/participate in galaxies.

This is NOT a derivation from the Canevas axioms and NOT a galaxy-formation
simulation. It is a deliberately simple structure-formation proxy using CLASS +
Sheth-Tormen collapse. The important question is whether an interior optimum
survives several predeclared cosmic-time windows WITHOUT tuning those windows to
the observed zeta.

Predeclared failure criteria
----------------------------
1. A window whose optimum sits on its valid scan boundary is labelled BOUNDARY.
2. If valid interior optima vary by more than a factor 2 across windows, the
   physical optimum is labelled temporally fragile.
3. No failed/CLASS-rejected cosmology is interpolated.
4. The observed zeta is used only for post-hoc reporting, never in the score.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.22'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)

# Frozen background, same family used earlier.
h=0.674
Omega_m=0.315
omega_m=Omega_m*h*h
Omega_b_obs=0.0493
zeta_obs=(Omega_m-Omega_b_obs)/Omega_b_obs
A_s=2.10e-9
n_s=0.965
YHe=0.245
Omega_L=1.0-Omega_m

# Broad zeta scan; observed zeta is inserted only so its score can be reported
# exactly after the scan. It does not define spacing or score.
ZETA=np.unique(np.sort(np.r_[np.logspace(np.log10(1.5),np.log10(25.0),39),zeta_obs]))

# Common redshift grid; windows below were frozen before result inspection.
Z=np.array([12.,10.,8.,6.,5.,4.,3.,2.,1.,0.5])
WINDOWS={
    'early_12_to_6':(12.,6.),
    'broad_10_to_2':(10.,2.),
    'middle_8_to_2':(8.,2.),
    'late_6_to_0p5':(6.,0.5),
    'full_12_to_0p5':(12.,0.5),
}

# Matter-spectrum/HMF grid.
k=np.logspace(-4,np.log10(40.0),700) # 1/Mpc
M=np.logspace(7,14.5,300)            # Msun/h
lnM=np.log(M)
rho_m=Omega_m*2.775e11               # Msun/h /(Mpc/h)^3
G=6.67430e-8; kB=1.380649e-16; mp=1.6726219e-24
Msun=1.98847e33; Mpc=3.0856776e24; mu=0.59
H0_cgs=100*h*1e5/Mpc


def Ez(z): return np.sqrt(Omega_m*(1+z)**3+Omega_L)
def dt_dz_abs(z): return 1.0/((1+z)*H0_cgs*Ez(z))

def R_from_M(m): return (m/((4*np.pi/3)*rho_m))**(1/3)
R=R_from_M(M)

def Wtop(x):
    out=np.ones_like(x)
    m=np.abs(x)>1e-5
    y=x[m]; out[m]=3*(np.sin(y)-y*np.cos(y))/y**3
    out[~m]=1-x[~m]**2/10
    return out


def sigma_M(kh,Ph):
    lnk=np.log(kh); base=kh**3*Ph/(2*np.pi**2)*np.gradient(lnk)
    X=R[:,None]*kh[None,:]
    return np.sqrt(np.maximum((Wtop(X)**2)@base,0))


def st_mass_fraction(sig):
    # Sheth-Tormen multiplicity converted to mass fraction per dlnM.
    dc=1.686; A=0.3222; a=0.707; p=0.3
    s=np.maximum(sig,1e-30); nu=dc/s
    f=A*np.sqrt(2*a/np.pi)*nu*(1+(1/(a*nu**2))**p)*np.exp(-a*nu**2/2)
    dlninv=np.gradient(np.log(1/s),lnM)
    # d rho_halo / rho_m / dlnM = f * dln(sigma^-1)/dlnM
    return np.maximum(f*dlninv,0)


def atomic_cooling_mass(z):
    """Approximate halo mass whose virial temperature is 1e4 K.

    We compute it from the virial relation using Delta=200 rho_crit. This avoids
    inserting an empirical galaxy mass scale that could be tuned to zeta.
    Result returned in Msun/h to match M grid.
    """
    T=1e4
    H=H0_cgs*Ez(z); rho_c=3*H**2/(8*np.pi*G); rho_v=200*rho_c
    # T = mu mp/(2 kB) * G M / R, R=(3M/4pi rho_v)^(1/3)
    C=(mu*mp*G/(2*kB))*(4*np.pi*rho_v/3)**(1/3)
    Mcgs=(T/C)**1.5
    return (Mcgs/Msun)*h


def class_all_z(zeta):
    wb=omega_m/(1+zeta); wc=omega_m-wb
    c=Class()
    try:
        c.set({'output':'mPk','h':h,'omega_b':float(wb),'omega_cdm':float(wc),
               'A_s':A_s,'n_s':n_s,'YHe':YHe,'P_k_max_1/Mpc':40.,
               'z_max_pk':float(Z.max()+0.5)})
        c.compute()
        out=[]
        for z in Z:
            P=np.array([c.pk(float(ki),float(z)) for ki in k])
            kh=k/h; Ph=P*h**3
            sig=sigma_M(kh,Ph)
            frac_lnM=st_mass_fraction(sig)
            Mc=atomic_cooling_mass(float(z))
            mask=M>=Mc
            fcoll=float(np.trapezoid(frac_lnM[mask],lnM[mask])) if np.count_nonzero(mask)>1 else 0.0
            out.append(min(max(fcoll,0.0),1.0))
        return np.array(out),None
    except Exception as e:
        return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass


def window_score(zeta,fcoll,zhi,zlo):
    # Baryon-time proxy: integrate baryonic mass fraction resident in halos above
    # the atomic-cooling threshold over cosmic time. No observer weighting.
    fb=1/(1+zeta)
    sel=(Z<=zhi)&(Z>=zlo)
    zz=Z[sel]; ff=fcoll[sel]
    # sort ascending z for numerical integration; |dt/dz| is positive.
    o=np.argsort(zz); zz=zz[o]; ff=ff[o]
    integrand=fb*ff*np.array([dt_dz_abs(float(z)) for z in zz])
    return float(np.trapezoid(integrand,zz))


def run():
    print('='*74)
    print(f' CANEVAS v{VERSION} — PHYSICAL INTERIOR-OPTIMUM TEST')
    print('='*74)
    print(f'{len(ZETA)} zeta values x {len(Z)} redshifts; each zeta uses one CLASS cosmology.')
    print('Observed zeta is NOT used by the score.\n')

    data={}; errors=[]
    for i,zeta in enumerate(ZETA,1):
        print(f'[{i:2d}/{len(ZETA)}] zeta={zeta:.7f}',end=' ... ',flush=True)
        f,e=class_all_z(float(zeta))
        if f is None:
            print('REJECTED'); errors.append((zeta,e)); continue
        print('OK'); data[float(zeta)]=f

    if len(data)<8: raise RuntimeError('Too few valid zeta cosmologies.')
    valid=np.array(sorted(data.keys()))
    rows=[]; summaries=[]; interior_peaks=[]

    for name,(zhi,zlo) in WINDOWS.items():
        scores=np.array([window_score(z,data[z],zhi,zlo) for z in valid])
        imax=int(np.nanargmax(scores)); peak=float(valid[imax]); mx=float(scores[imax])
        boundary=(imax==0 or imax==len(valid)-1)
        if not boundary: interior_peaks.append(peak)
        obs_score=np.interp(np.log(zeta_obs),np.log(valid),scores) if valid.min()<=zeta_obs<=valid.max() else np.nan
        ratio=float(obs_score/mx) if mx>0 and np.isfinite(obs_score) else np.nan
        summaries.append((name,zhi,zlo,peak,boundary,ratio))
        print(f'{name:18s} peak={peak:.6f}  {"BOUNDARY" if boundary else "INTERIOR"}  obs/peak={ratio:.6f}')
        for z,s in zip(valid,scores): rows.append((name,zhi,zlo,z,s))

    if len(interior_peaks)>=2:
        spread=max(interior_peaks)/min(interior_peaks)
        temporal='ROBUST' if spread<=2 else 'FRAGILE'
    elif len(interior_peaks)==1:
        spread=np.nan; temporal='INSUFFICIENT_INTERIOR_WINDOWS'
    else:
        spread=np.nan; temporal='NO_INTERIOR_OPTIMUM'

    with (OUT/'v022_physical_compromise_scores.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['window','z_high','z_low','zeta','baryon_time_score']); w.writerows(rows)
    with (OUT/'v022_class_rejections.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','error']); w.writerows(errors)

    lines=[f'CANEVAS v{VERSION} — PHYSICAL COMPROMISE SUMMARY', '='*52,
           'No distinguishability measure. No anthropic score. No observed-zeta tuning.',
           f'Observed zeta (reporting only) = {zeta_obs:.8f}',
           f'Valid CLASS zeta range = [{valid.min():.8f}, {valid.max():.8f}]',
           f'CLASS rejected zeta points = {len(errors)}','']
    for name,zhi,zlo,peak,boundary,ratio in summaries:
        lines.append(f'{name}: peak={peak:.8f}; status={"BOUNDARY" if boundary else "INTERIOR"}; observed/peak={ratio:.8f}')
    lines += ['',f'Interior-peak temporal spread factor = {spread}',f'PREDECLARED TEMPORAL VERDICT = {temporal}','',
              'INTERPRETATION LOCK:',
              '- Boundary maxima do not count as evidence for a selected finite zeta.',
              '- Interior maxima count only as a physical proxy result, not as evidence for Canevas.',
              '- Strong movement across time windows means the optimum is not universal.',
              '- No post-run window may be selected merely because it matches the observed zeta.']
    text='\n'.join(lines)+'\n'
    (OUT/'v022_physical_compromise_summary.txt').write_text(text,encoding='utf8')
    print('\n'+text+'\nFINISHED v0.22')

if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
