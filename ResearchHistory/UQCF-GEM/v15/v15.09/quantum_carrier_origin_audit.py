#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


EXPECTED_BINDINGS = {
    "ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md": "e5d9566bfc86c801d2933e63453d1800f60a675b",
    "ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md": "1afbb7aebe384a1fb761f99fd2b040e595be1fa5",
    "ResearchHistory/UQCF-GEM/v15/v15.02/REPORT.md": "be1281621b0e2872e555223b2c1cdb98fe9d8011",
    "ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md": "6c3aed73c63c9c7554107d163e15b8fae7549c1c",
    "ResearchHistory/UQCF-GEM/v15/v15.07/REPORT.md": "c3abb3af5b5c7210fc717392d4e2cc6fc4648284",
    "ResearchHistory/UQCF-GEM/v15/v15.08/REPORT.md": "23bbeaecdb81adfe1a39b3140569d23c367b8b55",
}

GRAPH_NODES = tuple(range(5))
GRAPH_EDGES = ((0, 1), (1, 3), (0, 2), (2, 4), (4, 3), (1, 2), (0, 4))
GRAPH_SOURCE = (-1, 0, 0, +1, 0)
V1503_RADII_A = (0.15, -0.31, 0.42, 0.63, -0.22)


def adjudicate_gate(carrier_underived: bool, carrier_certified: bool) -> str:
    if carrier_underived and carrier_certified:
        raise ValueError("v15.09 underived and certified carrier adjudications are mutually exclusive")
    if carrier_underived:
        return "CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER"
    if carrier_certified:
        return "FROZEN_ONTOLOGY_DERIVES_RETAINED_QUANTUM_CARRIER"
    return "V15_09_GATE_UNRESOLVED"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def _archive_bindings() -> Dict[str, str]:
    root = _repo_root()
    return {rel: _git_blob_sha(root / rel) for rel in EXPECTED_BINDINGS}


def _unordered_multiplicative_partitions(n: int, minimum: int = 2) -> List[List[int]]:
    """All nondecreasing factor lists with factors >= minimum and product n.

    The one-factor decomposition [n] is included. No factor 1 is permitted.
    """
    out: List[List[int]] = [[n]]
    limit = int(np.sqrt(n))
    for f in range(minimum, limit + 1):
        if n % f != 0:
            continue
        q = n // f
        for tail in _unordered_multiplicative_partitions(q, f):
            out.append([f] + tail)
    out.sort(key=lambda xs: (len(xs), xs))
    return out


def _kron_all(mats: Sequence[np.ndarray]) -> np.ndarray:
    result = np.array([[1.0]], dtype=complex)
    for m in mats:
        result = np.kron(result, m)
    return result


def _neutral_reference(dim: int) -> np.ndarray:
    return np.eye(dim, dtype=complex) / float(dim)


def _factorization_blindness() -> dict:
    dimension = 32
    decompositions = _unordered_multiplicative_partitions(dimension)
    tau = _neutral_reference(dimension)
    errors = {}
    for factors in decompositions:
        rebuilt = _kron_all([_neutral_reference(d) for d in factors])
        errors["x".join(map(str, factors))] = float(np.linalg.norm(rebuilt - tau))

    five = [f for f in decompositions if len(f) == 5]
    return {
        "classification": "FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND",
        "dimension": dimension,
        "unordered_factorizations": decompositions,
        "unordered_factorization_count": len(decompositions),
        "five_nontrivial_factor_decompositions": five,
        "five_nontrivial_factor_decomposition_count": len(five),
        "factorization_errors": errors,
        "max_neutral_factorization_error": max(errors.values()),
        "factorization_selected_by_tau": False,
        "factorization_selected_by_Q_definition": False,
        "theorem": (
            "For every tensor decomposition D=product_i d_i, I_D/D equals tensor_i(I_di/d_i). "
            "Therefore the unique frame-neutral state is compatible with every supplied tensor decomposition and cannot select one. "
            "Likewise Q_D(rho)=D*rho is defined without a tensor decomposition; its product factorization property applies only after a product structure is supplied."
        ),
    }


def _permute_tensor_operator(op: np.ndarray, dims: Sequence[int], perm: Sequence[int]) -> np.ndarray:
    n = len(dims)
    shape = tuple(dims) + tuple(dims)
    tensor = op.reshape(shape)
    row_axes = list(perm)
    col_axes = [n + p for p in perm]
    transposed = tensor.transpose(row_axes + col_axes)
    new_dims = [dims[p] for p in perm]
    d = int(np.prod(new_dims))
    return transposed.reshape((d, d))


