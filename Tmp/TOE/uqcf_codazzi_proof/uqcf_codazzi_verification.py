#!/usr/bin/env python3
"""
Executable verification harness for the smallest canonical UQCF-GEM
state-level Codazzi audit.

This is an executable mathematical verification, not a formal proof assistant
certificate. It reconstructs every quantity from the exact eight-state
three-spin exponential family; no reported tensor values are hard-coded.

Model
-----
p(x) ∝ exp[h1*x1 + h2*x2 + J*(x1*x2 + x2*x3 + x3*x1)],
x_i ∈ {-1,+1}, h3 = 0.

It verifies:
1. canonical binary Fisher/BKM score extraction;
2. intrinsic covariance-defined edge response;
3. bidirectionally symmetrized pulled-back response tensor;
4. nonzero exponential-affine Codazzi defect at a fixed point;
5. exact spin-flip-protected zero at the unbiased point numerically;
6. full-rank weak-coupling susceptibility;
7. leading J^2 quarter-turn susceptibility structure.

Requirements: Python 3.10+, mpmath.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from typing import Callable

import mpmath as mp


STATES = tuple(itertools.product((-1, 1), repeat=3))
UNDIRECTED_EDGES = ((0, 1), (1, 2), (2, 0))


@dataclass(frozen=True)
class AuditPoint:
    h1: mp.mpf
    h2: mp.mpf
    J: mp.mpf


def probabilities(h1: mp.mpf, h2: mp.mpf, J: mp.mpf) -> list[mp.mpf]:
    weights = []
    for x1, x2, x3 in STATES:
        exponent = h1*x1 + h2*x2 + J*(x1*x2 + x2*x3 + x3*x1)
        weights.append(mp.exp(exponent))
    z = mp.fsum(weights)
    return [w / z for w in weights]


def moments(h1: mp.mpf, h2: mp.mpf, J: mp.mpf):
    p = probabilities(h1, h2, J)
    means = [
        mp.fsum(px * state[i] for px, state in zip(p, STATES))
        for i in range(3)
    ]
    second = [
        [
            mp.fsum(px * state[i] * state[j] for px, state in zip(p, STATES))
            for j in range(3)
        ]
        for i in range(3)
    ]
    variances = [1 - means[i]**2 for i in range(3)]
    covariances = [
        [second[i][j] - means[i]*means[j] for j in range(3)]
        for i in range(3)
    ]
    return means, variances, covariances


def score_coefficients(h1: mp.mpf, h2: mp.mpf, J: mp.mpf):
    """
    For binary natural parameters h1,h2:
        ∂_{h_a} m_i = Cov(x_i, x_a)
    and the canonical local Fisher/BKM score coefficient is
        s_{i,a} = Cov(x_i,x_a) / Var(x_i).
    """
    _, v, c = moments(h1, h2, J)
    return [[c[i][a] / v[i] for a in range(2)] for i in range(3)]


def response_tensor_entry(a: int, b: int, h1: mp.mpf, h2: mp.mpf, J: mp.mpf) -> mp.mpf:
    """
    Bidirectionally symmetrized pulled-back response tensor:
      M_ab = 1/2 Σ_{ {i,j} } c_ij^2 [
          s_{i,a}s_{i,b}/v_j + s_{j,a}s_{j,b}/v_i
      ].
    """
    _, v, c = moments(h1, h2, J)
    s = [[c[i][aa] / v[i] for aa in range(2)] for i in range(3)]
    total = mp.mpf("0")
    for i, j in UNDIRECTED_EDGES:
        cij = c[i][j]
        total += mp.mpf("0.5") * cij**2 * (
            s[i][a]*s[i][b]/v[j] + s[j][a]*s[j][b]/v[i]
        )
    return total


def response_tensor(h1: mp.mpf, h2: mp.mpf, J: mp.mpf):
    return [
        [response_tensor_entry(a, b, h1, h2, J) for b in range(2)]
        for a in range(2)
    ]


def derivative(f: Callable[[mp.mpf], mp.mpf], x: mp.mpf) -> mp.mpf:
    return mp.diff(f, x)


def codazzi(h1: mp.mpf, h2: mp.mpf, J: mp.mpf):
    """
    Independent components on the (h1,h2) flat exponential-affine leaf:
      I_121 = ∂_{h1} M_21 - ∂_{h2} M_11
      I_122 = ∂_{h1} M_22 - ∂_{h2} M_12.
    """
    i121 = derivative(lambda x: response_tensor_entry(1, 0, x, h2, J), h1) \
         - derivative(lambda y: response_tensor_entry(0, 0, h1, y, J), h2)
    i122 = derivative(lambda x: response_tensor_entry(1, 1, x, h2, J), h1) \
         - derivative(lambda y: response_tensor_entry(0, 1, h1, y, J), h2)
    return i121, i122


def susceptibility(J: mp.mpf):
    """Jacobian of (I_121,I_122) with respect to (h1,h2) at h=0."""
    rows = []
    for component in range(2):
        dh1 = derivative(lambda x: codazzi(x, mp.mpf("0"), J)[component], mp.mpf("0"))
        dh2 = derivative(lambda y: codazzi(mp.mpf("0"), y, J)[component], mp.mpf("0"))
        rows.append([dh1, dh2])
    return rows


def det2(matrix) -> mp.mpf:
    return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]


def eigenvalues_symmetric_2x2(matrix):
    a, b = matrix[0]
    _, d = matrix[1]
    center = (a+d)/2
    radius = mp.sqrt(((a-d)/2)**2 + b**2)
    return center+radius, center-radius


def assert_close(actual, expected, tolerance, label):
    error = abs(actual - expected)
    if error > tolerance:
        raise AssertionError(
            f"{label}: actual={mp.nstr(actual, 30)}, "
            f"expected={mp.nstr(expected, 30)}, error={mp.nstr(error, 8)}"
        )


def run_audit(dps: int = 60) -> None:
    mp.mp.dps = dps

    point = AuditPoint(mp.mpf("0.20"), mp.mpf("-0.15"), mp.mpf("0.70"))
    tensor = response_tensor(point.h1, point.h2, point.J)
    defect = codazzi(point.h1, point.h2, point.J)

    expected_tensor = (
        ("1.38129946619327500003604689263", "1.35748327515301168689699113769"),
        ("1.35748327515301168689699113769", "1.39073195464899875795712611409"),
    )
    expected_defect = (
        "-0.345896392762439037790290015984",
        "-0.320972490518245982182853398245",
    )

    tol = mp.mpf("1e-28")
    for i in range(2):
        for j in range(2):
            assert_close(tensor[i][j], mp.mpf(expected_tensor[i][j]), tol, f"M[{i},{j}]")
    for i in range(2):
        assert_close(defect[i], mp.mpf(expected_defect[i]), tol, f"Codazzi[{i}]")

    # Tensor symmetry and positive definiteness.
    assert_close(tensor[0][1], tensor[1][0], tol, "tensor symmetry")
    eig_hi, eig_lo = eigenvalues_symmetric_2x2(tensor)
    if eig_lo <= 0:
        raise AssertionError(f"Response tensor is not positive definite: eigenvalues={eig_hi}, {eig_lo}")

    # Spin-flip-protected zero at the unbiased point.
    unbiased = codazzi(mp.mpf("0"), mp.mpf("0"), mp.mpf("0.1"))
    if max(abs(unbiased[0]), abs(unbiased[1])) > mp.mpf("1e-45"):
        raise AssertionError(f"Unbiased Codazzi defect should vanish; got {unbiased}")

    # Full-rank susceptibility and J^2 leading quarter-turn structure.
    J_small = mp.mpf("0.001")
    xi = susceptibility(J_small)
    determinant = det2(xi)
    if abs(determinant) <= mp.mpf("1e-30"):
        raise AssertionError(f"Susceptibility is not full rank: det={determinant}")

    scaled = [[xi[i][j] / J_small**2 for j in range(2)] for i in range(2)]
    quarter_turn = ((0, 1), (-1, 0))
    max_scaled_error = max(
        abs(scaled[i][j] - quarter_turn[i][j]) for i in range(2) for j in range(2)
    )
    # At J=1e-3, O(J) corrections are about 4e-3.
    if max_scaled_error > mp.mpf("0.006"):
        raise AssertionError(
            f"Scaled susceptibility does not approach the predicted quarter-turn; "
            f"max error={max_scaled_error}"
        )

    print("UQCF-GEM CODAZZI VERIFICATION: PASS")
    print()
    print("Audit point: h1=0.20, h2=-0.15, J=0.70")
    print("Bidirectionally symmetrized response tensor:")
    for row in tensor:
        print("  [" + ", ".join(mp.nstr(value, 18) for value in row) + "]")
    print("Eigenvalues:", mp.nstr(eig_hi, 18), mp.nstr(eig_lo, 18))
    print("Codazzi defect:", tuple(mp.nstr(value, 18) for value in defect))
    print()
    print("Unbiased-point defect at J=0.1:",
          tuple(mp.nstr(value, 8) for value in unbiased))
    print()
    print("Susceptibility at J=0.001:")
    for row in xi:
        print("  [" + ", ".join(mp.nstr(value, 18) for value in row) + "]")
    print("det(Xi) =", mp.nstr(determinant, 18))
    print("Xi / J^2:")
    for row in scaled:
        print("  [" + ", ".join(mp.nstr(value, 18) for value in row) + "]")
    print()
    print("Interpretation:")
    print("  * The canonical symmetrized response tensor is positive and symmetric.")
    print("  * Its exponential-affine Codazzi defect is robustly nonzero at the audit point.")
    print("  * Spin-flip symmetry forces a pointwise zero at h1=h2=0.")
    print("  * The field susceptibility at that zero is full rank for weak nonzero J.")
    print("  * The leading susceptibility is J^2 times a quarter-turn matrix.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dps", type=int, default=60, help="mpmath decimal precision")
    args = parser.parse_args()
    run_audit(args.dps)


if __name__ == "__main__":
    main()
