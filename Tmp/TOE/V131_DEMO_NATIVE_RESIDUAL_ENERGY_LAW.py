# V131_DEMO_NATIVE_RESIDUAL_ENERGY_LAW.py
# Toy demo:
# decoherence shock -> native lineage-mode residual
# captured residual energy -> geometry repair

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

EPS = 1e-12
DIM = 12
DEPTH = 5
BRANCH = 2
RETAIN = 0.88
SHOCK = 0.75
SEEDS = range(20)
CAPTURE_TARGETS = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,1.0]

@dataclass
class Tree:
    parent: np.ndarray
    depth: np.ndarray
    children: list
    leaves: np.ndarray
    n: int

def norm(X):
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + EPS)

def build_tree(depth=5, b=2):
    parent, dep, children = [-1], [0], [[]]
    front = [0]
    for d in range(1, depth+1):
        nxt = []
        for p in front:
            for _ in range(b):
                i = len(parent)
                parent.append(p)
                dep.append(d)
                children.append([])
                children[p].append(i)
                nxt.append(i)
        front = nxt
    parent = np.array(parent)
    dep = np.array(dep)
    leaves = np.array([i for i,c in enumerate(children) if not c])
    return Tree(parent, dep, children, leaves, len(parent))

def descendants(tree, root):
    out, stack = [], [int(root)]
    while stack:
        u = stack.pop()
        out.append(u)
        stack.extend(tree.children[u])
    return np.array(out)

def make_state(tree, rng):
    X = np.zeros((tree.n, DIM))
    X[0] = rng.normal(size=DIM)
    X[0] /= np.linalg.norm(X[0]) + EPS
    for i in range(1, tree.n):
        p = tree.parent[i]
        z = rng.normal(size=DIM)
        z /= np.linalg.norm(z) + EPS
        X[i] = RETAIN * X[p] + np.sqrt(1 - RETAIN**2) * z
        X[i] /= np.linalg.norm(X[i]) + EPS
    return X

def native_modes(tree):
    modes, meta = [], []
    for u, kids in enumerate(tree.children):
        if len(kids) < 2:
            continue
        for child in kids:
            m = np.zeros(tree.n)
            cd = descendants(tree, child)
            m[cd] = 1.0
            sib = []
            for k in kids:
                if k != child:
                    sib += descendants(tree, k).tolist()
            if sib:
                sib = np.array(sib)
                m[sib] = -len(cd) / max(1, len(sib))
            m -= m.mean()
            n = np.linalg.norm(m)
            if n > EPS:
                modes.append(m / n)
                meta.append(tree.depth[u])
    order = np.argsort(meta)
    return np.stack(modes, axis=1)[:, order]

def shock_state(X, tree, rng):
    mid = int(tree.depth.max() * 0.5)
    root = int(rng.choice(np.where(tree.depth == mid)[0]))
    region = descendants(tree, root)

    Y = X.copy()
    noise = norm(rng.normal(size=Y[region].shape))
    Y[region] = (1-SHOCK)*Y[region] + SHOCK*noise
    Y[region] = norm(Y[region])
    return Y

def geom_corr(Y, X0, tree):
    A, B = Y[tree.leaves], X0[tree.leaves]
    DY = 1 - np.clip(A @ A.T, -1, 1)
    DB = 1 - np.clip(B @ B.T, -1, 1)
    mask = ~np.eye(len(A), dtype=bool)
    y, b = DY[mask], DB[mask]
    if y.std() < EPS or b.std() < EPS:
        return 0.0
    return np.corrcoef(y, b)[0,1]

def repair_with_capture(Y, X0, M, capture_target):
    residual = Y - X0
    coeff = M.T @ residual
    mode_energy = np.sum(coeff**2, axis=1)

    order = np.argsort(-mode_energy)
    total = mode_energy.sum() + EPS
    cumulative = np.cumsum(mode_energy[order]) / total

    k = np.searchsorted(cumulative, capture_target) + 1
    chosen = order[:k]

    captured_energy = mode_energy[chosen].sum() / total

    coeff_repair = np.zeros_like(coeff)
    coeff_repair[chosen] = coeff[chosen]

    correction = M @ coeff_repair
    repaired = Y - correction
    repaired = norm(repaired)

    return repaired, captured_energy, k / M.shape[1]

rows = []
tree = build_tree(DEPTH, BRANCH)
M = native_modes(tree)

for seed in SEEDS:
    rng = np.random.default_rng(seed)
    X0 = make_state(tree, rng)
    Ys = shock_state(X0, tree, rng)

    before = geom_corr(Ys, X0, tree)

    for target in CAPTURE_TARGETS:
        Yr, captured, mode_frac = repair_with_capture(Ys, X0, M, target)
        after = geom_corr(Yr, X0, tree)
        repair_score = after - before

        rows.append({
            "seed": seed,
            "target_capture": target,
            "actual_captured_energy": captured,
            "mode_fraction": mode_frac,
            "geometry_before": before,
            "geometry_after": after,
            "repair_score": repair_score
        })

df = pd.DataFrame(rows)

print("\n=== V131 Native Residual Energy Law Demo ===")
print(df.groupby("target_capture")[["actual_captured_energy","mode_fraction","repair_score"]].mean())

corr_energy = df["actual_captured_energy"].corr(df["repair_score"])
corr_modes = df["mode_fraction"].corr(df["repair_score"])

print("\nCorrelation with repair score:")
print("captured residual energy:", round(corr_energy, 4))
print("raw mode fraction:", round(corr_modes, 4))

plt.figure(figsize=(8,5))
plt.scatter(df["actual_captured_energy"], df["repair_score"], alpha=0.45)
plt.xlabel("Captured native residual energy")
plt.ylabel("Geometry repair score")
plt.title("Geometry repair follows captured native residual energy")
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(8,5))
mean_curve = df.groupby("target_capture")["repair_score"].mean()
plt.plot(mean_curve.index, mean_curve.values, marker="o")
plt.xlabel("Target captured residual energy")
plt.ylabel("Mean geometry repair score")
plt.title("Repair saturates as residual energy capture approaches 90–100%")
plt.grid(True, alpha=0.3)
plt.show()
