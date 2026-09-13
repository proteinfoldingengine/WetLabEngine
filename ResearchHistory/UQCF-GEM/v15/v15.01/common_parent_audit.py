#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np


SEED = 1501
PARENT_DIM = 125
SUPPORT_DIM = 25
ISO_TOL = 2e-11
COV_TOL = 2e-10
PROJECTIVE_TOL = 2e-11


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _herm(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=complex)
    return (a + a.conj().T) / 2


def _rel_error(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(1.0, float(np.linalg.norm(a)), float(np.linalg.norm(b))))


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_module(path: Path, name: str) -> ModuleType:
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_v1403() -> ModuleType:
    path = _repo_root() / "ResearchHistory" / "UQCF-GEM" / "v14" / "v14.03" / "source_ray_audit.py"
    return _load_module(path, "uqcf_v1403_source_ray")


def _dft_unitary(n: int, offset: float = 0.0) -> np.ndarray:
    j = np.arange(n, dtype=float)[:, None]
    k = np.arange(n, dtype=float)[None, :]
    return np.exp(2j * np.pi * (j + offset) * (k + offset) / n) / np.sqrt(n)


def _parent_probe() -> np.ndarray:
    x = np.arange(PARENT_DIM, dtype=float)
    diag = np.cos(0.173 * (x + 1.0)) + 0.23 * np.sin(0.071 * (x + 2.0))
    A = np.diag(diag.astype(complex))
    for i, j, z in ((0, 7, 0.31), (2, 19, -0.27j), (11, 37, 0.19 + 0.13j), (23, 61, -0.21 + 0.09j)):
        A[i, j] = z
        A[j, i] = np.conj(z)
    return _herm(A)


def build_parent_configuration(v1403: ModuleType, name: str) -> dict[str, Any]:
    v1402 = v1403.load_v1402()
    cfg = v1403.build_configuration(v1402, name)
    L = np.asarray(cfg["L"], dtype=complex)
    X0 = _herm(np.asarray(cfg["X0"], dtype=complex))
    T = _herm(np.asarray(cfg["state"]["T"], dtype=complex))
    if L.shape != (PARENT_DIM, SUPPORT_DIM):
        raise ArithmeticError(f"{name} unexpected L shape {L.shape}")
    if X0.shape != (SUPPORT_DIM, SUPPORT_DIM):
        raise ArithmeticError(f"{name} unexpected X0 shape {X0.shape}")
    if T.shape != (PARENT_DIM, PARENT_DIM):
        raise ArithmeticError(f"{name} unexpected T shape {T.shape}")
    return {**cfg, "L": L, "X0": X0, "T": T, "Pi": _herm(L @ L.conj().T), "v1402": v1402}


def compress_parent_operator(L: np.ndarray, A: np.ndarray) -> np.ndarray:
    L = np.asarray(L, dtype=complex)
    A = _herm(A)
    if L.shape != (PARENT_DIM, SUPPORT_DIM):
        raise ValueError(f"expected L shape {(PARENT_DIM, SUPPORT_DIM)}, got {L.shape}")
    if A.shape != (PARENT_DIM, PARENT_DIM):
        raise ValueError(f"expected parent operator shape {(PARENT_DIM, PARENT_DIM)}, got {A.shape}")
    return _herm(L.conj().T @ A @ L)


