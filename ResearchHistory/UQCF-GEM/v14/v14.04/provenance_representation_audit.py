#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np

SEED = 1404
SUPPORT_DIM = 25
TWIRL_TOL = 2e-11
ISOMETRY_TOL = 2e-12
PGRL_NULL_TOL = 2e-11
PROJECTIVE_AMBIGUITY_TOL = 1e-4


def herm(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=complex)
    return (a + a.conj().T) / 2.0


def rel_matrix_error(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(1.0, float(np.linalg.norm(a)), float(np.linalg.norm(b))))


def load_v1403() -> ModuleType:
    repo_root = Path(__file__).resolve().parents[4]
    path = repo_root / "ResearchHistory" / "UQCF-GEM" / "v14" / "v14.03" / "source_ray_audit.py"
    if not path.exists():
        raise FileNotFoundError(f"v14.03 source-ray audit not found: {path}")
    spec = importlib.util.spec_from_file_location("uqcf_v1403_source_ray", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load v14.03 source-ray audit: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def projective_fit_residual(P: np.ndarray, Q: np.ndarray) -> dict[str, float]:
    """Fit Q ~= a P + b I in the v14.03 positive-projective equivalence class."""
    P = herm(P)
    Q = herm(Q)
    I = np.eye(P.shape[0], dtype=complex)

    def vec(A: np.ndarray) -> np.ndarray:
        return np.concatenate([A.real.ravel(), A.imag.ravel()])

    A = np.column_stack([vec(P), vec(I)])
    x, *_ = np.linalg.lstsq(A, vec(Q), rcond=None)
    a, b = map(float, x)
    fit = a * P + b * I
    residual = float(np.linalg.norm(Q - fit) / max(1.0, float(np.linalg.norm(Q)), float(np.linalg.norm(fit))))
    if a <= 0.0:
        residual = max(residual, 1.0)
    return {"a": a, "b": b, "residual": residual}


def heisenberg_weyl_twirl(P: np.ndarray) -> np.ndarray:
    """Exact finite unitary-1-design twirl for d=25 using all d^2 Weyl operators."""
    P = herm(P)
    d = P.shape[0]
    omega = np.exp(2j * np.pi / d)
    X = np.zeros((d, d), dtype=complex)
    for j in range(d):
        X[(j + 1) % d, j] = 1.0
    Z = np.diag(np.array([omega**j for j in range(d)], dtype=complex))
    Xpowers = [np.linalg.matrix_power(X, a) for a in range(d)]
    Zpowers = [np.linalg.matrix_power(Z, b) for b in range(d)]
    acc = np.zeros_like(P, dtype=complex)
    for a in range(d):
        Xa = Xpowers[a]
        for b in range(d):
            W = Xa @ Zpowers[b]
            acc += W @ P @ W.conj().T
    return herm(acc / float(d * d))


def _hadamard_mix(d: int, i: int = 0, j: int = 1) -> np.ndarray:
    U = np.eye(d, dtype=complex)
    s = 1.0 / np.sqrt(2.0)
    U[i, i] = s
    U[i, j] = s
    U[j, i] = s
    U[j, j] = -s
    return U


def _fourier_unitary(d: int) -> np.ndarray:
    jj, kk = np.meshgrid(np.arange(d), np.arange(d), indexing="ij")
    return np.exp(2j * np.pi * jj * kk / d) / np.sqrt(float(d))


def centrality_controls() -> dict[str, Any]:
    d = SUPPORT_DIM
    P1 = np.diag(np.linspace(-1.0, 1.0, d)).astype(complex)
    P2 = np.diag(np.arange(d, dtype=float)).astype(complex)
    for i in range(d - 1):
        P2[i, i + 1] += 0.37
        P2[i + 1, i] += 0.37
    P2 = herm(P2)
    probes = [P1, P2]
    units = [_hadamard_mix(d), _fourier_unitary(d)]

    twirl_errors: list[float] = []
    orbit_residuals: list[float] = []
    for P in probes:
        twirled = heisenberg_weyl_twirl(P)
        target = np.trace(P) * np.eye(d, dtype=complex) / d
        twirl_errors.append(rel_matrix_error(twirled, target))
        for U in units:
            Q = herm(U @ P @ U.conj().T)
            orbit_residuals.append(projective_fit_residual(P, Q)["residual"])

    central = 2.75 * np.eye(d, dtype=complex)
    central_invariance = max(rel_matrix_error(U @ central @ U.conj().T, central) for U in units)
    return {
        "weyl_design_size": d * d,
        "max_weyl_twirl_error": float(max(twirl_errors)),
        "min_noncentral_orbit_projective_residual": float(min(orbit_residuals)),
        "max_central_invariance_error": float(central_invariance),
        "noncentral_probe_count": len(probes),
        "unitary_orbit_control_count": len(probes) * len(units),
    }


def class_a_audit(v1403: ModuleType) -> dict[str, Any]:
    controls = centrality_controls()
    v1402 = v1403.load_v1402()
    cfg = v1403.build_configuration(v1402, "V_A")
    I = np.eye(SUPPORT_DIM, dtype=complex)
    norms = []
    for lam in (-3.5, -1.0, 0.2, 2.0, 11.0):
        dotX = v1403.pgrl_tangent(cfg["X0"], lam * I)
        norms.append(float(np.linalg.norm(dotX)))
    max_null = float(max(norms))
    return {
        "analytic_theorem": "SUPPORT_GAUGE_PROJECTIVE_CENTRALITY",
        "theorem_statement": (
            "If provenance is trivial under the full U(25) support-coordinate action and "
            "[U P U^dagger]_+=[P]_+ for every U, then every conjugate must lie in the real affine "
            "span of P and I and therefore commute with P. A noncentral Hermitian P admits a unitary "
            "mixing distinct eigenspaces for which U P U^dagger does not commute with P. Hence P is central; "
            "central representatives are PGRL-null."
        ),
        "central_only": True,
        "identity_pgrl_null": bool(max_null < PGRL_NULL_TOL),
        "max_identity_tangent_norm": max_null,
        **controls,
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def class_b_audit() -> dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[4]
    candidates = [
        {
            "name": "genesis_ledger_identity",
            "path": "Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py",
            "domain_type": "hash/root/event/witness append-only ledger",
            "transformation_law": "source-origin and ordered-lineage identity; no certified U(25) support action",
            "carrier_class": "gauge_trivial_identity_data",
        },
        {
            "name": "genesis_6d_field",
            "path": "Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py",
            "domain_type": "real 6D Genesis/pruning field on RES^6 grid",
            "transformation_law": "model-specific 6D grid/roll/pruning transformations",
            "carrier_class": "nontrivial_carrier",
        },
        {
            "name": "retained_source_grade",
            "path": "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md",
            "domain_type": "retained scalar/extensive source grade",
            "transformation_law": "positive retained-source scaling",
            "carrier_class": "gauge_trivial_scalar_data",
        },
        {
            "name": "retained_source_current",
            "path": "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md",
            "domain_type": "retained graph source/current package satisfying B J = s",
            "transformation_law": "graph balance/covariance inside the retained measurement convention",
            "carrier_class": "nontrivial_carrier",
        },
    ]

    explicit_link_markers = (
        "Herm(25)",
        "Hermitian support-source",
        "support-coefficient Hermitian",
        "source_ray_audit",
        "K_prov -> H_supp",
        "K_{\\rm prov}\\to\\mathcal H_{\\rm supp}",
    )
    missing: list[str] = []
    natural_links = 0
    nontrivial = 0
    inventory = []
    for c in candidates:
        path = repo_root / c["path"]
        if not path.exists():
            missing.append(c["path"])
            inventory.append({**c, "exists": False, "sha256": None, "support_map_status": "UNRESOLVED_MISSING_ARTIFACT"})
            continue
        text = path.read_text(errors="replace")
        marker_hits = [m for m in explicit_link_markers if m in text]
        support_map_status = "EXPLICIT_SUPPORT_LINK_REQUIRES_REVIEW" if marker_hits else "NONE_CERTIFIED"
        # No inventoried frozen artifact currently documents the required natural support intertwiner.
        if support_map_status == "EXPLICIT_SUPPORT_LINK_REQUIRES_REVIEW":
            natural_links += 1
        if c["carrier_class"] == "nontrivial_carrier":
            nontrivial += 1
        inventory.append({
            **c,
            "exists": True,
            "sha256": _sha256(path),
            "explicit_support_link_markers": marker_hits,
            "support_map_status": support_map_status,
        })

    # The marker scan is deliberately conservative; an explicit marker would stop automatic negative adjudication.
    return {
        "candidate_count": len(candidates),
        "missing_artifact_count": len(missing),
        "missing_artifacts": missing,
        "nontrivial_carrier_count": nontrivial,
        "certified_natural_support_link_count": natural_links,
        "inventory": inventory,
        "archive_statement": (
            "The frozen provenance stack contains nontrivial carriers, but the audited artifacts do not certify "
            "a natural representation/intertwiner from those carriers into the fixed 25-dimensional v14.03 support."
        ),
    }


def _deterministic_isometry(n: int, k: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((n, k)) + 1j * rng.standard_normal((n, k))
    Q, R = np.linalg.qr(A)
    d = np.diag(R)
    phases = np.ones_like(d, dtype=complex)
    nz = np.abs(d) > 1e-14
    phases[nz] = d[nz] / np.abs(d[nz])
    return Q @ np.diag(phases.conj())


def _dual_sep(A: np.ndarray, B: np.ndarray) -> float:
    dot = float(np.real(np.trace(A.conj().T @ B)))
    return float(max(0.0, 1.0 - dot))


def class_c_audit(v1403: ModuleType) -> dict[str, Any]:
    v1402 = v1403.load_v1402()
    cfg = v1403.build_configuration(v1402, "V_A")
    Pprov = herm(np.array([
        [1.0, 0.25 + 0.1j, 0.0],
        [0.25 - 0.1j, -0.6, 0.15],
        [0.0, 0.15, -0.4],
    ], dtype=complex))
    candidate_seeds = (14041, 14042, 14043, 14044, 14045, 14046)
    attempted: list[dict[str, Any]] = []
    successful: list[dict[str, Any]] = []
    I = np.eye(SUPPORT_DIM, dtype=complex)

    for seed in candidate_seeds:
        J = _deterministic_isometry(SUPPORT_DIM, 3, seed)
        iso_error = float(np.linalg.norm(J.conj().T @ J - np.eye(3)))
        P = herm(J @ Pprov @ J.conj().T)
        P = herm(P - float(np.real(np.trace(cfg["X0"] @ P))) * I)
        contact = v1403.source_contact(v1402, cfg, P, certify_base_formula=True)
        ok = bool(
            iso_error < ISOMETRY_TOL
            and contact["hidden"]["classification"] == "NONZERO_HIDDEN_COMPONENT"
            and contact["boundary"] is not None
            and contact["boundary"]["simple"]
            and contact["normal"] is not None
            and contact["normal"]["classification"] == "RAY"
            and contact["dual_rep"] is not None
        )
        attempted.append({
            "seed": seed,
            "isometry_error": iso_error,
            "hidden_classification": contact["hidden"]["classification"],
            "boundary_simple": bool(contact["boundary"]["simple"]) if contact["boundary"] is not None else False,
            "normal_classification": contact["normal"]["classification"] if contact["normal"] is not None else None,
            "successful": ok,
        })
        if ok:
            successful.append({"seed": seed, "J": J, "P": P, "contact": contact, "isometry_error": iso_error})
        if len(successful) >= 3:
            break

    pair_projective: list[float] = []
    hidden_seps: list[float] = []
    boundary_seps: list[float] = []
    dual_seps: list[float] = []
    pair_records: list[dict[str, Any]] = []
    for i in range(len(successful)):
        for j in range(i + 1, len(successful)):
            A = successful[i]
            B = successful[j]
            pres = projective_fit_residual(A["P"], B["P"])["residual"]
            hsep = rel_matrix_error(A["contact"]["hidden"]["unit_matrix"], B["contact"]["hidden"]["unit_matrix"])
            bsep = rel_matrix_error(A["contact"]["boundary"]["Xstar"], B["contact"]["boundary"]["Xstar"])
            dsep = _dual_sep(A["contact"]["dual_rep"], B["contact"]["dual_rep"])
            pair_projective.append(float(pres))
            hidden_seps.append(float(hsep))
            boundary_seps.append(float(bsep))
            dual_seps.append(float(dsep))
            pair_records.append({
                "seed_i": A["seed"],
                "seed_j": B["seed"],
                "projective_residual": float(pres),
                "hidden_direction_separation": float(hsep),
                "boundary_separation": float(bsep),
                "dual_ray_separation": float(dsep),
            })

    declared_count = len(successful)
    if pair_projective:
        min_projective = float(min(pair_projective))
        max_hidden = float(max(hidden_seps))
        max_boundary = float(max(boundary_seps))
        max_dual = float(max(dual_seps))
    else:
        min_projective = 0.0
        max_hidden = 0.0
        max_boundary = 0.0
        max_dual = 0.0
    genuine = bool(
        declared_count >= 2
        and min_projective > PROJECTIVE_AMBIGUITY_TOL
        and max_hidden > 1e-4
        and max_boundary > 1e-6
        and max_dual > 1e-6
    )
    return {
        "fixture_status": "SUPPLIED_INTERTWINER_CONTROL_NOT_DERIVED_PROVENANCE",
        "declared_intertwiner_count": declared_count,
        "attempted_seeds": [x["seed"] for x in attempted],
        "attempt_records": attempted,
        "max_isometry_error": float(max((x["isometry_error"] for x in attempted), default=0.0)),
        "min_pair_projective_residual": min_projective,
        "max_hidden_direction_separation": max_hidden,
        "max_boundary_separation": max_boundary,
        "max_dual_ray_separation": max_dual,
        "genuine_projective_ambiguity": genuine,
        "pair_records": pair_records,
    }


def run_audit() -> dict[str, Any]:
    v1403 = load_v1403()
    class_a = class_a_audit(v1403)
    class_b = class_b_audit()
    class_c = class_c_audit(v1403)

    if class_b["missing_artifact_count"] > 0:
        gate = "UNRESOLVED_REPRESENTATION_AUDIT"
    elif class_b["certified_natural_support_link_count"] > 0:
        gate = "DERIVED_PROVENANCE_SOURCE_RAY"
    elif class_b["nontrivial_carrier_count"] == 0:
        gate = "CENTRAL_ONLY_PGRL_NULL"
    elif class_c["genuine_projective_ambiguity"]:
        gate = "REQUIRES_NEW_REPRESENTATION_LINK"
    else:
        gate = "UNRESOLVED_REPRESENTATION_AUDIT"

    return {
        "version": "v14.04",
        "seed": SEED,
        "support_dimension": SUPPORT_DIM,
        "Pillar_3": "OPEN",
        "scientific_breakthrough": False,
        "claim_scope": (
            "representation/naturality audit from frozen Genesis/provenance carriers to the positive projective "
            "Hermitian source ray consumed by v14.03"
        ),
        "class_a": class_a,
        "class_b": class_b,
        "class_c": class_c,
        "gate_outcome": gate,
        "stop_rule": (
            "If no frozen natural provenance-to-support representation is certified and supplied admissible "
            "intertwiners produce inequivalent projective/downstream rays, stop pending a genuinely new "
            "representation principle or independently earned intertwiner."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
