
"""
bridge_sparc_colab_runner.py

Colab-ready runner for the SPARC Bridge challenge.

What it does:
1. Downloads the public SPARC Newtonian mass-model archive (Rotmod_LTG.zip)
2. Extracts all *_rotmod.dat files
3. Runs the current best shared Bridge response family across every available galaxy
4. Exports:
   - per-galaxy fit metrics
   - parameter summary
   - per-galaxy Bridge curves
   - a compact leaderboard of best / worst fits

Current shared Bridge family (from 3-galaxy holdout progress):
    beta = 1.1
    L_kpc = 3.5
    gamma_curv = 1.0
    eta_signed = 0.35
    zeta_disk = 0.5

This is a real-data pressure-test scaffold, not a claim of final physical truth.
"""

from __future__ import annotations

import os
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SPARC_URL = "https://astroweb.case.edu/SPARC/Rotmod_LTG.zip"


def maybe_download_sparc(data_dir: Path) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    zip_path = data_dir / "Rotmod_LTG.zip"
    extract_dir = data_dir / "Rotmod_LTG"

    if extract_dir.exists() and any(extract_dir.rglob("*_rotmod.dat")):
        return extract_dir

    if not zip_path.exists():
        print(f"Downloading SPARC mass models from {SPARC_URL}")
        os.system(f'wget -O "{zip_path}" "{SPARC_URL}"')

    print("Extracting SPARC archive...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    return extract_dir


def find_rotmod_files(extract_dir: Path):
    files = sorted(extract_dir.rglob("*_rotmod.dat"))
    if not files:
        raise FileNotFoundError("No *_rotmod.dat files found after extraction.")
    return files


def load_rotmod(path: Path):
    first = path.read_text().splitlines()[0]
    dist = float(first.split("=")[1].split()[0])
    data = np.loadtxt(path, comments="#")
    cols = ["R", "Vobs", "errV", "Vgas", "Vdisk", "Vbul", "SBdisk", "SBbul"]
    return dist, pd.DataFrame(data, columns=cols)


def smooth_transfer(x, r, L, eps=1e-9):
    dr = np.abs(r[:, None] - r[None, :])
    K = np.exp(-dr / max(L, eps))
    K /= np.sum(K, axis=1, keepdims=True) + eps
    return K @ x


def bridge_curve_diskweighted(
    df,
    beta=1.1,
    L=3.5,
    gamma_curv=1.0,
    eta_signed=0.35,
    zeta_disk=0.5,
    gate_frac=0.85,
    gate_width_frac=0.15,
    alpha_s=0.08,
    alpha_f=0.35,
    eps=1e-9,
):
    r = df["R"].to_numpy()
    vgas = df["Vgas"].to_numpy()
    vdisk = df["Vdisk"].to_numpy()
    vbul = df["Vbul"].to_numpy()
    vobs = df["Vobs"].to_numpy()

    vbar2 = vgas**2 + vdisk**2 + vbul**2
    vbar = np.sqrt(np.maximum(vbar2, 0.0))
    gbar = vbar2 / np.maximum(r, eps)

    disk_frac = (vdisk**2 + vgas**2) / np.maximum(vbar2, eps)
    bulge_frac = (vbul**2) / np.maximum(vbar2, eps)
    component_weight = np.clip(disk_frac - 0.5 * bulge_frac, 0.0, 1.0)

    logg = np.log(np.maximum(gbar, eps))
    grad = np.zeros_like(gbar)
    grad[1:] = np.diff(logg) / np.maximum(np.diff(r), eps)

    curv = np.zeros_like(gbar)
    if len(r) > 2:
        dr = np.diff(r)
        d1 = np.diff(logg) / np.maximum(dr, eps)
        d2 = np.diff(d1) / np.maximum((dr[1:] + dr[:-1]) / 2.0, eps)
        curv[2:] = d2

    r_norm = r / (np.nanmedian(r) + eps)
    radial_shape = np.abs(grad) * (r_norm / (1 + r_norm)) + gamma_curv * np.abs(curv) * (
        r_norm**2 / (1 + r_norm**2)
    )
    signed_shape = np.sign(curv) * np.minimum(
        np.abs(curv)
        / (
            (
                np.nanmedian(np.abs(curv[np.abs(curv) > 0]))
                if np.any(np.abs(curv) > 0)
                else 1.0
            )
            + eps
        ),
        3.0,
    )

    drive_abs = radial_shape * (1 + zeta_disk * component_weight)
    m_s = np.zeros_like(gbar)
    m_f = np.zeros_like(gbar)
    for i in range(len(r)):
        ps = m_s[i - 1] if i > 0 else 0.0
        pf = m_f[i - 1] if i > 0 else 0.0
        m_s[i] = (1 - alpha_s) * ps + alpha_s * drive_abs[i]
        m_f[i] = (1 - alpha_f) * pf + alpha_f * drive_abs[i]

    lam = m_s / (m_s + m_f + eps)
    rw = m_f / (m_s + m_f + eps)

    a0 = np.nanmedian(gbar)
    rw_nonlocal = smooth_transfer(rw, r, L=L, eps=eps)
    shape_scale = np.nanmedian(radial_shape[radial_shape > 0]) if np.any(radial_shape > 0) else 1.0
    pos_shape = smooth_transfer(radial_shape / (shape_scale + eps), r, L=L, eps=eps)
    signed_shape_s = smooth_transfer(signed_shape, r, L=L, eps=eps)

    r0 = np.nanmedian(r)
    outer_gate = 1.0 / (1.0 + np.exp(-(r - gate_frac * r0) / (gate_width_frac * r0 + eps)))
    low_acc = a0 / (gbar + a0 + eps)

    corr_raw = beta * (1 - lam) * rw_nonlocal * low_acc * outer_gate * (
        (1 + zeta_disk * component_weight) * pos_shape + eta_signed * signed_shape_s
    )
    corr = np.tanh(corr_raw)

    gbridge = np.maximum(gbar * (1.0 + corr), 0.0)
    vbridge = np.sqrt(np.maximum(gbridge * r, 0.0))

    return pd.DataFrame(
        {
            "R": r,
            "Vobs": vobs,
            "Vbar": vbar,
            "Vbridge": vbridge,
            "delta_v_obs": vobs - vbar,
            "delta_v_bridge": vbridge - vbar,
            "corr": corr,
            "lambda": lam,
            "retained_weight": rw,
            "component_weight": component_weight,
        }
    )


def fit_metrics(res: pd.DataFrame):
    finite = np.isfinite(res["delta_v_obs"]) & np.isfinite(res["delta_v_bridge"])
    rmse_bar = float(np.sqrt(np.nanmean((res["Vobs"] - res["Vbar"]) ** 2)))
    rmse_bridge = float(np.sqrt(np.nanmean((res["Vobs"] - res["Vbridge"]) ** 2)))
    corrcoef = (
        float(np.corrcoef(res["delta_v_obs"][finite], res["delta_v_bridge"][finite])[0, 1])
        if np.sum(finite) > 2
        else np.nan
    )
    sign_match = float(np.mean(np.sign(res["delta_v_obs"][finite]) == np.sign(res["delta_v_bridge"][finite])))

    r = res["R"].to_numpy()
    dv = res["delta_v_bridge"].to_numpy()

    onset = np.nan
    for i in range(len(dv) - 1):
        if np.isfinite(dv[i]) and np.isfinite(dv[i + 1]) and dv[i] > 0 and dv[i + 1] > 0:
            onset = float(r[i])
            break

    outer = finite & (r > np.nanmedian(r[finite]))
    outer_flatness_cv = float(np.nanstd(res["Vbridge"][outer]) / (np.nanmean(res["Vbridge"][outer]) + 1e-9))

    return {
        "rmse_bar": rmse_bar,
        "rmse_bridge": rmse_bridge,
        "rmse_improvement": rmse_bar - rmse_bridge,
        "delta_v_corrcoef_vs_obs": corrcoef,
        "delta_v_sign_match_fraction": sign_match,
        "onset_radius_kpc": onset,
        "mean_outer_delta_v": float(np.nanmean(dv[outer])),
        "outer_flatness_cv": outer_flatness_cv,
    }


def run_full_sample(
    rotmod_dir: Path,
    outdir: Path,
    beta=1.1,
    L=3.5,
    gamma_curv=1.0,
    eta_signed=0.35,
    zeta_disk=0.5,
):
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    rotmods = find_rotmod_files(rotmod_dir)

    print(f"Found {len(rotmods)} SPARC rotmod files")

    for path in rotmods:
        galaxy = path.name.replace("_rotmod.dat", "")
        try:
            dist, df = load_rotmod(path)
            res = bridge_curve_diskweighted(
                df,
                beta=beta,
                L=L,
                gamma_curv=gamma_curv,
                eta_signed=eta_signed,
                zeta_disk=zeta_disk,
            )
            metrics = fit_metrics(res)
            row = {"galaxy": galaxy, "distance_mpc": dist, **metrics}
            rows.append(row)

            res.to_csv(outdir / f"{galaxy}_bridge_curve.csv", index=False)

        except Exception as e:
            rows.append(
                {
                    "galaxy": galaxy,
                    "distance_mpc": np.nan,
                    "rmse_bar": np.nan,
                    "rmse_bridge": np.nan,
                    "rmse_improvement": np.nan,
                    "delta_v_corrcoef_vs_obs": np.nan,
                    "delta_v_sign_match_fraction": np.nan,
                    "onset_radius_kpc": np.nan,
                    "mean_outer_delta_v": np.nan,
                    "outer_flatness_cv": np.nan,
                    "error": str(e),
                }
            )

    summary = pd.DataFrame(rows)
    summary.to_csv(outdir / "sparc_full_sample_summary.csv", index=False)

    valid = summary.dropna(subset=["rmse_improvement", "delta_v_corrcoef_vs_obs"])
    aggregate = pd.DataFrame(
        [
            {
                "n_galaxies": len(valid),
                "mean_rmse_improvement": valid["rmse_improvement"].mean(),
                "median_rmse_improvement": valid["rmse_improvement"].median(),
                "mean_delta_v_corrcoef": valid["delta_v_corrcoef_vs_obs"].mean(),
                "median_delta_v_corrcoef": valid["delta_v_corrcoef_vs_obs"].median(),
                "mean_sign_match": valid["delta_v_sign_match_fraction"].mean(),
                "fraction_positive_rmse_improvement": np.mean(valid["rmse_improvement"] > 0),
            }
        ]
    )
    aggregate.to_csv(outdir / "sparc_full_sample_aggregate.csv", index=False)

    best = valid.sort_values("rmse_improvement", ascending=False).head(20)
    worst = valid.sort_values("rmse_improvement", ascending=True).head(20)
    best.to_csv(outdir / "top20_rmse_improvement.csv", index=False)
    worst.to_csv(outdir / "bottom20_rmse_improvement.csv", index=False)

    plt.figure(figsize=(8.5, 5.5))
    plt.hist(valid["rmse_improvement"].to_numpy(), bins=30)
    plt.xlabel("RMSE improvement over baryonic baseline [km/s]")
    plt.ylabel("Number of galaxies")
    plt.title("Bridge full-sample RMSE improvement distribution")
    plt.tight_layout()
    plt.savefig(outdir / "rmse_improvement_histogram.png", dpi=180)
    plt.close()

    print(aggregate.to_string(index=False))
    print("\nTop 10 improvements:")
    print(best.head(10).to_string(index=False))
    return summary, aggregate


if __name__ == "__main__":
    data_dir = Path("./sparc_data")
    rotmod_dir = maybe_download_sparc(data_dir)
    outdir = Path("./bridge_sparc_full_sample_results")
    run_full_sample(
        rotmod_dir=rotmod_dir,
        outdir=outdir,
        beta=1.1,
        L=3.5,
        gamma_curv=1.0,
        eta_signed=0.35,
        zeta_disk=0.5,
    )
