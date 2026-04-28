from pathlib import Path
import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass
class Round13Config:
    corpus_csv: str = "/content/round13_locked_corpus.csv"
    output_dir: str = "/content/round13_results_stability_patch"
    catastrophic_rmse_threshold: float = -10.0
    vflat_outer_frac_start: float = 0.70
    min_outer_points: int = 3
    eps: float = 1e-12

CFG = Round13Config()
Path(CFG.output_dir).mkdir(parents=True, exist_ok=True)

REQUIRED_COLS = [
    "galaxy", "Rad", "Vobs", "Vgas", "Vdisk", "Vbul",
    "Mgas_total", "Mstar_disk_total", "Mstar_bul_total"
]

PARAMS = {
    "alpha_s": 0.10,
    "alpha_f": 0.35,
    "beta": 0.55,              # reduced from 12D-like transfer
    "eta_signed": 0.18,
    "zeta_disk": 0.35,
    "disk_mix": 0.35,
    "L": 2.5,
    "gate_frac": 0.60,
    "gate_width_frac": 0.18,
    "overshoot_penalty": 0.55, # stronger than before
    "amp_cap_ratio": 1.25,     # hard amplitude cap vs baryonic baseline
    "corr_cap": 0.22,          # limit correction strength in gas-only mode
    "residual_gate_strength": 0.75,
    "eps": 1e-9,
}

