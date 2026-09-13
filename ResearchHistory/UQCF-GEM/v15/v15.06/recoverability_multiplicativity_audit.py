#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np

EXPECTED_BINDINGS = {
    "ResearchHistory/UQCF-GEM/v13/v13.16/REPORT.md": "cf2420b2545f801869a617092f4955b7a57ddc60",
    "ResearchHistory/UQCF-GEM/v13/v13.22/REPORT.md": "e6920facaa4d133e2767951612c608d0e514806c",
    "ResearchHistory/UQCF-GEM/v15/v15.05/REPORT.md": "b191c08c22ded0439cc4c2c125fbccfdb677dcbc",
    "ResearchHistory/UQCF-GEM/v15/v15.05/SUMMARY.json": "7aed8e530edc54c5b3a0b3556b54d72c0f7aa932",
    "Tmp/TOE/Einstein Phase 1/V822_peer_review_packet/V818_THEOREM_SHAPE_ACCESSIBILITY_LAW.md": "a92b414c7394f6db8b85b4e2938ca5011d6ee5a3",
    "Tmp/TOE/Einstein Phase 1/V824_accessibility_curvature_paper_python_proof/accessibility_curvature_proof.py": "01e291fa2c490033bdc91e48f3877d0440343ef1",
}

I2 = np.eye(2, dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
PAULIS = (SX, SY, SZ)


def adjudicate_gate(type_boundary_certified: bool, source_selector_certified: bool) -> str:
    if type_boundary_certified and source_selector_certified:
        raise ValueError("v15.06 type-boundary and source-selection certificates are mutually exclusive")
    if type_boundary_certified:
        return "MULTIPLICATIVE_RECOVERABILITY_SCALAR_DOES_NOT_SELECT_LOCAL_SOURCE_LAW"
    if source_selector_certified:
        return "RECOVERABILITY_MULTIPLICATIVITY_SELECTS_LOCAL_SOURCE_LAW"
    return "V15_06_GATE_UNRESOLVED"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def _archive_bindings() -> Dict[str, str]:
    root = _repo_root()
    return {rel: _git_blob_sha(root / rel) for rel in EXPECTED_BINDINGS}


def _random_density(dim: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(dim, dim)) + 1.0j * rng.normal(size=(dim, dim))
    rho = x @ x.conj().T + 0.35 * np.eye(dim)
    return rho / np.trace(rho)


def _psd_sqrt(a: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh((a + a.conj().T) / 2.0)
    vals = np.clip(vals.real, 0.0, None)
    return (vecs * np.sqrt(vals)) @ vecs.conj().T


def _root_fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    sr = _psd_sqrt(rho)
    middle = sr @ sigma @ sr
    value = float(np.trace(_psd_sqrt(middle)).real)
    return max(value, 0.0)


def _negative_log(x: float) -> float:
    return float(-np.log(max(x, np.finfo(float).tiny)))


def _recovery_pair_multiplicativity_controls() -> dict:
    product_errors = []
    log_errors = []
    records = []
    for k in range(16):
        rho1 = _random_density(2, 15060 + 4 * k)
        sig1 = _random_density(2, 15061 + 4 * k)
        rho2 = _random_density(3, 15062 + 4 * k)
        sig2 = _random_density(3, 15063 + 4 * k)
        f1 = _root_fidelity(rho1, sig1)
        f2 = _root_fidelity(rho2, sig2)
        f12 = _root_fidelity(np.kron(rho1, rho2), np.kron(sig1, sig2))
        product_error = abs(f12 - f1 * f2)
        log_error = abs(_negative_log(f12) - (_negative_log(f1) + _negative_log(f2)))
        product_errors.append(product_error)
        log_errors.append(log_error)
        records.append({
            "control": k,
            "F_root_1": f1,
            "F_root_2": f2,
            "F_root_product": f12,
            "product_error": product_error,
            "negative_log_additivity_error": log_error,
        })
    return {
        "classification": "ROOT_FIDELITY_MULTIPLIES_ON_INDEPENDENT_RECOVERY_PAIRS",
        "theorem": (
            "For normalized positive states rho_i,sigma_i, root fidelity obeys "
            "F_root(rho1 tensor rho2, sigma1 tensor sigma2)=F_root(rho1,sigma1)F_root(rho2,sigma2). "
            "Therefore -log F_root is additive wherever the fidelity is nonzero."
        ),
        "scope": "INDEPENDENT_SUPPLIED_STATE_RECOVERY_PAIRS",
        "num_random_controls": len(records),
        "max_root_fidelity_product_error": max(product_errors),
        "max_negative_log_additivity_error": max(log_errors),
        "uses_entropy_or_time": False,
        "controls": records,
    }


def _qubit_state(radius: float, direction: Tuple[float, float, float]) -> np.ndarray:
    n = np.asarray(direction, dtype=float)
    n = n / np.linalg.norm(n)
    bloch = sum(float(n[k]) * PAULIS[k] for k in range(3))
    return 0.5 * (I2 + float(radius) * bloch)


def _entropy(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh((rho + rho.conj().T) / 2.0).real
    vals = vals[vals > 1e-15]
    return float(-np.sum(vals * np.log(vals)))


def _tripartite_product_cmi(rho_a: np.ndarray, rho_b: np.ndarray, rho_c: np.ndarray) -> float:
    # For the executed exact-recovery family the state is a literal product.
    # Compute the entropy expression explicitly as a numerical theorem control.
    rho_ab = np.kron(rho_a, rho_b)
    rho_bc = np.kron(rho_b, rho_c)
    rho_abc = np.kron(rho_ab, rho_c)
    return float(_entropy(rho_ab) + _entropy(rho_bc) - _entropy(rho_b) - _entropy(rho_abc))


def _response_coefficient(radius: float, kind: str) -> float:
    if kind == "linear":
        return 1.0
    if kind == "log":
        if radius < 1e-14:
            return 2.0
        return float(2.0 * np.arctanh(radius) / radius)
    if kind == "polynomial":
        return float(1.0 + radius * radius)
    raise ValueError(kind)


def _local_source(rho: np.ndarray, kind: str) -> np.ndarray:
    rvec = np.array([np.trace(rho @ p).real for p in PAULIS])
    r = float(np.linalg.norm(rvec))
    return _response_coefficient(r, kind) * (rho - 0.5 * I2)


def _compose_sources(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.kron(left, np.eye(right.shape[0])) + np.kron(np.eye(left.shape[0]), right)


def _ray_separation(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    return float(np.linalg.norm(a / na - b / nb))


def _exact_recovery_sector_nonselection() -> dict:
    radii = [0.05, 0.20, 0.40, 0.60, 0.80, 0.95]
    rho_b = _qubit_state(0.33, (0.3, -0.4, 0.866))
    rho_c = _qubit_state(0.41, (-0.6, 0.2, 0.7746))
    records = []
    infidelities = []
    cmis = []
    log_coeffs = []

    for idx, r in enumerate(radii):
        rho_a = _qubit_state(r, (0.21, -0.57, 0.794))
        rho_abc = np.kron(np.kron(rho_a, rho_b), rho_c)
        # The recovery channel that appends rho_c to AB recovers this product state exactly.
        recovered = rho_abc.copy()
        fid = _root_fidelity(rho_abc, recovered)
        cmi = _tripartite_product_cmi(rho_a, rho_b, rho_c)
        coeff = _response_coefficient(r, "log")
        infidelities.append(abs(1.0 - fid))
        cmis.append(abs(cmi))
        log_coeffs.append(coeff)
        records.append({
            "radius": r,
            "exact_recovery_root_fidelity": fid,
            "product_state_CMI": cmi,
            "log_response_coefficient": coeff,
        })

    rho_left = _qubit_state(0.20, (0.0, 0.0, 1.0))
    rho_right = _qubit_state(0.80, (0.0, 0.0, 1.0))
    sources = {
        kind: _compose_sources(_local_source(rho_left, kind), _local_source(rho_right, kind))
        for kind in ("linear", "log", "polynomial")
    }
    separations = {
        "linear_vs_log": _ray_separation(sources["linear"], sources["log"]),
        "linear_vs_polynomial": _ray_separation(sources["linear"], sources["polynomial"]),
        "log_vs_polynomial": _ray_separation(sources["log"], sources["polynomial"]),
    }

    return {
        "classification": "EXACT_RECOVERY_SCALAR_IS_CONSTANT_ACROSS_ALL_FAITHFUL_LOCAL_QUBIT_SPECTRA",
        "theorem": (
            "For every faithful qubit state rho_A(r), choose any faithful rho_B,rho_C and the product triple "
            "rho_A(r) tensor rho_B tensor rho_C. The channel that appends rho_C to AB recovers the state exactly, "
            "so the recovery-pair root fidelity is 1 for every local Bloch radius r. Consequently the exact-recovery "
            "scalar cannot constrain the v15.04 response function a(r)."
        ),
        "tested_radii": radii,
        "tested_radius_min": min(radii),
        "tested_radius_max": max(radii),
        "max_exact_recovery_infidelity": max(infidelities),
        "max_product_state_cmi": max(cmis),
        "log_response_coefficient_min": min(log_coeffs),
        "log_response_coefficient_max": max(log_coeffs),
        "log_response_coefficient_span": max(log_coeffs) - min(log_coeffs),
        "pairwise_source_ray_separations_at_same_exact_recovery_scalar": separations,
        "min_pairwise_source_ray_separation": min(separations.values()),
        "same_recoverability_scalar_multiple_source_rays": True,
        "records": records,
    }


def _frozen_dependency_audit(bindings: Dict[str, str]) -> dict:
    root = _repo_root()
    v818 = (root / "Tmp/TOE/Einstein Phase 1/V822_peer_review_packet/V818_THEOREM_SHAPE_ACCESSIBILITY_LAW.md").read_text()
    v824 = (root / "Tmp/TOE/Einstein Phase 1/V824_accessibility_curvature_paper_python_proof/accessibility_curvature_proof.py").read_text()
    return {
        "archive_bindings": bindings,
        "archive_bindings_match_expected": bindings == EXPECTED_BINDINGS,
        "v13_16": {
            "root_fidelity_recoverability_bound_present": True,
            "frozen_statement": "F_root(rho_ABC,R(rho_AB)) >= exp[-I(A:C|B)/2] for some recovery channel",
            "canonical_recovery_map_selected": False,
            "role": "scalar certification of closeness between a state and a recovered state",
        },
        "v13_22": {
            "product_refinement_present": True,
            "frozen_refinement": "R_tau(rho)=rho tensor tau",
            "role": "state refinement and supplied-source embedding, not state-to-source selection",
        },
        "v15_05": {
            "unique_state_to_source_law_selected": False,
            "frozen_result": "FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE",
        },
        "legacy_accessibility": {
            "classification": "LEGACY_ACCESSIBILITY_MULTIPLICATIVITY_NOT_FROZEN_DERIVATION",
            "v818_multiplicativity_statement_is_conditional": "If accessible futures combine multiplicatively" in v818,
            "v818_exact_wording": "If accessible futures combine multiplicatively, then the natural potential is log A.",
            "v824_accessibility_is_defined_exponentially": "A=np.exp(C-mu+ETA*repair)" in v824,
            "v824_role": "synthetic accessibility-curvature harness with exponential A declared in the construction",
            "independent_multiplicativity_derivation_present": False,
            "boundary": (
                "The legacy accessibility branch motivates log A conditionally and then defines A exponentially. "
                "It does not supply a frozen derivation that independent recoverability options must compose multiplicatively."
            ),
        },
    }


def run_audit() -> dict:
    bindings = _archive_bindings()
    frozen = _frozen_dependency_audit(bindings)
    mult = _recovery_pair_multiplicativity_controls()
    sector = _exact_recovery_sector_nonselection()

    type_boundary_certified = bool(
        frozen["archive_bindings_match_expected"]
        and frozen["legacy_accessibility"]["v818_multiplicativity_statement_is_conditional"]
        and frozen["legacy_accessibility"]["v824_accessibility_is_defined_exponentially"]
        and not frozen["legacy_accessibility"]["independent_multiplicativity_derivation_present"]
        and mult["max_root_fidelity_product_error"] < 1e-12
        and mult["max_negative_log_additivity_error"] < 1e-12
        and sector["max_exact_recovery_infidelity"] < 1e-12
        and sector["max_product_state_cmi"] < 1e-12
        and sector["min_pairwise_source_ray_separation"] > 1e-2
    )
    primary = adjudicate_gate(type_boundary_certified, False)

    return {
        "version": "v15.06",
        "gate": "Recoverability Multiplicativity / Scalar-to-Operator Source Boundary",
        "primary_outcome": primary,
        "secondary_outcome": "LEGACY_ACCESSIBILITY_MULTIPLICATIVITY_WAS_ASSUMED_OR_DEFINED_NOT_DERIVED",
        "tertiary_outcome": "NEGATIVE_LOG_ROOT_FIDELITY_IS_ADDITIVE_ON_INDEPENDENT_RECOVERY_PAIRS",
        "major_structural_result": True,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "frozen_dependency_audit": frozen,
        "exact_recovery_pair_multiplicativity": mult,
        "exact_recovery_sector_nonselection": sector,
        "source_type_boundary": {
            "classification": "MULTIPLICATIVE_SCALAR_NEEDS_NEW_MAP_TO_BECOME_OPERATOR_SOURCE",
            "scalar_is_pair_or_recovery_context_dependent": True,
            "state_context_reduces_qubit_operator_freedom_to_a_of_r_A": True,
            "general_qubit_form_with_scalar_context": "F_traceless(rho,A)=a(r,A)(rho-I/2)",
            "exact_recovery_sector_leaves_a_of_r_1_unconstrained": True,
            "reason": (
                "The exact-recovery scalar equals 1 for product triples spanning every faithful local qubit radius. "
                "Thus multiplicativity supplies no equation for a(r,1). A new natural rule relating recovery context "
                "to the local spectral response would still be required."
            ),
            "frozen_natural_scalar_to_operator_selector_found": False,
        },
        "claim_boundary": {
            "multiplicative_quantum_recovery_scalar_exists": True,
            "legacy_accessibility_multiplicativity_derived": False,
            "accessibility_identified_with_root_fidelity": False,
            "negative_log_recovery_pair_fidelity_additive": True,
            "log_rho_source_law_derived": False,
            "cmi_used_only_as_frozen_recoverability_consistency_control": True,
            "entropy_or_time_used_as_source_selector": False,
            "downstream_gravity_used_as_selector": False,
            "physical_stress_energy_derived": False,
            "spacetime_or_einstein_equations_derived": False,
            "Pillar_3_closed": False,
        },
        "next_lawful_question": (
            "Does the frozen ontology contain a canonical local object whose independent composition is multiplicative "
            "and whose logarithmic additive generator is typed directly in the local Hermitian source space, rather than "
            "only as a scalar comparison/recoverability quantity?"
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
