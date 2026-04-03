
from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
import pandas as pd
from scipy.optimize import minimize

# ============================================================
# Frozen solved core from the coefficient-eliminated fixed point
# ============================================================
SIGMA_STAR = 0.7332746
DF_STAR = 2.0 + SIGMA_STAR
GAMMA_STAR = 1.0 - SIGMA_STAR
ETA_STAR = 0.7563147
DELTA_STAR = GAMMA_STAR ** 3
BETA_STAR = -1.0  # strict frozen-core first pass


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


# ============================================================
# Core UQCF-inspired model family
# ============================================================
def model_M0(x: np.ndarray, A0: float) -> np.ndarray:
    return np.full_like(x, A0, dtype=float)


def model_M1(
    x: np.ndarray,
    A1: float,
    gamma: float = GAMMA_STAR,
    beta: float = BETA_STAR,
) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return A1 * np.power(x, -gamma) * (1.0 + beta * np.log(x))


def gaussian_bump(x: np.ndarray, xc: float, w: float) -> np.ndarray:
    t = np.log(x) - np.log(xc)
    return np.exp(-(t * t) / (2.0 * w * w))


def damping(x: np.ndarray, xd: float, p: float) -> np.ndarray:
    return np.exp(-np.power(x / xd, p))


def model_M2(
    x: np.ndarray,
    A2: float,
    xc: float,
    w: float,
    xd: float,
    p: float,
    gamma: float = GAMMA_STAR,
    beta: float = BETA_STAR,
    delta: float = DELTA_STAR,
) -> np.ndarray:
    core = model_M1(x, A2, gamma=gamma, beta=beta)
    bump = 1.0 + delta * gaussian_bump(x, xc, w)
    damp = damping(x, xd, p)
    return core * bump * damp


# ============================================================
# Metrics and fitting helpers
# ============================================================
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


# ============================================================
# Dataset loaders
# ============================================================
def load_planck_csv(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    df = pd.read_csv(path)
    # Expect columns from the current reproducibility bundle:
    # Lgeom, C_data, sigma_C
    x = df["Lgeom"].to_numpy(dtype=float)
    y = df["C_data"].to_numpy(dtype=float)
    sigma = df["sigma_C"].to_numpy(dtype=float)
    return x, y, sigma


def load_desi_stub(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    This is a placeholder loader for a frozen-core *shape* pass on the parsed
    DESI mean vector CSV in the current bundle. Because the full observable map
    from the original fitting code is not bundled here, we run the same nested
    family against the parsed mean vector index as a consistency / sensitivity
    probe, not as a replacement for the original full DESI model.
    """
    df = pd.read_csv(path)
    x = np.arange(1, len(df) + 1, dtype=float)
    y = df["value"].to_numpy(dtype=float)

    # conservative stub uncertainty if only the parsed mean vector is present
    # (the original full covariance-based fit should be restored when that code
    # is available). This keeps the script runnable and highlights the missing
    # implementation cleanly rather than silently failing.
    sigma = np.maximum(np.abs(y) * 0.05, 1e-6)
    return x, y, sigma


# ============================================================
# Run passes
# ============================================================
def run_nested_family(dataset_name: str, x: np.ndarray, y: np.ndarray, sigma: np.ndarray) -> list[FitResult]:
    results: list[FitResult] = []

    results.append(
        fit_model(
            dataset_name=dataset_name,
            model_name="M0_amplitude_only",
            model_fn=model_M0,
            x=x,
            y=y,
            sigma=sigma,
            p0=[float(np.median(y))],
            bounds=[(1e-20, None)],
            param_names=["A0"],
        )
    )

    results.append(
        fit_model(
            dataset_name=dataset_name,
            model_name="M1_frozen_core_only",
            model_fn=model_M1,
            x=x,
            y=y,
            sigma=sigma,
            p0=[float(np.median(y))],
            bounds=[(1e-20, None)],
            param_names=["A1"],
        )
    )

    results.append(
        fit_model(
            dataset_name=dataset_name,
            model_name="M2_frozen_core_plus_minimal_response",
            model_fn=model_M2,
            x=x,
            y=y,
            sigma=sigma,
            p0=[
                float(np.median(y)),  # A2
                float(np.median(x)),  # xc
                0.4,                  # w
                float(np.max(x)),     # xd
                1.5,                  # p
            ],
            bounds=[
                (1e-20, None),              # A2
                (float(np.min(x)), float(np.max(x))),   # xc
                (0.05, 3.0),                # w
                (float(np.min(x)), 10 * float(np.max(x))),  # xd
                (0.1, 5.0),                 # p
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
        for key, val in r.params.items():
            row[key] = val
        rows.append(row)
    pd.DataFrame(rows).to_csv(out_csv, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Frozen-core rerun for UQCF-GEM nested model family.")
    parser.add_argument("--bundle-dir", type=str, required=True, help="Directory containing the reproducibility bundle files.")
    parser.add_argument("--out-dir", type=str, required=True, help="Directory to write result CSVs.")
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Planck aggressive
    pa = bundle_dir / "planck2018_lensing_mv_aggressive_from_table1.csv"
    x, y, sigma = load_planck_csv(pa)
    results = run_nested_family("planck_aggressive_frozen_core", x, y, sigma)
    save_results(results, out_dir / "planck_aggressive_frozen_core_results.csv")

    # Planck conservative
    pc = bundle_dir / "planck2018_lensing_mv_conservative_from_table1.csv"
    x, y, sigma = load_planck_csv(pc)
    results = run_nested_family("planck_conservative_frozen_core", x, y, sigma)
    save_results(results, out_dir / "planck_conservative_frozen_core_results.csv")

    # DESI stub pass
    desi = bundle_dir / "desi_dr2_bao_mean_vector_parsed.csv"
    x, y, sigma = load_desi_stub(desi)
    results = run_nested_family("desi_dr2_frozen_core_stub", x, y, sigma)
    save_results(results, out_dir / "desi_dr2_frozen_core_stub_results.csv")

    # Save frozen-core metadata
    meta = {
        "SIGMA_STAR": SIGMA_STAR,
        "DF_STAR": DF_STAR,
        "GAMMA_STAR": GAMMA_STAR,
        "ETA_STAR": ETA_STAR,
        "DELTA_STAR": DELTA_STAR,
        "BETA_STAR": BETA_STAR,
        "notes": [
            "Planck passes use the bundled transcribed Table 1 CSVs directly.",
            "DESI pass is a stub shape test against the parsed mean vector only.",
            "Full DESI covariance-aware rerun still requires the original observable map / fit implementation.",
        ],
    }
    pd.Series(meta).to_json(out_dir / "frozen_core_metadata.json", indent=2)

    print("Wrote frozen-core rerun outputs to:", out_dir)


if __name__ == "__main__":
    main()
