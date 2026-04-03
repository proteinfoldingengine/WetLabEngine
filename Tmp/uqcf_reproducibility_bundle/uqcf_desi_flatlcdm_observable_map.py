
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

SIGMA_STAR = 0.7332746
DF_STAR = 2.0 + SIGMA_STAR
GAMMA_STAR = 1.0 - SIGMA_STAR
ETA_STAR = 0.7563147
DELTA_STAR = GAMMA_STAR ** 3

@dataclass
class FitSummary:
    model: str
    chi2: float
    red_chi2: float
    aic: float
    bic: float
    rms_pct: float
    params: dict

def load_mean(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_cov(path: Path) -> np.ndarray:
    return np.loadtxt(path, dtype=float)

def chi2_cov(y_obs: np.ndarray, y_model: np.ndarray, cov: np.ndarray) -> float:
    inv = np.linalg.inv(cov)
    r = y_obs - y_model
    return float(r.T @ inv @ r)

def rms_pct(y_obs: np.ndarray, y_model: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square((y_model - y_obs) / y_obs))) * 100.0)

def info_criteria(chi2_val: float, k: int, n: int) -> tuple[float, float]:
    aic = chi2_val + 2 * k
    bic = chi2_val + k * np.log(n)
    return float(aic), float(bic)

def E_of_z(z: np.ndarray, omega_m: float) -> np.ndarray:
    return np.sqrt(omega_m * (1.0 + z) ** 3 + (1.0 - omega_m))

def dm_over_rs_single(z: float, A: float, omega_m: float, n_grid: int = 800) -> float:
    zz = np.linspace(0.0, z, n_grid)
    return float(A * np.trapezoid(1.0 / E_of_z(zz, omega_m), zz))

def dh_over_rs_single(z: float, A: float, omega_m: float) -> float:
    return float(A / E_of_z(np.array([z]), omega_m)[0])

def dv_over_rs_single(z: float, A: float, omega_m: float) -> float:
    dm = dm_over_rs_single(z, A, omega_m)
    dh = dh_over_rs_single(z, A, omega_m)
    return float((z * dm * dm * dh) ** (1.0 / 3.0))

def baseline_predict(df: pd.DataFrame, A: float, omega_m: float) -> np.ndarray:
    out = []
    for _, row in df.iterrows():
        z = float(row["z"])
        q = row["quantity"]
        if q == "DM_over_rs":
            out.append(dm_over_rs_single(z, A, omega_m))
        elif q == "DH_over_rs":
            out.append(dh_over_rs_single(z, A, omega_m))
        elif q == "DV_over_rs":
            out.append(dv_over_rs_single(z, A, omega_m))
        else:
            raise ValueError(f"Unknown quantity: {q}")
    return np.array(out, dtype=float)

def frozen_core_transfer(df: pd.DataFrame, alpha_dm: float, alpha_dh: float, z0: float, q: float) -> np.ndarray:
    z = df["z"].to_numpy(dtype=float)
    quantity = df["quantity"].to_numpy(dtype=object)
    x = np.power(z / z0, q)
    out = np.ones_like(z)

    dm_mask = quantity == "DM_over_rs"
    dh_mask = quantity == "DH_over_rs"
    dv_mask = quantity == "DV_over_rs"

    out[dm_mask] = 1.0 + alpha_dm * DELTA_STAR * x[dm_mask]
    out[dh_mask] = 1.0 - alpha_dh * DELTA_STAR * x[dh_mask]
    out[dv_mask] = 1.0 + 0.5 * (alpha_dm - alpha_dh) * DELTA_STAR * x[dv_mask]
    return out

