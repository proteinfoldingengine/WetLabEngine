"""Trace the payload and peer selected by ordinary v16.51 disjoint role exchange."""
import argparse
from collections import Counter, defaultdict
import gzip
from hashlib import sha256
from itertools import combinations, product
import json
import lzma
from pathlib import Path
import sys
from unittest.mock import patch

from ternary_preparation import ARCHIVE_SHA256, PINS

HERE = Path(__file__).resolve().parent


def encode(row):
    return (json.dumps(row, sort_keys=True, separators=(",", ":"))+"\n").encode()


def observe(p, verifier, tree, ranks, start):
    """Observe the historical worker, including its two calls from the same cross frame."""
    original = p.replace_role
    exchanges = []
    pending = None

    def watch(current, nodes, child, removed, added, path):
        nonlocal pending
        worker = sys._getframe(1)
        caller = worker.f_back
        if caller.f_code.co_name != "cross":
            return original(current, nodes, child, removed, added, path)
        c, w = caller.f_locals, worker.f_locals
        swap = caller.f_back
        assert swap.f_code.co_name == "swap"
        indices = [swap.f_locals[name] for name in ("i", "j")]
        direct = w["owner"][indices[0]] != w["owner"][indices[1]]
        begin = len(path)-1
        capture = dict(slot=w["i"], slots=[c["i"],c["j"]], direct=direct, source_label=c["x"], desired=c["y"],
                       owners=list(w["owner"]), roles=list(w["flat"]), child=child,
                       removed=removed, added=added, begin=begin)
        original(current, nodes, child, removed, added, path)
        capture["end"] = len(path)-1
        if w["i"] == c["i"]:
            assert pending is None
            assert (removed, added) == (c["x"], c["y"])
            pending = capture
        else:
            assert pending is not None and pending["end"] == begin
            assert (removed, added) == (c["y"], c["x"])
            assert pending["child"] != child and pending["slots"] == capture["slots"]
            exchanges.append((pending, capture))
            pending = None

    with patch.object(p, "replace_role", watch):
        path = p.normalize(start, tree, len(start), ranks)
    assert pending is None
    endpoint = verifier.model(tree, ranks, len(start))[2]
    verifier.path_check(tree, len(start), ranks, path, start, endpoint)
    return path, exchanges


def focal(exchanges, destination):
    pair, = [(a,b) for a,b in exchanges if a["child"] == 1 and b["child"] == destination and a["desired"] == 1]
    return pair


def rename(state, mapping):
    result = [0]*len(state)
    for label, mask in enumerate(state):
        result[mapping.get(label, label)] = mask
    return result


def primitive_steps(path):
    result = []
    for before, after in zip(path,path[1:]):
        (x, change), = [(j,a^b) for j,(a,b) in enumerate(zip(before, after)) if a != b]
        assert change.bit_count() == 1
        result.append((x, change))
    return result


def midpoint_readout(midpoint, children, targets):
    """Infer the missing labels, the unique double holder, and its canonical owner."""
    holders = [[c for c in children if mask & (1 << c)] for mask in midpoint]
    repeated, = [label for label, branches in enumerate(holders) if len(branches) > 1]
    pair = holders[repeated]
    assert len(pair) == 2
    missing = {label for label, branches in enumerate(holders) if not branches}
    canonical = next((c for c, row in zip(children, targets) if repeated in row), None)
    return missing, repeated, pair, canonical


def single_mismatch_exchange(state, children, endpoint):
    """Predict one exchange using only incidence, topology and the ordered target.

    This restricted prediction applies when the first mismatched branch has
    one wrong role and its desired role already lives in exactly one peer.
    """
    branches = children[0]
    def support(raw, node):
        return {j for j, mask in enumerate(raw) if mask & (1 << node)}

    source = next(c for c in branches if support(state, c) != support(endpoint, c))
    current, desired = support(state, source), support(endpoint, source)
    x, = current - desired
    y, = desired - current
    receiver, = [c for c in branches if c != source and y in support(state, c)]

    def preorder(c):
        return [c] + [site for child in children[c] for site in preorder(child)]

    path = [state[:]]
    for c, old, new in ((source, x, y), (receiver, y, x)):
        sites = [site for site in preorder(c) if path[-1][old] & (1 << site)]
        assert sites and new not in support(path[-1], c)
        for label, ordered in ((new, sites), (old, reversed(sites))):
            for site in ordered:
                step = path[-1][:]
                step[label] ^= 1 << site
                path.append(step)
    return path


