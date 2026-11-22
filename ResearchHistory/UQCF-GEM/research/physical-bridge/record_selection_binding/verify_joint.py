"""Verify the unique two-outcome instrument on every matrix unit and controls."""
from fractions import Fraction as F
import json

import numpy as np


TOL = 1e-14
Q = np.diag([1., 1., 0., 1.]).astype(complex)
U = np.diag([0., 0., 1., 0.]).astype(complex)
P = np.diag([0., 1., 0., 0.]).astype(complex)
K = np.zeros((4, 4), dtype=complex)
K[1, 2] = 1
WRONG = np.zeros((4, 4), dtype=complex)
WRONG[3, 2] = 1


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def branch_q(a):
    return Q @ a @ Q


def branch_u(a):
    return K @ a @ K.conj().T


def benchmark(a):
    return Q @ a @ Q + a[2, 2] * P


def matrix_units():
    for i in range(4):
        for j in range(4):
            e = np.zeros((4, 4), dtype=complex)
            e[i, j] = 1
            yield i, j, e


def max_unit_error(map_a, map_b):
    return max(float(np.max(np.abs(map_a(e) - map_b(e)))) for _, _, e in matrix_units())


def exact_case(z):
    q = F(1) - z[2]
    conditional = [value / q if i != 2 else F(0) for i, value in enumerate(z)]
    pushed = list(z)
    pushed[1] += pushed[2]
    pushed[2] = F(0)
    return q, conditional, pushed


def run():
    completeness_error = float(np.max(np.abs(Q.conj().T @ Q + K.conj().T @ K - np.eye(4))))
    all_input_error = max_unit_error(lambda a: branch_q(a) + branch_u(a), benchmark)
    uniqueness_error = max_unit_error(lambda a: benchmark(a) - branch_q(a), branch_u)
    require(max(completeness_error, all_input_error, uniqueness_error) <= TOL,
            "Instrument identity or uniqueness failed")

    cases = {
        "canonical_plus": [F(1, 5), F(1, 5), F(2, 5), F(1, 5)],
        "canonical_minus": [F(1, 5), F(1, 5), F(1, 5), F(2, 5)],
    }
    rows = {}
    for name, z in cases.items():
        rho = np.diag([float(v) for v in z]).astype(complex)
        q, conditional, pushed = exact_case(z)
        mq, mu, total = branch_q(rho), branch_u(rho), benchmark(rho)
        require(abs(float(np.trace(mq).real) - float(q)) <= TOL, "Q probability mismatch")
        require(abs(float(np.trace(mu).real) - float(z[2])) <= TOL, "u probability mismatch")
        require(np.max(np.abs(mq / float(q) - np.diag(list(map(float, conditional))))) <= TOL,
                "conditional state mismatch")
        require(np.max(np.abs(total - np.diag(list(map(float, pushed))))) <= TOL,
                "P1 total mismatch")
        rows[name] = {
            "q_probability": str(q),
            "u_probability": str(z[2]),
            "q_conditional_diagonal": list(map(str, conditional)),
            "u_conditional_diagonal": ["0", "1", "0", "0"],
            "total_diagonal": list(map(str, pushed)),
        }

    old_branch_error = max_unit_error(lambda a: U @ a @ U, branch_u)
    wrong_reset_error = max_unit_error(lambda a: WRONG @ a @ WRONG.conj().T, branch_u)
    omitted_branch_completeness_error = float(np.max(np.abs(Q.conj().T @ Q - np.eye(4))))
    require(old_branch_error == 1.0, "Original pinching branch unexpectedly equals the reset")
    require(wrong_reset_error == 1.0, "Wrong reset did not reject")
    require(omitted_branch_completeness_error == 1.0, "Missing branch did not reject")

    return {
        "status": "PASS",
        "numpy": np.__version__,
        "basis": ["o", "p", "u", "v"],
        "contract": "two outcomes; fixed Q probability and conditional state; total channel C on all inputs",
        "matrix_units_checked": 16,
        "maximum_errors": {
            "kraus_completeness": completeness_error,
            "instrument_sum_vs_benchmark": all_input_error,
            "forced_complement_vs_reset_branch": uniqueness_error,
        },
        "cases": rows,
        "rejecting_controls": {
            "old_u_to_u_branch_error": old_branch_error,
            "wrong_u_to_v_reset_error": wrong_reset_error,
            "omitted_branch_completeness_error": omitted_branch_completeness_error,
        },
        "native_event_binding": "NOT_DERIVED",
        "receiver_access": "NOT_DERIVED",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
