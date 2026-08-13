"""BOOK2024-B2 — GALACTIC SETTLEMENT TIMESCALE v1

Book anchor: finite technological civilizations / Fermi silence.
Primary literature anchor: Carroll-Nellenback et al. (2019), analytic
settlement-front approximation with stellar motions and finite probe range.

Purpose
-------
Quantify how quickly a settlement front can cross a Milky-Way-sized system
across a preregistered parameter grid. This does NOT infer civilization
motivation, prevalence, or actual historical settlement. It tests whether
long-lived expansion phases would generically have ample time to propagate.

No post-output retuning under B2.
"""

import math
import itertools

# Literature/reference constants
RHO = 0.0023  # stars per cubic light-year, from paper's solar-neighborhood reference
VS_KMS = 30.0
C_KMS = 299792.458
GALAXY_DIAMETER_LY = 100000.0
GALAXY_AGE_YR = 1.0e10  # deliberately rounded order-of-magnitude comparison scale
VFAST_RATIO = 3.0       # preregistered midpoint of paper's ~2--3.5 range
EPSILON = 0.25

# Frozen grid before output
F_VALUES = [0.01, 0.1, 1.0]          # settleable fraction
DP_VALUES = [5.0, 10.0, 20.0]       # probe range in ly
VP_FRAC_C = [0.001, 0.01, 0.1]      # probe speed
TP_VALUES = [100.0, 1000.0, 10000.0]# launch interval in yr


def nu_l(tau_l):
    # Eq. 9 in Carroll-Nellenback et al.; numerically stable enough on this grid.
    if tau_l <= 0:
        return 1.0
    return 1 + 3*tau_l**3*math.log(tau_l/(tau_l+1)) + 3*tau_l**2 - 1.5*tau_l


def front_speed(f, dp, vp_frac, tp):
    vp_kms = vp_frac * C_KMS
    vp_lyyr = vp_frac  # c = 1 ly/yr by definition to excellent approximation
    vs_frac_c = VS_KMS / C_KMS
    eta = f * RHO * dp**3
    nu_s = vs_frac_c / vp_frac
    t_probe = dp / vp_lyyr
    tau_p = tp / t_probe
    tau_c = 1.0 / (math.pi * eta * nu_s) if eta > 0 and nu_s > 0 else math.inf
    D1 = 1.0 - math.exp(-(4*math.pi/3)*EPSILON*eta)
    tau_launch = D1*tau_p + (1-D1)*tau_c
    nul = nu_l(tau_launch)
    nu = max(VFAST_RATIO*nu_s, nul)
    vfront_lyyr = nu * vp_lyyr
    return vfront_lyyr, dict(eta=eta,nu_s=nu_s,tau_p=tau_p,tau_c=tau_c,D1=D1,tau_l=tau_launch,nu_l=nul,nu=nu)


def main():
    print('='*82)
    print('BOOK2024-B2 — GALACTIC SETTLEMENT TIMESCALE v1')
    print('='*82)
    print('Literature-anchored analytic approximation; no civilization prevalence inferred.\n')

    rows=[]
    for f,dp,vp,tp in itertools.product(F_VALUES,DP_VALUES,VP_FRAC_C,TP_VALUES):
        vfront,d=front_speed(f,dp,vp,tp)
        cross = GALAXY_DIAMETER_LY / vfront if vfront>0 else math.inf
        ratio = cross / GALAXY_AGE_YR
        fast = cross < 0.1*GALAXY_AGE_YR
        rows.append((f,dp,vp,tp,vfront,cross,ratio,fast,d))
        print(f'f={f:>4.2f} dp={dp:>4.0f}ly vp={vp:>5.3f}c Tp={tp:>6.0f}yr '
              f'vfront={vfront:.6g} ly/yr cross={cross:.6g} yr age_ratio={ratio:.6g} fast10pct={fast}')

    finite=[r for r in rows if math.isfinite(r[5])]
    fast=[r for r in finite if r[7]]
    under_age=[r for r in finite if r[5] < GALAXY_AGE_YR]
    cross_vals=sorted(r[5] for r in finite)
    med=cross_vals[len(cross_vals)//2]

    print('\nPREDECLARED BOOK2024-B2 SUMMARY')
    print('n_models =',len(rows))
    print('fraction crossing within Galaxy age =',len(under_age)/len(finite))
    print('fraction crossing within 10% Galaxy age =',len(fast)/len(finite))
    print('median crossing time yr =',med)
    print('min crossing time yr =',min(cross_vals))
    print('max crossing time yr =',max(cross_vals))

    # Predeclared interpretation rule
    frac_fast=len(fast)/len(finite)
    if frac_fast >= 0.75:
        verdict='LONG_LIVED_EXPANSION_WOULD_OFTEN_PROPAGATE_RAPIDLY'
    elif len(under_age)/len(finite) >= 0.75:
        verdict='EXPANSION_OFTEN_FASTER_THAN_GALACTIC_AGE_BUT_NOT_UNIFORMLY_RAPID'
    else:
        verdict='SETTLEMENT_TIMESCALE_NOT_ROBUSTLY_SHORT_ON_GRID'
    print('PREDECLARED BOOK2024-B2 VERDICT =',verdict)

    print('\nINTERPRETATION LOCK:')
    print('- This reproduces a published-style analytic settlement-front model; it is not evidence aliens expand.')
    print('- A short crossing time does not imply Earth should have been visited unless appearance, motivation, settleability, lifetime, and detectability conditions also hold.')
    print('- A long-lived expansion phase becomes observationally relevant only when its lifetime exceeds the propagation timescale needed to generate a large footprint.')
    print('- B2 therefore constrains the plausibility of the book\'s finite-window mechanism only conditionally, not universally.')
    print('- Do not tune f, dp, vp, Tp, diameter, or verdict thresholds after output under the B2 label.')
    print('\nFINISHED BOOK2024-B2 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    main()
