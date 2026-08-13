# SELF-LOCATION D3 — External demographic convergence test

Status: PREREGISTERED BEFORE D3 OUTPUT

## Purpose
D3 asks whether a demographic trajectory built from published population studies, without using the observed 1992 birth rank to choose its parameters, happens to generate a cumulative-birth scale close to the D2 self-location scale.

D3 is not an extinction forecast and not evidence for Canevas by itself.

## External demographic anchors
1. UN World Population Prospects 2024 medium world population in 2100: 10.180160751 billion.
2. UN World Population Prospects 2024 world life expectancy in 2100: 81.7342 years.
3. UN World Population to 2300 (2004) published long-range world-population endpoints for 2300:
   - LOW: 2.3 billion
   - MEDIUM: 9.0 billion
   - HIGH: 36.4 billion
4. The same UN long-range report states that world life expectancy in its long-term scenarios exceeds roughly 95 years by 2300. D3 uses exactly 95 years as its preregistered 2300 turnover-timescale anchor.
5. Cumulative births through 2100 are fixed at 127.036804776 billion from D1.1's historical + WPP2024 birth reconstruction. This is demographic bookkeeping; D3 does not use the observed 1992 rank to alter it.

## Demographic bridge
For each LOW/MEDIUM/HIGH scenario, population P(t) is linearly interpolated from the WPP2024 medium 2100 population to the corresponding independent 2300 long-range endpoint.

Life expectancy/turnover timescale L(t) is linearly interpolated from 81.7342 years in 2100 to 95 years in 2300.

Annual births are approximated by the stationary-turnover relation

B(t) = P(t) / L(t).

This is explicitly an approximate demographic bridge, not an official UN birth projection to 2300.

The cumulative births generated between 2101 and 2300 are integrated before any comparison with D2 or the observed rank.

## Post-2300 continuation diagnostic
After 2300, each scenario is continued at its 2300 population and L=95 years solely to calculate the calendar year at which selected externally supplied cumulative-birth targets would be crossed.

The demographic trajectory itself is frozen before those targets are supplied.

## Comparison targets opened only after demographic trajectory is constructed
- observed-rank exact-median target: 2r = 225.960076712 billion births
- D2 LOG_UNIFORM + SSA posterior median: 225.957 billion births
- D2 LOGNORMAL + SSA posterior median: 265.100 billion births

These targets must not modify P(t), L(t), the 2100/2300 anchors, interpolation, or turnover formula.

## Predeclared interpretation
A convergence is labelled SCALE_OVERLAP only if a demographic scenario reaches the D2 LOG_UNIFORM+SSA median between years 2300 and 5000 under the frozen stationary post-2300 continuation.

It is labelled NO_NEAR_TERM_SCALE_OVERLAP if none does.

This label is descriptive only. Even SCALE_OVERLAP would not validate SSA, predict extinction, or establish Canevas.

## Interpretation lock
- Population projections are not extinction forecasts.
- The 2004 long-range projections are old and highly assumption-sensitive; that is part of the test, not hidden uncertainty.
- B=P/L is a turnover approximation, not a cohort-component demographic model.
- D3 is useful mainly as an order-of-magnitude independence check.
- No scenario may be selected after the result because it best matches the observed rank.
