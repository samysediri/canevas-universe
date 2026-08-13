# CANEVAS T4.1 — Network predictive-compression experiment

Status: PREREGISTERED BEFORE NETWORK RESULTS

## Instrument lock
T4.1 uses the predictive-compression logic validated in T4.0b. T4.0 remains a historical failure; T4.0b is the validated synthetic instrument. No T4.1 parameter may be changed after seeing T4.1 results under the same label.

## Question
Within broad Boolean-network families, are persistent information-processing subsystems associated with more compressible predictive representations of their environments?

This is NOT a consciousness test and does not establish observerhood.

## Network families
Use the same six broad families previously used for T3.9, but T4.1 is a new experiment:
- sparse_random
- dense_random
- modular
- local_ring
- global_majority
- hierarchical

## Fixed design
- N nodes = 24
- subsystem size = 4
- networks per family = 20
- candidate subsystems per network = 8
- burn-in = 100
- sampled transitions = 600
- random seed fixed in code before run

## Support score
Reuse the T3.9 narrow information-processing proxy only as a ranking variable:
- temporal memory
- non-frozen persistence/activity
- perturbation robustness
combined by geometric mean.

This is not called consciousness.

## Predictive-compression outcome
For each subsystem:
1. Define E_t as all external structural parents of subsystem nodes.
2. Estimate the held-out predictive gain of E_t for S_{t+1} conditional on S_t.
3. If the full environment is not significant against a permutation null, label the subsystem NO_PREDICTIVE_ENVIRONMENT and exclude it from the primary compression-ratio correlation.
4. Otherwise construct candidate compressed binary features using the same finite T4.0b family where computationally feasible: raw channels, XOR features up to order 4, and majority features. To cap combinatorics, if E has >8 parent channels, choose 8 parent channels on TRAIN DATA ONLY using train conditional predictive gain, then freeze them.
5. Find the smallest code size k in {1,2,3,4} that retains >=90% of the full-environment held-out predictive gain and is significant on calibration data against a permutation null.
6. Define compression ratio C = k / min(8, |E|). Smaller C = stronger predictive compression.

If no k<=4 reaches 90%, set k=5 (censored-above-range) and C=5/min(8,|E|), reported explicitly.

## Primary statistic
For each family separately, compute Spearman rho between SUPPORT and COMPRESSION_RATIO among subsystems with a significant predictive environment.

Predeclared direction supporting the hypothesis:
POSITIVE rho if larger C means worse compression? No. Since smaller C = better compression, the hypothesised association 'higher support -> better compression' predicts NEGATIVE rho.

Primary family-level summary:
- median within-family rho
- fraction of evaluable families with rho < 0

## Primary preregistered verdict
SUPPORTS_T4_COMPRESSION_ASSOCIATION only if:
1. at least 4 families are evaluable with >=30 valid subsystems each;
2. >=75% of evaluable families have rho < 0;
3. median within-family rho <= -0.20.

EVIDENCE_AGAINST_T4_COMPRESSION_ASSOCIATION if:
1. at least 4 families are evaluable; and
2. <=25% of evaluable families have rho < 0 OR median rho >= +0.20.

Otherwise: INCONCLUSIVE_T4_1.

## Secondary outcomes
Report, but do not use to change the primary verdict:
- full-environment predictive gain vs support;
- k distribution by family;
- fraction NO_PREDICTIVE_ENVIRONMENT by family;
- structural parent count vs support;
- top/bottom support quartile compression ratio within family.

## Null and sensitivity locks
- Use permutation nulls that independently permute external channels relative to S_t/S_{t+1} while preserving channel marginals.
- Selection occurs on train data; significance on calibration; final gain/compression retention on untouched test data.
- Family weights are equal in the primary family-level summary regardless of number of valid subsystems.
- No family may be dropped because its result is inconvenient; only the predeclared evaluability threshold applies.
- Do not change 90%, k<=4, support formula, network families, or family weights after seeing results.

## Interpretation lock
A positive result would support only the narrow claim that persistent information-processing proxies are associated with predictive environmental compression in these model ensembles. It would NOT establish consciousness, observer measure, emergent locality, anthropic selection, or Canevas cosmology.
A null/negative result must be reported as such and cannot be repaired by post-hoc family selection.
