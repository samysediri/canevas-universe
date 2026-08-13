"""Canevas + CLASS v0.10

Sensitivity / falsification scan around the observed dark-matter-to-baryon ratio.

Scientific intent
-----------------
Do NOT optimize the model toward zeta_obs. Instead:
1. use CLASS for P(k,z) on a fine zeta grid;
2. reuse each CLASS spectrum to test reasonable post-processing variants;
3. ask whether the preferred zeta remains in the same broad region.

Variants tested without extra CLASS calls:
- primordial amplitude scale A_s x {0.8, 1.0, 1.2};
- halo mass function: Sheth-Tormen vs Press-Schechter;
- cooling strength x {0.5, 1.0, 2.0};
- atomic cooling threshold T_min x {8000, 10000, 15000 K}.

This remains an exploratory semi-analytic calculation, not a proof of Canevas.
"""

from pathlib import Path
import csv
import traceback
import numpy as np
from classy import Class

VERSION = "0.10"
OUTDIR = Path(__file__).resolve().parent / "results"
OUTDIR.mkdir(exist_ok=True)

# -------------------------
# Frozen reference cosmology
# -------------------------
h = 0.674
H0 = 100.0 * h
Omega_m = 0.315
omega_m = Omega_m * h * h
Omega_b_obs = 0.0493
zeta_obs = (Omega_m - Omega_b_obs) / Omega_b_obs
A_s = 2.10e-9
n_s = 0.965
YHe = 0.245

delta_c = 1.686

# cgs constants
G = 6.67430e-8
kB = 1.380649e-16
mp = 1.6726219e-24
Msun = 1.98847e33
Mpc = 3.0856776e24
mu = 0.59
H0_cgs = H0 * 1e5 / Mpc

# CLASS is known to be stable on this installation in roughly this region.
# Fine scan deliberately brackets zeta_obs without touching previously rejected extremes.
zeta_grid = np.unique(np.sort(np.append(np.logspace(np.log10(3.0), np.log10(20.0), 37), zeta_obs)))
redshifts = [10.0, 8.0, 6.0, 4.0, 2.0]
k_class = np.logspace(-4, np.log10(50.0), 650)  # 1/Mpc

# Halo masses in Msun/h
Mgrid = np.logspace(7, 14.5, 300)
lnM = np.log(Mgrid)
dlnM = np.gradient(lnM)
rho_m_hunits = Omega_m * 2.775e11

# Sensitivity variants (pre-declared)
AS_SCALES = [0.8, 1.0, 1.2]
HMF_MODELS = ["ST", "PS"]
COOLING_SCALES = [0.5, 1.0, 2.0]
T_MINS = [8000.0, 10000.0, 15000.0]


def R_from_M(M):
    return (M / ((4 * np.pi / 3) * rho_m_hunits)) ** (1 / 3)


Rgrid = R_from_M(Mgrid)


def W_tophat(x):
    x = np.asarray(x)
    out = np.ones_like(x)
    mask = np.abs(x) > 1e-5
    y = x[mask]
    out[mask] = 3 * (np.sin(y) - y * np.cos(y)) / y**3
    out[~mask] = 1 - x[~mask] ** 2 / 10
    return out


def sigma_M(k_h, P_h, Rvals):
    lnk = np.log(k_h)
    dlnk = np.gradient(lnk)
    base = k_h**3 * P_h / (2 * np.pi**2) * dlnk
    X = Rvals[:, None] * k_h[None, :]
    s2 = (W_tophat(X) ** 2) @ base
    return np.sqrt(np.maximum(s2, 0))


def hmf_sheth_tormen(sig):
    A0, aa, p = 0.3222, 0.707, 0.3
    s = np.maximum(sig, 1e-30)
    nu = delta_c / s
    f = A0 * np.sqrt(2 * aa / np.pi) * nu * (1 + (1 / (aa * nu**2)) ** p) * np.exp(-aa * nu**2 / 2)
    deriv = np.gradient(np.log(1 / s), lnM)
    return np.maximum(rho_m_hunits / Mgrid * f * deriv, 0)


def hmf_press_schechter(sig):
    s = np.maximum(sig, 1e-30)
    nu = delta_c / s
    f = np.sqrt(2 / np.pi) * nu * np.exp(-0.5 * nu**2)
    deriv = np.gradient(np.log(1 / s), lnM)
    return np.maximum(rho_m_hunits / Mgrid * f * deriv, 0)


def halo_mass_function(sig, model):
    return hmf_sheth_tormen(sig) if model == "ST" else hmf_press_schechter(sig)


def Ez(z):
    return np.sqrt(Omega_m * (1 + z) ** 3 + (1 - Omega_m))


def rho_crit_cgs(z):
    H = H0_cgs * Ez(z)
    return 3 * H**2 / (8 * np.pi * G)


