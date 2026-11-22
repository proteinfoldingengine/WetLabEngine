"""Read the original V1700.2 audit after a metadata-only intervention."""
from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile

import numpy as np


ARCHIVE_PATH = Path(
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/History/"
    "V1700_2_nontautological_momentum_test_package.zip"
)
ARCHIVE_BLOB = "49742bac537ba7f7cbe61532c4bb959daed25d3a"
COMMIT = "a553b24f7699d57051c155644dc10dba9aa546e8"
MEMBER = "V1700_2_nontautological_momentum_test.py"


def load_pinned_functions(path):
    archive = path.read_bytes()
    header = f"blob {len(archive)}\0".encode()
    assert hashlib.sha1(header + archive).hexdigest() == ARCHIVE_BLOB
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        member = z.read(MEMBER)
    source = ast.parse(member)
    constants = {"EPS", "SIZES", "CANDS"}
    body = [
        node for node in source.body
        if isinstance(node, ast.FunctionDef)
        or (isinstance(node, ast.Assign)
            and any(isinstance(name, ast.Name) and name.id in constants for name in node.targets))
    ]
    body = [ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0), *body]
    env = {"np": np, "hashlib": hashlib, "math": math}
    nodes = ast.fix_missing_locations(ast.Module(body=body, type_ignores=[]))
    exec(compile(nodes, MEMBER, "exec"), env)
    return env, hashlib.sha256(member).hexdigest()


def swap_event_ids(rows):
    rows[0]["event"], rows[1]["event"] = rows[1]["event"], rows[0]["event"]


def replace_prior_pointer(rows):
    rows[1]["prior"] = rows[1]["event"]


def with_chart_edit(env, size, edit):
    original_charts = env["charts"]
    captured = {}

    def edited_charts(n):
        root, rows = original_charts(n)
        edit(rows)
        captured.update(root=root, rows=rows)
        return root, rows

    env["charts"] = edited_charts
    try:
        result = env["eval_case"](size, "valid")
    finally:
        env["charts"] = original_charts
    return result, captured


def return_bytes(value):
    return json.dumps(value, sort_keys=True, allow_nan=False).encode()


def check(path):
    env, member_sha256 = load_pinned_functions(path)
    evaluate = env["eval_case"]
    records = []
    assert env["SIZES"] == [9, 13, 17, 25, 33, 49, 65, 97]
    for size in env["SIZES"]:
        initial_row, initial_cells = evaluate(size, "valid")
        root, original_rows = env["charts"](size)
        cell_inputs = env["cells"](size, root)
        assert original_rows[1]["prior"] == original_rows[0]["event"]
        assert len(initial_cells) == size
        assert initial_row["full_stack_gate"]
        initial = return_bytes((initial_row, initial_cells))
        interventions = {}
        for name, edit, expected in (
            ("swap_first_two_event_ids", swap_event_ids, [[0, "event"], [1, "event"]]),
            ("replace_second_prior_pointer", replace_prior_pointer, [[1, "prior"]]),
        ):
            (final_row, final_cells), captured = with_chart_edit(env, size, edit)
            assert captured["root"] == root
            changed_rows = captured["rows"]
            assert len(changed_rows) == len(original_rows)
            assert all(before.keys() == after.keys() for before, after in zip(original_rows, changed_rows))
            differences = [
                [i, key] for i, (before, after) in enumerate(zip(original_rows, changed_rows))
                for key in before if before[key] != after[key]
            ]
            assert differences == expected
            assert changed_rows[1]["prior"] != changed_rows[0]["event"]
            assert return_bytes((final_row, final_cells)) == initial
            assert env["integrity"](changed_rows, original_rows, root, cell_inputs, cell_inputs) == (0, 0, 0)
            interventions[name] = {
                "modified_fields": differences,
                "chain_link_broken": True,
                "full_return_exact_equal": True,
                "gate": final_row["full_stack_gate"],
                "integrity_mismatches_against_unedited_reference": [0, 0, 0],
            }

        # An original non-metadata-only control verifies that input use can be detected.
        order_row, order_cells = evaluate(size, "order_shuffle")
        assert order_row["chart_mismatches"] > 0 and not order_row["full_stack_gate"]
        assert [cell["cell"] for cell in initial_cells] == [cell["cell"] for cell in order_cells]
        changed_q_count = sum(old["q"] != new["q"] for old, new in zip(initial_cells, order_cells))
        assert changed_q_count > 0
        records.append({
            "n": size,
            "returned_cell_rows_compared": size,
            "unmodified_gate": initial_row["full_stack_gate"],
            "metadata_interventions": interventions,
            "order_shuffle_chart_mismatches": order_row["chart_mismatches"],
            "order_shuffle_gate": False,
            "order_shuffle_changed_q_count": changed_q_count,
        })
    return {
        "archive_repository_commit": COMMIT,
        "archive_repository_path": str(ARCHIVE_PATH),
        "archive_git_blob": ARCHIVE_BLOB,
        "python_member": MEMBER,
        "python_member_sha256": member_sha256,
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=ARCHIVE_PATH)
    args = parser.parse_args()
    print(json.dumps(check(args.archive), indent=2, sort_keys=True))
