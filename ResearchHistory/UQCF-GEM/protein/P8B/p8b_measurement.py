from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import statistics
from pathlib import Path

import torch

import p8b_core as p8b

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "measurement_output"
CHECKPOINTS = (0, 99, 100, 500, 1000, 2000)
REQUIRED_OUTPUTS = (
    "p8b_results.csv",
    "p8b_controller_traces.csv",
    "p8b_checkpoint_traces.csv",
    "p8b_summary.csv",
    "p8b_primary_comparisons.csv",
    "p8b_acceptance.json",
    "p8b_run_manifest.json",
    "SHA256SUMS.txt",
)
CONTROLS = (
    "fixed_step99_lockin",
    "static_lockin",
    "compaction_only",
)
EXPECTED_HISTORICAL_HASHES = {
    ROOT.parent / "P8" / "recovered_stable_globular_qis_best" / "dag_engine.py":
        "1eccbcdd4367db5ee63459e631657e634788387208d113eb7713880b2c08b43f",
    ROOT.parent / "P8" / "recovered_stable_globular_qis_best" / "force_field.py":
        "1aa99c3e681c1c9a8c9e591e2c514e3762ed568b2fc5d2725313aa3b97578935",
    ROOT / "recovered_common" / "physics_metrics.py":
        "1663b78670077936129989654684158f2bbe989e1533c90bac3247598086ca46",
    ROOT / "recovered_common" / "physics_constants.py":
        "2018c8335aa366be4598eb55df1dc6d5b7a5fe08b313ef12defaedc6e31ce708",
    ROOT.parent / "P8" / "recovered_globular_fold_qis" / "metrics_history.py":
        "bb5883f08721e2cf0394a3218fe890369eba47d3899ba8704010b886520b0bd6",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_integrity_selfcheck() -> bool:
    for path, expected in EXPECTED_HISTORICAL_HASHES.items():
        if not path.exists() or sha256_file(path) != expected:
            return False

    coincident = torch.zeros((10, 3), dtype=torch.float64)
    separated = (
        torch.arange(10, dtype=torch.float64).unsqueeze(1).repeat(1, 3)
        * 20.0
    )
    if p8b.historical_betti1_proxy(coincident) != 27:
        return False
    if p8b.historical_betti1_proxy(separated) != 0:
        return False

    history = p8b.HistoricalBettiHistory()
    for index in range(99):
        history.append(8)
        if index < 20:
            history.append(0)
    if history.qualifying_count() != 99:
        return False
    history.append(8)
    return history.qualifying_count() == 100


def expected_run_keys() -> list[tuple[str, int, str]]:
    return [
        (target, seed, mode)
        for target in p8b.TARGET_NAMES
        for seed in p8b.SEEDS
        for mode in p8b.MODES
    ]


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


def _controller_state(
    mode: str,
    controller: p8b.RecoveredController | None,
    last_event: dict[str, object] | None,
    transition_step: int | None,
    lockin_active_steps: int,
) -> dict[str, object]:
    if mode == "recovered_state_gate":
        qualifying = (
            controller.history.qualifying_count()
            if controller is not None
            else 0
        )
        phase = controller.phase if controller is not None else "Compaction"
    else:
        qualifying = (
            last_event.get("qualifying_count")
            if last_event is not None
            else None
        )
        phase = (
            str(last_event.get("phase"))
            if last_event is not None
            else "Compaction"
        )
    return {
        "phase": phase,
        "transition_step": transition_step,
        "qualifying_count": qualifying,
        "lockin_active_steps": int(lockin_active_steps),
    }


def simulate_trajectory(
    target,
    *,
    seed: int,
    mode: str,
    step_budget: int = p8b.STEPS,
    collect_trace: bool = True,
) -> dict[str, object]:
    if mode not in p8b.MODES:
        raise ValueError(mode)
    if step_budget < 0 or step_budget > p8b.STEPS:
        raise ValueError(step_budget)

    phi0, psi0 = p8b.initial_torsions_for_mode(target, seed, mode)
    phi_free = phi0.detach().clone().requires_grad_(True)
    psi = psi0.detach().clone().requires_grad_(True)
    optimizer = torch.optim.Adam(
        [phi_free, psi],
        lr=p8b.LEARNING_RATE,
    )
    controller = (
        p8b.RecoveredController()
        if mode == "recovered_state_gate"
        else None
    )
    snapshots: dict[int, tuple[torch.Tensor, torch.Tensor]] = {
        0: (
            phi_free.detach().clone(),
            psi.detach().clone(),
        )
    }
    controller_trace: list[dict[str, object]] = []
    failed = False
    failure_reason = ""
    completed_steps = 0
    transition_step: int | None = None
    lockin_active_steps = 0
    max_length_drift = 0.0
    max_angle_drift = 0.0
    last_event: dict[str, object] | None = None
    last_components: dict[str, float] = {}

    for step_index in range(step_budget):
        optimizer.zero_grad(set_to_none=True)

        _, _, _, modeled_ca, _ = p8b.reconstruct(
            target, phi_free, psi
        )
        force_names, event = p8b.force_names_for_step(
            mode,
            step_index,
            modeled_ca,
            controller,
        )
        last_event = dict(event)
        if bool(event.get("transitioned")):
            transition_step = step_index
        if bool(event.get("lockin_force_active")):
            lockin_active_steps += 1

        energy, _, components = p8b.coordinate_objective(
            target,
            phi_free,
            psi,
            force_names,
        )
        if not bool(torch.isfinite(energy)):
            failed = True
            failure_reason = f"nonfinite_energy_step_{step_index}"
            break

        energy.backward()
        if (
            phi_free.grad is None
            or psi.grad is None
            or not bool(torch.isfinite(phi_free.grad).all())
            or not bool(torch.isfinite(psi.grad).all())
        ):
            failed = True
            failure_reason = f"nonfinite_gradient_step_{step_index}"
            break

        optimizer.step()
        with torch.no_grad():
            phi_free.copy_(p8b.wrap_angle(phi_free))
            psi.copy_(p8b.wrap_angle(psi))

        completed_steps = step_index + 1
        _, _, n_after, ca_after, c_after = p8b.reconstruct(
            target, phi_free, psi
        )
        if not all(
            bool(torch.isfinite(value).all())
            for value in (n_after, ca_after, c_after)
        ):
            failed = True
            failure_reason = (
                f"nonfinite_coordinates_step_{step_index}"
            )
            break

        dl, da = p8b.covalent_drift(
            target,
            phi_free,
            psi,
        )
        max_length_drift = max(max_length_drift, float(dl))
        max_angle_drift = max(max_angle_drift, float(da))
        last_components = components

        if completed_steps in CHECKPOINTS:
            snapshots[completed_steps] = (
                phi_free.detach().clone(),
                psi.detach().clone(),
            )

        if collect_trace and mode == "recovered_state_gate":
            row: dict[str, object] = {
                "target": target.name,
                "seed": seed,
                "mode": mode,
                "optimizer_index": step_index,
                "completed_steps": completed_steps,
                "historical_betti1_proxy": int(event["proxy"]),
                "qualifying_count": int(
                    event["qualifying_count"]
                ),
                "phase": str(event["phase"]),
                "transitioned": bool(event["transitioned"]),
                "lockin_force_active": bool(
                    event["lockin_force_active"]
                ),
                "total_energy": float(energy.detach()),
            }
            for key, value in components.items():
                row[f"energy_{key}"] = value
            controller_trace.append(row)

    state = _controller_state(
        mode,
        controller,
        last_event,
        transition_step,
        lockin_active_steps,
    )
    return {
        "phi_free": phi_free.detach().clone(),
        "psi": psi.detach().clone(),
        "initial_phi_free": phi0.detach().clone(),
        "initial_psi": psi0.detach().clone(),
        "snapshots": snapshots,
        "controller_trace": controller_trace,
        "controller_state": state,
        "failed": failed,
        "failure_reason": failure_reason,
        "completed_steps": completed_steps,
        "max_bond_length_drift_A": max_length_drift,
        "max_bond_angle_drift_rad": max_angle_drift,
        "last_components": last_components,
    }


def native_contact_recall(
    model_ca: torch.Tensor,
    native_ca: torch.Tensor,
) -> float:
    model_d = torch.cdist(model_ca, model_ca)
    native_d = torch.cdist(native_ca, native_ca)
    pairs = [
        (i, j)
        for i in range(native_ca.shape[0])
        for j in range(
            i + p8b.p6.CONTACT_MIN_SEQ_SEPARATION,
            native_ca.shape[0],
        )
        if float(native_d[i, j])
        < p8b.p6.NATIVE_CONTACT_CUTOFF_A
    ]
    if not pairs:
        return float("nan")
    hits = sum(
        float(model_d[i, j])
        < p8b.p6.NATIVE_CONTACT_CUTOFF_A
        for i, j in pairs
    )
    return hits / len(pairs)


def evaluate_snapshot(
    target,
    phi_free: torch.Tensor,
    psi: torch.Tensor,
    *,
    mode: str,
    completed_steps: int,
) -> dict[str, object]:
    geometry, _, n, ca, c = p8b.reconstruct(
        target, phi_free, psi
    )
    precision, k = p8b.topk_native_contact_precision(
        ca, target.native_ca
    )
    modeled_rg = p8b.radius_of_gyration(ca)
    native_rg = p8b.radius_of_gyration(target.native_ca)
    dl, da = p8b.p6.covalent_drift(geometry, n, ca, c)
    return {
        "target": target.name,
        "mode": mode,
        "completed_steps": completed_steps,
        "topk_native_contact_precision": precision,
        "topk_contact_budget": k,
        "ca_rmsd_A": p8b.kabsch_rmsd(
            ca, target.native_ca
        ),
        "native_contact_recall": native_contact_recall(
            ca, target.native_ca
        ),
        "rg_A": modeled_rg,
        "native_rg_A": native_rg,
        "rg_ratio": modeled_rg / native_rg,
        "historical_betti1_proxy": p8b.historical_betti1_proxy(
            ca
        ),
        "max_bond_length_drift_A": float(dl),
        "max_bond_angle_drift_rad": float(da),
    }


def run_one(
    target_name: str,
    seed: int,
    mode: str,
) -> tuple[
    dict[str, object],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    target = p8b.load_target(target_name)
    simulation = simulate_trajectory(
        target,
        seed=seed,
        mode=mode,
        step_budget=p8b.STEPS,
        collect_trace=True,
    )

    checkpoint_rows: list[dict[str, object]] = []
    for completed_steps in sorted(simulation["snapshots"]):
        phi_free, psi = simulation["snapshots"][
            completed_steps
        ]
        row = evaluate_snapshot(
            target,
            phi_free,
            psi,
            mode=mode,
            completed_steps=completed_steps,
        )
        row["seed"] = seed
        checkpoint_rows.append(row)

    final_eval = evaluate_snapshot(
        target,
        simulation["phi_free"],
        simulation["psi"],
        mode=mode,
        completed_steps=int(simulation["completed_steps"]),
    )
    start_eval = next(
        row
        for row in checkpoint_rows
        if int(row["completed_steps"]) == 0
    )

    controller_state = simulation["controller_state"]
    final = {
        "target": target_name,
        "seed": seed,
        "mode": mode,
        "start_topk_native_contact_precision": float(
            start_eval["topk_native_contact_precision"]
        ),
        "final_topk_native_contact_precision": float(
            final_eval["topk_native_contact_precision"]
        ),
        "final_rg_ratio": float(final_eval["rg_ratio"]),
        "final_rg_A": float(final_eval["rg_A"]),
        "native_rg_A": float(final_eval["native_rg_A"]),
        "final_ca_rmsd_A": float(final_eval["ca_rmsd_A"]),
        "final_native_contact_recall": float(
            final_eval["native_contact_recall"]
        ),
        "final_historical_betti1_proxy": int(
            final_eval["historical_betti1_proxy"]
        ),
        "max_bond_length_drift_A": max(
            float(simulation["max_bond_length_drift_A"]),
            max(
                float(row["max_bond_length_drift_A"])
                for row in checkpoint_rows
            ),
        ),
        "max_bond_angle_drift_rad": max(
            float(simulation["max_bond_angle_drift_rad"]),
            max(
                float(row["max_bond_angle_drift_rad"])
                for row in checkpoint_rows
            ),
        ),
        "failed": bool(simulation["failed"]),
        "failure_reason": str(
            simulation["failure_reason"]
        ),
        "final_step": int(simulation["completed_steps"]),
        "transitioned_to_lockin": (
            controller_state["transition_step"] is not None
            if mode == "recovered_state_gate"
            else False
        ),
        "lockin_transition_step": controller_state[
            "transition_step"
        ],
        "lockin_active_steps": int(
            controller_state["lockin_active_steps"]
        ),
        "lockin_active_fraction": (
            int(controller_state["lockin_active_steps"])
            / p8b.STEPS
        ),
    }
    for key, value in simulation["last_components"].items():
        final[f"final_energy_{key}"] = value

    return (
        final,
        simulation["controller_trace"],
        checkpoint_rows,
    )


def grouped_summary(
    results: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target_name in (*p8b.TARGET_NAMES, "pooled"):
        for mode in p8b.MODES:
            subset = [
                row
                for row in results
                if row["mode"] == mode
                and (
                    target_name == "pooled"
                    or row["target"] == target_name
                )
            ]
            if not subset:
                continue
            precision = [
                float(
                    row[
                        "final_topk_native_contact_precision"
                    ]
                )
                for row in subset
            ]
            rg_ratio = [
                float(row["final_rg_ratio"])
                for row in subset
            ]
            rows.append(
                {
                    "target": target_name,
                    "mode": mode,
                    "n": len(subset),
                    "primary_precision_mean": statistics.mean(
                        precision
                    ),
                    "primary_precision_median": statistics.median(
                        precision
                    ),
                    "final_rg_ratio_mean": statistics.mean(
                        rg_ratio
                    ),
                    "final_rg_ratio_median": statistics.median(
                        rg_ratio
                    ),
                    "failed_runs": sum(
                        bool(row["failed"])
                        for row in subset
                    ),
                }
            )
    return rows


def paired_differences(
    results: list[dict[str, object]],
    control: str,
) -> tuple[list[float], dict[str, list[float]]]:
    index = {
        (
            str(row["target"]),
            int(row["seed"]),
            str(row["mode"]),
        ): row
        for row in results
    }
    pooled: list[float] = []
    by_target = {
        name: [] for name in p8b.TARGET_NAMES
    }
    for target_name in p8b.TARGET_NAMES:
        for seed in p8b.SEEDS:
            candidate = float(
                index[
                    (
                        target_name,
                        seed,
                        "recovered_state_gate",
                    )
                ][
                    "final_topk_native_contact_precision"
                ]
            )
            baseline = float(
                index[(target_name, seed, control)][
                    "final_topk_native_contact_precision"
                ]
            )
            delta = candidate - baseline
            pooled.append(delta)
            by_target[target_name].append(delta)
    return pooled, by_target


def adjudicate(
    results: list[dict[str, object]],
) -> dict[str, object]:
    observed_keys = [
        (
            str(row["target"]),
            int(row["seed"]),
            str(row["mode"]),
        )
        for row in results
    ]
    expected_keys = expected_run_keys()
    matrix_complete = (
        len(observed_keys) == len(expected_keys)
        and len(set(observed_keys)) == len(expected_keys)
        and set(observed_keys) == set(expected_keys)
    )

    if not matrix_complete:
        return {
            "decision":
                "NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",
            "conditions": {
                "complete_unique_72_run_matrix": False
            },
            "primary_comparisons": [],
        }

    summary = grouped_summary(results)
    pooled_means = {
        str(row["mode"]): float(
            row["primary_precision_mean"]
        )
        for row in summary
        if row["target"] == "pooled"
    }

    comparisons: list[dict[str, object]] = []
    raw_p: list[float] = []
    target_deltas: dict[str, dict[str, float]] = {}
    for control in CONTROLS:
        diffs, by_target = paired_differences(
            results, control
        )
        p_value = p8b.exact_sign_flip_p(diffs)
        raw_p.append(p_value)
        target_deltas[control] = {
            target: statistics.mean(values)
            for target, values in by_target.items()
        }
        comparisons.append(
            {
                "comparison":
                    f"recovered_state_gate_vs_{control}",
                "n_pairs": len(diffs),
                "candidate_minus_control_mean_precision":
                    statistics.mean(diffs),
                "candidate_minus_control_median_precision":
                    statistics.median(diffs),
                "candidate_wins": sum(
                    delta > 0 for delta in diffs
                ),
                "ties": sum(
                    delta == 0 for delta in diffs
                ),
                "raw_exact_sign_flip_p": p_value,
                **{
                    f"{target}_mean_delta_precision":
                        statistics.mean(values)
                    for target, values in by_target.items()
                },
            }
        )

    adjusted = p8b.holm_three(raw_p)
    for row, value in zip(comparisons, adjusted):
        row["holm_adjusted_p"] = value

    candidate_rows = [
        row
        for row in results
        if row["mode"] == "recovered_state_gate"
    ]

    candidate_final_by_target: dict[str, float] = {}
    candidate_start_by_target: dict[str, float] = {}
    candidate_rg_median: dict[str, float] = {}
    for target in p8b.TARGET_NAMES:
        subset = [
            row
            for row in candidate_rows
            if row["target"] == target
        ]
        candidate_final_by_target[target] = statistics.mean(
            float(
                row[
                    "final_topk_native_contact_precision"
                ]
            )
            for row in subset
        )
        candidate_start_by_target[target] = statistics.mean(
            float(
                row[
                    "start_topk_native_contact_precision"
                ]
            )
            for row in subset
        )
        candidate_rg_median[target] = statistics.median(
            float(row["final_rg_ratio"])
            for row in subset
        )

    geometry_good = all(
        float(row["max_bond_length_drift_A"]) < 1e-8
        and float(row["max_bond_angle_drift_rad"]) < 1e-8
        for row in results
    )
    numerical_good = all(
        not bool(row["failed"])
        and int(row["final_step"]) == p8b.STEPS
        and math.isfinite(
            float(
                row[
                    "final_topk_native_contact_precision"
                ]
            )
        )
        and math.isfinite(float(row["final_rg_ratio"]))
        for row in results
    )
    controller_used = all(
        bool(row["transitioned_to_lockin"])
        and int(row["lockin_active_steps"]) > 0
        for row in candidate_rows
    )

    conditions: dict[str, bool] = {
        "complete_unique_72_run_matrix":
            matrix_complete,
        "candidate_highest_pooled_mean_primary_precision":
            all(
                pooled_means["recovered_state_gate"]
                > pooled_means[mode]
                for mode in CONTROLS
            ),
        "candidate_beats_every_control_on_every_target":
            all(
                target_deltas[control][target] > 0.0
                for control in CONTROLS
                for target in p8b.TARGET_NAMES
            ),
        "all_three_holm_adjusted_p_lt_0_05":
            all(value < 0.05 for value in adjusted),
        "candidate_improves_from_start_on_every_target":
            all(
                candidate_final_by_target[target]
                > candidate_start_by_target[target]
                for target in p8b.TARGET_NAMES
            ),
        "all_candidate_trajectories_exercise_lockin":
            controller_used,
        "candidate_rg_ratio_gate_every_target":
            all(
                0.75
                <= candidate_rg_median[target]
                <= 1.25
                for target in p8b.TARGET_NAMES
            ),
        "all_runs_preserve_canonical_covalent_geometry":
            geometry_good,
        "all_runs_numerically_healthy":
            numerical_good,
        "native_information_firewall_passed":
            p8b.native_firewall_selfcheck(),
        "historical_source_integrity_and_proxy_passed":
            source_integrity_selfcheck(),
    }

    decision = (
        "GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION"
        if all(conditions.values())
        else "NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION"
    )
    return {
        "decision": decision,
        "conditions": conditions,
        "pooled_primary_precision_mean": pooled_means,
        "candidate_target_final_primary_mean":
            candidate_final_by_target,
        "candidate_target_start_primary_mean":
            candidate_start_by_target,
        "candidate_target_rg_ratio_median":
            candidate_rg_median,
        "primary_comparisons": comparisons,
        "claim_boundary": (
            "A GO establishes only transferable native-topology "
            "enrichment by the frozen recovered state-gated "
            "coordinate mechanism beyond same-force nonadaptive "
            "controls on the preregistered valid-backbone benchmark."
        ),
    }


def build_run_manifest() -> dict[str, object]:
    return {
        "schema": "protein-p8b-measurement-v1",
        "git_head": os.environ.get("GITHUB_SHA"),
        "preregistration_commit":
            "02683349f5c0d7c961b06401e8b6e5bdda9d2592",
        "p8_source_certification_run": 35358832587,
        "p8_source_certification_artifact": 10553705794,
        "targets": list(p8b.TARGET_NAMES),
        "seeds": list(p8b.SEEDS),
        "modes": list(p8b.MODES),
        "steps": p8b.STEPS,
        "learning_rate": p8b.LEARNING_RATE,
        "optimizer": "Adam",
        "dtype": "float64",
        "device": "cpu",
        "torch_deterministic_algorithms": True,
        "common_random_initial_torsions": True,
        "native_information_used_in_objective": False,
        "native_information_used_in_controller": False,
        "native_evaluation_timing":
            "post-trajectory/checkpoint-state generation only",
        "representation":
            "P6 target-independent canonical peptide geometry; phi/psi only",
        "historical_betti1_proxy":
            "max(0, int(E_nonadjacent_contacts - (N-1))) at 8 A",
        "qualifying_count_semantics":
            "count within maxlen-120 history; not necessarily consecutive",
        "dag_thresholds": {
            "proxy": p8b.BETTI_PROXY_THRESHOLD,
            "transition_count": p8b.DAG_QUALIFYING_COUNT,
            "force_count": p8b.FORCE_QUALIFYING_COUNT,
        },
        "fixed_lockin_first_optimizer_index":
            p8b.FIXED_LOCKIN_FIRST_STEP,
        "checkpoints_completed_steps": list(CHECKPOINTS),
        "primary_endpoint":
            "final fixed-budget top-K long-range native-contact precision",
        "rg_ratio_gate": [0.75, 1.25],
    }


def write_sha256sums(out: Path) -> None:
    names = [
        name
        for name in REQUIRED_OUTPUTS
        if name != "SHA256SUMS.txt"
    ]
    lines = [
        f"{sha256_file(out / name)}  {name}"
        for name in names
    ]
    (out / "SHA256SUMS.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    results: list[dict[str, object]] = []
    controller_traces: list[dict[str, object]] = []
    checkpoint_traces: list[dict[str, object]] = []

    for target, seed, mode in expected_run_keys():
        final, controller_rows, checkpoint_rows = run_one(
            target, seed, mode
        )
        results.append(final)
        controller_traces.extend(controller_rows)
        checkpoint_traces.extend(checkpoint_rows)

    summary = grouped_summary(results)
    acceptance = adjudicate(results)
    comparisons = acceptance["primary_comparisons"]
    manifest = build_run_manifest()

    write_csv(OUT / "p8b_results.csv", results)
    write_csv(
        OUT / "p8b_controller_traces.csv",
        controller_traces,
    )
    write_csv(
        OUT / "p8b_checkpoint_traces.csv",
        checkpoint_traces,
    )
    write_csv(OUT / "p8b_summary.csv", summary)
    write_csv(
        OUT / "p8b_primary_comparisons.csv",
        comparisons,
    )
    (OUT / "p8b_acceptance.json").write_text(
        json.dumps(acceptance, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    (OUT / "p8b_run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    write_sha256sums(OUT)

    print(json.dumps(acceptance, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
