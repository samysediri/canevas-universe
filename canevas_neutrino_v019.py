"""Canevas v0.19 — prospective neutrino-mass distinguishability test.

PRE-REGISTERED INTENT
---------------------
This run extends the already-frozen distinguishability construction to one new
physical axis: the total mass of three degenerate standard active neutrinos.
The code does not use an observational best-fit neutrino mass to tune the
metric, scan density, observables, or weights.

Important limitation: this is still not a blind prediction in the strongest
sense, because the broader cosmological framework and observable family were
developed using known cosmology. It is a prospective out-of-development-axis
stress test, not proof of the Canevas axioms.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.19'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)

# Frozen cosmological background used in the previous metric family.
h=.674; Om=.315; Ob=.0493
omega_m_total=Om*h*h
omega_b=Ob*h*h
omega_L=(1-Om)*h*h
A_s=2.10e-9; n_s=.965; YHe=.245
zeta_obs=(Om-Ob)/Ob

# Prospective scan selected independently of current cosmological upper limits.
# Positive log grid, broad enough to explore structural effects without using a
# current posterior as a range selector. Units: eV, sum over 3 degenerate masses.
MNU=np.logspace(np.log10(0.01),np.log10(2.0),45)
ks=np.logspace(-2,0.7,8)
zs=[0.,2.,6.]


def feature_vector(sum_mnu):
    # Three degenerate massive active neutrinos. CLASS recommends T_ncdm=0.71611
    # for standard active neutrinos. Their non-cold matter density is inferred
    # from the masses. To keep total non-relativistic matter omega_m fixed, CDM
    # is reduced by omega_ncdm after a first CLASS background calculation would
    # otherwise be needed. For standard neutrinos omega_nu ~= sum_mnu/93.14 eV.
    omega_nu=sum_mnu/93.14
    omega_cdm=omega_m_total-omega_b-omega_nu
    if omega_cdm <= 0:
        return None,'omega_cdm <= 0 at this mass'

    c=Class()
    try:
        params={
            'output':'mPk',
            'h':h,
            'omega_b':omega_b,
            'omega_cdm':float(omega_cdm),
            'A_s':A_s,
            'n_s':n_s,
            'YHe':YHe,
            'N_ncdm':3,
            'm_ncdm':','.join([f'{sum_mnu/3:.12g}']*3),
            'T_ncdm':'0.71611,0.71611,0.71611',
            # Keep approximately the standard total early radiation content:
            # three massive species contribute about 3*1.013 to Neff in CLASS's
            # recommended convention, leaving a tiny massless residual.
            'N_ur':0.005,
            'P_k_max_1/Mpc':6.,
            'z_max_pk':6.5,
        }
        c.set(params); c.compute()
        f=[]
        for z in zs:
            for k in ks:
                f.append(np.log(max(c.pk(float(k),float(z)),1e-300)))
            # Hubble rate is included exactly as an observable, converted only by
            # a fixed unit so logarithms are dimensionless up to an additive constant.
            f.append(np.log(max(c.Hubble(float(z)),1e-300)))
        return np.asarray(f),None
    except Exception as e:
        return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass


def weighted_summary(x,speed):
    u=np.log(x); w=np.maximum(speed,0)
    norm=np.trapezoid(w,u)
    if not np.isfinite(norm) or norm<=0:
        return np.nan,np.nan,np.nan,np.nan
    p=w/norm
    area=.5*(p[:-1]+p[1:])*np.diff(u)
    c=np.r_[0,np.cumsum(area)]; c/=c[-1]
    q16=float(np.exp(np.interp(.16,c,u)))
    med=float(np.exp(np.interp(.50,c,u)))
    q84=float(np.exp(np.interp(.84,c,u)))
    mode=float(x[np.argmax(w)])
    return q16,med,q84,mode


def run():
    print('='*72)
    print(f' CANEVAS v{VERSION} — PROSPECTIVE NEUTRINO-MASS TEST')
    print('='*72)
    print('Observed neutrino-mass constraints are NOT used by this program.')
    print(f'Scan: {MNU.min():.5g} to {MNU.max():.5g} eV, {len(MNU)} points\n')

    rows=[]; feats=[]; valid_m=[]
    for i,m in enumerate(MNU,1):
        print(f'[{i:2d}/{len(MNU)}] sum_mnu={m:.7f} eV',end=' ... ',flush=True)
        f,e=feature_vector(float(m))
        if f is None:
            print('REJECTED')
            rows.append((m,'rejected','',e)); continue
        print('OK')
        valid_m.append(m); feats.append(f); rows.append((m,'ok','',''))

    if len(valid_m)<5:
        raise RuntimeError('Too few valid CLASS neutrino cosmologies.')
    x=np.asarray(valid_m); F=np.vstack(feats); u=np.log(x)

    # Frozen identity-W metric: Euclidean speed of the same log-observable family
    # with respect to log(sum mnu). No scan-derived standardisation.
    dF=np.gradient(F,u,axis=0)
    speed_all=np.sqrt(np.sum(dF*dF,axis=1))

    # Predeclared component robustness variants, analogous to v0.17.
    # Feature ordering: for each z, 8 P(k) then one H.
    idx_pk=[]; idx_h=[]; idx_z=[]
    for zi in range(3):
        base=zi*9
        idx_pk.extend(range(base,base+8)); idx_h.append(base+8)
        idx_z.append(list(range(base,base+9)))
    lowk=[]; highk=[]
    for zi in range(3):
        base=zi*9
        lowk.extend(range(base,base+4)); highk.extend(range(base+4,base+8))

    variants={
        'identity_all':list(range(F.shape[1])),
        'pk_only':idx_pk,
        'z0_all':idx_z[0],
        'z2_all':idx_z[1],
        'z6_all':idx_z[2],
        'low_k_pk':lowk,
        'high_k_pk':highk,
    }

    summaries=[]
    for name,idx in variants.items():
        D=dF[:,idx]
        s=np.sqrt(np.sum(D*D,axis=1))
        q16,med,q84,mode=weighted_summary(x,s)
        summaries.append((name,q16,med,q84,mode))
        print(f'{name:14s} median={med:.6f} eV  16-84=[{q16:.6f},{q84:.6f}]  density-peak={mode:.6f}')

    meds=np.array([r[2] for r in summaries],float)
    q16s=np.array([r[1] for r in summaries],float)
    q84s=np.array([r[3] for r in summaries],float)

    with (OUT/'v019_neutrino_metric.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['sum_mnu_eV','identity_metric_density_per_dlogmnu'])
        for m,s in zip(x,speed_all): w.writerow([m,s])
    with (OUT/'v019_neutrino_variants.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['variant','q16_eV','median_eV','q84_eV','density_peak_eV']); w.writerows(summaries)

    text=f'''CANEVAS v{VERSION} — PROSPECTIVE NEUTRINO-MASS SUMMARY
========================================================
This file intentionally does NOT compare against current observational bounds.
Metric family frozen from the previous cosmology work; no anthropic score.
Mass model: 3 degenerate standard active massive neutrinos.
Total non-relativistic omega_m held fixed by replacing CDM with neutrino mass.
Valid CLASS masses: {x.min():.8f} to {x.max():.8f} eV ({len(x)} points)

PRE-REGISTERED METRIC-FAMILY PREDICTION:
median across metric variants = {np.median(meds):.8f} eV
variant-median range = [{np.min(meds):.8f}, {np.max(meds):.8f}] eV
median lower-16% endpoint = {np.median(q16s):.8f} eV
median upper-84% endpoint = {np.median(q84s):.8f} eV

IDENTITY-W PRIMARY RESULT:
16% = {summaries[0][1]:.8f} eV
median = {summaries[0][2]:.8f} eV
84% = {summaries[0][3]:.8f} eV
density peak = {summaries[0][4]:.8f} eV

INTERPRETATION LOCK:
- These numbers must be recorded before comparison to modern neutrino constraints.
- No later modification of scan, W, observable family, neutrino hierarchy, or fixed-total-matter rule may be used to rescue agreement.
- Agreement would only support this distinguishability hypothesis within this model family; it would not prove Canevas.
- Disagreement is a genuine failure of this prospective extension and must be reported as such.
'''
    (OUT/'v019_neutrino_prediction_BEFORE_COMPARISON.txt').write_text(text,encoding='utf8')
    print('\n'+text+'\nFINISHED v0.19 — DO NOT MODIFY BEFORE COMPARISON')

if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
