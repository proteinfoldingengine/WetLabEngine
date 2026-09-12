import copy
import hashlib
import json
import numpy as np

from .linalg import paulis, hermitian_log
from .quantum import build_default_model, state_at_lambda, state_from_logtilt, pauli_expectations
from .geometry import geometry_snapshot
from .source_current import (
    incidence_matrix,
    balanced_source,
    conditional_response_selected_current,
    projective_scale_control,
)
from .adm import represented_q, dewitt_diagnostic, dewitt_controls
from .ledger import claim_ledger


def default_config(frames=25):
    return {
        "seed": 1327,
        "frames": int(frames),
        "lambda_min": -0.8,
        "lambda_max": 0.8,
        "source_scale": 1.0,
        "q_regularizer": 1e-6,
    }


def _node_incident_scores(n, edges, edge_values):
    score = np.zeros(n, dtype=float)
    count = np.zeros(n, dtype=float)
    for value, (i, j) in zip(edge_values, edges):
        score[i] += value
        score[j] += value
        count[i] += 1.0
        count[j] += 1.0
    return score / np.maximum(count, 1.0)


def _float_list(x):
    return [float(v) for v in np.asarray(x).ravel()]


def _canonical_for_hash(obj):
    if isinstance(obj, dict):
        return {k: _canonical_for_hash(v) for k, v in sorted(obj.items()) if k != "telemetry_hash"}
    if isinstance(obj, list):
        return [_canonical_for_hash(v) for v in obj]
    if isinstance(obj, float):
        return round(obj, 9)
    return obj


