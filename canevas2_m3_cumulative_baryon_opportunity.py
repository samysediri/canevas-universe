"""CANEVAS 2.0 M3 — CUMULATIVE BARYON OPPORTUNITY v1

PREREGISTERED BEFORE OUTPUT.

Goal
----
Eliminate arbitrary epoch weighting. For each zeta = rho_cdm/rho_b cosmology,
compute a full collapse history from z=20 to z=0 and count only positive NEW
increments of mass entering atomic-cooling halos. Each increment is counted once.
The score is therefore a cumulative baryonic opportunity mass, not a snapshot
average and not an observer probability.

Observed zeta is intentionally absent from the score, scan construction, and
verdict. It is not printed anywhere in this script.

Physical interpretation
-----------------------
More CDM can accelerate/supply structure formation; more baryons increase ordinary
matter available inside eligible halos. The score tests only whether this simple
competition produces a stable finite interior optimum.

This is still a simplified CLASS + Sheth-Tormen proxy, not a galaxy-formation model
and not evidence for Canevas by itself.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='C2-M3-v1'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)

# Frozen background; no observed-zeta quantity is defined.
h=0.674
Omega_m=0.315
omega_m=Omega_m*h*h
Omega_L=1.0-Omega_m
A_s=2.10e-9
n_s=0.965
YHe=0.245

# Frozen blind zeta grid. Endpoints are broad sensitivity limits, not chosen from observation.
ZETA=np.logspace(np.log10(1.5),np.log10(25.0),49)
Z=np.array([20.,18.,16.,14.,12.,10.,9.,8.,7.,6.,5.,4.,3.,2.5,2.,1.5,1.,0.7,0.5,0.3,0.1,0.0])

k=np.logspace(-4,np.log10(40.0),700)
M=np.logspace(7,14.5,300); lnM=np.log(M)
rho_m=Omega_m*2.775e11
G=6.67430e-8; kB=1.380649e-16; mp=1.6726219e-24
Msun=1.98847e33; Mpc=3.0856776e24; mu=0.59
H0_cgs=100*h*1e5/Mpc


def Ez(z): return np.sqrt(Omega_m*(1+z)**3+Omega_L)
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
    T=1e4
    H=H0_cgs*Ez(z); rho_c=3*H**2/(8*np.pi*G); rho_v=200*rho_c
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

def score_cumulative(zeta,fcoll):
    # Z is descending (early -> late). Count each positive increment once.
    f=np.asarray(fcoll,float)
    df=np.r_[max(f[0],0.0), np.maximum(np.diff(f),0.0)]
    fb=1.0/(1.0+zeta)
    return float(fb*np.sum(df))

def run():
    print('='*80)
    print('CANEVAS 2.0 M3 — CUMULATIVE BARYON OPPORTUNITY v1')
    print('='*80)
    print('Observed zeta is absent from this calculation and is not printed.')
    print(f'{len(ZETA)} blind zeta cosmologies x {len(Z)} epochs.\n')

    rows=[]; errors=[]
    for i,zeta in enumerate(ZETA,1):
        print(f'[{i:2d}/{len(ZETA)}] zeta={zeta:.7f}',end=' ... ',flush=True)
        hist,e=class_history(float(zeta))
        if hist is None:
            print('REJECTED'); errors.append((zeta,e)); continue
        s=score_cumulative(float(zeta),hist)
        rows.append((float(zeta),s))
        print(f'OK score={s:.8e}')

    if len(rows)<20: raise RuntimeError('Too few valid cosmologies for M3.')
    z=np.array([r[0] for r in rows]); s=np.array([r[1] for r in rows])
    im=int(np.nanargmax(s)); peak=float(z[im]); mx=float(s[im])
    boundary=(im==0 or im==len(z)-1)

    # Predeclared shape checks around the maximum.
    left_ok = im>=2 and np.all(np.diff(s[:im+1])>=-1e-12)
    right_ok = im<=len(s)-3 and np.all(np.diff(s[im:])<=1e-12)
    finite_selection=(not boundary) and left_ok and right_ok

    # Grid-stability diagnostic: recompute max after taking every second valid point.
    z2=z[::2]; s2=s[::2]; peak2=float(z2[int(np.nanargmax(s2))])
    peak_grid_factor=max(peak,peak2)/min(peak,peak2)

    with (OUT/'c2_m3_cumulative_baryon_scores.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','cumulative_baryon_opportunity']); w.writerows(rows)
    with (OUT/'c2_m3_rejections.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','error']); w.writerows(errors)

    if finite_selection and peak_grid_factor<=1.25:
        verdict='BLIND_PHYSICAL_PROXY_HAS_STABLE_INTERIOR_ZETA_OPTIMUM'
    elif boundary:
        verdict='BLIND_PHYSICAL_PROXY_MAXIMUM_IS_SCAN_BOUNDARY'
    else:
        verdict='BLIND_PHYSICAL_PROXY_NO_STABLE_UNIMODAL_INTERIOR_OPTIMUM'

    print('\nC2-M3 SUMMARY')
    print(f'valid cosmologies = {len(rows)}')
    print(f'peak_zeta_blind = {peak:.8f}')
    print(f'peak_score = {mx:.8e}')
    print(f'peak_is_boundary = {boundary}')
    print(f'monotonic_rise_to_peak = {left_ok}')
    print(f'monotonic_fall_after_peak = {right_ok}')
    print(f'half_grid_peak = {peak2:.8f}')
    print(f'grid_peak_factor = {peak_grid_factor:.8f}')
    print(f'C2-M3 PREDECLARED VERDICT = {verdict}')

    print('\nINTERPRETATION LOCK:')
    print('- M3 tests a physical opportunity proxy, not observers or consciousness.')
    print('- No observed zeta may be inserted, reported, or used to tune this M3 run.')
    print('- An interior optimum is not evidence for Canevas; it only establishes a nontrivial physical competition in this proxy.')
    print('- A later reveal may compare the frozen M3 prediction with observation, but no parameter may be changed under the M3 label afterward.')
    print('- A boundary or unstable result closes this proxy unless a separately motivated model is preregistered.')
    print('\nFINISHED C2-M3 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
