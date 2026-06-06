#!/usr/bin/env python3
"""
V1638 Full-Stack Retained Bridge L1/L2/L3 Visual Simulation
==========================================================

Purpose
-------
Upgrade V1637 from a downstream L3 mechanism demo into a full-stack,
claim-safe synthetic simulation that explicitly includes:

1. Genesis Pin / source-origin identity
2. Pruning-order causal governor
3. Admissible ordered slice formation
4. L1 dissipative convergence
5. L2 irreducible plateau
6. L3 third-order retained-current emergence
7. L3 blocker status: integrated-only, not closed

Boundary
--------
DATA_STATUS = synthetic controlled simulation
CLAIM_STATUS = illustrative mechanism demo
CLOSURE_STATUS = l1_l2_closed_l3_integrated_only_not_closed

This DOES NOT claim:
- empirical validation
- L3 closure
- physical General Relativity
- Einstein equations
- ADM proof
- physical spacetime
- physical curvature
- physical time

Language guardrail
------------------
Use pruning-order / ordered frame / ordered update.
Do not call the animation index physical time.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle


# ============================================================
# Status metadata
# ============================================================

DATA_STATUS = "synthetic controlled simulation"
CLAIM_STATUS = "illustrative full-stack mechanism demo"
CLOSURE_STATUS = "l1_l2_closed_l3_integrated_only_not_closed"
NOT_EMPIRICAL_VALIDATION = True
NOT_CLOSURE_PROOF = True
FULL_STACK_INCLUDED = True


# ============================================================
# Output
# ============================================================

OUT = Path("v1638_full_stack_retained_bridge_l123")
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# Helpers
# ============================================================

EPS = 1e-12

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def normalize01(x):
    x = np.asarray(x, dtype=float)
    lo, hi = np.nanmin(x), np.nanmax(x)
    if hi - lo < EPS:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)

def second_diff(x):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if len(x) >= 3:
        y[1:-1] = x[2:] - 2 * x[1:-1] + x[:-2]
        y[0] = y[1]
        y[-1] = y[-2]
    return y

def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x, dtype=float) ** 2)))

def ordering_fidelity(signal, true_order):
    """
    Synthetic ordering fidelity score using rank correlation, clipped to [0, 1].
    This is an internal synthetic demo metric, not empirical validation.
    """
    signal = np.asarray(signal, dtype=float)
    true_order = np.asarray(true_order, dtype=float)
    rank_sig = np.argsort(np.argsort(signal))
    rank_ord = np.argsort(np.argsort(true_order))
    if np.std(rank_sig) < EPS or np.std(rank_ord) < EPS:
        return 0.0
    corr = float(np.corrcoef(rank_sig, rank_ord)[0, 1])
    return max(0.0, corr)

def short_hash(*parts: object, n: int = 12) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()[:n]


# ============================================================
# Genesis Pin layer
# ============================================================

PINNED_GENESIS_REGISTRY = ("W1", "W2", "W3", "W4")
PINNED_GENESIS_ROOT = "ROOT:GENESIS_ANCHOR_000"
QUORUM = 3

def chain_transition(prev_root, registry, ordered_index, event_id, event_type, provenance_id, witnesses):
    return short_hash("transition", prev_root, ",".join(registry), ordered_index, event_id, event_type, provenance_id, ",".join(witnesses))

def quorum_valid(witnesses):
    return len(set(witnesses).intersection(PINNED_GENESIS_REGISTRY)) >= QUORUM

def build_roots(events, registry=PINNED_GENESIS_REGISTRY, root=PINNED_GENESIS_ROOT):
    roots = [root]
    cur = root
    for ev in events:
        cur = chain_transition(
            cur,
            registry,
            ev["pruning_order_index"],
            ev["event_id"],
            ev["event_type"],
            ev["provenance_id"],
            tuple(ev["witnesses"]),
        )
        roots.append(cur)
    return roots

def genesis_pin_pass(events, roots, registry=PINNED_GENESIS_REGISTRY, root=PINNED_GENESIS_ROOT):
    if tuple(registry) != tuple(PINNED_GENESIS_REGISTRY):
        return False
    if root != PINNED_GENESIS_ROOT:
        return False
    if len(roots) != len(events) + 1 or roots[0] != root:
        return False
    cur = root
    for i, ev in enumerate(events):
        if not quorum_valid(tuple(ev["witnesses"])):
            return False
        cur = chain_transition(
            cur,
            registry,
            ev["pruning_order_index"],
            ev["event_id"],
            ev["event_type"],
            ev["provenance_id"],
            tuple(ev["witnesses"]),
        )
        if roots[i + 1] != cur:
            return False
    return True


# ============================================================
# Synthetic full-stack trace
# ============================================================

N = 72
rng = np.random.default_rng(1638)
order = np.arange(N)

# Branch events staged across pruning order.
events = [
    {"event_id": "g0_source_A", "event_type": "source",     "pruning_order_index": 0,  "provenance_id": "P0", "requires_prior": False, "prior_dependency": None,             "entropy_before": 0.10, "entropy_after": 0.10, "damaged": 0, "repaired": 0, "branch": "A", "witnesses": ("W1","W2","W3")},
    {"event_id": "g1_source_B", "event_type": "source",     "pruning_order_index": 4,  "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "g0_source_A",    "entropy_before": 0.10, "entropy_after": 0.12, "damaged": 0, "repaired": 0, "branch": "B", "witnesses": ("W1","W2","W3")},
    {"event_id": "g2_source_C", "event_type": "source",     "pruning_order_index": 8,  "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "g1_source_B",    "entropy_before": 0.12, "entropy_after": 0.13, "damaged": 0, "repaired": 0, "branch": "C", "witnesses": ("W1","W2","W3")},
    {"event_id": "dA",          "event_type": "disruption", "pruning_order_index": 12, "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "g2_source_C",    "entropy_before": 0.13, "entropy_after": 0.55, "damaged": 3, "repaired": 0, "branch": "A", "witnesses": ("W1","W2","W4")},
    {"event_id": "dB",          "event_type": "loss",       "pruning_order_index": 17, "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "dA",             "entropy_before": 0.55, "entropy_after": 0.74, "damaged": 2, "repaired": 0, "branch": "B", "witnesses": ("W1","W3","W4")},
    {"event_id": "dC",          "event_type": "loss",       "pruning_order_index": 22, "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "dB",             "entropy_before": 0.74, "entropy_after": 0.86, "damaged": 1, "repaired": 0, "branch": "C", "witnesses": ("W2","W3","W4")},
    {"event_id": "rA",          "event_type": "repair",     "pruning_order_index": 29, "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "dA",             "entropy_before": 0.86, "entropy_after": 0.61, "damaged": 0, "repaired": 2, "branch": "A", "witnesses": ("W1","W2","W3")},
    {"event_id": "rB",          "event_type": "repair",     "pruning_order_index": 37, "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "dB",             "entropy_before": 0.61, "entropy_after": 0.43, "damaged": 0, "repaired": 2, "branch": "B", "witnesses": ("W1","W2","W3")},
    {"event_id": "rC",          "event_type": "recovery",   "pruning_order_index": 46, "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "dC",             "entropy_before": 0.43, "entropy_after": 0.27, "damaged": 0, "repaired": 1, "branch": "C", "witnesses": ("W1","W2","W3")},
    {"event_id": "h3",          "event_type": "closure",    "pruning_order_index": 57, "provenance_id": "P0", "requires_prior": True,  "prior_dependency": "rC",             "entropy_before": 0.27, "entropy_after": 0.18, "damaged": 0, "repaired": 1, "branch": "ABC", "witnesses": ("W1","W2","W4")},
]

events = sorted(events, key=lambda e: e["pruning_order_index"])
roots = build_roots(events)
GENESIS_PIN_VALID = genesis_pin_pass(events, roots)

def causal_governor_series(events, n=N):
    active_event_ids = set()
    source_seen = False
    source_provenance = None
    total_damaged = 0
    total_repaired = 0
    seq_checks = 0
    seq_valid = 0
    entropy_checks = 0
    entropy_valid = 0

    P = np.zeros(n)
    E = np.zeros(n)
    C = np.zeros(n)
    A = np.zeros(n)
    failures = []
    event_cursor = 0

    for k in range(n):
        while event_cursor < len(events) and events[event_cursor]["pruning_order_index"] <= k:
            ev = events[event_cursor]
            checks_here = 0
            valid_here = 0

            checks_here += 1
            if ev["event_type"] == "source" or source_seen:
                valid_here += 1
            else:
                failures.append(f"non_source_before_source:{ev['event_id']}")

            checks_here += 1
            if not ev["requires_prior"] or ev["prior_dependency"] in active_event_ids:
                valid_here += 1
            else:
                failures.append(f"missing_prior_event_dependency:{ev['event_id']}->{ev['prior_dependency']}")

            if ev["event_type"] == "source" and not source_seen:
                source_seen = True
                source_provenance = ev["provenance_id"]

            checks_here += 1
            if source_provenance is not None and ev["provenance_id"] == source_provenance:
                valid_here += 1
            else:
                failures.append(f"provenance_lineage_violation:{ev['event_id']}:{ev['provenance_id']}")

            checks_here += 1
            if quorum_valid(tuple(ev["witnesses"])):
                valid_here += 1
            else:
                failures.append(f"quorum_violation:{ev['event_id']}")

            # Entropy arrow: source can be flat/slight; disruption/loss should raise; repair/recovery/closure should lower.
            entropy_checks += 1
            etype = ev["event_type"]
            delta = ev["entropy_after"] - ev["entropy_before"]
            if etype in ["source"]:
                entropy_ok = abs(delta) <= 0.03
            elif etype in ["disruption", "loss"]:
                entropy_ok = delta > 0
            elif etype in ["repair", "recovery", "closure"]:
                entropy_ok = delta < 0
            else:
                entropy_ok = False

            if entropy_ok:
                entropy_valid += 1
            else:
                failures.append(f"entropy_arrow_violation:{ev['event_id']}")

            seq_checks += checks_here
            seq_valid += valid_here
            total_damaged += ev["damaged"]
            total_repaired += ev["repaired"]
            active_event_ids.add(ev["event_id"])
            event_cursor += 1

        P[k] = seq_valid / seq_checks if seq_checks else 0.0
        E[k] = entropy_valid / entropy_checks if entropy_checks else 0.0
        C[k] = min(1.0, total_repaired / total_damaged) if total_damaged else 0.0
        A[k] = C[k] * P[k] * E[k] * (1.0 if GENESIS_PIN_VALID else 0.0)

    return P, E, C, A, failures

P_sequence, E_arrow, C_closure, admissible_slice, governor_failures = causal_governor_series(events, N)

# Continuous entropy/order observable anchored to event entropy milestones.
event_x = np.array([e["pruning_order_index"] for e in events])
event_entropy = np.array([e["entropy_after"] for e in events])
entropy_raw = np.interp(order, event_x, event_entropy)
entropy_smooth = entropy_raw + 0.025 * np.sin(order / 3.8) + rng.normal(0, 0.0035, N)
E_order = entropy_smooth
Delta2_E_order = second_diff(E_order)


# ============================================================
# L1 / L2 / L3 progression
# ============================================================

# L1: dissipative convergence downstream of admissible repair/recovery.
L1_convergence = normalize01(
    0.65 * normalize01(1.0 - E_order)
    + 0.35 * C_closure
)
L1_closed = bool(L1_convergence[-1] > 0.82 and admissible_slice[-1] > 0.95)

# L2: irreducible plateau. Pairwise recovery rises and plateaus below full closure.
pairwise_recovery = np.clip(
    0.64 * sigmoid((order - 19) / 5.8)
    + 0.04 * np.sin(order / 5.4)
    + 0.05 * L1_convergence,
    0,
    0.82,
)
L2_plateau = np.clip(0.80 * pairwise_recovery + 0.10 * C_closure, 0, 0.86)
L2_residual_floor = np.clip(1.0 - L2_plateau, 0.14, 1.0)
L2_closed = bool(0.14 <= L2_residual_floor[-1] <= 0.38 and pairwise_recovery[-1] < 0.85)

# L3: third-order retained-current excess, not closed.
hyperedge_memory = sigmoid((order - 37) / 5.6) * admissible_slice
twist_component = normalize01(np.abs(Delta2_E_order)) * sigmoid((order - 28) / 4.8)
A123_associator = normalize01(
    np.abs(np.sin(order / 6.0 + 0.5) * hyperedge_memory)
    + 0.35 * twist_component
)
D123_divergence = normalize01(
    np.abs(np.gradient(pairwise_recovery + 0.30 * hyperedge_memory))
    + 0.45 * np.abs(Delta2_E_order)
)
Omega123_overlap = normalize01(
    0.25 * sigmoid((order - 30) / 5.0)
    + 0.75 * hyperedge_memory
)
I_cov_transfer = normalize01(
    0.55 * normalize01(np.abs(np.gradient(A123_associator)))
    + 0.45 * normalize01(D123_divergence * Omega123_overlap)
)

# Target T_H = third-order hyperedge memory target [Omega_ijk], gated by full prior stack.
T_H = np.clip(
    0.12 * pairwise_recovery
    + 0.48 * hyperedge_memory
    + 0.15 * A123_associator
    + 0.15 * D123_divergence * Omega123_overlap
    + 0.10 * I_cov_transfer
    + rng.normal(0, 0.006, N),
    0,
    1,
)

D_L3_signal = normalize01(
    0.40 * normalize01(E_order.max() - E_order)
    + 0.25 * normalize01(np.abs(Delta2_E_order))
    + 0.20 * A123_associator
    + 0.15 * I_cov_transfer
)

delta_C_L3 = normalize01(np.maximum(0.0, T_H - pairwise_recovery * 0.80))
L3_integrated_signal = normalize01(
    T_H * D_L3_signal * admissible_slice * (0.50 + 0.50 * delta_C_L3)
)

# Closure blockers are active by design; L3 is integrated but not closed.
CT3_block = np.full(N, 0.42)
CT7_block = np.full(N, 0.37)
closure_blocked = 0.68 * normalize01(
    0.45 * L3_integrated_signal
    + 0.25 * CT3_block
    + 0.20 * CT7_block
    + 0.10 * np.maximum(0, 0.24 - I_cov_transfer)
)
L3_integrated_only = bool(np.max(L3_integrated_signal) > 0.50)
L3_closed = False


# ============================================================
# Full-stack nulls / synthetic payoff demo
# ============================================================

real_fid_L3 = ordering_fidelity(L3_integrated_signal, order)
real_fid_pw = ordering_fidelity(pairwise_recovery, order)

n_nulls = 140
null_fids_L3 = []
null_fids_pw = []
for _ in range(n_nulls):
    perm = rng.permutation(N)
    # Ordered-trace null breaks retained order but preserves values.
    null_fids_L3.append(ordering_fidelity(L3_integrated_signal[perm], order))
    null_fids_pw.append(ordering_fidelity(pairwise_recovery[perm], order))

avg_null_L3 = float(np.mean(null_fids_L3))
avg_null_pw = float(np.mean(null_fids_pw))
sep_L3 = float(real_fid_L3 - avg_null_L3)
sep_pw = float(real_fid_pw - avg_null_pw)
improvement_pct = float((sep_L3 / sep_pw - 1.0) * 100.0) if sep_pw > EPS else 0.0


# ============================================================
# Save trace + event ledger
# ============================================================

trace = pd.DataFrame({
    "pruning_order_index": order,
    "genesis_pin_valid": GENESIS_PIN_VALID,
    "P_sequence": P_sequence,
    "E_arrow": E_arrow,
    "C_closure": C_closure,
    "admissible_slice": admissible_slice,
    "E_order": E_order,
    "Delta2_E_order": Delta2_E_order,
    "L1_convergence": L1_convergence,
    "pairwise_recovery": pairwise_recovery,
    "L2_plateau": L2_plateau,
    "L2_residual_floor": L2_residual_floor,
    "A123_associator": A123_associator,
    "D123_divergence": D123_divergence,
    "Omega123_overlap": Omega123_overlap,
    "I_cov_transfer": I_cov_transfer,
    "T_H": T_H,
    "D_L3": D_L3_signal,
    "delta_C_L3": delta_C_L3,
    "L3_integrated": L3_integrated_signal,
    "closure_blocked": closure_blocked,
    "data_status": DATA_STATUS,
    "claim_status": CLAIM_STATUS,
    "closure_status": CLOSURE_STATUS,
})
trace.to_csv(OUT / "trace.csv", index=False)
pd.DataFrame(events).to_csv(OUT / "genesis_pruning_event_ledger.csv", index=False)


# ============================================================
# Static visual
# ============================================================

C = {
    "bg": "#0a0f1e",
    "panel": "#0f172a",
    "grid": "#475569",
    "text": "#e0f2fe",
    "muted": "#94a3b8",
    "l1": "#86efac",
    "l2": "#fbbf24",
    "l3": "#a5f3fc",
    "hyper": "#22d3ee",
    "driver": "#fb923c",
    "block": "#f472b6",
    "genesis": "#c4b5fd",
}

fig = plt.figure(figsize=(17, 11.5), facecolor=C["bg"])
gs = fig.add_gridspec(4, 3, height_ratios=[0.9, 1.1, 0.60, 0.75], hspace=0.30, wspace=0.22)

ax0 = fig.add_subplot(gs[0:2, 0:2])
ax1 = fig.add_subplot(gs[0:2, 2])
ax2 = fig.add_subplot(gs[2, :])
ax3 = fig.add_subplot(gs[3, :])

# Main progression curves
ax0.set_facecolor(C["bg"])
for spine in ax0.spines.values():
    spine.set_color("#334155")

ax0.plot(order, admissible_slice, color=C["genesis"], linewidth=2.4, label="Genesis + pruning admissibility")
ax0.plot(order, L1_convergence, color=C["l1"], linewidth=2.5, label="L1 dissipative convergence")
ax0.plot(order, L2_plateau, color=C["l2"], linewidth=2.5, label="L2 pairwise plateau")
ax0.plot(order, T_H, color=C["hyper"], linewidth=2.4, label=r"L3 hyperedge target $T_H$")
ax0.plot(order, D_L3_signal, color=C["driver"], linewidth=2.3, label=r"L3 driver $D_{L3}$")
ax0.plot(order, L3_integrated_signal, color=C["l3"], linewidth=4.5, label="Integrated L3 signal", zorder=5)
ax0.plot(order, closure_blocked, color=C["block"], linewidth=2.2, linestyle="--", label="L3 closure blocked")

ax0.fill_between(order, 0, admissible_slice, alpha=0.045, color=C["genesis"])
ax0.fill_between(order, 0, L3_integrated_signal, alpha=0.085, color=C["l3"])
ax0.set_title("Full-Stack Emergence over Pruning-Order History", fontsize=16, color=C["text"], pad=12, fontweight="semibold")
ax0.set_xlabel("Pruning-order index", fontsize=11, color=C["muted"])
ax0.set_ylabel("Normalized signal strength", fontsize=11, color=C["muted"])
ax0.tick_params(colors=C["muted"])
ax0.grid(True, alpha=0.15, color=C["grid"])
ax0.legend(loc="upper left", fontsize=9.2, framealpha=0.85, facecolor=C["panel"], edgecolor="#334155")

# Component scatter
ax1.set_facecolor(C["bg"])
for spine in ax1.spines.values():
    spine.set_color("#334155")
ax1.scatter(A123_associator, T_H, s=38, alpha=0.78, c=C["hyper"], label=r"$A_{123}$ associator")
ax1.scatter(D123_divergence * Omega123_overlap, T_H, s=38, alpha=0.78, c=C["driver"], label=r"$D_{123}\cdot\Omega_{123}$")
ax1.scatter(I_cov_transfer, T_H, s=38, alpha=0.65, c=C["genesis"], label=r"$I_{cov}$ transfer")
ax1.set_title("L3 Components vs Hyperedge Target", fontsize=13, color=C["text"], pad=8)
ax1.set_xlabel("Normalized component", fontsize=10, color=C["muted"])
ax1.set_ylabel(r"$T_H$", fontsize=10, color=C["muted"])
ax1.tick_params(colors=C["muted"])
ax1.grid(True, alpha=0.15, color=C["grid"])
ax1.legend(fontsize=8.5, loc="lower right", framealpha=0.8, facecolor=C["panel"], edgecolor="#334155")

bar_y = 0.12
ax1.text(0.06, bar_y + 0.05, "Synthetic separation: ordered trace − ordered null", fontsize=8.4, color=C["muted"], transform=ax1.transAxes)
ax1.barh(bar_y - 0.02, sep_pw, height=0.075, left=0.06, color="#64748b", transform=ax1.transAxes)
ax1.barh(bar_y - 0.06, sep_L3, height=0.075, left=0.06, color=C["hyper"], transform=ax1.transAxes)
ax1.text(0.06 + min(sep_pw,0.82) + 0.01, bar_y - 0.02, f"{sep_pw:.2f}", fontsize=8, color=C["muted"], va="center", transform=ax1.transAxes)
ax1.text(0.06 + min(sep_L3,0.82) + 0.01, bar_y - 0.06, f"{sep_L3:.2f}", fontsize=8, color=C["l3"], va="center", transform=ax1.transAxes)

# Flow diagram
ax2.set_facecolor(C["bg"])
ax2.axis("off")
steps = [
    ("1. Genesis Pin\nsource-origin\nidentity", C["genesis"]),
    ("2. Pruning-order\ngovernor", "#60a5fa"),
    ("3. Admissible\nordered slice", "#38bdf8"),
    ("4. L1\nconvergence", C["l1"]),
    ("5. L2\nplateau", C["l2"]),
    ("6. L3\nintegrated-only", C["l3"]),
]
x_positions = [0.07, 0.22, 0.37, 0.52, 0.67, 0.82]
for i, (label, color) in enumerate(steps):
    ax2.text(
        x_positions[i], 0.62, label,
        ha="center", va="center", fontsize=10.1, color=C["text"],
        bbox=dict(boxstyle="round,pad=0.52", facecolor=color, alpha=0.18, edgecolor=color, linewidth=1.5),
    )
    if i < len(steps) - 1:
        ax2.annotate("", xy=(x_positions[i+1]-0.055, 0.62), xytext=(x_positions[i]+0.055, 0.62),
                     arrowprops=dict(arrowstyle="->", color="#fbbf24", lw=2.2))

ax2.text(
    0.5, 0.15,
    "Full-stack synthetic mechanism demo only  •  L1/L2 closed in this controlled run  •  L3 integrated-only, not closed  •  CT3 + CT7 blockers active",
    ha="center", va="center", fontsize=10.2, color=C["muted"],
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#1e2937", alpha=0.6, edgecolor="#334155"),
)

# Bottom status/payoff
ax3.set_facecolor(C["bg"])
ax3.axis("off")
status_str = (
    "FULL-STACK SYNTHETIC DEMO: GENESIS PIN → PRUNING GOVERNOR → L1 → L2 → L3\n\n"
    f"Genesis Pin valid: {GENESIS_PIN_VALID}   |   Final admissible slice: {admissible_slice[-1]:.3f}   |   L1 closed: {L1_closed}   |   L2 closed: {L2_closed}   |   L3 closed: {L3_closed}\n"
    f"Ordering Fidelity on Synthetic Ordered Traces:  L3 = {real_fid_L3:.3f}   vs   Pairwise = {real_fid_pw:.3f}\n"
    f"Adversarial Ordered-Null Rejection, lower = better:  L3 = {avg_null_L3:.3f}   vs   Pairwise = {avg_null_pw:.3f}\n\n"
    f"Separation, Ordered Synthetic Trace − Null:  L3 = {sep_L3:.3f}   Pairwise = {sep_pw:.3f}\n"
    f"→ In this synthetic mechanism demo, the full-stack L3 integrated signal shows ~{improvement_pct:.0f}% better ordered-null discrimination than pairwise recovery."
)
ax3.text(
    0.5, 0.55, status_str,
    ha="center", va="center", fontsize=11.4, color=C["text"], family="monospace",
    bbox=dict(boxstyle="round,pad=0.8", facecolor=C["panel"], alpha=0.96, edgecolor=C["hyper"], linewidth=2.3),
)

fig.suptitle(
    "V1638 Full-Stack Retained Bridge — Genesis Pin → Pruning → L1/L2/L3\n"
    "Synthetic Mechanism Demo: L3 Integrated Signal Remains Claim-Safe and Not Closed",
    fontsize=15, color="#bae6fd", y=0.986, fontweight="semibold",
)
plt.tight_layout(rect=[0, 0.01, 1, 0.955])
fig.savefig(OUT / "static_full_stack_claimsafe.png", dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)


# ============================================================
# Animation
# ============================================================

nodes = 18
theta = np.linspace(0, 2*np.pi, nodes, endpoint=False)
xy = np.c_[np.cos(theta), np.sin(theta)]
triads = [(i % nodes, (i + 6) % nodes, (i + 12) % nodes) for i in range(0, nodes, 2)]
branch_nodes = {"A": [0, 1, 2, 3, 4, 5], "B": [6, 7, 8, 9, 10, 11], "C": [12, 13, 14, 15, 16, 17]}

fig, (axn, axs) = plt.subplots(1, 2, figsize=(15, 7), facecolor=C["bg"])
fig.patch.set_facecolor(C["bg"])

def frame(k):
    axn.clear()
    axs.clear()

    # Left topology panel
    axn.set_facecolor(C["bg"])
    axn.set_xlim(-1.45, 1.45)
    axn.set_ylim(-1.45, 1.45)
    axn.set_aspect("equal")
    axn.axis("off")

    for r in [0.35, 0.7, 1.05]:
        axn.add_patch(Circle((0,0), r, fill=False, color="#1e2937", linewidth=0.8, alpha=0.6))

    # Branch provenance coloring intensity earned from admissibility.
    node_scale = 55 + 340 * admissible_slice[k]
    for i, (x, y) in enumerate(xy):
        axn.scatter([x], [y], s=node_scale, c=C["l3"], alpha=0.82, edgecolors="white", linewidths=0.55, zorder=3)

    # Genesis key / source beam once genesis valid.
    if k >= 0 and GENESIS_PIN_VALID:
        axn.annotate("", xy=(0, 1.18), xytext=(0, 0.18), arrowprops=dict(arrowstyle="->", color=C["genesis"], lw=2.6), zorder=4)
        axn.text(0, 1.30, "Genesis Pin", color=C["genesis"], fontsize=9, ha="center", va="center")

    # Pairwise edges
    pw_alpha = 0.08 + 0.65 * pairwise_recovery[k]
    pw_lw = 0.8 + 2.6 * pairwise_recovery[k]
    edge_list = [(i, (i+1) % nodes) for i in range(nodes)] + [(i, (i+4) % nodes) for i in range(0, nodes, 2)]
    for a, b in edge_list:
        axn.plot([xy[a,0], xy[b,0]], [xy[a,1], xy[b,1]], color=C["l2"], alpha=pw_alpha, linewidth=pw_lw, zorder=1)

    # Branch sectors / three-source provenance memory
    for branch, ns in branch_nodes.items():
        pts = xy[ns + [ns[0]]]
        axn.plot(pts[:,0], pts[:,1], color=C["genesis"], alpha=0.10 + 0.28 * admissible_slice[k], linewidth=1.0, zorder=0)

    # Hyperedges emerge after admissible recovery.
    if k > 20:
        he_alpha = 0.05 + 0.76 * T_H[k]
        he_lw = 1.0 + 4.3 * T_H[k]
        for a, b, c in triads:
            pts = xy[[a,b,c,a]]
            axn.plot(pts[:,0], pts[:,1], color=C["hyper"], alpha=he_alpha, linewidth=he_lw, zorder=2)
            if T_H[k] > 0.45:
                axn.plot(pts[:,0], pts[:,1], color=C["l3"], alpha=he_alpha * 0.35, linewidth=he_lw * 1.75, zorder=1)

    # Central L-stack node: L1/L2/L3
    l3_size = 180 + 1250 * L3_integrated_signal[k]
    l3_alpha = 0.30 + 0.58 * L3_integrated_signal[k]
    for r_scale, alpha_scale in [(1.7,0.10),(1.25,0.20),(1.0,0.34)]:
        axn.add_patch(Circle((0,0), (l3_size/430)*r_scale, fill=True, color=C["l3"], alpha=l3_alpha*alpha_scale*0.55))
    axn.scatter([0], [0], s=l3_size, c=C["l3"], alpha=l3_alpha, edgecolors="white", linewidths=1.6, zorder=5)
    center_label = "L1/L2\nL3" if k > 35 else "L1/L2"
    axn.text(0, 0, center_label, ha="center", va="center", fontsize=11.5, fontweight="bold", color=C["bg"], zorder=6)

    # Holonomy-like memory vector
    twist_angle = np.sum(Delta2_E_order[:k+1]) * 0.8
    twist_len = 0.48 + 0.35 * L3_integrated_signal[k]
    dx = twist_len * np.cos(twist_angle)
    dy = twist_len * np.sin(twist_angle)
    axn.annotate("", xy=(dx,dy), xytext=(0,0), arrowprops=dict(arrowstyle="->", color=C["block"], lw=2.2, connectionstyle="arc3,rad=0.15"), zorder=4)
    axn.text(dx*1.15, dy*1.15, "holonomy-like\nmemory", fontsize=7.5, color=C["block"], ha="center", va="center", alpha=0.9)

    axn.set_title("Genesis-pinned retained-order topology with hyperedge memory", color=C["text"], fontsize=12, pad=6)

    # Right signal panel
    axs.set_facecolor(C["bg"])
    for spine in axs.spines.values():
        spine.set_color("#334155")

    upto = np.arange(k+1)
    for y, color, lw in [
        (admissible_slice, C["genesis"], 1.6),
        (L1_convergence, C["l1"], 1.6),
        (L2_plateau, C["l2"], 1.6),
        (T_H, C["hyper"], 1.6),
        (D_L3_signal, C["driver"], 1.6),
        (L3_integrated_signal, C["l3"], 2.0),
    ]:
        axs.plot(order, y, alpha=0.16, color=color, linewidth=lw)

    axs.plot(upto, admissible_slice[:k+1], color=C["genesis"], linewidth=2.2, label="Genesis + pruning admissibility")
    axs.plot(upto, L1_convergence[:k+1], color=C["l1"], linewidth=2.2, label="L1 convergence")
    axs.plot(upto, L2_plateau[:k+1], color=C["l2"], linewidth=2.2, label="L2 plateau")
    axs.plot(upto, T_H[:k+1], color=C["hyper"], linewidth=2.2, label=r"$T_H$ hyperedge memory")
    axs.plot(upto, D_L3_signal[:k+1], color=C["driver"], linewidth=2.0, label=r"$D_{L3}$ driver")
    axs.plot(upto, L3_integrated_signal[:k+1], color=C["l3"], linewidth=4.0, label="Integrated L3", zorder=4)
    axs.plot(upto, closure_blocked[:k+1], color=C["block"], linewidth=2.1, linestyle="--", label="L3 closure blocked")

    axs.set_ylim(-0.04, 1.06)
    axs.set_xlim(-1, N+1)
    axs.set_title("Full-stack signal emergence over pruning order", color=C["text"], fontsize=12, pad=6)
    axs.set_xlabel("Pruning-order index", color=C["muted"], fontsize=10)
    axs.tick_params(colors=C["muted"])
    axs.grid(True, alpha=0.2, color=C["grid"])
    axs.legend(loc="upper left", fontsize=8.0, framealpha=0.85, facecolor=C["panel"], edgecolor="#334155")

    fig.suptitle(
        f"V1638 Full-Stack Retained Bridge | pruning-order frame = {k:02d}",
        color="#bae6fd", fontsize=14, y=0.98,
    )

anim = FuncAnimation(fig, frame, frames=N, interval=115)
anim.save(OUT / "animation_full_stack_claimsafe.gif", writer=PillowWriter(fps=8), dpi=140)
plt.close(fig)


# ============================================================
# Summary + README
# ============================================================

summary = {
    "document_id": "V1638_FULL_STACK_RETAINED_BRIDGE_L123_CLAIMSAFE",
    "status": "completed",
    "full_stack_included": FULL_STACK_INCLUDED,
    "data_status": DATA_STATUS,
    "claim_status": CLAIM_STATUS,
    "closure_status": CLOSURE_STATUS,
    "not_empirical_validation": NOT_EMPIRICAL_VALIDATION,
    "not_closure_proof": NOT_CLOSURE_PROOF,
    "claim_boundary": (
        "Synthetic controlled full-stack mechanism demo only. "
        "Genesis Pin, pruning governor, admissible ordered slice, L1, L2, and L3 are simulated in one chain. "
        "L3 remains integrated-only, not closed."
    ),
    "language_guardrail": "No physical-time primitive; animation uses pruning-order frame.",
    "full_stack_layers": [
        "Genesis Pin / source-origin identity",
        "Pruning-order causal governor",
        "Admissible ordered slice",
        "L1 dissipative convergence",
        "L2 irreducible plateau",
        "L3 third-order retained-current integrated signal",
        "CT3/CT7 closure blockers",
    ],
    "status_flags": {
        "genesis_pin_valid": bool(GENESIS_PIN_VALID),
        "l1_closed_in_controlled_demo": bool(L1_closed),
        "l2_closed_in_controlled_demo": bool(L2_closed),
        "l3_integrated_only": bool(L3_integrated_only),
        "l3_closed": bool(L3_closed),
    },
    "target": "T_H = [Omega_ijk] synthetic hyperedge-memory target",
    "driver": "D_L3 = (E_order, Delta^2 E_order, A123, D123*Omega123, I_cov_transfer)",
    "l3_decomposition_terms": [
        "A123 associator",
        "D123 third-order divergence",
        "Omega123 triple-overlap support",
        "I_cov_transfer geometry-transfer covariance",
        "delta_C_L3 excess over pairwise recovery",
    ],
    "closure_blockers": ["CT3 minimality", "CT7 operator-class boundary"],
    "synthetic_payoff": {
        "ordered_trace_L3_fidelity": float(real_fid_L3),
        "ordered_trace_pairwise_fidelity": float(real_fid_pw),
        "avg_ordered_null_L3": float(avg_null_L3),
        "avg_ordered_null_pairwise": float(avg_null_pw),
        "separation_L3": float(sep_L3),
        "separation_pairwise": float(sep_pw),
        "relative_improvement_percent": float(improvement_pct),
    },
    "outputs": [
        "static_full_stack_claimsafe.png",
        "animation_full_stack_claimsafe.gif",
        "trace.csv",
        "genesis_pruning_event_ledger.csv",
        "summary.json",
        "README.md",
    ],
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2))

readme = f"""# V1638 Full-Stack Retained Bridge L1/L2/L3 — Claim-Safe Synthetic Demo

