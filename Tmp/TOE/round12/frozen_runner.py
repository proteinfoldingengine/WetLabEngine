from pathlib import Path
import json
import numpy as np
import pandas as pd

PARAMS = {
    "beta": 1.1,
    "L": 3.5,
    "gamma_curv": 1.0,
    "eta_signed": 0.35,
    "zeta_disk": 0.5,
    "gate_frac": 0.85,
    "gate_width_frac": 0.15,
    "alpha_s": 0.08,
    "alpha_f": 0.35,
    "eps": 1e-9,
}

def smooth_transfer(x, r, L, eps=1e-9):
    dr = np.abs(r[:, None] - r[None, :])
    K = np.exp(-dr / max(L, eps))
    K /= np.sum(K, axis=1, keepdims=True) + eps
    return K @ x

def compute_bridge(df: pd.DataFrame, params=PARAMS) -> pd.DataFrame:
    r = df["Rad"].to_numpy(float)
    vobs = df["Vobs"].to_numpy(float)
    vgas = df["Vgas"].to_numpy(float)
    vdisk = df["Vdisk"].to_numpy(float)
    vbul = df["Vbul"].to_numpy(float)

    eps = params["eps"]
    vbar2 = np.sign(vgas) * (vgas ** 2) + vdisk ** 2 + vbul ** 2
    vbar2 = np.maximum(vbar2, 0.0)
    vbar = np.sqrt(vbar2)
    gbar = vbar2 / np.maximum(r, eps)

    disk_frac = (np.sign(vgas) * (vgas ** 2) + vdisk ** 2) / np.maximum(vbar2, eps)
    bulge_frac = (vbul ** 2) / np.maximum(vbar2, eps)
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
    radial_shape = np.abs(grad) * (r_norm / (1 + r_norm)) + params["gamma_curv"] * np.abs(curv) * (r_norm**2 / (1 + r_norm**2))
    cscale = np.nanmedian(np.abs(curv[np.abs(curv) > 0])) if np.any(np.abs(curv) > 0) else 1.0
    signed_shape = np.sign(curv) * np.minimum(np.abs(curv) / (cscale + eps), 3.0)

    drive_abs = radial_shape * (1 + params["zeta_disk"] * component_weight)
    m_s = np.zeros_like(gbar)
    m_f = np.zeros_like(gbar)
    for i in range(len(r)):
        ps = m_s[i - 1] if i > 0 else 0.0
        pf = m_f[i - 1] if i > 0 else 0.0
        m_s[i] = (1 - params["alpha_s"]) * ps + params["alpha_s"] * drive_abs[i]
        m_f[i] = (1 - params["alpha_f"]) * pf + params["alpha_f"] * drive_abs[i]

    lam = m_s / (m_s + m_f + eps)
    rw = m_f / (m_s + m_f + eps)

    a0 = np.nanmedian(gbar)
    rw_nonlocal = smooth_transfer(rw, r, L=params["L"], eps=eps)
    shape_scale = np.nanmedian(radial_shape[radial_shape > 0]) if np.any(radial_shape > 0) else 1.0
    pos_shape = smooth_transfer(radial_shape / (shape_scale + eps), r, L=params["L"], eps=eps)
    signed_shape_s = smooth_transfer(signed_shape, r, L=params["L"], eps=eps)

    r0 = np.nanmedian(r)
    outer_gate = 1.0 / (1.0 + np.exp(-(r - params["gate_frac"] * r0) / (params["gate_width_frac"] * r0 + eps)))
    low_acc = a0 / (gbar + a0 + eps)

    corr_raw = params["beta"] * (1 - lam) * rw_nonlocal * low_acc * outer_gate * (
        (1 + params["zeta_disk"] * component_weight) * pos_shape + params["eta_signed"] * signed_shape_s
    )
    corr = np.tanh(corr_raw)
    gbridge = np.maximum(gbar * (1.0 + corr), 0.0)
    vbridge = np.sqrt(np.maximum(gbridge * r, 0.0))

    out = df.copy()
    out["Vbar"] = vbar
    out["Vbridge"] = vbridge
    out["improvement_pointwise"] = np.abs(vobs - vbar) - np.abs(vobs - vbridge)
    return out

def score_galaxy(csv_path):
    df = pd.read_csv(csv_path)
    need = ["Rad", "Vobs", "Vgas", "Vdisk", "Vbul"]
    df = df[need].replace([np.inf, -np.inf], np.nan).dropna().copy()
    out = compute_bridge(df)
    rmse_bary = float(np.sqrt(np.mean((out["Vobs"] - out["Vbar"]) ** 2)))
    rmse_bridge = float(np.sqrt(np.mean((out["Vobs"] - out["Vbridge"]) ** 2)))
    improvement = rmse_bary - rmse_bridge
    return {
        "galaxy_file": str(csv_path),
        "n_points_used": int(len(out)),
        "rmse_baryonic": rmse_bary,
        "rmse_bridge": rmse_bridge,
        "improvement": improvement,
        "positive_improvement": bool(improvement > 0),
        "catastrophic_failure": bool(improvement < -10.0),
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python frozen_runner.py galaxy.csv")
        raise SystemExit(1)
    result = score_galaxy(sys.argv[1])
    print(json.dumps(result, indent=2))
