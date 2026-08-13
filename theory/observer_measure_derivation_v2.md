# Canevas 1.0 — Observer-measure derivation v2

## Goal
Attempt to derive a reference class / observer measure from the Canevas axioms without using the user's birth year, technology dates, cosmological constants, or any previously observed numerical success.

This document separates what is logically necessary from what remains an additional hypothesis.

---

## Starting point
A4 (current form): a determined conscious experience requires limits / local determination.

We interpret this minimally as:
- an experience cannot simultaneously contain unrestricted access to all information in the Canevas;
- an experience must instantiate at least two distinguishable internal possibilities, otherwise there is no informational distinction to constitute a determinate content;
- if an experience has temporal continuity or memory, there must be physical correlations linking successive local states.

None of these statements yet implies biology, Homo sapiens, birth, language, technology, or a specific neural architecture.

---

## Definitions

### D1 — Local observer-state
A local observer-state O is a physically instantiated subsystem/state satisfying, at minimum:
1. bounded informational access: O does not encode the complete state of the total Canevas;
2. distinguishability: O contains at least two physically distinguishable internal macrostates;
3. environmental coupling: O is correlated with some states outside itself;
4. if temporal identity/memory is claimed, there exists a chain of correlations linking O_t to O_{t+dt}.

This is deliberately substrate-neutral.

### D2 — Observer-moment
An observer-moment is one locally determined experiential state O_t, not an entire biological lifetime.

### D3 — Equivalence class of observer-moments
Two observer-moments are equivalent relative to a question Q if they contain the same Q-relevant information up to physically irrelevant relabelling.

This is critical: self-location should condition on the information actually present in the observer-state, not on arbitrary facts unavailable to that state.

---

## Candidate theorem T1 — Reference-class locality

If self-location uncertainty concerns "which locally realised experience is this one?", then the broadest admissible reference class is not 'all humans' or 'all births', but the set of locally realised observer-moments compatible with the information contained in the current observer-state.

Formally, for current observer information I:

R(I) = { O_i : O_i is a valid local observer-moment and O_i is compatible with I }.

### Status
CONDITIONAL, not yet a theorem.

What follows from A4:
- locality / boundedness of an observer-state is motivated.

What does NOT follow yet:
- that probabilities must be uniform over elements of R(I);
- how duplicate observer-moments are counted;
- whether physically identical copies count separately;
- whether duration, computational steps, entropy production, algorithmic complexity, or branch amplitude changes the weight.

---

## Candidate theorem T2 — Conditioning principle

A self-location calculation must not condition on information unavailable to the observer-state at the moment being sampled.

Reason: using hidden external labels (e.g. exact universe ID, future history, arbitrary coordinate labels) distinguishes otherwise identical local experiences by information that is not part of the experience itself.

This gives a candidate invariance principle:

If O_a and O_b are internally identical with respect to all information I available to the observer, then a self-location rule should not assign different probabilities merely because an external bookkeeping label differs.

### Status
STRONG CANDIDATE PRINCIPLE.

It resembles label invariance / indifference under physically irrelevant relabelling, but it still does not define the measure uniquely.

---

## Candidate measure family

Given compatible local observer-moments O_i in R(I), write

P(O_i | I) ∝ w(O_i).

A4 + label-invariance appears to forbid weights depending purely on arbitrary external labels. But many non-arbitrary weights remain possible:

- w = 1 per physical occurrence;
- w ∝ duration represented by the observer-moment discretisation;
- w ∝ number of computational transitions;
- w ∝ branch/Born weight in quantum models;
- w ∝ entropy production;
- w ∝ integrated information or another consciousness functional;
- w ∝ algorithmic multiplicity;
- other physically defined measures.

Therefore the Canevas axioms currently define, at best, a restricted FAMILY of admissible observer measures, not a unique one.

---

## Important consequence for previous tests

### Birth-year analysis
'All Homo sapiens births' is not derived as the fundamental reference class.
It was a useful diagnostic only.

### Technology ladder
Conditioning on writing, electricity, computing, Web, etc. approximated progressively richer information I, but the milestones were historical proxies, not the fundamental definition of R(I).

### Doomsday / SSA / SIA
SSA corresponds roughly to a particular counting rule over occurrences.
SIA introduces an additional multiplicity weighting.
Neither is currently derived from A4.

Thus:

A4 -> local observer-state -> compatibility class R(I)

is substantially better motivated than:

A4 -> SSA
or
A4 -> SIA.

---

## New falsification target

The next task is NOT to fit the user's birth year.
It is to test whether the candidate compatibility-class rule produces contradictions or paradoxes.

Predeclared counterexamples:

C1 — Exact duplicate observers
Two physically distinct but internally identical copies. Should they have equal conditional weight?

C2 — Sleeping Beauty / temporal duplication
One physical person generates multiple indistinguishable observer-moments. Does counting moments versus persons change probabilities?

C3 — Long-lived versus short-lived observers
If one observer has 10x as many compatible observer-moments, is self-location 10x more likely there?

C4 — Simulation multiplicity
If identical observer-moments are instantiated one million times in simulations, should multiplicity matter?

C5 — Quantum branching
If identical observer-states occur on branches with different amplitudes, occurrence-counting and Born weighting disagree.

C6 — Boltzmann-brain style duplicates
A theory may generate enormous numbers of fleeting observer-moments with matching local memories. A naive occurrence measure can become dominated by them.

Any unique Canevas measure must handle these without post-hoc exceptions.

---

## Provisional conclusion

The strongest result currently available is:

1. A4 plausibly motivates local / bounded observer-states.
2. Self-location should condition on information internal to the observer-state rather than arbitrary external labels.
3. This naturally replaces an arbitrary biological reference class with a compatibility class R(I).
4. The axioms still do NOT provide a unique weighting w(O).
5. Therefore the fundamental unsolved problem is no longer primarily 'which humans count?' but 'what physically determines measure over compatible local observer-moments?'

This is the same structural issue previously encountered in cosmological measure tests.

---

## Anti-tuning rule

Do not choose w(O) because it makes 1992 typical, rescues the Doomsday intuition, reproduces zeta, or matches any other known observation.

A candidate w must be justified independently, then tested prospectively on self-location paradoxes and physical observations.
