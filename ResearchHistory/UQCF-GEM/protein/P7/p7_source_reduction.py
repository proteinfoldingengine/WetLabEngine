from __future__ import annotations

import ast
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "recovered_stable_dag"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import dag_engine  # noqa: E402


EXPECTED_SHA256 = {
    "main.py": "71500484969c5e67db0f106f1417be57274c9a5eb71e886df98e55a4b918c6be",
    "dag_engine.py": "32dd940a4d81d1b718f040cb9944e13586792928fbc869260b8120e0fb69d92d",
    "force_field.py": "2d13e3b00dada665724a41ce3a9acc1eb69f2389cbdf465bd9eefa53936ba44e",
    "physics_constants.py": "1a5aa4ecea48e755f190e797d5c625053dde1dd8627bb52ebf9d088634c858ee",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def function_loaded_names(path: Path, function_name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return {
                n.id
                for n in ast.walk(node)
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
            }
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == function_name:
                    return {
                        n.id
                        for n in ast.walk(child)
                        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
                    }
    raise KeyError(function_name)


def main() -> None:
    hashes = {name: sha256(SRC / name) for name in EXPECTED_SHA256}

    zero_history_metrics = {
        "d2S_dt2": 0.0,
        "dgamma_dt": 0.0,
        "dphi_rms_dt": 0.0,
        "dgamma_dt_prev": 0.0,
        "phi_rms_variance": 99.0,
        "max_phi_rms_variance": 1.0,
        "gamma_bar": 1.0,
        "betti1_delta": 99.0,
        "df": 0.1,
    }

    exit_value, exit_reason = dag_engine.trigger_initial_relaxation_exit(
        zero_history_metrics, {}
    )

    constants = {
        "k_gamma_surge": 2.0,
        "k_phi_torque_base": 1.0,
        "k_lj_repulsion_base": 0.1,
        "k_df_funnel": 8000.0,
        "k_entropy_pulse": 1.5,
        "k_contact_spring_base": 0.30,
    }
    d = dag_engine.DagEngine(
        dag_engine.DAG_SCHEMA, constants, dag_engine._dag_force_mapping
    )
    phase_before = d.get_current_phase_name()
    historical_console = io.StringIO()
    with contextlib.redirect_stdout(historical_console):
        d.update_phase(zero_history_metrics, 0)
    phase_after = d.get_current_phase_name()

    phases = dag_engine.DAG_SCHEMA["phases"]
    p0 = set(phases[0]["activated_forces"])
    p1 = set(phases[1]["activated_forces"])
    p2 = set(phases[2]["activated_forces"])

    # In main.py update_phase is called before active_params are copied and before
    # calculate_total_force_loss is called. Therefore a step-0 transition means
    # phase-0 forces never govern an optimizer step.
    main_text = (SRC / "main.py").read_text(encoding="utf-8-sig")
    update_pos = main_text.index("dag_engine.update_phase(metrics_for_physics, step)")
    copy_pos = main_text.index("step_active_params = dag_engine.active_params.copy()")
    loss_pos = main_text.index("force_field.calculate_total_force_loss(")

    dag_text = (SRC / "dag_engine.py").read_text(encoding="utf-8-sig").lower()
    force_text = (SRC / "force_field.py").read_text(encoding="utf-8-sig").lower()

    df_loaded_names = function_loaded_names(
        SRC / "force_field.py", "apply_fractal_compaction_funnel"
    )

    result = {
        "schema": "protein-p7-source-reduction-v1",
        "source_hashes": hashes,
        "hashes_match_freeze": hashes == EXPECTED_SHA256,
        "initial_exit_triggered_with_source_initial_history": bool(exit_value),
        "initial_exit_reason": exit_reason,
        "phase_before_step0_update": phase_before,
        "phase_after_step0_update": phase_after,
        "historical_step0_console": historical_console.getvalue().strip(),
        "main_calls_update_before_active_param_copy": update_pos < copy_pos,
        "main_calls_update_before_force_loss": update_pos < loss_pos,
        "phase0_effective_optimizer_steps": 0 if exit_value and update_pos < loss_pos else None,
        "phase0_forces": sorted(p0),
        "phase1_forces": sorted(p1),
        "phase2_forces": sorted(p2),
        "phase1_minus_phase0": sorted(p1 - p0),
        "phase2_minus_phase1": sorted(p2 - p1),
        "only_late_adaptive_force_addition_is_contact_springs": (p2 - p1) == {"contact_springs"},
        "fractal_funnel_loads_coords_argument": "coords" in df_loaded_names,
        "fractal_funnel_coordinate_gradient_path": "coords" in df_loaded_names,
        "dag_mentions_rmsd_or_native": ("rmsd" in dag_text or "native" in dag_text),
        "force_field_mentions_rmsd_or_native": ("rmsd" in force_text or "native" in force_text),
    }

    conditions = {
        "frozen_source_hashes_verified": result["hashes_match_freeze"],
        "phase0_skipped_before_first_force_application":
            result["phase0_effective_optimizer_steps"] == 0,
        "fractal_funnel_has_no_coordinate_gradient_path":
            result["fractal_funnel_coordinate_gradient_path"] is False,
        "only_late_adaptive_force_addition_is_contact_springs":
            result["only_late_adaptive_force_addition_is_contact_springs"] is True,
        "recovered_dag_is_native_blind":
            result["dag_mentions_rmsd_or_native"] is False,
        "recovered_force_field_is_native_blind":
            result["force_field_mentions_rmsd_or_native"] is False,
    }
    result["conditions"] = conditions
    result["verdict"] = (
        "NO_DISTINCT_MULTIFORCE_ADAPTIVE_CONTROLLER_AFTER_SOURCE_REDUCTION"
        if all(conditions.values())
        else "SOURCE_REDUCTION_INCONCLUSIVE"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
