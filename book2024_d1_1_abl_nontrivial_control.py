"""BOOK2024-D1.1 — NONTRIVIAL ABL CONTROL v1

Correction after D1 control failure. D1 remains frozen and is not retuned.

Purpose:
Validate that future post-selection can alter an intermediate conditional
probability in standard quantum mechanics, while averaging over unrecorded
future outcomes recovers the ordinary Born distribution.

This is NOT evidence for retrocausation and NOT a Canevas-specific prediction.

PREDECLARED GEOMETRY
--------------------
Initial state: |+x>.
Intermediate projective measurement: sigma_z with outcomes |0>, |1>.
Future projective measurement/postselection: sigma_z.

Analytic expectation:
- Ordinary intermediate Born distribution from |+x>: [1/2, 1/2].
- Conditional on future |0>, ABL gives [1, 0].
- Conditional on future |1>, ABL gives [0, 1].
- Future outcomes themselves occur with probabilities [1/2, 1/2].
- Averaging the conditional intermediate distributions over unrecorded future
  outcomes returns [1/2, 1/2].

The deterministic conditional result is intentionally chosen analytically
before execution to validate the ABL implementation with a nontrivial control.
"""

import numpy as np

TOL=1e-12

# basis states
z0=np.array([1.0,0.0],dtype=complex)
z1=np.array([0.0,1.0],dtype=complex)
plusx=(z0+z1)/np.sqrt(2.0)

Pz=[np.outer(z0,z0.conj()),np.outer(z1,z1.conj())]
future=[z0,z1]


def born_probs(state, projectors):
    return np.array([float(np.real(state.conj() @ P @ state)) for P in projectors])


def abl_probs(initial, final, projectors):
    w=[]
    for P in projectors:
        amp=final.conj() @ P @ initial
        w.append(float(abs(amp)**2))
    w=np.array(w)
    return w/w.sum()


def future_prob_with_intermediate_unrecorded(initial, final, projectors):
    # Sequential experiment: projective z measurement occurs but its result is
    # not recorded, then future z measurement.
    return sum(abs(final.conj() @ P @ initial)**2 for P in projectors)


def main():
    print('='*78)
    print('BOOK2024-D1.1 — NONTRIVIAL ABL CONTROL v1')
    print('='*78)
    print('D1 remains a frozen historical control failure; this is a new labelled correction.\n')

    ordinary=born_probs(plusx,Pz)
    cond=[]; pf=[]
    for f in future:
        cond.append(abl_probs(plusx,f,Pz))
        pf.append(future_prob_with_intermediate_unrecorded(plusx,f,Pz))
    cond=np.array(cond); pf=np.array(pf); pf=pf/pf.sum()
    averaged=np.sum(pf[:,None]*cond,axis=0)

    print('ordinary Born intermediate distribution =',ordinary)
    print('ABL conditioned on future z=0 =',cond[0])
    print('ABL conditioned on future z=1 =',cond[1])
    print('future-result probabilities =',pf)
    print('ABL averaged over unrecorded future result =',averaged)

    normalized=np.allclose(cond.sum(axis=1),1.0,atol=TOL)
    future_changes=(not np.allclose(cond[0],ordinary,atol=TOL)) and (not np.allclose(cond[1],ordinary,atol=TOL))
    deterministic=np.allclose(cond[0],[1,0],atol=TOL) and np.allclose(cond[1],[0,1],atol=TOL)
    recovers=np.allclose(averaged,ordinary,atol=TOL)

    print('\nPREDECLARED BOOK2024-D1.1 SUMMARY')
    print('ABL normalized =',normalized)
    print('future postselection changes intermediate conditional distribution =',future_changes)
    print('analytic deterministic control recovered =',deterministic)
    print('ignoring future result recovers ordinary Born distribution =',recovers)

    if normalized and future_changes and deterministic and recovers:
        verdict='STANDARD_QM_TIME_SYMMETRIC_CONDITIONING_CONTROL_VALIDATED'
    else:
        verdict='CONTROL_FAILURE_DO_NOT_INTERPRET'
    print('PREDECLARED BOOK2024-D1.1 VERDICT =',verdict)

    print('\nINTERPRETATION LOCK:')
    print('- A positive result validates a standard conditional-probability calculation only.')
    print('- It does NOT show that a future choice dynamically changes an already-recorded past event.')
    print('- It does NOT permit signalling to the past.')
    print('- The recovery of Born statistics when future outcomes are ignored is essential.')
    print('- Therefore agreement supports mathematical compatibility with the book\'s temporal intuition, not empirical uniqueness.')
    print('- A Canevas-specific test would require a preregistered deviation from standard quantum mechanics before data are inspected.')
    print('\nFINISHED BOOK2024-D1.1 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    main()
