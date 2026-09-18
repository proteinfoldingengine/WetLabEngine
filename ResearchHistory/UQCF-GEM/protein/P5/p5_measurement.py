from __future__ import annotations

import csv
import json
import os
import statistics
from pathlib import Path

import numpy as np
import torch

import p5_core as p5

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "measurement_output"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def grouped_summary(results: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target in ("1VII", "1CRN", "pooled"):
        for mode in p5.MODES:
            subset = [
                r for r in results
                if r["mode"] == mode and (target == "pooled" or r["target"] == target)
            ]
            vals = [float(r["best_ca_rmsd_A"]) for r in subset]
            finals = [float(r["final_ca_rmsd_A"]) for r in subset]
            contacts = [float(r["final_contact_recovery"]) for r in subset]
            torsions = [float(r["final_native_torsion_rmse_rad"]) for r in subset]
            rows.append(
                {
                    "target": target,
                    "mode": mode,
                    "n": len(subset),
                    "best_ca_rmsd_mean_A": statistics.mean(vals),
                    "best_ca_rmsd_median_A": statistics.median(vals),
                    "final_ca_rmsd_mean_A": statistics.mean(finals),
                    "final_contact_recovery_mean": statistics.mean(contacts),
                    "final_native_torsion_rmse_mean_rad": statistics.mean(torsions),
                    "max_bond_length_drift_A": max(float(r["max_bond_length_drift_A"]) for r in subset),
                    "max_bond_angle_drift_rad": max(float(r["max_bond_angle_drift_rad"]) for r in subset),
                }
            )
    return rows


def paired_diffs(
    results: list[dict[str, object]],
    control: str,
) -> tuple[list[float], dict[str, list[float]]]:
    index = {(str(r["target"]), int(r["seed"]), str(r["mode"])): r for r in results}
    pooled: list[float] = []
    by_target = {"1VII": [], "1CRN": []}
    for target in ("1VII", "1CRN"):
        for seed in p5.SEEDS:
            candidate = float(index[(target, seed, "rama_entropy")]["best_ca_rmsd_A"])
            baseline = float(index[(target, seed, control)]["best_ca_rmsd_A"])
            d = candidate - baseline
            pooled.append(d)
            by_target[target].append(d)
    return pooled, by_target


def adjudicate(results: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    summary = grouped_summary(results)
    pooled_means = {
        row["mode"]: float(row["best_ca_rmsd_mean_A"])
        for row in summary
        if row["target"] == "pooled"
    }

    comparisons: list[dict[str, object]] = []
    raw_ps = []
    for control in ("rama", "variance"):
        diffs, by_target = paired_diffs(results, control)
        p_raw = p5.exact_sign_flip_p(diffs)
        raw_ps.append(p_raw)
        comparisons.append(
            {
                "comparison": f"rama_entropy_vs_{control}",
                "n_pairs": len(diffs),
                "candidate_minus_control_mean_A": statistics.mean(diffs),
                "candidate_minus_control_median_A": statistics.median(diffs),
                "candidate_wins": sum(d < 0 for d in diffs),
                "raw_exact_sign_flip_p": p_raw,
                "1VII_mean_delta_A": statistics.mean(by_target["1VII"]),
                "1CRN_mean_delta_A": statistics.mean(by_target["1CRN"]),
            }
        )

    adj = p5.holm_two(raw_ps[0], raw_ps[1])
    for row, value in zip(comparisons, adj):
        row["holm_adjusted_p"] = value

    index_cmp = {row["comparison"]: row for row in comparisons}
    candidate_mean = pooled_means["rama_entropy"]
    primary_other = [m for m in p5.PRIMARY_MODES if m != "rama_entropy"]

    all_geometry_good = all(
        float(r["max_bond_length_drift_A"]) < 1e-8
        and float(r["max_bond_angle_drift_rad"]) < 1e-8
        for r in results
    )
    no_failures = all(not bool(r["failed"]) for r in results)

    conditions = {
        "rama_entropy_lowest_pooled_mean_of_primary_modes":
            all(candidate_mean < pooled_means[m] for m in primary_other),
        "rama_entropy_lower_than_rama_on_1VII":
            float(index_cmp["rama_entropy_vs_rama"]["1VII_mean_delta_A"]) < 0.0,
        "rama_entropy_lower_than_rama_on_1CRN":
            float(index_cmp["rama_entropy_vs_rama"]["1CRN_mean_delta_A"]) < 0.0,
        "rama_entropy_lower_than_variance_on_1VII":
            float(index_cmp["rama_entropy_vs_variance"]["1VII_mean_delta_A"]) < 0.0,
        "rama_entropy_lower_than_variance_on_1CRN":
            float(index_cmp["rama_entropy_vs_variance"]["1CRN_mean_delta_A"]) < 0.0,
        "rama_entropy_vs_rama_holm_p_lt_0_05":
            float(index_cmp["rama_entropy_vs_rama"]["holm_adjusted_p"]) < 0.05,
        "rama_entropy_vs_variance_holm_p_lt_0_05":
            float(index_cmp["rama_entropy_vs_variance"]["holm_adjusted_p"]) < 0.05,
        "all_runs_preserve_covalent_geometry": all_geometry_good,
        "no_numerical_failures": no_failures,
    }
    decision = (
        "GO_TPO_ENTROPY_SURVIVES_CONSTRAINED_BACKBONE"
        if all(conditions.values())
        else "NO_GO_TPO_ENTROPY_INCREMENT"
    )
    acceptance = {
        "decision": decision,
        "conditions": conditions,
        "pooled_best_ca_rmsd_mean_A": pooled_means,
        "primary_comparisons": comparisons,
        "claim_boundary": (
            "GO would establish only incremental predictive/optimization value of the recovered "
            "entropy observable under this constrained protocol; NO-GO closes TPO-entropy-specific "
            "continuation, not the kinematic representation itself."
        ),
    }
    return comparisons, acceptance


def main() -> None:
    OUT.mkdir(exist_ok=True)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    results: list[dict[str, object]] = []
    traces: list[dict[str, object]] = []

    for target in ("1VII", "1CRN"):
        for seed in p5.SEEDS:
            for mode in p5.MODES:
                row, trace = p5.run_one(target, seed, mode)
                results.append(row)
                traces.extend(trace)

    summary = grouped_summary(results)
    comparisons, acceptance = adjudicate(results)

    manifest = {
        "schema": "protein-p5-measurement-v1",
        "git_head": os.environ.get("GITHUB_SHA"),
        "targets": ["1VII", "1CRN"],
        "seeds": list(p5.SEEDS),
        "modes": list(p5.MODES),
        "primary_modes": list(p5.PRIMARY_MODES),
        "steps": p5.STEPS,
        "learning_rate": p5.LEARNING_RATE,
        "gradient_match_ratio": p5.GRADIENT_MATCH_RATIO,
        "historical_entropy_k": p5.HISTORICAL_ENTROPY_K,
        "optimizer": "Adam",
        "dtype": "float64",
        "device": "cpu",
        "torch_deterministic_algorithms": True,
        "native_geometry_used_in_objective": False,
        "common_random_initial_torsions": True,
        "geometry_contract": "fixed source bond lengths, bond angles and omega; phi/psi only",
    }

    write_csv(OUT / "p5_results.csv", results)
    write_csv(OUT / "p5_traces.csv", traces)
    write_csv(OUT / "p5_summary.csv", summary)
    write_csv(OUT / "p5_primary_comparisons.csv", comparisons)
    (OUT / "p5_acceptance.json").write_text(
        json.dumps(acceptance, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (OUT / "p5_run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(acceptance, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
