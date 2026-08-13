# Canevas 1.0 — T3.8 Generative simplicity -> modularity -> autonomy?

## Goal
Test whether a generative measure favouring simple/compressible laws can explain why modular, partially autonomous subsystems (and therefore effective observer boundaries) are typical.

This is an adversarial derivation audit. We must not assume that simplicity implies locality or modularity.

---

## Candidate hypothesis S
Suppose physical realisations/laws L receive prior generative weight decreasing with description complexity K(L), schematically

M_dyn(L) proportional to 2^{-K(L)}

or more generally M_dyn(L) = f(K(L)) with f decreasing.

This is motivated by algorithmic probability, NOT derived from A1-A4.

Question: does S imply modularity, sparse dependence, autonomy, or effective locality?

---

## T3.8-A — Simple does NOT imply local
Counterexample 1: global parity.

For N binary variables x_i, define

y(t+1) = XOR_i x_i(t).

The rule has a very short description even for enormous N, yet y depends directly on every variable.

Counterexample 2: mean-field/global coupling.

x_i(t+1) = F(x_i(t), (1/N) sum_j x_j(t)).

Again the law is compact and symmetric, but every degree of freedom can depend on a global collective variable.

Counterexample 3: permutation-symmetric all-to-all interaction.

H = (g/N) sum_{i<j} h(x_i,x_j).

The interaction graph is complete while the law is highly compressible.

VERDICT:
Simplicity/compressibility alone does NOT imply sparse locality or small Markov blankets.

---

## T3.8-B — Simple does NOT imply modular
A globally coupled chaotic map can have a concise generator while lacking a decomposition into weakly coupled modules.

Likewise, a short program can compute a cryptographic/hash-like global transformation with high sensitivity to many inputs.

Therefore

low K(L) != modular dynamics.

VERDICT: FAILED as a theorem.

---

## T3.8-C — Modularity CAN reduce description cost under an additional reuse condition
Suppose a large system contains repeated subsystem types with repeated interaction motifs. A modular description can be shorter than listing each interaction independently:

K(total) approximately K(module rule) + K(interface rule) + K(arrangement),

rather than K(full interaction table).

Thus simplicity can favour modular representations WHEN:
1. motifs repeat;
2. interfaces reuse a common rule;
3. the alternative requires largely independent specification.

But highly symmetric global all-to-all laws are also extremely compressible. Hence modularity is one route to compression, not the unique route.

VERDICT: CONDITIONAL ADVANTAGE, not derivation.

---

## T3.8-D — Observer conditioning may change the comparison
The relevant distribution for experienced worlds is not merely M_dyn(L), but schematically

P(L | observer-compatible information I) proportional to M_dyn(L) * W_obs(L,I),

where W_obs represents the measure/availability of compatible observer states.

A simple globally coupled law may have high M_dyn but produce few or no persistent information-processing subsystems. A somewhat more structured/modular law may have lower raw generative weight but vastly larger observer-compatible weight.

This creates a possible selection mechanism:

simple generative laws
x
ability to support persistent predictive subsystems
=> experienced worlds biased toward simple laws with effective modularity.

Crucially, this is NOT yet a result because W_obs is precisely part of the unresolved observer-measure problem.

---

## T3.8-E — A stronger candidate: predictive compressibility
Instead of raw description simplicity, define a subsystem S as predictively autonomous at tolerance epsilon if a compressed interface B allows

I(S_{t+1}; E_t | S_t, B_t) <= epsilon.

Let C_epsilon(S) be the minimal information/description cost of such an interface B.

Small C_epsilon means the subsystem can interact with a huge environment through a compact predictive boundary.

This quantity directly captures the property needed in T3.7, unlike K(L).

However, no current Canevas axiom says the generative measure must favour small C_epsilon.

---

## T3.8-F — Combined variational idea (candidate only)
A future model could study an objective of the form

J = alpha K(L) + beta C_epsilon(S) - gamma PERSIST(S)

or a probabilistic analogue, where lower law complexity and interface complexity compete with persistence/information-processing capacity.

DO NOT fit alpha, beta, gamma to our universe. Unless independently derived, these are arbitrary knobs and therefore not predictive.

---

## Main result
The hoped-for chain

simple generative measure
-> modularity
-> autonomy
-> observer boundaries

FAILS as a logical derivation.

The strongest defensible chain is only:

repeated modular structure
-> potentially shorter description,

and

observer-compatible persistent subsystems
-> likely require some predictive compression/interface,

but neither direction establishes that the fundamental measure favours such worlds.

---

## Important conceptual consequence
We have now encountered the same missing ingredient from two directions:

1. Physics side: probability consistency does not determine M_dyn.
2. Observer side: bounded experience does not determine a small effective boundary.

Trying to bridge them with generic 'simplicity' is insufficient because simple laws can be radically nonlocal/global.

Therefore the Canevas currently needs either:
A. an independently motivated measure principle stronger than simplicity; or
B. an observer/existence selection theorem showing that persistent self-modeling observers are overwhelmingly associated with low-interface-complexity sectors even under broad measures.

B is testable computationally without assuming our observed physical constants.

---

# T3.9 — Proposed computational experiment: Observer-support landscape

## Question
Across broad ensembles of dynamical networks, are persistent information-processing subsystems disproportionately found in systems with compact predictive boundaries?

## Ensemble families
Compare, without privileging our universe:
1. sparse random Boolean networks;
2. dense random Boolean networks;
3. globally symmetric/mean-field networks;
4. modular networks;
5. cellular/local networks;
6. mixed hierarchical networks.

## Metrics
For candidate subsystems measure:
- persistence time;
- internal memory/predictive information;
- perturbation robustness;
- interface complexity C_epsilon;
- mutual information with environment;
- degree/density/modularity of interaction graph.

## Pre-registered qualitative prediction
If persistent information-processing subsystems strongly concentrate at low/intermediate interface complexity across multiple ensemble definitions, then observer conditioning could plausibly generate effective locality even when fundamental locality is not assumed.

If equally capable persistent subsystems are common in irreducibly global high-interface systems, this route is weakened/refuted.

## Why this matters
Unlike attempts to derive locality by word-level reasoning, T3.9 can generate falsifiable numerical evidence about a mathematical claim. It does NOT prove that consciousness equals these metrics; it tests the narrower prerequisite that stable information-processing individuality correlates with compressible boundaries.

---

## Status
T3.8 RESULT: NEGATIVE for raw simplicity -> locality/modularity.

NEW POSITIVE TARGET: predictive interface complexity C_epsilon and computational T3.9.

## Anti-tuning lock
Do not choose network ensembles, thresholds, subsystem sizes, or metric weights because they reproduce 3+1 dimensions, known physics, human cognition, 1992, or any observed cosmological number. Report sensitivity across broad choices.