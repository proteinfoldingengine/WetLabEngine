
"""
bridge_round4_structure_runner.py

Round 4 runner:
- Downloads SPARC Rotmod_LTG.zip
- Evaluates Bridge, MOND-standard, and baryonic baseline on full SPARC sample
- Builds a SECOND SCOREBOARD beyond raw RC fit:
    * morphology-conditioned residual behavior
    * onset-radius behavior
    * outer-support behavior
- Exports comparison tables and plots showing where Bridge explains more structure

Models:
- baryonic
- bridge (shared family)
- mond_standard

Usage in Colab:
    !python bridge_round4_structure_runner.py
"""

from __future__ import annotations
import os
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SPARC_URL = "https://astroweb.case.edu/SPARC/Rotmod_LTG.zip"

BRIDGE_PARAMS = dict(
    beta=1.1,
    L=3.5,
    gamma_curv=1.0,
    eta_signed=0.35,
    zeta_disk=0.5,
    gate_frac=0.85,
    gate_width_frac=0.15,
    alpha_s=0.08,
    alpha_f=0.35,
)

A0_DEFAULT = 3700.0  # (km/s)^2 / kpc


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


def baryonic_components(df: pd.DataFrame, eps=1e-9):
    r = df["R"].to_numpy()
    vobs = df["Vobs"].to_numpy()
    errv = df["errV"].to_numpy()
    vgas = df["Vgas"].to_numpy()
    vdisk = df["Vdisk"].to_numpy()
    vbul = df["Vbul"].to_numpy()

    vbar2 = vgas**2 + vdisk**2 + vbul**2
    vbar = np.sqrt(np.maximum(vbar2, 0.0))
    gbar = vbar2 / np.maximum(r, eps)
    gobs = vobs**2 / np.maximum(r, eps)

    disk_frac = (vdisk**2 + vgas**2) / np.maximum(vbar2, eps)
    bulge_frac = (vbul**2) / np.maximum(vbar2, eps)

    return pd.DataFrame({
        "R": r,
        "Vobs": vobs,
        "errV": errv,
        "Vgas": vgas,
        "Vdisk": vdisk,
        "Vbul": vbul,
        "Vbar": vbar,
        "gbar": gbar,
        "gobs": gobs,
        "disk_frac": disk_frac,
        "bulge_frac": bulge_frac,
    })


def baryonic_curve(df: pd.DataFrame):
    b = baryonic_components(df)
    return pd.DataFrame({
        "R": b["R"],
        "Vobs": b["Vobs"],
        "errV": b["errV"],
        "Vmodel": b["Vbar"],
        "gmodel": b["gbar"],
    })


def bridge_curve(df: pd.DataFrame, eps=1e-9, **params):
    p = {**BRIDGE_PARAMS, **params}
    b = baryonic_components(df, eps=eps)

    r = b["R"].to_numpy()
    vobs = b["Vobs"].to_numpy()
    errv = b["errV"].to_numpy()
    vbar = b["Vbar"].to_numpy()
    gbar = b["gbar"].to_numpy()
    disk_frac = b["disk_frac"].to_numpy()
    bulge_frac = b["bulge_frac"].to_numpy()

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
    radial_shape = np.abs(grad) * (r_norm / (1 + r_norm)) + p["gamma_curv"] * np.abs(curv) * (
        r_norm**2 / (1 + r_norm**2)
    )
    signed_shape = np.sign(curv) * np.minimum(
        np.abs(curv) / (((np.nanmedian(np.abs(curv[np.abs(curv) > 0])) if np.any(np.abs(curv) > 0) else 1.0) + eps)),
        3.0,
    )

    drive_abs = radial_shape * (1 + p["zeta_disk"] * component_weight)
    m_s = np.zeros_like(gbar)
    m_f = np.zeros_like(gbar)
    for i in range(len(r)):
        ps = m_s[i - 1] if i > 0 else 0.0
        pf = m_f[i - 1] if i > 0 else 0.0
        m_s[i] = (1 - p["alpha_s"]) * ps + p["alpha_s"] * drive_abs[i]
        m_f[i] = (1 - p["alpha_f"]) * pf + p["alpha_f"] * drive_abs[i]

    lam = m_s / (m_s + m_f + eps)
    rw = m_f / (m_s + m_f + eps)

    a0 = np.nanmedian(gbar)
    rw_nonlocal = smooth_transfer(rw, r, L=p["L"], eps=eps)
    shape_scale = np.nanmedian(radial_shape[radial_shape > 0]) if np.any(radial_shape > 0) else 1.0
    pos_shape = smooth_transfer(radial_shape / (shape_scale + eps), r, L=p["L"], eps=eps)
    signed_shape_s = smooth_transfer(signed_shape, r, L=p["L"], eps=eps)

    r0 = np.nanmedian(r)
    outer_gate = 1.0 / (1.0 + np.exp(-(r - p["gate_frac"] * r0) / (p["gate_width_frac"] * r0 + eps)))
    low_acc = a0 / (gbar + a0 + eps)

    corr_raw = p["beta"] * (1 - lam) * rw_nonlocal * low_acc * outer_gate * (
        (1 + p["zeta_disk"] * component_weight) * pos_shape + p["eta_signed"] * signed_shape_s
    )
    corr = np.tanh(corr_raw)

    gbridge = np.maximum(gbar * (1.0 + corr), 0.0)
    vbridge = np.sqrt(np.maximum(gbridge * r, 0.0))

    return pd.DataFrame({
        "R": r,
        "Vobs": vobs,
        "errV": errv,
        "Vmodel": vbridge,
        "gmodel": gbridge,
        "component_weight": component_weight,
        "lambda": lam,
        "retained_weight": rw,
        "corr": corr,
    })


