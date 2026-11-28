"""Replay the v16.53 single missing incidence and clearance. Argument: pinned demo directory."""
import hashlib
import json
import sys
from collections import Counter
from itertools import groupby, permutations
from pathlib import Path
from random import Random

demo = Path(sys.argv[1]).resolve()
pins = {
    "producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "coverage.py": "e90576a0285357f62ca2f9d9cac872b2a226e823",
}
for file, expected in pins.items():
    data = (demo / file).read_bytes()
    assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected
sys.path.insert(0, str(demo))
import producer
import verifier

alphabet = tuple(range(7))
peers = ("A", "B", "C")
arities = {"outer": 3, "middle": 3, "inner": 3, "junction": 4, "source": 3,
           **{name: 3 for name in peers}}
identity = {name: tuple(range(n)) for name,n in arities.items()}


def prepare(evidence, wide, order, filled):
    # The only site varied between the marker arms is the remote evidence leaf.
    spec = {
        "outer": (alphabet, ("middle", "evidence", "outside6")),
        "middle": (range(6), ("inner", "key2", "outside5")),
        "inner": (range(5), ("junction", "key3", "outside4")),
        "evidence": (evidence, ()), "outside6": ((6,), ()), "outside5": ((5,), ()),
        "outside4": ((4,), ()), "key2": ((2,), ()), "key3": ((3,), ()),
        "junction": (range(4), ("source", "j", "k", "l")),
        "source": (range(4 if filled else 3), peers),
    }
    for name in "jkl":
        spec[name] = (range(4), ())
    for peer in peers:
        labels = (0, 1, 2) if peer == wide else (2, 2, 2)
        children = tuple(peer + str(i) for i in range(3))
        spec[peer] = ((0,1,2), children)
        for child, label in zip(children, labels):
            spec[child] = ((label,), ())
    sites = {}
    supports = []
    def build(name):
        sites[name] = len(supports)
        local, children = spec[name]
        supports.append(local)
        return tuple(build(children[i]) for i in order[name]) if children else ()
    tree = build("outer")
    start = [sum(1 << v for v, s in enumerate(supports) if j in s) for j in alphabet]
    profile = verifier.profile_check(tree, len(alphabet), start)
    return tree, sites, start, profile


def raw_support(state, site):
    return {j for j, row in enumerate(state) if row & (1 << site)}


def edits(path):
    result = []
    for before, after in zip(path, path[1:]):
        diff = [(j,a^b) for j,(a,b) in enumerate(zip(before, after)) if a != b]
        assert len(diff) == 1 and diff[0][1].bit_count() == 1
        j, bit = diff[0]
        result.append((j, bit.bit_length()-1, bool(after[j] & bit)))
    return result


