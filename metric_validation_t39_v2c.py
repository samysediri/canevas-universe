"""Canevas T3.9-v2c — null-calibrated predictive-dimension validation.

Preregistered synthetic instrument test. This does NOT test observer theory.
It asks whether a permutation-calibrated estimator can distinguish:
  1) one genuinely predictive external degree of freedom,
  2) eight redundant channels carrying one latent degree of freedom,
  3) four independent predictive degrees of freedom,
  4) eight irrelevant noise channels.

No thresholds/cases may be changed after seeing this run. Any later revision is v2d.
"""
from __future__ import annotations
import numpy as np
from collections import defaultdict

SEED=390117
RNG=np.random.default_rng(SEED)
N=24000
TRAIN_FRAC=0.40
CAL_FRAC=0.30
N_NULL=200
ALPHA=0.01
MAX_D=4
REDUNDANCY_FLIP=0.08


def encode_bits(a):
    a=np.asarray(a,dtype=np.uint8)
    if a.ndim==1: a=a[:,None]
    w=(1 << np.arange(a.shape[1],dtype=np.uint64))
    return (a.astype(np.uint64)*w).sum(1)


def entropy(y):
    _,c=np.unique(np.asarray(y),return_counts=True)
    if c.sum()==0:return 0.0
    p=c/c.sum(); return float(-(p*np.log2(p)).sum())


def cond_entropy(y,x):
    groups=defaultdict(list)
    for xx,yy in zip(np.asarray(x).tolist(),np.asarray(y).tolist()): groups[xx].append(yy)
    n=len(y)
    return float(sum(len(v)/n*entropy(v) for v in groups.values()))


def ce_for_cols(S0,S1,E,idx,cols):
    s0=encode_bits(S0[idx]); s1=encode_bits(S1[idx])
    if not cols:return cond_entropy(s1,s0)
    e=encode_bits(E[idx][:,cols])
    joint=s0+(e.astype(np.uint64)<<S0.shape[1])
    return cond_entropy(s1,joint)


def best_subset(S0,S1,E,idx,d):
    # Exhaustive for d<=4 among 8 channels. Avoids greedy synergy blindness.
    import itertools
    base=ce_for_cols(S0,S1,E,idx,[])
    best=(float('-inf'),None)
    for cols in itertools.combinations(range(E.shape[1]),d):
        gain=base-ce_for_cols(S0,S1,E,idx,list(cols))
        if gain>best[0]:best=(gain,list(cols))
    return best


def test_gain(S0,S1,E,idx,cols):
    return ce_for_cols(S0,S1,E,idx,[])-ce_for_cols(S0,S1,E,idx,cols)


def null_distribution(S0,S1,E,cal_idx,cols,n_null=N_NULL):
    # Keep target/internal-state pairs intact; independently permute selected
    # environmental channels, destroying predictive relation while preserving marginals.
    base=ce_for_cols(S0,S1,E,cal_idx,[])
    vals=[]
    original=E[cal_idx][:,cols].copy()
    s0=encode_bits(S0[cal_idx]); s1=encode_bits(S1[cal_idx])
    for _ in range(n_null):
        ep=original.copy()
        for j in range(ep.shape[1]): ep[:,j]=ep[RNG.permutation(len(ep)),j]
        eb=encode_bits(ep); joint=s0+(eb.astype(np.uint64)<<S0.shape[1])
        vals.append(base-cond_entropy(s1,joint))
    return np.asarray(vals)


def evaluate(name,S0,S1,E,expected):
    idx=RNG.permutation(len(S0)); a=int(TRAIN_FRAC*len(idx)); b=int((TRAIN_FRAC+CAL_FRAC)*len(idx))
    tr,cal,te=idx[:a],idx[a:b],idx[b:]
    rows=[]
    print('\n'+name, 'expected=',expected)
    for d in range(1,MAX_D+1):
        train_gain,cols=best_subset(S0,S1,E,tr,d)
        cal_gain=test_gain(S0,S1,E,cal,cols)
        null=null_distribution(S0,S1,E,cal,cols)
        # Empirical one-sided p with +1 correction; also demand positive excess over 99th null percentile.
        p=(1+int(np.sum(null>=cal_gain)))/(len(null)+1)
        q99=float(np.quantile(null,0.99))
        significant=(p<=ALPHA and cal_gain>q99 and cal_gain>0)
        held=test_gain(S0,S1,E,te,cols)
        rows.append((d,cols,train_gain,cal_gain,q99,p,significant,held))
        print(f'd={d} cols={cols} train={train_gain:.4f} cal={cal_gain:.4f} null99={q99:.4f} p={p:.4f} sig={significant} heldout={held:.4f}')

    sig=[r for r in rows if r[6]]
    # Effective dimension: smallest significant d whose independent held-out gain reaches
    # >=90% of the maximum significant held-out gain. This is channel-subset dimension,
    # not a claim of unique latent causal dimension.
    eff=0; maxheld=0.0
    if sig:
        maxheld=max(max(0.0,r[7]) for r in sig)
        if maxheld>0:
            target=.90*maxheld
            for r in sig:
                if r[7]>=target: eff=r[0]; break
    print(f'effective_dimension_90={eff} max_significant_heldout_gain={maxheld:.4f}')
    return {'name':name,'eff':eff,'maxgain':maxheld,'rows':rows}


