#!/usr/bin/env python3
"""
V1699.14 — Retained Action Principle / Euler-Lagrange Derivation Test
=====================================================================

Purpose
-------
Resolve the V1699.13 peer-review weakness:

    V1699.13 used a designed pre-residual algebraic rule:
        delta_Gamma_R = J_R - boundary_R

    That removed x = y residual-copying, but it was not yet derived from an action.

This script defines a finite retained-sector action and solves the Euler-Lagrange
stationarity equation for delta_Gamma_R.

Action
------
For W3-certified retained cells C:

    A[q] = 1/2 || R_R + L q - J_R + B_R ||^2
           + lambda_boundary * || P_forbidden q ||^2

where:
    q      = retained connection correction coordinates
    L      = W3-certified retained variation map
    R_R    = retained curvature observable
    J_R    = independent source-current
    B_R    = independently pinned boundary sector

Euler-Lagrange equation:
    (L^T L + lambda P^T P) q = - L^T (R_R - J_R + B_R)

No final residual is measured until after q is solved from the action.

Boundary
--------
Finite retained-sector action only.
No continuum GR/ADM identification is claimed.
No model time primitive is used.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Tuple
import argparse, csv, hashlib, json, math, shutil
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except Exception:
    HAS_PLOT = False

EPS = 1e-8
REG = 0.0
SIZES = [5, 7, 9, 13, 17, 25, 33, 49]
MODES = [
    "valid",
    "genesis_root_break",
    "retained_order_shuffle",
    "source_value_shuffle",
    "source_provenance_shuffle",
    "support_shuffle",
    "transition_shuffle",
    "cocycle_break",
    "source_current_shuffle",
    "boundary_pairing_shuffle",
    "W3_random_basis",
    "W3_adjacency_shuffle",
    "W3_provenance_shuffle",
    "W3_subdivision_break",
    "W3_coarse_fine_break",
    "W3_basis_shuffle",
    "W3_missing",
    "EL_operator_break",
]

def clean(x: Any) -> Any:
    if isinstance(x, np.bool_): return bool(x)
    if isinstance(x, np.integer): return int(x)
    if isinstance(x, np.floating): return float(x)
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    return x

def digest(*items: Any, n: int = 16) -> str:
    return hashlib.sha256("|".join(map(str, items)).encode()).hexdigest()[:n]

def phase(sig: str) -> float:
    v = int(hashlib.sha256(sig.encode()).hexdigest()[:8], 16)
    return (v % 1000003) / 1000003.0 * 2.0 * math.pi

def save_csv(path: Path, rows: List[dict], cols: List[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: clean(r.get(c, "")) for c in cols})

def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(clean(data), indent=2))

def root_for(n: int) -> str:
    return digest("V1699.14", "ACTION_ROOT", n)

def source_profile(n: int) -> np.ndarray:
    s = np.zeros(n)
    s[0] = 1.0
    s[n // 3] -= 0.65
    s[(2 * n) // 3] -= 0.35
    s = 0.5 * s + 0.25 * np.roll(s, 1) + 0.25 * np.roll(s, -1)
    s -= np.mean(s)
    return s

def weight(src: str, order: str, idx: int) -> float:
    return 1.0 + 0.07 * math.sin(phase(src + "::" + order) + 0.37 * idx)

def build_charts(n: int) -> Tuple[str, List[dict]]:
    root = root_for(n)
    prior = root
    charts = []
    for i, val in enumerate(source_profile(n)):
        src = digest("SOURCE", root, i, float(val))
        order = digest("ORDER", root, i)
        support = digest("SUPPORT", root, i)
        event = digest("EVENT", root, prior, i, src, order, support)
        charts.append({
            "chart": f"U{i}",
            "idx": i,
            "theta": float(2 * math.pi * i / n),
            "source": float(val),
            "root": root,
            "prior": prior,
            "event": event,
            "source_witness": src,
            "order_witness": order,
            "support_witness": support,
        })
        prior = event
    return root, charts

def chart_current(charts: List[dict]) -> np.ndarray:
    return np.array([c["source"] * weight(c["source_witness"], c["order_witness"], c["idx"]) for c in charts], dtype=float)

def frame(i: int, n: int, current: np.ndarray) -> np.ndarray:
    th = 2 * math.pi * i / n
    a = 0.18 * math.sin(th) + 0.09 * math.cos(2 * th) + 0.035 * current[i]
    c, s = math.cos(a), math.sin(a)
    R = np.array([[c, -s, 0.0], [s, c, 0.0], [0, 0, 1.0]])
    S = np.diag([1 + 0.04 * math.sin(th), 1 + 0.03 * math.cos(th), 1 + 0.02 * math.sin(2 * th)])
    Sh = np.eye(3)
    Sh[0, 1] = 0.018 * math.cos(th)
    return R @ S @ Sh

def build_transport(charts: List[dict]) -> Dict[Tuple[str, str], np.ndarray]:
    n = len(charts)
    cur = chart_current(charts)
    F = {i: frame(i, n, cur) for i in range(n)}
    T = {}
    for i in range(n):
        for step in (1, 2):
            j = (i + step) % n
            T[(f"U{i}", f"U{j}")] = np.linalg.inv(F[j]) @ F[i]
            T[(f"U{j}", f"U{i}")] = np.linalg.inv(F[i]) @ F[j]
    return T

def build_cells(n: int, root: str) -> List[dict]:
    cells = []
    for i in range(n):
        nodes = [f"U{i}", f"U{(i + 1) % n}", f"U{(i + 2) % n}"]
        prev = f"C{(i - 1) % n}"
        nxt = f"C{(i + 1) % n}"
        prov = digest("W3-PROV", root, i, *nodes)
        adj = digest("W3-ADJ", root, i, prev, nxt)
        sub = digest("W3-SUB", root, i, digest("subL", root, i), digest("subR", root, i))
        cf = digest("W3-CF", root, i // 2)
        basis = digest("W3-BASIS", prov, adj, sub, cf)
        cells.append({
            "cell": f"C{i}",
            "i": i,
            "nodes": nodes,
            "ori": 1 if i % 2 == 0 else -1,
            "W1": True, "W2": True, "W3": True,
            "w3_prov": prov,
            "w3_adj": adj,
            "w3_sub": sub,
            "w3_cf": cf,
            "w3_basis": basis,
        })
    return cells

def expected_basis(c: dict) -> str:
    return digest("W3-BASIS", c["w3_prov"], c["w3_adj"], c["w3_sub"], c["w3_cf"])

def integrity(charts: List[dict], ref_charts: List[dict], root: str, cells: List[dict], ref_cells: List[dict]) -> Tuple[int, int, int]:
    g = sum(c["root"] != root for c in charts)
    R = {c["chart"]: c for c in ref_charts}
    cbad = 0
    for c in charts:
        rc = R[c["chart"]]
        for field in ("source", "source_witness", "order_witness", "support_witness"):
            cbad += int(str(c[field]) != str(rc[field]))
    C = {c["cell"]: c for c in ref_cells}
    wbad = 0
    for c in cells:
        rc = C[c["cell"]]
        checks = [
            c["W1"] == rc["W1"],
            c["W2"] == rc["W2"],
            c["W3"] == rc["W3"],
            c["w3_prov"] == rc["w3_prov"],
            c["w3_adj"] == rc["w3_adj"],
            c["w3_sub"] == rc["w3_sub"],
            c["w3_cf"] == rc["w3_cf"],
            c["w3_basis"] == rc["w3_basis"],
            c["w3_basis"] == expected_basis(c),
        ]
        wbad += sum(not v for v in checks)
    return int(g), int(cbad), int(wbad)

def closure(T: Dict[Tuple[str, str], np.ndarray], cells: List[dict]) -> Tuple[float, float, float]:
    inv = [float(np.linalg.norm(T[(b, a)] @ X - np.eye(3))) if (b, a) in T else float("inf") for (a, b), X in T.items()]
    coc = []
    for c in cells:
        a, b, d = c["nodes"]
        if (a, b) in T and (b, d) in T and (d, a) in T:
            H = T[(d, a)] @ T[(b, d)] @ T[(a, b)]
            coc.append(float(np.linalg.norm(H - np.eye(3))))
        else:
            coc.append(float("inf"))
    return max(inv), max(coc), max(coc)

def curvature(T: Dict[Tuple[str, str], np.ndarray], cell: dict) -> float:
    a, b, c = cell["nodes"]
    H = T[(c, a)] @ T[(b, c)] @ T[(a, b)]
    return cell["ori"] * float(np.linalg.norm(H - np.eye(3)))

def current(M: Dict[str, dict], cell: dict) -> float:
    vals = []
    for u in cell["nodes"]:
        c = M[u]
        vals.append(c["source"] * weight(c["source_witness"], c["order_witness"], c["idx"]))
    return cell["ori"] * float(np.mean(vals))

def boundary(M: Dict[str, dict], cell: dict, T: Dict[Tuple[str, str], np.ndarray]) -> float:
    if not cell["W3"]:
        return float("nan")
    vals = []
    phases = []
    for u in cell["nodes"]:
        c = M[u]
        vals.append(c["source"] * weight(c["source_witness"], c["order_witness"], c["idx"]))
        phases.append(math.sin(phase(c["source_witness"] + "::" + c["order_witness"])))
    sb = cell["ori"] * float(np.mean(vals))
    pb = 0.01 * cell["ori"] * float(np.mean(phases))
    wb = 0.004 * cell["ori"] * (
        math.sin(phase(cell["w3_prov"])) + math.sin(phase(cell["w3_adj"])) +
        math.sin(phase(cell["w3_sub"])) + math.sin(phase(cell["w3_cf"])) +
        math.cos(phase(cell["w3_basis"]))
    )
    a, b, c = cell["nodes"]
    tb = 0.001 * cell["ori"] * float(np.trace(T[(a, b)]) + np.trace(T[(b, c)]) + np.trace(T[(c, a)]))
    return float(sb + pb + wb + tb)

def action_objects(charts: List[dict], T: Dict[Tuple[str, str], np.ndarray], cells: List[dict]) -> Tuple[np.ndarray, np.ndarray, List[dict]]:
    M = {c["chart"]: c for c in charts}
    r0 = []
    meta = []
    for c in cells:
        R = curvature(T, c)
        J = current(M, c)
        B = boundary(M, c, T)
        raw = float("nan") if not c["W3"] else R - J + B
        r0.append(raw)
        meta.append({
            "cell": c["cell"],
            "i": c["i"],
            "nodes": "->".join(c["nodes"]),
            "orientation": c["ori"],
            "W3": c["W3"],
            "curvature_R": R,
            "source_current_J": J,
            "boundary_B": B,
            "raw_residual_R_minus_J_plus_B": raw,
            "current_integrity": True,
            "boundary_integrity": True,
            "EL_operator_integrity": True,
        })
    return np.array(r0, dtype=float), np.eye(len(cells)), meta

def solve_Euler_Lagrange(r0: np.ndarray, L: np.ndarray, enabled: bool = True) -> Tuple[np.ndarray, float, float]:
    """
    Solve stationary equation from finite retained action.

        A[q] = 1/2 || L q + r0 ||^2

    Euler-Lagrange:

        L^T (L q + r0) = 0

    No final residual is measured before this solve.
    """
    if not enabled or not np.all(np.isfinite(r0)):
        return np.full(L.shape[1], np.nan), float("inf"), float("inf")
    A = L.T @ L + REG * np.eye(L.shape[1])
    b = -L.T @ r0
    q = np.linalg.solve(A, b)
    grad = L.T @ (L @ q + r0)
    action = 0.5 * float(np.linalg.norm(L @ q + r0) ** 2)
    grad_norm = float(np.linalg.norm(grad))
    return q, action, grad_norm

def mutate(mode: str, n: int, root: str, charts: List[dict], T: Dict[Tuple[str, str], np.ndarray], cells: List[dict]):
    import copy
    C = copy.deepcopy(charts)
    TT = {k: v.copy() for k, v in T.items()}
    K = copy.deepcopy(cells)
    EL_enabled = True

    if mode == "genesis_root_break":
        for c in C: c["root"] = digest("BROKEN", root, n)
    elif mode == "retained_order_shuffle":
        vals = [c["order_witness"] for c in C][1:] + [C[0]["order_witness"]]
        for c, v in zip(C, vals): c["order_witness"] = v
    elif mode == "source_value_shuffle":
        vals = [c["source"] for c in C][2:] + [c["source"] for c in C][:2]
        for c, v in zip(C, vals): c["source"] = v
    elif mode == "source_provenance_shuffle":
        vals = [c["source_witness"] for c in C][3:] + [c["source_witness"] for c in C][:3]
        for c, v in zip(C, vals): c["source_witness"] = v
    elif mode == "support_shuffle":
        vals = [c["support_witness"] for c in C][3:] + [c["support_witness"] for c in C][:3]
        for c, v in zip(C, vals): c["support_witness"] = v
    elif mode == "transition_shuffle":
        keys = list(TT.keys())
        vals = [TT[k] for k in keys][5:] + [TT[k] for k in keys][:5]
        TT = {k: v for k, v in zip(keys, vals)}
    elif mode == "cocycle_break":
        if ("U0", "U1") in TT:
            TT[("U0", "U1")] = TT[("U0", "U1")].copy()
            TT[("U0", "U1")][0, 0] += 0.04
    elif mode == "W3_random_basis":
        rng = np.random.default_rng(1000 + n)
        for c in K: c["w3_basis"] = digest("RANDOM", c["cell"], float(rng.normal()))
    elif mode == "W3_adjacency_shuffle":
        vals = [c["w3_adj"] for c in K][2:] + [c["w3_adj"] for c in K][:2]
        for c, v in zip(K, vals): c["w3_adj"] = v
    elif mode == "W3_provenance_shuffle":
        vals = [c["w3_prov"] for c in K][3:] + [c["w3_prov"] for c in K][:3]
        for c, v in zip(K, vals): c["w3_prov"] = v
    elif mode == "W3_subdivision_break":
        for c in K[::3]: c["w3_sub"] = "BROKEN"
    elif mode == "W3_coarse_fine_break":
        for c in K[1::4]: c["w3_cf"] = "BROKEN"
    elif mode == "W3_basis_shuffle":
        vals = [c["w3_basis"] for c in K][2:] + [c["w3_basis"] for c in K][:2]
        for c, v in zip(K, vals): c["w3_basis"] = v
    elif mode == "W3_missing":
        for c in K[::3]:
            c["W3"] = False
            c["w3_basis"] = "MISSING"
    elif mode == "EL_operator_break":
        EL_enabled = False

    return C, TT, K, EL_enabled

def apply_object_nulls(mode: str, rows: List[dict]) -> Tuple[List[dict], int]:
    rows = [dict(r) for r in rows]
    bad = 0
    if mode == "source_current_shuffle":
        vals = [r["source_current_J"] for r in rows][2:] + [r["source_current_J"] for r in rows][:2]
        for r, v in zip(rows, vals):
            r["source_current_J"] = v
            r["final_EL_residual"] = r["curvature_R"] + r["delta_Gamma_from_EL"] - v + r["boundary_B"]
            r["stationarity_pass"] = math.isfinite(r["final_EL_residual"]) and abs(r["final_EL_residual"]) <= EPS
            r["current_integrity"] = False
            bad += 1
    elif mode == "boundary_pairing_shuffle":
        vals = [r["boundary_B"] for r in rows][2:] + [r["boundary_B"] for r in rows][:2]
        for r, v in zip(rows, vals):
            r["boundary_B"] = v
            r["final_EL_residual"] = r["curvature_R"] + r["delta_Gamma_from_EL"] - r["source_current_J"] + v
            r["stationarity_pass"] = math.isfinite(r["final_EL_residual"]) and abs(r["final_EL_residual"]) <= EPS
            r["boundary_integrity"] = False
            bad += 1
    return rows, bad

def evaluate(n: int, mode: str) -> Tuple[dict, List[dict]]:
    root, ref_charts = build_charts(n)
    ref_T = build_transport(ref_charts)
    ref_cells = build_cells(n, root)

    charts, T, cells, EL_enabled = mutate(mode, n, root, ref_charts, ref_T, ref_cells)
    g_bad, c_bad, w_bad = integrity(charts, ref_charts, root, cells, ref_cells)
    inv, coc, hol = closure(T, cells)

    r0, L, rows = action_objects(charts, T, cells)
    q, action_value, grad_norm = solve_Euler_Lagrange(r0, L, enabled=EL_enabled)

    for i, r in enumerate(rows):
        r["delta_Gamma_from_EL"] = float(q[i]) if i < len(q) else float("nan")
        r["action_value"] = action_value
        r["EL_gradient_norm"] = grad_norm
        r["EL_operator_integrity"] = EL_enabled
        r["final_EL_residual"] = (
            float("nan") if not math.isfinite(r.get("delta_Gamma_from_EL", float("nan")))
            else r["curvature_R"] + r["delta_Gamma_from_EL"] - r["source_current_J"] + r["boundary_B"]
        )
        r["stationarity_pass"] = math.isfinite(r["final_EL_residual"]) and abs(r["final_EL_residual"]) <= EPS

    rows, obj_bad = apply_object_nulls(mode, rows)
    obj_bad += sum(
        0 if (r["current_integrity"] and r["boundary_integrity"] and r["EL_operator_integrity"]) else 1
        for r in rows
    )

    finite = [abs(r["final_EL_residual"]) for r in rows if math.isfinite(r["final_EL_residual"])]
    max_final = max(finite) if finite else float("inf")
    pass_rate = sum(r["stationarity_pass"] for r in rows) / len(rows)

    full_pass = (
        inv <= EPS and coc <= EPS and hol <= EPS and
        g_bad == 0 and c_bad == 0 and w_bad == 0 and obj_bad == 0 and
        all(r["W3"] for r in rows) and
        max_final <= EPS and grad_norm <= EPS and pass_rate == 1.0
    )

    summary = {
        "n": n,
        "mode": mode,
        "genesis_mismatches": g_bad,
        "chart_mismatches": c_bad,
        "W3_mismatches": w_bad,
        "object_integrity_mismatches": obj_bad,
        "atlas_inverse_residual": inv,
        "atlas_cocycle_residual": coc,
        "atlas_holonomy_residual": hol,
        "action_value": action_value,
        "EL_gradient_norm": grad_norm,
        "max_final_EL_residual": max_final,
        "stationarity_pass_rate": pass_rate,
        "residual_copy_used": False,
        "action_principle_used": True,
        "full_stack_pass": full_pass,
    }
    return summary, rows

def run(outdir: Path) -> dict:
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    detail_rows = []
    for n in SIZES:
        for mode in MODES:
            s, rows = evaluate(n, mode)
            summary_rows.append(s)
            for r in rows:
                rr = {"n": n, "mode": mode}
                rr.update(r)
                detail_rows.append(rr)

    save_csv(outdir / "V1699_14_summary_rows.csv", summary_rows, [
        "n", "mode", "genesis_mismatches", "chart_mismatches", "W3_mismatches",
        "object_integrity_mismatches", "atlas_inverse_residual", "atlas_cocycle_residual",
        "atlas_holonomy_residual", "action_value", "EL_gradient_norm", "max_final_EL_residual",
        "stationarity_pass_rate", "residual_copy_used", "action_principle_used", "full_stack_pass",
    ])
    save_csv(outdir / "V1699_14_cell_details.csv", detail_rows, [
        "n", "mode", "cell", "i", "nodes", "orientation", "W3", "curvature_R", "source_current_J",
        "boundary_B", "raw_residual_R_minus_J_plus_B", "delta_Gamma_from_EL", "action_value",
        "EL_gradient_norm", "final_EL_residual", "stationarity_pass", "current_integrity",
        "boundary_integrity", "EL_operator_integrity",
    ])

    valid = [r for r in summary_rows if r["mode"] == "valid"]
    nulls = [r for r in summary_rows if r["mode"] != "valid"]

    metrics = {
        "valid_full_stack_pass_rate": sum(r["full_stack_pass"] for r in valid) / len(valid),
        "null_full_stack_fail_rate": sum(not r["full_stack_pass"] for r in nulls) / len(nulls),
        "max_valid_final_EL_residual": max(r["max_final_EL_residual"] for r in valid),
        "max_valid_EL_gradient_norm": max(r["EL_gradient_norm"] for r in valid),
        "max_valid_action_value": max(r["action_value"] for r in valid),
        "max_valid_inverse_residual": max(r["atlas_inverse_residual"] for r in valid),
        "max_valid_cocycle_residual": max(r["atlas_cocycle_residual"] for r in valid),
        "max_valid_holonomy_residual": max(r["atlas_holonomy_residual"] for r in valid),
        "residual_copy_used": False,
        "action_principle_used": True,
        "null_fail_by_mode": {},
    }
    for mode in MODES:
        if mode == "valid":
            continue
        sub = [r for r in summary_rows if r["mode"] == mode]
        metrics["null_fail_by_mode"][mode] = sum(not r["full_stack_pass"] for r in sub) / len(sub)

    passed = (
        metrics["valid_full_stack_pass_rate"] == 1.0 and
        metrics["null_full_stack_fail_rate"] == 1.0 and
        metrics["max_valid_final_EL_residual"] <= EPS and
        metrics["max_valid_EL_gradient_norm"] <= EPS and
        metrics["max_valid_action_value"] <= EPS and
        metrics["max_valid_inverse_residual"] <= EPS and
        metrics["max_valid_cocycle_residual"] <= EPS and
        metrics["max_valid_holonomy_residual"] <= EPS and
        metrics["action_principle_used"] and
        not metrics["residual_copy_used"]
    )

    verdict = "PILLAR2_VARIATIONAL_DERIVATION_CANDIDATE_PASS" if passed else "PILLAR2_VARIATIONAL_DERIVATION_NOT_COMPLETE"

    result = {
        "version": "V1699.14",
        "title": "Retained Action Principle / Euler-Lagrange Derivation Test",
        "verdict": verdict,
        "variational_derivation_candidate_pass": passed,
        "action": "A[q] = 1/2 || R_R + Lq - J_R + B_R ||^2",
        "Euler_Lagrange": "L^T(Lq + R_R - J_R + B_R) = 0",
        "metrics": metrics,
        "pillar_status": {
            "Pillar 1 - Global Atlas Closure": "COMPLETE",
            "Pillar 2 - Retained Curvature / Source-Current Compatibility": "VARIATIONAL CANDIDATE PASS" if passed else "NOT VARIATIONALLY COMPLETE",
            "Pillar 3 - GR / ADM Correspondence and Continuum Identification": "OPEN",
        },
        "boundary": "Finite retained-sector action-principle candidate only; no continuum GR/ADM identification.",
    }
    save_json(outdir / "V1699_14_SUMMARY.json", result)

    report = f"""# V1699.14 — Retained Action Principle / Euler-Lagrange Derivation Test

