"""CANEVAS T4.0 — predictive-compression instrument, synthetic validation only.

Implements the preregistered T4 question without using network/Canevas results.
We estimate how much of the environment's predictive information can be retained by
compressed binary representations Z of increasing code size.

IMPORTANT: this is an instrument test, not an observer/consciousness test.
"""
from __future__ import annotations
import itertools
import numpy as np
from collections import defaultdict

SEED = 404001
RNG = np.random.default_rng(SEED)
N = 30000
TRAIN_FRAC = 0.40
CAL_FRAC = 0.30
N_NULL = 200
ALPHA = 0.01
MAX_CODE_BITS = 4


def enc(a):
    a=np.asarray(a,dtype=np.uint8)
    if a.ndim==1:a=a[:,None]
    return (a.astype(np.uint64)*(1<<np.arange(a.shape[1],dtype=np.uint64))).sum(1)


def H(y):
    _,c=np.unique(y,return_counts=True); p=c/c.sum()
    return float(-(p*np.log2(p)).sum())


def Hcond(y,x):
    d=defaultdict(list)
    for xx,yy in zip(x.tolist(),y.tolist()):d[xx].append(yy)
    n=len(y)
    return float(sum(len(v)/n*H(np.asarray(v)) for v in d.values()))


def gain(S0,S1,Z,idx):
    s0=enc(S0[idx]); s1=enc(S1[idx]); base=Hcond(s1,s0)
    if Z is None:return 0.0
    z=enc(Z[idx]); joint=s0+(z<<S0.shape[1])
    return base-Hcond(s1,joint)


def full_gain(S0,S1,E,idx):return gain(S0,S1,E,idx)


