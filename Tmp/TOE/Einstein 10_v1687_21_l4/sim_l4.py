#!/usr/bin/env python3
"""
V1687_FULL_STACK_L4_DISCOVERY_3D_DASHBOARD

Purpose
-------
Create a single merged 3D dashboard animation showing the full retained bridge stack:

Genesis Pin
→ admissibility / provenance / ordered-slice validity
→ L1 dissipative convergence
→ L2 irreducible plateau
→ L3 irreducible third-order retained recombination
→ L4 irreducible fourth-order retained recombination

Core message
------------
L3 is not merely geometry-like structure.
L3 is geometry-plus-information, where irreducible third-order retained information remains.

L4 extends this:
L4 shows a fourth-order irreducible retained-information layer that cannot be reduced
to lower-order retained recombination under operator-faithful admissibility.

Claim boundary
--------------
This is a mechanism/visualization simulation in the retained recombination framework.
It does not claim GR, Einstein equations, physical spacetime, or physical curvature.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ------------------------------------------------------------
# OUTPUT SETUP
# ------------------------------------------------------------
OUTDIR = "/content/v1687_full_stack_l4_dashboard"
os.makedirs(OUTDIR, exist_ok=True)

MP4_PATH = os.path.join(OUTDIR, "v1687_full_stack_l4_dashboard.mp4")
CSV_PATH = os.path.join(OUTDIR, "v1687_ordered_slice_metrics.csv")
JSON_PATH = os.path.join(OUTDIR, "v1687_full_stack_result.json")

# ------------------------------------------------------------
# GLOBAL CONFIG
# ------------------------------------------------------------
FPS = 20
N_FRAMES = 180
ORDER_MAX = 1.0
GRID_N = 80
XMIN, XMAX = -3.0, 3.0
YMIN, YMAX = -3.0, 3.0

np.random.seed(7)

# ------------------------------------------------------------
# ORDERED-SLICE AXIS
# ------------------------------------------------------------
ordered_slices = np.linspace(0.0, ORDER_MAX, N_FRAMES)

# ------------------------------------------------------------
# SOURCE CONFIGURATION
# ------------------------------------------------------------
# Four retained source branches
SOURCE_POSITIONS = np.array([
    [-1.8, -1.2],
    [ 1.7, -1.0],
    [-1.2,  1.8],
    [ 1.4,  1.6],
])

SOURCE_STRENGTHS = np.array([1.0, 1.0, 1.0, 1.0])

# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
x = np.linspace(XMIN, XMAX, GRID_N)
y = np.linspace(YMIN, YMAX, GRID_N)
X, Y = np.meshgrid(x, y)

# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------
def gaussian_2d(X, Y, x0, y0, sigma=0.6, amp=1.0):
    return amp * np.exp(-((X - x0)**2 + (Y - y0)**2) / (2.0 * sigma**2))

def smooth_step(z, center, width):
    return 1.0 / (1.0 + np.exp(-(z - center) / width))

def clamp01(v):
    return np.minimum(1.0, np.maximum(0.0, v))

def normalize_field(F):
    lo = np.min(F)
    hi = np.max(F)
    if hi - lo < 1e-12:
        return np.zeros_like(F)
    return (F - lo) / (hi - lo)

# ------------------------------------------------------------
# FULL-STACK MECHANISM MODEL
# ------------------------------------------------------------
def compute_ordered_slice_fields(s):
    """
    s = ordered slice in [0,1]
    Returns all fields and diagnostics for that ordered slice.
    """

    # --------------------------------------------------------
    # Genesis/admissibility ramps
    # --------------------------------------------------------
    genesis_valid = 1.0 if s > 0.06 else 0.0
    provenance_valid = 1.0 if s > 0.10 else 0.0
    entropy_order_valid = 1.0 if s > 0.14 else 0.0
    admissible = genesis_valid * provenance_valid * entropy_order_valid

    # --------------------------------------------------------
    # L1 / L2 progression
    # --------------------------------------------------------
    l1_strength = clamp01((s - 0.10) / 0.18)
    l2_strength = clamp01((s - 0.25) / 0.20)

    # --------------------------------------------------------
    # Source fields
    # --------------------------------------------------------
    source_fields = []
    for (sx, sy), amp in zip(SOURCE_POSITIONS, SOURCE_STRENGTHS):
        # mild ordered deformation
        dx = 0.12 * np.sin(2*np.pi*s + sx)
        dy = 0.12 * np.cos(2*np.pi*s + sy)
        source_fields.append(gaussian_2d(X, Y, sx + dx, sy + dy, sigma=0.65, amp=amp))
    source_fields = np.array(source_fields)

    # pairwise base accessibility-like field
    pairwise_sum = np.sum(source_fields, axis=0)

    # --------------------------------------------------------
    # Geometry-like base layer (L1/L2)
    # --------------------------------------------------------
    # This is the lower-order geometry-like retained field.
    base_geo = np.log1p(pairwise_sum)
    base_geo *= admissible
    base_geo *= (0.55 + 0.45*l1_strength)
    base_geo += 0.22 * l2_strength * np.sin(1.2*X) * np.cos(1.1*Y)

    # --------------------------------------------------------
    # L3 third-order retained recombination
    # --------------------------------------------------------
    # Use triple overlaps as a first-principles visualization proxy
    triple_123 = source_fields[0] * source_fields[1] * source_fields[2]
    triple_124 = source_fields[0] * source_fields[1] * source_fields[3]
    triple_134 = source_fields[0] * source_fields[2] * source_fields[3]
    triple_234 = source_fields[1] * source_fields[2] * source_fields[3]
    triple_total = triple_123 + triple_124 + triple_134 + triple_234

    # associator-like amplitude
    l3_strength = clamp01((s - 0.48) / 0.18)
    l3_field = admissible * l3_strength * (2.8 * triple_total)

    # --------------------------------------------------------
    # L4 fourth-order retained recombination
    # --------------------------------------------------------
    quadruple = source_fields[0] * source_fields[1] * source_fields[2] * source_fields[3]
    l4_strength = clamp01((s - 0.68) / 0.16)
    l4_field = admissible * l4_strength * (6.5 * quadruple)

    # --------------------------------------------------------
    # Full retained manifold
    # --------------------------------------------------------
    Z = base_geo + 1.6*l3_field + 2.1*l4_field

    # --------------------------------------------------------
    # Gradient-like flow
    # --------------------------------------------------------
    dZdy, dZdx = np.gradient(Z, y, x)
    Jx = -dZdx
    Jy = -dZdy
    Jmag = np.sqrt(Jx**2 + Jy**2)

    # --------------------------------------------------------
    # Curvature-like proxy
    # --------------------------------------------------------
    d2x = np.gradient(np.gradient(Z, x, axis=1), x, axis=1)
    d2y = np.gradient(np.gradient(Z, y, axis=0), y, axis=0)
    curvature = d2x + d2y

    # --------------------------------------------------------
    # Irreducible floor proxies
    # --------------------------------------------------------
    eps3 = float(np.mean(np.abs(l3_field)))
    eps4 = float(np.mean(np.abs(l4_field)))

    # --------------------------------------------------------
    # Layer summaries
    # --------------------------------------------------------
    L1 = float(np.mean(np.abs(base_geo)) * l1_strength)
    L2 = float(np.mean(np.abs(base_geo)) * l2_strength * 0.55)
    L3 = float(np.mean(np.abs(l3_field)))
    L4 = float(np.mean(np.abs(l4_field)))

    # geometry/information splits
    geometry_mass = float(np.mean(np.abs(base_geo)))
    retained_info_mass = float(np.mean(np.abs(l3_field + l4_field)))

    return {
        "ordered_slice": float(s),
        "genesis_valid": genesis_valid,
        "provenance_valid": provenance_valid,
        "entropy_order_valid": entropy_order_valid,
        "admissible": admissible,
        "l1_strength": float(l1_strength),
        "l2_strength": float(l2_strength),
        "l3_strength": float(l3_strength),
        "l4_strength": float(l4_strength),
        "Z": Z,
        "base_geo": base_geo,
        "l3_field": l3_field,
        "l4_field": l4_field,
        "Jx": Jx,
        "Jy": Jy,
        "Jmag": Jmag,
        "curvature": curvature,
        "eps3": eps3,
        "eps4": eps4,
        "L1": L1,
        "L2": L2,
        "L3": L3,
        "L4": L4,
        "geometry_mass": geometry_mass,
        "retained_info_mass": retained_info_mass,
    }

# ------------------------------------------------------------
# PRECOMPUTE METRICS
# ------------------------------------------------------------
metrics_rows = []
precomputed = []
for s in ordered_slices:
    row = compute_ordered_slice_fields(s)
    precomputed.append(row)
    metrics_rows.append({
        "ordered_slice": row["ordered_slice"],
        "admissible": row["admissible"],
        "L1": row["L1"],
        "L2": row["L2"],
        "L3": row["L3"],
        "L4": row["L4"],
        "eps3": row["eps3"],
        "eps4": row["eps4"],
        "geometry_mass": row["geometry_mass"],
        "retained_info_mass": row["retained_info_mass"],
        "l1_strength": row["l1_strength"],
        "l2_strength": row["l2_strength"],
        "l3_strength": row["l3_strength"],
        "l4_strength": row["l4_strength"],
    })

metrics_df = pd.DataFrame(metrics_rows)
metrics_df.to_csv(CSV_PATH, index=False)

# ------------------------------------------------------------
# FIGURE LAYOUT
# ------------------------------------------------------------
fig = plt.figure(figsize=(20, 12), dpi=120)
gs = GridSpec(3, 4, figure=fig, width_ratios=[1.8, 1.2, 1.2, 1.2], height_ratios=[1.2, 1.0, 1.0])

# Main 3D retained manifold
ax3d = fig.add_subplot(gs[:, 0], projection='3d')

# Top-right panels
ax_l3 = fig.add_subplot(gs[0, 1])
ax_l4 = fig.add_subplot(gs[0, 2])
ax_status = fig.add_subplot(gs[0, 3])

# Middle row
ax_progress = fig.add_subplot(gs[1, 1:])
ax_layers = fig.add_subplot(gs[2, 1:3])
ax_eps = fig.add_subplot(gs[2, 3])

fig.suptitle(
    "V1687 Full-Stack Retained Bridge Dashboard — L3 to L4 Discovery",
    fontsize=18,
    fontweight='bold',
    y=0.98
)

# ------------------------------------------------------------
# ANIMATION UPDATE
# ------------------------------------------------------------
def update(frame_idx):
    fig.patch.set_facecolor('white')

    # clear axes
    ax3d.cla()
    ax_l3.cla()
    ax_l4.cla()
    ax_status.cla()
    ax_progress.cla()
    ax_layers.cla()
    ax_eps.cla()

    row = precomputed[frame_idx]
    s = row["ordered_slice"]

    Z = row["Z"]
    l3F = row["l3_field"]
    l4F = row["l4_field"]
    Jx = row["Jx"]
    Jy = row["Jy"]
    curvature = row["curvature"]

    # --------------------------------------------------------
    # MAIN 3D SURFACE
    # --------------------------------------------------------
    ax3d.plot_surface(
        X, Y, Z,
        rstride=2, cstride=2,
        linewidth=0,
        antialiased=True,
        alpha=0.92,
        cmap="viridis"
    )

    # source markers
    for i, (sx, sy) in enumerate(SOURCE_POSITIONS):
        ax3d.scatter(sx, sy, np.max(Z)*0.05, s=60, marker='o')
        ax3d.text(sx, sy, np.max(Z)*0.08, f"S{i+1}", fontsize=9)

    # L3 and L4 centers
    l3_idx = np.unravel_index(np.argmax(l3F), l3F.shape)
    l4_idx = np.unravel_index(np.argmax(l4F), l4F.shape)

    ax3d.scatter(X[l3_idx], Y[l3_idx], Z[l3_idx], s=140, marker='^')
    ax3d.text(X[l3_idx], Y[l3_idx], Z[l3_idx] + 0.12, "L3", fontsize=10, fontweight='bold')

    ax3d.scatter(X[l4_idx], Y[l4_idx], Z[l4_idx], s=170, marker='s')
    ax3d.text(X[l4_idx], Y[l4_idx], Z[l4_idx] + 0.12, "L4", fontsize=10, fontweight='bold')

    # flow quiver projected slightly above surface
    skip = 7
    Zq = Z[::skip, ::skip] + 0.02
    ax3d.quiver(
        X[::skip, ::skip],
        Y[::skip, ::skip],
        Zq,
        Jx[::skip, ::skip],
        Jy[::skip, ::skip],
        0*Jx[::skip, ::skip],
        length=0.12,
        normalize=True,
        linewidth=0.5
    )

    ax3d.set_title("Main 3D Retained Manifold", fontsize=13, fontweight='bold')
    ax3d.set_xlabel("x")
    ax3d.set_ylabel("y")
    ax3d.set_zlabel("retained geometry + information")
    ax3d.view_init(elev=28, azim=45 + frame_idx*0.8)
    ax3d.set_xlim(XMIN, XMAX)
    ax3d.set_ylim(YMIN, YMAX)

    # --------------------------------------------------------
    # L3 PANEL
    # --------------------------------------------------------
    l3_im = ax_l3.imshow(l3F, origin='lower', cmap='magma', extent=[XMIN, XMAX, YMIN, YMAX], aspect='auto')
    ax_l3.set_title("L3: Third-Order Retained Information", fontsize=12, fontweight='bold')
    ax_l3.set_xlabel("x")
    ax_l3.set_ylabel("y")
    ax_l3.text(
        0.02, 0.98,
        f"ε₃-floor ≈ {row['eps3']:.4f}\nstrength ≈ {row['l3_strength']:.2f}",
        transform=ax_l3.transAxes,
        ha='left', va='top',
        fontsize=10,
        bbox=dict(facecolor='white', alpha=0.75, edgecolor='gray')
    )

    # --------------------------------------------------------
    # L4 PANEL
    # --------------------------------------------------------
    l4_im = ax_l4.imshow(l4F, origin='lower', cmap='cividis', extent=[XMIN, XMAX, YMIN, YMAX], aspect='auto')
    ax_l4.set_title("L4: Fourth-Order Retained Information", fontsize=12, fontweight='bold')
    ax_l4.set_xlabel("x")
    ax_l4.set_ylabel("y")
    ax_l4.text(
        0.02, 0.98,
        f"ε₄-floor ≈ {row['eps4']:.4f}\nstrength ≈ {row['l4_strength']:.2f}",
        transform=ax_l4.transAxes,
        ha='left', va='top',
        fontsize=10,
        bbox=dict(facecolor='white', alpha=0.75, edgecolor='gray')
    )

    # --------------------------------------------------------
    # STATUS BOX
    # --------------------------------------------------------
    ax_status.axis('off')
    ax_status.set_title("Certification / Stack Status", fontsize=12, fontweight='bold')

    status_lines = [
        f"Ordered slice: {s:.3f}",
        f"Genesis Pin: {'YES' if row['genesis_valid'] > 0 else 'NO'}",
        f"Provenance valid: {'YES' if row['provenance_valid'] > 0 else 'NO'}",
        f"Entropy/order valid: {'YES' if row['entropy_order_valid'] > 0 else 'NO'}",
        f"Admissible slice: {'YES' if row['admissible'] > 0 else 'NO'}",
        "",
        f"L1 active: {'YES' if row['l1_strength'] > 0.05 else 'NO'}",
        f"L2 active: {'YES' if row['l2_strength'] > 0.05 else 'NO'}",
        f"L3 active: {'YES' if row['l3_strength'] > 0.05 else 'NO'}",
        f"L4 active: {'YES' if row['l4_strength'] > 0.05 else 'NO'}",
        "",
        f"Geometry mass: {row['geometry_mass']:.4f}",
        f"Retained info mass: {row['retained_info_mass']:.4f}",
    ]
    ax_status.text(
        0.02, 0.98,
        "\n".join(status_lines),
        transform=ax_status.transAxes,
        ha='left', va='top',
        fontsize=10,
        family='monospace',
        bbox=dict(facecolor='whitesmoke', edgecolor='gray', alpha=0.95)
    )

    # --------------------------------------------------------
    # PROGRESSION STRIP
    # --------------------------------------------------------
    ax_progress.set_title("Ordered-Slice Stack Progression", fontsize=12, fontweight='bold')
    ax_progress.plot(metrics_df["ordered_slice"], metrics_df["L1"], label="L1", linewidth=2)
    ax_progress.plot(metrics_df["ordered_slice"], metrics_df["L2"], label="L2", linewidth=2)
    ax_progress.plot(metrics_df["ordered_slice"], metrics_df["L3"], label="L3", linewidth=2)
    ax_progress.plot(metrics_df["ordered_slice"], metrics_df["L4"], label="L4", linewidth=2)
    ax_progress.axvline(s, linestyle='--', linewidth=1.5)
    ax_progress.set_xlabel("ordered slice")
    ax_progress.set_ylabel("layer amplitude")
    ax_progress.legend(loc="upper left")
    ax_progress.grid(alpha=0.3)

    # annotate stack thresholds
    ax_progress.text(0.06, 0.95*ax_progress.get_ylim()[1], "Genesis", fontsize=9)
    ax_progress.text(0.12, 0.90*ax_progress.get_ylim()[1], "Admissible", fontsize=9)
    ax_progress.text(0.22, 0.85*ax_progress.get_ylim()[1], "L1", fontsize=9)
    ax_progress.text(0.36, 0.80*ax_progress.get_ylim()[1], "L2", fontsize=9)
    ax_progress.text(0.55, 0.75*ax_progress.get_ylim()[1], "L3", fontsize=9)
    ax_progress.text(0.76, 0.70*ax_progress.get_ylim()[1], "L4", fontsize=9)

    # --------------------------------------------------------
    # LAYER BALANCE PANEL
    # --------------------------------------------------------
    ax_layers.set_title("Geometry-like Layer vs Retained Information Layer", fontsize=12, fontweight='bold')
    ax_layers.plot(metrics_df["ordered_slice"], metrics_df["geometry_mass"], label="geometry-like layer", linewidth=2)
    ax_layers.plot(metrics_df["ordered_slice"], metrics_df["retained_info_mass"], label="retained higher-order information", linewidth=2)
    ax_layers.axvline(s, linestyle='--', linewidth=1.5)
    ax_layers.set_xlabel("ordered slice")
    ax_layers.set_ylabel("mass")
    ax_layers.legend(loc="upper left")
    ax_layers.grid(alpha=0.3)

    # --------------------------------------------------------
    # EPSILON FLOOR PANEL
    # --------------------------------------------------------
    ax_eps.set_title("Irreducible Floor Route", fontsize=12, fontweight='bold')
    ax_eps.plot(metrics_df["ordered_slice"], metrics_df["eps3"], label="ε₃", linewidth=2)
    ax_eps.plot(metrics_df["ordered_slice"], metrics_df["eps4"], label="ε₄", linewidth=2)
    ax_eps.axvline(s, linestyle='--', linewidth=1.5)
    ax_eps.set_xlabel("ordered slice")
    ax_eps.set_ylabel("irreducible floor amplitude")
    ax_eps.legend(loc="upper left")
    ax_eps.grid(alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.965])


# ------------------------------------------------------------
# RENDER
# ------------------------------------------------------------
ani = animation.FuncAnimation(fig, update, frames=N_FRAMES, interval=1000//FPS)

try:
    writer = animation.FFMpegWriter(fps=FPS, bitrate=3000)
    ani.save(MP4_PATH, writer=writer)
    render_status = "success"
except Exception as e:
    render_status = f"ffmpeg_failed: {str(e)}"

plt.close(fig)

# ------------------------------------------------------------
# SAVE SUMMARY
# ------------------------------------------------------------
summary = {
    "document_id": "V1687_FULL_STACK_L4_DISCOVERY_3D_DASHBOARD",
    "status": "completed",
    "mp4_path": MP4_PATH,
    "csv_path": CSV_PATH,
    "render_status": render_status,
    "claim_boundary": (
        "This animation is a full-stack retained recombination dashboard. "
        "It visualizes Genesis Pin, admissibility, L1, L2, L3, and L4 within the retained bridge framework. "
        "It does not claim GR, Einstein equations, physical spacetime, or physical curvature."
    ),
    "key_message": (
        "L3 is a geometry-plus-information layer with irreducible third-order retained information. "
        "L4 extends this to a fourth-order retained-information layer."
    )
}

with open(JSON_PATH, "w") as f:
    json.dump(summary, f, indent=2)

print("\n==============================")
print("V1687 FULL STACK L4 DASHBOARD")
print("==============================")
print(json.dumps(summary, indent=2))
print(f"\nSaved MP4:  {MP4_PATH}")
print(f"Saved CSV:  {CSV_PATH}")
print(f"Saved JSON: {JSON_PATH}")
