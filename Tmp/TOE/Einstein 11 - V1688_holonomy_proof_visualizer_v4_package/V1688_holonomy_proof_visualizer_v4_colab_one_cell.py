
# V1688 Holonomy Proof Visualizer V4 — Colab one-cell runnable
# Produces static PNG + GIF + MP4.
#
# V4 goal:
#   Show the mechanism clearly, not just decorate it.
#   Large 3D retained L3/L4 topology on the left.
#   Active edge transport and readable equations on the right.
#   Edge-product ledger and defect accumulation at the bottom.
#
# Science boundary:
#   This is a finite retained-flow proof visualization.
#   It does not claim GR, Einstein equations, Riemann curvature, or physical spacetime.
#   The displayed curve is a visualization of the discrete provenance cycle.
#   The proof object is the ordered edge product Π_loop c_pq.
#
# Core equations:
#   T_pq(dx) = dx + gamma_pq [roll(dx) ⊙ q − dx ⊙ roll(q)]
#   c_pq = <Z_q, T_pq Z_p> / (||T_pq Z_p|| ||Z_q||)
#   H_cycle^dir = Π_loop c_pq
#   defect = |1 − H_cycle^dir| · mean(|C_corr|)
#
# No Kabsch/Gramian/Procrustes alignment.
# No reversible full-matrix holonomy requirement.
# No fitted counterterms.
# No primitive time coordinate.

import os, json, ast, math, warnings, shutil
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

warnings.filterwarnings("ignore")

OUT = Path("V1688_holonomy_proof_visualizer_v4_outputs")
OUT.mkdir(exist_ok=True)

SEED = 168864
N_NODES = 8
DIM = 4

BG = "#05070d"
PANEL = "#0a1020"
PANEL2 = "#0d1528"
GRID = "#223552"
TEXT = "#f4f7ff"
MUTED = "#aab5c5"
CYAN = "#4ee7ff"
BLUE = "#3b82f6"
GOLD = "#ffd65a"
ORANGE = "#ffb347"
VIOLET = "#b877ff"
MAGENTA = "#ff6bd6"
RED = "#ff6b6b"
GREEN = "#7ef29a"
WHITE = "#ffffff"

def parse_vec(x):
    if isinstance(x, np.ndarray):
        return x.astype(float)
    if isinstance(x, list):
        return np.array(x, dtype=float)
    if isinstance(x, str):
        return np.array(ast.literal_eval(x), dtype=float)
    raise TypeError(type(x))

def unit(v, eps=1e-12):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    return np.zeros_like(v) if n < eps else v/n

def roll(v):
    return np.roll(np.asarray(v, dtype=float), 1)

def native_transport(dx, q_state, gamma):
    dx = np.asarray(dx, dtype=float)
    q_state = np.asarray(q_state, dtype=float)
    return dx + gamma * (roll(dx) * q_state - dx * roll(q_state))

def directional_scalar(Zp, Zq, q_state, gamma):
    TpZ = native_transport(Zp, q_state, gamma)
    denom = np.linalg.norm(TpZ) * np.linalg.norm(Zq) + 1e-12
    return float(np.dot(Zq, TpZ) / denom), TpZ

def maybe_load_existing():
    candidates = [
        ("V1688_v2_nodes.csv", "V1688_v2_edges.csv"),
        ("/mnt/data/V1688_v2_nodes.csv", "/mnt/data/V1688_v2_edges.csv"),
        ("V1688_holonomy_proof_nodes.csv", "V1688_holonomy_proof_edges.csv"),
        ("/mnt/data/V1688_holonomy_proof_nodes(1).csv", "/mnt/data/V1688_holonomy_proof_edges(1).csv"),
    ]
    for nf, ef in candidates:
        if Path(nf).exists() and Path(ef).exists():
            nodes = pd.read_csv(nf)
            edges = pd.read_csv(ef)
            required_node = {"node_id","x","y","z","C_corr","state","Z","O3","H4_perp"}
            required_edge = {"from_node","to_node","gamma_pq"}
            if required_node.issubset(nodes.columns) and required_edge.issubset(edges.columns):
                return nodes, edges, "loaded_uploaded_or_prior_proof_object"
    return None, None, "generated_deterministic_proof_object"

