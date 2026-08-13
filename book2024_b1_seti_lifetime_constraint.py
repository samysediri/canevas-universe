"""BOOK2024-B1 — SETI NULL / CIVILIZATION-LIFETIME DEGENERACY v1

Book anchor: chapter 6 claim that technological civilizations are finite and
that finite lifetimes may help explain Fermi silence.

External empirical anchor (frozen before output):
Wlodarczyk-Sroka, Garrett & Siemion (2020), arXiv:2006.09756, report an upper
limit of ~0.0660% on the prevalence of nearby (within 50 pc) high-duty-cycle
radio transmitters with EIRP >= 1e13 W, under their survey assumptions.

This script asks what that observation constrains about lifetime WITHOUT
assuming every star produces a technological civilization.

Definitions
-----------
eta      = fraction of stellar systems that ever enter the searched transmitter phase
ell      = fraction of an eligible system's reference opportunity window spent in that phase
f_active = instantaneous prevalence of searched transmitter phase

Steady-state factorization: f_active = eta * ell.
Observed upper bound: f_active <= FMAX = 6.60e-4.
Thus ell <= FMAX/eta (capped at 1).

Important: ell is dimensionless. Converting it to years requires an independently
chosen physical opportunity-window duration T; B1 does not choose T.
"""

FMAX = 6.60e-4
ETA_VALUES = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001]


def max_lifetime_fraction(eta):
    return min(1.0, FMAX / eta)


def main():
    print('='*80)
    print('BOOK2024-B1 — SETI NULL / CIVILIZATION-LIFETIME DEGENERACY v1')
    print('='*80)
    print('Book anchor: finite technological civilizations / Fermi silence.')
    print('Empirical anchor: transmitter prevalence <= 0.0660% within 50 pc')
    print('for the searched high-duty-cycle class (EIRP >= 1e13 W).')
    print('No opportunity-window duration in years is assumed.\n')

    print('eta = fraction of systems ever producing searched transmitter phase')
    print('ell_max = maximum allowed fraction of reference window spent in phase\n')

    for eta in ETA_VALUES:
        ell = max_lifetime_fraction(eta)
        constrained = ell < 1.0
        print(f'eta={eta:.6g}  ell_max={ell:.9g}  lifetime_fraction_constrained={constrained}')

    eta_threshold = FMAX
    print('\nPREDECLARED BOOK2024-B1 SUMMARY')
    print('f_active_upper =', FMAX)
    print('eta threshold below which lifetime fraction is unconstrained =', eta_threshold)
    print('If eta=1, ell_max =', max_lifetime_fraction(1.0))
    print('If eta=0.1, ell_max =', max_lifetime_fraction(0.1))
    print('If eta=0.01, ell_max =', max_lifetime_fraction(0.01))
    print('If eta=0.001, ell_max =', max_lifetime_fraction(0.001))

    # The empirical null constrains a product, not lifetime alone.
    verdict = 'SETI_NULL_CONSTRAINS_ETA_TIMES_LIFETIME_NOT_UNIVERSAL_FINITUDE'
    print('PREDECLARED BOOK2024-B1 VERDICT =', verdict)

    print('\nINTERPRETATION LOCK:')
    print('- This is genuine use of an external observational upper bound, but only for one searched transmitter class.')
    print('- The null result does not prove civilizations are short-lived.')
    print('- It constrains eta * ell: rarity and short lifetime are observationally degenerate here.')
    print('- If eta <= 6.60e-4, this survey alone does not constrain ell below 1.')
    print('- Converting ell into years requires an independent reference-window model and must be a new preregistered step.')
    print('- Radio silence cannot be equated with extinction: civilizations may be radio-quiet, intermittent, beamed elsewhere, or below threshold.')
    print('- Do not alter FMAX or choose eta after output under the B1 label.')
    print('\nFINISHED BOOK2024-B1 — DO NOT RETUNE AFTER OUTPUT')

if __name__ == '__main__':
    main()
