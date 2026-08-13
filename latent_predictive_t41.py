"""CANEVAS T4.1 — preregistered network predictive-compression experiment.

Run only after T4.0b synthetic validation. See T4_1_PREREGISTRATION.md.
This tests a narrow association in Boolean-network ensembles, not consciousness.
"""
from __future__ import annotations
import csv, math, random
from collections import defaultdict
import numpy as np

SEED=441017
RNG=np.random.default_rng(SEED); random.seed(SEED)
N=24; SUBSYSTEM_SIZE=4; NETWORKS_PER_FAMILY=20; SUBSYSTEMS_PER_NETWORK=8
BURN_IN=100; STEPS=600; PERTURB_STEPS=40
TRAIN_FRAC=.40; CAL_FRAC=.30; N_NULL=50; ALPHA=.05
MAX_PARENTS=8; MAX_CODE_BITS=4; RETAIN_TARGET=.90
FAMILIES=['sparse_random','dense_random','modular','local_ring','global_majority','hierarchical']


def enc(a):
    a=np.asarray(a,dtype=np.uint8)
    if a.ndim==1:a=a[:,None]
    return (a.astype(np.uint64)*(1<<np.arange(a.shape[1],dtype=np.uint64))).sum(1)

def H(y):
    if len(y)==0:return 0.0
    _,c=np.unique(y,return_counts=True); p=c/c.sum(); return float(-(p*np.log2(p)).sum())

def Hc(y,x):
    d=defaultdict(list)
    for xx,yy in zip(np.asarray(x).tolist(),np.asarray(y).tolist()):d[xx].append(yy)
    n=len(y); return float(sum(len(v)/n*H(np.asarray(v)) for v in d.values()))

def rankdata(a):
    a=np.asarray(a,float); o=np.argsort(a,kind='mergesort'); r=np.empty(len(a),float); i=0
    while i<len(a):
        j=i
        while j+1<len(a) and a[o[j+1]]==a[o[i]]:j+=1
        r[o[i:j+1]]=0.5*(i+j)+1; i=j+1
    return r

def spearman(x,y):
    if len(x)<3:return float('nan')
    x=rankdata(x); y=rankdata(y)
    if np.std(x)==0 or np.std(y)==0:return float('nan')
    return float(np.corrcoef(x,y)[0,1])

def gain_labels(S0,S1,Z,idx):
    s0=enc(S0[idx]); s1=enc(S1[idx]); base=Hc(s1,s0)
    if Z is None or Z.shape[1]==0:return 0.0
    z=enc(Z[idx]); joint=s0+(z<<S0.shape[1]); return base-Hc(s1,joint)

def full_gain(S0,S1,E,idx):return gain_labels(S0,S1,E,idx)

