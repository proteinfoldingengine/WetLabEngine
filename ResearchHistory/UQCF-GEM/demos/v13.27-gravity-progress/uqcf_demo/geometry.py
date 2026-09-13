import numpy as np
from .linalg import paulis, raw_orthogonal_polar, proper_orthogonal_polar, so3_angle_audit
from .quantum import (
    one_site_reductions,
    pair_reduction,
    bkm_covariance,
    connected_correlation,
    state_at_lambda,
)


def default_cycles():
    return [
        (0, 1, 2, 0),
        (3, 4, 5, 3),
        (1, 2, 3, 4, 1),
    ]


def geometry_snapshot(model, rho, cycles=None):
    n = model["n"]
    singles = one_site_reductions(rho, n)
    _, X, Y, Z = paulis()
    metrics = [bkm_covariance(r, [X, Y, Z]) for r in singles]
    edges = []
    lookup = {}
    for idx, (i, j) in enumerate(model["edges"]):
        pair = pair_reduction(rho, i, j, n)
        C = connected_correlation(pair, singles[i], singles[j])
        Q_raw = raw_orthogonal_polar(C)
        O = proper_orthogonal_polar(C)
        M = metrics[j] - O.T @ metrics[i] @ O
        M = (M + M.T) / 2
        record = {
            "index": idx,
            "i": i,
            "j": j,
            "C": C,
            "O": O,
            "M": M,
            "raw_polar_det": float(np.linalg.det(Q_raw)),
            "corr_norm": float(np.linalg.norm(C, ord="fro")),
            "nonmetricity_norm": float(np.linalg.norm(M, ord="fro")),
        }
        edges.append(record)
        lookup[(i, j)] = O
        lookup[(j, i)] = O.T
    cycle_records = []
    for cyc in cycles or default_cycles():
        H = np.eye(3)
        valid = True
        for a, b in zip(cyc[:-1], cyc[1:]):
            if (a, b) not in lookup:
                valid = False
                break
            H = H @ lookup[(a, b)]
        if valid:
            audit = so3_angle_audit(H)
            cycle_records.append({
                "nodes": tuple(cyc),
                "H": H,
                "angle": audit["angle"],
                "raw_cos_argument": audit["raw_cos_argument"],
                "clipped_cos_argument": audit["clipped_cos_argument"],
                "clip_excess": audit["clip_excess"],
            })
    return {
        "metrics": metrics,
        "singles": singles,
        "edges": edges,
        "cycles": cycle_records,
    }


def finite_difference_geometry_jet(model, lam, delta=1e-4):
    sm = geometry_snapshot(model, state_at_lambda(model, lam - delta))
    sp = geometry_snapshot(model, state_at_lambda(model, lam + delta))
    dM = []
    dO = []
    for em, ep in zip(sm["edges"], sp["edges"]):
        dM.append((ep["M"] - em["M"]) / (2 * delta))
        dO.append((ep["O"] - em["O"]) / (2 * delta))
    return {
        "dM": dM,
        "dO": dO,
        "mean_dM_norm": float(np.mean([np.linalg.norm(x, ord="fro") for x in dM])),
        "mean_dO_norm": float(np.mean([np.linalg.norm(x, ord="fro") for x in dO])),
    }
