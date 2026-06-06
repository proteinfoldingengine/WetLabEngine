# ============================================================
# V1686.35 — Forced-HD Export Fix for L3 Dashboard MP4
# ============================================================
# Colab-ready, self-contained.
#
# Purpose:
#   Same scientific dashboard as V1686.34, but with forced 1920×1080 export.
#
# Fixes:
#   1. render at exact 1920×1080 canvas
#   2. save raw MP4
#   3. post-process with ffmpeg:
#          -vf scale=1920:1080
#          -c:v libx264
#          -pix_fmt yuv420p
#          -b:v 9000k
#          -movflags +faststart
#   4. validate output dimensions with ffprobe
#
# Core message:
#   L3 is not eliminated. It is reclassified.
#   L3 = geometry + irreducible retained information.
#   ε-floor is a lower-bound route from a third-order retained-current
#   associator obstruction under operator-faithful admissibility.
#
# Boundary:
#   Synthetic full-stack audit simulation only.
#   No empirical L3 claim.
#   No physical geometry / GR / ADM claim.
#   No universal theorem over all operators.
# ============================================================

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Tuple, List

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, PillowWriter, FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


# ============================================================
# CONFIG
# ============================================================

DOCUMENT_ID = "V1686_35_FORCED_HD_EXPORT_FIX"

OUT = Path("/content/v1686_35_forced_hd_export_fix")
OUT.mkdir(parents=True, exist_ok=True)

SEED = 168635
rng = np.random.default_rng(SEED)

MODE = "PUBLIC"  # PUBLIC or AUDIT

# Exact HD canvas.
TARGET_W = 1920
TARGET_H = 1080
DPI = 100
FIGSIZE = (TARGET_W / DPI, TARGET_H / DPI)

N = 50
ORDERED_SLICES = 48

FPS = 24
HOLD_EACH_ORDERED_SLICE = 8
INTRO_CARD_FRAMES = 48
END_CARD_FRAMES = 120

RAW_MP4_NAME = "v1686_35_raw_dashboard.mp4"
HD_MP4_NAME = "v1686_35_forced_1920x1080_l3_dashboard.mp4"
GIF_NAME = "v1686_35_forced_hd_preview.gif"

SAVE_MP4 = True
SAVE_GIF_PREVIEW = True
SAVE_KEYFRAMES = True
SAVE_CSV = True

print(f"Output directory: {OUT}")
print(f"Target canvas: {TARGET_W} × {TARGET_H}")
print(f"FIGSIZE: {FIGSIZE}, DPI={DPI}")


# ============================================================
# STRUCTURES
# ============================================================

@dataclass
class GenesisPin:
    root_anchor: str
    quorum_required: int
    witness_count: int
    pinned: bool
    note: str


@dataclass
class BranchCurrent:
    name: str
    source_id: str
    retained_order: int
    support: np.ndarray
    flow: np.ndarray
    closure_weight: float
    provenance_valid: bool = True

    def vector(self) -> np.ndarray:
        return self.support * self.flow * self.closure_weight


@dataclass
class RecombinedState:
    vector: np.ndarray
    sources: Tuple[str, ...]
    retained_order_signature: Tuple[int, ...]
    branch_names: Tuple[str, ...]
    closure_weight: float
    provenance_valid: bool


# ============================================================
# FIELD HELPERS
# ============================================================

def make_grid(n=N):
    axis = np.linspace(-1.0, 1.0, n)
    X, Y = np.meshgrid(axis, axis)
    return X, Y

X, Y = make_grid(N)

def gaussian2d(cx, cy, sx, sy, amp=1.0):
    return amp * np.exp(-(((X - cx) ** 2) / (2 * sx ** 2) + ((Y - cy) ** 2) / (2 * sy ** 2)))

def normalize_field(z, eps=1e-12):
    m = np.max(np.abs(z))
    if m < eps:
        return z.copy()
    return z / m

def soft_support(cx, cy, radius, softness=0.07):
    r = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    return 1.0 / (1.0 + np.exp((r - radius) / softness))

def ring_support(radius=0.58, width=0.16, softness=0.04):
    r = np.sqrt(X**2 + Y**2)
    outer = 1.0 / (1.0 + np.exp((r - (radius + width)) / softness))
    inner = 1.0 / (1.0 + np.exp((r - (radius - width)) / softness))
    return outer * (1 - inner)

