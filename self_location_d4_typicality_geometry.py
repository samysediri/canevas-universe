"""CANEVAS SELF-LOCATION D4 — TYPICALITY GEOMETRY v1

PREDECLARED before observing D4 output.

Question:
Can broad 'typicality' itself force an observer near the exact median of a finite
reference class? D4 tests the geometry independently of Samy's observed rank,
calendar birth year, D2 posterior, and D3 demographic trajectories.

Frozen design:
- Work only with normalized rank q=r/N in (0,1).
- Candidate observer measures are declared ex ante:
  U: uniform rank (SSA conditional on fixed N)
  C2: symmetric center weighting proportional [q(1-q)]^2
  C8: stronger center weighting proportional [q(1-q)]^8
  E2: symmetric edge weighting proportional (|q-.5|+.02)^2
  EARLY: early-rank weighting proportional exp(-4q)
  LATE: late-rank weighting proportional exp(+4q)
- No candidate is claimed to follow from Canevas. They are countermodels.
- Metrics: central-50 mass, central-80 mass, exact-median-band [.45,.55],
  tail mass q<.01 or q>.99, expected |q-.5|, median q.
- Calibration identity: U should give central50=.5, central80=.8,
  median-band=.1, tails=.02, E|q-.5|=.25.
- Main logical criterion: if U passes calibration but does NOT privilege the
  exact median band beyond its width, then ordinary typicality alone does not
  derive 'near 50th percentile'.
- Any stronger central concentration requires an additional observer measure.

No empirical claim about consciousness, Canevas cosmology, extinction, or a
specific person's birth rank is licensed by this experiment.
"""
import numpy as np

SEED=440041
NMC=2_000_000
rng=np.random.default_rng(SEED)

# numerical grid for deterministic densities
q=np.linspace(1e-6,1-1e-6,400_001)


def norm(w):
    z=np.trapezoid(w,q)
    return w/z


def mass(w,a,b):
    m=(q>=a)&(q<=b)
    return float(np.trapezoid(w[m],q[m]))


def quantile(w,p):
    dq=q[1]-q[0]
    c=np.cumsum(w)*dq; c/=c[-1]
    return float(q[min(np.searchsorted(c,p),len(q)-1)])


def metrics(w):
    return {
      'central50':mass(w,.25,.75),
      'central80':mass(w,.10,.90),
      'medianband':mass(w,.45,.55),
      'tails01':mass(w,0,.01)+mass(w,.99,1),
      'mean_abs_center':float(np.trapezoid(w*np.abs(q-.5),q)),
      'median_q':quantile(w,.5),
    }

models={
 'U_UNIFORM':np.ones_like(q),
 'C2_CENTER':(q*(1-q))**2,
 'C8_CENTER':(q*(1-q))**8,
 'E2_EDGE':(np.abs(q-.5)+.02)**2,
 'EARLY':np.exp(-4*q),
 'LATE':np.exp(4*q),
}

print('='*82)
print('CANEVAS SELF-LOCATION D4 — TYPICALITY GEOMETRY v1')
print('='*82)
print('Independent of observed birth rank, birth year, D2, and D3.')
print('Candidate measures are countermodels; none is assumed to be Canevas.')
print()

out={}
for name,raw in models.items():
    w=norm(raw); m=metrics(w); out[name]=m
    print(f'[{name}]')
    for k,v in m.items(): print(f'  {k:16s} = {v:.6f}')
    print()

u=out['U_UNIFORM']
cal=(abs(u['central50']-.5)<2e-4 and abs(u['central80']-.8)<2e-4 and
     abs(u['medianband']-.1)<2e-4 and abs(u['tails01']-.02)<2e-4 and
     abs(u['mean_abs_center']-.25)<2e-4)

# Width of [.45,.55] is .10. Under uniform typicality its probability should
# simply be .10; exact center receives no special density.
uniform_exact_median_privilege = u['medianband'] > 0.1002

# Demonstrate that centrality can be produced, but only by changing measure.
strong_center_exists = out['C8_CENTER']['medianband'] > u['medianband']*2
measure_sensitivity=max(v['medianband'] for v in out.values())/min(v['medianband'] for v in out.values())

print('PREDECLARED D4 SUMMARY')
print('uniform calibration pass =',cal)
print('uniform exact-median privilege =',uniform_exact_median_privilege)
print('stronger median concentration exists under altered measure =',strong_center_exists)
print(f'median-band probability max/min across declared measures = {measure_sensitivity:.3f}x')

if not cal:
    verdict='INSTRUMENT_FAILURE'
elif uniform_exact_median_privilege:
    verdict='UNEXPECTED_UNIFORM_CENTER_PRIVILEGE'
elif strong_center_exists:
    verdict='TYPICALITY_DOES_NOT_DERIVE_EXACT_MEDIAN_MEASURE_REQUIRED'
else:
    verdict='TYPICALITY_NOT_EXACT_MEDIAN_NO_STRONG_COUNTERMODEL'
print('PREDECLARED D4 VERDICT =',verdict)
print()
print('INTERPRETATION LOCK:')
print('- Broad typicality can make extreme tails unlikely without privileging q=0.5.')
print('- Uniform rank predicts probability by interval width: [.45,.55] has mass 0.10.')
print('- A special attraction toward the median requires an extra measure/dynamics.')
print('- D4 cannot choose SSA vs SIA, cannot validate D2/D3, and cannot establish Canevas.')
print('- Any future Canevas observer measure must be derived independently, then tested')
print('  against these frozen countermodels; it may not be selected because it makes an')
print('  observed human rank look central.')
print('\nFINISHED D4 v1 — DO NOT RETUNE AFTER OUTPUT')
