#!/usr/bin/env python3
"""
V997 Genesis Pin Publication Audit

Merged version:
- V996 enhanced audit engine:
  visible-state convergence, pinned registry, pinned root, witness quorum,
  append-only chain validation, tamper detection, forked-root rejection,
  self-defined registry rejection, quorum-failed replay rejection,
  circular bootstrap rejection.

- Publication package layer:
  V923 / V994 / V995 framing, claim-boundary doc, full markdown report,
  manifest JSON, layer-stack CSV, results CSV, source ZIP, MP4/GIF/PNG outputs.

Core demonstrated claim
-----------------------
In the tested recoverability stack, visible-state equivalence accepts all five
histories. Adding a Genesis Pin converts legitimacy from a final-state property
into a recoverable-history property.

Only the history with pinned registry, pinned anchor root, quorum witness
participation, append-only continuity, and no circular bootstrap is accepted.

Claim boundary
--------------
This is a modeled full-stack audit demonstration, not a universal mathematical
proof. It does not claim physical spacetime, physical time, GR, Einstein
equations, actual cryptographic production security, or universal theorem status.
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.patches import Circle, FancyBboxPatch


OUT = Path("v997_genesis_pin_outputs")
OUT.mkdir(exist_ok=True)

N_STEPS = 8
FPS = 1.2

PINNED_GENESIS_REGISTRY = ("W1", "W2", "W3", "W4")
PINNED_GENESIS_ROOT = "ROOT:GENESIS_ANCHOR_000"
QUORUM = 3
COMMON_VISIBLE_STATE = np.array([0.0, 0.0])

EVENTS = [
    "observe",
    "emit_symbol",
    "fresh_nonce",
    "append_ledger",
    "witness_root",
    "registry_ok",
    "anchor_update",
]


# ==============================================================================
# LOW-LEVEL CHAIN / CERTIFICATION ENGINE
# ==============================================================================

def short_hash(*parts: object, n: int = 12) -> str:
    msg = "|".join(map(str, parts)).encode("utf-8")
    return hashlib.sha256(msg).hexdigest()[:n]


def chained_transition(
    prev_root: str,
    registry: Tuple[str, ...],
    step: int,
    event: str,
    witnesses: Tuple[str, ...],
) -> str:
    """
    Deterministic hash-chain transition used for this audit.

    This is intentionally called a chained transition rather than a signed
    transition. It is a modeled chain commitment, not a production signature
    system.
    """
    return short_hash(
        "transition",
        prev_root,
        ",".join(registry),
        step,
        event,
        ",".join(witnesses),
    )


def quorum_valid(witnesses: Tuple[str, ...], registry: Tuple[str, ...]) -> bool:
    """
    Simulated witness-quorum check:
    at least QUORUM witnesses must belong to the pinned registry.
    """
    return len(set(witnesses).intersection(set(registry))) >= QUORUM


def registry_matches(registry: Tuple[str, ...]) -> bool:
    return tuple(registry) == tuple(PINNED_GENESIS_REGISTRY)


def root_matches(root: str) -> bool:
    return root == PINNED_GENESIS_ROOT


def detect_circular_bootstrap(registry: Tuple[str, ...], root: str) -> bool:
    """
    Minimal modeled circularity test:
    a path that defines its own registry or root outside the pinned boundary
    is self-bootstrapping relative to the stack.
    """
    return not registry_matches(registry) or not root_matches(root)


def validate_append_only_chain(
    genesis_root: str,
    registry: Tuple[str, ...],
    events: List[str],
    witnesses: List[Tuple[str, ...]],
    roots: List[str],
) -> bool:
    if len(roots) != len(events) + 1:
        return False
    if roots[0] != genesis_root:
        return False

    cur = genesis_root
    for i, (event, witness_set) in enumerate(zip(events, witnesses), start=1):
        cur = chained_transition(cur, registry, i, event, witness_set)
        if roots[i] != cur:
            return False
    return True


# ==============================================================================
# HISTORY MODEL
# ==============================================================================

@dataclass
class HistoryPath:
    name: str
    color: str
    genesis_registry: Tuple[str, ...]
    genesis_root: str
    events: List[str]
    witness_sets: List[Tuple[str, ...]]
    points: np.ndarray
    roots: List[str]
    final_observable: Tuple[float, float]
    same_visible_state: bool
    accepted_without_genesis_pin: bool
    accepted_with_genesis_pin: bool
    registry_matches: bool
    root_matches: bool
    quorum_all_steps: bool
    append_only_valid: bool
    circular_bootstrap_detected: bool
    rejection_reason: str


def make_points(start: Tuple[float, float], arc_height: float) -> np.ndarray:
    t = np.linspace(0, 1, N_STEPS)
    start = np.array(start, dtype=float)
    x = (1 - t) * start[0] + t * COMMON_VISIBLE_STATE[0]
    y = (1 - t) * start[1] + t * COMMON_VISIBLE_STATE[1] + arc_height * t * (1 - t)
    return np.column_stack([x, y])


def build_path(
    name: str,
    color: str,
    genesis_registry: Tuple[str, ...],
    genesis_root: str,
    events: List[str],
    witness_sets: List[Tuple[str, ...]],
    start: Tuple[float, float],
    arc_height: float,
    tamper_chain: bool = False,
) -> HistoryPath:
    points = make_points(start, arc_height)

    roots = [genesis_root]
    current = genesis_root
    for i, (event, witnesses) in enumerate(zip(events, witness_sets), start=1):
        current = chained_transition(current, genesis_registry, i, event, witnesses)
        roots.append(current)

    if tamper_chain and len(roots) > 4:
        roots[4] = "TAMPERED_" + roots[4]

    same_visible = bool(np.allclose(points[-1], COMMON_VISIBLE_STATE))
    reg_ok = registry_matches(genesis_registry)
    root_ok = root_matches(genesis_root)
    quorum_ok = all(quorum_valid(w, PINNED_GENESIS_REGISTRY) for w in witness_sets)
    append_ok = validate_append_only_chain(genesis_root, genesis_registry, events, witness_sets, roots)
    circular = detect_circular_bootstrap(genesis_registry, genesis_root)

    accepted_without_pin = same_visible
    accepted_with_pin = bool(
        same_visible
        and reg_ok
        and root_ok
        and quorum_ok
        and append_ok
        and not circular
    )

    if accepted_with_pin:
        reason = "accepted: visible state + pinned genesis + quorum + append-only chain"
    elif not same_visible:
        reason = "rejected: final observable mismatch"
    elif not reg_ok and not root_ok:
        reason = "rejected: self-defined registry and self-defined root"
    elif not root_ok:
        reason = "rejected: wrong genesis anchor root"
    elif not reg_ok:
        reason = "rejected: wrong witness registry"
    elif not quorum_ok:
        reason = "rejected: witness quorum failed"
    elif not append_ok:
        reason = "rejected: append-only chain failed"
    elif circular:
        reason = "rejected: circular bootstrap boundary failed"
    else:
        reason = "rejected: unspecified modeled legitimacy failure"

    return HistoryPath(
        name=name,
        color=color,
        genesis_registry=genesis_registry,
        genesis_root=genesis_root,
        events=events,
        witness_sets=witness_sets,
        points=points,
        roots=roots,
        final_observable=tuple(points[-1]),
        same_visible_state=same_visible,
        accepted_without_genesis_pin=accepted_without_pin,
        accepted_with_genesis_pin=accepted_with_pin,
        registry_matches=reg_ok,
        root_matches=root_ok,
        quorum_all_steps=quorum_ok,
        append_only_valid=append_ok,
        circular_bootstrap_detected=circular,
        rejection_reason=reason,
    )


def build_histories() -> List[HistoryPath]:
    pinned_witnesses = [("W1", "W2", "W3") for _ in EVENTS]
    weak_witnesses = [("W1", "X9", "Y9") for _ in EVENTS]
    attacker_witnesses = [("A1", "A2", "A3") for _ in EVENTS]

    return [
        build_path(
            "Legitimate history",
            "#2ca25f",
            PINNED_GENESIS_REGISTRY,
            PINNED_GENESIS_ROOT,
            EVENTS,
            pinned_witnesses,
            (-4.2, 2.6),
            1.0,
        ),
        build_path(
            "Forked counterfeit",
            "#de2d26",
            PINNED_GENESIS_REGISTRY,
            "ROOT:FORKED_ANCHOR_999",
            EVENTS,
            pinned_witnesses,
            (-4.2, -2.4),
            -1.1,
        ),
        build_path(
            "Self-defined counterfeit",
            "#fdae6b",
            ("A1", "A2", "A3", "A4"),
            "ROOT:SELF_DEFINED_123",
            EVENTS,
            attacker_witnesses,
            (4.2, 1.7),
            1.2,
        ),
        build_path(
            "Quorum-failed replay",
            "#756bb1",
            PINNED_GENESIS_REGISTRY,
            PINNED_GENESIS_ROOT,
            EVENTS,
            weak_witnesses,
            (4.2, -2.1),
            -0.9,
        ),
        build_path(
            "Tampered append chain",
            "#3182bd",
            PINNED_GENESIS_REGISTRY,
            PINNED_GENESIS_ROOT,
            EVENTS,
            pinned_witnesses,
            (0.0, 3.4),
            0.8,
            tamper_chain=True,
        ),
    ]


# ==============================================================================
# DATA OUTPUTS
# ==============================================================================

def make_results(histories: List[HistoryPath]) -> pd.DataFrame:
    rows = []
    for h in histories:
        rows.append({
            "history": h.name,
            "final_x": h.final_observable[0],
            "final_y": h.final_observable[1],
            "same_visible_state": h.same_visible_state,
            "accepted_without_genesis_pin": h.accepted_without_genesis_pin,
            "genesis_registry_matches": h.registry_matches,
            "genesis_root_matches": h.root_matches,
            "witness_quorum_all_steps": h.quorum_all_steps,
            "append_only_chain_valid": h.append_only_valid,
            "circular_bootstrap_detected": h.circular_bootstrap_detected,
            "accepted_with_genesis_pin": h.accepted_with_genesis_pin,
            "reason": h.rejection_reason,
            "genesis_registry": ",".join(h.genesis_registry),
            "genesis_root": h.genesis_root,
            "final_chain_root": h.roots[-1],
        })
    return pd.DataFrame(rows)


def make_layer_stack() -> pd.DataFrame:
    rows = [
        {
            "layer": "V923",
            "name": "Observable-state insufficiency",
            "role": "Visible equality is not legitimacy.",
            "audit_test": "All histories converge to same final observable coordinate.",
            "failure_without_pin": "All paths accepted under visible-state equivalence.",
        },
        {
            "layer": "V994",
            "name": "Bootstrap/circularity boundary",
            "role": "Prevent self-defined legitimacy.",
            "audit_test": "Reject self-defined registry/root.",
            "failure_without_pin": "Attacker can define its own registry and root.",
        },
        {
            "layer": "V995",
            "name": "Recoverable-history legitimacy",
            "role": "Legitimacy requires rooted continuity, not just final state.",
            "audit_test": "Require pinned root, quorum, append-only chain.",
            "failure_without_pin": "Forks, replays, and tampered chains can end at same visible state.",
        },
        {
            "layer": "V997",
            "name": "Genesis Pin publication audit",
            "role": "Merge audit engine with publication package.",
            "audit_test": "Five histories; 5 accepted without pin, 1 accepted with pin.",
            "failure_without_pin": "Visible-state-only certification is underdetermined.",
        },
    ]
    return pd.DataFrame(rows)


def result_manifest(results: pd.DataFrame) -> Dict[str, Any]:
    return {
        "document_id": "V997_GENESIS_PIN_PUBLICATION_AUDIT",
        "verdict": "genesis_pin_publication_audit_complete",
        "claim_demonstrated": (
            "Same observable state does not certify legitimate history in the tested "
            "recoverability stack. Genesis Pin turns legitimacy into a recoverable-history property."
        ),
        "histories_tested": int(len(results)),
        "accepted_without_genesis_pin": int(results["accepted_without_genesis_pin"].sum()),
        "accepted_with_genesis_pin": int(results["accepted_with_genesis_pin"].sum()),
        "minimal_genesis_pin": {
            "pinned_genesis_registry": list(PINNED_GENESIS_REGISTRY),
            "pinned_genesis_anchor_root": PINNED_GENESIS_ROOT,
            "witness_quorum": QUORUM,
            "append_only_chain_required": True,
            "circular_bootstrap_rejected": True,
        },
        "claim_boundary": (
            "Modeled full-stack audit demonstration; not a universal proof, not production "
            "cryptographic security, and not a physics claim."
        ),
        "publication_claim": (
            "In the tested recoverability stack, visible-state equivalence accepts all five "
            "histories. With Genesis Pin, only the path satisfying pinned registry, pinned root, "
            "quorum witness participation, append-only continuity, and no circular bootstrap is accepted."
        ),
    }


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def draw_box(ax, xy, w, h, text, fc="#f7f7f7", ec="#333333", fontsize=10, weight="normal"):
    box = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.03,rounding_size=0.04",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.2,
        transform=ax.transAxes,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + w / 2,
        xy[1] + h / 2,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
    )


def draw_frame(fig, histories: List[HistoryPath], frame: int, results: pd.DataFrame):
    fig.clear()
    gs = fig.add_gridspec(2, 2, height_ratios=[1.8, 1.05], width_ratios=[1.35, 1.0])
    ax = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-4.2, 4.2)
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.set_xlabel("Observable coordinate 1", fontsize=10)
    ax.set_ylabel("Observable coordinate 2", fontsize=10)
    ax.set_title(
        "V997 Genesis Pin Publication Audit\nSame observable state can arise from incompatible histories",
        fontsize=14,
        fontweight="bold",
        pad=12,
    )

    ax.add_patch(
        Circle(
            COMMON_VISIBLE_STATE,
            0.52,
            facecolor="#9ecae1",
            edgecolor="#08519c",
            alpha=0.65,
            zorder=2,
        )
    )
    ax.text(
        0,
        -0.72,
        "same visible\nstate",
        ha="center",
        va="top",
        fontsize=10,
        color="#08306b",
        fontweight="bold",
    )

    k = min(frame, N_STEPS - 1)
    label_offsets = {
        "Legitimate history": (-0.4, 0.45),
        "Forked counterfeit": (-0.4, -0.6),
        "Self-defined counterfeit": (0.25, 0.45),
        "Quorum-failed replay": (0.25, -0.6),
        "Tampered append chain": (0.0, 0.35),
    }

    for h in histories:
        pts = h.points
        ax.plot(pts[: k + 1, 0], pts[: k + 1, 1], color=h.color, linewidth=3.0, alpha=0.85, zorder=3)
        ax.scatter(pts[k, 0], pts[k, 1], color=h.color, s=125, edgecolor="white", linewidth=1.3, zorder=5)
        dx, dy = label_offsets[h.name]
        ax.text(pts[0, 0] + dx, pts[0, 1] + dy, h.name, color=h.color, fontsize=9.5, fontweight="bold", ha="center", zorder=6)

    if frame >= N_STEPS:
        y_positions = {
            "Legitimate history": 1.45,
            "Forked counterfeit": -1.45,
            "Self-defined counterfeit": 0.55,
            "Quorum-failed replay": -0.55,
            "Tampered append chain": 2.35,
        }
        for h in histories:
            symbol = "ACCEPT" if h.accepted_with_genesis_pin else "REJECT"
            yoff = y_positions[h.name]
            ax.text(1.55, yoff, symbol, color=h.color, fontsize=11, fontweight="bold", va="center")
            ax.plot([0.5, 1.25], [0, yoff], color=h.color, alpha=0.55, linestyle=":", linewidth=2)

    ax2.axis("off")
    ax2.text(0.5, 1.05, "Genesis Pin Filter", transform=ax2.transAxes, ha="center", fontsize=16, fontweight="bold")
    ax2.text(0.5, 0.96, "Minimal non-circular initialization boundary", transform=ax2.transAxes, ha="center", fontsize=10)

    draw_box(ax2, (0.05, 0.76), 0.9, 0.14, "1. Same visible state", fc="#eff3ff", ec="#3182bd", fontsize=10, weight="bold")
    draw_box(ax2, (0.05, 0.59), 0.9, 0.14, "2. Pinned genesis registry\nW1,W2,W3,W4", fc="#edf8e9", ec="#238b45", fontsize=10, weight="bold")
    draw_box(ax2, (0.05, 0.42), 0.9, 0.14, "3. Pinned anchor root\nGENESIS_ANCHOR_000", fc="#eff3ff", ec="#3182bd", fontsize=10, weight="bold")
    draw_box(ax2, (0.05, 0.25), 0.9, 0.14, "4. Witness quorum\n≥ 3 pinned witnesses", fc="#fff7bc", ec="#d95f0e", fontsize=10, weight="bold")
    draw_box(ax2, (0.05, 0.08), 0.9, 0.14, "5. Append-only chain\nno rollback / tamper", fc="#f7f7f7", ec="#636363", fontsize=10, weight="bold")

    ax3.axis("off")
    ax3.text(0.02, 0.93, "Certification Outcomes", transform=ax3.transAxes, fontsize=13, fontweight="bold")

    x_cols = [0.02, 0.25, 0.39, 0.53, 0.67, 0.79, 0.91]
    headers = ["History", "Visible", "Registry", "Root", "Quorum", "Chain", "With Pin"]
    for x, header in zip(x_cols, headers):
        ax3.text(x, 0.76, header, transform=ax3.transAxes, fontsize=9.5, fontweight="bold", ha="left")

    y0 = 0.60
    color_map = {h.name: h.color for h in histories}
    for i, row in results.iterrows():
        y = y0 - i * 0.125
        color = color_map[row["history"]]
        ax3.text(x_cols[0], y, row["history"], transform=ax3.transAxes, fontsize=9.2, color=color, fontweight="bold", ha="left")

        cols = [
            "same_visible_state",
            "genesis_registry_matches",
            "genesis_root_matches",
            "witness_quorum_all_steps",
            "append_only_chain_valid",
        ]
        for j, col in enumerate(cols, start=1):
            ax3.text(x_cols[j], y, "YES" if row[col] else "NO", transform=ax3.transAxes, fontsize=9.2, ha="left")

        accepted = row["accepted_with_genesis_pin"]
        ax3.text(
            x_cols[6],
            y,
            "ACCEPT" if accepted else "REJECT",
            transform=ax3.transAxes,
            fontsize=9.2,
            color="#238b45" if accepted else "#de2d26",
            fontweight="bold",
            ha="left",
        )

    bottom = (
        "Audit result: same observable state accepts every path under visible-state equivalence. "
        "Genesis Pin accepts only the path with pinned registry, pinned root, quorum, and append-only continuity."
    )
    ax3.text(
        0.5,
        -0.08,
        bottom,
        transform=ax3.transAxes,
        ha="center",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#f7f7f7", edgecolor="#999999"),
    )

    fig.subplots_adjust(hspace=0.38, wspace=0.10)


# ==============================================================================
# PUBLICATION DOCS
# ==============================================================================

def write_claim_boundaries():
    text = """# V997 Claim Boundaries