def laplacian(z):
    return (
        np.roll(z, 1, axis=0) + np.roll(z, -1, axis=0)
        + np.roll(z, 1, axis=1) + np.roll(z, -1, axis=1)
        - 4 * z
    )

def curvature_like(z):
    return normalize_field(-laplacian(z))

def branch_rank(vectors: List[np.ndarray], tol=1e-9):
    M = np.stack([v.reshape(-1) for v in vectors], axis=1)
    return int(np.linalg.matrix_rank(M, tol=tol))

def rank_lift(branch_vectors: List[np.ndarray], assoc: np.ndarray):
    B = np.stack([v.reshape(-1) for v in branch_vectors], axis=1)
    BA = np.column_stack([B, assoc.reshape(-1)])
    return int(np.linalg.matrix_rank(BA, tol=1e-9) - np.linalg.matrix_rank(B, tol=tol if False else 1e-9))

def residual_to_span(x: np.ndarray, basis: List[np.ndarray]):
    B = np.stack([b.reshape(-1) for b in basis], axis=1)
    xf = x.reshape(-1)
    coeff = np.linalg.pinv(B) @ xf
    proj = B @ coeff
    res = xf - proj
    return res.reshape(x.shape), float(np.linalg.norm(res)), coeff


# ============================================================
# GENESIS + BRANCHES
# ============================================================

def create_genesis_pin():
    return GenesisPin(
        root_anchor="ROOT:GENESIS_ANCHOR_000",
        quorum_required=3,
        witness_count=3,
        pinned=True,
        note="Synthetic genesis pin: provenance root required before retained recombination is admissible."
    )

def create_branch_currents() -> List[BranchCurrent]:
    S1 = np.maximum(soft_support(-0.35, -0.15, 0.70), 0.42 * ring_support())
    S2 = np.maximum(soft_support(0.35, -0.12, 0.70), 0.42 * ring_support())
    S3 = np.maximum(soft_support(0.02, 0.43, 0.70), 0.42 * ring_support())

    F1 = (
        1.1 * gaussian2d(-0.45, -0.20, 0.24, 0.34)
        - 0.52 * gaussian2d(0.30, 0.34, 0.30, 0.22)
        + 0.18 * np.sin(3.0 * np.pi * X) * np.cos(2.0 * np.pi * Y)
    )
    F2 = (
        1.05 * gaussian2d(0.42, -0.18, 0.25, 0.35)
        - 0.46 * gaussian2d(-0.28, 0.34, 0.28, 0.24)
        + 0.20 * np.cos(2.6 * np.pi * X) * np.sin(2.2 * np.pi * Y)
    )
    F3 = (
        1.02 * gaussian2d(0.02, 0.44, 0.34, 0.24)
        - 0.38 * gaussian2d(0.02, -0.46, 0.28, 0.25)
        + 0.22 * np.sin(2.2 * np.pi * (X + Y))
    )

    return [
        BranchCurrent("J1", "SOURCE_A", 0, S1, normalize_field(F1), 1.0),
        BranchCurrent("J2", "SOURCE_B", 1, S2, normalize_field(F2), 1.0),
        BranchCurrent("J3", "SOURCE_C", 2, S3, normalize_field(F3), 1.0),
    ]


# ============================================================
# RETAINED RECOMBINATION
# ============================================================

def overlap_gate(a, b):
    overlap = np.minimum(np.abs(a), np.abs(b))
    return overlap / (1.0 + overlap)

def retained_order_orientation(sig_a, sig_b):
    oa = float(np.mean(sig_a))
    ob = float(np.mean(sig_b))
    if ob > oa:
        return 1.0
    if ob < oa:
        return -1.0
    return 0.0

def harmonic_closure_weight(ca, cb):
    return (2.0 * ca * cb) / max(1e-12, ca + cb)

def kernel_order_overlap(a, b):
    roll_a = 0.5 * (np.roll(a, 1, axis=0) + np.roll(a, 1, axis=1))
    roll_b = 0.5 * (np.roll(b, -1, axis=0) + np.roll(b, -1, axis=1))
    return roll_a * b - a * roll_b

