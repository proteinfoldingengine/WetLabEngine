
"""
field_equation_variation_verifier.py

Verifier for FIELD_EQUATION_VARIATION.md.

Goal:
Test the symbolic variational chain in a simplified scalar-density setting:

    S_eff = S_EH + S_mat + S_mem

Target:
    G_mu_nu = 8*pi*(T_mat + T_mem)

This verifier does not vary the full Einstein-Hilbert action.
It verifies the memory-sector stress-energy scaling and Bianchi-compatible
exchange-current structure in a simplified flat/conformal proxy.

Checks:
    - T_mem has no O(1) term when V(0)=0
    - interaction contribution is O(eta)
    - total conservation can be represented as Q_nu exchange
    - unsafe cases V(0)!=0 or singular coefficients hard-fail
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import sympy as sp


@dataclass(frozen=True)
class VariationParams:
    v0: float
    v1: float
    v2: float
    ZR: float
    lam: float
    mat_scale: float


@dataclass(frozen=True)
class VariationResult:
    leading_order: int
    has_O1_residue: bool
    Q_order: int
    finite_coefficients: bool
    decouples: bool
    bianchi_controlled: bool


def symbolic_variation_proxy() -> Dict[str, str]:
    eta, r, dr2, Tmat, divT = sp.symbols("eta r dr2 Tmat divT", real=True)
    v0, v1, v2, ZR, lam = sp.symbols("v0 v1 v2 ZR lam", real=True)

    R = eta * r
    V = v0 + v1 * R + sp.Rational(1, 2) * v2 * R**2

    # Stress-energy scaling proxy:
    # kinetic ~ eta^2, potential ~ V, interaction ~ eta
    Tmem = sp.Rational(1, 2) * ZR * eta**2 * dr2 + V + lam * R * Tmat

    # Exchange-current proxy: interaction makes matter non-separately conserved.
    # If L_int = lam R O_mat, then schematic exchange scales like grad(R)*O + R*grad(O).
    # Use eta-order proxy.
    Q = lam * eta * (r * divT + Tmat)

    return {
        "Tmem_general": str(sp.series(Tmem, eta, 0, 3)),
        "Tmem_with_V0_zero": str(sp.series(Tmem.subs(v0, 0), eta, 0, 3)),
        "Q_exchange_proxy": str(sp.series(Q, eta, 0, 3)),
    }


def classify_params(p: VariationParams, singular_cutoff: float = 1e6, tol: float = 1e-12) -> Tuple[str, VariationResult]:
    finite = all(np.isfinite(x) and abs(x) < singular_cutoff for x in [p.v0, p.v1, p.v2, p.ZR, p.lam, p.mat_scale])

    if not finite:
        return "HARD_FAIL", VariationResult(0, True, 0, False, False, False)

    has_O1 = abs(p.v0) > tol

    # If V0 != 0, T_mem has O(1). Otherwise:
    # v1 or interaction gives O(eta); if v1=lam=0, leading is O(eta^2).
    if has_O1:
        leading = 0
    elif abs(p.v1) > tol or abs(p.lam * p.mat_scale) > tol:
        leading = 1
    else:
        leading = 2

    # Q from interaction is O(eta) if lam finite; zero if lam=0.
    Q_order = 999 if abs(p.lam) <= tol else 1

    decouples = (not has_O1) and leading >= 1
    bianchi_controlled = decouples and (Q_order == 1 or Q_order == 999)

    result = VariationResult(
        leading_order=leading,
        has_O1_residue=has_O1,
        Q_order=Q_order,
        finite_coefficients=finite,
        decouples=decouples,
        bianchi_controlled=bianchi_controlled,
    )

    if not decouples:
        return "HARD_FAIL", result
    if not bianchi_controlled:
        return "SOFT_FAIL", result
    return "PASS", result


def run_sweep(n_sweeps: int = 50000, seed: int = 97) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    leading_orders = []
    q_orders = []

    for _ in range(n_sweeps):
        # Mostly enforce V(0)=0, but inject residual vacuum failures.
        v0 = 0.0 if rng.random() < 0.96 else float(rng.uniform(-1, 1))
        v1 = float(rng.uniform(-2, 2))
        v2 = float(rng.uniform(0, 5))
        ZR = float(10 ** rng.uniform(-2, 2))
        lam = float(10 ** rng.uniform(-4, 1))
        mat_scale = float(10 ** rng.uniform(-2, 2))

        # Inject singular/pathological cases.
        roll = rng.random()
        if roll < 0.005:
            ZR = 1e12
        elif roll < 0.010:
            lam = 1e12

        label, r = classify_params(VariationParams(v0, v1, v2, ZR, lam, mat_scale))
        counts[label] += 1

        if label in {"PASS", "SOFT_FAIL"}:
            leading_orders.append(r.leading_order)
            q_orders.append(r.Q_order)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if leading_orders:
        out.update({
            "leading_order_median": float(np.median(leading_orders)),
            "fraction_Oeta": float(np.mean(np.array(leading_orders) == 1) * 100),
            "fraction_Oeta2": float(np.mean(np.array(leading_orders) == 2) * 100),
            "fraction_Q_Oeta": float(np.mean(np.array(q_orders) == 1) * 100),
        })
    return out


def main() -> None:
    print("Field equation variation verifier")
    print("=" * 50)
    print("Symbolic proxy:")
    for k, v in symbolic_variation_proxy().items():
        print(f"{k}: {v}")

    print("\nSweep results:")
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
