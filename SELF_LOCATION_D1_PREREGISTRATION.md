# SELF-LOCATION D1 — Finite Human Birth Distribution

Status: PREREGISTERED BEFORE D1 OUTPUT

## Origin of the hypothesis
This branch formalizes an intuition stated independently of the present computation: if a human observer is approximately typical by cumulative birth-rank within a finite Homo sapiens birth distribution, then a birth occurring during the modern demographic transition may lie near an interior quantile of the eventual total distribution rather than arbitrarily close to its beginning or end.

This is NOT a derivation from Canevas and NOT evidence for Canevas unless a separate observer measure is independently justified.

## Fixed observed datum
Birth year: 1992.

The approximate mid-1992 cumulative birth rank is reconstructed from the same historical procedure already used in self_location_full_history_v1.py:
- PRB cumulative births by 1950 = 107,901,175,171
- UN WPP/OWID annual births from 1950 onward
- mid-year rank uses half of 1992 births.

The 1992 rank is not used to construct any future demographic trajectory.

## Independent demographic input
Use UN World Population Prospects 2024 annual world births through 2100 as distributed by Our World in Data. The UN projection is external to the self-location hypothesis.

Beyond 2100, D1 evaluates a predeclared tail ensemble anchored to the UN-projected 2100 annual birth rate. No tail parameter may be selected because it makes 1992 look typical.

## Predeclared post-2100 tail families
A. EXTINCTION_2100: zero births after 2100.
B. EXP_DECAY_5PCT: annual births decline exponentially at 5%/yr.
C. EXP_DECAY_2PCT: decline at 2%/yr.
D. EXP_DECAY_1PCT: decline at 1%/yr.
E. EXP_DECAY_0P5PCT: decline at 0.5%/yr.
F. EXP_DECAY_0P25PCT: decline at 0.25%/yr.
G. PLATEAU_1000Y: 2100 birth rate held constant for 1000 years, then zero.
H. PLATEAU_10000Y: held constant for 10,000 years, then zero.
I. INDEFINITE_PLATEAU: constant forever; total births diverge.

These are sensitivity models, not forecasts.

## Quantities reported for every finite scenario
Let r be mid-1992 cumulative birth rank and N_total the total births implied by the scenario.

q = r / N_total

Report:
- total future births after mid-1992;
- N_total;
- q, the eventual birth-rank quantile of mid-1992;
- distance from the median, |q-0.5|;
- whether q lies in broad predeclared central bands [0.25,0.75], [0.10,0.90], and [0.05,0.95];
- calendar year at which cumulative births reach 2r, when such a year exists under that scenario.

The 2r crossing is a diagnostic corresponding to the exact-median hypothesis q=0.5. It must NOT be used to choose a preferred scenario.

## Self-location likelihood models
D1 reports but does not endorse two toy likelihoods:

1. SSA-like rank likelihood for a fixed total N:
   L_SSA(r | N) = 1/N for 1 <= r <= N.

2. Simple SIA+SSA toy weighting:
   prior observer-number factor proportional to N times SSA 1/N, yielding a constant factor across N before any additional prior.

These illustrate measure dependence. D1 must explicitly state that the data cannot select a Doomsday conclusion without a prior over N and a justified reference class / observer measure.

## Primary empirical question
Do independently constructed finite demographic scenarios place mid-1992 robustly in an interior quantile of the eventual cumulative birth distribution?

## Predeclared qualitative reading
- ROBUST_INTERIOR: every finite scenario places q in [0.10,0.90], and at least 75% place q in [0.25,0.75].
- SENSITIVE_TO_TAIL: at least one finite scenario is central and at least one lies outside [0.10,0.90].
- GENERALLY_NONCENTRAL: fewer than 25% of finite scenarios place q in [0.25,0.75].
- INTERMEDIATE: otherwise.

This verdict concerns robustness across this scenario ensemble only. It is not a p-value and is not evidence for Canevas by itself.

## Interpretation lock
- Population peak is not the same thing as the median of cumulative births.
- The result is about births, not contemporaneous population size.
- Prehistoric birth totals are highly uncertain; PRB is an approximate reconstruction.
- The tail after 2100 dominates long-horizon conclusions and is not empirically known.
- A finite total human birth distribution is itself an assumption in finite scenarios, not an observed fact.
- SSA, SIA, reference class, and observer measure remain unresolved.
- No extinction date may be advertised as a prediction unless it follows from a separately justified demographic model and self-location rule.
