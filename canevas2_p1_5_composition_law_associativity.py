"""CANEVAS 2.0 P1.5 — COMPOSITION LAW / ASSOCIATIVITY STRESS TEST v1

PREREGISTERED BEFORE OUTPUT.

P1.4 established only:
- duplicate records of the SAME physical event must not be double-counted;
- distinct overlapping events remain underdetermined.

P1.5 does not use self-location data. It asks whether generic structural requirements
on a binary composition law for DISTINCT physical contributions can remove that
underdetermination.

Frozen requirements:
C1 identity bookkeeping invariance (duplicates canonicalized before composition)
C2 commutativity: a⊕b=b⊕a
C3 associativity: (a⊕b)⊕c=a⊕(b⊕c)
C4 neutral zero: a⊕0=a
C5 monotonicity for nonnegative contributions
C6 exact additivity in the declared noninteracting/disjoint limit
C7 positive homogeneity: (ka)⊕(kb)=k(a⊕b)

Candidate laws are declared before output. Passing does NOT prove a law is physical.
If inequivalent nonlinear laws survive, structural algebra alone does not uniquely
extend P1.2/P1.4 to interacting events.
"""
import math

TOL=1e-9
VALS=[0.0,0.2,0.7,1.0,2.3,5.0]
KS=[0.5,2.0,7.0]

# law(a,b,g): g is independently supplied interaction/overlap strength.
# g=0 is the disjoint/noninteracting limit and MUST recover a+b.
def additive(a,b,g): return a+b

def interaction_bonus(a,b,g):
    # homogeneous but generally non-associative when g>0
    return a+b+g*math.sqrt(max(a*b,0.0))

def lp_interaction(a,b,g):
    # interpolation: g=0 -> L1/additive; g=1 -> L2-like composition.
    # symmetric, homogeneous; associativity is not guaranteed for intermediate g.
    p=1.0+g
    return (a**p+b**p)**(1.0/p)

def max_interaction(a,b,g):
    # g=0 additive; g=1 max-like. convex interpolation, generally non-associative.
    return (1-g)*(a+b)+g*max(a,b)

LAWS={
    'ADDITIVE':additive,
    'SQRT_INTERACTION_BONUS':interaction_bonus,
    'LP_INTERACTION':lp_interaction,
    'MAX_INTERACTION':max_interaction,
}
GS=[0.0,0.25,0.5,1.0]

def close(x,y): return abs(x-y)<=TOL*max(1.0,abs(x),abs(y))

def tests(fn,g):
    C2=all(close(fn(a,b,g),fn(b,a,g)) for a in VALS for b in VALS)
    C3=all(close(fn(fn(a,b,g),c,g),fn(a,fn(b,c,g),g)) for a in VALS for b in VALS for c in VALS)
    C4=all(close(fn(a,0,g),a) for a in VALS)
    C5=True
    for a in VALS:
      for b1 in VALS:
       for b2 in VALS:
        if b2>=b1 and fn(a,b2,g)+TOL<fn(a,b1,g): C5=False
    # C6 is a property of each law family at g=0, regardless of current g.
    C6=all(close(fn(a,b,0.0),a+b) for a in VALS for b in VALS)
    C7=all(close(fn(k*a,k*b,g),k*fn(a,b,g)) for k in KS for a in VALS for b in VALS)
    return C2,C3,C4,C5,C6,C7

def signature(fn,g):
    return tuple(round(fn(a,b,g),8) for a,b in [(0.2,0.7),(1,1),(1,2.3),(2.3,5)])

def run():
    print('='*80)
    print('CANEVAS 2.0 P1.5 — COMPOSITION LAW / ASSOCIATIVITY STRESS TEST v1')
    print('='*80)
    print('No observational/self-location data. Interaction strength g is a structural test parameter.\n')
    survivors=[]
    for name,fn in LAWS.items():
      for g in GS:
        C2,C3,C4,C5,C6,C7=tests(fn,g)
        surv=all([C2,C3,C4,C5,C6,C7])
        if surv: survivors.append((name,g,signature(fn,g)))
        print(f'{name:24s} g={g:.2f} C2={C2} C3={C3} C4={C4} C5={C5} C6={C6} C7={C7} survivor={surv}')
    nonlinear=[x for x in survivors if x[1]>0 and x[2]!=signature(additive,0)]
    inequivalent=[]
    for i,a in enumerate(survivors):
      for b in survivors[i+1:]:
        if a[2]!=b[2]: inequivalent.append((a[:2],b[:2]))
    if nonlinear:
        verdict='GENERIC_ALGEBRAIC_AXIOMS_DO_NOT_FORCE_ADDITIVITY_FOR_INTERACTING_EVENTS'
    else:
        verdict='WITHIN_DECLARED_FAMILIES_ASSOCIATIVITY_AND_HOMOGENEITY_ELIMINATE_NONLINEAR_INTERACTION_RULES'
    print('\nP1.5 SUMMARY')
    print('n_survivors =',len(survivors))
    print('survivors =',[(n,g) for n,g,_ in survivors])
    print('nonlinear_interacting_survivors =',[(n,g) for n,g,_ in nonlinear])
    print('inequivalent_survivor_pairs =',inequivalent)
    print('P1.5 PREDECLARED VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- Passing algebraic tests does not establish a physical observer measure.')
    print('- Failure of candidate nonlinear laws does not prove all nonlinear laws impossible.')
    print('- If only additive composition survives, a later proof must establish this beyond the finite candidate families.')
    print('- If nonlinear laws survive, Canevas needs an independently motivated physical interaction/composition principle.')
    print('- Do not choose g or a law using observer location, zeta, or desired phenomenology after output.')
    print('\nFINISHED C2-P1.5 — DO NOT RETUNE AFTER OUTPUT')
if __name__=='__main__': run()
