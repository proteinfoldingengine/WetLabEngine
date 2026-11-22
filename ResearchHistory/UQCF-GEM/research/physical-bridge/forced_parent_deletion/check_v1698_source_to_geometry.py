"""Check the original V1698 source paths and ledger cases with frozen inputs."""
from collections import Counter
from copy import deepcopy
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import numpy as np


DIRECTORY = Path("Tmp/TOE/Einstein_12_V1698_valid_only_slow_atlas_closure_mp4_package/WorkProduct ")
FILES = {
    75: (
        "V1698_75_validator_failure_record_extraction_final_alignment_package.zip",
        "2f9109426d927d14a68f3319170d375fe51ae6ea970f8be9e32bbbdefc568038",
    ),
    76: (
        "V1698_76_multi_mode_full_stack_ledger_replication_run_package.zip",
        "755e72ada217b0f1011c9d4c64b12df2e89795806b7c7effb641b21477f35ff2",
    ),
    77: (
        "V1698_77_multimode_replication_postmortem_freeze_package.zip",
        "d241ab8fedc25e721887d6a74486930b191ec9eeab4acc4e418265e6bfcd4e77",
    ),
}
EMITTER_MEMBER = "V1698_75_full_stack_ledger_emitter_final_aligned.py"
VALIDATOR_MEMBER = "V1698_75_full_stack_ledger_validator_final_aligned.py"
FREEZE_MEMBER = "V1698_77_MULTIMODE_REPLICATION_POSTMORTEM_FREEZE_REPORT.md"
MERGED = "V1698_76_merged_full_stack_ledger/"
MODES = ("valid", "source_shuffle", "order_shuffle", "support_shuffle", "edge_package_shuffle", "cycle_package_shuffle")
DOMAINS = ("open", "closed_filled")
SEED = 169876
IDENTITY = np.eye(4, dtype=int).tolist()
ZERO = np.zeros((4, 4), dtype=int).tolist()


def rows(raw):
    return list(csv.DictReader(raw.decode().splitlines()))


def read_csv(path):
    return rows(path.read_bytes())


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def label_control(emitter, scratch):
    valid = scratch / "mode_valid"
    null = scratch / "mode_source_shuffle"
    emitter.emit(valid, 2, 2, SEED, "closed_filled", "baseline", "valid")
    emitter.emit(null, 2, 2, SEED, "closed_filled", "baseline", "source_shuffle")
    names = {p.name for p in valid.iterdir()}
    assert names == {p.name for p in null.iterdir()}
    changed = sorted(n for n in names if (valid / n).read_bytes() != (null / n).read_bytes())
    assert changed == ["gate_checks.csv", "null_transform_log.csv", "run_manifest.csv"]
    gates = [read_csv(folder/"gate_checks.csv")[0] for folder in (valid, null)]
    rates = [gate["curvature_null_B_corrupt_rate"] for gate in gates]
    assert rates == ["1.0", "0.5"] and all(gate["passed"] == "true" for gate in gates)
    return {"changed_tables":changed,"unchanged_tables":sorted(names-set(changed)), "reported_curvature_rates":rates}


def compare_geometry(emitter, inputs, changed_transport=False):
    edges = emitter.build_edges(inputs, 2, 2, SEED, "closed_filled")
    if changed_transport:
        target, = [row for row in edges if (row["p"], row["q"]) == (0, 1)]
        matrix = emitter.T(target)
        matrix[0, 0] += 1 / 8
        target["T_pq"] = emitter.mat_s(matrix)
        target["A_pq"] = emitter.mat_s(matrix - np.eye(4))
    cycles = emitter.candidate_cycles(edges)
    r2 = emitter.build_R2(edges, cycles)
    r3 = emitter.build_R3(edges, cycles)
    w1 = emitter.build_W1(edges)
    w3 = emitter.build_W3(emitter.build_W2(cycles, edges, w1))
    br = emitter.build_bianchi(w3, r2, r3)
    signed, = [x for x in emitter.build_signed_boundary_pairing(edges, "closed_filled") if x["variation"] == "source"]
    return {
        "edge_deltas": {(e["p"], e["q"]): e["source_delta"] for e in edges},
        "transports": {(e["p"], e["q"]): e["T_pq"] for e in edges},
        "r2": {(r["p"], r["q"], r["r"]): r["F2_matrix"] for r in r2},
        "r3": {r["cycle_nodes"]: (r["holonomy_matrix"], r["F3_matrix"]) for r in r3},
        "current": [float(r["JR_value"]) for r in emitter.build_JR(w3)],
        "bianchi": [r["B_R_norm"] for r in br],
        "boundary": signed["C_signed"],
    }


