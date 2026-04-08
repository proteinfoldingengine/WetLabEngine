#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
import pandas as pd

A_bridge = 0.40117290 - 0.37911244
z_c = 1.0
p = 2.0
Omega_m = 0.30

def E0(z):
    z = np.asarray(z, dtype=float)
    return np.sqrt(Omega_m * (1 + z) ** 3 + (1 - Omega_m))

def S(z):
    z = np.asarray(z, dtype=float)
    return (z / z_c) ** p / (1 + (z / z_c) ** p)

def E_bridge(z):
    z = np.asarray(z, dtype=float)
    return E0(z) * (1 + A_bridge * S(z))

def main():
    z = np.linspace(0.1, 2.33, 600)
    E0_vals = E0(z)
    Eb_vals = E_bridge(z)
    H_ratio = Eb_vals / E0_vals
    invE0 = 1.0 / E0_vals
    invEb = 1.0 / Eb_vals
    dz = np.diff(z)
    cum0 = np.zeros_like(z)
    cumb = np.zeros_like(z)
    cum0[1:] = np.cumsum(0.5 * (invE0[:-1] + invE0[1:]) * dz)
    cumb[1:] = np.cumsum(0.5 * (invEb[:-1] + invEb[1:]) * dz)
    DM_ratio = np.divide(cumb, cum0, out=np.ones_like(cumb), where=cum0 != 0.0)
    FAP_ratio = H_ratio * DM_ratio
    sample_z = np.array([0.51, 0.71, 0.93, 1.32, 1.48, 2.10, 2.33])
    sample_df = pd.DataFrame({
        "z": sample_z,
        "H_ratio": np.interp(sample_z, z, H_ratio),
        "DM_ratio": np.interp(sample_z, z, DM_ratio),
        "FAP_ratio": np.interp(sample_z, z, FAP_ratio),
    })
    sample_df["FAP_percent_shift"] = 100.0 * (sample_df["FAP_ratio"] - 1.0)
    out = Path(__file__).resolve().parents[1] / "reproduced" / "observable_proxy"
    out.mkdir(parents=True, exist_ok=True)
    sample_df.to_csv(out / "locked_falsification_grid.csv", index=False)
    summary = {
        "min_shift_percent": float(sample_df["FAP_percent_shift"].min()),
        "max_shift_percent": float(sample_df["FAP_percent_shift"].max()),
        "grid_z": sample_z.tolist()
    }
    (out / "observable_proxy_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
