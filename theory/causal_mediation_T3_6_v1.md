# Canevas 1.0 — T3.6 Causal mediation audit

## Goal
Determine whether a primitive "causal mediation" principle is genuinely weaker/more informative than simply postulating locality.

Candidate principle CM:
Any influence between distinguishable subsystems/events is represented by a composable chain of elementary dependence relations. No metric distance or pre-existing spacetime is assumed.

The question is whether CM yields new structure, or merely renames locality.

---

## 1. Minimal formalisation
Let V be distinguishable subsystems/events. Let E be a set of elementary directed dependence relations. A composite influence u => v exists iff there is a finite directed path

u = x_0 -> x_1 -> ... -> x_n = v.

The primitive relation is E. Reachability E* is derived by path composition.

This immediately distinguishes:
- elementary dependence: one edge;
- mediated/composite dependence: path length >= 2.

No metric is used.

---

## 2. Is CM different from locality?
Not automatically.

If one allows E to contain every ordered pair (u,v), then CM is satisfied trivially: every influence is a one-edge path. Thus CM alone permits an all-to-all complete graph.

Therefore:

CM != sparse locality.

Causal mediation by itself does NOT imply finite degree, finite propagation speed, dimensionality, or neighbourhood structure beyond the chosen elementary-edge relation.

VERDICT: CM alone is too weak to derive locality.

---

## 3. Can "irreducible" elementary edges help?
Define an edge u->v as irreducible if the dependence cannot be reproduced by composition through other available subsystems while preserving the same intervention/statistical effect.

This creates a minimal causal graph only relative to a specified factorisation and notion of causal equivalence.

Problems:
1. different latent-variable choices can change which edges are irreducible;
2. a complete graph can still be irreducible if every pair has a genuine direct coupling;
3. irreducibility does not imply sparsity;
4. quantum/nonclassical causal structure may not admit a simple classical directed-graph interpretation.

VERDICT: useful structural definition, but not a derivation of locality.

---

## 4. Nontrivial consequence of CM: path composition / categorical structure
Although CM does not force sparsity, it does impose a compositional organisation if taken seriously.

Elementary processes can be composed sequentially when outputs/inputs match. This suggests a process category-like structure:
- objects: subsystem/state interfaces;
- morphisms: allowed processes/influences;
- composition: sequential mediation;
- identity: do-nothing process.

Parallel composition can be added if independent subsystems can coexist.

This is a genuine consequence stronger than raw set-theoretic possibility, but it remains kinematic. Many local and nonlocal theories share it.

VERDICT: STRUCTURAL SUCCESS, NOT LOCALITY DERIVATION.

---

## 5. What extra principle would actually exclude all-to-all irreducible coupling?
At least one additional restriction is needed. Candidate families:

### B1 — Bounded elementary fan-in/fan-out
Each primitive event has at most K direct parents/children at a given resolution.
This directly yields finite-degree locality, but essentially postulates a capacity/locality bound.

### B2 — Finite information-transfer capacity per elementary relation
Each edge transmits a bounded amount of independent information per update.
This does not alone bound the number of edges; an event could have infinitely many finite-capacity inputs unless total capacity is also bounded.

### B3 — Bounded total elementary update capacity
The total independently controllable information entering/leaving a primitive subsystem per elementary step is finite.
Combined with a nonzero minimum information quantum per independent channel, this can imply finite effective degree.
But the minimum-channel assumption is additional.

### B4 — Factorisation / conditional independence
Require that sufficiently separated subsets can be conditionally independent given a boundary/mediator set.
This can imply sparse graphical structure, but "sufficiently separated" or the existence of small separators is itself an extra structural assumption.

### B5 — Markov blanket principle
Every persistent subsystem has a finite/small interface B such that its internal state is conditionally screened from the rest by B.
This directly formalises a stable informational boundary.
It is much closer to A4, but A4 currently says observer information is bounded; it does NOT prove that the world's causal graph has finite Markov blankets.

---

## 6. Strongest possible bridge from A4
A4 can motivate the following OBSERVER-level statement:

For a bounded observer O, there exists a set of accessible interface variables B such that all information O receives from the rest of the world is mediated through B during the relevant experience.

Symbolically, at an effective stochastic level one may seek

O_future ⟂ Environment_remote | (O_present, B)

or an analogous quantum conditional-independence statement.

If such a finite/small B exists, O has an effective Markov blanket/interface.

Important:
This does NOT imply every fundamental subsystem has such a blanket, nor that microscopic spacetime is local.

VERDICT: A4 plausibly motivates EFFECTIVE MEDIATION AT OBSERVER BOUNDARIES, not universal fundamental locality.

---

## 7. New conceptual result: locality may be scale-relative
The repeated failures T3.5-T3.6 suggest a useful reformulation:

Fundamental all-to-all dependence may coexist with emergent subsystems whose effective dynamics has sparse interfaces/Markov blankets after coarse-graining.

Therefore the Canevas may not need to derive microscopic locality from A4. A weaker and more relevant target is:

bounded experience
-> finite effective interface
-> emergent local causal neighbourhood for the observer/subsystem.

This could explain why local spacetime descriptions are operationally natural without claiming they are ontologically fundamental.

This is a conceptual shift and should be tested, not assumed.

---

## 8. T3.6 verdict

FAILED AS A FUNDAMENTAL LOCALITY DERIVATION.

CM alone:
- permits complete/all-to-all elementary graphs;
- does not imply finite degree;
- does not imply finite signal speed;
- does not imply geometry or dimension.

SUPPORTED:
- causal influence can be organised compositionally into elementary and mediated processes;
- A4 may motivate finite effective mediation/interface for observer-like subsystems;
- an effective Markov-blanket route is more defensible than claiming universal microscopic locality.

---

## New target T3.7 — Effective boundary / Markov-blanket theorem attempt
Test whether a locally determined persistent observer-state necessarily requires an effective finite interface B mediating information exchange with the environment.

Success criterion:
Derive a precise conditional-independence/interface statement from definitions of bounded accessible information + persistent distinguishability, without assuming spatial locality.

Failure criterion:
Construct a coherent observer-like subsystem with bounded internal information but irreducibly all-to-all environmental dependence and no finite/small screening interface.

If counterexamples exist, even effective locality is not derived from A4.

## Anti-tuning lock
Do not define the interface, graph, degree, update scale, or conditional-independence criterion to reproduce known spacetime locality, c, 3+1 dimensions, GR, gauge theories, Standard Model fields, cosmological constants, Higgs physics, dark matter, life, or the user's birth-era observations.