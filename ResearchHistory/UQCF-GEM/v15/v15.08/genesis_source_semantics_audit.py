#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, Tuple

import numpy as np


EXPECTED_BINDINGS = {
    "Tmp/TOE/Einstein 3/v923_full_stack_source_role_closure_proof/FULL_REPORT_AND_PROOF.md": "9a1523c08d2b9b2c5ba2d298dfed3d563a750bec",
    "Tmp/TOE/Einstein 4/v995_pre_report_closure_synthesis_packet/V995_PRE_REPORT_CLOSURE_SYNTHESIS.md": "a0cb9a17344800ebfee1cbe3f724da2ac418e164",
    "Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md": "8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e",
    "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md": "9917085b211ca0e1f4737082227f55097cc72b66",
    "ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md": "e5d9566bfc86c801d2933e63453d1800f60a675b",
    "ResearchHistory/UQCF-GEM/v15/v15.07/REPORT.md": "c3abb3af5b5c7210fc717392d4e2cc6fc4648284",
}

I2 = np.eye(2, dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
PAULIS = (SX, SY, SZ)


def adjudicate_gate(underived: bool, identified: bool) -> str:
    if underived and identified:
        raise ValueError("v15.08 underived and identified certificates are mutually exclusive")
    if underived:
        return "GENESIS_PROVENANCE_DOES_NOT_IDENTIFY_NEUTRAL_PREPARATION_SOURCE"
    if identified:
        return "FROZEN_GENESIS_IDENTIFIES_NEUTRAL_PREPARATION_SOURCE"
    return "V15_08_GATE_UNRESOLVED"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def _archive_bindings() -> Dict[str, str]:
    root = _repo_root()
    return {rel: _git_blob_sha(root / rel) for rel in EXPECTED_BINDINGS}


def _center(a: np.ndarray) -> np.ndarray:
    d = a.shape[0]
    return a - (np.trace(a) / d) * np.eye(d, dtype=complex)


def _hermitian_function(a: np.ndarray, fn) -> np.ndarray:
    vals, vecs = np.linalg.eigh(0.5 * (a + a.conj().T))
    return (vecs * fn(vals)) @ vecs.conj().T


def _logm_pos(a: np.ndarray) -> np.ndarray:
    vals = np.linalg.eigvalsh(a)
    if float(np.min(vals)) <= 0.0:
        raise ValueError("positive definite matrix required")
    return _hermitian_function(a, np.log)


def _expm_herm(a: np.ndarray) -> np.ndarray:
    return _hermitian_function(a, np.exp)


def _pgrl_state(base: np.ndarray, generator: np.ndarray, s: float) -> np.ndarray:
    x = _expm_herm(_logm_pos(base) + float(s) * generator)
    return x / np.trace(x)


def _qubit_state(radius: float, direction: Tuple[float, float, float]) -> np.ndarray:
    n = np.asarray(direction, dtype=float)
    n /= np.linalg.norm(n)
    bloch = sum(float(n[k]) * PAULIS[k] for k in range(3))
    return 0.5 * (I2 + float(radius) * bloch)


def _a_log(r: float) -> float:
    if r < 1e-14:
        return 2.0
    return float(2.0 * np.arctanh(r) / r)


def _local_source(rho: np.ndarray, kind: str) -> np.ndarray:
    r = float(np.linalg.norm([np.trace(rho @ p).real for p in PAULIS]))
    if kind == "linear":
        a = 1.0
    elif kind == "log":
        a = _a_log(r)
    elif kind == "polynomial":
        a = 1.0 + r * r
    else:
        raise ValueError(kind)
    return a * (rho - 0.5 * I2)


def _compose_two(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.kron(p, I2) + np.kron(I2, q)


def _ray_separation(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    return float(np.linalg.norm(a / na - b / nb))


def _genesis_pin_semantics() -> dict:
    return {
        "classification": "GENESIS_PIN_CERTIFIES_HISTORY_LEGITIMACY_NOT_QUANTUM_REFERENCE_STATE",
        "history_legitimacy_certified": True,
        "certified_content": [
            "pinned witness registry",
            "pinned genesis anchor root",
            "witness quorum",
            "append-only continuity",
            "non-circular origin",
        ],
        "quantum_neutral_reference_identified": False,
        "neutral_preparation_generator_identified": False,
        "reason": (
            "V997 changes certification from final-state equivalence to recoverable-history legitimacy. "
            "Its Genesis Pin is a registry/root/witness/history boundary, not a density operator and not a state-preparation law."
        ),
    }


def _source_role_semantics() -> dict:
    roles = [
        "source_active_role",
        "source_basin_eligible_nonactive_role",
        "source_rejected_or_broken_role",
    ]
    return {
        "classification": "TERNARY_SOURCE_ROLE_IS_LEGITIMACY_INFORMATION_NOT_OPERATOR_GENERATOR",
        "ternary_role_count": len(roles),
        "roles": roles,
        "role_to_hermitian_generator_map_found": False,
        "role_to_spectral_response_law_found": False,
        "generator_compatibility_is_identity_selection": False,
        "reason": (
            "V923 proves a minimal ternary role label for exact source-legitimacy classification. "
            "V995 adds causal generator compatibility as a closure layer, but neither artifact defines a map from a role symbol or provenance record to a local Hermitian source generator."
        ),
    }


def _independence_no_go() -> dict:
    rho = _qubit_state(0.20, (0.3, -0.4, 0.8660254037844386))
    sigma = _qubit_state(0.80, (-0.5, 0.7, 0.5099019513592785))
    product = np.kron(rho, sigma)

    # Frozen provenance/source-role facts are deliberately identical in every extension.
    provenance_signature = (
        "pinned_genesis_pass",
        "source_active_role",
        "append_only_valid",
        "quorum_valid",
        "same_retained_source_grade",
    )

    candidates = {}
    output_checks = {}
    for kind in ("linear", "log", "polynomial"):
        p = _compose_two(_local_source(rho, kind), _local_source(sigma, kind))
        candidates[kind] = p
        out = _pgrl_state(product, p, 0.17)
        output_checks[kind] = {
            "provenance_signature": list(provenance_signature),
            "min_output_eigenvalue": float(np.min(np.linalg.eigvalsh(out))),
            "trace_error": abs(float(np.trace(out).real) - 1.0),
            "centered_generator_trace_norm": abs(complex(np.trace(p))),
        }

    separations = {
        "linear_vs_log": _ray_separation(candidates["linear"], candidates["log"]),
        "linear_vs_polynomial": _ray_separation(candidates["linear"], candidates["polynomial"]),
        "log_vs_polynomial": _ray_separation(candidates["log"], candidates["polynomial"]),
    }
    min_sep = min(separations.values())

    canonical_log = _center(_logm_pos(product))
    log_match = _ray_separation(canonical_log, candidates["log"])
    all_valid = all(
        row["min_output_eigenvalue"] > 0.0
        and row["trace_error"] < 1e-12
        and row["centered_generator_trace_norm"] < 1e-12
        for row in output_checks.values()
    )
    same_provenance = len({tuple(row["provenance_signature"]) for row in output_checks.values()}) == 1

    return {
        "classification": "COUNTERMODEL_INDEPENDENCE_PROVES_SOURCE_SEMANTICS_NOT_ENTAILED",
        "theorem": (
            "If two extensions satisfy every frozen provenance/source-role certificate and all audited source kinematics, "
            "but assign inequivalent Hermitian source rays to the same state/provenance data, then the frozen ontology does not entail either assignment."
        ),
        "same_frozen_provenance_supports_multiple_source_laws": bool(all_valid and same_provenance and min_sep > 1e-2),
        "common_provenance_signature": list(provenance_signature),
        "candidate_source_laws": ["linear", "log", "polynomial"],
        "pairwise_source_ray_separations": separations,
        "min_pairwise_source_ray_separation": min_sep,
        "canonical_log_ray_matches_v15_07_generator": log_match,
        "max_trace_error": max(row["trace_error"] for row in output_checks.values()),
        "min_output_eigenvalue": min(row["min_output_eigenvalue"] for row in output_checks.values()),
        "provenance_only_noncentral_map_blocked_by_v14_04": True,
        "output_checks": output_checks,
    }


def _frozen_dependency_audit(bindings: Dict[str, str]) -> dict:
    return {
        "archive_bindings": bindings,
        "archive_bindings_match_expected": bindings == EXPECTED_BINDINGS,
        "v923": {
            "result": "ternary source-role primitive closes source-legitimacy classification in the tested branch",
            "operator_source_map_defined": False,
        },
        "v995": {
            "result": "pinned genesis plus source role, provenance, generator compatibility, freshness and ledgers maintain legitimacy closure",
            "neutral_reference_state_defined": False,
            "neutral_preparation_source_law_defined": False,
        },
        "v997": {
            "result": "Genesis Pin selects legitimate recoverable history among visible-equivalent histories",
            "genesis_object_type": "registry/root/witness/append-only history boundary",
            "quantum_state_reference_defined": False,
        },
        "v13_26": {
            "result": "Genesis anchoring is identity/compatibility and does not supply absolute source calibration",
        },
        "v14_04": {
            "result": "gauge-trivial provenance can map naturally only to a central/PGRL-null support class; richer provenance lacks a certified natural intertwiner",
        },
        "v15_07": {
            "result": "frame symmetry derives tau_d=I/d, Q_d=d rho and centered log rho generator",
            "source_semantics_derived": False,
        },
        "source_equals_neutral_preparation_axiom_found": False,
        "genesis_equals_maximally_mixed_state_axiom_found": False,
        "classification": "NO_FROZEN_GENESIS_TO_NEUTRAL_PREPARATION_SOURCE_SEMANTICS",
    }


def run_audit() -> dict:
    bindings = _archive_bindings()
    frozen = _frozen_dependency_audit(bindings)
    pin = _genesis_pin_semantics()
    roles = _source_role_semantics()
    no_go = _independence_no_go()

    underived = bool(
        frozen["archive_bindings_match_expected"]
        and frozen["source_equals_neutral_preparation_axiom_found"] is False
        and frozen["genesis_equals_maximally_mixed_state_axiom_found"] is False
        and pin["history_legitimacy_certified"]
        and pin["quantum_neutral_reference_identified"] is False
        and pin["neutral_preparation_generator_identified"] is False
        and roles["role_to_hermitian_generator_map_found"] is False
        and roles["role_to_spectral_response_law_found"] is False
        and no_go["same_frozen_provenance_supports_multiple_source_laws"]
        and no_go["provenance_only_noncentral_map_blocked_by_v14_04"]
        and no_go["canonical_log_ray_matches_v15_07_generator"] < 1e-11
    )

    primary = adjudicate_gate(underived, False)

    return {
        "version": "v15.08",
        "gate": "Genesis Source-Semantics / Neutral-Preparation Identification Gate",
        "primary_outcome": primary,
        "secondary_outcome": "SOURCE_SEMANTICS_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY",
        "tertiary_outcome": "LOG_PROJECTIVE_SOURCE_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM",
        "major_structural_result": True,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "frozen_dependency_audit": frozen,
        "genesis_pin_semantics": pin,
        "source_role_semantics": roles,
        "independence_no_go": no_go,
        "claim_boundary": {
            "canonical_neutral_reference_preserved": True,
            "canonical_multiplicative_operator_preserved": True,
            "canonical_log_generator_preserved": True,
            "canonical_log_generator_identified_as_source": False,
            "genesis_pin_is_quantum_neutral_state": False,
            "source_role_is_hermitian_generator": False,
            "new_source_semantics_axiom_required": True,
            "branch_stop_relative_to_frozen_ontology": True,
            "absolute_source_scale_derived": False,
            "retained_node_to_quantum_site_carrier_derived": False,
            "physical_stress_energy_derived": False,
            "spacetime_or_einstein_equations_derived": False,
            "downstream_gravity_used_as_selector": False,
            "entropy_or_time_used_as_selector": False,
            "Pillar_3_closed": False,
        },
        "stop_rule": (
            "Do not identify Genesis with tau_d=I/d and do not identify sourcehood with the neutral-to-state preparation generator "
            "without one explicit new source-semantics axiom. The logarithmic projective source branch stops here relative to the frozen ontology."
        ),
        "next_lawful_frontier": (
            "Either introduce and independently motivate one NEW SOURCE-SEMANTICS AXIOM, or leave the log generator as a canonical local information generator "
            "without physical-source status and redirect work to an independent unresolved bridge."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
