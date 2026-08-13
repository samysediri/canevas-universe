# Canevas 1.0 — Observer-measure destructive stress test v3

## Goal
Stress-test the observer-measure family derived in `observer_measure_derivation_v2.md` without using the user's birth year, technology dates, zeta, Lambda, neutrino masses, or any desired observational result.

We ask which properties any admissible measure w(O) must satisfy before it is applied to data.

---

## Starting definitions

Let R(I) be the set of physically realised local observer-states compatible with the information I available to the present experience.

Let mu be a non-negative measure over compatible observer occurrences/trajectories. Self-location probabilities, when normalisable, are

P(A | I) = mu(A ∩ R(I)) / mu(R(I)).

The central question is not yet the numerical value of mu, but which invariances and consistency rules constrain it.

---

# Constraint K1 — Label invariance

If two local observer-states are physically identical with respect to all Q-relevant accessible information, changing an external bookkeeping label cannot change their individual measure.

External names, universe IDs, file numbers, coordinate names, or arbitrary enumeration order are inadmissible weight sources.

Status: STRONG CANDIDATE, inherited from v2.

---

# Constraint K2 — Refinement invariance

A probability rule must not change merely because we choose a finer arbitrary temporal discretisation.

Suppose an experiential interval E is represented once as one segment or alternatively partitioned into n consecutive subsegments E_1...E_n without changing the underlying physics. Then consistency requires

mu(E) = sum_i mu(E_i).

Consequences:
- naive '1 unit of weight per observer-moment object' is ill-defined unless the physical definition fixes a non-arbitrary atomic moment;
- simply sampling discrete time-slices can create arbitrary probabilities by changing the timestep;
- an admissible temporal measure should be additive and independent of bookkeeping resolution.

This does NOT yet imply weighting by ordinary clock time. Proper time, physical transitions, information change, or another additive invariant remain candidates.

Status: STRONG CONSISTENCY REQUIREMENT.

---

# Constraint K3 — Coarse-graining consistency

If a set of mutually exclusive observer alternatives is grouped into a macro-alternative, its measure must equal the sum of the component measures.

mu(A union B) = mu(A) + mu(B), for disjoint A,B.

Otherwise probabilities depend on how an analyst names or groups outcomes.

Status: STRONG CONSISTENCY REQUIREMENT.

---

# C1 — Exact duplicate observers

Setup:
World W1 contains one occurrence of local observer-state O.
World W2 contains two physically distinct simultaneous occurrences O_a and O_b that are internally/Q-relevantly identical.

K1 requires
w(O_a)=w(O_b).

But two possibilities survive:

TOKEN measure: mu({O_a,O_b}) = 2 w(O).
TYPE measure: duplicated instantiations do not increase total measure because only the informational type counts.

A4 does not presently choose TOKEN vs TYPE.

Verdict: UNDERDETERMINED.

---

# C2 — Sleeping-Beauty / temporal duplication

Setup:
One physical observer passes through multiple locally indistinguishable awakenings/observer-states.

A person-counting rule and an occurrence/trajectory measure disagree.

K2 rules out a crude 'number of saved frames' measure because arbitrary temporal subdivision changes the answer. However K2 permits any additive measure on the physical trajectory.

Candidate forms include

mu = integral rho(O_tau) d tau

where tau could be invariant proper time and rho a local physical density, or an alternative additive functional over state transitions.

Nothing in A4 currently fixes rho=constant or even selects proper time as the relevant base measure.

Verdict: DISCRETISATION PROBLEM SOLVED IN FORM, NOT UNIQUE WEIGHT.

---

# C3 — Long-lived versus short-lived observers

Setup:
Observer A has a compatible experiential trajectory ten times longer than B.

If mu is proper-time additive with constant density, A has 10x total weight.
If mu weights only distinct informational transitions, a static extra duration may add little/no weight.
If mu is TYPE-based, repeated identical states may add no weight at all.

A4 requires local determination, not duration proportionality.

Verdict: UNDERDETERMINED.

---

# C4 — Simulation multiplicity

Setup:
A local experience O occurs once biologically and one million physically realised exact simulations instantiate an equivalent O.

K1 says substrate labels alone cannot make equivalent experiences have unequal individual weight if the relevant experiential/physical structure is genuinely equivalent.

TOKEN measures therefore strongly favour the simulated population by multiplicity.
TYPE measures do not.
Substrate-sensitive measures are admissible only if the substrate difference changes a physically relevant property used by the independently justified measure; 'biological' cannot be inserted as an ad-hoc privilege.

Verdict: TOKEN/TYPE ambiguity becomes operationally enormous.

---

# C5 — Quantum branching

Setup:
Compatible observer-states occur in quantum branches with unequal physical branch weights/amplitudes.

