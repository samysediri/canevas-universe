"""CANEVAS T4.0b — predictive compression with permutation-calibrated null control.

T4.0 is closed as NOT VALIDATED because NULL_NOISE failed an absolute full-gain
threshold, despite producing no significant compressed code. T4.0b changes only
the null-control decision rule: significance of the FULL environment is now
calibrated against a permutation null using the same held-out estimator.

All non-null synthetic cases and the 90% retention rule are kept conceptually
unchanged. This is still instrument validation only.
"""
from __future__ import annotations
import itertools
import numpy as np
from collections import defaultdict

SEED = 404101
RNG = np.random.default_rng(SEED)
N = 30000
TRAIN_FRAC = 0.40
CAL_FRAC = 0.30
N_NULL = 300
ALPHA = 0.01
MAX_CODE_BITS = 4


def enc(a):
    a=np.asarray(a,dtype=np.uint8)
    if a.ndim==1:a=a[:,None]
    return (a.astype(np.uint64)*(1<<np.arange(a.shape[1],dtype=np.uint64))).sum(1)


def H(y):
    _,c=np.unique(y,return_counts=True)
    p=c/c.sum()
    return float(-(p*np.log2(p)).sum())


def Hcond(y,x):
    d=defaultdict(list)
    for xx,yy in zip(x.tolist(),y.tolist()): d[xx].append(yy)
    n=len(y)
    return float(sum(len(v)/n*H(np.asarray(v)) for v in d.values()))


def gain(S0,S1,Z,idx):
    s0=enc(S0[idx]); s1=enc(S1[idx]); base=Hcond(s1,s0)
    if Z is None:return 0.0
    z=enc(Z[idx]); joint=s0+(z<<S0.shape[1])
    return base-Hcond(s1,joint)


