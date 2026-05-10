#!/usr/bin/env python3
"""
Retained Branch Identity / Lineage Addressability Audit
=======================================================

Standalone toy-model audit for testing the current UQCF-GEM-inspired mechanism branch:

    retained coherence
    + lineage addressability
    + reference-frame anchors
    + moderate phase-lock synchronization
    -> observer-compatible causal accessibility geometry

This script is NOT a GR derivation, NOT physical validation, and NOT a TOE proof.
It is a bounded computational toy audit for another AI / researcher to run and inspect.

Main experiments included:
1. Addressability integrity scaling
2. Hysteresis / collapse-recovery threshold
3. Seed nucleation and seed placement
4. Repair wave by lineage distance
5. Root-frame corruption threshold
6. Federated frame phase-locking window

Outputs:
    retained_branch_identity_audit_outputs/
        case_results.csv
        summaries.json
        README_RESULTS.md

Run:
    python retained_branch_identity_audit.py
"""

from __future__ import annotations

import csv
import json
import math
import os
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np


# -----------------------------
# Configuration
# -----------------------------

OUT_DIR = Path("retained_branch_identity_audit_outputs")
SEEDS = list(range(20))
DEPTHS = [4, 5, 6]
BRANCH_FACTORS = [2, 3]
DIM = 12
RETAIN = 0.90
NOISE = 0.15

ADDRESS_INTEGRITIES = np.linspace(0.0, 1.0, 11)
ALIGNMENT_STRENGTHS = np.linspace(0.0, 1.0, 11)
ROOT_INTEGRITIES = np.linspace(0.0, 1.0, 11)
SEED_FRACTIONS = [0.0, 0.005, 0.01, 0.03, 0.05, 0.10, 0.20]


# -----------------------------
# Tree / lineage utilities
# -----------------------------

@dataclass
class Tree:
    parent: np.ndarray
    depth: np.ndarray
    children: List[List[int]]
    n: int
    leaves: np.ndarray


def build_kary_tree(depth: int, branch_factor: int) -> Tree:
    parent = [-1]
    node_depth = [0]
    children = [[]]

    current = [0]
    for d in range(1, depth + 1):
        nxt = []
        for p in current:
            for _ in range(branch_factor):
                idx = len(parent)
                parent.append(p)
                node_depth.append(d)
                children.append([])
                children[p].append(idx)
                nxt.append(idx)
        current = nxt

    parent = np.array(parent, dtype=int)
    node_depth = np.array(node_depth, dtype=int)
    leaves = np.array([i for i, ch in enumerate(children) if len(ch) == 0], dtype=int)
    return Tree(parent=parent, depth=node_depth, children=children, n=len(parent), leaves=leaves)


def ancestors(tree: Tree, node: int) -> List[int]:
    out = []
    while node >= 0:
        out.append(node)
        node = int(tree.parent[node])
    return out


def lca(tree: Tree, a: int, b: int) -> int:
    aa = set(ancestors(tree, a))
    while b not in aa:
        b = int(tree.parent[b])
    return b


def tree_distance_matrix(tree: Tree) -> np.ndarray:
    leaves = tree.leaves
    m = len(leaves)
    D = np.zeros((m, m), dtype=float)
    anc_cache = {int(x): ancestors(tree, int(x)) for x in leaves}
    anc_sets = {int(x): set(anc_cache[int(x)]) for x in leaves}

    for i, a in enumerate(leaves):
        for j in range(i + 1, m):
            b = int(leaves[j])
            # LCA by walking b upward
            bb = b
            aset = anc_sets[int(a)]
            while bb not in aset:
                bb = int(tree.parent[bb])
            l = bb
            dist = tree.depth[int(a)] + tree.depth[b] - 2 * tree.depth[l]
            D[i, j] = D[j, i] = dist
    return D


def adjacency(tree: Tree) -> List[List[int]]:
    adj = [[] for _ in range(tree.n)]
    for i, p in enumerate(tree.parent):
        if p >= 0:
            adj[i].append(int(p))
            adj[int(p)].append(i)
    return adj


def leaf_to_node_index(tree: Tree) -> Dict[int, int]:
    return {int(node): idx for idx, node in enumerate(tree.leaves)}


# -----------------------------
# State generation and metrics
# -----------------------------

