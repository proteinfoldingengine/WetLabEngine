
"""
continuum_limit_verifier.py

Structural verifier for the scalar-density memory action candidate in
CONTINUUM_LIMIT.md.

Purpose:
- Test weak-memory decoupling for R_eff = eta * r(x).
- Confirm that V(0)=0 removes O(1) residual stress-energy.
- Separate minimal GR decoupling from the stronger stationary-vacuum condition V'(0)=0.
- Classify coefficient families as PASS, SOFT_FAIL, or HARD_FAIL.

This verifier does not derive the microscopic coefficient functions.
It only tests structural admissibility of the scalar-density candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import sympy as sp


@dataclass(frozen=True)
class Coefficients:
    """Coefficient sample for the scalar-density candidate."""

    v0: float
    v1: float
    ZR: float
    lam: float


def symbolic_weak_memory_expansion() -> Dict[str, str]:
    """Return symbolic weak-memory expansions as strings."""

    eta, chi = sp.symbols("eta chi", positive=True, real=True)
    r, dr2, Tmat = sp.symbols("r dr2 Tmat", real=True)

    ZR, lam = sp.symbols("ZR lam", finite=True, real=True)
    v0, v1, v2, v3, v4 = sp.symbols("v0 v1 v2 v3 v4", real=True)

    R = eta * r

    V = (
        v0
        + v1 * R
        + sp.Rational(1, 2) * v2 * R**2
        + sp.Rational(1, 6) * v3 * R**3
        + sp.Rational(1, 24) * v4 * R**4
    )

    # Scaling proxy for the stress-energy contribution.
    # If R = eta r(x), then (nabla R)^2 = eta^2 (nabla r)^2.
    kinetic_proxy = sp.Rational(1, 2) * ZR * eta**2 * dr2
    interaction_proxy = lam * R * Tmat
    Tmem_proxy = kinetic_proxy + V + interaction_proxy

    expansions = {
        "general": str(sp.series(Tmem_proxy, eta, 0, 3)),
        "V0_zero": str(sp.series(Tmem_proxy.subs(v0, 0), eta, 0, 3)),
        "V0_Vprime0_zero": str(sp.series(Tmem_proxy.subs({v0: 0, v1: 0}), eta, 0, 4)),
    }

    return expansions


def classify_coefficients(
    coeffs: Coefficients,
    require_stationary_vacuum: bool = False,
    singular_cutoff: float = 1e6,
    tol: float = 1e-10,
) -> str:
    """
    Classify weak-memory decoupling for the scalar-density candidate.

    PASS:
        V(0)=0, finite coefficients, T_mem = O(eta) or smaller.

    SOFT_FAIL:
        Weak-memory decoupling holds, but an optional stronger condition
        such as V'(0)=0 is not met.

    HARD_FAIL:
        Residual O(1) term survives or coefficients are singular.
    """

    if abs(coeffs.ZR) > singular_cutoff or abs(coeffs.lam) > singular_cutoff:
        return "HARD_FAIL"

    if abs(coeffs.v0) > tol:
        return "HARD_FAIL"

    if require_stationary_vacuum and abs(coeffs.v1) > tol:
        return "SOFT_FAIL"

    return "PASS"


def run_verifier_sweep(
    n_sweeps: int = 10000,
    require_stationary_vacuum: bool = False,
    seed: int = 7,
) -> Dict[str, float]:
    """Run a reproducible random coefficient-family sweep."""

    rng = np.random.default_rng(seed)
    results = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    for _ in range(n_sweeps):
        # Enforce V(0)=0 in the admissible class most of the time,
        # but inject deliberate residual O(1) failures.
        v0 = 0.0 if rng.random() < 0.95 else float(rng.uniform(-1, 1))
        v1 = float(rng.uniform(-2, 2))
        ZR = float(rng.uniform(0.1, 10.0))
        lam = float(rng.uniform(0.01, 5.0))

        # Inject rare singular failures.
        if rng.random() < 0.005:
            ZR = 1e9
        if rng.random() < 0.005:
            lam = 1e9

        coeffs = Coefficients(v0=v0, v1=v1, ZR=ZR, lam=lam)
        label = classify_coefficients(
            coeffs,
            require_stationary_vacuum=require_stationary_vacuum,
        )
        results[label] += 1

    return {k: 100.0 * v / n_sweeps for k, v in results.items()}


def main() -> None:
    print("Symbolic weak-memory expansions")
    print("=" * 40)
    expansions = symbolic_weak_memory_expansion()
    for name, expansion in expansions.items():
        print(f"\n{name}:")
        print(expansion)

    print("\nWeak-memory decoupling only")
    print("=" * 40)
    print(run_verifier_sweep(require_stationary_vacuum=False))

    print("\nWith stronger stationary-vacuum condition V'(0)=0")
    print("=" * 40)
    print(run_verifier_sweep(require_stationary_vacuum=True))


if __name__ == "__main__":
    main()