def rmse(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    return float(np.sqrt(np.mean((a[m] - b[m]) ** 2))) if np.any(m) else np.nan

def signed_baryonic_velocity(vgas, vdisk, vbul):
    vbar2 = np.sign(vgas) * (vgas ** 2) + vdisk ** 2 + vbul ** 2
    vbar2 = np.maximum(vbar2, 0.0)
    return np.sqrt(vbar2)

def extract_vflat(rad, vel, outer_frac_start=0.70, min_outer_points=3):
    rad = np.asarray(rad, float)
    vel = np.asarray(vel, float)
    m = np.isfinite(rad) & np.isfinite(vel)
    rad = rad[m]
    vel = vel[m]
    if len(rad) == 0:
        return np.nan
    order = np.argsort(rad)
    rad = rad[order]
    vel = vel[order]
    start_idx = int(np.floor(outer_frac_start * len(rad)))
    start_idx = min(start_idx, max(len(rad) - min_outer_points, 0))
    outer = vel[start_idx:]
    if len(outer) < min_outer_points:
        outer = vel[-min_outer_points:] if len(vel) >= min_outer_points else vel
    return float(np.nanmedian(outer)) if len(outer) else np.nan

def total_baryonic_mass(df_gal):
    mgas = float(df_gal["Mgas_total"].dropna().iloc[0]) if df_gal["Mgas_total"].notna().any() else np.nan
    mdisk = float(df_gal["Mstar_disk_total"].dropna().iloc[0]) if df_gal["Mstar_disk_total"].notna().any() else np.nan
    mbul = float(df_gal["Mstar_bul_total"].dropna().iloc[0]) if df_gal["Mstar_bul_total"].notna().any() else np.nan
    parts = [x for x in [mgas, mdisk, mbul] if np.isfinite(x)]
    return float(np.sum(parts)) if parts else np.nan

def compute_accelerations(rad, vel, eps=1e-12):
    rad = np.asarray(rad, float)
    vel = np.asarray(vel, float)
    return (vel ** 2) / np.maximum(rad, eps)

def safe_log10(x):
    x = np.asarray(x, float)
    out = np.full_like(x, np.nan, dtype=float)
    m = x > 0
    out[m] = np.log10(x[m])
    return out

def smooth_transfer(x, idx, L, eps=1e-9):
    d = np.abs(idx[:, None] - idx[None, :])
    K = np.exp(-d / max(L, eps))
    K /= np.sum(K, axis=1, keepdims=True) + eps
    return K @ x

def compute_bridge_prediction(df_gal: pd.DataFrame) -> pd.DataFrame:
    out = df_gal.copy()
    eps = PARAMS["eps"]

    r = out["Rad"].to_numpy(float)
    vobs = out["Vobs"].to_numpy(float)
    vgas = np.maximum(out["Vgas"].to_numpy(float), 0.0)
    vdisk = out["Vdisk"].to_numpy(float)
    vbul = out["Vbul"].to_numpy(float)

    out["Vbar"] = signed_baryonic_velocity(vgas, vdisk, vbul)
    vbar = out["Vbar"].to_numpy(float)

    r0 = np.nanmedian(r)
    rnorm = r / (r0 + eps)

    gas_shape = vgas / (np.nanmax(vgas) + eps) if np.nanmax(vgas) > 0 else np.zeros_like(vgas)

    cum_sd_norm = np.cumsum(gas_shape)
    cum_sd_norm = cum_sd_norm / (np.nanmax(cum_sd_norm) + eps) if np.nanmax(cum_sd_norm) > 0 else np.zeros_like(cum_sd_norm)

    disk_like = np.sqrt(np.maximum(cum_sd_norm, 0.0)) * np.sqrt(np.maximum(gas_shape, 0.0))
    if np.nanmax(disk_like) > 0:
        disk_like = disk_like / (np.nanmax(disk_like) + eps)

    base_shape = np.maximum(
        (1.0 - PARAMS["disk_mix"]) * gas_shape + PARAMS["disk_mix"] * disk_like,
        eps
    )

    log_sd = np.log(np.maximum(gas_shape, eps))
    grad = np.zeros_like(gas_shape)
    grad[1:] = np.diff(log_sd) / np.maximum(np.diff(rnorm), eps)

    curv = np.zeros_like(gas_shape)
    if len(gas_shape) > 2:
        dr = np.diff(rnorm)
        d1 = np.diff(log_sd) / np.maximum(dr, eps)
        d2 = np.diff(d1) / np.maximum((dr[1:] + dr[:-1]) / 2.0, eps)
        curv[2:] = d2

    drive_abs = np.abs(grad) + 0.5 * np.abs(curv)

    m_s = np.zeros_like(gas_shape)
    m_f = np.zeros_like(gas_shape)
    for i in range(len(gas_shape)):
        ps = m_s[i - 1] if i > 0 else 0.0
        pf = m_f[i - 1] if i > 0 else 0.0
        m_s[i] = (1 - PARAMS["alpha_s"]) * ps + PARAMS["alpha_s"] * drive_abs[i]
        m_f[i] = (1 - PARAMS["alpha_f"]) * pf + PARAMS["alpha_f"] * drive_abs[i]

    lam = m_s / (m_s + m_f + eps)
    rw = m_f / (m_s + m_f + eps)

    idx = np.arange(len(gas_shape), dtype=float)
    rw_nonlocal = smooth_transfer(rw, idx, PARAMS["L"], eps=eps)

    cscale = np.nanmedian(np.abs(curv[np.abs(curv) > 0])) if np.any(np.abs(curv) > 0) else 1.0
    signed_shape = np.sign(curv) * np.minimum(np.abs(curv) / (cscale + eps), 3.0)
    signed_shape_s = smooth_transfer(signed_shape, idx, PARAMS["L"], eps=eps)

    outer_gate = 1.0 / (1.0 + np.exp(-(rnorm - PARAMS["gate_frac"]) / (PARAMS["gate_width_frac"] + eps)))

    dominance = disk_like / (base_shape + eps)
    overshoot = np.clip(dominance - 1.0, 0.0, None)

    drive_scale = np.nanmedian(drive_abs[drive_abs > 0]) if np.any(drive_abs > 0) else 1.0
    corr_raw = PARAMS["beta"] * (1 - lam) * rw_nonlocal * outer_gate * (
        drive_abs / (drive_scale + eps)
        + PARAMS["eta_signed"] * signed_shape_s
        + PARAMS["zeta_disk"] * disk_like
        - PARAMS["overshoot_penalty"] * overshoot
    )

    # cap raw correction in gas-only mode
    corr = np.clip(np.tanh(corr_raw), -PARAMS["corr_cap"], PARAMS["corr_cap"])

    bridge_shape = np.maximum(base_shape * (1.0 + corr), eps)

    anchor = 0
    scale_bridge = vobs[anchor] / (bridge_shape[anchor] + eps)
    vbridge_raw = scale_bridge * bridge_shape

    # residual-aware damping and hard cap vs baryonic baseline
    residual_need = vobs - vbar
    residual_gate = 1.0 / (1.0 + np.exp(-PARAMS["residual_gate_strength"] * residual_need / (np.nanstd(vobs) + eps)))
    # if residual_need is strongly negative, suppress added lift
    added = np.maximum(vbridge_raw - vbar, 0.0) * residual_gate
    vbridge = vbar + added

    # hard cap: bridge cannot exceed capped multiple of baryonic baseline
    cap = PARAMS["amp_cap_ratio"] * np.maximum(vbar, vobs[anchor])
    vbridge = np.minimum(vbridge, cap)

    out["Vbridge"] = vbridge
    out["corr_term"] = corr
    out["residual_gate"] = residual_gate
    out["amp_cap"] = cap
    return out

def fit_btfr(df_summary: pd.DataFrame, v_col: str):
    sub = df_summary[["log10_m_baryon", v_col]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(sub) < 3:
        return {"n": len(sub), "slope": np.nan, "intercept": np.nan, "scatter_rmse": np.nan}
    x = sub["log10_m_baryon"].to_numpy(float)
    y = sub[v_col].to_numpy(float)
    a, b = np.polyfit(x, y, 1)
    yhat = a * x + b
    scatter = float(np.sqrt(np.mean((y - yhat) ** 2)))
    return {"n": len(sub), "slope": float(a), "intercept": float(b), "scatter_rmse": scatter}

def rar_scatter(rar: pd.DataFrame, pred_col: str):
    sub = rar[["log10_g_obs", pred_col]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(sub) < 3:
        return {"n": len(sub), "scatter_rmse": np.nan}
    scatter = float(np.sqrt(np.mean((sub["log10_g_obs"] - sub[pred_col]) ** 2)))
    return {"n": len(sub), "scatter_rmse": scatter}

def run_round13():
    corpus = pd.read_csv(CFG.corpus_csv)
    missing = [c for c in REQUIRED_COLS if c not in corpus.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    summaries = []
    rar_rows = []

    for galaxy, g in corpus.groupby("galaxy", sort=True):
        g = g.replace([np.inf, -np.inf], np.nan).dropna(subset=["Rad", "Vobs", "Vgas", "Vdisk", "Vbul"]).copy()
        g = g.sort_values("Rad").reset_index(drop=True)
        out = compute_bridge_prediction(g)

        rmse_bary = rmse(out["Vobs"], out["Vbar"])
        rmse_bridge = rmse(out["Vobs"], out["Vbridge"])
        improvement = rmse_bary - rmse_bridge

        vflat_obs = extract_vflat(out["Rad"], out["Vobs"], CFG.vflat_outer_frac_start, CFG.min_outer_points)
        vflat_bridge = extract_vflat(out["Rad"], out["Vbridge"], CFG.vflat_outer_frac_start, CFG.min_outer_points)
        m_baryon = total_baryonic_mass(out)

        g_obs = compute_accelerations(out["Rad"], out["Vobs"], CFG.eps)
        g_bar = compute_accelerations(out["Rad"], out["Vbar"], CFG.eps)
        g_bridge = compute_accelerations(out["Rad"], out["Vbridge"], CFG.eps)

        tmp = out.copy()
        tmp["g_obs"] = g_obs
        tmp["g_bar"] = g_bar
        tmp["g_bridge"] = g_bridge
        safe_name = str(galaxy).lower().replace(" ", "_").replace("/", "_")
        tmp.to_csv(Path(CFG.output_dir) / f"{safe_name}_radial_detail.csv", index=False)

        rar_rows.append(pd.DataFrame({
            "galaxy": galaxy,
            "Rad": out["Rad"].to_numpy(float),
            "log10_g_obs": safe_log10(g_obs),
            "log10_g_bar": safe_log10(g_bar),
            "log10_g_bridge": safe_log10(g_bridge),
        }))

        summaries.append({
            "galaxy": galaxy,
            "n_points": len(out),
            "rmse_baryonic": rmse_bary,
            "rmse_bridge": rmse_bridge,
            "improvement": improvement,
            "vflat_obs": vflat_obs,
            "vflat_bridge": vflat_bridge,
            "m_baryon": m_baryon,
            "log10_vflat_obs": float(safe_log10([vflat_obs])[0]) if np.isfinite(vflat_obs) else np.nan,
            "log10_vflat_bridge": float(safe_log10([vflat_bridge])[0]) if np.isfinite(vflat_bridge) else np.nan,
            "log10_m_baryon": float(safe_log10([m_baryon])[0]) if np.isfinite(m_baryon) else np.nan,
            "catastrophic_failure": bool(improvement < CFG.catastrophic_rmse_threshold),
            "usable": True,
        })

    summary = pd.DataFrame(summaries)
    summary.to_csv(Path(CFG.output_dir) / "round13_per_galaxy_summary.csv", index=False)

    rar = pd.concat(rar_rows, ignore_index=True)
    rar.to_csv(Path(CFG.output_dir) / "round13_rar_points.csv", index=False)

    valid = summary["usable"] == True
    aggregate = {
        "n_galaxies_total": int(len(summary)),
        "n_galaxies_usable": int(valid.sum()),
        "positive_improvement_rate": float((summary.loc[valid, "improvement"] > 0).mean()),
        "mean_rmse_improvement": float(summary.loc[valid, "improvement"].mean()),
        "catastrophic_failures": int(summary.loc[valid, "catastrophic_failure"].sum()),
        "btfr_obs": fit_btfr(summary.loc[valid].copy(), "log10_vflat_obs"),
        "btfr_bridge": fit_btfr(summary.loc[valid].copy(), "log10_vflat_bridge"),
        "rar_baryonic": rar_scatter(rar, "log10_g_bar"),
        "rar_bridge": rar_scatter(rar, "log10_g_bridge"),
    }

    print(summary.to_string(index=False))
    print("\nAggregate:")
    print(aggregate)

run_round13()
