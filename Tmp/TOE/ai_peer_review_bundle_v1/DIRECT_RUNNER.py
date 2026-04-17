"""
run_restricted_affine_calibration.py

Direct runner for the Restricted Affine Coupling calibration phase.

Expected inputs:
- baseline_anchor.json
- screened_family_vectors.jsonl

This script:
1. loads the baseline anchor
2. computes C0, V0, lambda0, a0, b0
3. calibrates the screened family
4. saves CSV tables and plots

Usage:
    python run_restricted_affine_calibration.py \
        --baseline baseline_anchor.json \
        --screened screened_family_vectors.jsonl \
        --outdir calibration_output
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def cov(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return float(np.mean((x - x.mean()) * (y - y.mean())))


def var(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    return float(np.mean((x - x.mean()) ** 2))


def baseline_residual(q: np.ndarray, p_b: np.ndarray) -> np.ndarray:
    return np.asarray(q, dtype=float) - np.asarray(p_b, dtype=float)


def project_lambda(delta: np.ndarray, r: np.ndarray) -> float:
    vr = var(r)
    if vr <= 0:
        raise ValueError("Residual variance is zero; cannot project update onto residual direction.")
    return cov(delta, r) / vr


def projected_innovation(delta: np.ndarray, r: np.ndarray, lam: float) -> np.ndarray:
    return np.asarray(delta, dtype=float) - lam * np.asarray(r, dtype=float)


def delta_cov(q: np.ndarray, p_b: np.ndarray, p_c: np.ndarray) -> float:
    return cov(q, p_c) - cov(q, p_b)


def delta_var(p_b: np.ndarray, p_c: np.ndarray) -> float:
    return var(p_c) - var(p_b)


def load_baseline(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for key in ["q", "p_b", "p_c_ref"]:
        if key not in data:
            raise KeyError(f"Missing key '{key}' in baseline file.")
    return data


def load_screened_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if not rows:
        raise ValueError("Screened family JSONL file is empty.")
    return rows


def compute_anchor(baseline: dict) -> dict:
    q = np.asarray(baseline["q"], dtype=float)
    p_b = np.asarray(baseline["p_b"], dtype=float)
    p_c_ref = np.asarray(baseline["p_c_ref"], dtype=float)

    if not (len(q) == len(p_b) == len(p_c_ref)):
        raise ValueError("Baseline vectors q, p_b, p_c_ref must have the same length.")

    r = baseline_residual(q, p_b)
    delta0 = p_c_ref - p_b

    C0 = cov(p_b, r)
    V0 = var(r)
    lambda0 = project_lambda(delta0, r)

    denom_a = 2 * C0 + 2 * lambda0 * V0
    if abs(denom_a) < 1e-12:
        raise ValueError("Denominator for a0 is too close to zero.")
    a0 = (C0 + V0) / denom_a

    denom_b = 2 * (C0 + lambda0 * V0)
    if abs(denom_b) < 1e-12:
        raise ValueError("Denominator for b0 is too close to zero.")
    b0 = (lambda0 ** 2 * V0 * (C0 + V0)) / denom_b

    sigma_p = math.sqrt(max(var(p_b), 0.0))
    r4 = float(np.mean(r ** 4))
    r4_term = math.sqrt(max(r4, 0.0))

    return {
        "q": q,
        "p_b": p_b,
        "r": r,
        "C0": C0,
        "V0": V0,
        "lambda0": lambda0,
        "a0": a0,
        "b0": b0,
        "sigma_p": sigma_p,
        "r4_term": r4_term,
    }


def calibrate_screened(anchor: dict, screened_rows: list[dict]) -> pd.DataFrame:
    q_ref = anchor["q"]
    p_b_ref = anchor["p_b"]
    r = anchor["r"]

    results = []
    for row in screened_rows:
        q = np.asarray(row["q"], dtype=float)
        p_b = np.asarray(row["p_b"], dtype=float)
        p_c = np.asarray(row["p_c"], dtype=float)

        if not (len(q) == len(p_b) == len(p_c) == len(q_ref) == len(p_b_ref)):
            raise ValueError(f"Vector length mismatch for point {row.get('label', '<unknown>')}.")

        delta = p_c - p_b
        lam = project_lambda(delta, r)
        xi = projected_innovation(delta, r, lam)
        eta_nu = math.sqrt(max(var(xi), 0.0))

        # Placeholder curvature; replace if you have analytic or empirical curvature estimates
        M_theta = float(row.get("M_theta", 0.0))

        dCov = delta_cov(q, p_b, p_c)
        dVar = delta_var(p_b, p_c)
        eps_obs = dCov - anchor["a0"] * dVar - anchor["b0"]

        eps_bound = (
            abs(anchor["a0"]) * anchor["V0"] * (lam - anchor["lambda0"]) ** 2
            + abs(1 - 2 * anchor["a0"]) * anchor["sigma_p"] * (0.5 * M_theta * anchor["r4_term"] + eta_nu)
            + abs(anchor["a0"]) * (0.5 * M_theta * anchor["r4_term"] + eta_nu) ** 2
        )

        results.append({
            "label": row.get("label", ""),
            "alpha": row.get("alpha", np.nan),
            "beta": row.get("beta", np.nan),
            "nu": row.get("nu", np.nan),
            "delta_cov": dCov,
            "delta_var": dVar,
            "lambda_theta": lam,
            "lambda_drift": abs(lam - anchor["lambda0"]),
            "eta_nu_theta": eta_nu,
            "M_theta": M_theta,
            "epsilon_observed": eps_obs,
            "epsilon_bound": eps_bound,
            "bound_minus_abs_epsilon": eps_bound - abs(eps_obs),
        })

    return pd.DataFrame(results)


def save_outputs(anchor: dict, screened_df: pd.DataFrame, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    anchor_df = pd.DataFrame([{
        "C0": anchor["C0"],
        "V0": anchor["V0"],
        "lambda0": anchor["lambda0"],
        "a0": anchor["a0"],
        "b0": anchor["b0"],
        "sigma_p": anchor["sigma_p"],
        "sqrt_E_r4": anchor["r4_term"],
    }])
    anchor_df.to_csv(outdir / "anchor_constants.csv", index=False)
    screened_df.to_csv(outdir / "screened_family_calibration.csv", index=False)

    # affine overlay
    plt.figure(figsize=(7, 5))
    plt.scatter(screened_df["delta_var"], screened_df["delta_cov"])
    xline = np.linspace(float(screened_df["delta_var"].min()) * 0.95,
                        float(screened_df["delta_var"].max()) * 1.05, 200)
    yline = anchor["a0"] * xline + anchor["b0"]
    plt.plot(xline, yline)
    plt.xlabel("Delta Var")
    plt.ylabel("Delta Cov")
    plt.title("Empirical cloud vs anchored affine line")
    plt.tight_layout()
    plt.savefig(outdir / "affine_overlay.png", dpi=180)
    plt.close()

    # remainder vs bound
    plt.figure(figsize=(7, 5))
    x = np.abs(screened_df["epsilon_observed"].to_numpy())
    y = screened_df["epsilon_bound"].to_numpy()
    plt.scatter(x, y)
    mx = max(float(x.max()), float(y.max())) * 1.05 if len(x) else 1.0
    plt.plot([0, mx], [0, mx], linestyle="--")
    plt.xlabel("|epsilon observed|")
    plt.ylabel("Predicted bound")
    plt.title("Observed remainder vs theorem bound")
    plt.tight_layout()
    plt.savefig(outdir / "remainder_vs_bound.png", dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--screened", required=True, type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()

    baseline = load_baseline(args.baseline)
    screened_rows = load_screened_jsonl(args.screened)

    anchor = compute_anchor(baseline)
    screened_df = calibrate_screened(anchor, screened_rows)
    save_outputs(anchor, screened_df, args.outdir)

    print("Calibration complete.")
    print("Anchor:")
    print(pd.DataFrame([{
        "C0": anchor["C0"],
        "V0": anchor["V0"],
        "lambda0": anchor["lambda0"],
        "a0": anchor["a0"],
        "b0": anchor["b0"],
    }]).to_string(index=False))
    print("\nSaved outputs to:", args.outdir)


if __name__ == "__main__":
    main()