## Allowed Claim

In the tested recoverability stack, same observable state does not certify legitimate history.

A Genesis Pin converts legitimacy from a final-state property into a recoverable-history property by requiring:

1. same visible state,
2. pinned genesis registry,
3. pinned genesis anchor root,
4. quorum witness participation,
5. append-only chain continuity,
6. rejection of circular bootstrap/self-defined origins.

## Not Claimed

This artifact does not claim:

- universal mathematical proof,
- production cryptographic security,
- physical spacetime,
- physical time,
- General Relativity,
- Einstein equations,
- physical curvature,
- metaphysical origin proof.

## Correct Public Sentence

Same observable state is insufficient for legitimacy in the tested recoverability stack; legitimacy requires recoverable history anchored to pinned genesis.
"""
    (OUT / "CLAIM_BOUNDARIES.md").write_text(text)


def write_protocol():
    text = """# V997 Protocol

## Objective

Demonstrate that visible-state equivalence underdetermines legitimate history.

## Procedure

1. Construct five histories.
2. Force all histories to converge to the same visible final state.
3. Certify once with visible-state-only acceptance.
4. Certify again with Genesis Pin acceptance.
5. Report which paths pass or fail and why.

## Histories

1. Legitimate history
2. Forked counterfeit
3. Self-defined counterfeit
4. Quorum-failed replay
5. Tampered append chain

