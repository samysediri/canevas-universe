# Canevas 1.0 — Self-location test v1

## Status
Conceptual/statistical branch. This is NOT an axiom and NOT evidence for Canevas by itself.

## Question
Is the intuition "it is extraordinarily unlikely that I find myself alive now, in a very populous technological era" still surprising after conditioning correctly on observer selection? And separately: does our early rank among potentially all future observers support a Doomsday-like conclusion?

## Crucial separation
There are two different observations:

O1 — Calendar-time observation: I am an observer in a recent, populous, technological human era.
O2 — Rank observation: conditional on some reference class, my observer/birth rank is relatively early if civilization eventually creates vastly more observers.

O1 and O2 must never be conflated.

## Models to compare (declared before numerical results)

### M0 — Uniform calendar time (straw model)
P(t) constant over a chosen historical interval. Included only to expose the naive intuition. It is not a serious observer-sampling model.

### M1 — Birth sampling
P(t | human birth) proportional to B(t), the number of human births per unit time.
Prediction: populous eras receive much more probability mass than sparse eras.

### M2 — Observer-moment sampling
P(t | observer-moment) proportional to N(t) * L(t), where N is number of relevant observers and L is effective conscious-observer-moment production per observer. L=constant is the baseline; alternatives must be declared.

### M3 — Technological conditioning
P(t | technological observer) proportional to B(t) * q_tech(t), where q_tech is the probability that a birth yields an observer satisfying a predeclared technological/cognitive criterion. This model is explicitly conditional and cannot be used to claim that technology itself was predicted.

### M4 — SSA rank model
Given total reference-class population N_total and observed rank r, assume approximately uniform rank among 1..N_total:
P(r | N_total, SSA)=1/N_total for r<=N_total.
This generates a Doomsday-type likelihood penalty for extremely large N_total.

### M5 — SIA + SSA schematic model
Before conditioning on rank, worlds are weighted by the number of eligible observers N_total. With the simple SIA factor proportional to N_total, the 1/N_total SSA rank likelihood cancels. This demonstrates why Doomsday conclusions depend on the self-location rule and prior.

## Reference classes to stress-test
R1: Homo sapiens births.
R2: humans reaching conscious adulthood.
R3: technologically literate humans capable in principle of posing the present abstract question.
R4: observer-moments rather than persons.

No single reference class is privileged by the Canevas axioms at present.

## Predeclared future scenarios
Use dimensionless future totals relative to present cumulative reference-class count R_now:
F1 = 1.1 R_now
F2 = 2 R_now
F3 = 10 R_now
F4 = 10^3 R_now
F5 = 10^6 R_now
F6 = 10^12 R_now
These are stress-test scenarios, not forecasts.

## Tests

### Test A — Population-density correction
Compare the percentile of the present era under M0 versus M1. If the apparent improbability largely disappears under M1, the raw calendar-time intuition is selection-biased.

### Test B — Technology conditioning
Compare M1 and M3. If conditioning on the ability to formulate the question makes recent technological eras overwhelmingly likely, "why now, with technology?" is not independent evidence for Canevas.

### Test C — Doomsday rank likelihood
For each F scenario compute relative likelihood under M4:
L(F) proportional to 1/F (once current rank scale is factored out).
This is a likelihood only, not a posterior. A posterior requires a prior over future population.

### Test D — SIA cancellation
Repeat with M5. Under the simplest SIA weighting, L(F) becomes approximately constant. If the Doomsday effect disappears, record that the conclusion is measure-dependent.

### Test E — Reference-class robustness
Repeat the qualitative conclusion for R1-R4. If conclusions reverse with plausible reference classes, no unique Canevas prediction exists yet.

## Success/failure criteria

The user's original "too big a coincidence" intuition is SUPPORTED as a robust anomaly only if:
1. O1 remains strongly atypical after birth-density and technological conditioning; AND
2. O2 produces qualitatively similar pressure against enormous futures under multiple defensible self-location rules and reference classes.

It is PARTIALLY SUPPORTED if only O2 survives, in which case the relevant phenomenon is a Doomsday/self-location problem, not the mere coincidence of being born in a populous technological era.

It is NOT ROBUST if O1 disappears after conditioning and O2 reverses/cancels under reasonable SSA/SIA/reference-class choices.

## Relation to Canevas
A4 may motivate the existence of bounded/local observer states, which creates indexical uncertainty: multiple observer states may be physically possible while an experience is locally one of them. However, A4 currently does NOT select SSA, SIA, a reference class, or a probability measure over observer-moments.

Therefore:
Canevas -> local observer boundary -> self-location problem
is a candidate logical chain.

Canevas -> SSA -> Doomsday
is NOT currently derived.

## Anti-tuning rule
If the result is unfavorable, do not modify the reference class, prior, or conditioning criterion to recover the intuition. Any new rule becomes a separately labelled hypothesis and a new preregistration.
