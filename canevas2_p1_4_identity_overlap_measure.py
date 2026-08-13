"""CANEVAS 2.0 P1.4 — PHYSICAL IDENTITY VS OVERLAP MEASURE v1

PREREGISTERED BEFORE OUTPUT.

Purpose
-------
P1.2 established a conditional duration×support result for disjoint event tokens.
P1.3 showed that disjoint exact additivity does not determine how overlapping /
interacting events compose. P1.4 asks whether a physically motivated distinction
between (i) duplicate REPRESENTATIONS of one physical event and (ii) genuinely
DISTINCT physical events occupying the same interval resolves that ambiguity.

No self-location or observational data are used.

Ontology
--------
Each record has (physical_id, t0, t1, support). Two identical records with the same
physical_id are duplicate representations of one physical event and should not be
double-counted. Two records with different physical_id values are distinct physical
events even if their intervals and supports coincide.

New independently motivated axiom B7 — representation invariance:
Duplicating an identical record for the SAME physical_id does not change measure.
This is a bookkeeping/ontology axiom, not an observer-selection axiom.

Retained requirements:
B1 positivity.
B2 permutation invariance.
B3 exact additivity for physically disjoint collections.
B4 physical-copy distinction: distinct physical_ids can contribute separately.
B5 temporal subdivision invariance for one physical event.
B6 support homogeneity.
B7 representation invariance for duplicate records of the same event.

This test deliberately does NOT add a no-interaction axiom. If both a pure identity-
union rule and an interaction rule survive B1-B7, overlap composition remains
physically underdetermined.
"""
from itertools import permutations
import math

TOL=1e-10

def close(a,b): return abs(a-b)<=TOL*max(1.0,abs(a),abs(b))
def dur(r): return max(0.0,r[2]-r[1])

# records: (physical_id, t0, t1, support)
SINGLE=[('A',0.0,1.0,1.0)]
DUP_REP=[('A',0.0,1.0,1.0),('A',0.0,1.0,1.0)]
DISTINCT_COINCIDENT=[('A',0.0,1.0,1.0),('B',0.0,1.0,1.0)]
DISJOINT_A=[('A',0.0,1.0,2.0)]
DISJOINT_B=[('B',2.0,4.0,3.0)]
SUBDIV=[('A',0.0,0.4,1.0),('A',0.4,1.0,1.0)]
OVERLAP_DISTINCT=[('A',0.0,2.0,1.0),('B',1.0,3.0,2.0)]

# canonicalize exact duplicate representations only.
def unique_records(h):
    out=[]; seen=set()
    for r in h:
        key=(r[0],r[1],r[2],r[3])
        if key not in seen:
            seen.add(key); out.append(r)
    return out

def base_identity_measure(h):
    # sum unique record pieces; adjacent subdivision pieces of same physical_id add.
    return sum(dur(r)*r[3] for r in unique_records(h))

def M_naive_records(h):
    return sum(dur(r)*r[3] for r in h)

def M_identity_union(h):
    return base_identity_measure(h)

def M_spacetime_union(h):
    # ignores physical identity and counts only maximum support at each time slice.
    rec=unique_records(h)
    pts=sorted(set([x for r in rec for x in (r[1],r[2])]))
    total=0.0
    for a,b in zip(pts,pts[1:]):
        mid=(a+b)/2
        active=[r[3] for r in rec if r[1]<=mid<r[2]]
        if active: total+=(b-a)*max(active)
    return total

def overlap_len(r1,r2): return max(0.0,min(r1[2],r2[2])-max(r1[1],r2[1]))

def M_distinct_interaction(h):
    # same bookkeeping invariance, but adds a symmetric positive interaction for
    # overlapping DISTINCT physical events. Coefficient fixed before output.
    rec=unique_records(h)
    total=sum(dur(r)*r[3] for r in rec)
    eta=0.25
    bonus=0.0
    for i,a in enumerate(rec):
        for b in rec[i+1:]:
            if a[0]==b[0]: continue
            bonus += eta*overlap_len(a,b)*math.sqrt(a[3]*b[3])
    return total+bonus

