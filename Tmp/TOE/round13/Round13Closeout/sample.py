import numpy as np
import pandas as pd

# --------------------------------------------------
# Expected input format:
# one row per galaxy, with radial arrays stored as lists or CSV strings
#
# required columns:
# - galaxy
# - rad
# - vobs
# - sd_gas          # gas surface density proxy/profile
# - mgas_total
# - mstar_total
#
# optional columns:
# - axis_ratio
# --------------------------------------------------

EPS = 1e-9

PARAMS = {
    "alpha_s": 0.10,
    "alpha_f": 0.35,
    "beta": 0.45,
    "eta_signed": 0.15,
    "zeta_disk": 0.25,
    "disk_mix": 0.28,
    "L": 2.5,
    "gate_frac": 0.60,
    "gate_width_frac": 0.18,
    "corr_cap": 0.15,
    "need_fraction_cap": 0.65,
}

def parse_array(x):
    if isinstance(x, (list, np.ndarray)):
        return np.asarray(x, dtype=float)
    if pd.isna(x):
        return np.array([], dtype=float)
    return np.array([float(v) for v in str(x).split(",") if str(v).strip() != ""], dtype=float)

def rmse(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    m = np.isfinite(y_true) & np.isfinite(y_pred)
    if not np.any(m):
        return np.nan
    return float(np.sqrt(np.mean((y_true[m] - y_pred[m]) ** 2)))

def extract_vflat(rad, vel, outer_frac_start=0.70, min_outer_points=3):
    rad = np.asarray(rad, dtype=float)
    vel = np.asarray(vel, dtype=float)
    m = np.isfinite(rad) & np.isfinite(vel)
    rad, vel = rad[m], vel[m]
    if len(rad) == 0:
        return np.nan
    o = np.argsort(rad)
    rad, vel = rad[o], vel[o]
    s = int(np.floor(outer_frac_start * len(rad)))
    s = min(s, max(len(rad) - min_outer_points, 0))
    outer = vel[s:]
    if len(outer) < min_outer_points:
        outer = vel[-min_outer_points:] if len(vel) >= min_outer_points else vel
    return float(np.nanmedian(outer)) if len(outer) else np.nan

def compute_acceleration(rad, vel):
    rad = np.asarray(rad, dtype=float)
    vel = np.asarray(vel, dtype=float)
    return (vel ** 2) / np.maximum(rad, EPS)

def smooth_transfer(x, L):
    x = np.asarray(x, dtype=float)
    idx = np.arange(len(x), dtype=float)
    d = np.abs(idx[:, None] - idx[None, :])
    K = np.exp(-d / max(L, EPS))
    K /= np.sum(K, axis=1, keepdims=True) + EPS
    return K @ x

def compute_vgas_proxy(rad, sd_gas, mgas_total):
    rad = np.asarray(rad, dtype=float)
    sd_gas = np.asarray(sd_gas, dtype=float)

    prof = np.maximum(sd_gas, 0.0)
    if np.nanmax(prof) <= 0 or not np.isfinite(mgas_total) or mgas_total <= 0:
        return np.zeros_like(rad)

    prof = prof / (np.nanmax(prof) + EPS)
    cum = np.cumsum(prof)
    cum = cum / (np.nanmax(cum) + EPS)

    vgas = np.sqrt(np.maximum(cum, 0.0)) * np.sqrt(mgas_total) / 1e4
    if np.nanmax(vgas) > 0:
        vgas = vgas / np.nanmax(vgas) * max(0.35 * np.nanmax(rad), np.nanmax(vgas))
    return vgas

def gas_first_bridge(rad, vobs, sd_gas, mgas_total, mstar_total):
    rad = np.asarray(rad, dtype=float)
    vobs = np.asarray(vobs, dtype=float)
    sd_gas = np.asarray(sd_gas, dtype=float)

    vgas = compute_vgas_proxy(rad, sd_gas, mgas_total)
    vbar = np.sqrt(np.maximum(vgas ** 2, 0.0))

    gas_shape = vgas / (np.nanmax(vgas) + EPS) if np.nanmax(vgas) > 0 else np.zeros_like(vgas)

    cum_sd_norm = np.cumsum(gas_shape)
    if np.nanmax(cum_sd_norm) > 0:
        cum_sd_norm /= (np.nanmax(cum_sd_norm) + EPS)

    disk_like = np.sqrt(np.maximum(cum_sd_norm, 0.0)) * np.sqrt(np.maximum(gas_shape, 0.0))
    if np.nanmax(disk_like) > 0:
        disk_like /= (np.nanmax(disk_like) + EPS)

    base_shape = np.maximum(
        (1.0 - PARAMS["disk_mix"]) * gas_shape + PARAMS["disk_mix"] * disk_like,
        EPS
    )

    r0 = np.nanmedian(rad)
    rnorm = rad / (r0 + EPS)

    log_sd = np.log(np.maximum(gas_shape, EPS))
    grad = np.zeros_like(gas_shape)
    grad[1:] = np.diff(log_sd) / np.maximum(np.diff(rnorm), EPS)

    curv = np.zeros_like(gas_shape)
    if len(gas_shape) > 2:
        dr = np.diff(rnorm)
        d1 = np.diff(log_sd) / np.maximum(dr, EPS)
        d2 = np.diff(d1) / np.maximum((dr[1:] + dr[:-1]) / 2.0, EPS)
        curv[2:] = d2

    drive_abs = np.abs(grad) + 0.5 * np.abs(curv)

    m_s = np.zeros_like(gas_shape)
    m_f = np.zeros_like(gas_shape)
    for i in range(len(gas_shape)):
        ps = m_s[i - 1] if i > 0 else 0.0
        pf = m_f[i - 1] if i > 0 else 0.0
        m_s[i] = (1 - PARAMS["alpha_s"]) * ps + PARAMS["alpha_s"] * drive_abs[i]
        m_f[i] = (1 - PARAMS["alpha_f"]) * pf + PARAMS["alpha_f"] * drive_abs[i]

    lam = m_s / (m_s + m_f + EPS)
    rw = m_f / (m_s + m_f + EPS)
    rw_nonlocal = smooth_transfer(rw, PARAMS["L"])

    cscale = np.nanmedian(np.abs(curv[np.abs(curv) > 0])) if np.any(np.abs(curv) > 0) else 1.0
    signed_shape = np.sign(curv) * np.minimum(np.abs(curv) / (cscale + EPS), 3.0)
    signed_shape_s = smooth_transfer(signed_shape, PARAMS["L"])

    outer_gate = 1.0 / (1.0 + np.exp(-(rnorm - PARAMS["gate_frac"]) / (PARAMS["gate_width_frac"] + EPS)))
    drive_scale = np.nanmedian(drive_abs[drive_abs > 0]) if np.any(drive_abs > 0) else 1.0

    corr_raw = PARAMS["beta"] * (1 - lam) * rw_nonlocal * outer_gate * (
        drive_abs / (drive_scale + EPS)
        + PARAMS["eta_signed"] * signed_shape_s
        + PARAMS["zeta_disk"] * disk_like
    )
    corr = np.clip(np.tanh(corr_raw), -PARAMS["corr_cap"], PARAMS["corr_cap"])

    shape_uplift = np.maximum(base_shape * (1.0 + corr), base_shape)

    anchor = 0
    scale_shape = vobs[anchor] / (shape_uplift[anchor] + EPS)
    vshape = scale_shape * shape_uplift

    residual_need = np.maximum(vobs - vbar, 0.0)
    proposed_add = np.maximum(vshape - vbar, 0.0)
    allowed_add = PARAMS["need_fraction_cap"] * residual_need
    actual_add = np.minimum(proposed_add, allowed_add)

    vbridge = vbar + actual_add

    return {
        "vbar": vbar,
        "vbridge": vbridge,
        "rmse_bar": rmse(vobs, vbar),
        "rmse_bridge": rmse(vobs, vbridge),
        "improvement": rmse(vobs, vbar) - rmse(vobs, vbridge),
        "vflat_obs": extract_vflat(rad, vobs),
        "vflat_bridge": extract_vflat(rad, vbridge),
    }

def evaluate_dataset(df):
    rows = []
    rar_rows = []

    for _, r in df.iterrows():
        galaxy = r["galaxy"]
        rad = parse_array(r["rad"])
        vobs = parse_array(r["vobs"])
        sd_gas = parse_array(r["sd_gas"])

        n = min(len(rad), len(vobs), len(sd_gas))
        rad, vobs, sd_gas = rad[:n], vobs[:n], sd_gas[:n]

        mgas_total = float(r["mgas_total"])
        mstar_total = float(r["mstar_total"])

        out = gas_first_bridge(rad, vobs, sd_gas, mgas_total, mstar_total)

        rows.append({
            "galaxy": galaxy,
            "n_points": n,
            "rmse_bar": out["rmse_bar"],
            "rmse_bridge": out["rmse_bridge"],
            "improvement": out["improvement"],
            "vflat_obs": out["vflat_obs"],
            "vflat_bridge": out["vflat_bridge"],
            "catastrophic_failure": bool(out["improvement"] < -10.0),
        })

        g_obs = compute_acceleration(rad, vobs)
        g_bar = compute_acceleration(rad, out["vbar"])
        g_bridge = compute_acceleration(rad, out["vbridge"])

        rar_rows.append(pd.DataFrame({
            "galaxy": galaxy,
            "Rad": rad,
            "log10_g_obs": np.log10(np.maximum(g_obs, EPS)),
            "log10_g_bar": np.log10(np.maximum(g_bar, EPS)),
            "log10_g_bridge": np.log10(np.maximum(g_bridge, EPS)),
        }))

    summary = pd.DataFrame(rows)
    rar = pd.concat(rar_rows, ignore_index=True)

    aggregate = {
        "n": int(len(summary)),
        "positive_improvement_rate": float((summary["improvement"] > 0).mean()),
        "mean_improvement": float(summary["improvement"].mean()),
        "catastrophic_failures": int(summary["catastrophic_failure"].sum()),
        "rar_baryonic_scatter": float(np.sqrt(np.mean((rar["log10_g_obs"] - rar["log10_g_bar"]) ** 2))),
        "rar_bridge_scatter": float(np.sqrt(np.mean((rar["log10_g_obs"] - rar["log10_g_bridge"]) ** 2))),
    }

    return summary, rar, aggregate

# Example usage:
# df = pd.read_csv("your_radial_curve_dataset.csv")
# summary, rar, aggregate = evaluate_dataset(df)
# print(summary)
# print(aggregate)
