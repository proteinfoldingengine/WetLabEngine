"""Validate the pinned first binary leaf edit workflow archives against the checked-in experiment."""
from contextlib import ExitStack
from functools import cache
from itertools import combinations
from hashlib import sha256
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile

here = Path(__file__).resolve().parent
meta = json.loads((here / "MANIFEST.json").read_bytes())
science = Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent.parent / "junction_reachability"


def digest(data):
    return sha256(data).hexdigest()


def shortest_interval(start, finish, exact):
    """Count ways backward on every Hamming substate with an independent admission rule."""
    parents = (-1,0,0,0,3,3,3,0,7,7)
    branches = ((1,2,3,7),(4,5,6),(8,9))
    required = (2,3,2)
    @cache
    def count(state):
        columns = [{j for j,m in enumerate(state) if m >> v & 1} for v in range(10)]
        if columns[0] != {0,1,2} or any(not columns[v] or not columns[v] <= columns[parents[v]] for v in range(1,10)):
            return 0
        covers = []
        for leaves in branches:
            cover = next(k for k in (1,2,3) if any(all(set(team) & columns[v] for v in leaves)
                                                    for team in combinations((0,1,2), k)))
            covers.append(cover)
        if sum(abs(a-b) for a,b in zip(covers,required)) > (0 if exact else 1):
            return 0
        if state == start:
            return 1
        total = 0
        for j,(current,original) in enumerate(zip(state,start)):
            for v in range(1,10):
                if ((current^original) >> v) & 1:
                    neighbor=list(state)
                    neighbor[j] ^= 1 << v
                    total += count(tuple(neighbor))
        return total
    return count(finish)