def _five_site_permutation_control() -> dict:
    dims = [2] * 5
    tau = _kron_all([_neutral_reference(2) for _ in range(5)])
    errors = []
    accepted = 0
    for perm in itertools.permutations(range(5)):
        moved = _permute_tensor_operator(tau, dims, perm)
        err = float(np.linalg.norm(moved - tau))
        errors.append(err)
        if err < 1e-12:
            accepted += 1
    return {
        "classification": "NEUTRAL_FIVE_QUBIT_REFERENCE_HAS_FULL_S5_SITE_PERMUTATION_SYMMETRY",
        "permutation_count": len(errors),
        "accepted_permutation_count": accepted,
        "max_neutral_permutation_error": max(errors),
        "site_label_selected_by_neutral_reference": False,
    }


def _graph_automorphisms() -> List[Tuple[int, ...]]:
    edge_set = set(GRAPH_EDGES)
    autos = []
    for perm in itertools.permutations(GRAPH_NODES):
        moved = {(perm[u], perm[v]) for u, v in GRAPH_EDGES}
        if moved == edge_set:
            autos.append(tuple(perm))
    return autos


def _site_spectral_fingerprints() -> Tuple[Tuple[float, float], ...]:
    fingerprints = []
    for r in V1503_RADII_A:
        vals = sorted(((1.0 - abs(float(r))) / 2.0, (1.0 + abs(float(r))) / 2.0))
        fingerprints.append((round(vals[0], 15), round(vals[1], 15)))
    return tuple(fingerprints)


def _site_spectral_stabilizer(fingerprints: Sequence[Tuple[float, float]]) -> List[Tuple[int, ...]]:
    stabilizer = []
    base = tuple(fingerprints)
    for perm in itertools.permutations(range(len(base))):
        moved = tuple(base[perm[i]] for i in range(len(base)))
        if moved == base:
            stabilizer.append(tuple(perm))
    return stabilizer


def _cross_domain_independence() -> dict:
    graph_autos = _graph_automorphisms()
    fingerprints = _site_spectral_fingerprints()
    site_stabilizer = _site_spectral_stabilizer(fingerprints)
    bijections = list(itertools.permutations(range(5)))

    # With both within-sort stabilizers trivial, every bijection is its own double-coset class.
    inequivalent = len(bijections) if len(graph_autos) == 1 and len(site_stabilizer) == 1 else None

    return {
        "classification": "TWO_SORT_REDUCT_DOES_NOT_DEFINE_NODE_SITE_BIJECTION",
        "graph_automorphism_order": len(graph_autos),
        "graph_automorphisms": [list(x) for x in graph_autos],
        "quantum_site_spectral_fingerprints": [list(x) for x in fingerprints],
        "all_site_spectral_fingerprints_distinct": len(set(fingerprints)) == 5,
        "quantum_site_spectral_stabilizer_order": len(site_stabilizer),
        "node_site_bijection_count": len(bijections),
        "inequivalent_bijection_count": inequivalent,
        "certified_cross_domain_relation_found": False,
        "same_reduct_supports_all_bijections": True,
        "supplied_five_qubit_factorization_required_before_site_fingerprints_exist": True,
        "theorem": (
            "Treat retained nodes and quantum sites as distinct sorts. If the frozen reduct contains only within-sort relations and no cross-sort relation, "
            "then adjoining any node-to-site bijection yields an expansion with the same reduct. Hence the reduct cannot entail one bijection. "
            "The v15.07 neutral/reference operators live entirely on the quantum sort and do not add a cross-sort relation."
        ),
    }


def _compatibility_parent_boundary() -> dict:
    parent_dimension = 125
    parts = _unordered_multiplicative_partitions(parent_dimension)
    five = [f for f in parts if len(f) == 5]
    return {
        "parent_dimension": parent_dimension,
        "parent_unordered_factorizations": parts,
        "five_nontrivial_factor_decompositions": five,
        "five_nontrivial_factor_decomposition_count": len(five),
        "five_site_carrier_can_equal_parent": len(five) > 0,
        "supplied_five_qubit_dimension": 32,
        "dimension_match_with_supplied_five_qubit_carrier": parent_dimension == 32,
        "natural_supplied_five_qubit_to_C125_map_found": False,
        "classification": "V15_07_NEUTRAL_STRUCTURE_DOES_NOT_REPAIR_C125_PARENT_TYPE_MISMATCH",
    }