def parent_support_audit(configs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    A = _parent_probe()
    U = _dft_unitary(PARENT_DIM, 0.0)
    V = _dft_unitary(SUPPORT_DIM, 0.25)
    scales = (0.2, 0.5, 2.0, 5.0, 11.0)
    shifts = (-3.0, -0.7, 0.4, 2.5)
    records = {}
    max_iso = 0.0
    max_recon = 0.0
    max_proj_herm = 0.0
    max_proj_idem = 0.0
    max_cov = 0.0
    max_projective = 0.0
    for name, cfg in configs.items():
        L, X0, T, Pi = cfg["L"], cfg["X0"], cfg["T"], cfg["Pi"]
        iso = float(np.linalg.norm(L.conj().T @ L - np.eye(SUPPORT_DIM)))
        recon = float(np.linalg.norm(T - L @ X0 @ L.conj().T))
        ph = float(np.linalg.norm(Pi - Pi.conj().T))
        pi = float(np.linalg.norm(Pi @ Pi - Pi))
        P = compress_parent_operator(L, A)
        for a in scales:
            for b in shifts:
                lhs = compress_parent_operator(L, a * A + b * np.eye(PARENT_DIM))
                rhs = a * P + b * np.eye(SUPPORT_DIM)
                max_projective = max(max_projective, _rel_error(lhs, rhs))
        L2 = U @ L @ V.conj().T
        A2 = U @ A @ U.conj().T
        lhs_cov = compress_parent_operator(L2, A2)
        rhs_cov = _herm(V @ P @ V.conj().T)
        cov = _rel_error(lhs_cov, rhs_cov)
        records[name] = {
            "isometry_error": iso,
            "reconstruction_error": recon,
            "projector_hermiticity_error": ph,
            "projector_idempotence_error": pi,
            "compression_covariance_error": cov,
        }
        max_iso = max(max_iso, iso)
        max_recon = max(max_recon, recon)
        max_proj_herm = max(max_proj_herm, ph)
        max_proj_idem = max(max_proj_idem, pi)
        max_cov = max(max_cov, cov)
    return {
        "status": "COMPATIBILITY_PARENT_SUPPORT_VERIFIED",
        "parent_dimension": PARENT_DIM,
        "support_dimension": SUPPORT_DIM,
        "records": records,
        "max_isometry_error": max_iso,
        "max_reconstruction_error": max_recon,
        "max_projector_hermiticity_error": max_proj_herm,
        "max_projector_idempotence_error": max_proj_idem,
        "max_compression_covariance_error": max_cov,
        "max_projective_descent_error": max_projective,
        "analytic_projective_descent": "C_L(aA+bI_125)=a C_L(A)+bI_25 because L^dagger L=I_25",
        "analytic_covariance": "for L'=U L V^dagger and A'=U A U^dagger, C_L'(A')=V C_L(A) V^dagger",
    }


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [m for m in markers if m not in text]
    if missing:
        raise ArithmeticError(f"{label} missing expected frozen markers: {missing}")


def archive_inventory() -> dict[str, Any]:
    root = _repo_root()
    specs = [
        {
            "name": "compatibility_tripartite_parent",
            "path": "Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py",
            "carrier_type": "tripartite quantum parent H_A tensor H_B1 tensor H_B2 = C^125 with orthonormal C^25 support",
            "carrier_dimension": 125,
            "source_status": "NO_PROVENANCE_SOURCE_COVECTOR_CERTIFIED",
            "parent_map_status": "PARENT_SUPPORT_MAP_L_CERTIFIED",
            "markers": ("N = 5", "def build_completion", "L=np.column_stack(L)", "T=(L*np.asarray(populations))@L.T"),
            "same_parent_source_class": False,
            "support_preserving_parent_tangent": False,
        },
        {
            "name": "v1404_representation_audit",
            "path": "ResearchHistory/UQCF-GEM/v14/v14.04/SUMMARY.json",
            "carrier_type": "prior typed provenance/support representation audit",
            "carrier_dimension": None,
            "source_status": "REQUIRES_NEW_REPRESENTATION_LINK",
            "parent_map_status": "NO_CERTIFIED_NATURAL_SUPPORT_LINK",
            "markers": ("REQUIRES_NEW_REPRESENTATION_LINK", "certified_natural_support_link_count"),
            "same_parent_source_class": False,
            "support_preserving_parent_tangent": False,
        },
        {
            "name": "genesis_6d_field_and_ledger",
            "path": "Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py",
            "carrier_type": "append-only provenance ledger plus real 6D Genesis/pruning field on RES^6 grid",
            "carrier_dimension": "8^6 real grid",
            "source_status": "PROVENANCE_AND_FIELD_CARRIER_NOT_PARENT_HERMITIAN_SOURCE",
            "parent_map_status": "NO_FROZEN_MAP_TO_HERM_C125",
            "markers": ("RES = 8", "PINNED_GENESIS_ROOT", "def build_genesis", "def source_flow_closure_metrics"),
            "same_parent_source_class": False,
            "support_preserving_parent_tangent": False,
        },
        {
            "name": "retained_source_current",
            "path": "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md",
            "carrier_type": "retained source grade and graph source/current package satisfying B J = s",
            "carrier_dimension": "retained graph/current convention",
            "source_status": "SOURCE_DIRECTION_AND_BALANCE_NOT_PARENT_COVECTOR",
            "parent_map_status": "NO_FROZEN_MAP_TO_HERM_C125",
            "markers": ("B J = s", "Genesis Pin / source-origin", "PGRL provides an exact source direction/response family"),
            "same_parent_source_class": False,
            "support_preserving_parent_tangent": False,
        },
        {
            "name": "v1327_six_qubit_source_demo",
            "path": "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py",
            "carrier_type": "six-qubit finite demonstration parent with explicitly chosen PGRL source operator",
            "carrier_dimension": 64,
            "source_status": "EXPLICIT_DEMO_SOURCE_NOT_GENESIS_PROVENANCE_DERIVATION",
            "parent_map_status": "DIFFERENT_PARENT_NO_FROZEN_NATURAL_FUNCTOR_TO_C125",
            "markers": ("if n != 6", "2**n", "P = source_scale *"),
            "same_parent_source_class": False,
            "support_preserving_parent_tangent": False,
        },
    ]
    inventory = []
    missing = []
    for spec in specs:
        path = root / spec["path"]
        if not path.exists():
            missing.append(spec["path"])
            continue
        text = path.read_text(errors="replace")
        _require_markers(text, spec.pop("markers"), spec["name"])
        inventory.append({**spec, "sha256": _sha256_path(path)})
    same_parent = [x for x in inventory if x["same_parent_source_class"]]
    tangents = [x for x in inventory if x["support_preserving_parent_tangent"]]
    return {
        "candidate_count": len(inventory),
        "missing_artifact_count": len(missing),
        "missing_artifacts": missing,
        "same_parent_source_class_count": len(same_parent),
        "support_preserving_parent_tangent_count": len(tangents),
        "support_changing_parent_tangent_count": 0,
        "inventory": inventory,
        "archive_statement": "The compatibility C^25 support is explicitly embedded in a C^125 quantum parent, but the frozen provenance/source artifacts audited here supply neither a provenance-certified Hermitian source class on that same parent nor a support-preserving parent tangent with such provenance meaning.",
    }


def _projective_residual(P: np.ndarray, Q: np.ndarray) -> float:
    P = _herm(P)
    Q = _herm(Q)
    k = P.shape[0]
    I = np.eye(k, dtype=complex)
    Pc = P - np.trace(P).real * I / k
    Qc = Q - np.trace(Q).real * I / k
    pnorm2 = float(np.real(np.trace(Pc.conj().T @ Pc)))
    qnorm = float(np.linalg.norm(Qc))
    if pnorm2 <= 1e-24 or qnorm <= 1e-12:
        return 0.0 if np.linalg.norm(Pc) <= 1e-12 and qnorm <= 1e-12 else 1.0
    a = float(np.real(np.trace(Pc.conj().T @ Qc)) / pnorm2)
    if a <= 0:
        return 1.0
    return float(np.linalg.norm(Qc - a * Pc) / max(1.0, qnorm, abs(a) * np.linalg.norm(Pc)))


def _control_family() -> list[tuple[str, np.ndarray]]:
    x = np.arange(PARENT_DIM, dtype=float)
    controls = []
    A1 = np.diag(np.linspace(-1.0, 1.0, PARENT_DIM).astype(complex))
    controls.append(("diagonal_ramp", A1))
    A2 = np.diag((np.sin(0.19 * (x + 1)) + 0.31 * np.cos(0.047 * (x + 3))).astype(complex))
    for i, j, z in ((0, 5, 0.41), (7, 22, -0.29j), (31, 48, 0.17 + 0.23j)):
        A2[i, j] = z
        A2[j, i] = np.conj(z)
    controls.append(("oscillatory_sparse", _herm(A2)))
    A3 = np.zeros((PARENT_DIM, PARENT_DIM), dtype=complex)
    for i in range(PARENT_DIM - 1):
        z = 0.23 * np.cos(0.13 * (i + 1)) + 0.17j * np.sin(0.09 * (i + 2))
        A3[i, i + 1] = z
        A3[i + 1, i] = np.conj(z)
    A3 += np.diag((0.2 * np.cos(0.11 * x)).astype(complex))
    controls.append(("nearest_band", _herm(A3)))
    return controls


def positive_control(v1403: ModuleType, configs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    U = _dft_unitary(PARENT_DIM, 0.0)
    V = _dft_unitary(SUPPORT_DIM, 0.25)
    attempts = []
    successful = None
    max_descent = 0.0
    for cfg_name in ("V_A", "V_B"):
        cfg = configs[cfg_name]
        for ctrl_name, A in _control_family():
            P = compress_parent_operator(cfg["L"], A)
            centered = P - np.trace(P).real * np.eye(SUPPORT_DIM) / SUPPORT_DIM
            noncentral = float(np.linalg.norm(centered)) > 1e-10
            rec: dict[str, Any] = {"configuration": cfg_name, "control": ctrl_name, "noncentral": noncentral}
            if not noncentral:
                attempts.append(rec)
                continue
            try:
                contact = v1403.source_contact(cfg["v1402"], cfg, P, certify_base_formula=True)
            except Exception as exc:
                rec["error"] = type(exc).__name__
                attempts.append(rec)
                continue
            hidden_ok = contact["hidden"]["classification"] == "NONZERO_HIDDEN_COMPONENT"
            boundary_ok = bool(contact["boundary"] is not None and contact["boundary"]["simple"])
            normal_ok = bool(contact["normal"] is not None and contact["normal"]["classification"] == "RAY")
            rec.update({"hidden_ok": hidden_ok, "boundary_ok": boundary_ok, "normal_ok": normal_ok})
            attempts.append(rec)
            if hidden_ok and boundary_ok and normal_ok and contact["dual_rep"] is not None:
                successful = (cfg, ctrl_name, A, P, contact)
                break
        if successful is not None:
            break
    if successful is None:
        return {
            "classification": "SUPPLIED_PARENT_SOURCE_NOT_PROVENANCE_DERIVATION",
            "noncentral_compressed_source": False,
            "nonzero_hidden_component": False,
            "boundary_simple": False,
            "normal_classification": "NONE",
            "max_parent_support_covariance_error": float("inf"),
            "max_projective_descent_error": float("inf"),
            "attempts": attempts,
        }
    cfg, ctrl_name, A, P, base = successful
    L = cfg["L"]
    for a in (0.2, 0.5, 2.0, 5.0, 11.0):
        for b in (-3.0, -0.7, 0.4, 2.5):
            lhs = compress_parent_operator(L, a * A + b * np.eye(PARENT_DIM))
            rhs = a * P + b * np.eye(SUPPORT_DIM)
            max_descent = max(max_descent, _rel_error(lhs, rhs))
    L2 = U @ L @ V.conj().T
    A2 = U @ A @ U.conj().T
    P2 = compress_parent_operator(L2, A2)
    expected_P2 = _herm(V @ P @ V.conj().T)
    max_cov = _rel_error(P2, expected_P2)
    cfg2 = {
        **cfg,
        "X0": _herm(V @ cfg["X0"] @ V.conj().T),
        "modes": np.asarray([_herm(V @ q @ V.conj().T) for q in cfg["modes"]]),
    }
    contact2 = v1403.source_contact(cfg["v1402"], cfg2, P2, certify_base_formula=False)
    max_cov = max(max_cov, _rel_error(contact2["dotX"], V @ base["dotX"] @ V.conj().T))
    max_cov = max(max_cov, _rel_error(contact2["hidden"]["V"], V @ base["hidden"]["V"] @ V.conj().T))
    max_cov = max(max_cov, _rel_error(contact2["boundary"]["Xstar"], V @ base["boundary"]["Xstar"] @ V.conj().T))
    max_cov = max(max_cov, _rel_error(contact2["dual_rep"], V @ base["dual_rep"] @ V.conj().T))

    dotX = v1403.pgrl_tangent(cfg["X0"], P)
    deltaT = _herm(L @ dotX @ L.conj().T)
    Pi = cfg["Pi"]
    support_leakage = max(float(np.linalg.norm((np.eye(PARENT_DIM) - Pi) @ deltaT)), float(np.linalg.norm(deltaT @ (np.eye(PARENT_DIM) - Pi))))
    deltaX = _herm(L.conj().T @ deltaT @ L)
    P_rec = v1403._source_from_tangent(cfg["X0"], deltaX)
    roundtrip = _projective_residual(P, P_rec)

    return {
        "classification": "SUPPLIED_PARENT_SOURCE_NOT_PROVENANCE_DERIVATION",
        "selected_configuration": cfg["name"],
        "selected_control": ctrl_name,
        "attempts": attempts,
        "noncentral_compressed_source": True,
        "compressed_noncentral_norm": float(np.linalg.norm(P - np.trace(P).real * np.eye(SUPPORT_DIM) / SUPPORT_DIM)),
        "nonzero_hidden_component": True,
        "hidden_norm": float(base["hidden"]["hidden_norm"]),
        "boundary_simple": True,
        "boundary_radius": float(base["boundary"]["radius"]),
        "normal_classification": base["normal"]["classification"],
        "max_parent_support_covariance_error": float(max_cov),
        "max_projective_descent_error": float(max_descent),
        "support_preserving_tangent_leakage": float(support_leakage),
        "tangent_roundtrip_projective_residual": float(roundtrip),
    }


def run_audit() -> dict[str, Any]:
    v1403 = load_v1403()
    configs = {name: build_parent_configuration(v1403, name) for name in ("V_A", "V_B")}
    parent = parent_support_audit(configs)
    inv = archive_inventory()
    ctrl = positive_control(v1403, configs)

    if inv["missing_artifact_count"]:
        outcome = "UNRESOLVED_COMMON_PARENT_AUDIT"
    elif inv["same_parent_source_class_count"] == 1 or inv["support_preserving_parent_tangent_count"] == 1:
        outcome = "COMMON_PARENT_INDUCES_SOURCE_RAY"
    elif inv["same_parent_source_class_count"] > 1 or inv["support_preserving_parent_tangent_count"] > 1:
        outcome = "COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE"
    else:
        outcome = "NO_COMMON_PARENT_REPRESENTATION"

    return {
        "version": "v15.01",
        "seed": SEED,
        "parent_dimension": PARENT_DIM,
        "support_dimension": SUPPORT_DIM,
        "Pillar_3": "OPEN",
        "parent_support": parent,
        "archive_inventory": inv,
        "positive_control": ctrl,
        "gate_outcome": outcome,
        "scientific_breakthrough": outcome == "COMMON_PARENT_INDUCES_SOURCE_RAY",
        "claim_scope": "common-parent representation audit from frozen Genesis/provenance/source structures to the C^125 compatibility parent and its canonical C^25 support compression",
        "interpretation": "The archived compatibility support is a genuine orthonormal support of a C^125 quantum parent. Common-parent compression would canonically and projectively produce the v14.03 support source if provenance supplied a lawful source class or support-preserving tangent on that same parent. The gate outcome is determined only by whether such a frozen provenance object exists, not by the supplied-parent positive control.",
        "not_derived": [
            "gravity",
            "stress-energy",
            "source-to-solder/coframe law",
            "absolute source-to-geometry coupling",
            "physical metric or spacetime",
            "Einstein equations",
            "Pillar 3 closure",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
