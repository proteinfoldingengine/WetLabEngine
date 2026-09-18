from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "P8_RECOVERED_SOURCE_MANIFEST.json"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_bundle(label: str):
    base = ROOT / f"recovered_{label}"
    dag = _load_module(f"p8_{label}_dag", base / "dag_engine.py")
    force = _load_module(f"p8_{label}_force", base / "force_field.py")
    history = _load_module(f"p8_{label}_history", base / "metrics_history.py")
    loader = _load_module(f"p8_{label}_loader", base / "config_loader.py")
    constants = _load_module(f"p8_{label}_constants", base / "physics_constants.py")
    with contextlib.redirect_stdout(io.StringIO()):
        config = loader.load_config(
            str(base / "1ubq_baseline.yaml"),
            constants.GLOBAL_PHYSICS_CONSTANTS,
        )
    return base, dag, force, history, config


def _integrity_result() -> tuple[bool, dict]:
    manifest = json.loads(MANIFEST.read_text())
    checks = {}
    for bundle in manifest["bundles"].values():
        for record in bundle["files"]:
            path = ROOT / record["path"]
            observed = _sha256(path)
            checks[record["path"]] = {
                "expected_sha256": record["sha256"],
                "observed_sha256": observed,
                "match": observed == record["sha256"],
                "drive_id": record["drive_id"],
                "git_blob_sha": record["git_blob_sha"],
            }
    return all(v["match"] for v in checks.values()), checks


def _runner_order(base: Path) -> dict:
    source = (base / "main.py").read_text()
    append_pos = source.index("metrics_history.betti_history.append(betti1_count)")
    dag_pos = source.index("dag_engine.update_and_get_params")
    force_pos = source.index("force_field.calculate_total_force_loss")
    phi_detached = "phi_tensor.std().item()" in source
    return {
        "betti_history_append_before_dag": append_pos < dag_pos,
        "dag_before_force_loss": dag_pos < force_pos,
        "phi_rms_detached_to_python_scalar": phi_detached,
    }


def _trace_and_forces(label: str) -> dict:
    base, dag, force_mod, history_mod, config = _load_bundle(label)
    hist = history_mod.MetricsHistory(
        memory_window=config["memory_window"],
        global_constants=config,
    )
    engine = dag.DagEngine(dag.DAG_SCHEMA, config, dag._dag_force_mapping)
    threshold = int(config["topological_gating"]["betti_threshold"])
    phases = []
    transitions = []
    active_at_step0 = None
    active_at_step99 = None

    with contextlib.redirect_stdout(io.StringIO()):
        for step in range(100):
            hist.betti_history.append(threshold)
            active, _, transitioned = engine.update_and_get_params(
                {"betti1_count": threshold}, hist, step
            )
            phases.append(engine.get_current_phase_name())
            if step == 0:
                active_at_step0 = dict(active)
            if step == 99:
                active_at_step99 = dict(active)
            if transitioned:
                transitions.append(step)

    p0 = set(dag.DAG_SCHEMA["phases"][0]["activated_forces"])
    p1 = set(dag.DAG_SCHEMA["phases"][1]["activated_forces"])

    device = torch.device("cpu")
    ff = force_mod.ForceField(config, device)

    coords = torch.tensor(
        [
            [0.0, 0.0, 0.0],
            [2.7, 0.4, 0.2],
            [5.3, -0.6, 0.7],
            [7.8, 1.1, -0.2],
            [10.1, -0.2, 1.3],
        ],
        dtype=torch.float64,
        requires_grad=True,
    )
    fractal = ff.apply_fractal_compaction_funnel(
        coords, {"k_df_funnel": config["k_df_funnel"]}
    )
    fractal_grad = torch.autograd.grad(fractal, coords)[0]
    fractal_grad_norm = float(torch.linalg.vector_norm(fractal_grad).item())

    e_coords = coords.detach().clone().requires_grad_(True)
    charges = torch.tensor([1.0, -1.0, 1.0, -1.0, 1.0], dtype=torch.float64)
    electro = ff.apply_screened_electrostatics(
        e_coords,
        charges,
        {"k_electrostatic_base": config["k_electrostatic_base"]},
    )
    electro_grad = torch.autograd.grad(electro, e_coords)[0]
    electro_grad_norm = float(torch.linalg.vector_norm(electro_grad).item())

    result = {
        "configured_betti_threshold": threshold,
        "configured_dag_transition_lifetime": int(
            config["topological_gating"]["dag_transition_lifetime"]
        ),
        "configured_force_activation_lifetime": int(
            config["topological_gating"]["force_activation_lifetime"]
        ),
        "phase_step0": phases[0],
        "phase_step98": phases[98],
        "phase_step99": phases[99],
        "transition_steps": transitions,
        "lockin_minus_compaction": sorted(p1 - p0),
        "step0_active_param_keys": sorted((active_at_step0 or {}).keys()),
        "step99_active_param_keys": sorted((active_at_step99 or {}).keys()),
        "fractal_coordinate_gradient_norm": fractal_grad_norm,
        "electrostatic_coordinate_gradient_norm": electro_grad_norm,
        "runner_order": _runner_order(base),
    }

    if label == "patch624":
        isolated_coords = torch.tensor(
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
            dtype=torch.float64,
            requires_grad=True,
        )
        gamma = torch.tensor(3.0, dtype=torch.float64, requires_grad=True)
        zero_angles = torch.zeros(2, dtype=torch.float64)
        isolated_hist = history_mod.MetricsHistory(
            memory_window=config["memory_window"],
            global_constants=config,
        )
        total, individual, _ = ff.calculate_total_force_loss(
            isolated_coords,
            zero_angles,
            zero_angles,
            gamma,
            ["A", "A"],
            torch.zeros(2, dtype=torch.float64),
            {"k_torsion_penalty": config["k_torsion_penalty"]},
            {"betti1_count": 0, "phi_rms": 2.0},
            isolated_hist,
            "LockIn",
            0,
        )
        coord_grad, gamma_grad = torch.autograd.grad(
            total, [isolated_coords, gamma], allow_unused=True
        )
        result["torsional_penalty"] = {
            "present": "torsional_incoherence_penalty_loss" in individual,
            "coordinate_gradient_is_none": coord_grad is None,
            "gamma_gradient": None if gamma_grad is None else float(gamma_grad.item()),
        }

    return result


