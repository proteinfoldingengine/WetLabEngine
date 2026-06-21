#!/usr/bin/env python3
"""
LAB: When Conservation Isn't Enough — Underdetermination on a Network
=====================================================================
A first-year computational physics experiment.

BIG IDEA: A conservation law tells you what is preserved. It does NOT always
tell you a unique answer. On a network with loops, "what flows in equals what
flows out at every node" leaves a whole family of valid flows. Choosing one
requires extra information. This lab lets you see that happen, by hand and in code.

You will:
  Part 1  Build a small network, find its loops (cycle space), see the ambiguity.
  Part 2  Try to remove the ambiguity with a "cost" rule (a metric) — and discover
          the answer depends on which cost you pick.
  Part 3  Resolve it with a measurement (a response operator) — and find the exact
          condition under which the ambiguity collapses.

Run:  python phi_lab.py
Needs: numpy, matplotlib    (pip install numpy matplotlib)
Outputs: five labeled figures in lab_figures/ + a printed lab log.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("lab_figures"); OUT.mkdir(exist_ok=True)
TOL = 1e-10
np.set_printoptions(precision=3, suppress=True)

# ----------------------------------------------------------------------
# THE NETWORK  (you can edit this — see Exercise 1c)
# 5 nodes, 7 directed edges. A source pushes 1 unit in at node 0, out at node 3.
# ----------------------------------------------------------------------
NODES = [0, 1, 2, 3, 4]
EDGES = [(0,1),(1,3),(0,2),(2,4),(4,3),(1,2),(0,4)]
SOURCE = np.zeros(len(NODES)); SOURCE[0] = -1.0; SOURCE[3] = +1.0

# Fixed 2D coordinates so every figure shows the SAME network in the SAME place.
COORD = {0:(0.0,1.0), 1:(1.0,1.7), 2:(1.0,0.3), 3:(2.0,1.0), 4:(1.0,-0.8)}

def incidence(nodes, edges):
    """B[node, edge] = -1 at tail, +1 at head. Row = node, column = edge."""
    idx = {n:i for i,n in enumerate(nodes)}
    B = np.zeros((len(nodes), len(edges)))
    for k,(u,v) in enumerate(edges):
        B[idx[u],k] = -1.0; B[idx[v],k] = +1.0
    return B

def cycle_space(B, tol=TOL):
    """Orthonormal basis Z for ker(B): the loops. Columns of Z are independent cycles."""
    U,S,Vt = np.linalg.svd(B, full_matrices=True)
    rank = int((S > tol).sum())
    return Vt[rank:].T, rank

def min_norm_current(B, s):
    """The 'smallest' current satisfying B J = s (minimum Euclidean norm)."""
    return B.T @ np.linalg.pinv(B @ B.T, rcond=TOL) @ s

def min_cost_current(B, s, w):
    """The current of least cost  sum_e w_e J_e^2  subject to B J = s, w>0 per edge."""
    Winv = np.diag(1.0/w)
    return Winv @ B.T @ np.linalg.pinv(B @ Winv @ B.T, rcond=TOL) @ s

# ----------------------------------------------------------------------
# Drawing helper: show a current as colored/width-coded arrows on the network.
# ----------------------------------------------------------------------
def draw_current(ax, J, title, color="#2a6fb0"):
    for n,(x,y) in COORD.items():
        ax.scatter([x],[y], s=520, c="#eef2f7", edgecolors="#33445c", zorder=3, linewidths=1.5)
        ax.text(x, y, str(n), ha="center", va="center", fontsize=12, zorder=4, color="#22303f")
    jmax = max(np.abs(J).max(), 1e-9)
    for k,(u,v) in enumerate(EDGES):
        x0,y0 = COORD[u]; x1,y1 = COORD[v]
        val = J[k]
        # arrow points along the +current direction; reverse if negative
        if val >= 0: sx,sy,ex,ey = x0,y0,x1,y1
        else:        sx,sy,ex,ey = x1,y1,x0,y0
        lw = 0.8 + 5.0*abs(val)/jmax
        ax.annotate("", xy=(ex,ey), xytext=(sx,sy),
                    arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                    shrinkA=16, shrinkB=16, alpha=0.85), zorder=2)
        mx,my = (x0+x1)/2, (y0+y1)/2
        ax.text(mx, my+0.07, f"{val:+.2f}", ha="center", fontsize=8, color="#555", zorder=5)
    ax.set_title(title, fontsize=11)
    ax.set_xlim(-0.5,2.5); ax.set_ylim(-1.4,2.2); ax.axis("off")

# ======================================================================
print("="*68)
print(" LAB: When Conservation Isn't Enough")
print("="*68)

B = incidence(NODES, EDGES)
Z, rank_B = cycle_space(B)
beta1 = Z.shape[1]

print(f"\nPART 1 — The network and its loops")
print(f"  nodes N = {len(NODES)},  edges E = {len(EDGES)}")
print(f"  rank(B) = {rank_B}")
print(f"  number of independent loops (cycle dimension) = E - N + 1 = "
      f"{len(EDGES)} - {len(NODES)} + 1 = {len(EDGES)-len(NODES)+1}")
print(f"  cycle space dimension from the code (dim ker B) = {beta1}")
print(f"  --> PREDICT THIS BY HAND FIRST (Exercise 1a), then check it matches.")

# Part 1: three different currents, all conserving.
J0 = min_norm_current(B, SOURCE)
a_choices = [np.zeros(beta1), np.linspace(-0.8,0.8,beta1), np.linspace(0.7,-0.5,beta1)]
currents = [J0 + Z@a for a in a_choices]
print(f"\n  Three DIFFERENT currents, each satisfying B J = s exactly:")
for i,J in enumerate(currents):
    print(f"   choice {i}: conservation error |BJ - s| = {np.linalg.norm(B@J-SOURCE):.2e}"
          f"   (machine zero = perfectly conserved),  |J| = {np.linalg.norm(J):.3f}")
print(f"  All three obey the SAME conservation law. Conservation did NOT pick one.")

fig, axes = plt.subplots(1, 3, figsize=(15,4.6))
fig.suptitle("PART 1 — Three currents that ALL satisfy conservation (B J = s). "
             "The law does not select one.", fontsize=13)
for ax,J,lab in zip(axes, currents, ["cycle coeffs = 0","cycle coeffs spread +","cycle coeffs spread −"]):
    draw_current(ax, J, f"{lab}\n|BJ−s|={np.linalg.norm(B@J-SOURCE):.0e}", color="#2a6fb0")
fig.tight_layout(); fig.savefig(OUT/"part1_ambiguity.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# ======================================================================
# Part 2: a cost rule (metric) selects ONE current — but different costs disagree.
print(f"\nPART 2 — Try to fix it with a 'cost' rule (a metric W)")
edge_len = np.array([max(1,abs(v-u)) for u,v in EDGES], float)
access   = np.array([1.0,0.9,1.05,0.85,0.8,0.7,0.55])
metrics = {
    "equal cost":        np.ones(len(EDGES)),
    "cost = length":     edge_len.copy(),
    "cost = 1/access":   1.0/np.maximum(access,1e-9),
    "cost = length/acc": edge_len/np.maximum(access,1e-9),
}
mcur = {name: min_cost_current(B, SOURCE, w) for name,w in metrics.items()}
names = list(mcur)
print(f"  Each cost rule gives a valid conserved current — but they DISAGREE:")
for n in names:
    print(f"   {n:18s}: |J| = {np.linalg.norm(mcur[n]):.3f},  conserves to "
          f"{np.linalg.norm(B@mcur[n]-SOURCE):.0e}")
maxrel = max(np.linalg.norm(mcur[a]-mcur[b])/(np.linalg.norm(mcur[a])+1e-12)
             for a in names for b in names)
print(f"  Largest disagreement between cost rules: {maxrel*100:.0f}% of the current.")
print(f"  --> Lesson: 'minimize a cost' works, but the NETWORK doesn't tell you")
print(f"      which cost is the right one. The choice is external.")

fig, axes = plt.subplots(1, 4, figsize=(19,4.6))
fig.suptitle("PART 2 — Each cost rule selects a DIFFERENT conserved current. "
             "The network does not say which cost is 'correct'.", fontsize=13)
cols = ["#1b7a44","#b5651d","#8a3ab0","#0d6e8c"]
for ax,n,c in zip(axes, names, cols):
    draw_current(ax, mcur[n], f"{n}\n|J|={np.linalg.norm(mcur[n]):.2f}", color=c)
fig.tight_layout(); fig.savefig(OUT/"part2_metric_disagreement.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# comparison bar: edge-by-edge currents across the four metrics
fig, ax = plt.subplots(figsize=(11,4.6))
x = np.arange(len(EDGES)); wbar = 0.2
for i,(n,c) in enumerate(zip(names,cols)):
    ax.bar(x+(i-1.5)*wbar, mcur[n], wbar, label=n, color=c, alpha=0.85)
ax.axhline(0, color="#333", lw=0.8)
ax.set_xticks(x); ax.set_xticklabels([f"e{k}\n{u}->{v}" for k,(u,v) in enumerate(EDGES)], fontsize=8)
ax.set_ylabel("selected current  J_e"); ax.set_title("PART 2 — Same network, four cost rules, four different answers per edge")
ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig(OUT/"part2_edge_comparison.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# ======================================================================
# Part 3: a measurement (response operator R) resolves the loops.
print(f"\nPART 3 — Resolve it with a measurement (response operator R)")
print(f"  Suppose nature has a hidden 'true' current. We probe it with R and try to recover it.")
a_true = np.linspace(0.5,-0.4,beta1); J_true = J0 + Z@a_true

def recover(R):
    RZ = R @ Z
    a_hat = np.linalg.pinv(RZ, rcond=TOL) @ (R@J_true - R@J0)
    J_hat = J0 + Z@a_hat
    return J_hat, int(np.linalg.matrix_rank(RZ, tol=TOL))

R_full = Z.T                # a probe that sees every loop
R_weak = Z[:, :1].T         # a probe that sees only ONE loop
J_full, rank_full = recover(R_full)
J_weak, rank_weak = recover(R_weak)
print(f"  STRONG probe: rank(R Z) = {rank_full}, number of loops = {beta1}  ->  "
      f"{'EQUAL: ambiguity collapses' if rank_full==beta1 else 'not enough'}")
print(f"     recovered current error vs truth = {np.linalg.norm(J_full-J_true):.2e}  (≈0: solved)")
print(f"  WEAK probe:   rank(R Z) = {rank_weak}, number of loops = {beta1}  ->  "
      f"{'EQUAL' if rank_weak==beta1 else 'TOO FEW: ambiguity remains'}")
print(f"     recovered current error vs truth = {np.linalg.norm(J_weak-J_true):.2e}  (large: unsolved)")
print(f"\n  THE CONDITION:  the measurement resolves the flow exactly when")
print(f"                  rank(R Z) = (number of loops).")

fig, axes = plt.subplots(1, 3, figsize=(15,4.6))
fig.suptitle("PART 3 — A measurement resolves the flow only if it 'sees' every loop:  "
             "rank(RZ) = number of loops", fontsize=13)
draw_current(axes[0], J_true, "hidden true current", color="#333333")
draw_current(axes[1], J_full, f"STRONG probe recovers it\nrank(RZ)={rank_full} = loops={beta1}  ✓\nerror={np.linalg.norm(J_full-J_true):.0e}", color="#1b7a44")
draw_current(axes[2], J_weak, f"WEAK probe fails\nrank(RZ)={rank_weak} < loops={beta1}  ✗\nerror={np.linalg.norm(J_weak-J_true):.2f}", color="#b03030")
fig.tight_layout(); fig.savefig(OUT/"part3_measurement_closure.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# summary figure: the rank gate
fig, ax = plt.subplots(figsize=(7.5,5))
ax.bar(["strong probe\nrank(RZ)","weak probe\nrank(RZ)"], [rank_full, rank_weak],
       color=["#1b7a44","#b03030"], alpha=0.85, width=0.6)
ax.axhline(beta1, ls="--", color="#222", lw=1.5, label=f"loops to resolve = {beta1}")
ax.set_ylabel("rank(R Z)  =  loops the probe can distinguish")
ax.set_title("PART 3 — The closure gate:\nflow is uniquely recovered iff rank(RZ) reaches the loop count")
ax.legend()
fig.tight_layout(); fig.savefig(OUT/"part3_rank_gate.png", dpi=160, bbox_inches="tight"); plt.close(fig)

print("\n" + "="*68)
print(" Figures written to lab_figures/:")
for f in ["part1_ambiguity.png","part2_metric_disagreement.png","part2_edge_comparison.png",
          "part3_measurement_closure.png","part3_rank_gate.png"]:
    print("   -", f)
print("="*68)
