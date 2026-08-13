"""CANEVAS SELF-LOCATION D5 — OBSERVER-MEASURE AXIOM SIEVE v1

PREDECLARED before observing D5 output.

Goal:
Test whether a small set of structural desiderata can uniquely select an
observer measure, WITHOUT using Samy's birth year/rank, D2, D3, or D4 outputs.

This is a logical/axiomatic sieve, not an empirical consciousness test.

Toy observer records have fields:
 support s in (0,1], duration tau>0, multiplicity m>=1, representation copies k>=1.

Candidate measures (declared ex ante):
 M0 COUNT          = m
 M1 SUPPORT        = m*s
 M2 DURATION       = m*tau
 M3 SUPPORT_TIME   = m*s*tau
 M4 SQRT_ST        = m*sqrt(s*tau)
 M5 QUOTIENT_ST    = s*tau   (ignores exact duplicate multiplicity)

Frozen desiderata/tests:
 A LABEL_INVARIANCE: reordering/renaming records cannot change normalized weights.
 B SPLIT_INVARIANCE: splitting one observer-history into two adjacent pieces whose
   durations sum to tau should preserve its total weight when s is unchanged.
 C DISJOINT_ADDITIVITY: weight of disjoint union is sum of component weights.
 D CLONE_LINEARITY: n physically distinct exact copies carry n times the weight.
 E CLONE_QUOTIENT: alternatively, exact duplicate descriptions are quotient-equivalent
   and should NOT multiply measure. D and E are intentionally competing axioms.
 F SUPPORT_MONOTONICITY: with other fields fixed, larger support cannot get less weight.
 G ZERO_SUPPORT: s->0 should drive observer weight toward zero.

Logical lock:
- No single candidate is expected to satisfy both D and E; if D/E choice changes the
  selected measure family, observer measure remains underdetermined by the other axioms.
- A unique winner under BOTH clone conventions would count as strong selection.
- Multiple winners or convention-dependent winners => MEASURE_UNDERDETERMINED.

No result may be used to retrofit a measure toward median human birth rank.
"""
from __future__ import annotations
import math

CANDS=['COUNT','SUPPORT','DURATION','SUPPORT_TIME','SQRT_ST','QUOTIENT_ST']

def w(name,s,tau,m=1):
    if name=='COUNT': return float(m)
    if name=='SUPPORT': return float(m*s)
    if name=='DURATION': return float(m*tau)
    if name=='SUPPORT_TIME': return float(m*s*tau)
    if name=='SQRT_ST': return float(m*math.sqrt(s*tau))
    if name=='QUOTIENT_ST': return float(s*tau)
    raise ValueError(name)

def approx(a,b,tol=1e-10): return abs(a-b)<=tol*max(1.0,abs(a),abs(b))

def tests(name):
    # A: labels/reorder irrelevant by construction if same scalar records sum.
    rec=[(.2,2,1),(.8,3,2),(.5,1,1)]
    a=approx(sum(w(name,*r) for r in rec),sum(w(name,*r) for r in reversed(rec)))
    # B: split duration while preserving support and multiplicity 1.
    base=w(name,.7,5,1); split=w(name,.7,2,1)+w(name,.7,3,1)
    b=approx(base,split)
    # C: disjoint additivity at aggregate level.
    left=w(name,.4,2,1)+w(name,.9,1,1); right=w(name,.5,4,2)
    c=approx(left+right,sum([w(name,.4,2,1),w(name,.9,1,1),w(name,.5,4,2)]))
    # D clone linearity.
    one=w(name,.6,2,1); four=w(name,.6,2,4); d=approx(four,4*one)
    # E quotient duplicates.
    e=approx(four,one)
    # F support monotonicity.
    f=w(name,.8,2,1)>=w(name,.2,2,1)-1e-12
    # G zero support limit proxy s=1e-12 relative to s=1.
    g=w(name,1e-12,2,1) <= 1e-5*max(w(name,1.0,2,1),1e-300)
    return dict(A=a,B=b,C=c,D=d,E=e,F=f,G=g)

print('='*84)
print('CANEVAS SELF-LOCATION D5 — OBSERVER-MEASURE AXIOM SIEVE v1')
print('='*84)
print('Independent of birth rank/year and D2-D4 numerical outputs.')
print('D=clone-linearity and E=clone-quotient are competing conventions.\n')

out={n:tests(n) for n in CANDS}
for n,t in out.items():
    print(f'[{n}] '+' '.join(f'{k}={v}' for k,v in t.items()))

core=['A','B','C','F','G']
linear=[n for n,t in out.items() if all(t[k] for k in core+['D'])]
quot=[n for n,t in out.items() if all(t[k] for k in core+['E'])]
all_but_clone=[n for n,t in out.items() if all(t[k] for k in core)]

print('\nPREDECLARED D5 SUMMARY')
print('core axioms A,B,C,F,G survivors =',all_but_clone)
print('with CLONE_LINEARITY D survivors =',linear)
print('with CLONE_QUOTIENT E survivors =',quot)

if len(linear)==1 and len(quot)==1 and linear==quot:
    verdict='UNIQUE_MEASURE_SELECTED_ACROSS_CLONE_CONVENTIONS'
elif linear and quot and linear!=quot:
    verdict='MEASURE_UNDERDETERMINED_BY_CLONE_CONVENTION'
elif len(linear)>1 or len(quot)>1:
    verdict='MEASURE_UNDERDETERMINED_MULTIPLE_SURVIVORS'
else:
    verdict='AXIOM_SET_INCONSISTENT_OR_NO_CANDIDATE'
print('PREDECLARED D5 VERDICT =',verdict)

print('\nINTERPRETATION LOCK:')
print('- D5 is a logical sieve over declared candidates, not a proof of a physical observer measure.')
print('- If clone convention changes the winner, Canevas needs an independent principle deciding whether')
print('  physically distinct identical observer-moments multiply measure or are quotient-equivalent.')
print('- No birth-rank fact may be used to choose between D and E.')
print('- A later D5.1 may add independently motivated axioms only if preregistered before testing them.')
print('\nFINISHED D5 v1 — DO NOT RETUNE AFTER OUTPUT')
