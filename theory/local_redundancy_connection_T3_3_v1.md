# Canevas 1.0 — T3.3 Local redundancy -> connection -> curvature

## Goal
Test whether promoting relational/redescription redundancy from global to local forces nontrivial geometric structure, without assuming the Standard Model gauge group, Lorentz invariance, Hilbert space, or observed particles.

## Starting point from T3.2
Let D be a description space and ~ an equivalence relation identifying descriptions that represent the same physical state. The physical state space is D/~. Physical observables and dynamics must descend to the quotient.

T3.3 adds one new candidate principle:

LR — the redundant convention may be chosen independently at different base points/regions.

This is stronger than global relabelling and is NOT yet derived from A1-A4. It is the assumption under test.

---

## Minimal mathematical model
Let X be a base space of locations/events/regions. At each x in X, let a local description live in a fibre F_x. A redundancy group G acts on each fibre. A local change of convention is a map g(x) in G.

A field-like local description psi(x) transforms schematically as

psi(x) -> g(x) psi(x).

If g is constant, ordinary comparison between neighbouring values may remain covariant. If g varies with x, the ordinary derivative contains an extra term involving partial g:

partial_mu [g(x) psi(x)] = (partial_mu g) psi + g partial_mu psi.

Therefore partial_mu psi does NOT transform in the same way as psi under arbitrary local changes of convention.

This is the key obstruction.

---

## T3.3-A — Need for a comparison/transport rule
If the theory needs to compare local states at neighbouring points while local conventions may vary independently, a compensating comparison structure is required.

Introduce a connection-like object A_mu and a covariant derivative

D_mu psi = partial_mu psi + A_mu psi

(with representation-dependent signs/couplings suppressed).

Demanding

D'_mu psi' = g(x) D_mu psi

forces A_mu to transform inhomogeneously, schematically

A'_mu = g A_mu g^{-1} - (partial_mu g) g^{-1}.

Thus the connection transformation law is not arbitrary decoration: it is what cancels the derivative of the local convention.

VERDICT:
Conditional theorem. GIVEN a differentiable base, local redundancy G, and a need for derivative/comparison between fibres, an ordinary derivative is insufficient and connection-like structure is required.

This satisfies the T3.3 structural target without selecting G.

---

## T3.3-B — Curvature emerges from noncommuting transport
Once D_mu exists, compare two infinitesimal transport directions. Their commutator defines curvature/field strength:

[D_mu, D_nu] psi = F_mu_nu psi.

Schematically

F_mu_nu = partial_mu A_nu - partial_nu A_mu + [A_mu, A_nu].

For an Abelian redundancy the commutator term vanishes. For non-Abelian redundancy it remains.

Geometrically, nonzero F measures path dependence/holonomy: transporting around a small loop need not return the internal description unchanged.

VERDICT:
Conditional theorem once connection/differentiability are assumed.

---

## T3.3-C — What is genuinely derived vs imported

Derived CONDITIONALLY from LR + differentiable comparison:
1. local convention changes obstruct ordinary derivatives;
2. a connection/covariant derivative repairs local comparison;
3. connection transformation law contains an inhomogeneous derivative term;
4. curvature is the natural obstruction to path-independent transport;
5. physical local quantities can be built from gauge-covariant/invariant combinations rather than raw convention-dependent components.

NOT derived:
1. existence of spacetime X itself;
2. dimension or metric/signature of X;
3. why redundancy is local rather than merely global;
4. which group G;
5. whether G is continuous, compact, finite, Abelian, non-Abelian, etc.;
6. matter representations;
7. a kinetic action such as F^2;
8. coupling constants;
9. quantum mechanics;
10. Standard Model gauge structure.

Therefore this is a structural derivation, not a derivation of known gauge physics from A1-A4.

---

## Important failure mode: redundancy alone does not imply a physical force
A connection can be mathematically necessary for local comparison while still being nondynamical or pure gauge. To obtain a propagating interaction one needs additional structure/a dynamical action for A.

Hence the chain

local redundancy -> connection

is defensible under stated assumptions, but

local redundancy -> new force

is NOT.

---

## Relation to the Canevas
The possible Canevas bridge is now precise:

No external privileged labels
-> descriptions related only by convention represent one physical state
-> IF convention freedom is local over a structured base
-> neighbouring descriptions require relational transport
-> connection
-> curvature.

The weak link is explicit: A1-A4 do not yet force the capitalised IF.

This is progress because the missing assumption is no longer vague. The project must explain why physically meaningless conventions should be independently selectable locally, and why a base/local-neighbourhood structure exists.

---

## New target T3.4 — Can locality itself emerge from distinguishability?
Instead of assuming a spacetime manifold, test whether A4's bounded/local observer information plus compositional independence can motivate a primitive adjacency/network structure:

finite distinguishable subsystems
+ restricted information exchange
-> interaction graph / causal adjacency
-> notion of local neighbourhood
-> local redundancy over that network
-> discrete connection/holonomy
-> continuum geometry only as a possible limit.

This route is preferable to simply assuming a differentiable spacetime, because otherwise T3.3 mostly reconstructs known gauge geometry.

### T3.4 success criterion
Derive at least a primitive adjacency/causal partial-order or interaction-network structure from independently motivated information/composition principles, without inserting Euclidean/Lorentzian geometry.

### T3.4 failure criterion
If adjacency/locality must simply be postulated, then the Canevas axioms have not derived the base geometry; T3.3 remains only a conditional reconstruction.

---

## Status
T3.3 RESULT: CONDITIONAL SUCCESS.

The mathematical implication
LOCAL REDUNDANCY + DIFFERENTIABLE COMPARISON => CONNECTION => CURVATURE
is robust.

But Canevas has not yet derived LOCAL REDUNDANCY, DIFFERENTIABLE BASE, or the dynamics of the connection.

## Anti-tuning lock
Do not choose G, dimension, metric, action, representations, or couplings because they reproduce electromagnetism, weak/strong interactions, gravity, Higgs physics, dark matter, or any measured constant.