CANDS={
    'NAIVE_RECORD_SUM':M_naive_records,
    'IDENTITY_UNION':M_identity_union,
    'SPACETIME_UNION':M_spacetime_union,
    'DISTINCT_INTERACTION':M_distinct_interaction,
}

def scale_support(h,c): return [(pid,t0,t1,c*s) for pid,t0,t1,s in h]

def check(f):
    B1=all(f(h)>=-TOL for h in [SINGLE,DUP_REP,DISTINCT_COINCIDENT,OVERLAP_DISTINCT])
    # permutation invariance
    B2=True
    for h in [DUP_REP,DISTINCT_COINCIDENT,OVERLAP_DISTINCT]:
        v=f(h)
        if any(not close(v,f(list(p))) for p in permutations(h)): B2=False
    # exact additivity for temporally disjoint collections
    B3=close(f(DISJOINT_A+DISJOINT_B),f(DISJOINT_A)+f(DISJOINT_B))
    # distinct coincident physical copy must add positive measure beyond one copy
    B4=f(DISTINCT_COINCIDENT)>f(SINGLE)+TOL
    # subdivision of same physical event preserves total
    B5=close(f(SINGLE),f(SUBDIV))
    # support homogeneity
    c=3.7
    B6=all(close(f(scale_support(h,c)),c*f(h)) for h in [SINGLE,DISTINCT_COINCIDENT,OVERLAP_DISTINCT])
    # representation invariance for duplicated identical record of same physical id
    B7=close(f(SINGLE),f(DUP_REP))
    return {'B1':B1,'B2':B2,'B3':B3,'B4':B4,'B5':B5,'B6':B6,'B7':B7}

print('='*86)
print('CANEVAS 2.0 P1.4 — PHYSICAL IDENTITY VS OVERLAP MEASURE v1')
print('='*86)
print('No self-location or observational data. B7 representation invariance is the only new axiom.\n')

survivors=[]; results={}
for name,f in CANDS.items():
    r=check(f); results[name]=r; ok=all(r.values())
    if ok: survivors.append(name)
    print(f'{name:24s} '+' '.join(f'{k}={v}' for k,v in r.items())+f' survivor={ok}')

# Compare survivors on the overlapping-distinct test history after normalizing to SINGLE.
def normalized_value(f,h): return f(h)/f(SINGLE)
inequiv=[]
for i,a in enumerate(survivors):
    for b in survivors[i+1:]:
        if not close(normalized_value(CANDS[a],OVERLAP_DISTINCT),normalized_value(CANDS[b],OVERLAP_DISTINCT)):
            inequiv.append((a,b))

if len(survivors)==1:
    verdict='IDENTITY_DISTINCTION_SELECTS_UNIQUE_OVERLAP_RULE_WITHIN_CANDIDATES'
elif inequiv:
    verdict='IDENTITY_DISTINCTION_SOLVES_DOUBLE_COUNTING_BUT_OVERLAP_INTERACTION_REMAINS_UNDERDETERMINED'
else:
    verdict='SURVIVING_RULES_EQUIVALENT_ON_TEST_DOMAIN'

print('\nP1.4 SUMMARY')
print(f'n_candidates = {len(CANDS)}')
print(f'n_survivors = {len(survivors)}')
print(f'survivors = {survivors}')
print(f'inequivalent_overlapping_survivor_pairs = {inequiv}')
for n in survivors:
    print(f'{n}_overlap_normalized = {normalized_value(CANDS[n],OVERLAP_DISTINCT):.12g}')
print(f'P1.4 PREDECLARED VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- B7 distinguishes duplicate bookkeeping from genuine physical multiplicity.')
print('- Passing B1-B7 does not prove a candidate is nature\'s observer measure.')
print('- If IDENTITY_UNION and DISTINCT_INTERACTION both survive, no interaction law may be chosen from self-location fit.')
print('- P1.2 remains a conditional theorem on genuinely disjoint event pieces.')
print('- A later P1.5 may add a separability/locality principle only if independently motivated from physical ontology, not to force IDENTITY_UNION.')
print('\nFINISHED C2-P1.4 — DO NOT RETUNE AFTER OUTPUT')
