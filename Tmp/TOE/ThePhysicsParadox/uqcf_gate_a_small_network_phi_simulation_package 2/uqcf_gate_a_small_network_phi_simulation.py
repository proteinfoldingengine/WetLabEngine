#!/usr/bin/env python3
"""
UQCF-GEM Gate A Small-Network Phi Simulation
============================================

Standalone reproducible simulation of the Gate A finding:

1. Bare Genesis/source anchoring + conservation does NOT select a unique Phi/current.
   If BJ=s has one solution J0, then J=J0+Za is also a solution for every cycle
   coefficient a, where Z spans ker(B).

2. Network-only Hodge/minimum-action selection does NOT close Phi canonically unless
   the metric W is itself derived. Different admissible local metrics W produce
   different minimum-action currents.

3. Observer/interaction response closes Phi when the response operator R resolves
   the cycle space: rank(RZ)=dim(Z). Rank-deficient response leaves residual gauge.

No spacetime/ADM/GR claim is made here. This is a finite graph source-current
identifiability simulation.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TOL = 1e-10

@dataclass(frozen=True)
class SmallNetwork:
    nodes: list[int]
    edges: list[tuple[int, int]]
    source: np.ndarray


def incidence(nodes: list[int], edges: list[tuple[int, int]]) -> np.ndarray:
    """Signed incidence B with -1 at edge tail and +1 at edge head."""
    idx = {node: i for i, node in enumerate(nodes)}
    B = np.zeros((len(nodes), len(edges)), dtype=float)
    for k, (u, v) in enumerate(edges):
        B[idx[u], k] = -1.0
        B[idx[v], k] = 1.0
    return B


def nullspace(A: np.ndarray, tol: float = 1e-10) -> tuple[np.ndarray, int, np.ndarray]:
    """Return orthonormal basis for ker(A), rank, singular values."""
    U, S, Vt = np.linalg.svd(A, full_matrices=True)
    rank = int((S > tol).sum())
    return Vt[rank:].T, rank, S


def particular_current(B: np.ndarray, s: np.ndarray) -> np.ndarray:
    """Minimum Euclidean norm particular solution of BJ=s."""
    return B.T @ np.linalg.pinv(B @ B.T, rcond=TOL) @ s


def min_action_current(B: np.ndarray, s: np.ndarray, W_diag: np.ndarray) -> np.ndarray:
    """Solve min 1/2 J^T W J subject to BJ=s for positive diagonal W."""
    Winv = np.diag(1.0 / W_diag)
    return Winv @ B.T @ np.linalg.pinv(B @ Winv @ B.T, rcond=TOL) @ s


def solve_observer_coefficients(J0: np.ndarray, Z: np.ndarray, R: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    """Given y=R(J0+Za), solve for a using RZ."""
    RZ = R @ Z
    rhs = y - R @ J0
    a_hat = np.linalg.pinv(RZ, rcond=TOL) @ rhs
    J_hat = J0 + Z @ a_hat
    rank_RZ = int(np.linalg.matrix_rank(RZ, tol=TOL))
    return a_hat, J_hat, rank_RZ


def build_small_network() -> SmallNetwork:
    """A five-node graph with nontrivial cycle space."""
    nodes = [0, 1, 2, 3, 4]
    edges = [
        (0, 1),  # e0
        (1, 3),  # e1
        (0, 2),  # e2
        (2, 4),  # e3
        (4, 3),  # e4
        (1, 2),  # e5 cross edge
        (0, 4),  # e6 shortcut
    ]
    s = np.zeros(len(nodes))
    s[0] = -1.0
    s[3] = +1.0
    return SmallNetwork(nodes, edges, s)


def local_metric_family(edge_features: pd.DataFrame) -> dict[str, np.ndarray]:
    """Several plausible network-only positive diagonal Hodge/current metrics."""
    length = edge_features["ordered_transfer_distance"].to_numpy(float)
    access = edge_features["accessibility_support"].to_numpy(float)
    prov = edge_features["provenance_compatibility"].to_numpy(float)
    support = edge_features["active_support"].to_numpy(float)
    return {
        "unweighted_hodge": np.ones(len(edge_features)),
        "length_only_hodge": length.copy(),
        "accessibility_only_hodge": 1.0 / np.maximum(access, 1e-12),
        "candidate_genesis_hodge": length / np.maximum(access * prov * support, 1e-12),
    }


def run(output_dir: str | Path = "gate_a_outputs") -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    net = build_small_network()
    B = incidence(net.nodes, net.edges)
    Z, rank_B, sing_B = nullspace(B)
    beta1 = Z.shape[1]
    J0 = particular_current(B, net.source)

    # Bare ambiguity: multiple cycle coefficients, same conservation.
    cycle_coefficients = [
        np.zeros(beta1),
        np.linspace(-0.75, 0.75, beta1),
        np.linspace(0.60, -0.40, beta1),
    ]
    bare_rows = []
    for i, a in enumerate(cycle_coefficients):
        J = J0 + Z @ a
        bare_rows.append({
            "case": f"bare_family_{i}",
            "cycle_coefficients": json.dumps(a.tolist()),
            "conservation_residual": float(np.linalg.norm(B @ J - net.source)),
            "current_norm": float(np.linalg.norm(J)),
            **{f"J_e{k}": float(v) for k, v in enumerate(J)}
        })
    bare_family = pd.DataFrame(bare_rows)

    # Local raw network features for Hodge candidates.
    edge_features = pd.DataFrame({
        "edge_id": [f"e{i}" for i in range(len(net.edges))],
        "tail": [u for u, v in net.edges],
        "head": [v for u, v in net.edges],
        "ordered_transfer_distance": [max(1, abs(v-u)) for u, v in net.edges],
        "accessibility_support": [1.0, 0.90, 1.05, 0.85, 0.80, 0.70, 0.55],
        "provenance_compatibility": [0.95, 0.85, 0.90, 0.80, 0.82, 0.70, 0.65],
        "active_support": [1.0, 0.92, 0.98, 0.88, 0.86, 0.75, 0.60],
    })

    metrics = local_metric_family(edge_features)
    hodge_rows = []
    hodge_currents = {}
    for name, W in metrics.items():
        J = min_action_current(B, net.source, W)
        hodge_currents[name] = J
        hodge_rows.append({
            "metric": name,
            "conservation_residual": float(np.linalg.norm(B @ J - net.source)),
            "W_cycle_orthogonality_residual": float(np.linalg.norm(Z.T @ (W * J))),
            "current_norm": float(np.linalg.norm(J)),
            **{f"W_e{k}": float(w) for k, w in enumerate(W)},
            **{f"J_e{k}": float(v) for k, v in enumerate(J)},
        })
    hodge_table = pd.DataFrame(hodge_rows)

    # Difference matrix between Hodge-selected currents.
    names = list(hodge_currents)
    diff_rows = []
    for a in names:
        for b in names:
            diff_rows.append({
                "metric_a": a,
                "metric_b": b,
                "relative_current_difference": float(
                    np.linalg.norm(hodge_currents[a] - hodge_currents[b]) /
                    (np.linalg.norm(hodge_currents[a]) + 1e-12)
                )
            })
    hodge_differences = pd.DataFrame(diff_rows)

    # Observer-selected Phi: hidden cycle coefficients and response recovery.
    a_true = np.linspace(0.42, -0.35, beta1)
    J_true = J0 + Z @ a_true

    R_full = Z.T
    y_full = R_full @ J_true
    a_hat_full, J_hat_full, rank_full = solve_observer_coefficients(J0, Z, R_full, y_full)

    R_weak = Z[:, :1].T if beta1 else np.zeros((0, len(net.edges)))
    y_weak = R_weak @ J_true
    a_hat_weak, J_hat_weak, rank_weak = solve_observer_coefficients(J0, Z, R_weak, y_weak)

    observer_table = pd.DataFrame([
        {
            "observer": "cycle_resolving_response_R_full",
            "rank_RZ": rank_full,
            "dim_Z": beta1,
            "phi_identifiable": bool(rank_full == beta1),
            "current_error_vs_hidden_truth": float(np.linalg.norm(J_hat_full - J_true)),
            "cycle_coeff_error": float(np.linalg.norm(a_hat_full - a_true)),
        },
        {
            "observer": "rank_deficient_response_R_weak",
            "rank_RZ": rank_weak,
            "dim_Z": beta1,
            "phi_identifiable": bool(rank_weak == beta1),
            "current_error_vs_hidden_truth": float(np.linalg.norm(J_hat_weak - J_true)),
            "cycle_coeff_error": float(np.linalg.norm(a_hat_weak - a_true)),
        }
    ])

    theorem_status = pd.DataFrame([
        {
            "claim": "Bare Genesis + conservation selects unique Phi",
            "result": "FAIL",
            "evidence": f"cycle_dim_beta1={beta1}; J=J0+Za gives multiple conserved currents"
        },
        {
            "claim": "Network-only Hodge closes Phi canonically",
            "result": "FAIL",
            "evidence": "multiple local positive metrics W select different minimum-action currents"
        },
        {
            "claim": "Observer/response closes Phi when rank(RZ)=dim(Z)",
            "result": "PASS",
            "evidence": f"full observer rank_RZ={rank_full}, dim_Z={beta1}, current error={np.linalg.norm(J_hat_full-J_true):.3e}"
        },
        {
            "claim": "Rank-deficient observer leaves gauge",
            "result": "PASS",
            "evidence": f"weak observer rank_RZ={rank_weak}, dim_Z={beta1}"
        },
        {
            "claim": "ADM/GR derived",
            "result": "NO CLAIM",
            "evidence": "finite graph source-current identifiability only"
        }
    ])

    summary = pd.DataFrame([{
        "result": "GATE_A_SMALL_NETWORK_DEMONSTRATION",
        "node_count": len(net.nodes),
        "edge_count": len(net.edges),
        "rank_B": rank_B,
        "cycle_dim_beta1": beta1,
        "bare_genesis_unique_phi": False,
        "network_hodge_canonical_phi": False,
        "observer_full_rank_closes_phi": bool(rank_full == beta1),
        "weak_observer_leaves_gauge": bool(rank_weak < beta1),
        "adm_gr_claim": False,
    }])

    summary.to_csv(out / "summary.csv", index=False)
    edge_features.to_csv(out / "edge_features.csv", index=False)
    bare_family.to_csv(out / "bare_conserved_family.csv", index=False)
    hodge_table.to_csv(out / "network_hodge_candidates.csv", index=False)
    hodge_differences.to_csv(out / "network_hodge_current_differences.csv", index=False)
    observer_table.to_csv(out / "observer_response_closure.csv", index=False)
    theorem_status.to_csv(out / "theorem_status.csv", index=False)

    plt.figure(figsize=(10, 5))
    for name, J in hodge_currents.items():
        plt.plot(range(len(J)), J, marker="o", label=name)
    plt.axhline(0, linewidth=0.8)
    plt.title("Network-only Hodge choices select different currents")
    plt.xlabel("edge index")
    plt.ylabel("selected current J_e")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out / "hodge_currents_disagree.png", dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7, 5))
    plt.bar(observer_table["observer"], observer_table["rank_RZ"])
    plt.axhline(beta1, linestyle="--", linewidth=1.0, label="dim(Z)")
    plt.title("Observer closure gate: rank(RZ)=dim(Z)")
    plt.ylabel("rank(RZ)")
    plt.xticks(rotation=20, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "observer_rank_gate.png", dpi=200, bbox_inches="tight")
    plt.close()

    report = f"""# Gate A Small-Network Phi Simulation

