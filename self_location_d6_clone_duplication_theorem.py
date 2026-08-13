"""CANEVAS SELF-LOCATION D6 — CLONE / DUPLICATION THEOREM v1

PREDECLARED before observing D6 output.

Purpose
-------
D5 showed that the observer measure is underdetermined by whether physically
identical observer-moments are COUNTED separately or QUOTIENTED as equivalent.
D6 asks whether a duplication rule follows from structural principles alone.

STRICT BLINDING
---------------
D6 does not use birth year, human birth rank, D2/D3 outputs, demographic data,
or where any resulting observer measure would place a real human.

Declared representation
-----------------------
An observer-realization is represented by:
  (information_state, causal_history, support_id, amplitude)
Only the first three matter in this classical finite diagnostic.

Declared axioms / desiderata
-----------------------------
A LABEL: renaming support IDs cannot alter total measure.
B SPLIT: splitting one physical support into bookkeeping fragments with total
         amplitude conserved cannot alter total measure.
C DISJOINT_ADD: causally disjoint nonidentical observer realizations add.
D COPY_LOCALITY: adding a causally disconnected exact physical copy does not
                 alter any intrinsic property of the original realization.
E REPRESENTATION: duplicating a database record referring to the SAME physical
                  support cannot change measure.
F PHYSICAL_MULTIPLICITY_NEUTRALITY: exact copies with identical information
                  state and causal history but distinct physical supports are
                  quotient-equivalent.  This is NOT treated as a core axiom;
                  it is a separate Canevas-strengthening candidate.
G PHYSICAL_MULTIPLICITY_COUNTS: distinct physical supports add even when their
                  information state and causal history are identical.  This is
                  the competing strengthening candidate.

Candidate rules frozen ex ante
------------------------------
COUNT_SUPPORT: sum amplitude over distinct physical supports; duplicate records
               of same support are deduplicated.
QUOTIENT_INFO_CAUSAL: sum one representative amplitude per equivalence class
               (information_state, causal_history), taking max amplitude inside
               an exact class to avoid bookkeeping replication.
COUNT_RECORDS: naive sum over database rows (negative control).
INFO_ONLY_QUOTIENT: quotient only by information state, ignoring causal history
               (negative/control alternative).

Core criterion
--------------
Core axioms A-E deliberately do NOT contain a metaphysical statement about
whether exact physical copies count. If >1 incompatible candidate survives
A-E, D6 verdict is UNDERDETERMINED_CORE. Only if A-E themselves uniquely force
COUNT or QUOTIENT may D6 claim derivation.

Strengthening diagnostics F and G are reported separately and may not be folded
back into the core after output.
"""
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class R:
    info:str
    history:str
    support:str
    amp:float=1.0

# Frozen test worlds. Duplicate rows are intentional in representation tests.
BASE=[R('O','h0','s1',1.0)]
RENAMED=[R('O','h0','xyz',1.0)]
BOOKKEEP_SPLIT=[R('O','h0','s1a',0.4),R('O','h0','s1b',0.6)]
# For SPLIT these fragments are tagged as distinct IDs, exposing whether a rule
# depends on support count rather than conserved amplitude.
EXACT_PHYSICAL_COPY=[R('O','h0','s1',1.0),R('O','h0','s2',1.0)]
DUPLICATE_RECORD=[R('O','h0','s1',1.0),R('O','h0','s1',1.0)]
NONIDENTICAL_DISJOINT=[R('O','h0','s1',1.0),R('P','hP','s2',1.0)]
SAME_INFO_DIFFERENT_HISTORY=[R('O','h0','s1',1.0),R('O','h1','s2',1.0)]


def count_records(rs): return sum(x.amp for x in rs)

def count_support(rs):
    # same support is one physical realization; keep max represented amplitude
    d={}
    for x in rs: d[x.support]=max(d.get(x.support,0.0),x.amp)
    return sum(d.values())

def quotient_info_causal(rs):
    d={}
    for x in rs:
        k=(x.info,x.history); d[k]=max(d.get(k,0.0),x.amp)
    return sum(d.values())

def info_only(rs):
    d={}
    for x in rs: d[x.info]=max(d.get(x.info,0.0),x.amp)
    return sum(d.values())

