#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Callable, Dict, Tuple

import numpy as np


EXPECTED_BINDINGS = {
    "ResearchHistory/UQCF-GEM/v13/v13.04/REPORT.md": "e857d81f58a540833a7672fe769b2a301bad4459",
    "ResearchHistory/UQCF-GEM/v13/v13.22/REPORT.md": "e6920facaa4d133e2767951612c608d0e514806c",
    "ResearchHistory/UQCF-GEM/v13/v13.23/REPORT.md": "1162d8f8378cb5292d6c2f8526dd5bd53198d2c4",
    "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md": "9917085b211ca0e1f4737082227f55097cc72b66",
    "ResearchHistory/UQCF-GEM/v14/v14.03/REPORT.md": "03d5e8df43d1f163901d33b1182fbfd3f21b626a",
    "ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md": "6c3aed73c63c9c7554107d163e15b8fae7549c1c",
    "ResearchHistory/UQCF-GEM/v15/v15.04/REPORT.md": "9a6a289cc5471def4c4d4f86756c3183802d1cc4",
    "ResearchHistory/UQCF-GEM/v15/v15.04/SUMMARY.json": "a2c4cf211e625dfb3a7673fd7d6c008e382e3d8d",
}

I2 = np.eye(2, dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
PAULIS = (SX, SY, SZ)


def adjudicate_gate(nonselection_certified: bool, frozen_unique_selector_certified: bool) -> str:
    if nonselection_certified and frozen_unique_selector_certified:
        raise ValueError("v15.05 unique-selection and non-selection certificates are mutually exclusive")
    if nonselection_certified:
        return "FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE"
    if frozen_unique_selector_certified:
        return "FROZEN_COMPOSITION_LAW_SELECTS_UNIQUE_SPECTRAL_RESPONSE"
    return "V15_05_GATE_UNRESOLVED"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def _archive_bindings() -> Dict[str, str]:
    root = _repo_root()
    return {rel: _git_blob_sha(root / rel) for rel in EXPECTED_BINDINGS}


def _qubit_state(radius: float, direction: Tuple[float, float, float]) -> np.ndarray:
    n = np.asarray(direction, dtype=float)
    n = n / np.linalg.norm(n)
    bloch = sum(float(n[k]) * PAULIS[k] for k in range(3))
    return 0.5 * (I2 + float(radius) * bloch)


def _bloch_radius(rho: np.ndarray) -> float:
    components = np.array([np.trace(rho @ p).real for p in PAULIS], dtype=float)
    return float(np.linalg.norm(components))


def _response_coefficient(radius: float, kind: str) -> float:
    if kind == "linear":
        return 1.0
    if kind == "log":
        if radius < 1e-14:
            return 2.0
        return float(2.0 * np.arctanh(radius) / radius)
    if kind == "polynomial":
        return float(1.0 + radius * radius)
    raise ValueError(f"unknown response kind: {kind}")


def _local_source(rho: np.ndarray, kind: str) -> np.ndarray:
    radius = _bloch_radius(rho)
    return _response_coefficient(radius, kind) * (rho - 0.5 * I2)


def _compose_sources(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    dl = left.shape[0]
    dr = right.shape[0]
    return np.kron(left, np.eye(dr, dtype=complex)) + np.kron(np.eye(dl, dtype=complex), right)


def _deterministic_unitary(seed: int, dim: int = 2) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dim, dim)) + 1.0j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    phases = np.ones_like(diagonal, dtype=complex)
    nz = np.abs(diagonal) > 0.0
    phases[nz] = diagonal[nz] / np.abs(diagonal[nz])
    return q @ np.diag(np.conjugate(phases))


def _swap_matrix(d1: int, d2: int) -> np.ndarray:
    swap = np.zeros((d1 * d2, d1 * d2), dtype=complex)
    for i in range(d1):
        for j in range(d2):
            swap[j * d1 + i, i * d2 + j] = 1.0
    return swap


def _projective_ray_separation(a: np.ndarray, b: np.ndarray) -> float:
    # Every witness here is traceless, so the identity-shift part of the
    # positive projective equivalence is already absent.
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        raise ValueError("projective comparison requires nonzero sources")
    return float(np.linalg.norm(a / na - b / nb))


