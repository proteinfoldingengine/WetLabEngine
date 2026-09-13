#!/usr/bin/env python3
"""v15.03 graph-site factorization / local-gauge source-lift audit.

Archived evidence and supplied five-qubit controls are intentionally separate.
Controls test mathematical sufficiency/covariance only; they are not provenance.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
SOURCE_PATH = ROOT / "Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py"
SMALL_NETWORK_PATH = ROOT / "Tmp/TOE/ThePhysicsParadox/uqcf_gate_a_small_network_phi_simulation_package 2/uqcf_gate_a_small_network_phi_simulation.py"
V1311 = ROOT / "ResearchHistory/UQCF-GEM/v13/v13.11/SUMMARY.json"
V1315 = ROOT / "ResearchHistory/UQCF-GEM/v13/v13.15/SUMMARY.json"
V1327 = ROOT / "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/README.md"
V1404 = ROOT / "ResearchHistory/UQCF-GEM/v14/v14.04/SUMMARY.json"
V1501 = ROOT / "ResearchHistory/UQCF-GEM/v15/v15.01/SUMMARY.json"
V1502 = ROOT / "ResearchHistory/UQCF-GEM/v15/v15.02/SUMMARY.json"

EXPECTED_NODES = (0, 1, 2, 3, 4)
EXPECTED_EDGES = ((0, 1), (1, 3), (0, 2), (2, 4), (4, 3), (1, 2), (0, 4))
EXPECTED_SOURCE = (-1.0, 0.0, 0.0, 1.0, 0.0)
DIMS = (2, 2, 2, 2, 2)
R_A = (0.15, -0.31, 0.42, 0.63, -0.22)
R_B = (0.52, -0.18, 0.27, -0.47, 0.36)
FUNCTIONS = ("identity", "linear", "square", "log")
SCALES = (0.2, 0.5, 2.0, 5.0, 11.0)

I2 = np.eye(2, dtype=complex)
Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
H = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2.0)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha256_json(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def incidence_matrix(nodes: Sequence[int], edges: Sequence[Sequence[int]]) -> np.ndarray:
    pos = {n: i for i, n in enumerate(nodes)}
    B = np.zeros((len(nodes), len(edges)), dtype=float)
    for e, (u, v) in enumerate(edges):
        B[pos[int(u)], e] = -1.0
        B[pos[int(v)], e] = 1.0
    return B


def _literal_assignment(tree: ast.AST, name: str) -> Any:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            try:
                return ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    raise ValueError(f"literal assignment {name!r} not found")


def _subscript_assignments(scope: ast.AST, array_name: str, length: int) -> tuple[float, ...]:
    out = np.zeros(length, dtype=float)
    found = 0
    for node in ast.walk(scope):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Subscript):
            continue
        if not isinstance(target.value, ast.Name) or target.value.id != array_name:
            continue
        try:
            idx = int(ast.literal_eval(target.slice))
            val = float(ast.literal_eval(node.value))
        except (ValueError, TypeError):
            continue
        out[idx] = val
        found += 1
    if not found:
        raise ValueError(f"no literal assignments to {array_name}[i]")
    return tuple(float(x) for x in out)


def parse_source_fixture() -> dict[str, Any]:
    tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
    nodes = tuple(int(x) for x in _literal_assignment(tree, "NODES"))
    edges = tuple(tuple(int(y) for y in e) for e in _literal_assignment(tree, "EDGES"))
    source = _subscript_assignments(tree, "SOURCE", len(nodes))
    assert nodes == EXPECTED_NODES
    assert edges == EXPECTED_EDGES
    assert source == EXPECTED_SOURCE
    B = incidence_matrix(nodes, edges)
    rank = int(np.linalg.matrix_rank(B, tol=1e-12))
    fixture = {"nodes": nodes, "edges": edges, "source": source}
    return {
        "path": SOURCE_PATH.relative_to(ROOT).as_posix(),
        "sha256": sha256_file(SOURCE_PATH),
        "fixture_sha256": sha256_json(fixture),
        "nodes": list(nodes),
        "edges": [list(e) for e in edges],
        "source": list(source),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "source_sum_abs": abs(sum(source)),
        "incidence_rank": rank,
        "cycle_dimension": len(edges) - rank,
    }


def parse_small_network_fixture() -> dict[str, Any]:
    """Parse build_small_network structurally; never rely on prose substrings."""
    tree = ast.parse(SMALL_NETWORK_PATH.read_text(encoding="utf-8"))
    fn = next(
        n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "build_small_network"
    )
    nodes = tuple(int(x) for x in _literal_assignment(fn, "nodes"))
    edges = tuple(tuple(int(y) for y in e) for e in _literal_assignment(fn, "edges"))
    source = _subscript_assignments(fn, "s", len(nodes))
    assert nodes == EXPECTED_NODES
    assert edges == EXPECTED_EDGES
    assert source == EXPECTED_SOURCE
    return {
        "nodes": list(nodes),
        "edges": [list(e) for e in edges],
        "source": list(source),
        "fixture_sha256": sha256_json({"nodes": nodes, "edges": edges, "source": source}),
    }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _record(path: Path, classification: str, facts: Sequence[str]) -> dict[str, Any]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": sha256_file(path),
        "classification": classification,
        "decisive_facts": list(facts),
    }


def archive_graph_site_audit() -> dict[str, Any]:
    v1311 = _load_json(V1311)
    v1315 = _load_json(V1315)
    v1404 = _load_json(V1404)
    v1501 = _load_json(V1501)
    v1502 = _load_json(V1502)
    demo = V1327.read_text(encoding="utf-8")
    small_fixture = parse_small_network_fixture()

    assert v1315["generic_path_counterexample"]["graph"].startswith("4-node path")
    assert v1311["gauge_covariance"]["status"] == "PASS"
    assert "six-qubit laboratory" in demo
    assert small_fixture["nodes"] == list(EXPECTED_NODES)
    assert small_fixture["edges"] == [list(e) for e in EXPECTED_EDGES]
    assert small_fixture["source"] == list(EXPECTED_SOURCE)
    assert v1404["class_b"]["certified_natural_support_link_count"] == 0
    assert v1501["parent_dimension"] == 125 and v1501["support_dimension"] == 25
    assert v1501["archive_inventory"]["same_parent_source_class_count"] == 0
    assert v1502["gate_outcome"] == "NO_CERTIFIED_SHARED_LABEL_CARRIER"

    records = [
        _record(V1315, "GRAPH_INDEXED_QUANTUM_MODEL_CONTROL_ONLY", [
            "quantum graph example is a 4-node path, not the retained 5-node/7-edge graph",
            "site-local quantum source and graph-local response are explicit",
        ]),
        _record(V1311, "LOCAL_FRAME_COVARIANCE_ONLY", [
            "independent local-frame covariance is certified",
            "no exact retained graph-to-quantum-site identity is certified",
        ]),
        _record(V1327, "GRAPH_INDEXED_QUANTUM_MODEL_CONTROL_ONLY", [
            "artifact is an explicit six-qubit laboratory",
            "graph/source support are declared model inputs, not provenance derivation",
        ]),
        _record(SMALL_NETWORK_PATH, "NO_GRAPH_SITE_IDENTITY_STATEMENT", [
            "AST parsing recovers the exact retained five-node/seven-edge/source fixture",
            "artifact is graph source-current identifiability, not quantum factor identity",
        ]),
        _record(V1404, "NO_GRAPH_SITE_IDENTITY_STATEMENT", [
            "certified natural support-link count is zero",
        ]),
        _record(V1501, "NO_GRAPH_SITE_IDENTITY_STATEMENT", [
            "compatibility parent is C^125 with C^25 support",
            "same-parent provenance/source class count is zero",
            "six-qubit demo is a different parent with no frozen natural functor to C^125",
        ]),
        _record(V1502, "NO_GRAPH_SITE_IDENTITY_STATEMENT", [
            "five-node to five-level basis-label shortcut is not certified",
        ]),
    ]
    graph_models = any(r["classification"] == "GRAPH_INDEXED_QUANTUM_MODEL_CONTROL_ONLY" for r in records)
    exact = any(r["classification"] == "EXACT_RETAINED_GRAPH_SITE_IDENTITY" for r in records)
    natural_map = v1404["class_b"]["certified_natural_support_link_count"] > 0
    if exact:
        factorization = "EXACT_GRAPH_SITE_FACTORIZATION_CERTIFIED"
    elif graph_models:
        factorization = "GRAPH_INDEXED_QUANTUM_MODELS_EXIST_BUT_EXACT_FACTOR_IDENTIFICATION_UNDERIVED"
    else:
        factorization = "NO_GRAPH_INDEXED_QUANTUM_CARRIER_FOUND"
    if not exact:
        carrier = "NO_EXACT_GRAPH_SITE_CARRIER"
    elif natural_map:
        carrier = "NATURAL_MAP_TO_COMPATIBILITY_PARENT_CERTIFIED"
    else:
        carrier = "GRAPH_SITE_CARRIER_DISTINCT_FROM_COMPATIBILITY_PARENT"
    return {
        "factorization_status": factorization,
        "exact_graph_site_factorization_certified": exact,
        "graph_indexed_quantum_models_exist": graph_models,
        "carrier_status": carrier,
        "natural_map_to_compatibility_parent_certified": bool(natural_map),
        "compatibility_parent_relation": "FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT",
        "small_network_fixture": small_fixture,
        "records": records,
        "records_sha256": sha256_json(records),
    }


def dimension_factorization_audit() -> dict[str, Any]:
    target, sites = 125, 5
    solutions: list[tuple[int, ...]] = []

    def walk(prefix: tuple[int, ...], product: int) -> None:
        if len(prefix) == sites:
            if product == target:
                solutions.append(prefix)
            return
        for d in range(2, target + 1):
            p = product * d
            if p > target:
                break
            if target % p == 0:
                walk(prefix + (d,), p)

    walk((), 1)
    assert not solutions
    return {
        "compatibility_parent_dimension": target,
        "required_site_count": sites,
        "minimum_site_dimension": 2,
        "prime_factorization": [5, 5, 5],
        "five_nontrivial_factorization_possible": False,
        "solution_count": 0,
        "classification": "FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT",
    }


def kron_all(ops: Iterable[np.ndarray]) -> np.ndarray:
    out = np.array([[1.0 + 0.0j]])
    for op in ops:
        out = np.kron(out, np.asarray(op, dtype=complex))
    return out


def embed_site(op: np.ndarray, site: int) -> np.ndarray:
    ops = [I2] * len(DIMS)
    ops[site] = np.asarray(op, dtype=complex)
    return kron_all(ops)


def swap_operator(dim: int = 2) -> np.ndarray:
    out = np.zeros((dim * dim, dim * dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            out[j * dim + i, i * dim + j] = 1.0
    return out


def _rotation(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=complex)


def deterministic_local_unitaries() -> tuple[np.ndarray, ...]:
    return (
        H,
        np.diag([1.0, np.exp(1j * math.pi / 5.0)]),
        _rotation(math.pi / 7.0),
        H @ np.diag([1.0, np.exp(1j * math.pi / 9.0)]),
        _rotation(-math.pi / 11.0),
    )


def centrality_audit() -> tuple[dict[str, Any], dict[str, Any]]:
    us = deterministic_local_unitaries()
    U = kron_all(us)
    I32 = np.eye(32, dtype=complex)
    identity_error = float(np.linalg.norm(U @ I32 @ U.conj().T - I32))
    Pz = embed_site(Z, 0)
    noncentral = float(np.linalg.norm(U @ Pz @ U.conj().T - Pz))
    S01 = kron_all((swap_operator(), I2, I2, I2))
    U_ind = kron_all((H, us[1], I2, I2, I2))
    U_tied = kron_all((H, H, I2, I2, I2))
    swap_ind = float(np.linalg.norm(U_ind @ S01 @ U_ind.conj().T - S01))
    swap_tied = float(np.linalg.norm(U_tied @ S01 @ U_tied.conj().T - S01))
    theorem = {
        "analytic_classification": "FULL_PRODUCT_LOCAL_UNITARY_COMMUTANT_IS_CENTER",
        "state_independent_source_classification": "CENTRAL_ONLY",
        "pgrl_classification": "CENTRAL_PGRL_NULL",
        "statement": "A deterministic state-independent Hermitian lift of gauge-trivial graph scalar/current data invariant under all independent local unitaries lies in the scalar center; central P is PGRL-null.",
    }
    controls = {
        "fixture": "SUPPLIED_FIVE_QUBIT_CARRIER_CONTROL_NOT_PROVENANCE_DERIVATION",
        "identity_invariance_error": identity_error,
        "noncentral_independent_frame_violation": noncentral,
        "swap_independent_frame_violation": swap_ind,
        "swap_tied_frame_error": swap_tied,
        "tied_frame_classification": "WEAKER_TIED_FRAME_GAUGE_NOT_ADJUDICATION_GAUGE",
    }
    return theorem, controls


def qubit_state(r: float) -> np.ndarray:
    rho = 0.5 * (I2 + float(r) * Z)
    vals = np.linalg.eigvalsh(rho)
    assert vals[0] > 0.0
    assert abs(float(np.trace(rho).real) - 1.0) < 1e-14
    return rho


def matrix_function_centered(rho: np.ndarray, name: str) -> np.ndarray:
    vals, vecs = np.linalg.eigh(np.asarray(rho, dtype=complex))
    if name == "identity":
        fvals = np.ones_like(vals)
    elif name == "linear":
        fvals = vals
    elif name == "square":
        fvals = vals**2
    elif name == "log":
        if np.min(vals) <= 0.0:
            raise ValueError("log requires faithful local states")
        fvals = np.log(vals)
    else:
        raise ValueError(name)
    op = (vecs * fvals) @ vecs.conj().T
    op = 0.5 * (op + op.conj().T)
    return op - np.trace(op) / 2.0 * I2


def graph_site_source(source: Sequence[float], states: Sequence[np.ndarray], fn: str) -> np.ndarray:
    P = np.zeros((32, 32), dtype=complex)
    for i, coeff in enumerate(source):
        P += float(coeff) * embed_site(matrix_function_centered(states[i], fn), i)
    return 0.5 * (P + P.conj().T)


def _center(P: np.ndarray) -> np.ndarray:
    return P - np.trace(P) / P.shape[0] * np.eye(P.shape[0], dtype=complex)


def projective_residual(P: np.ndarray, Q: np.ndarray) -> float:
    P, Q = _center(P), _center(Q)
    a, b = float(np.linalg.norm(P)), float(np.linalg.norm(Q))
    if a < 1e-14 and b < 1e-14:
        return 0.0
    if min(a, b) < 1e-14:
        return 1.0
    return float(np.linalg.norm(P / a - Q / b))


def _covariance_error(source: Sequence[float], states: Sequence[np.ndarray], fn: str) -> float:
    us = deterministic_local_unitaries()
    U = kron_all(us)
    base = graph_site_source(source, states, fn)
    rotated = [u @ rho @ u.conj().T for u, rho in zip(us, states)]
    rebuilt = graph_site_source(source, rotated, fn)
    target = U @ base @ U.conj().T
    return float(np.linalg.norm(rebuilt - target) / max(1.0, float(np.linalg.norm(target))))


def state_dependent_audit(fixture: dict[str, Any]) -> dict[str, Any]:
    source = tuple(float(x) for x in fixture["source"])
    controls: dict[str, Any] = {}
    pair_values: list[float] = []
    max_cov = max_scale = max_herm = max_trace = 0.0
    for label, radii in (("A", R_A), ("B", R_B)):
        states = [qubit_state(r) for r in radii]
        matrices: dict[str, np.ndarray] = {}
        families: dict[str, Any] = {}
        for fn in FUNCTIONS:
            P = graph_site_source(source, states, fn)
            matrices[fn] = P
            herm = float(np.linalg.norm(P - P.conj().T))
            tr = float(abs(complex(np.trace(P))))
            cov = _covariance_error(source, states, fn)
            scales = []
            if fn != "identity":
                for a in SCALES:
                    scaled = graph_site_source(tuple(a * x for x in source), states, fn)
                    scales.append(projective_residual(P, scaled))
            max_cov = max(max_cov, cov)
            max_scale = max(max_scale, max(scales, default=0.0))
            max_herm = max(max_herm, herm)
            max_trace = max(max_trace, tr)
            families[fn] = {
                "norm": float(np.linalg.norm(P)),
                "centered_norm": float(np.linalg.norm(_center(P))),
                "hermiticity_error": herm,
                "trace_abs": tr,
                "covariance_error": cov,
                "max_positive_scale_projective_residual": max(scales, default=0.0),
            }
        pairs: dict[str, float] = {}
        noncentral = ("linear", "square", "log")
        for i, a in enumerate(noncentral):
            for b in noncentral[i + 1:]:
                d = projective_residual(matrices[a], matrices[b])
                pairs[f"{a}__{b}"] = d
                pair_values.append(d)
        controls[label] = {
            "bloch_radii": list(radii),
            "minimum_local_eigenvalue": min(float(np.min(np.linalg.eigvalsh(rho))) for rho in states),
            "families": families,
            "pairwise_projective_residuals": pairs,
        }
    nonunique = any(x > 1e-8 for x in pair_values)
    B = incidence_matrix(fixture["nodes"], fixture["edges"])
    s = np.asarray(source)
    J = np.linalg.pinv(B) @ s
    return {
        "classification": "SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION",
        "scientific_evidence_for_factorization": False,
        "candidate_functions": list(FUNCTIONS),
        "controls": controls,
        "constant_family_max_norm": max(controls[c]["families"]["identity"]["centered_norm"] for c in controls),
        "max_covariance_error": max_cov,
        "max_positive_scale_projective_residual": max_scale,
        "max_hermiticity_error": max_herm,
        "max_trace_abs": max_trace,
        "max_pairwise_projective_residual": max(pair_values),
        "min_pairwise_projective_residual": min(pair_values),
        "family_status": "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE" if nonunique else "STATE_DEPENDENT_FROZEN_FAMILIES_PROJECTIVELY_EQUIVALENT",
        "current_control": {
            "scientific_evidence": False,
            "classification": "MIN_NORM_CURRENT_CONTROL_NOT_PROVENANCE_SELECTED",
            "current": [float(x) for x in J],
            "balance_residual": float(np.linalg.norm(B @ J - s)),
        },
    }


def run_audit() -> dict[str, Any]:
    fixture = parse_source_fixture()
    archive = archive_graph_site_audit()
    dimension = dimension_factorization_audit()
    theorem, centrality = centrality_audit()
    state = state_dependent_audit(fixture)
    numerical_failure = not (
        fixture["source_sum_abs"] < 1e-14
        and fixture["incidence_rank"] == 4
        and fixture["cycle_dimension"] == 3
        and centrality["identity_invariance_error"] < 2e-12
        and centrality["noncentral_independent_frame_violation"] > 1e-6
        and centrality["swap_independent_frame_violation"] > 1e-6
        and centrality["swap_tied_frame_error"] < 2e-12
        and state["constant_family_max_norm"] < 2e-12
        and state["max_covariance_error"] < 2e-10
        and state["max_positive_scale_projective_residual"] < 2e-12
        and state["max_hermiticity_error"] < 2e-12
        and state["max_trace_abs"] < 2e-12
    )
    exact = archive["exact_graph_site_factorization_certified"]
    natural_map = archive["natural_map_to_compatibility_parent_certified"]
    nonunique = state["family_status"] == "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"
    if numerical_failure:
        outcome = "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT"
    elif not exact:
        outcome = "NO_CERTIFIED_GRAPH_SITE_FACTORIZATION"
    elif exact and not natural_map:
        outcome = "GRAPH_SITE_CARRIER_NOT_COMPATIBILITY_PARENT"
    elif nonunique:
        outcome = "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"
    else:
        outcome = "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT"
    return {
        "version": "v15.03",
        "title": "Graph-Site Factorization / Local-Gauge Source Lift Gate",
        "source_fixture": fixture,
        "archive_graph_site_audit": archive,
        "dimension_theorem": dimension,
        "centrality_theorem": theorem,
        "centrality_controls": centrality,
        "state_dependent_controls": state,
        "gate_outcome": outcome,
        "secondary_statuses": [theorem["pgrl_classification"], state["family_status"], dimension["classification"], archive["carrier_status"]],
        "scientific_breakthrough": outcome == "GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY",
        "Pillar_3": "OPEN",
        "claim_scope": "graph-site factorization, independent local-gauge source-lift naturality, state-dependent source-family canonicality, and carrier relevance to the certified C^125 parent",
        "interpretation": "Graph-indexed quantum modeling and independent local-frame covariance exist in the frozen stack, but the audited archive does not certify the exact retained five-node source graph as five quantum tensor factors. Independently, scalar/current data alone are central/PGRL-null under full independent local gauge. Supplied state context can produce lawful noncentral covariant source families, whose projective canonicality is audited separately. Any genuine five-site carrier is arithmetically distinct from C^125 and still requires an earned natural cross-carrier map.",
        "not_derived": [
            "a certified exact retained-node-to-quantum-site factorization",
            "a natural graph-site-to-C125 compatibility-parent map",
            "Genesis/provenance to the v14.03 projective support-source ray",
            "absolute source magnitude",
            "observer source calibration",
            "physical stress-energy",
            "source-to-coframe/solder law",
            "physical metric or spacetime",
            "absolute gravitational coupling",
            "Einstein equations",
            "physical time primitive",
            "Pillar 3 closure",
        ],
        "stop_rule": "Do not choose a Pauli axis, privilege log(rho), tie local frames, invent a cross-carrier isometry, promote a min-norm current, import pruning/entropy as a pre-pruning selector, or use ADM/Einstein/gravity residuals.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