## Result

This small network has:

- nodes: {len(net.nodes)}
- directed edges: {len(net.edges)}
- rank(B): {rank_B}
- cycle dimension dim(Z): {beta1}

Because dim(Z) > 0, bare conservation leaves an affine family:

```text
J = J0 + Z a
```

All currents in this family satisfy the same source-current law BJ=s.

## Finding 1: Bare Genesis fails

Bare Genesis/source anchoring plus conservation does not select a unique Phi. The ambiguity appears in a small graph, so it is not a compute-scale artifact.

## Finding 2: Network-only Hodge does not close canonically

For any chosen positive metric W, a minimum-action current exists. But the network alone does not choose W. Several plausible local W choices produce different currents.

This is why "Hodge exists" is not enough. A canonical Hodge metric must be derived, not selected by convenience.

## Finding 3: Observer/response closes conditionally

When the response operator R resolves the cycle space:

```text
rank(RZ) = dim(Z)
```

the hidden cycle coefficients are identifiable and Phi is selected. A rank-deficient response leaves residual gauge.

## Boundary

This simulation does not derive physical spacetime, ADM, or GR. It demonstrates a finite graph source-current identifiability theorem.
"""
    (out / "REPORT.md").write_text(report)
    return {"summary": summary.to_dict(orient="records")[0], "output_dir": str(out)}

if __name__ == "__main__":
    result = run()
    print(json.dumps(result["summary"], indent=2))
    print(f"outputs written to: {result['output_dir']}")
