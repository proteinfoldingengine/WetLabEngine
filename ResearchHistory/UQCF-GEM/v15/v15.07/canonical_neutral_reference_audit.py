#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, Tuple

import numpy as np


EXPECTED_BINDINGS = {
    "ResearchHistory/UQCF-GEM/v13/v13.02/REPORT.md": "f560c85c73e3167e034d09ab0fab081e33cd3895",
    "ResearchHistory/UQCF-GEM/v13/v13.11/REPORT.md": "b18b3582060cb6b6527059987d6635e120ee7fb0",
    "ResearchHistory/UQCF-GEM/v15/v15.04/REPORT.md": "9a6a289cc5471def4c4d4f86756c3183802d1cc4",
    "ResearchHistory/UQCF-GEM/v15/v15.05/REPORT.md": "b191c08c22ded0439cc4c2c125fbccfdb677dcbc",
    "ResearchHistory/UQCF-GEM/v15/v15.06/REPORT.md": "bdeac09b2b162f07baa874ef1c1d6415fdd5e236",
    "ResearchHistory/UQCF-GEM/v15/v15.06/SUMMARY.json": "0eeff65e80ea26090206b0907119a25a3b7bef45",
}

I2 = np.eye(2, dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
PAULIS = (SX, SY, SZ)


def adjudicate_gate(canonical_generator_exists_but_not_source: bool, source_identification_certified: bool) -> str:
    if canonical_generator_exists_but_not_source and source_identification_certified:
        raise ValueError("v15.07 source-identification and underived-identification certificates are mutually exclusive")
    if canonical_generator_exists_but_not_source:
        return "CANONICAL_NEUTRAL_RELATIVE_GENERATOR_EXISTS_SOURCE_IDENTIFICATION_UNDERIVED"
    if source_identification_certified:
        return "FROZEN_ONTOLOGY_IDENTIFIES_CANONICAL_GENERATOR_AS_SOURCE"
    return "V15_07_GATE_UNRESOLVED"


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
    out_vals = fn(vals)
    return (vecs * out_vals) @ vecs.conj().T


def _logm_pos(a: np.ndarray) -> np.ndarray:
    vals = np.linalg.eigvalsh(a)
    if float(np.min(vals)) <= 0.0:
        raise ValueError("matrix logarithm requires positive definite input")
    return _hermitian_function(a, np.log)


def _expm_herm(a: np.ndarray) -> np.ndarray:
    return _hermitian_function(a, np.exp)


def _random_density(seed: int, dim: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(dim, dim)) + 1.0j * rng.normal(size=(dim, dim))
    rho = x @ x.conj().T + 0.35 * np.eye(dim, dtype=complex)
    return rho / np.trace(rho)


def _deterministic_unitary(seed: int, dim: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(dim, dim)) + 1.0j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(x)
    diag = np.diag(r)
    phases = np.ones_like(diag, dtype=complex)
    nz = np.abs(diag) > 0.0
    phases[nz] = diag[nz] / np.abs(diag[nz])
    return q @ np.diag(np.conjugate(phases))


def _neutral_reference(dim: int) -> np.ndarray:
    return np.eye(dim, dtype=complex) / float(dim)


def _weyl_generators(dim: int) -> Tuple[np.ndarray, np.ndarray]:
    shift = np.zeros((dim, dim), dtype=complex)
    for j in range(dim):
        shift[(j + 1) % dim, j] = 1.0
    omega = np.exp(2j * np.pi / dim)
    clock = np.diag([omega**j for j in range(dim)]).astype(complex)
    return shift, clock


def _commutant_nullity(dim: int) -> Tuple[int, float]:
    shift, clock = _weyl_generators(dim)
    cols = []
    for j in range(dim):
        for k in range(dim):
            e = np.zeros((dim, dim), dtype=complex)
            e[j, k] = 1.0
            cols.append(np.concatenate(((shift @ e - e @ shift).ravel(), (clock @ e - e @ clock).ravel())))
    constraint = np.column_stack(cols)
    singular = np.linalg.svd(constraint, compute_uv=False)
    tol = 1e-11
    nullity = int(dim * dim - np.sum(singular > tol))
    tau = _neutral_reference(dim)
    residual = max(float(np.linalg.norm(shift @ tau - tau @ shift)), float(np.linalg.norm(clock @ tau - tau @ clock)))
    return nullity, residual


def _canonical_neutral_reference_controls() -> dict:
    dims = [2, 3, 4, 5]
    nullities = {}
    residuals = {}
    invariance_errors = {}
    for d in dims:
        nullity, residual = _commutant_nullity(d)
        nullities[str(d)] = nullity
        residuals[str(d)] = residual
        tau = _neutral_reference(d)
        u = _deterministic_unitary(15070 + d, d)
        invariance_errors[str(d)] = float(np.linalg.norm(u @ tau @ u.conj().T - tau))

    tensor_errors = []
    for d1, d2 in ((2, 2), (2, 3), (3, 4)):
        tensor_errors.append(float(np.linalg.norm(_neutral_reference(d1 * d2) - np.kron(_neutral_reference(d1), _neutral_reference(d2)))))

    return {
        "classification": "UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED",
        "theorem": (
            "A normalized density operator invariant under conjugation by every local unitary lies in the full-unitary commutant, "
            "hence is scalar; trace one fixes tau_d=I_d/d. The references obey tau_{d1*d2}=tau_d1 tensor tau_d2."
        ),
        "tested_dimensions": dims,
        "commutant_nullities": nullities,
        "all_commutant_nullities_one": all(v == 1 for v in nullities.values()),
        "max_commutant_residual": max(residuals.values()),
        "max_unitary_invariance_error": max(invariance_errors.values()),
        "max_reference_tensor_error": max(tensor_errors),
        "reference_formula": "tau_d=I_d/d",
        "requires_basis_choice": False,
        "uses_entropy_or_time": False,
    }


def _relative_density(rho: np.ndarray) -> np.ndarray:
    # tau_d^{-1/2} rho tau_d^{-1/2}; for tau_d=I/d this is exactly d*rho.
    d = rho.shape[0]
    return float(d) * rho


def _relative_density_generator_controls() -> dict:
    controls = []
    max_relative_tensor = 0.0
    max_log_add = 0.0
    max_centered_identity = 0.0
    max_cov = 0.0

    for idx, (d1, d2) in enumerate(((2, 2), (2, 3), (3, 3), (3, 4))):
        rho = _random_density(15700 + 2 * idx, d1)
        sigma = _random_density(15701 + 2 * idx, d2)
        q1 = _relative_density(rho)
        q2 = _relative_density(sigma)
        product = np.kron(rho, sigma)
        q12 = _relative_density(product)
        rel_err = float(np.linalg.norm(q12 - np.kron(q1, q2)))

        k1 = _logm_pos(q1)
        k2 = _logm_pos(q2)
        k12 = _logm_pos(q12)
        rhs = np.kron(k1, np.eye(d2, dtype=complex)) + np.kron(np.eye(d1, dtype=complex), k2)
        log_err = float(np.linalg.norm(k12 - rhs))

        centered_err = max(
            float(np.linalg.norm(_center(k1) - _center(_logm_pos(rho)))),
            float(np.linalg.norm(_center(k2) - _center(_logm_pos(sigma)))),
        )

        u = _deterministic_unitary(15800 + idx, d1)
        rho_u = u @ rho @ u.conj().T
        q_cov = float(np.linalg.norm(_relative_density(rho_u) - u @ q1 @ u.conj().T))
        k_cov = float(np.linalg.norm(_logm_pos(_relative_density(rho_u)) - u @ k1 @ u.conj().T))
        cov_err = max(q_cov, k_cov)

        max_relative_tensor = max(max_relative_tensor, rel_err)
        max_log_add = max(max_log_add, log_err)
        max_centered_identity = max(max_centered_identity, centered_err)
        max_cov = max(max_cov, cov_err)
        controls.append({
            "dims": [d1, d2],
            "relative_operator_tensor_error": rel_err,
            "log_tensor_additivity_error": log_err,
            "centered_log_identity_error": centered_err,
            "local_frame_covariance_error": cov_err,
        })

    return {
        "classification": "CANONICAL_RELATIVE_DENSITY_OPERATOR_IS_MULTIPLICATIVE",
        "relative_operator": "Q_d(rho)=tau_d^{-1/2} rho tau_d^{-1/2}=d*rho",
        "multiplicative_law": "Q_{d1*d2}(rho tensor sigma)=Q_d1(rho) tensor Q_d2(sigma)",
        "additive_generator": "K_d(rho)=log Q_d(rho)=log rho + log(d) I",
        "centered_generator": "K_d^0(rho)=log rho - Tr(log rho) I/d",
        "generator_shape": "centered_log_rho",
        "controls": controls,
        "max_relative_operator_tensor_error": max_relative_tensor,
        "max_log_tensor_additivity_error": max_log_add,
        "max_centered_log_identity_error": max_centered_identity,
        "max_local_frame_covariance_error": max_cov,
        "uses_reference_beyond_frame_symmetry": False,
    }


def _pgrl_state(base: np.ndarray, generator: np.ndarray, s: float = 1.0) -> np.ndarray:
    h = _logm_pos(base) + float(s) * generator
    x = _expm_herm(h)
    return x / np.trace(x)


def _neutral_to_state_endpoint_controls() -> dict:
    records = []
    max_reconstruction = 0.0
    max_generator_identity = 0.0
    for idx, d in enumerate((2, 3, 4, 5)):
        rho = _random_density(15900 + idx, d)
        tau = _neutral_reference(d)
        k = _logm_pos(_relative_density(rho))
        reconstructed = _pgrl_state(tau, k, 1.0)
        rec_err = float(np.linalg.norm(reconstructed - rho))
        gen_err = float(np.linalg.norm(_center(k) - _center(_logm_pos(rho))))
        max_reconstruction = max(max_reconstruction, rec_err)
        max_generator_identity = max(max_generator_identity, gen_err)
        records.append({"dim": d, "endpoint_reconstruction_error": rec_err, "centered_generator_identity_error": gen_err})

    rho = _random_density(15920, 2)
    sigma = _random_density(15921, 3)
    target = np.kron(rho, sigma)
    tau = _neutral_reference(6)
    product_generator = _logm_pos(_relative_density(target))
    product_endpoint_error = float(np.linalg.norm(_pgrl_state(tau, product_generator, 1.0) - target))

    return {
        "classification": "NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY",
        "status": "CONDITIONAL_ON_SOURCE_AS_NEUTRAL_TO_STATE_PREPARATION_GENERATOR",
        "theorem": (
            "For tau_d=I/d and faithful rho, any PGRL endpoint equation rho=exp(log tau_d+s P)/Z with s>0 fixes "
            "the positive projective centered generator ray [P]_+=[centered log rho]_+. The magnitude remains tied to the arbitrary endpoint parameter s."
        ),
        "records": records,
        "max_endpoint_reconstruction_error": max_reconstruction,
        "max_generator_identity_error": max_generator_identity,
        "product_endpoint_error": product_endpoint_error,
        "absolute_generator_scale_selected": False,
        "projective_generator_ray_selected": True,
        "premise_frozen_as_source_semantics": False,
    }


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


def _source_identification_boundary() -> dict:
    rho = _qubit_state(0.20, (0.3, -0.4, 0.8660254037844386))
    sigma = _qubit_state(0.80, (-0.5, 0.7, 0.5099019513592785))
    product = np.kron(rho, sigma)

    candidates = {}
    min_output_eig = float("inf")
    max_trace_error = 0.0
    for kind in ("linear", "log", "polynomial"):
        p = _compose_two(_local_source(rho, kind), _local_source(sigma, kind))
        candidates[kind] = p
        out = _pgrl_state(product, p, 0.17)
        min_output_eig = min(min_output_eig, float(np.min(np.linalg.eigvalsh(out))))
        max_trace_error = max(max_trace_error, abs(float(np.trace(out).real) - 1.0))

    separations = {
        "linear_vs_log": _ray_separation(candidates["linear"], candidates["log"]),
        "linear_vs_polynomial": _ray_separation(candidates["linear"], candidates["polynomial"]),
        "log_vs_polynomial": _ray_separation(candidates["log"], candidates["polynomial"]),
    }
    min_sep = min(separations.values())

    canonical_centered = _center(_logm_pos(_relative_density(product)))
    log_sum = candidates["log"]
    log_ray_match = _ray_separation(canonical_centered, log_sum)

    return {
        "classification": "CANONICAL_OPERATOR_GENERATOR_DOES_NOT_BY_ITSELF_DEFINE_THE_SOURCE",
        "frozen_source_equals_neutral_relative_generator_axiom_found": False,
        "audited_source_kinematics": "v13.11 PGRL permits arbitrary centered Hermitian source generator P at a fixed faithful state",
        "same_state_multiple_valid_pgrl_generators": bool(min_output_eig > 0.0 and max_trace_error < 1e-12 and min_sep > 1e-2),
        "candidate_generators": ["linear", "log", "polynomial"],
        "pairwise_global_source_ray_separations": separations,
        "min_pairwise_global_source_ray_separation": min_sep,
        "min_finite_pgrl_output_eigenvalue": min_output_eig,
        "max_finite_pgrl_trace_error": max_trace_error,
        "canonical_generator_vs_v15_04_log_source_ray_residual": log_ray_match,
        "reason": (
            "Frame symmetry canonically supplies tau_d and therefore the Hermitian additive generator centered log rho. "
            "But the frozen PGRL law treats P as an independently supplied generator; it does not state that sourcehood means "
            "the neutral-to-state preparation generator. That semantic identification is the remaining premise."
        ),
    }


def _frozen_dependency_audit(bindings: Dict[str, str]) -> dict:
    return {
        "archive_bindings": bindings,
        "archive_bindings_match_expected": bindings == EXPECTED_BINDINGS,
        "v13_02": {
            "fact": "maximally mixed local state is the isotropic BKM point",
            "role": "consistent with neutral frame-invariant reference; does not define sourcehood",
        },
        "v13_11": {
            "source_family": "rho_s=exp(log rho+sP)/Z_s",
            "source_generator_status": "P independently supplied; tangent linear in centered P",
            "forces_P_equal_centered_log_rho": False,
        },
        "v15_04": {
            "state_derived_qubit_family": "F_traceless(rho)=a(r)(rho-I/2)",
            "a_of_r_selected": False,
        },
        "v15_05": {
            "log_shape_conditional_selector": "universal scalar functional calculus plus centered tensor derivation",
            "premise_was_frozen": False,
        },
        "v15_06": {
            "result": "multiplicative recovery scalar exists but does not select local operator source",
            "next_question_answered_here": "a canonical local multiplicative operator does exist: Q_d(rho)=d rho",
        },
        "source_semantics_rule_found": False,
        "classification": "CANONICAL_OPERATOR_OBJECT_EARNED_SOURCE_SEMANTICS_NOT_EARNED",
    }


def run_audit() -> dict:
    bindings = _archive_bindings()
    frozen = _frozen_dependency_audit(bindings)
    neutral = _canonical_neutral_reference_controls()
    relative = _relative_density_generator_controls()
    endpoint = _neutral_to_state_endpoint_controls()
    boundary = _source_identification_boundary()

    positive_math = bool(
        frozen["archive_bindings_match_expected"]
        and neutral["all_commutant_nullities_one"]
        and neutral["max_commutant_residual"] < 1e-12
        and neutral["max_reference_tensor_error"] < 1e-12
        and relative["max_relative_operator_tensor_error"] < 1e-12
        and relative["max_log_tensor_additivity_error"] < 1e-11
        and relative["max_centered_log_identity_error"] < 1e-12
        and relative["max_local_frame_covariance_error"] < 1e-11
        and endpoint["max_endpoint_reconstruction_error"] < 1e-11
        and endpoint["product_endpoint_error"] < 1e-11
        and boundary["canonical_generator_vs_v15_04_log_source_ray_residual"] < 1e-11
    )
    source_underived = bool(
        positive_math
        and frozen["source_semantics_rule_found"] is False
        and boundary["frozen_source_equals_neutral_relative_generator_axiom_found"] is False
        and boundary["same_state_multiple_valid_pgrl_generators"]
        and boundary["min_pairwise_global_source_ray_separation"] > 1e-2
    )

    primary = adjudicate_gate(source_underived, False)

    return {
        "version": "v15.07",
        "gate": "Canonical Neutral Reference / Relative-Density Generator Gate",
        "primary_outcome": primary,
        "secondary_outcome": "UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED",
        "tertiary_outcome": "NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY",
        "major_structural_result": True,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "frozen_dependency_audit": frozen,
        "canonical_neutral_reference": neutral,
        "relative_density_generator": relative,
        "neutral_to_state_endpoint": endpoint,
        "source_identification_boundary": boundary,
        "claim_boundary": {
            "canonical_neutral_reference_derived": True,
            "canonical_multiplicative_local_operator_derived": True,
            "centered_log_generator_derived": True,
            "neutral_to_state_log_projective_ray_theorem": True,
            "log_generator_identified_as_physical_source": False,
            "new_source_semantics_needed": True,
            "absolute_source_scale_derived": False,
            "retained_node_to_quantum_site_carrier_derived": False,
            "graph_site_to_compatibility_parent_map_derived": False,
            "physical_stress_energy_derived": False,
            "spacetime_or_einstein_equations_derived": False,
            "downstream_gravity_used_as_selector": False,
            "entropy_or_time_used_as_selector": False,
            "Pillar_3_closed": False,
        },
        "next_lawful_question": (
            "Does sourcehood in the frozen provenance/Genesis ontology have an independently earned meaning as a neutral-reference-to-state "
            "preparation generator? If yes, the positive projective log source ray becomes canonical without downstream fitting; if no, stop "
            "and label that semantic identification a NEW ASSUMPTION."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
