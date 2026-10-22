from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import statistics
from pathlib import Path

import torch

import p9_core as p9

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "measurement_output"
SOURCE_MANIFEST_PATH = ROOT / "P9_SOURCE_MANIFEST.json"
EXPECTED_SOURCE_MANIFEST_GIT_BLOB = "16ab23c9405b371af6886cf034e79370c54359bc"
SOURCE_MANIFEST_COMMIT = "0f723410c39ba4fe03471720ec59d5acfc0c1fc3"
CORE_GREEN_HEAD = "b4573dd46436adc36fd7b957b4f546bdf0f00079"

REQUIRED_OUTPUTS = (
    "p9_results.csv",
    "p9_group_correlations.csv",
    "p9_primary_comparisons.csv",
    "p9_summary.csv",
    "p9_acceptance.json",
    "p9_run_manifest.json",
    "SHA256SUMS.txt",
)

RAW_SCORE_FIELDS = (
    "compat_field",
    "dihedral_preserve",
    "productive_contact",
    "sigma_bridge",
    "closure_ready",
    "false_closure",
    "dir_pen",
    "angle_var",
    "dihed_smooth",
    "soft_contacts",
    "density_var",
    "rg",
    "loop_compat",
    "R_micro",
    "compactness",
    "C_meso",
    "flat_primary",
    "flat_secondary",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_run_keys() -> list[tuple[str, int, int]]:
    return p9.expected_state_keys()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_sha256sums(
    out: Path,
    *,
    names: tuple[str, ...] | list[str],
) -> None:
    lines = [
        f"{sha256_file(out / name)}  {name}"
        for name in names
    ]
    (out / "SHA256SUMS.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def build_run_manifest(*, git_head: str | None = None) -> dict[str, object]:
    return {
        "schema": "protein-p9-measurement-v1",
        "git_head": git_head if git_head is not None else os.environ.get("GITHUB_SHA"),
        "source_manifest_commit": SOURCE_MANIFEST_COMMIT,
        "source_manifest_git_blob": EXPECTED_SOURCE_MANIFEST_GIT_BLOB,
        "core_green_head": CORE_GREEN_HEAD,
        "core_green_run": 35383868978,
        "core_green_job": 105726089975,
        "targets": list(p9.TARGET_NAMES),
        "seeds": list(p9.SEEDS),
        "checkpoints": list(p9.CHECKPOINTS),
        "generator_steps": p9.GENERATOR_STEPS,
        "handoff_steps": p9.HANDOFF_STEPS,
        "optimizer": "Adam",
        "learning_rate": p9.LEARNING_RATE,
        "dtype": "float64",
        "device": "cpu",
        "generator_objective": "P6 physical_real_sequence",
        "handoff_objective": "P6 physical_real_sequence",
        "optimizer_reset_at_handoff": True,
        "v9_used_as_force": False,
        "native_information_used_in_dynamics": False,
        "native_information_used_in_score": False,
        "native_information_used_in_handoff": False,
        "candidate_score": "closure_ready",
        "same_information_controls": ["flat_primary", "flat_secondary"],
        "primary_outcome": "future_quality = -best_handoff_ca_rmsd_A",
        "grouping": "target x checkpoint; six seeds per group",
        "group_statistic": "Spearman rank correlation",
        "primary_test": "exact two-sided paired sign-flip over 16 group-level Spearman deltas",
        "multiplicity": "Holm over two primary comparisons",
        "native_evaluation_timing": "checkpoint/handoff states only; never used in dynamics or score",
    }


def _checkpoint_row(
    target,
    seed: int,
    checkpoint: int,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
) -> dict[str, object]:
    energy, (_, ca, _), components = p9.p6_objective_from_state(
        target, phi_free, psi
    )
    if not bool(torch.isfinite(energy)) or not bool(torch.isfinite(ca).all()):
        raise FloatingPointError(
            f"nonfinite checkpoint target={target.name} seed={seed} checkpoint={checkpoint}"
        )

    scores = p9.coherence_scores(ca)
    checkpoint_eval = p9._evaluate_state(target, phi_free, psi)
    handoff = p9.run_handoff(target, phi_free, psi)

    row: dict[str, object] = {
        "target": target.name,
        "seed": int(seed),
        "checkpoint": int(checkpoint),
        **scores,
        "checkpoint_ca_rmsd_A": float(checkpoint_eval["ca_rmsd_A"]),
        "checkpoint_topk_native_contact_precision": float(
            checkpoint_eval["topk_native_contact_precision"]
        ),
        "checkpoint_topk_contact_budget": int(
            checkpoint_eval["topk_contact_budget"]
        ),
        "checkpoint_native_contact_recall": float(
            checkpoint_eval["native_contact_recall"]
        ),
        "checkpoint_rg_A": float(checkpoint_eval["rg_A"]),
        "checkpoint_native_rg_A": float(checkpoint_eval["native_rg_A"]),
        "checkpoint_rg_ratio": float(checkpoint_eval["rg_ratio"]),
        "checkpoint_bond_length_drift_A": float(
            checkpoint_eval["bond_length_drift_A"]
        ),
        "checkpoint_bond_angle_drift_rad": float(
            checkpoint_eval["bond_angle_drift_rad"]
        ),
        **handoff,
    }
    row["max_bond_length_drift_A"] = max(
        float(row["checkpoint_bond_length_drift_A"]),
        float(handoff["max_bond_length_drift_A"]),
    )
    row["max_bond_angle_drift_rad"] = max(
        float(row["checkpoint_bond_angle_drift_rad"]),
        float(handoff["max_bond_angle_drift_rad"]),
    )
    for key, value in components.items():
        row[f"checkpoint_energy_{key}"] = value
    return row


def run_target_seed(
    target_name: str,
    seed: int,
) -> list[dict[str, object]]:
    target = p9.load_target(target_name)
    bank = p9.generate_state_bank(target, seed=seed)
    rows = []
    for checkpoint in p9.CHECKPOINTS:
        phi_free, psi = bank[checkpoint]
        rows.append(
            _checkpoint_row(
                target,
                seed,
                checkpoint,
                phi_free,
                psi,
            )
        )
    return rows


def all_observable_group_correlations(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    fields = [
        field
        for field in RAW_SCORE_FIELDS
        if all(field in row for row in rows)
    ]
    if not fields:
        fields = [
            score
            for score in p9.PRIMARY_SCORES
            if all(score in row for row in rows)
        ]

    groups: list[dict[str, object]] = []
    for target in p9.TARGET_NAMES:
        for checkpoint in p9.CHECKPOINTS:
            subset = [
                row
                for row in rows
                if row["target"] == target
                and int(row["checkpoint"]) == checkpoint
            ]
            if len(subset) != len(p9.SEEDS):
                continue
            future_quality = [
                -float(row["best_handoff_ca_rmsd_A"])
                for row in subset
            ]
            out: dict[str, object] = {
                "target": target,
                "checkpoint": checkpoint,
                "n": len(subset),
            }
            for field in fields:
                out[f"spearman_{field}"] = p9.spearman_rank(
                    [float(row[field]) for row in subset],
                    future_quality,
                )
            groups.append(out)
    return groups


def grouped_summary(
    rows: list[dict[str, object]],
    group_correlations: list[dict[str, object]],
) -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for target in (*p9.TARGET_NAMES, "pooled"):
        subset = [
            row
            for row in rows
            if target == "pooled" or row["target"] == target
        ]
        gsubset = [
            row
            for row in group_correlations
            if target == "pooled" or row["target"] == target
        ]
        if not subset:
            continue
        summary.append(
            {
                "target": target,
                "n_states": len(subset),
                "n_groups": len(gsubset),
                "closure_ready_mean": statistics.mean(
                    float(row["closure_ready"]) for row in subset
                ),
                "flat_primary_mean": statistics.mean(
                    float(row["flat_primary"]) for row in subset
                ),
                "flat_secondary_mean": statistics.mean(
                    float(row["flat_secondary"]) for row in subset
                ),
                "best_handoff_ca_rmsd_A_mean": statistics.mean(
                    float(row["best_handoff_ca_rmsd_A"]) for row in subset
                ),
                "closure_ready_spearman_mean": (
                    statistics.mean(
                        float(row["spearman_closure_ready"]) for row in gsubset
                    )
                    if gsubset
                    else float("nan")
                ),
                "flat_primary_spearman_mean": (
                    statistics.mean(
                        float(row["spearman_flat_primary"]) for row in gsubset
                    )
                    if gsubset
                    else float("nan")
                ),
                "flat_secondary_spearman_mean": (
                    statistics.mean(
                        float(row["spearman_flat_secondary"]) for row in gsubset
                    )
                    if gsubset
                    else float("nan")
                ),
                "failed_handoffs": sum(bool(row["failed"]) for row in subset),
                "max_bond_length_drift_A": max(
                    float(row["max_bond_length_drift_A"]) for row in subset
                ),
                "max_bond_angle_drift_rad": max(
                    float(row["max_bond_angle_drift_rad"]) for row in subset
                ),
            }
        )
    return summary


def validate_matrix(rows: list[dict[str, object]]) -> None:
    observed = [
        (
            str(row["target"]),
            int(row["seed"]),
            int(row["checkpoint"]),
        )
        for row in rows
    ]
    expected = expected_run_keys()
    if (
        len(observed) != len(expected)
        or len(set(observed)) != len(expected)
        or set(observed) != set(expected)
    ):
        raise AssertionError(
            f"measurement matrix mismatch: observed={len(observed)} expected={len(expected)}"
        )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    rows: list[dict[str, object]] = []
    for target in p9.TARGET_NAMES:
        for seed in p9.SEEDS:
            rows.extend(run_target_seed(target, seed))

    validate_matrix(rows)
    acceptance = p9.adjudicate(rows)
    group_correlations = all_observable_group_correlations(rows)
    summary = grouped_summary(rows, group_correlations)
    comparisons = list(acceptance["primary_comparisons"])
    manifest = build_run_manifest()

    write_csv(OUT / "p9_results.csv", rows)
    write_csv(OUT / "p9_group_correlations.csv", group_correlations)
    write_csv(OUT / "p9_primary_comparisons.csv", comparisons)
    write_csv(OUT / "p9_summary.csv", summary)
    (OUT / "p9_acceptance.json").write_text(
        json.dumps(acceptance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "p9_run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_sha256sums(
        OUT,
        names=tuple(
            name
            for name in REQUIRED_OUTPUTS
            if name != "SHA256SUMS.txt"
        ),
    )

    print(json.dumps(acceptance, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