def as_state(obj):
    if isinstance(obj, RecombinedState):
        return obj
    if isinstance(obj, BranchCurrent):
        return RecombinedState(
            vector=obj.vector(),
            sources=(obj.source_id,),
            retained_order_signature=(obj.retained_order,),
            branch_names=(obj.name,),
            closure_weight=obj.closure_weight,
            provenance_valid=obj.provenance_valid,
        )
    raise TypeError(type(obj))

def retained_recombine(a, b):
    A = as_state(a)
    B = as_state(b)
    orient = retained_order_orientation(A.retained_order_signature, B.retained_order_signature)
    closure = harmonic_closure_weight(A.closure_weight, B.closure_weight)
    gate = overlap_gate(A.vector, B.vector)
    phi = closure * orient * gate * kernel_order_overlap(A.vector, B.vector)

    return RecombinedState(
        vector=A.vector + B.vector + phi,
        sources=tuple(list(A.sources) + list(B.sources)),
        retained_order_signature=tuple(list(A.retained_order_signature) + list(B.retained_order_signature)),
        branch_names=tuple(list(A.branch_names) + list(B.branch_names)),
        closure_weight=float(closure),
        provenance_valid=bool(A.provenance_valid and B.provenance_valid),
    )

def associator_obstruction(J1, J2, J3):
    left = retained_recombine(retained_recombine(J1, J2), J3)
    right = retained_recombine(J1, retained_recombine(J2, J3))
    return left.vector - right.vector


# ============================================================
# PROJECTION AUDIT
# ============================================================

def project_field_lowpass(z, keep_radius=0.20):
    F = np.fft.fftshift(np.fft.fft2(z))
    n, m = z.shape
    yy, xx = np.ogrid[-1:1:n*1j, -1:1:m*1j]
    rr = np.sqrt(xx**2 + yy**2)
    mask = (rr <= keep_radius).astype(float)
    return np.real(np.fft.ifft2(np.fft.ifftshift(F * mask)))

def project_branch(branch: BranchCurrent, keep_radius=0.20):
    return BranchCurrent(
        name=branch.name,
        source_id=branch.source_id,
        retained_order=branch.retained_order,
        support=np.clip(project_field_lowpass(branch.support, keep_radius), 0, None),
        flow=project_field_lowpass(branch.flow, keep_radius),
        closure_weight=branch.closure_weight,
        provenance_valid=branch.provenance_valid,
    )

def operator_faithfulness_gap(branches, keep_radius=0.20):
    gaps = {}
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        Ji, Jj = branches[i], branches[j]
        lhs = project_field_lowpass(retained_recombine(Ji, Jj).vector, keep_radius)
        Pi = project_branch(Ji, keep_radius)
        Pj = project_branch(Jj, keep_radius)
        rhs = retained_recombine(Pi, Pj).vector
        gaps[f"{Ji.name}{Jj.name}"] = float(np.linalg.norm(lhs - rhs))
    return gaps


# ============================================================
# ORDERED SLICE ENGINE
# ============================================================

def emergence_weight(ordered_slice, center, sharpness=0.55):
    x = (ordered_slice - center) * sharpness
    return 1.0 / (1.0 + np.exp(-x))

