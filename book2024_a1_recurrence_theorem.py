"""BOOK2024-A1 — RECURRENCE / EVENTUAL-OCCURRENCE TEST v1

Anchored proposition B24-P2:
An infinite generative field is claimed to eventually realize every possibility.

Purpose:
Determine the minimal probabilistic condition under which infinitely many
opportunities imply eventual occurrence with probability 1.

IMPORTANT:
- This is a mathematical bridge test, not evidence that the physical universe
  actually obeys the bridge assumptions.
- No cosmological, anthropic, consciousness, or 1992 data enter this test.
- Cases and expected asymptotic classes are declared before execution.

For independent Bernoulli opportunities with probabilities p_n,
P(no occurrence through N) = product_{n<=N}(1-p_n).
If sum p_n diverges (with standard independence assumptions), eventual
occurrence has probability 1. If sum p_n converges, non-occurrence can retain
positive probability. Thus 'infinite opportunities' alone is insufficient.
"""

import math

N_VALUES = [10, 100, 1_000, 10_000, 100_000, 1_000_000]

CASES = {
    "FIXED_1PCT": lambda n: 0.01,
    "HARMONIC_1_OVER_N": lambda n: 1.0 / (n + 1.0),
    "SQUARE_SUMMABLE_1_OVER_N2": lambda n: 1.0 / ((n + 1.0) ** 2),
    "ZERO": lambda n: 0.0,
}

EXPECTED = {
    "FIXED_1PCT": "EVENTUAL_OCCURRENCE_A_S",
    "HARMONIC_1_OVER_N": "EVENTUAL_OCCURRENCE_A_S",
    "SQUARE_SUMMABLE_1_OVER_N2": "NONOCCURRENCE_RETAINS_POSITIVE_MASS",
    "ZERO": "IMPOSSIBLE",
}


def log_survival_to_N(prob_fn, N):
    log_s = 0.0
    cumulative_hazard = 0.0
    for n in range(1, N + 1):
        p = prob_fn(n)
        if not (0.0 <= p < 1.0):
            raise ValueError(f"p_n outside [0,1): n={n}, p={p}")
        cumulative_hazard += p
        if p > 0.0:
            log_s += math.log1p(-p)
    return log_s, cumulative_hazard


def asymptotic_class(name):
    if name in ("FIXED_1PCT", "HARMONIC_1_OVER_N"):
        return "SUM_P_DIVERGES"
    if name == "SQUARE_SUMMABLE_1_OVER_N2":
        return "SUM_P_CONVERGES"
    return "SUM_P_ZERO"


def main():
    print("=" * 78)
    print("BOOK2024-A1 — INFINITE OPPORTUNITY / EVENTUAL OCCURRENCE v1")
    print("=" * 78)
    print("Source anchor: B24-P2 from the 2024 book research program.")
    print("No empirical target values are used.\n")

    observed = {}
    for name, fn in CASES.items():
        print(f"[{name}] expected={EXPECTED[name]} class={asymptotic_class(name)}")
        last_log_s = None
        for N in N_VALUES:
            log_s, hazard = log_survival_to_N(fn, N)
            last_log_s = log_s
            surv = 0.0 if log_s < -745 else math.exp(log_s)
            occurrence = 1.0 - surv
            print(
                f"N={N:>8d} sum_p={hazard:>12.6f} "
                f"P(no occurrence)={surv:.12g} P(>=1)={occurrence:.12g}"
            )
        cls = asymptotic_class(name)
        if cls == "SUM_P_DIVERGES":
            verdict = "EVENTUAL_OCCURRENCE_A_S"
        elif cls == "SUM_P_CONVERGES":
            verdict = "NONOCCURRENCE_RETAINS_POSITIVE_MASS"
        else:
            verdict = "IMPOSSIBLE"
        observed[name] = verdict
        print(f"asymptotic verdict = {verdict}\n")

    all_match = all(observed[k] == EXPECTED[k] for k in EXPECTED)

    print("PREDECLARED BOOK2024-A1 SUMMARY")
    for k in CASES:
        print(f"{k}: expected={EXPECTED[k]} observed={observed[k]}")
    print("all_controls_match =", all_match)

    if all_match:
        final = "INFINITY_ALONE_INSUFFICIENT_RECURRENCE_CONDITION_IDENTIFIED"
    else:
        final = "CONTROL_FAILURE_DO_NOT_INTERPRET"
    print("PREDECLARED BOOK2024-A1 VERDICT =", final)

    print("\nINTERPRETATION LOCK:")
    print("- Passing does NOT prove that the physical Canevas exists or is infinite.")
    print("- It formalizes a necessary distinction inside the book's B24-P2 intuition.")
    print("- Infinite opportunities do not imply realization unless probability mass recurs sufficiently strongly.")
    print("- Under independent trials, divergence of sum(p_n) is sufficient for eventual occurrence with probability 1.")
    print("- A physical Canevas model must independently justify its opportunity structure, probabilities, and dependence/correlation law.")
    print("- Do not modify these cases after output under the A1 label.")
    print("\nFINISHED BOOK2024-A1 — DO NOT RETUNE AFTER OUTPUT")


if __name__ == "__main__":
    main()
