"""Test whether the original recoloring actually uses the acquired receiver bit."""
from fractions import Fraction
from hashlib import sha256
from inspect import getsourcelines
from itertools import permutations
import json
from pathlib import Path
import sys
from types import CodeType

import check_donor_read as historical


U = Path("ResearchHistory/UQCF-GEM")
STAR = historical.STAR
ATOM = historical.ATOM
GRADES = [(1, 1, 1, 1), (5, Fraction(1, 3), Fraction(3, 2), 2)]
ROW_IDS = {(1, 7, 13): 7, (1, 13, 7): 16, (7, 1, 13): 101,
           (7, 13, 1): 131, (13, 1, 7): 232, (13, 7, 1): 247}


def source_line(code, predicate):
    lines, start = getsourcelines(code)
    line, = (start + i for i, source in enumerate(lines) if predicate(source.strip()))
    return line


def replay(normalize, seed, receiver, source, *, suppress=False, bit_at_boundary=None):
    """Trace actual commands and optionally exchange only one live receiver bit."""
    code = normalize.__code__
    nested = {item.co_name: item for item in code.co_consts if isinstance(item, CodeType)}
    change = nested["change"]
    snapshot_line = source_line(change, lambda line: line == "path.append(list(s))")
    boundary_line = source_line(code, lambda line: line.startswith("def colors():"))
    prefix_end = None
    boundary = {}
    commands = []
    colors = []
    restored = False

    def trace(frame, event, _arg):
        nonlocal prefix_end, restored
        if frame.f_code is change:
            live = frame.f_locals
            if event == "call" and prefix_end is not None:
                commands.append((live["j"], live["v"], live["add"]))
            if suppress and event == "line" and frame.f_lineno == snapshot_line and len(live["path"]) == 1:
                assert not restored and (live["j"], live["v"], live["add"]) == (source, 2, False)
                assert live["s"][source] & 4 == 0
                live["s"][source] |= 4
                restored = True
        if frame.f_code is code and event == "line" and frame.f_lineno == boundary_line:
            assert prefix_end is None
            live = frame.f_locals
            prefix_end = len(live["path"])
            boundary["prior"] = list(live["s"])
            assert live["path"][-1] == boundary["prior"]
            if bit_at_boundary is not None:
                assert bool(live["s"][receiver] & 4) != bit_at_boundary
                live["s"][receiver] ^= 4
            boundary["effective"] = list(live["s"])
        if frame.f_code is nested["colors"] and event == "return":
            colors.append(list(_arg))
        return trace

    old = sys.gettrace()
    try:
        sys.settrace(trace)
        path = normalize(seed, 3, 3, 2)
    finally:
        sys.settrace(old)
    assert prefix_end is not None and restored == suppress and colors and commands
    suffix = [boundary["effective"], *path[prefix_end:]]
    assert len(suffix) == len(commands) + 1
    return {"prefix": path[:prefix_end], "boundary": boundary,
            "continuation": {"states": suffix, "commands": commands, "colors": colors}}


def grades(lin, mask, values):
    keys = ((), (1,), (2,), (3,))
    retained = tuple(key for i, key in enumerate(keys) if mask >> i & 1)
    fine = lin.Carrier("historical-receiver-recoloring", keys)
    coarse = lin.Carrier(fine.genesis, retained)
    projection = dict(zip(retained, lin.Pruning(fine, coarse).aggregate(values), strict=True))
    return [projection.get(k, 0) for k in keys]


def exact_path(checker, graph, lookup, path):
    ids = [lookup[tuple(state)] for i, state in enumerate(path) if i == 0 or path[i - 1] != state]
    assert checker.path_valid(ids, ids[0], lookup[checker.canonical(3, 3, 2)], graph, 2, 0)
    historical.check_edges(path, graph, lookup, 4)


def first_effective(replay_result):
    commands = replay_result["commands"]
    states = replay_result["states"]
    return next(command for command, before, after in zip(commands, states[:-1], states[1:], strict=True)
                if before != after)


