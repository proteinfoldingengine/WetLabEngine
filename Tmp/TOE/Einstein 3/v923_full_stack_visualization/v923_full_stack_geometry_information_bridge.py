#!/usr/bin/env python3
"""
V923 Full-Stack Geometry–Information Bridge Visualization
=========================================================

Purpose
-------
This script replaces the earlier synthetic Gaussian visualization with a
full-stack visualization tied to the actual V921/V923 closure data.

It does four things:

1. Loads the frozen V921 blind endpoint cohort.
2. Recomputes the V923 lift ladder:
   - observable quotient only
   - best binary source-role lift
   - minimal ternary source-role primitive
   - full four-family source lift
3. Generates faithful visualization coordinates from the actual observable
   quotient groups, not random Gaussian stand-ins.
4. Renders the Geometry–Information Bridge:
   - Left: geometry/quotient view, where source roles can overlap
   - Right: discrete ternary information lift, which closes source legitimacy

Scientific claim boundary
-------------------------
This is a source-legitimacy closure visualization.

YES:
- E_OSC / endpoint-path observables define an observable quotient.
- Observable-only closure is source-degenerate in the V921 cohort.
- A ternary source-role primitive gives exact closure in this branch.

NO:
- The Z-axis is not physical space or physical time.
- This is not a GR / Einstein equation / spacetime curvature proof.
- This is not a 1/f ledger claim.
- This is not a CMB or black-hole claim.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------

DEFAULT_INPUT = Path(
    "/mnt/data/v921_ternary_source_role_primitive_blind_regeneration_audit/"
    "v921_ternary_endpoint_scores.csv"
)

DEFAULT_OUT = Path("/mnt/data/v923_full_stack_visualization_run")

SOURCE_ROLE_MAP = {
    "active_source": "source_active_role",
    "passive_source": "source_basin_eligible_nonactive_role",
    "structured_source": "source_basin_eligible_nonactive_role",
    "rejected_or_broken_source": "source_rejected_or_broken_role",
}

ROLE_Z = {
    "source_rejected_or_broken_role": 0,
    "source_basin_eligible_nonactive_role": 1,
    "source_active_role": 2,
}

ROLE_COLORS = {
    "source_rejected_or_broken_role": "#ff1744",
    "source_basin_eligible_nonactive_role": "#ffea00",
    "source_active_role": "#39ff14",
}

ROLE_LABELS = {
    "source_rejected_or_broken_role": "Rejected/Broken",
    "source_basin_eligible_nonactive_role": "Basin-Eligible Nonactive",
    "source_active_role": "Active Repair",
}


# ---------------------------------------------------------------------
# Utility: canonical partitions of source families
# ---------------------------------------------------------------------

def canonical_partitions(items: List[str], k: int) -> Iterable[Dict[str, str]]:
    """
    Generate all onto partitions of `items` into exactly k canonical symbols.

    Example for items [a,b,c] and k=2:
      a is always symbol_0; subsequent labels are introduced in canonical order.
    This avoids duplicate label permutations.
    """
    n = len(items)
    if k == 1:
        yield {item: "symbol_0" for item in items}
        return

    assignments = [0] * n
    assignments[0] = 0

    def rec(i: int, max_label: int):
        if i == n:
            used = set(assignments)
            if len(used) == k and used == set(range(k)):
                yield {items[j]: f"symbol_{assignments[j]}" for j in range(n)}
            return

        # Existing labels plus one new label, but never exceed k-1
        for lab in range(0, min(max_label + 2, k)):
            assignments[i] = lab
            yield from rec(i + 1, max(max_label, lab))

    yield from rec(1, 0)


def majority_lookup_predict(
    df: pd.DataFrame,
    key_cols: List[str],
    true_col: str = "true_class",
) -> Tuple[pd.Series, pd.DataFrame, Dict[str, int]]:
    """
    Build a deterministic lookup from key_cols to majority true class and predict.
    Also return collision diagnostics.

    A collision group is a key that maps to more than one true class.
    """
    grouped = df.groupby(key_cols, dropna=False)

    # Majority class lookup.
    lookup = {}
    collision_rows = 0
    collision_groups = 0
    collision_details = []

    for key, g in grouped:
        counts = g[true_col].value_counts()
        majority = counts.index[0]
        lookup[key if isinstance(key, tuple) else (key,)] = majority

        if len(counts) > 1:
            collision_groups += 1
            collision_rows += len(g)
            collision_details.append({
                "key": repr(key),
                "rows": len(g),
                "n_classes": len(counts),
                "classes": json.dumps(counts.to_dict()),
                "majority_class": majority,
            })

    preds = []
    for _, row in df.iterrows():
        key = tuple(row[c] for c in key_cols)
        preds.append(lookup[key])

    pred = pd.Series(preds, index=df.index, name="pred_class")
    collisions = pd.DataFrame(collision_details)
    metrics = {
        "rows": int(len(df)),
        "accuracy": float((pred == df[true_col]).mean()),
        "false_cases": int((pred != df[true_col]).sum()),
        "collision_groups": int(collision_groups),
        "collision_rows": int(collision_rows),
    }
    return pred, collisions, metrics


def evaluate_partition(
    df: pd.DataFrame,
    mapping: Dict[str, str],
    quotient_col: str,
    name: str,
) -> Dict[str, object]:
    tmp = df.copy()
    tmp["source_symbol"] = tmp["source_family"].map(mapping)
    pred, collisions, metrics = majority_lookup_predict(
        tmp, [quotient_col, "source_symbol"], "true_class"
    )
    return {
        "name": name,
        "symbol_count": int(tmp["source_symbol"].nunique()),
        "mapping": mapping,
        "pred": pred,
        "collisions": collisions,
        "metrics": metrics,
    }


# ---------------------------------------------------------------------
# Load and validate data
# ---------------------------------------------------------------------

def load_endpoint_data(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input data not found: {input_path}\n"
            "Expected the V921 endpoint scores CSV."
        )

    df = pd.read_csv(input_path)

    # Normalize / locate columns.
    required = {"source_family", "true_class"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input file is missing required columns: {sorted(missing)}")

    quotient_candidates = [
        "v921_observable_quotient",
        "observable_quotient",
        "quotient",
    ]
    quotient_col = next((c for c in quotient_candidates if c in df.columns), None)
    if quotient_col is None:
        # Make a conservative fallback from endpoint/path-ish columns.
        # This should not be needed for the official V921 CSV.
        possible = [c for c in df.columns if any(s in c.lower() for s in [
            "basin", "accepted", "reduction", "endpoint", "start"
        ])]
        if not possible:
            raise ValueError(
                "Could not find observable quotient column and no endpoint/path "
                "columns are available to construct one."
            )
        df["v921_observable_quotient"] = (
            df[possible].astype(str).agg("|".join, axis=1)
        )
        quotient_col = "v921_observable_quotient"

    df = df.copy()
    df["source_role"] = df["source_family"].map(SOURCE_ROLE_MAP)
    if df["source_role"].isna().any():
        bad = sorted(df.loc[df["source_role"].isna(), "source_family"].unique())
        raise ValueError(f"Unrecognized source_family values: {bad}")

    df["_quotient_col"] = quotient_col
    return df


# ---------------------------------------------------------------------
# Geometry coordinates from actual quotient groups
# ---------------------------------------------------------------------

def make_quotient_coordinates(df: pd.DataFrame, quotient_col: str, seed: int = 923) -> pd.DataFrame:
    """
    Give each actual observable quotient group a stable 2D coordinate.

    Important:
    - Same quotient gets same basin center.
    - Individual rows receive tiny deterministic jitter only for visibility.
    - Coordinates are for visualization, not physical coordinates.
    """
    rng = np.random.default_rng(seed)
    q_values = list(pd.Series(df[quotient_col].unique()).sort_values())
    n = len(q_values)

    # Place quotient groups along a compact spiral, then mark high-collision basin
    # groups toward the center. This lets exact quotient collisions visually overlap.
    q_counts = df.groupby(quotient_col)["true_class"].nunique().rename("n_classes")
    q_size = df.groupby(quotient_col).size().rename("n_rows")
    q_info = pd.concat([q_counts, q_size], axis=1).reset_index()

    coords = {}
    # Collision/multi-class quotients are centered to show degeneracy.
    collision_q = set(q_info.loc[q_info["n_classes"] > 1, quotient_col])

    non_collision_q = [q for q in q_values if q not in collision_q]
    collision_q_sorted = [q for q in q_values if q in collision_q]

    for i, q in enumerate(collision_q_sorted):
        angle = 2 * np.pi * i / max(1, len(collision_q_sorted))
        radius = 0.20 + 0.10 * (i % 3)
        coords[q] = (radius * np.cos(angle), radius * np.sin(angle))

    # Non-collision quotients around wider ring.
    for i, q in enumerate(non_collision_q):
        angle = 2 * np.pi * i / max(1, len(non_collision_q))
        radius = 2.3 + 0.45 * ((i % 5) / 4)
        coords[q] = (radius * np.cos(angle), radius * np.sin(angle))

    xs, ys = [], []
    for idx, row in df.iterrows():
        cx, cy = coords[row[quotient_col]]
        # Jitter is very small for collision groups and larger outside.
        scale = 0.10 if row[quotient_col] in collision_q else 0.16
        jitter = rng.normal(0, scale, 2)
        xs.append(cx + jitter[0])
        ys.append(cy + jitter[1])

    out = df.copy()
    out["viz_x"] = xs
    out["viz_y"] = ys
    out["viz_z"] = out["source_role"].map(ROLE_Z).astype(float)
    out["is_quotient_collision"] = out[quotient_col].isin(collision_q)
    return out


# ---------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------

def render_bridge_plot(
    df: pd.DataFrame,
    out_png: Path,
    title: str = "V923 Geometry–Information Bridge: Resolving Source Degeneracy",
):
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(18, 9), dpi=180)
    fig.suptitle(title, fontsize=20, fontweight="bold", color="white", y=0.965)

    order = [
        "source_rejected_or_broken_role",
        "source_basin_eligible_nonactive_role",
        "source_active_role",
    ]

    # ---------------- Left: geometry quotient view ----------------
    ax1 = fig.add_subplot(1, 2, 1)
    for role in order:
        d = df[df["source_role"] == role]
        ax1.scatter(
            d["viz_x"], d["viz_y"],
            c=ROLE_COLORS[role],
            label=ROLE_LABELS[role],
            s=18 if role != "source_active_role" else 16,
            alpha=0.60 if role != "source_rejected_or_broken_role" else 0.40,
            edgecolors="none",
        )

    ax1.set_title(
        "The Geometry Paradigm\n$E_{OSC}$ Basin / Observable Quotient View",
        fontsize=14,
        pad=15,
    )
    ax1.set_xlabel("Observable Quotient Dimension 1")
    ax1.set_ylabel("Observable Quotient Dimension 2")
    ax1.grid(True, alpha=0.15)
    ax1.legend(loc="upper right", facecolor="#050505", edgecolor="white", framealpha=0.85)

    # Annotation points to center collision area.
    ax1.annotate(
        "Source-Degenerate Quotient\n(geometry alone is incomplete)",
        xy=(0, 0),
        xytext=(-2.8, 2.8),
        arrowprops=dict(facecolor="white", edgecolor="white", shrink=0.05, width=1, headwidth=7),
        color="white",
        fontsize=11,
        ha="center",
        fontweight="bold",
    )
    ax1.set_aspect("equal", adjustable="box")

    # ---------------- Right: information lift ----------------
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    for role in order:
        d = df[df["source_role"] == role]
        ax2.scatter(
            d["viz_x"], d["viz_y"], d["viz_z"],
            c=ROLE_COLORS[role],
            s=18 if role != "source_active_role" else 16,
            alpha=0.70,
            edgecolors="none",
        )

    # Dotted lift lines for a subset of basin points.
    basin = df[df["source_role"].isin([
        "source_basin_eligible_nonactive_role",
        "source_active_role",
    ])].sample(min(120, len(df)), random_state=923)
    for _, r in basin.iterrows():
        ax2.plot(
            [r["viz_x"], r["viz_x"]],
            [r["viz_y"], r["viz_y"]],
            [0, r["viz_z"]],
            color=ROLE_COLORS[r["source_role"]],
            alpha=0.16,
            linestyle=":",
            linewidth=0.8,
        )

    ax2.set_title(
        "The It-From-Bit Paradigm\nTernary Source-Role Primitive",
        fontsize=14,
        pad=15,
    )
    ax2.set_xlabel("Observable Quotient Dimension 1", labelpad=10)
    ax2.set_ylabel("Observable Quotient Dimension 2", labelpad=10)
    ax2.set_zlabel("Information Lift (discrete role)", labelpad=12)
    ax2.set_zticks([0, 1, 2])
    ax2.set_zticklabels([
        "Z=0\nRejected/Broken",
        "Z=1\nBasin-Eligible\nNonactive",
        "Z=2\nActive",
    ], fontsize=8)
    ax2.view_init(elev=18, azim=45)
    ax2.xaxis.pane.fill = False
    ax2.yaxis.pane.fill = False
    ax2.zaxis.pane.fill = False
    ax2.grid(True, alpha=0.15)

    # ---------------- Bottom handshake ----------------
    fig.text(
        0.5, 0.045,
        "THE V923 HANDSHAKE\n\n"
        "Geometry provides the admissible basin / quotient form (Left).\n"
        "Information provides the minimal source-legitimacy primitive (Right).\n"
        "Both are required for exact source-legitimacy closure in this branch.",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="#e8e8e8",
        bbox=dict(
            facecolor="#111111",
            alpha=0.94,
            edgecolor="#c9a227",
            boxstyle="round,pad=0.75",
            linewidth=1.8,
        ),
    )

    plt.subplots_adjust(left=0.055, right=0.985, top=0.89, bottom=0.20, wspace=0.18)
    fig.savefig(out_png, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def render_lift_ladder_plot(lift_table: pd.DataFrame, out_png: Path):
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=180)
    ax.axis("off")
    ax.set_title("V923 Lift Ladder: First Exact Closure Appears at Three Symbols",
                 fontsize=14, fontweight="bold", pad=20)

    display = lift_table[[
        "lift",
        "symbol_count",
        "accuracy",
        "false_cases",
        "collision_rows",
    ]].copy()
    display["accuracy"] = display["accuracy"].map(lambda x: f"{x:.6f}")
    display.columns = ["Lift", "Symbols", "Accuracy", "False Cases", "Collision Rows"]

    table = ax.table(
        cellText=display.values,
        colLabels=display.columns,
        loc="center",
        cellLoc="center",
        colLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.15, 1.6)

    # Color header and ternary row.
    for (r, c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor("#08306b")
            cell.set_text_props(color="white", weight="bold")
        elif r == 3:  # ternary row; table row index after header
            cell.set_facecolor("#d9f0d3")
            cell.set_text_props(weight="bold")
        else:
            cell.set_facecolor("#f7fbff" if r % 2 else "#eef5ff")

    fig.text(
        0.5, 0.08,
        "Observable-only and binary lifts fail. The ternary source-role primitive is minimal and exact.",
        ha="center",
        fontsize=10,
        color="#08306b",
        fontweight="bold",
    )
    fig.savefig(out_png, dpi=220, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------
# Main proof and outputs
# ---------------------------------------------------------------------

def run(input_path: Path, out_dir: Path, seed: int = 923) -> Dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = load_endpoint_data(input_path)
    quotient_col = df["_quotient_col"].iloc[0]

    # Observable-only.
    obs_pred, obs_collisions, obs_metrics = majority_lookup_predict(
        df, [quotient_col], "true_class"
    )

    # Exhaustive partitions.
    source_families = sorted(df["source_family"].unique())
    all_rows = []
    best_by_k = {}

    for k in range(1, len(source_families) + 1):
        best = None
        for mapping in canonical_partitions(source_families, k):
            result = evaluate_partition(df, mapping, quotient_col, f"partition_{k}")
            m = result["metrics"]
            row = {
                "symbol_count": k,
                "accuracy": m["accuracy"],
                "false_cases": m["false_cases"],
                "collision_groups": m["collision_groups"],
                "collision_rows": m["collision_rows"],
                "mapping_json": json.dumps(mapping, sort_keys=True),
            }
            all_rows.append(row)
            if best is None:
                best = (row, result)
            else:
                # Accuracy desc, false cases asc, collision rows asc.
                prev = best[0]
                key_new = (row["accuracy"], -row["false_cases"], -row["collision_rows"])
                key_old = (prev["accuracy"], -prev["false_cases"], -prev["collision_rows"])
                if key_new > key_old:
                    best = (row, result)
        best_by_k[k] = best

    all_partitions = pd.DataFrame(all_rows)
    all_partitions.to_csv(out_dir / "v923_all_source_role_partitions.csv", index=False)

    # Named lifts.
    observable_row = {
        "lift": "observable_quotient_only",
        "symbol_count": 1,
        **obs_metrics,
        "mapping_json": json.dumps({sf: "symbol_0" for sf in source_families}, sort_keys=True),
    }

    best_binary_row = {
        "lift": "best_binary_source_role_lift",
        **{k: v for k, v in best_by_k[2][0].items() if k != "mapping_json"},
        "mapping_json": best_by_k[2][0]["mapping_json"],
    }

    ternary_mapping = {
        "active_source": "source_active_role",
        "passive_source": "source_basin_eligible_nonactive_role",
        "structured_source": "source_basin_eligible_nonactive_role",
        "rejected_or_broken_source": "source_rejected_or_broken_role",
    }
    ternary_result = evaluate_partition(df, ternary_mapping, quotient_col, "ternary_source_role_primitive")
    ternary_row = {
        "lift": "ternary_source_role_primitive",
        "symbol_count": 3,
        **ternary_result["metrics"],
        "mapping_json": json.dumps(ternary_mapping, sort_keys=True),
    }

    full_mapping = {sf: sf for sf in source_families}
    full_result = evaluate_partition(df, full_mapping, quotient_col, "full_four_family_source_lift")
    full_row = {
        "lift": "full_four_family_source_lift",
        "symbol_count": 4,
        **full_result["metrics"],
        "mapping_json": json.dumps(full_mapping, sort_keys=True),
    }

    lift_table = pd.DataFrame([observable_row, best_binary_row, ternary_row, full_row])
    lift_table.to_csv(out_dir / "v923_full_stack_lift_ladder.csv", index=False)

    # Endpoint scores with predictions.
    viz_df = make_quotient_coordinates(df, quotient_col, seed=seed)
    viz_df["pred_observable_only"] = obs_pred
    viz_df["pred_ternary"] = ternary_result["pred"]
    viz_df["observable_only_correct"] = viz_df["pred_observable_only"] == viz_df["true_class"]
    viz_df["ternary_correct"] = viz_df["pred_ternary"] == viz_df["true_class"]
    viz_df.to_csv(out_dir / "v923_full_stack_visualization_endpoint_scores.csv", index=False)

    # Collision outputs.
    obs_collisions.to_csv(out_dir / "v923_observable_only_collision_groups.csv", index=False)
    ternary_result["collisions"].to_csv(out_dir / "v923_ternary_collision_groups.csv", index=False)

    # Plots.
    bridge_png = out_dir / "v923_geometry_information_bridge_full_stack.png"
    ladder_png = out_dir / "v923_lift_ladder_full_stack.png"
    render_bridge_plot(viz_df, bridge_png)
    render_lift_ladder_plot(lift_table, ladder_png)

    # Report.
    minimal_exact_symbol_count = int(
        all_partitions.loc[all_partitions["accuracy"].eq(1.0), "symbol_count"].min()
    ) if (all_partitions["accuracy"] == 1.0).any() else None

    summary = {
        "verdict": "v923_full_stack_visualization_recomputed_from_v921_data",
        "certified": bool(
            minimal_exact_symbol_count == 3
            and ternary_row["false_cases"] == 0
            and observable_row["false_cases"] > 0
            and best_binary_row["false_cases"] > 0
        ),
        "input": str(input_path),
        "rows": int(len(df)),
        "quotient_column": quotient_col,
        "minimal_exact_symbol_count": minimal_exact_symbol_count,
        "lift_ladder": lift_table.to_dict(orient="records"),
        "claim_boundary": {
            "z_axis": "discrete source-role information index, not physical dimension",
            "not_claimed": [
                "1/f ledger",
                "physical time",
                "CMB or black-hole claim",
                "GR / Einstein equations / spacetime curvature / continuum closure",
                "unique repair-channel law",
            ],
        },
        "outputs": {
            "bridge_png": str(bridge_png),
            "ladder_png": str(ladder_png),
            "lift_ladder_csv": str(out_dir / "v923_full_stack_lift_ladder.csv"),
            "endpoint_scores_csv": str(out_dir / "v923_full_stack_visualization_endpoint_scores.csv"),
        },
    }
    (out_dir / "v923_full_stack_visualization_result.json").write_text(
        json.dumps(summary, indent=2)
    )

    report = f"""# V923 Full-Stack Geometry–Information Bridge Visualization

