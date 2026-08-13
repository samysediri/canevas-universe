# Canevas 1.0 — T3.4 Emergent locality from restricted dependence

## Goal
Test whether a primitive notion of locality/adjacency can emerge without assuming a spacetime manifold, Euclidean distance, Lorentz symmetry, dimensionality, or known fields.

This is a derivation audit. The target is modest: obtain a nontrivial relational structure that could later support geometry.

---

## Starting point
From earlier stages:
- A4 motivates bounded/local observer information, but does not itself define spatial locality.
- T3/T3.1 motivate composition and consistent generative structure.
- T3.2 says physical states should be quotiented by physically meaningless relabellings.
- T3.3 shows that IF local redundancy lives over a base with neighbouring points, connection/curvature follow naturally.

The missing object is the base/adjacency itself.

---

## Candidate primitive P — Restricted direct dependence

Let the total physical state be decomposable, at some scale, into distinguishable subsystems/events {v_i}.

Assume:
P1. A subsystem/event does not directly depend on every other subsystem/event in a single elementary update.
P2. Direct influence/dependence is a physical relation, not an external coordinate label.
P3. The relation is finite or sufficiently sparse at the primitive scale.

P1-P3 are NOT derived from A1-A4. They are candidate physical principles motivated by compositional independence and bounded information exchange.

Given P1-P3, define a directed graph G=(V,E):

v_i -> v_j iff the elementary update/statistics of v_j can depend directly on v_i.

This graph is relational: vertices need no absolute positions, and graph automorphisms that preserve all physical relations represent the same unlabeled structure.

---

## T3.4-A — Adjacency emerges from direct dependence

Once direct dependence is primitive, neighbourhood is definable without distance:

N(v) = {u : (u,v) or (v,u) is an elementary dependency edge}.

Therefore a primitive locality concept can be defined as 'one interaction step away' rather than 'near in metres'.

Graph distance then becomes a derived combinatorial quantity:

d_G(u,v) = minimum number of dependency links in a path from u to v

for undirected/symmetrised reachability where appropriate.

VERDICT: CONDITIONAL SUCCESS.
Restricted direct dependence is sufficient to define relational adjacency and a primitive graph distance without presupposing continuum geometry.

---

## T3.4-B — Causal order requires stronger assumptions

A directed dependency graph is not automatically a causal partial order.

To obtain a partial order <=, one needs at least:
1. transitive reachability interpreted as causal precedence;
2. antisymmetry/no directed causal cycles at the primitive level;
3. reflexive completion if using the mathematical definition of partial order.

Then

u <= v iff v is reachable from u by a directed dependency path.

This is structurally similar to causal-set kinematics, where primitive elements are partially ordered by causal precedence and local finiteness supplies discreteness. But Canevas has NOT derived causal-set theory; it only reaches an analogous mathematical possibility under additional assumptions.

VERDICT: NOT DERIVED FROM P1-P3 ALONE. Requires an acyclicity/causal-orientation principle.

---

## T3.4-C — Local finiteness from bounded interaction capacity

If every primitive subsystem has finite direct interaction capacity in any finite update interval, then each vertex has finite in/out neighbourhood at that resolution.

This gives graph-theoretic local finiteness.

However, A4's bounded conscious information does NOT imply that all fundamental physics has finite degree. Therefore local finiteness remains conditional on a physical capacity bound.

VERDICT: CONDITIONAL.

---

## T3.4-D — Geometry does not follow uniquely from a graph

A graph gives adjacency, connectivity, shortest-path distance, degree, spectra, growth rates, and other relational invariants. But these do not uniquely imply a smooth metric manifold.

Many graphs are highly non-geometric. A continuum-like geometry would require additional large-scale regularities, for example:
- stable volume-growth law |B(r)| ~ r^d over a scaling range;
- approximately homogeneous/isotropic statistics;
- spectral behaviour compatible with a finite effective dimension;
- causal structure compatible with a Lorentzian continuum, if that is the target;
- suitable suppression of pathological/non-manifold-like graph ensembles.

Therefore

interaction graph -> possible emergent geometry

is legitimate, but

interaction graph -> 3+1 dimensional spacetime

is false without more structure.

---

## T3.4-E — Dimension can become an emergent observable, not an input

If a graph/network has approximate polynomial ball growth,

|B(v,r)| ~ r^d,

a large-scale effective dimension d can be estimated from

d_eff(r) = d log |B(v,r)| / d log r.