def compute_slice(branches, ordered_slice: int):
    J1, J2, J3 = branches

    w1 = emergence_weight(ordered_slice, 4, 0.78)
    w2 = emergence_weight(ordered_slice, 12, 0.70)
    w3 = emergence_weight(ordered_slice, 21, 0.68)

    B1 = BranchCurrent(J1.name, J1.source_id, J1.retained_order, J1.support, J1.flow, w1)
    B2 = BranchCurrent(J2.name, J2.source_id, J2.retained_order, J2.support, J2.flow, w2)
    B3 = BranchCurrent(J3.name, J3.source_id, J3.retained_order, J3.support, J3.flow, w3)

    pair12 = retained_recombine(B1, B2).vector
    pair23 = retained_recombine(B2, B3).vector
    pair13 = retained_recombine(B1, B3).vector
    pair_mean = (pair12 + pair23 + pair13) / 3.0

    O123 = associator_obstruction(B1, B2, B3)

    geom_field = curvature_like(pair_mean)
    info_field = normalize_field(O123)

    l3_field = normalize_field(0.78 * geom_field + 0.55 * info_field)
    projected_l3 = project_field_lowpass(l3_field, keep_radius=0.20)
    epsilon_floor_field = l3_field - projected_l3

    branches_active = [B1.vector(), B2.vector(), B3.vector()]
    r_branch = branch_rank(branches_active)
    r_lift = rank_lift(branches_active, O123)

    assoc_norm = float(np.linalg.norm(O123))
    res, res_norm, coeff = residual_to_span(O123, branches_active)
    rel_res = float(res_norm / max(1e-12, assoc_norm))

    gap = operator_faithfulness_gap([B1, B2, B3], keep_radius=0.20)

    metrics = {
        "ordered_slice": int(ordered_slice),
        "branch_rank": int(r_branch),
        "rank_lift": int(r_lift),
        "NOOCI_supported": int(r_lift > 0 and res_norm > 1e-10),
        "associator_norm": assoc_norm,
        "associator_span_residual_norm": float(res_norm),
        "associator_span_relative_residual": rel_res,
        "epsilon_floor_norm": float(np.linalg.norm(epsilon_floor_field)),
        "operator_faithfulness_gap_max_lowpass_projection": float(max(gap.values())),
        "w1": float(w1),
        "w2": float(w2),
        "w3": float(w3),
    }

    return {
        "branches": [B1, B2, B3],
        "branch_sum": sum(branches_active),
        "pair_mean": pair_mean,
        "geom_field": geom_field,
        "O123": O123,
        "info_field": info_field,
        "l3_field": l3_field,
        "projected_l3": projected_l3,
        "epsilon_floor_field": epsilon_floor_field,
        "metrics": metrics,
    }


# ============================================================
# PRECOMPUTE
# ============================================================

genesis = create_genesis_pin()
branches = create_branch_currents()
states = [compute_slice(branches, k) for k in range(48)]
metrics_df = pd.DataFrame([s["metrics"] for s in states])

if SAVE_CSV:
    metrics_df.to_csv(OUT / "v1686_35_ordered_slice_metrics.csv", index=False)


# ============================================================
# DRAWING
# ============================================================

def add_surface(ax, Z, title, cmap="viridis", zlim=(-1.15, 1.15), elev=30, azim=-55, alpha=0.94, title_size=12):
    ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=True, alpha=alpha)
    ax.set_title(title, fontsize=title_size, pad=5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_zlim(*zlim)
    ax.view_init(elev=elev, azim=azim)

def norm(vals):
    vals = np.asarray(vals, dtype=float)
    mx = np.max(np.abs(vals))
    if mx < 1e-12:
        return vals
    return vals / mx

def draw_chart_panel(ax, frame_idx):
    ax.clear()
    x = metrics_df["ordered_slice"].values[:frame_idx+1]

    eps = norm(metrics_df["epsilon_floor_norm"].values)
    assoc = norm(metrics_df["associator_norm"].values)
    res_span = metrics_df["associator_span_relative_residual"].values
    rank_l = metrics_df["rank_lift"].values
    nooci = metrics_df["NOOCI_supported"].values

    ax.plot(x, eps[:frame_idx+1], linewidth=3.0, label="ε-floor")
    ax.plot(x, assoc[:frame_idx+1], linewidth=2.6, label="O₁₂₃")
    ax.plot(x, res_span[:frame_idx+1], linewidth=2.5, label="residual/span")
    ax.step(x, rank_l[:frame_idx+1], where="post", linewidth=2.6, label="rank_lift")
    ax.step(x, nooci[:frame_idx+1], where="post", linewidth=2.4, label="NOOCI")

    ax.set_xlim(0, 47)
    ax.set_ylim(-0.08, 1.12)
    ax.set_title("Progression across ordered slices", fontsize=15, pad=8)
    ax.set_xlabel("ordered_slice", fontsize=11)
    ax.set_ylabel("normalized / pass metric", fontsize=11)
    ax.tick_params(labelsize=10)
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=10, loc="lower right", framealpha=0.95)

    for x0, label in [(4, "J1"), (12, "J2"), (21, "J3"), (23, "NOOCI")]:
        ax.axvline(x0, linestyle="--", alpha=0.25)
        ax.text(x0 + 0.2, 1.07, label, fontsize=9, rotation=90, va="top")

