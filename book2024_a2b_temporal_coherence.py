"""BOOK2024-A2b — TEMPORAL COHERENCE FROM DYNAMICS v1

Book-anchored motivation:
A1 formalized eventual realization. A2 showed that infinite realization alone does
not determine typicality. A2b asks a narrower mathematical question relevant to
the 2024 book: can ordinary temporal persistence make long coherent histories
far more probable than the same histories under independent instantaneous draws?

This is NOT a consciousness model, Boltzmann-brain calculation, or cosmological
prediction. It is a bridge diagnostic only.

PREDECLARED DESIGN
------------------
Binary state X_t. All models have stationary marginal P(X_t=0)=P(X_t=1)=1/2.
IID model: consecutive states independent.
Persistent Markov model: P(X_t=X_{t-1}) = s.
s values fixed before output: [0.50, 0.60, 0.75, 0.90, 0.99].
Lengths fixed before output: [8, 16, 32, 64, 128].
A history is COHERENT iff number of transitions <= floor(0.20*(L-1)).

Exact probability is computed from a Binomial distribution for transition count:
under persistence s, each transition indicator has probability q=1-s.
P(coherent|s,L)=sum_{k=0}^{K} C(L-1,k) q^k (1-q)^(L-1-k).

Primary diagnostic: likelihood ratio versus IID (s=0.5).
No empirical values, observer rank, birth date, cosmological parameters, or
post-output tuning are allowed under A2b.
"""

import math

S_VALUES = [0.50, 0.60, 0.75, 0.90, 0.99]
LENGTHS = [8, 16, 32, 64, 128]
COHERENCE_FRACTION = 0.20


def binom_cdf(kmax, n, q):
    return sum(math.comb(n, k) * (q ** k) * ((1.0-q) ** (n-k)) for k in range(kmax+1))


def p_coherent(s, L):
    n = L - 1
    kmax = math.floor(COHERENCE_FRACTION * n)
    q = 1.0 - s
    return binom_cdf(kmax, n, q), kmax


def main():
    print('='*78)
    print('BOOK2024-A2b — TEMPORAL COHERENCE FROM DYNAMICS v1')
    print('='*78)
    print('Same instantaneous state marginals; only temporal dependence changes.')
    print('No empirical target values are used.\n')

    baseline = {}
    for L in LENGTHS:
        baseline[L], _ = p_coherent(0.50, L)

    monotonic_all = True
    exponential_signature = True

    for s in S_VALUES:
        print(f'[PERSISTENCE s={s:.2f}]')
        previous = None
        log10_lrs = []
        for L in LENGTHS:
            p, kmax = p_coherent(s, L)
            p0 = baseline[L]
            lr = p / p0 if p0 > 0 else math.inf
            loglr = math.log10(lr) if lr > 0 and math.isfinite(lr) else math.inf
            log10_lrs.append(loglr)
            print(f'L={L:3d} Kmax={kmax:2d} Pcoh={p:.12g} Pcoh_IID={p0:.12g} LR={lr:.12g} log10LR={loglr:.6f}')
            if previous is not None and s > 0.50 and lr < previous:
                monotonic_all = False
            previous = lr
        if s >= 0.75 and log10_lrs[-1] <= log10_lrs[1]:
            exponential_signature = False
        print()

    # Analytic large-deviation direction: for q<0.2, coherent set contains the
    # typical transition fraction; for IID q=0.5 it is a lower-tail deviation.
    strong_persistence_expected = all((1-s) < COHERENCE_FRACTION for s in [0.90,0.99])

    print('PREDECLARED BOOK2024-A2b SUMMARY')
    print('LR nondecreasing with L for every s>0.5 =', monotonic_all)
    print('strong-persistence large-L amplification present =', exponential_signature)
    print('q<coherence threshold for s=0.90,0.99 =', strong_persistence_expected)

    if monotonic_all and exponential_signature and strong_persistence_expected:
        verdict = 'LOCAL_PERSISTENCE_CAN_EXPONENTIALLY_FAVOR_COHERENT_HISTORIES'
    else:
        verdict = 'BRIDGE_CONTROL_FAILURE_OR_WEAK_EFFECT'
    print('PREDECLARED BOOK2024-A2b VERDICT =', verdict)

    print('\nINTERPRETATION LOCK:')
    print('- A positive result is a mathematical mechanism, not evidence for Canevas cosmology.')
    print('- It does not identify coherent histories with consciousness or observers.')
    print('- It does not solve the cosmological measure problem or compute physical fluctuation rates.')
    print('- It shows only whether temporal law can strongly alter history-level typicality while instantaneous marginals stay identical.')
    print('- A2c must independently motivate a physical dynamics and compare physically meaningful structured-history and fluctuation rates.')
    print('- Do not change s values, lengths, or the 20% coherence threshold after output under A2b.')
    print('\nFINISHED BOOK2024-A2b — DO NOT RETUNE AFTER OUTPUT')

if __name__ == '__main__':
    main()
