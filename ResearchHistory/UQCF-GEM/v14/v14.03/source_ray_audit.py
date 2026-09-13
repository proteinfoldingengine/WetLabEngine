#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
from scipy.linalg import expm


SEED = 1403
PRIMARY_SAMPLES = 64
FD_EPS = 1e-6
SOURCE_HERM_TOL = 1e-12
TANGENT_HERM_TOL = 2e-11
TANGENT_TRACE_TOL = 2e-11
FD_REL_TOL = 2e-7
HIDDEN_REL_TOL = 1e-10
BOUNDARY_TOL = 2e-9
NULL_REL_TOL = 1e-9
PROJECTIVE_TOL = 2e-9
GAUGE_TOL = 2e-9
SCALES = (0.2, 0.5, 2.0, 5.0, 11.0)
SHIFTS = (-3.0, -0.7, 0.4, 2.5)


def _herm(a: np.ndarray) -> np.ndarray:
    return (a + a.conj().T) / 2


def _rel_matrix_error(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(1.0, float(np.linalg.norm(a)), float(np.linalg.norm(b))))


def _source_hash(sources: np.ndarray) -> str:
    a = np.ascontiguousarray(np.asarray(sources, dtype=np.complex128))
    return hashlib.sha256(a.view(np.float64).tobytes()).hexdigest()


