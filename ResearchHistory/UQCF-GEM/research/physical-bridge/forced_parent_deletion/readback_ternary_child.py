"""Verify the archived v16.52 direct child calls and their source preparation."""
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

DEMOS = Path(__file__).resolve().parents[3] / "demos"
V52 = "v16.52-recursive-ternary-composition/"
PARENTS = (-1, 0, 1, 1, 1, 0, 0)
PREPARATION = (127, 33)

def read(path, blob):
    data = (DEMOS / path).read_bytes()
    assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == blob
    return data

def module(path, blob, name):
    read(path, blob)
    spec = importlib.util.spec_from_file_location(name, DEMOS / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def sites(mask):
    return tuple(v for v in range(7) if mask & (1 << v))

def run(machine, start, q):
    direct = {}
    def watch(frame, event, ret):
        if event != "return" or frame.f_code is not machine.normalize.__code__:
            return
        parent = frame.f_back
        if parent.f_code is not machine._normalize.__code__ or parent.f_locals["t"] != machine.A:
            return
        child = parent.f_locals["c"]
        local = frame.f_locals
        direct[child] = {"raw": local["state"][:], "k": local["k"], "q": local["q"][:], "returned_path": ret}
    old = sys.getprofile()
    try:
        sys.setprofile(watch)
        path = machine.normalize(list(start), machine.A, 2, list(q))
    finally:
        sys.setprofile(old)
    assert set(direct) == {1, 5, 6}
    return path, direct

def main():
    machine = module(V52+"producer.py", "90108c926299ca7cb66dca6acc4530bafcdb4a7e", "v52_child_producer")
    atom = module("v16.26-consistency-increment-law/engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b", "v26_child_source")
    verifier = module("v16.26-consistency-increment-law/verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3", "v26_verify_child_atom")
    compressed = read(V52+"evidence/science/scientific/CERTIFICATE.json.gz", "bafc28846f2e1704bafb9e6f8ead15caa6ac89f3")
    archived = json.loads(gzip.decompress(compressed))["cases"]
    specs = machine.specs()
    assert len(archived) == 7236 and [row["spec"] for row in archived] == specs
    result = {}
    for name, actor, num in (("delete_B_v5", 1, 6), ("delete_A_v5", 0, 36), ("no_deletion", None, None)):
        views = list(map(sites, PREPARATION))
        if actor is not None:
            record = atom.atomic(PARENTS, views, actor, 5)
            verifier.verify_atomic(record)
            views = record["after"]
        start = [sum(1 << v for v in view) for view in views]
        profile = [atom.tau_at(PARENTS, views, v) for v in (0, 1)]
        path, calls = run(machine, start, profile)
        expected = [1] if actor == 0 else [1, 1]
        assert calls[6] == {"raw": expected, "k": len(expected), "q": [], "returned_path": [expected]}
        assert calls[1]["raw"] == ([15] if actor == 0 else [15, 1])
        assert (len(calls[1]["returned_path"]) > 1) == (actor != 0)
        if num is not None:
            row = archived[num]
            spec = specs[num]
            assert spec == {"tree": "A", "q": profile, "k": 2, "permutation": "identity", "mode": "compact"}
            assert machine.initial(machine.A, 2, profile, "identity", "compact") == row["start"] == start
            assert row["failure"] is None and row["path"] == path
        result[name] = {"archive_row_zero_based": num, "initial": start, "q_computed_separately": profile,
                        "whole_path_moves": len(path)-1, "final": path[-1],
                        "untouched_subtree_v1": calls[1], "untouched_leaf_v6": calls[6]}
    assert result["delete_B_v5"]["whole_path_moves"] == 12 and result["delete_A_v5"]["whole_path_moves"] == 0
    print(json.dumps({"archive_sha256": hashlib.sha256(compressed).hexdigest(), "archive_rows": len(archived),
                      "runs": result, "historical_root_q": "supplied by campaign spec"}, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
