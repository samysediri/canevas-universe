# Canevas 1.0 — T3.5 Can restricted dependence be derived?

## Goal
Test whether sparse/local direct dependence follows from independently motivated principles already present in the Canevas programme, rather than being inserted as an extra physical axiom.

This is a destructive derivation audit. We actively search for counterexamples.

---

## Starting point
T3.4 showed:

restricted direct dependence -> interaction graph -> primitive adjacency -> possible emergent geometry.

The missing step is therefore:

WHY restricted direct dependence?

Candidate routes from T3.4:
R1 finite update/information capacity;
R2 compositional separability;
R3 stable distinguishability / observer boundaries;
R4 algorithmic economy.

---

# R1 — Finite state/information capacity

Suppose subsystem Y has a finite state space and is updated by inputs X_1,...,X_N.

A tempting claim is:
'a finite Y cannot depend on arbitrarily many independent sources, therefore its dependency degree must be finite/sparse.'

This claim is FALSE in general.

Counterexample:
Y is one bit and

Y' = XOR(X_1, X_2, ..., X_N).

Y has only two possible output states but depends functionally on every input. Similarly, majority, parity, threshold, mean-field, hash/compression, and other maps can combine very many inputs into finite output information.

For countably/infinite source families, a well-defined aggregate rule may still depend on an unbounded set under suitable mathematical assumptions.

What finite capacity DOES imply:
Y cannot preserve independently distinguishable information about arbitrarily many independent source degrees of freedom in a lossless one-to-one manner.

But

finite distinguishable output capacity != sparse causal dependence.

VERDICT: R1 FAILS to derive locality. It only constrains retained/distinguishable information unless an extra no-compression or bounded-fan-in principle is imposed.

---

# R2 — Compositional separability

T3 used the idea that genuinely independent systems should compose consistently.

Does this imply sparse coupling?

No.

A globally interacting model can still have a well-defined composite state space, e.g. a product state space with a Hamiltonian/update rule containing pairwise interactions among every pair.

Schematically:

H = sum_i H_i + sum_{i<j} J_ij V_ij

with J_ij nonzero for all pairs.

The kinematic state space can remain compositional even when the dynamics is all-to-all.

Exact dynamical independence of two selected subsystems WOULD require vanishing relevant couplings, but the Canevas axioms do not establish that arbitrary subsystems must enjoy exact dynamical independence.

VERDICT: R2 FAILS to derive sparse dependence. It distinguishes composition of state descriptions from locality of dynamics.

---

# R3 — Stable distinguishability / bounded observers

A stronger intuition is:
if everything directly affects everything else immediately, stable subsystem boundaries and observer-like states should be impossible.

This is also not a theorem.

Counterexample classes include:
- mean-field systems with all-to-all coupling but stable collective phases;
- globally coupled oscillator networks with persistent synchronised/subcluster states;
- permutation-symmetric models where robust macroscopic degrees of freedom exist despite dense microscopic interaction;
- error-correcting/attractor dynamics that can preserve a stable pattern in the presence of widespread couplings.

Thus dense interaction does not logically eliminate stable distinguishable subsystems.

What A4 may require is an EFFECTIVE information boundary for an observer, not microscopic zero coupling to distant degrees of freedom.

This is a crucial distinction:

observer boundedness -> effective conditional independence / limited accessible information

need not imply

observer boundedness -> fundamental sparse interaction graph.

VERDICT: R3 FAILS as a derivation of fundamental locality.

---

# R4 — Algorithmic/local rule economy

Sparse regular local rules can often be described more compactly than an arbitrary dense matrix of couplings.

But this cannot establish locality without an additional principle such as:
- shorter generative descriptions receive greater measure;
- laws minimise algorithmic complexity;
- primitive structure should be minimal.

Even then, highly symmetric all-to-all laws can be extremely simple, e.g.
'each node couples equally to every other node.'

So simplicity does not uniquely select locality either.

VERDICT: R4 FAILS as a unique derivation and requires an independent simplicity/algorithmic-measure axiom.

---

# Stronger candidate principles and what they would buy

Although A1-A4 do not derive locality, several explicit extra principles WOULD.

## L1 — Bounded fan-in
Each elementary update can depend directly on at most K other primitive degrees of freedom, with finite K independent of total system size.