def run(evidence, wide, order, palette, filled=False):
    tree, sites, start, q = prepare(evidence, wide, order, filled)
    nodes = producer.layout(tree)
    junction = sites["junction"]
    source = sites["source"]
    w = sites[wide]
    qtree = tree
    for name, childname in [("outer","middle"),("middle","inner"),("inner","junction")]:
        qtree = qtree[nodes[sites[name]].index(sites[childname])]
    # Observe the actual plan produced by normalize_four, before it is executed.
    lifts = []
    clearances = []
    def observe(frame, event, ignored):
        if event != "call":
            return
        if frame.f_code is producer.clear_role.__code__:
            f = frame.f_locals
            proper = producer.vertices(f["nodes"], f["child"])[1:]
            used = set().union(*(raw_support(f["state"], v) for v in proper))
            spare = raw_support(f["state"], f["child"]) - used
            clearances.append((f["child"], f["x"], f["y"], spare))
        if frame.f_code is not producer.lift_root_path.__code__:
            return
        f = frame.f_locals
        local_roots = producer.layout(f["tree"])[0]
        source_slot = nodes[junction].index(source)
        assert f["tree"] == qtree
        caller = frame.f_back.f_back.f_back  # Skip normalize_four and the junction implementation.
        while caller is not None and caller.f_code is not producer._normalize.__code__:
            caller = caller.f_back
        labels = list(range(4))
        while caller is not None and caller.f_code is producer._normalize.__code__:
            labels = [caller.f_locals["labels"][i] for i in labels]
            caller = caller.f_back.f_back
        roots = [[{labels[j] for j in row} for row in step] for step in f["root_path"]]
        lifts.append((labels, roots, source_slot, local_roots, list(f["state"]),
                      list(f["q"]), list(f["order"]), f["root_path"][0]))
    old = sys.getprofile()
    sys.setprofile(observe)
    try:
        path = producer.normalize(start, tree, len(alphabet), q, palette)
    finally:
        sys.setprofile(old)
    # Endpoint from the verifier, also handling arbitrary external enumeration.
    canonical = verifier.model(tree, q, len(alphabet))[2]
    endpoint = [canonical[palette.index(j)] for j in alphabet]
    peak = verifier.path_check(tree, len(alphabet), q, path, start, endpoint)
    x = next(j for j in palette if j in evidence)
    removed = 1-x
    (labels, planned, slot, local_roots, lift_start, lift_q, lift_order, initial_roots), = lifts
    assert labels == [3,2,x,removed]
    local_edits = [(step[slot], nxt[slot]) for step,nxt in zip(planned,planned[1:])
                   if step[slot] != nxt[slot]]
    full = set(range(4))
    expected = [(full, full-{removed})]
    if not filled:
        expected.insert(0, ({0,1,2},full))
        assert planned[1][slot] == full and all(row == full for row in planned[1])
    assert local_edits == expected
    steps = edits(path)
    gain_receiver = steps.index((3,w,True)) + 1
    if filled:
        assert not clearances
        assert (3,source,True) not in steps[:gain_receiver]
        return {"start":start, "profile":q, "endpoint":endpoint, "early_receiver_gain":gain_receiver,
                "plan":local_edits, "peak":peak}
    assert clearances == [(local_roots[slot], labels.index(removed), labels.index(3), {labels.index(3)})]
    if order == identity and palette == alphabet and wide == "A":
        premature = [set(row) for row in initial_roots]
        premature[slot].remove(labels.index(removed))
        try:
            producer.lift_root_path(lift_start, qtree, lift_q, [initial_roots, premature], lift_order, [])
        except producer.ConstructionFailure as error:
            assert str(error) == "root deletion below minimum"
        else:
            raise AssertionError("Original lift accepted a withdrawal below the required width")
    gain = steps.index((3,source,True)) + 1
    cut = next(i for i in range(gain, len(steps)) if steps[i] == (removed,source,False)) + 1
    assert gain < gain_receiver < cut
    region = set(producer.vertices(nodes, source))
    moves = [(j,v,add) for j,v,add in steps[gain-1:cut] if v in region]
    tip, = [v for v in nodes[w] if removed in raw_support(path[gain], v)]
    assert moves == [(3,source,True),(3,w,True),(3,tip,True),
                     (removed,tip,False),(removed,w,False),(removed,source,False)]
    assert raw_support(path[gain-1], w) == raw_support(path[gain-1],source) == {0,1,2}
    assert raw_support(path[cut], w) == raw_support(path[cut],source) == {2,3,x}
    assert all(not (s[3] & (1 << n)) for s in path[:cut+1]
               for name in peers if name != wide for n in producer.vertices(nodes,sites[name]))
    # The same receiver's local observation suffices without a supplied clock.
    word = []
    for s in path[:cut+1]:
        held = sorted(raw_support(s,w))
        if not word or word[-1] != held:
            word.append(held)
    assert word == [[0,1,2],[0,1,2,3],sorted([2,3,x])]
    return {"start":start, "profile":q, "endpoint":endpoint, "peak":peak, "word":word,
            "gain":gain,"write":gain_receiver,"cut":cut, "length":len(path)-1, "m":x,
            "raw_window":path[gain-1:cut+1],"sites":sites, "labels":labels}


