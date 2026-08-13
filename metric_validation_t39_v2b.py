"""Canevas T3.9-v2b — held-out predictive-interface validation.

Goal
----
Validate a narrower claim than T3.9-v2:
a rich environment can still have LOW EFFECTIVE predictive complexity if its
influence on a subsystem is compressible through a small latent summary.

This is a synthetic calibration test. No observed physics is used.
"""

from __future__ import annotations
import math
import numpy as np
from collections import defaultdict

SEED = 84217
RNG = np.random.default_rng(SEED)
N_SAMPLES = 20000
TRAIN_FRAC = 0.5
MAX_SELECTED = 8
MIN_TEST_GAIN = 0.01


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
    total = len(y)
    return float(sum((len(v)/total) * entropy(v) for v in groups.values()))


def joint_label(a, b, a_bits):
    return a.astype(np.uint64) + (b.astype(np.uint64) << a_bits)


def select_greedy_train(S0, S1, E, train_idx):
    s0 = encode_bits(S0[train_idx])
    s1 = encode_bits(S1[train_idx])
    baseline = conditional_entropy(s1, s0)
    chosen, remaining = [], list(range(E.shape[1]))
    current = baseline
    for _ in range(min(MAX_SELECTED, len(remaining))):
        best = None
        for c in remaining:
            cols = chosen + [c]
            b = encode_bits(E[train_idx][:, cols])
            h = conditional_entropy(s1, joint_label(s0, b, S0.shape[1]))
            if best is None or h < best[0]:
                best = (h, c)
        if best is None or current - best[0] < 1e-6:
            break
        current, c = best
        chosen.append(c); remaining.remove(c)
    return chosen


def heldout_curve(S0, S1, E, chosen, test_idx):
    s0 = encode_bits(S0[test_idx]); s1 = encode_bits(S1[test_idx])
    base = conditional_entropy(s1, s0)
    gains = []
    prev_h = base
    cumulative = 0.0
    for k in range(1, len(chosen)+1):
        b = encode_bits(E[test_idx][:, chosen[:k]])
        h = conditional_entropy(s1, joint_label(s0, b, S0.shape[1]))
        marginal = max(0.0, prev_h - h)
        cumulative = max(0.0, base - h)
        gains.append((k, h, marginal, cumulative))
        prev_h = h
    return base, gains


def summarize_case(name, S0, S1, E, expected):
    idx = np.arange(len(S0)); RNG.shuffle(idx)
    cut = int(TRAIN_FRAC * len(idx))
    tr, te = idx[:cut], idx[cut:]
    chosen = select_greedy_train(S0, S1, E, tr)
    base, curve = heldout_curve(S0, S1, E, chosen, te)

    # Effective complexity = smallest k with >=90% of maximum held-out gain.
    total_gain = curve[-1][3] if curve else 0.0
    eff = 0
    if total_gain >= MIN_TEST_GAIN:
        target = 0.90 * total_gain
        eff = next((k for k, h, mg, cg in curve if cg >= target), len(curve))

    print(f'\n{name}')
    print(f' expected_class = {expected}')
    print(f' structural_inputs = {E.shape[1]}')
    print(f' selected_train = {chosen}')
    print(f' heldout_baseline_H = {base:.4f}')
    print(f' heldout_total_gain = {total_gain:.4f}')
    print(f' effective_complexity_90 = {eff}')
    if curve:
        print(' heldout_curve:')
        for k, h, mg, cg in curve:
            print(f'   k={k:2d} H={h:.4f} marginal_gain={mg:.4f} cumulative_gain={cg:.4f}')
    return {'name':name,'expected':expected,'structural':E.shape[1], 'eff':eff, 'gain':total_gain}


