from pathlib import Path
import pandas as pd
import numpy as np

CORPUS = Path("round13_locked_corpus.csv")
OUTDIR = Path("rerun_output")
OUTDIR.mkdir(exist_ok=True)

PARAMS = {
    "alpha_s": 0.10,
    "alpha_f": 0.35,
    "beta": 0.45,
    "eta_signed": 0.15,
    "zeta_disk": 0.25,
    "disk_mix": 0.30,
    "L": 2.5,
    "gate_frac": 0.60,
    "gate_width_frac": 0.18,
    "corr_cap": 0.15,
    "need_fraction_cap": 0.65,
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

def total_baryonic_mass(df_gal):
    mgas = float(df_gal["Mgas_total"].dropna().iloc[0]) if df_gal["Mgas_total"].notna().any() else np.nan
    mdisk = float(df_gal["Mstar_disk_total"].dropna().iloc[0]) if df_gal["Mstar_disk_total"].notna().any() else np.nan
    mbul = float(df_gal["Mstar_bul_total"].dropna().iloc[0]) if df_gal["Mstar_bul_total"].notna().any() else np.nan
    parts = [x for x in [mgas, mdisk, mbul] if np.isfinite(x)]
    return float(np.sum(parts)) if parts else np.nan

def compute_bridge_prediction(df_gal):
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

    base_shape = np.maximum((1.0 - PARAMS["disk_mix"]) * gas_shape + PARAMS["disk_mix"] * disk_like, eps)

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

    drive_scale = np.nanmedian(drive_abs[drive_abs > 0]) if np.any(drive_abs > 0) else 1.0
    corr_raw = PARAMS["beta"] * (1 - lam) * rw_nonlocal * outer_gate * (
        drive_abs / (drive_scale + eps)
        + PARAMS["eta_signed"] * signed_shape_s
        + PARAMS["zeta_disk"] * disk_like
    )
    corr = np.clip(np.tanh(corr_raw), -PARAMS["corr_cap"], PARAMS["corr_cap"])

    shape_uplift = np.maximum(base_shape * (1.0 + corr), base_shape)

    anchor = 0
    scale_shape = vobs[anchor] / (shape_uplift[anchor] + eps)
    vshape = scale_shape * shape_uplift

    residual_need = np.maximum(vobs - vbar, 0.0)
    proposed_add = np.maximum(vshape - vbar, 0.0)
    allowed_add = PARAMS["need_fraction_cap"] * residual_need
    actual_add = np.minimum(proposed_add, allowed_add)

    out["Vbridge"] = vbar + actual_add
    out["Vbar"] = vbar
    return out

def fit_btfr(df_summary, v_col):
    sub = df_summary[["log10_m_baryon", v_col]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(sub) < 3:
        return {"n": len(sub), "slope": np.nan, "intercept": np.nan, "scatter_rmse": np.nan}
    x = sub["log10_m_baryon"].to_numpy(float)
    y = sub[v_col].to_numpy(float)
    a, b = np.polyfit(x, y, 1)
    yhat = a * x + b
    scatter = float(np.sqrt(np.mean((y - yhat) ** 2)))
    return {"n": len(sub), "slope": float(a), "intercept": float(b), "scatter_rmse": scatter}

def rar_scatter(rar, pred_col):
    sub = rar[["log10_g_obs", pred_col]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(sub) < 3:
        return {"n": len(sub), "scatter_rmse": np.nan}
    scatter = float(np.sqrt(np.mean((sub["log10_g_obs"] - sub[pred_col]) ** 2)))
    return {"n": len(sub), "scatter_rmse": scatter}

def run():
    corpus = pd.read_csv(CORPUS)
    summaries = []
    rar_rows = []

    for galaxy, g in corpus.groupby("galaxy", sort=True):
        g = g.sort_values("Rad").reset_index(drop=True)
        out = compute_bridge_prediction(g)

        rmse_bary = rmse(out["Vobs"], out["Vbar"])
        rmse_bridge = rmse(out["Vobs"], out["Vbridge"])
        improvement = rmse_bary - rmse_bridge

        vflat_obs = extract_vflat(out["Rad"], out["Vobs"])
        vflat_bridge = extract_vflat(out["Rad"], out["Vbridge"])
        m_baryon = total_baryonic_mass(out)

        g_obs = compute_accelerations(out["Rad"], out["Vobs"])
        g_bar = compute_accelerations(out["Rad"], out["Vbar"])
        g_bridge = compute_accelerations(out["Rad"], out["Vbridge"])

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
            "catastrophic_failure": bool(improvement < -10.0),
            "usable": True,
        })

        rar_rows.append(pd.DataFrame({
            "galaxy": galaxy,
            "Rad": out["Rad"].to_numpy(float),
            "log10_g_obs": safe_log10(g_obs),
            "log10_g_bar": safe_log10(g_bar),
            "log10_g_bridge": safe_log10(g_bridge),
        }))

    summary = pd.DataFrame(summaries)
    summary.to_csv(OUTDIR / "round13_per_galaxy_summary.csv", index=False)

    rar = pd.concat(rar_rows, ignore_index=True)
    rar.to_csv(OUTDIR / "round13_rar_points.csv", index=False)

    agg = {
        "n_galaxies_total": int(len(summary)),
        "n_galaxies_usable": int(summary["usable"].sum()),
        "positive_improvement_rate": float((summary["improvement"] > 0).mean()),
        "mean_rmse_improvement": float(summary["improvement"].mean()),
        "catastrophic_failures": int(summary["catastrophic_failure"].sum()),
        "btfr_obs": fit_btfr(summary, "log10_vflat_obs"),
        "btfr_bridge": fit_btfr(summary, "log10_vflat_bridge"),
        "rar_baryonic": rar_scatter(rar, "log10_g_bar"),
        "rar_bridge": rar_scatter(rar, "log10_g_bridge"),
    }

    with open(OUTDIR / "round13_aggregate_summary.json", "w", encoding="utf-8") as f:
        import json
        json.dump(agg, f, indent=2)

    print(summary.to_string(index=False))
    print("\nAggregate:")
    print(agg)

if __name__ == "__main__":
    run()