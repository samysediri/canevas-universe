"""BOOK2024-B4 — Fermi bottleneck bound v1

Preregistered before output.
Purpose: translate a null observation into a bound on a COMBINED bottleneck probability,
not identify civilization lifetime or any single Drake-like factor.

Toy/statistical bridge only. It uses no claim that every older world is inhabited.
"""
import math

# Fixed, transparent opportunity-count grid. These are scenario counts, not measurements.
N_OPPORTUNITIES = [10, 100, 1_000, 10_000, 100_000, 1_000_000, 100_000_000]
# Probability of zero observed arrivals/signatures under independent Bernoulli opportunities.
# We report one-sided 95% and 50% upper bounds on the combined success probability p.
ZERO_PROB_LEVELS = {"95pct_upper": 0.05, "median_boundary": 0.50}

print("="*78)
print("BOOK2024-B4 — FERMI BOTTLENECK BOUND v1")
print("="*78)
print("Null-observation bridge: P(0 | N,p)=(1-p)^N.")
print("p is the full combined chain: emergence × expansion × persistence × reach × detectability.")
print("N is an effective number of independent prior opportunities; B4 does NOT estimate N.")
print("No factor of p may be identified individually from this test.\n")

rows=[]
for N in N_OPPORTUNITIES:
    vals={}
    for label, alpha in ZERO_PROB_LEVELS.items():
        # Solve (1-p)^N = alpha exactly.
        pmax = 1.0 - alpha**(1.0/N)
        vals[label]=pmax
    rows.append((N, vals))
    print(f"N={N:>9,d}  p_95max={vals['95pct_upper']:.6g}  p_50boundary={vals['median_boundary']:.6g}  "
          f"approx_3_over_N={3/N:.6g}")

# Fixed interpretive thresholds, declared before seeing output.
# These classify the COMBINED bottleneck only.
def classify(p):
    if p < 1e-8: return "EXTREME_COMBINED_BOTTLENECK"
    if p < 1e-5: return "STRONG_COMBINED_BOTTLENECK"
    if p < 1e-3: return "SUBPERCENT_COMBINED_BOTTLENECK"
    return "WEAK_OR_UNCONSTRAINED_COMBINED_BOTTLENECK"

print("\nPREDECLARED BOOK2024-B4 SUMMARY")
for N, vals in rows:
    print(f"N={N:>9,d}  class95={classify(vals['95pct_upper'])}")

# The result can only establish how p scales with an assumed/effective N.
largeN = rows[-1][1]['95pct_upper']
if largeN < 1e-8:
    verdict="LARGE_EFFECTIVE_OPPORTUNITY_COUNTS_REQUIRE_EXTREME_COMBINED_BOTTLENECK"
elif largeN < 1e-5:
    verdict="LARGE_EFFECTIVE_OPPORTUNITY_COUNTS_REQUIRE_STRONG_COMBINED_BOTTLENECK"
else:
    verdict="NULL_ALONE_DOES_NOT_REQUIRE_STRONG_COMBINED_BOTTLENECK"
print(f"PREDECLARED BOOK2024-B4 VERDICT = {verdict}")

print("\nINTERPRETATION LOCK:")
print("- B4 does NOT prove civilizations are short-lived.")
print("- B4 does NOT estimate the true number of inhabited, technological, or expansive worlds.")
print("- p is a product/aggregate bottleneck; rarity, non-expansion, finite persistence, reach, and detectability remain degenerate.")
print("- The opportunity-count grid is a sensitivity analysis, not an empirical prior.")
print("- A strong bound becomes physically informative only after an independent empirical model constrains effective N.")
print("- Do not tune N grid, confidence levels, or classification thresholds after output under the B4 label.")
print("\nFINISHED BOOK2024-B4 — DO NOT RETUNE AFTER OUTPUT")