with ExitStack() as stack:
    archives = {}
    for name, row in meta["archives"].items():
        path = here / (name + ".zip")
        assert path.stat().st_size == row["bytes"] and digest(path.read_bytes()) == row["sha256"]
        z = archives[name] = stack.enter_context(ZipFile(path))
        assert z.testzip() is None
        if "SHA256SUMS" in z.namelist():
            for line in z.read("SHA256SUMS").decode().splitlines():
                expected, member = line.split(None, 1)
                assert digest(z.read(member.strip())) == expected
    review = archives["junction-reachability-review"]
    published = archives["junction-reachability-publication"]
    foundation = archives["junction-reachability-foundation"]
    for key in ("receipt.json", "review.txt", "response.json", "raw.json", "result.json"):
        assert review.read(key) == published.read(key)
    assert review.read("raw.json") == lzma.decompress((science / "raw.json.xz").read_bytes())
    assert review.read("result.json") == (science / "result.json").read_bytes()
    summary = json.loads(review.read("result.json"))
    assert digest(review.read("raw.json")) == meta["raw_sha256"] == summary["raw_sha256"]
    raw = json.loads(review.read("raw.json"))
    after, final = tuple(summary["after"]), tuple(summary["final"])
    start, chamber = tuple(summary["start"]), tuple(summary["chamber"])
    for mode, expected in (("exact",(270,564,33,24,12,8)), ("root_only",(882,3150,98,98,8,2)),
                           ("binary_only",(1248,4398,33,90,4,6))):
        record, metrics = raw[mode], summary["modes"][mode]
        graph = {tuple(s): {tuple(n) for n in adj} for s,adj in record["component"]}
        edges = sum(map(len,graph.values())) // 2
        for s,adj in graph.items():
            for n in adj:
                assert s in graph[n] and sum((a^b).bit_count() for a,b in zip(s,n)) == 1
        # Count shortest paths directly from the archived graph, independent of the submitted BFS.
        wave, seen, depth = {after:1}, set(), 0
        while final not in wave:
            assert wave
            seen.update(wave)
            nxt = {}
            for s, count in wave.items():
                for n in graph[s]-seen:
                    nxt[n] = nxt.get(n,0) + count
            wave, depth = nxt, depth + 1
        first = record["first_edges"]
        found = (len(graph),edges,metrics["first"]["prior_states"],len(first),depth,wave[final])
        assert found == expected
        assert (depth,wave[final]) == (metrics["exchange_distance"],metrics["shortest_exchanges"])
        if mode == "exact":
            assert all(j == 0 and t in (8,9) for a,b,(j,t),d,k in first)
            assert all((a[0] & 6) != 6 and (a[0] & 128) != 0 for a,b,action,d,k in first)
            assert sum(k for a,b,action,d,k in first if d == 4) == 8
    for mode, initial, number in (("original_exact",start,2),("original_band",start,1900),("after_band",after,6)):
        arcs = [(tuple(a),tuple(b)) for a,b in raw[mode]]
        distance = lambda s: sum((a^b).bit_count() for a,b in zip(s,initial))
        ways = {initial:1}
        for a,b in sorted(arcs,key=lambda e: distance(e[0])):
            assert distance(b) == distance(a)+1 and sum((x^y).bit_count() for x,y in zip(a,b)) == 1
            ways[b] = ways.get(b,0) + ways[a]
        assert ways[final] == number == summary["geodesics"][mode]["shortest_paths"]
        assert shortest_interval(initial,final,mode == "original_exact") == number
        if initial == start:
            assert not ({chamber,after} & set(ways))
    family = raw["original_preparation_family"]
    assert len({tuple(r["start"]) for r in family}) == len(family) == 36
    counts = {"outside":0,"inside":0,"silent":0}
    for row in family:
        # Additional readback: predict the ordered normalizer's first binary write
        # from the two initial private holders and compare with the frozen trace.
        initial = row["start"]
        left, = (j for j,m in enumerate(initial) if m & (1 << 8))
        right, = (j for j,m in enumerate(initial) if m & (1 << 9))
        outside_chart, = set(range(3)) - {left,right}
        assert outside_chart == row["outsider"]
        if right < left:
            predicted = [right,8,1]
        elif outside_chart != 0:
            predicted = [outside_chart,8,1]
        else:
            predicted = None
        assert row["first"] == predicted
        if row["first"] is None:
            counts["silent"] += 1
            continue
        j,site,sign = row["first"]
        assert sign==1 and site in (8,9)
        outside = j == row["outsider"]
        counts["outside" if outside else "inside"] += 1
        assert row["profile_after"] == ([1,3,2] if outside else [2,3,1])
        assert not row["exact_prefix"]
    assert counts == {"outside":12,"inside":18,"silent":6}
    assert sum(r.get("still_holds_copied_leaf_at_return") is False for r in family) == 18
    assert summary["exact_witness_relabelings"] == 144
    receipt = json.loads(review.read("receipt.json"))
    assert published.read("foundation-checksums.txt") == foundation.read("SHA256SUMS")
    assert json.loads(published.read("publication_audit.json")) == {"audit": "PASS", **receipt}
    assert receipt["workflow_sha"] == receipt["checkout_sha"] == meta["verified_commit"]
    assert int(receipt["run_id"]) == meta["run"] and int(receipt["attempt"]) == 1
    assert receipt["model_requested"] == receipt["model_returned"] == "gemini-3.1-pro-preview"
    for key, name in (("request", "request.json"), ("response", "response.json"), ("prompt", "prompt.txt")):
        assert digest(review.read(name)) == receipt[key + "_sha256"]
    assert json.loads(review.read("request.json"))["contents"][0]["parts"][0]["text"].encode() == review.read("prompt.txt")
    parts = json.loads(review.read("response.json"))["candidates"][0]["content"]["parts"]
    answer = "\n".join(p["text"] for p in parts if "text" in p and not p.get("thought")).strip().encode()
    assert answer == review.read("review.txt")
    verdict = json.loads(answer)
    assert receipt["verdict"] == verdict["verdict"] == "ACCEPTED"
    assert (verdict["program_status"], verdict["native_bridge_status"]) == ("DERIVED", "OPEN")
    assert all(verdict[k] == [] for k in ("findings", "missing_assumptions", "counterexamples"))
    assert foundation.read("workflow-head.txt").decode().strip() == meta["verified_commit"]
    assert foundation.read("inherited-head.txt").decode().strip() == meta["historical_commit"]
    tests = json.loads(foundation.read("TEST_RECEIPT.json"))
    assert tests["passed"] and tests["tests_run"] == 22
    verify = json.loads(foundation.read("VERIFICATION.json"))
    assert verify["all_valid"] and json.loads(foundation.read("REPRODUCED_1615F.json"))["all_valid"]
    assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == verify["raw_certificate_sha256"] == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
print("PASS", meta["run"], receipt["model_returned"], verdict["verdict"], "native bridge", verdict["native_bridge_status"])