def generate_deterministic_proof():
    rng = np.random.default_rng(SEED)
    theta = np.linspace(0, 2*np.pi, N_NODES, endpoint=False)
    radius = 2.9 + 0.28*np.sin(3*theta + 0.25)
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    z = 0.70*np.sin(2*theta + 0.55)

    states, O3, H4, Z, Ccorr = [], [], [], [], []
    for i in range(N_NODES):
        s = unit(rng.normal(size=DIM))
        o = unit(roll(s) - np.roll(s, -1))
        h_raw = rng.normal(size=DIM) + 0.22*np.roll(o, 1)
        for b in [s, o]:
            h_raw = h_raw - np.dot(h_raw, b)*b
        h = unit(h_raw)
        zz = unit(0.35*o + 1.0*h)
        cc = float(0.55 + 0.20*np.sin(theta[i] + 0.7) + 0.05*rng.normal())
        states.append(s); O3.append(o); H4.append(h); Z.append(zz); Ccorr.append(cc)

    nodes = pd.DataFrame({
        "node_id": [f"p{i}" for i in range(N_NODES)],
        "x": x, "y": y, "z": z,
        "C_corr": Ccorr,
        "state": [v.tolist() for v in states],
        "Z": [v.tolist() for v in Z],
        "O3": [v.tolist() for v in O3],
        "H4_perp": [v.tolist() for v in H4],
    })
    edges = []
    for i in range(N_NODES):
        j = (i + 1) % N_NODES
        gamma = float(0.24*np.tanh(np.dot(states[i], states[j])) + 0.10*np.sin(theta[i]-theta[j]))
        edges.append({"from_node": f"p{i}", "to_node": f"p{j}", "gamma_pq": gamma})
    return nodes, pd.DataFrame(edges)

nodes, edges, source_mode = maybe_load_existing()
if nodes is None:
    nodes, edges = generate_deterministic_proof()

pos = {r["node_id"]: np.array([float(r["x"]), float(r["y"]), float(r["z"])]) for _, r in nodes.iterrows()}
states = {r["node_id"]: parse_vec(r["state"]) for _, r in nodes.iterrows()}
Zs = {r["node_id"]: parse_vec(r["Z"]) for _, r in nodes.iterrows()}
O3s = {r["node_id"]: parse_vec(r["O3"]) for _, r in nodes.iterrows()}
H4s = {r["node_id"]: parse_vec(r["H4_perp"]) for _, r in nodes.iterrows()}
Ccorr = {r["node_id"]: float(r["C_corr"]) for _, r in nodes.iterrows()}

edge_rows, step_rows = [], []
partial = 1.0
mean_abs_C = float(np.mean(np.abs(list(Ccorr.values()))))
for k, er in edges.iterrows():
    p, q = er["from_node"], er["to_node"]
    gamma = float(er["gamma_pq"])
    c, TpZ = directional_scalar(Zs[p], Zs[q], states[q], gamma)
    partial *= c
    defect = abs(1 - partial) * mean_abs_C
    edge_rows.append({
        "from_node": p, "to_node": q, "gamma_pq": gamma, "c_pq": c,
        "transport_norm": float(np.linalg.norm(TpZ)),
        "Z_alignment_raw": float(np.dot(Zs[q], TpZ)),
    })
    step_rows.append({
        "step": k+1, "from_node": p, "to_node": q,
        "gamma_pq": gamma, "c_pq": c,
        "H_cycle_partial": partial,
        "directional_defect_partial": defect,
        "transport_norm": float(np.linalg.norm(TpZ)),
        "Z_alignment_raw": float(np.dot(Zs[q], TpZ)),
    })