def numeric_controls(emitter):
    template = emitter.build_nodes(2, 2, SEED)
    baseline_nodes, edited_nodes = deepcopy(template), deepcopy(template)
    for node, value in zip(baseline_nodes, (0, 1, 2, 3)):
        node["source_value"] = value
    for node, value in zip(edited_nodes, (0, 3, 2, 1)):
        node["source_value"] = value
    first = compare_geometry(emitter, baseline_nodes)
    second = compare_geometry(emitter, edited_nodes)
    matrix_control = compare_geometry(emitter, baseline_nodes, changed_transport=True)
    assert len(first["transports"]) == 8 and len(first["r2"]) == 8 and len(first["r3"]) == 2
    assert all(first[field] == second[field] for field in ("transports", "r2", "r3", "current", "bianchi"))
    assert first["edge_deltas"] != second["edge_deltas"]
    assert all(x == 0 for x in first["current"] + first["bianchi"])
    assert abs(first["boundary"] + 3 / 20) < 1e-14
    assert abs(second["boundary"] + 1 / 5) < 1e-14
    changed = sum(first["r3"][k][1] != matrix_control["r3"][k][1] for k in first["r3"])
    assert changed >= 1 and matrix_control["bianchi"] == first["bianchi"]
    return {
        "source_total_both":6, "boundary_rational_values":["-3/20","-1/5"],
        "identical_transport_matrices":len(first["transports"]),
        "identical_r2_matrices":len(first["r2"]),
        "identical_r3_loops":len(first["r3"]),
        "changed_f3_matrices_after_direct_transport_edit":changed,
        "bianchi_norms_all_three_runs":first["bianchi"],
    }


def by_case(table, key, expected_per_case, cases):
    groups = {c: [] for c in cases}
    for row in table:
        case, _ = row[key].rsplit("::", 1)
        groups[case].append(row)
    assert all(len(group) == expected_per_case for group in groups.values())
    return groups


