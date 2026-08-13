# Canevas 1.0 — T3 Generative Consistency v1

## Goal
Determine how far the generative measure M_dyn can be constrained BEFORE looking at any empirical target (birth year, zeta, Lambda, neutrino masses, Higgs, dark matter, life, etc.).

This is a derivation audit, not a fit.

---

## Setup
Let X be a space of physical realisations/histories/branches. Let M(A) be the non-negative generative measure assigned to a measurable subset A of X.

Observer conditioning occurs only afterward:

P(A | I) = M(A ∩ R(I)) / M(R(I)),

when the denominator is finite and non-zero.

The task here is solely to constrain M.

---

# G1 — Non-negativity
M(A) >= 0.

Negative ordinary probabilities are inadmissible at the final probability level. Quantum amplitudes may be complex, but M itself must be non-negative if it is the probability measure used for observer conditionalisation.

Status: REQUIRED.

# G2 — Null and additive structure
M(empty)=0.
For disjoint alternatives A and B:
M(A union B)=M(A)+M(B).

Otherwise merely splitting or merging named alternatives changes probability.

Status: REQUIRED for ordinary probability measure.

# G3 — Relabelling invariance
A bijective change of arbitrary labels cannot change physical measure. Coordinate descriptions may change densities through the appropriate Jacobian, but the measure assigned to the same physical set must be invariant.

Important distinction: this does NOT imply a uniform density in every parameterisation. There is no parameterisation-independent notion of 'uniform over all possible values' without additional structure.

Status: REQUIRED; immediately rules out naive coordinate-uniform priors as fundamental without a preferred physical measure element.

# G4 — Refinement/projective consistency
If a history is represented at resolutions r and r', marginalising the finer description back to the coarser description must reproduce the coarse measure.

For coarse state x and refinements y compatible with x:
M_r(x) = sum/integral_{y -> x} M_r'(y).

This is stronger than merely saying probabilities add. It requires a consistent family of finite-resolution distributions if the fundamental history space is continuous/infinite-dimensional.

Status: REQUIRED for discretisation-independent physics.

# G5 — Independent composition
For genuinely independent systems A and B, the joint measure should factorise:
M(A,B)=M_A(A) M_B(B),
up to overall normalisation conventions.

Equivalently, an additive information/action-like quantity S=-log M satisfies
S(A,B)=S(A)+S(B).

This is a major structural result: multiplicative probability weights naturally correspond to additive generators under -log.

Status: STRONG CANDIDATE, conditional on a meaningful notion of physical independence.

# G6 — Sequential composition
If a process can be decomposed into successive conditional transitions, consistency requires a chain rule:
M(x_0,...,x_n)=M(x_0) product_k P(x_{k+1}|x_0...x_k).

If the dynamics is Markovian this reduces to local transition kernels; if not, history dependence remains. Therefore generative consistency alone does NOT imply Markov dynamics or locality in time.

Status: PROBABILITY-THEORETIC CONSEQUENCE once conditional probabilities exist; does not choose dynamics.

---

# What these axioms already exclude

1. Raw counting of arbitrarily discretised histories: violates refinement invariance.
2. 'Uniform over parameter x' without a physically preferred measure element: generally violates reparameterisation neutrality.
3. Post-hoc weights chosen to make an observation typical: violates anti-tuning lock.
4. Endpoint-only weights that ignore generative history when different histories carry different physical probability: fail the Boltzmann-brain stress test.

---

# Candidate mathematical families

## A. Classical stochastic/path measures
A transition law plus initial measure induces a probability measure over trajectories. This naturally satisfies non-negativity, additivity, chain rules, and—when constructed consistently—refinement/projective consistency.

Problem: the transition law and initial measure are additional physics. T3 does not derive them uniquely.

## B. Gibbs / exponential measures
If independent composition makes a generator additive, weights of the form
M(x) proportional to exp[-S(x)]
are natural, where S is additive for independent composition.

This form is extremely broad: S could be an action, entropy-related functional, information cost, etc. G1-G5 alone do not determine S.

Important: exp(-S) is NOT yet a prediction of Canevas; it is a structural representation when positive multiplicative weights admit a logarithm.

## C. Maximum-entropy measures
Given specified constraints, maximizing entropy yields an exponential-family distribution.

Problem: MaxEnt requires a prior/base measure and explicit constraints. Neither is uniquely supplied by A1-A4 at present. Therefore MaxEnt cannot secretly solve the measure problem without additional assumptions.