edges = pd.DataFrame(edge_rows)
steps = pd.DataFrame(step_rows)

H_final = float(steps["H_cycle_partial"].iloc[-1])
defect_final = float(abs(1 - H_final) * mean_abs_C)

reverse_product = 1.0
for _, er in edges.iloc[::-1].iterrows():
    p, q = er["to_node"], er["from_node"]
    gamma = float(er["gamma_pq"])
    c_rev, _ = directional_scalar(Zs[p], Zs[q], states[q], gamma)
    reverse_product *= c_rev
reverse_defect = float(abs(1 - reverse_product) * mean_abs_C)
orientation_asym = float(abs(defect_final - reverse_defect))

continuity = {nid: 0.0 for nid in nodes["node_id"]}
flux_rows = []
for _, er in edges.iterrows():
    p, q = er["from_node"], er["to_node"]
    gamma = float(er["gamma_pq"])
    c_fwd, _ = directional_scalar(Zs[p], Zs[q], states[q], gamma)
    c_rev, _ = directional_scalar(Zs[q], Zs[p], states[p], gamma)
    F_pq = c_fwd * Ccorr[p]
    F_qp = c_rev * Ccorr[q]
    J = 0.5*(F_pq - F_qp)
    continuity[p] -= J
    continuity[q] += J
    flux_rows.append({"from_node": p, "to_node": q, "c_pq": c_fwd, "c_qp": c_rev, "F_pq": F_pq, "F_qp": F_qp, "J_pq": J})
flux_df = pd.DataFrame(flux_rows)
continuity_df = pd.DataFrame([{"node_id": k, "continuity_residual": v} for k, v in continuity.items()])

metrics = {
    "source_mode": source_mode,
    "H_cycle_dir": H_final,
    "native_directional_cycle_defect": defect_final,
    "mean_abs_C_corr": mean_abs_C,
    "reverse_H_cycle_dir": reverse_product,
    "reverse_directional_cycle_defect": reverse_defect,
    "orientation_asymmetry_abs": orientation_asym,
    "edge_count": int(len(edges)),
    "node_count": int(len(nodes)),
    "max_abs_continuity_residual": float(np.max(np.abs(list(continuity.values())))),
    "interpretation": "Directed native holonomy is generated edge-by-edge by native recombination transport acting on retained correction mode Z over an explicit provenance cycle."
}

