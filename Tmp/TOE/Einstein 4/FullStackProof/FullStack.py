#!/usr/bin/env python3
"""
V996 Genesis Pin Visual Proof Simulation

This script creates a visual simulation and animation showing why the
Genesis Pin is necessary in the V923 -> V995 recoverability stack.

Core demonstrated claim:
    Same observable state does NOT imply legitimate history.

Three histories are engineered to converge to the same visible state:
    1. Legitimate path: rooted in pinned genesis registry + pinned anchor root.
    2. Forked counterfeit: same registry, wrong genesis root.
    3. Self-defined counterfeit: attacker-defined registry and root.

Without Genesis Pin:
    all three are accepted because the final observable state matches.

With Genesis Pin:
    only the legitimate path is accepted because the history chains back to
    the pinned genesis registry and pinned anchor root.

Outputs:
    v996_genesis_pin_outputs/v996_genesis_pin_visual_proof.mp4
    v996_genesis_pin_outputs/v996_genesis_pin_visual_proof.gif
    v996_genesis_pin_outputs/v996_genesis_pin_final_frame.png
    v996_genesis_pin_outputs/v996_genesis_pin_results.csv
    v996_genesis_pin_outputs/v996_genesis_pin_result.json

Requirements:
    pip install numpy pandas matplotlib
    ffmpeg is required for mp4 output.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.patches import Circle, FancyBboxPatch


OUT = Path("v996_genesis_pin_outputs")
OUT.mkdir(exist_ok=True)

N_STEPS = 8
FPS = 1.2

PINNED_GENESIS_REGISTRY = "REGISTRY:W1,W2,W3,W4"
PINNED_GENESIS_ROOT = "ROOT:GENESIS_ANCHOR_000"
COMMON_VISIBLE_STATE = np.array([0.0, 0.0])


def short_hash(*parts: object, n: int = 12) -> str:
    msg = "|".join(map(str, parts)).encode("utf-8")
    return hashlib.sha256(msg).hexdigest()[:n]


def signed_transition(prev_root: str, registry: str, step: int, event: str) -> str:
    return short_hash("transition", prev_root, registry, step, event)


@dataclass
class HistoryPath:
    name: str
    color: str
    genesis_registry: str
    genesis_root: str
    events: List[str]
    points: np.ndarray
    roots: List[str]
    final_observable: Tuple[float, float]
    visible_accept_without_pin: bool
    accept_with_pin: bool
    rejection_reason: str


def build_path(name: str, color: str, genesis_registry: str, genesis_root: str,
               events: List[str], start: Tuple[float, float], arc_height: float) -> HistoryPath:
    t = np.linspace(0, 1, N_STEPS)
    start = np.array(start, dtype=float)

    # Different histories converge to the same final observable state.
    x = (1 - t) * start[0] + t * COMMON_VISIBLE_STATE[0]
    y = (1 - t) * start[1] + t * COMMON_VISIBLE_STATE[1] + arc_height * t * (1 - t)
    pts = np.column_stack([x, y])

    roots = [genesis_root]
    current = genesis_root
    for i, ev in enumerate(events, start=1):
        current = signed_transition(current, genesis_registry, i, ev)
        roots.append(current)

    visible_accept_without_pin = bool(np.allclose(pts[-1], COMMON_VISIBLE_STATE))

    accept_with_pin = (
        genesis_registry == PINNED_GENESIS_REGISTRY
        and genesis_root == PINNED_GENESIS_ROOT
        and visible_accept_without_pin
    )

    if accept_with_pin:
        reason = "accepted: pinned genesis registry + pinned anchor root"
    elif genesis_registry != PINNED_GENESIS_REGISTRY and genesis_root != PINNED_GENESIS_ROOT:
        reason = "rejected: self-defined registry and self-defined root"
    elif genesis_root != PINNED_GENESIS_ROOT:
        reason = "rejected: wrong genesis anchor root"
    elif genesis_registry != PINNED_GENESIS_REGISTRY:
        reason = "rejected: wrong witness registry"
    else:
        reason = "rejected: failed visible-state check"

    return HistoryPath(
        name=name,
        color=color,
        genesis_registry=genesis_registry,
        genesis_root=genesis_root,
        events=events,
        points=pts,
        roots=roots,
        final_observable=tuple(pts[-1]),
        visible_accept_without_pin=visible_accept_without_pin,
        accept_with_pin=accept_with_pin,
        rejection_reason=reason,
    )


def build_histories() -> List[HistoryPath]:
    return [
        build_path(
            name="Legitimate history",
            color="#2ca25f",
            genesis_registry=PINNED_GENESIS_REGISTRY,
            genesis_root=PINNED_GENESIS_ROOT,
            events=["observe", "emit_symbol", "fresh_nonce", "append_ledger", "witness_root", "registry_ok", "anchor_update"],
            start=(-4.0, 2.7),
            arc_height=1.0,
        ),
        build_path(
            name="Forked counterfeit",
            color="#de2d26",
            genesis_registry=PINNED_GENESIS_REGISTRY,
            genesis_root="ROOT:FORKED_ANCHOR_999",
            events=["observe", "emit_symbol", "fresh_nonce", "append_ledger", "witness_root", "registry_ok", "forked_anchor"],
            start=(-4.0, -2.3),
            arc_height=-1.0,
        ),
        build_path(
            name="Self-defined counterfeit",
            color="#fdae6b",
            genesis_registry="REGISTRY:ATTACKER_A,ATTACKER_B,ATTACKER_C",
            genesis_root="ROOT:SELF_DEFINED_123",
            events=["observe", "emit_symbol", "fresh_nonce", "append_ledger", "fake_witness", "fake_registry", "self_anchor"],
            start=(4.0, 0.2),
            arc_height=1.7,
        ),
    ]


def make_results(histories: List[HistoryPath]) -> pd.DataFrame:
    rows = []
    for h in histories:
        rows.append({
            "history": h.name,
            "final_x": h.final_observable[0],
            "final_y": h.final_observable[1],
            "same_visible_state": h.visible_accept_without_pin,
            "genesis_registry_matches": h.genesis_registry == PINNED_GENESIS_REGISTRY,
            "genesis_root_matches": h.genesis_root == PINNED_GENESIS_ROOT,
            "accepted_without_genesis_pin": h.visible_accept_without_pin,
            "accepted_with_genesis_pin": h.accept_with_pin,
            "reason": h.rejection_reason,
        })
    return pd.DataFrame(rows)


def draw_box(ax, xy, w, h, text, fc="#f7f7f7", ec="#333333", fontsize=10, weight="normal"):
    box = FancyBboxPatch(
        xy, w, h,
        boxstyle="round,pad=0.03,rounding_size=0.04",
        facecolor=fc, edgecolor=ec, linewidth=1.2,
        transform=ax.transAxes
    )
    ax.add_patch(box)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, transform=ax.transAxes,
            ha="center", va="center", fontsize=fontsize, fontweight=weight)


def setup_axes(ax):
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-4, 4)
    ax.grid(True, alpha=0.25, linestyle='--')
    ax.set_xlabel("Observable coordinate 1", fontsize=11)
    ax.set_ylabel("Observable coordinate 2", fontsize=11)


def draw_frame(fig, histories: List[HistoryPath], frame: int, results: pd.DataFrame):
    fig.clear()
    
    # Updated GridSpec layout proportions
    gs = fig.add_gridspec(2, 2, height_ratios=[1.8, 1], width_ratios=[1.3, 1.0])

    ax = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    setup_axes(ax)
    ax.set_title("Genesis Pin Visual Proof\nSame observable state can arise from incompatible histories.", fontsize=14, fontweight='bold', pad=15)

    # Re-centered and sized observable state circle
    ax.add_patch(Circle(COMMON_VISIBLE_STATE, 0.5, facecolor="#9ecae1", edgecolor="#08519c", alpha=0.6, zorder=2))
    ax.text(0, -0.7, "same visible\nstate", ha="center", va="top", fontsize=10, color="#08306b", fontweight='bold')

    k = min(frame, N_STEPS - 1)

    for h in histories:
        pts = h.points
        ax.plot(pts[:k+1, 0], pts[:k+1, 1], color=h.color, linewidth=3.5, alpha=0.85, zorder=3)
        ax.scatter(pts[k, 0], pts[k, 1], color=h.color, s=150, edgecolor="white", linewidth=1.5, zorder=5)
        
        # Dynamic padding for the history labels so they do not overlap
        if "Legitimate" in h.name:
            txt_pos = (pts[0, 0] - 0.2, pts[0, 1] + 0.4)
        elif "Forked" in h.name:
            txt_pos = (pts[0, 0] - 0.2, pts[0, 1] - 0.6)
        else:
            txt_pos = (pts[0, 0] + 0.2, pts[0, 1] + 0.4)
        ax.text(txt_pos[0], txt_pos[1], h.name, color=h.color, fontsize=11, fontweight='bold', ha="center", zorder=6)

    # Only draw the results indicators once the lines hit the state node
    if frame >= N_STEPS:
        for h in histories:
            symbol = "ACCEPT" if h.accept_with_pin else "REJECT"
            yoff = {"Legitimate history": 1.2, "Forked counterfeit": -1.2, "Self-defined counterfeit": 0}[h.name]
            ax.text(1.5, yoff, symbol, color=h.color, fontsize=12, fontweight="bold", va='center')
            ax.plot([0.5, 1.2], [0, yoff], color=h.color, alpha=0.5, linestyle=':', linewidth=2)

    # Plot 2: Genesis Pin Checkboxes
    ax2.axis("off")
    ax2.text(0.5, 1.05, "Genesis Pin Check", transform=ax2.transAxes, ha="center", fontsize=16, fontweight="bold")
    ax2.text(0.5, 0.95, "Minimal non-circular initialization boundary", transform=ax2.transAxes, ha="center", fontsize=11)

    draw_box(ax2, (0.05, 0.70), 0.9, 0.18, "Pinned Genesis Registry\nREGISTRY: W1,W2,W3,W4", fc="#edf8e9", ec="#238b45", fontsize=11, weight="bold")
    draw_box(ax2, (0.05, 0.48), 0.9, 0.18, "Pinned Genesis Anchor Root\nROOT: GENESIS_ANCHOR_000", fc="#eff3ff", ec="#3182bd", fontsize=11, weight="bold")
    draw_box(ax2, (0.05, 0.26), 0.9, 0.16, "Without Genesis Pin:\ncheck only final visible state", fc="#fee0d2", ec="#de2d26", fontsize=11)
    draw_box(ax2, (0.05, 0.05), 0.9, 0.16, "With Genesis Pin:\ncheck final state + rooted history", fc="#e5f5e0", ec="#31a354", fontsize=11)

    # Plot 3: Certification Outcomes Table
    ax3.axis("off")
    ax3.text(0.02, 0.9, "Certification Outcomes", transform=ax3.transAxes, fontsize=14, fontweight="bold")

    x_cols = [0.02, 0.35, 0.55, 0.75, 0.90]
    headers = ["History", "Same Visible State?", "Genesis Root Matches?", "Registry Matches?", "With Pin"]
    for x, head in zip(x_cols, headers):
        ax3.text(x, 0.75, head, transform=ax3.transAxes, fontsize=11, fontweight="bold", ha='left')

    y0 = 0.50
    colors_map = {"Legitimate history": "#2ca25f", "Forked counterfeit": "#de2d26", "Self-defined counterfeit": "#fdae6b"}

    for i, row in results.iterrows():
        y = y0 - i * 0.25
        c = colors_map.get(row['history'], "black")
        
        ax3.text(x_cols[0], y, row['history'], transform=ax3.transAxes, fontsize=11, color=c, fontweight="bold", ha='left')
        ax3.text(x_cols[1], y, "YES" if row['same_visible_state'] else "NO", transform=ax3.transAxes, fontsize=11, ha='left')
        ax3.text(x_cols[2], y, "YES" if row['genesis_root_matches'] else "NO", transform=ax3.transAxes, fontsize=11, ha='left')
        ax3.text(x_cols[3], y, "YES" if row['genesis_registry_matches'] else "NO", transform=ax3.transAxes, fontsize=11, ha='left')
        
        accept = row['accepted_with_genesis_pin']
        ax3.text(x_cols[4], y, "ACCEPT" if accept else "REJECT", transform=ax3.transAxes, fontsize=11, color="#238b45" if accept else "#de2d26", fontweight="bold", ha='left')

    bottom_text = "Proof idea: visible-state equivalence accepts all paths. A Genesis Pin adds a pinned registry and anchor root, separating legitimate continuity from forked or self-defined histories."
    ax3.text(0.5, -0.1, bottom_text, transform=ax3.transAxes, ha='center', fontsize=11, bbox=dict(boxstyle="round,pad=0.5", facecolor="#f7f7f7", edgecolor="#999999"))

    fig.subplots_adjust(hspace=0.4, wspace=0.1)


def main():
    histories = build_histories()
    results = make_results(histories)
    results.to_csv(OUT / "v996_genesis_pin_results.csv", index=False)

    result_json = {
        "verdict": "genesis_pin_visual_proof_complete",
        "claim_demonstrated": "Same observable state does not imply legitimate history.",
        "accepted_without_genesis_pin": int(results["accepted_without_genesis_pin"].sum()),
        "accepted_with_genesis_pin": int(results["accepted_with_genesis_pin"].sum()),
        "minimal_genesis_pin": {
            "pinned_genesis_registry": PINNED_GENESIS_REGISTRY,
            "pinned_genesis_anchor_root": PINNED_GENESIS_ROOT,
        },
        "interpretation": (
            "Without pinned genesis, all histories landing on the same visible state are accepted. "
            "With pinned genesis, only histories rooted in the pinned registry and pinned anchor root are accepted."
        ),
    }
    (OUT / "v996_genesis_pin_result.json").write_text(json.dumps(result_json, indent=2))

    # Increased figure size and DPI for proper layout dimensions
    fig = plt.figure(figsize=(14, 9), dpi=150)
    total_frames = N_STEPS + 4

    def update(frame):
        draw_frame(fig, histories, frame, results)
        return []

    anim = FuncAnimation(fig, update, frames=total_frames, interval=1000 / FPS, blit=False)

    mp4_path = OUT / "v996_genesis_pin_visual_proof.mp4"
    gif_path = OUT / "v996_genesis_pin_visual_proof.gif"
    png_path = OUT / "v996_genesis_pin_final_frame.png"

    try:
        writer = FFMpegWriter(fps=FPS, bitrate=2200)
        anim.save(mp4_path, writer=writer)
        print(f"Saved MP4: {mp4_path}")
    except Exception as e:
        print("MP4 save failed, likely ffmpeg missing:", e)

    try:
        gif_writer = PillowWriter(fps=FPS)
        anim.save(gif_path, writer=gif_writer)
        print(f"Saved GIF: {gif_path}")
    except Exception as e:
        print("GIF save failed:", e)

    draw_frame(fig, histories, total_frames - 1, results)
    fig.savefig(png_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(json.dumps(result_json, indent=2))
    print(f"Saved final frame: {png_path}")
    print(f"Saved results: {OUT / 'v996_genesis_pin_results.csv'}")


if __name__ == "__main__":
    main()