def cases():
    S0=RNG.integers(0,2,(N,2),dtype=np.uint8)
    # low simple
    E1=RNG.integers(0,2,(N,8),dtype=np.uint8); y=S0[:,0]^E1[:,0]
    Y1=np.column_stack([y,S0[:,1]]).astype(np.uint8)
    # rich compressible: 8 noisy sensors of one latent Z; target depends only on Z
    Z=RNG.integers(0,2,N,dtype=np.uint8); E2=np.empty((N,8),dtype=np.uint8)
    for j in range(8): E2[:,j]=Z^(RNG.random(N)<REDUNDANCY_FLIP).astype(np.uint8)
    Y2=np.column_stack([S0[:,0]^Z,S0[:,1]]).astype(np.uint8)
    # rich irreducible: four independent target bits need four independent E dimensions
    S03=RNG.integers(0,2,(N,4),dtype=np.uint8); E3=RNG.integers(0,2,(N,8),dtype=np.uint8)
    Y3=np.column_stack([S03[:,j]^E3[:,j] for j in range(4)]).astype(np.uint8)
    # rich noise
    E4=RNG.integers(0,2,(N,8),dtype=np.uint8); U=RNG.integers(0,2,N,dtype=np.uint8)
    Y4=np.column_stack([S0[:,0]^U,S0[:,1]]).astype(np.uint8)
    return [('LOW_SIMPLE',S0,Y1,E1,'dimension~1'),('RICH_COMPRESSIBLE',S0,Y2,E2,'low dimension despite 8 channels'),('RICH_IRREDUCIBLE',S03,Y3,E3,'dimension>=3, ideally 4'),('RICH_NOISE',S0,Y4,E4,'no significant predictive dimension')]


def run():
    print('='*78); print('CANEVAS T3.9-v2c — NULL-CALIBRATED PREDICTIVE DIMENSION VALIDATION'); print('='*78)
    print('seed=',SEED,'N/case=',N,'train/cal/test=',TRAIN_FRAC,CAL_FRAC,1-TRAIN_FRAC-CAL_FRAC)
    print('null permutations=',N_NULL,'alpha=',ALPHA,'max dimension=',MAX_D)
    print('Selection=train; significance=calibration; final gain=untouched test.')
    print('No post-hoc threshold/case changes are allowed.\n')
    out={r['name']:r for r in [evaluate(*c) for c in cases()]}
    c1=(out['LOW_SIMPLE']['eff']==1 and out['LOW_SIMPLE']['maxgain']>0)
    c2=(1<=out['RICH_COMPRESSIBLE']['eff']<=2 and out['RICH_COMPRESSIBLE']['maxgain']>0)
    c3=(out['RICH_IRREDUCIBLE']['eff']>=3 and out['RICH_IRREDUCIBLE']['maxgain']>0)
    c4=(out['RICH_NOISE']['eff']==0)
    print('\n'+'-'*78); print('PREDECLARED VALIDATION SUMMARY'); print('-'*78)
    print('LOW_SIMPLE dimension exactly 1:',c1)
    print('RICH_COMPRESSIBLE dimension <=2 despite 8 channels:',c2)
    print('RICH_IRREDUCIBLE dimension >=3:',c3)
    print('RICH_NOISE no significant dimension:',c4)
    if c1 and c2 and c3 and c4: verdict='NULL_CALIBRATED_DIMENSION_METRIC_VALIDATED_SYNTHETICALLY'
    elif not c4: verdict='FAIL_NOISE_NULL_CONTROL'
    elif not c2: verdict='FAIL_COMPRESSIBLE_LATENT_CONTROL'
    elif not c3: verdict='FAIL_IRREDUCIBLE_DIMENSION_CONTROL'
    else: verdict='METRIC_NOT_VALIDATED'
    print('\nPREDECLARED T3.9-v2c VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- A pass validates this instrument only on these synthetic controls, not Canevas or observer theory.')
    print('- A failure ends this metric branch unless a separately preregistered v2d has an independently motivated correction.')
    print('- T3.9-v1/v2 predictive correlations remain uninterpretable regardless of this result; a pass permits only a NEW preregistered network replication.')
    print('- Structural v2 remains a separate weak/inconclusive result.')
    print('\nFINISHED T3.9-v2c')
if __name__=='__main__': run()