nodes.to_csv(OUT / "V1688_v4_nodes.csv", index=False)
edges.to_csv(OUT / "V1688_v4_edges.csv", index=False)
steps.to_csv(OUT / "V1688_v4_cycle_steps.csv", index=False)
flux_df.to_csv(OUT / "V1688_v4_antisymmetric_flux.csv", index=False)
continuity_df.to_csv(OUT / "V1688_v4_continuity.csv", index=False)
with open(OUT / "V1688_v4_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

def setup_3d(ax, title=None):
    ax.set_facecolor(BG)
    ax.grid(False)
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.set_alpha(0.045)
        pane.set_facecolor(GRID)
        pane.set_edgecolor(CYAN)
    ax.tick_params(colors=MUTED, labelsize=7)
    ax.set_xlabel("display x", color=MUTED, labelpad=-2)
    ax.set_ylabel("display y", color=MUTED, labelpad=-2)
    ax.set_zlabel("display z", color=MUTED, labelpad=-2)
    if title:
        ax.set_title(title, color=TEXT, fontsize=16, pad=8)
    ax.view_init(elev=25, azim=-55)

def draw_arrow3d(ax, start, vec, color, lw=2.0, alpha=1.0, label=None, label_offset=0.05):
    start = np.asarray(start)
    vec = np.asarray(vec)
    ax.quiver(start[0], start[1], start[2], vec[0], vec[1], vec[2],
              color=color, linewidth=lw, alpha=alpha, arrow_length_ratio=0.23, normalize=False)
    if label:
        end = start + vec
        ax.text(end[0]+label_offset, end[1]+label_offset, end[2]+label_offset, label, color=color, fontsize=8)

def draw_cycle(ax, active_step=None, trail_steps=None, show_vectors=True, show_curve=True):
    ids = list(nodes["node_id"])
    P = np.array([pos[nid] for nid in ids])

    if show_curve:
        PP = np.vstack([P, P[0]])
        dense = []
        for i in range(len(PP)-1):
            for t in np.linspace(0, 1, 14, endpoint=False):
                dense.append((1-t)*PP[i] + t*PP[i+1])
        dense.append(PP[-1])
        dense = np.array(dense)
        ax.plot(dense[:,0], dense[:,1], dense[:,2], color=GOLD, lw=1.3, alpha=0.22)

    for i, er in edges.iterrows():
        p, q = er["from_node"], er["to_node"]
        a, b = pos[p], pos[q]
        col, lw, alpha = GOLD, 2.2, 0.72
        if active_step is not None and i == active_step:
            col, lw, alpha = WHITE, 6.0, 1.0
        elif trail_steps is not None and i in trail_steps:
            col, lw, alpha = GREEN, 3.6, 0.95
        ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color=col, lw=lw, alpha=alpha)
        mid = 0.55*a + 0.45*b
        draw_arrow3d(ax, mid, unit(b-a)*0.20, col, lw=lw, alpha=alpha)

    ax.scatter(P[:,0], P[:,1], P[:,2], s=88, c=CYAN, edgecolors=WHITE, linewidths=0.8, alpha=0.98)
    for nid in ids:
        p = pos[nid]
        ax.text(p[0]+0.04, p[1]+0.04, p[2]+0.08, nid, color=TEXT, fontsize=9)

    if show_vectors:
        for nid in ids:
            p = pos[nid]
            draw_arrow3d(ax, p, unit(O3s[nid][:3])*0.34, ORANGE, lw=1.4, alpha=0.42)   # L3/O3
            draw_arrow3d(ax, p, unit(H4s[nid][:3])*0.39, VIOLET, lw=1.6, alpha=0.58)   # L4/H4_perp
            draw_arrow3d(ax, p, unit(Zs[nid][:3])*0.55, MAGENTA, lw=2.7, alpha=0.96)  # Z

def add_card(ax, title, lines, title_color=CYAN, fontsize=10.5):
    ax.set_facecolor(PANEL)
    ax.axis("off")
    # subtle border
    ax.add_patch(FancyBboxPatch((0.01,0.01),0.98,0.98,boxstyle="round,pad=0.012",
                                edgecolor=CYAN, facecolor=PANEL, linewidth=0.8, alpha=0.55))
    ax.text(0.04, 0.92, title, color=title_color, fontsize=13, family="DejaVu Sans Mono", va="top")
    y = 0.77
    for txt, color in lines:
        ax.text(0.04, y, txt, color=color, fontsize=fontsize, family="DejaVu Sans Mono", va="top")
        y -= 0.12

def draw_current_step_card(ax, active):
    er = edges.iloc[active]
    st = steps.iloc[active]
    lines = [
        (f"edge: {er['from_node']} → {er['to_node']}", WHITE),
        (f"γ_pq = {er['gamma_pq']:+.5f}", GOLD),
        (f"c_pq = {er['c_pq']:+.6f}", CYAN),
        (f"partial H = {st['H_cycle_partial']:+.3e}", CYAN),
        (f"partial defect = {st['directional_defect_partial']:.6f}", RED),
    ]
    add_card(ax, "Active native transport", lines, CYAN, fontsize=10.5)

