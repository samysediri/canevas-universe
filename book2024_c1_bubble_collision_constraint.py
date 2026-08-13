"""BOOK2024-C1 — BUBBLE-UNIVERSE OBSERVABILITY CONSTRAINT v1

Book anchor: chapter 3 explicitly imagines random phenomena producing multiple
Big Bangs, parallel and indefinitely subsequent. This script does NOT identify
that claim with eternal inflation; it tests eternal-inflation bubble nucleation as
one concrete, falsifiable physical instantiation.

Published inputs frozen before output:
- Freivogel et al. (2009): N_LS ~ sqrt(Omega_k) * N for observable-size collisions.
- Feeney et al. (2010): WMAP7 mean detectable-collision count < 1.6 (68% CL).
- Planck 2018 + BAO: Omega_K = 0.0007 +/- 0.0019 (68%).

No Canevas parameter is fitted. We compute what combinations of curvature and
underlying collision abundance N remain compatible with the observational limit.
"""
import math

WMAP_LIMIT = 1.6
OMEGA_K_MEAN = 0.0007
OMEGA_K_SIGMA = 0.0019

# Positive/open-curvature magnitudes used only as diagnostic slices. Values are
# frozen before output and include the Planck+BAO central positive value and
# several conservative positive envelopes.
OMEGA_K_SLICES = [0.0001, 0.0007, 0.0019, 0.0026, 0.0045, 0.01]
N_TEST = [1, 3, 10, 30, 100, 300, 1000]


def n_detectable(N, omega_k):
    return math.sqrt(max(omega_k, 0.0)) * N


def n_max_allowed(omega_k):
    if omega_k <= 0:
        return math.inf
    return WMAP_LIMIT / math.sqrt(omega_k)


def main():
    print('='*80)
    print('BOOK2024-C1 — BUBBLE-UNIVERSE OBSERVABILITY CONSTRAINT v1')
    print('='*80)
    print('Candidate physical instantiation only; not an identification of Canevas with eternal inflation.')
    print(f'WMAP detectable-collision mean limit = {WMAP_LIMIT}')
    print(f'Planck+BAO Omega_K = {OMEGA_K_MEAN} +/- {OMEGA_K_SIGMA} (68%)\n')

    print('ALLOWED UNDERLYING COLLISION ABUNDANCE BY CURVATURE SLICE')
    for ok in OMEGA_K_SLICES:
        nmax = n_max_allowed(ok)
        print(f'Omega_k={ok:.4g} -> N_max_from_WMAP_scaling={nmax:.6g}')

    print('\nGRID DIAGNOSTIC')
    any_excluded = False
    any_allowed = False
    for ok in OMEGA_K_SLICES:
        row=[]
        for N in N_TEST:
            nd=n_detectable(N,ok)
            allowed=nd < WMAP_LIMIT
            any_allowed |= allowed
            any_excluded |= (not allowed)
            row.append(f'N={N}:Ndet={nd:.3g}:{"OK" if allowed else "EXCLUDED"}')
        print(f'Omega_k={ok:.4g} | ' + ' | '.join(row))

    central_nmax=n_max_allowed(max(OMEGA_K_MEAN,0.0))
    two_sigma_positive=max(OMEGA_K_MEAN+2*OMEGA_K_SIGMA,0.0)
    two_sigma_nmax=n_max_allowed(two_sigma_positive)

    print('\nPREDECLARED BOOK2024-C1 SUMMARY')
    print('Nmax at positive Planck+BAO central Omega_k =',central_nmax)
    print('positive 2sigma diagnostic Omega_k =',two_sigma_positive)
    print('Nmax at positive 2sigma diagnostic Omega_k =',two_sigma_nmax)
    print('grid contains allowed cases =',any_allowed)
    print('grid contains excluded cases =',any_excluded)

    if any_allowed and any_excluded:
        verdict='BUBBLE_INSTANTIATION_PARTLY_CONSTRAINED_NOT_SELECTED'
    elif any_excluded:
        verdict='GRID_EXCLUDED_UNDER_THIS_INSTANTIATION'
    else:
        verdict='GRID_UNCONSTRAINED_BY_THIS_TEST'
    print('PREDECLARED BOOK2024-C1 VERDICT =',verdict)

    print('\nINTERPRETATION LOCK:')
    print('- This constrains one eternal-inflation-style realization of the book, not the metaphysical Canevas itself.')
    print('- N is not predicted by the 2024 book, so agreement cannot validate the book.')
    print('- Non-detection can exclude portions of a concrete physical realization once N and Omega_k are independently predicted.')
    print('- Small curvature suppresses observable collisions, so a null CMB result does not by itself rule out many underlying domains.')
    print('- No parameter may be tuned after this output under the C1 label.')
    print('\nFINISHED BOOK2024-C1 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    main()
