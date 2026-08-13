"""CANEVAS 2.0 P1 — MEASURE THEOREM ATTEMPT v1

PREREGISTERED BEFORE OUTPUT.

Goal
----
Test whether the surviving qualitative principles of Canevas 2.0 uniquely force a
measure over observer-supporting physical event tokens, or whether multiple
inequivalent measures satisfy the same declared axioms.

This is a logical/model-identifiability sieve. It is NOT evidence about nature and
uses no observed self-location data.

Toy ontology
------------
A history consists of event TOKENS. Tokens may belong to the same physical TYPE but
occur as distinct copies. Each token has:
- duration d > 0
- support/intensity s > 0
- type label

Declared surviving axioms tested here:
A1 positivity: positive physical events receive nonnegative measure.
A2 permutation invariance: relabelling tokens does not change total measure.
A3 disjoint extensivity: adding a physically disjoint event cannot decrease total measure.
A4 clone distinction: two distinct physical copies are not required to collapse to one token.
A5 coarse-graining consistency: splitting one token into identical sub-tokens whose durations sum to the original should not change measure.
A6 scale homogeneity in support: multiplying all support values by c multiplies measure by c.

Candidate families are declared BEFORE output. We search for survivors and then
ask whether all survivors are proportional on all test histories. If not, the
axioms underdetermine the measure.
"""
from itertools import permutations
import math

# Histories: list of (type, duration, support)
HISTORIES={
    'single':[('A',1.0,1.0)],
    'clone_pair':[('A',1.0,1.0),('A',1.0,1.0)],
    'unequal_duration':[('A',1.0,1.0),('B',3.0,1.0)],
    'unequal_support':[('A',1.0,1.0),('B',1.0,4.0)],
    'mixed':[('A',0.5,2.0),('A',1.5,2.0),('B',2.0,0.5)],
}

# Candidate measures. No parameter will be selected after output.
def M_count(h): return sum(s for _,d,s in h)
def M_duration(h): return sum(d*s for _,d,s in h)
def M_sqrt_duration(h): return sum(math.sqrt(d)*s for _,d,s in h)
def M_type_quotient(h):
    # collapse physical copies by type, then count max support per type
    by={}
    for t,d,s in h: by[t]=max(by.get(t,0.0),s)
    return sum(by.values())
def M_duration_squared(h): return sum((d*d)*s for _,d,s in h)

def M_log_duration(h): return sum(math.log1p(d)*s for _,d,s in h)

CANDS={
    'COUNT_SUPPORT':M_count,
    'DURATION_SUPPORT':M_duration,
    'SQRT_DURATION_SUPPORT':M_sqrt_duration,
    'TYPE_QUOTIENT_SUPPORT':M_type_quotient,
    'DURATION2_SUPPORT':M_duration_squared,
    'LOG1P_DURATION_SUPPORT':M_log_duration,
}

TOL=1e-10

def close(a,b): return abs(a-b)<=TOL*max(1.0,abs(a),abs(b))

def split_token(h,idx=0):
    t,d,s=h[idx]
    if d<=0: raise ValueError
    return h[:idx]+[(t,d/2,s),(t,d/2,s)]+h[idx+1:]


def check(name,f):
    A1=all(f(h)>=-TOL for h in HISTORIES.values())
    A2=True
    for h in HISTORIES.values():
        base=f(h)
        for p in permutations(h):
            if not close(base,f(list(p))): A2=False; break
        if not A2: break
    # A3: append disjoint positive token
    A3=all(f(h+[('NEW',0.7,1.3)])+TOL>=f(h) for h in HISTORIES.values())
    # A4: distinct clone pair should have strictly more measure than one physical token
    A4=f(HISTORIES['clone_pair'])>f(HISTORIES['single'])+TOL
    # A5: splitting any first token by duration must preserve measure
    A5=all(close(f(h),f(split_token(h,0))) for h in HISTORIES.values())
    # A6: scale all supports by fixed c
    c=3.7
    A6=True
    for h in HISTORIES.values():
        hs=[(t,d,c*s) for t,d,s in h]
        if not close(f(hs),c*f(h)): A6=False; break
    return {'A1':A1,'A2':A2,'A3':A3,'A4':A4,'A5':A5,'A6':A6}

print('='*82)
print('CANEVAS 2.0 P1 — MEASURE THEOREM ATTEMPT v1')
print('='*82)
print('No observed self-location data are used.\n')

survivors=[]
results={}
for n,f in CANDS.items():
    r=check(n,f); results[n]=r
    ok=all(r.values())
    if ok: survivors.append(n)
    print(f'{n:28s} '+ ' '.join(f'{k}={v}' for k,v in r.items()) + f' survivor={ok}')

# Distinctness test: survivors are equivalent only if ratios are constant across histories.
def proportional(f,g):
    ratios=[]
    for h in HISTORIES.values():
        a=f(h); b=g(h)
        if abs(b)<=TOL:
            if abs(a)>TOL: return False
            continue
        ratios.append(a/b)
    return max(ratios)-min(ratios)<=1e-9*max(1.0,max(map(abs,ratios))) if ratios else True

inequivalent=[]
for i,a in enumerate(survivors):
    for b in survivors[i+1:]:
        if not proportional(CANDS[a],CANDS[b]): inequivalent.append((a,b))

unique_up_to_scale=(len(survivors)>=1 and len(inequivalent)==0)

print('\nP1 SUMMARY')
print(f'n_candidates = {len(CANDS)}')
print(f'n_survivors = {len(survivors)}')
print(f'survivors = {survivors}')
print(f'inequivalent_survivor_pairs = {inequivalent}')
print(f'unique_measure_up_to_scale = {unique_up_to_scale}')

if len(survivors)==0:
    verdict='DECLARED_AXIOMS_INCONSISTENT_WITH_CANDIDATE_FAMILY'
elif unique_up_to_scale:
    verdict='DECLARED_AXIOMS_SELECT_UNIQUE_MEASURE_WITHIN_CANDIDATE_FAMILY'
else:
    verdict='DECLARED_AXIOMS_UNDERDETERMINE_MEASURE'
print(f'P1 PREDECLARED VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- P1 is a logical sieve over a finite declared candidate family, not a theorem over all possible measures.')
print('- Multiple inequivalent survivors are sufficient to show these axioms do not uniquely determine a measure within this family.')
print('- A unique survivor would not prove nature uses it; it would only justify a stronger theorem attempt.')
print('- No birth rank, zeta value, observer location, or desired prediction may be used to add axioms after output under the P1 label.')
print('- Any new axiom must be independently motivated and tested in a separately labelled P1.x experiment.')
print('\nFINISHED C2-P1 — DO NOT RETUNE AFTER OUTPUT')