Run:

```bash
python v1638_full_stack_retained_bridge_l123.py
```

## Status

```text
DATA_STATUS = {DATA_STATUS}
CLAIM_STATUS = {CLAIM_STATUS}
CLOSURE_STATUS = {CLOSURE_STATUS}
```

## What this includes

This version is a full-stack synthetic mechanism demo:

1. Genesis Pin / source-origin identity
2. Pruning-order causal governor
3. Admissible ordered slice formation
4. L1 dissipative convergence
5. L2 irreducible plateau
6. L3 third-order retained-current integrated signal
7. CT3/CT7 closure blockers

## Claim boundary

This is **not** empirical validation and **not** a closure proof.

It does **not** claim physical General Relativity, Einstein equations, ADM proof,
physical spacetime, physical curvature, or physical time.

## Language guardrail

The animation uses:

```text
pruning-order frame
```

not `t`, because the index is an ordered pruning/update index, not physical time.

## Outputs

- `static_full_stack_claimsafe.png`
- `animation_full_stack_claimsafe.gif`
- `trace.csv`
- `genesis_pruning_event_ledger.csv`
- `summary.json`
"""

(OUT / "README.md").write_text(readme)

print("V1638 full-stack claim-safe package created in:", OUT.resolve())
print(json.dumps(summary, indent=2))