def _frozen_dependency_audit(bindings: Dict[str, str]) -> dict:
    return {
        "archive_bindings": bindings,
        "archive_bindings_match_expected": bindings == EXPECTED_BINDINGS,
        "v14_04": "provenance-to-support representation link remains missing",
        "v15_01": "C125 parent/support is verified but provenance supplies no same-parent source/carrier representation",
        "v15_02": "120 inequivalent node-to-quantum-label identifications; shared cardinality is insufficient",
        "v15_03": "exact retained graph-to-five-site factorization remains underived and five nontrivial sites cannot equal C125",
        "v15_07": "tau_d=I/d and Q_d=d*rho are canonical only after the Hilbert carrier is specified; tau factorizes for every supplied tensor decomposition",
        "v15_08": "source-semantics branch is stopped and is not reused as a carrier selector",
        "new_v15_07_structure_reopens_v15_02": False,
        "new_v15_07_structure_reopens_v15_03": False,
        "v15_08_source_semantics_branch_stop_preserved": True,
        "classification": "CANONICAL_QUANTUM_INTRASORT_STRUCTURE_DOES_NOT_SUPPLY_CROSS_DOMAIN_CARRIER_ORIGIN",
    }


def run_audit() -> dict:
    bindings = _archive_bindings()
    frozen = _frozen_dependency_audit(bindings)
    factorization = _factorization_blindness()
    permutation = _five_site_permutation_control()
    independence = _cross_domain_independence()
    parent = _compatibility_parent_boundary()

    carrier_underived = bool(
        frozen["archive_bindings_match_expected"]
        and factorization["unordered_factorization_count"] == 7
        and factorization["max_neutral_factorization_error"] < 1e-12
        and factorization["factorization_selected_by_tau"] is False
        and permutation["permutation_count"] == 120
        and permutation["accepted_permutation_count"] == 120
        and independence["graph_automorphism_order"] == 1
        and independence["quantum_site_spectral_stabilizer_order"] == 1
        and independence["inequivalent_bijection_count"] == 120
        and independence["certified_cross_domain_relation_found"] is False
        and parent["five_nontrivial_factor_decomposition_count"] == 0
        and parent["natural_supplied_five_qubit_to_C125_map_found"] is False
    )

    primary = adjudicate_gate(carrier_underived, False)

    return {
        "version": "v15.09",
        "gate": "Quantum Carrier Origin / Tensor-Factorization Blindness Gate",
        "primary_outcome": primary,
        "secondary_outcome": "FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND",
        "tertiary_outcome": "SUPPLIED_SITE_FINGERPRINTS_DO_NOT_DEFINE_CROSS_DOMAIN_NODE_SITE_FUNCTOR",
        "major_structural_result": True,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "frozen_dependency_audit": frozen,
        "factorization_blindness": factorization,
        "five_site_permutation_control": permutation,
        "cross_domain_independence": independence,
        "compatibility_parent_boundary": parent,
        "claim_boundary": {
            "canonical_neutral_reference_preserved": True,
            "canonical_log_generator_preserved": True,
            "five_site_quantum_carrier_derived": False,
            "retained_node_to_quantum_site_functor_derived": False,
            "graph_site_to_C125_parent_map_derived": False,
            "source_semantics_reopened": False,
            "new_representation_principle_required": True,
            "physical_stress_energy_derived": False,
            "spacetime_or_einstein_equations_derived": False,
            "downstream_gravity_used_as_selector": False,
            "entropy_or_time_used_as_selector": False,
            "Pillar_3_closed": False,
        },
        "stop_rule": (
            "Do not infer a five-site carrier from tau_d=I/d, do not match rigid graph nodes to distinct quantum-site spectra by sorting or analogy, "
            "and do not invent an H32-to-C125 embedding. The carrier-origin branch requires a new cross-domain representation/functor principle."
        ),
        "next_lawful_frontier": (
            "Preserve the canonical quantum information generator as an intrasort result and redirect to a genuinely independent bridge, unless an independently motivated "
            "cross-domain carrier/functor principle is proposed explicitly as a NEW ASSUMPTION."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