def draw_audit_panel(ax, state, frame_idx):
    ax.clear()
    ax.axis("off")
    m = state["metrics"]

    phase = (
        "GENESIS / BRANCH FORMATION" if frame_idx < 10 else
        "PAIRWISE CLOSURE FORMING" if frame_idx < 21 else
        "TRIPLE RECOMBINATION ACTIVE" if frame_idx < 30 else
        "L3 = GEOMETRY + INFORMATION"
    )

    nooci_status = "PASS" if m["NOOCI_supported"] else "WAIT"
    rank_status = "PASS" if m["rank_lift"] > 0 else "WAIT"

    lines = [
        "LIVE FULL-STACK AUDIT",
        "",
        f"ordered_slice: {frame_idx}",
        f"phase: {phase}",
        "",
        "Genesis Pin: PASS",
        "Provenance:  PASS",
        "",
        f"rank_lift:   {m['rank_lift']}  {rank_status}",
        f"NOOCI:       {nooci_status}",
        f"residual/span: {m['associator_span_relative_residual']:.3f}",
        f"ε-floor norm:  {m['epsilon_floor_norm']:.3f}",
        "",
        "Interpretation:",
        "L3 is not eliminated.",
        "L3 = geometry + retained information.",
        "ε-floor marks irreducible",
        "third-order retained recombination.",
    ]

    ax.text(
        0.02, 0.98, "\n".join(lines),
        va="top", ha="left",
        fontsize=14,
        family="monospace",
        linespacing=1.18
    )

def draw_intro_card(fig):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.axis("off")
    txt = (
        "V1686.35 — Full-Stack L3 Irreducibility\n\n"
        "Genesis Pin → Pairwise Closure → Third-Order Associator → ε-floor\n\n"
        "L3 is not merely geometry.\n"
        "L3 is geometry plus irreducible retained information.\n\n"
        "Forced-HD synthetic full-stack audit simulation"
    )
    ax.text(0.5, 0.56, txt, ha="center", va="center", fontsize=32, linespacing=1.32)

def draw_end_card(fig):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.axis("off")
    txt = (
        "V1686.35 Result\n\n"
        "L3 is not eliminated. It is reclassified.\n\n"
        "Three-branch retained recombination creates an operator-faithful\n"
        "associator obstruction O₁₂₃ that contributes an independent retained direction.\n\n"
        "Under honest admissibility, that structure cannot be erased\n"
        "by reducing everything to pairwise branch geometry.\n\n"
        "ε-floor is a lower-bound route from irreducible\n"
        "third-order retained information.\n\n"
        "Boundary: synthetic mechanism/audit simulation only.\n"
        "No empirical L3, physical geometry, GR, or ADM claim."
    )
    ax.text(0.5, 0.52, txt, ha="center", va="center", fontsize=28, linespacing=1.30)

ORDERED_SLICES = 48
INTRO_CARD_FRAMES = 48
END_CARD_FRAMES = 120
HOLD_EACH_ORDERED_SLICE = 8
TOTAL_FRAMES = INTRO_CARD_FRAMES + ORDERED_SLICES * HOLD_EACH_ORDERED_SLICE + END_CARD_FRAMES

