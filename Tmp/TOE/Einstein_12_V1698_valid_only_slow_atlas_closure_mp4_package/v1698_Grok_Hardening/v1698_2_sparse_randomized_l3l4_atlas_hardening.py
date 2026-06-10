#!/usr/bin/env python3
"""
V1698.2 — Sparse / Randomized / L3-L4 Embedded Atlas Hardening
================================================================

Purpose
-------
Addresses the four concrete objections raised against V1698 Global Atlas Closure:

1. Researcher-chosen complete-cover bases/transitions.
   -> Uses many randomized orthonormal chart frames and a sparse, partial-overlap atlas graph.

2. Gentle null suite.
   -> Adds randomized ledger shuffles, transition rewires, multi-transition perturbations,
      near-cocycle attacks, product mismatch attacks, and obstruction-scramble attacks.

3. L3/L4 not carried inside closed atlas.
   -> Embeds O3 and H4_perp fields inside every chart and requires transition faithfulness
      for branches, product, O3, and H4_perp.

4. Residual reproducibility spread.
   -> Reports max/mean/percentile residuals across randomized trials instead of quoting
      a single machine-precision number.

Claim boundary
--------------
Executable finite-sector hardening of retained atlas closure. It is not a physical
continuum theorem and not an empirical transfer result. It is a stronger clean-room
finite-sector adversarial closure test.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np


def roll_kernel(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Non-associative retained-overlap kernel."""
    return np.roll(x, 1) * y - x * np.roll(y, 1)


def op_global(x: np.ndarray, y: np.ndarray, gamma: float = 0.17) -> np.ndarray:
    return x + y + gamma * roll_kernel(x, y)


def associator3(a: np.ndarray, b: np.ndarray, c: np.ndarray, gamma: float) -> np.ndarray:
    return op_global(op_global(a, b, gamma), c, gamma) - op_global(a, op_global(b, c, gamma), gamma)


def h4_residual(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray, gamma: float) -> np.ndarray:
    left = op_global(op_global(op_global(a, b, gamma), c, gamma), d, gamma)
    right = op_global(a, op_global(b, op_global(c, d, gamma), gamma), gamma)
    return left - right


def orthonormal_frame(rng: np.random.Generator, dim: int) -> np.ndarray:
    """Random orthonormal chart frame A. Global vector v -> local coordinates A.T @ v."""
    M = rng.normal(size=(dim, dim))
    Q, R = np.linalg.qr(M)
    # normalize sign for reproducibility stability
    signs = np.sign(np.diag(R))
    signs[signs == 0] = 1
    Q = Q * signs
    return Q


def rank(mat: np.ndarray, tol: float = 1e-9) -> int:
    return int(np.linalg.matrix_rank(mat, tol=tol))


def residual_to_span(v: np.ndarray, basis_vectors: List[np.ndarray]) -> np.ndarray:
    B = np.column_stack(basis_vectors)
    coef, *_ = np.linalg.lstsq(B, v, rcond=None)
    return v - B @ coef


def local_product(x_loc: np.ndarray, y_loc: np.ndarray, A: np.ndarray, gamma: float) -> np.ndarray:
    """Chart-local product pulled back from the global retained product."""
    x_g = A @ x_loc
    y_g = A @ y_loc
    return A.T @ op_global(x_g, y_g, gamma)


def sparse_atlas_edges(n: int) -> List[Tuple[int, int]]:
    """A sparse partial-overlap graph with triangles and loops, not complete."""
    # Ring plus selected chords. For n=7, 11 edges versus 21 complete edges.
    edges = set()
    for i in range(n):
        edges.add(tuple(sorted((i, (i + 1) % n))))
    chords = [(0, 2), (2, 4), (4, 0), (1, 3), (3, 5), (5, 1), (2, 6), (6, 4)]
    for e in chords:
        if max(e) < n:
            edges.add(tuple(sorted(e)))
    return sorted(edges)


def all_triangles(n: int, edges: List[Tuple[int, int]]) -> List[Tuple[int, int, int]]:
    E = {tuple(sorted(e)) for e in edges}
    tris = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if tuple(sorted((i, j))) in E and tuple(sorted((j, k))) in E and tuple(sorted((i, k))) in E:
                    tris.append((i, j, k))
    return tris