Alternatively, diffusion/spectral dimension can be defined from return probabilities of a random walk.

This is conceptually important: dimension need not be assigned to the primitive vertices. It can be a property of connectivity at large scales.

VERDICT: STRUCTURAL POSSIBILITY, not a derivation of d=3 spatial dimensions.

---

## T3.4-F — Information propagation gives a primitive light-cone analogue only conditionally

If updates occur in discrete causal steps and information traverses at most one (or finitely many) dependency edges per step, then after n steps an influence can reach only the n-neighbourhood.

That creates a finite propagation cone in graph distance.

But this requires:
- an update/order parameter;
- a finite propagation rule;
- no instantaneous long-range edge outside the graph relation.

It does NOT by itself produce Lorentz invariance or a universal speed c.

VERDICT: CONDITIONAL.

---

## Relation to A4

The strongest honest bridge from A4 is not

bounded observer -> spacetime locality.

It is only:

bounded observer information
-> motivates finite accessible causal neighbourhood for an observer
-> suggests testing whether underlying dynamics also has restricted dependence.

The last arrow is an additional physical hypothesis, not a theorem.

This distinction must remain explicit.

---

## Main result

T3.4 succeeds only in the following conditional sense:

RESTRICTED DIRECT DEPENDENCE
=> RELATIONAL INTERACTION GRAPH
=> PRIMITIVE ADJACENCY
=> DERIVED GRAPH DISTANCE / REACHABILITY

Additional assumptions can then give:

ACYCLIC ORIENTATION
=> CAUSAL PARTIAL ORDER

FINITE INTERACTION CAPACITY
=> LOCAL FINITENESS

LARGE-SCALE REGULARITY
=> POSSIBLE EMERGENT CONTINUUM GEOMETRY / EFFECTIVE DIMENSION.

This is the first route in the Canevas program where a notion resembling 'space is relations, not a container' can be made mathematically explicit without assuming coordinates.

But the crucial physical principle — why dependence is restricted rather than all-to-all — is still missing.

---

## Comparison with known causal-set ideas

Causal-set theory demonstrates that a locally finite partial order can serve as a discrete proto-spacetime and may approximate continuum Lorentzian geometry in suitable cases. This supports the mathematical viability of the general route, but does NOT validate the Canevas derivation because causal-set theory postulates its order/local-finiteness structure rather than deriving it from A1-A4.

Use this comparison only as an existence proof that such relational kinematics is mathematically serious.

---

## New target T3.5 — Can restricted dependence be derived from finite distinguishability/composition?

We now isolate the real missing step:

Why should elementary physical dependence be sparse/local instead of all-to-all?

Candidate non-empirical routes to test:

R1. Finite update capacity: a finite-state subsystem cannot absorb independent information from infinitely many sources in one elementary transition without additional compression/degeneracy.

R2. Compositional separability: genuinely independent subsystems must admit product/composed states; universal instantaneous coupling destroys exact independence.

R3. Stable distinguishability: if every degree of freedom directly affects every other in one step, local perturbations generically erase any persistent subsystem boundary, potentially conflicting with the existence of bounded observer-like structures.

R4. Algorithmic/local rule economy: sparse local update laws may require less primitive structure than arbitrary all-to-all kernels, but this becomes an algorithmic simplicity assumption and is NOT free.

### T3.5 success criterion
Derive a finite/sparse dependency relation from independently justified principles stronger than mere convenience, without assuming metric distance or known locality.

### Failure criterion
If restricted dependence must simply be postulated, then locality remains an extra physical axiom of Canevas rather than a consequence of A1-A4.

---

## Status

SUPPORTED CONDITIONALLY:
- restricted dependence defines adjacency;
- adjacency can support graph distance and neighbourhoods;
- with acyclicity, reachability yields a causal partial order;
- effective dimension can emerge from network scaling rather than being fundamental.

NOT DERIVED:
- restricted dependence itself;
- acyclicity;
- finite degree;
- continuum manifold;
- 3+1 dimensions;
- Lorentz invariance;
- gravity;
- metric dynamics.

MAIN VERDICT: CONDITIONAL SUCCESS, WITH THE CORE MISSING AXIOM NOW SHARPLY IDENTIFIED.

## Anti-tuning lock
Do not choose graph degree, dimension, update rule, causal orientation, continuum limit, or dynamics because it reproduces 3+1 spacetime, c, GR, Standard Model fields, cosmological constants, dark matter, Higgs physics, life, or any other observed target.