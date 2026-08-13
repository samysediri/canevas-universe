"""BOOK2024-E1 — FINITE LOCAL STATE SPACE / RECURRENCE SCALE v1
Preregistered before output.

Tests only the conditional bridge: if a local causal domain has finite dimensionless entropy S/kB, an information/state-count scale exp(S/kB) is finite. This does not derive global infinity, literal duplicate universes, or a recurrence time.
"""
import math

S_grid=[10.0,100.0,1e3,1e6,1e12,1e30,1e60,1e90,1e120,1e122]

print('='*80)
print('BOOK2024-E1 — FINITE LOCAL STATE SPACE / RECURRENCE SCALE v1')
print('='*80)
print('Conditional test only: finite local entropy -> finite exponential state-count scale.')
print('No global Canevas infinity is assumed or inferred.\n')

rows=[]
for S in S_grid:
    log10N=S/math.log(10.0)
    rows.append((S,log10N))
    print(f'S_over_k={S:.3e} log10_state_scale={log10N:.6e}')

finite_logs=all(math.isfinite(r[1]) for r in rows)
monotonic=all(rows[i+1][1]>rows[i][1] for i in range(len(rows)-1))
exact_recurrence_time_derived=False
global_infinity_derived=False
literal_duplicate_universes_derived=False

print('\nPREDECLARED BOOK2024-E1 SUMMARY')
print(f'finite_entropy_gives_finite_log_state_scale = {finite_logs}')
print(f'state_scale_monotonic_in_entropy = {monotonic}')
print(f'exact_recurrence_time_derived = {exact_recurrence_time_derived}')
print(f'global_infinity_derived = {global_infinity_derived}')
print(f'literal_duplicate_universes_derived = {literal_duplicate_universes_derived}')

if finite_logs and monotonic and not global_infinity_derived and not literal_duplicate_universes_derived:
    verdict='FINITE_LOCAL_INFORMATION_CAPACITY_COMPATIBLE_WITH_BOOK_ARCHITECTURE_GLOBAL_INFINITY_NOT_DERIVED'
else:
    verdict='FINITE_LOCAL_STATE_BRIDGE_NOT_ESTABLISHED'
print(f'PREDECLARED BOOK2024-E1 VERDICT = {verdict}')

print('\nINTERPRETATION LOCK:')
print('- E1 is conditional mathematics, not evidence that the universe or Canevas is infinite.')
print('- Finite entropy can motivate a finite information/state-count scale; interpreting this as an exact finite Hilbert-space dimension requires additional physics.')
print('- Recurrence additionally requires suitable dynamics; E1 does not derive an exact recurrence time.')
print('- Local finiteness alone does not imply literal duplicate universes.')
print('- E2, if pursued, must independently motivate a physical cosmological entropy scale before inspecting its consequence.')
print('\nFINISHED BOOK2024-E1 — DO NOT RETUNE AFTER OUTPUT')