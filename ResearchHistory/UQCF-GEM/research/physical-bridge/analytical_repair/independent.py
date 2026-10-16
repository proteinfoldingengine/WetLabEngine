#!/usr/bin/env python3
"""Independent, exact reconstruction of the frozen analytical repair universe.

No producer imports, sampling, floating point, fitted constants, or quadrature.
Polynomial coefficients are in increasing power order. Haar simplex integrals,
Bloch-sphere integrals, and commutant linear algebra reconstruct the values.
These finite checks do not certify the accompanying continuum arguments.
"""
from fractions import Fraction as Q
import json
from math import comb
from pathlib import Path
import sys

SOURCE_PARENT = "1ef7d25cedd5af6be6e72fea4e5963414a92cc0a"
CONTRACT_COMMIT = "cbefdb85f21cd9606d1a9260d38176c2dc068b91"
CONTRACT_PATH = "ResearchHistory/UQCF-GEM/research/physical-bridge/analytical_repair/CONTRACT.md"
CONTROL_IDS = ["identical_centralizer", "reader_retention", "block_product",
               "block_resolving", "so3_real", "so3_helicity"]


def integral(coefficients, lower=Q(0), upper=Q(1)):
    """Integrate a polynomial exactly over a rational interval."""
    return sum((Q(c) * (upper ** (i + 1) - lower ** (i + 1)) / (i + 1)
                for i, c in enumerate(coefficients)), Q(0))


def multiply(left, right):
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def complement_power(k):
    return [Q((-1) ** j * comb(k, j)) for j in range(k + 1)]


def absolute_linear_integral(intercept, slope, weight, lower, upper):
    """Integrate |intercept+slope*x| weight(x), splitting at its zero."""
    polynomial = multiply([intercept, slope], weight)
    boundaries = [lower, upper]
    if slope and lower < -intercept / slope < upper:
        boundaries.insert(1, -intercept / slope)
    total = Q(0)
    for a, b in zip(boundaries, boundaries[1:]):
        sign = 1 if intercept + slope * (a + b) / 2 >= 0 else -1
        total += sign * integral(polynomial, a, b)
    return total


def qubit_contrast(distance, radius):
    # Sphere axial coordinate has density 1/2; TV is half the signed
    # density absolute integral. The signed density is 2*D*r*x.
    return absolute_linear_integral(Q(0), 2 * distance * radius,
                                    [Q(1, 2)], Q(-1), Q(1)) / 2


def orthogonal_contrast(n):
    # Haar p1,p2: s=p1+p2, t=(p1-p2)/s. For n>2 the joint
    # density is (n-1)(n-2)(1-s)^(n-3)*s/2 on 0<s<1, -1<t<1.
    # The likelihood difference is n*s*t; integrate |t| independently.
    t_integral = absolute_linear_integral(Q(0), Q(1), [Q(1)], Q(-1), Q(1))
    if n == 2:
        # Degenerate simplex p2=1-p1: p1 is uniform on [0,1].
        return Q(n, 2) * absolute_linear_integral(Q(-1), Q(2), [Q(1)], Q(0), Q(1))
    radial = integral(multiply([Q(0), Q(0), Q(1)], complement_power(n - 3)))
    return Q(n * (n - 1) * (n - 2), 4) * radial * t_integral


def pure_mixed_contrast(n):
    # Marginal p1 density (n-1)*(1-p1)^(n-2), signed density n*p1-1.
    weight = [(n - 1) * c for c in complement_power(n - 2)]
    return absolute_linear_integral(Q(-1), Q(n), weight, Q(0), Q(1)) / 2


