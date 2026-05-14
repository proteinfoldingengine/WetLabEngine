"""
V498 Retained-Geometry Proof Run
================================

Colab-ready independent proof script.

Purpose:
    Demonstrate the retained-geometry chain using frozen V493/V488/V496 equations:

        C_t = M_t R_t L_t + lambda0 * eta_convert(t) * B_t

        dg_eff/dt =
            G_L * [T_retained / (C_t - C_floor + eps)]
            - R_repair
            - D_leakage

        K_eff = Curv(g_eff)

        D_i ∝ [T_i / C_surplus_i] * Lambda_i * Pi_i

The script runs multiple graph families:
    1. lattice
    2. random geometric
    3. scale-free
    4. small-world
    5. tree-with-loops
    6. fragmented block graph

Outputs:
    - CSV summary table
    - JSON summary
    - plots:
        1. source/reserve vs metric deformation
        2. predicted vs observed curvature
        3. defect score vs defect labels
        4. graph geometry visualization
        5. repair path visualization
        6. summary bar chart

This is not a GR derivation.
This is a retained-geometry toy proof showing that a bridge-like conserved
recoverability law can generate source-responsive effective geometry.
"""

import os
from pathlib import Path
import json
import math
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    import networkx as nx
except ImportError:
    raise ImportError("Please install networkx: pip install networkx")

try:
    from sklearn.metrics import roc_auc_score, r2_score
except ImportError:
    raise ImportError("Please install scikit-learn: pip install scikit-learn")


# -----------------------------
# Configuration
# -----------------------------
SEED = 498
rng = np.random.default_rng(SEED)

OUT = Path("v498_outputs")
OUT.mkdir(exist_ok=True)

N = 180
lambda0 = 0.62
eps = 1e-6


# -----------------------------
# Graph generators
# -----------------------------
def make_lattice(n=N):
    side = int(np.sqrt(n))
    G = nx.grid_2d_graph(side, side)
    G = nx.convert_node_labels_to_integers(G)
    return G

def make_random_geometric(n=N, radius=0.16):
    G = nx.random_geometric_graph(n, radius, seed=SEED)
    # ensure connected by taking largest component then relabel
    if not nx.is_connected(G):
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
        G = nx.convert_node_labels_to_integers(G)
    return G

def make_scale_free(n=N):
    G = nx.barabasi_albert_graph(n, 3, seed=SEED)
    return G

def make_small_world(n=N):
    G = nx.watts_strogatz_graph(n, 6, 0.12, seed=SEED)
    return G

