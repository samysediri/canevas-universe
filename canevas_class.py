"""Canevas + CLASS v0.11.1 — dark-energy / measure test.

Scientific question
-------------------
The raw structure score S(Lambda) is expected to favor smaller positive vacuum
energy. So this version separates physical selection S(Lambda) from the prior /
measure P(Lambda), and it never forces CLASS through parameter regions that its
solver rejects.

Two priors are declared before looking at the result:
- flat per unit positive vacuum density Lambda;
- flat per logarithmic interval in Lambda.

IMPORTANT v0.11.1 change
------------------------
On this Windows/classy build, sufficiently large Lambda values are rejected by
CLASS and a still larger value can stall for a long time. Once three consecutive
increasing Lambda values have already been rejected, the remaining higher-Lambda
points are marked as skipped_beyond_rejection_frontier and are NOT sent to CLASS.
This is a numerical-domain rule, not a physical claim.

Any posterior summary is therefore conditional on the CLASS-valid sampled domain.
"""

from pathlib import Path
import csv
import traceback
import numpy as np
from classy import Class

VERSION = "0.11.1"
OUTDIR = Path(__file__).resolve().parent / "results"
OUTDIR.mkdir(exist_ok=True)

h_ref = 0.674
Omega_m_ref = 0.315
Omega_b_ref = 0.0493
omega_m = Omega_m_ref * h_ref**2
omega_b = Omega_b_ref * h_ref**2
omega_cdm = omega_m - omega_b
Omega_L_ref = 1.0 - Omega_m_ref
omega_L_ref = Omega_L_ref * h_ref**2
A_s = 2.10e-9
n_s = 0.965
YHe = 0.245
zeta_obs = omega_cdm / omega_b

delta_c = 1.686

G = 6.67430e-8
kB = 1.380649e-16
mp = 1.6726219e-24
Msun = 1.98847e33
Mpc = 3.0856776e24
mu = 0.59

rho_m_phys = omega_m * 2.775e11
Mgrid = np.logspace(7, 15, 320)
lnM = np.log(Mgrid)
dlnM = np.gradient(lnM)
Rgrid = (Mgrid / ((4*np.pi/3)*rho_m_phys))**(1/3)
kgrid = np.logspace(-4, np.log10(50.0), 700)

lambda_grid = np.unique(np.sort(np.append(np.logspace(-2, 2, 41), 1.0)))
redshifts = np.array([10.0, 8.0, 6.0, 4.0, 3.0, 2.0, 1.0, 0.5, 0.0])
MAX_CONSECUTIVE_REJECTIONS = 3


def W_tophat(x):
    x = np.asarray(x)
    out = np.ones_like(x)
    m = np.abs(x) > 1e-5
    y = x[m]
    out[m] = 3*(np.sin(y)-y*np.cos(y))/y**3
    out[~m] = 1-x[~m]**2/10
    return out


def sigma_M(Pk):
    lnk = np.log(kgrid)
    dlnk = np.gradient(lnk)
    base = kgrid**3 * Pk/(2*np.pi**2) * dlnk
    X = Rgrid[:,None]*kgrid[None,:]
    return np.sqrt(np.maximum((W_tophat(X)**2) @ base, 0))


def hmf_sheth_tormen(sig):
    A0, aa, p = 0.3222, 0.707, 0.3
    s = np.maximum(sig,1e-30)
    nu = delta_c/s
    f = A0*np.sqrt(2*aa/np.pi)*nu*(1+(1/(aa*nu**2))**p)*np.exp(-aa*nu**2/2)
    deriv = np.gradient(np.log(1/s), lnM)
    return np.maximum(rho_m_phys/Mgrid*f*deriv, 0)


def cooling_function(T):
    safeT = np.maximum(np.asarray(T),1)
    line = 1.2e-22*np.exp(-((np.log10(safeT)-5.25)/0.75)**2)
    gate = 1/(1+np.exp(-(np.log10(safeT)-4.0)*20))
    brem = 1.4e-27*np.sqrt(safeT)
    return gate*line+brem


def background_hubble_cgs(z, lambda_ratio):
    omega_L = omega_L_ref*lambda_ratio
    H_km_s_Mpc = 100.0*np.sqrt(omega_m*(1+z)**3 + omega_L)
    return H_km_s_Mpc*1e5/Mpc


def rho_crit_cgs(z, lambda_ratio):
    H = background_hubble_cgs(z,lambda_ratio)
    return 3*H**2/(8*np.pi*G)