## Pass Condition

The audit passes if:

- all histories are accepted without Genesis Pin,
- only the legitimate history is accepted with Genesis Pin,
- every rejected path has a specific rejection reason.
"""
    (OUT / "PROTOCOL.md").write_text(text)


def write_report(results: pd.DataFrame, manifest: Dict[str, Any], layer_stack: pd.DataFrame):
    pivot = results[
        [
            "history",
            "same_visible_state",
            "genesis_registry_matches",
            "genesis_root_matches",
            "witness_quorum_all_steps",
            "append_only_chain_valid",
            "circular_bootstrap_detected",
            "accepted_without_genesis_pin",
            "accepted_with_genesis_pin",
            "reason",
        ]
    ]

    report = f"""# V997 Genesis Pin Publication Audit

## Executive Summary

This full-stack audit tests whether same observable state is sufficient to certify legitimate history in the V923 → V995 recoverability stack.

It is not sufficient.

All five histories converge to the same final observable state. Under visible-state-only certification, all five are accepted. Under Genesis Pin certification, only one is accepted.

```text
Histories tested: {manifest["histories_tested"]}
Accepted without Genesis Pin: {manifest["accepted_without_genesis_pin"]}
Accepted with Genesis Pin: {manifest["accepted_with_genesis_pin"]}
```