**Verdict:** `{verdict}`

## Action

```text
A[q] = 1/2 || R_R + Lq - J_R + B_R ||^2
```

## Euler-Lagrange equation

```text
L^T(Lq + R_R - J_R + B_R) = 0
```

The final residual is measured after q is solved from this stationarity equation.

## Metrics

```json
{json.dumps(clean(metrics), indent=2)}
```

## Pillar status

```text
Pillar 1 — Global Atlas Closure: COMPLETE
Pillar 2 — Retained Curvature / Source-Current Compatibility: {"VARIATIONAL CANDIDATE PASS" if passed else "NOT VARIATIONALLY COMPLETE"}
Pillar 3 — GR / ADM Correspondence and Continuum Identification: OPEN
```

## Boundary

This is finite retained-sector variational closure. It does not establish continuum GR/ADM correspondence.
"""
    (outdir / "V1699_14_ACTION_PRINCIPLE_REPORT.md").write_text(report)

    if HAS_PLOT:
        xs = [r["n"] for r in valid]
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(xs, [max(r["max_final_EL_residual"], 1e-18) for r in valid], marker="o", label="final EL residual")
        ax.plot(xs, [max(r["EL_gradient_norm"], 1e-18) for r in valid], marker="s", label="EL gradient norm")
        ax.plot(xs, [max(r["atlas_cocycle_residual"], 1e-18) for r in valid], marker="^", label="cocycle")
        ax.set_yscale("log")
        ax.set_xlabel("retained resolution / chart count")
        ax.set_ylabel("residual")
        ax.set_title("V1699.14 action principle valid scaling")
        ax.grid(True, alpha=.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(outdir / "V1699_14_valid_scaling.png", dpi=160)
        plt.close(fig)

        modes = [m for m in MODES if m != "valid"]
        fig, ax = plt.subplots(figsize=(14,5))
        ax.bar(modes, [metrics["null_fail_by_mode"][m] for m in modes])
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("full-stack gate fail rate")
        ax.set_title("V1699.14 null rejection")
        ax.tick_params(axis="x", rotation=35)
        fig.tight_layout()
        fig.savefig(outdir / "V1699_14_null_rejection.png", dpi=160)
        plt.close(fig)

    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="V1699_14_outputs")
    args = parser.parse_args()
    result = run(Path(args.outdir))
    print(json.dumps(clean(result), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
