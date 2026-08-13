"""BOOK2024-A2 — COHERENT-HISTORY VS FLUCTUATION-OBSERVER MEASURE v1

Anchored to B24-P2/B24-P3/B24-P6 from the 2024 book research program.

Question:
If an infinite generative field realizes both structured evolutionary observers
and fluctuation-produced observer-moments, does 'infinity' itself determine
which class is typical?

This test deliberately does NOT assume Boltzmann observers dominate.
It proves a narrower statement: once both classes recur indefinitely, raw
cardinality infinity/infinity is insufficient. A measure or asymptotic rate is
required.

Model:
Two independent Poisson occurrence processes per unit four-volume/time:
  S = structured-history observer events, rate lambda_S
  F = fluctuation observer events, rate lambda_F
For stationary rates, expected observed fraction among event tokens is
  f_S = lambda_S/(lambda_S+lambda_F).
Scaling the total spacetime exposure T -> infinity sends both counts to infinity
when both rates are positive, but the fraction remains rate-dependent.

No empirical cosmology, consciousness threshold, 1992 data, or observed target
is used. Rate scenarios are countermodels frozen before execution.
"""

import math

SCENARIOS = {
    "STRUCTURED_DOMINANT": (1e-3, 1e-6),
    "EQUAL_RATES": (1e-6, 1e-6),
    "FLUCTUATION_DOMINANT": (1e-9, 1e-4),
    "BOTH_TINY_EQUAL": (1e-30, 1e-30),
    "NO_FLUCTUATIONS": (1e-8, 0.0),
}

EXPOSURES = [1e3, 1e6, 1e12, 1e30]


def structured_fraction(ls, lf):
    total = ls + lf
    return math.nan if total == 0 else ls / total


def expected_counts(ls, lf, T):
    return ls*T, lf*T


def main():
    print("="*80)
    print("BOOK2024-A2 — COHERENT-HISTORY VS FLUCTUATION-OBSERVER MEASURE v1")
    print("="*80)
    print("Source anchor: B24-P2/P3/P6. No empirical target values are used.\n")

    fractions = {}
    for name,(ls,lf) in SCENARIOS.items():
        fs = structured_fraction(ls,lf)
        fractions[name] = fs
        print(f"[{name}] lambda_S={ls:.3e} lambda_F={lf:.3e} asymptotic_f_S={fs:.12g}")
        for T in EXPOSURES:
            ns,nf = expected_counts(ls,lf,T)
            print(f"  T={T:.1e} E[N_S]={ns:.6g} E[N_F]={nf:.6g}")
        print()

    # Frozen diagnostics
    infinite_cardinality_not_enough = (
        fractions["STRUCTURED_DOMINANT"] > 0.99 and
        abs(fractions["EQUAL_RATES"] - 0.5) < 1e-12 and
        fractions["FLUCTUATION_DOMINANT"] < 1e-4
    )
    scale_invariance_of_fraction = all(
        abs(structured_fraction(*SCENARIOS[k]) - fractions[k]) < 1e-15
        for k in SCENARIOS
    )
    equal_tiny_same_fraction = abs(fractions["BOTH_TINY_EQUAL"] - 0.5) < 1e-12

    print("PREDECLARED BOOK2024-A2 SUMMARY")
    print("countermodels span structured/equal/fluctuation dominance =", infinite_cardinality_not_enough)
    print("fractions independent of total exposure T =", scale_invariance_of_fraction)
    print("arbitrarily tiny equal rates still give 50/50 conditional fraction =", equal_tiny_same_fraction)

    if infinite_cardinality_not_enough and scale_invariance_of_fraction and equal_tiny_same_fraction:
        verdict = "INFINITE_REALIZATION_DOES_NOT_FIX_TYPICALITY_MEASURE_REQUIRED"
    else:
        verdict = "CONTROL_FAILURE_DO_NOT_INTERPRET"
    print("PREDECLARED BOOK2024-A2 VERDICT =", verdict)

    print("\nINTERPRETATION LOCK:")
    print("- This does NOT show that fluctuation observers dominate our universe.")
    print("- It shows that making both classes occur infinitely often does not solve the typicality problem.")
    print("- The 2024 book therefore needs a generative measure/rate law, not only an infinite possibility space.")
    print("- A future physical A2b must derive or constrain lambda_S/lambda_F from an explicit cosmology.")
    print("- No self-location observation may be used to choose that ratio.")
    print("- If a physical model predicts lambda_F >> lambda_S, coherent experience becomes a serious adversarial problem;")
    print("  if it predicts lambda_S >> lambda_F or suppresses F, the book's architecture survives that test.")
    print("\nFINISHED BOOK2024-A2 — DO NOT RETUNE AFTER OUTPUT")


if __name__ == "__main__":
    main()