def matrix_rank(rows):
    a = [[Q(v) for v in row] for row in rows]
    pivot_row = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(pivot_row, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][column]
        a[pivot_row] = [v / scale for v in a[pivot_row]]
        for i in range(len(a)):
            if i != pivot_row:
                scale = a[i][column]
                a[i] = [x - scale * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def commutant_dimension(matrix):
    n = len(matrix)
    # Vectorize AX-XA as n*n equations on the n*n complex entries of X.
    rows = []
    for i in range(n):
        for j in range(n):
            row = [Q(0)] * (n * n)
            for k in range(n):
                row[k * n + j] += matrix[i][k]
                row[i * n + k] -= matrix[k][j]
            rows.append(row)
    return Q(n * n - matrix_rank(rows))


def reader_tv(left, right, blocks):
    return sum((abs(sum((left[i] - right[i] for i in block), Q(0)))
                for block in blocks), Q(0)) / 2


def controls():
    rho = [[Q(3, 4), Q(0)], [Q(0), Q(1, 4)]]
    dim0, dim1 = commutant_dimension(rho), commutant_dimension(rho)
    left, right = [Q(1, 2), Q(0), Q(1, 2), Q(0)], [Q(0), Q(3, 4), Q(0), Q(1, 4)]
    coarse = [(0, 1), (2, 3)]
    fine = [(i,) for i in range(4)]
    # Equal visible blocks: X,Y independent uniform [-1,1]. Their sum
    # has density (2-|s|)/4; signed density is s, hence TV=E|s|/2.
    product = integral(multiply([Q(0), Q(1)], [Q(1, 2), Q(-1, 4)]), Q(0), Q(2))
    # A resolving block label retains each block's separate |x| integral.
    resolving = sum((Q(1, 2) * qubit_contrast(Q(1), Q(1)) for _ in range(2)), Q(0))
    # For real vectors v, the two helicity probabilities are both
    # (vx^2+vy^2)/2. Equal polynomial coefficients make their difference zero.
    real_difference = [a - b for a, b in zip([Q(1, 2), Q(1, 2)], [Q(1, 2), Q(1, 2)])]
    real = integral(real_difference)
    # Helicity seed: squared overlaps (1+x)^2/4 and (1-x)^2/4.
    # Subtract their coefficient vectors, then apply orbit normalization 3.
    plus, minus = [Q(1, 4), Q(1, 2), Q(1, 4)], [Q(1, 4), Q(-1, 2), Q(1, 4)]
    difference = [a - b for a, b in zip(plus, minus)]
    helicity = Q(3, 2) * absolute_linear_integral(difference[0], difference[1], [Q(1, 2)], Q(-1), Q(1))
    return {
        "identical_centralizer": {"dim0": dim0, "dim1": dim1, "false_contrast": reader_tv(left, left, fine)},
        "reader_retention": {"coarse_before": reader_tv(left, right, coarse), "coarse_after": reader_tv(left, right, coarse), "fine_after": reader_tv(left, right, fine)},
        "block_product": product, "block_resolving": resolving,
        "so3_real": real, "so3_helicity": helicity,
    }


def rational(value):
    if isinstance(value, dict):
        return {key: rational(item) for key, item in value.items()}
    value = Q(value)
    return f"{value.numerator}/{value.denominator}"


def reconstruct():
    records = {}
    for d_name, distance in [("1_2", Q(1, 2)), ("1", Q(1))]:
        for r_name, radius in [("0", Q(0)), ("1_2", Q(1, 2)), ("1", Q(1))]:
            records[f"qubit_D{d_name}_r{r_name}"] = qubit_contrast(distance, radius)
    for n in range(2, 9):
        records[f"orthogonal_n{n}"] = orthogonal_contrast(n)
        records[f"pure_mixed_n{n}"] = pure_mixed_contrast(n)
    records.update(controls())
    return {
        "schema": "uqcf-analytical-repair-v1",
        "source_parent": SOURCE_PARENT,
        "contract_commit": CONTRACT_COMMIT,
        "contract_path": CONTRACT_PATH,
        "domain": {"qubit_D": ["1/2", "1/1"], "qubit_r": ["0/1", "1/2", "1/1"],
                   "n": list(range(2, 9)), "control_ids": list(CONTROL_IDS)},
        "records": [{"id": key, "value": rational(records[key])} for key in sorted(records)],
    }


def exact_equal(actual, expected):
    # Reject bool masquerading as int, integer-valued floats, and subclasses.
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(exact_equal(actual[k], expected[k]) for k in expected)
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(exact_equal(a, b) for a, b in zip(actual, expected))
    return actual == expected


def verify(obj):
    if not exact_equal(obj, reconstruct()):
        raise ValueError("certificate differs from the complete frozen identity/value/provenance/domain universe")
    return True


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        raise SystemExit("usage: independent.py certificate.json output.json")
    try:
        obj = json.loads(Path(argv[0]).read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        verify(obj)
        result, status = {"verified": True, "record_count": len(obj["records"])}, 0
    except (ValueError, OSError) as exc:
        result, status = {"verified": False, "error": str(exc)}, 1
    Path(argv[1]).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
