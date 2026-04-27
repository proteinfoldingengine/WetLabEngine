from pathlib import Path
import pandas as pd
import numpy as np

LOCK_PATH = Path("/content/round12_test_set_locked_strict.csv")
IN_DIR = Path("/content/unseen_galaxy_csvs_strict")
OUT_DIR = Path("/content/round12b_wallaby_results")
OUT_DIR.mkdir(exist_ok=True)

# -------------------------
# frozen 12B parameters
# -------------------------
PARAMS = {
    "alpha_s": 0.10,      # slow memory
    "alpha_f": 0.35,      # fast memory
    "beta": 0.90,         # correction strength
    "eta_signed": 0.25,   # signed curvature contribution
    "L": 2.5,             # nonlocal smoothing length in index-space
    "gate_frac": 0.60,    # outer activation
    "gate_width_frac": 0.18,
    "eps": 1e-9,
}

def rmse(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    return float(np.sqrt(np.mean((a[m] - b[m]) ** 2))) if np.any(m) else np.nan

def smooth_transfer(x, idx, L, eps=1e-9):
    d = np.abs(idx[:, None] - idx[None, :])
    K = np.exp(-d / max(L, eps))
    K /= np.sum(K, axis=1, keepdims=True) + eps
    return K @ x

def compute_round12b_bridge(sub, params=PARAMS):
    eps = params["eps"]

    r = sub["Rad"].to_numpy(float)
    vobs = sub["Vobs"].to_numpy(float)
    sd = sub["sd_proxy"].to_numpy(float)

    # enforce nonnegative gas surface density proxy
    sd = np.maximum(sd, 0.0)

    # normalized radius
    r0 = np.nanmedian(r)
    rnorm = r / (r0 + eps)

    # cumulative gas support
    cum_sd = np.cumsum(sd)
    cum_sd_norm = cum_sd / (np.nanmax(cum_sd) + eps)

    # local gas support
    sd_norm = sd / (np.nanmax(sd) + eps) if np.nanmax(sd) > 0 else np.zeros_like(sd)

    # anchored gas-only baseline shape: sqrt(M(<r)/r)
    gas_shape = np.sqrt(np.maximum(cum_sd_norm / np.maximum(rnorm, eps), 0.0))

    # log-shape derivatives
    log_sd = np.log(np.maximum(sd_norm, eps))
    grad = np.zeros_like(sd_norm)
    grad[1:] = np.diff(log_sd) / np.maximum(np.diff(rnorm), eps)

    curv = np.zeros_like(sd_norm)
    if len(sd_norm) > 2:
        dr = np.diff(rnorm)
        d1 = np.diff(log_sd) / np.maximum(dr, eps)
        d2 = np.diff(d1) / np.maximum((dr[1:] + dr[:-1]) / 2.0, eps)
        curv[2:] = d2

    drive_abs = np.abs(grad) + 0.5 * np.abs(curv)

    # slow / fast memory
    m_s = np.zeros_like(sd_norm)
    m_f = np.zeros_like(sd_norm)
    for i in range(len(sd_norm)):
        ps = m_s[i - 1] if i > 0 else 0.0
        pf = m_f[i - 1] if i > 0 else 0.0
        m_s[i] = (1 - params["alpha_s"]) * ps + params["alpha_s"] * drive_abs[i]
        m_f[i] = (1 - params["alpha_f"]) * pf + params["alpha_f"] * drive_abs[i]

    lam = m_s / (m_s + m_f + eps)
    rw = m_f / (m_s + m_f + eps)

    idx = np.arange(len(sd_norm), dtype=float)
    rw_nonlocal = smooth_transfer(rw, idx, params["L"], eps=eps)

    cscale = np.nanmedian(np.abs(curv[np.abs(curv) > 0])) if np.any(np.abs(curv) > 0) else 1.0
    signed_shape = np.sign(curv) * np.minimum(np.abs(curv) / (cscale + eps), 3.0)
    signed_shape_s = smooth_transfer(signed_shape, idx, params["L"], eps=eps)

    # outer gate
    outer_gate = 1.0 / (1.0 + np.exp(-(rnorm - params["gate_frac"]) / (params["gate_width_frac"] + eps)))

    # correction
    corr_raw = params["beta"] * (1 - lam) * rw_nonlocal * outer_gate * (
        drive_abs / (np.nanmedian(drive_abs[drive_abs > 0]) + eps if np.any(drive_abs > 0) else 1.0)
        + params["eta_signed"] * signed_shape_s
    )
    corr = np.tanh(corr_raw)

    gas_bridge_shape = np.maximum(gas_shape * (1.0 + corr), eps)

    # anchored scaling: fix only the first observed point
    anchor = 0
    scale_base = vobs[anchor] / (gas_shape[anchor] + eps)
    scale_bridge = vobs[anchor] / (gas_bridge_shape[anchor] + eps)

    vpred_base = scale_base * gas_shape
    vpred_bridge = scale_bridge * gas_bridge_shape

    out = sub.copy()
    out["cum_sd_norm"] = cum_sd_norm
    out["sd_norm"] = sd_norm
    out["gas_shape_base"] = gas_shape
    out["gas_shape_bridge"] = gas_bridge_shape
    out["corr_term"] = corr
    out["outer_gate"] = outer_gate
    out["Vpred_base"] = vpred_base
    out["Vpred_bridge"] = vpred_bridge
    return out

rows = []
locked = pd.read_csv(LOCK_PATH)

for _, r in locked.iterrows():
    galaxy = r["galaxy"]
    fn = r["csv_filename"]
    df = pd.read_csv(IN_DIR / fn).copy()

    sub = df[["Rad", "Vobs", "sd_proxy"]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    sub = sub.sort_values("Rad").reset_index(drop=True)

    if len(sub) < 5:
        rows.append({
            "galaxy": galaxy,
            "n_points": len(sub),
            "rmse_base": np.nan,
            "rmse_bridge": np.nan,
            "improvement": np.nan,
            "positive_improvement": False,
            "notes": "too few points"
        })
        continue

    out = compute_round12b_bridge(sub)

    # score from point 1 onward, since point 0 is the anchor
    score_slice = out.iloc[1:].copy()

    rmse_base = rmse(score_slice["Vobs"], score_slice["Vpred_base"])
    rmse_bridge = rmse(score_slice["Vobs"], score_slice["Vpred_bridge"])
    improvement = rmse_base - rmse_bridge

    out.to_csv(OUT_DIR / f"{Path(fn).stem}_round12b_detail.csv", index=False)

    rows.append({
        "galaxy": galaxy,
        "n_points": len(out),
        "rmse_base": rmse_base,
        "rmse_bridge": rmse_bridge,
        "improvement": improvement,
        "positive_improvement": improvement > 0,
        "notes": r["notes"]
    })

res = pd.DataFrame(rows)
res.to_csv(OUT_DIR / "round12b_wallaby_summary.csv", index=False)

print(res.to_string(index=False))

valid = res["improvement"].notna()
agg = {
    "n_scored": int(valid.sum()),
    "positive_rate": float(res.loc[valid, "positive_improvement"].mean()) if valid.any() else np.nan,
    "mean_improvement": float(res.loc[valid, "improvement"].mean()) if valid.any() else np.nan,
    "catastrophic_failures": int((res.loc[valid, "improvement"] < -10.0).sum()) if valid.any() else 0,
}
print("\nAggregate:")
print(agg)

print("\nSaved:", OUT_DIR / "round12b_wallaby_summary.csv")
