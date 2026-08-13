# CANEVAS T4 — Latent predictive representation

Status: PREREGISTERED BEFORE NETWORK RESULTS

## Why T4 exists
T3.9 is closed. Its structural small-boundary signal did not replicate robustly within families, and its predictive-interface metrics failed synthetic validation or measured access-channel count rather than latent generative dimension. T4 is a new question, not a repair of T3.9.

## T4 question
Can a bounded persistent information-processing subsystem interact with a high-dimensional environment through a lower-dimensional predictive representation?

We distinguish:
- structural boundary size: number of external connections;
- access dimension: number of observed channels needed for prediction;
- latent predictive dimension: dimension of a compressed representation Z that preserves predictive information about the subsystem's future.

Target relation:
P(S[t+1] | S[t], E[t]) ~= P(S[t+1] | S[t], Z[t])
with Z lower-dimensional than E when the environment contains redundant predictive structure.

This is an instrument-development branch first. It is NOT evidence for consciousness, observers, anthropic selection, or Canevas cosmology.

## Synthetic controls before any network experiment
A T4 instrument must be tested on predeclared cases:
1. NULL_NOISE: 8 external channels, none predictive -> latent predictive dimension should be 0.
2. ONE_CAUSE_REDUNDANT: 8 noisy measurements of one latent binary cause -> representation should behave as one latent source, not eight independent causes.
3. FOUR_CAUSES: 8 channels containing four independent predictive causes -> effective predictive complexity must be clearly greater than ONE_CAUSE_REDUNDANT.
4. NUISANCE_RICH: many high-variance external channels plus one predictive latent cause -> nuisance dimensionality must not inflate predictive complexity substantially.
5. SYNERGY_XOR: future depends jointly on multiple causes with zero/weak univariate information -> method must not declare dimension 0 merely because marginal tests fail.

## Primary preregistered ordering
The first T4 instrument is considered promising only if, on untouched synthetic test data:
NULL_NOISE < ONE_CAUSE_REDUNDANT < FOUR_CAUSES
and NUISANCE_RICH remains close to ONE_CAUSE_REDUNDANT, while SYNERGY_XOR is detected as non-null.

No numeric threshold will be selected after seeing a failed run. A failed implementation may be diagnosed, but any changed estimator/cutoff/case definition receives a new version and new preregistration.

## Interpretation lock
- Passing synthetic controls validates only the measurement procedure on those controls.
- No synthetic pass supports Canevas axioms.
- No observer/consciousness language may be inferred from persistence alone.
- T3.9 correlations are not resurrected by T4.
- Only after an instrument passes synthetic controls may a new, separately preregistered network experiment be run.
- Any network result must be tested across families and against appropriate null/shuffled controls.

## First implementation target
T4.0 should estimate predictive compression without pretending that raw subset size equals latent causal dimension. The first implementation should compare predictive performance of deliberately compressed representations against full-environment performance, with held-out evaluation and null controls. It should report a predictive-compression curve rather than a single metaphysical 'observer dimension'.
