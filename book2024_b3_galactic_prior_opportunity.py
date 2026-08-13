"""BOOK2024-B3 — GALACTIC PRIOR OPPORTUNITY TEST v1

Book anchor: chapter-6 finite technological civilizations / Fermi silence.
External astrophysical anchor: published estimates suggest many terrestrial
planets / GHZ stars are older than Earth/Sun, with a representative mean age
lead around 1.8 +/- 0.9 Gyr and roughly 75% older.
Internal prior result: BOOK2024-B2 produced Galactic settlement crossing times
with median ~33.3 Myr and maximum ~331 Myr across the preregistered grid.

Purpose
-------
Quantify how much extra biological/technological delay an older world could
have relative to Earth and STILL retain enough temporal head start for a
B2-style settlement front to cross the Galaxy before our technological era.

CRITICAL LIMIT
--------------
This does NOT assume older planets host older civilizations. It explicitly
models an unknown extra emergence delay Delta_bio. The test only maps the
region where the simple timing opportunity exists.

PREDECLARED VALUES
------------------
Age-lead scenarios (Gyr): 0.9, 1.8, 2.7  (representative mean +/- 1 sigma)
Settlement times (Gyr): 0.033331, 0.331   (B2 median and conservative max)
Extra emergence delays Delta_bio (Gyr):
0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0

Opportunity margin = age_lead - Delta_bio - settlement_time.
Positive margin means only that a hypothetical earlier civilization had enough
clock time for B2-style propagation; it does not imply civilization arose,
expanded, survived, or would be detectable.
"""

AGE_LEADS_GYR = [0.9, 1.8, 2.7]
SETTLEMENT_GYR = {
    "B2_MEDIAN": 0.033331,
    "B2_CONSERVATIVE_MAX": 0.331,
}
DELTA_BIO_GYR = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
OLDER_FRACTION_REFERENCE = 0.75


def main():
    print('='*80)
    print('BOOK2024-B3 — GALACTIC PRIOR OPPORTUNITY TEST v1')
    print('='*80)
    print('Maps timing opportunity only. Older planet != older civilization.\n')

    positive = 0
    total = 0
    per_settlement = {}

    for label, tsettle in SETTLEMENT_GYR.items():
        npos = 0
        ntot = 0
        print(f'[{label}] settlement_time={tsettle:.6f} Gyr')
        for lead in AGE_LEADS_GYR:
            critical_delay = lead - tsettle
            print(f'  age_lead={lead:.1f} Gyr critical_extra_delay={critical_delay:.6f} Gyr')
            for delay in DELTA_BIO_GYR:
                margin = lead - delay - tsettle
                ok = margin > 0.0
                print(f'    Delta_bio={delay:>4.2f} margin={margin:+.6f} Gyr opportunity={ok}')
                npos += int(ok)
                ntot += 1
                positive += int(ok)
                total += 1
        per_settlement[label] = npos / ntot
        print()

    # At the representative 1.8 Gyr mean lead, calculate direct thresholds.
    mean_lead = 1.8
    thresholds = {k: mean_lead - v for k,v in SETTLEMENT_GYR.items()}

    print('PREDECLARED BOOK2024-B3 SUMMARY')
    print('reference fraction of terrestrial/GHZ systems older than Earth/Sun ~=', OLDER_FRACTION_REFERENCE)
    for k,v in thresholds.items():
        print(f'at 1.8 Gyr age lead, max extra emergence delay retaining opportunity under {k} = {v:.6f} Gyr')
    for k,v in per_settlement.items():
        print(f'fraction of preregistered lead-delay cells with positive timing opportunity [{k}] = {v:.6f}')
    print('overall positive timing cells =', positive, '/', total, '=', positive/total)

    # Interpretation is deliberately conditional, not a claim of Fermi resolution.
    mean_median_positive = thresholds['B2_MEDIAN'] > 1.5
    mean_max_positive = thresholds['B2_CONSERVATIVE_MAX'] > 1.0

    if mean_median_positive and mean_max_positive:
        verdict = 'OLDER_WORLDS_ALLOW_GYR_SCALE_DELAY_AND_STILL_LEAVE_SETTLEMENT_TIME'
    else:
        verdict = 'TIMING_OPPORTUNITY_WEAK_UNDER_CONSERVATIVE_DELAYS'

    print('PREDECLARED BOOK2024-B3 VERDICT =', verdict)
    print('\nINTERPRETATION LOCK:')
    print('- Positive opportunity is necessary timing room only, never evidence that civilizations existed.')
    print('- Planet age is not civilization age; Delta_bio explicitly carries that uncertainty.')
    print('- B3 does not infer civilization lifetime, expansion probability, or detectability.')
    print('- A Fermi constraint requires an independent model for emergence rate, expansion fraction, persistence, and observation selection.')
    print('- The ~75% older-system result is contextual, not multiplied into a civilization probability here.')
    print('- Do not tune age leads, settlement times, or delay grid after output under B3.')
    print('\nFINISHED BOOK2024-B3 — DO NOT RETUNE AFTER OUTPUT')

if __name__ == '__main__':
    main()
