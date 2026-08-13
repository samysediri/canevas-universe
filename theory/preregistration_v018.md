# Canevas v0.18 — preregistration / freeze point

Date: 2026-08-12

## Purpose

Freeze the current distinguishability framework before testing any additional cosmological parameter.

## What is frozen

1. Parameter-space geometry is relational: local metric is built from physical-observable changes, not raw coordinate distance.
2. Base form: `g = J^T W J`, with local volume element proportional to `sqrt(det(g))`.
3. Primary observable family: log matter power `P(k,z)` plus expansion history `H(z)`.
4. Reference epochs previously used: `z = 0, 2, 6`.
5. Reference matter-power scales previously used: logarithmic `k` sampling from about `1e-2` to `5 1/Mpc`.
6. CLASS is the Boltzmann solver.
7. Rejected CLASS cosmologies are never interpolated. Only fully valid local cells are used.
8. Robustness is assessed over a predeclared family of positive-semidefinite observable weightings `W`; degenerate metrics are reported, not repaired.
9. No anthropic/complexity score is part of the distinguishability-only test.
10. Existing successful values for zeta and Lambda must not be used to retune the framework.

## Retrospective contamination disclosure

A genuinely blind prediction of standard LCDM parameters is no longer possible inside this project because previous versions explicitly fixed several observed values (`h`, `Omega_m`, `Omega_b`, `A_s`, `n_s`, flat geometry, and `w=-1`) while the metric family was being developed. Merely hiding those values from a future script would not undo that information exposure.

Therefore v0.18 does **not** claim a blind prediction of `n_s`, `A_s`, `h`, curvature, or other parameters already used as fixed inputs.

## Next valid test class

The next prospective test must satisfy all of the following:

- introduce a sector/degree of freedom that was not used to tune the v0.13–v0.17 metric family;
- define its scan domain and CLASS implementation before examining the resulting distinguishability distribution;
- leave the frozen metric rules unchanged;
- report failure, boundary preference, degeneracy, and numerical rejection without post-hoc repair;
- compare against empirical information only after the model output has been saved.

## Scientific status at freeze

The robust result so far is **not** that Canevas predicts the observed constants. It is narrower:

> Within the tested finite cosmological domains and observable families, a class of relational distinguishability metrics places the observed dark-matter-to-baryon ratio near the centre of the induced measure, and places the joint `(zeta, Lambda)` point in a non-extreme region.

This remains conditional on the added metric hypothesis and does not establish the philosophical axioms.
