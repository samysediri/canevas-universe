"""Canevas T3.9-v1b — synthetic validation of predictive-interface metric.

Purpose
-------
Validate the greedy interface estimator used in observer_support_landscape_v1.py
BEFORE interpreting or modifying the T3.9-v1 Monte Carlo result.

No cosmological/anthropic observations are used.

Predeclared tests
-----------------
A. DIRECT independent channels: true external boundary k in {0,1,2,4,8}.
   Y has 8 bits. For the first k output bits, Y_j = E_j; remaining bits copy S_j.
   Therefore H(Y|S) ~= k bits and each true E_j contributes ~1 independent bit.
   With TARGET_EXPLAINED=0.90, expected greedy complexity is ceil(0.9*k)
   (0,1,2,4,8 respectively).

B. NOISY DIRECT channels: same construction with 5% output flips.
   Expected ordering must remain nondecreasing with k; exact recovery may soften.

C. XOR SYNERGY adversary: one output bit is XOR of k external bits.
   For k>1 each variable alone can have zero predictive information, although the
   full set is sufficient. A one-variable-at-a-time greedy estimator is expected
   to fail here. This test quantifies a KNOWN LIMITATION, not a reason to retune.

Primary validity criterion
--------------------------
The v1 metric is BASICALLY VALID only if:
1) noiseless DIRECT recovered complexities equal [0,1,2,4,8], and
2) noisy DIRECT complexities are nondecreasing with k and Spearman rho>=0.9.

If either fails, T3.9-v1 predictive-interface results are NOT INTERPRETABLE.
If both pass but XOR fails, T3.9-v1 is usable only for predominantly additive /
individually informative interfaces, and v2 must preregister a synergy-aware
estimator before rerunning network ensembles.
"""

from __future__ import annotations
from collections import defaultdict
import math
import numpy as np

SEED = 731903
RNG = np.random.default_rng(SEED)
SAMPLES = 12000
SUB_BITS = 8
MAX_GREEDY_BOUNDARY = 8
TARGET_EXPLAINED = 0.90
KS = [0, 1, 2, 4, 8]
NOISE = 0.05


def encode_bits(arr):
    arr = np.asarray(arr, dtype=np.uint8)
    if arr.ndim == 1:
        arr = arr[:, None]
    weights = (1 << np.arange(arr.shape[1], dtype=np.uint64))
    return (arr.astype(np.uint64) * weights).sum(axis=1)


def entropy(labels):
    labels = np.asarray(labels)
    if len(labels) == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def conditional_entropy(y, x):
    y = np.asarray(y); x = np.asarray(x)
    groups = defaultdict(list)
    for xi, yi in zip(x.tolist(), y.tolist()):
        groups[xi].append(yi)
    n = len(y)
    return float(sum((len(v)/n)*entropy(v) for v in groups.values()))


def rankdata(a):
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind='mergesort')
    ranks = np.empty(len(a), dtype=float)
    i = 0
    while i < len(a):
        j = i
        while j+1 < len(a) and a[order[j+1]] == a[order[i]]:
            j += 1
        ranks[order[i:j+1]] = 0.5*(i+j)+1.0
        i = j+1
    return ranks


def spearman(x, y):
    x = rankdata(x); y = rankdata(y)
    if np.std(x) == 0 or np.std(y) == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0,1])


def greedy_interface(S, Y, E):
    """Same conceptual estimator as T3.9-v1, on synthetic arrays."""
    s0 = encode_bits(S)
    y1 = encode_bits(Y)
    baseline = conditional_entropy(y1, s0)
    if baseline < 1e-9 or E.shape[1] == 0:
        return 0, baseline, baseline, []

    remaining = list(range(E.shape[1]))
    chosen = []
    history = [(0, baseline)]
    current = baseline

    for _ in range(min(MAX_GREEDY_BOUNDARY, len(remaining))):
        best = None
        for c in remaining:
            cols = chosen + [c]
            b = encode_bits(E[:, cols])
            joint = s0.astype(np.uint64) + (b.astype(np.uint64) << SUB_BITS)
            h = conditional_entropy(y1, joint)
            if best is None or h < best[0]:
                best = (h, c)
        h, c = best
        if current - h < 1e-6:
            break
        chosen.append(c)
        remaining.remove(c)
        current = h
        history.append((len(chosen), current))

    best_h = current
    total_reduction = baseline - best_h
    if total_reduction <= 1e-9:
        return 0, baseline, best_h, chosen

    target_h = baseline - TARGET_EXPLAINED*total_reduction
    complexity = len(chosen)
    for nsel, h in history:
        if h <= target_h + 1e-12:
            complexity = nsel
            break
    return complexity, baseline, best_h, chosen


