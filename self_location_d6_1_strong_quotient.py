"""Canevas self-location D6.1 — adversarial clone/fragment test.

Independent of birth rank/year and D2-D4 outputs.
Purpose: repair the weak quotient candidate from D6 by distinguishing
physical supports from bookkeeping fragments, then ask whether the
same preregistered structural axioms still uniquely select physical count.
"""
from collections import defaultdict

EPS = 1e-12

# Each record: (physical_support_id, informational_state, bookkeeping_weight)
BASE = [("p0", "s", 1.0)]
PHYSICAL_CLONE = [("p0", "s", 1.0), ("p1", "s", 1.0)]
BOOKKEEPING_SPLIT = [("p0", "s", 0.4), ("p0", "s", 0.6)]
DOUBLE_SPLIT_CLONES = [
    ("p0", "s", 0.4), ("p0", "s", 0.6),
    ("p1", "s", 0.25), ("p1", "s", 0.75),
]
DIFFERENT_STATE = [("p0", "s", 1.0), ("p1", "t", 1.0)]
DUPLICATE_RECORD = [("p0", "s", 0.5), ("p0", "s", 0.5)]


def support_totals(records):
    out = defaultdict(float)
    for pid, state, w in records:
        out[(pid, state)] += w
    return out


def count_physical(records):
    """One unit per distinct realized physical support/state."""
    return float(len(support_totals(records)))


def quotient_info_causal_strong(records):
    """Best adversarial quotient candidate.

    Bookkeeping fragments of one physical support are recombined first.
    Physically distinct supports realizing the same informational state are
    then quotient-equivalent: one unit per informational state represented.
    """
    totals = support_totals(records)
    states = {state for (pid, state), total in totals.items() if total > EPS}
    return float(len(states))


def raw_record_count(records):
    """Deliberately naive control; should fail fragmentation invariance."""
    return float(len(records))


def close(a, b):
    return abs(a-b) < EPS


def axioms(fn):
    b = fn(BASE)
    clone = fn(PHYSICAL_CLONE)
    split = fn(BOOKKEEPING_SPLIT)
    double_split = fn(DOUBLE_SPLIT_CLONES)
    diff = fn(DIFFERENT_STATE)
    dup = fn(DUPLICATE_RECORD)

    # A positivity / normalization
    A = close(b, 1.0)
    # B bookkeeping fragmentation invariance
    B = close(split, b) and close(dup, b)
    # C physical-copy additivity: two causally distinct supports contribute twice
    C = close(clone, 2.0*b)
    # D fragmentation commutes with physical copying
    D = close(double_split, clone)
    # E distinct realized states on distinct supports remain additive
    E = close(diff, 2.0*b)
    return dict(A=A,B=B,C=C,D=D,E=E,base=b,clone=clone,split=split,
                double_split=double_split,different_state=diff,duplicate_record=dup)


def main():
    print("="*78)
    print("CANEVAS SELF-LOCATION D6.1 — STRONG QUOTIENT ADVERSARIAL TEST")
    print("="*78)
    print("Blind to birth rank/year and D2-D4 empirical outputs.")
    print("Question: after repairing quotient fragmentation, do A-E still select COUNT?")
    print()

    candidates = {
        "COUNT_PHYSICAL": count_physical,
        "QUOTIENT_INFO_CAUSAL_STRONG": quotient_info_causal_strong,
        "RAW_RECORD_COUNT_CONTROL": raw_record_count,
    }
    survivors=[]
    for name, fn in candidates.items():
        r=axioms(fn)
        core=all(r[k] for k in "ABCDE")
        if core: survivors.append(name)
        print(f"[{name}]")
        print(" ".join(f"{k}={r[k]}" for k in "ABCDE"))
        print(f" base={r['base']:.3f} physical_clone={r['clone']:.3f} split={r['split']:.3f} "
              f"double_split={r['double_split']:.3f} different_state={r['different_state']:.3f} "
              f"duplicate_record={r['duplicate_record']:.3f}")
        print()

    print("PREDECLARED D6.1 SUMMARY")
    print("core A-E survivors =", survivors)
    if survivors == ["COUNT_PHYSICAL"]:
        verdict="COUNT_SURVIVES_STRONG_QUOTIENT"
    elif "COUNT_PHYSICAL" in survivors and "QUOTIENT_INFO_CAUSAL_STRONG" in survivors:
        verdict="COUNT_QUOTIENT_UNDERDETERMINED"
    elif "QUOTIENT_INFO_CAUSAL_STRONG" in survivors and "COUNT_PHYSICAL" not in survivors:
        verdict="STRONG_QUOTIENT_SURVIVES_COUNT_FAILS"
    else:
        verdict="NO_UNIQUE_MEASURE"
    print("PREDECLARED D6.1 VERDICT =", verdict)
    print()
    print("INTERPRETATION LOCK:")
    print("- D6.1 is a logical stress test, not a theorem about consciousness.")
    print("- The strong quotient candidate explicitly repairs D6 bookkeeping fragmentation.")
    print("- A COUNT win means only that axiom C (physical-copy additivity), together with A-E, selects it.")
    print("- Therefore C must NOT be smuggled in as an empirical fact: it is the substantive clone premise.")
    print("- If COUNT and QUOTIENT both survive, observer measure remains underdetermined.")
    print("- No birth-rank evidence may be used to alter these axioms after this run.")
    print()
    print("FINISHED D6.1 v1 — DO NOT RETUNE AFTER OUTPUT")

if __name__ == "__main__":
    main()
