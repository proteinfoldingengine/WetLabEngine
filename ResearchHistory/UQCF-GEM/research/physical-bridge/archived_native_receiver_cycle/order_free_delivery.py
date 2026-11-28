"""Replay the v16.51 rank-one first write and rank-two source-survivor controls."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
import lzma
from pathlib import Path
import sys

from ternary_preparation import ARCHIVE_SHA256, PINS

HERE = Path(__file__).resolve().parent


def encode(row):
    return (json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode()


def schedules(nodes, v=0):
    """All sibling orders, retaining old vertex IDs alongside the new tree."""
    if not nodes[v]:
        yield (), (v,)
        return
    for children in permutations(nodes[v]):
        for choices in product(*(list(schedules(nodes, c)) for c in children)):
            tree = tuple(t for t, _ in choices)
            names = (v,) + tuple(site for _, group in choices for site in group)
            yield tree, names


def translate(state, names):
    return [sum(1 << i for i, u in enumerate(names) if z & (1 << u)) for z in state]


def run(p, verifier, tree, start, order):
    k = len(start)
    q = verifier.profile_check(tree, k, start)
    trace = []
    path = p.normalize(start, tree, k, q, order=order, trace=trace)
    # The verifier's canonical construction uses natural label order. Pull it
    # back to global labels to check the endpoint for each alternate priority.
    canonical = verifier.model(tree, q, k)[2]
    endpoint = [canonical[order.index(j)] for j in range(k)]
    verifier.path_check(tree, k, q, path, start, endpoint)
    return path, trace


def support(state, c):
    return {j for j, mask in enumerate(state) if mask & (1 << c)}


def missing_pair(state, children):
    return [(c,j) for c in children for j, z in enumerate(state) if not z & (1 << c)]


def gain_frames(path, label, sites):
    out = {}
    for c in sites:
        hits = [i for i in range(1, len(path))
                if path[i][label] & ~path[i-1][label] & (1 << c)]
        assert len(hits) == 1
        out[c], = hits
    return out


def check_footprint(p, tree, path, site, label):
    nodes = p.layout(tree)
    descendants = p.vertices(nodes, site)
    times = gain_frames(path, label, descendants)
    assert times[site] == 1
    assert all(times[u] < times[c] for u in descendants for c in nodes[u])
    return times


def archived_and_controls(p, v, rows, record):
    counts = Counter()
    archived_indices = []
    for idx, case in enumerate(rows):
        s = case["spec"]
        tree = p.TREES[s["tree"]]
        start = case["start"]
        q = v.profile_check(tree, len(start), start)
        assert q == s["q"]
        if q[0] != 1:
            continue
        counts["rank_one_archived_cases"] += 1
        nodes, targets, _ = p.data(tree, q)
        holes = missing_pair(start, nodes[0])
        if len(holes) != 1:
            continue
        counts["unique_upper_hole_cases"] += 1
        site, x = holes[0]
        region = p.vertices(nodes, site)
        if len(region) == 1 or any(targets.get(u,1) != 1 for u in region):
            continue
        path, _ = run(p, v, tree, start, tuple(range(len(start))))
        assert case["failure"] is None and path == case["path"]
        gains = check_footprint(p,tree,path,site,x)
        archived_indices.append(idx)
        record(dict(kind="archived", case=idx, receiver=site, label=x, gains=gains, path=path))
    counts["rank_one_receiving_subtree_cases"] = len(archived_indices)

    case = rows[1728]
    assert case["spec"]["tree"] == "U" and case["start"] == [65399,187]
    detail = {}
    ends = Counter()
    for tree, names in schedules(p.layout(p.U)):
        for order in permutations(range(2)):
            start = translate(case["start"], names)
            path, _ = run(p,v,tree,start,order)
            (site,x), = missing_pair(start,p.layout(tree)[0])
            assert (names[site],x) == (9,1)
            gains = check_footprint(p,tree,path,site,x)
            complete = set(p.vertices(p.layout(tree),site))
            end_sites = {u for u in complete if path[-1][x] & (1 << u)}
            assert end_sites == (complete if order[0] == x else set())
            ends[len(end_sites)] += 1
            counts["case_1728_complete_order_runs"] += 1
            record(dict(kind="case_1728_order", map=names, order=order, path=path))
            if names == tuple(range(len(names))) and order == (0,1):
                assert path == case["path"]
                assert len(path) == 17 and path[-1] == start
                q = v.profile_check(tree,2,start)
                v.path_check(tree,2,q,[start],start,path[-1])
                detail["first_gains"] = gains
                detail["original_path"] = path
                detail["stationary_path_verified"] = True

    # The exact historical binary child is a full binary tree of seven sites.
    # Match its two local inputs with identical descendants and one extra bit
    # at its root in the actual arm. No observer-chosen site is passed to it.
    child = p.U[2]
    raw = [127, 1]
    q = [1,1,1]
    actual = p.binary.normalize(raw, child, 2, q)
    with_gain = [z[1] for z in actual]
    without = p.binary.normalize([127], child, 1, q)
    assert without == [[127]] and set(gain_frames(actual,1,range(1,7))) == set(range(1,7))
    site_mask = 127 << 9
    projected = [[(z & site_mask) >> 9 for z in f] for f in case["path"]]
    # Stop at the actual child return, just before outer palette compression.
    assert projected[3:3+len(actual)] == actual
    detail.update(local_actual=actual, local_without_gain=without, local_new_role_masks=with_gain,
                  endpoint_number_of_sites=dict(ends))
    return counts, archived_indices, detail


def peer_controls(p, v, record):
    # Old node IDs: source leaf 1, fork 2 with leaves 3 and 4, bystander leaf 5.
    leaf = ()
    tree0 = (leaf, (leaf,leaf), leaf)
    common = [7,7,29,33]
    counts = Counter()
    examples = {}
    for tree, names in schedules(p.layout(tree0)):
        source, receiver = names.index(1), names.index(2)
        neutral = names.index(5)
        nodes = p.layout(tree)
        descendants = p.vertices(nodes, receiver)
        source_first = nodes[0].index(source) < nodes[0].index(receiver)
        for order in permutations(range(4)):
            initial = translate(common, names)
            expected = next(j for j in order if j in (0,1))
            for surviving in (None, 0, 1):
                start = initial[:]
                if surviving is not None:
                    start[1 - surviving] &= ~(1 << source)
                y = expected if surviving is None else surviving
                path, trace = run(p,v,tree,start,order)
                anchor, = [s for s in trace if s["kind"] == "anchor"]
                assert anchor["label"] == y
                assert {nodes[0][i] for i in anchor["pair"]} == {source,receiver}
                done = {s["child"]: s["end"] for s in trace if s["kind"] == "child_normalization"}
                at_receiver = path[done[receiver]]
                assert all(support(at_receiver,u) == {y} for u in descendants)
                assert all(support(start,u) == {2} for u in nodes[receiver])
                assert support(start, neutral) == support(at_receiver, neutral) == {3}
                # At the end of all three initial visits only the prescribed
                # survivor is present at both participating branches.
                parent_cut = max(done.values())
                assert support(path[parent_cut],source) == {y}
                assert at_receiver[y] & (1 << receiver)
                assert all(support(path[parent_cut],u) == {y} for u in descendants)
                if surviving is None:
                    counts["common_runs"] += 1
                    if source_first:
                        counts["source_first"] += 1
                        counts["source_first_survivor_" + str(y)] += 1
                        clipped = initial[:]
                        clipped[1-y] &= ~(1 << source)
                        # The bystander, if visited first, contributes no edit.
                        assert done[source] == 1 and path[1] == clipped
                        replay, _ = run(p,v,tree,path[1],order)
                        assert replay == path[1:]
                    else:
                        counts["receiver_first"] += 1
                        assert support(at_receiver,source) == {0,1}
                else:
                    counts["post_prune_runs"] += 1
                    initial_outer = [set(support(start,u)) for u in nodes[0]]
                    shared = [(i,j,lab) for i in range(3) for j in range(i+1,3)
                              for lab in initial_outer[i]&initial_outer[j]]
                    assert len(shared) == 1
                    # Only the receiving fork changes in the first full pass.
                    outside = ~sum(1 << u for u in descendants)
                    assert all(all(((z ^ a) & outside) == 0 for z,a in zip(frame,start))
                               for frame in path[:parent_cut+1])
                record(dict(kind="peer", map=names, order=order, fixed_survivor=surviving,
                            source_end=done[source], receiver_end=done[receiver], cut=parent_cut, path=path))
                if names == tuple(range(6)) and order == (0,1,2,3):
                    examples[str(surviving)] = dict(start=start, source_end=done[source],
                            cut=parent_cut, first_pass=path[parent_cut], full_path=path)
    return counts, examples


def unique_prune_controls(p, v, demo, record):
    modules = {}
    for name, digest in (
            ("engine", "6502835186740c437b636cb08a63a446614b196df5dc1ca50a0c7ba07e4f6260"),
            ("verify", "8aa98fa05f473a10b81439e06aba4c20f5e97138262ae472dd191591d06fd670")):
        path = demo.parent / "v16.26-consistency-increment-law" / (name + ".py")
        assert sha256(path.read_bytes()).hexdigest() == digest
        spec = importlib.util.spec_from_file_location("atom_" + name, path)
        modules[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modules[name])
    start = [499,655]
    nodes = p.layout(p.T)
    parents = [-1] + [next(v for v, cs in enumerate(nodes) if u in cs) for u in range(1,len(nodes))]
    views = [[u for u in range(len(nodes)) if mask & (1 << u)] for mask in start]
    accepted = []
    for index, sites in enumerate(views):
        for site in sites:
            try:
                result = modules["engine"].atomic(parents,views,index,site)
            except ValueError:
                continue
            accepted.append(result)
    event, = accepted
    assert modules["verify"].verify_atomic(event) == (0,True)
    assert (event["tau_before"], event["tau_after"], event["h_before"], event["h_after"]) == (1,2,2,2)
    assert (event["index"],event["leaf"],event["parent"]) == (0,1,0)
    after = [sum(1 << u for u in row) for row in event["after"]]
    assert after == [497,655]
    counts = Counter()
    for tree, names in schedules(nodes):
        receiver = names.index(4)
        sites = [receiver, *p.layout(tree)[receiver]]
        for order in permutations(range(2)):
            for pruned, state in ((False,start),(True,after)):
                seed = translate(state,names)
                path, trace = run(p,v,tree,seed,order)
                done, = [e["end"] for e in trace if e["kind"]=="child_normalization" and e["child"]==receiver]
                if pruned:
                    assert all(support(frame,u)=={0} for frame in path[:done+1] for u in sites)
                else:
                    gains = gain_frames(path[:done+1],1,sites)
                    assert gains[receiver] == 1
                counts["unique_prune_paired_orders"] += pruned
                record(dict(kind="unique_prune", pruned=pruned, map=names, order=order,
                            receiver_end=done, path=path))
    return counts,event


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo",type=Path)
    parser.add_argument("--certificate",type=Path)
    parser.add_argument("--write-paths",action="store_true")
    args = parser.parse_args()
    demo = args.demo.resolve()
    for name,digest in PINS.items():
        assert sha256((demo/name).read_bytes()).hexdigest() == digest
    sys.path.insert(0,str(demo))
    import producer as p
    import verifier as v
    blob = (args.certificate or demo/"evidence/science/scientific/CERTIFICATE.json.gz").read_bytes()
    assert sha256(blob).hexdigest() == ARCHIVE_SHA256
    rows = json.loads(gzip.decompress(blob))["cases"]
    digest = sha256()
    with lzma.open(HERE/"order_free_delivery_paths.jsonl.xz","wb" if args.write_paths else "rb") as evidence:
        def record(row):
            line = encode(row)
            digest.update(line)
            if args.write_paths:
                evidence.write(line)
            else:
                assert evidence.readline() == line
        count1, cases, detail = archived_and_controls(p,v,rows,record)
        count2, pair = peer_controls(p,v,record)
        count3, atom = unique_prune_controls(p,v,demo,record)
        if not args.write_paths:
            assert evidence.read(1) == b""
    print(json.dumps(dict(archive_sha256=ARCHIVE_SHA256, counts=count1+count2+count3,unique_atom=atom,
                         archived_cases=cases, case_1728=detail, peer_examples=pair,
                         evidence_sha256=digest.hexdigest()),indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
