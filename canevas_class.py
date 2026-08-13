"""Canevas + CLASS v0.9.2

Robust CLASS scan of zeta = rho_cdm/rho_b.
A failed cosmology is recorded and the scan continues.

IMPORTANT: this is an exploratory anthropic/structure-formation proxy, not a
proof of Canevas and not a complete galaxy-formation simulation.
"""

from pathlib import Path
import csv
import math
import traceback
import numpy as np
from classy import Class

VERSION = "0.9.2"
OUTDIR = Path(__file__).resolve().parent / "results"
OUTDIR.mkdir(exist_ok=True)

# Frozen reference cosmology
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

# Include observed zeta explicitly in addition to a broad log grid.
zeta_grid = np.unique(np.sort(np.append(np.logspace(-1, 2, 25), zeta_obs)))
redshifts = [10.0, 8.0, 6.0, 4.0, 2.0]
k_class = np.logspace(-4, np.log10(50.0), 600)  # 1/Mpc
Mgrid = np.logspace(7, 14.5, 260)  # Msun/h
lnM = np.log(Mgrid)
dlnM = np.gradient(lnM)
rho_m_hunits = Omega_m * 2.775e11


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


def sheth_tormen(sig):
    A0, aa, p = 0.3222, 0.707, 0.3
    s = np.maximum(sig, 1e-30)
    nu = delta_c / s
    f = A0 * np.sqrt(2 * aa / np.pi) * nu * (1 + (1 / (aa * nu**2)) ** p) * np.exp(-aa * nu**2 / 2)
    deriv = np.gradient(np.log(1 / s), lnM)
    return np.maximum(rho_m_hunits / Mgrid * f * deriv, 0)


def Ez(z):
    return np.sqrt(Omega_m * (1 + z) ** 3 + (1 - Omega_m))


def rho_crit_cgs(z):
    H = H0_cgs * Ez(z)
    return 3 * H**2 / (8 * np.pi * G)


def cooling_function(T):
    T = np.asarray(T)
    safeT = np.maximum(T, 1)
    line = 1.2e-22 * np.exp(-((np.log10(safeT) - 5.25) / 0.75) ** 2)
    gate = 1 / (1 + np.exp(-(np.log10(safeT) - 4.0) * 20))
    brem = 1.4e-27 * np.sqrt(safeT)
    return gate * line + brem


def cooling_efficiency(M_h, z, fb):
    Mcgs = (M_h / h) * Msun
    rh = 200 * rho_crit_cgs(z)
    Rv = (3 * Mcgs / (4 * np.pi * rh)) ** (1 / 3)
    V = np.sqrt(G * Mcgs / Rv)
    T = mu * mp * V**2 / (2 * kB)
    tdyn = Rv / V
    rhohot = fb * rh
    n = rhohot / (mu * mp)
    tcool = 1.5 * kB * T / (np.maximum(n, 1e-100) * np.maximum(cooling_function(T), 1e-100))
    eff = 1 / (1 + tcool / tdyn)
    return np.where(T >= 1e4, eff, 0.0)


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
        data = class_spectrum(zeta, z)
        return data, None
    except Exception as exc:
        # Do not alter CLASS safety barriers. Record the rejected cosmology.
        return None, f"{type(exc).__name__}: {exc}".replace("\n", " ")


def run():
    rows = []
    summaries = []
    total = len(zeta_grid) * len(redshifts)
    counter = 0

    print("=" * 64)
    print(f" CANEVAS + CLASS v{VERSION}")
    print(" Robust scan: rejected cosmologies are logged, not forced")
    print("=" * 64)
    print(f"zeta observed reference = {zeta_obs:.6f}")
    print(f"{len(zeta_grid)} zeta values x {len(redshifts)} epochs = {total} CLASS attempts\n")

    for z in redshifts:
        valid = []
        for zeta in zeta_grid:
            counter += 1
            print(f"[{counter:3d}/{total}] z={z:g}, zeta={zeta:.6g}", end=" ... ", flush=True)
            result, error = safe_class_spectrum(float(zeta), float(z))

            if result is None:
                print("REJECTED BY CLASS")
                omega_b = omega_m / (1 + zeta)
                omega_cdm = omega_m - omega_b
                rows.append({
                    "z": z, "zeta": float(zeta), "omega_b": float(omega_b),
                    "omega_cdm": float(omega_cdm), "status": "class_rejected",
                    "sigma8_z0_CLASS": "", "cooling_weighted_baryon_proxy": "",
                    "error": error,
                })
                continue

            k_h, P_h, s8, omega_b, omega_cdm = result
            sig = sigma_M(k_h, P_h, Rgrid)
            hmf = sheth_tormen(sig)
            fb = 1 / (1 + zeta)
            eff = cooling_efficiency(Mgrid, z, fb)
            proxy = fb * np.sum(Mgrid * hmf * eff * dlnM) / rho_m_hunits
            print(f"OK  score={proxy:.6e}")
            rows.append({
                "z": z, "zeta": float(zeta), "omega_b": float(omega_b),
                "omega_cdm": float(omega_cdm), "status": "ok",
                "sigma8_z0_CLASS": float(s8),
                "cooling_weighted_baryon_proxy": float(proxy), "error": "",
            })
            valid.append((float(zeta), float(proxy)))

        if valid:
            zs = np.array([v[0] for v in valid])
            scores = np.array([v[1] for v in valid])
            imax = int(np.argmax(scores))
            peak_zeta = float(zs[imax])
            peak_score = float(scores[imax])
            # observed zeta was explicitly inserted; if CLASS rejects it, report NA.
            obs_matches = [(zz, ss) for zz, ss in valid if np.isclose(zz, zeta_obs, rtol=1e-10)]
            obs_ratio = obs_matches[0][1] / peak_score if obs_matches and peak_score > 0 else float("nan")
            summaries.append((z, peak_zeta, obs_ratio, len(valid), len(zeta_grid) - len(valid)))
            print(f"\n>>> z={z:g}: valid optimum zeta={peak_zeta:.6g}; observed/max={obs_ratio:.6f}\n")
        else:
            summaries.append((z, float("nan"), float("nan"), 0, len(zeta_grid)))

    csv_path = OUTDIR / "canevas_class_results.csv"
    fields = ["z", "zeta", "omega_b", "omega_cdm", "status", "sigma8_z0_CLASS", "cooling_weighted_baryon_proxy", "error"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    txt_path = OUTDIR / "canevas_class_summary.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        f.write(f"CANEVAS + CLASS v{VERSION}\n======================\n\n")
        f.write(f"zeta observed reference = {zeta_obs:.6f}\n")
        f.write("Failed CLASS cosmologies were recorded and excluded, never forced.\n\n")
        for z, peak, ratio, nvalid, nfail in summaries:
            f.write(f"z={z:4.1f}: peak_zeta={peak:10.6f}; observed_over_peak={ratio:10.6f}; valid={nvalid}; rejected={nfail}\n")
        f.write("\nInterpretation must account for rejected parameter-space regions.\n")
        f.write("This result is not evidence by itself for the philosophical axioms.\n")

    print("=" * 64)
    print("FINISHED")
    print(f"Results: {OUTDIR}")
    print("Commit/push the results folder to GitHub, then tell ChatGPT to analyze it.")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        traceback.print_exc()
        input("\nUnexpected pipeline error. Press Enter to close...")
