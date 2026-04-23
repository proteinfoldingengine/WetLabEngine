
"""
bridge_round5_structure_diagnostics.py

Round 5 diagnostics:
- Downloads / reuses SPARC Rotmod_LTG.zip
- Evaluates Bridge and MOND-standard on full SPARC sample
- Builds diagnostic tables showing:
    1) Bridge vs MOND outer-support ratio by morphology quartile
    2) Bridge internal structural observables vs concentration / disk fraction
    3) Correlations between Bridge internals and residual quality
- Exports tables and plots for posting / pressure-test

Usage in Colab:
    !python bridge_round5_structure_diagnostics.py
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

A0_DEFAULT = 3700.0


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
        "R": r, "Vobs": vobs, "errV": errv,
        "Vgas": vgas, "Vdisk": vdisk, "Vbul": vbul,
        "Vbar": vbar, "gbar": gbar, "gobs": gobs,
        "disk_frac": disk_frac, "bulge_frac": bulge_frac,
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
    radial_shape = np.abs(grad) * (r_norm / (1 + r_norm)) + p["gamma_curv"] * np.abs(curv) * (r_norm**2 / (1 + r_norm**2))
    signed_shape = np.sign(curv) * np.minimum(
        np.abs(curv) / (((np.nanmedian(np.abs(curv[np.abs(curv) > 0])) if np.any(np.abs(curv) > 0) else 1.0) + eps)),
        3.0,
    )

    drive_abs = radial_shape * (1 + p["zeta_disk"] * component_weight)
    m_s = np.zeros_like(gbar)
    m_f = np.zeros_like(gbar)
    for i in range(len(r)):
        ps = m_s[i-1] if i > 0 else 0.0
        pf = m_f[i-1] if i > 0 else 0.0
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
        "R": r, "Vobs": vobs, "errV": errv,
        "Vmodel": vbridge, "gmodel": gbridge,
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
        "R": b["R"], "Vobs": b["Vobs"], "errV": b["errV"],
        "Vmodel": v, "gmodel": g,
    })


def per_galaxy_metrics(df_input: pd.DataFrame, df_model: pd.DataFrame, model_name: str, eps=1e-9):
    b = baryonic_components(df_input, eps=eps)
    r = b["R"].to_numpy()
    vobs = b["Vobs"].to_numpy()
    vbar = b["Vbar"].to_numpy()
    gobs = b["gobs"].to_numpy()
    gbar = b["gbar"].to_numpy()
    vmodel = df_model["Vmodel"].to_numpy()
    gmodel = df_model["gmodel"].to_numpy()

    rmse = float(np.sqrt(np.nanmean((vobs - vmodel) ** 2)))
    rmse_bar = float(np.sqrt(np.nanmean((vobs - vbar) ** 2)))
    rmse_improvement = rmse_bar - rmse

    dv_obs = vobs - vbar
    dv_model = vmodel - vbar
    finite = np.isfinite(dv_obs) & np.isfinite(dv_model)
    corrcoef = np.nan
    if np.sum(finite) > 2 and np.std(dv_obs[finite]) > 0 and np.std(dv_model[finite]) > 0:
        corrcoef = float(np.corrcoef(dv_obs[finite], dv_model[finite])[0, 1])
    sign_match = float(np.mean(np.sign(dv_obs[finite]) == np.sign(dv_model[finite]))) if np.sum(finite) else np.nan

    onset = np.nan
    for i in range(len(dv_model)-1):
        if np.isfinite(dv_model[i]) and np.isfinite(dv_model[i+1]) and dv_model[i] > 0 and dv_model[i+1] > 0:
            onset = float(r[i]); break

    outer = finite & (r > np.nanmedian(r[finite]))
    mean_outer_delta_v = float(np.nanmean(dv_model[outer])) if np.any(outer) else np.nan
    outer_flatness_cv = float(np.nanstd(vmodel[outer]) / (np.nanmean(vmodel[outer]) + eps)) if np.any(outer) else np.nan

    out = {
        "model": model_name,
        "rmse": rmse,
        "rmse_improvement": rmse_improvement,
        "delta_v_corrcoef_vs_obs": corrcoef,
        "delta_v_sign_match_fraction": sign_match,
        "onset_radius_kpc": onset,
        "mean_outer_delta_v": mean_outer_delta_v,
        "outer_flatness_cv": outer_flatness_cv,
        "mean_disk_frac": float(np.nanmean(b["disk_frac"])),
        "mean_bulge_frac": float(np.nanmean(b["bulge_frac"])),
        "concentration_proxy": float(np.nanmax(vbar) / (np.nanmean(vbar[r > np.nanmedian(r)]) + eps)) if np.any(r > np.nanmedian(r)) else np.nan,
    }

    if model_name == "bridge":
        out.update({
            "mean_component_weight": float(np.nanmean(df_model["component_weight"])),
            "mean_lambda": float(np.nanmean(df_model["lambda"])),
            "mean_retained_weight": float(np.nanmean(df_model["retained_weight"])),
            "mean_corr_field": float(np.nanmean(df_model["corr"])),
        })
    else:
        out.update({
            "mean_component_weight": np.nan,
            "mean_lambda": np.nan,
            "mean_retained_weight": np.nan,
            "mean_corr_field": np.nan,
        })
    return out


def run_round5(rotmod_dir: Path, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    rotmods = find_rotmod_files(rotmod_dir)
    print(f"Found {len(rotmods)} SPARC rotmod files")

    rows = []
    for path in rotmods:
        galaxy = path.name.replace("_rotmod.dat", "")
        dist, df = load_rotmod(path)
        bridge_df = bridge_curve(df)
        mond_df = mond_standard_curve(df)
        bary = baryonic_components(df)

        rows.append({"galaxy": galaxy, "distance_mpc": dist, **per_galaxy_metrics(df, pd.DataFrame({
            "Vmodel": bary["Vbar"], "gmodel": bary["gbar"]
        }), "baryonic")})
        rows.append({"galaxy": galaxy, "distance_mpc": dist, **per_galaxy_metrics(df, bridge_df, "bridge")})
        rows.append({"galaxy": galaxy, "distance_mpc": dist, **per_galaxy_metrics(df, mond_df, "mond_standard")})

    full = pd.DataFrame(rows)
    full.to_csv(outdir / "round5_full_metrics.csv", index=False)

    bridge = full[full["model"] == "bridge"].copy()
    mond = full[full["model"] == "mond_standard"].copy()

    merged = bridge.merge(
        mond,
        on=["galaxy", "distance_mpc"],
        suffixes=("_bridge", "_mond")
    )

    merged["outer_support_ratio_bridge_to_mond"] = merged["mean_outer_delta_v_bridge"] / (merged["mean_outer_delta_v_mond"] + 1e-9)
    merged["rmse_improvement_delta_bridge_minus_mond"] = merged["rmse_improvement_bridge"] - merged["rmse_improvement_mond"]
    merged["corr_delta_bridge_minus_mond"] = merged["delta_v_corrcoef_vs_obs_bridge"] - merged["delta_v_corrcoef_vs_obs_mond"]

    for col in ["mean_disk_frac_bridge", "mean_bulge_frac_bridge", "concentration_proxy_bridge"]:
        try:
            merged[f"{col}_quartile"] = pd.qcut(merged[col], 4, labels=["Q1","Q2","Q3","Q4"])
        except ValueError:
            pass

    merged.to_csv(outdir / "round5_bridge_vs_mond_merged.csv", index=False)

    quartile_rows = []
    for axis in ["mean_disk_frac_bridge", "mean_bulge_frac_bridge", "concentration_proxy_bridge"]:
        qcol = f"{axis}_quartile"
        if qcol not in merged.columns:
            continue
        for q in ["Q1","Q2","Q3","Q4"]:
            sub = merged[merged[qcol] == q]
            if len(sub) == 0:
                continue
            quartile_rows.append({
                "axis": axis,
                "quartile": q,
                "n_galaxies": len(sub),
                "bridge_mean_rmse_improvement": sub["rmse_improvement_bridge"].mean(),
                "mond_mean_rmse_improvement": sub["rmse_improvement_mond"].mean(),
                "bridge_mean_delta_v_corr": sub["delta_v_corrcoef_vs_obs_bridge"].mean(),
                "mond_mean_delta_v_corr": sub["delta_v_corrcoef_vs_obs_mond"].mean(),
                "bridge_mean_outer_delta_v": sub["mean_outer_delta_v_bridge"].mean(),
                "mond_mean_outer_delta_v": sub["mean_outer_delta_v_mond"].mean(),
                "mean_outer_support_ratio_bridge_to_mond": sub["outer_support_ratio_bridge_to_mond"].mean(),
                "bridge_mean_lambda": sub["mean_lambda_bridge"].mean(),
                "bridge_mean_retained_weight": sub["mean_retained_weight_bridge"].mean(),
                "bridge_mean_component_weight": sub["mean_component_weight_bridge"].mean(),
            })
    quartiles = pd.DataFrame(quartile_rows)
    quartiles.to_csv(outdir / "round5_quartile_diagnostics.csv", index=False)

    # Correlation table: bridge internal variables vs quality
    corr_targets = [
        "rmse_improvement_bridge",
        "delta_v_corrcoef_vs_obs_bridge",
        "delta_v_sign_match_fraction_bridge",
        "onset_radius_kpc_bridge",
        "mean_outer_delta_v_bridge",
    ]
    corr_sources = [
        "mean_component_weight_bridge",
        "mean_lambda_bridge",
        "mean_retained_weight_bridge",
        "mean_corr_field_bridge",
        "mean_disk_frac_bridge",
        "mean_bulge_frac_bridge",
        "concentration_proxy_bridge",
        "outer_support_ratio_bridge_to_mond",
    ]
    corr_rows = []
    for s in corr_sources:
        for t in corr_targets:
            x = merged[s].to_numpy()
            y = merged[t].to_numpy()
            mask = np.isfinite(x) & np.isfinite(y)
            corr = np.nan
            if np.sum(mask) > 3 and np.std(x[mask]) > 0 and np.std(y[mask]) > 0:
                corr = float(np.corrcoef(x[mask], y[mask])[0,1])
            corr_rows.append({"source": s, "target": t, "corrcoef": corr})
    corr_df = pd.DataFrame(corr_rows)
    corr_df.to_csv(outdir / "round5_bridge_internal_correlations.csv", index=False)

    # Representative tables
    merged.sort_values("rmse_improvement_delta_bridge_minus_mond", ascending=False).head(20).to_csv(
        outdir / "round5_top20_bridge_advantage.csv", index=False
    )
    merged.sort_values("rmse_improvement_delta_bridge_minus_mond", ascending=True).head(20).to_csv(
        outdir / "round5_top20_mond_advantage.csv", index=False
    )

    # Plots
    plt.figure(figsize=(8.5,5.5))
    plt.scatter(merged["mean_component_weight_bridge"], merged["delta_v_corrcoef_vs_obs_bridge"])
    plt.xlabel("Bridge mean component weight")
    plt.ylabel("Bridge Δv correlation")
    plt.title("Bridge structure vs residual-shape quality")
    plt.tight_layout()
    plt.savefig(outdir / "round5_bridge_component_vs_corr.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5,5.5))
    plt.scatter(merged["concentration_proxy_bridge"], merged["outer_support_ratio_bridge_to_mond"])
    plt.xlabel("Concentration proxy")
    plt.ylabel("Bridge / MOND outer-support ratio")
    plt.title("How Bridge outer support scales vs MOND")
    plt.tight_layout()
    plt.savefig(outdir / "round5_bridge_vs_mond_outer_support_ratio.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5,5.5))
    plt.scatter(merged["mean_lambda_bridge"], merged["rmse_improvement_bridge"])
    plt.xlabel("Bridge mean lambda")
    plt.ylabel("Bridge RMSE improvement")
    plt.title("Bridge retained-memory state vs fit improvement")
    plt.tight_layout()
    plt.savefig(outdir / "round5_lambda_vs_rmse_improvement.png", dpi=180)
    plt.close()

    # Compact aggregate
    agg = full.groupby("model", as_index=False).agg(
        n_galaxies=("galaxy", "count"),
        mean_rmse=("rmse", "mean"),
        mean_rmse_improvement=("rmse_improvement", "mean"),
        mean_delta_v_corr=("delta_v_corrcoef_vs_obs", "mean"),
        mean_sign_match=("delta_v_sign_match_fraction", "mean"),
        mean_outer_delta_v=("mean_outer_delta_v", "mean"),
    )
    agg.to_csv(outdir / "round5_aggregate.csv", index=False)

    print(agg.to_string(index=False))
    print("\nQuartile diagnostics preview:")
    if len(quartiles):
        print(quartiles.head(12).to_string(index=False))
    print("\nTop bridge internal correlations:")
    print(corr_df.sort_values("corrcoef", ascending=False).head(12).to_string(index=False))
    return full, merged, quartiles, corr_df


if __name__ == "__main__":
    data_dir = Path("./sparc_data")
    rotmod_dir = maybe_download_sparc(data_dir)
    outdir = Path("./bridge_round5_results")
    run_round5(rotmod_dir, outdir)