## Verdict

`{summary["verdict"]}`

Certified: **{summary["certified"]}**

Rows: **{len(df)}**  
Input: `{input_path}`  
Observable quotient column: `{quotient_col}`

## Lift ladder

{lift_table[["lift","symbol_count","accuracy","false_cases","collision_rows"]].to_markdown(index=False)}

## Minimal exact lift

The first exact closure appears at:

```text
{minimal_exact_symbol_count} source-role symbols
```

The certified ternary primitive is:

```text
active_source             -> source_active_role
passive_source            -> source_basin_eligible_nonactive_role
structured_source         -> source_basin_eligible_nonactive_role
rejected_or_broken_source -> source_rejected_or_broken_role
```

## What the visualization means

The left panel visualizes the observable quotient / basin view. It is allowed to be source-degenerate.

The right panel adds a discrete information lift. The Z-axis is **not physical space or time**. It is a discrete source-role index:

```text
Z=0 rejected/broken
Z=1 basin-eligible nonactive
Z=2 active
```

## Claim boundary

YES:
- The figure is derived from the actual V921 blind endpoint cohort.
- The lift ladder is recomputed in this script.
- Observable-only and binary closure fail.
- Ternary source-role closure succeeds in this branch.

NO:
- No 1/f ledger claim.
- No CMB / black-hole claim.
- No physical-time claim.
- No GR / Einstein equation / spacetime curvature / continuum-closure claim.
"""
    (out_dir / "V923_FULL_STACK_VISUALIZATION_REPORT.md").write_text(report)

    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=923)
    args = parser.parse_args()

    summary = run(args.input, args.out, seed=args.seed)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
