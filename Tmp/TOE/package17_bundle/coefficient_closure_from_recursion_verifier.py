
"""
coefficient_closure_from_recursion_verifier.py

Verifier for COEFFICIENT_CLOSURE_FROM_RECURSION.md.

Purpose:
Close the coefficient seam ONLY if production recursion coefficients are supplied.

Input contract:
A JSON file named production_recursion_coefficients.json in the same directory,
with:

{
  "a_R": float,
  "b_R": float,
  "c_R": float,
  "d_R": float,
  "sigma_R": float,
  "a_A": float,
  "b_A": float,
  "d_A": float,
  "sigma_A": float,
  "dt": float,
  "chi": float,
  "eps_star": float
}

If this file is absent, the verifier returns CONDITIONAL_NOT_CLOSED.

If present, it extracts:
    k_R = (1-a_R)/dt
    D_R = sigma_R^2/(2dt)
    lambda_micro = c_R/dt
    Z_R = 1/(2D_R)
    m_R^2 = k_R/D_R
    lambda_int = lambda_micro/D_R

and classifies whether the production recursion is stable and coefficient-valid.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import numpy as np


@dataclass(frozen=True)
class RecursionParams:
    a_R: float
    b_R: float
    c_R: float
    d_R: float
    sigma_R: float
    a_A: float
    b_A: float
    d_A: float
    sigma_A: float
    dt: float
    chi: float
    eps_star: float


def load_params(path: Path):
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["a_R","b_R","c_R","d_R","sigma_R","a_A","b_A","d_A","sigma_A","dt","chi","eps_star"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing required keys: {missing}")
    return RecursionParams(**{k: float(data[k]) for k in required})


def fixed_point(p: RecursionParams):
    M = np.array([[p.a_R, p.b_R], [p.b_A, p.a_A]], dtype=float)
    d = np.array([p.d_R, p.d_A], dtype=float)
    A = np.eye(2) - M
    try:
        x = np.linalg.solve(A, d)
        return float(x[0]), float(x[1])
    except np.linalg.LinAlgError:
        return np.nan, np.nan


def extract(p: RecursionParams):
    M = np.array([[p.a_R, p.b_R], [p.b_A, p.a_A]], dtype=float)
    rho = float(np.max(np.abs(np.linalg.eigvals(M))))

    R_star, A_star = fixed_point(p)
    k_R = (1.0 - p.a_R) / p.dt
    D_R = (p.sigma_R ** 2) / (2.0 * p.dt)
    lambda_micro = p.c_R / p.dt

    if D_R <= 0:
        Z_R = np.nan
        m_R2 = np.nan
        lambda_int = np.nan
        V_quad = np.nan
    else:
        Z_R = 1.0 / (2.0 * D_R)
        m_R2 = k_R / D_R
        lambda_int = lambda_micro / D_R
        V_quad = 0.5 * m_R2

    vals = np.array([rho, R_star, A_star, k_R, D_R, lambda_micro, Z_R, m_R2, lambda_int, V_quad])
    finite = bool(np.all(np.isfinite(vals)))

    pass_conditions = {
        "finite_all": finite,
        "spectral_radius_lt_1": bool(np.isfinite(rho) and rho < 1.0),
        "positive_k_R": bool(np.isfinite(k_R) and k_R > 0),
        "positive_D_R": bool(np.isfinite(D_R) and D_R > 0),
        "positive_m_R2": bool(np.isfinite(m_R2) and m_R2 > 0),
        "finite_lambda_int": bool(np.isfinite(lambda_int) and abs(lambda_int) < 1e6),
        "chi_reasonable": bool(np.isfinite(p.chi) and -10 < p.chi < 10),
        "eps_star_positive": bool(np.isfinite(p.eps_star) and p.eps_star >= 0),
    }

    status = "PASS" if all(pass_conditions.values()) else "FAIL"

    return {
        "status": status,
        "conditions": pass_conditions,
        "inputs": p.__dict__,
        "outputs": {
            "spectral_radius": rho,
            "R_star": R_star,
            "A_star": A_star,
            "k_R": k_R,
            "D_R": D_R,
            "lambda_micro": lambda_micro,
            "Z_R": Z_R,
            "m_R2": m_R2,
            "V_quad": V_quad,
            "lambda_int": lambda_int,
        }
    }


def main():
    here = Path(__file__).resolve().parent
    input_path = here / "production_recursion_coefficients.json"
    p = load_params(input_path)

    print("Coefficient closure from recursion verifier")
    print("=" * 50)

    if p is None:
        print("STATUS: CONDITIONAL_NOT_CLOSED")
        print("Reason: production_recursion_coefficients.json was not supplied.")
        print()
        print("To close this seam, provide JSON with:")
        print("a_R,b_R,c_R,d_R,sigma_R,a_A,b_A,d_A,sigma_A,dt,chi,eps_star")
        return

    result = extract(p)
    print(f"STATUS: {result['status']}")
    print()
    print("Conditions:")
    for k, v in result["conditions"].items():
        print(f"{k}: {v}")
    print()
    print("Extracted coefficients:")
    for k, v in result["outputs"].items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