def _labeled_monoidal_controls() -> dict:
    rho = _qubit_state(0.15, (0.2, -0.7, 0.68))
    sigma = _qubit_state(0.72, (-0.4, 0.1, 0.91))
    tau = _qubit_state(0.43, (0.5, 0.5, 0.707))
    u = _deterministic_unitary(1505)
    v = _deterministic_unitary(1506)
    uv = np.kron(u, v)
    swap = _swap_matrix(2, 2)

    witnesses = ("linear", "log", "polynomial")
    pair_sources: Dict[str, np.ndarray] = {}
    metrics: Dict[str, dict] = {}

    for kind in witnesses:
        fr = _local_source(rho, kind)
        fs = _local_source(sigma, kind)
        ft = _local_source(tau, kind)
        pair = _compose_sources(fr, fs)
        pair_sources[kind] = pair

        rho_u = u @ rho @ u.conj().T
        sigma_v = v @ sigma @ v.conj().T
        transformed = _compose_sources(_local_source(rho_u, kind), _local_source(sigma_v, kind))
        covariance_error = float(np.linalg.norm(transformed - uv @ pair @ uv.conj().T))

        left_assoc = _compose_sources(_compose_sources(fr, fs), ft)
        right_assoc = _compose_sources(fr, _compose_sources(fs, ft))
        associativity_error = float(np.linalg.norm(left_assoc - right_assoc))

        swapped = _compose_sources(fs, fr)
        swap_error = float(np.linalg.norm(swap @ pair @ swap.conj().T - swapped))

        metrics[kind] = {
            "rho_radius": _bloch_radius(rho),
            "sigma_radius": _bloch_radius(sigma),
            "rho_response_coefficient": _response_coefficient(_bloch_radius(rho), kind),
            "sigma_response_coefficient": _response_coefficient(_bloch_radius(sigma), kind),
            "local_covariance_error": covariance_error,
            "associativity_error": associativity_error,
            "swap_naturality_error": swap_error,
        }

    separations = {
        "linear_vs_log": _projective_ray_separation(pair_sources["linear"], pair_sources["log"]),
        "linear_vs_polynomial": _projective_ray_separation(pair_sources["linear"], pair_sources["polynomial"]),
        "log_vs_polynomial": _projective_ray_separation(pair_sources["log"], pair_sources["polynomial"]),
    }

    max_covariance = max(m["local_covariance_error"] for m in metrics.values())
    max_associativity = max(m["associativity_error"] for m in metrics.values())
    max_swap = max(m["swap_naturality_error"] for m in metrics.values())
    min_separation = min(separations.values())

    return {
        "classification": "LABELED_MONOIDAL_COMPOSITION_PRESERVES_ARBITRARY_LOCAL_SPECTRAL_RESPONSE",
        "theorem_scope": "LABELED_PRODUCT_STATES_WITH_FIXED_TENSOR_FACTORS",
        "theorem": (
            "For any already-chosen family of local covariant sources F_a on labeled factors, "
            "M_a(rho_1 tensor ... tensor rho_n)=sum_i I tensor ... tensor F_a(rho_i) tensor ... tensor I "
            "is associative, permutation-natural, and locally covariant. Therefore tensor composition "
            "composes a local law but does not select the local spectral response a(r)."
        ),
        "witnesses": list(witnesses),
        "witness_metrics": metrics,
        "pairwise_projective_ray_separations": separations,
        "max_local_covariance_error": max_covariance,
        "max_associativity_error": max_associativity,
        "max_swap_naturality_error": max_swap,
        "min_pairwise_projective_ray_separation": min_separation,
        "all_three_monoidal": bool(max(max_covariance, max_associativity, max_swap) < 1e-12),
        "all_three_projectively_distinct": bool(min_separation > 1e-2),
    }


def _centered_matrix_function(rho: np.ndarray, kind: str) -> np.ndarray:
    values, vectors = np.linalg.eigh(rho)
    if np.min(values) <= 0.0:
        raise ValueError("matrix function requires a faithful state")
    if kind == "log":
        out_values = np.log(values)
    elif kind == "linear":
        out_values = values
    elif kind == "cubic":
        out_values = values**3
    else:
        raise ValueError(f"unknown scalar function kind: {kind}")
    out = (vectors * out_values) @ vectors.conj().T
    dim = rho.shape[0]
    return out - (np.trace(out) / dim) * np.eye(dim, dtype=complex)


def _centered_tensor_error(rho: np.ndarray, sigma: np.ndarray, kind: str) -> float:
    lhs = _centered_matrix_function(np.kron(rho, sigma), kind)
    rhs = _compose_sources(_centered_matrix_function(rho, kind), _centered_matrix_function(sigma, kind))
    return float(np.linalg.norm(lhs - rhs))


def _stronger_selector_boundary() -> dict:
    rho = _qubit_state(0.15, (0.2, -0.7, 0.68))
    sigma = _qubit_state(0.72, (-0.4, 0.1, 0.91))

    log_error = _centered_tensor_error(rho, sigma, "log")
    linear_error = _centered_tensor_error(rho, sigma, "linear")
    cubic_error = _centered_tensor_error(rho, sigma, "cubic")

    return {
        "classification": "CONTINUOUS_UNIVERSAL_SCALAR_FUNCTIONAL_CALCULUS_PLUS_CENTERED_TENSOR_DERIVATION_SELECTS_LOG_SHAPE",
        "status": "NEW_ASSUMPTION_NOT_FROZEN",
        "assumptions": [
            "one dimension-independent continuous scalar function f acts by functional calculus on every faithful finite-dimensional state",
            "the centered response obeys F(rho tensor sigma)=F(rho) tensor I + I tensor F(sigma)",
            "the response is nontrivial; central shifts are projectively irrelevant",
        ],
        "log_centered_tensor_error": log_error,
        "linear_centered_tensor_error": linear_error,
        "cubic_centered_tensor_error": cubic_error,
        "proof": {
            "centered_tensor_law_implies_scale_independent_pairwise_differences": True,
            "difference_identity": "f(x*y)-f(z*y)=f(x)-f(z)",
            "consequence": "f(x*y)-f(x)=c(y) independent of x",
            "multiplicative_cauchy": "c(y*z)=c(y)+c(z)",
            "continuity_reduces_multiplicative_cauchy_to_log": True,
            "result": "f(x)=alpha*log(x)+beta",
            "projective_shape": "[log(rho)]",
            "orientation_note": "alpha sign is not fixed by the tensor equation alone; positive-projective orientation requires alpha>0",
        },
        "boundary": (
            "This theorem does not follow from v15.04 covariance. The universal coordinatewise scalar functional-calculus "
            "assumption is strictly stronger than the general permutation-equivariant spectral assignment allowed there."
        ),
    }