def settings():
    yield identity, alphabet
    yield identity, alphabet[::-1]
    for name,n in arities.items():
        for local in permutations(range(n)):
            if local != identity[name]:
                yield {**identity,name:local}, alphabet
    rng = Random(5303)
    for src_order in permutations(range(3)):
        for j_order in permutations(range(4)):
            other = {name:tuple(rng.sample(range(n),n)) for name,n in arities.items()}
            yield {**other,"source":src_order,"junction":j_order}, tuple(rng.sample(alphabet,7))


def receiver_controls():
    # Only reorder the three leaves *inside* the wide receiver. Compare using their original names.
    for x in (0,1):
        projections = [{}, {}]
        for filled in (False, True):
            for permutation in permutations(range(3)):
                order = {**identity, "A":permutation}
                tree, sites, start, q = prepare((x,), "A", order, filled)
                path = producer.normalize(start, tree, 7, q, alphabet)
                verifier.path_check(tree, 7, q, path, start, verifier.model(tree,q,7)[2])
                names = ("A","A0","A1","A2")
                rows = (tuple(tuple(sorted(raw_support(state,sites[name]))) for name in names) for state in path)
                whole = tuple(k for k,_ in groupby(rows))
                root_word = tuple(k for k,_ in groupby(r[0] for r in whole))
                stop = next(i for i,r in enumerate(whole) if set(r[0]) == {2,3,x})
                projections[filled][permutation] = (root_word, whole[:stop+1], whole)
        for perm in projections[0]:
            assert projections[0][perm][0] == projections[1][perm][0]
            assert projections[0][perm][2] != projections[1][perm][2]
        matches = [(a,b) for a,wa in projections[0].items() for b,wb in projections[1].items()
                   if wa[1] == wb[1]]
        assert len(matches) == 1
        print("Evidence", x, "complete root word matches at all six leaf orders;",
              "four-site prefixes match across leaf orders", matches)


def main():
    totals = Counter()
    for i,(order,palette) in enumerate(settings()):
        previous = None
        for wide in peers:
            a,b = [run((x,),wide,order,palette) for x in (0,1)]
            site = a["sites"]["evidence"]
            assert [l^r for l,r in zip(a["start"],b["start"])] == [1<<site,1<<site,0,0,0,0,0]
            assert a["profile"] == b["profile"] and a["endpoint"] == b["endpoint"]
            if previous is not None:
                tips = {a["sites"][p+str(tip)] for p in peers for tip in range(3)}
                different = {v for v in a["sites"].values()
                             if raw_support(previous,v) != raw_support(a["start"],v)}
                assert different and different <= tips
            previous = a["start"]
            totals["pairs"] += 1
            if i == 0:
                print("Default",wide,[(r["gain"],r["write"],r["cut"],r["word"]) for r in (a,b)])
        totals["settings"] += 1
    for x in (0,1):
        result = run((x,), "A", identity, alphabet, filled=True)
        print("Prefilled source",x,"receiver already gains 3 at", result["early_receiver_gain"],
              "source plan",[(sorted(a),sorted(b)) for a,b in result["plan"]])
    for palette in (alphabet, alphabet[::-1]):
        result = run((0,1), "A", identity, palette)
        print("Tied remote evidence, palette",palette,"receiver retains",result["m"])
    assert totals["settings"] == 204 and totals["pairs"] == 612
    print("Checked",dict(totals),"paired whole paths",2*totals["pairs"])
    receiver_controls()


if __name__ == "__main__":
    if sys.argv[2:] == ["--example"]:
        print(json.dumps([run((x,),"A",identity,alphabet) for x in (0,1)],separators=(",",":")))
    else:
        main()