def draw_equation_card(ax):
    lines = [
        ("G_p = span(B_p, O3_p, H4⊥_p)", TEXT),
        ("T_pq(dx)=dx+γ[roll(dx)⊙q − dx⊙roll(q)]", GOLD),
        ("c_pq=<Z_q,T_pq Z_p>/(||T_pq Z_p||||Z_q||)", CYAN),
        ("H_cycle^dir = Π_loop c_pq", MAGENTA),
        ("defect = |1 − H| · mean(|C_corr|)", RED),
    ]
    add_card(ax, "Proof object", lines, GOLD, fontsize=9.1)

def draw_metrics_card(ax):
    lines = [
        (f"H_cycle^dir = {H_final:+.3e}", CYAN),
        (f"native defect = {defect_final:.6f}", RED),
        (f"reverse diagnostic = {reverse_defect:.6f}", MUTED),
        (f"|fwd−rev| = {orientation_asym:.3e}", MUTED),
        (f"nodes={len(nodes)}, edges={len(edges)}", WHITE),
    ]
    add_card(ax, "Computed result", lines, GOLD, fontsize=10.0)

def draw_boundary_card(ax):
    lines = [
        ("Displayed curve = visualization only.", MUTED),
        ("Proof = ordered edge product Π_loop c_pq.", CYAN),
        ("No reversible full-matrix requirement.", WHITE),
        ("No Kabsch / Gramian alignment.", WHITE),
        ("Finite retained-flow proof object.", MUTED),
    ]
    add_card(ax, "Science boundary", lines, VIOLET, fontsize=9.8)

def draw_accumulation(ax, upto=None):
    ax.set_facecolor(PANEL)
    if upto is None:
        upto = len(steps)-1
    ax.plot(steps["step"], steps["directional_defect_partial"], color=GRID, lw=1.1, alpha=0.55)
    d = steps.iloc[:upto+1]
    ax.plot(d["step"], d["directional_defect_partial"], color=CYAN, marker="o", lw=2.3)
    ax.scatter([d["step"].iloc[-1]], [d["directional_defect_partial"].iloc[-1]], color=ORANGE, s=75, zorder=10)
    ax.set_title("Defect generated edge-by-edge", color=TEXT, fontsize=12)
    ax.set_xlabel("cycle step", color=MUTED)
    ax.set_ylabel("partial defect", color=MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(alpha=0.13, color=GRID)
    for sp in ax.spines.values():
        sp.set_color(CYAN); sp.set_alpha(0.75)

def draw_edge_ledger(ax, upto=None):
    ax.set_facecolor(PANEL)
    if upto is None:
        upto = len(steps)-1
    cols = []
    for i, v in enumerate(steps["c_pq"]):
        if i <= upto:
            cols.append(GREEN if v >= 0 else RED)
        else:
            cols.append(GRID)
    ax.bar(steps["step"], steps["c_pq"], color=cols, alpha=0.88)
    ax.axhline(0, color=WHITE, lw=0.8, alpha=0.5)
    ax.set_title("Edge-product ledger: c_pq values whose product generates H_cycle^dir", color=TEXT, fontsize=12)
    ax.set_xlabel("cycle step", color=MUTED)
    ax.set_ylabel("c_pq", color=MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(alpha=0.10, color=GRID)
    for sp in ax.spines.values():
        sp.set_color(CYAN); sp.set_alpha(0.75)

def draw_continuity_small(ax):
    ax.set_facecolor(PANEL)
    vals = continuity_df["continuity_residual"].values
    labels = continuity_df["node_id"].values
    colors = [RED if v > 0 else BLUE for v in vals]
    ax.bar(range(len(vals)), vals, color=colors, alpha=0.85)
    ax.axhline(0, color=WHITE, lw=0.8, alpha=0.55)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, rotation=45, color=MUTED, fontsize=7)
    ax.set_title("Incidence continuity residual", color=TEXT, fontsize=11)
    ax.tick_params(colors=MUTED, labelsize=7)
    for sp in ax.spines.values():
        sp.set_color(CYAN); sp.set_alpha(0.65)

# -----------------------------
# Static image V4: clean, readable
# -----------------------------
fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG)
gs = fig.add_gridspec(
    4, 5,
    width_ratios=[1.55, 1.55, 0.95, 0.95, 0.95],
    height_ratios=[0.16, 1.0, 0.86, 0.72],
    wspace=0.22, hspace=0.24
)

