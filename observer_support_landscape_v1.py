"""Canevas T3.9 — Observer-support landscape v1.

Question
--------
Across broad Boolean-network ensembles, do persistent/memory-bearing/robust
subsystems disproportionately have compact predictive interfaces?

This is NOT a consciousness model. It tests a narrower prerequisite:
individual-like information-processing persistence vs boundary compressibility.

Predeclared primary statistic:
Spearman correlation between SUPPORT_SCORE and INTERFACE_COMPLEXITY across all
candidate subsystems. Negative = stronger support tends to require a smaller
predictive boundary.

No observed physical constants are used.
"""

from __future__ import annotations
import math, random, statistics
from collections import Counter, defaultdict
import numpy as np

SEED = 39017
RNG = np.random.default_rng(SEED)
random.seed(SEED)

N = 24
SUBSYSTEM_SIZE = 4
NETWORKS_PER_FAMILY = 18
SUBSYSTEMS_PER_NETWORK = 6
BURN_IN = 80
STEPS = 420
PERTURB_STEPS = 40
MAX_GREEDY_BOUNDARY = 8
TARGET_EXPLAINED = 0.90

FAMILIES = [
    "sparse_random",
    "dense_random",
    "modular",
    "local_ring",
    "global_majority",
    "hierarchical",
]


def encode_bits(arr):
    """Encode rows of 0/1 matrix (T,k) as integer state labels."""
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
    """H(Y|X) for discrete integer labels."""
    y = np.asarray(y)
    x = np.asarray(x)
    if len(y) == 0:
        return 0.0
    groups = defaultdict(list)
    for xi, yi in zip(x.tolist(), y.tolist()):
        groups[xi].append(yi)
    total = len(y)
    out = 0.0
    for vals in groups.values():
        out += (len(vals) / total) * entropy(vals)
    return float(out)


def rankdata(a):
    """Average ranks, scipy-free."""
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[order[j + 1]] == a[order[i]]:
            j += 1
        r = 0.5 * (i + j) + 1.0
        ranks[order[i:j+1]] = r
        i = j + 1
    return ranks


def spearman(x, y):
    x = rankdata(x); y = rankdata(y)
    if np.std(x) == 0 or np.std(y) == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