def mond_standard_curve(df: pd.DataFrame, a0=A0_DEFAULT, eps=1e-9):
    b = baryonic_components(df, eps=eps)
    gbar = b["gbar"].to_numpy()
    y = gbar / max(a0, eps)
    nu = np.sqrt(0.5 + 0.5 * np.sqrt(1.0 + 4.0 / np.maximum(y**2, eps)))
    g = nu * gbar
    v = np.sqrt(np.maximum(g * b["R"].to_numpy(), 0.0))
    return pd.DataFrame({
        "R": b["R"],
        "Vobs": b["Vobs"],
        "errV": b["errV"],
        "Vmodel": v,
        "gmodel": g,
    })


def score_model(df_input: pd.DataFrame, df_model: pd.DataFrame, model_name: str, eps=1e-9):
    b = baryonic_components(df_input, eps=eps)

    r = b["R"].to_numpy()
    vobs = b["Vobs"].to_numpy()
    errv = np.maximum(b["errV"].to_numpy(), 1e-6)
    vbar = b["Vbar"].to_numpy()
    gobs = b["gobs"].to_numpy()
    gbar = b["gbar"].to_numpy()

    vmodel = df_model["Vmodel"].to_numpy()
    gmodel = df_model["gmodel"].to_numpy()

    rmse = float(np.sqrt(np.nanmean((vobs - vmodel) ** 2)))
    rmse_bar = float(np.sqrt(np.nanmean((vobs - vbar) ** 2)))
    rmse_improvement = rmse_bar - rmse

    chi2_red = float(np.nansum(((vobs - vmodel) / errv) ** 2) / max(len(vobs) - 1, 1))

    dv_obs = vobs - vbar
    dv_model = vmodel - vbar
    finite = np.isfinite(dv_obs) & np.isfinite(dv_model)

    corrcoef = np.nan
    if np.sum(finite) > 2:
        xo = dv_obs[finite]
        xm = dv_model[finite]
        if np.std(xo) > 0 and np.std(xm) > 0:
            corrcoef = float(np.corrcoef(xo, xm)[0, 1])

    sign_match = float(np.mean(np.sign(dv_obs[finite]) == np.sign(dv_model[finite]))) if np.sum(finite) else np.nan

    onset = np.nan
    for i in range(len(dv_model) - 1):
        if np.isfinite(dv_model[i]) and np.isfinite(dv_model[i + 1]) and dv_model[i] > 0 and dv_model[i + 1] > 0:
            onset = float(r[i])
            break

    outer = finite & (r > np.nanmedian(r[finite]))
    mean_outer_delta_v = float(np.nanmean(dv_model[outer]))
    outer_flatness_cv = float(np.nanstd(vmodel[outer]) / (np.nanmean(vmodel[outer]) + eps)) if np.any(outer) else np.nan

    finite_g = np.isfinite(gobs) & np.isfinite(gmodel) & (gobs > 0) & (gmodel > 0)
    rar_scatter = float(np.std(np.log10(gobs[finite_g]) - np.log10(gmodel[finite_g]))) if np.sum(finite_g) > 2 else np.nan

    # Second scoreboard: morphology-conditioned diagnostics
    disk_dominance = float(np.nanmean(b["disk_frac"]))
    bulge_dominance = float(np.nanmean(b["bulge_frac"]))
    concentration_proxy = float(np.nanmax(vbar) / (np.nanmean(vbar[r > np.nanmedian(r)]) + eps)) if np.any(r > np.nanmedian(r)) else np.nan

    out = {
        "model": model_name,
        "rmse": rmse,
        "rmse_improvement": rmse_improvement,
        "chi2_red": chi2_red,
        "delta_v_corrcoef_vs_obs": corrcoef,
        "delta_v_sign_match_fraction": sign_match,
        "onset_radius_kpc": onset,
        "mean_outer_delta_v": mean_outer_delta_v,
        "outer_flatness_cv": outer_flatness_cv,
        "rar_scatter_dex": rar_scatter,
        "mean_disk_frac": disk_dominance,
        "mean_bulge_frac": bulge_dominance,
        "concentration_proxy": concentration_proxy,
    }

    # Bridge-only structural observables
    if model_name == "bridge":
        out["mean_component_weight"] = float(np.nanmean(df_model["component_weight"]))
        out["mean_lambda"] = float(np.nanmean(df_model["lambda"]))
        out["mean_retained_weight"] = float(np.nanmean(df_model["retained_weight"]))
        out["mean_corr_field"] = float(np.nanmean(df_model["corr"]))
    else:
        out["mean_component_weight"] = np.nan
        out["mean_lambda"] = np.nan
        out["mean_retained_weight"] = np.nan
        out["mean_corr_field"] = np.nan

    return out


