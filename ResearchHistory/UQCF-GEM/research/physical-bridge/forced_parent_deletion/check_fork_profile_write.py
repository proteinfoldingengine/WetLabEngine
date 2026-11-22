"""Use the original atomic checker, fork controller and archived certificate."""
import gzip
import hashlib
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys

SCI = Path("ResearchHistory/UQCF-GEM/demos")
FORK = SCI / "v16.45-binary-fork-unit-barrier"
ATOM = SCI / "v16.26-consistency-increment-law"
CERT = "evidence/science/scientific/CERTIFICATE.json.gz"
PINS = {
    FORK / "producer.py": "e73a02ee05e11f0c6b041b783ba6ff9738271073",
    FORK / "verifier.py": "26b4ab278c70ad9c958dbaccc676b2f18f2b30ad",
    FORK / "graph_producer.py": "6c8eca570cda82b64c0d06775672f33977be430a",
    FORK / "graph_verifier.py": "ff8af4ecf743507d0d601daffa9b054441b85fd1",
    FORK / "star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b",
    FORK / CERT: "3ed66277766b9836804ed9ec222d9728009b2b67",
    ATOM / "engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    ATOM / "verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
}
PARENTS = (-1, 0, 1, 1, 0, 4, 4)
PREP = (31, 15, 113)
MEET = (31, 17, 113)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def own(path, index):
    return [s[index] for i, s in enumerate(path) if not i or path[i-1][index] != s[index]]


def drop(mod, check, state, site):
    views = [tuple(v for v in range(7) if m & (1 << v)) for m in state]
    event = mod.atomic(PARENTS, views, 0, site)
    check.verify_atomic(event)
    return tuple(sum(1 << v for v in view) for view in event["after"]), event


class Replay:
    def __init__(self, entry, producer, verifier):
        self.graph = entry["graph"]
        self.k = entry["k"]
        self.rows = {r["state"]: r for r in entry["normalizations"]}
        self.index = {tuple(s): i for i, s in enumerate(self.graph["states"])}
        self.producer = producer
        self.verifier = verifier

    def profile(self, state):
        i = self.index[state]
        return self.graph["attained_profiles"][self.graph["profile_ids"][i]]

    def path(self, state):
        q = self.profile(state)
        masks = list(map(tuple, self.producer.normalize(state, 2, 2, self.k, q)))
        ids = [self.index[s] for s in masks]
        end = self.verifier.canonical(2, 2, self.k, q)
        assert self.verifier.path_valid(ids, self.index[state], self.index[end], self.graph, q)
        return masks, ids


def run(out):
    for path, expected in PINS.items():
        data = path.read_bytes()
        assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected, path
    with gzip.open(FORK / CERT, "rt") as handle:
        archive = json.load(handle)
    sys.path.insert(0, str(FORK.resolve()))
    producer = load("fork_producer", FORK / "producer.py")
    verifier = load("fork_verifier", FORK / "verifier.py")
    atom = load("atom", ATOM / "engine.py")
    av = load("atom_check", ATOM / "verify.py")
    domain = ((2, 2, 2), (2, 2, 3))
    replayed = producer.produce(domain)
    expected_entries = [e for e in archive["entries"] if (e["b"], e["c"], e["k"]) in domain]
    assert replayed["entries"] == expected_entries
    check = verifier.verify(replayed, domain)
    assert check["outcome"] == "BINARY_FORK_THEOREM_VALIDATED"
    two, three = [Replay(e, producer, verifier) for e in expected_entries]

    coalescing = []
    for site in (2, 3):
        state, _ = drop(atom, av, (127, 127), site)
        path, ids = two.path(state)
        assert path[1] == (115, 127) and path[0][1] == path[1][1] == 127
        coalescing.append(path[1:])
    assert coalescing[0] == coalescing[1]

    cases = {}
    for name, site, rep, root_cover, expected in (
        ("junction", 4, 6, 2, [15,11,3,1,17,49,113]),
        ("left_leaf", 2, 0, 1, [15,11,3,1,17,1]),
    ):
        state, event = drop(atom, av, PREP, site)
        q = three.profile(state)
        assert q == [root_cover, 1, 0, 0, 1, 0, 0]
        assert state[1:] == PREP[1:] and all((s & 96) == (t & 96) for s,t in zip(PREP,state))
        path, ids = three.path(state)
        at = path.index(MEET)
        assert path.count(MEET) == 1 and own(path[:at+1],1) == [15,11,3,1,17]
        assert own(path,1) == expected and three.index[state] not in three.rows
        row = three.rows[rep]
        assert row["q"] == q and row["path"][10] == three.index[MEET] == 1488
        assert ids[at:] == row["path"][10:]
        assert three.profile(MEET) == [1,1,0,0,1,0,0]
        cases[name] = {"site":site, "source_atom":event, "initial_graph_row":ids[0],
                       "target_profile":q,"representative":rep,"meet_offset":at,
                       "local_masks":expected,"path_ids":ids,"masks":path,
                       "archived_row":row, "matching_suffix":ids[at:]}
    left, right = (three.rows[i]["path"] for i in (0,6))
    assert left[6:11] == right[6:11] == [600,595,594,1463,1488]
    assert left[11] == 2657 and right[11] == 1518
    assert three.graph["states"][2657] == [63,17,113] and three.graph["states"][1518] == [31,49,113]
    # Fresh measurement at the common state assigns the same root cover in either arm.
    reset, _ = three.path(MEET)
    assert reset[-1] == (127,1,1)

    # Keep the physical roles fixed while varying the ordering used by the original code.
    orders = []
    for roles in permutations(range(3)):
        receiver = roles.index(1)
        source = roles.index(0)
        ends = []
        for name in ("junction","left_leaf"):
            start = cases[name]["masks"][0]
            path, _ = three.path(tuple(start[j] for j in roles))
            ends.append(path[-1])
        changed = [i for i in range(3) if (ends[0][i] ^ ends[1][i]) & 32]
        assert changed == [0,1] and set(changed)-{source}
        orders.append({"roles":roles,"B_rank":receiver,"B_bit5":[(e[receiver]>>5)&1 for e in ends]})
    assert sum(x["B_bit5"][0]!=x["B_bit5"][1] for x in orders) == 4
    no_event, _ = three.path(PREP)
    assert own(no_event,1) == cases["left_leaf"]["local_masks"]
    evidence = {"cases":cases,"dot_common_suffix":coalescing[0],"order_controls":orders,
                "historical_graph_rows":[three.rows[i] for i in (0,6)],"reset_path":reset}
    raw = (json.dumps(evidence,indent=2,sort_keys=True)+"\n").encode()
    out.mkdir(parents=True,exist_ok=True)
    (out/"fork_certificate.json").write_bytes(raw)
    return {"domain":domain, "original_verifier":check["outcome"], "reproduced_complete_graph_sizes":[121,6241],
            "common_masks":MEET, "historical_shared_states":left[6:11], "receiver":1,
            "local_histories":{name:c["local_masks"] for name,c in cases.items()},
            "stored_root_covers":{name:c["target_profile"][0] for name,c in cases.items()},
            "source_rows":{name:c["initial_graph_row"] for name,c in cases.items()},
            "archived_sources_of_suffixes":[0,6],"reset_endpoint":reset[-1],
            "fixed_receiver_contrasts_per_six_orders":4, "certificate_sha256":hashlib.sha256(raw).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])),sort_keys=True,indent=2))
