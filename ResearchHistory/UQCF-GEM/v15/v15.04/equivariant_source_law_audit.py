#!/usr/bin/env python3
"""v15.04 equivariant source-law classification / spectral-freedom audit.

The analytic classification is primary. Numerical work only checks deterministic
corollaries and binds the theorem to the frozen v15.03 controls; it is not the
foundation of the theorem and it does not select a physical source law.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
V1326 = ROOT / "ResearchHistory/UQCF-GEM/v13/v13.26/SUMMARY.json"
V1403 = ROOT / "ResearchHistory/UQCF-GEM/v14/v14.03/SUMMARY.json"
V1503 = ROOT / "ResearchHistory/UQCF-GEM/v15/v15.03/SUMMARY.json"

EXPECTED_SOURCE = (-1.0, 0.0, 0.0, 1.0, 0.0)
EXPECTED_R_A = (0.15, -0.31, 0.42, 0.63, -0.22)
EXPECTED_R_B = (0.52, -0.18, 0.27, -0.47, 0.36)

I2 = np.eye(2, dtype=complex)
Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
H = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2.0)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _herm(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=complex)
    return 0.5 * (a + a.conj().T)


def _center(a: np.ndarray) -> np.ndarray:
    a = _herm(a)
    return a - np.trace(a) / a.shape[0] * np.eye(a.shape[0], dtype=complex)


def kron_all(ops: Iterable[np.ndarray]) -> np.ndarray:
    out = np.array([[1.0 + 0.0j]])
    for op in ops:
        out = np.kron(out, np.asarray(op, dtype=complex))
    return out


def embed_site(op: np.ndarray, site: int, nsites: int = 5) -> np.ndarray:
    ops = [I2] * nsites
    ops[site] = np.asarray(op, dtype=complex)
    return kron_all(ops)


def qubit_state(r: float) -> np.ndarray:
    if not abs(float(r)) < 1.0:
        raise ValueError("faithful qubit state requires |r| < 1")
    rho = 0.5 * (I2 + float(r) * Z)
    if np.min(np.linalg.eigvalsh(rho)) <= 0.0:
        raise ValueError("state must be faithful")
    return rho


def bloch_radius(rho: np.ndarray) -> float:
    rho = _herm(rho)
    purity = float(np.trace(rho @ rho).real)
    r2 = max(0.0, 2.0 * purity - 1.0)
    return float(math.sqrt(r2))


def deterministic_local_unitaries() -> tuple[np.ndarray, ...]:
    def rot(theta: float) -> np.ndarray:
        c, s = math.cos(theta), math.sin(theta)
        return np.array([[c, -s], [s, c]], dtype=complex)

    return (
        H,
        np.diag([1.0, np.exp(1j * math.pi / 5.0)]),
        rot(math.pi / 7.0),
        H @ np.diag([1.0, np.exp(1j * math.pi / 9.0)]),
        rot(-math.pi / 11.0),
    )


def projective_residual(p: np.ndarray, q: np.ndarray) -> float:
    p, q = _center(p), _center(q)
    np_, nq = float(np.linalg.norm(p)), float(np.linalg.norm(q))
    if np_ < 1e-14 and nq < 1e-14:
        return 0.0
    if min(np_, nq) < 1e-14:
        return 1.0
    return float(np.linalg.norm(p / np_ - q / nq))


def spectral_classification_theorem() -> dict[str, Any]:
    """Record the exact representation-theoretic classification.

    If F(U rho U*) = U F(rho) U* for all U, every stabilizer of rho also
    stabilizes F(rho). On each eigenspace of rho, the stabilizer contains the
    full unitary group of that eigenspace, so F(rho) is scalar on that block.
    This is exactly spectral functional freedom, with no scalar response law
    selected by covariance alone.
    """
    return {
        "classification": "LOCAL_UNITARY_EQUIVARIANCE_IMPLIES_SPECTRAL_SOURCE_LAW",
        "domain": "faithful finite-dimensional density operators",
        "codomain": "Hermitian operators on the same local Hilbert space",
        "covariance": "F(U rho U^dagger)=U F(rho) U^dagger for every unitary U",
        "stabilizer_implication": "U rho U^dagger=rho => U F(rho) U^dagger=F(rho)",
        "commutator_consequence": "[F(rho),rho]=0",
        "degenerate_eigenspace_consequence": "F(rho) is scalar on each degenerate eigenspace of rho",
        "spectral_form": "rho=V diag(lambda) V^dagger => F(rho)=V diag(Phi(lambda)) V^dagger",
        "spectral_assignment_constraint": "Phi is permutation-equivariant and equal eigenvalues receive equal outputs",
        "regularity_assumption_required": False,
        "converse": "Every well-defined real permutation-equivariant spectral assignment with equal outputs on equal eigenvalues defines a conjugation-equivariant Hermitian map.",
        "converse_certified": True,
        "selection_result": "COVARIANCE_FIXES_EIGENSPACES_NOT_SPECTRAL_RESPONSE_VALUES",
    }


def _spectral_map(rho: np.ndarray, response: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
    vals, vecs = np.linalg.eigh(_herm(rho))
    out = np.asarray(response(vals), dtype=float)
    if out.shape != vals.shape:
        raise ValueError("spectral response must preserve eigenvalue-vector shape")
    return _herm((vecs * out) @ vecs.conj().T)


def theorem_controls() -> dict[str, Any]:
    lam = np.array([0.57, 0.29, 0.14], dtype=float)
    rho = np.diag(lam).astype(complex)
    theta = np.array([math.pi / 7.0, -math.pi / 5.0, math.pi / 11.0])
    stabilizer = np.diag(np.exp(1j * theta))
    omega = np.exp(2j * math.pi / 3.0)
    fourier = np.array(
        [[1.0, 1.0, 1.0], [1.0, omega, omega**2], [1.0, omega**2, omega]],
        dtype=complex,
    ) / math.sqrt(3.0)

    laws = {
        "linear": lambda x: x,
        "square": lambda x: x**2,
        "log": lambda x: np.log(x),
        "spectrum_coupled": lambda x: x + float(np.sum(x**2)) * np.ones_like(x),
    }
    max_cov = 0.0
    max_stab = 0.0
    max_comm = 0.0
    for fn in laws.values():
        f0 = _spectral_map(rho, fn)
        rotated_rho = fourier @ rho @ fourier.conj().T
        f1 = _spectral_map(rotated_rho, fn)
        target = fourier @ f0 @ fourier.conj().T
        max_cov = max(max_cov, float(np.linalg.norm(f1 - target)))
        max_stab = max(max_stab, float(np.linalg.norm(stabilizer @ f0 @ stabilizer.conj().T - f0)))
        max_comm = max(max_comm, float(np.linalg.norm(f0 @ rho - rho @ f0)))

    nonspectral = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=complex)
    nonspectral_stabilizer_violation = float(
        np.linalg.norm(stabilizer @ nonspectral @ stabilizer.conj().T - nonspectral)
    )
    return {
        "fixture_spectrum": lam.tolist(),
        "tested_spectral_laws": list(laws),
        "max_covariance_error": max_cov,
        "max_stabilizer_invariance_error": max_stab,
        "max_commutator_norm": max_comm,
        "nonspectral_stabilizer_violation": nonspectral_stabilizer_violation,
        "classification": "DETERMINISTIC_CONTROLS_CORROBORATE_ANALYTIC_THEOREM",
        "scientific_foundation": False,
    }


def a_linear(radius: float) -> float:
    return 1.0


def a_log(radius: float) -> float:
    radius = float(radius)
    if radius < 0.0 or radius >= 1.0:
        raise ValueError("faithful qubit radius must lie in [0,1)")
    if radius < 1e-12:
        return 2.0
    return 2.0 * math.atanh(radius) / radius


def a_polynomial_witness(radius: float) -> float:
    radius = float(radius)
    return 1.0 + radius * radius


def local_response(rho: np.ndarray, a: Callable[[float], float]) -> np.ndarray:
    rho = _herm(rho)
    return float(a(bloch_radius(rho))) * (rho - 0.5 * I2)


def graph_source(
    source: Sequence[float],
    states: Sequence[np.ndarray],
    a: Callable[[float], float],
) -> np.ndarray:
    if len(source) != len(states):
        raise ValueError("source/state length mismatch")
    p = np.zeros((2 ** len(states), 2 ** len(states)), dtype=complex)
    for i, coeff in enumerate(source):
        ops = [I2] * len(states)
        ops[i] = local_response(states[i], a)
        p += float(coeff) * kron_all(ops)
    return _herm(p)


def qubit_corollary() -> dict[str, Any]:
    radii = sorted({abs(x) for x in EXPECTED_R_A + EXPECTED_R_B})
    max_square_identity = 0.0
    max_log_formula = 0.0
    coefficients: dict[str, float] = {}
    for radius in radii:
        rho = qubit_state(radius)
        delta = rho - 0.5 * I2
        rho2_centered = rho @ rho - np.trace(rho @ rho) / 2.0 * I2
        max_square_identity = max(max_square_identity, float(np.linalg.norm(rho2_centered - delta)))

        vals, vecs = np.linalg.eigh(rho)
        logrho = (vecs * np.log(vals)) @ vecs.conj().T
        log_centered = _center(logrho)
        predicted = a_log(radius) * delta
        max_log_formula = max(max_log_formula, float(np.linalg.norm(log_centered - predicted)))
        coefficients[f"{radius:.12g}"] = a_log(radius)

    log_vals = list(coefficients.values())
    return {
        "classification": "QUBIT_EQUIVARIANT_TRACELESS_MAP_IS_RADIAL",
        "general_form": "F(rho)=c(r) I + a(r)(rho-I/2) for r=|Bloch(rho)|; covariance alone leaves c and a arbitrary real scalar functions (with traceless part zero at r=0)",
        "projective_relevance": "the central c(r) I term is irrelevant after traceless/projective centering, but a(r) remains",
        "linear_response": "a_linear(r)=1",
        "square_identity": "rho^2-Tr(rho^2)I/2 = rho-I/2 exactly for every qubit density matrix",
        "max_linear_square_identity_error": max_square_identity,
        "log_identity": "log(rho)-Tr(log(rho))I/2 = artanh(r) rhat.sigma = [2 artanh(r)/r](rho-I/2)",
        "max_log_formula_error": max_log_formula,
        "a_log_values": coefficients,
        "log_response_nonconstant": max(log_vals) - min(log_vals) > 1e-6,
        "covariance_selection": "DIRECTION_ONLY_NOT_RESPONSE_LAW",
    }


def _fixture_from_v1503(v1503: dict[str, Any]) -> tuple[tuple[float, ...], dict[str, tuple[float, ...]]]:
    source = tuple(float(x) for x in v1503["source_fixture"]["source"])
    controls = v1503["state_dependent_controls"]["controls"]
    out = {
        "A": tuple(float(x) for x in controls["A"]["bloch_radii"]),
        "B": tuple(float(x) for x in controls["B"]["bloch_radii"]),
    }
    assert source == EXPECTED_SOURCE
    assert out["A"] == EXPECTED_R_A
    assert out["B"] == EXPECTED_R_B
    return source, out


def global_ray_controls(v1503: dict[str, Any]) -> dict[str, Any]:
    source, fixtures = _fixture_from_v1503(v1503)
    out: dict[str, Any] = {}
    for label, signed_radii in fixtures.items():
        states = [qubit_state(r) for r in signed_radii]
        linear = graph_source(source, states, a_linear)
        log = graph_source(source, states, a_log)
        poly = graph_source(source, states, a_polynomial_witness)
        source_sites = [i for i, s in enumerate(source) if abs(s) > 0.0]
        source_radii = [abs(signed_radii[i]) for i in source_sites]
        out[label] = {
            "source_support_sites": source_sites,
            "source_support_radii": source_radii,
            "source_support_spectra_unequal": len(set(source_radii)) > 1,
            "a_log_on_source_support": [a_log(r) for r in source_radii],
            "linear_log_projective_residual": projective_residual(linear, log),
            "linear_polynomial_projective_residual": projective_residual(linear, poly),
            "log_polynomial_projective_residual": projective_residual(log, poly),
        }
    return {
        "classification": "UNEQUAL_LOCAL_SPECTRA_GENERICALLY_SPLIT_PROJECTIVE_SOURCE_RAYS",
        "analytic_condition": "for Hilbert-Schmidt-orthogonal embedded nonzero site terms, [P_a]=[P_b] iff their response coefficients on source-support sites are related by one common positive factor; unequal radii plus nonconstant a(r)/b(r) therefore split the ray",
        "log_monotonicity": "2*artanh(r)/r is strictly increasing for 0<r<1",
        **out,
    }


def _covariance_error(
    source: Sequence[float],
    states: Sequence[np.ndarray],
    a: Callable[[float], float],
) -> float:
    us = deterministic_local_unitaries()
    u = kron_all(us)
    base = graph_source(source, states, a)
    rotated = [ui @ rho @ ui.conj().T for ui, rho in zip(us, states)]
    rebuilt = graph_source(source, rotated, a)
    target = u @ base @ u.conj().T
    return float(np.linalg.norm(rebuilt - target) / max(1.0, float(np.linalg.norm(target))))


def frozen_axiom_audit(v1326: dict[str, Any], v1403: dict[str, Any], v1503: dict[str, Any]) -> dict[str, Any]:
    assert v1326["adjudication"]["RSCL"] == "IRREDUCIBLE_RELATIVE_TO_CURRENT_FROZEN_ONTOLOGY"
    assert v1326["common_scale_control"]["max_normalized_source_direction_change"] < 1e-12
    assert v1403["telemetry"]["max_projective_tangent_scaling_error"] < 1e-12
    assert v1503["centrality_theorem"]["analytic_classification"] == "FULL_PRODUCT_LOCAL_UNITARY_COMMUTANT_IS_CENTER"
    assert v1503["state_dependent_controls"]["family_status"] == "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"

    source, fixtures = _fixture_from_v1503(v1503)
    balanced_delta = (0.25, -0.10, -0.05, -0.10, 0.0)
    assert abs(sum(balanced_delta)) < 1e-14
    laws: dict[str, Callable[[float], float]] = {
        "linear": a_linear,
        "log": a_log,
        "polynomial_witness": a_polynomial_witness,
    }
    telemetry: dict[str, Any] = {}
    max_add = max_hom = max_cov = max_proj = max_null = 0.0
    for name, law in laws.items():
        law_rows: dict[str, Any] = {}
        for label, signed_radii in fixtures.items():
            states = [qubit_state(r) for r in signed_radii]
            ps = graph_source(source, states, law)
            pt = graph_source(balanced_delta, states, law)
            pst = graph_source(tuple(x + y for x, y in zip(source, balanced_delta)), states, law)
            add = float(np.linalg.norm(pst - ps - pt))
            scale = 3.7
            pscaled = graph_source(tuple(scale * x for x in source), states, law)
            hom = float(np.linalg.norm(pscaled - scale * ps))
            cov = _covariance_error(source, states, law)
            proj = projective_residual(ps, pscaled)
            null = float(np.linalg.norm(graph_source((0.0,) * 5, states, law)))
            max_add = max(max_add, add)
            max_hom = max(max_hom, hom)
            max_cov = max(max_cov, cov)
            max_proj = max(max_proj, proj)
            max_null = max(max_null, null)
            law_rows[label] = {
                "source_additivity_error": add,
                "source_homogeneity_error": hom,
                "local_unitary_covariance_error": cov,
                "positive_scale_projective_residual": proj,
                "null_source_norm": null,
            }
        telemetry[name] = law_rows

    all_linear = max(max_add, max_hom, max_null) < 2e-12
    all_covariant = max_cov < 2e-10
    all_projective = max_proj < 2e-12
    return {
        "classification": "FROZEN_SOURCE_AXIOMS_DO_NOT_SELECT_SPECTRAL_RESPONSE_FUNCTION",
        "scope": "audited frozen source-law constraints carried by v13.26, v14.03, and v15.03",
        "archive_bindings": {
            "v13.26": {"path": V1326.relative_to(ROOT).as_posix(), "sha256": _sha256(V1326)},
            "v14.03": {"path": V1403.relative_to(ROOT).as_posix(), "sha256": _sha256(V1403)},
            "v15.03": {"path": V1503.relative_to(ROOT).as_posix(), "sha256": _sha256(V1503)},
        },
        "frozen_constraints_tested": [
            "retained source amount/extensivity and homogeneous source-current scaling",
            "positive projective source rescaling",
            "independent local-unitary/frame covariance",
            "source additivity/linearity in the retained scalar source coefficients",
            "null-source compatibility",
        ],
        "tensor_state_functional_equation_status": "NO_CERTIFIED_TENSOR_COMPOSITION_FUNCTIONAL_EQUATION_IN_AUDITED_SOURCE_LAW_DEPENDENCIES",
        "all_tested_response_functions_preserve_source_linearity": all_linear,
        "all_tested_response_functions_preserve_local_unitary_covariance": all_covariant,
        "all_tested_response_functions_preserve_positive_projective_source_scaling": all_projective,
        "max_source_additivity_error": max_add,
        "max_source_homogeneity_error": max_hom,
        "max_local_unitary_covariance_error": max_cov,
        "max_positive_scale_projective_residual": max_proj,
        "max_null_source_norm": max_null,
        "witness_laws": list(laws),
        "telemetry": telemetry,
        "selection_result": "NO_UNIQUE_A_OF_R",
        "boundary": "A new tensor-composition or other spectral functional equation could reduce the freedom, but it would be a new assumption unless independently recovered from frozen structure.",
    }


def v1503_binding(v1503: dict[str, Any], rays: dict[str, Any]) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    square_ok = True
    log_ok = True
    for label in ("A", "B"):
        frozen = v1503["state_dependent_controls"]["controls"][label]["pairwise_projective_residuals"]
        theorem_linear_square = 0.0
        current_linear_log = float(rays[label]["linear_log_projective_residual"])
        square_delta = abs(float(frozen["linear__square"]) - theorem_linear_square)
        log_delta = abs(float(frozen["linear__log"]) - current_linear_log)
        square_ok = square_ok and square_delta < 2e-12
        log_ok = log_ok and log_delta < 2e-12
        rows[label] = {
            "frozen_linear_square_residual": float(frozen["linear__square"]),
            "theorem_linear_square_residual": theorem_linear_square,
            "linear_square_absolute_difference": square_delta,
            "frozen_linear_log_residual": float(frozen["linear__log"]),
            "theorem_linear_log_residual": current_linear_log,
            "linear_log_absolute_difference": log_delta,
        }
    return {
        "classification": "V15_03_NUMERICS_ARE_ILLUSTRATIONS_OF_V15_04_THEOREM",
        "linear_square_residuals_match_theorem": square_ok,
        "linear_log_residuals_match_theorem": log_ok,
        "controls": rows,
    }


def adjudicate_gate(*, freedom_certified: bool, unique_selection_certified: bool) -> str:
    """Return only positively certified scientific outcomes.

    Verification failure is not evidence for the opposite hypothesis. The two
    decisive scientific outcomes are mutually exclusive and each requires its
    own positive certificate; otherwise the gate remains unresolved.
    """
    if freedom_certified and unique_selection_certified:
        raise ValueError("mutually exclusive v15.04 outcomes cannot both be certified")
    if freedom_certified:
        return "COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM"
    if unique_selection_certified:
        return "FROZEN_AXIOMS_SELECT_UNIQUE_SPECTRAL_LAW"
    return "V15_04_GATE_UNRESOLVED"


def run_audit() -> dict[str, Any]:
    v1326 = _load_json(V1326)
    v1403 = _load_json(V1403)
    v1503 = _load_json(V1503)

    theorem = spectral_classification_theorem()
    theorem_num = theorem_controls()
    qubit = qubit_corollary()
    rays = global_ray_controls(v1503)
    axioms = frozen_axiom_audit(v1326, v1403, v1503)
    binding = v1503_binding(v1503, rays)

    theorem_controls_ok = (
        theorem_num["max_covariance_error"] < 2e-12
        and theorem_num["max_stabilizer_invariance_error"] < 2e-12
        and theorem_num["max_commutator_norm"] < 2e-12
        and theorem_num["nonspectral_stabilizer_violation"] > 1e-6
    )
    qubit_ok = (
        qubit["max_linear_square_identity_error"] < 2e-12
        and qubit["max_log_formula_error"] < 2e-12
        and qubit["log_response_nonconstant"]
    )
    rays_ok = all(
        rays[label]["source_support_spectra_unequal"]
        and rays[label]["linear_log_projective_residual"] > 1e-6
        for label in ("A", "B")
    )
    axioms_ok = (
        axioms["all_tested_response_functions_preserve_source_linearity"]
        and axioms["all_tested_response_functions_preserve_local_unitary_covariance"]
        and axioms["all_tested_response_functions_preserve_positive_projective_source_scaling"]
        and axioms["selection_result"] == "NO_UNIQUE_A_OF_R"
    )
    binding_ok = (
        binding["linear_square_residuals_match_theorem"]
        and binding["linear_log_residuals_match_theorem"]
    )

    freedom_certified = theorem_controls_ok and qubit_ok and rays_ok and axioms_ok and binding_ok
    outcome = adjudicate_gate(
        freedom_certified=freedom_certified,
        unique_selection_certified=False,
    )

    return {
        "version": "v15.04",
        "title": "Equivariant Source-Law Classification / Spectral Freedom Gate",
        "theorem": theorem,
        "theorem_controls": theorem_num,
        "qubit_corollary": qubit,
        "frozen_axiom_audit": axioms,
        "global_ray_controls": rays,
        "v1503_binding": binding,
        "gate_outcome": outcome,
        "secondary_statuses": [
            theorem["selection_result"],
            qubit["covariance_selection"],
            axioms["selection_result"],
            binding["classification"],
        ],
        "major_structural_result": outcome == "COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM",
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "claim_scope": "classification of local conjugation-equivariant Hermitian source maps and whether the already-frozen source-law constraints select the remaining spectral response function",
        "interpretation": "Local-unitary covariance fixes the eigenspaces/direction of a state-dependent operator source but not its spectral response values. For qubits the entire traceless freedom is one scalar function a(r). The frozen retained source linearity, positive projective scaling, and local-frame covariance constraints remain satisfied by inequivalent a(r), so v15.03 nonuniqueness is an illustration of an exact classification theorem rather than evidence for it.",
        "not_derived": [
            "a unique operator-valued source response law a(r)",
            "a certified exact retained-node-to-quantum-site factorization",
            "a natural graph-site-to-C125 compatibility-parent map",
            "Genesis/provenance selection of a spectral response law",
            "absolute source magnitude or observer source calibration",
            "physical stress-energy",
            "source-to-coframe/solder law",
            "physical metric or spacetime",
            "absolute gravitational coupling",
            "Einstein equations",
            "physical time primitive",
            "Pillar 3 closure",
        ],
        "stop_rule": "Do not privilege log(rho), linear rho, or any other a(r) using downstream gravity/ADM/Einstein quality. A further selector must be independently frozen structure or an explicit NEW ASSUMPTION; no entropy, pruning, or physical time enters this pre-pruning gate.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
