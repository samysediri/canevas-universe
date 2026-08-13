"""BOOK2024-A2d — LITERATURE-ANCHORED BOLTZMANN-BRAIN TRIANGULATION v1

Purpose
-------
Move beyond toy parameters by encoding several mutually incompatible but
published physical frameworks for Boltzmann-brain production/avoidance.
This test does NOT pick the framework that best helps Canevas. It asks whether
Book-2024's architecture is robust across them, or remains model-dependent.

Primary-source anchors used when designing this preregistration:
1) De Simone et al., Phys. Rev. D 82, 063520 (2010): under scale-factor cutoff,
   BB/ordinary-observer ratio is finite and depends on BB nucleation and vacuum
   decay rates; acceptable measures require suitable rate inequalities.
2) Olum, Upadhyay & Vilenkin, Phys. Rev. D 104, 023528 (2021): for scale-factor
   measure, ordinary observers dominate if vacuum decay rate exceeds BB rate;
   small-black-hole nucleation can contribute to decay and may enforce this.
3) Page, Phys. Lett. B 669, 197-200 (2008): with a finite-comoving-volume style
   regularization, a universe lasting too long after its ordinary-observer era
   can become BB-dominated; illustrative lifetime bounds are model-dependent.
4) Boddy, Carroll & Pollack, arXiv:1505.02780: under a quiescent de Sitter vacuum
   with suitable quantum assumptions, dynamical BB production may be absent.

No observed birth rank, zeta target, or Canevas-fitting parameter enters here.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Framework:
    name: str
    premise: str
    canevas_condition: str
    status_if_book_has_finite_local_episodes: str

FRAMEWORKS = [
    Framework(
        "SCALE_FACTOR_CUTOFF",
        "BB and ordinary observers are regulated by scale-factor cutoff; rate comparison matters.",
        "Require effective vacuum-exit/decay rate kappa > BB nucleation rate Gamma_BB in relevant long-lived vacua.",
        "CONDITIONAL_PASS_IF_RATE_INEQUALITY"
    ),
    Framework(
        "PAGE_FINITE_COMOVING_VOLUME",
        "Ordinary-observer era is finite and later BB production can accumulate with duration.",
        "Require local episode/vacuum lifetime below the framework-dependent BB-dominance bound.",
        "CONDITIONAL_PASS_IF_LOCAL_LIFETIME_SHORT_ENOUGH"
    ),
    Framework(
        "QUIESCENT_DE_SITTER",
        "Stationary de Sitter vacuum has no dynamical BB production under stated quantum assumptions.",
        "No finite-lifetime BB suppression is required if Gamma_BB,dynamical = 0.",
        "PASS_UNDER_FRAMEWORK_ASSUMPTIONS"
    ),
]


def main():
    print('='*82)
    print('BOOK2024-A2d — LITERATURE-ANCHORED BOLTZMANN-BRAIN TRIANGULATION v1')
    print('='*82)
    print('No fitted Canevas parameters. No empirical target chosen after output.\n')

    statuses=[]
    for f in FRAMEWORKS:
        statuses.append(f.status_if_book_has_finite_local_episodes)
        print(f'[{f.name}]')
        print('premise =', f.premise)
        print('book survival condition =', f.canevas_condition)
        print('classification =', f.status_if_book_has_finite_local_episodes)
        print()

    unconditional_pass = all(s.startswith('PASS_') for s in statuses)
    unconditional_fail = all(s.startswith('FAIL_') for s in statuses)
    mixed_or_conditional = not unconditional_pass and not unconditional_fail

    print('PREDECLARED BOOK2024-A2d SUMMARY')
    print('unconditional_pass_across_frameworks =', unconditional_pass)
    print('unconditional_fail_across_frameworks =', unconditional_fail)
    print('mixed_or_conditional =', mixed_or_conditional)

    if unconditional_pass:
        verdict='BOOK_ARCHITECTURE_ROBUSTLY_AVOIDS_BB_ACROSS_DECLARED_FRAMEWORKS'
    elif unconditional_fail:
        verdict='BOOK_ARCHITECTURE_ROBUSTLY_FAILS_BB_ACROSS_DECLARED_FRAMEWORKS'
    else:
        verdict='BB_CONSTRAINT_IS_FRAMEWORK_AND_RATE_DEPENDENT_PHYSICAL_INSTANTIATION_REQUIRED'

    print('PREDECLARED BOOK2024-A2d VERDICT =', verdict)

    print('\nINTERPRETATION LOCK:')
    print('- A2d is a literature triangulation, not new empirical evidence.')
    print('- Published frameworks disagree about whether dynamical BB production occurs and how infinities are regulated.')
    print('- Therefore Book-2024 cannot claim victory by choosing one favorable framework post hoc.')
    print('- The finite-local-episode intuition is physically useful only after Canevas derives a concrete local dynamics/lifetime or vacuum-exit process.')
    print('- The next empirical step must instantiate ONE independently motivated cosmology and then apply that framework\'s published condition without retuning.')
    print('- Negative or indeterminate outcomes must be retained.')
    print('\nFINISHED BOOK2024-A2d — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    main()
