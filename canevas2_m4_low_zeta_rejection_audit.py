"""CANEVAS 2.0 M4 — LOW-ZETA REJECTION AUDIT v1

PREREGISTERED BEFORE OUTPUT.

Purpose
-------
M3's blind proxy maximum occurred at the first numerically valid zeta. M4 does NOT
score observer opportunity and does NOT search for a preferred zeta. It asks only
why low-zeta CLASS cosmologies were rejected.

Frozen diagnostic logic
-----------------------
For each zeta on a dense low-zeta grid, construct the same fixed-total-matter
background as M3 and test CLASS in stages:
  A background/thermodynamics only,
  B linear matter power at z=0,
  C linear matter power at z=20.
Record omega_b, omega_cdm, baryon fraction, failure stage and exact exception.

Then repeat a deliberately diagnostic (NOT Canevas-predictive) control in which
omega_b is capped at a conservative reference ceiling near the standard BBN/CMB
physical baryon density while excess fixed total matter is assigned to CDM. If a
failed fixed-total model succeeds only after this cap, the rejection is attributed
to the high-baryon parameterization/physics handled by CLASS, not to a newly
established anthropic boundary.

Observed zeta is absent and must not be used to tune thresholds after output.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
h=0.674; Omega_m=0.315; omega_m=Omega_m*h*h
A_s=2.10e-9; n_s=0.965; YHe=0.245
# Dense low-zeta audit grid; extends below M3 failures and across its first successes.
ZETA=np.geomspace(0.5,4.0,41)
# Diagnostic reference cap only; not a fitted boundary and not used for a Canevas score.
OMEGA_B_CAP=0.024


def params(zeta, capped=False):
    wb=omega_m/(1+zeta)
    if capped: wb=min(wb,OMEGA_B_CAP)
    wc=omega_m-wb
    return float(wb),float(wc)


def stage_test(zeta,capped=False):
    wb,wc=params(zeta,capped)
    common={'h':h,'omega_b':wb,'omega_cdm':wc,'A_s':A_s,'n_s':n_s,'YHe':YHe}
    # Stage A: background/thermodynamics without requesting P(k)
    c=Class()
    try:
        c.set(dict(common)); c.compute(); _=c.age()
    except Exception as e:
        return 'A_BACKGROUND_THERMO',f'{type(e).__name__}: {e}'.replace('\n',' '),wb,wc
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass
    # Stage B: P(k), z=0
    c=Class()
    try:
        p=dict(common); p.update({'output':'mPk','P_k_max_1/Mpc':40.,'z_max_pk':0.5})
        c.set(p); c.compute(); v=c.pk(0.1,0.0)
        if not np.isfinite(v) or v<=0: raise RuntimeError('nonfinite/nonpositive P(k,z=0)')
    except Exception as e:
        return 'B_PK_Z0',f'{type(e).__name__}: {e}'.replace('\n',' '),wb,wc
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass
    # Stage C: P(k), high redshift as required by M3
    c=Class()
    try:
        p=dict(common); p.update({'output':'mPk','P_k_max_1/Mpc':40.,'z_max_pk':20.5})
        c.set(p); c.compute(); v=c.pk(0.1,20.0)
        if not np.isfinite(v) or v<=0: raise RuntimeError('nonfinite/nonpositive P(k,z=20)')
        return 'PASS','',wb,wc
    except Exception as e:
        return 'C_PK_Z20',f'{type(e).__name__}: {e}'.replace('\n',' '),wb,wc
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass


def run():
    print('='*82)
    print('CANEVAS 2.0 M4 — LOW-ZETA REJECTION AUDIT v1')
    print('='*82)
    print('No observer score. No preferred-zeta search. Observed zeta is absent.\n')
    rows=[]
    for i,z in enumerate(ZETA,1):
        st,err,wb,wc=stage_test(float(z),False)
        cst,cerr,cwb,cwc=stage_test(float(z),True)
        rescued=(st!='PASS' and cst=='PASS')
        fb=wb/(wb+wc)
        rows.append([z,wb,wc,fb,st,err,cst,cerr,rescued])
        print(f'[{i:02d}/{len(ZETA)}] zeta={z:.6f} fb={fb:.6f} wb={wb:.6f} fixed={st} cap_control={cst} rescued={rescued}')
        if err: print('  fixed_error:',err[:500])

    with (OUT/'c2_m4_low_zeta_audit.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['zeta','omega_b','omega_cdm','baryon_fraction','fixed_total_stage','fixed_error','cap_control_stage','cap_control_error','rescued_by_baryon_cap']); w.writerows(rows)

    fails=[r for r in rows if r[4]!='PASS']; passes=[r for r in rows if r[4]=='PASS']
    rescued=[r for r in rows if r[8]]
    first_pass=min((r[0] for r in passes),default=float('nan'))
    last_fail=max((r[0] for r in fails),default=float('nan'))
    fail_stages=sorted(set(r[4] for r in fails))

    if not fails:
        verdict='NO_LOW_ZETA_CLASS_REJECTION_REPRODUCED'
    elif len(rescued)==len(fails):
        verdict='REJECTIONS_TRACK_HIGH_BARYON_PARAMETERIZATION_NOT_ESTABLISHED_PHYSICAL_BOUNDARY'
    elif rescued:
        verdict='REJECTIONS_PARTLY_TRACK_HIGH_BARYON_PARAMETERIZATION_CAUSE_MIXED'
    else:
        verdict='REJECTIONS_NOT_EXPLAINED_BY_SIMPLE_BARYON_CAP_REQUIRES_DEEPER_AUDIT'

    print('\nC2-M4 SUMMARY')
    print(f'n_fail = {len(fails)}')
    print(f'n_pass = {len(passes)}')
    print(f'n_rescued_by_baryon_cap = {len(rescued)}')
    print(f'last_failed_zeta = {last_fail}')
    print(f'first_passed_zeta = {first_pass}')
    print(f'failure_stages = {fail_stages}')
    print(f'C2-M4 PREDECLARED VERDICT = {verdict}')
    print('\nINTERPRETATION LOCK:')
    print('- A CLASS failure is not by itself a physical exclusion of a universe.')
    print('- The baryon-cap control is diagnostic only and is not a new cosmological model prediction.')
    print('- Rescue by the cap means the M3 boundary cannot be used as anthropic evidence.')
    print('- Non-rescue also does not prove physical impossibility; the exact module/error must be investigated.')
    print('- Do not use the observed zeta or M3 peak to redefine this audit after output.')
    print('\nFINISHED C2-M4 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
