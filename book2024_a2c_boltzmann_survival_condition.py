"""BOOK2024-A2c — BOLTZMANN-OBSERVER SURVIVAL CONDITION v1

Anchored to B24-P2/P3/P6 from the 2024 book.

Scientific motivation
---------------------
A1 showed that infinite opportunity requires a recurrence condition for eventual
occurrence. A2 showed that infinite realization does not determine typicality.
A2b showed, in a toy process, that temporal persistence can strongly favor
coherent histories over IID histories.

A2c now moves to a physically motivated rate model inspired by the cosmological
Boltzmann-brain literature. The goal is NOT to estimate the actual universe's
rates. It is to derive the quantitative condition under which ordinary observers
from structured cosmological histories outnumber fluctuation observers.

Literature anchor
-----------------
Scale-factor-cutoff calculations in eternal-inflation cosmology compare ordinary
observers and Boltzmann brains using vacuum decay rates and Boltzmann-brain
nucleation rates. The general lesson used here is only that the competition is a
rate/lifetime problem; no literature numerical rate is imported into this test.

PREDECLARED MODEL
-----------------
One metastable cosmological region produces:
  N_O = total ordinary observers generated during its finite structured era.
  gamma_BB = fluctuation-observer production rate per unit time.
  kappa = terminal decay rate of the region.

Assume the region lifetime T is exponentially distributed with mean 1/kappa.
Then the expected number of fluctuation observers is
  E[N_BB] = gamma_BB * E[T] = gamma_BB / kappa.

Define ordinary-observer dominance fraction
  f_O = N_O / (N_O + gamma_BB/kappa).

The exact survival condition f_O > 1/2 is therefore
  kappa > gamma_BB / N_O.
Equivalently, mean lifetime 1/kappa < N_O/gamma_BB.

This script verifies this scaling over preregistered dimensionless grids and
reports the critical boundary. It does NOT claim physical values for N_O,
gamma_BB, or kappa.
"""

import math

# Dimensionless grid. Setting gamma_BB=1 fixes the time unit; only ratios matter.
GAMMA_BB = 1.0
N_ORDINARY = [1.0, 1e3, 1e6, 1e12]
KAPPA_FACTORS = [0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]


def ordinary_fraction(n_o, gamma_bb, kappa):
    n_bb = gamma_bb / kappa
    return n_o / (n_o + n_bb)


def main():
    print('='*82)
    print('BOOK2024-A2c — BOLTZMANN-OBSERVER SURVIVAL CONDITION v1')
    print('='*82)
    print('Physically motivated rate/lifetime bridge; NO empirical cosmological rates used.\n')

    all_boundaries_correct = True
    for n_o in N_ORDINARY:
        kcrit = GAMMA_BB / n_o
        print(f'[N_O={n_o:.3e}] analytic critical kappa = gamma_BB/N_O = {kcrit:.3e}')
        below_seen = False
        above_seen = False
        for fac in KAPPA_FACTORS:
            kappa = fac * kcrit
            f = ordinary_fraction(n_o, GAMMA_BB, kappa)
            dom = 'ORDINARY' if f > 0.5 else ('EQUAL' if abs(f-0.5)<1e-12 else 'FLUCTUATION')
            print(f' factor={fac:7.2g} kappa={kappa:.3e} mean_lifetime={1/kappa:.3e} f_O={f:.9f} dominance={dom}')
            if fac < 1 and f < 0.5:
                below_seen = True
            if fac > 1 and f > 0.5:
                above_seen = True
            if fac == 1.0 and abs(f-0.5) > 1e-12:
                all_boundaries_correct = False
        if not (below_seen and above_seen):
            all_boundaries_correct = False
        print()

    print('PREDECLARED BOOK2024-A2c SUMMARY')
    print('critical condition: kappa_crit = gamma_BB / N_O')
    print('equivalent lifetime condition: tau_crit = N_O / gamma_BB')
    print('grid verifies both sides of boundary =', all_boundaries_correct)

    if all_boundaries_correct:
        verdict='BOOK_ARCHITECTURE_REQUIRES_FINITE_RATE_LIFETIME_INEQUALITY'
    else:
        verdict='CONTROL_FAILURE_DO_NOT_INTERPRET'
    print('PREDECLARED BOOK2024-A2c VERDICT =', verdict)

    print('\nINTERPRETATION LOCK:')
    print('- This is not evidence that our universe satisfies the inequality.')
    print('- It derives a quantitative survival condition for any model with ordinary and fluctuation observers of this rate form.')
    print('- Infinite duration with gamma_BB>0 makes the expected fluctuation count diverge unless the measure/regulator changes the comparison.')
    print('- A finite metastable lifetime can suppress fluctuation dominance if kappa > gamma_BB/N_O.')
    print('- Therefore the 2024 book can turn the Boltzmann-observer objection into a constraint on its generative dynamics.')
    print('- A future A2d must obtain or bound gamma_BB, kappa, and N_O from an explicit physical cosmology; they may not be chosen to force survival.')
    print('\nFINISHED BOOK2024-A2c — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    main()
