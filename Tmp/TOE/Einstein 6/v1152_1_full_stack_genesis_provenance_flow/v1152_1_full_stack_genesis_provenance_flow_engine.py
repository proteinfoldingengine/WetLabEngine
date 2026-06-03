#!/usr/bin/env python3
"""
V1152.1 Full-Stack Genesis → Provenance → Geometry Flow Engine

Purpose
-------
Upgrade V1152 from a labeled visualization into a full-stack computed
certification engine.

V1152 issue fixed:
    The old dimensionless margin was assigned by mode.

V1152.1 fix:
    The certification margin is computed from:

        Ω / geometry similarity
        + Genesis Pin provenance
        + source-flow closure

Then the 3D trajectories are annotated by earned certification status.

Primitive guardrail
-------------------
No physical-time primitive is used. The model uses ordered slices,
retained-order sequence, and provenance order.

Claim boundary
--------------
This is a model-native recoverability / provenance / geometry certification
engine and visualization.

It does NOT claim:
    physical spacetime,
    physical time,
    physical GR,
    Einstein equations,
    physical curvature,
    production cryptographic security.

It DOES test:
    whether visually similar 3D geometry/Ω flows are fully certified only when
    geometry resemblance, pinned provenance, and source-flow closure all pass.

Outputs
-------
v1152_1_full_stack_results.csv
v1152_1_summary.json
v1152_1_static_3d.png
v1152_1_certification_panels.png
v1152_1_genesis_provenance_flow.gif
V1152_1_FULL_STACK_REPORT.md
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Tuple, List, Dict, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# ==============================================================================
# CONFIG
# ==============================================================================

OUT = Path("v1152_1_full_stack_outputs")
OUT.mkdir(exist_ok=True)

SEED = 11521
RNG = np.random.default_rng(SEED)

N_POINTS = 360
N_FRAMES = 90
EPS = 1e-9

PINNED_GENESIS_REGISTRY = ("W1", "W2", "W3", "W4")
PINNED_GENESIS_ROOT = "ROOT:GENESIS_ANCHOR_000"
QUORUM = 3

OMEGA_SIM_THRESHOLD = 0.985
K_SIGMA = 3.0

MODES = [
    "valid_label_transported",
    "raw_c_only_shift",
    "retained_order_shuffle",
    "source_event_shuffle",
    "valid_prefix_invalid_suffix",
    "geometry_matched_counterfeit",
    "genesis_valid_source_shuffled",
]


# ==============================================================================
# GENESIS PIN / PROVENANCE ENGINE
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


def append_chain_valid(root: str, registry: Tuple[str, ...], events: List[str], witnesses: List[Tuple[str, ...]], roots: List[str]) -> bool:
    if len(roots) != len(events) + 1 or roots[0] != root:
        return False
    cur = root
    for i, (ev, wit) in enumerate(zip(events, witnesses), start=1):
        cur = chain_transition(cur, registry, i, ev, wit)
        if roots[i] != cur:
            return False
    return True


def genesis_pin_passes(registry: Tuple[str, ...], root: str, events: List[str], witnesses: List[Tuple[str, ...]], roots: List[str]) -> bool:
    return (
        registry_matches(registry)
        and root_matches(root)
        and all(quorum_valid(w) for w in witnesses)
        and append_chain_valid(root, registry, events, witnesses, roots)
        and not circular_bootstrap_detected(registry, root)
    )


@dataclass
class History:
    mode: str
    registry: Tuple[str, ...]
    root: str
    events: List[str]
    witnesses: List[Tuple[str, ...]]
    roots: List[str]


def make_history(mode: str) -> History:
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
    weak_witnesses = [("W1", "X9", "Y9") for _ in events]
    attacker_witnesses = [("A1", "A2", "A3") for _ in events]

    registry = PINNED_GENESIS_REGISTRY
    root = PINNED_GENESIS_ROOT
    witnesses = pinned_witnesses
    tamper_at = None

    if mode in ["raw_c_only_shift", "geometry_matched_counterfeit"]:
        registry = ("A1", "A2", "A3", "A4")
        root = "ROOT:SELF_DEFINED_OR_COUNTERFEIT"
        witnesses = attacker_witnesses
    elif mode == "retained_order_shuffle":
        # provenance is pinned, but ordered sequence will be broken by event order
        events = list(reversed(events))
    elif mode == "source_event_shuffle":
        registry = PINNED_GENESIS_REGISTRY
        root = PINNED_GENESIS_ROOT
        witnesses = pinned_witnesses
    elif mode == "valid_prefix_invalid_suffix":
        tamper_at = 5
    elif mode == "genesis_valid_source_shuffled":
        registry = PINNED_GENESIS_REGISTRY
        root = PINNED_GENESIS_ROOT
        witnesses = pinned_witnesses
    elif mode == "valid_label_transported":
        pass
    else:
        raise ValueError(mode)

    roots = build_chain(root, registry, events, witnesses, tamper_at=tamper_at)
    return History(mode, registry, root, events, witnesses, roots)


# ==============================================================================
# GEOMETRY / SOURCE / FLOW ENGINE
# ==============================================================================

def base_curve(n: int = N_POINTS) -> Dict[str, np.ndarray]:
    """
    Base 3D genesis→provenance→geometry response path.
    """
    s = np.linspace(0, 2 * np.pi, n)

    x = 1.35 * np.cos(s) + 0.45 * np.cos(2.3 * s + 0.3)
    y = 1.05 * np.sin(s) + 0.40 * np.sin(1.7 * s - 0.5)
    z = 0.32 * np.sin(2.1 * s) + 0.22 * np.cos(3.3 * s + 0.2)

    # Source and flow fields live along the ordered path.
    source = 0.85 * np.sin(s + 0.2) + 0.35 * np.cos(2.4 * s)
    flow = np.gradient(z, s) + 0.20 * np.sin(1.5 * s)

    # Ω-like geometry scalar along the path.
    psi = -0.28 * source + 0.12 * flow
    omega = np.exp(-psi)

    return dict(s=s, x=x, y=y, z=z, source=source, flow=flow, psi=psi, omega=omega)


def transform_curve(base: Dict[str, np.ndarray], mode: str, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    b = {k: np.array(v, copy=True) for k, v in base.items()}
    s = b["s"]

    if mode == "valid_label_transported":
        # A legitimate smooth label-transported deformation.
        phase = 0.15
        b["x"] = b["x"] + 0.08 * np.sin(s + phase)
        b["y"] = b["y"] + 0.06 * np.cos(1.3 * s - phase)
        b["z"] = b["z"] + 0.03 * np.sin(2.0 * s)
        b["source"] = b["source"] + 0.02 * np.sin(s)
        b["flow"] = b["flow"] + 0.02 * np.cos(2*s)

    elif mode == "raw_c_only_shift":
        # Similar geometry but raw coordinate shift breaks source identity.
        b["x"] = b["x"] + 0.35
        b["y"] = b["y"] - 0.10
        b["z"] = b["z"] + 0.04
        b["source"] = np.roll(b["source"], 33)
        b["flow"] = b["flow"] * 0.55 + 0.15 * rng.normal(size=len(s))

    elif mode == "retained_order_shuffle":
        # Same geometry set, wrong retained order.
        perm = np.r_[np.arange(len(s)//2, len(s)), np.arange(0, len(s)//2)]
        for key in ["x", "y", "z", "source", "flow"]:
            b[key] = b[key][perm]

    elif mode == "source_event_shuffle":
        # Geometry path preserved, source events shuffled.
        b["source"] = rng.permutation(b["source"])
        b["flow"] = rng.permutation(b["flow"])

    elif mode == "valid_prefix_invalid_suffix":
        # Prefix is valid, suffix spliced.
        cut = int(0.62 * len(s))
        b["x"][cut:] = b["x"][cut:] + 0.12 * np.sin(4*s[cut:])
        b["y"][cut:] = b["y"][cut:] - 0.16 * np.cos(3*s[cut:])
        b["source"][cut:] = np.roll(b["source"][cut:], 41)
        b["flow"][cut:] = np.roll(b["flow"][cut:], 23)

    elif mode == "geometry_matched_counterfeit":
        # Keep geometry very close, break provenance/source relation.
        b["x"] = b["x"] + 0.015 * np.sin(5*s)
        b["y"] = b["y"] + 0.015 * np.cos(4*s)
        b["z"] = b["z"] + 0.010 * np.sin(3*s)
        b["source"] = np.roll(b["source"], 61)
        b["flow"] = -0.25 * b["flow"] + 0.30 * np.sin(2.8*s)

    elif mode == "genesis_valid_source_shuffled":
        # Valid Genesis Pin but source-flow closure should fail.
        b["source"] = rng.permutation(b["source"])
        b["flow"] = np.roll(b["flow"], 77)

    else:
        raise ValueError(mode)

    # recompute Ω from resulting source/flow for certification.
    b["psi"] = -0.28 * b["source"] + 0.12 * b["flow"]
    b["omega"] = np.exp(-b["psi"])

    return b


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a.ravel(), b.ravel()) / (np.linalg.norm(a.ravel()) * np.linalg.norm(b.ravel()) + EPS))


def corr(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) < EPS or np.std(b) < EPS:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def rms(a: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.asarray(a) ** 2)))


def closure_features(curve: Dict[str, np.ndarray]) -> Dict[str, float]:
    """
    Source-flow closure diagnostics along the ordered path.

    residual: fixed-law residual from legitimate calibration
    source_alignment: corr(source, geometry response)
    flow_alignment: corr(flow, geometry derivative)
    """
    x, y, z = curve["x"], curve["y"], curve["z"]
    source, flow = curve["source"], curve["flow"]
    s = curve["s"]

    geom_response = np.sqrt(x*x + y*y) + 0.35 * z
    dz = np.gradient(z, s)

    source_alignment = corr(source, geom_response)
    flow_alignment = corr(flow, dz)

    return dict(
        geom_response=geom_response,
        dz=dz,
        source_alignment=source_alignment,
        flow_alignment=flow_alignment,
    )


def calibrate_legitimate_thresholds(valid_curves: List[Dict[str, np.ndarray]]) -> Dict[str, float]:
    """
    Calibrate source-flow law from legitimate curves only.
    """
    residuals = []
    src_align = []
    flow_align = []

    # Global simple law from legitimate references:
    # geom_response ≈ b0 + b1*source + b2*flow
    ys = []
    xs = []
    for c in valid_curves:
        f = closure_features(c)
        y = f["geom_response"]
        X = np.column_stack([np.ones(len(y)), c["source"], c["flow"]])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        pred = X @ beta
        residuals.append(rms(y - pred))
        src_align.append(f["source_alignment"])
        flow_align.append(f["flow_alignment"])

    return {
        "B_like_mean": float(np.mean(residuals)),
        "B_like_std": float(np.std(residuals) + EPS),
        "B_like_threshold": float(np.mean(residuals) + K_SIGMA * (np.std(residuals) + EPS)),
        "source_alignment_mean": float(np.mean(src_align)),
        "source_alignment_std": float(np.std(src_align) + EPS),
        "source_alignment_min": float(np.mean(src_align) - K_SIGMA * (np.std(src_align) + EPS)),
        "flow_alignment_mean": float(np.mean(flow_align)),
        "flow_alignment_std": float(np.std(flow_align) + EPS),
        "flow_alignment_min": float(np.mean(flow_align) - K_SIGMA * (np.std(flow_align) + EPS)),
    }


def certify_curve(curve: Dict[str, np.ndarray], ref_curve: Dict[str, np.ndarray], history: History, thresholds: Dict[str, float]) -> Dict[str, Any]:
    omega_similarity = cosine(curve["omega"], ref_curve["omega"])
    geometry_similarity = cosine(np.column_stack([curve["x"], curve["y"], curve["z"]]),
                                 np.column_stack([ref_curve["x"], ref_curve["y"], ref_curve["z"]]))

    genesis_pass = genesis_pin_passes(history.registry, history.root, history.events, history.witnesses, history.roots)

    f = closure_features(curve)
    y = f["geom_response"]
    X = np.column_stack([np.ones(len(y)), curve["source"], curve["flow"]])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    pred = X @ beta
    B_like_rms = rms(y - pred)

    residual_certified = B_like_rms <= thresholds["B_like_threshold"]
    source_alignment_certified = f["source_alignment"] >= thresholds["source_alignment_min"]
    flow_alignment_certified = f["flow_alignment"] >= thresholds["flow_alignment_min"]

    closure_certified = bool(residual_certified and source_alignment_certified and flow_alignment_certified)
    omega_certified = omega_similarity >= OMEGA_SIM_THRESHOLD

    full_certified = bool(omega_certified and genesis_pass and closure_certified)

    # Dimensionless earned margin, not assigned by mode.
    # Positive means above the certification boundary.
    omega_margin = (omega_similarity - OMEGA_SIM_THRESHOLD) / max(1 - OMEGA_SIM_THRESHOLD, EPS)
    genesis_margin = 1.0 if genesis_pass else -1.0
    closure_margin = min(
        (thresholds["B_like_threshold"] - B_like_rms) / (thresholds["B_like_threshold"] + EPS),
        (f["source_alignment"] - thresholds["source_alignment_min"]) / (abs(thresholds["source_alignment_min"]) + EPS),
        (f["flow_alignment"] - thresholds["flow_alignment_min"]) / (abs(thresholds["flow_alignment_min"]) + EPS),
    )
    dimensionless_margin = float(np.mean([omega_margin, genesis_margin, closure_margin]))

    return {
        "mode": history.mode,
        "omega_similarity": float(omega_similarity),
        "geometry_similarity": float(geometry_similarity),
        "omega_certified": bool(omega_certified),
        "genesis_pin_pass": bool(genesis_pass),
        "B_like_rms": float(B_like_rms),
        "source_alignment": float(f["source_alignment"]),
        "flow_alignment": float(f["flow_alignment"]),
        "residual_certified": bool(residual_certified),
        "source_alignment_certified": bool(source_alignment_certified),
        "flow_alignment_certified": bool(flow_alignment_certified),
        "closure_certified": bool(closure_certified),
        "full_certified": bool(full_certified),
        "omega_margin": float(omega_margin),
        "genesis_margin": float(genesis_margin),
        "closure_margin": float(closure_margin),
        "dimensionless_margin": dimensionless_margin,
        "registry_matches": bool(registry_matches(history.registry)),
        "root_matches": bool(root_matches(history.root)),
        "quorum_valid": bool(all(quorum_valid(w) for w in history.witnesses)),
        "append_valid": bool(append_chain_valid(history.root, history.registry, history.events, history.witnesses, history.roots)),
        "circular_bootstrap_detected": bool(circular_bootstrap_detected(history.registry, history.root)),
    }


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def plot_static(curves: Dict[str, Dict[str, np.ndarray]], metrics: pd.DataFrame):
    fig = plt.figure(figsize=(13, 9))
    ax = fig.add_subplot(111, projection="3d")

    colors = {
        "valid_label_transported": "tab:blue",
        "raw_c_only_shift": "tab:orange",
        "retained_order_shuffle": "tab:green",
        "source_event_shuffle": "tab:red",
        "valid_prefix_invalid_suffix": "tab:purple",
        "geometry_matched_counterfeit": "tab:brown",
        "genesis_valid_source_shuffled": "tab:pink",
    }

    for mode, c in curves.items():
        row = metrics[metrics["mode"] == mode].iloc[0]
        label = f"{mode} | margin={row['dimensionless_margin']:.2f} | full={int(row['full_certified'])}"
        ax.plot(c["x"], c["y"], c["z"], color=colors.get(mode, None), lw=2.0, label=label)
        ax.scatter([c["x"][0]], [c["y"][0]], [c["z"][0]], color=colors.get(mode, None), s=45)

    ax.set_title("V1152.1 Full-Stack Genesis Provenance Flow Engine\ncomputed certification: Ω + Genesis Pin + source-flow closure")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z / response")
    ax.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig(OUT / "v1152_1_static_3d.png", dpi=180)
    plt.close(fig)


def plot_panels(metrics: pd.DataFrame):
    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    modes = metrics["mode"].tolist()
    x = np.arange(len(modes))

    axs[0, 0].bar(x, metrics["omega_similarity"])
    axs[0, 0].axhline(OMEGA_SIM_THRESHOLD, linestyle="--")
    axs[0, 0].set_title("Ω similarity")
    axs[0, 0].set_ylim(0.8, 1.01)

    axs[0, 1].bar(x, metrics["source_alignment"])
    axs[0, 1].set_title("Source / geometry alignment")

    axs[1, 0].bar(x, metrics["closure_margin"])
    axs[1, 0].axhline(0, linestyle="--")
    axs[1, 0].set_title("Computed closure margin")

    axs[1, 1].bar(x, metrics["dimensionless_margin"])
    axs[1, 1].axhline(0, linestyle="--")
    axs[1, 1].set_title("Earned full-stack margin")

    for ax in axs.ravel():
        ax.set_xticks(x)
        ax.set_xticklabels(modes, rotation=30, ha="right")
        ax.grid(True, alpha=0.2)

    plt.tight_layout()
    fig.savefig(OUT / "v1152_1_certification_panels.png", dpi=180)
    plt.close(fig)


def make_animation(curves: Dict[str, Dict[str, np.ndarray]], metrics: pd.DataFrame):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    colors = {
        "valid_label_transported": "tab:blue",
        "raw_c_only_shift": "tab:orange",
        "retained_order_shuffle": "tab:green",
        "source_event_shuffle": "tab:red",
        "valid_prefix_invalid_suffix": "tab:purple",
        "geometry_matched_counterfeit": "tab:brown",
        "genesis_valid_source_shuffled": "tab:pink",
    }

    modes = list(curves.keys())
    lines = {}
    dots = {}

    for mode in modes:
        line, = ax.plot([], [], [], color=colors.get(mode, None), lw=2, label=mode)
        dot = ax.scatter([], [], [], color=colors.get(mode, None), s=45)
        lines[mode] = line
        dots[mode] = dot

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.2, 2.2)
    ax.set_zlim(-1.0, 1.0)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("response")
    ax.legend(loc="upper left", fontsize=7)

    def update(frame):
        ax.set_title(f"V1152.1 Genesis→Provenance→Geometry Flow | ordered frame {frame}/{N_FRAMES-1}")
        k = max(2, int((frame + 1) / N_FRAMES * N_POINTS))
        for mode in modes:
            c = curves[mode]
            lines[mode].set_data(c["x"][:k], c["y"][:k])
            lines[mode].set_3d_properties(c["z"][:k])
            dots[mode]._offsets3d = ([c["x"][k-1]], [c["y"][k-1]], [c["z"][k-1]])
        return list(lines.values())

    ani = FuncAnimation(fig, update, frames=N_FRAMES, interval=70, blit=False)
    ani.save(OUT / "v1152_1_genesis_provenance_flow.gif", writer=PillowWriter(fps=12))
    plt.close(fig)


# ==============================================================================
# REPORT
# ==============================================================================

def write_report(metrics: pd.DataFrame, summary: Dict[str, Any], thresholds: Dict[str, float]):
    md = f"""# V1152.1 Full-Stack Genesis Provenance Flow Engine