def make_cases(n=N_SAMPLES):
    # Internal present state: 2 bits. It contributes weakly so environment matters.
    S0 = RNG.integers(0,2,size=(n,2),dtype=np.uint8)

    # Case 1: LOW_SIMPLE — one external bit causally matters.
    E1 = RNG.integers(0,2,size=(n,8),dtype=np.uint8)
    y1 = S0[:,0] ^ E1[:,0]
    S1_1 = np.column_stack([y1, S0[:,1]]).astype(np.uint8)

    # Case 2: RICH_COMPRESSIBLE — 8 observed environmental channels are noisy
    # copies of ONE latent bit Z. The subsystem depends on Z. Structurally rich,
    # but effective predictive dimension should be near 1.
    Z = RNG.integers(0,2,size=n,dtype=np.uint8)
    E2 = np.empty((n,8),dtype=np.uint8)
    for j in range(8):
        noise = (RNG.random(n) < 0.08).astype(np.uint8)
        E2[:,j] = Z ^ noise
    y2 = S0[:,0] ^ Z
    S1_2 = np.column_stack([y2, S0[:,1]]).astype(np.uint8)

    # Case 3: RICH_IRREDUCIBLE — target is 4 bits carrying four independent
    # environmental influences. To predict all of S1 well, several independent
    # external variables are genuinely required.
    E3 = RNG.integers(0,2,size=(n,8),dtype=np.uint8)
    S0_3 = RNG.integers(0,2,size=(n,4),dtype=np.uint8)
    S1_3 = np.column_stack([
        S0_3[:,0] ^ E3[:,0],
        S0_3[:,1] ^ E3[:,1],
        S0_3[:,2] ^ E3[:,2],
        S0_3[:,3] ^ E3[:,3],
    ]).astype(np.uint8)

    # Case 4: RICH_NOISE — many external inputs exist but none predicts S1.
    E4 = RNG.integers(0,2,size=(n,8),dtype=np.uint8)
    random_future = RNG.integers(0,2,size=n,dtype=np.uint8)
    S1_4 = np.column_stack([S0[:,0] ^ random_future, S0[:,1]]).astype(np.uint8)

    return [
        ('LOW_SIMPLE', S0, S1_1, E1, 'LOW_EFFECTIVE_COMPLEXITY'),
        ('RICH_COMPRESSIBLE', S0, S1_2, E2, 'LOW_EFFECTIVE_COMPLEXITY_DESPITE_8_CHANNELS'),
        ('RICH_IRREDUCIBLE', S0_3, S1_3, E3, 'HIGHER_EFFECTIVE_COMPLEXITY'),
        ('RICH_NOISE', S0, S1_4, E4, 'ZERO_PREDICTIVE_GAIN'),
    ]


def run():
    print('='*78)
    print(' CANEVAS T3.9-v2b — HELD-OUT COMPRESSIBILITY VALIDATION')
    print('='*78)
    print('seed =', SEED, 'samples/case =', N_SAMPLES)
    print('train fraction =', TRAIN_FRAC, 'max selected =', MAX_SELECTED)
    print('No post-hoc thresholds may be changed after this run.\n')

    results=[]
    for case in make_cases():
        results.append(summarize_case(*case))

    r={x['name']:x for x in results}

    c1 = r['LOW_SIMPLE']['eff'] <= 2 and r['LOW_SIMPLE']['gain'] >= MIN_TEST_GAIN
    c2 = r['RICH_COMPRESSIBLE']['eff'] <= 2 and r['RICH_COMPRESSIBLE']['gain'] >= MIN_TEST_GAIN
    c3 = r['RICH_IRREDUCIBLE']['eff'] >= 3 and r['RICH_IRREDUCIBLE']['gain'] >= MIN_TEST_GAIN
    c4 = r['RICH_NOISE']['gain'] < MIN_TEST_GAIN

    print('\n'+'-'*78)
    print('PREDECLARED VALIDATION SUMMARY')
    print('-'*78)
    print('LOW_SIMPLE low complexity:', c1)
    print('RICH_COMPRESSIBLE low effective complexity despite 8 channels:', c2)
    print('RICH_IRREDUCIBLE requires >=3 effective variables:', c3)
    print('RICH_NOISE gives negligible held-out gain:', c4)

    if c1 and c2 and c3 and c4:
        verdict='HELDOUT_COMPRESSIBILITY_METRIC_BASICALLY_VALID'
    elif c1 and c4 and not c2:
        verdict='FAILS_COMPRESSIBLE_LATENT_TEST'
    elif not c3:
        verdict='FAILS_IRREDUCIBLE_DIMENSION_TEST'
    else:
        verdict='METRIC_NOT_VALIDATED'

    print('\nPREDECLARED T3.9-v2b VERDICT =', verdict)
    print('\nINTERPRETATION LOCK:')
    print('- Passing validates only these synthetic distinctions, not observer theory.')
    print('- Failure means T3.9-v2 predictive correlations remain uninterpretable.')
    print('- Do not tune noise, thresholds, sample size, or case definitions after seeing this run.')
    print('- Even a pass would require a separately preregistered network replication.')
    print('\nFINISHED T3.9-v2b')

if __name__=='__main__':
    run()
