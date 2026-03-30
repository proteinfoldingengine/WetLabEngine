from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Tuple
import json
import math
import numpy as np
import pandas as pd

C_LIGHT = 299792.458  # km/s

@dataclass
class BAOBin:
    z: float
    DM_over_rd: float
    sigma_DM_over_rd: float
    DH_over_rd: float
    sigma_DH_over_rd: float
    rho: float

    def covariance(self) -> np.ndarray:
        return np.array([
            [self.sigma_DM_over_rd**2, self.rho * self.sigma_DM_over_rd * self.sigma_DH_over_rd],
            [self.rho * self.sigma_DM_over_rd * self.sigma_DH_over_rd, self.sigma_DH_over_rd**2]
        ])

    def f_ap_data(self) -> Tuple[float, float]:
        dm = self.DM_over_rd
        dh = self.DH_over_rd
        f = dm / dh
        grad = np.array([1.0 / dh, -dm / (dh * dh)])
        var = grad @ self.covariance() @ grad
        return f, math.sqrt(max(var, 0.0))

DESI_DR2_GALAXY_BAO: List[BAOBin] = [
    BAOBin(z=0.510, DM_over_rd=13.587, sigma_DM_over_rd=0.169, DH_over_rd=21.863, sigma_DH_over_rd=0.427, rho=-0.475),
    BAOBin(z=0.706, DM_over_rd=17.347, sigma_DM_over_rd=0.180, DH_over_rd=19.458, sigma_DH_over_rd=0.332, rho=-0.423),
    BAOBin(z=0.934, DM_over_rd=21.574, sigma_DM_over_rd=0.153, DH_over_rd=17.641, sigma_DH_over_rd=0.193, rho=-0.425),
    BAOBin(z=1.321, DM_over_rd=27.605, sigma_DM_over_rd=0.320, DH_over_rd=14.178, sigma_DH_over_rd=0.217, rho=-0.437),
    BAOBin(z=1.484, DM_over_rd=30.519, sigma_DM_over_rd=0.758, DH_over_rd=12.816, sigma_DH_over_rd=0.513, rho=-0.489),
]

def cumulative_trapezoid(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    out = np.zeros_like(x, dtype=float)
    for i in range(1, len(x)):
        out[i] = out[i-1] + 0.5 * (y[i] + y[i-1]) * (x[i] - x[i-1])
    return out

def compute_distances_from_H(z_values: np.ndarray, H_of_z: Callable[[np.ndarray], np.ndarray]) -> Dict[str, np.ndarray]:
    z_values = np.asarray(z_values, dtype=float)
    z_grid = np.linspace(0.0, float(np.max(z_values)), 4000)
    H_grid = H_of_z(z_grid)
    integrand = C_LIGHT / H_grid
    DM_grid = cumulative_trapezoid(z_grid, integrand)
    DM_interp = np.interp(z_values, z_grid, DM_grid)
    DH = C_LIGHT / H_of_z(z_values)
    return {"z": z_values, "DM_Mpc": DM_interp, "DH_Mpc": DH}

def evaluate_bao_model(rd_Mpc: float, H_of_z: Callable[[np.ndarray], np.ndarray], bins: List[BAOBin] = DESI_DR2_GALAXY_BAO) -> pd.DataFrame:
    z = np.array([b.z for b in bins], dtype=float)
    d = compute_distances_from_H(z, H_of_z)
    DM_over_rd_model = d["DM_Mpc"] / rd_Mpc
    DH_over_rd_model = d["DH_Mpc"] / rd_Mpc
    F_AP_model = d["DM_Mpc"] / d["DH_Mpc"]

    rows = []
    for i, b in enumerate(bins):
        f_data, sigma_f = b.f_ap_data()
        rows.append({
            "z": b.z,
            "DM_over_rd_data": b.DM_over_rd,
            "DH_over_rd_data": b.DH_over_rd,
            "DM_over_rd_model": DM_over_rd_model[i],
            "DH_over_rd_model": DH_over_rd_model[i],
            "F_AP_data": f_data,
            "sigma_F_AP": sigma_f,
            "F_AP_model": F_AP_model[i],
        })
    return pd.DataFrame(rows)

def chi2_bao(rd_Mpc: float, H_of_z: Callable[[np.ndarray], np.ndarray], bins: List[BAOBin] = DESI_DR2_GALAXY_BAO) -> Dict[str, float]:
    z = np.array([b.z for b in bins], dtype=float)
    d = compute_distances_from_H(z, H_of_z)
    DM_over_rd_model = d["DM_Mpc"] / rd_Mpc
    DH_over_rd_model = d["DH_Mpc"] / rd_Mpc

    total = 0.0
    for i, b in enumerate(bins):
        data_vec = np.array([b.DM_over_rd, b.DH_over_rd], dtype=float)
        model_vec = np.array([DM_over_rd_model[i], DH_over_rd_model[i]], dtype=float)
        delta = model_vec - data_vec
        cov_inv = np.linalg.inv(b.covariance())
        total += float(delta.T @ cov_inv @ delta)

    n_points = 2 * len(bins)
    return {"chi2": total, "n_points": n_points, "reduced_chi2_if_no_free_params": total / n_points}
