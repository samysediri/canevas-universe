"""CANEVAS 2.0 P1.3 — EXACT ADDITIVITY STRESS TEST v1

PREREGISTERED BEFORE OUTPUT.

Purpose
-------
P1.2 showed that exact disjoint additivity + temporal subdivision consistency +
support homogeneity select DURATION_SUPPORT up to scale within the declared setting.
P1.3 does NOT search for a preferred self-location measure. It asks whether exact
additivity is physically coherent once event supports overlap or interact.

Toy ontology
------------
Each event token has duration d>0, support s>0, and an overlap fraction o in [0,1]
with another token. For truly disjoint events o=0. Exact additivity is required only
for o=0. We compare three extensions to overlapping pairs:

1) NAIVE_ADD: M = d1*s1 + d2*s2 for all overlaps.
2) UNION_SUPPORT: overlap is counted once using a union-like correction
   M = d1*s1 + d2*s2 - o*min(d1,d2)*min(s1,s2).
3) INTERACTION_BONUS: overlapping support can create extra integrated support
   M = d1*s1 + d2*s2 + k*o*min(d1,d2)*min(s1,s2), with frozen k=0.5.

All three coincide with exact additivity for disjoint pairs. The question is whether
P1.2's axioms by themselves determine the extension beyond the disjoint domain.
No observational/self-location data are used.
"""
import math

K=0.5
TOL=1e-10

PAIRS=[
    # d1,s1,d2,s2,overlap
    (1.0,1.0,2.0,1.5,0.0),
    (1.0,1.0,2.0,1.5,0.25),
    (1.0,1.0,2.0,1.5,0.75),
    (1.0,1.0,1.0,1.0,1.0),
    (3.0,0.5,1.5,2.0,0.5),
]

def base(d,s): return d*s

def naive(p):
    d1,s1,d2,s2,o=p
    return base(d1,s1)+base(d2,s2)

def union_support(p):
    d1,s1,d2,s2,o=p
    return base(d1,s1)+base(d2,s2)-o*min(d1,d2)*min(s1,s2)

def interaction_bonus(p):
    d1,s1,d2,s2,o=p
    return base(d1,s1)+base(d2,s2)+K*o*min(d1,d2)*min(s1,s2)

CANDS={'NAIVE_ADD':naive,'UNION_SUPPORT':union_support,'INTERACTION_BONUS':interaction_bonus}

def close(a,b): return abs(a-b)<=TOL*max(1.0,abs(a),abs(b))

def check(name,f):
    # B1 positivity
    B1=all(f(p)>=-TOL for p in PAIRS)
    # B2 permutation symmetry between event labels
    B2=True
    for d1,s1,d2,s2,o in PAIRS:
        if not close(f((d1,s1,d2,s2,o)),f((d2,s2,d1,s1,o))): B2=False; break
    # B3 exact additivity on the DISJOINT domain only
    B3=True
    for d1,s1,d2,s2,o in PAIRS:
        if o==0 and not close(f((d1,s1,d2,s2,o)),base(d1,s1)+base(d2,s2)):
            B3=False; break
    # B4 global support homogeneity
    c=3.7
    B4=True
    for d1,s1,d2,s2,o in PAIRS:
        p=(d1,s1,d2,s2,o); pc=(d1,c*s1,d2,c*s2,o)
        if not close(f(pc),c*f(p)): B4=False; break
    # B5 common time-rescaling homogeneity: multiplying all durations by c multiplies measure by c
    B5=True
    for d1,s1,d2,s2,o in PAIRS:
        p=(d1,s1,d2,s2,o); pc=(c*d1,s1,c*d2,s2,o)
        if not close(f(pc),c*f(p)): B5=False; break
    # B6 overlap continuity diagnostic using a small step near o=0
    B6=True
    for d1,s1,d2,s2,_ in PAIRS[:2]:
        a=f((d1,s1,d2,s2,0.0)); b=f((d1,s1,d2,s2,1e-8))
        if not math.isfinite(a) or not math.isfinite(b): B6=False
    return {'B1':B1,'B2':B2,'B3_disjoint_exact':B3,'B4':B4,'B5':B5,'B6':B6}

print('='*82)
print('CANEVAS 2.0 P1.3 — EXACT ADDITIVITY STRESS TEST v1')
print('='*82)
print('No self-location or observational data. Exact additivity is enforced only for physically disjoint events.\n')

survivors=[]
for n,f in CANDS.items():
    r=check(n,f); ok=all(r.values())
    if ok: survivors.append(n)
    print(f'{n:20s} '+' '.join(f'{k}={v}' for k,v in r.items())+f' survivor={ok}')

# Inequivalence on overlapping domain
inequiv=[]
for i,a in enumerate(survivors):
    for b in survivors[i+1:]:
        different=any(not close(CANDS[a](p),CANDS[b](p)) for p in PAIRS if p[4]>0)
        if different: inequiv.append((a,b))

if len(survivors)>1 and inequiv:
    verdict='DISJOINT_EXACT_ADDITIVITY_DOES_NOT_UNIQUELY_FIX_OVERLAPPING_EVENT_MEASURE'
elif len(survivors)==1:
    verdict='DECLARED_STRESS_AXIOMS_SELECT_SINGLE_OVERLAP_EXTENSION_WITHIN_FAMILY'
else:
    verdict='DECLARED_STRESS_AXIOMS_INCONSISTENT_WITH_CANDIDATE_EXTENSIONS'

print('\nP1.3 SUMMARY')
print(f'n_survivors = {len(survivors)}')
print(f'survivors = {survivors}')
print(f'inequivalent_overlapping_survivor_pairs = {inequiv}')
print(f'P1.3 PREDECLARED VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- P1.2 remains valid on its declared disjoint-event domain.')
print('- P1.3 asks whether that theorem extends uniquely to overlapping/interacting events; it does not alter P1.2 after output.')
print('- Multiple surviving overlap rules mean a new physical composition law is required before DURATION_SUPPORT can be used universally.')
print('- An interaction/overlap rule must be independently motivated; it may not be chosen to improve self-location agreement.')
print('- No birth rank, zeta value, observer location, or desired prediction may be used to select among surviving rules.')
print('\nFINISHED C2-P1.3 — DO NOT RETUNE AFTER OUTPUT')
