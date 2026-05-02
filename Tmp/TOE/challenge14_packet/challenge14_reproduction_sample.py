import numpy as np
import pandas as pd

# Data-agnostic evaluation sample for Challenge 14 style testing.
# Expected columns:
# galaxy, rad, vobs, vgas, vdisk, vbul

def rmse(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    return float(np.sqrt(np.mean((a[m] - b[m]) ** 2))) if np.any(m) else np.nan

def parse_array(x):
    if isinstance(x, (list, np.ndarray)):
        return np.asarray(x, dtype=float)
    return np.array([float(v) for v in str(x).split(",") if str(v).strip() != ""], dtype=float)

def signed_baryonic_velocity(vgas, vdisk, vbul):
    vbar2 = np.sign(vgas) * (vgas ** 2) + vdisk ** 2 + vbul ** 2
    return np.sqrt(np.maximum(vbar2, 0.0))

def simple_bridge(rad, vobs, vgas, vdisk, vbul, need_fraction_cap=0.65):
    rad = np.asarray(rad, float)
    vobs = np.asarray(vobs, float)
    vgas = np.asarray(vgas, float)
    vdisk = np.asarray(vdisk, float)
    vbul = np.asarray(vbul, float)

    vbar = signed_baryonic_velocity(vgas, vdisk, vbul)

    shape = np.maximum(np.abs(vgas), 1e-9)
    shape = shape / np.max(shape)
    vshape = vobs[0] * shape

    residual_need = np.maximum(vobs - vbar, 0.0)
    proposed_add = np.maximum(vshape - vbar, 0.0)
    actual_add = np.minimum(proposed_add, need_fraction_cap * residual_need)

    vbridge = vbar + actual_add
    return vbar, vbridge

def evaluate(df):
    rows = []
    for _, r in df.iterrows():
        rad = parse_array(r["rad"])
        vobs = parse_array(r["vobs"])
        vgas = parse_array(r["vgas"])
        vdisk = parse_array(r["vdisk"])
        vbul = parse_array(r["vbul"])

        n = min(len(rad), len(vobs), len(vgas), len(vdisk), len(vbul))
        rad, vobs, vgas, vdisk, vbul = rad[:n], vobs[:n], vgas[:n], vdisk[:n], vbul[:n]

        vbar, vbridge = simple_bridge(rad, vobs, vgas, vdisk, vbul)

        rows.append({
            "galaxy": r["galaxy"],
            "rmse_bar": rmse(vobs, vbar),
            "rmse_bridge": rmse(vobs, vbridge),
            "improvement": rmse(vobs, vbar) - rmse(vobs, vbridge),
        })
    return pd.DataFrame(rows)
