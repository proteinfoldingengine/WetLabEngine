#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

import numpy as np

VERSION = "v15.02"
N = 5
PARENT_DIM = 125
SUPPORT_DIM = 25
PERM_TOL = 2e-12
GAUGE_TOL = 2e-9
PROJECTIVE_TOL = 2e-9


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _herm(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=complex)
    return (a + a.conj().T) / 2


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_json(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _load_module(path: Path, name: str) -> ModuleType:
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_v1501() -> ModuleType:
    return _load_module(
        _repo_root() / "ResearchHistory" / "UQCF-GEM" / "v15" / "v15.01" / "common_parent_audit.py",
        "uqcf_v1501_common_parent",
    )


def load_v1403() -> ModuleType:
    return _load_module(
        _repo_root() / "ResearchHistory" / "UQCF-GEM" / "v14" / "v14.03" / "source_ray_audit.py",
        "uqcf_v1403_source_ray_for_v1502",
    )


def all_permutations() -> tuple[tuple[int, ...], ...]:
    out = tuple(itertools.permutations(range(N)))
    if len(out) != 120 or len(set(out)) != 120:
        raise ArithmeticError("S5 enumeration failed")
    return out


def compose_perm(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Composition p o q, with tuples mapping old labels to new labels."""
    return tuple(p[q[i]] for i in range(N))


def inverse_perm(p: tuple[int, ...]) -> tuple[int, ...]:
    inv = [0] * N
    for i, j in enumerate(p):
        inv[j] = i
    return tuple(inv)


def permutation_matrix(p: tuple[int, ...]) -> np.ndarray:
    U = np.zeros((N, N), dtype=complex)
    for old, new in enumerate(p):
        U[new, old] = 1.0
    return U


def permute_vector(v: np.ndarray, p: tuple[int, ...]) -> np.ndarray:
    v = np.asarray(v)
    out = np.empty_like(v)
    for old, new in enumerate(p):
        out[new] = v[old]
    return out


def parent_index_perm(p: tuple[int, ...]) -> np.ndarray:
    q = np.empty(PARENT_DIM, dtype=int)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                old = (a * N + b) * N + c
                new = (p[a] * N + p[b]) * N + p[c]
                q[old] = new
    return q


def permute_parent_matrix(M: np.ndarray, p: tuple[int, ...]) -> np.ndarray:
    q = parent_index_perm(p)
    out = np.empty_like(M)
    out[np.ix_(q, q)] = M
    return out


def _numeric_literal(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        x = _numeric_literal(node.operand)
        return -x if isinstance(node.op, ast.USub) else x
    raise ValueError(f"not a numeric literal: {ast.dump(node)}")


def parse_source_fixture() -> dict[str, Any]:
    path = _repo_root() / "Tmp" / "TOE" / "ThePhysicsParadox" / "Physics101" / "phi lab.py"
    text = path.read_text()
    tree = ast.parse(text)
    nodes = None
    edges = None
    source_updates: dict[int, float] = {}
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name) and target.id == "NODES":
                    nodes = tuple(int(x) for x in ast.literal_eval(stmt.value))
                elif isinstance(target, ast.Name) and target.id == "EDGES":
                    edges = tuple(tuple(int(y) for y in x) for x in ast.literal_eval(stmt.value))
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id == "SOURCE":
                    idx_node = target.slice
                    if isinstance(idx_node, ast.Constant):
                        idx = int(idx_node.value)
                    else:
                        idx = int(ast.literal_eval(idx_node))
                    source_updates[idx] = _numeric_literal(stmt.value)
    if nodes is None or edges is None:
        raise ArithmeticError("source fixture literals not found")
    source = np.zeros(len(nodes), dtype=float)
    for i, value in source_updates.items():
        source[i] = value
    expected_nodes = (0, 1, 2, 3, 4)
    expected_edges = ((0, 1), (1, 3), (0, 2), (2, 4), (4, 3), (1, 2), (0, 4))
    expected_source = (-1.0, 0.0, 0.0, 1.0, 0.0)
    if nodes != expected_nodes or edges != expected_edges or tuple(source) != expected_source:
        raise ArithmeticError((nodes, edges, tuple(source)))
    canonical = {"nodes": nodes, "edges": edges, "source": tuple(float(x) for x in source)}
    return {
        **canonical,
        "path": str(path.relative_to(_repo_root())),
        "sha256": _sha256_path(path),
        "fixture_sha256": _sha256_json(canonical),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "source_sum_abs": float(abs(source.sum())),
    }


def incidence_matrix(nodes: Iterable[int], edges: Iterable[tuple[int, int]]) -> np.ndarray:
    nodes = tuple(nodes)
    edges = tuple(edges)
    idx = {n: i for i, n in enumerate(nodes)}
    B = np.zeros((len(nodes), len(edges)), dtype=float)
    for e, (u, v) in enumerate(edges):
        B[idx[u], e] = -1.0
        B[idx[v], e] = 1.0
    return B


def source_side_audit(fixture: dict[str, Any], perms: tuple[tuple[int, ...], ...]) -> dict[str, Any]:
    edges = set(tuple(x) for x in fixture["edges"])
    source = np.asarray(fixture["source"], dtype=float)
    graph_group = []
    state_group = []
    for p in perms:
        moved_edges = {(p[u], p[v]) for u, v in edges}
        if moved_edges == edges:
            graph_group.append(p)
            if np.array_equal(permute_vector(source, p), source):
                state_group.append(p)
    B = incidence_matrix(fixture["nodes"], fixture["edges"])
    rank = int(np.linalg.matrix_rank(B, tol=1e-10))
    cycle_dim = int(B.shape[1] - rank)
    return {
        "incidence_rank": rank,
        "cycle_dimension": cycle_dim,
        "graph_automorphism_order": len(graph_group),
        "source_stabilizer_order": len(state_group),
        "graph_automorphisms": [list(p) for p in graph_group],
        "source_stabilizers": [list(p) for p in state_group],
        "graph_group_sha256": _sha256_json(graph_group),
        "source_stabilizer_sha256": _sha256_json(state_group),
    }


def build_configs(v1501: ModuleType) -> tuple[ModuleType, dict[str, dict[str, Any]]]:
    v1403 = v1501.load_v1403()
    configs = {name: v1501.build_parent_configuration(v1403, name) for name in ("V_A", "V_B")}
    return v1403, configs


def transform_arrangement(V: np.ndarray, p: tuple[int, ...]) -> np.ndarray:
    out = np.empty_like(V)
    for i in range(N):
        for j in range(N):
            out[p[i], p[j]] = V[i, j]
    return out


def compatibility_side_audit(cfg: dict[str, Any], perms: tuple[tuple[int, ...], ...]) -> dict[str, Any]:
    V = np.asarray(cfg["state"]["V"], dtype=int)
    Pi = _herm(cfg["Pi"])
    T = _herm(cfg["T"])
    arrangement_group = []
    fixed_group = []
    max_projector_error = 0.0
    max_state_error = 0.0
    records = []
    for p in perms:
        arrangement_invariant = bool(np.array_equal(transform_arrangement(V, p), V))
        if arrangement_invariant:
            arrangement_group.append(p)
            Pi2 = permute_parent_matrix(Pi, p)
            T2 = permute_parent_matrix(T, p)
            perr = float(np.linalg.norm(Pi2 - Pi))
            terr = float(np.linalg.norm(T2 - T))
            if perr < GAUGE_TOL and terr < GAUGE_TOL:
                fixed_group.append(p)
                max_projector_error = max(max_projector_error, perr)
                max_state_error = max(max_state_error, terr)
            records.append({
                "permutation": list(p),
                "projector_error": perr,
                "state_error": terr,
                "fixed_gauge": bool(perr < GAUGE_TOL and terr < GAUGE_TOL),
            })
    return {
        "parent_dimension": PARENT_DIM,
        "support_dimension": SUPPORT_DIM,
        "arrangement_group_order": len(arrangement_group),
        "fixed_gauge_group_order": len(fixed_group),
        "arrangement_group": [list(p) for p in arrangement_group],
        "fixed_gauge_group": [list(p) for p in fixed_group],
        "arrangement_group_sha256": _sha256_json(arrangement_group),
        "fixed_gauge_group_sha256": _sha256_json(fixed_group),
        "max_projector_covariance_error": float(max_projector_error),
        "max_state_covariance_error": float(max_state_error),
        "records": records,
    }


def group_intersection(*groups: list[list[int]]) -> list[tuple[int, ...]]:
    sets = [set(tuple(x) for x in g) for g in groups]
    if not sets:
        return []
    return sorted(set.intersection(*sets))


def double_cosets(
    G_comp: list[tuple[int, ...]], G_src: list[tuple[int, ...]], perms: tuple[tuple[int, ...], ...]
) -> list[dict[str, Any]]:
    unseen = set(perms)
    classes = []
    while unseen:
        rep = min(unseen)
        orbit = {
            compose_perm(gc, compose_perm(rep, inverse_perm(gs)))
            for gc in G_comp for gs in G_src
        }
        if not orbit:
            orbit = {rep}
        classes.append({"representative": list(rep), "size": len(orbit)})
        unseen -= orbit
    if sum(x["size"] for x in classes) != len(perms):
        raise ArithmeticError("double-coset partition does not cover S5")
    return classes


def centered_source_operator(s: np.ndarray) -> np.ndarray:
    s = np.asarray(s, dtype=float)
    if s.shape != (N,):
        raise ValueError(s.shape)
    return np.diag(s) - float(np.mean(s)) * np.eye(N)


def projective_affine_residual(P: np.ndarray, Q: np.ndarray) -> float:
    P = _herm(P)
    Q = _herm(Q)
    k = P.shape[0]
    I = np.eye(k, dtype=complex)
    Pc = P - np.trace(P).real * I / k
    Qc = Q - np.trace(Q).real * I / k
    p2 = float(np.real(np.trace(Pc.conj().T @ Pc)))
    np_ = float(np.linalg.norm(Pc))
    nq = float(np.linalg.norm(Qc))
    if np_ <= 1e-12 or nq <= 1e-12:
        return 0.0 if np_ <= 1e-12 and nq <= 1e-12 else 1.0
    a = float(np.real(np.trace(Pc.conj().T @ Qc)) / p2)
    if a <= 0:
        return 1.0
    return float(np.linalg.norm(Qc - a * Pc) / max(1.0, nq, abs(a) * np_))


def scalar_source_controls(source: np.ndarray, perms: tuple[tuple[int, ...], ...]) -> dict[str, Any]:
    constant_norm = float(np.linalg.norm(centered_source_operator(np.ones(N))))
    Q = centered_source_operator(source)
    max_cov = 0.0
    for p in perms:
        U = permutation_matrix(p)
        lhs = centered_source_operator(permute_vector(source, p))
        rhs = _herm(U @ Q @ U.conj().T)
        max_cov = max(max_cov, float(np.linalg.norm(lhs - rhs)))
    max_scale = 0.0
    for a in (0.2, 0.5, 2.0, 5.0, 11.0):
        max_scale = max(max_scale, projective_affine_residual(Q, centered_source_operator(a * source)))
    return {
        "constant_source_norm": constant_norm,
        "max_permutation_covariance_error": float(max_cov),
        "max_positive_scale_projective_residual": float(max_scale),
        "source_operator_norm": float(np.linalg.norm(Q)),
    }


def current_operator(nodes: tuple[int, ...], edges: tuple[tuple[int, int], ...], J: np.ndarray) -> np.ndarray:
    K = np.zeros((len(nodes), len(nodes)), dtype=float)
    for value, (u, v) in zip(np.asarray(J, dtype=float), edges):
        K[u, v] += value
        K[v, u] -= value
    return 1j * K


def structural_current_control(fixture: dict[str, Any], perms: tuple[tuple[int, ...], ...]) -> dict[str, Any]:
    B = incidence_matrix(fixture["nodes"], fixture["edges"])
    s = np.asarray(fixture["source"], dtype=float)
    J = B.T @ np.linalg.pinv(B @ B.T, rcond=1e-10) @ s
    PJ = current_operator(tuple(fixture["nodes"]), tuple(fixture["edges"]), J)
    max_herm = float(np.linalg.norm(PJ - PJ.conj().T))
    return {
        "scientific_evidence": False,
        "classification": "STRUCTURAL_MIN_NORM_CURRENT_CONTROL_NOT_CERTIFIED_SELECTED_CURRENT",
        "balance_residual": float(np.linalg.norm(B @ J - s)),
        "operator_hermiticity_error": max_herm,
        "operator_norm": float(np.linalg.norm(PJ)),
        "reason": "v13.25 certifies conditional selected-current existence/accuracy but does not archive the selected-current vector; this min-norm fixture is control-only",
    }


def parent_action_diagonal(q: np.ndarray, placement: str) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    out = np.empty(PARENT_DIM, dtype=float)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                idx = (a * N + b) * N + c
                if placement == "A_A":
                    out[idx] = q[a]
                elif placement == "A_B":
                    out[idx] = 0.5 * (q[b] + q[c])
                elif placement == "A_all":
                    out[idx] = (q[a] + q[b] + q[c]) / 3.0
                elif placement == "B1_only":
                    out[idx] = q[b]
                elif placement == "B2_only":
                    out[idx] = q[c]
                else:
                    raise ValueError(placement)
    return out


def placement_equivariance(perms: tuple[tuple[int, ...], ...]) -> dict[str, Any]:
    q0 = np.array([-2.0, -0.3, 0.4, 0.8, 1.1])
    max_err = 0.0
    for placement in ("A_A", "A_B", "A_all"):
        d0 = parent_action_diagonal(q0, placement)
        for p in perms:
            q1 = permute_vector(q0, p)
            d1 = parent_action_diagonal(q1, placement)
            pind = parent_index_perm(p)
            moved = np.empty_like(d0)
            moved[pind] = d0
            max_err = max(max_err, float(np.linalg.norm(d1 - moved)))
    q = q0
    b1 = parent_action_diagonal(q, "B1_only")
    b2 = parent_action_diagonal(q, "B2_only")
    # Partner swap is an exact reshaping control.
    B1 = b1.reshape(N, N, N)
    swap_error = float(np.linalg.norm(np.transpose(B1, (0, 2, 1)).reshape(-1) - b2))
    AB = parent_action_diagonal(q, "A_B").reshape(N, N, N)
    partner_sym_error = float(np.linalg.norm(np.transpose(AB, (0, 2, 1)) - AB))
    return {
        "max_allowed_placement_equivariance_error": float(max_err),
        "single_partner_swap_error": swap_error,
        "partner_symmetric_action_error": partner_sym_error,
    }


def compress_diagonal(L: np.ndarray, d: np.ndarray) -> np.ndarray:
    L = np.asarray(L, dtype=complex)
    d = np.asarray(d, dtype=float)
    return _herm(L.conj().T @ (d[:, None] * L))


def mapped_source(source: np.ndarray, phi: tuple[int, ...]) -> np.ndarray:
    return permute_vector(np.asarray(source, dtype=float), phi)


def identification_and_factor_diagnostics(
    source: np.ndarray,
    classes: list[dict[str, Any]],
    configs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    placements = ("A_A", "A_B", "A_all")
    class_results: dict[str, Any] = {}
    max_class_residual = 0.0
    max_factor_residual = 0.0
    for cfg_name, cfg in configs.items():
        L = cfg["L"]
        per_placement: dict[str, list[np.ndarray]] = {p: [] for p in placements}
        for rec in classes:
            phi = tuple(rec["representative"])
            q = mapped_source(source, phi)
            for placement in placements:
                P = compress_diagonal(L, parent_action_diagonal(q, placement))
                per_placement[placement].append(P)
        class_residuals = {}
        for placement, rays in per_placement.items():
            base = rays[0]
            residuals = [projective_affine_residual(base, x) for x in rays]
            class_residuals[placement] = float(max(residuals) if residuals else 0.0)
            max_class_residual = max(max_class_residual, class_residuals[placement])
        phi0 = tuple(classes[0]["representative"])
        q0 = mapped_source(source, phi0)
        rays0 = {
            p: compress_diagonal(L, parent_action_diagonal(q0, p)) for p in placements
        }
        factor_pairs = {}
        for i, p in enumerate(placements):
            for qname in placements[i + 1 :]:
                r = projective_affine_residual(rays0[p], rays0[qname])
                factor_pairs[f"{p}__{qname}"] = float(r)
                max_factor_residual = max(max_factor_residual, r)
        class_results[cfg_name] = {
            "max_identification_residual_by_placement": class_residuals,
            "factor_pair_residuals_first_class": factor_pairs,
            "centered_norms_first_class": {
                p: float(np.linalg.norm(rays0[p] - np.trace(rays0[p]).real * np.eye(SUPPORT_DIM) / SUPPORT_DIM))
                for p in placements
            },
        }
    return {
        "by_configuration": class_results,
        "max_identification_projective_residual": float(max_class_residual),
        "max_factor_projective_residual": float(max_factor_residual),
    }


def _contact_summary(v1403: ModuleType, cfg: dict[str, Any], P: np.ndarray) -> dict[str, Any]:
    c = v1403.source_contact(cfg["v1402"], cfg, P, certify_base_formula=False)
    hidden = c["hidden"]
    boundary = c["boundary"]
    normal = c["normal"]
    return {
        "hidden_classification": hidden["classification"],
        "hidden_norm": float(hidden["hidden_norm"]),
        "boundary_simple": bool(boundary is not None and boundary["simple"]),
        "boundary_radius": None if boundary is None else float(boundary["radius"]),
        "normal_classification": None if normal is None else normal["classification"],
    }


def positive_control(v1403: ModuleType, configs: dict[str, dict[str, Any]], actual_source: np.ndarray) -> dict[str, Any]:
    # Supplied identity identification and A-factor placement. Synthetic sources are
    # permitted only inside this explicitly non-scientific sensitivity control.
    controls = [
        ("archived_source", np.asarray(actual_source, dtype=float)),
        ("ramp_source", np.array([-2.0, -1.0, 0.0, 1.0, 2.0])),
        ("alternating_source", np.array([1.0, -1.0, 2.0, -2.0, 0.0])),
    ]
    attempts = []
    selected = None
    for cfg_name in ("V_A", "V_B"):
        cfg = configs[cfg_name]
        for source_name, s in controls:
            q = mapped_source(s, (0, 1, 2, 3, 4))
            P = compress_diagonal(cfg["L"], parent_action_diagonal(q, "A_A"))
            centered = P - np.trace(P).real * np.eye(SUPPORT_DIM) / SUPPORT_DIM
            rec = {
                "configuration": cfg_name,
                "source_name": source_name,
                "compressed_noncentral_norm": float(np.linalg.norm(centered)),
            }
            if np.linalg.norm(centered) > 1e-10:
                contact = _contact_summary(v1403, cfg, P)
                rec.update(contact)
                if (
                    contact["hidden_classification"] == "NONZERO_HIDDEN_COMPONENT"
                    and contact["boundary_simple"]
                    and contact["normal_classification"] == "RAY"
                    and selected is None
                ):
                    selected = dict(rec)
            attempts.append(rec)
    if selected is None:
        return {
            "classification": "SUPPLIED_SHARED_LABEL_AND_FACTOR_ACTION_NOT_PROVENANCE_DERIVATION",
            "success": False,
            "attempts": attempts,
        }
    return {
        "classification": "SUPPLIED_SHARED_LABEL_AND_FACTOR_ACTION_NOT_PROVENANCE_DERIVATION",
        "success": True,
        "selected": selected,
        "attempts": attempts,
        "scientific_evidence": False,
    }


def incompatible_control(
    comp: dict[str, Any], configs: dict[str, dict[str, Any]], perms: tuple[tuple[int, ...], ...]
) -> dict[str, Any]:
    common = set(tuple(x) for x in comp["common_fixed_gauge_group"])
    candidates = [p for p in perms if p not in common]
    if not candidates:
        return {"classification": "INCOMPATIBLE_LABEL_ACTION_REJECTED", "success": False}
    # Deterministic: choose the lexicographically first outside the common fixed group.
    p = candidates[0]
    errors = {}
    rejected = False
    for name, cfg in configs.items():
        perr = float(np.linalg.norm(permute_parent_matrix(cfg["Pi"], p) - cfg["Pi"]))
        terr = float(np.linalg.norm(permute_parent_matrix(cfg["T"], p) - cfg["T"]))
        arrangement_same = bool(np.array_equal(transform_arrangement(np.asarray(cfg["state"]["V"], int), p), cfg["state"]["V"]))
        errors[name] = {"projector_error": perr, "state_error": terr, "arrangement_invariant": arrangement_same}
        if (not arrangement_same) or perr >= GAUGE_TOL or terr >= GAUGE_TOL:
            rejected = True
    return {
        "classification": "INCOMPATIBLE_LABEL_ACTION_REJECTED",
        "success": bool(rejected),
        "permutation": list(p),
        "errors": errors,
        "scientific_evidence": False,
    }


def archive_semantic_link_status() -> dict[str, Any]:
    paths = [
        _repo_root() / "ResearchHistory" / "UQCF-GEM" / "v13" / "v13.25" / "REPORT.md",
        _repo_root() / "Tmp" / "TOE" / "UQCF_Quantum_Compatibility_Lab" / "README.md",
    ]
    return {
        "explicit_cross_model_label_functor_found": False,
        "audited_paths": [str(p.relative_to(_repo_root())) for p in paths],
        "sha256": {str(p.relative_to(_repo_root())): _sha256_path(p) for p in paths},
        "statement": "The frozen source-control and compatibility artifacts independently use five labels, but neither artifact certifies a node-to-quantum-label functor or semantic identification between them.",
    }


def run_audit() -> dict[str, Any]:
    perms = all_permutations()
    identity = tuple(range(N))
    # Exact group sanity checks.
    if inverse_perm(identity) != identity:
        raise ArithmeticError("identity inverse failed")
    for p in perms:
        if compose_perm(p, inverse_perm(p)) != identity:
            raise ArithmeticError("permutation inverse failed")

    fixture = parse_source_fixture()
    src = source_side_audit(fixture, perms)
    if src["incidence_rank"] != 4 or src["cycle_dimension"] != 3:
        raise ArithmeticError("source graph rank/cycle regression")

    v1501 = load_v1501()
    v1403, configs = build_configs(v1501)
    compat = {name: compatibility_side_audit(cfg, perms) for name, cfg in configs.items()}
    common_fixed = group_intersection(
        compat["V_A"]["fixed_gauge_group"], compat["V_B"]["fixed_gauge_group"]
    )
    if not common_fixed:
        raise ArithmeticError("identity missing from compatibility groups")
    comp_summary = {
        "V_A": compat["V_A"],
        "V_B": compat["V_B"],
        "common_fixed_gauge_group": [list(p) for p in common_fixed],
        "common_fixed_gauge_order": len(common_fixed),
        "common_group_sha256": _sha256_json(common_fixed),
    }

    Gsrc = [tuple(x) for x in src["graph_automorphisms"]]
    classes = double_cosets(common_fixed, Gsrc, perms)
    source = np.asarray(fixture["source"], dtype=float)
    scalar_ctrl = scalar_source_controls(source, perms)
    placement_ctrl = placement_equivariance(perms)
    diagnostics = identification_and_factor_diagnostics(source, classes, configs)
    current_ctrl = structural_current_control(fixture, perms)
    semantic = archive_semantic_link_status()
    pos = positive_control(v1403, configs, source)
    neg = incompatible_control(comp_summary, configs, perms)

    numerical_failure = (
        scalar_ctrl["max_permutation_covariance_error"] >= PERM_TOL
        or scalar_ctrl["max_positive_scale_projective_residual"] >= PERM_TOL
        or placement_ctrl["max_allowed_placement_equivariance_error"] >= PERM_TOL
        or any(compat[n]["max_projector_covariance_error"] >= GAUGE_TOL for n in ("V_A", "V_B"))
        or not pos.get("success", False)
        or not neg.get("success", False)
    )

    common_nontrivial = len(common_fixed) > 1
    canonical_identification = len(classes) == 1
    identification_inert = diagnostics["max_identification_projective_residual"] < PROJECTIVE_TOL
    factor_inert = diagnostics["max_factor_projective_residual"] < PROJECTIVE_TOL

    if numerical_failure:
        outcome = "UNRESOLVED_EQUIVARIANCE_AUDIT"
    elif not common_nontrivial and not semantic["explicit_cross_model_label_functor_found"]:
        outcome = "NO_CERTIFIED_SHARED_LABEL_CARRIER"
    elif not canonical_identification and not identification_inert:
        outcome = "SHARED_LABEL_IDENTIFICATION_NONUNIQUE"
    elif not factor_inert:
        outcome = "SHARED_LABEL_BUT_FACTOR_ACTION_NONUNIQUE"
    else:
        outcome = "SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY"

    centered_norms = []
    for cfg in configs.values():
        q = source
        for placement in ("A_A", "A_B", "A_all"):
            P = compress_diagonal(cfg["L"], parent_action_diagonal(q, placement))
            Pc = P - np.trace(P).real * np.eye(SUPPORT_DIM) / SUPPORT_DIM
            centered_norms.append(float(np.linalg.norm(Pc)))
    secondary = "CENTRAL_ONLY_OR_PGRL_NULL" if max(centered_norms) <= 1e-10 else "NONCENTRAL_CONTROL_SOURCES_EXIST"

    return {
        "version": VERSION,
        "permutation_count": len(perms),
        "source_fixture": {
            k: v for k, v in fixture.items() if k not in {"nodes", "edges", "source"}
        } | {
            "nodes": list(fixture["nodes"]),
            "edges": [list(x) for x in fixture["edges"]],
            "source": [float(x) for x in fixture["source"]],
        },
        "source_side": src,
        "compatibility": {name: {k: v for k, v in compat[name].items() if k != "records"} for name in ("V_A", "V_B")},
        "common_fixed_gauge_group": [list(p) for p in common_fixed],
        "common_fixed_gauge_order": len(common_fixed),
        "common_group_sha256": _sha256_json(common_fixed),
        "identification_orbits": {
            "double_coset_count": len(classes),
            "classes": classes,
            "partition_size": int(sum(x["size"] for x in classes)),
            "sha256": _sha256_json(classes),
            "canonical_up_to_gauge": bool(canonical_identification),
            "downstream_projectively_inert": bool(identification_inert),
        },
        "semantic_link": semantic,
        "scalar_source_controls": scalar_ctrl,
        "current_control": current_ctrl,
        "placement_controls": placement_ctrl,
        "representation_diagnostics": diagnostics,
        "positive_control": pos,
        "incompatible_control": neg,
        "secondary_status": secondary,
        "gate_outcome": outcome,
        "scientific_breakthrough": bool(outcome == "SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY"),
        "claim_scope": "finite shared-label/permutation representation audit between the frozen five-node source control and frozen three-factor five-level quantum compatibility model",
        "not_derived": [
            "absolute source magnitude",
            "observer source calibration",
            "physical stress-energy",
            "source-to-coframe/solder law",
            "physical metric or spacetime",
            "absolute gravitational coupling",
            "Einstein equations",
            "Pillar 3 closure",
        ],
        "Pillar_3": "OPEN",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