def archive_replay(z, emitter, validator, scratch, evidence):
    cases = [f"{a}::{m}" for a in DOMAINS for m in MODES]
    merged = scratch / "original_merged"
    merged.mkdir()
    tables = {}
    for name in z.namelist():
        if name.startswith(MERGED) and name.endswith(".csv"):
            member = Path(name).name
            data = z.read(name)
            (merged/member).write_bytes(data)
            tables[Path(member).stem] = rows(data)
    manifest = tables["run_manifest"]
    assert Counter(f'{x["domain"]}::{x["mode"]}' for x in manifest) == Counter(cases)
    assert all(x["size_label"] == "3x4" and x["emitter_version"] == "V1698.76_direct_full_stack" for x in manifest)
    archived = json.loads(z.read("V1698_76_multi_ledger_validation.json"))
    reproduced = validator.validate(merged, validation_mode="multi")
    assert reproduced == archived
    assert archived["verdict"] == "FULL_STACK_LEDGER_VALIDATION_PASS_LAW_CANDIDATE"
    assert archived["gate_recompute"]["pass_rate"] == 1.0
    groups = {
        "nodes":by_case(tables["C0_nodes"],"node_id",2,cases),
        "edges":by_case(tables["C1_edges"],"edge_id",1,cases),
        "gamma":by_case(tables["Gamma_R_connection"],"edge_id",1,cases),
        "r2":by_case(tables["R2_path_faces"],"face_id",1,cases),
        "r3":by_case(tables["R3_cycle_faces"],"cycle_id",1,cases),
        "w3":by_case(tables["W3_cell_witnesses"],"cell_id",1,cases),
        "br":by_case(tables["W3_bianchi_residuals"],"cell_id",1,cases),
        "jr":by_case(tables["J_R_source_current"],"cell_id",1,cases),
    }
    failures = []
    for case in cases:
        named = {r["node_id"]: r for r in groups["nodes"][case]}
        a,b = f"{case}::n0", f"{case}::n1"
        assert set(named) == {a,b}
        assert [float(named[x]["source_value"]) for x in (a,b)] == [0,1]
        edge, = groups["edges"][case]
        assert (edge["p"],edge["q"]) == (a,b)
        assert json.loads(edge["T_pq"]) == IDENTITY and float(edge["source_delta"]) == 1
        gamma, = groups["gamma"][case]
        assert json.loads(gamma["transition_matrix"]) == IDENTITY
        face, = groups["r2"][case]
        cycle, = groups["r3"][case]
        assert json.loads(face["F2_matrix"]) == json.loads(cycle["F3_matrix"]) == ZERO
        assert json.loads(cycle["holonomy_matrix"]) == IDENTITY
        assert float(groups["w3"][case][0]["cell_source_current_JR"]) == 0
        assert float(groups["jr"][case][0]["JR_value"]) == 0
        assert float(groups["br"][case][0]["B_R_norm"]) == 0
        lookup = {edge["edge_id"]:(edge["p"],edge["q"])}
        face_nodes = [face["p"],face["q"],face["r"]]
        cycle_nodes = cycle["cycle_nodes"].split(";")
        assert face_nodes == cycle_nodes == [a,b,a]
        r2_legs = [lookup[face[key]] for key in ("edge_pq","edge_qr")]
        r3_legs = [lookup[key] for key in cycle["ordered_edge_ids"].split(";")]
        expected = list(zip(cycle_nodes,cycle_nodes[1:]))
        assert r2_legs == [(a,b),(a,b)] and r3_legs == [(a,b)]
        assert r2_legs != expected and r3_legs != expected and expected[1] not in lookup.values()
        failures.append({"case":case,"r2_direction_failure":True,"r3_missing_directed_leg":True})
    raw_seeds = []
    raw_vectors = []
    raw_values = {}
    for mode, expected_seed in zip(MODES[:2], (169876,169976)):
        prefix = f"case_ledgers/open_{mode}_baseline/"
        raw_manifest, = rows(z.read(prefix+"run_manifest.csv"))
        assert (raw_manifest["size_label"], raw_manifest["domain"], raw_manifest["mode"]) == ("3x4","open",mode)
        seed = int(raw_manifest["seed"])
        assert seed == expected_seed
        raw = sorted(rows(z.read(prefix+"C0_nodes.csv")),key=lambda x:int(x["ordered_index"]))
        incoming = [float(r["source_value"]) for r in raw]
        regenerated = [r["source_value"] for r in emitter.build_nodes(3, 4, seed)]
        assert len(incoming) == len(regenerated) == 12
        np.testing.assert_allclose(incoming,regenerated,rtol=0,atol=1e-14)
        raw_seeds.append(seed)
        raw_vectors.append(incoming)
        raw_values[mode] = raw
    assert Counter(raw_vectors[0]) != Counter(raw_vectors[1])
    case_items = {t:tables[t] for t in ("run_manifest","C0_nodes","C1_edges","R2_path_faces","R3_cycle_faces","J_R_source_current","gate_checks")}
    (evidence/"original_ledger_rows.json").write_text(json.dumps({"merged":case_items,"open_source_rows":raw_values},sort_keys=True,indent=2)+"\n")
    return {"merged_cases":len(cases),"merged_source_values_per_case":[0,1],"original_validator":reproduced,
            "directed_failures":failures,"raw_open_seeds":raw_seeds,"source_shuffle_is_permutation":False}


def main(repo, evidence):
    members = {}
    for version in FILES:
        member, expect = FILES[version]
        path = repo/DIRECTORY/member
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expect
        members[version] = path
    evidence.mkdir(parents=True,exist_ok=True)
    with ZipFile(members[75]) as pkg, ZipFile(members[77]) as freeze:
        mapping = {"v1698_75_emitter.py":pkg.read(EMITTER_MEMBER), "v1698_75_validator.py":pkg.read(VALIDATOR_MEMBER),
                   "v1698_77_postmortem.md":freeze.read(FREEZE_MEMBER)}
        for name, data in mapping.items():
            (evidence/name).write_bytes(data)
    # Avoid writing cache files into the evidence.
    sys.dont_write_bytecode = True
    emitter=load(evidence/"v1698_75_emitter.py","historical_emitter")
    validator=load(evidence/"v1698_75_validator.py","historical_validator")
    with TemporaryDirectory() as tmp, ZipFile(members[76]) as archive:
        scratch = Path(tmp)
        return {"labels_only":label_control(emitter,scratch),
                "numeric_source_and_transport":numeric_controls(emitter),
                "archive":archive_replay(archive,emitter,validator,scratch,evidence),
                "archive_hashes":{member:h for member,h in FILES.values()}}


if __name__ == "__main__":
    repo = Path(sys.argv[2]).resolve() if len(sys.argv)==3 else Path(__file__).resolve().parents[5]
    print(json.dumps(main(repo,Path(sys.argv[1]).resolve()),sort_keys=True,indent=2))
