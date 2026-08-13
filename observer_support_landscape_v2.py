"""Canevas T3.9-v2 — controlled observer-support replication.

Goals (predeclared before seeing v2 results)
------------------------------------------
1) Test whether SUPPORT vs STRUCTURAL_BOUNDARY remains negative WITHIN families.
2) Replace the invalid in-sample predictive-interface metric with a held-out
   cross-validated predictive gain metric.

No thresholds are tuned from v2 outcomes.
"""

from __future__ import annotations
import math, random
from collections import defaultdict
import numpy as np

SEED = 49103
RNG = np.random.default_rng(SEED)
random.seed(SEED)

N = 24
SUBSYSTEM_SIZE = 4
NETWORKS_PER_FAMILY = 24
SUBSYSTEMS_PER_NETWORK = 8
BURN_IN = 100
STEPS = 600
TRAIN_FRAC = 0.60
MAX_GREEDY_BOUNDARY = 8
MIN_TEST_GAIN_BITS = 0.02
PERTURB_STEPS = 40

FAMILIES = [
    "sparse_random", "dense_random", "modular", "local_ring",
    "global_majority", "hierarchical",
]


def encode_bits(arr):
    arr = np.asarray(arr, dtype=np.uint8)
    if arr.ndim == 1:
        arr = arr[:, None]
    w = (1 << np.arange(arr.shape[1], dtype=np.uint64))
    return (arr.astype(np.uint64) * w).sum(axis=1)


def entropy(labels):
    labels = np.asarray(labels)
    if len(labels) == 0: return 0.0
    _, c = np.unique(labels, return_counts=True)
    p = c / c.sum()
    return float(-(p*np.log2(p)).sum())


def cond_entropy(y, x):
    y = np.asarray(y); x = np.asarray(x)
    groups = defaultdict(list)
    for xi, yi in zip(x.tolist(), y.tolist()): groups[xi].append(yi)
    n = len(y)
    return float(sum((len(v)/n)*entropy(v) for v in groups.values()))


def rankdata(a):
    a=np.asarray(a,float); o=np.argsort(a,kind='mergesort'); r=np.empty(len(a),float)
    i=0
    while i<len(a):
        j=i
        while j+1<len(a) and a[o[j+1]]==a[o[i]]: j+=1
        rr=0.5*(i+j)+1; r[o[i:j+1]]=rr; i=j+1
    return r


def spearman(x,y):
    x=rankdata(x); y=rankdata(y)
    if np.std(x)==0 or np.std(y)==0: return float('nan')
    return float(np.corrcoef(x,y)[0,1])


