"""CANEVAS T4.2 — independent replication of SUPPORT vs environmental predictive gain.

Uses the T4.1 network machinery unchanged where possible, but a new seed and new
networks. See T4_2_PREREGISTRATION.md.
"""
from __future__ import annotations
import csv, random, math
import numpy as np
import latent_predictive_t41 as b

SEED=842021
RNG=np.random.default_rng(SEED)
random.seed(SEED)
# Repoint the imported module's RNG because its classes/functions read b.RNG globally.
b.RNG=RNG
b.random.seed(SEED)

NETWORKS_PER_FAMILY=24
SUBSYSTEMS_PER_NETWORK=8


def corr(x,y):
    return b.spearman(x,y)


def run():
    print('='*78)
    print('CANEVAS T4.2 — INDEPENDENT ENVIRONMENTAL-DEPENDENCE REPLICATION')
    print('='*78)
    print('seed=',SEED,'networks/family=',NETWORKS_PER_FAMILY,'subsystems/network=',SUBSYSTEMS_PER_NETWORK)
    print('Primary prediction: within-family SUPPORT vs FULL_ENVIRONMENT_HELDOUT_GAIN is NEGATIVE.')
    print('Replication threshold: >=75% negative and median rho <= -0.40, with >=4 evaluable families.\n')

    rows=[]; done=0; total=len(b.FAMILIES)*NETWORKS_PER_FAMILY
    for fam in b.FAMILIES:
        for ni in range(NETWORKS_PER_FAMILY):
            net=b.BooleanNet(fam)
            full=net.traj(b.BURN_IN+b.STEPS+1)
            tr=full[b.BURN_IN:]
            for si in range(SUBSYSTEMS_PER_NETWORK):
                sub=b.choose_sub(fam)
                parents=net.extparents(sub)
                mem=b.memory_score(tr,sub)
                per=b.persistence_score(tr,sub)
                rob=b.robustness(net,tr[-1].copy(),sub)
                sup=b.gmean([mem,per,rob])
                cm=b.compression_measure(tr,sub,parents)
                rows.append({'family':fam,'support':sup,'memory':mem,'persistence':per,'robustness':rob,
                             'structural_parents':len(parents),**cm})
            done+=1
            if done%12==0 or done==total:
                print(f'progress {done}/{total} networks')

    with open('t42_results.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    print('\nPRIMARY WITHIN-FAMILY RESULT')
    rhos=[]
    for fam in b.FAMILIES:
        rr=[r for r in rows if r['family']==fam and r['valid']]
        rho=corr([r['support'] for r in rr],[r['full_gain'] for r in rr]) if len(rr)>=3 else float('nan')
        print(f'{fam:18s} valid={len(rr):3d} rho_support_fullgain={rho:+.4f} '
              f'fullgain_med={np.median([r["full_gain"] for r in rr]) if rr else float("nan"):.4f} '
              f'support_med={np.median([r["support"] for r in rr]) if rr else float("nan"):.3f}')
        if len(rr)>=30 and not np.isnan(rho):
            rhos.append(rho)

    neg=sum(r<0 for r in rhos)
    frac=neg/len(rhos) if rhos else float('nan')
    med=float(np.median(rhos)) if rhos else float('nan')
    print(f'evaluable families = {len(rhos)}; negative = {neg}; negative_fraction = {frac:.3f}')
    print(f'median within-family rho = {med:+.4f}')

    print('\nSECONDARY DIAGNOSTICS')
    for fam in b.FAMILIES:
        rr=[r for r in rows if r['family']==fam and r['valid']]
        allr=[r for r in rows if r['family']==fam]
        if len(rr)>=3:
            rm=corr([r['support'] for r in rr],[r['memory'] for r in rr])
            rp=corr([r['support'] for r in rr],[r['persistence'] for r in rr])
            rrho=corr([r['support'] for r in rr],[r['robustness'] for r in rr])
            rratio=corr([r['support'] for r in rr],[r['ratio'] for r in rr]) if all(r['ratio'] is not None for r in rr) else float('nan')
        else:
            rm=rp=rrho=rratio=float('nan')
        rs=corr([r['support'] for r in allr],[r['structural_parents'] for r in allr]) if len(allr)>=3 else float('nan')
        print(f'{fam:18s} rho_mem={rm:+.3f} rho_persist={rp:+.3f} rho_robust={rrho:+.3f} '
              f'rho_structparents={rs:+.3f} rho_compression_ratio={rratio:+.3f}')

    if len(rhos)>=4 and frac>=.75 and med<=-.40:
        verdict='REPLICATES_NEGATIVE_ENVIRONMENTAL_DEPENDENCE'
    elif len(rhos)>=4 and (frac<=.25 or med>=-.10):
        verdict='EVIDENCE_AGAINST_NEGATIVE_ENVIRONMENTAL_DEPENDENCE'
    else:
        verdict='INCONCLUSIVE_T4_2'

    print('\nPREDECLARED T4.2 VERDICT =',verdict)
    print('\nINTERPRETATION LOCK:')
    print('- This is an independent replication of a post-hoc T4.1 pattern on new Boolean networks.')
    print('- A positive result would concern only these ensembles and these information-processing proxies.')
    print('- It does not establish consciousness, observerhood, emergent locality, anthropic selection, or Canevas cosmology.')
    print('- Secondary diagnostics cannot rescue the primary verdict.')
    print('- Raw results saved to t42_results.csv.')
    print('\nFINISHED T4.2')

if __name__=='__main__':
    run()