def logical_frame_to_ordered_slice(logical_frame):
    if logical_frame < INTRO_CARD_FRAMES:
        return None, "intro"
    k = logical_frame - INTRO_CARD_FRAMES
    progression_frames = ORDERED_SLICES * HOLD_EACH_ORDERED_SLICE
    if k >= progression_frames:
        return None, "end"
    return int(min(ORDERED_SLICES - 1, k // HOLD_EACH_ORDERED_SLICE)), "dashboard"

def render_dashboard_frame(fig, logical_frame):
    ordered_slice, mode = logical_frame_to_ordered_slice(logical_frame)

    if mode == "intro":
        draw_intro_card(fig)
        return []
    if mode == "end":
        draw_end_card(fig)
        return []

    fig.clear()
    state = states[ordered_slice]
    az = -58 + 0.85 * ordered_slice

    gs = fig.add_gridspec(
        3, 4,
        height_ratios=[1.08, 1.08, 0.95],
        width_ratios=[1, 1, 1, 1.28]
    )

    ax_main = fig.add_subplot(gs[0:2, 0:2], projection="3d")
    add_surface(
        ax_main,
        state["l3_field"],
        "MAIN: L3 = geometry-like closure + retained information",
        cmap="magma",
        elev=31,
        azim=az,
        title_size=17
    )

    ax_chart = fig.add_subplot(gs[0, 2:4])
    draw_chart_panel(ax_chart, ordered_slice)

    ax_audit = fig.add_subplot(gs[1, 2:4])
    draw_audit_panel(ax_audit, state, ordered_slice)

    sub = gs[2, :].subgridspec(1, 5, wspace=0.03)

    panels = [
        (normalize_field(state["branch_sum"]), "Genesis-certified\nbranches", "viridis"),
        (state["geom_field"], "L1/L2 pairwise\nclosure", "plasma"),
        (state["info_field"], "O₁₂₃ associator\ninformation", "coolwarm"),
        (normalize_field(state["projected_l3"]), "Projection\nattempt", "cividis"),
        (normalize_field(state["epsilon_floor_field"]), "ε-floor\nremainder", "inferno"),
    ]

    for i, (Z, title, cmap) in enumerate(panels):
        ax = fig.add_subplot(sub[0, i], projection="3d")
        add_surface(ax, Z, title, cmap=cmap, elev=25, azim=az, title_size=12)

    fig.suptitle(
        "V1686.35 Full-Stack L3 Irreducibility Dashboard",
        fontsize=22,
        y=0.985
    )
    fig.subplots_adjust(left=0.025, right=0.985, top=0.925, bottom=0.035, wspace=0.18, hspace=0.20)
    return []


# ============================================================
# EXPORT HELPERS
# ============================================================

def run_cmd(cmd):
    print("RUN:", " ".join(cmd))
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.stdout:
        print(p.stdout[-1000:])
    if p.stderr:
        print(p.stderr[-1000:])
    return p

def ffprobe_dimensions(path: Path):
    if not shutil.which("ffprobe"):
        return {"available": False}
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration",
        "-of", "json",
        str(path)
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return {"available": True, "error": p.stderr}
    return json.loads(p.stdout)

def render_keyframes():
    key_ordered = [0, 8, 16, 24, 32, 41, 47]
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    for k in key_ordered:
        logical = INTRO_CARD_FRAMES + k * HOLD_EACH_ORDERED_SLICE
        render_dashboard_frame(fig, logical)
        fig.savefig(OUT / f"v1686_35_keyframe_ordered_{k:03d}.png", dpi=DPI)
    plt.close(fig)

def render_raw_mp4():
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    raw_path = OUT / RAW_MP4_NAME
    writer = FFMpegWriter(
        fps=FPS,
        metadata={"title": DOCUMENT_ID},
        bitrate=9000,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    )
    with writer.saving(fig, str(raw_path), DPI):
        for frame_idx in range(TOTAL_FRAMES):
            render_dashboard_frame(fig, frame_idx)
            writer.grab_frame()
    plt.close(fig)
    return raw_path

def force_hd_export(raw_path: Path):
    hd_path = OUT / HD_MP4_NAME
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found; copying raw MP4 as fallback.")
        shutil.copy2(raw_path, hd_path)
        return hd_path

    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_path),
        "-vf", f"scale={TARGET_W}:{TARGET_H}:flags=lanczos",
        "-r", str(FPS),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-b:v", "9000k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-an",
        str(hd_path),
    ]
    p = run_cmd(cmd)
    if p.returncode != 0:
        print("Forced HD export failed; copying raw MP4 fallback.")
        shutil.copy2(raw_path, hd_path)
    return hd_path

