"""CANEVAS SELF-LOCATION D2 — HUMAN FUTURE POSTERIOR v1

Predeclared before observing D2 output.
Purpose: quantify how an observed human birth rank updates hypotheses about the
TOTAL number of human births, while making the self-location rule explicit.

IMPORTANT: this is a self-location/anthropic diagnostic, not an extinction
forecast and not evidence for Canevas cosmology by itself.

Frozen inputs/rules:
- observed mid-1992 cumulative birth rank r = 112,980,038,356 (from O1/D1.1)
- N_total is sampled on a log grid from r to 1e20 births
- three deliberately different priors over N:
    P1 log-uniform: p(N) proportional 1/N
    P2 uniform-N:   p(N) constant
    P3 lognormal centered 1e12 births, sigma=2 natural-log units
- likelihood rules:
    SSA: p(r|N)=1/N for N>=r
    simple SIA+SSA: p(r|N) proportional constant for N>=r
- no prior/range/threshold may be changed after seeing v1.

The code reports posterior quantiles for N_total and remaining births, plus the
probability that the observed rank lies in central 50% / central 80% of the
complete birth distribution. Mapping births to calendar years is intentionally
NOT attempted in D2 because it requires an independent future demographic model.
"""
import math
import numpy as np

R = 112_980_038_356.0
NMAX = 1e20
GRID_N = 200_000
LN_CENTER = math.log(1e12)
LN_SIGMA = 2.0

# Work in x=ln N. Numerical integration is over dx, so density in x includes
# Jacobian N relative to a density defined over N.
x = np.linspace(math.log(R), math.log(NMAX), GRID_N)
N = np.exp(x)
dx = x[1]-x[0]


def normalize(w):
    z = np.trapezoid(w, x)
    if not np.isfinite(z) or z <= 0:
        raise RuntimeError('invalid normalization')
    return w/z


def quantile_from_density(w, probs):
    c = np.cumsum(w)*dx
    c /= c[-1]
    return [float(N[min(np.searchsorted(c,p),len(N)-1)]) for p in probs]


def prior_x(name):
    # Return density with respect to x=ln N.
    if name == 'LOG_UNIFORM':
        # p_N(N)~1/N; multiply Jacobian N => constant in log-space.
        return np.ones_like(N)
    if name == 'UNIFORM_N':
        # p_N(N)=const; Jacobian => N.
        return N.copy()
    if name == 'LOGNORMAL_1E12_SIGMA2':
        return np.exp(-0.5*((x-LN_CENTER)/LN_SIGMA)**2)
    raise ValueError(name)


def likelihood(rule):
    if rule == 'SSA':
        return 1.0/N
    if rule == 'SIA_SSA':
        return np.ones_like(N)
    raise ValueError(rule)


def fmt(v):
    if v < 1e12: return f'{v/1e9:.3f} billion'
    if v < 1e15: return f'{v/1e12:.3f} trillion'
    return f'{v:.4e}'


def main():
    print('='*86)
    print('CANEVAS SELF-LOCATION D2 — HUMAN FUTURE POSTERIOR v1')
    print('='*86)
    print(f'observed birth rank r = {R:,.0f}')
    print(f'N domain = [{R:.6e}, {NMAX:.6e}] births; grid={GRID_N}')
    print('No calendar extinction year is inferred in D2.')
    print()

    combos=[]
    for pname in ['LOG_UNIFORM','UNIFORM_N','LOGNORMAL_1E12_SIGMA2']:
        px=normalize(prior_x(pname))
        for rule in ['SSA','SIA_SSA']:
            post=normalize(px*likelihood(rule))
            q025,q10,q25,q50,q75,q90,q975=quantile_from_density(post,[.025,.10,.25,.50,.75,.90,.975])
            # For fixed observed r, central-50 typicality means q=r/N in [.25,.75].
            # central-80 means q in [.10,.90].
            qobs=R/N
            p_c50=float(np.trapezoid(post*((qobs>=.25)&(qobs<=.75)),x))
            p_c80=float(np.trapezoid(post*((qobs>=.10)&(qobs<=.90)),x))
            p_q45_55=float(np.trapezoid(post*((qobs>=.45)&(qobs<=.55)),x))
            rem50=max(0.0,q50-R)
            combos.append((pname,rule,q50,p_c50,p_c80,p_q45_55))
            print(f'[{pname} + {rule}]')
            print(f' posterior N 2.5/10/25/50/75/90/97.5% =')
            print('   '+' | '.join(fmt(v) for v in [q025,q10,q25,q50,q75,q90,q975]))
            print(f' posterior median remaining births = {fmt(rem50)}')
            print(f' P(observed rank in central 50%) = {p_c50:.4f}')
            print(f' P(observed rank in central 80%) = {p_c80:.4f}')
            print(f' P(observed quantile in [0.45,0.55]) = {p_q45_55:.4f}')
            print()

    print('PREDECLARED D2 INTERPRETATION')
    print('- If posterior scale changes strongly across priors/rules: SELF_LOCATION_MODEL_DEPENDENT.')
    print('- If SSA consistently shifts N downward relative to matched SIA+SSA: SSA_DOOMSDAY_SHIFT_PRESENT.')
    print('- Exact median proximity is not predicted by ordinary uniform-rank typicality.')
    print('- A typical observer is more likely to be in a broad central interval than an extreme tail,')
    print('  but the exact 50th percentile has no special density under uniform rank.')
    print('- No posterior here may be translated into an extinction year without a separately')
    print('  preregistered demographic mapping from future births to calendar time.')

    # Mechanical qualitative verdicts, frozen before output.
    medians=[c[2] for c in combos]
    spread=max(medians)/min(medians)
    verdict='SELF_LOCATION_MODEL_DEPENDENT' if spread>=10 else 'RELATIVELY_ROBUST_TO_RULE_AND_PRIOR'
    ssa_shift=True
    for pname in ['LOG_UNIFORM','UNIFORM_N','LOGNORMAL_1E12_SIGMA2']:
        a=next(c[2] for c in combos if c[0]==pname and c[1]=='SSA')
        b=next(c[2] for c in combos if c[0]==pname and c[1]=='SIA_SSA')
        if not a < b: ssa_shift=False
    print(f'posterior-median max/min spread = {spread:.4g}x')
    print('SSA downward shift in all matched priors =',ssa_shift)
    print('PREDECLARED D2 VERDICT =',verdict)
    print('PREDECLARED D2 SSA DIAGNOSTIC =', 'SSA_DOOMSDAY_SHIFT_PRESENT' if ssa_shift else 'SSA_SHIFT_NOT_UNIVERSAL')
    print('\nFINISHED D2 v1 — DO NOT RETUNE AFTER OUTPUT')

if __name__=='__main__':
    main()
