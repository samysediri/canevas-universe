"""CANEVAS + CLASS ZETA-T1A — BOUNDARY AUTOPSY

Predeclared after ZETA-T1 returned BOUNDARY_NO_FINITE_SELECTION.
Purpose: diagnose whether the low-zeta boundary is numerical/configurational or
whether recovered models continue to favor still-lower zeta.

Scientific locks:
- ZETA-T1 result is retained unchanged.
- No setting is promoted because it produces a value near observed zeta.
- This script is a boundary diagnostic, not a replacement T1 prediction.
- Observed zeta is not used to choose configurations or verdict.
"""
from pathlib import Path
import csv, math
import numpy as np
from classy import Class

VERSION='ZETA-T1A'
OUTDIR=Path(__file__).resolve().parent/'results'; OUTDIR.mkdir(exist_ok=True)

h=0.674
Omega_m=0.315
omega_m=Omega_m*h*h
Omega_L=1.0-Omega_m
A_s=2.10e-9
n_s=0.965
YHE_FIXED=0.245
redshifts=np.array([12.,10.,8.,6.,4.,3.,2.,1.,0.5,0.])
zeta_grid=np.array([0.5,0.7,0.9,1.1,1.3,1.5,1.8,2.0,2.2,2.4,2.6,2.75,3.0,3.5,4.0])

# Frozen technical configurations. These are not scientific models to select among.
CONFIGS={
 'BASELINE': dict(yhe='fixed', pkmax=50.0, zpad=0.5),
 'YHE_CLASS_DEFAULT': dict(yhe='default', pkmax=50.0, zpad=0.5),
 'LOWER_PKMAX': dict(yhe='fixed', pkmax=10.0, zpad=0.5),
 'YHE_DEFAULT_LOWER_PKMAX': dict(yhe='default', pkmax=10.0, zpad=0.5),
}


def run_class(zeta,cfg):
    omega_b=omega_m/(1+zeta)
    omega_cdm=omega_m-omega_b
    p={'output':'mPk','h':h,'omega_b':omega_b,'omega_cdm':omega_cdm,
       'A_s':A_s,'n_s':n_s,'P_k_max_1/Mpc':cfg['pkmax'],
       'z_max_pk':float(redshifts.max()+cfg['zpad'])}
    if cfg['yhe']=='fixed': p['YHe']=YHE_FIXED
    c=Class()
    try:
        c.set(p); c.compute()
        # Require representative spectra to be numerically finite.
        probes=[]
        for z in [12.,6.,0.]:
            for k in [1e-3,0.1,1.0,min(5.0,cfg['pkmax']*0.5)]:
                probes.append(float(c.pk(k,z)))
        ok=all(np.isfinite(probes)) and all(v>=0 for v in probes)
        return ok,omega_b,omega_cdm,'' if ok else 'nonfinite_or_negative_pk'
    except Exception as e:
        return False,omega_b,omega_cdm,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try:c.struct_cleanup(); c.empty()
        except Exception:pass


def main():
    print('='*82)
    print('CANEVAS + CLASS ZETA-T1A — LOW-ZETA BOUNDARY AUTOPSY')
    print('='*82)
    print('T1 remains BOUNDARY_NO_FINITE_SELECTION. This diagnostic cannot repair it.')
    print('Observed zeta is not used in configuration choice or verdict.\n')

    rows=[]
    frontier={}
    for cname,cfg in CONFIGS.items():
        print(f'[{cname}]')
        valid=[]
        for zeta in zeta_grid:
            ok,ob,oc,err=run_class(float(zeta),cfg)
            rows.append(dict(config=cname,zeta=zeta,omega_b=ob,omega_cdm=oc,status='OK' if ok else 'REJECTED',error=err))
            print(f' zeta={zeta:5.2f} ... {"OK" if ok else "REJECTED"}')
            if ok: valid.append(float(zeta))
        frontier[cname]=min(valid) if valid else math.nan
        print(f' lowest valid zeta = {frontier[cname]}\n')

    with (OUTDIR/'zeta_t1a_boundary_status.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['config','zeta','omega_b','omega_cdm','status','error']); w.writeheader(); w.writerows(rows)

    vals=np.array([v for v in frontier.values() if np.isfinite(v)],float)
    recovered_below_t1=bool(np.any(vals < 2.75-1e-9)) if len(vals) else False
    config_sensitive=bool((np.max(vals)-np.min(vals))>=0.5) if len(vals)>1 else False

    if recovered_below_t1 and config_sensitive:
        verdict='BOUNDARY_CONFIGURATION_SENSITIVE'
    elif recovered_below_t1:
        verdict='LOW_ZETA_DOMAIN_RECOVERABLE'
    elif len(vals):
        verdict='LOW_ZETA_REJECTION_ROBUST_ACROSS_CONFIGS'
    else:
        verdict='CLASS_DOMAIN_FAILURE'

    print('PREDECLARED ZETA-T1A SUMMARY')
    for k,v in frontier.items(): print(f'{k:28s} lowest_valid_zeta = {v}')
    print('recovered any zeta below T1 boundary =',recovered_below_t1)
    print('frontier configuration-sensitive >=0.5 in zeta =',config_sensitive)
    print('PREDECLARED ZETA-T1A VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- This diagnoses CLASS domain behavior only; it does not create a new zeta prediction.')
    print('- If lower zeta becomes valid under a technical configuration, T1 remains a boundary result.')
    print('- If all configurations reject low zeta similarly, the numerical domain is robust but still not a physical selection boundary.')
    print('- A future T2 may test a new physically motivated score only after this diagnostic is recorded.')
    print('\nFINISHED ZETA-T1A — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__': main()