class BooleanNet:
    def __init__(self,fam): self.fam=fam; self.inputs=[]; self.tables=[]; self.rule='tables'; self.build()
    def rin(self,k,pool=None):
        p=list(range(N)) if pool is None else list(dict.fromkeys(pool))
        if len(p)<k: p=list(range(N))
        return np.array(RNG.choice(p,size=k,replace=False),int)
    def add(self,ins):
        ins=np.array(ins,int); self.inputs.append(ins)
        self.tables.append(RNG.integers(0,2,size=(1<<len(ins)),dtype=np.uint8))
    def build(self):
        if self.fam=='global_majority': self.rule='global_majority'; return
        for i in range(N):
            if self.fam=='sparse_random': ins=self.rin(2)
            elif self.fam=='dense_random': ins=self.rin(8)
            elif self.fam=='modular':
                b=(i//6)*6; local=list(range(b,b+6)); ins=self.rin(3, local if RNG.random()<0.85 else None)
            elif self.fam=='local_ring': ins=self.rin(3,[(i+d)%N for d in (-2,-1,0,1,2)])
            elif self.fam=='hierarchical':
                b=(i//6)*6; local=list(range(b,b+6)); a=list(self.rin(2,local)); hubs=[0,6,12,18]
                ext=int(RNG.choice([h for h in hubs if h!=b])) if RNG.random()<0.35 else int(RNG.choice(local)); ins=a+[ext]
            else: raise ValueError(self.fam)
            self.add(ins)
    def step(self,x):
        x=np.asarray(x,dtype=np.uint8)
        if self.rule=='global_majority':
            s=int(x.sum()); maj=1 if s>N/2 else 0
            if s==N/2: maj=int(x[0])
            return np.array([maj^(i&1) for i in range(N)],dtype=np.uint8)
        out=np.empty(N,dtype=np.uint8)
        for i,(ins,tab) in enumerate(zip(self.inputs,self.tables)):
            idx=int(np.dot(x[ins],1<<np.arange(len(ins)))); out[i]=tab[idx]
        return out
    def traj(self,steps):
        x=RNG.integers(0,2,size=N,dtype=np.uint8); tr=np.empty((steps,N),dtype=np.uint8)
        for t in range(steps): tr[t]=x; x=self.step(x)
        return tr
    def extparents(self,sub):
        ss=set(sub)
        if self.rule=='global_majority': return [i for i in range(N) if i not in ss]
        p=set()
        for j in sub: p.update(int(k) for k in self.inputs[j] if int(k) not in ss)
        return sorted(p)


def choose_sub(fam):
    if fam in ('modular','hierarchical'):
        b=int(RNG.integers(0,4))*6; return sorted(RNG.choice(np.arange(b,b+6),size=SUBSYSTEM_SIZE,replace=False).tolist())
    if fam=='local_ring':
        s=int(RNG.integers(0,N)); return sorted([(s+i)%N for i in range(SUBSYSTEM_SIZE)])
    return sorted(RNG.choice(np.arange(N),size=SUBSYSTEM_SIZE,replace=False).tolist())


def memory_score(tr,sub):
    s0=encode_bits(tr[:-1,sub]); s1=encode_bits(tr[1:,sub]); h=entropy(s1)
    return 0.0 if h<1e-9 else max(0.0,min(1.0,(h-cond_entropy(s1,s0))/h))


def persistence_score(tr,sub):
    x=tr[:,sub].astype(float); activity=float(np.mean(np.var(x,axis=0)*4.0)); retain=float(np.mean(tr[1:,sub]==tr[:-1,sub])); temporal=abs(retain-0.5)*2.0
    return max(0.0,min(1.0,activity*(0.5+0.5*temporal)))


def robustness(net,state,sub):
    outside=[i for i in range(N) if i not in sub]; vals=[]
    for _ in range(6):
        x=state.copy(); y=state.copy(); j=int(RNG.choice(outside)); y[j]^=1
        for _ in range(PERTURB_STEPS): x=net.step(x); y=net.step(y)
        vals.append(float(np.mean(x[sub]==y[sub])))
    return float(np.mean(vals))


def gmean(vals,eps=1e-6): return float(math.exp(sum(math.log(max(eps,min(1.0,float(v)))) for v in vals)/len(vals)))


def heldout_interface_gain(tr,sub,candidates):
    """Greedy variable selection on train only; evaluate entropy gain on untouched test.

    Returns selected_count and heldout predictive gain in bits. Selection stops when
    the next selected variable fails to improve TRAIN entropy. No test data guide selection.
    """
    S0=encode_bits(tr[:-1,sub]); S1=encode_bits(tr[1:,sub]); m=len(S0); cut=int(TRAIN_FRAC*m)
    tr_idx=np.arange(cut); te_idx=np.arange(cut,m)
    base_test=cond_entropy(S1[te_idx],S0[te_idx])
    if len(candidates)==0: return 0,0.0
    chosen=[]; remaining=list(candidates); cur_train=cond_entropy(S1[tr_idx],S0[tr_idx])
    for _ in range(min(MAX_GREEDY_BOUNDARY,len(remaining))):
        best=None
        for c in remaining:
            cols=chosen+[c]; B=encode_bits(tr[:-1,cols]); joint=S0.astype(np.uint64)+(B.astype(np.uint64)<<SUBSYSTEM_SIZE)
            h=cond_entropy(S1[tr_idx],joint[tr_idx])
            if best is None or h<best[0]: best=(h,c)
        if best is None or cur_train-best[0] < 1e-6: break
        cur_train,c=best; chosen.append(c); remaining.remove(c)
    if not chosen: return 0,0.0
    B=encode_bits(tr[:-1,chosen]); joint=S0.astype(np.uint64)+(B.astype(np.uint64)<<SUBSYSTEM_SIZE)
    test_h=cond_entropy(S1[te_idx],joint[te_idx]); gain=max(0.0,base_test-test_h)
    effective_count=len(chosen) if gain>=MIN_TEST_GAIN_BITS else 0
    return effective_count,gain


def run():
    print('='*76); print(' CANEVAS T3.9-v2 — CONTROLLED REPLICATION'); print('='*76)
    print('seed=',SEED,' networks/family=',NETWORKS_PER_FAMILY,' subsystems/network=',SUBSYSTEMS_PER_NETWORK)
    print('Primary structural hypothesis: within-family SUPPORT vs boundary should be negative.')
    print('Predictive metric: train-selected, held-out entropy gain; test never guides selection.\n')
    rows=[]; total=len(FAMILIES)*NETWORKS_PER_FAMILY; done=0
    for fam in FAMILIES:
        for _ in range(NETWORKS_PER_FAMILY):
            net=BooleanNet(fam); full=net.traj(BURN_IN+STEPS+1); tr=full[BURN_IN:]
            for _ in range(SUBSYSTEMS_PER_NETWORK):
                sub=choose_sub(fam); cand=net.extparents(sub)
                mem=memory_score(tr,sub); per=persistence_score(tr,sub); rob=robustness(net,tr[-1].copy(),sub); sup=gmean([mem,per,rob])
                pc,pg=heldout_interface_gain(tr,sub,cand)
                rows.append((fam,sup,len(cand),pc,pg))
            done+=1
            if done%16==0 or done==total: print(f'progress {done}/{total} networks')

    print('\nPRIMARY STRUCTURAL RESULT')
    fam_rhos=[]
    for fam in FAMILIES:
        rr=[r for r in rows if r[0]==fam]; s=[r[1] for r in rr]; b=[r[2] for r in rr]; rho=spearman(s,b); fam_rhos.append(rho)
        print(f'{fam:18s} rho_within={rho:+.4f}  n={len(rr)}  boundary_med={np.median(b):.2f}  support_med={np.median(s):.3f}')
    finite=[r for r in fam_rhos if not np.isnan(r)]
    neg=sum(r<0 for r in finite); med=float(np.median(finite)) if finite else float('nan')
    print(f'within-family negative count = {neg}/{len(finite)}')
    print(f'median within-family rho = {med:+.4f}')

    print('\nHELD-OUT PREDICTIVE RESULT')
    s=np.array([r[1] for r in rows]); pc=np.array([r[3] for r in rows],float); pg=np.array([r[4] for r in rows],float)
    print(f'Spearman SUPPORT vs CV_INTERFACE_COUNT = {spearman(s,pc):+.4f}')
    print(f'Spearman SUPPORT vs HELDOUT_GAIN       = {spearman(s,pg):+.4f}')
    print(f'fraction with positive heldout gain >= {MIN_TEST_GAIN_BITS:.2f} bits = {np.mean(pg>=MIN_TEST_GAIN_BITS):.4f}')

    # Predeclared coarse verdict for structural signal.
    if len(finite)>=3 and neg>=math.ceil(0.75*len(finite)) and med<=-0.20:
        verdict='STRUCTURAL_SIGNAL_REPLICATES_WITHIN_FAMILIES'
    elif len(finite)>=3 and neg<=math.floor(0.50*len(finite)) and med>-0.10:
        verdict='GLOBAL_V1_SIGNAL_LIKELY_BETWEEN_FAMILY_CONFOUND'
    else:
        verdict='INCONCLUSIVE_CONTROLLED_REPLICATION'
    print('\nPREDECLARED T3.9-v2 VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- Do not rescue a failed structural replication by changing family weights or thresholds.')
    print('- Predictive-interface result is secondary until separately validated on synthetic held-out tests.')
    print('- This experiment concerns persistent information-processing proxies, not consciousness.')
    print('\nFINISHED T3.9-v2')

if __name__=='__main__': run()
