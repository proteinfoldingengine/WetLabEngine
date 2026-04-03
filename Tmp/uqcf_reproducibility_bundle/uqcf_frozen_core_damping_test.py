
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SIGMA_STAR = 0.7332746
DF_STAR = 2.0 + SIGMA_STAR
GAMMA_STAR = 1.0 - SIGMA_STAR
ETA_STAR = 0.7563147
DELTA_STAR = GAMMA_STAR ** 3

@dataclass
class FitResult:
    dataset: str
    model: str
    n: int
    k: int
    chi2: float
    red_chi2: float
    weighted_rms: float
    aic: float
    bic: float
    params: dict

def chi2(y_obs, y_model, sigma):
    r = (y_obs - y_model) / sigma
    return float(np.sum(r * r))

def weighted_rms(y_obs, y_model, sigma):
    w = 1.0 / np.square(sigma)
    return float(np.sqrt(np.sum(w * np.square(y_obs - y_model)) / np.sum(w)))

def info_criteria(chi2_val, k, n):
    aic = chi2_val + 2 * k
    bic = chi2_val + k * np.log(n)
    return float(aic), float(bic)

def fit_model(dataset_name, model_name, model_fn, x, y, sigma, p0, bounds, param_names):
    def objective(theta):
        yhat = model_fn(x, *theta)
        return chi2(y, yhat, sigma)
    res = minimize(objective, x0=np.array(p0, dtype=float), bounds=bounds, method="L-BFGS-B")
    theta = res.x
    yhat = model_fn(x, *theta)
    k = len(theta)
    n = len(x)
    chi2_val = chi2(y, yhat, sigma)
    red_chi2 = chi2_val / max(n - k, 1)
    rms = weighted_rms(y, yhat, sigma)
    aic, bic = info_criteria(chi2_val, k, n)
    return FitResult(dataset_name, model_name, n, k, chi2_val, red_chi2, rms, aic, bic,
                     dict(zip(param_names, map(float, theta))))

def damping(x, xd, p):
    return np.exp(-np.power(x / xd, p))

def model_M0(x, A0):
    return np.full_like(x, A0, dtype=float)

def model_MD(x, A, xd, p):
    return A * damping(x, xd, p)

def model_MDP(x, A, xd, p, q):
    # slight core-shaped perturbation without free bump/window
    x = np.asarray(x, dtype=float)
    return A * damping(x, xd, p) * (1.0 - DELTA_STAR * np.power(x / np.max(x), q))

def load_planck_csv(path):
    df = pd.read_csv(path)
    return (df["Lgeom"].to_numpy(dtype=float),
            df["C_data"].to_numpy(dtype=float),
            df["sigma_C"].to_numpy(dtype=float))

def run_pass(dataset_name, x, y, sigma):
    results = []
    results.append(
        fit_model(dataset_name, "M0_constant", model_M0, x, y, sigma,
                  p0=[float(np.median(y))],
                  bounds=[(1e-20, None)],
                  param_names=["A0"])
    )
    results.append(
        fit_model(dataset_name, "MD_damping_only", model_MD, x, y, sigma,
                  p0=[float(np.median(y)), float(np.max(x)), 1.0],
                  bounds=[(1e-20, None), (float(np.min(x)), 10.0 * float(np.max(x))), (0.1, 5.0)],
                  param_names=["A", "xd", "p"])
    )
    results.append(
        fit_model(dataset_name, "MDP_damping_plus_frozen_core_shape", model_MDP, x, y, sigma,
                  p0=[float(np.median(y)), float(np.max(x)), 1.0, 1.0],
                  bounds=[(1e-20, None), (float(np.min(x)), 10.0 * float(np.max(x))), (0.1, 5.0), (0.1, 4.0)],
                  param_names=["A", "xd", "p", "q"])
    )
    return results

def save_results(results, out_csv):
    rows = []
    for r in results:
        row = {
            "dataset": r.dataset,
            "model": r.model,
            "n": r.n,
            "k": r.k,
            "chi2": r.chi2,
            "red_chi2": r.red_chi2,
            "weighted_rms": r.weighted_rms,
            "aic": r.aic,
            "bic": r.bic,
        }
        row.update(r.params)
        rows.append(row)
    pd.DataFrame(rows).to_csv(out_csv, index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    bundle = Path(args.bundle_dir)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    for name, fname in [
        ("planck_aggressive_damping_test", "planck2018_lensing_mv_aggressive_from_table1.csv"),
        ("planck_conservative_damping_test", "planck2018_lensing_mv_conservative_from_table1.csv"),
    ]:
        x, y, sigma = load_planck_csv(bundle / fname)
        results = run_pass(name, x, y, sigma)
        save_results(results, out / f"{name}_results.csv")

if __name__ == "__main__":
    main()