def _frozen_dependency_audit(bindings: Dict[str, str]) -> dict:
    return {
        "classification": "NO_FROZEN_STATE_TO_SOURCE_COMPOSITION_SELECTOR",
        "archive_bindings": bindings,
        "archive_bindings_match_expected": bindings == EXPECTED_BINDINGS,
        "v13_04_polar_tensor_naturality": {
            "frozen_fact": "polar(C1 tensor C2)=polar(C1) tensor polar(C2)",
            "typed_object": "polar transport",
            "selects_state_to_source_response": False,
        },
        "v13_22_refinement_naturality": {
            "frozen_refinement": "R_tau(rho)=rho tensor tau",
            "source_rule": "SUPPLIED_P_TO_P_TENSOR_I",
            "two_step_composition": "tensor associativity",
            "state_to_source_functional_equation": False,
            "selects_a_of_r": False,
            "reason": (
                "P is an independent supplied source variable. The frozen naturality rule tells how that already-supplied P embeds "
                "under refinement; it does not define P=F(rho) or compare F(rho tensor tau) with F(rho)."
            ),
        },
        "v13_23_qrsl": {
            "status": "IRREDUCIBLE_RELATIVE_TO_CURRENT_FROZEN_ONTOLOGY",
            "relevance": "no canonical hidden refinement selector supplies the missing stronger state-composition law",
        },
        "v13_26_source_scale": {
            "absolute_source_scale_selected": False,
            "relevance": "PGRL has P->aP, t->t/a parameterization freedom",
        },
        "v14_03_projective_source": {
            "source_ray_is_supplied": True,
            "relevance": "the positive projective source ray selects a downstream dual ray conditionally but its origin remains upstream",
        },
        "v15_03_log_warning": {
            "pgrl_log_coordinate_selects_log_source_law": False,
            "frozen_stop_rule": "do not privilege log(rho) merely because PGRL uses log coordinates",
        },
        "v15_04_spectral_freedom": {
            "unique_a_of_r": False,
            "qubit_family": "F_traceless(rho)=a(r)(rho-I/2)",
        },
        "typed_distinction": (
            "composition of already-chosen source operators is not a state-to-source selector; "
            "a selector must constrain the map from state spectrum to source response before composition"
        ),
    }


def run_audit() -> dict:
    bindings = _archive_bindings()
    frozen = _frozen_dependency_audit(bindings)
    mono = _labeled_monoidal_controls()
    strong = _stronger_selector_boundary()

    nonselection_certified = bool(
        frozen["archive_bindings_match_expected"]
        and frozen["classification"] == "NO_FROZEN_STATE_TO_SOURCE_COMPOSITION_SELECTOR"
        and mono["all_three_monoidal"]
        and mono["all_three_projectively_distinct"]
        and strong["status"] == "NEW_ASSUMPTION_NOT_FROZEN"
        and strong["log_centered_tensor_error"] < 1e-12
        and strong["linear_centered_tensor_error"] > 1e-2
        and strong["cubic_centered_tensor_error"] > 1e-2
    )

    primary = adjudicate_gate(nonselection_certified, False)

    return {
        "version": "v15.05",
        "gate": "Frozen Composition-Law Audit / Monoidal Non-Selection and Log-Selector Boundary",
        "primary_outcome": primary,
        "secondary_outcome": "LOG_SHAPE_REQUIRES_NEW_FUNCTIONAL_CALCULUS_ASSUMPTION",
        "major_structural_result": True,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "frozen_dependency_audit": frozen,
        "labeled_monoidal_nonselection": mono,
        "stronger_selector_boundary": strong,
        "claim_boundary": {
            "frozen_monoidal_selector_found": False,
            "log_source_law_derived_from_frozen_ontology": False,
            "downstream_gravity_used_as_selector": False,
            "entropy_or_time_used_as_selector": False,
            "new_assumption_needed_for_log_selector": True,
            "physical_stress_energy_derived": False,
            "spacetime_or_einstein_equations_derived": False,
            "Pillar_3_closed": False,
        },
        "next_lawful_question": (
            "Is there an independently justified ontology-native reason to promote the source map to a universal scalar functional calculus, "
            "or another equally strong state-to-source law, without selecting it from downstream gravity behavior?"
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_audit(), indent=2, sort_keys=True))
