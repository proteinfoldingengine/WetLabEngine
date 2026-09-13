#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np


SEED = 1402
PRIMARY_SAMPLES = 64
HERMITICITY_TOL = 1e-11
HIDDEN_NULL_TOL = 1e-10
PSD_REL_TOL = 1e-10
NULL_REL_TOL = 1e-9
NORMAL_RANK_REL_TOL = 1e-10
CERT_REL_TOL = 2e-9


def load_archived_lab() -> ModuleType:
    repo_root = Path(__file__).resolve().parents[4]
    path = repo_root / "Tmp" / "TOE" / "UQCF_Quantum_Compatibility_Lab" / "uqcf_quantum_lab.py"
    if not path.exists():
        raise FileNotFoundError(f"Archived compatibility lab not found: {path}")
    spec = importlib.util.spec_from_file_location("uqcf_quantum_compatibility_lab_v1402", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load archived compatibility lab: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _herm(a: np.ndarray) -> np.ndarray:
    return (a + a.conj().T) / 2


def _scaled_error(a: float, b: float) -> float:
    return float(abs(a - b) / max(1.0, abs(a), abs(b)))


def _matrix_rel_error(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(1.0, float(np.linalg.norm(a)), float(np.linalg.norm(b))))


def build_primary_configuration(lab: ModuleType, name: str) -> dict[str, Any]:
    if name not in {"V_A", "V_B"}:
        raise ValueError(name)
    V = getattr(lab, name)
    state = lab.build_completion(V, lab.FIXED_T)
    modes, hidden_report = lab.hidden_basis(state["L"])
    modes = np.asarray(modes, dtype=complex)
    X0 = np.asarray(state["X0"], dtype=complex)

    herm_residual = float(np.max([np.linalg.norm(q - q.conj().T) for q in modes]))
    hidden_residual = float(hidden_report["maximum_marginal_null_residual"])
    center_eigs = np.linalg.eigvalsh(_herm(X0))
    min_center_eig = float(center_eigs[0])
    if herm_residual >= HERMITICITY_TOL:
        raise ArithmeticError(f"{name} hidden basis Hermiticity residual {herm_residual}")
    if hidden_residual >= HIDDEN_NULL_TOL:
        raise ArithmeticError(f"{name} hidden marginal residual {hidden_residual}")
    if min_center_eig <= 0:
        raise ArithmeticError(f"{name} center is not faithful: {min_center_eig}")

    return {
        "name": name,
        "state": state,
        "X0": X0,
        "modes": modes,
        "hidden_report": hidden_report,
        "hidden_dimension": int(modes.shape[0]),
        "support_dimension": int(X0.shape[0]),
        "hermiticity_residual": herm_residual,
        "hidden_marginal_residual": hidden_residual,
        "minimum_center_eigenvalue": min_center_eig,
    }


def normalized_hidden_directions(dim: int, count: int, rng: np.random.Generator) -> np.ndarray:
    x = rng.standard_normal((count, dim))
    norms = np.linalg.norm(x, axis=1)
    if np.any(norms == 0):
        raise ArithmeticError("zero random hidden direction")
    x = x / norms[:, None]
    return x


def _direction_hash(directions: np.ndarray) -> str:
    return hashlib.sha256(np.asarray(directions, dtype=np.float64).tobytes()).hexdigest()


def radial_boundary(X0: np.ndarray, modes: np.ndarray, u: np.ndarray) -> dict[str, Any]:
    u = np.asarray(u, dtype=float)
    u = u / np.linalg.norm(u)
    D = np.einsum("a,aij->ij", u, modes, optimize=True)
    D = _herm(D)
    diag = np.real(np.diag(X0))
    if np.any(diag <= 0):
        raise ArithmeticError("X0 must be positive diagonal")
    inv_sqrt = np.diag(1.0 / np.sqrt(diag))
    G = _herm(inv_sqrt @ D @ inv_sqrt)
    geigs = np.linalg.eigvalsh(G)
    if geigs[0] >= -1e-12:
        raise ArithmeticError(f"hidden direction lacks negative generalized eigenvalue: {geigs[0]}")
    radius = float(-1.0 / geigs[0])
    Xstar = _herm(X0 + radius * D)
    evals, evecs = np.linalg.eigh(Xstar)
    norm2 = float(np.max(np.abs(evals)))
    scale = max(1.0, norm2)
    tau_null = NULL_REL_TOL * scale
    null_mask = np.abs(evals) <= tau_null
    nullity = int(np.sum(null_mask))
    second = float(evals[1]) if len(evals) > 1 else float("inf")
    simple = bool(nullity == 1 and second >= 100.0 * tau_null)
    psd_residual = float(abs(evals[0]))
    psd_violation = float(max(0.0, -evals[0]))
    allowed_psd = PSD_REL_TOL * scale
    sensitivity_nullities = {
        "half_tau": int(np.sum(np.abs(evals) <= 0.5 * tau_null)),
        "tau": nullity,
        "double_tau": int(np.sum(np.abs(evals) <= 2.0 * tau_null)),
    }
    stable_nullity = len(set(sensitivity_nullities.values())) == 1
    return {
        "u": u,
        "D": D,
        "radius": radius,
        "xstar": radius * u,
        "Xstar": Xstar,
        "evals": evals,
        "evecs": evecs,
        "norm2": norm2,
        "tau_null": float(tau_null),
        "nullity": nullity,
        "simple": simple,
        "near_degenerate": not simple,
        "stable_nullity": stable_nullity,
        "sensitivity_nullities": sensitivity_nullities,
        "min_eigenvalue": float(evals[0]),
        "second_smallest_eigenvalue": second,
        "psd_residual": psd_residual,
        "psd_violation": psd_violation,
        "allowed_psd_residual": float(allowed_psd),
        "hermiticity_residual": float(np.linalg.norm(Xstar - Xstar.conj().T)),
        "direction_trace_abs": float(abs(np.trace(D))),
    }


def kernel_hermitian_basis(r: int) -> np.ndarray:
    basis: list[np.ndarray] = []
    for i in range(r):
        z = np.zeros((r, r), dtype=complex)
        z[i, i] = 1.0
        basis.append(z)
    for i in range(r):
        for j in range(i + 1, r):
            z = np.zeros((r, r), dtype=complex)
            z[i, j] = z[j, i] = 1.0 / np.sqrt(2.0)
            basis.append(z)
            z = np.zeros((r, r), dtype=complex)
            z[i, j] = -1j / np.sqrt(2.0)
            z[j, i] = 1j / np.sqrt(2.0)
            basis.append(z)
    return np.asarray(basis)


def project_hidden_covector(modes: np.ndarray, Y: np.ndarray) -> np.ndarray:
    # Real Hilbert-Schmidt coordinates: Re Tr(Q_a^dagger Y).  Q_a are Hermitian.
    return np.real(np.einsum("aij,ij->a", modes.conj(), Y, optimize=True))


def _normal_rank(rows: np.ndarray) -> tuple[int, list[float]]:
    if rows.size == 0:
        return 0, []
    s = np.linalg.svd(rows, compute_uv=False)
    if len(s) == 0 or s[0] <= 1e-14:
        return 0, [float(v) for v in s]
    rank = int(np.sum(s > NORMAL_RANK_REL_TOL * s[0]))
    return rank, [float(v) for v in s]


def _rank_one_kernel_vectors(r: int) -> list[np.ndarray]:
    vecs: list[np.ndarray] = []
    eye = np.eye(r, dtype=complex)
    for i in range(r):
        vecs.append(eye[:, i])
    for i in range(r):
        for j in range(i + 1, r):
            vecs.append((eye[:, i] + eye[:, j]) / np.sqrt(2.0))
            vecs.append((eye[:, i] + 1j * eye[:, j]) / np.sqrt(2.0))
    return vecs


def normal_cone_audit(boundary: dict[str, Any], modes: np.ndarray) -> dict[str, Any]:
    evals = boundary["evals"]
    evecs = boundary["evecs"]
    tau = boundary["tau_null"]
    null_mask = np.abs(evals) <= tau
    V0 = evecs[:, null_mask]
    r = V0.shape[1]
    if r == 0:
        return {
            "classification": "ZERO_OR_UNRESOLVED",
            "span_rank": 0,
            "representative_Y": None,
            "representative_g": None,
            "ray_consistent": False,
            "normal_norm": 0.0,
            "singular_values": [],
        }

    hb = kernel_hermitian_basis(r)
    projected = []
    for Z in hb:
        Y = _herm(V0 @ Z @ V0.conj().T)
        projected.append(project_hidden_covector(modes, Y))
    projected_arr = np.asarray(projected)
    span_rank, singular_values = _normal_rank(projected_arr)

    representative_Y = None
    representative_g = None
    ray_consistent = False
    positive_ray_min_dot = None

    if r == 1:
        v = V0[:, 0]
        representative_Y = np.outer(v, v.conj())
        representative_g = project_hidden_covector(modes, representative_Y)
        ray_consistent = bool(np.linalg.norm(representative_g) > 1e-12)
    elif span_rank == 1:
        normals = []
        Ys = []
        for z in _rank_one_kernel_vectors(r):
            w = V0 @ z
            Y = np.outer(w, w.conj())
            g = project_hidden_covector(modes, Y)
            ng = float(np.linalg.norm(g))
            if ng > 1e-12:
                normals.append(g / ng)
                Ys.append(Y)
        if normals:
            dots = []
            for i in range(len(normals)):
                for j in range(i + 1, len(normals)):
                    dots.append(float(np.dot(normals[i], normals[j])))
            positive_ray_min_dot = min(dots) if dots else 1.0
            ray_consistent = positive_ray_min_dot > 1.0 - CERT_REL_TOL
            representative_Y = Ys[0]
            representative_g = project_hidden_covector(modes, representative_Y)

    if span_rank > 1:
        classification = "NONUNIQUE_NORMAL_CONE"
    elif span_rank == 0:
        classification = "NO_BOUNDARY_SELECTOR"
    elif ray_consistent:
        classification = "RAY"
    else:
        classification = "NONUNIQUE_NORMAL_CONE"

    normal_norm = 0.0 if representative_g is None else float(np.linalg.norm(representative_g))
    return {
        "classification": classification,
        "span_rank": span_rank,
        "kernel_dimension": int(r),
        "representative_Y": representative_Y,
        "representative_g": representative_g,
        "ray_consistent": bool(ray_consistent),
        "positive_ray_min_dot": positive_ray_min_dot,
        "normal_norm": normal_norm,
        "singular_values": singular_values,
    }


def _coordinates_to_matrix(X0: np.ndarray, modes: np.ndarray, x: np.ndarray) -> np.ndarray:
    return _herm(X0 + np.einsum("a,aij->ij", x, modes, optimize=True))


def support_identity_audit(
    X0: np.ndarray,
    modes: np.ndarray,
    boundary: dict[str, Any],
    Y: np.ndarray,
    g: np.ndarray,
    rng: np.random.Generator,
) -> dict[str, float]:
    xstar = boundary["xstar"]
    points = [np.zeros_like(xstar)]
    points.extend([t * xstar for t in (0.2, 0.5, 0.8)])
    for _ in range(4):
        w = rng.standard_normal(len(xstar))
        w /= np.linalg.norm(w)
        other = radial_boundary(X0, modes, w)
        points.append(0.5 * other["xstar"])

    max_error = 0.0
    min_support = float("inf")
    max_feasibility_violation = 0.0
    for x in points:
        X = _coordinates_to_matrix(X0, modes, x)
        lhs = float(np.dot(g, x - xstar))
        rhs = float(np.real(np.trace(Y @ X)))
        max_error = max(max_error, _scaled_error(lhs, rhs))
        min_support = min(min_support, lhs)
        max_feasibility_violation = max(max_feasibility_violation, max(0.0, -float(np.linalg.eigvalsh(X)[0])))
    return {
        "max_relative_error": float(max_error),
        "minimum_support_value": float(min_support),
        "max_feasibility_violation": float(max_feasibility_violation),
    }


def basis_invariance_audit(modes: np.ndarray, g: np.ndarray, rng: np.random.Generator, rotations: int = 8) -> float:
    d = len(g)
    if d < 2:
        return 0.0
    NH = np.einsum("a,aij->ij", g, modes, optimize=True)
    max_error = 0.0
    for _ in range(rotations):
        p, q = rng.choice(d, size=2, replace=False)
        theta = float(rng.uniform(-1.2, 1.2))
        c, s = np.cos(theta), np.sin(theta)
        modes_rot = modes.copy()
        gp = g[p]
        gq = g[q]
        Qp = modes[p].copy()
        Qq = modes[q].copy()
        modes_rot[p] = c * Qp + s * Qq
        modes_rot[q] = -s * Qp + c * Qq
        g_rot = g.copy()
        g_rot[p] = c * gp + s * gq
        g_rot[q] = -s * gp + c * gq
        NH_rot = np.einsum("a,aij->ij", g_rot, modes_rot, optimize=True)
        max_error = max(max_error, _matrix_rel_error(NH, NH_rot))
    return float(max_error)


def orthogonal_objective_control(
    X0: np.ndarray,
    modes: np.ndarray,
    boundary: dict[str, Any],
    g: np.ndarray,
    rng: np.random.Generator,
) -> dict[str, float | bool]:
    ng = float(np.linalg.norm(g))
    if ng <= 1e-12:
        return {"found_non_supporting_direction": False, "minimum_test_value": 0.0}
    ghat = g / ng
    xstar = boundary["xstar"]
    candidates = [0.99 * xstar, np.zeros_like(xstar)]
    for _ in range(4):
        w = rng.standard_normal(len(xstar))
        w /= np.linalg.norm(w)
        other = radial_boundary(X0, modes, w)
        candidates.append(0.5 * other["xstar"])

    for _ in range(32):
        h = rng.standard_normal(len(g))
        h = h - np.dot(h, ghat) * ghat
        nh = float(np.linalg.norm(h))
        if nh <= 1e-12:
            continue
        h /= nh
        vals = [float(np.dot(h, x - xstar)) for x in candidates]
        if min(vals) < -1e-8:
            return {"found_non_supporting_direction": True, "minimum_test_value": float(min(vals))}
        vals_flip = [-v for v in vals]
        if min(vals_flip) < -1e-8:
            return {"found_non_supporting_direction": True, "minimum_test_value": float(min(vals_flip))}
    return {"found_non_supporting_direction": False, "minimum_test_value": 0.0}


def synthetic_degenerate_control() -> dict[str, Any]:
    # Test fixture only: X(x1,x2)=diag(x1,x2,1) at x=(0,0).
    rows = np.array([[1.0, 0.0], [0.0, 1.0]])
    rank = int(np.linalg.matrix_rank(rows))
    return {
        "fixture": "diag(x1,x2,1)_at_origin",
        "kernel_dimension": 2,
        "projected_normal_span_rank": rank,
        "classification": "NONUNIQUE_NORMAL_CONE" if rank > 1 else "UNEXPECTED",
        "scientific_evidence": False,
    }


def _sample_record(boundary: dict[str, Any], normal: dict[str, Any], support_error: float | None) -> dict[str, Any]:
    return {
        "radius": float(boundary["radius"]),
        "min_eigenvalue": float(boundary["min_eigenvalue"]),
        "second_smallest_eigenvalue": float(boundary["second_smallest_eigenvalue"]),
        "tau_null": float(boundary["tau_null"]),
        "nullity": int(boundary["nullity"]),
        "simple": bool(boundary["simple"]),
        "stable_nullity": bool(boundary["stable_nullity"]),
        "normal_span_rank": int(normal["span_rank"]),
        "normal_classification": normal["classification"],
        "normal_norm": float(normal["normal_norm"]),
        "psd_residual": float(boundary["psd_residual"]),
        "support_identity_relative_error": None if support_error is None else float(support_error),
    }


def run_audit() -> dict[str, Any]:
    lab = load_archived_lab()
    configs = {name: build_primary_configuration(lab, name) for name in ("V_A", "V_B")}
    rng = np.random.default_rng(SEED)

    directions = {}
    for name in ("V_A", "V_B"):
        directions[name] = normalized_hidden_directions(configs[name]["hidden_dimension"], PRIMARY_SAMPLES, rng)

    global_simple = 0
    global_near = 0
    global_zero = 0
    global_nonunique = 0
    global_unresolved = 0
    rank_hist: dict[str, int] = {}
    max_psd_residual = 0.0
    max_support_error = 0.0
    max_basis_error = 0.0
    min_simple_gap = float("inf")
    max_hidden_herm = 0.0
    max_hidden_null = 0.0
    min_center_eig = float("inf")
    objective_controls = []
    survey: dict[str, Any] = {}

    for name in ("V_A", "V_B"):
        cfg = configs[name]
        X0 = cfg["X0"]
        modes = cfg["modes"]
        max_hidden_herm = max(max_hidden_herm, cfg["hermiticity_residual"])
        max_hidden_null = max(max_hidden_null, cfg["hidden_marginal_residual"])
        min_center_eig = min(min_center_eig, cfg["minimum_center_eigenvalue"])
        records = []
        simple_count = 0
        near_count = 0
        zero_count = 0
        nonunique_count = 0
        unresolved_count = 0
        first_basis_done = False
        local_rank_hist: dict[str, int] = {}

        for u in directions[name]:
            boundary = radial_boundary(X0, modes, u)
            max_psd_residual = max(max_psd_residual, boundary["psd_residual"])
            if boundary["simple"]:
                simple_count += 1
                global_simple += 1
                min_simple_gap = min(min_simple_gap, boundary["second_smallest_eigenvalue"])
            else:
                near_count += 1
                global_near += 1

            normal = normal_cone_audit(boundary, modes)
            rank_key = str(normal["span_rank"])
            local_rank_hist[rank_key] = local_rank_hist.get(rank_key, 0) + 1
            rank_hist[rank_key] = rank_hist.get(rank_key, 0) + 1

            numerical_ok = (
                boundary["psd_residual"] <= boundary["allowed_psd_residual"]
                and boundary["hermiticity_residual"] < HERMITICITY_TOL
            )
            if not boundary["simple"] and not boundary["stable_nullity"]:
                numerical_ok = False

            if not numerical_ok or boundary["nullity"] == 0:
                unresolved_count += 1
                global_unresolved += 1

            if normal["classification"] == "NONUNIQUE_NORMAL_CONE":
                nonunique_count += 1
                global_nonunique += 1
            if normal["classification"] in {"NO_BOUNDARY_SELECTOR", "ZERO_OR_UNRESOLVED"}:
                zero_count += 1
                global_zero += 1

            support_error = None
            if normal["representative_g"] is not None and normal["representative_Y"] is not None:
                support = support_identity_audit(
                    X0, modes, boundary, normal["representative_Y"], normal["representative_g"], rng
                )
                support_error = support["max_relative_error"]
                max_support_error = max(max_support_error, support["max_relative_error"])
                if support["minimum_support_value"] < -CERT_REL_TOL:
                    unresolved_count += 1
                    global_unresolved += 1
                control = orthogonal_objective_control(X0, modes, boundary, normal["representative_g"], rng)
                objective_controls.append(control)
                if not first_basis_done:
                    max_basis_error = max(
                        max_basis_error,
                        basis_invariance_audit(modes, normal["representative_g"], rng, rotations=8),
                    )
                    first_basis_done = True

            records.append(_sample_record(boundary, normal, support_error))

        survey[name] = {
            "sample_count": PRIMARY_SAMPLES,
            "hidden_dimension": cfg["hidden_dimension"],
            "support_dimension": cfg["support_dimension"],
            "direction_sha256": _direction_hash(directions[name]),
            "simple_boundary_count": simple_count,
            "near_degenerate_boundary_count": near_count,
            "zero_projected_normal_count": zero_count,
            "nonunique_normal_count": nonunique_count,
            "unresolved_numerical_count": unresolved_count,
            "normal_cone_rank_histogram": local_rank_hist,
            "minimum_center_eigenvalue": cfg["minimum_center_eigenvalue"],
            "hidden_marginal_residual": cfg["hidden_marginal_residual"],
            "sample_records": records,
        }

    if global_unresolved > 0:
        gate_outcome = "UNRESOLVED_NUMERICAL_BOUNDARY"
    elif global_nonunique > 0:
        gate_outcome = "NONUNIQUE_NORMAL_CONE"
    elif global_zero == 0 and global_simple + global_near == 2 * PRIMARY_SAMPLES:
        gate_outcome = "CANONICAL_DUAL_RAY"
    else:
        gate_outcome = "NO_BOUNDARY_SELECTOR"

    if gate_outcome == "CANONICAL_DUAL_RAY":
        source_lift_status = "CANONICAL_DUAL_DIRECTION_BUT_SOURCE_LIFT_UNDERIVED"
    else:
        source_lift_status = "SOURCE_TO_HIDDEN_COMPLETION_LIFT_UNDERIVED"

    objective_success_count = int(sum(bool(c["found_non_supporting_direction"]) for c in objective_controls))
    interior_control = {
        "classification": "NO_BOUNDARY_SELECTOR",
        "minimum_center_eigenvalue": float(min_center_eig),
        "relative_normal_cone_rank": 0,
        "reason": "faithful centers are interior points of the hidden spectrahedra",
    }

    return {
        "version": "v14.02",
        "seed": SEED,
        "construction": {
            "archived_lab_path": "Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py",
            "fixed_t": float(lab.FIXED_T),
            "uses_full_hidden_kernel": True,
            "uses_visualization_section": False,
            "max_hidden_basis_hermiticity_residual": float(max_hidden_herm),
            "max_hidden_marginal_null_residual": float(max_hidden_null),
        },
        "survey": survey,
        "primary_sample_count": 2 * PRIMARY_SAMPLES,
        "simple_boundary_count": global_simple,
        "near_degenerate_boundary_count": global_near,
        "zero_projected_normal_count": global_zero,
        "nonunique_normal_count": global_nonunique,
        "unresolved_numerical_count": global_unresolved,
        "normal_cone_rank_histogram": rank_hist,
        "minimum_simple_boundary_spectral_gap": None if not np.isfinite(min_simple_gap) else float(min_simple_gap),
        "max_boundary_psd_residual": float(max_psd_residual),
        "max_support_identity_relative_error": float(max_support_error),
        "max_basis_invariance_relative_error": float(max_basis_error),
        "objective_independence_control": {
            "tested_boundary_count": len(objective_controls),
            "non_supporting_orthogonal_objective_count": objective_success_count,
            "all_tested_orthogonal_objectives_rejected": bool(
                len(objective_controls) > 0 and objective_success_count == len(objective_controls)
            ),
        },
        "typed_dual_control": "VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE",
        "interior_control": interior_control,
        "synthetic_degenerate_control": synthetic_degenerate_control(),
        "source_lift_status": source_lift_status,
        "gate_outcome": gate_outcome,
        "claim_scope": "objective-free local dual geometry of the two frozen archived compatibility spectrahedra only",
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