## Purpose

V1152.1 upgrades the 3D visualization into a computed certification engine.

The prior version visually labeled margins by mode. This version earns margins from:

```text
Ω similarity
+ Genesis Pin
+ source-flow closure
```

## Summary

```json
{json.dumps(summary, indent=2)}
```

## Legitimate Calibration Thresholds

```json
{json.dumps(thresholds, indent=2)}
```

## Metrics

{metrics.to_markdown(index=False)}

## Certification Stack

```text
1. Ω similarity
   Tests geometry / conformal resemblance.

2. Genesis Pin
   Tests provenance legitimacy:
   pinned registry, pinned root, quorum, append-only chain, no circular bootstrap.

3. Source-flow closure
   Tests whether the source and flow fields remain aligned with the geometry response.

4. Full certification
   full_certified = Ω similarity AND Genesis Pin AND source-flow closure
```

## What Changed from V1152

The `dimensionless_margin` is no longer assigned by mode.

It is computed as an earned score from:

```text
omega_margin
genesis_margin
closure_margin
```

## Claim Boundary

Allowed:

```text
V1152.1 provides a runnable 3D engine where flow trajectories are certified by
computed Ω similarity, Genesis Pin provenance, and source-flow closure.
```

Not allowed:

```text
physical spacetime
physical time
General Relativity
Einstein equations
physical curvature
production cryptographic security
```
"""
    (OUT / "V1152_1_FULL_STACK_REPORT.md").write_text(md)


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    rng = np.random.default_rng(SEED)
    base = base_curve()

    # Generate several legitimate samples for threshold calibration.
    valid_samples = []
    for i in range(30):
        r = np.random.default_rng(SEED + i)
        valid_samples.append(transform_curve(base, "valid_label_transported", r))
    thresholds = calibrate_legitimate_thresholds(valid_samples)

    curves = {}
    histories = {}
    rows = []

    # Use a stable reference valid curve.
    ref_rng = np.random.default_rng(SEED + 999)
    ref_curve = transform_curve(base, "valid_label_transported", ref_rng)

    for i, mode in enumerate(MODES):
        local_rng = np.random.default_rng(SEED + 1000 + i)
        history = make_history(mode)
        curve = transform_curve(base, mode, local_rng)
        cert = certify_curve(curve, ref_curve, history, thresholds)
        curves[mode] = curve
        histories[mode] = history
        rows.append(cert)

    metrics = pd.DataFrame(rows)
    metrics.to_csv(OUT / "v1152_1_full_stack_results.csv", index=False)

    summary = {
        "document_id": "V1152_1_FULL_STACK_GENESIS_PROVENANCE_FLOW_ENGINE",
        "status": "computed full-stack 3D engine generated",
        "seed": SEED,
        "frames": N_FRAMES,
        "points": N_POINTS,
        "modes": MODES,
        "full_certified_modes": metrics.loc[metrics["full_certified"], "mode"].tolist(),
        "geometry_only_certified_count": int(metrics["omega_certified"].sum()),
        "genesis_pin_pass_count": int(metrics["genesis_pin_pass"].sum()),
        "closure_certified_count": int(metrics["closure_certified"].sum()),
        "full_certified_count": int(metrics["full_certified"].sum()),
        "invalid_full_certified_count": int(((metrics["mode"] != "valid_label_transported") & metrics["full_certified"]).sum()),
        "claim_boundary": "Model-native 3D certification engine; no physical GR/spacetime/Einstein claim.",
    }
    (OUT / "v1152_1_summary.json").write_text(json.dumps(summary, indent=2))

    plot_static(curves, metrics)
    plot_panels(metrics)
    make_animation(curves, metrics)
    write_report(metrics, summary, thresholds)

    # Source zip
    source_zip = OUT / "v1152_1_source.zip"
    if source_zip.exists():
        source_zip.unlink()
    with zipfile.ZipFile(source_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(Path(__file__), arcname=Path(__file__).name)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