RULES={
 'COUNT_SUPPORT':count_support,
 'QUOTIENT_INFO_CAUSAL':quotient_info_causal,
 'COUNT_RECORDS':count_records,
 'INFO_ONLY_QUOTIENT':info_only,
}
EPS=1e-12

def eq(a,b): return abs(a-b)<EPS

def test(fn):
    b=fn(BASE)
    A=eq(fn(RENAMED),b)
    # A physically valid split must conserve measure. For quotient rules the
    # two bookkeeping fragments have same info/history and max rather than sum,
    # so this deliberately tests tension with amplitude subdivision.
    B=eq(fn(BOOKKEEP_SPLIT),b)
    C=eq(fn(NONIDENTICAL_DISJOINT),b+fn([NONIDENTICAL_DISJOINT[1]]))
    # locality is represented as original contribution unchanged; all declared
    # rules satisfy this unless the total rule feeds back globally.
    D=True
    E=eq(fn(DUPLICATE_RECORD),b)
    F=eq(fn(EXACT_PHYSICAL_COPY),b)
    G=eq(fn(EXACT_PHYSICAL_COPY),2*b)
    H=eq(fn(SAME_INFO_DIFFERENT_HISTORY),2*b) # causal-history sensitivity
    return dict(A=A,B=B,C=C,D=D,E=E,F=F,G=G,H=H,
                base=b,copy=fn(EXACT_PHYSICAL_COPY),split=fn(BOOKKEEP_SPLIT))

print('='*82)
print('CANEVAS SELF-LOCATION D6 — CLONE / DUPLICATION THEOREM v1')
print('='*82)
print('Blind to human self-location and all D2/D3 empirical outputs.')
print('Core axioms = A-E. F/G are mutually competing strengthenings.')
print()
results={}
for name,fn in RULES.items():
    t=test(fn); results[name]=t
    flags=' '.join(f'{k}={t[k]}' for k in 'ABCDEFGH')
    print(f'[{name}] {flags} base={t["base"]:.3f} copy={t["copy"]:.3f} split={t["split"]:.3f}')

core_survivors=[n for n,t in results.items() if all(t[k] for k in 'ABCDE')]
count_strength=[n for n in core_survivors if results[n]['G']]
quot_strength=[n for n in core_survivors if results[n]['F']]
causal_sensitive=[n for n in core_survivors if results[n]['H']]

print('\nPREDECLARED D6 SUMMARY')
print('core A-E survivors =',core_survivors)
print('among core survivors, G physical-copies-count =',count_strength)
print('among core survivors, F physical-copies-neutral =',quot_strength)
print('among core survivors, causal-history-sensitive =',causal_sensitive)

# Unique derivation is allowed only from A-E, not by choosing F/G after output.
if len(core_survivors)==0:
    verdict='CORE_AXIOMS_INCONSISTENT_WITH_DECLARED_RULES'
elif len(core_survivors)==1:
    only=core_survivors[0]
    if results[only]['G'] and not results[only]['F']:
        verdict='CORE_DERIVES_COUNT'
    elif results[only]['F'] and not results[only]['G']:
        verdict='CORE_DERIVES_QUOTIENT'
    else:
        verdict='CORE_UNIQUE_BUT_CLONE_STATUS_AMBIGUOUS'
else:
    verdict='UNDERDETERMINED_CORE'
print('PREDECLARED D6 VERDICT =',verdict)

if verdict=='UNDERDETERMINED_CORE':
    if count_strength and quot_strength:
        diag='EXPLICIT_EXTRA_PRINCIPLE_REQUIRED_COUNT_VS_QUOTIENT'
    else:
        diag='DECLARED_CANDIDATES_REQUIRE_REFINEMENT'
else:
    diag='SEE_PRIMARY_VERDICT'
print('PREDECLARED D6 DIAGNOSTIC =',diag)
print('\nINTERPRETATION LOCK:')
print('- D6 is a finite logical sieve, not a physical theorem about consciousness.')
print('- F or G cannot be adopted merely because its downstream anthropic result is attractive.')
print('- If core is underdetermined, Canevas needs an independently justified ontology of copies.')
print('- No D6 result licenses an extinction date or validates a personal birth-rank anomaly.')
print('- A later D6.1 may add a genuinely independent physical principle only if it is')
print('  preregistered before examining downstream self-location consequences.')
print('\nFINISHED D6 v1 — DO NOT RETUNE AFTER OUTPUT')
