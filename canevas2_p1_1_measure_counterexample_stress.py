"""CANEVAS 2.0 P1.1 — ADVERSARIAL MEASURE COUNTEREXAMPLE STRESS TEST

PREREGISTERED BEFORE OUTPUT.

Purpose
-------
P1 found DURATION_SUPPORT as the only survivor within six hand-picked candidate
measures. P1.1 asks a stronger adversarial question: do the SAME axioms A1-A6
actually imply uniqueness, or can we explicitly construct inequivalent measures
outside the original candidate list that still satisfy all six?

No new observational data are used. No new axiom is added.
"""
from itertools import permutations
import math

HISTORIES={
    'single':[('A',1.0,1.0)],
    'clone_pair':[('A',1.0,1.0),('A',1.0,1.0)],
    'unequal_duration':[('A',1.0,1.0),('B',3.0,1.0)],
    'unequal_support':[('A',1.0,1.0),('B',1.0,4.0)],
    'mixed':[('A',0.5,2.0),('A',1.5,2.0),('B',2.0,0.5)],
}
TOL=1e-10

def close(a,b): return abs(a-b)<=TOL*max(1.0,abs(a),abs(b))
def split_token(h,idx=0):
    t,d,s=h[idx]
    return h[:idx]+[(t,d/2,s),(t,d/2,s)]+h[idx+1:]

# Baseline survivor from P1.
def M_duration(h): return sum(d*s for _,d,s in h)

# Adversarial family. The extra max-support term is:
# - positive,
# - permutation invariant,
# - monotone when adding a positive event,
# - unchanged by splitting a token into equal-duration clones with same support,
# - homogeneous of degree 1 in support.
# Clone distinction is retained because the duration term increases for a physical copy.
def make_M_lambda(lam):
    def f(h):
        return sum(d*s for _,d,s in h) + lam*max((s for _,d,s in h), default=0.0)
    return f

LAMBDAS=[0.0,0.1,1.0,10.0]


def check(f):
    A1=all(f(h)>=-TOL for h in HISTORIES.values())
    A2=True
    for h in HISTORIES.values():
        base=f(h)
        for p in permutations(h):
            if not close(base,f(list(p))): A2=False; break
        if not A2: break
    A3=all(f(h+[('NEW',0.7,1.3)])+TOL>=f(h) for h in HISTORIES.values())
    A4=f(HISTORIES['clone_pair'])>f(HISTORIES['single'])+TOL
    A5=all(close(f(h),f(split_token(h,0))) for h in HISTORIES.values())
    c=3.7
    A6=all(close(f([(t,d,c*s) for t,d,s in h]),c*f(h)) for h in HISTORIES.values())
    return {'A1':A1,'A2':A2,'A3':A3,'A4':A4,'A5':A5,'A6':A6}


def proportional(f,g):
    ratios=[]
    for h in HISTORIES.values():
        a=f(h); b=g(h)
        if abs(b)<=TOL:
            if abs(a)>TOL: return False
            continue
        ratios.append(a/b)
    return max(ratios)-min(ratios)<=1e-9*max(1.0,max(map(abs,ratios)))

print('='*84)
print('CANEVAS 2.0 P1.1 — ADVERSARIAL MEASURE COUNTEREXAMPLE STRESS TEST')
print('='*84)
print('Same P1 axioms A1-A6. No new observational data. No new axiom.\n')

survivors=[]
inequivalent=[]
for lam in LAMBDAS:
    f=make_M_lambda(lam)
    r=check(f); ok=all(r.values())
    prop=proportional(f,M_duration)
    print(f'lambda={lam:5.2f} '+ ' '.join(f'{k}={v}' for k,v in r.items()) + f' survivor={ok} proportional_to_duration={prop}')
    if ok: survivors.append(lam)
    if ok and not prop: inequivalent.append(lam)

if inequivalent:
    verdict='P1_AXIOMS_DO_NOT_UNIQUELY_DETERMINE_MEASURE_COUNTEREXAMPLES_EXIST'
else:
    verdict='NO_INEQUIVALENT_COUNTEREXAMPLE_FOUND_IN_DECLARED_ADVERSARIAL_FAMILY'

print('\nP1.1 SUMMARY')
print(f'n_lambda_candidates = {len(LAMBDAS)}')
print(f'surviving_lambdas = {survivors}')
print(f'inequivalent_surviving_lambdas = {inequivalent}')
print(f'P1.1 PREDECLARED VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- If any lambda>0 survives and is not proportional to DURATION_SUPPORT, P1 finite-family uniqueness is not a general theorem.')
print('- This does not prove the adversarial measure is physically correct; it only proves A1-A6 are insufficient for uniqueness.')
print('- Do not add a new axiom under the P1.1 label after seeing this output.')
print('- A future P1.2 may introduce a separately motivated exact disjoint-additivity axiom and attempt a true functional-equation derivation.')
print('\nFINISHED C2-P1.1 — DO NOT RETUNE AFTER OUTPUT')