def run_round4(rotmod_dir: Path, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    rotmods = find_rotmod_files(rotmod_dir)
    print(f"Found {len(rotmods)} SPARC rotmod files")

    model_fns = {
        "baryonic": baryonic_curve,
        "bridge": bridge_curve,
        "mond_standard": mond_standard_curve,
    }

    rows = []
    for path in rotmods:
        galaxy = path.name.replace("_rotmod.dat", "")
        dist, df = load_rotmod(path)
        for name, fn in model_fns.items():
            model_df = fn(df)
            metrics = score_model(df, model_df, name)
            rows.append({"galaxy": galaxy, "distance_mpc": dist, **metrics})

    full = pd.DataFrame(rows)
    full.to_csv(outdir / "round4_full_comparison.csv", index=False)

    aggregate = full.groupby("model", as_index=False).agg(
        n_galaxies=("galaxy", "count"),
        mean_rmse=("rmse", "mean"),
        median_rmse=("rmse", "median"),
        mean_rmse_improvement=("rmse_improvement", "mean"),
        median_rmse_improvement=("rmse_improvement", "median"),
        mean_chi2_red=("chi2_red", "mean"),
        median_chi2_red=("chi2_red", "median"),
        mean_delta_v_corr=("delta_v_corrcoef_vs_obs", "mean"),
        median_delta_v_corr=("delta_v_corrcoef_vs_obs", "median"),
        mean_sign_match=("delta_v_sign_match_fraction", "mean"),
        mean_rar_scatter=("rar_scatter_dex", "mean"),
        fraction_positive_improvement=("rmse_improvement", lambda s: np.mean(np.array(s) > 0)),
    )
    aggregate.to_csv(outdir / "round4_aggregate.csv", index=False)

    # Second scoreboard by morphology quartiles
    bary = full[full["model"] == "baryonic"][["galaxy", "mean_disk_frac", "mean_bulge_frac", "concentration_proxy"]].copy()
    bridge = full[full["model"] == "bridge"][["galaxy", "rmse_improvement", "delta_v_corrcoef_vs_obs", "delta_v_sign_match_fraction", "onset_radius_kpc", "mean_outer_delta_v", "mean_component_weight", "mean_lambda", "mean_retained_weight"]].copy()
    mond = full[full["model"] == "mond_standard"][["galaxy", "rmse_improvement", "delta_v_corrcoef_vs_obs", "delta_v_sign_match_fraction", "onset_radius_kpc", "mean_outer_delta_v"]].copy()

    bridge = bridge.merge(bary, on="galaxy", how="left")
    mond = mond.merge(bary, on="galaxy", how="left")

    for col in ["mean_disk_frac", "mean_bulge_frac", "concentration_proxy"]:
        try:
            bridge[f"{col}_quartile"] = pd.qcut(bridge[col], 4, labels=["Q1", "Q2", "Q3", "Q4"])
            mond[f"{col}_quartile"] = pd.qcut(mond[col], 4, labels=["Q1", "Q2", "Q3", "Q4"])
        except ValueError:
            pass

    # Compare Bridge vs MOND by morphology quartile
    second_rows = []
    for col in ["mean_disk_frac", "mean_bulge_frac", "concentration_proxy"]:
        qcol = f"{col}_quartile"
        if qcol not in bridge.columns:
            continue
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            bsub = bridge[bridge[qcol] == q]
            msub = mond[mond[qcol] == q]
            if len(bsub) == 0 or len(msub) == 0:
                continue
            second_rows.append({
                "morphology_axis": col,
                "quartile": q,
                "bridge_mean_rmse_improvement": bsub["rmse_improvement"].mean(),
                "mond_mean_rmse_improvement": msub["rmse_improvement"].mean(),
                "bridge_mean_delta_v_corr": bsub["delta_v_corrcoef_vs_obs"].mean(),
                "mond_mean_delta_v_corr": msub["delta_v_corrcoef_vs_obs"].mean(),
                "bridge_mean_onset": bsub["onset_radius_kpc"].mean(),
                "mond_mean_onset": msub["onset_radius_kpc"].mean(),
                "bridge_mean_outer_delta_v": bsub["mean_outer_delta_v"].mean(),
                "mond_mean_outer_delta_v": msub["mean_outer_delta_v"].mean(),
                "n_galaxies": len(bsub),
            })
    second = pd.DataFrame(second_rows)
    second.to_csv(outdir / "round4_second_scoreboard_morphology.csv", index=False)

    # Bridge-specific “things MOND doesn't natively give”
    bridge_struct = bridge[[
        "galaxy",
        "rmse_improvement",
        "delta_v_corrcoef_vs_obs",
        "mean_component_weight",
        "mean_lambda",
        "mean_retained_weight",
        "mean_disk_frac",
        "mean_bulge_frac",
        "concentration_proxy",
    ]].copy()
    bridge_struct.to_csv(outdir / "round4_bridge_structure_table.csv", index=False)

    # Win rates
    pivot = full.pivot_table(index="galaxy", columns="model", values="rmse")
    models = [c for c in ["baryonic", "bridge", "mond_standard"] if c in pivot.columns]
    win_rows = []
    for m in models:
        wins = 0
        ties = 0
        total = 0
        for _, row in pivot[models].iterrows():
            if row.isna().any():
                continue
            total += 1
            best = row.min()
            if np.isclose(row[m], best):
                if (np.isclose(row, best)).sum() > 1:
                    ties += 1
                else:
                    wins += 1
        win_rows.append({"model": m, "wins": wins, "ties": ties, "total": total, "win_rate": wins / total if total else np.nan})
    win_df = pd.DataFrame(win_rows)
    win_df.to_csv(outdir / "round4_win_rates.csv", index=False)

    # Plots
    plt.figure(figsize=(9, 5.5))
    for name in ["baryonic", "bridge", "mond_standard"]:
        sub = full[full["model"] == name]
        plt.hist(sub["rmse"].to_numpy(), bins=30, alpha=0.5, label=name)
    plt.xlabel("RMSE [km/s]")
    plt.ylabel("Count")
    plt.title("Round 4 RMSE distribution by model")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "round4_rmse_distribution.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.5))
    for name in ["bridge", "mond_standard"]:
        sub = full[full["model"] == name]
        vals = sub["delta_v_corrcoef_vs_obs"].dropna().to_numpy()
        plt.hist(vals, bins=30, alpha=0.5, label=name)
    plt.xlabel("Δv correlation vs observed")
    plt.ylabel("Count")
    plt.title("Round 4 residual-shape correlation distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "round4_delta_v_corr_distribution.png", dpi=180)
    plt.close()

    # Scatter: Bridge structure vs quality
    plt.figure(figsize=(8.5, 5.5))
    plt.scatter(bridge["mean_component_weight"], bridge["delta_v_corrcoef_vs_obs"])
    plt.xlabel("Bridge mean component weight")
    plt.ylabel("Bridge Δv correlation")
    plt.title("Bridge structure vs residual-shape quality")
    plt.tight_layout()
    plt.savefig(outdir / "round4_bridge_structure_scatter.png", dpi=180)
    plt.close()

    print(aggregate.to_string(index=False))
    print("\nWin rates:")
    print(win_df.to_string(index=False))
    print("\nSecond scoreboard preview:")
    if len(second):
        print(second.head(12).to_string(index=False))
    return full, aggregate, second, win_df


if __name__ == "__main__":
    data_dir = Path("./sparc_data")
    rotmod_dir = maybe_download_sparc(data_dir)
    outdir = Path("./bridge_round4_results")
    run_round4(rotmod_dir, outdir)