def build_result() -> dict:
    integrity_ok, integrity = _integrity_result()
    p622 = _trace_and_forces("patch622")
    p624 = _trace_and_forces("patch624")

    conditions = {
        "frozen_source_hashes_verified": integrity_ok,
        "p622_runner_appends_history_before_dag_before_force": (
            p622["runner_order"]["betti_history_append_before_dag"]
            and p622["runner_order"]["dag_before_force_loss"]
        ),
        "p622_compaction_not_skipped": p622["phase_step0"] == "Compaction",
        "p622_transition_step_99_under_continuously_qualifying_history": (
            p622["phase_step98"] == "Compaction"
            and p622["phase_step99"] == "LockIn"
            and p622["transition_steps"] == [99]
        ),
        "p622_lockin_adds_electrostatics_and_contacts": (
            p622["lockin_minus_compaction"]
            == ["contact_springs", "screened_electrostatics"]
        ),
        "p622_fractal_has_coordinate_gradient": (
            math.isfinite(p622["fractal_coordinate_gradient_norm"])
            and p622["fractal_coordinate_gradient_norm"] > 0.0
        ),
        "p622_electrostatics_has_coordinate_gradient": (
            math.isfinite(p622["electrostatic_coordinate_gradient_norm"])
            and p622["electrostatic_coordinate_gradient_norm"] > 0.0
        ),
        "p624_lockin_adds_torsion_electrostatics_contacts": (
            p624["lockin_minus_compaction"]
            == [
                "contact_springs",
                "screened_electrostatics",
                "torsional_incoherence_penalty",
            ]
        ),
        "p624_runner_detaches_phi_rms": p624["runner_order"][
            "phi_rms_detached_to_python_scalar"
        ],
        "p624_torsion_is_gamma_not_direct_coordinate_gradient": (
            p624["torsional_penalty"]["present"]
            and p624["torsional_penalty"]["coordinate_gradient_is_none"]
            and p624["torsional_penalty"]["gamma_gradient"] is not None
            and abs(p624["torsional_penalty"]["gamma_gradient"]) > 0.0
        ),
    }

    verdict = (
        "REOPEN_RULE_SATISFIED_DISTINCT_HISTORICAL_MECHANISM_SOURCE_LEVEL"
        if all(conditions.values())
        else "SOURCE_CERTIFICATION_INCOMPLETE"
    )
    return {
        "schema": "protein-p8-source-certification-v1",
        "p7_reference": {
            "closeout_commit": "0e156790b961abdebcd288b333b44c2e6df05d61",
            "certified_source_head": "72c6d464cad50183fd17ac932b40745438576331",
            "workflow_run": 35298063514,
            "artifact_id": 10528821674,
            "artifact_sha256": "c34e49c1ce9f23eae00afa2e0f15b25f15509acc275d4372d5e47726ad33f02d",
        },
        "conditions": conditions,
        "p622": p622,
        "p624": p624,
        "source_integrity": integrity,
        "raw_historical_execution_log_recovered": False,
        "scope": "source-level mechanism certification only; no historical folding result validated",
        "verdict": verdict,
    }


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