# Title strip
axTitle = fig.add_subplot(gs[0, :])
axTitle.set_facecolor(BG); axTitle.axis("off")
axTitle.text(0.5, 0.55, "V1688 Native Directional Holonomy — First-Principles Proof Visualization V4",
             ha="center", va="center", color=TEXT, fontsize=20, family="DejaVu Sans")
axTitle.text(0.5, 0.08, "L3/O3 + L4/H4⊥ correction mode transported around an explicit provenance cycle",
             ha="center", va="center", color="#9cecff", fontsize=10, family="DejaVu Sans Mono")

# Large topology
ax3d = fig.add_subplot(gs[1:4, 0:2], projection="3d")
setup_3d(ax3d, "3D retained L3/L4 provenance cycle")
draw_cycle(ax3d, active_step=None, trail_steps=set(range(len(edges))), show_vectors=True)
ax3d.text2D(0.02, 0.02,
            "Gold = explicit provenance cycle   Orange = L3/O3   Violet = L4/H4⊥   Magenta = Z correction mode\n"
            "Smoothed line is display-only; proof uses ordered edge product Π c_pq.",
            transform=ax3d.transAxes, color="#9cecff", fontsize=8.5, family="DejaVu Sans Mono")

# Cards
axEq = fig.add_subplot(gs[1, 2])
draw_equation_card(axEq)
axResult = fig.add_subplot(gs[1, 3])
draw_metrics_card(axResult)
axBound = fig.add_subplot(gs[1, 4])
draw_boundary_card(axBound)

# Plots
axAccum = fig.add_subplot(gs[2, 2:4])
draw_accumulation(axAccum, upto=len(edges)-1)
axContinuity = fig.add_subplot(gs[2, 4])
draw_continuity_small(axContinuity)

axLedger = fig.add_subplot(gs[3, 2:5])
draw_edge_ledger(axLedger, upto=len(edges)-1)

static_path = OUT / "V1688_v4_static_proof.png"
fig.savefig(static_path, dpi=180, facecolor=BG, bbox_inches="tight")
plt.close(fig)