class BooleanNet:
    def __init__(self, family):
        self.family = family
        self.inputs = []
        self.tables = []
        self.rule = "tables"
        self._build()

    def _random_inputs(self, i, k, pool=None):
        if pool is None:
            pool = list(range(N))
        pool = list(dict.fromkeys(pool))
        if len(pool) < k:
            pool = list(range(N))
        return np.array(RNG.choice(pool, size=k, replace=False), dtype=int)

    def _add_table_node(self, ins):
        k = len(ins)
        table = RNG.integers(0, 2, size=(1 << k), dtype=np.uint8)
        self.inputs.append(np.array(ins, dtype=int))
        self.tables.append(table)

    def _build(self):
        if self.family == "global_majority":
            self.rule = "global_majority"
            return

        if self.family == "sparse_random":
            for i in range(N):
                self._add_table_node(self._random_inputs(i, 2))

        elif self.family == "dense_random":
            for i in range(N):
                self._add_table_node(self._random_inputs(i, 8))

        elif self.family == "modular":
            m = 6
            for i in range(N):
                block = (i // m) * m
                local = list(range(block, min(block + m, N)))
                if RNG.random() < 0.85:
                    ins = self._random_inputs(i, 3, local)
                else:
                    ins = self._random_inputs(i, 3)
                self._add_table_node(ins)

        elif self.family == "local_ring":
            for i in range(N):
                pool = [(i-2) % N, (i-1) % N, i, (i+1) % N, (i+2) % N]
                self._add_table_node(self._random_inputs(i, 3, pool))

        elif self.family == "hierarchical":
            # Four 6-node modules; each node uses two local inputs and one
            # module-summary proxy (first node of another module) with 35% chance.
            m = 6
            hubs = [0, 6, 12, 18]
            for i in range(N):
                block = (i // m) * m
                local = list(range(block, block + m))
                local_ins = list(self._random_inputs(i, 2, local))
                if RNG.random() < 0.35:
                    ext = int(RNG.choice([h for h in hubs if h != block]))
                else:
                    ext = int(RNG.choice(local))
                self._add_table_node(local_ins + [ext])
        else:
            raise ValueError(self.family)

    def step(self, x):
        x = np.asarray(x, dtype=np.uint8)
        if self.rule == "global_majority":
            # Compact, maximally global symmetric rule with node-specific bias bit.
            total = int(x.sum())
            maj = 1 if total > N/2 else 0
            if total == N/2:
                maj = int(x[0])
            # preserve some heterogeneity while retaining all-to-all dependence
            out = np.empty(N, dtype=np.uint8)
            for i in range(N):
                out[i] = maj ^ (i & 1)
            return out

        out = np.empty(N, dtype=np.uint8)
        for i, (ins, table) in enumerate(zip(self.inputs, self.tables)):
            bits = x[ins]
            idx = int(np.dot(bits, (1 << np.arange(len(ins)))))
            out[i] = table[idx]
        return out

    def trajectory(self, initial=None, steps=STEPS+BURN_IN):
        x = RNG.integers(0, 2, size=N, dtype=np.uint8) if initial is None else initial.copy()
        tr = np.empty((steps, N), dtype=np.uint8)
        for t in range(steps):
            tr[t] = x
            x = self.step(x)
        return tr

    def external_parent_set(self, sub):
        sub = set(sub)
        if self.rule == "global_majority":
            return [i for i in range(N) if i not in sub]
        parents = set()
        for node in sub:
            parents.update(int(j) for j in self.inputs[node] if int(j) not in sub)
        return sorted(parents)


def choose_subsystem(family):
    if family == "modular":
        block = int(RNG.integers(0, 4)) * 6
        return sorted(RNG.choice(np.arange(block, block+6), size=SUBSYSTEM_SIZE, replace=False).tolist())
    if family == "local_ring":
        start = int(RNG.integers(0, N))
        return sorted([(start+i) % N for i in range(SUBSYSTEM_SIZE)])
    if family == "hierarchical":
        block = int(RNG.integers(0, 4)) * 6
        return sorted(RNG.choice(np.arange(block, block+6), size=SUBSYSTEM_SIZE, replace=False).tolist())
    return sorted(RNG.choice(np.arange(N), size=SUBSYSTEM_SIZE, replace=False).tolist())


def predictive_interface(tr, sub, candidates):
    """Greedy empirical predictive boundary.

    Baseline = H(S_{t+1}|S_t).
    Candidate external variables are added one at a time to minimize residual
    conditional entropy. Stop when 90% of the best available reduction has
    been captured, or MAX_GREEDY_BOUNDARY variables have been selected.

    To keep v1 computationally auditable, 'best available' is approximated by
    the entropy obtained after greedily adding up to MAX_GREEDY_BOUNDARY vars.
    """
    S0 = encode_bits(tr[:-1, sub])
    S1 = encode_bits(tr[1:, sub])
    baseline = conditional_entropy(S1, S0)
    if baseline < 1e-9 or len(candidates) == 0:
        return 0, baseline, baseline, []

    remaining = list(candidates)
    chosen = []
    history = [(0, baseline)]
    current = baseline

    for _ in range(min(MAX_GREEDY_BOUNDARY, len(remaining))):
        best = None
        for c in remaining:
            cols = chosen + [c]
            B = encode_bits(tr[:-1, cols])
            # Combine S_t and B_t into one joint label safely.
            joint = S0.astype(np.uint64) + (B.astype(np.uint64) << SUBSYSTEM_SIZE)
            h = conditional_entropy(S1, joint)
            if best is None or h < best[0]:
                best = (h, c)
        if best is None:
            break
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

    target_h = baseline - TARGET_EXPLAINED * total_reduction
    complexity = len(chosen)
    for k, h in history:
        if h <= target_h + 1e-12:
            complexity = k
            break
    return complexity, baseline, best_h, chosen


def memory_score(tr, sub):
    s0 = encode_bits(tr[:-1, sub]); s1 = encode_bits(tr[1:, sub])
    h1 = entropy(s1)
    if h1 < 1e-9:
        return 0.0
    mi = h1 - conditional_entropy(s1, s0)
    return max(0.0, min(1.0, mi / h1))


def activity_persistence(tr, sub):
    # Reward non-frozen yet temporally structured states.
    x = tr[:, sub].astype(float)
    activity = float(np.mean(np.var(x, axis=0) * 4.0))  # 0 frozen, <=1 maximal
    # persistence via probability each bit retains value one step later
    retain = float(np.mean(tr[1:, sub] == tr[:-1, sub]))
    temporal = abs(retain - 0.5) * 2.0
    # Need some activity; a frozen fixed point should not score as an observer-like subsystem.
    return max(0.0, min(1.0, activity * (0.5 + 0.5*temporal)))


def robustness_score(net, base_state, sub):
    # Perturb one external bit and ask how similar the subsystem remains after a horizon.
    outside = [i for i in range(N) if i not in sub]
    sims = []
    for _ in range(6):
        x = base_state.copy(); y = base_state.copy()
        j = int(RNG.choice(outside)); y[j] ^= 1
        for _ in range(PERTURB_STEPS):
            x = net.step(x); y = net.step(y)
        sims.append(float(np.mean(x[sub] == y[sub])))
    return float(np.mean(sims))


def geometric_mean(vals, eps=1e-6):
    vals = [max(eps, min(1.0, float(v))) for v in vals]
    return float(math.exp(sum(math.log(v) for v in vals)/len(vals)))


def run():
    print('='*78)
    print(' CANEVAS T3.9 — OBSERVER-SUPPORT LANDSCAPE v1')
    print('='*78)
    print('seed =', SEED)
    print('families =', ', '.join(FAMILIES))
    print('networks/family =', NETWORKS_PER_FAMILY, ' subsystems/network =', SUBSYSTEMS_PER_NETWORK)
    print('N =', N, ' subsystem size =', SUBSYSTEM_SIZE, ' samples/subsystem ~', STEPS)
    print()

    rows = []
    total_networks = len(FAMILIES) * NETWORKS_PER_FAMILY
    done = 0
    for family in FAMILIES:
        for ni in range(NETWORKS_PER_FAMILY):
            net = BooleanNet(family)
            full = net.trajectory(steps=BURN_IN+STEPS+1)
            tr = full[BURN_IN:]
            for si in range(SUBSYSTEMS_PER_NETWORK):
                sub = choose_subsystem(family)
                cand = net.external_parent_set(sub)
                iface, hbase, hbest, chosen = predictive_interface(tr, sub, cand)
                mem = memory_score(tr, sub)
                pers = activity_persistence(tr, sub)
                robust = robustness_score(net, tr[-1].copy(), sub)
                support = geometric_mean([mem, pers, robust])
                rows.append({
                    'family': family,
                    'interface': iface,
                    'candidate_boundary': len(cand),
                    'memory': mem,
                    'persistence': pers,
                    'robustness': robust,
                    'support': support,
                    'Hbase': hbase,
                    'Hbest': hbest,
                })
            done += 1
            if done % 12 == 0 or done == total_networks:
                print(f'progress {done}/{total_networks} networks')

    support = np.array([r['support'] for r in rows])
    iface = np.array([r['interface'] for r in rows], dtype=float)
    candb = np.array([r['candidate_boundary'] for r in rows], dtype=float)

    rho_primary = spearman(support, iface)
    rho_struct = spearman(support, candb)

    print('\n' + '-'*78)
    print('PRIMARY RESULT')
    print('-'*78)
    print(f'n_subsystems = {len(rows)}')
    print(f'Spearman SUPPORT vs PREDICTIVE_INTERFACE = {rho_primary:+.4f}')
    print(f'Spearman SUPPORT vs STRUCTURAL_BOUNDARY = {rho_struct:+.4f}')
    print('Predeclared direction supporting the hypothesis: NEGATIVE.')

    # Compare top vs bottom support quartiles.
    q25, q75 = np.quantile(support, [0.25, 0.75])
    low = iface[support <= q25]
    high = iface[support >= q75]
    print(f'bottom support quartile median interface = {np.median(low):.3f}')
    print(f'top support quartile median interface    = {np.median(high):.3f}')

    print('\nBY FAMILY')
    for fam in FAMILIES:
        rr = [r for r in rows if r['family']==fam]
        s = np.array([r['support'] for r in rr])
        ii = np.array([r['interface'] for r in rr], dtype=float)
        cc = np.array([r['candidate_boundary'] for r in rr], dtype=float)
        print(f'{fam:18s} n={len(rr):3d}  support_med={np.median(s):.3f}  '
              f'iface_med={np.median(ii):.2f}  boundary_med={np.median(cc):.2f}  '
              f'rho={spearman(s,ii):+.3f}')

    # Simple robustness: correlations with each constituent metric.
    print('\nCOMPONENT CHECKS (Spearman vs predictive interface)')
    for key in ['memory','persistence','robustness']:
        vals = np.array([r[key] for r in rows])
        print(f'{key:12s}: {spearman(vals, iface):+.4f}')

    # Locked qualitative verdict, deliberately broad.
    if np.isfinite(rho_primary) and rho_primary <= -0.20 and np.median(high) < np.median(low):
        verdict = 'SUPPORTED_PRELIMINARY'
    elif np.isfinite(rho_primary) and rho_primary >= +0.20:
        verdict = 'CONTRADICTED_PRELIMINARY'
    else:
        verdict = 'INCONCLUSIVE_PRELIMINARY'

    print('\nPREDECLARED T3.9 VERDICT =', verdict)
    print('\nINTERPRETATION LOCK:')
    print('- This does NOT identify consciousness.')
    print('- A negative correlation only supports the narrower claim that persistent')
    print('  information-processing individuality tends to coexist with compact predictive interfaces.')
    print('- Family-specific reversals count against universality and must be reported.')
    print('- Do not tune thresholds/ensembles after seeing this run; changes require v2 preregistration.')
    print('\nFINISHED T3.9 v1')


if __name__ == '__main__':
    run()