def candidate_codes(E,max_bits=MAX_CODE_BITS):
    """Deterministic, predeclared code family.

    Includes individual observed bits plus XOR and majority projections of subsets.
    This deliberately tests whether a small predictive representation can summarize
    redundant channels and detect synergistic structure. It is not claimed universal.
    """
    m=E.shape[1]; codes=[]; names=[]
    # individual channels
    for j in range(m): codes.append(E[:,j:j+1]); names.append(f'x{j}')
    # subset majority codes (sizes 3..m) and XOR codes (sizes 2..min(4,m))
    for r in range(3,m+1):
        for sub in itertools.combinations(range(m),r):
            a=E[:,sub]; codes.append((a.sum(1)>=(r+1)//2).astype(np.uint8)[:,None]); names.append('maj'+str(sub))
    for r in range(2,min(4,m)+1):
        for sub in itertools.combinations(range(m),r):
            a=np.bitwise_xor.reduce(E[:,sub],axis=1); codes.append(a[:,None]); names.append('xor'+str(sub))
    return codes,names


def choose_codebook(S0,S1,E,tr,max_k=MAX_CODE_BITS):
    atoms,names=candidate_codes(E)
    # Rank atoms on train, then form codebooks from top atoms. This is intentionally
    # a representation-size curve, not a claim about causal latent dimension.
    scored=sorted([(gain(S0,S1,z,tr),i) for i,z in enumerate(atoms)],reverse=True)
    top=[i for _,i in scored[:max(12,max_k)]]
    books=[]
    for k in range(1,max_k+1):
        best=(-1,None,None)
        # Exhaustive combinations among pre-screened train-only atoms.
        for inds in itertools.combinations(top,k):
            Z=np.column_stack([atoms[i][:,0] for i in inds])
            g=gain(S0,S1,Z,tr)
            if g>best[0]:best=(g,Z,[names[i] for i in inds])
        books.append(best)
    return books


def null_p(S0,S1,Z,idx,observed):
    vals=[]
    for _ in range(N_NULL):
        Zp=Z.copy()
        for j in range(Zp.shape[1]):Zp[:,j]=Zp[RNG.permutation(len(Zp)),j]
        # local arrays so permutation applies only calibration rows
        s0=enc(S0[idx]); s1=enc(S1[idx]); base=Hcond(s1,s0); z=enc(Zp[idx]); joint=s0+(z<<S0.shape[1])
        vals.append(base-Hcond(s1,joint))
    vals=np.asarray(vals)
    return (1+np.sum(vals>=observed))/(N_NULL+1),float(np.quantile(vals,.99))


def evaluate(name,S0,S1,E):
    idx=RNG.permutation(N); a=int(TRAIN_FRAC*N); b=int((TRAIN_FRAC+CAL_FRAC)*N)
    tr,ca,te=idx[:a],idx[a:b],idx[b:]
    fg=full_gain(S0,S1,E,te)
    books=choose_codebook(S0,S1,E,tr)
    rows=[]
    print('\n'+name); print(f'full_environment_heldout_gain={fg:.5f}')
    for k,(tg,Z,names) in enumerate(books,1):
        cg=gain(S0,S1,Z,ca); p,q=null_p(S0,S1,Z,ca,cg); hg=gain(S0,S1,Z,te)
        retention=(hg/fg if fg>1e-9 else 0.0)
        sig=(p<=ALPHA and cg>q and cg>0)
        rows.append((k,hg,retention,sig,names))
        print(f'k={k} heldout_gain={hg:.5f} retention={retention:.4f} sig={sig} p={p:.4f} code={names}')
    return {'full':fg,'rows':rows}


def make_cases():
    # Internal present state is deliberately independent nuisance context.
    S=np.zeros((N,1),dtype=np.uint8)
    # NULL
    E0=RNG.integers(0,2,(N,8),dtype=np.uint8); y0=RNG.integers(0,2,N,dtype=np.uint8)[:,None]
    # ONE CAUSE REDUNDANT: 8 noisy sensors of Z; majority is compact recovery.
    z=RNG.integers(0,2,N,dtype=np.uint8); E1=np.column_stack([z^(RNG.random(N)<.10) for _ in range(8)]).astype(np.uint8); y1=z[:,None]
    # FOUR CAUSES: target is 4-bit vector, four independent causes plus nuisance copies.
    c=RNG.integers(0,2,(N,4),dtype=np.uint8); E4=np.column_stack([c,RNG.integers(0,2,(N,4),dtype=np.uint8)]); y4=c.copy(); S4=np.zeros((N,1),dtype=np.uint8)
    # NUISANCE_RICH: one exact predictive channel + seven independent nuisance channels.
    zn=RNG.integers(0,2,N,dtype=np.uint8); En=np.column_stack([zn,RNG.integers(0,2,(N,7),dtype=np.uint8)]); yn=zn[:,None]
    # XOR synergy: two individually uninformative causes jointly determine target.
    Ex=RNG.integers(0,2,(N,8),dtype=np.uint8); yx=(Ex[:,0]^Ex[:,1])[:,None]
    return [('NULL_NOISE',S,y0,E0),('ONE_CAUSE_REDUNDANT',S,y1,E1),('FOUR_CAUSES',S4,y4,E4),('NUISANCE_RICH',S,yn,En),('SYNERGY_XOR',S,yx,Ex)]


def min_k_90(r):
    for k,g,ret,sig,_ in r['rows']:
        if sig and ret>=.90:return k
    return None


def run():
    print('='*76);print('CANEVAS T4.0 — PREDICTIVE COMPRESSION SYNTHETIC VALIDATION');print('='*76)
    print('seed=',SEED,'N/case=',N,'null permutations=',N_NULL)
    print('Train chooses representations; calibration tests significance; test reports retention.')
    out={name:evaluate(name,S0,S1,E) for name,S0,S1,E in make_cases()}
    dims={k:min_k_90(v) for k,v in out.items()}
    null_ok=out['NULL_NOISE']['full']<0.02 and dims['NULL_NOISE'] is None
    one_ok=dims['ONE_CAUSE_REDUNDANT']==1
    four_ok=dims['FOUR_CAUSES'] is not None and dims['FOUR_CAUSES']>=3
    nuisance_ok=dims['NUISANCE_RICH']==1
    xor_ok=dims['SYNERGY_XOR'] is not None and out['SYNERGY_XOR']['rows'][dims['SYNERGY_XOR']-1][1]>0.5
    print('\n'+'-'*76);print('PREDECLARED T4.0 SUMMARY');print('-'*76)
    for k,v in dims.items():print(f'{k:20s} min_code_bits_for_90pct={v}')
    print('NULL_NOISE pass:',null_ok);print('ONE_CAUSE_REDUNDANT pass:',one_ok);print('FOUR_CAUSES pass:',four_ok);print('NUISANCE_RICH pass:',nuisance_ok);print('SYNERGY_XOR pass:',xor_ok)
    verdict='T4_INSTRUMENT_PROMISING_SYNTHETIC' if all([null_ok,one_ok,four_ok,nuisance_ok,xor_ok]) else 'T4_INSTRUMENT_NOT_VALIDATED'
    print('\nPREDECLARED T4.0 VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- Passing validates only this finite candidate-code family on these synthetic controls.')
    print('- It does not establish latent causal dimension, consciousness, observers, or Canevas cosmology.')
    print('- Failure may be diagnosed but not repaired under the T4.0 label.')
    print('- A pass permits only a separately preregistered network experiment.')
    print('\nFINISHED T4.0')
if __name__=='__main__':run()