## Core Result

Same observable state does not certify legitimate history in the tested recoverability stack.

Genesis Pin changes the certification object:

```text
from: final-state equivalence
to: recoverable-history legitimacy
```

## Genesis Pin Requirements

A path is accepted only if it satisfies:

1. same visible state,
2. pinned genesis registry,
3. pinned genesis anchor root,
4. witness quorum,
5. append-only chain continuity,
6. no circular bootstrap/self-defined origin.

## V923 / V994 / V995 Layer Stack

{layer_stack.to_markdown(index=False)}

## Certification Table

{pivot.to_markdown(index=False)}

## Interpretation

The audit demonstrates a modeled counterexample to visible-state-only legitimacy.

Five histories land on the same visible state. They are observationally equivalent at the final coordinate. But their generative histories are not equivalent.

The Genesis Pin separates legitimate continuity from:

- forked anchors,
- self-defined registries,
- quorum-failed replays,
- tampered append chains.

## Claim Boundary

This is a modeled full-stack audit demonstration.

It does not claim universal theorem status, production cryptographic security, physical spacetime, physical time, General Relativity, Einstein equations, or physical curvature.

## Correct Public Claim

Same observable state is insufficient for legitimacy in the tested recoverability stack; legitimacy requires recoverable history anchored to pinned genesis.
"""
    (OUT / "V997_GENESIS_PIN_PUBLICATION_AUDIT.md").write_text(report)


def write_readme(manifest: Dict[str, Any]):
    text = f"""# V997 Genesis Pin Publication Audit