def cooling_efficiency(z, lambda_ratio):
    fb = omega_b/omega_m
    Mcgs = Mgrid*Msun
    rh = 200*rho_crit_cgs(z,lambda_ratio)
    Rv = (3*Mcgs/(4*np.pi*rh))**(1/3)
    V = np.sqrt(G*Mcgs/Rv)
    T = mu*mp*V**2/(2*kB)
    tdyn = Rv/V
    n = fb*rh/(mu*mp)
    tcool = 1.5*kB*T/(np.maximum(n,1e-100)*np.maximum(cooling_function(T),1e-100))
    eff = 1/(1+tcool/tdyn)
    return np.where(T>=1e4,eff,0.0)


def class_cosmology(lambda_ratio):
    omega_L = omega_L_ref*lambda_ratio
    h = float(np.sqrt(omega_m + omega_L))
    params = {
        "output":"mPk",
        "h":h,
        "omega_b":omega_b,
        "omega_cdm":omega_cdm,
        "A_s":A_s,
        "n_s":n_s,
        "YHe":YHe,
        "P_k_max_1/Mpc":50.0,
        "z_max_pk":float(redshifts.max()+0.5),
    }
    cosmo = Class()
    try:
        cosmo.set(params)
        cosmo.compute()
        spectra = {}
        for z in redshifts:
            spectra[float(z)] = np.array([cosmo.pk(float(k),float(z)) for k in kgrid])
        return spectra, h, None
    except Exception as exc:
        return None, h, f"{type(exc).__name__}: {exc}".replace("\n"," ")
    finally:
        try:
            cosmo.struct_cleanup(); cosmo.empty()
        except Exception:
            pass


def score_epoch(Pk,z,lambda_ratio):
    sig = sigma_M(Pk)
    hmf = hmf_sheth_tormen(sig)
    eff = cooling_efficiency(z,lambda_ratio)
    fb = omega_b/omega_m
    return fb*np.sum(Mgrid*hmf*eff*dlnM)/rho_m_phys


def normalize_density(x,dens):
    norm = np.trapz(dens,x)
    return dens/norm if norm>0 else dens*np.nan


def cdf_at_one(x,dens):
    p = normalize_density(x,dens)
    mask = x<=1.0
    return float(np.trapz(p[mask],x[mask]))


def weighted_quantile(x,dens,q):
    p = normalize_density(x,dens)
    dx = np.diff(x)
    area = 0.5*(p[:-1]+p[1:])*dx
    c = np.concatenate([[0.0],np.cumsum(area)])
    c /= c[-1]
    return float(np.interp(q,c,x))


