"""Compare two original source deletions, fresh fork normalization and archived continuations."""
from functools import cache
from itertools import product
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json
import sys

U = Path("ResearchHistory/UQCF-GEM")
FORK = U / "demos/v16.45-binary-fork-unit-barrier"
ATOM = U / "demos/v16.26-consistency-increment-law"
PARENTS = (-1, 0, 1, 1, 0, 4, 4)
KEYS = ((), (0,), (0, 0), (0, 1), (1,), (1, 0), (1, 1))
LEAVES = (2, 3, 5, 6)


def read_blob(path, expected):
    data = path.read_bytes()
    assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected
    return data


def load_module(name, path, expected):
    read_blob(path, expected)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(out):
    atom = load_module("source_atom", ATOM/"engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = load_module("source_verify", ATOM/"verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    lineage = load_module("lineage", U/"foundational-closure-verification/lineage.py", "e95e3e978779164dd91f09b80e3389247e6320c2")
    sys.path.insert(0, str(FORK.resolve()))
    writer = load_module("original_writer", FORK/"producer.py", "e73a02ee05e11f0c6b041b783ba6ff9738271073")
    archive = read_blob(FORK/"evidence/science/scientific/CERTIFICATE.json.gz", "3ed66277766b9836804ed9ec222d9728009b2b67")
    entry = next(e for e in json.loads(gzip.decompress(archive))["entries"] if (e["b"], e["c"], e["k"]) == (2,2,2))
    graph = entry["graph"]
    states = list(map(tuple, graph["states"]))
    ids = {s: i for i, s in enumerate(states)}
    records = entry["normalizations"]
    tree = lineage.Carrier("fork", KEYS)

    @cache
    def balance(mask):
        view = lineage.Carrier("fork", tuple(v for i, v in enumerate(KEYS) if mask >> i & 1))
        grade = lineage.Pruning(tree, view).aggregate(tuple(int(i in LEAVES) for i in range(7)))
        return int(grade[view.keys.index(KEYS[4])] - grade[view.keys.index(KEYS[1])])

    def views(s):
        return [tuple(v for v in range(7) if mask >> v & 1) for mask in s]

    def profile(s):
        q = graph["attained_profiles"][graph["profile_ids"][ids[s]]]
        assert q == [atom.tau_at(PARENTS, views(s), v) for v in range(7)]
        return q

    def atomic(s, owner, vertex):
        cert = atom.atomic(PARENTS, views(s), owner, vertex)
        verifier.verify_atomic(cert)
        result = tuple(sum(1 << v for v in view) for view in cert["after"])
        assert result in ids and graph["forward_moves"][ids[result]] >> (6*owner + vertex-1) & 1
        return result, cert

    def deletions(s):
        edits = []
        for owner, mask in enumerate(s):
            for v in range(1,7):
                t = list(s)
                t[owner] &= ~(1 << v)
                if tuple(t) in ids and tuple(t) != s:
                    result, cert = atomic(s, owner, v)
                    edits.append((owner, v, result, cert))
        return edits

    def path_check(path):
        for before, after in zip(path, path[1:]):
            changes = [(i, a^b) for i, (a,b) in enumerate(zip(before,after)) if a != b]
            (owner, bit), = changes
            assert bit.bit_count() == 1
            smaller = before if before[owner] < after[owner] else after
            assert graph["forward_moves"][ids[smaller]] >> (6*owner + bit.bit_length()-2) & 1

    # Relabel both pairs of siblings, swap the two root branches and swap owner ranks.
    cases = []
    membership_paths = set()
    for swap, left, right, receiver in product((False,True), (2,3), (5,6), (0,1)):
        source = 1 - receiver
        prep = [127,127]
        prep[receiver] = 19 | (1 << left) | (1 << right)
        prep = tuple(prep)
        assert balance(prep[receiver]) == 0
        for anatomical, event, opposite in (("left",left,right),("right",right,left)):
            after, event_cert = atomic(prep, source, event)
            assert event_cert["trigger"] and event_cert["delta_h"] == 1
            candidates = deletions(after)
            assert len(candidates) == 2
            neutral, = [(i,v,t) for i,v,t,c in candidates if not c["trigger"]]
            assert neutral[:2] == (receiver, opposite)
            assert all(c["delta_h"] == 0 and c["h_before"] == c["h_after"] == 2 for *_,c in candidates)
            assert profile(after) == profile(neutral[2])
            silent, = [t for i,v,t,c in candidates if c["trigger"] and i == source and v == opposite]
            assert silent[receiver] == prep[receiver] and not deletions(silent)
            q = profile(after)
            path = [tuple(s) for s in writer.normalize(after,2,2,2,q)]
            path_check(path)
            step = next(i for i,s in enumerate(path) if s[receiver] != prep[receiver])
            pixel = path[step][receiver]
            orientation = -1 if swap else 1
            sign = orientation * (1 if anatomical == "left" else -1)
            assert orientation*balance(pixel) == orientation*balance(neutral[2][receiver]) == sign
            assert after not in {states[row["state"]] for row in records}
            raw = []
            for row in records:
                for i,j in enumerate(row["path"]):
                    if j != ids[after]:
                        continue
                    seq = [states[t] for t in row["path"][i:]]
                    path_check(seq)
                    observed = next((s[receiver] for s in seq if s[receiver] != prep[receiver]), None)
                    raw.append({"seed":row["state"],"position":i,"first_C":observed,
                                "balance":None if observed is None else orientation*balance(observed),
                                "entered_by_source": i>0 and states[row["path"][i-1]]==prep})
            assert not any(r["entered_by_source"] for r in raw)
            if not swap and left == 2 and right == 5 and receiver == 0:
                assert raw and all(r["balance"] == -sign for r in raw)
                assert step == 1 and path[1] == neutral[2]
                assert balance(path[-1][receiver]) == -sign
            membership_paths.add((left,right,receiver,event))
            cases.append({"swap_branch_names":swap,"marked":[left,right],"C_index":receiver,
                          "source_side":("right" if anatomical=="left" else "left") if swap else anatomical,
                          "source_site":event,"post_state":after,"profile":q,"neutral_C_drop":opposite,
                          "unrestricted_silent_terminal":silent,"after_neutral_deletion":neutral[2],
                          "first_writer_C_step":step,"first_writer_C_mask":pixel,"first_writer_balance":sign,
                          "stored_visits":raw})
    samples = [c for c in cases if not c["swap_branch_names"] and c["marked"]==[2,5] and c["C_index"]==0]
    assert samples[0]["unrestricted_silent_terminal"] == samples[1]["unrestricted_silent_terminal"] == (55,91)
    result = {"cases":cases,"matched_preparations_in_fixed_numbering":8,"distinct_fresh_paths_checked":len(membership_paths)}
    out.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(result, sort_keys=True, indent=2)+"\n").encode()
    (out/"first_write_certificate.json").write_bytes(data)
    return {"source_cases_with_orientation":len(cases),"distinct_inputs":len(membership_paths),
            "first_C_step_range":[min(c["first_writer_C_step"] for c in cases),max(c["first_writer_C_step"] for c in cases)],
            "certificate_sha256":hashlib.sha256(data).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), sort_keys=True, indent=2))
