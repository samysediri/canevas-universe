"""CANEVAS SELF-LOCATION D6.2 — MULTIPLICITY ONTOLOGY INDEPENDENCE TEST

PREDECLARED before observing output.
Blind to human birth year/rank, D2-D4 numerical outputs, and downstream
anthropic attractiveness.

Question
--------
Can ordinary event ontology distinguish two physically distinct but
isomorphic realizations WITHOUT assuming an observer-counting rule?

This deliberately avoids using COUNT/QUOTIENT as axioms. We instead test
whether generic event identity based on physical causal coordinates treats
an exact remote replica as the same event or a distinct event.

Declared ontology
-----------------
An event token has:
  state: intrinsic informational/physical state
  past:  causal-parent token IDs
  region: physical causal region ID
A representation label is explicitly nonphysical metadata.

Core principles
---------------
A LABEL_INVARIANCE: changing only a representation label changes nothing.
B TOKEN_REFLEXIVITY: an event token is identical to itself.
C REGION_SEPARATION: events in causally distinct physical regions are not the
   same event token even if intrinsic state and local causal pattern match.
D CAUSAL_SEPARATION: different causal-parent token sets imply distinct event
   tokens even if intrinsic state matches.
E ISOMORPHISM_NOT_IDENTITY: structural isomorphism may establish same TYPE,
   but does not by itself establish same TOKEN.

Important lock
--------------
Even if D6.2 derives TOKEN multiplicity, it does NOT automatically derive
probability measure proportional to token count. That bridge is a separate
claim to be tested later. Thus D6.2 cannot by itself rescue D6/D6.1 COUNT as
an observer measure.
"""
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Event:
    token: str
    state: str
    past: tuple
    region: str
    label: str = ''

E0 = Event('e0','S',('a0','b0'),'R0','display-A')
RELABEL = replace(E0,label='display-Z')
REMOTE_ISOMORPH = Event('e1','S',('a1','b1'),'R1','display-A')
SAME_REGION_NEW_PAST = Event('e2','S',('c0','d0'),'R0','display-A')
SAME_TYPE_OTHER_TOKEN = Event('e3','S',('a0','b0'),'R0','display-A')


def physical_signature(e):
    return (e.state,e.past,e.region)

def same_token_physical(a,b):
    # token identity is grounded in physical event signature; display label ignored
    return physical_signature(a)==physical_signature(b)

def same_type(a,b):
    # deliberately weak structural type: intrinsic state only
    return a.state==b.state


def main():
    print('='*82)
    print('CANEVAS SELF-LOCATION D6.2 — MULTIPLICITY ONTOLOGY INDEPENDENCE TEST')
    print('='*82)
    print('Blind to human self-location and downstream anthropic consequences.')
    print()

    A = same_token_physical(E0,RELABEL)
    B = same_token_physical(E0,E0)
    C = not same_token_physical(E0,REMOTE_ISOMORPH)
    D = not same_token_physical(E0,SAME_REGION_NEW_PAST)
    E = same_type(E0,REMOTE_ISOMORPH) and not same_token_physical(E0,REMOTE_ISOMORPH)

    print(f'A LABEL_INVARIANCE      = {A}')
    print(f'B TOKEN_REFLEXIVITY      = {B}')
    print(f'C REGION_SEPARATION      = {C}')
    print(f'D CAUSAL_SEPARATION      = {D}')
    print(f'E ISOMORPHISM_NOT_IDENTITY = {E}')
    print()
    print('DIAGNOSTIC CASES')
    print('same intrinsic type, remote region:')
    print('  same_type =',same_type(E0,REMOTE_ISOMORPH))
    print('  same_token =',same_token_physical(E0,REMOTE_ISOMORPH))
    print('same physical signature, different arbitrary token name:')
    print('  same_token =',same_token_physical(E0,SAME_TYPE_OTHER_TOKEN))

    core=all([A,B,C,D,E])
    print('\nPREDECLARED D6.2 SUMMARY')
    print('core ontology principles A-E pass =',core)
    if core:
        verdict='DISTINCT_PHYSICAL_ISOMORPHS_ARE_DISTINCT_EVENT_TOKENS'
    else:
        verdict='EVENT_MULTIPLICITY_NOT_DERIVED'
    print('PREDECLARED D6.2 VERDICT =',verdict)

    # Bridge is intentionally not inferred by the program.
    print('PREDECLARED MEASURE BRIDGE VERDICT = NOT_DERIVED')
    print('\nINTERPRETATION LOCK:')
    print('- A remote exact replica can be a distinct physical EVENT TOKEN while remaining the same TYPE.')
    print('- This is an ontology-of-events result only; it is not an observer-measure theorem.')
    print('- Distinct token existence does NOT imply equal probability weight or linear additivity.')
    print('- Therefore D6.2 cannot be cited as proving COUNT_SUPPORT in D5.')
    print('- A later bridge test must independently ask whether measure is additive over distinct event tokens.')
    print('- No self-location fact may be used to choose that bridge.')
    print('\nFINISHED D6.2 v1 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    main()
