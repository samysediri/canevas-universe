# Canevas 1.0 — T3.1 Symmetry + Locality + Composition

## Goal
Test whether independently motivated structural principles can restrict the unknown generative weight strongly enough to approach a specific action/amplitude law, without using any observed numerical target.

## Starting point
From T3 we already have:
- a measure/probability layer must be additive under coarse graining;
- arbitrary relabellings cannot change physical measure;
- refinement of a history description cannot change probabilities;
- independent composition suggests multiplicative weights, equivalently an additive generator after a logarithm.

These constraints do NOT uniquely determine the physics.

## Candidate structural principle S1 — Local compositionality
Assume that, for a history described by local degrees of freedom phi on spacetime, the generator is built additively from local contributions:

S[phi] = integral d^d x L(phi, partial phi, partial^2 phi, ...)

This is not derived from A1-A4. It is an additional physical principle motivated by the idea that independent spacetime regions should compose locally rather than require arbitrary global bookkeeping.

Status: CANDIDATE PHYSICAL PRINCIPLE.

## Candidate structural principle S2 — Symmetry invariance
Let G be the set of fundamental transformations under which the Canevas has no physical preference. Require the generative law to assign equivalent physical histories the same total weight/amplitude.

Examples of possible symmetry classes, to be justified rather than assumed:
- spacetime translations;
- rotations;
- Lorentz transformations;
- diffeomorphisms;
- internal/gauge symmetries.

Important: A1-A4 currently do NOT uniquely imply this list. In particular, Lorentz invariance, gauge groups, and dimensionality of spacetime cannot be smuggled in as consequences of the philosophical axioms.

Status: FRAMEWORK, not yet a derivation.

## Structural consequence of S1 + composition
If the weight of independent regions factorises, a positive classical weight can be represented schematically as

M[phi] proportional to exp(-S[phi])

with additive S. In quantum mechanics, local composition instead points naturally to amplitude composition, schematically

A[phi] proportional to exp(i S[phi] / hbar),

followed by interference and a probability rule.

These are broad structural forms, not unique physical theories: infinitely many local Lagrangians L are possible.

## Why symmetry helps but does not finish the job
Symmetries severely restrict which terms may appear in L. Locality plus the field content and symmetry assumptions can sometimes make a theory very rigid. However, even a fixed symmetry class typically permits many operators and coupling constants. Effective field theory makes this explicit: every local operator compatible with the symmetries generally appears, suppressed by scales/couplings.

Therefore:

locality + symmetry + composition -> constrained family of generators,

not generally

locality + symmetry + composition -> unique generator.

## Candidate T3.1 result — “Form before constants”
A defensible target for Canevas is weaker but still meaningful:

1. derive the admissible mathematical FORM of the generator from composition/locality;
2. derive the relevant symmetry group from deeper principles, if possible;
3. use those symmetries to classify allowed terms;
4. only then ask whether any coefficients/couplings can be fixed by an additional non-empirical principle.

This is substantially stronger than fitting constants directly, but it still leaves an open coefficient problem.

## Quantum fork
There are two logically distinct routes.

### Q-classical
Assume a classical stochastic ontology with positive path weights. Then M is an ordinary path measure. Local transition laws plus an initial measure determine it.

Problem: the transition law and initial state remain extra physics.

### Q-quantum
Assume Hilbert-space quantum mechanics. Then histories carry amplitudes rather than classical probabilities before interference. Noncontextual probability assignment on Hilbert space strongly constrains final outcome probabilities toward Born-type weights, but that conclusion depends on the Hilbert-space structure itself.

Therefore Canevas cannot claim a Born-rule derivation from A1-A4 unless it first derives or independently motivates quantum state-space structure.

## The hardest missing derivation
The central unresolved question is now:

Why this state space and these symmetries?

Examples:
- Why 3+1 dimensional Lorentzian spacetime?
- Why quantum amplitudes rather than classical probabilities?
- Why Standard Model gauge symmetry?
- Why these field representations?

Without answers, locality and symmetry merely re-express known physical structure.

## A promising new target: relational symmetry
The Canevas axioms may motivate one more primitive principle without using observed constants:

R1. No physically meaningless external label should affect generative weight.
R2. Only relationally defined distinctions can matter.

If strengthened into a physical statement, this might motivate gauge redundancy / coordinate redundancy: multiple mathematical descriptions representing the same relational physical state should not be counted as distinct physical possibilities.

This is promising because it connects the earlier observer-side label invariance to the world-side description of physical states.

However:
- label invariance alone does not determine a specific gauge group;
- diffeomorphism/gauge redundancy is stronger than ordinary relabelling;
- this connection is therefore a candidate bridge, not a theorem.

## T3.2 preregistered target
Try to derive a “relational state principle” from the Canevas axioms:

Canevas has no external reference frame / external label
-> physical states are equivalence classes under redundant descriptions
-> admissible dynamics must act on equivalence classes
-> symmetry/gauge structure may emerge as redundancy constraints.

Success criterion:
Produce at least one nontrivial mathematical restriction on state space or dynamics that is NOT inserted by assuming known Standard Model/GR symmetries.

Failure criterion:
If all concrete restrictions require importing Lorentz invariance, Hilbert space, gauge groups, dimensionality, or observed fields as assumptions, then the philosophical axioms have not yet generated new physics.

## Current verdict
SUPPORTED:
- composition strongly motivates additive generators/log-weights;
- local compositionality plus symmetry is a legitimate route for restricting dynamics;
- known physics shows that locality and symmetry can be highly constraining in specific field-content classes.

NOT DERIVED FROM CANEVAS:
- locality itself as a fundamental law;
- spacetime dimension/signature;
- Lorentz symmetry;
- Hilbert-space quantum structure;
- gauge group;
- particle content;
- coupling constants;
- unique action.

MAIN CONCLUSION:
T3.1 does not produce a unique law. It identifies the next genuine leverage point: derive relational redundancy/symmetry from the absence of external labels, then see whether that yields any nontrivial restriction before importing known physics.

## Anti-tuning lock
Do not choose a symmetry, dimensionality, field content, action term, or coupling because it reproduces observed constants or known particles. Those may only be used after the structural derivation is frozen.