def fit_baseline(df: pd.DataFrame, cov: np.ndarray) -> FitSummary:
    y = df["value"].to_numpy(dtype=float)
    n = len(y)

    def objective(theta: np.ndarray) -> float:
        A, omega_m = map(float, theta)
        yhat = baseline_predict(df, A, omega_m)
        return chi2_cov(y, yhat, cov)

    p0 = np.array([30.0, 0.3], dtype=float)
    bounds = [(1.0, 100.0), (0.05, 0.95)]
    opt = minimize(objective, p0, method="L-BFGS-B", bounds=bounds)
    A, omega_m = map(float, opt.x)
    yhat = baseline_predict(df, A, omega_m)
    c2 = chi2_cov(y, yhat, cov)
    aic, bic = info_criteria(c2, 2, n)
    return FitSummary(
        model="M1_flatLCDM_linked_baseline",
        chi2=c2,
        red_chi2=c2 / max(n - 2, 1),
        aic=aic,
        bic=bic,
        rms_pct=rms_pct(y, yhat),
        params={"A": A, "omega_m": omega_m},
    )

def fit_frozen_transfer(df: pd.DataFrame, cov: np.ndarray, baseline: FitSummary) -> FitSummary:
    y = df["value"].to_numpy(dtype=float)
    n = len(y)

    def objective(theta: np.ndarray) -> float:
        alpha_dm, alpha_dh, z0, q = map(float, theta)
        base = baseline_predict(df, baseline.params["A"], baseline.params["omega_m"])
        resp = frozen_core_transfer(df, alpha_dm, alpha_dh, z0, q)
        yhat = base * resp
        return chi2_cov(y, yhat, cov)

    p0 = np.array([1.0, 1.0, 1.0, 1.0], dtype=float)
    bounds = [(-5.0, 5.0), (-5.0, 5.0), (0.1, 5.0), (-3.0, 3.0)]
    opt = minimize(objective, p0, method="L-BFGS-B", bounds=bounds)
    alpha_dm, alpha_dh, z0, q = map(float, opt.x)
    base = baseline_predict(df, baseline.params["A"], baseline.params["omega_m"])
    resp = frozen_core_transfer(df, alpha_dm, alpha_dh, z0, q)
    yhat = base * resp
    c2 = chi2_cov(y, yhat, cov)
    aic, bic = info_criteria(c2, 6, n)
    return FitSummary(
        model="M2_frozen_core_transfer_on_flatLCDM_baseline",
        chi2=c2,
        red_chi2=c2 / max(n - 6, 1),
        aic=aic,
        bic=bic,
        rms_pct=rms_pct(y, yhat),
        params={
            **baseline.params,
            "alpha_dm": alpha_dm,
            "alpha_dh": alpha_dh,
            "z0": z0,
            "q": q,
        },
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mean-csv", required=True)
    parser.add_argument("--cov-txt", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_mean(Path(args.mean_csv))
    cov = load_cov(Path(args.cov_txt))

    baseline = fit_baseline(df, cov)
    transfer = fit_frozen_transfer(df, cov, baseline)

    pd.DataFrame([
        {
            "model": baseline.model,
            "chi2": baseline.chi2,
            "red_chi2": baseline.red_chi2,
            "aic": baseline.aic,
            "bic": baseline.bic,
            "rms_pct": baseline.rms_pct,
            **baseline.params,
        },
        {
            "model": transfer.model,
            "chi2": transfer.chi2,
            "red_chi2": transfer.red_chi2,
            "aic": transfer.aic,
            "bic": transfer.bic,
            "rms_pct": transfer.rms_pct,
            **transfer.params,
        },
    ]).to_csv(out_dir / "desi_flatlcdm_observable_map_results.csv", index=False)

    pd.Series({
        "SIGMA_STAR": SIGMA_STAR,
        "DF_STAR": DF_STAR,
        "GAMMA_STAR": GAMMA_STAR,
        "ETA_STAR": ETA_STAR,
        "DELTA_STAR": DELTA_STAR,
        "note": "Flat-LCDM-inspired linked DM/DH/DV reconstruction with frozen-core transfer. Use as a cleaner DESI transfer scaffold, not as a claim of final DESI baseline completeness.",
    }).to_json(out_dir / "desi_flatlcdm_observable_map_metadata.json", indent=2)

if __name__ == "__main__":
    main()