Pure branch-counting is not yet justified by A4 and can depend on how branching is coarse-grained.
A quantum-mechanical measure such as Born weighting may satisfy independent quantum consistency principles, but it is NOT derivable from the present Canevas axioms merely by invoking local observers.

Therefore Canevas must either:
(a) inherit a measure from the underlying physical dynamics, or
(b) derive an additional principle strong enough to choose one.

Verdict: CANEVAS-ONLY MEASURE NOT YET DERIVED.

---

# C6 — Boltzmann-brain / false-history duplicates

Setup:
O_normal is an observer-state generated by a long ordinary causal history.
O_BB is a rare fluctuation whose current local accessible state, memories, and immediately accessible records are physically indistinguishable from O_normal.

If I contains only the information currently accessible to the observer, then both belong to R(I).

K1 prevents assigning different weights solely because an omniscient external observer labels one 'normal' and one 'Boltzmann brain'.

This yields a major tension:

1. Pure TOKEN occurrence counting can be dominated by whichever production mechanism creates more compatible copies, including pathological fluctuation observers in some cosmologies.
2. Excluding O_BB because of its hidden causal provenance uses information not contained in I, apparently violating the conditioning/locality principle.
3. Expanding I to include accessible environmental records helps only if the fluctuation does not reproduce those records too. A sufficiently large fluctuation can reproduce the entire accessible local patch.
4. Therefore avoiding Boltzmann-brain domination appears to require the MEASURE itself to encode the physical generative weight/probability of histories, not merely count locally compatible endpoints.

This is the strongest stress-test result so far.

Candidate structural conclusion:

LOCAL COMPATIBILITY determines what alternatives cannot be distinguished by the observer,
but DYNAMICAL/GENERATIVE MEASURE determines how much physical weight those alternatives carry.

Symbolically:

P(O | I) ∝ M_dyn(history/realisation leading to O) × 1[O compatible with I]

where M_dyn must come from independently specified physics or a further Canevas axiom. It cannot be chosen after seeing which histories resemble ours.

Verdict: ENDPOINT-ONLY OBSERVER MEASURE IS INSUFFICIENT.

---

# New structural decomposition

The stress tests suggest that the measure problem should be split into two logically different pieces:

## 1. Epistemic compatibility
R(I) = locally realised observer-states consistent with accessible information I.

This component is motivated by A4 / observer locality.

## 2. Ontic/generative weight
M_dyn(x) = physical measure assigned to the realisation/history/branch x by the underlying generative dynamics.

Then

P(x | I) = M_dyn(x) 1[x compatible with I] / Z(I).

This is ordinary conditionalisation in structure, but the key unresolved object is M_dyn.

A4 constrains the conditioning set. It does NOT currently generate M_dyn.

---

# Consequence for the Canevas project

This substantially narrows the theory-building target.

Previous question:
'What reference class should we use?'

Improved question:
'What underlying generative law/measure does the Canevas assign to physical realisations before any observer conditions on them?'

If the Canevas truly realises every physically possible configuration, this question is unavoidable: existence of all possibilities alone does not specify relative measure.

Thus a new axiom or theorem is required unless M_dyn can be inherited uniquely from deeper physical dynamics.

---

# Candidate next theorem target T3 — Generative consistency

Seek a measure M_dyn satisfying, at minimum:

G1. non-negativity;
G2. normal/additive coarse-graining consistency;
G3. invariance under arbitrary relabelling/reparametrisation;
G4. refinement invariance (no dependence on arbitrary slicing of a process);
G5. composition consistency for independent subsystems;
G6. compatibility with known quantum probabilities if quantum mechanics is retained;
G7. no ad-hoc dependence on the observed values the measure will later be asked to explain.

Question: do these constraints uniquely or nearly uniquely determine a known mathematical measure class?

That question should be attacked BEFORE any new comparison to 1992, Doomsday, zeta, Lambda, Higgs, dark matter, or life.

---

# Status after v3

SUPPORTED AS STRUCTURAL CONSTRAINTS:
- local compatibility / accessible-information conditioning;
- label invariance;
- additivity/coarse-graining consistency;
- temporal refinement invariance.

NOT DERIVED:
- token vs type counting;
- duration weighting;
- computational weighting;
- simulation weighting;
- Born weighting from Canevas itself;
- the fundamental generative measure M_dyn.

NEW FAILURE:
- endpoint-only/local-state counting cannot generically solve Boltzmann-brain style pathologies.

NEW TARGET:
- derive or constrain M_dyn independently of observations.

---

## Anti-tuning lock
No candidate generative measure may be selected because it makes the user's birth year typical, avoids a preferred Doomsday conclusion, reproduces zeta, predicts neutrino masses, or produces familiar constants. Selection must precede those comparisons.