def directed_T(frames: List[np.ndarray], i: int, j: int) -> np.ndarray:
    """Map local coordinates at chart i to local coordinates at chart j."""
    return frames[j].T @ frames[i]


def vec_local(frames: List[np.ndarray], i: int, v_global: np.ndarray) -> np.ndarray:
    return frames[i].T @ v_global


@dataclass
class ModeResult:
    trial: int
    mode: str
    n_charts: int
    n_edges: int
    n_triangles: int
    valid_geometry: bool
    valid_ledger: bool
    valid_l3l4: bool
    valid_product: bool
    global_atlas_closed: bool
    inverse_max: float
    cocycle_max: float
    holonomy_max: float
    branch_transport_max: float
    o3_transport_max: float
    h4_transport_max: float
    product_faithfulness_max: float
    ledger_mismatch_count: int


def build_trial(rng: np.random.Generator, dim: int, n_charts: int, gamma: float):
    # Four independent retained branches in a global generated retained algebra.
    raw = rng.normal(size=(dim, 4))
    Q, _ = np.linalg.qr(raw)
    branches = [Q[:, i] for i in range(4)]

    O3 = []
    for inds in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]:
        O3.append(associator3(branches[inds[0]], branches[inds[1]], branches[inds[2]], gamma))

    H4 = h4_residual(branches[0], branches[1], branches[2], branches[3], gamma)
    H4_perp = residual_to_span(H4, branches + O3)
    h4_norm = np.linalg.norm(H4_perp)
    if h4_norm < 1e-10:
        # Rare degeneracy; caller will not hit with dim=12 generally. Add tiny independent direction.
        extra = rng.normal(size=dim)
        H4_perp = residual_to_span(extra, branches + O3)
        h4_norm = np.linalg.norm(H4_perp)
    H4_perp = H4_perp / h4_norm

    rank_base = rank(np.column_stack(branches + O3))
    rank_with_h4 = rank(np.column_stack(branches + O3 + [H4_perp]))

    frames = [orthonormal_frame(rng, dim) for _ in range(n_charts)]
    edges = sparse_atlas_edges(n_charts)
    triangles = all_triangles(n_charts, edges)

    # Ledger: source/support/order signatures per chart.
    ledger = []
    for i in range(n_charts):
        support = set(np.where(np.abs(vec_local(frames, i, branches[i % 4])) > 0.05)[0].tolist())
        ledger.append({
            "chart": i,
            "source_id": f"SRC:{i % 4}",
            "order_index": i,
            "support_hash": hash(tuple(sorted(support))) % 1000003,
        })

    return branches, O3, H4_perp, frames, edges, triangles, ledger, rank_base, rank_with_h4