def generate_retained_state(tree: Tree, rng: np.random.Generator, retain: float = RETAIN, dim: int = DIM, noise: float = NOISE) -> np.ndarray:
    """
    Generates branch states where child vectors retain parent identity plus innovation.
    """
    X = np.zeros((tree.n, dim), dtype=float)
    X[0] = rng.normal(size=dim)
    X[0] /= np.linalg.norm(X[0]) + 1e-12

    for i in range(1, tree.n):
        p = int(tree.parent[i])
        innov = rng.normal(size=dim)
        innov /= np.linalg.norm(innov) + 1e-12
        X[i] = retain * X[p] + math.sqrt(max(1e-12, 1 - retain**2)) * innov + noise * rng.normal(size=dim)
        X[i] /= np.linalg.norm(X[i]) + 1e-12
    return X


def leaf_state_distance(X: np.ndarray, tree: Tree) -> np.ndarray:
    Y = X[tree.leaves]
    # cosine distance
    S = Y @ Y.T
    S = np.clip(S, -1, 1)
    return 1.0 - S


def corr_flat(A: np.ndarray, B: np.ndarray) -> float:
    mask = ~np.eye(A.shape[0], dtype=bool)
    a = A[mask].ravel()
    b = B[mask].ravel()
    if np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def geometry_corr(X: np.ndarray, tree: Tree, true_D: np.ndarray | None = None) -> float:
    if true_D is None:
        true_D = tree_distance_matrix(tree)
    pred_D = leaf_state_distance(X, tree)
    # tree distance vs cosine distance should be positively correlated
    return corr_flat(true_D, pred_D)


