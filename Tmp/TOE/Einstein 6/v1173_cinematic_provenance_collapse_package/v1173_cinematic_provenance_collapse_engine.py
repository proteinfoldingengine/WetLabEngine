#!/usr/bin/env python3
"""
V1173 — Cinematic Provenance Collapse Engine

Goal:
    Make the full-stack mechanism visually obvious.

This version shows three synchronized panels:

LEFT:
    6D winner field projected into a 2D/3D geometry surface.

CENTER:
    living provenance network.
    Nodes are history families.
    Edges are retained-flow channels.
    Legitimate provenance glows and stabilizes.
    Counterfeit branches visibly collapse when Genesis / Ω / closure fails.

RIGHT:
    Genesis Pin + certification ledger.
    Events light up in order:
        Genesis -> Source ID -> Sequence -> Transport -> Geometry -> Flow -> Closure

Scientific stack:
    - 6D GPU pruning
    - source-origin identity
    - retained-sequence coherence
    - Genesis Pin / append-only ledger
    - Ω similarity
    - source-flow closure
    - earned dimensionless margin
    - adversarial controls

Colab:
    Works in one cell. If using Colab, run:
        !python v1173_cinematic_provenance_collapse_engine.py --animate

Fast metrics only:
        python v1173_cinematic_provenance_collapse_engine.py

Smoke test:
        set N_HISTORIES = 512

Full demo:
        N_HISTORIES = 2048
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List, Dict, Any

import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from tqdm import tqdm

# ==============================================================================
# CONFIG
# ==============================================================================
OUT = Path("v1173_cinematic_provenance_collapse_engine_outputs")
OUT.mkdir(exist_ok=True)

SEED = 11730
N_UPDATES = 120
N_HISTORIES = 2048
RES = 8
VIS_RES = 160
EPS = 1e-9

BETA = 2.3
DIFFUSION = 0.07
RELAX = 0.09
NOISE = 0.0025

OMEGA_SIM_THRESHOLD = 0.985
QUORUM = 3

PINNED_GENESIS_REGISTRY = ("W1", "W2", "W3", "W4")
PINNED_GENESIS_ROOT = "ROOT:GENESIS_ANCHOR_000"

MODES = [
    "valid_label_transported",
    "raw_c_only_shift",
    "retained_order_shuffle",
    "source_event_shuffle",
    "geometry_matched_counterfeit",
    "genesis_valid_source_shuffled",
]
VALID_MODES = {"valid_label_transported"}

EVENTS = [
    "Genesis",
    "Source ID",
    "Sequence",
    "Transport",
    "Geometry",
    "Flow",
    "Closure",
]

MODE_LABELS = {
    "valid_label_transported": "VALID",
    "raw_c_only_shift": "RAW SHIFT",
    "retained_order_shuffle": "ORDER SHUFFLE",
    "source_event_shuffle": "SOURCE SHUFFLE",
    "geometry_matched_counterfeit": "GEOMETRY FAKE",
    "genesis_valid_source_shuffled": "GENESIS+SOURCE FAKE",
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==============================================================================
# GENESIS PIN / APPEND-ONLY LEDGER
# ==============================================================================
def short_hash(*parts: object, n: int = 12) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()[:n]

def chain_transition(prev_root: str, registry: Tuple[str, ...], ordered_slice: int, event: str, witnesses: Tuple[str, ...]) -> str:
    return short_hash("transition", prev_root, ",".join(registry), ordered_slice, event, ",".join(witnesses))

def registry_matches(registry: Tuple[str, ...]) -> bool:
    return tuple(registry) == tuple(PINNED_GENESIS_REGISTRY)

def root_matches(root: str) -> bool:
    return root == PINNED_GENESIS_ROOT

def quorum_valid(witnesses: Tuple[str, ...]) -> bool:
    return len(set(witnesses).intersection(PINNED_GENESIS_REGISTRY)) >= QUORUM

def circular_bootstrap_detected(registry: Tuple[str, ...], root: str) -> bool:
    return (not registry_matches(registry)) or (not root_matches(root))

def build_chain(root: str, registry: Tuple[str, ...], events: List[str], witnesses: List[Tuple[str, ...]], tamper_at: int | None = None) -> List[str]:
    roots = [root]
    cur = root
    for i, (ev, wit) in enumerate(zip(events, witnesses), start=1):
        cur = chain_transition(cur, registry, i, ev, wit)
        roots.append(cur)
    if tamper_at is not None and 0 < tamper_at < len(roots):
        roots[tamper_at] = "TAMPERED_" + roots[tamper_at]
    return roots

def append_chain_valid_partial(root: str, registry: Tuple[str, ...], events: List[str], witnesses: List[Tuple[str, ...]], roots: List[str], k_event: int) -> bool:
    if len(roots) <= k_event or roots[0] != root:
        return False
    cur = root
    for i in range(1, k_event + 1):
        cur = chain_transition(cur, registry, i, events[i - 1], witnesses[i - 1])
        if roots[i] != cur:
            return False
    return True

def genesis_pin_passes_partial(registry: Tuple[str, ...], root: str, events: List[str], witnesses: List[Tuple[str, ...]], roots: List[str], k_event: int) -> bool:
    return (
        registry_matches(registry)
        and root_matches(root)
        and all(quorum_valid(witnesses[i]) for i in range(k_event))
        and append_chain_valid_partial(root, registry, events, witnesses, roots, k_event)
        and not circular_bootstrap_detected(registry, root)
    )

@dataclass
class HistoryLedger:
    mode: str
    registry: Tuple[str, ...]
    root: str
    events: List[str]
    witnesses: List[Tuple[str, ...]]
    roots: List[str]

def make_ledger(mode: str) -> HistoryLedger:
    events = [
        "genesis_source_key",
        "source_origin_identity",
        "retained_sequence_identity",
        "label_transport",
        "geometry_commit",
        "source_flow_commit",
        "closure_commit",
    ]
    pinned_witnesses = [("W1", "W2", "W3") for _ in events]
    attacker_witnesses = [("A1", "A2", "A3") for _ in events]

    registry = PINNED_GENESIS_REGISTRY
    root = PINNED_GENESIS_ROOT
    witnesses = pinned_witnesses

    if mode in {"raw_c_only_shift", "geometry_matched_counterfeit"}:
        registry = ("A1", "A2", "A3", "A4")
        root = "ROOT:SELF_DEFINED_OR_COUNTERFEIT"
        witnesses = attacker_witnesses
    elif mode == "retained_order_shuffle":
        events = list(reversed(events))

    roots = build_chain(root, registry, events, witnesses)
    return HistoryLedger(mode, registry, root, events, witnesses, roots)

# ==============================================================================
# 6D GPU PRUNING
# ==============================================================================
def normalize_batch(f: torch.Tensor) -> torch.Tensor:
    dims = tuple(range(1, f.ndim))
    return (f - f.mean(dim=dims, keepdim=True)) / (f.std(dim=dims, keepdim=True) + EPS)

def normalize_single(f: torch.Tensor) -> torch.Tensor:
    return (f - f.mean()) / (f.std() + EPS)

def laplacian_nd(f: torch.Tensor) -> torch.Tensor:
    lap = torch.zeros_like(f)
    start_axis = 1 if f.ndim == 7 else 0
    for ax in range(start_axis, f.ndim):
        lap += torch.roll(f, 1, ax) + torch.roll(f, -1, ax) - 2 * f
    return lap

def local_divergence_batch(fields: torch.Tensor, ensemble: torch.Tensor) -> torch.Tensor:
    dims = tuple(range(1, fields.ndim))
    p = torch.exp(-fields**2) + EPS
    p = p / p.sum(dim=dims, keepdim=True)
    q = torch.exp(-ensemble**2) + EPS
    q = q / q.sum()
    return (p * torch.log((p + EPS) / (q.unsqueeze(0) + EPS))).sum(dim=dims)

def cosine_batch_to_single(fields: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    f_flat = fields.reshape(fields.shape[0], -1)
    t_flat = target.reshape(-1)
    return torch.matmul(f_flat, t_flat) / (torch.norm(f_flat, dim=1) * torch.norm(t_flat) + EPS)

def build_genesis(res: int = RES) -> torch.Tensor:
    grid = torch.meshgrid([torch.arange(res, dtype=torch.float32, device=device) for _ in range(6)], indexing="ij")
    genesis = (
        0.55 * torch.sin(0.30 * grid[0])
        + 0.35 * torch.cos(0.37 * grid[1])
        + 0.25 * torch.sin(0.41 * grid[2] + 0.2 * grid[3])
        + 0.15 * torch.cos(0.29 * grid[4] - 0.31 * grid[5])
    )
    return normalize_single(genesis)

def apply_mode_transform(fields: torch.Tensor, mode: str, genesis: torch.Tensor) -> torch.Tensor:
    if mode == "valid_label_transported":
        return fields

    f = fields.clone()
    if mode == "raw_c_only_shift":
        f = torch.roll(f, shifts=1, dims=2)
    elif mode == "retained_order_shuffle":
        f = torch.flip(f, dims=[3])
    elif mode == "source_event_shuffle":
        f = normalize_batch(torch.roll(f, shifts=2, dims=4))
    elif mode == "geometry_matched_counterfeit":
        f = normalize_batch(0.92 * fields + 0.08 * genesis.unsqueeze(0))
    elif mode == "genesis_valid_source_shuffled":
        f = normalize_batch(torch.roll(fields, shifts=3, dims=5))
    else:
        raise ValueError(mode)
    return f

def source_flow_closure_metrics(field: torch.Tensor, genesis: torch.Tensor) -> Dict[str, float]:
    f = field.detach()
    g = genesis.detach()
    lap_f = laplacian_nd(f)
    lap_g = laplacian_nd(g)
    source_alignment = float(torch.sum(f * g) / (torch.norm(f) * torch.norm(g) + EPS))
    flow_alignment = float(torch.sum(lap_f * lap_g) / (torch.norm(lap_f) * torch.norm(lap_g) + EPS))
    residual = float(torch.sqrt(torch.mean((normalize_single(f) - normalize_single(g)) ** 2)))
    return {"B_like_rms": residual, "source_alignment": source_alignment, "flow_alignment": flow_alignment}

def calibrate_closure_thresholds(genesis: torch.Tensor, n_samples: int = 32) -> Dict[str, float]:
    vals = []
    gen = torch.Generator(device=device)
    gen.manual_seed(SEED + 77)
    for _ in range(n_samples):
        noisy = normalize_single(genesis + 0.035 * torch.randn(genesis.shape, device=device, generator=gen))
        vals.append(source_flow_closure_metrics(noisy, genesis))
    residuals = np.array([v["B_like_rms"] for v in vals])
    src = np.array([v["source_alignment"] for v in vals])
    flow = np.array([v["flow_alignment"] for v in vals])
    return {
        "B_like_threshold": float(residuals.mean() + 3.0 * (residuals.std() + EPS)),
        "source_alignment_min": float(src.mean() - 3.0 * (src.std() + EPS)),
        "flow_alignment_min": float(flow.mean() - 3.0 * (flow.std() + EPS)),
        "B_like_mean": float(residuals.mean()),
        "source_alignment_mean": float(src.mean()),
        "flow_alignment_mean": float(flow.mean()),
    }

def project_6d_to_2d(field: torch.Tensor, vis_res: int = VIS_RES) -> np.ndarray:
    field_cpu = field.detach().float().cpu().numpy()
    s = RES // 2
    slice2 = field_cpu[s, s, :, :, s, s]
    scale = max(1, vis_res // RES)
    up = np.repeat(np.repeat(slice2, scale, axis=0), scale, axis=1)
    if up.shape[0] != vis_res:
        tmp = np.zeros((vis_res, vis_res))
        m = min(vis_res, up.shape[0])
        tmp[:m, :m] = up[:m, :m]
        up = tmp
    return up

def certify_field(mode: str, winner: torch.Tensor, genesis: torch.Tensor, ledger: HistoryLedger, thresholds: Dict[str, float]) -> Dict[str, Any]:
    omega_w = torch.exp(-winner**2)
    omega_g = torch.exp(-genesis**2)
    omega_sim = float(torch.sum(omega_w * omega_g) / (torch.norm(omega_w) * torch.norm(omega_g) + EPS))
    omega_certified = omega_sim >= OMEGA_SIM_THRESHOLD

    genesis_pin = genesis_pin_passes_partial(ledger.registry, ledger.root, ledger.events, ledger.witnesses, ledger.roots, len(ledger.events))
    cm = source_flow_closure_metrics(winner, genesis)
    residual_certified = cm["B_like_rms"] <= thresholds["B_like_threshold"]
    source_certified = cm["source_alignment"] >= thresholds["source_alignment_min"]
    flow_certified = cm["flow_alignment"] >= thresholds["flow_alignment_min"]
    closure_certified = residual_certified and source_certified and flow_certified

    omega_margin = (omega_sim - OMEGA_SIM_THRESHOLD) / max(1.0 - OMEGA_SIM_THRESHOLD, EPS)
    genesis_margin = 1.0 if genesis_pin else -1.0
    closure_margin = min(
        (thresholds["B_like_threshold"] - cm["B_like_rms"]) / (thresholds["B_like_threshold"] + EPS),
        (cm["source_alignment"] - thresholds["source_alignment_min"]) / (abs(thresholds["source_alignment_min"]) + EPS),
        (cm["flow_alignment"] - thresholds["flow_alignment_min"]) / (abs(thresholds["flow_alignment_min"]) + EPS),
    )
    dimensionless_margin = float(np.mean([omega_margin, genesis_margin, closure_margin]))

    return {
        "mode": mode,
        "omega_similarity": omega_sim,
        "omega_certified": bool(omega_certified),
        "genesis_pin_pass": bool(genesis_pin),
        **cm,
        "residual_certified": bool(residual_certified),
        "source_alignment_certified": bool(source_certified),
        "flow_alignment_certified": bool(flow_certified),
        "closure_certified": bool(closure_certified),
        "full_certified": bool(omega_certified and genesis_pin and closure_certified),
        "omega_margin": float(omega_margin),
        "genesis_margin": float(genesis_margin),
        "closure_margin": float(closure_margin),
        "dimensionless_margin": float(dimensionless_margin),
        "registry_matches": registry_matches(ledger.registry),
        "root_matches": root_matches(ledger.root),
        "quorum_valid": all(quorum_valid(w) for w in ledger.witnesses),
        "append_valid": append_chain_valid_partial(ledger.root, ledger.registry, ledger.events, ledger.witnesses, ledger.roots, len(ledger.events)),
        "circular_bootstrap_detected": circular_bootstrap_detected(ledger.registry, ledger.root),
    }

def run_pruning_for_mode(mode: str, animate_store: bool = False) -> Dict[str, Any]:
    torch.manual_seed(SEED)
    shape = (RES,) * 6
    genesis = build_genesis(RES)
    thresholds = calibrate_closure_thresholds(genesis, n_samples=32)
    ledger = make_ledger(mode)

    fields = torch.empty((N_HISTORIES, *shape), dtype=torch.float32, device=device)
    fields[0] = genesis.clone()
    fields[1:] = normalize_batch(torch.randn((N_HISTORIES - 1, *shape), device=device) * 1.8)
    fields = apply_mode_transform(fields, mode, genesis)
    prev_fields = fields.clone()

    log_weights = torch.full((N_HISTORIES,), -np.log(N_HISTORIES), dtype=torch.float32, device=device)
    log_rows = []
    slices = []
    network_frames = []

    for step in tqdm(range(N_UPDATES), desc=f"{mode}", leave=False):
        weights = torch.softmax(log_weights, dim=0)
        ensemble = torch.einsum("n,n...->...", weights, fields)

        divergences = local_divergence_batch(fields, ensemble)
        source_scores = cosine_batch_to_single(fields, genesis)

        if step == 0:
            sequence_scores = torch.zeros(N_HISTORIES, device=device)
        else:
            df = fields - prev_fields
            de = ensemble.unsqueeze(0) - prev_fields
            df_flat = df.reshape(N_HISTORIES, -1)
            de_flat = de.reshape(N_HISTORIES, -1)
            sequence_scores = torch.sum(df_flat * de_flat, dim=1) / (torch.norm(df_flat, dim=1) * torch.norm(de_flat, dim=1) + EPS)

        prev_fields = fields.clone()

        action = divergences - 0.55 * source_scores - 0.35 * sequence_scores
        action = (action - action.mean()) / (action.std() + EPS)

        lap = laplacian_nd(fields)
        target = normalize_batch(fields + RELAX * (ensemble.unsqueeze(0) - fields))
        fields = normalize_batch(fields + RELAX * (target - fields) + DIFFUSION * lap + NOISE * torch.randn_like(fields))
        log_weights += -BETA * action

        weights = torch.softmax(log_weights, dim=0)
        winner_idx = int(torch.argmax(weights).detach().cpu())
        legit_prob = float(weights[0].detach().cpu())
        winner_prob = float(weights[winner_idx].detach().cpu())
        entropy = float((-torch.sum(weights * torch.log(weights + EPS))).detach().cpu())

        if animate_store and step % 2 == 0:
            topk = torch.topk(weights, k=min(24, N_HISTORIES))
            network_frames.append({
                "step": step,
                "top_indices": topk.indices.detach().cpu().numpy().tolist(),
                "top_weights": topk.values.detach().cpu().numpy().tolist(),
                "legit_prob": legit_prob,
                "winner_prob": winner_prob,
                "entropy": entropy,
            })
            slices.append(project_6d_to_2d(fields[winner_idx], VIS_RES))

        log_rows.append({
            "mode": mode,
            "step": step,
            "legit_prob": legit_prob,
            "winner_idx": winner_idx,
            "winner_prob": winner_prob,
            "entropy": entropy,
            "mean_divergence": float(divergences.mean().detach().cpu()),
            "mean_source_identity": float(source_scores.mean().detach().cpu()),
            "mean_sequence_identity": float(sequence_scores.mean().detach().cpu()),
        })

    final_weights = torch.softmax(log_weights, dim=0)
    winner_idx = int(torch.argmax(final_weights).detach().cpu())
    winner = fields[winner_idx].detach()
    cert = certify_field(mode, winner, genesis, ledger, thresholds)
    cert.update({
        "winner_idx": winner_idx,
        "winner_probability": float(final_weights[winner_idx].detach().cpu()),
        "legitimate_probability": float(final_weights[0].detach().cpu()),
        "final_entropy": float((-torch.sum(final_weights * torch.log(final_weights + EPS))).detach().cpu()),
        "emergent_curvature_proxy": float(torch.mean(laplacian_nd(winner) ** 2).detach().cpu()),
    })

    return {"mode": mode, "cert": cert, "log": log_rows, "slices": slices, "network_frames": network_frames}

# ==============================================================================
# VISUALS
# ==============================================================================
def plot_certification(results: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    x = np.arange(len(results))
    labels = results["mode"].tolist()
    panels = [
        ("omega_similarity", "Ω similarity", OMEGA_SIM_THRESHOLD),
        ("source_alignment", "source alignment", None),
        ("closure_margin", "closure margin", 0),
        ("dimensionless_margin", "dimensionless provenance margin", 0),
    ]
    for ax, (col, title, line) in zip(axes.ravel(), panels):
        ax.bar(x, results[col].astype(float))
        if line is not None:
            ax.axhline(line, ls="--", color="red", alpha=0.65)
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=35, ha="right")
        ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUT / "v1173_certification_panels.png", dpi=160)
    plt.close(fig)

def make_cinematic(valid_slices: List[np.ndarray], network_frames: List[Dict[str, Any]], results: pd.DataFrame, logs: pd.DataFrame):
    if not valid_slices or not network_frames:
        return None

    fig = plt.figure(figsize=(20, 11))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 1.25, 0.9], height_ratios=[1, 1])
    ax_geom = fig.add_subplot(gs[:, 0], projection="3d")
    ax_net = fig.add_subplot(gs[:, 1])
    ax_ledger = fig.add_subplot(gs[0, 2])
    ax_tel = fig.add_subplot(gs[1, 2])

    X, Y = np.meshgrid(np.arange(VIS_RES), np.arange(VIS_RES))
    valid_log = logs[logs["mode"] == "valid_label_transported"].copy()
    theta = np.linspace(0, 2*np.pi, 24, endpoint=False)
    node_xy = np.column_stack([np.cos(theta), np.sin(theta)])

    def update(frame):
        ax_geom.clear(); ax_net.clear(); ax_ledger.clear(); ax_tel.clear()

        idx = min(frame, len(valid_slices) - 1)
        height = valid_slices[idx]
        nf = network_frames[idx]

        # LEFT: geometry
        ax_geom.plot_surface(X, Y, height, cmap="plasma", alpha=0.92, linewidth=0, rstride=4, cstride=4)
        ax_geom.set_title("6D Winner Field → Projected Geometry")
        ax_geom.set_zlim(-3, 3)
        ax_geom.set_xlabel("projected axis")
        ax_geom.set_ylabel("projected axis")
        ax_geom.set_zlabel("response")

        # CENTER: provenance network / pruning
        weights = np.array(nf["top_weights"])
        weights = weights / (weights.max() + EPS)
        indices = nf["top_indices"]

        # draw edges to central source
        for i, (xy, w, idx_hist) in enumerate(zip(node_xy[:len(weights)], weights, indices)):
            color = "cyan" if idx_hist == 0 else ("orange" if w > 0.35 else "gray")
            lw = 0.8 + 5.0*w
            alpha = 0.15 + 0.75*w
            ax_net.plot([0, xy[0]], [0, xy[1]], color=color, lw=lw, alpha=alpha)
            ax_net.scatter([xy[0]], [xy[1]], s=80 + 500*w, color=color, edgecolor="white", alpha=alpha)
            if idx_hist == 0:
                ax_net.text(xy[0], xy[1], "GENESIS", color="black", fontsize=8, ha="center", va="center")
        ax_net.scatter([0], [0], s=900, color="cyan", edgecolor="white", alpha=0.95)
        ax_net.text(0, 0, "PIN", ha="center", va="center", fontsize=11, color="black")
        ax_net.set_xlim(-1.35, 1.35); ax_net.set_ylim(-1.35, 1.35)
        ax_net.set_aspect("equal")
        ax_net.axis("off")
        ax_net.set_title("Living Provenance Network\nbranches shrink as pruning selects retained flow")

        # RIGHT TOP: ledger
        active_event = min(len(EVENTS), max(1, int((frame + 1) / len(valid_slices) * len(EVENTS))))
        yvals = np.linspace(0.92, 0.10, len(EVENTS))
        for i, ev in enumerate(EVENTS):
            active = i < active_event
            color = "cyan" if active else "gray"
            ax_ledger.scatter([0.18], [yvals[i]], s=380, color=color, edgecolor="white")
            ax_ledger.text(0.32, yvals[i], ev, color="white", va="center", fontsize=10)
            if i > 0:
                ax_ledger.plot([0.18, 0.18], [yvals[i-1], yvals[i]], color="cyan" if active else "gray", lw=3, alpha=0.75)
        ax_ledger.set_xlim(0, 1); ax_ledger.set_ylim(0, 1); ax_ledger.axis("off")
        ax_ledger.set_title("Genesis Pin / Ledger")

        # RIGHT BOTTOM: telemetry
        upto = min(len(valid_log), nf["step"] + 1)
        if upto > 1:
            ax_tel.plot(valid_log["step"].iloc[:upto], valid_log["legit_prob"].iloc[:upto], color="cyan", lw=2.2, label="legit probability")
            ent_norm = valid_log["entropy"] / max(valid_log["entropy"].max(), EPS)
            ax_tel.plot(valid_log["step"].iloc[:upto], ent_norm.iloc[:upto], color="yellow", lw=1.8, label="entropy normalized")
        ax_tel.set_xlim(0, N_UPDATES)
        ax_tel.set_ylim(0, 1.1)
        ax_tel.grid(alpha=0.25)
        ax_tel.legend(fontsize=8)
        ax_tel.set_title("Pruning Telemetry")
        ax_tel.set_xlabel("step")

        fig.suptitle("V1173 Cinematic Provenance Collapse Engine", fontsize=17)
        return []

    ani = FuncAnimation(fig, update, frames=len(valid_slices), interval=80, blit=False)
    mp4 = OUT / "v1173_cinematic_provenance_collapse.mp4"
    try:
        ani.save(mp4, writer=FFMpegWriter(fps=12))
        plt.close(fig)
        return str(mp4)
    except Exception:
        gif = OUT / "v1173_cinematic_provenance_collapse.gif"
        ani.save(gif, writer=PillowWriter(fps=12))
        plt.close(fig)
        return str(gif)

# ==============================================================================
# MAIN
# ==============================================================================
def main(animate: bool = False):
    print(f"Running V1173 on device: {device}")
    np.random.seed(SEED)
    torch.manual_seed(SEED)

    all_cert = []
    all_logs = []
    valid_slices = []
    network_frames = []

    for mode in MODES:
        result = run_pruning_for_mode(mode, animate_store=(animate and mode == "valid_label_transported"))
        all_cert.append(result["cert"])
        all_logs.extend(result["log"])
        if mode == "valid_label_transported":
            valid_slices = result["slices"]
            network_frames = result["network_frames"]

    results_df = pd.DataFrame(all_cert)
    logs_df = pd.DataFrame(all_logs)
    results_df.to_csv(OUT / "v1173_full_stack_results.csv", index=False)
    logs_df.to_csv(OUT / "v1173_pruning_log.csv", index=False)

    plot_certification(results_df)
    animation_path = make_cinematic(valid_slices, network_frames, results_df, logs_df) if animate else None

    invalid_full = results_df[(~results_df["mode"].isin(VALID_MODES)) & (results_df["full_certified"])]
    valid_full = results_df[(results_df["mode"].isin(VALID_MODES)) & (results_df["full_certified"])]

    summary = {
        "document_id": "V1173_CINEMATIC_PROVENANCE_COLLAPSE_ENGINE",
        "device": str(device),
        "seed": SEED,
        "n_histories": N_HISTORIES,
        "resolution": RES,
        "dimension": 6,
        "updates": N_UPDATES,
        "valid_full_certified_count": int(len(valid_full)),
        "invalid_full_certified_count": int(len(invalid_full)),
        "full_certified_modes": results_df[results_df["full_certified"]]["mode"].tolist(),
        "outputs": {
            "results_csv": "v1173_full_stack_results.csv",
            "pruning_log_csv": "v1173_pruning_log.csv",
            "certification_panels": "v1173_certification_panels.png",
            "cinematic": animation_path,
        },
    }
    (OUT / "v1173_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--animate", action="store_true", help="Render cinematic provenance collapse animation.")
    args, _ = parser.parse_known_args()
    main(animate=args.animate)