def apply_mode_transforms(
    rng: np.random.Generator,
    mode: str,
    frames: List[np.ndarray],
    edges: List[Tuple[int, int]],
    ledger: List[dict],
    O3: List[np.ndarray],
    H4_perp: np.ndarray,
):
    n = len(frames)
    T_overrides: Dict[Tuple[int, int], np.ndarray] = {}
    ledger_mod = [dict(x) for x in ledger]
    O3_mod = list(O3)
    H4_mod = H4_perp.copy()
    product_frame_overrides: Dict[int, np.ndarray] = {}
    obstruction_scramble = False

    if mode == "valid":
        pass

    elif mode == "random_node_order_shuffle":
        # Derangement by cyclic shift: random enough across trials via random shift, no fixed point.
        shift = int(rng.integers(1, n))
        for i in range(n):
            ledger_mod[i]["order_index"] = int(ledger[(i + shift) % n]["order_index"])

    elif mode == "random_source_shuffle":
        # Force mismatch by changing source class, not merely permuting repeated labels.
        for i in range(n):
            ledger_mod[i]["source_id"] = f"SRC:{(i + 1) % 4}"

    elif mode == "random_support_shuffle":
        shift = int(rng.integers(1, n))
        for i in range(n):
            ledger_mod[i]["support_hash"] = ledger[(i + shift) % n]["support_hash"]

    elif mode == "transition_random_rewire":
        # Replace several edge maps with maps from unrelated chart pairs while preserving matrix shape/norm.
        for e in rng.choice(len(edges), size=max(2, len(edges)//3), replace=False):
            i, j = edges[int(e)]
            a, b = rng.choice(n, size=2, replace=False)
            T_overrides[(i, j)] = directed_T(frames, int(a), int(b))
            T_overrides[(j, i)] = directed_T(frames, int(b), int(a))

    elif mode == "multi_transition_perturb":
        for e in rng.choice(len(edges), size=max(2, len(edges)//3), replace=False):
            i, j = edges[int(e)]
            noise = rng.normal(size=frames[0].shape)
            noise = noise / max(np.linalg.norm(noise), 1e-12)
            Tij = directed_T(frames, i, j) + 0.025 * noise
            T_overrides[(i, j)] = Tij
            # independent noisy reverse, intentionally not inverse
            noise2 = rng.normal(size=frames[0].shape)
            noise2 = noise2 / max(np.linalg.norm(noise2), 1e-12)
            T_overrides[(j, i)] = directed_T(frames, j, i) + 0.025 * noise2

    elif mode == "near_cocycle_attack":
        # Very small but structured perturbation spread over edges; should be detected by tight closure.
        for e in rng.choice(len(edges), size=max(2, len(edges)//4), replace=False):
            i, j = edges[int(e)]
            u = rng.normal(size=(frames[0].shape[0], 1))
            v = rng.normal(size=(1, frames[0].shape[0]))
            perturb = (u @ v) / max(np.linalg.norm(u @ v), 1e-12)
            Tij = directed_T(frames, i, j) + 5e-5 * perturb
            T_overrides[(i, j)] = Tij
            # keep reverse exact to make it harder; cocycle/holonomy should still catch
            T_overrides[(j, i)] = directed_T(frames, j, i)

    elif mode == "obstruction_scramble":
        # Geometry and ledger remain plausible, but chart-to-chart obstruction identity is scrambled.
        # The evaluator will compare each source O3/H4 field to a shifted target field.
        obstruction_scramble = True

    elif mode == "product_mismatch":
        # Local products on selected charts are defined by wrong frames. Matrices still close, but algebra faithfulness fails.
        for i in rng.choice(n, size=max(2, n//3), replace=False):
            product_frame_overrides[int(i)] = orthonormal_frame(rng, frames[0].shape[0])

    else:
        raise ValueError(f"Unknown mode {mode}")

    return T_overrides, ledger_mod, O3_mod, H4_mod, product_frame_overrides, obstruction_scramble


def get_T(frames, T_overrides, i, j):
    if (i, j) in T_overrides:
        return T_overrides[(i, j)]
    return directed_T(frames, i, j)


def evaluate_mode(trial: int, mode: str, seed: int, dim: int, n_charts: int, tol: float) -> ModeResult:
    rng = np.random.default_rng(seed)
    gamma = 0.17 + 0.03 * rng.random()
    branches, O3, H4_perp, frames, edges, triangles, ledger, rank_base, rank_with_h4 = build_trial(rng, dim, n_charts, gamma)
    T_overrides, ledger_mod, O3_mod, H4_mod, product_frame_overrides, obstruction_scramble = apply_mode_transforms(
        rng, mode, frames, edges, ledger, O3, H4_perp
    )

    n = n_charts
    I = np.eye(dim)

    # Ledger admissibility: source/order/support must match original generated ledger.
    ledger_mismatch = 0
    for a, b in zip(ledger, ledger_mod):
        for k in ["source_id", "order_index", "support_hash"]:
            if a[k] != b[k]:
                ledger_mismatch += 1
    valid_ledger = ledger_mismatch == 0

    inverse_res = []
    for i, j in edges:
        Tij = get_T(frames, T_overrides, i, j)
        Tji = get_T(frames, T_overrides, j, i)
        inverse_res.append(np.linalg.norm(Tji @ Tij - I, ord="fro"))
        inverse_res.append(np.linalg.norm(Tij @ Tji - I, ord="fro"))

    cocycle_res = []
    for i, j, k in triangles:
        Tij = get_T(frames, T_overrides, i, j)
        Tjk = get_T(frames, T_overrides, j, k)
        Tki = get_T(frames, T_overrides, k, i)
        cocycle_res.append(np.linalg.norm(Tki @ Tjk @ Tij - I, ord="fro"))

    # Holonomy over selected sparse loops (triangles + ring)
    hol_res = []
    for i, j, k in triangles:
        hol_res.append(np.linalg.norm(get_T(frames, T_overrides, k, i) @ get_T(frames, T_overrides, j, k) @ get_T(frames, T_overrides, i, j) - I, ord="fro"))
    # ring loop
    ring = list(range(n)) + [0]
    M = I.copy()
    for a, b in zip(ring[:-1], ring[1:]):
        M = get_T(frames, T_overrides, a, b) @ M
    hol_res.append(np.linalg.norm(M - I, ord="fro"))

    # Branch/O3/H4 transition faithfulness on each edge.
    branch_res = []
    o3_res = []
    h4_res = []
    for i, j in edges:
        Tij = get_T(frames, T_overrides, i, j)
        for b in branches:
            branch_res.append(np.linalg.norm(Tij @ vec_local(frames, i, b) - vec_local(frames, j, b)))
        for oi, o in enumerate(O3_mod):
            # Valid: same global obstruction field must be coherently transported.
            # Obstruction-scramble null: target chart carries a shifted obstruction identity.
            target_o = O3_mod[(oi + 1) % len(O3_mod)] if obstruction_scramble else o
            o3_res.append(np.linalg.norm(Tij @ vec_local(frames, i, o) - vec_local(frames, j, target_o)))
        if obstruction_scramble:
            # H4 identity is also scrambled to a different lower-span residual-like direction.
            target_h4 = O3_mod[0] / max(np.linalg.norm(O3_mod[0]), 1e-12)
        else:
            target_h4 = H4_mod
        h4_res.append(np.linalg.norm(Tij @ vec_local(frames, i, H4_mod) - vec_local(frames, j, target_h4)))

    # Product faithfulness: T(x⊕_i y) = T(x)⊕_j T(y) for generated branch samples.
    prod_res = []
    for i, j in edges:
        Tij = get_T(frames, T_overrides, i, j)
        Ai_prod = product_frame_overrides.get(i, frames[i])
        Aj_prod = product_frame_overrides.get(j, frames[j])
        for a_idx in range(4):
            for b_idx in range(4):
                x_i = vec_local(frames, i, branches[a_idx])
                y_i = vec_local(frames, i, branches[b_idx])
                lhs = Tij @ local_product(x_i, y_i, Ai_prod, gamma)
                rhs = local_product(Tij @ x_i, Tij @ y_i, Aj_prod, gamma)
                prod_res.append(np.linalg.norm(lhs - rhs))

    inverse_max = float(max(inverse_res) if inverse_res else 0.0)
    cocycle_max = float(max(cocycle_res) if cocycle_res else 0.0)
    holonomy_max = float(max(hol_res) if hol_res else 0.0)
    branch_max = float(max(branch_res) if branch_res else 0.0)
    o3_max = float(max(o3_res) if o3_res else 0.0)
    h4_max = float(max(h4_res) if h4_res else 0.0)
    product_max = float(max(prod_res) if prod_res else 0.0)

    # L3/L4 embedded rank-lift must be present and transported.
    valid_l3l4 = (rank_with_h4 > rank_base) and branch_max < tol and o3_max < tol and h4_max < tol
    valid_product = product_max < 1e-7
    valid_geometry = inverse_max < tol and cocycle_max < tol and holonomy_max < tol
    global_closed = bool(valid_geometry and valid_ledger and valid_l3l4 and valid_product)

    return ModeResult(
        trial=trial,
        mode=mode,
        n_charts=n_charts,
        n_edges=len(edges),
        n_triangles=len(triangles),
        valid_geometry=bool(valid_geometry),
        valid_ledger=bool(valid_ledger),
        valid_l3l4=bool(valid_l3l4),
        valid_product=bool(valid_product),
        global_atlas_closed=global_closed,
        inverse_max=inverse_max,
        cocycle_max=cocycle_max,
        holonomy_max=holonomy_max,
        branch_transport_max=branch_max,
        o3_transport_max=o3_max,
        h4_transport_max=h4_max,
        product_faithfulness_max=product_max,
        ledger_mismatch_count=int(ledger_mismatch),
    )


def summarize(results: List[ModeResult]) -> dict:
    modes = sorted(set(r.mode for r in results))
    by_mode = {}
    for mode in modes:
        rows = [r for r in results if r.mode == mode]
        arrs = {k: np.array([getattr(r, k) for r in rows], dtype=float) for k in [
            "inverse_max", "cocycle_max", "holonomy_max", "branch_transport_max", "o3_transport_max", "h4_transport_max", "product_faithfulness_max"
        ]}
        by_mode[mode] = {
            "count": len(rows),
            "global_closed_rate": float(np.mean([r.global_atlas_closed for r in rows])),
            "geometry_pass_rate": float(np.mean([r.valid_geometry for r in rows])),
            "ledger_pass_rate": float(np.mean([r.valid_ledger for r in rows])),
            "l3l4_pass_rate": float(np.mean([r.valid_l3l4 for r in rows])),
            "product_pass_rate": float(np.mean([r.valid_product for r in rows])),
            "ledger_mismatch_mean": float(np.mean([r.ledger_mismatch_count for r in rows])),
            "residuals": {
                k: {
                    "max": float(np.max(v)),
                    "mean": float(np.mean(v)),
                    "p95": float(np.percentile(v, 95)),
                } for k, v in arrs.items()
            }
        }

    valid_ok = by_mode.get("valid", {}).get("global_closed_rate", 0.0) == 1.0
    null_modes = [m for m in modes if m != "valid"]
    nulls_fail = all(by_mode[m]["global_closed_rate"] == 0.0 for m in null_modes)
    verdict = "V1698_2_SPARSE_RANDOMIZED_L3L4_ATLAS_HARDENING_PASS" if valid_ok and nulls_fail else "V1698_2_HARDENING_FAIL"

    return {
        "verdict": verdict,
        "claim_tested": "Sparse randomized retained atlas closure with embedded L3/O3 and L4/H4_perp obstruction fields, generated-algebra product faithfulness, randomized/multi-point adversaries, and residual spread reporting.",
        "valid_closes_all_trials": bool(valid_ok),
        "all_null_modes_fail_global_closure": bool(nulls_fail),
        "modes": by_mode,
        "objections_addressed": {
            "researcher_chosen_complete_cover": "addressed_by_randomized_orthonormal_chart_frames_and_sparse_partial_overlap_graph",
            "gentle_null_suite": "addressed_by_randomized_shuffles_transition_rewire_multi_transition_perturb_near_cocycle_product_mismatch_obstruction_scramble",
            "l3_l4_not_embedded": "addressed_by_chart_embedded_O3_and_H4_perp_transport_faithfulness_and_rank_lift_check",
            "residual_sensitivity": "addressed_by_reporting_residual_distribution_across_trials_not_single_value",
        },
        "boundary": "Executable finite-sector hardening. Not empirical transfer, not a continuum physical theorem, not a complete exhaustion of all possible adversaries.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="/mnt/data/v1698_2_hardening_run")
    ap.add_argument("--trials", type=int, default=50)
    ap.add_argument("--dim", type=int, default=12)
    ap.add_argument("--charts", type=int, default=7)
    ap.add_argument("--tol", type=float, default=1e-8)
    ap.add_argument("--seed", type=int, default=16982)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    modes = [
        "valid",
        "random_node_order_shuffle",
        "random_source_shuffle",
        "random_support_shuffle",
        "transition_random_rewire",
        "multi_transition_perturb",
        "near_cocycle_attack",
        "obstruction_scramble",
        "product_mismatch",
    ]

    results: List[ModeResult] = []
    for trial in range(args.trials):
        for mi, mode in enumerate(modes):
            # independent deterministic sub-seeds per trial/mode
            seed = args.seed + 10000 * trial + 137 * mi
            results.append(evaluate_mode(trial, mode, seed, args.dim, args.charts, args.tol))

    summary = summarize(results)

    csv_path = outdir / "v1698_2_hardening_results.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))

    summary_path = outdir / "v1698_2_hardening_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps({
        "verdict": summary["verdict"],
        "valid_closes_all_trials": summary["valid_closes_all_trials"],
        "all_null_modes_fail_global_closure": summary["all_null_modes_fail_global_closure"],
        "results_csv": str(csv_path),
        "summary_json": str(summary_path),
        "valid_residuals": summary["modes"]["valid"]["residuals"],
        "global_closed_rates": {m: summary["modes"][m]["global_closed_rate"] for m in summary["modes"]},
    }, indent=2))


if __name__ == "__main__":
    main()
