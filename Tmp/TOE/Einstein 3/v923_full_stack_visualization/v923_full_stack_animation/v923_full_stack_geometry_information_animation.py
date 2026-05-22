#!/usr/bin/env python3
"""
V923 Full-Stack Animated Simulation
===================================

Creates a data-faithful MP4 animation for the V923 result:

    E_OSC / endpoint-path observables define a geometry-like quotient basin.
    Observable-only closure is source-degenerate.
    A ternary source-role primitive is the minimal exact information lift.

This script is not a synthetic DALL-E/graphic storyboard.
It loads the actual V921 endpoint cohort and recomputes the V923 closure ladder.

Default input:
    /mnt/data/v921_ternary_source_role_primitive_blind_regeneration_audit/
    v921_ternary_endpoint_scores.csv

Outputs:
    v923_full_stack_geometry_information_animation.mp4
    v923_full_stack_geometry_information_animation.gif   (fallback, optional)
    v923_animation_lift_ladder.csv
    v923_animation_result.json

Claim boundary:
    - Z is a discrete source-role information index, not physical space/time.
    - This is not a GR/EFE/physical-spacetime proof.
    - This is not a 1/f/CMB/black-hole claim.
"""

from __future__ import annotations

import argparse
import json
import shutil
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.patches import Circle, FancyBboxPatch


DEFAULT_INPUT = Path(
    "/mnt/data/v921_ternary_source_role_primitive_blind_regeneration_audit/"
    "v921_ternary_endpoint_scores.csv"
)
DEFAULT_OUT = Path("/mnt/data/v923_full_stack_animation_run")

SOURCE_ROLE_MAP = {
    "active_source": "source_active_role",
    "passive_source": "source_basin_eligible_nonactive_role",
    "structured_source": "source_basin_eligible_nonactive_role",
    "rejected_or_broken_source": "source_rejected_or_broken_role",
}

ROLE_Z = {
    "source_rejected_or_broken_role": 0.0,
    "source_basin_eligible_nonactive_role": 1.0,
    "source_active_role": 2.0,
}

ROLE_COLORS = {
    "source_rejected_or_broken_role": "#ff1744",
    "source_basin_eligible_nonactive_role": "#ffea00",
    "source_active_role": "#39ff14",
}

ROLE_LABELS = {
    "source_rejected_or_broken_role": "Broken / Rejected",
    "source_basin_eligible_nonactive_role": "Basin-Eligible Nonactive",
    "source_active_role": "Active Repair",
}

CLASS_ORDER = [
    "source_rejected_or_broken_role",
    "source_basin_eligible_nonactive_role",
    "source_active_role",
]


# ---------------------------------------------------------------------
# Proof / closure functions
# ---------------------------------------------------------------------

def canonical_partitions(items: List[str], k: int) -> Iterable[Dict[str, str]]:
    """Generate all onto partitions of items into k canonical symbols."""
    n = len(items)
    assignments = [0] * n

    if k == 1:
        yield {item: "symbol_0" for item in items}
        return

    def rec(i: int, max_label: int):
        if i == n:
            if len(set(assignments)) == k:
                yield {items[j]: f"symbol_{assignments[j]}" for j in range(n)}
            return

        for lab in range(0, min(max_label + 2, k)):
            assignments[i] = lab
            yield from rec(i + 1, max(max_label, lab))

    assignments[0] = 0
    yield from rec(1, 0)


def majority_lookup_predict(
    df: pd.DataFrame,
    key_cols: List[str],
    true_col: str = "true_class",
) -> Tuple[pd.Series, pd.DataFrame, Dict[str, int]]:
    """Predict true class by majority lookup within keys and return collision diagnostics."""
    lookup = {}
    collision_rows = 0
    collision_groups = 0
    collision_records = []

    for key, g in df.groupby(key_cols, dropna=False):
        key_tuple = key if isinstance(key, tuple) else (key,)
        counts = g[true_col].value_counts()
        pred = counts.index[0]
        lookup[key_tuple] = pred

        if len(counts) > 1:
            collision_groups += 1
            collision_rows += len(g)
            collision_records.append({
                "key": repr(key),
                "rows": int(len(g)),
                "n_classes": int(len(counts)),
                "class_counts_json": json.dumps(counts.to_dict(), sort_keys=True),
                "majority_class": pred,
            })

    preds = []
    for _, row in df.iterrows():
        key_tuple = tuple(row[c] for c in key_cols)
        preds.append(lookup[key_tuple])

    preds = pd.Series(preds, index=df.index, name="pred_class")
    metrics = {
        "rows": int(len(df)),
        "accuracy": float((preds == df[true_col]).mean()),
        "false_cases": int((preds != df[true_col]).sum()),
        "collision_groups": int(collision_groups),
        "collision_rows": int(collision_rows),
    }
    return preds, pd.DataFrame(collision_records), metrics


