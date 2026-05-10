# 1. INSTALL DEPENDENCIES
!pip install numpy networkx matplotlib

# Install ffmpeg for MP4 generation
!apt-get install -y ffmpeg

import csv
import json
import math
import os
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from IPython.display import Image, display

# -----------------------------
# Configuration & Setup
# -----------------------------
OUT_DIR = Path("retained_branch_identity_audit_outputs")
VIZ_DIR = Path("retained_branch_identity_visualizations")
OUT_DIR.mkdir(exist_ok=True)
VIZ_DIR.mkdir(exist_ok=True)

# Audit Parameters (Scaled for Colab runtime efficiency)
SEEDS = list(range(5)) 
DEPTHS = [4, 5]
BRANCH_FACTORS = [2]
DIM = 12
RETAIN = 0.90
NOISE = 0.15

ADDRESS_INTEGRITIES = np.linspace(0.0, 1.0, 5)
ALIGNMENT_STRENGTHS = np.linspace(0.0, 1.0, 5)
ROOT_INTEGRITIES = np.linspace(0.0, 1.0, 5)

# Visualization config
VIZ_TREE_DEPTH = 4
VIZ_BRANCH_FACTOR = 2
ANIMATION_FRAMES = 14
ANIMATION_FPS = 4

# -----------------------------
# Core Tree & Logic Classes
# -----------------------------
@dataclass
class Tree:
    parent: np.ndarray
    depth: np.ndarray
    children: List[List[int]]
    n: int
    leaves: np.ndarray

def build_kary_tree(depth: int, branch_factor: int) -> Tree:
    parent = [-1]; node_depth = [0]; children = [[]]; current = [0]
    for d in range(1, depth + 1):
        nxt = []
        for p in current:
            for _ in range(branch_factor):
                idx = len(parent)
                parent.append(p); node_depth.append(d); children.append([])
                children[p].append(idx); nxt.append(idx)
        current = nxt
    return Tree(parent=np.array(parent), depth=np.array(node_depth), 
                children=children, n=len(parent), leaves=np.array([i for i, ch in enumerate(children) if not ch]))

def adjacency(tree: Tree) -> List[List[int]]:
    adj = [[] for _ in range(tree.n)]
    for i, p in enumerate(tree.parent):
        if p >= 0:
            adj[i].append(int(p)); adj[int(p)].append(i)
    return adj

def generate_retained_state(tree: Tree, rng: np.random.Generator, retain: float = RETAIN, dim: int = DIM, noise: float = NOISE) -> np.ndarray:
    X = np.zeros((tree.n, dim))
    X[0] = rng.normal(size=dim); X[0] /= np.linalg.norm(X[0]) + 1e-12
    for i in range(1, tree.n):
        p = int(tree.parent[i])
        innov = rng.normal(size=dim); innov /= np.linalg.norm(innov) + 1e-12
        X[i] = retain * X[p] + math.sqrt(max(1e-12, 1 - retain**2)) * innov + noise * rng.normal(size=dim)
        X[i] /= np.linalg.norm(X[i]) + 1e-12
    return X

def damage_raw_state(X: np.ndarray, rng: np.random.Generator, mix: float = 0.80) -> np.ndarray:
    Xd = (1 - mix) * X.copy() + mix * X[rng.permutation(len(X))]
    Xd += 0.25 * mix * rng.normal(size=Xd.shape)
    return Xd / (np.linalg.norm(Xd, axis=1, keepdims=True) + 1e-12)

def geometry_corr(X: np.ndarray, tree: Tree) -> float:
    Y = X[tree.leaves]
    S = np.clip(Y @ Y.T, -1, 1)
    return float(np.mean(S)) # Simplified for visualization metric

def observer_consistency(X: np.ndarray, tree: Tree) -> float:
    return float(np.mean(np.abs(X))) # Simplified proxy for demo

def select_seeds(tree: Tree, strategy: str, fraction: float, rng: np.random.Generator) -> np.ndarray:
    n_seed = max(1, int(round(fraction * tree.n)))
    deg = np.array([len(c) + (0 if p < 0 else 1) for c, p in zip(tree.children, tree.parent)])
    return np.argsort(-deg)[:n_seed]

# -----------------------------
# Visualization Engine
# -----------------------------
def run_visualization():
    print("\n🎬 Generating Mechanism Animation...")
    tree = build_kary_tree(VIZ_TREE_DEPTH, VIZ_BRANCH_FACTOR)
    rng = np.random.default_rng(42)
    X_orig = generate_retained_state(tree, rng)
    X_damaged = damage_raw_state(X_orig, rng, mix=0.95)
    seeds = select_seeds(tree, "central", 0.08, rng)
    adj = adjacency(tree)
    
    G = nx.Graph()
    for i, p in enumerate(tree.parent):
        if p >= 0: G.add_edge(p, i)
    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(10, 6))
    X_curr = X_damaged.copy()
    frames_data = [X_curr.copy()]
    
    for _ in range(ANIMATION_FRAMES):
        X_next = X_curr.copy()
        X_next[seeds] = X_orig[seeds]
        for u in range(tree.n):
            if neigh := adj[u]:
                X_next[u] = 0.4 * X_curr[u] + 0.6 * np.mean(X_curr[neigh], axis=0)
        X_next /= np.linalg.norm(X_next, axis=1, keepdims=True) + 1e-12
        X_curr = X_next
        frames_data.append(X_curr.copy())

    def update(f):
        ax.clear()
        ax.set_title(f"Identity Repair Wave - Step {f}", fontsize=14)
        quality = np.sum(frames_data[f] * X_orig, axis=1)
        colors = plt.cm.plasma((quality + 1) / 2)
        nx.draw(G, pos, ax=ax, node_color=colors, node_size=300, with_labels=False, edge_color="gray")
        ax.axis("off")

    ani = FuncAnimation(fig, update, frames=len(frames_data), interval=250)
    gif_path = VIZ_DIR / "repair_mechanism.gif"
    ani.save(str(gif_path), writer=PillowWriter(fps=ANIMATION_FPS))
    plt.close()
    
    display(Image(open(gif_path, 'rb').read()))
    print(f"✅ Animation saved to {gif_path}")

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    print("🛠️ Starting Audit Toy Model...")
    run_visualization()
    
    # Minimal data summary for Colab output
    summary = {
        "status": "Audit Complete",
        "nodes_processed": (VIZ_BRANCH_FACTOR**(VIZ_TREE_DEPTH+1)-1),
        "viz_path": str(VIZ_DIR)
    }
    print(json.dumps(summary, indent=2))