Then the primitive dependency graph has bounded in-degree.

This directly gives restricted dependence but is essentially a locality/capacity axiom in graph language.

## L2 — Finite signalling capacity per elementary relation
If distinguishable influence must pass through finite-capacity channels and a subsystem has only finitely many elementary channels per update, local finiteness follows.

Again, the finite number of channels is an extra structural assumption.

## L3 — Lieb-Robinson-type finite propagation structure
If the generator decomposes into bounded local terms on a graph, information propagation has an effective finite velocity/cone.

But this presupposes a graph/local decomposition; it cannot derive the graph from nothing.

## L4 — Conditional-independence Markov property
Postulate that each primitive variable is conditionally independent of all non-neighbours given a finite neighbourhood.

This mathematically defines locality, but it is exactly the property we sought to derive.

---

# Important negative theorem-like result

A finite observer/information bound is insufficient to derive fundamental locality.

Reason by counterexample:
There exist systems with finite local state spaces, compositional global state spaces, stable distinguishable macrostates, and simple laws, yet dense/all-to-all direct interactions.

Therefore the conjunction of the presently motivated principles does not logically imply sparse dependency.

Symbolically:

A4 + finite local state + composability + stable patterns
NOT => bounded-degree interaction graph.

This is a genuine failure of the attempted derivation, not merely a missing calculation.

---

# What survives from the intuition

A4 still supports a weaker statement:

A bounded observer must have bounded ACCESS to information at a given observer-state.

That can be represented by an epistemic/effective dependency structure even if the fundamental dynamics is dense.

So two notions of locality must now be separated:

1. FUNDAMENTAL DYNAMICAL LOCALITY
   sparse/restricted primitive interactions.

2. EFFECTIVE/OBSERVER LOCALITY
   limited accessible information and approximately autonomous subsystems.

A4 directly motivates (2), not (1).

This distinction prevents the theory from smuggling spacetime locality out of consciousness assumptions.

---

# Consequence for T3.3/T3.4

T3.3 remains valid conditionally:
local redundancy over a base + comparison -> connection -> curvature.

T3.4 remains valid conditionally:
restricted dependence -> graph adjacency -> possible emergent geometry.

But T3.5 shows that the current Canevas axioms do NOT supply restricted dependence.

Therefore any route to emergent spacetime currently requires an additional physical principle.

---

# New target T3.6 — Which extra principle is minimal and genuinely Canevas-like?

Do NOT choose 'locality' merely because our universe is local.

Instead compare candidate extensions by logical economy and independence from observed targets:

E1. Finite elementary influence capacity:
No primitive event can receive an unbounded number of independently distinguishable causal influences in one elementary transition.

E2. Finite channel principle:
Every primitive transition is mediated by a finite number of elementary relational channels.

E3. Factorisation-at-separation principle:
There exist nontrivial subsystem partitions for which sufficiently remote/no-link components can be conditionally independent.

E4. Causal mediation principle:
Influence between non-identical primitive events must be mediated through a chain of intermediate relations rather than an irreducible universal all-to-all kernel.

E4 is particularly interesting because it encodes 'relations build influence' without presupposing metric distance. If adopted, adjacency is defined by irreducible mediation links and longer-range influence becomes path composition.

However E1-E4 are NEW candidate axioms unless one can derive them from a deeper statement about what counts as a physically distinct relation.

### T3.6 success criterion
Find a minimal additional principle whose content is not equivalent to assuming known spacetime locality, but which nontrivially excludes irreducible all-to-all dependence and yields a relational network.

### Failure criterion
If every successful principle is merely locality restated in other words, then locality must be acknowledged as an independent primitive of the theory.

---

## Main verdict
T3.5 = NEGATIVE RESULT.

The current Canevas axioms do NOT derive fundamental sparse/local dependence.

They plausibly motivate observer/effective locality, but all-to-all fundamental dynamics remains logically compatible with bounded observers, finite states, compositional descriptions, and stable structures.

This sharply identifies the next theory-choice point rather than hiding it.

## Anti-tuning lock
No new locality principle may be selected because it reproduces 3+1 spacetime, Lorentz invariance, finite c, GR, gauge fields, Standard Model particles, cosmological parameters, life, or any previous numerical result.