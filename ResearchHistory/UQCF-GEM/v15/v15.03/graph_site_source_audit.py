#!/usr/bin/env python3
"""v15.03 graph-site factorization / local-gauge source-lift audit.

This gate deliberately separates archived provenance/type evidence from supplied
five-qubit controls.  The supplied controls test sufficiency/covariance only;
they are not evidence that the frozen retained graph has been identified with a
quantum tensor-factor carrier.
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
HERE = Path(__file__).resolve().parent

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
X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
H = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2.0)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha256_json(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _literal_assignment(tree: ast.AST, name: str) -> Any:
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        pass
    raise ValueError(f"literal assignment {name!r} not found")


def parse_source_fixture() -> dict[str, Any]:
    tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
    nodes = tuple(int(x) for x in _literal_assignment(tree, "NODES"))
    edges = tuple(tuple(int(y) for y in x) for x in _literal_assignment(tree, "EDGES"))
    source = np.zeros(len(nodes), dtype=float)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Subscript):
            continue
        if not isinstance(target.value, ast.Name) or target.value.id != "SOURCE":
            continue
        try:
            idx = int(ast.literal_eval(target.slice))
            val = float(ast.literal_eval(node.value))
        except (ValueError, TypeError):
            continue
        source[idx] = val

    source_tuple = tuple(float(x) for x in source)
    assert nodes == EXPECTED_NODES, nodes
    assert edges == EXPECTED_EDGES, edges
    assert source_tuple == EXPECTED_SOURCE, source_tuple

    B = incidence_matrix(nodes, edges)
    rank = int(np.linalg.matrix_rank(B, tol=1e-12))
    fixture = {
        "nodes": list(nodes),
        "edges": [list(e) for e in edges],
        "source": list(source_tuple),
    }
    return {
        "path": SOURCE_PATH.relative_to(ROOT).as_posix(),
        "sha256": sha256_file(SOURCE_PATH),
        "fixture_sha256": sha256_json(fixture),
        "nodes": list(nodes),
        "edges": [list(e) for e in edges],
        "source": list(source_tuple),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "source_sum_abs": abs(float(np.sum(source))),
        "incidence_rank": rank,
        "cycle_dimension": len(edges) - rank,
    }


def incidence_matrix(nodes: Sequence[int], edges: Sequence[Sequence[int]]) -> np.ndarray:
    index = {n: i for i, n in enumerate(nodes)}
    B = np.zeros((len(nodes), len(edges)), dtype=float)
    for k, (u, v) in enumerate(edges):
        B[index[int(u)], k] = -1.0
        B[index[int(v)], k] = +1.0
    return B


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _evidence_record(path: Path, classification: str, decisive_facts: Sequence[str]) -> dict[str, Any]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": sha256_file(path),
        "classification": classification,
        "decisive_facts": list(decisive_facts),
    }


def archive_graph_site_audit() -> dict[str, Any]:
    v1311 = _read_json(V1311)
    v1315 = _read_json(V1315)
    v1404 = _read_json(V1404)
    v1501 = _read_json(V1501)
    v1502 = _read_json(V1502)
    demo = V1327.read_text(encoding="utf-8")
    small = SMALL_NETWORK_PATH.read_text(encoding="utf-8")

    assert v1315["generic_path_counterexample"]["graph"].startswith("4-node path")
    assert v1311["gauge_covariance"]["status"] == "PASS"
    assert "six-qubit laboratory" in demo
    assert "5 nodes" in small or "N = 5" in small or "NODES" in small
    assert v1404["class_b"]["certified_natural_support_link_count"] == 0
    assert v1501["parent_dimension"] == 125 and v1501["support_dimension"] == 25
    assert v1501["archive_inventory"]["same_parent_source_class_count"] == 0
    assert v1502["gate_outcome"] == "NO_CERTIFIED_SHARED_LABEL_CARRIER"

    records = [
        _evidence_record(
            V1315,
            "GRAPH_INDEXED_QUANTUM_MODEL_CONTROL_ONLY",
            [
                "generic counterexample uses a 4-node path, not the retained 5-node/7-edge graph",
                "site-local quantum source and graph-local response are explicit",
            ],
        ),
        _evidence_record(
            V1311,
            "LOCAL_FRAME_COVARIANCE_ONLY",
            [
                "independent local-frame covariance is certified",
                "no exact retained 5-node source-graph to quantum-site identity is certified",
            ],
        ),
        _evidence_record(
            V1327,
            "GRAPH_INDEXED_QUANTUM_MODEL_CONTROL_ONLY",
            [
                "artifact is an explicit six-qubit laboratory",
                "graph/source support are declared model inputs, not provenance derivation",
            ],
        ),
        _evidence_record(
            SMALL_NETWORK_PATH,
            "NO_GRAPH_SITE_IDENTITY_STATEMENT",
            [
                "exact retained five-node/seven-edge source-current network is present",
                "artifact is a finite network/current simulation and does not certify quantum tensor-factor identity",
            ],
        ),
        _evidence_record(
            V1404,
            "NO_GRAPH_SITE_IDENTITY_STATEMENT",
            [
                "certified natural support-link count is zero",
                "frozen richer carriers have no certified intertwiner into the v14.03 support",
            ],
        ),
        _evidence_record(
            V1501,
            "NO_GRAPH_SITE_IDENTITY_STATEMENT",
            [
                "compatibility parent is exactly C^125 with C^25 support",
                "same-parent provenance/source class count is zero",
                "six-qubit demo is explicitly classified as a different parent with no frozen natural functor to C^125",
            ],
        ),
        _evidence_record(
            V1502,
            "NO_GRAPH_SITE_IDENTITY_STATEMENT",
            [
                "five-node to five-level basis-label shortcut is not certified",
                "all 120 label identifications remain inequivalent under earned gauge actions",
            ],
        ),
    ]

    graph_indexed_exists = any(r["classification"] == "GRAPH_INDEXED_QUANTUM_MODEL_CONTROL_ONLY" for r in records)
    exact_identity_records = [r for r in records if r["classification"] == "EXACT_RETAINED_GRAPH_SITE_IDENTITY"]
    exact_certified = bool(exact_identity_records)
    natural_map_certified = bool(v1404["class_b"]["certified_natural_support_link_count"] > 0)

    if exact_certified:
        factorization_status = "EXACT_GRAPH_SITE_FACTORIZATION_CERTIFIED"
    elif graph_indexed_exists:
        factorization_status = "GRAPH_INDEXED_QUANTUM_MODELS_EXIST_BUT_EXACT_FACTOR_IDENTIFICATION_UNDERIVED"
    else:
        factorization_status = "NO_GRAPH_INDEXED_QUANTUM_CARRIER_FOUND"

    if not exact_certified:
        carrier_status = "NO_EXACT_GRAPH_SITE_CARRIER"
    elif natural_map_certified:
        carrier_status = "NATURAL_MAP_TO_COMPATIBILITY_PARENT_CERTIFIED"
    else:
        carrier_status = "GRAPH_SITE_CARRIER_DISTINCT_FROM_COMPATIBILITY_PARENT"

    return {
        "factorization_status": factorization_status,
        "exact_graph_site_factorization_certified": exact_certified,
        "graph_indexed_quantum_models_exist": graph_indexed_exists,
        "carrier_status": carrier_status,
        "natural_map_to_compatibility_parent_certified": natural_map_certified,
        "compatibility_parent_relation": "FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT",
        "records": records,
        "records_sha256": sha256_json(records),
    }


def dimension_factorization_audit() -> dict[str, Any]:
    target = 125
    site_count = 5
    solutions: list[tuple[int, ...]] = []

    def search(prefix: tuple[int, ...], product: int) -> None:
        if len(prefix) == site_count:
            if product == target:
                solutions.append(prefix)
            return
        for d in range(2, target + 1):
            new_product = product * d
            if new_product > target:
                break
            if target % new_product == 0:
                search(prefix + (d,), new_product)

    search((), 1)
    assert not solutions
    return {
        "compatibility_parent_dimension": target,
        "required_site_count": site_count,
        "minimum_site_dimension": 2,
        "prime_factorization": [5, 5, 5],
        "five_nontrivial_factorization_possible": False,
        "solution_count": len(solutions),
        "classification": "FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT",
    }


def kron_all(ops: Iterable[np.ndarray]) -> np.ndarray:
    out = np.array([[1.0 + 0.0j]])
    for op in ops:
        out = np.kron(out, np.asarray(op, dtype=complex))
    return out


def embed_site(op: np.ndarray, site: int, dims: Sequence[int] = DIMS) -> np.ndarray:
    if any(d != 2 for d in dims):
        raise ValueError("v15.03 supplied control currently uses qubit factors only")
    ops = [I2 for _ in dims]
    ops[site] = np.asarray(op, dtype=complex)
    return kron_all(ops)


def swap_operator(dim: int = 2) -> np.ndarray:
    S = np.zeros((dim * dim, dim * dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            S[j * dim + i, i * dim + j] = 1.0
    return S


def _real_rotation(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=complex)


def deterministic_local_unitaries() -> tuple[np.ndarray, ...]:
    phase = np.diag([1.0, np.exp(1j * math.pi / 5.0)])
    return (
        H,
        phase,
        _real_rotation(math.pi / 7.0),
        H @ np.diag([1.0, np.exp(1j * math.pi / 9.0)]),
        _real_rotation(-math.pi / 11.0),
    )


def centrality_controls() -> tuple[dict[str, Any], dict[str, Any]]:
    local_us = deterministic_local_unitaries()
    U = kron_all(local_us)
    I32 = np.eye(32, dtype=complex)
    identity_error = float(np.linalg.norm(U @ I32 @ U.conj().T - I32))

    Pz = embed_site(Z, 0)
    noncentral_violation = float(np.linalg.norm(U @ Pz @ U.conj().T - Pz))

    S01 = kron_all((swap_operator(2), I2, I2, I2))
    independent_pair = kron_all((H, local_us[1], I2, I2, I2))
    swap_independent_violation = float(
        np.linalg.norm(independent_pair @ S01 @ independent_pair.conj().T - S01)
    )
    tied_pair = kron_all((H, H, I2, I2, I2))
    swap_tied_error = float(np.linalg.norm(tied_pair @ S01 @ tied_pair.conj().T - S01))

    theorem = {
        "analytic_classification": "FULL_PRODUCT_LOCAL_UNITARY_COMMUTANT_IS_CENTER",
        "state_independent_source_classification": "CENTRAL_ONLY",
        "pgrl_classification": "CENTRAL_PGRL_NULL",
        "statement": (
            "Retained scalar/current graph data are invariant under independent internal local-unitary "
            "frame changes. A deterministic state-independent Hermitian lift natural under the full product "
            "local-unitary action must lie in its commutant, which is the scalar center. Central generators "
            "are projectively null for PGRL."
        ),
    }
    controls = {
        "fixture": "SUPPLIED_FIVE_QUBIT_CARRIER_CONTROL_NOT_PROVENANCE_DERIVATION",
        "identity_invariance_error": identity_error,
        "noncentral_independent_frame_violation": noncentral_violation,
        "swap_independent_frame_violation": swap_independent_violation,
        "swap_tied_frame_error": swap_tied_error,
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
            raise ValueError("log candidate requires faithful local state")
        fvals = np.log(vals)
    else:
        raise ValueError(name)
    op = (vecs * fvals) @ vecs.conj().T
    op = 0.5 * (op + op.conj().T)
    return op - np.trace(op) / op.shape[0] * np.eye(op.shape[0], dtype=complex)


def graph_site_source(
    source: Sequence[float], local_states: Sequence[np.ndarray], function_name: str
) -> np.ndarray:
    P = np.zeros((32, 32), dtype=complex)
    for i, coeff in enumerate(source):
        P += float(coeff) * embed_site(matrix_function_centered(local_states[i], function_name), i)
    return 0.5 * (P + P.conj().T)


def _center_full(P: np.ndarray) -> np.ndarray:
    P = np.asarray(P, dtype=complex)
    return P - np.trace(P) / P.shape[0] * np.eye(P.shape[0], dtype=complex)


def projective_residual(P: np.ndarray, Q: np.ndarray) -> float:
    Pc, Qc = _center_full(P), _center_full(Q)
    nP, nQ = np.linalg.norm(Pc), np.linalg.norm(Qc)
    if nP < 1e-14 and nQ < 1e-14:
        return 0.0
    if min(nP, nQ) < 1e-14:
        return 1.0
    # Positive scaling only: do not identify antipodal rays.
    return float(np.linalg.norm(Pc / nP - Qc / nQ))


def _unitary_covariance_record(source: Sequence[float], states: Sequence[np.ndarray], fn: str) -> float:
    local_us = deterministic_local_unitaries()
    U = kron_all(local_us)
    base = graph_site_source(source, states, fn)
    transformed_states = [u @ rho @ u.conj().T for u, rho in zip(local_us, states)]
    rebuilt = graph_site_source(source, transformed_states, fn)
    target = U @ base @ U.conj().T
    denom = max(1.0, float(np.linalg.norm(target)))
    return float(np.linalg.norm(rebuilt - target) / denom)


def state_dependent_family_audit(source_fixture: dict[str, Any]) -> dict[str, Any]:
    source = tuple(float(x) for x in source_fixture["source"])
    controls: dict[str, Any] = {}
    max_covariance_error = 0.0
    max_scale_residual = 0.0
    max_hermiticity_error = 0.0
    max_trace_abs = 0.0
    all_pair_residuals: list[float] = []

    for control_name, radii in (("A", R_A), ("B", R_B)):
        states = [qubit_state(r) for r in radii]
        families: dict[str, np.ndarray] = {}
        family_records: dict[str, Any] = {}
        for fn in FUNCTIONS:
            P = graph_site_source(source, states, fn)
            families[fn] = P
            herm = float(np.linalg.norm(P - P.conj().T))
            trace_abs = abs(complex(np.trace(P)))
            max_hermiticity_error = max(max_hermiticity_error, herm)
            max_trace_abs = max(max_trace_abs, float(trace_abs))
            cov = _unitary_covariance_record(source, states, fn)
            max_covariance_error = max(max_covariance_error, cov)

            scale_residuals = []
            if fn != "identity":
                for scale in SCALES:
                    scaled = graph_site_source(tuple(scale * x for x in source), states, fn)
                    scale_residuals.append(projective_residual(P, scaled))
                max_scale_residual = max(max_scale_residual, max(scale_residuals, default=0.0))

            family_records[fn] = {
                "norm": float(np.linalg.norm(P)),
                "centered_norm": float(np.linalg.norm(_center_full(P))),
                "hermiticity_error": herm,
                "trace_abs": float(trace_abs),
                "covariance_error": cov,
                "max_positive_scale_projective_residual": max(scale_residuals, default=0.0),
            }

        pairwise: dict[str, float] = {}
        noncentral = ("linear", "square", "log")
        for i, a in enumerate(noncentral):
            for b in noncentral[i + 1 :]:
                residual = projective_residual(families[a], families[b])
                pairwise[f"{a}__{b}"] = residual
                all_pair_residuals.append(residual)

        controls[control_name] = {
            "bloch_radii": list(radii),
            "minimum_local_eigenvalue": min(float(np.min(np.linalg.eigvalsh(rho))) for rho in states),
            "families": family_records,
            "pairwise_projective_residuals": pairwise,
        }

    nonunique = any(x > 1e-8 for x in all_pair_residuals)
    family_status = (
        "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"
        if nonunique
        else "STATE_DEPENDENT_FROZEN_FAMILIES_PROJECTIVELY_EQUIVALENT"
    )

    B = incidence_matrix(source_fixture["nodes"], source_fixture["edges"])
    s = np.asarray(source, dtype=float)
    J = np.linalg.pinv(B) @ s
    current_balance = float(np.linalg.norm(B @ J - s))

    return {
        "classification": "SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION",
        "scientific_evidence_for_factorization": False,
        "candidate_functions": list(FUNCTIONS),
        "controls": controls,
        "constant_family_max_norm": max(
            controls[name]["families"]["identity"]["centered_norm"] for name in controls
        ),
        "max_covariance_error": max_covariance_error,
        "max_positive_scale_projective_residual": max_scale_residual,
        "max_hermiticity_error": max_hermiticity_error,
        "max_trace_abs": max_trace_abs,
        "max_pairwise_projective_residual": max(all_pair_residuals, default=0.0),
        "min_pairwise_projective_residual": min(all_pair_residuals, default=0.0),
        "family_status": family_status,
        "current_control": {
            "scientific_evidence": False,
            "classification": "MIN_NORM_CURRENT_CONTROL_NOT_PROVENANCE_SELECTED",
            "current": [float(x) for x in J],
            "balance_residual": current_balance,
        },
    }


def run_audit() -> dict[str, Any]:
    source_fixture = parse_source_fixture()
    archive = archive_graph_site_audit()
    dimension = dimension_factorization_audit()
    centrality_theorem, centrality = centrality_controls()
    state_dep = state_dependent_family_audit(source_fixture)

    numerical_failure = not (
        source_fixture["source_sum_abs"] < 1e-14
        and source_fixture["incidence_rank"] == 4
        and source_fixture["cycle_dimension"] == 3
        and centrality["identity_invariance_error"] < 2e-12
        and centrality["noncentral_independent_frame_violation"] > 1e-6
        and centrality["swap_independent_frame_violation"] > 1e-6
        and centrality["swap_tied_frame_error"] < 2e-12
        and state_dep["constant_family_max_norm"] < 2e-12
        and state_dep["max_covariance_error"] < 2e-10
        and state_dep["max_positive_scale_projective_residual"] < 2e-12
        and state_dep["max_hermiticity_error"] < 2e-12
        and state_dep["max_trace_abs"] < 2e-12
    )

    exact_factorization = archive["exact_graph_site_factorization_certified"]
    natural_map = archive["natural_map_to_compatibility_parent_certified"]
    state_nonunique = state_dep["family_status"] == "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"

    if numerical_failure:
        outcome = "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT"
    elif not exact_factorization:
        outcome = "NO_CERTIFIED_GRAPH_SITE_FACTORIZATION"
    elif exact_factorization and not natural_map:
        outcome = "GRAPH_SITE_CARRIER_NOT_COMPATIBILITY_PARENT"
    elif state_nonunique:
        outcome = "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"
    else:
        # Reaching here would still require a unique noncentral law from the frozen archive.
        outcome = "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT"

    breakthrough = outcome == "GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY"
    return {
        "version": "v15.03",
        "title": "Graph-Site Factorization / Local-Gauge Source Lift Gate",
        "source_fixture": source_fixture,
        "archive_graph_site_audit": archive,
        "dimension_theorem": dimension,
        "centrality_theorem": centrality_theorem,
        "centrality_controls": centrality,
        "state_dependent_controls": state_dep,
        "gate_outcome": outcome,
        "secondary_statuses": [
            centrality_theorem["pgrl_classification"],
            state_dep["family_status"],
            dimension["classification"],
            archive["carrier_status"],
        ],
        "scientific_breakthrough": breakthrough,
        "Pillar_3": "OPEN",
        "claim_scope": (
            "graph-site quantum factorization, independent local-gauge source-lift naturality, "
            "state-dependent covariant source-family canonicality, and carrier relevance to the certified C^125 parent"
        ),
        "interpretation": (
            "Frozen UQCF-GEM artifacts contain graph-indexed quantum models and independent local-frame covariance, "
            "but do not certify identity of the exact retained five-node source graph with five nontrivial quantum "
            "tensor factors. Independently, scalar/current graph data alone cannot select a noncentral state-independent "
            "operator under full independent local gauge: the commutant is central and PGRL-null. Supplied state context "
            "does permit noncentral covariant functional-calculus lifts; their measured projective canonicality is reported "
            "separately. Any genuine five-site carrier is also arithmetically distinct from the certified C^125 parent and "
            "requires an earned natural cross-carrier map."
        ),
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
        "stop_rule": (
            "Do not choose a Pauli axis, privilege log(rho), tie local frames, invent a cross-carrier isometry, "
            "promote a min-norm current, use pruning/entropy as a pre-pruning selector, or use ADM/Einstein/gravity residuals."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
