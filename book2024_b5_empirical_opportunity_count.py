"""BOOK2024-B5 — empirical astrophysical opportunity-count bridge v1

Preregistered before output.
Question: using published astronomical scale estimates only, how large can the pool of
physically plausible rocky/HZ *world opportunities* be before any unknown biology,
intelligence, expansion, persistence, or detectability factors are applied?

IMPORTANT: N_world is NOT the B4 effective independent civilization count.
This script deliberately keeps an explicit unknown conversion q from worlds to effective
B4 opportunities. It therefore cannot by itself prove a Fermi anomaly or finite lifetimes.
"""

# Published anchor used in this preregistration:
# NASA summary of Bryson et al. (2020): at least ~300 million rocky potentially habitable
# worlds in the Milky Way under the conservative interpretation; average expected rate
# can be higher. We use 300M as the fixed conservative world-pool anchor.
N_ROCKY_HZ_CONSERVATIVE = 300_000_000

# B3 literature anchor/sensitivity: ~75% of terrestrial/GHZ systems older than Earth/Sun.
# Because this is not a direct age census of the exact 300M Bryson population, treat it
# as a sensitivity bridge, not a measured intersection.
OLDER_FRACTIONS = [0.50, 0.75]

# q converts an older rocky/HZ world into an EFFECTIVE independent B4 opportunity.
# It absorbs all unsupported filters before the B4 Bernoulli trial definition, including
# suitability beyond crude HZ/rocky criteria and independence/effective-count reduction.
# Biology/intelligence/expansion/persistence/detectability are NOT claimed measured here.
Q_GRID = [1.0, 0.1, 0.01, 0.001, 1e-4, 1e-5, 1e-6, 1e-7]

# B4 one-sided 95% null bound: P(0|N,p)=0.05 -> pmax=1-0.05^(1/N)
def p95max(N):
    return 1.0 - 0.05 ** (1.0 / N)

print("="*82)
print("BOOK2024-B5 — EMPIRICAL ASTROPHYSICAL OPPORTUNITY-COUNT BRIDGE v1")
print("="*82)
print(f"fixed conservative rocky/HZ world pool = {N_ROCKY_HZ_CONSERVATIVE:,}")
print("older-world fraction is a sensitivity bridge, not a measured intersection.")
print("q is explicitly unknown; N_eff = N_world * f_older * q.\n")

for f_old in OLDER_FRACTIONS:
    raw_old = N_ROCKY_HZ_CONSERVATIVE * f_old
    print(f"[OLDER_FRACTION={f_old:.2f}] raw older-world pool={raw_old:,.0f}")
    for q in Q_GRID:
        N_eff = raw_old * q
        if N_eff < 1:
            bound = float('nan')
            label = "N_EFF_LT_1"
        else:
            bound = p95max(N_eff)
            if bound < 1e-8: label="EXTREME_COMBINED_BOUND"
            elif bound < 1e-5: label="STRONG_COMBINED_BOUND"
            elif bound < 1e-3: label="SUBPERCENT_COMBINED_BOUND"
            else: label="WEAK_COMBINED_BOUND"
        print(f"q={q:.0e} N_eff={N_eff:,.3f} p95max={bound:.6g} class={label}")
    print()

# Critical q required to retain selected B4 effective-N scales.
TARGET_N = [1_000, 100_000, 1_000_000, 100_000_000]
print("CRITICAL q NEEDED TO REACH B4 EFFECTIVE-N SCALES")
for f_old in OLDER_FRACTIONS:
    raw_old = N_ROCKY_HZ_CONSERVATIVE * f_old
    print(f"older_fraction={f_old:.2f}")
    for target in TARGET_N:
        qcrit = target / raw_old
        print(f"  target_N={target:>11,d} q_required={qcrit:.6g}  (~1 in {1/qcrit:,.1f} older rocky/HZ worlds)")

print("\nPREDECLARED BOOK2024-B5 SUMMARY")
raw75 = N_ROCKY_HZ_CONSERVATIVE * 0.75
q_for_1m = 1_000_000/raw75
q_for_100k = 100_000/raw75
print(f"75pct sensitivity raw older-world pool = {raw75:,.0f}")
print(f"q needed for N_eff=100,000 = {q_for_100k:.6g}")
print(f"q needed for N_eff=1,000,000 = {q_for_1m:.6g}")
print("PREDECLARED BOOK2024-B5 VERDICT = LARGE_ASTROPHYSICAL_WORLD_POOL_EXISTS_BUT_EFFECTIVE_FERMI_N_REMAINS_CONVERSION_LIMITED")

print("\nINTERPRETATION LOCK:")
print("- 300 million is a published conservative estimate of rocky potentially habitable worlds, not inhabited worlds.")
print("- The 75% older fraction is from a different population/model and is used only as a sensitivity bridge; multiplying them is NOT a measured intersection.")
print("- q is unknown and must not be fitted from the Fermi null under the B5 label.")
print("- B5 does not estimate abiogenesis, intelligence, expansion, civilization lifetime, colonization persistence, or detectability.")
print("- Therefore B5 cannot turn B4 into a physical bound unless independent evidence later constrains q/effective N.")
print("- The useful output is the q threshold required for each B4 regime: it tells future empirical work how much attrition the huge astronomical pool can tolerate.")
print("- Do not retune the world count, older fractions, q grid, or B4 thresholds after output under B5.")
print("\nFINISHED BOOK2024-B5 — DO NOT RETUNE AFTER OUTPUT")