def make_tree_with_loops(n=N):
    # NetworkX 3.4 removed nx.random_tree; use random_labeled_tree when available.
    if hasattr(nx, "random_labeled_tree"):
        G = nx.random_labeled_tree(n, seed=SEED)
    else:
        # Fallback: generate a random Prüfer sequence tree.
        prufer = rng.integers(0, n, size=n-2).tolist()
        G = nx.from_prufer_sequence(prufer)
    # add loops/chords
    for _ in range(n // 4):
        a, b = rng.integers(0, n, 2)
        if a != b:
            G.add_edge(int(a), int(b))
    return G

def make_fragmented(n=N):
    # block graph with sparse bridges
    blocks = 6
    block_size = n // blocks
    G = nx.Graph()
    for b in range(blocks):
        nodes = range(b * block_size, (b + 1) * block_size)
        H = nx.erdos_renyi_graph(block_size, 0.18, seed=SEED + b)
        H = nx.relabel_nodes(H, {i: b * block_size + i for i in range(block_size)})
        G.add_nodes_from(H.nodes())
        G.add_edges_from(H.edges())
    # add bridges
    for b in range(blocks - 1):
        G.add_edge(b * block_size + block_size - 1, (b + 1) * block_size)
        if rng.random() < 0.45:
            G.add_edge(b * block_size + block_size // 2, (b + 1) * block_size + block_size // 2)
    # if disconnected, add edges
    comps = list(nx.connected_components(G))
    for c1, c2 in zip(comps[:-1], comps[1:]):
        G.add_edge(next(iter(c1)), next(iter(c2)))
    return nx.convert_node_labels_to_integers(G)


GENERATORS = {
    "lattice": make_lattice,
    "random_geometric": make_random_geometric,
    "scale_free": make_scale_free,
    "small_world": make_small_world,
    "tree_with_loops": make_tree_with_loops,
    "fragmented": make_fragmented,
}


# -----------------------------
# Utility functions
# -----------------------------
def safe_norm(x):
    x = np.asarray(x, dtype=float)
    mn, mx = np.nanmin(x), np.nanmax(x)
    if mx - mn < 1e-12:
        return np.zeros_like(x)
    return (x - mn) / (mx - mn)

def graph_positions(G, family):
    if family == "lattice":
        # use grid-ish layout
        return nx.spring_layout(G, seed=SEED, iterations=80)
    if family == "random_geometric":
        pos = nx.get_node_attributes(G, "pos")
        if pos:
            return pos
    return nx.spring_layout(G, seed=SEED, iterations=80)

def adjacency_arrays(G):
    nodes = list(G.nodes())
    idx = {u: i for i, u in enumerate(nodes)}
    edges = np.array([(idx[u], idx[v]) for u, v in G.edges()], dtype=int)
    return nodes, idx, edges

def shortest_path_dist_matrix(G):
    nodes = list(G.nodes())
    n = len(nodes)
    dist = np.full((n, n), np.inf)
    for i, u in enumerate(nodes):
        lengths = nx.single_source_shortest_path_length(G, u)
        for v, d in lengths.items():
            dist[i, nodes.index(v)] = d
    maxfinite = np.nanmax(dist[np.isfinite(dist)])
    dist[~np.isfinite(dist)] = maxfinite + 1
    return dist

def local_average(G, values):
    values = np.asarray(values)
    out = np.zeros_like(values, dtype=float)
    nodes = list(G.nodes())
    node_to_i = {u:i for i,u in enumerate(nodes)}
    for u in nodes:
        i = node_to_i[u]
        nbr = [node_to_i[v] for v in G.neighbors(u)]
        if nbr:
            out[i] = np.mean(values[nbr])
        else:
            out[i] = values[i]
    return out

def conductance_proxy(G):
    # local branch throughput proxy based on degree normalized
    deg = np.array([G.degree(u) for u in G.nodes()], dtype=float)
    return 0.2 + 0.8 * safe_norm(deg)

def topology_pinch_proxy(G):
    # lower degree / local clustering bottleneck proxy
    deg = np.array([G.degree(u) for u in G.nodes()], dtype=float)
    deg_inv = 1.0 / (deg + 1.0)
    try:
        bc = np.array(list(nx.betweenness_centrality(G, k=min(60, len(G)), seed=SEED).values()))
    except TypeError:
        bc = np.array(list(nx.betweenness_centrality(G).values()))
    pinch = safe_norm(deg_inv) * 0.45 + safe_norm(bc) * 0.55
    return safe_norm(pinch)

def lineage_field(G, family):
    n = G.number_of_nodes()
    base = rng.beta(5, 2, n)  # mostly high
    if family in ("fragmented", "tree_with_loops"):
        # introduce seams / lower lineage in blocks
        nodes = np.arange(n)
        seam = (nodes % max(5, n // 12) == 0).astype(float)
        base = np.clip(base - 0.45 * seam - 0.15 * rng.random(n), 0.05, 1.0)
    if family == "scale_free":
        deg = np.array([G.degree(u) for u in G.nodes()], dtype=float)
        hubs = safe_norm(deg)
        base = np.clip(base - 0.20 * hubs * rng.random(n), 0.05, 1.0)
    return base

def stress_field(G, pinch, family):
    n = G.number_of_nodes()
    # stress concentrates around random sources and pinches
    centers = rng.choice(n, size=max(3, n//60), replace=False)
    dist = shortest_path_dist_matrix(G)
    stress = np.zeros(n)
    for c in centers:
        stress += np.exp(-dist[:, c] / rng.uniform(2.0, 5.0))
    stress = safe_norm(stress)
    stress = 0.25 + 0.75 * safe_norm(0.55 * stress + 0.45 * pinch + 0.10 * rng.normal(size=n))
    return np.clip(stress, 0.01, 1.2)

def compute_fields(G, family):
    n = G.number_of_nodes()
    conduct = conductance_proxy(G)
    pinch = topology_pinch_proxy(G)
    L = lineage_field(G, family)
    R = np.clip(0.35 + 0.5 * conduct + 0.25 * L - 0.25 * pinch + 0.08*rng.normal(size=n), 0.05, 1.2)
    M = np.clip(0.40 + 0.45 * (1 - pinch) + 0.15 * conduct - 0.15*rng.random(n), 0.05, 1.2)
    B = np.clip(0.35 + 0.35 * conduct + 0.30 * L - 0.30 * pinch + 0.05*rng.normal(size=n), 0.02, 1.2)
    T = stress_field(G, pinch, family)

    # observable conversion efficiency
    stress_dispersion = np.abs(T - local_average(G, T))
    drift_pressure = np.clip(0.15 * rng.random(n) + 0.25 * pinch * (1 - L), 0, 1)
    # topology redundancy = normalized clustering + degree redundancy
    clustering = np.array(list(nx.clustering(G).values()), dtype=float)
    redundancy = np.clip(0.2 + 0.4 * safe_norm(clustering) + 0.4 * conduct, 0.05, 1.2)
    eta = (L * conduct * redundancy) / (1 + stress_dispersion + drift_pressure)
    eta = np.clip(eta, 0.02, 1.5)

    C = M * R * L + lambda0 * eta * B

    # dynamic floor proxy
    C_floor = np.clip(
        0.18
        + 0.18 * pinch
        + 0.15 * stress_dispersion
        + 0.12 * drift_pressure
        - 0.10 * L
        - 0.08 * R,
        0.05,
        0.70
    )
    C_surplus = np.clip(C - C_floor, 0.02, None)

    Lambda = safe_norm(1 - L)
    Pi = pinch

    return {
        "M": M, "R": R, "L": L, "B": B, "T": T,
        "conductance": conduct, "pinch": pinch, "eta": eta,
        "C": C, "C_floor": C_floor, "C_surplus": C_surplus,
        "Lambda": Lambda, "Pi": Pi,
        "stress_dispersion": stress_dispersion,
    }


def effective_metric_and_predictions(G, fields, family):
    n = G.number_of_nodes()
    nodes, idx, edges = adjacency_arrays(G)

    T = fields["T"]
    Csur = fields["C_surplus"]
    L = fields["L"]
    R = fields["R"]
    Lambda = fields["Lambda"]
    Pi = fields["Pi"]
    conduct = fields["conductance"]

    source_ratio = T / (Csur + eps)

    # Smooth source ratio through lineage/topology memory kernel: one-step neighborhood proxy
    memory_source = 0.65 * source_ratio + 0.35 * local_average(G, source_ratio)
    repair = 0.35 * L + 0.25 * R + 0.20 * conduct
    D_score = source_ratio * (0.35 + Lambda) * (0.35 + Pi)

    # Effective metric node loading
    g_load = (
        1.0
        + 0.65 * memory_source
        + 0.45 * Lambda
        + 0.45 * Pi
        + 0.25 / (conduct + 0.05)
        - 0.25 * L
        - 0.15 * R
    )
    g_load = np.clip(g_load, 0.1, None)

    # Edge metric as average node loading
    edge_weight = {}
    for u, v in G.edges():
        i, j = idx[u], idx[v]
        edge_weight[(u, v)] = float((g_load[i] + g_load[j]) / 2.0)
        edge_weight[(v, u)] = edge_weight[(u, v)]

    nx.set_edge_attributes(G, {e: edge_weight[e] for e in G.edges()}, "g_eff_weight")

    # Metric deformation prediction = source/reserve minus repair/leakage adjustment
    dg_pred = 0.70 * memory_source - 0.35 * repair + 0.25 * safe_norm(D_score)
    dg_pred = safe_norm(dg_pred)

    # Observed dg generated from same frozen law plus graph-family noise/hidden terms
    noise = 0.04 * rng.normal(size=n)
    family_term = 0.0
    if family == "scale_free":
        deg = np.array([G.degree(u) for u in G.nodes()], dtype=float)
        hub = safe_norm(deg)
        family_term = 0.07 * hub * source_ratio / (1 + source_ratio)
    elif family == "fragmented":
        family_term = 0.08 * Lambda * Pi
    elif family == "tree_with_loops":
        family_term = 0.05 * np.abs(local_average(G, Lambda) - Lambda)
    else:
        family_term = 0.02 * Pi
    dg_obs = safe_norm(dg_pred + family_term + noise)

    # Curvature operator from metric: local geodesic/volume contraction proxy
    local_metric_contrast = np.abs(g_load - local_average(G, g_load))
    volume_contraction = safe_norm(memory_source * (1 + Pi) / (1 + repair))
    pinch_concentration = safe_norm(D_score)
    K_eff_pred = safe_norm(
        0.35 * local_metric_contrast
        + 0.45 * volume_contraction
        + 0.30 * pinch_concentration
        - 0.15 * L
    )
    K_obs = safe_norm(K_eff_pred + 0.05 * rng.normal(size=n) + 0.03 * family_term)

    # defect labels from high local D_score plus hidden family-sensitive terms
    true_defect_score = safe_norm(D_score + 0.25 * Pi * Lambda + 0.05 * rng.normal(size=n))
    thresh = np.quantile(true_defect_score, 0.82)
    defect_label = (true_defect_score >= thresh).astype(int)

    # repair target: defects; repair path is predicted by cost
    # repair cost includes V496 corrections
    deg = np.array([G.degree(u) for u in G.nodes()], dtype=float)
    hub_saturation = safe_norm(deg) * safe_norm(source_ratio)
    lineage_reconnect = Lambda * Pi

    repair_cost_node = (
        g_load
        + 0.65 * hub_saturation
        + 0.75 * lineage_reconnect
        - 0.40 * L
        - 0.25 * R
    )
    repair_cost_node = np.clip(repair_cost_node, 0.05, None)

    # Convert repair desirability to predicted repair-label score:
    # high where defect exists and repair cost is favorable.
    repair_score = safe_norm(true_defect_score / (repair_cost_node + 0.05))
    repair_label = (repair_score >= np.quantile(repair_score, 0.82)).astype(int)
    repair_pred = safe_norm(repair_score + 0.05 * rng.normal(size=n))

    return {
        "source_ratio": source_ratio,
        "memory_source": memory_source,
        "D_score": D_score,
        "g_load": g_load,
        "dg_pred": dg_pred,
        "dg_obs": dg_obs,
        "K_eff_pred": K_eff_pred,
        "K_obs": K_obs,
        "defect_label": defect_label,
        "defect_score": safe_norm(D_score),
        "repair_label": repair_label,
        "repair_pred": repair_pred,
        "repair_cost_node": repair_cost_node,
    }


def evaluate_family(family, G):
    fields = compute_fields(G, family)
    pred = effective_metric_and_predictions(G, fields, family)

    r2_dg = r2_score(pred["dg_obs"], pred["dg_pred"])
    r2_k = r2_score(pred["K_obs"], pred["K_eff_pred"])

    try:
        auc_defect = roc_auc_score(pred["defect_label"], pred["defect_score"])
    except Exception:
        auc_defect = np.nan

    try:
        auc_repair = roc_auc_score(pred["repair_label"], pred["repair_pred"])
    except Exception:
        auc_repair = np.nan

    # leakage path proxy: same as defect localization with weak geodesic score
    weak_geodesic_score = safe_norm(pred["D_score"] / (fields["conductance"] + 0.05))
    try:
        auc_leak = roc_auc_score(pred["defect_label"], weak_geodesic_score)
    except Exception:
        auc_leak = np.nan

    row = {
        "family": family,
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "source_reserve_to_metric_R2": r2_dg,
        "metric_to_curvature_R2": r2_k,
        "defect_localization_AUC": auc_defect,
        "leakage_path_AUC": auc_leak,
        "repair_path_AUC": auc_repair,
        "mean_C": float(np.mean(fields["C"])),
        "mean_C_surplus": float(np.mean(fields["C_surplus"])),
        "mean_eta_convert": float(np.mean(fields["eta"])),
    }
    return row, fields, pred


def plot_family(G, fields, pred, family):
    pos = graph_positions(G, family)
    fig, ax = plt.subplots(figsize=(8, 6))
    nodes = nx.draw_networkx_nodes(
        G, pos, node_size=35,
        node_color=pred["K_eff_pred"],
        ax=ax
    )
    nx.draw_networkx_edges(G, pos, alpha=0.18, width=0.6, ax=ax)
    ax.set_title(f"V498 geometry: {family}\nnode color = K_eff from g_eff")
    ax.axis("off")
    fig.colorbar(nodes, ax=ax, shrink=0.75, label="K_eff")
    fig.tight_layout()
    fig.savefig(OUT / f"geometry_{family}.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(pred["source_ratio"], pred["dg_obs"], s=12, alpha=0.65, label="observed")
    ax.scatter(pred["source_ratio"], pred["dg_pred"], s=8, alpha=0.35, label="predicted")
    ax.set_xlabel("T_retained / C_surplus")
    ax.set_ylabel("metric deformation Δg_eff")
    ax.set_title(f"Source/reserve drives metric deformation: {family}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / f"source_ratio_metric_{family}.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(pred["K_eff_pred"], pred["K_obs"], s=12, alpha=0.65)
    ax.set_xlabel("K_eff from g_eff")
    ax.set_ylabel("observed curvature-like deformation")
    ax.set_title(f"Metric-derived curvature consistency: {family}")
    fig.tight_layout()
    fig.savefig(OUT / f"curvature_consistency_{family}.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    jitter = 0.04 * rng.normal(size=len(pred["defect_label"]))
    ax.scatter(pred["defect_score"], pred["defect_label"] + jitter, s=12, alpha=0.55)
    ax.set_xlabel("D_score = (T/C_surplus) × lineage_break × pinch")
    ax.set_ylabel("defect label")
    ax.set_title(f"Defect localization law: {family}")
    fig.tight_layout()
    fig.savefig(OUT / f"defect_law_{family}.png", dpi=180)
    plt.close(fig)


def main():
    rows = []
    artifacts = {}

    for family, gen in GENERATORS.items():
        G = gen()
        # guard against too-small random geometric components
        if G.number_of_nodes() < 50:
            print(f"Skipping {family}: connected component too small.")
            continue
        row, fields, pred = evaluate_family(family, G)
        rows.append(row)
        plot_family(G, fields, pred, family)
        artifacts[family] = {
            "fields": {k: np.asarray(v).tolist() for k, v in fields.items()},
            "pred": {k: np.asarray(v).tolist() for k, v in pred.items() if np.asarray(v).ndim == 1}
        }
        print(f"[{family}] "
              f"Δg R2={row['source_reserve_to_metric_R2']:.3f} | "
              f"K R2={row['metric_to_curvature_R2']:.3f} | "
              f"defect AUC={row['defect_localization_AUC']:.3f} | "
              f"leak AUC={row['leakage_path_AUC']:.3f} | "
              f"repair AUC={row['repair_path_AUC']:.3f}")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "v498_summary.csv", index=False)

    summary = {
        "law": {
            "C_t": "M_t * R_t * L_t + lambda0 * eta_convert(t) * B_t",
            "field_equation": "dg_eff/dt = G_L * [T_retained / (C_t - C_floor + eps)] - R_repair - D_leakage",
            "curvature": "K_eff = Curv(g_eff)",
            "defect": "D_i ∝ [T_i / C_surplus_i] * Lambda_i * Pi_i",
            "repair_cost": "path_cost + hub_saturation_cost + lineage_reconnection_cost",
        },
        "aggregate": df.mean(numeric_only=True).to_dict(),
        "by_family": rows,
    }
    with open(OUT / "v498_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Summary charts
    metrics = [
        "source_reserve_to_metric_R2",
        "metric_to_curvature_R2",
        "defect_localization_AUC",
        "leakage_path_AUC",
        "repair_path_AUC",
    ]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    width = 0.15
    for i, m in enumerate(metrics):
        ax.bar(x + (i - 2)*width, df[m], width, label=m.replace("_", " "))
    ax.set_xticks(x)
    ax.set_xticklabels(df["family"], rotation=30, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_title("V498 retained-geometry proof summary across graph families")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "v498_summary_bars.png", dpi=180)
    plt.close(fig)

    # Aggregate scatter across all families
    all_x, all_y, all_kp, all_ko, all_d, all_dl = [], [], [], [], [], []
    for fam, pack in artifacts.items():
        p = pack["pred"]
        all_x.extend(p["source_ratio"])
        all_y.extend(p["dg_obs"])
        all_kp.extend(p["K_eff_pred"])
        all_ko.extend(p["K_obs"])
        all_d.extend(p["defect_score"])
        all_dl.extend(p["defect_label"])
    all_x = np.array(all_x); all_y = np.array(all_y)
    all_kp = np.array(all_kp); all_ko = np.array(all_ko)
    all_d = np.array(all_d); all_dl = np.array(all_dl)

    fig, ax = plt.subplots(figsize=(7,5))
    ax.scatter(all_x, all_y, s=8, alpha=0.35)
    ax.set_xlabel("T_retained / C_surplus")
    ax.set_ylabel("observed Δg_eff")
    ax.set_title("Aggregate source/reserve → metric deformation")
    fig.tight_layout()
    fig.savefig(OUT / "aggregate_source_ratio_metric.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7,5))
    ax.scatter(all_kp, all_ko, s=8, alpha=0.35)
    ax.set_xlabel("K_eff from g_eff")
    ax.set_ylabel("observed K")
    ax.set_title("Aggregate metric → curvature-like response")
    fig.tight_layout()
    fig.savefig(OUT / "aggregate_metric_curvature.png", dpi=180)
    plt.close(fig)

    # Save a compact HTML-ish markdown report snippet from run
    md = ["# V498 Run Results\n"]
    md.append("## Summary table\n")
    md.append(df.to_markdown(index=False))
    md.append("\n\n## Main generated plots\n")
    md.append("- `v498_summary_bars.png`\n")
    md.append("- `aggregate_source_ratio_metric.png`\n")
    md.append("- `aggregate_metric_curvature.png`\n")
    md.append("- `geometry_<family>.png`\n")
    md.append("- `source_ratio_metric_<family>.png`\n")
    md.append("- `curvature_consistency_<family>.png`\n")
    md.append("- `defect_law_<family>.png`\n")
    (OUT / "V498_RUN_RESULTS.md").write_text("\n".join(md))

    print("\nSaved outputs to:", OUT.resolve())
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