def load_v1402() -> ModuleType:
    repo_root = Path(__file__).resolve().parents[4]
    path = repo_root / "ResearchHistory" / "UQCF-GEM" / "v14" / "v14.02" / "dual_normal_audit.py"
    if not path.exists():
        raise FileNotFoundError(f"v14.02 audit not found: {path}")
    spec = importlib.util.spec_from_file_location("uqcf_v1402_dual_normal", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load v14.02 audit: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_configuration(v1402: ModuleType, name: str) -> dict[str, Any]:
    lab = v1402.load_archived_lab()
    cfg = v1402.build_primary_configuration(lab, name)
    return {
        **cfg,
        "lab": lab,
        "L": np.asarray(cfg["state"]["L"], dtype=complex),
        "X0": np.asarray(cfg["X0"], dtype=complex),
        "modes": np.asarray(cfg["modes"], dtype=complex),
    }


def _log_mean_matrix(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    pi = p[:, None]
    pj = p[None, :]
    logdiff = np.log(pi) - np.log(pj)
    diff = pi - pj
    out = np.empty_like(logdiff)
    near = np.abs(logdiff) < 1e-13
    out[near] = ((pi + pj) / 2.0)[near]
    out[~near] = diff[~near] / logdiff[~near]
    return out


def pgrl_tangent(X0: np.ndarray, P: np.ndarray) -> np.ndarray:
    X0 = _herm(np.asarray(X0, dtype=complex))
    P = _herm(np.asarray(P, dtype=complex))
    p, U = np.linalg.eigh(X0)
    if p[0] <= 0:
        raise ArithmeticError("PGRL tangent requires faithful X0")
    Phat = U.conj().T @ P @ U
    lm = _log_mean_matrix(p)
    raw = lm * Phat
    mean = float(np.real(np.trace(X0 @ P)))
    idx = np.diag_indices(len(p))
    raw[idx] -= p * mean
    dotX = _herm(U @ raw @ U.conj().T)
    return dotX


def pgrl_state(X0: np.ndarray, P: np.ndarray, s: float) -> np.ndarray:
    X0 = _herm(np.asarray(X0, dtype=complex))
    P = _herm(np.asarray(P, dtype=complex))
    p, U = np.linalg.eigh(X0)
    if p[0] <= 0:
        raise ArithmeticError("PGRL state requires faithful X0")
    logX0 = U @ np.diag(np.log(p)) @ U.conj().T
    E = expm(_herm(logX0 + float(s) * P))
    return _herm(E / np.trace(E))


def sample_sources(X0: np.ndarray, count: int, rng: np.random.Generator) -> np.ndarray:
    k = X0.shape[0]
    sources = []
    I = np.eye(k, dtype=complex)
    for _ in range(count):
        A = rng.standard_normal((k, k)) + 1j * rng.standard_normal((k, k))
        P = _herm(A)
        P = P - float(np.real(np.trace(X0 @ P))) * I
        n = float(np.linalg.norm(P))
        if n <= 1e-14:
            raise ArithmeticError("zero sampled source")
        P = P / n
        if np.linalg.norm(P - P.conj().T) >= SOURCE_HERM_TOL:
            raise ArithmeticError("sampled source lost Hermiticity")
        sources.append(P)
    return np.asarray(sources)


def project_hidden(modes: np.ndarray, dotX: np.ndarray) -> dict[str, Any]:
    coords = np.real(np.einsum("aij,ij->a", modes.conj(), dotX, optimize=True))
    V = _herm(np.einsum("a,aij->ij", coords, modes, optimize=True))
    vnorm = float(np.linalg.norm(V))
    dnorm = float(np.linalg.norm(dotX))
    threshold = HIDDEN_REL_TOL * max(1.0, dnorm)
    residual_coords = np.real(np.einsum("aij,ij->a", modes.conj(), dotX - V, optimize=True))
    idempotence_error = float(np.linalg.norm(residual_coords))
    if vnorm <= threshold:
        return {
            "classification": "ZERO_HIDDEN_SOURCE_COMPONENT",
            "coords": coords,
            "V": V,
            "hidden_norm": vnorm,
            "tangent_norm": dnorm,
            "threshold": float(threshold),
            "idempotence_error": idempotence_error,
            "unit_coords": None,
            "unit_matrix": None,
        }
    return {
        "classification": "NONZERO_HIDDEN_COMPONENT",
        "coords": coords,
        "V": V,
        "hidden_norm": vnorm,
        "tangent_norm": dnorm,
        "threshold": float(threshold),
        "idempotence_error": idempotence_error,
        "unit_coords": coords / vnorm,
        "unit_matrix": V / vnorm,
    }


def coordinate_covariant_radial_boundary(X0: np.ndarray, D: np.ndarray) -> dict[str, Any]:
    X0 = _herm(np.asarray(X0, dtype=complex))
    D = _herm(np.asarray(D, dtype=complex))
    p, U = np.linalg.eigh(X0)
    if p[0] <= 0:
        raise ArithmeticError("radial boundary requires faithful X0")
    inv_sqrt = U @ np.diag(1.0 / np.sqrt(p)) @ U.conj().T
    G = _herm(inv_sqrt @ D @ inv_sqrt)
    geigs = np.linalg.eigvalsh(G)
    if geigs[0] >= -1e-12:
        raise ArithmeticError(f"hidden tangent lacks negative generalized eigenvalue: {geigs[0]}")
    radius = float(-1.0 / geigs[0])
    Xstar = _herm(X0 + radius * D)
    evals, evecs = np.linalg.eigh(Xstar)
    norm2 = float(np.max(np.abs(evals)))
    scale = max(1.0, norm2)
    tau_null = NULL_REL_TOL * scale
    null_mask = np.abs(evals) <= tau_null
    nullity = int(np.sum(null_mask))
    second = float(evals[1]) if len(evals) > 1 else float("inf")
    simple = bool(nullity == 1 and second >= 100.0 * tau_null)
    sensitivity_nullities = {
        "half_tau": int(np.sum(np.abs(evals) <= 0.5 * tau_null)),
        "tau": nullity,
        "double_tau": int(np.sum(np.abs(evals) <= 2.0 * tau_null)),
    }
    return {
        "D": D,
        "radius": radius,
        "Xstar": Xstar,
        "evals": evals,
        "evecs": evecs,
        "norm2": norm2,
        "tau_null": float(tau_null),
        "nullity": nullity,
        "simple": simple,
        "near_degenerate": not simple,
        "stable_nullity": len(set(sensitivity_nullities.values())) == 1,
        "sensitivity_nullities": sensitivity_nullities,
        "min_eigenvalue": float(evals[0]),
        "second_smallest_eigenvalue": second,
        "psd_residual": float(abs(evals[0])),
        "psd_violation": float(max(0.0, -evals[0])),
    }


def oriented_dual_representative(X0: np.ndarray, modes: np.ndarray, boundary: dict[str, Any], normal: dict[str, Any]) -> np.ndarray | None:
    g = normal.get("representative_g")
    if g is None or normal.get("classification") != "RAY":
        return None
    NH = _herm(np.einsum("a,aij->ij", g, modes, optimize=True))
    center_disp = X0 - boundary["Xstar"]
    pairing = float(np.real(np.trace(NH.conj().T @ center_disp)))
    if pairing < 0:
        NH = -NH
    n = float(np.linalg.norm(NH))
    if n <= 1e-12:
        return None
    return NH / n


def source_contact(v1402: ModuleType, cfg: dict[str, Any], P: np.ndarray, certify_base_formula: bool = True) -> dict[str, Any]:
    X0 = cfg["X0"]
    modes = cfg["modes"]
    dotX = pgrl_tangent(X0, P)
    hidden = project_hidden(modes, dotX)
    out: dict[str, Any] = {
        "dotX": dotX,
        "hidden": hidden,
        "boundary": None,
        "normal": None,
        "dual_rep": None,
        "base_formula_relative_error": 0.0,
    }
    if hidden["classification"] == "ZERO_HIDDEN_SOURCE_COMPONENT":
        return out
    D = hidden["unit_matrix"]
    boundary = coordinate_covariant_radial_boundary(X0, D)
    if certify_base_formula:
        ref = v1402.radial_boundary(X0, modes, hidden["unit_coords"])
        out["base_formula_relative_error"] = _rel_matrix_error(boundary["Xstar"], ref["Xstar"])
        out["base_formula_relative_error"] = max(
            out["base_formula_relative_error"],
            float(abs(boundary["radius"] - ref["radius"]) / max(1.0, abs(boundary["radius"]), abs(ref["radius"]))),
        )
    normal = v1402.normal_cone_audit(boundary, modes)
    dual_rep = oriented_dual_representative(X0, modes, boundary, normal)
    out.update({"boundary": boundary, "normal": normal, "dual_rep": dual_rep})
    return out


def _fd_error(X0: np.ndarray, P: np.ndarray, dotX: np.ndarray) -> float:
    fd = (pgrl_state(X0, P, FD_EPS) - pgrl_state(X0, P, -FD_EPS)) / (2.0 * FD_EPS)
    return _rel_matrix_error(_herm(fd), dotX)


def _dual_drift(A: np.ndarray, B: np.ndarray) -> float:
    dot = float(np.real(np.trace(A.conj().T @ B)))
    return float(max(0.0, 1.0 - dot))


def projective_invariance_audit(v1402: ModuleType, cfg: dict[str, Any], P: np.ndarray, base: dict[str, Any]) -> dict[str, float]:
    if base["hidden"]["classification"] == "ZERO_HIDDEN_SOURCE_COMPONENT":
        return {"tangent_scaling_error": 0.0, "hidden_direction_drift": 0.0, "boundary_relative_drift": 0.0, "dual_ray_drift": 0.0}
    I = np.eye(P.shape[0], dtype=complex)
    max_tangent = 0.0
    max_hidden = 0.0
    max_boundary = 0.0
    max_dual = 0.0
    for a in SCALES:
        for b in SHIFTS:
            P2 = a * P + b * I
            c2 = source_contact(v1402, cfg, P2, certify_base_formula=False)
            max_tangent = max(max_tangent, _rel_matrix_error(c2["dotX"], a * base["dotX"]))
            if c2["hidden"]["classification"] != "NONZERO_HIDDEN_COMPONENT" or c2["dual_rep"] is None:
                return {"tangent_scaling_error": max_tangent, "hidden_direction_drift": float("inf"), "boundary_relative_drift": float("inf"), "dual_ray_drift": float("inf")}
            max_hidden = max(max_hidden, _rel_matrix_error(c2["hidden"]["unit_matrix"], base["hidden"]["unit_matrix"]))
            max_boundary = max(max_boundary, _rel_matrix_error(c2["boundary"]["Xstar"], base["boundary"]["Xstar"]))
            max_dual = max(max_dual, _dual_drift(c2["dual_rep"], base["dual_rep"]))
    return {
        "tangent_scaling_error": float(max_tangent),
        "hidden_direction_drift": float(max_hidden),
        "boundary_relative_drift": float(max_boundary),
        "dual_ray_drift": float(max_dual),
    }


def _deterministic_unitaries(k: int, seed: int, count: int = 8) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(count):
        Z = rng.standard_normal((k, k)) + 1j * rng.standard_normal((k, k))
        Q, R = np.linalg.qr(Z)
        d = np.diag(R)
        phases = np.ones_like(d, dtype=complex)
        nz = np.abs(d) > 1e-14
        phases[nz] = d[nz] / np.abs(d[nz])
        Q = Q @ np.diag(phases.conj())
        out.append(Q)
    return out


def _gauge_contexts(cfg: dict[str, Any], seed: int) -> list[dict[str, Any]]:
    contexts = []
    for U in _deterministic_unitaries(cfg["support_dimension"], seed, 8):
        contexts.append({
            "U": U,
            "X0": _herm(U @ cfg["X0"] @ U.conj().T),
            "modes": np.asarray([_herm(U @ q @ U.conj().T) for q in cfg["modes"]]),
        })
    return contexts


def support_coordinate_covariance_audit(v1402: ModuleType, cfg: dict[str, Any], P: np.ndarray, base: dict[str, Any], contexts: list[dict[str, Any]]) -> float:
    if base["hidden"]["classification"] == "ZERO_HIDDEN_SOURCE_COMPONENT":
        return 0.0
    max_err = 0.0
    for ctx in contexts:
        U = ctx["U"]
        cfg2 = {**cfg, "X0": ctx["X0"], "modes": ctx["modes"]}
        P2 = _herm(U @ P @ U.conj().T)
        c2 = source_contact(v1402, cfg2, P2, certify_base_formula=False)
        if c2["hidden"]["classification"] != "NONZERO_HIDDEN_COMPONENT" or c2["dual_rep"] is None:
            return float("inf")
        max_err = max(max_err, _rel_matrix_error(c2["dotX"], U @ base["dotX"] @ U.conj().T))
        max_err = max(max_err, _rel_matrix_error(c2["hidden"]["V"], U @ base["hidden"]["V"] @ U.conj().T))
        max_err = max(max_err, _rel_matrix_error(c2["boundary"]["Xstar"], U @ base["boundary"]["Xstar"] @ U.conj().T))
        max_err = max(max_err, _rel_matrix_error(c2["dual_rep"], U @ base["dual_rep"] @ U.conj().T))
    return float(max_err)


def _source_from_tangent(X0: np.ndarray, target: np.ndarray) -> np.ndarray:
    X0 = _herm(X0)
    target = _herm(target)
    target = target - np.trace(target) * np.eye(target.shape[0]) / target.shape[0]
    p, U = np.linalg.eigh(X0)
    Th = U.conj().T @ target @ U
    lm = _log_mean_matrix(p)
    Ph = Th / lm
    P = _herm(U @ Ph @ U.conj().T)
    P = P - float(np.real(np.trace(X0 @ P))) * np.eye(P.shape[0])
    return P


def engineered_controls(v1402: ModuleType, cfg: dict[str, Any]) -> dict[str, Any]:
    k = cfg["support_dimension"]
    I = np.eye(k, dtype=complex)
    identity_tangent = pgrl_tangent(cfg["X0"], I)
    identity_control = {
        "classification": "ZERO_PGRL_TANGENT" if np.linalg.norm(identity_tangent) < TANGENT_HERM_TOL else "FAILED",
        "tangent_norm": float(np.linalg.norm(identity_tangent)),
    }

    target_hidden = _herm(cfg["modes"][0])
    P_hidden = _source_from_tangent(cfg["X0"], target_hidden)
    hidden_contact = source_contact(v1402, cfg, P_hidden, certify_base_formula=True)
    hidden_active = {
        "classification": hidden_contact["hidden"]["classification"],
        "hidden_norm": float(hidden_contact["hidden"]["hidden_norm"]),
        "tangent_target_error": _rel_matrix_error(hidden_contact["dotX"], target_hidden),
    }

    visible_seed = np.zeros((k, k), dtype=complex)
    visible_seed[0, 0] = 1.0
    visible_seed[1, 1] = -1.0
    proj = project_hidden(cfg["modes"], visible_seed)
    target_visible = _herm(visible_seed - proj["V"])
    target_visible -= np.trace(target_visible) * I / k
    if np.linalg.norm(target_visible) <= 1e-12:
        visible_control = {"classification": "NOT_CONSTRUCTED", "reason": "deterministic visible seed projected to zero"}
    else:
        target_visible /= np.linalg.norm(target_visible)
        P_visible = _source_from_tangent(cfg["X0"], target_visible)
        visible_contact = source_contact(v1402, cfg, P_visible, certify_base_formula=True)
        visible_control = {
            "classification": visible_contact["hidden"]["classification"],
            "hidden_norm": float(visible_contact["hidden"]["hidden_norm"]),
            "tangent_target_error": _rel_matrix_error(visible_contact["dotX"], target_visible),
        }
    return {
        "identity_source_control": identity_control,
        "hidden_active_control": hidden_active,
        "visible_only_tangent_control": visible_control,
    }


def provenance_audit() -> dict[str, Any]:
    return {
        "status": "PROVENANCE_SOURCE_TYPE_MISMATCH",
        "reason": "Frozen Genesis/provenance/source-grading objects certify origin, retained amount/flow, and compatibility but do not return the 25-dimensional support-coefficient Hermitian operator ray required by this archived compatibility fiber; no certified natural map between those typed spaces is present.",
        "random_survey_is_provenance_evidence": False,
    }


def _sample_record(contact: dict[str, Any], fd_error: float, projective: dict[str, float], gauge_error: float) -> dict[str, Any]:
    hidden = contact["hidden"]
    rec: dict[str, Any] = {
        "hidden_classification": hidden["classification"],
        "tangent_norm": float(hidden["tangent_norm"]),
        "hidden_norm": float(hidden["hidden_norm"]),
        "finite_difference_relative_error": float(fd_error),
        "projection_idempotence_error": float(hidden["idempotence_error"]),
        "base_boundary_formula_relative_error": float(contact["base_formula_relative_error"]),
        "projective_hidden_direction_drift": float(projective["hidden_direction_drift"]),
        "projective_boundary_relative_drift": float(projective["boundary_relative_drift"]),
        "projective_dual_ray_drift": float(projective["dual_ray_drift"]),
        "support_coordinate_covariance_error": float(gauge_error),
    }
    if contact["boundary"] is not None:
        rec.update({
            "boundary_radius": float(contact["boundary"]["radius"]),
            "boundary_simple": bool(contact["boundary"]["simple"]),
            "boundary_nullity": int(contact["boundary"]["nullity"]),
            "boundary_psd_residual": float(contact["boundary"]["psd_residual"]),
            "normal_classification": contact["normal"]["classification"],
            "normal_span_rank": int(contact["normal"]["span_rank"]),
        })
    return rec


def run_audit() -> dict[str, Any]:
    v1402 = load_v1402()
    configs = {name: build_configuration(v1402, name) for name in ("V_A", "V_B")}
    rng = np.random.default_rng(SEED)
    sources = {name: sample_sources(configs[name]["X0"], PRIMARY_SAMPLES, rng) for name in ("V_A", "V_B")}
    gauge_contexts = {
        "V_A": _gauge_contexts(configs["V_A"], 14031),
        "V_B": _gauge_contexts(configs["V_B"], 14032),
    }

    max_tangent_herm = 0.0
    max_tangent_trace = 0.0
    max_fd = 0.0
    max_base_formula = 0.0
    max_proj_tangent = 0.0
    max_proj_hidden = 0.0
    max_proj_boundary = 0.0
    max_proj_dual = 0.0
    max_gauge = 0.0
    max_boundary_psd = 0.0
    max_projection_idempotence = 0.0
    total_zero_hidden = 0
    total_nonzero = 0
    total_simple_ray = 0
    unresolved = 0
    nonunique = 0
    survey: dict[str, Any] = {}

    for name in ("V_A", "V_B"):
        cfg = configs[name]
        records = []
        zero_hidden = 0
        nonzero = 0
        simple_ray = 0
        for P in sources[name]:
            contact = source_contact(v1402, cfg, P, certify_base_formula=True)
            dotX = contact["dotX"]
            tangent_herm = float(np.linalg.norm(dotX - dotX.conj().T))
            tangent_trace = float(abs(np.trace(dotX)))
            fd_error = _fd_error(cfg["X0"], P, dotX)
            proj = projective_invariance_audit(v1402, cfg, P, contact)
            gauge_error = support_coordinate_covariance_audit(v1402, cfg, P, contact, gauge_contexts[name])

            max_tangent_herm = max(max_tangent_herm, tangent_herm)
            max_tangent_trace = max(max_tangent_trace, tangent_trace)
            max_fd = max(max_fd, fd_error)
            max_base_formula = max(max_base_formula, float(contact["base_formula_relative_error"]))
            max_proj_tangent = max(max_proj_tangent, proj["tangent_scaling_error"])
            max_proj_hidden = max(max_proj_hidden, proj["hidden_direction_drift"])
            max_proj_boundary = max(max_proj_boundary, proj["boundary_relative_drift"])
            max_proj_dual = max(max_proj_dual, proj["dual_ray_drift"])
            max_gauge = max(max_gauge, gauge_error)
            max_projection_idempotence = max(max_projection_idempotence, contact["hidden"]["idempotence_error"])

            numerical_bad = (
                tangent_herm >= TANGENT_HERM_TOL
                or tangent_trace >= TANGENT_TRACE_TOL
                or fd_error >= FD_REL_TOL
                or contact["base_formula_relative_error"] >= BOUNDARY_TOL
                or proj["hidden_direction_drift"] >= PROJECTIVE_TOL
                or proj["boundary_relative_drift"] >= PROJECTIVE_TOL
                or proj["dual_ray_drift"] >= PROJECTIVE_TOL
                or gauge_error >= GAUGE_TOL
            )

            if contact["hidden"]["classification"] == "ZERO_HIDDEN_SOURCE_COMPONENT":
                zero_hidden += 1
                total_zero_hidden += 1
            else:
                nonzero += 1
                total_nonzero += 1
                b = contact["boundary"]
                n = contact["normal"]
                max_boundary_psd = max(max_boundary_psd, b["psd_residual"])
                if b["psd_residual"] >= BOUNDARY_TOL or not b["stable_nullity"]:
                    numerical_bad = True
                if n["classification"] == "NONUNIQUE_NORMAL_CONE":
                    nonunique += 1
                if b["simple"] and n["classification"] == "RAY" and contact["dual_rep"] is not None:
                    simple_ray += 1
                    total_simple_ray += 1
                elif n["classification"] != "NONUNIQUE_NORMAL_CONE":
                    numerical_bad = True
            if numerical_bad or not np.isfinite(gauge_error):
                unresolved += 1
            records.append(_sample_record(contact, fd_error, proj, gauge_error))

        survey[name] = {
            "sample_count": PRIMARY_SAMPLES,
            "support_dimension": cfg["support_dimension"],
            "hidden_dimension": cfg["hidden_dimension"],
            "source_sha256": _source_hash(sources[name]),
            "zero_hidden_source_count": zero_hidden,
            "nonzero_hidden_contact_count": nonzero,
            "simple_ray_contact_count": simple_ray,
            "sample_records": records,
        }

    controls = engineered_controls(v1402, configs["V_A"])
    provenance = provenance_audit()

    if unresolved > 0:
        gate_outcome = "UNRESOLVED_NUMERICAL_SOURCE_LIFT"
    elif nonunique > 0:
        gate_outcome = "SOURCE_TO_BOUNDARY_NONUNIQUE"
    elif total_nonzero == 0:
        gate_outcome = "NO_HIDDEN_SOURCE_CONTACT"
    elif total_simple_ray == total_nonzero:
        gate_outcome = "PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY"
    else:
        gate_outcome = "UNRESOLVED_NUMERICAL_SOURCE_LIFT"

    return {
        "version": "v14.03",
        "seed": SEED,
        "construction": {
            "archived_lab_path": "Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py",
            "v1402_dependency": "ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py",
            "uses_full_support_state": True,
            "uses_full_hidden_kernel": True,
            "uses_visualization_section": False,
            "boundary_is_hidden_tangent_radial_contact_not_pgrl_crossing": True,
        },
        "survey": survey,
        "primary_sample_count": 2 * PRIMARY_SAMPLES,
        "zero_hidden_source_count": total_zero_hidden,
        "nonzero_hidden_contact_count": total_nonzero,
        "simple_ray_contact_count": total_simple_ray,
        "unresolved_numerical_count": unresolved,
        "nonunique_contact_count": nonunique,
        "max_tangent_hermiticity_residual": float(max_tangent_herm),
        "max_tangent_trace_abs": float(max_tangent_trace),
        "max_finite_difference_relative_error": float(max_fd),
        "max_base_boundary_formula_relative_error": float(max_base_formula),
        "max_projective_tangent_scaling_error": float(max_proj_tangent),
        "max_projective_hidden_direction_drift": float(max_proj_hidden),
        "max_projective_boundary_relative_drift": float(max_proj_boundary),
        "max_projective_dual_ray_drift": float(max_proj_dual),
        "max_support_coordinate_covariance_error": float(max_gauge),
        "max_boundary_psd_residual": float(max_boundary_psd),
        "max_hidden_projection_idempotence_error": float(max_projection_idempotence),
        "identity_source_control": controls["identity_source_control"],
        "hidden_active_control": controls["hidden_active_control"],
        "visible_only_tangent_control": controls["visible_only_tangent_control"],
        "provenance_source_ray_status": provenance["status"],
        "provenance_audit": provenance,
        "gate_outcome": gate_outcome,
        "claim_scope": "supplied projective support-space PGRL source rays mapped through their full-state hidden tangent component to radial compatibility-boundary contacts and v14.02 local dual rays",
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
