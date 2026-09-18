from __future__ import annotations

import ast
import hashlib
import io
import json
import contextlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAPSHOTS = {
    "globular_fold_qis": ROOT / "recovered_globular_fold_qis",
    "stable_globular_qis_best": ROOT / "recovered_stable_globular_qis_best",
}
EXPECTED_HASHES = {
    "globular_fold_qis": {
        "main.py": "7c461d6cb91531caf71b78c92e90244ba41b87323748e37c507670fb54ef94b3",
        "dag_engine.py": "ee2d2f3148105815e0670b83d7dc62427e4637f732539343943506fe29b9b91e",
        "force_field.py": "69dde0b4a4de06798963c7bc489b13143cb2c5bf70b500fa1b420347f52230ce",
        "1ubq_baseline.yaml": "2d1860bf586a5cb36d67f688aca032b2db262f8f77be4da92dc2aa45a2fe8638",
    },
    "stable_globular_qis_best": {
        "main.py": "a78b3c638682e206178e6022748d75cab2937de3b737e3c53b3fa9be1dfb0760",
        "dag_engine.py": "1eccbcdd4367db5ee63459e631657e634788387208d113eb7713880b2c08b43f",
        "force_field.py": "1aa99c3e681c1c9a8c9e591e2c514e3762ed568b2fc5d2725313aa3b97578935",
        "1ubq_baseline.yaml": "57d3ff93e1762b54e3495bbd401f29bf9bb236e836af238f0d56544625d0da91",
    },
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def assignment_literal(tree: ast.Module, name: str):
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(n.value)
    raise AssertionError(f"missing assignment: {name}")

def class_node(tree: ast.Module, name: str) -> ast.ClassDef:
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == name:
            return n
    raise AssertionError(f"missing class: {name}")

def method_source(text: str, tree: ast.Module, class_name: str, method: str) -> str:
    c = class_node(tree, class_name)
    for n in c.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == method:
            return ast.get_source_segment(text, n) or ""
    raise AssertionError(f"missing method: {class_name}.{method}")

def execute_dag_class(tree: ast.Module):
    c = class_node(tree, "DagEngine")
    mod = ast.Module(body=[c], type_ignores=[])
    ast.fix_missing_locations(mod)
    ns = {}
    exec(compile(mod, "<recovered-dag>", "exec"), ns)
    return ns["DagEngine"]

def config_int(text: str, key: str) -> int:
    m = re.search(rf"^\s*{re.escape(key)}:\s*(\d+)\s*$", text, re.MULTILINE)
    if not m:
        raise AssertionError(f"missing config key {key}")
    return int(m.group(1))

def analyze(name: str, root: Path) -> dict:
    dag_text = (root / "dag_engine.py").read_text(encoding="utf-8")
    ff_text = (root / "force_field.py").read_text(encoding="utf-8")
    main_text = (root / "main.py").read_text(encoding="utf-8")
    cfg_text = (root / "1ubq_baseline.yaml").read_text(encoding="utf-8")
    dag_tree = ast.parse(dag_text)
    ff_tree = ast.parse(ff_text)

    schema = assignment_literal(dag_tree, "DAG_SCHEMA")
    mapping = assignment_literal(dag_tree, "_dag_force_mapping")
    p0 = set(schema["phases"][0]["activated_forces"])
    p1 = set(schema["phases"][1]["activated_forces"])

    DagEngine = execute_dag_class(dag_tree)
    constants = {
        "topological_gating": {
            "betti_threshold": config_int(cfg_text, "betti_threshold"),
            "dag_transition_lifetime": config_int(cfg_text, "dag_transition_lifetime"),
            "force_activation_lifetime": config_int(cfg_text, "force_activation_lifetime"),
        }
    }
    for target in set(mapping.values()):
        constants[target] = 1.0

    class H:
        def __init__(self, lifetime): self.lifetime = lifetime
        def get_betti1_lifetime(self, threshold=8): return self.lifetime

    e = DagEngine(schema, constants, mapping)
    with contextlib.redirect_stdout(io.StringIO()):
        _, _, t0 = e.update_and_get_params({"betti1_count": 8}, H(1), 0)
        phase0 = e.get_current_phase_name()
        _, _, t99 = e.update_and_get_params({"betti1_count": 8}, H(99), 99)
        phase99 = e.get_current_phase_name()
        _, _, t100 = e.update_and_get_params({"betti1_count": 8}, H(100), 100)
        phase100 = e.get_current_phase_name()

    fractal = method_source(ff_text, ff_tree, "ForceField", "apply_fractal_compaction_funnel")
    electro = method_source(ff_text, ff_tree, "ForceField", "apply_screened_electrostatics")
    total = method_source(ff_text, ff_tree, "ForceField", "calculate_total_force_loss")

    return {
        "hashes_match_freeze": all(sha(root/f) == h for f,h in EXPECTED_HASHES[name].items()),
        "hashes": {f: sha(root/f) for f in EXPECTED_HASHES[name]},
        "phase0": schema["phases"][0]["name"],
        "phase1": schema["phases"][1]["name"],
        "phase1_minus_phase0": sorted(p1-p0),
        "step0_transitioned": bool(t0),
        "phase_after_step0": phase0,
        "step99_transitioned": bool(t99),
        "phase_after_step99": phase99,
        "step100_transitioned": bool(t100),
        "phase_after_step100": phase100,
        "fractal_loads_coords": "coords - coords.mean" in fractal and "return k_df * rg" in fractal,
        "electrostatics_loads_coords": "torch.cdist(coords, coords)" in electro and "dist_matrix" in electro,
        "torsional_phi_metric_rewrapped_as_tensor": "torch.tensor(phi_rms" in total,
        "history_before_dag": main_text.find("metrics_history.betti_history.append") < main_text.find("dag_engine.update_and_get_params"),
        "dag_before_force_loss": main_text.find("dag_engine.update_and_get_params") < main_text.find("force_field.calculate_total_force_loss"),
        "force_loss_before_backward": main_text.find("force_field.calculate_total_force_loss") < main_text.find("total_loss.backward"),
        "config_betti_threshold": config_int(cfg_text, "betti_threshold"),
        "config_dag_transition_lifetime": config_int(cfg_text, "dag_transition_lifetime"),
        "config_force_activation_lifetime": config_int(cfg_text, "force_activation_lifetime"),
    }

def main():
    out={name:analyze(name,root) for name,root in SNAPSHOTS.items()}
    out["classification"]={
        "p7_contact_only_reduction_applies_to_these_snapshots": False,
        "exact_named_patch_release_provenance": False,
        "reason":"Recovered Drive snapshots retain Compaction through the configured topology lifetime, use coords in the fractal term, and add screened electrostatics together with contacts at LockIn.",
    }
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
