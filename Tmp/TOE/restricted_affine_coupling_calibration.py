"""
restricted_affine_coupling_calibration.py

Scaffold for the numerical anchoring and calibration phase of the
Restricted Affine Coupling Program.

Fill in the data-loading section with your concrete baseline and screened-family
data, then run the functions in order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import math
import numpy as np


@dataclass
class CalibrationPoint:
    label: str
    q: np.ndarray
    p_b: np.ndarray
    p_c: np.ndarray
    alpha: Optional[float] = None
    beta: Optional[float] = None
    nu: Optional[float] = None


@dataclass
class AnchorConstants:
    C0: float
    V0: float
    lambda0: float
    a0: float
    b0: float
    sigma_p: float
    r_fourth_root_term: float


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


def anchor_constants(q: np.ndarray, p_b: np.ndarray, p_c_ref: np.ndarray) -> AnchorConstants:
    r = baseline_residual(q, p_b)
    delta0 = np.asarray(p_c_ref, dtype=float) - np.asarray(p_b, dtype=float)

    C0 = cov(p_b, r)
    V0 = var(r)
    lambda0 = project_lambda(delta0, r)

    denom = 2 * C0 + 2 * lambda0 * V0
    if abs(denom) < 1e-12:
        raise ValueError("Denominator for a0 is too close to zero.")

    a0 = (C0 + V0) / denom

    denom_b = 2 * (C0 + lambda0 * V0)
    if abs(denom_b) < 1e-12:
        raise ValueError("Denominator for b0 is too close to zero.")

    b0 = (lambda0 ** 2 * V0 * (C0 + V0)) / denom_b

    sigma_p = math.sqrt(max(var(p_b), 0.0))
    r_fourth_root_term = math.sqrt(float(np.mean(r ** 4)))

    return AnchorConstants(
        C0=C0,
        V0=V0,
        lambda0=lambda0,
        a0=a0,
        b0=b0,
        sigma_p=sigma_p,
        r_fourth_root_term=r_fourth_root_term,
    )


def delta_cov(q: np.ndarray, p_b: np.ndarray, p_c: np.ndarray) -> float:
    return cov(q, p_c) - cov(q, p_b)


def delta_var(p_b: np.ndarray, p_c: np.ndarray) -> float:
    return var(p_c) - var(p_b)


def epsilon_observed(dcov: float, dvar: float, a0: float, b0: float) -> float:
    return dcov - a0 * dvar - b0


def eta_nu_from_projection(delta: np.ndarray, r: np.ndarray) -> tuple[float, float]:
    lam = project_lambda(delta, r)
    xi = projected_innovation(delta, r, lam)
    eta_nu = math.sqrt(max(var(xi), 0.0))
    return lam, eta_nu


def remainder_bound(
    anchor: AnchorConstants,
    lambda_theta: float,
    M_theta: float,
    eta_nu_theta: float,
) -> float:
    term1 = abs(anchor.a0) * anchor.V0 * (lambda_theta - anchor.lambda0) ** 2
    term2_inner = 0.5 * M_theta * anchor.r_fourth_root_term + eta_nu_theta
    term2 = abs(1 - 2 * anchor.a0) * anchor.sigma_p * term2_inner
    term3 = abs(anchor.a0) * (term2_inner ** 2)
    return term1 + term2 + term3


def calibrate_points(
    points: Iterable[CalibrationPoint],
    reference_label: str,
    curvature_map: Optional[Dict[str, float]] = None,
) -> Dict[str, object]:
    points = list(points)
    if not points:
        raise ValueError("No calibration points provided.")

    ref = None
    for p in points:
        if p.label == reference_label:
            ref = p
            break
    if ref is None:
        raise ValueError(f"Reference point '{reference_label}' not found.")

    anchor = anchor_constants(ref.q, ref.p_b, ref.p_c)
    r = baseline_residual(ref.q, ref.p_b)

    rows: List[Dict[str, float]] = []
    for p in points:
        dcov = delta_cov(p.q, p.p_b, p.p_c)
        dvar = delta_var(p.p_b, p.p_c)
        eps_obs = epsilon_observed(dcov, dvar, anchor.a0, anchor.b0)

        delta = p.p_c - p.p_b
        lam_theta, eta_nu_theta = eta_nu_from_projection(delta, r)

        M_theta = 0.0
        if curvature_map is not None and p.label in curvature_map:
            M_theta = float(curvature_map[p.label])

        eps_bound = remainder_bound(anchor, lam_theta, M_theta, eta_nu_theta)

        rows.append(
            {
                "label": p.label,
                "alpha": float("nan") if p.alpha is None else float(p.alpha),
                "beta": float("nan") if p.beta is None else float(p.beta),
                "nu": float("nan") if p.nu is None else float(p.nu),
                "delta_cov": dcov,
                "delta_var": dvar,
                "lambda_theta": lam_theta,
                "eta_nu_theta": eta_nu_theta,
                "M_theta": M_theta,
                "epsilon_observed": eps_obs,
                "epsilon_bound": eps_bound,
            }
        )

    return {
        "anchor": anchor,
        "rows": rows,
    }


if __name__ == "__main__":
    print("Fill in your concrete baseline and screened-family data, then call calibrate_points().")
