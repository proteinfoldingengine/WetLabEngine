
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
import pandas as pd
from scipy.optimize import minimize

# ============================================================
# Frozen solved core
# ============================================================
SIGMA_STAR = 0.7332746
DF_STAR = 2.0 + SIGMA_STAR
GAMMA_STAR = 1.0 - SIGMA_STAR
ETA_STAR = 0.7563147
DELTA_STAR = GAMMA_STAR ** 3  # ~0.01897


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


def chi2(y_obs: np.ndarray, y_model: np.ndarray, sigma: np.ndarray) -> float:
    r = (y_obs - y_model) / sigma
    return float(np.sum(r * r))


def weighted_rms(y_obs: np.ndarray, y_model: np.ndarray, sigma: np.ndarray) -> float:
    w = 1.0 / np.square(sigma)
    return float(np.sqrt(np.sum(w * np.square(y_obs - y_model)) / np.sum(w)))


def info_criteria(chi2_val: float, k: int, n: int) -> tuple[float, float]:
    aic = chi2_val + 2 * k
    bic = chi2_val + k * np.log(n)
    return float(aic), float(bic)


def fit_model(
    dataset_name: str,
    model_name: str,
    model_fn: Callable,
    x: np.ndarray,
    y: np.ndarray,
    sigma: np.ndarray,
    p0: Sequence[float],
    bounds: Sequence[tuple[float | None, float | None]],
    param_names: Sequence[str],
) -> FitResult:
    def objective(theta: np.ndarray) -> float:
        yhat = model_fn(x, *theta)
        return chi2(y, yhat, sigma)

    res = minimize(
        objective,
        x0=np.array(p0, dtype=float),
        bounds=bounds,
        method="L-BFGS-B",
    )
    theta = res.x
    yhat = model_fn(x, *theta)

    k = len(theta)
    n = len(x)
    chi2_val = chi2(y, yhat, sigma)
    red_chi2 = chi2_val / max(n - k, 1)
    rms = weighted_rms(y, yhat, sigma)
    aic, bic = info_criteria(chi2_val, k, n)

    return FitResult(
        dataset=dataset_name,
        model=model_name,
        n=n,
        k=k,
        chi2=chi2_val,
        red_chi2=red_chi2,
        weighted_rms=rms,
        aic=aic,
        bic=bic,
        params=dict(zip(param_names, map(float, theta))),
    )


def gaussian_bump(x: np.ndarray, xc: float, w: float) -> np.ndarray:
    t = np.log(x) - np.log(xc)
    return np.exp(-(t * t) / (2.0 * w * w))


def damping(x: np.ndarray, xd: float, p: float) -> np.ndarray:
    return np.exp(-np.power(x / xd, p))


# -----------------------------------------------------------------
# Planck-facing observable map:
# The bundle tables are already amplitude-like observables around 1,
# so use a constant baseline with a frozen-core perturbation.
# -----------------------------------------------------------------
def model_M0_amp(x: np.ndarray, A0: float) -> np.ndarray:
    return np.full_like(x, A0, dtype=float)


def model_M1_frozen_core_perturbation(
    x: np.ndarray,
    A1: float,
    xc: float,
    w: float,
    delta: float = DELTA_STAR,
) -> np.ndarray:
    return A1 * (1.0 - delta * gaussian_bump(x, xc, w))


def model_M2_frozen_core_perturbation_plus_damping(
    x: np.ndarray,
    A2: float,
    xc: float,
    w: float,
    xd: float,
    p: float,
    delta: float = DELTA_STAR,
) -> np.ndarray:
    return A2 * (1.0 - delta * gaussian_bump(x, xc, w)) * damping(x, xd, p)


def load_planck_csv(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    df = pd.read_csv(path)
    x = df["Lgeom"].to_numpy(dtype=float)
    y = df["C_data"].to_numpy(dtype=float)
    sigma = df["sigma_C"].to_numpy(dtype=float)
    return x, y, sigma


def run_planck_pass(dataset_name: str, x: np.ndarray, y: np.ndarray, sigma: np.ndarray) -> list[FitResult]:
    results: list[FitResult] = []
    results.append(
        fit_model(
            dataset_name, "M0_constant_amplitude",
            model_M0_amp, x, y, sigma,
            p0=[float(np.median(y))],
            bounds=[(1e-20, None)],
            param_names=["A0"],
        )
    )
    results.append(
        fit_model(
            dataset_name, "M1_frozen_core_perturbation",
            model_M1_frozen_core_perturbation, x, y, sigma,
            p0=[float(np.median(y)), float(np.median(x)), 0.5],
            bounds=[
                (1e-20, None),
                (float(np.min(x)), float(np.max(x))),
                (0.05, 3.0),
            ],
            param_names=["A1", "xc", "w"],
        )
    )
    results.append(
        fit_model(
            dataset_name, "M2_frozen_core_plus_damping",
            model_M2_frozen_core_perturbation_plus_damping, x, y, sigma,
            p0=[float(np.median(y)), float(np.median(x)), 0.5, float(np.max(x)), 1.5],
            bounds=[
                (1e-20, None),
                (float(np.min(x)), float(np.max(x))),
                (0.05, 3.0),
                (float(np.min(x)), 10.0 * float(np.max(x))),
                (0.1, 5.0),
            ],
            param_names=["A2", "xc", "w", "xd", "p"],
        )
    )
    return results


def save_results(results: list[FitResult], out_csv: Path) -> None:
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Refined frozen-core Planck rerun for UQCF-GEM.")
    parser.add_argument("--bundle-dir", type=str, required=True)
    parser.add_argument("--out-dir", type=str, required=True)
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # aggressive
    pa = bundle_dir / "planck2018_lensing_mv_aggressive_from_table1.csv"
    x, y, sigma = load_planck_csv(pa)
    res = run_planck_pass("planck_aggressive_refined_frozen_core", x, y, sigma)
    save_results(res, out_dir / "planck_aggressive_refined_frozen_core_results.csv")

    # conservative
    pc = bundle_dir / "planck2018_lensing_mv_conservative_from_table1.csv"
    x, y, sigma = load_planck_csv(pc)
    res = run_planck_pass("planck_conservative_refined_frozen_core", x, y, sigma)
    save_results(res, out_dir / "planck_conservative_refined_frozen_core_results.csv")

    meta = {
        "SIGMA_STAR": SIGMA_STAR,
        "DF_STAR": DF_STAR,
        "GAMMA_STAR": GAMMA_STAR,
        "ETA_STAR": ETA_STAR,
        "DELTA_STAR": DELTA_STAR,
        "observable_map_note": "Constant baseline plus frozen-core perturbation, because the bundled Planck tables are already amplitude-like observables around unity.",
    }
    pd.Series(meta).to_json(out_dir / "refined_frozen_core_metadata.json", indent=2)

    print("Wrote refined frozen-core Planck outputs to:", out_dir)


if __name__ == "__main__":
    main()