def interleavings(p, verifier, tree, q, path, exchange):
    source, peer = exchange
    lo, mid, hi = source["begin"], source["end"], peer["end"]
    s = primitive_steps(path[lo:mid+1])
    r = primitive_steps(path[mid:hi+1])
    assert (len(s),len(r)) == (4,6)
    counts = Counter()
    for positions in combinations(range(len(s)+len(r)), len(s)):
        left, right = iter(s), iter(r)
        chunk = [path[lo]]
        for i in range(len(s)+len(r)):
            x, mask = next(left if i in positions else right)
            state = chunk[-1][:]
            state[x] ^= mask
            chunk.append(state)
        assert chunk[-1] == path[hi]
        whole = path[:lo]+chunk+path[hi+1:]
        verifier.path_check(tree, len(path[0]), q, whole, whole[0], path[-1])
        loses_payload = any(state[source["removed"]] == 1 for state in chunk)
        loses_desired = any(state[source["added"]] == 1 for state in chunk)
        assert loses_payload == (positions == (0,1,2,3))
        assert loses_desired == (positions == (6,7,8,9))
        counts["total"] += 1
        counts["payload_absent_below_root"] += loses_payload
        counts["both_labels_continuously_held_below_root"] += not (loses_payload or loses_desired)
    return dict(counts)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("demo",type=Path)
    ap.add_argument("--certificate",type=Path)
    ap.add_argument("--write-records",action="store_true")
    args = ap.parse_args()
    demo = args.demo.resolve()
    for name, pin in PINS.items():
        assert sha256((demo/name).read_bytes()).hexdigest() == pin
    sys.path.insert(0,str(demo))
    import producer as p
    import verifier as v

    raw = (args.certificate or demo/"evidence/science/scientific/CERTIFICATE.json.gz").read_bytes()
    assert sha256(raw).hexdigest() == ARCHIVE_SHA256
    original = json.loads(gzip.decompress(raw))["cases"]
    t, q = p.T, [3,2,1,1]
    nodes = p.layout(t)
    examples, census = {}, Counter()
    grouped = defaultdict(list)
    midpoint_outputs = defaultdict(lambda: (set(), set()))
    relays = []
    digest, size = sha256(), 0
    with lzma.open(HERE/"peer_exchange_paths.jsonl.xz", "wb" if args.write_records else "rb") as data:
        def record(row):
            nonlocal size
            line = encode(row)
            digest.update(line)
            size += 1
            if args.write_records:
                data.write(line)
            else:
                assert data.readline() == line

        for i, archived in enumerate(original):
            spec = archived["spec"]
            tree, k, ranks = p.TREES[spec["tree"]], spec["k"], spec["q"]
            layout, _, widths = p.data(tree, ranks)
            children = layout[0]
            targets = p.palettes(list(range(k)), [widths[c] for c in children], ranks[0])
            if ranks[0] == 2:
                path = p.normalize(archived["start"], tree, k, ranks)
                assert archived["failure"] is None and path == archived["path"]
                v.path_check(tree, k, ranks, path, archived["start"], v.model(tree, ranks, k)[2])
                census["rank_two_paths"] += 1
                for c, row in zip(children, targets):
                    if widths[c] == 1:
                        census["rank_two_width_one_branches"] += 1
                        for before, after in zip(path, path[1:]):
                            gains = {j for j in range(k) if (after[j] & ~before[j]) & (1 << c)}
                            assert gains <= set(row)
                            census["rank_two_width_one_gains"] += len(gains)
            if spec["q"][0] != 3:
                continue
            _, start, _ = v.model(tree, ranks, k, spec["permutation"], spec["mode"])
            assert start == p.initial(tree, k, ranks, spec["permutation"], spec["mode"]) == archived["start"]
            path, calls = observe(p, v, tree, ranks, start)
            assert archived["failure"] is None and path == archived["path"]
            census["archive_paths"] += 1
            for a,b in calls:
                missing, repeated, pair, canonical = midpoint_readout(path[a["end"]], children, targets)
                assert len(missing) == k - sum(map(len, targets)) + 1
                assert repeated == a["added"] and set(pair) == {a["child"], b["child"]}
                assert a["removed"] in missing and all(path[a["end"]][j] == 1 for j in missing)
                saturated = len(missing) == 1
                census["saturated_exchanges" if saturated else "spare_exchanges"] += 1
                mid = path[a["end"]]
                possible, direct_outputs = midpoint_outputs[spec["tree"],tuple(ranks),k,tuple(mid)]
                outcome = (a["child"],b["child"],a["removed"])
                possible.add(outcome)
                if a["direct"]:
                    assert canonical == a["child"] and [c for c in pair if c != canonical] == [b["child"]]
                    census["direct_exchanges"] += 1
                    census["direct_saturated_exchanges"] += saturated
                    if saturated:
                        # Supply no trace variables to the reconstruction. The
                        # direct-exchange hypothesis fixes the orientation.
                        x, = missing
                        receiver, = [c for c in pair if c != canonical]
                        continuation = [mid[:]]
                        p.replace_role(mid[:],layout,receiver,repeated,x,continuation)
                        assert continuation == path[a["end"]:b["end"]+1]
                        direct_outputs.add(outcome)
                key = (spec["tree"], tuple(ranks), k, tuple(path[a["end"]]), a["child"], a["desired"], b["child"])
                grouped[key].append((i, spec["mode"], a["removed"], a["end"]))
                census["archive_exchanges"] += 1
            if spec["mode"] == "compact":
                for (a, b), (c, d) in zip(calls, calls[1:]):
                    if b["end"] != c["begin"] or b["child"] != c["child"] or a["removed"] != c["removed"]:
                        continue
                    branches = [a["child"], b["child"], d["child"]]
                    if len(set(branches)) != 3:
                        continue
                    fresh = p.normalize(path[b["end"]], tree, k, ranks)
                    v.path_check(tree, k, ranks, fresh, path[b["end"]], path[-1])
                    relays.append(dict(case=i, frames=[a["begin"],a["end"],b["end"],c["end"],d["end"]],
                                       branches=branches, payload=a["removed"], exact_restart=fresh==path[b["end"]:]))
                    if i == 170:
                        assert a["direct"] and c["direct"] and path[24:] == fresh and len(fresh) == 13
                        assert path[18][3] == path[30][3] == 1
                        assert path[24][3] == sum(1 << j for j in (0,4,5,6))
                        assert path[-1][3] == sum(1 << j for j in (0,7,8,9))
                        assert relays[-1]["frames"] == [14,18,24,30,36]
                        endpoint = v.model(tree, ranks, k)[2]
                        topology = v.topology(tree)[0]
                        segment = single_mismatch_exchange(path[14],topology,endpoint)
                        tail = single_mismatch_exchange(segment[-1],topology,endpoint)
                        assert segment + tail[1:] == path[14:] and tail[-1] == endpoint
                        from_before = p.normalize(path[14],tree,k,ranks)
                        assert from_before == path[14:]
                        v.path_check(tree,k,ranks,from_before,path[14],endpoint)
                        census["case_170_incidence_predicted_edits"] = len(segment) + len(tail) - 2
                    record(dict(test="archived_compact_relay", case=i, spec=spec, path=path, exchanges=calls, restart=fresh))
            if i in (176,177):
                a,b = focal(calls,7)
                examples[i] = (path,a,b)
                record(dict(test="original", case=i, spec=spec, path=path, exchanges=calls))

        collisions = []
        for key, instances in grouped.items():
            if len({x for _,_,x,_ in instances}) <= 1:
                continue
            collisions.append(dict(tree=key[0], ranks=key[1], k=key[2], midpoint=key[3],
                                   sender=key[4], gained=key[5], peer=key[6], occurrences=instances))
        census["distinct_midpoint_keys"] = len(grouped)
        census["keys_with_several_payloads"] = len(collisions)
        census["keys_with_several_payloads_in_compact_alone"] = sum(
            len({x for _,mode,x,_ in row["occurrences"] if mode=="compact"})>1 for row in collisions)
        census["distinct_direct_saturated_midpoints"] = sum(bool(d) for _, d in midpoint_outputs.values())
        census["direct_saturated_midpoints_with_competing_archive_outcome"] = sum(
            bool(d) and pset != d for pset, d in midpoint_outputs.values())
        assert (len(grouped),len(collisions)) == (1154,73)
        assert len(relays) == len({r["case"] for r in relays}) == 14
        assert [r["case"] for r in relays if r["exact_restart"]] == [170,1466]

        path4,a4,b4 = examples[176]
        path3,a3,b3 = examples[177]
        assert path4[0][0] ^ path3[0][0] == 2 and path4[0][1:] == path3[0][1:]
        same = path4[a4["end"]]
        assert same == path3[a3["end"]] == [7,907,113,1,1]
        assert (a4["end"],a3["end"]) == (12,7)
        assert b4["roles"] == b3["roles"] == [0,1,2,1] and b4["owners"] == b3["owners"] == [1,1,4,7]
        assert b4["slots"] == b3["slots"] == [1,3]
        assert v.profile_check(t,5,same) == [2,2,1,1]
        receiver_region = sum(1 << j for j in (7,8,9))
        delivered4, delivered3 = path4[b4["end"]], path3[b3["end"]]
        assert delivered4 != delivered3
        assert all(((left ^ right) & ~receiver_region) == 0 for left, right in zip(delivered4, delivered3))
        assert delivered4[4] & receiver_region == delivered3[3] & receiver_region == receiver_region

        # Re-enter precisely the receiver worker used in both original calls,
        # varying only the payload actually retained by the enclosing exchange.
        for path,b in ((path4,b4),(path3,b3)):
            state = same[:]
            replay = [state[:]]
            p.replace_role(state,nodes,7,1,b["added"],replay)
            assert replay == path[b["begin"]:b["end"]+1]
            fresh = p.normalize(replay[-1],t,5,q)
            v.path_check(t,5,q,fresh,replay[-1],path[-1])
            assert fresh == path[b["end"]:]
        assert len(path4)-1-b4["end"] == 6 and len(path3)-1-b3["end"] == 0

        # Two independent permutations preserve compactness and change the
        # source's earlier role and/or which peer holds the desired label.
        panel = []
        for change_source, change_peer in product((False,True), repeat=2):
            mapping = {}
            if change_source:
                mapping.update({0:4,4:0})
            if change_peer:
                mapping.update({1:2,2:1})
            start = rename(path4[0],mapping)
            path, calls = observe(p,v,t,q,start)
            dest = 4 if change_peer else 7
            x = 3 if change_source else 4
            a,b = focal(calls,dest)
            assert (a["removed"],b["added"]) == (x,x)
            assert path[a["end"]][x] == 1
            if dest == 4:
                assert any(c["begin"] == b["end"] and (c["child"],c["removed"],e["child"],e["added"]) ==
                           (4,x,7,x) for c,e in calls)
            fresh = p.normalize(path[b["end"]],t,5,q)
            assert fresh == path[b["end"]:]
            shuffle = interleavings(p,v,t,q,path,(a,b))
            assert shuffle == dict(total=210,payload_absent_below_root=1,both_labels_continuously_held_below_root=208)
            record(dict(test="two_factors", source_changed=change_source, peer_changed=change_peer,
                        path=path, exchanges=calls, restart=fresh))
            panel.append(dict(source_changed=change_source, peer_changed=change_peer, destination=dest,
                              payload=x, midpoint=path[a["end"]], received=path[b["end"]], shuffles=shuffle))

        # Each start is an injective relabeling of the same compact four-role
        # pattern, with the historical numeric order retained for processing.
        nfamily = 0
        for k in range(4,33):
            for dest in (4,7):
                midpoints,outputs = set(),set()
                other = 11-dest
                for x in range(3,k):
                    canonical = p.canonical(t,k,q)
                    initial_labels = [0,x,2,1] if dest == 7 else [0,x,1,2]
                    remaining = [j for j in range(k) if j not in initial_labels]
                    start = rename(canonical, dict(enumerate(initial_labels + remaining)))
                    assert all(start[j] & 1 for j in range(k))
                    assert start[1] == 1+sum(1<<u for u in [dest,*nodes[dest]])
                    assert start[2] == 1+sum(1<<u for u in [other,*nodes[other]])
                    path, calls = observe(p,v,t,q,start)
                    a,b = focal(calls,dest)
                    assert a["begin"] == 0 and a["end"] == 4 and b["end"] == 10
                    assert single_mismatch_exchange(start,v.topology(t)[0],v.model(t,q,k)[2]) == path[:11]
                    assert (a["removed"], b["added"]) == (x,x)
                    midpoints.add(tuple(path[4]))
                    outputs.add(tuple(path[5]))
                    assert all(path[4][j] == 1 for j in range(3,k))
                    assert path[5][x] == (1 | (1<<dest))
                    assert path[10][x] == 1+sum(1<<u for u in [dest,*nodes[dest]])
                    fresh = p.normalize(path[10],t,k,q)
                    assert fresh == path[10:]
                    if dest == 4:
                        assert any(c["begin"]==10 and c["removed"]==x and e["child"]==7
                                   and e["added"]==x for c,e in calls)
                        second = single_mismatch_exchange(path[10],v.topology(t)[0],v.model(t,q,k)[2])
                        assert second == path[10:10+len(second)]
                    record(dict(test="family", k=k, destination=dest, payload=x, path=path))
                    nfamily += 1
                assert len(midpoints) == 1 and len(outputs) == k-3
        if not args.write_records:
            assert data.read(1) == b""

    print(json.dumps(dict(archive_sha256=ARCHIVE_SHA256,census=census,collisions=collisions,compact_relays=relays,
                          compact_factor_panel=panel,family_calls=nfamily,path_rows=size,
                          uncompressed_sha256=digest.hexdigest()), indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