def load_data(input_path: Path) -> Tuple[pd.DataFrame, str]:
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    df = pd.read_csv(input_path)
    required = {"source_family", "true_class"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    q_col = None
    for c in ["v921_observable_quotient", "observable_quotient", "quotient"]:
        if c in df.columns:
            q_col = c
            break
    if q_col is None:
        raise ValueError("Could not find v921_observable_quotient / observable_quotient column.")

    df = df.copy()
    df["source_role"] = df["source_family"].map(SOURCE_ROLE_MAP)
    if df["source_role"].isna().any():
        bad = sorted(df.loc[df["source_role"].isna(), "source_family"].unique())
        raise ValueError(f"Unrecognized source_family values: {bad}")

    return df, q_col


def evaluate_lift_ladder(df: pd.DataFrame, q_col: str) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Recompute observable-only, best binary, ternary, and full source lift."""
    source_families = sorted(df["source_family"].unique())

    obs_pred, obs_collisions, obs_metrics = majority_lookup_predict(df, [q_col])

    all_partitions = []
    best_by_k = {}

    for k in range(1, len(source_families) + 1):
        best = None
        for mapping in canonical_partitions(source_families, k):
            tmp = df.copy()
            tmp["source_symbol"] = tmp["source_family"].map(mapping)
            pred, collisions, metrics = majority_lookup_predict(tmp, [q_col, "source_symbol"])

            row = {
                "symbol_count": k,
                "accuracy": metrics["accuracy"],
                "false_cases": metrics["false_cases"],
                "collision_groups": metrics["collision_groups"],
                "collision_rows": metrics["collision_rows"],
                "mapping_json": json.dumps(mapping, sort_keys=True),
            }
            all_partitions.append(row)

            score = (row["accuracy"], -row["false_cases"], -row["collision_rows"])
            if best is None or score > best[0]:
                best = (score, row)
        best_by_k[k] = best[1]

    ternary_map = SOURCE_ROLE_MAP
    tmp_ternary = df.copy()
    tmp_ternary["source_symbol"] = tmp_ternary["source_family"].map(ternary_map)
    tern_pred, tern_collisions, tern_metrics = majority_lookup_predict(
        tmp_ternary, [q_col, "source_symbol"]
    )

    full_map = {sf: sf for sf in source_families}
    tmp_full = df.copy()
    tmp_full["source_symbol"] = tmp_full["source_family"].map(full_map)
    full_pred, full_collisions, full_metrics = majority_lookup_predict(
        tmp_full, [q_col, "source_symbol"]
    )

    ladder = pd.DataFrame([
        {
            "lift": "observable_quotient_only",
            "symbol_count": 1,
            **obs_metrics,
            "mapping_json": json.dumps({sf: "symbol_0" for sf in source_families}, sort_keys=True),
        },
        {
            "lift": "best_binary_source_role_lift",
            **best_by_k[2],
        },
        {
            "lift": "ternary_source_role_primitive",
            "symbol_count": 3,
            **tern_metrics,
            "mapping_json": json.dumps(ternary_map, sort_keys=True),
        },
        {
            "lift": "full_four_family_source_lift",
            "symbol_count": 4,
            **full_metrics,
            "mapping_json": json.dumps(full_map, sort_keys=True),
        },
    ])

    details = {
        "all_partitions": pd.DataFrame(all_partitions),
        "observable_collisions": obs_collisions,
        "ternary_collisions": tern_collisions,
        "observable_pred": obs_pred,
        "ternary_pred": tern_pred,
    }
    return ladder, details


# ---------------------------------------------------------------------
# Visualization coordinates
# ---------------------------------------------------------------------

def make_coordinates(df: pd.DataFrame, q_col: str, seed: int = 923) -> pd.DataFrame:
    """
    Generate stable 2D coordinates from actual observable quotient groups.

    Same quotient receives same underlying center.
    Jitter is only for visualization, so overlapping rows can be seen.
    """
    rng = np.random.default_rng(seed)
    out = df.copy()

    q_stats = out.groupby(q_col).agg(
        n_rows=("true_class", "size"),
        n_classes=("true_class", "nunique"),
    ).reset_index()

    collision_q = set(q_stats.loc[q_stats["n_classes"] > 1, q_col])
    q_values = list(pd.Series(out[q_col].unique()).sort_values())

    coords = {}
    collision_vals = [q for q in q_values if q in collision_q]
    other_vals = [q for q in q_values if q not in collision_q]

    # Put quotient collisions in the center: the source-degenerate basin.
    for i, q in enumerate(collision_vals):
        theta = 2 * np.pi * i / max(1, len(collision_vals))
        radius = 0.12 + 0.10 * (i % 4)
        coords[q] = (radius * np.cos(theta), radius * np.sin(theta))

    # Put non-collision quotients around the perimeter.
    for i, q in enumerate(other_vals):
        theta = 2 * np.pi * i / max(1, len(other_vals))
        radius = 2.55 + 0.35 * ((i % 7) / 6)
        coords[q] = (radius * np.cos(theta), radius * np.sin(theta))

    xs, ys = [], []
    for _, row in out.iterrows():
        cx, cy = coords[row[q_col]]
        scale = 0.08 if row[q_col] in collision_q else 0.14
        dx, dy = rng.normal(0, scale, 2)
        xs.append(cx + dx)
        ys.append(cy + dy)

    out["viz_x"] = xs
    out["viz_y"] = ys
    out["z_target"] = out["source_role"].map(ROLE_Z).astype(float)
    out["is_quotient_collision"] = out[q_col].isin(collision_q)
    return out


# ---------------------------------------------------------------------
# Animation
# ---------------------------------------------------------------------

def smoothstep(x: float) -> float:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def phase_for_frame(frame: int, n_frames: int) -> Tuple[int, float]:
    """
    Six narrative phases.
    Returns 1-based phase index and local progress in [0,1].
    """
    phase_len = n_frames / 6
    phase = min(5, int(frame // phase_len))
    local = (frame - phase * phase_len) / phase_len
    return phase + 1, smoothstep(local)


PHASE_TITLES = {
    1: "Step 1 — Observe the Geometry",
    2: "Step 2 — Geometry Finds a Basin",
    3: "Step 3 — Geometry Is Underdetermined",
    4: "Step 4 — Add the Information Lift",
    5: "Step 5 — Ternary Source-Role Primitive",
    6: "Step 6 — Exact Full-Stack Closure",
}

PHASE_CAPTIONS = {
    1: "Frame 1 of 6 — Geometry gives the admissible structural form.",
    2: "Frame 2 of 6 — Geometry identifies the basin, but not the source history.",
    3: "Frame 3 of 6 — Geometry alone cannot distinguish active repair from passive occupancy.",
    4: "Frame 4 of 6 — Information adds the missing source-legitimacy dimension.",
    5: "Frame 5 of 6 — The ternary source-role primitive is the first exact closure.",
    6: "Frame 6 of 6 — Both are required for exact source-legitimacy closure.",
}


def animate(
    df: pd.DataFrame,
    ladder: pd.DataFrame,
    out_mp4: Path,
    out_gif: Path | None = None,
    fps: int = 24,
    duration: float = 18.0,
    dpi: int = 150,
    max_points: int | None = None,
):
    # Optional downsample for speed.
    if max_points is not None and len(df) > max_points:
        df_plot = (
            df.groupby("source_role", group_keys=False)
              .apply(lambda g: g.sample(min(len(g), max(1, int(max_points * len(g) / len(df)))), random_state=923))
              .reset_index(drop=True)
        )
    else:
        df_plot = df.copy()

    # Extract arrays.
    x = df_plot["viz_x"].to_numpy()
    y = df_plot["viz_y"].to_numpy()
    z_target = df_plot["z_target"].to_numpy()
    roles = df_plot["source_role"].to_numpy()
    colors = np.array([ROLE_COLORS[r] for r in roles])
    sizes = np.where(roles == "source_active_role", 18, 20)

    # Use deterministic "pre-lift" jitter around zero.
    rng = np.random.default_rng(923)
    z_noise = rng.normal(0, 0.035, len(df_plot))

    n_frames = int(duration * fps)

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(16, 9), dpi=dpi)
    fig.patch.set_facecolor("#020202")

    ax1 = fig.add_axes([0.055, 0.22, 0.42, 0.62])
    ax2 = fig.add_axes([0.545, 0.22, 0.40, 0.62], projection="3d")

    # Static-ish left scatter objects by role.
    scat_left = {}
    scat_right = {}

    for role in CLASS_ORDER:
        mask = roles == role
        scat_left[role] = ax1.scatter(
            x[mask], y[mask],
            c=ROLE_COLORS[role],
            s=sizes[mask],
            alpha=0.58,
            label=ROLE_LABELS[role],
            edgecolors="none",
        )
        scat_right[role] = ax2.scatter(
            x[mask], y[mask], z_noise[mask],
            c=ROLE_COLORS[role],
            s=sizes[mask],
            alpha=0.15,
            edgecolors="none",
        )

    # Titles and persistent text handles.
    title = fig.text(
        0.5, 0.955,
        "V923 Geometry–Information Bridge",
        ha="center", va="top",
        fontsize=22, fontweight="bold", color="white",
    )
    subtitle = fig.text(
        0.5, 0.915,
        PHASE_TITLES[1],
        ha="center", va="top",
        fontsize=15, color="#dddddd",
    )

    footer = fig.text(
        0.5, 0.055,
        PHASE_CAPTIONS[1],
        ha="center", va="center",
        fontsize=12,
        color="white",
        fontweight="bold",
        bbox=dict(facecolor="#090909", edgecolor="#555555", boxstyle="round,pad=0.7", alpha=0.92),
    )

    callout_left = ax1.text(
        0.03, 0.95, "",
        transform=ax1.transAxes,
        va="top", ha="left",
        fontsize=11, color="white", fontweight="bold",
        bbox=dict(facecolor="#050505", alpha=0.65, edgecolor="none", pad=5),
    )
    callout_right = ax2.text2D(
        0.70, 0.48, "",
        transform=ax2.transAxes,
        ha="left", va="center",
        fontsize=11, color="white",
        bbox=dict(facecolor="#050505", alpha=0.55, edgecolor="none", pad=5),
    )

    # Left axes.
    ax1.set_title(
        "Geometry Paradigm\n$E_{OSC}$ Basin / Observable Quotient View",
        fontsize=13,
        pad=14,
    )
    ax1.set_xlabel("Observable Quotient Dimension 1")
    ax1.set_ylabel("Observable Quotient Dimension 2")
    ax1.grid(True, alpha=0.16)
    ax1.set_xlim(-3.5, 3.5)
    ax1.set_ylim(-3.5, 3.5)
    ax1.legend(loc="upper right", framealpha=0.82, facecolor="#050505", edgecolor="#dddddd")

    # Basin circle and ring.
    basin_circle = Circle((0, 0), 1.05, edgecolor="#ffea00", facecolor="none",
                          linestyle="--", linewidth=1.2, alpha=0.0)
    ax1.add_patch(basin_circle)

    # Right axes.
    ax2.set_title(
        "It-From-Bit Paradigm\nTernary Source-Role Primitive",
        fontsize=13,
        pad=14,
    )
    ax2.set_xlabel("Observable Quotient Dimension 1", labelpad=8)
    ax2.set_ylabel("Observable Quotient Dimension 2", labelpad=8)
    ax2.set_zlabel("Information Lift (discrete role)", labelpad=10)
    ax2.set_xlim(-3.5, 3.5)
    ax2.set_ylim(-3.5, 3.5)
    ax2.set_zlim(-0.15, 2.2)
    ax2.set_zticks([0, 1, 2])
    ax2.set_zticklabels(["Z=0\nBroken", "Z=1\nBasin-Eligible", "Z=2\nActive"], fontsize=8)
    ax2.view_init(elev=19, azim=45)
    ax2.xaxis.pane.fill = False
    ax2.yaxis.pane.fill = False
    ax2.zaxis.pane.fill = False
    ax2.grid(True, alpha=0.15)

    # Lift lines will be re-drawn each frame as needed.
    lift_lines = []

    # Metrics text table.
    metrics_txt = (
        "Lift ladder recomputed from V921 data\n"
        f"Observable only: {ladder.loc[0,'accuracy']:.6f} acc, {int(ladder.loc[0,'false_cases'])} false\n"
        f"Best binary:     {ladder.loc[1,'accuracy']:.6f} acc, {int(ladder.loc[1,'false_cases'])} false\n"
        f"Ternary:         {ladder.loc[2,'accuracy']:.6f} acc, {int(ladder.loc[2,'false_cases'])} false"
    )
    metrics_box = fig.text(
        0.5, 0.145, "",
        ha="center", va="center",
        fontsize=10,
        color="#eaeaea",
        bbox=dict(facecolor="#080808", edgecolor="#c9a227", boxstyle="round,pad=0.55", alpha=0.0),
    )

    def update(frame: int):
        nonlocal lift_lines

        phase, local = phase_for_frame(frame, n_frames)
        subtitle.set_text(PHASE_TITLES[phase])
        footer.set_text(PHASE_CAPTIONS[phase])

        # Camera slowly rotates after information lift activates.
        if phase >= 4:
            ax2.view_init(elev=19 + 2.5 * np.sin(frame / 20), azim=45 + 8 * local + 4 * (phase - 4))
        else:
            ax2.view_init(elev=17, azim=45)

        # Left alpha and basin circle.
        basin_alpha = 0.0
        if phase == 2:
            basin_alpha = 0.25 + 0.55 * local
        elif phase >= 3:
            basin_alpha = 0.75
        basin_circle.set_alpha(basin_alpha)

        # Update left callout.
        if phase == 1:
            callout_left.set_text("A basin is visible.")
            callout_left.set_position((0.68, 0.53))
        elif phase == 2:
            callout_left.set_text("Many trajectories\ncan land here.")
            callout_left.set_position((0.66, 0.24))
        elif phase == 3:
            callout_left.set_text("Same geometry,\ndifferent source history.")
            callout_left.set_position((0.66, 0.62))
        elif phase in (4, 5):
            callout_left.set_text("Geometry gives\nadmissible form.")
            callout_left.set_position((0.66, 0.53))
        else:
            callout_left.set_text("GEOMETRY RESOLVED\nAdmissible basin form.")
            callout_left.set_position((0.55, 0.22))

        # Information lift interpolation.
        if phase <= 2:
            lift_progress = 0.0
            right_alpha = 0.12
            callout_right.set_text("")
        elif phase == 3:
            lift_progress = 0.10 * local
            right_alpha = 0.28 + 0.22 * local
            callout_right.set_text("An extra axis\nis needed.")
        elif phase == 4:
            lift_progress = local
            right_alpha = 0.45 + 0.45 * local
            callout_right.set_text("A discrete information axis\nresolves the ambiguity.")
        else:
            lift_progress = 1.0
            right_alpha = 0.86
            if phase == 5:
                callout_right.set_text("Minimal exact closure\nappears at three roles.")
            else:
                callout_right.set_text("INFORMATION RESOLVED\nTernary lift is exact.")

        z_current = (1 - lift_progress) * z_noise + lift_progress * z_target

        # Update right scatters by role.
        for role in CLASS_ORDER:
            mask = roles == role
            scat_right[role]._offsets3d = (x[mask], y[mask], z_current[mask])
            scat_right[role].set_alpha(right_alpha if phase >= 4 else max(0.08, right_alpha))

        # Rebuild lift lines.
        for ln in lift_lines:
            try:
                ln.remove()
            except Exception:
                pass
        lift_lines = []

        if phase >= 4:
            # Draw subset lift lines.
            rng_local = np.random.default_rng(1000 + frame)
            idx_pool = np.arange(len(df_plot))
            idx = rng_local.choice(idx_pool, size=min(95, len(idx_pool)), replace=False)
            for i in idx:
                if z_target[i] > 0:
                    ln = ax2.plot(
                        [x[i], x[i]], [y[i], y[i]], [0, z_current[i]],
                        color=colors[i], alpha=0.20 * lift_progress, linestyle=":", linewidth=0.7
                    )[0]
                    lift_lines.append(ln)

        # Metrics box appears at the end.
        if phase >= 6:
            metrics_box.set_text(metrics_txt)
            metrics_box.get_bbox_patch().set_alpha(0.92)
        else:
            metrics_box.set_text("")
            metrics_box.get_bbox_patch().set_alpha(0.0)

        return []

    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps, blit=False)

    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    saved = {"mp4": False, "gif": False}

    if shutil.which("ffmpeg"):
        writer = FFMpegWriter(fps=fps, metadata={"title": "V923 Full-Stack Animation"}, bitrate=2400)
        anim.save(str(out_mp4), writer=writer, dpi=dpi)
        saved["mp4"] = True
    else:
        print("ffmpeg not found. Skipping MP4 export.")

    if out_gif is not None:
        # Lower FPS for gif.
        gif_writer = PillowWriter(fps=min(12, fps))
        anim.save(str(out_gif), writer=gif_writer, dpi=max(90, int(dpi * 0.65)))
        saved["gif"] = True

    plt.close(fig)
    return saved


# ---------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Create the V923 full-stack MP4 animation.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=18.0)
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--max-points", type=int, default=None,
                        help="Optional downsample for slower machines, e.g. 500.")
    parser.add_argument("--gif", action="store_true",
                        help="Also export GIF fallback. Slower and larger.")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    df, q_col = load_data(args.input)
    ladder, details = evaluate_lift_ladder(df, q_col)
    df_viz = make_coordinates(df, q_col)

    ladder.to_csv(args.out / "v923_animation_lift_ladder.csv", index=False)
    details["all_partitions"].to_csv(args.out / "v923_animation_all_partitions.csv", index=False)
    details["observable_collisions"].to_csv(args.out / "v923_animation_observable_collisions.csv", index=False)
    df_viz.to_csv(args.out / "v923_animation_endpoint_coordinates.csv", index=False)

    out_mp4 = args.out / "v923_full_stack_geometry_information_animation.mp4"
    out_gif = args.out / "v923_full_stack_geometry_information_animation.gif" if args.gif else None

    saved = animate(
        df_viz,
        ladder,
        out_mp4=out_mp4,
        out_gif=out_gif,
        fps=args.fps,
        duration=args.duration,
        dpi=args.dpi,
        max_points=args.max_points,
    )

    summary = {
        "verdict": "v923_full_stack_animation_from_actual_v921_data",
        "certified": bool(
            ladder.loc[0, "false_cases"] > 0
            and ladder.loc[1, "false_cases"] > 0
            and ladder.loc[2, "false_cases"] == 0
            and ladder.loc[2, "accuracy"] == 1.0
        ),
        "input": str(args.input),
        "rows": int(len(df)),
        "quotient_column": q_col,
        "fps": args.fps,
        "duration": args.duration,
        "dpi": args.dpi,
        "saved": saved,
        "mp4": str(out_mp4),
        "gif": str(out_gif) if out_gif else None,
        "lift_ladder": ladder.to_dict(orient="records"),
        "claim_boundary": {
            "z_axis": "discrete source-role information index, not physical space/time",
            "not_claimed": [
                "1/f ledger",
                "CMB or black-hole physics",
                "physical spacetime",
                "GR / Einstein equations / continuum closure",
                "unique repair-channel law",
            ],
        },
    }

    (args.out / "v923_animation_result.json").write_text(json.dumps(summary, indent=2))

    report = f"""# V923 Full-Stack Animation Report

This animation is generated from actual V921 endpoint data, not a synthetic Gaussian cohort.

## Input

`{args.input}`

Rows: **{len(df)}**  
Observable quotient column: **{q_col}**

## Recomputed lift ladder

{ladder[["lift","symbol_count","accuracy","false_cases","collision_rows"]].to_markdown(index=False)}

## Animation meaning

- Left panel: observable quotient / basin geometry.
- Right panel: discrete ternary source-role information lift.
- Z-axis: discrete source-role index, not physical space or physical time.

## Claim boundary

This is a source-legitimacy closure animation. It is not a 1/f ledger, CMB, black-hole, GR, Einstein-equation, physical-spacetime, or continuum-closure claim.
"""
    (args.out / "V923_FULL_STACK_ANIMATION_REPORT.md").write_text(report)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