def main(output):
    historical.blob(Path(__file__).with_name("check_donor_read.py"), "130151a17ee347734e8251a47cb0f439b0dbdd82")
    historical.blob(STAR / "graph_producer.py", "6c8eca570cda82b64c0d06775672f33977be430a")
    historical.blob(STAR / "graph_verifier.py", "ff8af4ecf743507d0d601daffa9b054441b85fd1")
    sys.path.insert(0, str(STAR.resolve()))
    normalizer = historical.module("old_star", STAR/"producer.py", "ffd513619d182abea2b31bd90c38e12784557bf3").normalize
    checker = historical.module("old_check", STAR/"verifier.py", "80a47f10231a086af161c4999c582fa038d064c7")
    atom = historical.module("old_atom", ATOM/"engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = historical.module("old_verify", ATOM/"verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    lineage = historical.module("old_lineage", U/"foundational-closure-verification/lineage.py",
                                "e95e3e978779164dd91f09b80e3389247e6320c2")
    archive = historical.archive(STAR, "b226fdef7d908f1f0186060ebf408eb0db823418")
    entry, = [entry for entry in archive if (entry["m"], entry["k"]) == (3, 3)]
    graph = entry["graph"]
    states = graph["states"]
    lookup = {tuple(state): i for i, state in enumerate(states)}
    rows = {row["state"]: row for row in entry["normalizations"]}
    cases = {}
    parents = (-1, 0, 0, 0)
    active_ids, color_changes = [], []
    for seed in permutations((1, 7, 13)):
        receiver = seed.index(1)
        ref, actor = [i for i in range(3) if i != receiver]
        idx = lookup[seed]
        assert idx == ROW_IDS[seed] and rows[idx]["q"] == 2
        actual = replay(normalizer, seed, receiver, actor)
        restored = replay(normalizer, seed, receiver, actor, suppress=True)
        row = {"order_masks":seed, "receiver":receiver, "source":actor, "reference":ref,
               "original":actual, "restored":restored}
        event = historical.certify(atom, verifier, parents, actual["prefix"][0], actual["prefix"][1], actor, 2)
        row["source_atom"] = event
        for branch in (actual, restored):
            path = branch["prefix"] + branch["continuation"]["states"][1:]
            if branch is actual:
                assert path == [states[i] for i in rows[idx]["path"]]
            exact_path(checker, graph, lookup, path)
            state = branch["boundary"]["effective"]
            colors = [min(i for i, mask in enumerate(state) if mask >> v & 1) for v in (1, 2, 3)]
            assert colors == branch["continuation"]["colors"][0]
        x, y = actual["boundary"]["prior"], restored["boundary"]["prior"]
        differing_view, = [i for i in range(3) if x[i] != y[i]]
        assert (x[differing_view] ^ y[differing_view]) == 4
        if receiver != 2:
            active_ids.append(idx)
            assert differing_view == receiver and x[actor] == y[actor] == 1 and x[ref] == y[ref] == seed[ref]
            assert x[receiver] == (seed[actor] & ~4) and y[receiver] == seed[actor]
            grade_checks = []
            for g in GRADES:
                low, high = (grades(lineage, mask, g) for mask in (x[receiver], y[receiver]))
                assert [b - a for a, b in zip(low, high, strict=True)] == [-g[2], 0, g[2], 0]
                grade_checks.append([list(map(str, data)) for data in (low, high)])
            row["receiver_grades_original_then_restored"] = grade_checks
            changed_color = actual["continuation"]["colors"][0] != restored["continuation"]["colors"][0]
            assert changed_color == (receiver < ref)
            if changed_color:
                color_changes.append(idx)
            for suppress, bit, origin, match in ((False, True, actual, restored), (True, False, restored, actual)):
                hybrid = replay(normalizer, seed, receiver, actor, suppress=suppress, bit_at_boundary=bit)
                assert hybrid["prefix"] == origin["prefix"] and hybrid["boundary"]["prior"] == origin["boundary"]["prior"]
                assert hybrid["boundary"]["effective"] == match["boundary"]["effective"]
                assert hybrid["continuation"] == match["continuation"]
                exact_path(checker, graph, lookup, hybrid["continuation"]["states"])
                row["restored_with_original_bit" if suppress else "original_with_restored_bit"] = hybrid
        else:
            assert differing_view == actor and all(s[receiver] == 1 for b in (actual, restored)
                                                   for s in b["continuation"]["states"])
        if idx == 7:
            a, b = (run["continuation"] for run in (actual, restored))
            assert a["colors"][0] == [1, 1, 0] and b["colors"][0] == [1, 0, 0]
            assert first_effective(a) == (0, 1, True)
            assert b["commands"][:2] == [(1, 2, True), (0, 2, False)]
            assert b["states"][0] == b["states"][1] == [13, 7, 1] and b["states"][2] == [9, 7, 1]
            row["receiver_pruning_atom"] = historical.certify(atom, verifier, parents, b["states"][1], b["states"][2], 0, 2)
            # Holding B's original bit cannot reproduce the alternate commands, even though both endpoints agree.
            assert a["states"][-1] == b["states"][-1] and a["commands"] != b["commands"]
            assert row["receiver_grades_original_then_restored"][0] == [["3", "0", "0", "1"], ["2", "0", "1", "1"]]
        if idx == 101:
            a, b = (run["continuation"] for run in (actual, restored))
            assert a["colors"][0] == b["colors"][0] == [0, 0, 1]
            assert a["commands"] == b["commands"]
            assert first_effective(a) == (1, 2, True) and first_effective(b) == (0, 2, False)
        cases[str(idx)] = row
    assert sorted(active_ids) == [7, 16, 101, 232] and sorted(color_changes) == [7, 16]
    certificate = {"grades": [list(map(str, g)) for g in GRADES], "cases": cases}
    raw = (json.dumps(certificate, indent=2, sort_keys=True) + "\n").encode()
    output.mkdir(parents=True, exist_ok=True)
    (output/"receiver_recoloring_certificate.json").write_bytes(raw)
    return {"active_rows":sorted(active_ids), "first_color_changes":sorted(color_changes),
            "silent_rows":[131,247], "complete_paths_checked":12, "substituted_suffixes_checked":8,
            "certificate_sha256":sha256(raw).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1])), indent=2, sort_keys=True))