## D. Algorithmic/Solomonoff-like measures
Weights decreasing with description length naturally privilege simpler generative rules.

Problems: dependence on description language/universal machine up to constants; computability assumptions; unclear direct physical justification; quantum generalisation nontrivial. Not derived from current axioms.

## E. Quantum measure / Born family
If Canevas retains Hilbert-space quantum mechanics, branch probabilities are empirically governed by the Born rule. Gleason-type/noncontextuality and decision/envariance derivations show that strong quantum structural assumptions can constrain probability weights toward squared amplitudes.

Crucial logical point: those derivations require quantum structure beyond A1-A4. Therefore T3 can INHERIT Born weighting conditional on quantum mechanics, but cannot currently claim to derive Born's rule from Canevas alone.

## F. Path-integral amplitudes
Quantum dynamics often assigns complex amplitudes roughly of phase form exp(i S/hbar) to histories, with observable probabilities arising after interference and Born conversion.

This is not an ordinary positive M over individual fine-grained histories. Therefore a naive classical probability measure over quantum paths is generally wrong. Any Canevas generative measure must distinguish amplitude-level composition from final probability-level measure if quantum mechanics is fundamental.

---

# Critical theorem-like result: probability consistency is not enough

G1-G5 strongly constrain the FORMAL BEHAVIOUR of M but do not select a unique M.

Proof by counterexample family:
Take any two distinct normalised physical densities p(x) and q(x) defined relative to the same invariant base measure. Both can satisfy non-negativity, additivity, relabelling covariance, refinement consistency, and independent composition when extended appropriately. Yet p != q.

Therefore:

G1-G5 => admissible measure class,
NOT
G1-G5 => unique physical measure.

A genuinely predictive Canevas requires at least one additional PHYSICAL principle, not merely more probability axioms.

---

# T3.1 — Search for the missing physical principle

The next candidate should be constrained without data. Candidate principle families:

P1. Dynamical symmetry: M is invariant under the fundamental symmetries of the Canevas.
P2. Local compositionality: the generator of history weight is an integral/sum of local contributions.
P3. Minimal extra structure: among measures satisfying symmetries and composition, introduce no additional preferred scales/coordinates.
P4. Quantum consistency: if fundamental state space is Hilbertian, require noncontextual probability assignments compatible with orthogonal decomposition.
P5. Typical-history stability: conditioning on larger accessible records should suppress fake-history realisations according to their generative weight without an ad-hoc 'normal observer' rule.

These are candidates, not axioms yet.

---

# Most promising route

The strongest non-empirical route appears to be:

Canevas structural axioms
-> local observer compatibility R(I)
-> probability consistency G1-G4
-> physical independence/composition G5
-> symmetry + local compositionality
-> additive generator S
-> candidate dynamical weight family
-> quantum consistency if applicable
-> only THEN empirical tests.

The key question becomes whether symmetry/locality/composition can determine S (or an amplitude analogue) uniquely enough to make predictions.

---

# Falsification criteria for T3.1

The route fails as a derivation if:
1. multiple inequivalent generators remain after all independently justified Canevas symmetries are imposed;
2. a preferred scale/coordinate must be inserted solely to obtain observed values;
3. quantum probabilities require an unrelated axiom with no Canevas motivation;
4. the resulting measure is non-normalisable in the relevant conditional classes and no principled regularisation exists;
5. Boltzmann-brain domination survives for physically reasonable cosmologies.

---

# Status

DERIVED/REQUIRED AT PROBABILITY LEVEL:
- non-negativity;
- additivity;
- relabelling/reparameterisation covariance of the measure;
- refinement/projective consistency.

STRONG BUT PHYSICALLY CONDITIONAL:
- factorisation for independent systems;
- additive -log generator for positive multiplicative weights.

NOT DERIVED:
- unique base measure;
- unique generator/action S;
- fundamental constants;
- Born rule from A1-A4;
- classical vs quantum ontology;
- a solution to the cosmological measure problem.

MAIN RESULT:
Consistency axioms alone cannot produce the missing physics. The next legitimate target is a symmetry/local-compositionality derivation of the generator, with quantum structure treated explicitly rather than smuggled into an ordinary classical probability measure.

## Anti-tuning lock
No candidate in T3.1 may be selected using 1992, Doomsday, zeta, Lambda, neutrino masses, Higgs mass, dark matter abundance, life, or any other observed numerical success.
