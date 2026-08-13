"""CANEVAS SELF-LOCATION D6.3 — MEASURE-ADDITIVITY BRIDGE TEST v1

PREDECLARED before output. Blind to birth rank/year and D2-D4.
Goal: ask whether generic consistency principles alone force observer measure
to be additive over distinct physical event tokens established by D6.2.

Important: this is a finite functional-equation sieve, not a proof about
consciousness or the Canevas.
"""
import math

# Candidate measure laws M(n), normalized M(1)=1.
def linear(n): return float(n)
def constant(n): return 1.0 if n > 0 else 0.0
def sqrt_law(n): return math.sqrt(n)
def log_law(n): return math.log2(n+1.0)
def square(n): return float(n*n)
def saturating(n): return 2.0*n/(n+1.0)

CANDIDATES={
    'LINEAR_TOKEN':linear,
    'QUOTIENT_CONSTANT':constant,
    'SQRT':sqrt_law,
    'LOG2_NPLUS1':log_law,
    'SQUARE':square,
    'SATURATING':saturating,
}
EPS=1e-10

def close(a,b): return abs(a-b)<EPS

def tests(fn):
    # A normalization/null
    A=close(fn(0),0.0) and close(fn(1),1.0)
    # B label invariance is represented by dependence on n only.
    B=True
    # C disjoint-union additivity, stated without anthropic/self-location data.
    # This is the substantive bridge candidate and must be reported separately.
    C=all(close(fn(a+b),fn(a)+fn(b)) for a,b in [(1,1),(1,2),(2,3),(3,5),(4,7)])
    # D regrouping consistency: grouping a disjoint union cannot change measure.
    D=all(close(fn(a+b+c),fn(a)+fn(b)+fn(c)) for a,b,c in [(1,1,1),(1,2,3),(2,3,4)])
    # E replication homogeneity for integer copies.
    E=all(close(fn(k*n),k*fn(n)) for n,k in [(1,2),(1,5),(2,3),(3,4)])
    # Weak principles excluding additivity/homogeneity.
    W=A and B and all(fn(n)>0 for n in range(1,9)) and all(fn(n+1)>=fn(n) for n in range(1,8))
    return A,B,C,D,E,W

def main():
    print('='*80)
    print('CANEVAS SELF-LOCATION D6.3 — MEASURE-ADDITIVITY BRIDGE TEST v1')
    print('='*80)
    print('Blind to birth rank/year and downstream anthropic attractiveness.')
    print('C/D/E are explicitly treated as substantive bridge assumptions, not free facts.\n')
    strong=[]; weak=[]
    for name,fn in CANDIDATES.items():
        A,B,C,D,E,W=tests(fn)
        if all([A,B,C,D,E]): strong.append(name)
        if W: weak.append(name)
        vals=', '.join(f'{fn(n):.4g}' for n in range(1,6))
        print(f'[{name}] A={A} B={B} C_add={C} D_group={D} E_rep={E} weak={W} M1..5=[{vals}]')

    print('\nPREDECLARED D6.3 SUMMARY')
    print('weak-principle survivors =',weak)
    print('A-E survivors =',strong)
    if strong==['LINEAR_TOKEN']:
        verdict='LINEAR_UNIQUE_GIVEN_ADDITIVITY_BRIDGE'
    elif len(strong)>1:
        verdict='BRIDGE_NOT_UNIQUE'
    else:
        verdict='NO_STRONG_SURVIVOR'
    print('PREDECLARED D6.3 VERDICT =',verdict)

    # Critical epistemic diagnostic.
    if len(weak)>1 and strong==['LINEAR_TOKEN']:
        bridge='ADDITIVITY_IS_DOING_THE_SELECTION_NOT_DERIVED_FROM_WEAK_AXIOMS'
    elif len(weak)==1 and weak==['LINEAR_TOKEN']:
        bridge='LINEAR_SELECTED_WITHOUT_ADDITIVITY'
    else:
        bridge='MEASURE_REMAINS_UNDERDETERMINED'
    print('PREDECLARED BRIDGE DIAGNOSTIC =',bridge)
    print('\nINTERPRETATION LOCK:')
    print('- If linear wins only after C/D/E, that does NOT independently derive COUNT measure.')
    print('- D and E are closely related consequences of finite additivity in this toy domain.')
    print('- The key scientific question is whether Canevas supplies an independent physical reason for C.')
    print('- D6.2 establishes distinct event tokens, not additive probability weight.')
    print('- No human self-location observation may be used to justify C after this output.')
    print('- Only LINEAR_SELECTED_WITHOUT_ADDITIVITY would constitute a genuine bridge derivation here.')
    print('\nFINISHED D6.3 v1 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__': main()
