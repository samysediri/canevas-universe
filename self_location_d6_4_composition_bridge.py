import math

# CANEVAS D6.4 — preregistered composition bridge diagnostic
# Blind to birth rank/year and downstream self-location outputs.
# Purpose: determine whether ordinary composition/extensivity can derive
# observer-measure additivity without assuming that bridge.

EPS = 1e-10

def close(a,b):
    return abs(a-b) < EPS

LAWS = {
    'LINEAR': lambda n: float(n),
    'CONSTANT': lambda n: 0.0 if n == 0 else 1.0,
    'SQRT': lambda n: math.sqrt(n),
    'LOG': lambda n: math.log2(n+1),
    'SQUARE': lambda n: float(n*n),
    'SATURATING': lambda n: 0.0 if n == 0 else 2*n/(n+1),
}

def composition_tests(f):
    null = close(f(0),0)
    unit = close(f(1),1)
    permutation = True
    disjoint_add = all(close(f(a+b), f(a)+f(b)) for a,b in [(1,1),(1,3),(2,5),(4,7)])
    coarsegrain = all(close(f(sum(p)), sum(f(x) for x in p)) for p in [(1,1,1),(1,2,4),(2,3,5)])
    return null, unit, permutation, disjoint_add, coarsegrain

def main():
    print('='*78)
    print('CANEVAS SELF-LOCATION D6.4 — COMPOSITION BRIDGE DIAGNOSTIC v1')
    print('='*78)
    print('Stage 1: generic non-anthropic extensive composition.')
    print('Stage 2: explicit audit of transfer to observer measure.\n')

    survivors=[]
    for name,f in LAWS.items():
        t=composition_tests(f)
        passed=all(t)
        if passed:
            survivors.append(name)
        print(f'[{name}] null={t[0]} unit={t[1]} perm={t[2]} add={t[3]} coarsegrain={t[4]} pass={passed}')

    stage1 = survivors == ['LINEAR']
    print('\nSTAGE 1 SUMMARY')
    print('survivors =', survivors)
    print('generic extensive composition uniquely linear =', stage1)

    # Critical preregistered bridge audit:
    # D6.2 establishes distinct event tokens, but no prior independent result
    # establishes that observer measure is an extensive physical quantity.
    distinct_event_tokens = True
    generic_extensivity_linear = stage1
    independent_observer_extensivity_theorem = False

    print('\nSTAGE 2 BRIDGE AUDIT')
    print('distinct physical event tokens =', distinct_event_tokens)
    print('generic extensivity is linear =', generic_extensivity_linear)
    print('independent theorem: observer measure is extensive =', independent_observer_extensivity_theorem)

    if stage1 and independent_observer_extensivity_theorem:
        verdict='OBSERVER_ADDITIVITY_DERIVED'
    elif stage1:
        verdict='GENERIC_EXTENSIVITY_DOES_NOT_DERIVE_OBSERVER_ADDITIVITY'
    else:
        verdict='GENERIC_COMPOSITION_FAILED_TO_SELECT_LINEARITY'

    print('\nPREDECLARED D6.4 VERDICT =', verdict)
    print('\nINTERPRETATION LOCK:')
    print('- Linearity of an ordinary extensive quantity follows because disjoint additivity is part of extensivity.')
    print('- This does not prove that observer probability/measure is itself extensive.')
    print('- Distinct physical copies/events alone do not supply probability weights.')
    print('- No self-location or birth-rank result may be used to introduce that missing premise after output.')
    print('- A negative bridge result closes this route unless an independently motivated observer ontology supplies additivity.')
    print('\nFINISHED D6.4 v1 — DO NOT RETUNE AFTER OUTPUT')

if __name__ == '__main__':
    main()