def candidate_codes(E):
    m=E.shape[1]; codes=[]; names=[]
    for j in range(m):
        codes.append(E[:,j:j+1]); names.append(f'x{j}')
    for r in range(3,m+1):
        for sub in itertools.combinations(range(m),r):
            a=E[:,sub]
            codes.append((a.sum(1)>=(r+1)//2).astype(np.uint8)[:,None]); names.append('maj'+str(sub))
    for r in range(2,min(4,m)+1):
        for sub in itertools.combinations(range(m),r):
            a=np.bitwise_xor.reduce(E[:,sub],axis=1)
            codes.append(a[:,None]); names.append('xor'+str(sub))
    return codes,names


def choose_codebooks(S0,S1,E,tr):
    atoms,names=candidate_codes(E)
    scored=sorted([(gain(S0,S1,z,tr),i) for i,z in enumerate(atoms)],reverse=True)
    top=[i for _,i in scored[:max(12,MAX_CODE_BITS)]]
    books=[]
    for k in range(1,MAX_CODE_BITS+1):
        best=(-1,None,None)
        for inds in itertools.combinations(top,k):
            Z=np.column_stack([atoms[i][:,0] for i in inds])
            g=gain(S0,S1,Z,tr)
            if g>best[0]: best=(g,Z,[names[i] for i in inds])
        books.append(best)
    return books


def permutation_null_gain(S0,S1,Z,idx,n_null=N_NULL):
    obs=gain(S0,S1,Z,idx)
    vals=[]
    Zidx=Z[idx].copy()
    s0=S0[idx]; s1=S1[idx]
    local_idx=np.arange(len(idx))
    for _ in range(n_null):
        Zp=Zidx.copy()
        # Row permutation preserves cross-channel dependence of the full representation.
        Zp=Zp[RNG.permutation(len(Zp))]
        vals.append(gain(s0,s1,Zp,local_idx))
    vals=np.asarray(vals)
    p=(1+int(np.sum(vals>=obs)))/(len(vals)+1)
    q99=float(np.quantile(vals,0.99))
    sig=(p<=ALPHA and obs>q99)
    return obs,p,q99,sig


def evaluate(name,S0,S1,E):
    idx=RNG.permutation(N); a=int(TRAIN_FRAC*N); b=int((TRAIN_FRAC+CAL_FRAC)*N)
    tr,ca,te=idx[:a],idx[a:b],idx[b:]

    # Full-environment significance is calibrated ONLY on calibration data.
    full_cal,full_p,full_q99,full_sig=permutation_null_gain(S0,S1,E,ca)
    full_test=gain(S0,S1,E,te)

    books=choose_codebooks(S0,S1,E,tr)
    rows=[]
    print('\n'+name)
    print(f'full_cal_gain={full_cal:.5f} full_null99={full_q99:.5f} full_p={full_p:.4f} full_sig={full_sig}')
    print(f'full_environment_heldout_gain={full_test:.5f}')
    for k,(tg,Z,names) in enumerate(books,1):
        cg,cp,cq,csig=permutation_null_gain(S0,S1,Z,ca)
        hg=gain(S0,S1,Z,te)
        retention=(hg/full_test if full_test>1e-9 else 0.0)
        rows.append((k,hg,retention,csig,names,cp,cq))
        print(f'k={k} heldout_gain={hg:.5f} retention={retention:.4f} sig={csig} p={cp:.4f} code={names}')
    return {'full_test':full_test,'full_sig':full_sig,'full_p':full_p,'rows':rows}


def make_cases():
    S=np.zeros((N,1),dtype=np.uint8)
    E0=RNG.integers(0,2,(N,8),dtype=np.uint8); y0=RNG.integers(0,2,N,dtype=np.uint8)[:,None]
    z=RNG.integers(0,2,N,dtype=np.uint8)
    E1=np.column_stack([z^(RNG.random(N)<.10) for _ in range(8)]).astype(np.uint8); y1=z[:,None]
    c=RNG.integers(0,2,(N,4),dtype=np.uint8)
    E4=np.column_stack([c,RNG.integers(0,2,(N,4),dtype=np.uint8)]); y4=c.copy(); S4=np.zeros((N,1),dtype=np.uint8)
    zn=RNG.integers(0,2,N,dtype=np.uint8)
    En=np.column_stack([zn,RNG.integers(0,2,(N,7),dtype=np.uint8)]); yn=zn[:,None]
    Ex=RNG.integers(0,2,(N,8),dtype=np.uint8); yx=(Ex[:,0]^Ex[:,1])[:,None]
    return [('NULL_NOISE',S,y0,E0),('ONE_CAUSE_REDUNDANT',S,y1,E1),('FOUR_CAUSES',S4,y4,E4),('NUISANCE_RICH',S,yn,En),('SYNERGY_XOR',S,yx,Ex)]


def min_k_90(r):
    if not r['full_sig']:
        return None
    for k,g,ret,sig,*_ in r['rows']:
        if sig and ret>=.90:return k
    return None


def run():
    print('='*78)
    print('CANEVAS T4.0b — PERMUTATION-CALIBRATED PREDICTIVE COMPRESSION')
    print('='*78)
    print('seed=',SEED,'N/case=',N,'null permutations=',N_NULL,'alpha=',ALPHA)
    print('Only T4.0 change: NULL/FULL significance is permutation-calibrated, not absolute-thresholded.')
    out={name:evaluate(name,S0,S1,E) for name,S0,S1,E in make_cases()}
    dims={k:min_k_90(v) for k,v in out.items()}

    null_ok=(not out['NULL_NOISE']['full_sig']) and dims['NULL_NOISE'] is None
    one_ok=dims['ONE_CAUSE_REDUNDANT']==1
    four_ok=dims['FOUR_CAUSES'] is not None and dims['FOUR_CAUSES']>=3
    nuisance_ok=dims['NUISANCE_RICH']==1
    xor_ok=dims['SYNERGY_XOR'] is not None and out['SYNERGY_XOR']['rows'][dims['SYNERGY_XOR']-1][1]>0.5

    print('\n'+'-'*78)
    print('PREDECLARED T4.0b SUMMARY')
    print('-'*78)
    for k,v in dims.items(): print(f'{k:20s} min_code_bits_for_90pct={v} full_sig={out[k]["full_sig"]}')
    print('NULL_NOISE permutation-null pass:',null_ok)
    print('ONE_CAUSE_REDUNDANT pass:',one_ok)
    print('FOUR_CAUSES pass:',four_ok)
    print('NUISANCE_RICH pass:',nuisance_ok)
    print('SYNERGY_XOR pass:',xor_ok)

    verdict='T4_INSTRUMENT_VALIDATED_ON_PREREGISTERED_SYNTHETICS' if all([null_ok,one_ok,four_ok,nuisance_ok,xor_ok]) else 'T4_0B_INSTRUMENT_NOT_VALIDATED'
    print('\nPREDECLARED T4.0b VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- A pass validates only this synthetic predictive-compression instrument.')
    print('- It does not validate Canevas, observer theory, consciousness, or emergent locality.')
    print('- T4.0 remains historically failed; T4.0b is a separately labelled correction.')
    print('- A pass permits only a separately preregistered T4.1 network experiment.')
    print('- A failure cannot be repaired under the T4.0b label.')
    print('\nFINISHED T4.0b')

if __name__=='__main__': run()
