"""CANEVAS 2.0 P1.2 — EXACT ADDITIVITY THEOREM ATTEMPT v1

PREREGISTERED BEFORE OUTPUT.

Purpose
-------
P1.1 showed that A1-A6 do not uniquely determine DURATION_SUPPORT because
non-additive counterexamples survive. P1.2 introduces one separately motivated
stronger axiom:

A3*: exact additivity for physically disjoint event collections:
    M(H union K) = M(H) + M(K)
for disjoint H,K.

Question
--------
Given A3* together with coarse-graining consistency in duration and linear
homogeneity in support, is a single-token measure forced to be proportional to
    m(d,s) = d*s
and therefore total measure proportional to sum_i d_i s_i?

This is a mathematical identifiability test, not evidence about nature. The test
must not use observed self-location data, zeta, birth rank, or desired empirical
outputs.
"""
import math

TOL=1e-10

def close(a,b):
    return abs(a-b) <= TOL*max(1.0,abs(a),abs(b))

# Candidate single-token kernels declared before output.
# Total history measure is exactly additive by construction: sum kernel(d,s).
def k_ds(d,s): return d*s
def k_s(d,s): return s
def k_d2s(d,s): return d*d*s
def k_sqrt_ds(d,s): return math.sqrt(d)*s
def k_log_ds(d,s): return math.log1p(d)*s
def k_ds2(d,s): return d*s*s

KERNELS={
    'DURATION_SUPPORT':k_ds,
    'SUPPORT_ONLY':k_s,
    'DURATION2_SUPPORT':k_d2s,
    'SQRT_DURATION_SUPPORT':k_sqrt_ds,
    'LOG1P_DURATION_SUPPORT':k_log_ds,
    'DURATION_SUPPORT2':k_ds2,
}

# Dense positive audit grids.
D=[0.125,0.25,0.5,1.0,1.5,2.0,3.0,5.0]
S=[0.2,0.5,1.0,2.0,4.0]
C=[0.25,0.5,2.0,3.7]

# Axioms / functional equations checked at the single-token level once exact
# disjoint additivity has reduced total measure to a sum of token kernels.
def check_kernel(f):
    # positivity
    A1=all(f(d,s)>=-TOL for d in D for s in S)
    # duration subdivision: m(d1+d2,s)=m(d1,s)+m(d2,s)
    A5=True
    for d1 in D:
        for d2 in D:
            for s in S:
                if not close(f(d1+d2,s),f(d1,s)+f(d2,s)):
                    A5=False; break
            if not A5: break
        if not A5: break
    # support homogeneity: m(d,c*s)=c*m(d,s)
    A6=True
    for d in D:
        for s in S:
            for c in C:
                if not close(f(d,c*s),c*f(d,s)):
                    A6=False; break
            if not A6: break
        if not A6: break
    # clone distinction follows from exact additivity and positivity for nonzero token.
    A4=all((f(d,s)+f(d,s)) > f(d,s)+TOL for d in D for s in S if f(d,s)>TOL)
    return {'A1':A1,'A3_exact':True,'A4':A4,'A5':A5,'A6':A6}

print('='*84)
print('CANEVAS 2.0 P1.2 — EXACT ADDITIVITY THEOREM ATTEMPT v1')
print('='*84)
print('No observed self-location data are used. A3* exact additivity is the only new axiom.\n')

survivors=[]
for name,f in KERNELS.items():
    r=check_kernel(f); ok=all(r.values())
    if ok: survivors.append(name)
    print(f'{name:28s} '+' '.join(f'{k}={v}' for k,v in r.items())+f' survivor={ok}')

# Numerical functional-equation derivation check:
# For any surviving kernel, ratio m(d,s)/(d*s) should be constant over audit grid.
def proportional_to_ds(f):
    ratios=[f(d,s)/(d*s) for d in D for s in S if d*s>0]
    return max(ratios)-min(ratios) <= 1e-9*max(1.0,max(map(abs,ratios)))

prop={name:proportional_to_ds(KERNELS[name]) for name in survivors}
all_prop=bool(survivors) and all(prop.values())

# Analytic derivation flags. These are logic checks of the declared assumptions,
# not computer-discovered theorems:
# exact additivity -> total=sum single-token m
# duration subdivision + regularity/positivity -> additive positive function in d,
# hence linear in d on R_+
# support homogeneity -> linear in s
# therefore m(d,s)=C*d*s.
# We explicitly note the regularity role: positivity excludes pathological Cauchy
# solutions on positive reals for the additive duration dependence.
analytic_steps={
    'exact_additivity_reduces_to_token_kernel':True,
    'positive_duration_additivity_implies_linear_duration':True,
    'support_homogeneity_implies_linear_support':True,
    'combined_form_C_times_d_times_s':True,
}

print('\nP1.2 SUMMARY')
print(f'n_candidate_kernels = {len(KERNELS)}')
print(f'survivors = {survivors}')
print(f'survivor_proportional_to_duration_support = {prop}')
print(f'all_survivors_proportional_to_duration_support = {all_prop}')
for k,v in analytic_steps.items(): print(f'{k} = {v}')

if all_prop and all(analytic_steps.values()):
    verdict='EXACT_ADDITIVITY_PLUS_SUBDIVISION_AND_SUPPORT_HOMOGENEITY_FORCE_DURATION_SUPPORT_UP_TO_SCALE'
else:
    verdict='DECLARED_AXIOMS_DO_NOT_YET_FORCE_DURATION_SUPPORT'
print(f'P1.2 PREDECLARED VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- P1.2 is a theorem attempt conditional on A3* exact disjoint additivity and the other declared axioms.')
print('- It does not prove that nature or Canevas must satisfy exact additivity.')
print('- The key scientific question shifts to whether exact additivity is independently justified by the ontology, not whether it is mathematically convenient.')
print('- If P1.2 passes, DURATION_SUPPORT is unique only up to an overall multiplicative constant within this additive token ontology.')
print('- No observed rank, zeta, epoch, or desired prediction may be used to justify A3* retroactively.')
print('- A later P1.3 must stress-test the physical motivation for A3* against interactions, overlapping supports, and non-separable histories before the measure is used predictively.')
print('\nFINISHED C2-P1.2 — DO NOT RETUNE AFTER OUTPUT')