def run():
    print("="*72)
    print(f" CANEVAS + CLASS v{VERSION} — DARK ENERGY / MEASURE TEST")
    print("="*72)
    print(f"Fixed observed zeta = {zeta_obs:.6f}")
    print(f"Lambda scan: {len(lambda_grid)} requested physical-vacuum ratios")
    print(f"Safety rule: stop after {MAX_CONSECUTIVE_REJECTIONS} consecutive CLASS rejections.")
    print("No prior will be selected after seeing the result.\n")

    epoch_rows=[]
    selection=[]
    total=len(lambda_grid)
    consecutive_rejections = 0
    frontier_reached = False

    for i,lr in enumerate(lambda_grid,1):
        if frontier_reached:
            print(f"[{i:2d}/{total}] Lambda/Lambda_obs={lr:.5g} ... SKIPPED BEYOND REJECTION FRONTIER")
            selection.append((lr,np.nan))
            epoch_rows.append({
                "lambda_ratio":lr,"z":"","h":"","score":"",
                "status":"skipped_beyond_rejection_frontier",
                "error":f"Skipped after {MAX_CONSECUTIVE_REJECTIONS} consecutive CLASS rejections at lower Lambda."
            })
            continue

        print(f"[{i:2d}/{total}] CLASS Lambda/Lambda_obs={lr:.5g}",end=" ... ",flush=True)
        spectra,h,error=class_cosmology(float(lr))
        if spectra is None:
            consecutive_rejections += 1
            print(f"REJECTED ({consecutive_rejections}/{MAX_CONSECUTIVE_REJECTIONS})")
            selection.append((lr,np.nan))
            epoch_rows.append({"lambda_ratio":lr,"z":"","h":h,"score":"","status":"class_rejected","error":error})
            if consecutive_rejections >= MAX_CONSECUTIVE_REJECTIONS:
                frontier_reached = True
                print("    >>> Rejection frontier reached. Higher Lambda values will be skipped, not forced.")
            continue

        consecutive_rejections = 0
        print("OK")
        scores=[]
        for z in redshifts:
            s=score_epoch(spectra[float(z)],float(z),float(lr))
            scores.append(s)
            epoch_rows.append({"lambda_ratio":lr,"z":z,"h":h,"score":s,"status":"ok","error":""})
        selection.append((lr,float(np.mean(scores))))

    with (OUTDIR/"v011_lambda_epoch_scores.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["lambda_ratio","z","h","score","status","error"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(epoch_rows)

    valid=np.array([(x,s) for x,s in selection if np.isfinite(s)],float)
    if len(valid) < 3:
        raise RuntimeError("Too few CLASS-valid Lambda points for a meaningful summary.")
    x=valid[:,0]; S=valid[:,1]
    order=np.argsort(x); x=x[order]; S=S[order]
    Srel=S/np.max(S)

    prior_flat=np.ones_like(x)
    prior_log=1/x
    post_flat=S*prior_flat
    post_log=S*prior_log

    stats={
        "raw_score_peak_lambda":float(x[np.argmax(S)]),
        "raw_score_at_observed_over_peak":float(np.interp(1.0,x,Srel)),
        "flat_prior_CDF_at_observed":cdf_at_one(x,post_flat),
        "flat_prior_median_lambda":weighted_quantile(x,post_flat,0.5),
        "flat_prior_16":weighted_quantile(x,post_flat,0.16),
        "flat_prior_84":weighted_quantile(x,post_flat,0.84),
        "log_prior_CDF_at_observed":cdf_at_one(x,post_log),
        "log_prior_median_lambda":weighted_quantile(x,post_log,0.5),
        "log_prior_16":weighted_quantile(x,post_log,0.16),
        "log_prior_84":weighted_quantile(x,post_log,0.84),
        "valid_lambda_min":float(x.min()),
        "valid_lambda_max":float(x.max()),
    }

    with (OUTDIR/"v011_lambda_selection.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["lambda_ratio","selection_score","selection_relative","posterior_flat_unnorm","posterior_logflat_unnorm"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for i in range(len(x)):
            w.writerow({"lambda_ratio":x[i],"selection_score":S[i],"selection_relative":Srel[i],"posterior_flat_unnorm":post_flat[i],"posterior_logflat_unnorm":post_log[i]})

    lines=[
        f"CANEVAS + CLASS v{VERSION} — DARK ENERGY / MEASURE SUMMARY",
        "="*64,
        f"Fixed zeta = {zeta_obs:.6f}",
        f"CLASS-valid Lambda domain used for statistics = [{stats['valid_lambda_min']:.6f}, {stats['valid_lambda_max']:.6f}] x Lambda_obs",
        "IMPORTANT: posterior statistics below are CONDITIONAL on this CLASS-valid sampled domain.",
        "",
        "PHYSICS ONLY S(Lambda):",
        f"raw score peak Lambda/Lambda_obs = {stats['raw_score_peak_lambda']:.6f}",
        f"score at observed Lambda / peak = {stats['raw_score_at_observed_over_peak']:.6f}",
        "",
        "FLAT PRIOR PER UNIT POSITIVE LAMBDA (conditional on valid domain):",
        f"CDF at observed Lambda = {stats['flat_prior_CDF_at_observed']:.6f}",
        f"median = {stats['flat_prior_median_lambda']:.6f}",
        f"16-84% = [{stats['flat_prior_16']:.6f}, {stats['flat_prior_84']:.6f}]",
        "",
        "LOG-FLAT PRIOR (conditional on valid domain):",
        f"CDF at observed Lambda = {stats['log_prior_CDF_at_observed']:.6f}",
        f"median = {stats['log_prior_median_lambda']:.6f}",
        f"16-84% = [{stats['log_prior_16']:.6f}, {stats['log_prior_84']:.6f}]",
        "",
        "PRE-DECLARED INTERPRETATION:",
        "- If physics alone peaks at the lower scan boundary, non-zero Lambda is NOT explained by optimization.",
        "- If typicality changes strongly with the prior, the Canevas measure P(U) is essential.",
        "- No prior is promoted to correct because it matches observation.",
        "- CLASS rejection/skipping boundaries are numerical, not physical selection boundaries.",
    ]
    (OUTDIR/"v011_lambda_measure_summary.txt").write_text("\n".join(lines),encoding="utf-8")

    print("\n"+"\n".join(lines))
    print("\nFINISHED v0.11.1")


if __name__=="__main__":
    try:
        run()
    except Exception:
        traceback.print_exc()
        input("\nUnexpected error. Press Enter to close...")
