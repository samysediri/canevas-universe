"""BOOK2024-D1 — ABL TIME-SYMMETRIC CONDITIONING v1

Book anchor: the 2024 manuscript explicitly proposes that the future may influence
present probabilities and that time may be non-linear/interconnected.

Scientific anchor: Aharonov-Bergmann-Lebowitz (1964) time-symmetric quantum
conditioning for pre- and post-selected ensembles.

Purpose
-------
Reproduce, on a qubit, the precise mathematical fact that an intermediate
measurement probability can depend on BOTH an earlier preparation and a later
post-selection, while averaging over all future outcomes recovers the ordinary
Born-rule probability.

This is NOT a proof of physical retrocausation, consciousness-caused collapse,
or Canevas cosmology. It is a formal compatibility/translation test only.

PREDECLARED CASE
----------------
Initial state |psi_i> = |+x>.
Intermediate measurement = sigma_z with outcomes |0>, |1>.
Future postselection is measured in the x basis: |+x> or |-x>.

ABL rule:
P(z=k | psi_i, psi_f) = |<psi_f|P_k|psi_i>|^2 /
                        sum_j |<psi_f|P_j|psi_i>|^2

Controls:
1) ABL probabilities normalize to 1 for each allowed postselection.
2) Different future postselections may alter intermediate conditional probabilities.
3) If the future result is NOT selected/known, summing over it with its actual
   probability must recover the ordinary Born-rule distribution for the
   intermediate z measurement.
4) No postselection may be interpreted as sending usable information backward.
"""

import numpy as np

EPS = 1e-12

ket0 = np.array([1.0, 0.0], dtype=complex)
ket1 = np.array([0.0, 1.0], dtype=complex)
ket_px = (ket0 + ket1) / np.sqrt(2.0)
ket_mx = (ket0 - ket1) / np.sqrt(2.0)

P0 = np.outer(ket0, ket0.conj())
P1 = np.outer(ket1, ket1.conj())
PROJECTORS = [P0, P1]
POSTS = {"PLUS_X": ket_px, "MINUS_X": ket_mx}


def born_intermediate(psi):
    return np.array([float(np.real(np.vdot(psi, P @ psi))) for P in PROJECTORS])


def abl(psi_i, psi_f):
    weights=[]
    for P in PROJECTORS:
        amp = np.vdot(psi_f, P @ psi_i)
        weights.append(abs(amp)**2)
    weights=np.array(weights, dtype=float)
    return weights/weights.sum()


def joint_mid_future(psi_i, psi_f, P):
    # Sequential ideal measurement joint probability:
    # p(z=k then f) = |<f|P_k|i>|^2
    return abs(np.vdot(psi_f, P @ psi_i))**2


def main():
    print("="*80)
    print("BOOK2024-D1 — ABL TIME-SYMMETRIC CONDITIONING v1")
    print("="*80)
    print("Initial |+x>, intermediate sigma_z, future x-basis postselection.\n")

    born = born_intermediate(ket_px)
    print("Ordinary Born intermediate distribution:", born)

    abl_results={}
    norm_ok=True
    for name, pf in POSTS.items():
        probs=abl(ket_px,pf)
        abl_results[name]=probs
        norm_ok &= abs(probs.sum()-1.0)<EPS
        print(f"ABL conditioned on future {name}: P(z=0)={probs[0]:.12f} P(z=1)={probs[1]:.12f}")

    different_future = not np.allclose(abl_results["PLUS_X"], abl_results["MINUS_X"], atol=EPS)

    # Compute p(f) in the experiment where z is actually measured and outcome ignored.
    future_weights={}
    for name,pf in POSTS.items():
        future_weights[name]=sum(joint_mid_future(ket_px,pf,P) for P in PROJECTORS)
    total_f=sum(future_weights.values())
    future_weights={k:v/total_f for k,v in future_weights.items()}

    averaged = np.zeros(2)
    for name in POSTS:
        averaged += future_weights[name]*abl_results[name]
    recover_born=np.allclose(averaged,born,atol=EPS)

    print("\nFuture-result probabilities after unrecorded z result:", future_weights)
    print("ABL averaged over future results:", averaged)
    print("recovers Born rule =", recover_born)

    print("\nPREDECLARED BOOK2024-D1 SUMMARY")
    print("ABL normalized =", norm_ok)
    print("future postselection changes intermediate conditional distribution =", different_future)
    print("ignoring future result recovers ordinary Born distribution =", recover_born)

    if norm_ok and different_future and recover_born:
        verdict="FUTURE_BOUNDARY_CAN_ENTER_CONDITIONAL_DESCRIPTION_WITHOUT_BACKWARD_SIGNAL"
    else:
        verdict="CONTROL_FAILURE_DO_NOT_INTERPRET"
    print("PREDECLARED BOOK2024-D1 VERDICT =", verdict)

    print("\nINTERPRETATION LOCK:")
    print("- A positive result reproduces standard time-symmetric quantum conditioning.")
    print("- It does NOT prove that a future event dynamically causes an earlier event.")
    print("- It does NOT show consciousness changes quantum outcomes.")
    print("- The future condition changes a conditional ensemble; without postselection, ordinary Born statistics return.")
    print("- Therefore D1 supports mathematical compatibility with the book's temporal intuition, not empirical uniqueness.")
    print("- A genuinely new Canevas prediction would require a deviation from standard quantum mechanics fixed before data.")
    print("\nFINISHED BOOK2024-D1 — DO NOT RETUNE AFTER OUTPUT")

if __name__ == "__main__":
    main()
