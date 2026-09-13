#!/usr/bin/env python3
from __future__ import annotations

import itertools
import numpy as np


SEED = 1401
TRIALS = 256
SCALES = [0.2, 0.5, 2.0, 5.0, 11.0]
N = 5
EDGES = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 0), (1, 4)]
CHI = np.array([0.12, -0.33, 0.47, -0.21, 0.61, -0.08, 0.29], dtype=float)


def incidence_matrix(n: int, edges: list[tuple[int, int]]) -> np.ndarray:
    B = np.zeros((n, len(edges)), dtype=float)
    for e, (i, j) in enumerate(edges):
        B[i, e] = -1.0
        B[j, e] = 1.0
    return B


def centered_projector(n: int) -> np.ndarray:
    return np.eye(n) - np.ones((n, n), dtype=float) / n


def cycle_projector(B: np.ndarray) -> np.ndarray:
    e = B.shape[1]
    return np.eye(e) - B.T @ np.linalg.pinv(B @ B.T) @ B


def candidate_operator(Pcyc: np.ndarray, W: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Map arbitrary node source coordinates to balanced cycle-space edge defect."""
    return Pcyc @ W @ B.T @ C


def _relative_error(a: np.ndarray, b: np.ndarray) -> float:
    denom = max(float(np.linalg.norm(b)), 1e-15)
    return float(np.linalg.norm(a - b) / denom)


def _candidate_weights() -> dict[str, np.ndarray]:
    return {
        "linear_positive": np.diag(1.0 + CHI),
        "exponential_positive": np.diag(np.exp(CHI)),
        "quadratic_positive": np.diag(1.0 + CHI**2),
    }


def _signed_permutation(size: int, rng: np.random.Generator) -> np.ndarray:
    Q = np.eye(size)[rng.permutation(size)]
    signs = rng.choice(np.array([-1.0, 1.0]), size=size)
    return np.diag(signs) @ Q


def _edge_defect_to_symmetric(defect: np.ndarray) -> np.ndarray:
    """Fixed injective 7 -> Sym(4) control embedding; not a physical tensor map."""
    d = np.asarray(defect, dtype=float)
    if d.shape != (7,):
        raise ValueError("expected seven edge components")
    X = np.zeros((4, 4), dtype=float)
    diag = d[:4] - np.mean(d[:4])
    X[np.diag_indices(4)] = diag
    for value, (i, j) in zip(d[4:], [(0, 1), (1, 2), (2, 3)]):
        X[i, j] = X[j, i] = value / np.sqrt(2.0)
    return X


def run_audit() -> dict:
    B = incidence_matrix(N, EDGES)
    C = centered_projector(N)
    Pcyc = cycle_projector(B)
    cycle_dimension = len(EDGES) - int(np.linalg.matrix_rank(B))

    incidence_leakage = float(np.linalg.norm(Pcyc @ B.T, ord="fro"))

    weights = _candidate_weights()
    operators = {name: candidate_operator(Pcyc, W, B, C) for name, W in weights.items()}
    operator_norms = {name: float(np.linalg.norm(A, ord="fro")) for name, A in operators.items()}
    minimum_weighted_operator_norm = min(operator_norms.values())

    flattened = np.stack([A.reshape(-1) for A in operators.values()], axis=0)
    candidate_operator_span_rank = int(np.linalg.matrix_rank(flattened, tol=1e-12))

    rng = np.random.default_rng(SEED)
    max_scaling_error = 0.0
    max_covariance_error = 0.0
    max_direction_separation = 0.0
    nonzero_trial_count = 0
    positivity_perturbations: list[np.ndarray] = []

    for _ in range(TRIALS):
        raw = rng.standard_normal(N)
        source = C @ raw
        outputs = {name: A @ source for name, A in operators.items()}

        for name, out in outputs.items():
            if np.linalg.norm(out) > 1e-10:
                nonzero_trial_count += 1
            positivity_perturbations.append(_edge_defect_to_symmetric(out))
            A = operators[name]
            for scale in SCALES:
                scaled = A @ (scale * source)
                max_scaling_error = max(max_scaling_error, _relative_error(scaled, scale * out))

        for a, b in itertools.combinations(outputs.values(), 2):
            na = float(np.linalg.norm(a))
            nb = float(np.linalg.norm(b))
            if na > 1e-10 and nb > 1e-10:
                cosine = abs(float(np.dot(a, b) / (na * nb)))
                cosine = min(1.0, max(0.0, cosine))
                max_direction_separation = max(max_direction_separation, 1.0 - cosine)

        V = np.eye(N)[rng.permutation(N)]
        Eop = _signed_permutation(len(EDGES), rng)
        Bp = V @ B @ Eop.T
        Cp = V @ C @ V.T
        Pp = cycle_projector(Bp)

        for name, W in weights.items():
            Wp = Eop @ W @ Eop.T
            Ap = candidate_operator(Pp, Wp, Bp, Cp)
            target = Eop @ operators[name] @ V.T
            max_covariance_error = max(max_covariance_error, _relative_error(Ap, target))

    # Faithful-interior positivity theorem control. A positive-definite center has an open
    # neighborhood, so finitely many distinct bounded directions all remain feasible for
    # one sufficiently small common epsilon. Positivity therefore cannot select one of them.
    max_delta_opnorm = max(
        float(np.max(np.abs(np.linalg.eigvalsh(D)))) for D in positivity_perturbations
    )
    faithful_epsilon = 0.25 / max(max_delta_opnorm, 1e-15)
    X0 = np.eye(4)
    minimum_faithful_margin = min(
        float(np.min(np.linalg.eigvalsh(X0 + faithful_epsilon * D)))
        for D in positivity_perturbations
    )

    # Boundary loophole audit. At Xb=diag(0,1,1,1) with one-dimensional kernel e0,
    # first-order PSD feasibility requires only e0^T Delta e0 >= 0. In Sym(4), the
    # lineality subspace e0^T Delta e0 = 0 has dimension 10-1=9. Thus the positivity
    # boundary supplies an inequality/normal but does not generate a unique deformation.
    boundary_matrix_dimension = 4
    symmetric_dimension = boundary_matrix_dimension * (boundary_matrix_dimension + 1) // 2
    boundary_lineality_dimension = symmetric_dimension - 1

    # Added-law positive control: once both functional and coefficient are explicitly supplied,
    # the map is unique by construction. This is a sensitivity control, not a derivation.
    selected_name = "exponential_positive"
    selected_scale = 2.7
    eta_star = selected_scale * operators[selected_name]
    reconstructed = selected_scale * candidate_operator(Pcyc, weights[selected_name], B, C)
    positive_control_error = _relative_error(reconstructed, eta_star)

    positivity_does_not_select = (
        faithful_epsilon > 0.0
        and minimum_faithful_margin > 0.0
        and boundary_lineality_dimension > 0
    )

    if (
        incidence_leakage < 1e-12
        and minimum_weighted_operator_norm > 1e-8
        and candidate_operator_span_rank >= 2
        and max_direction_separation > 1e-3
        and max_scaling_error < 2e-12
        and max_covariance_error < 2e-12
        and positivity_does_not_select
    ):
        gate_outcome = "NONUNIQUE"
        branch_status = "STOPPED_PENDING_NEW_SOURCE_TO_HIGHER_INCIDENCE_AXIOM_OR_CALIBRATION"
    elif minimum_weighted_operator_norm <= 1e-8:
        gate_outcome = "NO_NATIVE_DEFORMATION"
        branch_status = "STOPPED_PENDING_NEW_SOURCE_TO_HIGHER_INCIDENCE_AXIOM_OR_CALIBRATION"
    else:
        gate_outcome = "DERIVED"
        branch_status = "OPEN"

    return {
        "version": "v14.01",
        "seed": SEED,
        "trials": TRIALS,
        "scales": SCALES,
        "graph": {
            "n": N,
            "edge_count": len(EDGES),
            "cycle_dimension": cycle_dimension,
            "edges": [list(e) for e in EDGES],
        },
        "state_action_classification": "STATE_ACTION_NOT_LAW_DEFORMATION_UNLESS_SOURCE_ENTERS_CONSTRAINT_MAP",
        "incidence_only_cycle_leakage_norm": incidence_leakage,
        "candidate_operator_norms": operator_norms,
        "minimum_weighted_operator_norm": minimum_weighted_operator_norm,
        "candidate_operator_span_rank": candidate_operator_span_rank,
        "max_relative_source_scaling_error": max_scaling_error,
        "max_covariance_error": max_covariance_error,
        "max_normalized_candidate_direction_separation": max_direction_separation,
        "nonzero_trial_outputs": nonzero_trial_count,
        "candidate_count": len(operators),
        "candidate_functions": {
            "linear_positive": "f(x)=1+x",
            "exponential_positive": "f(x)=exp(x)",
            "quadratic_positive": "f(x)=1+x^2",
        },
        "positivity_audit": {
            "faithful_interior_common_epsilon": float(faithful_epsilon),
            "minimum_faithful_interior_margin": float(minimum_faithful_margin),
            "boundary_matrix_dimension": boundary_matrix_dimension,
            "boundary_tangent_lineality_dimension": boundary_lineality_dimension,
            "boundary_selector_classification": "INEQUALITY_FILTER_NOT_CANONICAL_SOURCE_MAP",
            "interpretation": "faithful positivity admits all bounded candidate directions locally; a simple PSD boundary imposes a half-space condition with a 9-dimensional lineality space, not a unique source deformation",
        },
        "positive_control": {
            "status": "ADDED_LAW_POSITIVE_CONTROL",
            "selected_candidate": selected_name,
            "declared_coefficient": selected_scale,
        },
        "positive_control_reconstruction_error": positive_control_error,
        "incidence_theorem": "P_cyc B^T = 0: an incidence-exact source 1-cochain has zero cycle-space component",
        "weighted_family_interpretation": "state/relational weighting can create nonzero cycle defects, but covariance and source linearity permit multiple inequivalent weighting functionals",
        "gate_outcome": gate_outcome,
        "branch_status": branch_status,
        "claim_scope": "current frozen architecture plus the audited incidence/state-weighted and PSD-positivity construction class; not all conceivable deeper nonlinear laws",
        "Pillar_3": "OPEN",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