def observer_consistency(X: np.ndarray, tree: Tree, observers: int = 8) -> float:
    """
    Toy observer consistency:
    compare nearest-neighbor rankings among randomly selected observer leaves.
    Higher means observers infer compatible neighborhood structure.
    """
    leaves = tree.leaves
    Y = X[leaves]
    D = 1.0 - np.clip(Y @ Y.T, -1, 1)
    m = len(leaves)
    if m < 4:
        return 1.0

    obs_idx = np.linspace(0, m - 1, min(observers, m), dtype=int)
    rank_vectors = []
    for oi in obs_idx:
        order = np.argsort(D[oi])
        # binary near-neighborhood
        k = max(2, m // 8)
        v = np.zeros(m)
        v[order[:k]] = 1.0
        rank_vectors.append(v)

    vals = []
    for i in range(len(rank_vectors)):
        for j in range(i + 1, len(rank_vectors)):
            vals.append(float(np.dot(rank_vectors[i], rank_vectors[j]) / (np.linalg.norm(rank_vectors[i]) * np.linalg.norm(rank_vectors[j]) + 1e-12)))
    return float(np.mean(vals)) if vals else 0.0


def damage_raw_state(X: np.ndarray, rng: np.random.Generator, mix: float = 0.80) -> np.ndarray:
    """
    Heavy raw-state damage by random mixing/permutation and noise.
    """
    Xd = X.copy()
    perm = rng.permutation(len(Xd))
    Xd = (1 - mix) * Xd + mix * Xd[perm]
    Xd += 0.25 * mix * rng.normal(size=Xd.shape)
    Xd /= np.linalg.norm(Xd, axis=1, keepdims=True) + 1e-12
    return Xd


def corrupt_address_map(n: int, integrity: float, rng: np.random.Generator) -> np.ndarray:
    """
    Address map: maps node -> remembered lineage-address node.
    integrity=1 means identity map, 0 means random permutation.
    """
    address = np.arange(n)
    corrupt = rng.random(n) > integrity
    perm = rng.permutation(n)
    address[corrupt] = perm[corrupt]
    address[0] = 0  # root is separately handled in root-frame tests
    return address


def repair_with_address(X_damaged: np.ndarray, X_memory: np.ndarray, address: np.ndarray, strength: float = 0.85) -> np.ndarray:
    """
    Repair raw state using addressability relation.
    If address is correct, each node pulls toward its own lineage memory.
    If corrupted, it pulls toward wrong memory.
    """
    Xr = (1 - strength) * X_damaged + strength * X_memory[address]
    Xr /= np.linalg.norm(Xr, axis=1, keepdims=True) + 1e-12
    return Xr


# -----------------------------
# Experiment 1: addressability scaling
# -----------------------------

def experiment_addressability_scaling(rows: List[Dict]) -> Dict:
    summary = defaultdict(list)
    for depth in DEPTHS:
        for bf in BRANCH_FACTORS:
            tree = build_kary_tree(depth, bf)
            true_D = tree_distance_matrix(tree)
            for seed in SEEDS:
                rng = np.random.default_rng(seed + 1000 * depth + 100 * bf)
                X = generate_retained_state(tree, rng)
                Xd = damage_raw_state(X, rng, mix=0.8)
                for integrity in ADDRESS_INTEGRITIES:
                    addr = corrupt_address_map(tree.n, float(integrity), rng)
                    Xr = repair_with_address(Xd, X, addr)
                    gc = geometry_corr(Xr, tree, true_D)
                    oc = observer_consistency(Xr, tree)
                    row = dict(
                        experiment="addressability_scaling",
                        depth=depth, branch_factor=bf, seed=seed,
                        address_integrity=float(integrity),
                        geometry_corr=gc,
                        observer_consistency=oc,
                    )
                    rows.append(row)
                    summary[float(integrity)].append(gc)

    means = {str(k): float(np.mean(v)) for k, v in summary.items()}
    return {"addressability_scaling_mean_geometry_corr": means}


# -----------------------------
# Experiment 2: hysteresis
# -----------------------------

def experiment_hysteresis(rows: List[Dict]) -> Dict:
    """
    Collapse path and recovery path differ. Toy implementation uses prior collapse state
    as additional damage during repair path.
    """
    collapse_thresholds = []
    recovery_thresholds = []

    for seed in SEEDS:
        tree = build_kary_tree(5, 2)
        true_D = tree_distance_matrix(tree)
        rng = np.random.default_rng(5000 + seed)
        X = generate_retained_state(tree, rng)
        Xd = damage_raw_state(X, rng, mix=0.8)

        collapse_vals = []
        for integrity in ADDRESS_INTEGRITIES[::-1]:
            addr = corrupt_address_map(tree.n, float(integrity), rng)
            Xr = repair_with_address(Xd, X, addr)
            gc = geometry_corr(Xr, tree, true_D)
            collapse_vals.append((float(integrity), gc))
            rows.append(dict(experiment="hysteresis_collapse", seed=seed, address_integrity=float(integrity), geometry_corr=gc))

        # Recovery starts from collapsed mixed state, requiring more integrity.
        Xcollapsed = damage_raw_state(Xd, rng, mix=1.0)
        recovery_vals = []
        for integrity in ADDRESS_INTEGRITIES:
            addr = corrupt_address_map(tree.n, float(integrity), rng)
            Xr = repair_with_address(Xcollapsed, X, addr, strength=0.70)
            gc = geometry_corr(Xr, tree, true_D)
            recovery_vals.append((float(integrity), gc))
            rows.append(dict(experiment="hysteresis_recovery", seed=seed, address_integrity=float(integrity), geometry_corr=gc))

        # Threshold = first crossing of 0.25 geometry_corr
        cthr = next((i for i, gc in collapse_vals if gc < 0.25), 0.0)
        rthr = next((i for i, gc in recovery_vals if gc > 0.25), 1.0)
        collapse_thresholds.append(cthr)
        recovery_thresholds.append(rthr)

    return {
        "hysteresis_collapse_threshold_mean": float(np.mean(collapse_thresholds)),
        "hysteresis_recovery_threshold_mean": float(np.mean(recovery_thresholds)),
        "hysteresis_gap_mean": float(np.mean(recovery_thresholds) - np.mean(collapse_thresholds)),
    }


# -----------------------------
# Experiment 3: seed placement and nucleation
# -----------------------------

def select_seeds(tree: Tree, strategy: str, fraction: float, rng: np.random.Generator) -> np.ndarray:
    n_seed = max(1, int(round(fraction * tree.n)))
    nodes = np.arange(tree.n)

    if strategy == "random":
        return rng.choice(nodes, size=n_seed, replace=False)

    if strategy == "root":
        # root and shallow nodes
        order = np.argsort(tree.depth)
        return order[:n_seed]

    if strategy == "mid":
        target = np.median(tree.depth)
        order = np.argsort(np.abs(tree.depth - target))
        return order[:n_seed]

    if strategy == "leaf":
        leaves = tree.leaves
        return rng.choice(leaves, size=min(n_seed, len(leaves)), replace=False)

    if strategy == "central":
        # degree centrality
        deg = np.array([len(c) + (0 if p < 0 else 1) for c, p in zip(tree.children, tree.parent)])
        order = np.argsort(-deg)
        return order[:n_seed]

    if strategy == "multiscale":
        groups = []
        for d in sorted(set(tree.depth)):
            group = np.where(tree.depth == d)[0]
            if len(group):
                groups.append(int(rng.choice(group)))
        # fill remainder randomly
        selected = list(dict.fromkeys(groups))
        while len(selected) < n_seed:
            x = int(rng.choice(nodes))
            if x not in selected:
                selected.append(x)
        return np.array(selected[:n_seed], dtype=int)

    if strategy == "clustered":
        center = int(rng.choice(nodes))
        adj = adjacency(tree)
        seen = {center}
        q = deque([center])
        while q and len(seen) < n_seed:
            u = q.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
                    if len(seen) >= n_seed:
                        break
        return np.array(list(seen), dtype=int)

    raise ValueError(strategy)


def seed_repair(Xd: np.ndarray, Xmem: np.ndarray, tree: Tree, seeds: np.ndarray, steps: int = 5, strength: float = 0.65) -> np.ndarray:
    """
    Local repair wave: seeds are restored; neighbors pull toward repaired nodes.
    """
    X = Xd.copy()
    adj = adjacency(tree)

    X[seeds] = Xmem[seeds]
    for _ in range(steps):
        Xnew = X.copy()
        for u in range(tree.n):
            neigh = adj[u]
            if not neigh:
                continue
            neigh_mean = np.mean(X[neigh], axis=0)
            Xnew[u] = (1 - strength) * X[u] + strength * neigh_mean
        # keep seeds protected
        Xnew[seeds] = Xmem[seeds]
        Xnew /= np.linalg.norm(Xnew, axis=1, keepdims=True) + 1e-12
        X = Xnew
    return X


def experiment_seed_placement(rows: List[Dict]) -> Dict:
    strategies = ["random", "root", "central", "mid", "multiscale", "leaf", "clustered"]
    fraction = 0.05
    scores = defaultdict(list)

    for seed in SEEDS:
        tree = build_kary_tree(5, 2)
        true_D = tree_distance_matrix(tree)
        rng = np.random.default_rng(8000 + seed)
        X = generate_retained_state(tree, rng)
        Xd = damage_raw_state(X, rng, mix=0.9)

        for strategy in strategies:
            s = select_seeds(tree, strategy, fraction, rng)
            Xr = seed_repair(Xd, X, tree, s)
            gc = geometry_corr(Xr, tree, true_D)
            oc = observer_consistency(Xr, tree)
            score = 0.55 * oc + 0.45 * max(0.0, gc)
            rows.append(dict(
                experiment="seed_placement",
                seed=seed,
                strategy=strategy,
                seed_fraction=fraction,
                geometry_corr=gc,
                observer_consistency=oc,
                observer_weighted_score=score,
            ))
            scores[strategy].append(score)

    return {"seed_placement_observer_weighted_score_mean": {k: float(np.mean(v)) for k, v in scores.items()}}


# -----------------------------
# Experiment 4: repair wave by lineage distance
# -----------------------------

def lineage_distance_to_seeds(tree: Tree, seeds: np.ndarray) -> np.ndarray:
    adj = adjacency(tree)
    dist = np.full(tree.n, np.inf)
    q = deque()
    for s in seeds:
        dist[int(s)] = 0
        q.append(int(s))
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def experiment_repair_wave(rows: List[Dict]) -> Dict:
    shell_repair = defaultdict(list)
    for seed in SEEDS:
        tree = build_kary_tree(5, 2)
        rng = np.random.default_rng(9000 + seed)
        X = generate_retained_state(tree, rng)
        Xd = damage_raw_state(X, rng, mix=0.9)

        seeds = select_seeds(tree, "central", 0.05, rng)
        dist = lineage_distance_to_seeds(tree, seeds)
        Xr = seed_repair(Xd, X, tree, seeds, steps=5)

        # nodewise repair quality: cosine to original memory
        repair = np.sum(Xr * X, axis=1)
        for d in sorted(set(dist[np.isfinite(dist)].astype(int))):
            vals = repair[dist == d]
            mean_repair = float(np.mean(vals))
            shell_repair[int(d)].append(mean_repair)
            rows.append(dict(experiment="repair_wave", seed=seed, shell_distance=int(d), repair_quality=mean_repair))

    return {"repair_wave_quality_by_shell": {str(k): float(np.mean(v)) for k, v in shell_repair.items()}}


# -----------------------------
# Experiment 5: root-frame threshold
# -----------------------------

def apply_root_frame_corruption(Xmem: np.ndarray, tree: Tree, root_integrity: float, rng: np.random.Generator) -> np.ndarray:
    """
    Corrupts shared shallow reference frame memory, then propagates partial corruption downstream.
    """
    Xc = Xmem.copy()
    shallow = np.where(tree.depth <= 2)[0]
    corrupt = rng.random(len(shallow)) > root_integrity
    noise = rng.normal(size=(len(shallow), Xmem.shape[1]))
    noise /= np.linalg.norm(noise, axis=1, keepdims=True) + 1e-12
    Xc[shallow[corrupt]] = noise[corrupt]

    # Downstream nodes inherit some shallow frame corruption via nearest ancestor <=2.
    for i in range(tree.n):
        a = i
        while tree.parent[a] >= 0 and tree.depth[a] > 2:
            a = int(tree.parent[a])
        if a in shallow:
            Xc[i] = 0.65 * Xc[i] + 0.35 * Xc[a]
            Xc[i] /= np.linalg.norm(Xc[i]) + 1e-12
    return Xc


def experiment_root_threshold(rows: List[Dict]) -> Dict:
    by_integrity = defaultdict(list)
    for seed in SEEDS:
        tree = build_kary_tree(5, 2)
        true_D = tree_distance_matrix(tree)
        rng = np.random.default_rng(10000 + seed)
        X = generate_retained_state(tree, rng)
        Xd = damage_raw_state(X, rng, mix=0.8)
        address = np.arange(tree.n)

        for ri in ROOT_INTEGRITIES:
            Xmem_corrupt = apply_root_frame_corruption(X, tree, float(ri), rng)
            Xr = repair_with_address(Xd, Xmem_corrupt, address)
            gc = geometry_corr(Xr, tree, true_D)
            oc = observer_consistency(Xr, tree)
            rows.append(dict(experiment="root_frame_threshold", seed=seed, root_integrity=float(ri), geometry_corr=gc, observer_consistency=oc))
            by_integrity[float(ri)].append(gc)

    return {"root_frame_threshold_geometry_corr_mean": {str(k): float(np.mean(v)) for k, v in by_integrity.items()}}


# -----------------------------
# Experiment 6: federated phase locking
# -----------------------------

def federated_frame_repair(Xd: np.ndarray, Xmem: np.ndarray, tree: Tree, alignment: float, rng: np.random.Generator) -> np.ndarray:
    """
    Toy federated frame synchronization:
    split leaves into local islands by depth-2 ancestors.
    Each island repairs locally; then moderate alignment synchronizes island frames.
    Too much alignment creates smoothing collapse.
    """
    X = Xd.copy()
    # identify island roots at depth 2
    island_roots = np.where(tree.depth == min(2, tree.depth.max()))[0]
    if len(island_roots) == 0:
        return X

    # local island assignment
    island_of = np.zeros(tree.n, dtype=int)
    for i in range(tree.n):
        a = i
        while tree.parent[a] >= 0 and tree.depth[a] > 2:
            a = int(tree.parent[a])
        # closest island index
        matches = np.where(island_roots == a)[0]
        island_of[i] = int(matches[0]) if len(matches) else 0

    # local repair
    for k in range(len(island_roots)):
        nodes = np.where(island_of == k)[0]
        local_anchor = np.mean(Xmem[nodes], axis=0)
        local_anchor /= np.linalg.norm(local_anchor) + 1e-12
        X[nodes] = 0.55 * X[nodes] + 0.45 * local_anchor
        X[nodes] /= np.linalg.norm(X[nodes], axis=1, keepdims=True) + 1e-12

    # global frame alignment; moderate helps, excessive smooths
    global_anchor = np.mean([np.mean(X[island_of == k], axis=0) for k in range(len(island_roots))], axis=0)
    global_anchor /= np.linalg.norm(global_anchor) + 1e-12

    Xsyn = (1 - alignment) * X + alignment * global_anchor
    Xsyn /= np.linalg.norm(Xsyn, axis=1, keepdims=True) + 1e-12
    return Xsyn


def lineage_specificity(X: np.ndarray, tree: Tree) -> float:
    """
    Penalizes global smoothing: leaf vectors should not all collapse to one vector.
    """
    Y = X[tree.leaves]
    sim = Y @ Y.T
    mask = ~np.eye(len(Y), dtype=bool)
    # lower average off-diagonal similarity means more specificity
    return float(1.0 - np.mean(sim[mask]))


def experiment_phase_locking(rows: List[Dict]) -> Dict:
    by_align = defaultdict(list)
    for seed in SEEDS:
        tree = build_kary_tree(5, 2)
        true_D = tree_distance_matrix(tree)
        rng = np.random.default_rng(11000 + seed)
        X = generate_retained_state(tree, rng)
        Xd = damage_raw_state(X, rng, mix=0.85)

        for a in ALIGNMENT_STRENGTHS:
            Xr = federated_frame_repair(Xd, X, tree, float(a), rng)
            gc = geometry_corr(Xr, tree, true_D)
            oc = observer_consistency(Xr, tree)
            spec = lineage_specificity(Xr, tree)
            # balanced phase-lock score: wants geometry and observer agreement, but penalizes smoothing collapse
            score = 0.40 * max(0.0, gc) + 0.40 * oc + 0.20 * max(0.0, spec)
            rows.append(dict(
                experiment="phase_locking",
                seed=seed,
                alignment_strength=float(a),
                geometry_corr=gc,
                observer_consistency=oc,
                lineage_specificity=spec,
                phase_lock_score=score,
            ))
            by_align[float(a)].append(score)

    return {"phase_lock_score_by_alignment": {str(k): float(np.mean(v)) for k, v in by_align.items()}}


# -----------------------------
# Main
# -----------------------------

def write_csv(path: Path, rows: List[Dict]) -> None:
    keys = sorted(set().union(*(r.keys() for r in rows)))
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def make_readme(summaries: Dict) -> str:
    return f"""# Retained Branch Identity / Lineage Addressability Audit

## Claim boundary

This is a toy-model computational audit. It does **not** claim GR recovery, Einstein equation derivation,
external physics validation, or TOE proof.

## Mechanism under test

retained coherence
+ lineage addressability
+ reference-frame anchors
+ moderate phase-lock synchronization
-> observer-compatible causal accessibility geometry

## What to inspect

- `case_results.csv`: all case-level metrics
- `summaries.json`: aggregate summary curves and thresholds

## Key questions

1. Does recoverable causal geometry scale with addressability integrity?
2. Is there hysteresis after lineage collapse?
3. Do seed placement and root-frame anchors matter?
4. Does repair propagate through lineage distance rather than global smoothing?
5. Is there a moderate phase-locking window for federated partial frames?

## Summary JSON

```json
{json.dumps(summaries, indent=2)}
```
"""


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    rows: List[Dict] = []
    summaries: Dict = {}

    print("Running addressability scaling...")
    summaries.update(experiment_addressability_scaling(rows))

    print("Running hysteresis...")
    summaries.update(experiment_hysteresis(rows))

    print("Running seed placement...")
    summaries.update(experiment_seed_placement(rows))

    print("Running repair wave...")
    summaries.update(experiment_repair_wave(rows))

    print("Running root-frame threshold...")
    summaries.update(experiment_root_threshold(rows))

    print("Running phase-locking...")
    summaries.update(experiment_phase_locking(rows))

    write_csv(OUT_DIR / "case_results.csv", rows)
    (OUT_DIR / "summaries.json").write_text(json.dumps(summaries, indent=2, sort_keys=True))
    (OUT_DIR / "README_RESULTS.md").write_text(make_readme(summaries))

    print("\nDone.")
    print(f"Output directory: {OUT_DIR.resolve()}")
    print("\nSummary:")
    print(json.dumps(summaries, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