def direct_dataset(k, noise=0.0):
    S = RNG.integers(0, 2, size=(SAMPLES, SUB_BITS), dtype=np.uint8)
    E = RNG.integers(0, 2, size=(SAMPLES, max(k,1)), dtype=np.uint8)
    Y = S.copy()
    if k:
        Y[:, :k] = E[:, :k]
    if noise > 0:
        flips = RNG.random(Y.shape) < noise
        Y ^= flips.astype(np.uint8)
    return S, Y, E[:, :k]


def xor_dataset(k):
    S = RNG.integers(0, 2, size=(SAMPLES, SUB_BITS), dtype=np.uint8)
    E = RNG.integers(0, 2, size=(SAMPLES, max(k,1)), dtype=np.uint8)
    Y = S.copy()
    if k:
        Y[:, 0] = np.bitwise_xor.reduce(E[:, :k], axis=1)
    return S, Y, E[:, :k]


def nondecreasing(xs):
    return all(b >= a for a,b in zip(xs, xs[1:]))


def run():
    print('='*76)
    print(' CANEVAS T3.9-v1b — PREDICTIVE INTERFACE METRIC VALIDATION')
    print('='*76)
    print('seed =', SEED, ' samples/case =', SAMPLES)
    print('k values =', KS, ' target explained =', TARGET_EXPLAINED)

    direct = []
    noisy = []
    xor = []

    print('\nA) NOISELESS DIRECT CHANNELS')
    for k in KS:
        S,Y,E = direct_dataset(k, 0.0)
        c,h0,h1,ch = greedy_interface(S,Y,E)
        direct.append(c)
        print(f'k={k:>2d}  recovered={c}  Hbase={h0:.4f}  Hbest={h1:.4f}  chosen={ch}')

    print('\nB) 5% NOISY DIRECT CHANNELS')
    for k in KS:
        S,Y,E = direct_dataset(k, NOISE)
        c,h0,h1,ch = greedy_interface(S,Y,E)
        noisy.append(c)
        print(f'k={k:>2d}  recovered={c}  Hbase={h0:.4f}  Hbest={h1:.4f}  chosen={ch}')

    print('\nC) XOR SYNERGY ADVERSARY')
    for k in KS:
        S,Y,E = xor_dataset(k)
        c,h0,h1,ch = greedy_interface(S,Y,E)
        xor.append(c)
        print(f'k={k:>2d}  recovered={c}  Hbase={h0:.4f}  Hbest={h1:.4f}  chosen={ch}')

    expected = [0,1,2,4,8]
    direct_exact = (direct == expected)
    rho_noisy = spearman(KS, noisy)
    noisy_order = nondecreasing(noisy)
    basic_valid = bool(direct_exact and noisy_order and rho_noisy >= 0.9)

    print('\n' + '-'*76)
    print('PREDECLARED VALIDATION SUMMARY')
    print('-'*76)
    print('expected noiseless DIRECT =', expected)
    print('observed noiseless DIRECT =', direct)
    print('direct exact recovery      =', direct_exact)
    print('observed noisy DIRECT      =', noisy)
    print(f'noisy monotonic            = {noisy_order}')
    print(f'noisy Spearman(k,metric)   = {rho_noisy:+.4f}')
    print('XOR observed               =', xor)

    if not basic_valid:
        verdict = 'METRIC_INVALID_T39_V1_NOT_INTERPRETABLE'
    else:
        # XOR k>1 being missed demonstrates synergy blindness. Even if by finite-sample
        # accident some are detected, the estimator remains conceptually greedy.
        xor_synergy_failure = any(xor[i] < KS[i] for i in range(2, len(KS)))
        if xor_synergy_failure:
            verdict = 'BASIC_VALID_BUT_SYNERGY_BLIND'
        else:
            verdict = 'BASIC_VALID_SYNERGY_TEST_DID_NOT_EXPOSE_FAILURE'

    print('\nPREDECLARED T3.9-v1b VERDICT =', verdict)
    print('\nINTERPRETATION LOCK:')
    print('- Do not alter thresholds after seeing this result.')
    print('- If metric invalid: do not interpret T3.9-v1 predictive-interface rho.')
    print('- If basic-valid but synergy-blind: v2 needs a preregistered multivariate/synergy-aware metric.')
    print('- Structural-boundary result from v1 is a separate statistic and is not validated by this test.')
    print('\nFINISHED T3.9-v1b')


if __name__ == '__main__':
    run()
