
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Frozen solved core
SIGMA_STAR = 0.7332746
DF_STAR = 2.0 + SIGMA_STAR
GAMMA_STAR = 1.0 - SIGMA_STAR
ETA_STAR = 0.7563147
DELTA_STAR = GAMMA_STAR ** 3  # ~0.01897


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


# ------------------------------------------------------------------
# Observable-map reconstruction
#
# We use a physically linked reconstruction:
#   DM(z) = A_dm * z * (1+z)^p_dm
#   DH(z) = A_dh * (1+z)^(-p_dh)
#   DV(z) = ( z * DM(z)^2 * DH(z) )^(1/3)
#
# Then apply frozen-core transfer as a minimal multiplicative perturbation.
# This is still a reconstruction scaffold, not a claim of the original DESI
# baseline used in prior nested fits.
# ------------------------------------------------------------------
def dm_model(z: np.ndarray, A_dm: float, p_dm: float) -> np.ndarray:
    return A_dm * z * np.power(1.0 + z, p_dm)


def dh_model(z: np.ndarray, A_dh: float, p_dh: float) -> np.ndarray:
    return A_dh * np.power(1.0 + z, -p_dh)


def dv_from_dm_dh(z: np.ndarray, dm: np.ndarray, dh: np.ndarray) -> np.ndarray:
    return np.power(z * np.square(dm) * dh, 1.0 / 3.0)


def baseline_predict(df: pd.DataFrame, A_dm: float, p_dm: float, A_dh: float, p_dh: float) -> np.ndarray:
    out = []
    for _, row in df.iterrows():
        z = float(row["z"])
        q = row["quantity"]
        dm = dm_model(np.array([z]), A_dm, p_dm)[0]
        dh = dh_model(np.array([z]), A_dh, p_dh)[0]
        dv = dv_from_dm_dh(np.array([z]), np.array([dm]), np.array([dh]))[0]
        if q == "DM_over_rs":
            out.append(dm)
        elif q == "DH_over_rs":
            out.append(dh)
        elif q == "DV_over_rs":
            out.append(dv)
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
        A_dm, p_dm, A_dh, p_dh = map(float, theta)
        yhat = baseline_predict(df, A_dm, p_dm, A_dh, p_dh)
        return chi2_cov(y, yhat, cov)

    p0 = np.array([30.0, 0.0, 25.0, 0.5], dtype=float)
    bounds = [
        (1.0, 100.0),   # A_dm
        (-5.0, 5.0),    # p_dm
        (1.0, 100.0),   # A_dh
        (-5.0, 5.0),    # p_dh
    ]
    opt = minimize(objective, p0, method="L-BFGS-B", bounds=bounds)
    A_dm, p_dm, A_dh, p_dh = map(float, opt.x)
    yhat = baseline_predict(df, A_dm, p_dm, A_dh, p_dh)
    c2 = chi2_cov(y, yhat, cov)
    aic, bic = info_criteria(c2, 4, n)
    return FitSummary(
        model="M1_physical_DM_DH_DV_baseline",
        chi2=c2,
        red_chi2=c2 / max(n - 4, 1),
        aic=aic,
        bic=bic,
        rms_pct=rms_pct(y, yhat),
        params={"A_dm": A_dm, "p_dm": p_dm, "A_dh": A_dh, "p_dh": p_dh},
    )


def fit_frozen_transfer(df: pd.DataFrame, cov: np.ndarray, baseline: FitSummary) -> FitSummary:
    y = df["value"].to_numpy(dtype=float)
    n = len(y)

    def objective(theta: np.ndarray) -> float:
        alpha_dm, alpha_dh, z0, q = map(float, theta)
        base = baseline_predict(df, **baseline.params)
        resp = frozen_core_transfer(df, alpha_dm, alpha_dh, z0, q)
        yhat = base * resp
        return chi2_cov(y, yhat, cov)

    p0 = np.array([1.0, 1.0, 1.0, 1.0], dtype=float)
    bounds = [
        (-5.0, 5.0),   # alpha_dm
        (-5.0, 5.0),   # alpha_dh
        (0.1, 5.0),    # z0
        (-3.0, 3.0),   # q
    ]
    opt = minimize(objective, p0, method="L-BFGS-B", bounds=bounds)
    alpha_dm, alpha_dh, z0, q = map(float, opt.x)
    base = baseline_predict(df, **baseline.params)
    resp = frozen_core_transfer(df, alpha_dm, alpha_dh, z0, q)
    yhat = base * resp
    c2 = chi2_cov(y, yhat, cov)
    aic, bic = info_criteria(c2, 8, n)
    return FitSummary(
        model="M2_frozen_core_transfer_on_physical_baseline",
        chi2=c2,
        red_chi2=c2 / max(n - 8, 1),
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
    parser = argparse.ArgumentParser(description="DESI observable-map reconstruction with frozen-core transfer.")
    parser.add_argument("--mean-csv", required=True)
    parser.add_argument("--cov-txt", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    mean_csv = Path(args.mean_csv)
    cov_txt = Path(args.cov_txt)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_mean(mean_csv)
    cov = load_cov(cov_txt)

    baseline = fit_baseline(df, cov)
    transfer = fit_frozen_transfer(df, cov, baseline)

    results = pd.DataFrame([
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
    ])
    results.to_csv(out_dir / "desi_observable_map_reconstruction_results.csv", index=False)

    pd.Series({
        "SIGMA_STAR": SIGMA_STAR,
        "DF_STAR": DF_STAR,
        "GAMMA_STAR": GAMMA_STAR,
        "ETA_STAR": ETA_STAR,
        "DELTA_STAR": DELTA_STAR,
        "note": "This is a physically linked DM/DH/DV observable-map reconstruction, not the original DESI baseline from earlier nested results.",
    }).to_json(out_dir / "desi_observable_map_reconstruction_metadata.json", indent=2)

    print("Wrote DESI observable-map reconstruction outputs to:", out_dir)


if __name__ == "__main__":
    main()
