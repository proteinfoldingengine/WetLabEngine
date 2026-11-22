"""Replay pinned v16.52/v16.53 attached contraction; print canonical compact JSON.

Run from any directory: python check_attached_contraction.py [--output FILE].
The matching palette orders are explicit controls, not inferred event inputs.
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[3] / "demos"
COMMIT = "e7e01bab68ba5171dacd91333f98d208d810dac3"
SOURCES = {
    "producer52": ("v16.52-recursive-ternary-composition/producer.py", "90108c926299ca7cb66dca6acc4530bafcdb4a7e"),
    "verifier52": ("v16.52-recursive-ternary-composition/verifier.py", "93fb1a7f40e304fc8fd05767a086b912cf4288a6"),
    "coverage52": ("v16.52-recursive-ternary-composition/coverage.py", "973244d0eb8a48bcb2464870377139cf4e9870c6"),
    "producer53": ("v16.53-four-child-boundary/producer.py", "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80"),
    "feasibility53": ("v16.53-four-child-boundary/feasibility.py", "9e995e21c9a477034a2fd4be615e28a2551b0bf9"),
}
TREE = (((), ()), ())
NAMES = ("o", "p", "l", "w", "d")
LABELS = "ABC"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_sources():
    for relative, expected in SOURCES.values():
        data = (BASE / relative).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(actual == expected, f"Historical Git blob mismatch: {relative}: {actual}")


def load(key, dependencies=None):
    spec = importlib.util.spec_from_file_location("attached_" + key, BASE / SOURCES[key][0])
    module = importlib.util.module_from_spec(spec)
    dependencies = dependencies or {}
    previous = {name: sys.modules.get(name) for name in dependencies}
    try:
        sys.modules.update(dependencies)
        spec.loader.exec_module(module)
    finally:
        for name, old in previous.items():
            if old is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old
    return module


def columns(supports):
    return [sum(1 << v for v, row in enumerate(supports) if j in row) for j in range(3)]


def edits(path):
    out = []
    for left, right in itertools.pairwise(path):
        changed = [(j, v) for j in range(3) for v in range(5) if (left[j] ^ right[j]) & (1 << v)]
        require(len(changed) == 1, "Nonprimitive move")
        j, v = changed[0]
        out.append(("+" if right[j] & (1 << v) else "-") + LABELS[j] + "(" + NAMES[v] + ")")
    return out


def run():
    check_sources()  # Verify every source and dependency before importing any of them.
    verifier = load("verifier52", {"coverage": load("coverage52")})
    producers = {"v16.52": load("producer52"),
                 "v16.53": load("producer53", {"feasibility": load("feasibility53")})}
    records, standalone = [], []
    for source in "AB":
        before = columns([range(3), range(3), [1] if source == "A" else [0], [2], [0]])
        matching = [1, 2, 0] if source == "A" else [0, 2, 1]
        for kind, order in [("default", [0, 1, 2]), ("matching_control", matching)]:
            paths = []
            for version, producer in producers.items():
                trace = []
                path = producer.normalize(before, TREE, 3, [1, 2], order=order, trace=trace)
                # Independent expected endpoint; it is never passed to normalize().
                endpoint = columns([range(3), order[:2], order[:1], order[1:2], order[:1]])
                require(verifier.path_check(TREE, 3, [1, 2], path, before, endpoint) == [0, 0, 0], "Excursion")
                require(all(verifier.profile_check(TREE, 3, row) == [1, 2] for row in path), "Profile changed")
                moves = edits(path)
                first = ["+B(d)", "+C(d)"] if order != [0, 2, 1] else ["+C(d)", "+B(d)"]
                require(moves[:2] == first, "Expected outer-root expansion first")
                parent_deletions = [move for move in moves if move.startswith("-") and move.endswith("(p)")]
                expected = "-C(p)" if kind == "default" else f"-{source}(p)"
                require(parent_deletions == [expected], "Wrong attached contraction")
                require(len(moves) == ((9 if source == "A" else 7) if kind == "default" else 5), "Move count")
                if kind == "matching_control":
                    require(moves[2] == expected, "Matching contraction was not the third move")
                records.append({"version": version, "source": source, "order_kind": kind,
                                "order": "".join(LABELS[j] for j in order), "path_columns": path,
                                "edits": moves, "constant_profile": [1, 2],
                                "parent_deletions": parent_deletions,
                                "deletion_only": False, "fixed_anchor_d": False})
                paths.append(path)
            require(paths[0] == paths[1], "Versions disagree on fixture path")
        for version, producer in producers.items():
            raw = columns([range(3), [1] if source == "A" else [0], [2]])
            path = producer.normalize(raw, ((), ()), 3, [2], order=matching)
            require(path == [raw], "Standalone fixed root unexpectedly contracted")
            verifier.path_check(((), ()), 3, [2], path, raw, raw)
            standalone.append({"version": version, "source": source,
                               "order": "".join(LABELS[j] for j in matching), "path_columns": path})
    require(len(records) == 8 and len(standalone) == 4, "Incomplete control set")
    return {"schema": 1, "status": "PASS", "source_commit": COMMIT,
            "sources": {key: {"path": path, "git_blob": sha} for key, (path, sha) in SOURCES.items()},
            "vertex_order": NAMES, "label_order": LABELS,
            "checked_whole_tree_paths": 8, "checked_standalone_controls": 4,
            "paths": records, "standalone_controls": standalone,
            "conclusion": "Attached contraction is an actual caller operation, but default order removes C in both source branches. Matching orders are supplied controls and expand d before the desired deletion. Root hitting number stays 1.",
            "scope": "Direct historical-function replay; no full campaign, publication, certification, or physical event-selection claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Also write the canonical JSON result to this file")
    args = parser.parse_args()
    text = json.dumps(run(), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