class BooleanNet:
    def __init__(self,fam):self.fam=fam;self.inputs=[];self.tables=[];self.rule='tables';self.build()
    def rin(self,k,pool=None):
        p=list(range(N)) if pool is None else list(dict.fromkeys(pool))
        if len(p)<k:p=list(range(N))
        return np.array(RNG.choice(p,size=k,replace=False),int)
    def add(self,ins):
        ins=np.array(ins,int);self.inputs.append(ins);self.tables.append(RNG.integers(0,2,size=1<<len(ins),dtype=np.uint8))
    def build(self):
        if self.fam=='global_majority':self.rule='global_majority';return
        for i in range(N):
            if self.fam=='sparse_random':ins=self.rin(2)
            elif self.fam=='dense_random':ins=self.rin(8)
            elif self.fam=='modular':
                b=(i//6)*6;local=list(range(b,b+6));ins=self.rin(3,local if RNG.random()<.85 else None)
            elif self.fam=='local_ring':ins=self.rin(3,[(i+d)%N for d in (-2,-1,0,1,2)])
            elif self.fam=='hierarchical':
                b=(i//6)*6;local=list(range(b,b+6));a=list(self.rin(2,local));hubs=[0,6,12,18]
                ext=int(RNG.choice([h for h in hubs if h!=b])) if RNG.random()<.35 else int(RNG.choice(local));ins=a+[ext]
            else:raise ValueError(self.fam)
            self.add(ins)
    def step(self,x):
        x=np.asarray(x,dtype=np.uint8)
        if self.rule=='global_majority':
            s=int(x.sum());maj=1 if s>N/2 else 0
            if s==N/2:maj=int(x[0])
            return np.array([maj^(i&1) for i in range(N)],dtype=np.uint8)
        out=np.empty(N,dtype=np.uint8)
        for i,(ins,tab) in enumerate(zip(self.inputs,self.tables)):
            out[i]=tab[int(np.dot(x[ins],1<<np.arange(len(ins))))]
        return out
    def traj(self,steps):
        x=RNG.integers(0,2,N,dtype=np.uint8);tr=np.empty((steps,N),dtype=np.uint8)
        for t in range(steps):tr[t]=x;x=self.step(x)
        return tr
    def extparents(self,sub):
        ss=set(sub)
        if self.rule=='global_majority':return [i for i in range(N) if i not in ss]
        p=set()
        for j in sub:p.update(int(k) for k in self.inputs[j] if int(k) not in ss)
        return sorted(p)

def choose_sub(fam):
    if fam in ('modular','hierarchical'):
        b=int(RNG.integers(0,4))*6;return sorted(RNG.choice(np.arange(b,b+6),SUBSYSTEM_SIZE,replace=False).tolist())
    if fam=='local_ring':
        s=int(RNG.integers(0,N));return sorted([(s+i)%N for i in range(SUBSYSTEM_SIZE)])
    return sorted(RNG.choice(np.arange(N),SUBSYSTEM_SIZE,replace=False).tolist())

def memory_score(tr,sub):
    a=enc(tr[:-1,sub]);b=enc(tr[1:,sub]);h=H(b)
    return 0.0 if h<1e-9 else max(0.0,min(1.0,(h-Hc(b,a))/h))
def persistence_score(tr,sub):
    x=tr[:,sub].astype(float);activity=float(np.mean(np.var(x,axis=0)*4));retain=float(np.mean(tr[1:,sub]==tr[:-1,sub]));temporal=abs(retain-.5)*2
    return max(0.0,min(1.0,activity*(.5+.5*temporal)))
def robustness(net,state,sub):
    outside=[i for i in range(N) if i not in sub];vals=[]
    for _ in range(6):
        x=state.copy();y=state.copy();j=int(RNG.choice(outside));y[j]^=1
        for _ in range(PERTURB_STEPS):x=net.step(x);y=net.step(y)
        vals.append(float(np.mean(x[sub]==y[sub])))
    return float(np.mean(vals))
def gmean(vals,eps=1e-6):return float(math.exp(sum(math.log(max(eps,min(1,float(v)))) for v in vals)/len(vals)))

def split_indices(m):
    idx=RNG.permutation(m);a=int(TRAIN_FRAC*m);b=int((TRAIN_FRAC+CAL_FRAC)*m);return idx[:a],idx[a:b],idx[b:]

def select_parents_train(S0,S1,E,parent_ids,tr):
    if E.shape[1]<=MAX_PARENTS:return E,parent_ids
    scores=[(full_gain(S0,S1,E[:,j:j+1],tr),j) for j in range(E.shape[1])]
    keep=[j for _,j in sorted(scores,reverse=True)[:MAX_PARENTS]]
    return E[:,keep],[parent_ids[j] for j in keep]

def candidate_atoms(E):
    import itertools
    m=E.shape[1];atoms=[];names=[]
    for j in range(m):atoms.append(E[:,j]);names.append(f'x{j}')
    for r in range(2,min(4,m)+1):
        for sub in itertools.combinations(range(m),r):atoms.append(np.bitwise_xor.reduce(E[:,sub],axis=1));names.append('xor'+str(sub))
    for r in range(3,m+1):
        for sub in itertools.combinations(range(m),r):atoms.append((E[:,sub].sum(1)>=(r+1)//2).astype(np.uint8));names.append('maj'+str(sub))
    return atoms,names

def build_code_curve(S0,S1,E,tr):
    atoms,names=candidate_atoms(E)
    if not atoms:return []
    # Train-only greedy forward code construction. XOR/majority synergy can appear as a single atom.
    chosen=[];remaining=list(range(len(atoms)));curve=[];current=0.0
    for k in range(1,MAX_CODE_BITS+1):
        best=None
        for i in remaining:
            inds=chosen+[i];Z=np.column_stack([atoms[q] for q in inds]);g=gain_labels(S0,S1,Z,tr)
            if best is None or g>best[0]:best=(g,i,Z)
        if best is None:break
        current,i,Z=best;chosen.append(i);remaining.remove(i);curve.append((k,Z,[names[q] for q in chosen]))
    return curve

def perm_p_full(S0,S1,E,cal,obs):
    vals=[];baseE=E.copy()
    for _ in range(N_NULL):
        P=baseE.copy()
        for j in range(P.shape[1]):P[:,j]=P[RNG.permutation(len(P)),j]
        vals.append(full_gain(S0,S1,P,cal))
    vals=np.asarray(vals);p=(1+np.sum(vals>=obs))/(N_NULL+1);q=float(np.quantile(vals,.95))
    return float(p),q

def perm_p_code(S0,S1,Z,cal,obs):
    vals=[]
    for _ in range(N_NULL):
        P=Z.copy()
        for j in range(P.shape[1]):P[:,j]=P[RNG.permutation(len(P)),j]
        vals.append(gain_labels(S0,S1,P,cal))
    vals=np.asarray(vals);p=(1+np.sum(vals>=obs))/(N_NULL+1);q=float(np.quantile(vals,.95))
    return float(p),q

def compression_measure(tr,sub,parent_ids):
    if len(parent_ids)==0:return {'valid':False,'full_gain':0.0,'k':None,'ratio':None,'parents_raw':0,'parents_used':0}
    S0=tr[:-1,sub];S1=tr[1:,sub];E=tr[:-1,parent_ids];m=len(S0);tridx,calidx,teidx=split_indices(m)
    E,parent_ids=select_parents_train(S0,S1,E,parent_ids,tridx)
    fcal=full_gain(S0,S1,E,calidx);fp,q=perm_p_full(S0,S1,E,calidx,fcal);ftest=full_gain(S0,S1,E,teidx)
    full_sig=(fp<=ALPHA and fcal>q and fcal>0 and ftest>0)
    if not full_sig:return {'valid':False,'full_gain':ftest,'k':None,'ratio':None,'parents_raw':len(parent_ids),'parents_used':E.shape[1]}
    curve=build_code_curve(S0,S1,E,tridx);chosen_k=None
    for k,Z,names in curve:
        ccal=gain_labels(S0,S1,Z,calidx);cp,cq=perm_p_code(S0,S1,Z,calidx,ccal);ctest=gain_labels(S0,S1,Z,teidx)
        sig=(cp<=ALPHA and ccal>cq and ccal>0)
        if sig and ctest>=RETAIN_TARGET*ftest:
            chosen_k=k;break
    if chosen_k is None:chosen_k=MAX_CODE_BITS+1
    denom=max(1,min(MAX_PARENTS,E.shape[1]));ratio=chosen_k/denom
    return {'valid':True,'full_gain':ftest,'k':chosen_k,'ratio':ratio,'parents_raw':len(parent_ids),'parents_used':E.shape[1]}

def run():
    print('='*78);print('CANEVAS T4.1 — NETWORK PREDICTIVE-COMPRESSION EXPERIMENT');print('='*78)
    print('seed=',SEED,'networks/family=',NETWORKS_PER_FAMILY,'subsystems/network=',SUBSYSTEMS_PER_NETWORK)
    print('train/cal/test=',TRAIN_FRAC,CAL_FRAC,1-TRAIN_FRAC-CAL_FRAC,'null perms=',N_NULL,'alpha=',ALPHA)
    print('Primary prediction: within-family SUPPORT vs COMPRESSION_RATIO is NEGATIVE.\n')
    rows=[];done=0;total=len(FAMILIES)*NETWORKS_PER_FAMILY
    for fam in FAMILIES:
        for ni in range(NETWORKS_PER_FAMILY):
            net=BooleanNet(fam);full=net.traj(BURN_IN+STEPS+1);tr=full[BURN_IN:]
            for si in range(SUBSYSTEMS_PER_NETWORK):
                sub=choose_sub(fam);parents=net.extparents(sub)
                mem=memory_score(tr,sub);per=persistence_score(tr,sub);rob=robustness(net,tr[-1].copy(),sub);sup=gmean([mem,per,rob])
                cm=compression_measure(tr,sub,parents)
                rows.append({'family':fam,'support':sup,'memory':mem,'persistence':per,'robustness':rob,'structural_parents':len(parents),**cm})
            done+=1
            if done%10==0 or done==total:print(f'progress {done}/{total} networks')
    with open('t41_results.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
    print('\nPRIMARY WITHIN-FAMILY RESULT')
    rhos=[];evaluable=[]
    for fam in FAMILIES:
        rr=[r for r in rows if r['family']==fam and r['valid']]
        rho=spearman([r['support'] for r in rr],[r['ratio'] for r in rr]) if len(rr)>=3 else float('nan')
        ks=[r['k'] for r in rr];rat=[r['ratio'] for r in rr]
        print(f'{fam:18s} valid={len(rr):3d} rho={rho:+.4f} ratio_med={np.median(rat) if rat else float("nan"):.3f} k_med={np.median(ks) if ks else float("nan"):.2f}')
        if len(rr)>=30 and not np.isnan(rho):evaluable.append((fam,rho));rhos.append(rho)
    neg=sum(r<0 for r in rhos);frac=neg/len(rhos) if rhos else float('nan');med=float(np.median(rhos)) if rhos else float('nan')
    print(f'evaluable families = {len(rhos)}; negative = {neg}; negative_fraction = {frac:.3f}')
    print(f'median within-family rho = {med:+.4f}')
    print('\nSECONDARY')
    for fam in FAMILIES:
        allr=[r for r in rows if r['family']==fam];valid=[r for r in allr if r['valid']]
        no=1-len(valid)/len(allr)
        rg=spearman([r['support'] for r in valid],[r['full_gain'] for r in valid]) if len(valid)>=3 else float('nan')
        rs=spearman([r['support'] for r in allr],[r['structural_parents'] for r in allr])
        print(f'{fam:18s} no_predictive_env={no:.3f} rho_support_fullgain={rg:+.3f} rho_support_structparents={rs:+.3f}')
    if len(rhos)>=4 and frac>=.75 and med<=-.20:verdict='SUPPORTS_T4_COMPRESSION_ASSOCIATION'
    elif len(rhos)>=4 and (frac<=.25 or med>=.20):verdict='EVIDENCE_AGAINST_T4_COMPRESSION_ASSOCIATION'
    else:verdict='INCONCLUSIVE_T4_1'
    print('\nPREDECLARED T4.1 VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- This concerns information-processing proxies in these Boolean-network ensembles, not consciousness.')
    print('- Do not alter family weights, 90% retention, k range, support formula, or evaluability threshold after this run.')
    print('- A positive result does not establish emergent locality, anthropic selection, observer measure, or Canevas cosmology.')
    print('- Raw per-subsystem results saved to t41_results.csv.')
    print('\nFINISHED T4.1')
if __name__=='__main__':run()
