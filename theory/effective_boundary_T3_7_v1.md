# Canevas 1.0 — T3.7 Effective boundary / Markov-blanket stress test

## Goal
Test whether A4-style bounded experience can force an effective information boundary for a persistent observer-like subsystem, even if the underlying universe is fundamentally nonlocal.

This is NOT a claim that literal biological skins or spatial surfaces are fundamental. The target is weaker: conditional separation in the dynamics/statistics.

---

## Setup
Partition a total system into:
- I: internal state of a candidate observer/subsystem;
- E: external degrees of freedom;
- B: a proposed effective boundary/interface variable.

A strong Markov-blanket-style condition would be, schematically,

I_future ⟂ E_distant | (I_present, B)

meaning that once the present internal state and boundary variables are specified, distant environment variables add no further predictive information about the next internal state.

Equivalent information-theoretic form:

I(I_future ; E_distant | I_present, B) = 0.

Approximate versions allow this conditional mutual information to be small rather than exactly zero.

---

# Candidate derivation D1 — Bounded accessible information

A4 motivates that an observer cannot encode unrestricted total information about the Canevas.

This implies only a capacity/access bound such as

H(I) < infinity

or, more generally, finite effective accessible information at an observer-moment.

It does NOT imply that the environment influences I only through a small mediator B.

Counterexample:
Let I be one bit and let E contain N bits e_1...e_N. Define

I_{t+1} = XOR(e_1,...,e_N).

I remains finite and perfectly well-defined while depending irreducibly on arbitrarily many external variables in one update. No small boundary variable is forced unless one defines B to be the already-compressed XOR itself, which simply repackages the global dependence.

VERDICT: BOUNDED INFORMATION DOES NOT IMPLY A NONTRIVIAL MARKOV BLANKET.

---

# Candidate derivation D2 — Persistent identity

Hypothesis:
A persistent observer/subsystem must retain some predictable relation between I_t and I_{t+1}; perhaps this requires shielding from arbitrary environmental details.

Counterexample:
Let

I_{t+1} = I_t XOR f(E_t)

where f is a deterministic global function of the full environment. If f is itself stable/predictable or highly constrained by global dynamics, I can remain persistent and structured despite direct global dependence.

More generally, dense/global coupling does not logically preclude attractors, error-correcting structures, synchronized modes, or stable low-dimensional collective variables.

VERDICT: PERSISTENCE ALONE DOES NOT FORCE CONDITIONAL SEPARATION.

---

# Candidate derivation D3 — Partial autonomy

Define a stronger property:
A subsystem is partially autonomous if its future can be predicted to some accuracy using a bounded set of internal/interface variables without conditioning on the entire environment.

Then by definition there exists some statistic B(E) such that

P(I_future | I_present, E) ≈ P(I_future | I_present, B(E)).

This DOES give an effective boundary/compression.

But note the logic:

PARTIAL AUTONOMY => EFFECTIVE SUFFICIENT INTERFACE.

This is almost definitional. A4 does not yet prove partial autonomy.

VERDICT: CONDITIONAL SUCCESS, NOT DERIVED FROM A4.

---

# Exact versus trivial boundaries

A dangerous loophole is to set B=E. Then

I_future ⟂ E | (I_present,B)

holds trivially because B contains the entire environment.

Therefore a meaningful effective boundary must satisfy a compression/nontriviality condition, for example:

H(B) << H(E)

or lower effective dimension/complexity than E, while retaining most predictive information about I_future.

One possible optimisation target is an information bottleneck:

min_B I(B;E)
subject to
I(I_future;E | I_present,B) <= epsilon.

This formalises the idea of the smallest interface that preserves prediction of the subsystem.

IMPORTANT: choosing the information-bottleneck criterion is additional mathematical structure, not derived from A1-A4.

---

# Main counterexample — finite globally coupled observer

Construct a universe with environment E of arbitrarily large dimension and a finite observer state I of k bits. Let the update be

I_{t+1}=F(I_t,E_t)

where F is a generic hash-like/global function with high conditional dependence on all coordinates of E.

Such a system can still:
- have finite I;
- possess multiple distinguishable states;
- have temporal correlations/memory if F is designed accordingly;
- be physically instantiated as a finite subsystem;
- lack any low-complexity B that screens I_future from E.

Thus an observer-like finite state is logically compatible with irreducible global dependence.

This defeats the strong theorem:

BOUNDED EXPERIENCE => SMALL EFFECTIVE BOUNDARY.

---

# What survives

A weaker and useful statement survives:

If an observer/subsystem has PARTIAL DYNAMICAL AUTONOMY, then its interaction with the rest of the universe can be summarised by an effective interface/sufficient statistic at the scale of interest.

Symbolically:

partial autonomy
=> predictive compression of environment
=> effective boundary B
=> observer-relative/effective locality.

This locality can emerge even when fundamental microphysics is nonlocal.

However, partial autonomy is an extra physical property. It is not implied solely by finite consciousness.

---

# Relation to Markov blankets

In probabilistic graphical models, a Markov blanket is the set of variables that screens a node/set from the rest of the graph. Such blankets exist relative to a specified factorisation/graph and can sometimes characterise subsystem boundaries.

But the existence of a useful small blanket is NOT automatic for an arbitrary joint distribution or arbitrary dynamics. A complete graph may give a blanket containing nearly the whole environment.

Therefore invoking 'Markov blanket' does not solve the Canevas locality problem unless the factorisation/sparsity that makes the blanket small is independently derived.

---

# T3.7 verdict

STRONG CLAIM:
A4 / bounded experience => nontrivial Markov blanket.

VERDICT: FALSE IN GENERAL.

WEAKER CLAIM:
Partial dynamical autonomy => effective predictive boundary.

VERDICT: TRUE BY STANDARD SUFFICIENCY/CONDITIONAL-INDEPENDENCE STRUCTURE, but partial autonomy is additional physics.

This means observer-relative local appearance is possible without fundamental locality, but it is not forced by the Canevas axioms currently stated.

---

# New target T3.8 — Why partial autonomy?

The remaining question is now extremely sharp:

Why should the space of physically realised histories contain persistent low-dimensional subsystems with compressible interfaces rather than only globally entangled/all-to-all dynamics?

Candidate routes to test WITHOUT using observed constants:

A. Dynamical attractors / error correction:
Persistent observer-like structures may require metastable attractors that automatically suppress most environmental degrees of freedom.

B. Thermodynamic nonequilibrium:
Maintaining an organised subsystem may require a restricted set of fluxes through an interface, potentially making an effective boundary physically generic.

C. Algorithmic/generative measure:
If M_dyn strongly favours simpler/compressible generative laws, histories with modular partially autonomous structures might receive more measure than arbitrary global hash-like couplings.

D. Selection conditional on observers:
Even if non-autonomous worlds dominate globally, conditioning on the existence of persistent observers may select the rare subset with effective autonomy. This would be an anthropic/conditional statement, not a fundamental-law derivation.

## T3.8 success criterion
Show that at least one independently justified dynamical/generative principle makes partial autonomy generic or overwhelmingly weighted, without inserting spatial locality or known biology.

## T3.8 failure criterion
If modular autonomy must simply be postulated or selected anthropically, then effective locality remains contingent rather than a fundamental prediction of Canevas.

---

## Anti-tuning lock
Do not choose an autonomy measure, bottleneck size, entropy flux, attractor form, or generative simplicity prior because it reproduces our observed local world, life, 3+1 dimensions, Standard Model physics, dark matter, Higgs parameters, or any previous numerical target.