def cooling_function(T, strength=1.0):
    T = np.asarray(T)
    safeT = np.maximum(T, 1)
    line = 1.2e-22 * np.exp(-((np.log10(safeT) - 5.25) / 0.75) ** 2)
    gate = 1 / (1 + np.exp(-(np.log10(safeT) - 4.0) * 20))
    brem = 1.4e-27 * np.sqrt(safeT)
    return strength * (gate * line + brem)


def cooling_efficiency(M_h, z, fb, strength=1.0, T_min=1e4):
    Mcgs = (M_h / h) * Msun
    rh = 200 * rho_crit_cgs(z)
    Rv = (3 * Mcgs / (4 * np.pi * rh)) ** (1 / 3)
    V = np.sqrt(G * Mcgs / Rv)
    T = mu * mp * V**2 / (2 * kB)
    tdyn = Rv / V
    rhohot = fb * rh
    n = rhohot / (mu * mp)
    tcool = 1.5 * kB * T / (np.maximum(n, 1e-100) * np.maximum(cooling_function(T, strength), 1e-100))
    eff = 1 / (1 + tcool / tdyn)
    return np.where(T >= T_min, eff, 0.0)


def class_spectrum(zeta, z):
    omega_b = omega_m / (1 + zeta)
    omega_cdm = omega_m - omega_b
    params = {
        "output": "mPk",
        "h": h,
        "omega_b": omega_b,
        "omega_cdm": omega_cdm,
        "A_s": A_s,
        "n_s": n_s,
        "YHe": YHe,
        "P_k_max_1/Mpc": 50.0,
        "z_max_pk": max(redshifts) + 0.5,
    }
    cosmo = Class()
    try:
        cosmo.set(params)
        cosmo.compute()
        P_Mpc3 = np.array([cosmo.pk(float(ki), float(z)) for ki in k_class])
        k_h = k_class / h
        P_h = P_Mpc3 * h**3
        try:
            s8 = float(cosmo.sigma8())
        except Exception:
            s8 = float("nan")
        return k_h, P_h, s8, omega_b, omega_cdm
    finally:
        try:
            cosmo.struct_cleanup()
            cosmo.empty()
        except Exception:
            pass


def safe_class_spectrum(zeta, z):
    try:
        return class_spectrum(zeta, z), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}".replace("\n", " ")


def score_variant(sig_base, zeta, z, as_scale, hmf_model, cooling_scale, T_min):
    # Linear P(k) is proportional to A_s, hence sigma scales as sqrt(A_s).
    sig = sig_base * np.sqrt(as_scale)
    hmf = halo_mass_function(sig, hmf_model)
    fb = 1 / (1 + zeta)
    eff = cooling_efficiency(Mgrid, z, fb, cooling_scale, T_min)
    return fb * np.sum(Mgrid * hmf * eff * dlnM) / rho_m_hunits


def interpolate_peak(zs, scores):
    """Quadratic interpolation in log-zeta around the best grid point when possible."""
    zs = np.asarray(zs, float)
    scores = np.asarray(scores, float)
    i = int(np.argmax(scores))
    if i == 0 or i == len(zs) - 1:
        return float(zs[i]), float(scores[i])
    x = np.log(zs[i-1:i+2])
    y = scores[i-1:i+2]
    try:
        c2, c1, c0 = np.polyfit(x, y, 2)
        if c2 >= 0:
            return float(zs[i]), float(scores[i])
        xp = -c1/(2*c2)
        zp = float(np.exp(xp))
        if not (zs[i-1] <= zp <= zs[i+1]):
            return float(zs[i]), float(scores[i])
        yp = float(np.polyval([c2, c1, c0], xp))
        return zp, yp
    except Exception:
        return float(zs[i]), float(scores[i])


