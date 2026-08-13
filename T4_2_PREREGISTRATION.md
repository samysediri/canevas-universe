# CANEVAS T4.2 — Independent replication of support vs environmental predictive dependence

Status: PREREGISTERED BEFORE T4.2 NETWORK RESULTS

## Origin of hypothesis
T4.1's preregistered compression-ratio hypothesis was inconclusive. A secondary, post-hoc pattern appeared in several families: higher SUPPORT tended to correlate with lower held-out predictive gain supplied by the external environment. T4.2 treats that observation only as hypothesis generation and tests it on entirely new networks generated from a new random seed.

## Primary question
Within a network family, among subsystems for which the external environment has statistically validated predictive information about the subsystem future, is SUPPORT negatively associated with the held-out full-environment predictive gain?

Primary statistic per family:
Spearman rho(SUPPORT, FULL_ENVIRONMENT_HELDOUT_GAIN).

Predicted sign: NEGATIVE.

## Design lock
- New seed: 842021.
- Same six Boolean-network families as T4.1.
- 24 new networks per family.
- 8 candidate subsystems per network.
- N=24 nodes; subsystem size=4; burn-in=100; trajectory steps=600.
- Same SUPPORT construction as T4.1: geometric mean of memory, persistence, robustness.
- Same T4.1 train/calibration/test split and full-environment permutation significance machinery.
- Same parent cap/selection logic as T4.1 when the raw external-parent set exceeds MAX_PARENTS.
- Only subsystems classified as `valid=True` by the unchanged T4.1 full-environment predictive test enter the primary correlation.
- A family is evaluable only with >=30 valid subsystems and nondegenerate ranks.

## Primary verdict
`REPLICATES_NEGATIVE_ENVIRONMENTAL_DEPENDENCE` only if:
1. at least 4 families are evaluable;
2. >=75% of evaluable families have rho < 0;
3. median within-family rho <= -0.40.

`EVIDENCE_AGAINST_NEGATIVE_ENVIRONMENTAL_DEPENDENCE` if at least 4 families are evaluable and either:
- <=25% have rho < 0; or
- median rho >= -0.10.

Otherwise: `INCONCLUSIVE_T4_2`.

The -0.40 replication threshold is declared before T4.2 results. It is intentionally weaker than the roughly -0.6 to -0.75 post-hoc values that motivated T4.2, to require a meaningful but not identical independent effect.

## Secondary diagnostics (not part of confirmation)
Report within-family correlations of SUPPORT with memory, persistence, robustness, structural parent count, and T4.1 compression ratio where available. These are diagnostic only and cannot rescue the primary verdict.

## Interpretation lock
- A replication would establish only a property of these Boolean-network ensembles under these proxies.
- It would not establish consciousness, observerhood, emergent locality, anthropic selection, or Canevas cosmology.
- T4.1 remains historically inconclusive regardless of T4.2.
- No family weights, support formula, valid-subsystem rule, seed, threshold, or family definition may be altered after seeing T4.2.
- Any new hypothesis discovered in T4.2 requires another separately preregistered experiment.
