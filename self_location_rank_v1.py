"""Canevas self-location rank test v1.

This script tests the rank part of the preregistered self-location module.
It deliberately avoids any empirical demographic inputs. Future scenarios are
expressed only as F = N_total / R_now, so the absolute present rank cancels.

Interpretation guardrail:
- SSA produces a 1/F likelihood penalty for large futures.
- simple SIA weighting multiplies by F and cancels that penalty.
- therefore Doomsday pressure is not a consequence of the Canevas axioms alone.
"""
from pathlib import Path
import csv
import numpy as np

OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
F=np.array([1.1,2.0,10.0,1e3,1e6,1e12],float)
labels=['F1','F2','F3','F4','F5','F6']

# Relative likelihoods. Constants involving current rank cancel.
L_ssa=1/F
L_sia_ssa=F*(1/F)

# Normalize only for display under an explicitly equal discrete prior over the
# six stress-test scenarios. These are NOT physical posterior probabilities.
P_ssa=L_ssa/L_ssa.sum()
P_sia=L_sia_ssa/L_sia_ssa.sum()

# Bayes factors relative to the smallest tested future.
BF_ssa=L_ssa/L_ssa[0]
BF_sia=L_sia_ssa/L_sia_ssa[0]

rows=[]
for lab,f,l1,l2,p1,p2,b1,b2 in zip(labels,F,L_ssa,L_sia_ssa,P_ssa,P_sia,BF_ssa,BF_sia):
    rows.append((lab,f,l1,l2,p1,p2,b1,b2))

with (OUT/'self_location_rank_v1.csv').open('w',newline='',encoding='utf8') as fp:
    w=csv.writer(fp)
    w.writerow(['scenario','F_Ntotal_over_Rnow','SSA_likelihood_relative','SIAxSSA_likelihood_relative','SSA_display_posterior_equal_scenario_prior','SIAxSSA_display_posterior_equal_scenario_prior','SSA_BF_vs_F1','SIAxSSA_BF_vs_F1'])
    w.writerows(rows)

lines=[
'CANEVAS SELF-LOCATION RANK TEST v1',
'==================================',
'No demographic data used. F = total future reference-class count / current cumulative rank scale.',
'',
'Under SSA: likelihood is proportional to 1/F.',
'Under simple SIA+SSA: SIA contributes F, cancelling 1/F, so likelihood is constant.',
'',
'SCENARIO RESULTS:'
]
for r in rows:
    lab,f,l1,l2,p1,p2,b1,b2=r
    lines.append(f'{lab}: F={f:.3g} | SSA BF vs F1={b1:.6g} | SIA+SSA BF vs F1={b2:.6g}')
lines += [
'',
'INTERPRETATION:',
'- SSA alone heavily favors futures with fewer total observers.',
'- Simple SIA+SSA removes that preference exactly in this toy setup.',
'- Therefore a Doomsday conclusion is measure-dependent unless Canevas independently derives a self-location rule.',
'- Equal-scenario-prior normalized numbers in the CSV are illustrations only, not forecasts.',
'',
'PREDECLARED VERDICT = SELF_LOCATION_RULE_DEPENDENT',
]
text='\n'.join(lines)+'\n'
(OUT/'self_location_rank_v1_summary.txt').write_text(text,encoding='utf8')
print(text)