def telemetry_hash(data):
    canonical = json.dumps(_canonical_for_hash(data), sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def scientific_fingerprint(data):
    """Portable fingerprint of scientifically material, numerically stable output.

    The full telemetry hash remains useful as a byte-level numerical diagnostic, but
    eigensolver/SVD implementations may differ at machine epsilon across BLAS/LAPACK
    runs.  This fingerprint intentionally hashes rounded invariant observables plus
    structural gate outcomes, not epsilon-scale residuals or gauge-sensitive matrix
    representatives.
    """
    s = data["summary"]
    cfg = data["config"]
    graph = data["graph"]
    portable = {
        "version": data["version"],
        "config": {
            "frames": int(cfg["frames"]),
            "lambda_min": round(float(cfg["lambda_min"]), 12),
            "lambda_max": round(float(cfg["lambda_max"]), 12),
            "source_scale": round(float(cfg["source_scale"]), 12),
            "q_regularizer": round(float(cfg["q_regularizer"]), 12),
        },
        "graph": {
            "n": int(graph["n"]),
            "edges": graph["edges"],
            "source_nodes": graph["source_nodes"],
        },
        "invariants": {
            "min_state_eigenvalue": round(float(s["min_state_eigenvalue"]), 10),
            "min_bkm_eigenvalue": round(float(s["min_bkm_eigenvalue"]), 10),
            "max_cycle_angle": round(float(s["max_cycle_angle"]), 10),
            "max_qmar_jet_norm": round(float(s["max_qmar_jet_norm"]), 10),
            "mean_dewitt_diagnostic": round(float(s["mean_dewitt_diagnostic"]), 10),
            "dewitt_pure_trace_control": round(float(s["dewitt_pure_trace_control"]), 10),
            "dewitt_traceless_control": round(float(s["dewitt_traceless_control"]), 10),
            "tensor_completion_spatial_stress_distance": round(
                float(s["tensor_completion_spatial_stress_distance"]), 10
            ),
            "max_cycle_rank_deficit": int(s["max_cycle_rank_deficit"]),
        },
        "structural_gates": {
            "source_balance_machine_zero": bool(s["max_source_balance_residual"] < 1e-10),
            "projective_ray_machine_zero": bool(s["max_projective_direction_change"] < 1e-10),
            "pgrl_reparameterization_machine_zero": bool(s["pgrl_reparameterization_error"] < 1e-10),
            "faithful_state": bool(s["min_state_eigenvalue"] > 0.0),
            "bkm_psd": bool(s["min_bkm_eigenvalue"] > -1e-9),
            "dewitt_trace_sign": bool(
                s["dewitt_pure_trace_control"] < 0.0
                and s["dewitt_traceless_control"] > -1e-10
            ),
        },
        "claim_boundary": {
            "projective_sigma_status": s["projective_sigma_status"],
            "RGCL": s["RGCL"],
            "physical_Einstein_closure": s["physical_Einstein_closure"],
        },
    }
    canonical = json.dumps(portable, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_telemetry(config=None):
    cfg = default_config() if config is None else copy.deepcopy(config)
    frames = int(cfg["frames"])
    if frames < 3:
        raise ValueError("at least 3 frames are required")
    model = build_default_model(source_scale=float(cfg.get("source_scale", 1.0)))
    n = model["n"]
    edges = model["edges"]
    E = len(edges)
    lambdas = np.linspace(float(cfg["lambda_min"]), float(cfg["lambda_max"]), frames)
    _, _, _, Zop = paulis()

    state_min_eig = []
    bkm_min_eig = []
    local_z = np.zeros((frames, n), dtype=float)
    edge_corr = np.zeros((frames, E), dtype=float)
    edge_nonmetricity = np.zeros((frames, E), dtype=float)
    edge_M = np.zeros((frames, E, 3, 3), dtype=float)
    edge_O = np.zeros((frames, E, 3, 3), dtype=float)
    q = np.zeros((frames, n, 3, 3), dtype=float)
    cycle_angles = []
    node_geometry_score = np.zeros((frames, n), dtype=float)

    for f, lam in enumerate(lambdas):
        rho = state_at_lambda(model, float(lam))
        state_min_eig.append(float(np.linalg.eigvalsh(rho).min()))
        snap = geometry_snapshot(model, rho)
        local_z[f] = [float(np.trace(r @ Zop).real) for r in snap["singles"]]
        mins = [float(np.linalg.eigvalsh(K).min()) for K in snap["metrics"]]
        bkm_min_eig.append(min(mins))
        for e, record in enumerate(snap["edges"]):
            edge_corr[f, e] = record["corr_norm"]
            edge_nonmetricity[f, e] = record["nonmetricity_norm"]
            edge_M[f, e] = record["M"]
            edge_O[f, e] = record["O"]
        cycle_angles.append([float(c["angle"]) for c in snap["cycles"]])
        node_geometry_score[f] = _node_incident_scores(n, edges, edge_nonmetricity[f])
        for i, K in enumerate(snap["metrics"]):
            q[f, i] = represented_q(K, regularizer=float(cfg["q_regularizer"]))

    edge_order = 2 if frames >= 3 else 1
    local_response = np.gradient(local_z, lambdas, axis=0, edge_order=edge_order)
    edge_response = np.gradient(edge_corr, lambdas, axis=0, edge_order=edge_order)
    dM = np.gradient(edge_M, lambdas, axis=0, edge_order=edge_order)
    dO = np.gradient(edge_O, lambdas, axis=0, edge_order=edge_order)
    qdot = np.gradient(q, lambdas, axis=0, edge_order=edge_order)

    B = incidence_matrix(n, edges)
    current = np.zeros((frames, E), dtype=float)
    source = np.zeros((frames, n), dtype=float)
    balance_residual = np.zeros(frames, dtype=float)
    response_residual = np.zeros(frames, dtype=float)
    cycle_rank = np.zeros(frames, dtype=int)
    cycle_dim = np.zeros(frames, dtype=int)
    projective_error = np.zeros(frames, dtype=float)
    dewitt = np.zeros(frames, dtype=float)
    qmar_jet = np.zeros(frames, dtype=float)

    for f in range(frames):
        source[f] = balanced_source(local_response[f])
        weights = 1.0 + edge_nonmetricity[f]
        selected = conditional_response_selected_current(B, source[f], edge_response[f], weights)
        current[f] = selected["J"]
        balance_residual[f] = np.linalg.norm(B @ current[f] - source[f])
        response_residual[f] = selected["response_residual"]
        cycle_rank[f] = selected["cycle_rank"]
        cycle_dim[f] = selected["cycle_dim"]
        ray = np.r_[source[f], current[f]]
        projective_error[f] = projective_scale_control(ray)["max_direction_change"]
        dewitt[f] = float(np.mean([dewitt_diagnostic(q[f, i], qdot[f, i]) for i in range(n)]))
        dm_norm = np.mean([np.linalg.norm(dM[f, e], ord="fro") for e in range(E)])
        do_norm = np.mean([np.linalg.norm(dO[f, e], ord="fro") for e in range(E)])
        qmar_jet[f] = float(np.hypot(dm_norm, do_norm))

    mid = frames // 2
    controls = dewitt_controls(q[mid, 0])

    # Exact PGRL source-parameterization control; this is a source-unit gauge, not a gravity law.
    log_rho0 = hermitian_log(model["rho0"])
    a = 4.2
    lam_probe = 0.37
    pgrl_a = state_from_logtilt(log_rho0, lam_probe, model["P"])
    pgrl_b = state_from_logtilt(log_rho0, lam_probe / a, a * model["P"])
    pgrl_reparam_error = float(np.linalg.norm(pgrl_a - pgrl_b, ord="fro"))

    # Tensor-completion witness: same coupled rho/j projection, different spatial stress block.
    stress_a = np.diag([0.25, -0.10, 0.05])
    stress_b = np.array([[0.55, 0.12, 0.0], [0.12, -0.25, 0.08], [0.0, 0.08, 0.18]])
    tensor_completion_distance = float(np.linalg.norm(stress_a - stress_b, ord="fro"))

    records = []
    for f, lam in enumerate(lambdas):
        records.append({
            "frame": int(f),
            "lambda_source": float(lam),
            "state_min_eigenvalue": state_min_eig[f],
            "bkm_min_eigenvalue": bkm_min_eig[f],
            "mean_nonmetricity": float(np.mean(edge_nonmetricity[f])),
            "mean_correlation": float(np.mean(edge_corr[f])),
            "mean_cycle_angle": float(np.mean(cycle_angles[f])) if cycle_angles[f] else 0.0,
            "max_cycle_angle": float(np.max(cycle_angles[f])) if cycle_angles[f] else 0.0,
            "source_norm": float(np.linalg.norm(source[f])),
            "current_norm": float(np.linalg.norm(current[f])),
            "balance_residual": float(balance_residual[f]),
            "conditional_response_residual": float(response_residual[f]),
            "cycle_rank": int(cycle_rank[f]),
            "cycle_dim": int(cycle_dim[f]),
            "projective_direction_change": float(projective_error[f]),
            "qmar_jet_norm": float(qmar_jet[f]),
            "dewitt_diagnostic": float(dewitt[f]),
            "local_z": _float_list(local_z[f]),
            "node_source": _float_list(source[f]),
            "edge_current": _float_list(current[f]),
            "edge_correlation": _float_list(edge_corr[f]),
            "edge_nonmetricity": _float_list(edge_nonmetricity[f]),
            "node_geometry_score": _float_list(node_geometry_score[f]),
            "cycle_angles": [float(x) for x in cycle_angles[f]],
        })

    summary = {
        "min_state_eigenvalue": float(np.min(state_min_eig)),
        "min_bkm_eigenvalue": float(np.min(bkm_min_eig)),
        "max_source_balance_residual": float(np.max(balance_residual)),
        "max_projective_direction_change": float(np.max(projective_error)),
        "max_cycle_rank_deficit": int(np.max(cycle_dim - cycle_rank)),
        "max_cycle_angle": float(np.max(cycle_angles)) if cycle_angles else 0.0,
        "max_qmar_jet_norm": float(np.max(qmar_jet)),
        "mean_dewitt_diagnostic": float(np.mean(dewitt)),
        "dewitt_pure_trace_control": float(controls["pure_trace"]),
        "dewitt_traceless_control": float(controls["traceless"]),
        "pgrl_reparameterization_error": pgrl_reparam_error,
        "tensor_completion_spatial_stress_distance": tensor_completion_distance,
        "projective_sigma_status": "RAY_ONLY__MAGNITUDE_NOT_DERIVED",
        "RGCL": "MISSING",
        "physical_Einstein_closure": "OPEN",
    }

    data = {
        "version": "v13.27-gravity-progress-demo",
        "config": cfg,
        "graph": {
            "n": n,
            "edges": [list(e) for e in edges],
            "positions": model["positions"].tolist(),
            "source_nodes": list(model["source_nodes"]),
        },
        "records": records,
        "summary": summary,
        "claim_ledger": claim_ledger(),
        "controlled_correspondence_overlay": {
            "source": "retained v13.24 external analytical correspondence only",
            "combined_weak_residual_exponent": 1.980,
            "q_pi_bracket_exponent": 2.474,
            "finest_combined_source_weak_residual": 8.388e-06,
            "used_as_selector": False,
        },
    }
    data["scientific_fingerprint"] = scientific_fingerprint(data)
    data["telemetry_hash"] = telemetry_hash(data)
    return data
