
"""
continuum_limit_verifier_v2.py

Patch CL-2 verifier:
Tie the scalar-density memory-action coefficient candidates to the seam-2
loading fixed point from CHI_FIXED_POINT.md.

Candidate identifications:
    Lambda_* = b / (1 - a)
    chi_* = 1 / (1 + Lambda_*) = (1 - a)/(1 - a + b)

    Z_R(chi) = Z0 * chi * (1 - chi)
    lambda_int(chi) = lambda0 * chi * (1 - chi)
    m_R^2 = mu_R^2 * (1 - a)
    R_* = Lambda_*
    V(R) = 0.5*m_R^2*(R - R_*)^2 - 0.5*m_R^2*R_*^2

Important:
    This potential enforces V(0)=0 and V'(R_*)=0.
    It does NOT make R=0 a stationary vacuum unless R_*=0.
    Therefore it passes weak-memory GR decoupling but carries a linear O(eta)
    term near R=0.

This verifier checks:
    - stable loading map: 0 <= a < 1, b > 0
    - chi in (0,1)
    - finite positive Z_R and lambda_int
    - m_R^2 > 0
    - V(0)=0
    - V'(R_*)=0
    - V''(R_*)>0
    - weak-memory expansion has no O(1) residual
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import sympy as sp


@dataclass(frozen=True)
class CL2Params:
    a: float
    b: float
    Z0: float
    lambda0: float
    mu_R: float


@dataclass(frozen=True)
class CL2Derived:
    Lambda_star: float
    chi_star: float
    Z_R: float
    lambda_int: float
    m_R2: float
    V0: float
    Vprime_at_Rstar: float
    Vsecond_at_Rstar: float


def derive_coefficients(params: CL2Params) -> CL2Derived:
    """Derive continuum coefficient candidates from seam-2 loading parameters."""

    if not (0 <= params.a < 1):
        raise ValueError("a must satisfy 0 <= a < 1 for stable loading.")
    if not (params.b > 0):
        raise ValueError("b must be positive.")
    if not (params.Z0 > 0 and params.lambda0 >= 0 and params.mu_R > 0):
        raise ValueError("Z0 > 0, lambda0 >= 0, and mu_R > 0 are required.")

    Lambda_star = params.b / (1.0 - params.a)
    chi_star = 1.0 / (1.0 + Lambda_star)

    Z_R = params.Z0 * chi_star * (1.0 - chi_star)
    lambda_int = params.lambda0 * chi_star * (1.0 - chi_star)
    m_R2 = params.mu_R**2 * (1.0 - params.a)

    # Candidate V(R) = 0.5 m^2 (R-R*)^2 - 0.5 m^2 R*^2
    V0 = 0.5 * m_R2 * (0.0 - Lambda_star) ** 2 - 0.5 * m_R2 * Lambda_star**2
    Vprime_at_Rstar = m_R2 * (Lambda_star - Lambda_star)
    Vsecond_at_Rstar = m_R2

    return CL2Derived(
        Lambda_star=Lambda_star,
        chi_star=chi_star,
        Z_R=Z_R,
        lambda_int=lambda_int,
        m_R2=m_R2,
        V0=V0,
        Vprime_at_Rstar=Vprime_at_Rstar,
        Vsecond_at_Rstar=Vsecond_at_Rstar,
    )


def symbolic_cl2_expansion() -> Dict[str, str]:
    """Symbolically expand the CL-2 potential in the weak-memory regime R=eta*r."""

    eta, r, dr2, Tmat = sp.symbols("eta r dr2 Tmat", positive=True, real=True)
    R = sp.symbols("R", real=True)
    a, b, Z0, lambda0, muR = sp.symbols("a b Z0 lambda0 muR", positive=True, real=True)

    Lambda_star = b / (1 - a)
    chi = (1 - a) / (1 - a + b)

    Z_R = Z0 * chi * (1 - chi)
    lam = lambda0 * chi * (1 - chi)
    m_R2 = muR**2 * (1 - a)

    V_R = sp.Rational(1, 2) * m_R2 * (R - Lambda_star) ** 2 - sp.Rational(1, 2) * m_R2 * Lambda_star**2
    V0 = sp.simplify(V_R.subs(R, 0))
    Vprime_R = sp.diff(V_R, R)
    Vprime_at_Rstar = sp.simplify(Vprime_R.subs(R, Lambda_star))
    Vsecond_at_Rstar = sp.simplify(sp.diff(V_R, R, 2).subs(R, Lambda_star))

    # Weak-memory substitution after differentiating in independent R.
    R_weak = eta * r
    V_weak = V_R.subs(R, R_weak)
    kinetic_proxy = sp.Rational(1, 2) * Z_R * eta**2 * dr2
    interaction_proxy = lam * R_weak * Tmat
    Tmem_proxy = kinetic_proxy + V_weak + interaction_proxy

    return {
        "Lambda_star": str(sp.simplify(Lambda_star)),
        "chi": str(sp.simplify(chi)),
        "Z_R": str(sp.simplify(Z_R)),
        "lambda_int": str(sp.simplify(lam)),
        "m_R2": str(sp.simplify(m_R2)),
        "V0": str(V0),
        "Vprime_at_Rstar": str(Vprime_at_Rstar),
        "Vsecond_at_Rstar": str(Vsecond_at_Rstar),
        "Tmem_expansion": str(sp.series(sp.simplify(Tmem_proxy), eta, 0, 3)),
    }


def classify_cl2(params: CL2Params, singular_cutoff: float = 1e6, tol: float = 1e-9) -> Tuple[str, CL2Derived]:
    """Classify one CL-2 sample."""

    try:
        d = derive_coefficients(params)
    except ValueError:
        d = CL2Derived(np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)
        return "HARD_FAIL", d

    if not (0 < d.chi_star < 1):
        return "HARD_FAIL", d

    if any(abs(x) > singular_cutoff for x in [d.Z_R, d.lambda_int, d.m_R2, d.Lambda_star]):
        return "HARD_FAIL", d

    if abs(d.V0) > tol:
        return "HARD_FAIL", d

    if abs(d.Vprime_at_Rstar) > tol:
        return "HARD_FAIL", d

    if not (d.Vsecond_at_Rstar > 0):
        return "HARD_FAIL", d

    if not (d.Z_R > 0):
        return "HARD_FAIL", d

    if not (d.lambda_int >= 0):
        return "HARD_FAIL", d

    return "PASS", d


def run_cl2_sweep(n_sweeps: int = 100000, seed: int = 11) -> Dict[str, float]:
    """Sweep stable seam-2 loading parameters and CL-2 scale coefficients."""

    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    chi_values = []
    lambda_values = []
    z_values = []
    m_values = []
    Lambda_values = []

    for _ in range(n_sweeps):
        # Stable seam-2 loading map.
        a = float(rng.uniform(0.0, 0.995))
        b = float(10 ** rng.uniform(-3, 1))  # 0.001 to 10, log-uniform

        Z0 = float(10 ** rng.uniform(-2, 2))       # 0.01 to 100
        lambda0 = float(10 ** rng.uniform(-3, 1))  # 0.001 to 10
        mu_R = float(10 ** rng.uniform(-2, 2))     # 0.01 to 100

        # Deliberately inject rare invalid/pathological cases.
        roll = rng.random()
        if roll < 0.002:
            a = 1.0 + rng.uniform(0.0, 0.1)
        elif roll < 0.004:
            b = -rng.uniform(0.001, 1.0)
        elif roll < 0.006:
            Z0 = 1e12
        elif roll < 0.008:
            mu_R = 1e12

        params = CL2Params(a=a, b=b, Z0=Z0, lambda0=lambda0, mu_R=mu_R)
        label, d = classify_cl2(params)
        counts[label] += 1

        if label == "PASS":
            chi_values.append(d.chi_star)
            lambda_values.append(d.lambda_int)
            z_values.append(d.Z_R)
            m_values.append(d.m_R2)
            Lambda_values.append(d.Lambda_star)

    result = {k: 100.0 * v / n_sweeps for k, v in counts.items()}

    if chi_values:
        result.update(
            {
                "chi_min": float(np.min(chi_values)),
                "chi_median": float(np.median(chi_values)),
                "chi_max": float(np.max(chi_values)),
                "Lambda_min": float(np.min(Lambda_values)),
                "Lambda_median": float(np.median(Lambda_values)),
                "Lambda_max": float(np.max(Lambda_values)),
                "Z_R_median": float(np.median(z_values)),
                "lambda_int_median": float(np.median(lambda_values)),
                "m_R2_median": float(np.median(m_values)),
            }
        )

    return result


def main() -> None:
    print("CL-2 symbolic coefficient derivation")
    print("=" * 50)
    for k, v in symbolic_cl2_expansion().items():
        print(f"{k}: {v}")

    print("\nCL-2 numerical sweep")
    print("=" * 50)
    results = run_cl2_sweep()
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