## Run Summary

```json
{json.dumps(manifest, indent=2)}
```

## Files

- `v997_genesis_pin_publication_audit.py`
- `V997_GENESIS_PIN_PUBLICATION_AUDIT.md`
- `CLAIM_BOUNDARIES.md`
- `PROTOCOL.md`
- `MANIFEST.json`
- `v997_layer_stack.csv`
- `v997_genesis_pin_results.csv`
- `v997_genesis_pin_result.json`
- `v997_genesis_pin_publication_audit.mp4`
- `v997_genesis_pin_publication_audit.gif`
- `v997_genesis_pin_final_frame.png`
- `v997_source.zip`

## Correct Claim

Same observable state is insufficient for legitimacy in the tested recoverability stack; legitimacy requires recoverable history anchored to pinned genesis.
"""
    (OUT / "README.md").write_text(text)


def write_source_zip(script_path: Path):
    zip_path = OUT / "v997_source.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(script_path, arcname=script_path.name)


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    histories = build_histories()
    results = make_results(histories)
    layer_stack = make_layer_stack()
    manifest = result_manifest(results)

    results.to_csv(OUT / "v997_genesis_pin_results.csv", index=False)
    layer_stack.to_csv(OUT / "v997_layer_stack.csv", index=False)

    (OUT / "v997_genesis_pin_result.json").write_text(json.dumps(manifest, indent=2))
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))

    write_claim_boundaries()
    write_protocol()
    write_report(results, manifest, layer_stack)
    write_readme(manifest)

    # copy source into output folder and source zip
    local_script = Path(__file__).resolve()
    copied_script = OUT / "v997_genesis_pin_publication_audit.py"
    if local_script != copied_script.resolve():
        copied_script.write_text(local_script.read_text())
    write_source_zip(copied_script)

    # visuals
    fig = plt.figure(figsize=(14.5, 9.3), dpi=150)
    total_frames = N_STEPS + 4

    def update(frame):
        draw_frame(fig, histories, frame, results)
        return []

    anim = FuncAnimation(fig, update, frames=total_frames, interval=1000 / FPS, blit=False)

    try:
        anim.save(
            OUT / "v997_genesis_pin_publication_audit.mp4",
            writer=FFMpegWriter(fps=FPS, bitrate=2600),
        )
    except Exception as e:
        print(f"MP4 save failed: {e}")

    try:
        anim.save(
            OUT / "v997_genesis_pin_publication_audit.gif",
            writer=PillowWriter(fps=FPS),
        )
    except Exception as e:
        print(f"GIF save failed: {e}")

    draw_frame(fig, histories, total_frames - 1, results)
    fig.savefig(OUT / "v997_genesis_pin_final_frame.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
