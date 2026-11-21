"""Replay the two source branches using the original view-deletion engine and its verifier."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parents[3] / "demos/v16.26-consistency-increment-law"
PARENTS = (-1, 0, 1, 1, 0)
NAMES = ("o", "p", "l", "w", "d")
VIEWS = [[0, 1, 2], [0, 1, 2], [0, 1, 3, 4]]


def load_archived(name, blob):
    path = DIRECTORY / (name + ".py")
    data = path.read_bytes()
    assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == blob
    spec = importlib.util.spec_from_file_location("archive_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def leaf_hull(views):
    global_leaves = set(range(len(PARENTS))) - set(PARENTS[1:])
    result = []
    for view in views:
        hull = {0}
        for vertex in set(view) & global_leaves:
            while vertex not in hull:
                hull.add(vertex)
                vertex = PARENTS[vertex]
        result.append(sorted(hull))
    return result


def permitted(engine, verifier, views):
    legal = {}
    for i, label in enumerate("ABC"):
        for vertex, name in enumerate(NAMES[1:], 1):
            try:
                cert = engine.atomic(PARENTS, views, i, vertex)
            except ValueError:
                continue
            verifier.verify_atomic(cert)
            legal[label, name] = cert
    return legal


def main():
    engine = load_archived("engine", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = load_archived("verify", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    assert leaf_hull(VIEWS) == VIEWS
    first = permitted(engine, verifier, VIEWS)
    assert set(first) == {("A", "l"), ("B", "l")}
    output = {}
    for (label, _), cert in sorted(first.items()):
        after_source = cert["after"]
        assert after_source != leaf_hull(after_source)
        second = permitted(engine, verifier, after_source)
        assert set(second) == {(label, "p")}
        endpoint = second[label, "p"]["after"]
        assert endpoint == leaf_hull(after_source)
        assert not permitted(engine, verifier, endpoint)
        non_atomic = copy.deepcopy(cert)
        non_atomic["after"] = endpoint
        try:
            verifier.verify_atomic(non_atomic)
        except ValueError as exc:
            assert str(exc) == "not atomic"
        else:
            raise AssertionError("Bundled source and parent edits accepted as one atom")
        stopped = engine.factor(PARENTS, VIEWS, after_source)
        completed = engine.factor(PARENTS, VIEWS, endpoint)
        assert verifier.verify_factor(stopped) and verifier.verify_factor(completed)
        assert [s["after"] for s in stopped["steps"]] == [after_source]
        assert [s["after"] for s in completed["steps"]] == [after_source, endpoint]
        output[label] = {
            "first_successful_sites": [[l, v] for l, v in sorted(first)],
            "next_successful_sites": [[l, v] for l, v in sorted(second)],
            "view_of_removed_label_after_source": after_source["ABC".index(label)],
            "view_of_removed_label_after_second": endpoint["ABC".index(label)],
            "supplied_endpoint_factor_lengths": [len(stopped["steps"]), len(completed["steps"])],
            "bundled_edit_rejection": "not atomic",
            "nonroot_requests_tried_per_state": 12,
        }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