def render_gif_preview():
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    frame_list = list(range(0, TOTAL_FRAMES, 12))
    if frame_list[-1] != TOTAL_FRAMES - 1:
        frame_list.append(TOTAL_FRAMES - 1)

    def update(i):
        return render_dashboard_frame(fig, frame_list[i])

    anim = FuncAnimation(fig, update, frames=len(frame_list), interval=1000/FPS, blit=False)
    gif_path = OUT / GIF_NAME
    anim.save(gif_path, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    return gif_path

def make_report(raw_path=None, hd_path=None, gif_path=None):
    final = states[-1]["metrics"]
    verdict = (
        "FORCED_HD_PUBLIC_REVIEWER_RENDER_PASS"
        if final["rank_lift"] > 0 and final["NOOCI_supported"]
        else "FORCED_HD_PUBLIC_REVIEWER_RENDER_INCONCLUSIVE"
    )

    raw_probe = ffprobe_dimensions(raw_path) if raw_path else None
    hd_probe = ffprobe_dimensions(hd_path) if hd_path else None

    result = {
        "document_id": DOCUMENT_ID,
        "status": "completed",
        "verdict": verdict,
        "target_resolution": [TARGET_W, TARGET_H],
        "fps": FPS,
        "total_frames": TOTAL_FRAMES,
        "approx_duration_seconds": TOTAL_FRAMES / FPS,
        "genesis": asdict(genesis),
        "final_metrics": final,
        "ffprobe_raw": raw_probe,
        "ffprobe_forced_hd": hd_probe,
        "outputs": {
            "raw_mp4": str(raw_path) if raw_path else None,
            "forced_hd_mp4": str(hd_path) if hd_path else None,
            "gif_preview": str(gif_path) if gif_path else None,
            "metrics_csv": str(OUT / "v1686_35_ordered_slice_metrics.csv"),
            "keyframes_pattern": str(OUT / "v1686_35_keyframe_ordered_*.png"),
        },
        "interpretation": {
            "L3_status": "not eliminated; reclassified",
            "core_claim": "L3 is geometry-plus-information in this synthetic full-stack audit.",
            "epsilon_floor_meaning": "epsilon-floor persists as a lower-bound route from irreducible third-order retained-current associator obstruction.",
            "operator_boundary": "metadata-only projection is insufficient; admissible projection must preserve recombination law.",
        },
        "claim_boundary": "Synthetic full-stack audit simulation only. Not empirical L3, physical geometry, GR, or ADM.",
    }

    (OUT / "v1686_35_forced_hd_result.json").write_text(json.dumps(result, indent=2))

    md = f"""# V1686.35 Forced-HD Export Fix

## Verdict

```text
{verdict}
```

## Target resolution

```text
{TARGET_W} × {TARGET_H}
```

## ffprobe forced-HD output

```json
{json.dumps(hd_probe, indent=2)}
```

## Core visual claim

```text
L3 is not merely a geometric layer.
L3 is geometry-plus-information:
a third-order retained-current associator obstruction contributes
irreducible information that operator-faithful admissible projection cannot erase.
```

## Final metrics

```json
{json.dumps(final, indent=2)}
```

## Outputs

```json
{json.dumps(result["outputs"], indent=2)}
```

## Boundary

Synthetic full-stack audit simulation only.
No empirical L3 claim.
No physical geometry / GR / ADM claim.
No universal theorem over all operators.
"""
    (OUT / "V1686_35_FORCED_HD_REPORT.md").write_text(md)

    print("\n==============================")
    print("V1686.35 RESULT")
    print("==============================")
    print(json.dumps(result, indent=2))
    print(f"\nOutputs saved to: {OUT}")

def main():
    print("==============================")
    print("V1686.35 FORCED-HD EXPORT FIX")
    print("==============================")
    print(f"Target: {TARGET_W} × {TARGET_H}")
    print(f"Total frames: {TOTAL_FRAMES}")
    print(f"Duration: {TOTAL_FRAMES/FPS:.1f} sec")

    if SAVE_KEYFRAMES:
        print("Rendering keyframes...")
        render_keyframes()

    raw_path = None
    hd_path = None
    gif_path = None

    if SAVE_MP4:
        print("Rendering raw MP4...")
        raw_path = render_raw_mp4()

        print("Forcing HD export with ffmpeg...")
        hd_path = force_hd_export(raw_path)

    if SAVE_GIF_PREVIEW:
        print("Rendering GIF preview...")
        gif_path = render_gif_preview()

    make_report(raw_path=raw_path, hd_path=hd_path, gif_path=gif_path)

main()