# -----------------------------
# Animation frames V4
# -----------------------------
frame_paths = []
for frame_idx in range(len(edges)):
    fig = plt.figure(figsize=(16, 9), facecolor=BG)
    gs = fig.add_gridspec(
        3, 4,
        width_ratios=[1.45, 1.45, 1.0, 1.0],
        height_ratios=[0.16, 1.15, 0.75],
        wspace=0.22, hspace=0.25
    )

    axTitle = fig.add_subplot(gs[0, :])
    axTitle.set_facecolor(BG); axTitle.axis("off")
    axTitle.text(0.5, 0.60, "Directed native holonomy being generated", ha="center", va="center",
                 color=TEXT, fontsize=18)
    axTitle.text(0.5, 0.10, "active edge transport → c_pq → partial H_cycle^dir → defect",
                 ha="center", va="center", color="#9cecff", fontsize=10, family="DejaVu Sans Mono")

    ax3 = fig.add_subplot(gs[1:, 0:2], projection="3d")
    setup_3d(ax3, "Explicit provenance cycle")
    draw_cycle(ax3, active_step=frame_idx, trail_steps=set(range(frame_idx+1)), show_vectors=True)

    er = edges.iloc[frame_idx]
    p, q = er["from_node"], er["to_node"]
    gamma = float(er["gamma_pq"])
    c = float(er["c_pq"])
    TpZ = native_transport(Zs[p], states[q], gamma)
    draw_arrow3d(ax3, pos[q], unit(TpZ[:3])*0.72, WHITE, lw=3.4, alpha=1.0, label="T_pq Z_p")
    ax3.text2D(0.02, 0.05, f"edge {frame_idx+1}: {p} → {q}\nγ={gamma:+.4f}   c_pq={c:+.4f}",
               transform=ax3.transAxes, color=GOLD, fontsize=11, family="DejaVu Sans Mono")

    axStep = fig.add_subplot(gs[1, 2])
    draw_current_step_card(axStep, frame_idx)

    axAccum = fig.add_subplot(gs[1, 3])
    draw_accumulation(axAccum, upto=frame_idx)

    axLedger = fig.add_subplot(gs[2, 2:4])
    draw_edge_ledger(axLedger, upto=frame_idx)

    fpath = OUT / f"frame_{frame_idx:03d}.png"
    fig.savefig(fpath, dpi=140, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    frame_paths.append(fpath)

gif_path = OUT / "V1688_v4_holonomy_animation.gif"
mp4_path = OUT / "V1688_v4_holonomy_animation.mp4"

gif_ok = False
mp4_ok = False
try:
    from PIL import Image
    imgs = [Image.open(p).convert("P", palette=Image.ADAPTIVE) for p in frame_paths]
    imgs[0].save(gif_path, save_all=True, append_images=imgs[1:], duration=950, loop=0)
    gif_ok = gif_path.exists()
except Exception as e:
    print("GIF creation failed:", repr(e))

try:
    from PIL import Image
    import imageio.v2 as imageio
    even_dir = OUT / "mp4_even_frames"
    even_dir.mkdir(exist_ok=True)
    imgs = []
    for p in frame_paths:
        im = Image.open(p).convert("RGB")
        w, h = im.size
        if w % 2 or h % 2:
            im = im.crop((0, 0, w - (w % 2), h - (h % 2)))
        fp = even_dir / p.name
        im.save(fp)
        imgs.append(imageio.imread(str(fp)))
    imageio.mimsave(str(mp4_path), imgs, fps=1.2, codec="libx264", quality=8, macro_block_size=None)
    mp4_ok = mp4_path.exists() and mp4_path.stat().st_size > 1000
except Exception as e:
    print("MP4 creation failed:", repr(e))
    try:
        import sys, subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "-q", "install", "imageio-ffmpeg"])
        import imageio.v2 as imageio
        imgs = [imageio.imread(str(p)) for p in frame_paths]
        imageio.mimsave(str(mp4_path), imgs, fps=1.2)
        mp4_ok = mp4_path.exists() and mp4_path.stat().st_size > 1000
    except Exception as e2:
        print("MP4 fallback failed:", repr(e2))

metrics["gif_created"] = bool(gif_ok)
metrics["mp4_created"] = bool(mp4_ok)
with open(OUT / "V1688_v4_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

readme = f"""# V1688 Holonomy Proof Visualizer V4

Colab one-cell runnable proof visualization. Generates static PNG, GIF, and MP4.

## Core equations

```text
T_pq(dx) = dx + gamma_pq [roll(dx) ⊙ q − dx ⊙ roll(q)]
c_pq = <Z_q, T_pq Z_p> / (||T_pq Z_p|| ||Z_q||)
H_cycle^dir = Π_loop c_pq
native_directional_cycle_defect = |1 − H_cycle^dir| · mean(|C_corr|)
```

## Metrics

```json
{json.dumps(metrics, indent=2)}
```

## Boundary

The displayed curve is only a visualization of the discrete provenance cycle.
The proof object is the ordered edge product Π_loop c_pq.

This is a finite retained-flow proof object, not a GR/Einstein derivation.
"""
with open(OUT / "README.md", "w") as f:
    f.write(readme)

print("V1688 V4 complete.")
print(json.dumps(metrics, indent=2))
print("static:", static_path)
print("gif:", gif_path, "created:", gif_ok)
print("mp4:", mp4_path, "created:", mp4_ok)