def run():
    print("=" * 72)
    print(f" CANEVAS + CLASS v{VERSION} — SENSITIVITY / FALSIFICATION")
    print("=" * 72)
    print(f"Observed zeta = {zeta_obs:.6f}")
    print(f"Fine grid: {len(zeta_grid)} zeta values x {len(redshifts)} epochs")
    print(f"Post-CLASS variants per spectrum: {len(AS_SCALES)*len(HMF_MODELS)*len(COOLING_SCALES)*len(T_MINS)}")
    print()

    raw_rows = []
    # cache[(z,zeta)] = (sigma_base, sigma8, omega_b, omega_cdm)
    cache = {}
    counter = 0
    total = len(zeta_grid) * len(redshifts)

    for z in redshifts:
        for zeta in zeta_grid:
            counter += 1
            print(f"[{counter:3d}/{total}] CLASS z={z:g}, zeta={zeta:.6f}", end=" ... ", flush=True)
            result, error = safe_class_spectrum(float(zeta), float(z))
            if result is None:
                print("REJECTED")
                raw_rows.append({"z":z, "zeta":float(zeta), "status":"class_rejected", "sigma8_z0_CLASS":"", "error":error})
                continue
            k_h, P_h, s8, ob, oc = result
            sig_base = sigma_M(k_h, P_h, Rgrid)
            cache[(float(z), float(zeta))] = (sig_base, s8, ob, oc)
            print("OK")
            raw_rows.append({"z":z, "zeta":float(zeta), "status":"ok", "sigma8_z0_CLASS":s8, "error":""})

    # Save CLASS raw-status table
    with (OUTDIR / "v010_class_status.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["z", "zeta", "status", "sigma8_z0_CLASS", "error"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(raw_rows)

    variant_rows = []
    summary_rows = []

    for z in redshifts:
        for as_scale in AS_SCALES:
            for hmf_model in HMF_MODELS:
                for cool_scale in COOLING_SCALES:
                    for T_min in T_MINS:
                        zs, scores = [], []
                        obs_score = np.nan
                        for zeta in zeta_grid:
                            key = (float(z), float(zeta))
                            if key not in cache:
                                continue
                            sig_base = cache[key][0]
                            s = score_variant(sig_base, float(zeta), z, as_scale, hmf_model, cool_scale, T_min)
                            zs.append(float(zeta)); scores.append(float(s))
                            if np.isclose(zeta, zeta_obs, rtol=1e-10):
                                obs_score = float(s)
                            variant_rows.append({
                                "z":z, "zeta":float(zeta), "as_scale":as_scale,
                                "hmf":hmf_model, "cooling_scale":cool_scale, "T_min":T_min,
                                "score":float(s)
                            })
                        if not scores:
                            continue
                        peak_zeta, peak_score = interpolate_peak(zs, scores)
                        obs_over_peak = obs_score/peak_score if np.isfinite(obs_score) and peak_score > 0 else np.nan
                        summary_rows.append({
                            "z":z, "as_scale":as_scale, "hmf":hmf_model,
                            "cooling_scale":cool_scale, "T_min":T_min,
                            "peak_zeta":peak_zeta, "observed_over_peak":obs_over_peak,
                            "n_valid_zeta":len(scores)
                        })

    with (OUTDIR / "v010_variant_scores.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["z","zeta","as_scale","hmf","cooling_scale","T_min","score"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(variant_rows)

    with (OUTDIR / "v010_sensitivity_summary.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["z","as_scale","hmf","cooling_scale","T_min","peak_zeta","observed_over_peak","n_valid_zeta"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(summary_rows)

    # Global robustness summary
    peaks = np.array([r["peak_zeta"] for r in summary_rows], float)
    ratios = np.array([r["observed_over_peak"] for r in summary_rows], float)
    finite = np.isfinite(peaks) & np.isfinite(ratios)
    peaks = peaks[finite]; ratios = ratios[finite]

    # Epoch-specific stats
    lines = []
    lines.append(f"CANEVAS + CLASS v{VERSION} — ROBUSTNESS SUMMARY")
    lines.append("=" * 56)
    lines.append(f"Observed zeta = {zeta_obs:.6f}")
    lines.append(f"Total model variants = {len(summary_rows)}")
    lines.append("")
    for z in redshifts:
        rr = [r for r in summary_rows if r["z"] == z and np.isfinite(r["peak_zeta"])]
        pp = np.array([r["peak_zeta"] for r in rr])
        oo = np.array([r["observed_over_peak"] for r in rr])
        lines.append(
            f"z={z:4.1f}: peak median={np.median(pp):.4f}; "
            f"16-84%=[{np.percentile(pp,16):.4f},{np.percentile(pp,84):.4f}]; "
            f"obs/max median={np.nanmedian(oo):.4f}"
        )
    lines.append("")
    lines.append(f"ALL VARIANTS peak median = {np.median(peaks):.4f}")
    lines.append(f"ALL VARIANTS peak 5-95% = [{np.percentile(peaks,5):.4f}, {np.percentile(peaks,95):.4f}]")
    lines.append(f"Fraction of variants with 3 <= peak_zeta <= 10 = {np.mean((peaks>=3)&(peaks<=10)):.4f}")
    lines.append(f"Fraction with observed_over_peak >= 0.90 = {np.mean(ratios>=0.90):.4f}")
    lines.append(f"Fraction with observed_over_peak >= 0.75 = {np.mean(ratios>=0.75):.4f}")
    lines.append("")
    lines.append("Interpretation rule (pre-declared):")
    lines.append("- robust-interesting if most variants keep peak zeta in the same order of magnitude;")
    lines.append("- weak/non-robust if reasonable variants scatter the peak across the scan range;")
    lines.append("- never interpret proximity alone as proof of Canevas.")

    summary_text = "\n".join(lines)
    (OUTDIR / "v010_robustness_summary.txt").write_text(summary_text, encoding="utf-8")
    print("\n" + summary_text)
    print("\nFINISHED. Results are in:", OUTDIR)


if __name__ == "__main__":
    try:
        run()
    except Exception:
        traceback.print_exc()
        input("\nUnexpected pipeline error. Press Enter to close...")
