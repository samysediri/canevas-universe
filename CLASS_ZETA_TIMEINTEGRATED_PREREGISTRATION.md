# CLASS ZETA-T1 — preregistration

## Question
Can a single non-anthropic, time-integrated structure/cooling proxy select one dark-matter-to-baryon ratio zeta without choosing a redshift after seeing the observed value?

## Locked inputs
- h = 0.674
- total physical matter density omega_m = 0.315*h^2
- A_s = 2.10e-9
- n_s = 0.965
- YHe = 0.245
- spatially flat background with Omega_m fixed
- zeta scan = 0.5 to 30 on a fixed logarithmic grid of 49 points, plus zeta=1
- redshift grid = [12,10,8,6,4,3,2,1,0.5,0]

For each zeta:
omega_b = omega_m/(1+zeta)
omega_cdm = omega_m-omega_b

The observed zeta (~5.389) is NOT used in the score or to choose an epoch.

## Primary score
At each redshift CLASS supplies P(k). A Sheth-Tormen halo mass function and the already-used atomic-cooling efficiency proxy generate F_cool(z,zeta), the fraction of total matter in cooling-capable halos weighted by baryon fraction.

The single primary score is the cosmic-time integral

    J(zeta) = integral F_cool(t,zeta) dt

from z=12 to z=0. This is interpreted only as cooling-capable baryon-time per unit total matter. It is not consciousness, life, or an anthropic score.

## Primary prediction
zeta_pred is the valid grid point maximizing J(zeta).

No redshift window, weighting, scan range, cooling threshold, or cosmological parameter may be changed after seeing ZETA-T1 output under the same label.

## Locked reporting
After zeta_pred is fixed, report:
- zeta_pred
- whether the maximum is interior or at a valid-domain boundary
- observed/peak score ratio at zeta_obs=5.389452
- multiplicative distance max(zeta_pred/zeta_obs, zeta_obs/zeta_pred)

Interpretation labels:
- boundary maximum: BOUNDARY_NO_FINITE_SELECTION
- interior and multiplicative distance <= 1.25: CLOSE_NUMERICAL_OVERLAP
- interior and distance <= 2: BROAD_ORDER_OVERLAP
- otherwise: NO_CLOSE_OVERLAP

These labels describe only this proxy. None is evidence for Canevas by itself.

## Next-step lock
A positive T1 result must be stress-tested with predeclared metric/physics variants before comparison can be promoted. A negative result is retained and not repaired under T1.
