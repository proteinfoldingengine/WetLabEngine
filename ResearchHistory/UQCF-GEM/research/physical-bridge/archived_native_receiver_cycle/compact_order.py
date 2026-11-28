"""Recover admissible execution orders from a v16.51 compact incidence state."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
from hashlib import sha256
from itertools import groupby, permutations, product
import json
import lzma
from pathlib import Path
import sys
from unittest.mock import patch

from ternary_preparation import ARCHIVE_SHA256, PINS, support_table

HERE = Path(__file__).resolve().parent


def layouts(children, node):
    """Yield ordered trees and their maps from traversal indices back to physical sites."""
    if not children[node]:
        yield (), (node,)
        return
    for order in permutations(children[node]):
        for subtrees in product(*(layouts(children, child) for child in order)):
            yield tuple(t for t, sites in subtrees), (node,) + tuple(v for t, sites in subtrees for v in sites)


def represented(state, sites, labels):
    return [sum(1 << j for j, physical in enumerate(sites) if state[x] & (1 << physical)) for x in labels]


def physical(state, sites, labels):
    result = [0] * len(labels)
    for j, x in enumerate(labels):
        result[x] = sum(1 << v for i, v in enumerate(sites) if state[j] & (1 << i))
    return result


def label_orders(canonical, columns):
    """Solve the bijection by matching the complete incidence column of each label."""
    if sorted(canonical) != sorted(columns):
        return
    wanted, available = defaultdict(list), defaultdict(list)
    for i, (left, right) in enumerate(zip(canonical, columns)):
        wanted[left].append(i)
        available[right].append(i)
    for groups in product(*(permutations(group) for group in available.values())):
        order = [None] * len(columns)
        for key, matching in zip(available, groups):
            for i, label in zip(wanted[key], matching):
                order[i] = label
        yield tuple(order)


def edits(before, after, sites):
    return [(v, x) for x, (a, b) in enumerate(zip(before, after)) for v in sites if (a ^ b) & (1 << v)]


def receiver_from_compact(state, nodes):
    """Closed-form prediction on the three-label witness family; no ordered comparisons."""
    rows = {v: set(x for x, mask in enumerate(state) if mask & (1 << v)) for v in range(len(nodes))}
    single, = (v for v in nodes[0] if len(rows[v]) == 1)
    peer, = (v for v in nodes[0] if rows[v].isdisjoint(rows[single]))
    last, = (v for v in nodes[0] if v not in (single, peer))
    a, = rows[single]
    b, = rows[peer] & rows[last]
    c, = rows[peer] - rows[last]
    narrow, = (v for v in nodes[last] if len(rows[v]) == 1)
    assert rows[last] == {a,b} and rows[narrow] in ({a}, {b})
    forward = rows[narrow] == {a}
    order = (single, peer, last) if forward else (last, peer, single)
    leaves = [v for child in nodes[peer] for v in (nodes[child] or [child])]
    changed = {b:c, c:b} if forward else {b:b, c:c}
    holdings = {}
    for v in leaves:
        old, = rows[v]
        holdings[v] = changed[old]
    return order, c, (c if forward else b), holdings


def variable_leaf_steps(paths, nodes):
    """Locate intermediate states between two commuting edits of sibling leaves."""
    reference = paths[0]
    alternatives = []
    for frame, states in enumerate(zip(*paths, strict=True)):
        choices = sorted({tuple(state) for state in states})
        if len(choices) == 1:
            continue
        assert len(choices) == 2 and all(path[frame-1] == reference[frame-1] and
                                         path[frame+1] == reference[frame+1] for path in paths)
        before, after = reference[frame-1], reference[frame+1]
        (u, x), (w, y) = edits(before, after, range(len(nodes)))
        assert x == y and not nodes[u] and not nodes[w] and any(set(ch) == {u,w} for ch in nodes)
        assert bool(after[x] & (1 << u)) == bool(after[y] & (1 << w))
        assert {tuple(edits(before, choice, range(len(nodes)))) for choice in choices} == {((u,x),), ((w,x),)}
        alternatives.append((frame, choices))
    return alternatives


def observed_preparation(producer, ordered, qs, label, region):
    """Observe just the selected incidences inside the original initializer."""
    local_masks = []
    def observe(frame, event, arg):
        if frame.f_code is not producer.initial.__code__:
            return None
        if "state" in frame.f_locals:
            local_masks.append(frame.f_locals["state"][label] & region)
        return observe
    old_trace = sys.gettrace()
    try:
        sys.settrace(observe)
        start = producer.initial(ordered, 3, list(qs), "identity", "interface_and_binary_inflated")
    finally:
        sys.settrace(old_trace)
    return start, [key for key, _ in groupby(local_masks)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--write-records", action="store_true")
    args = parser.parse_args()
    demo = args.demo.resolve()
    for file, pin in PINS.items():
        assert sha256((demo / file).read_bytes()).hexdigest() == pin
    sys.path.insert(0, str(demo))
    import producer as p
    import verifier as v

    archive = (args.certificate or demo/"evidence/science/scientific/CERTIFICATE.json.gz").read_bytes()
    assert sha256(archive).hexdigest() == ARCHIVE_SHA256
    cases = json.loads(gzip.decompress(archive))["cases"]

    @lru_cache(None)
    def orderings(tree):
        return tuple(layouts(p.layout(tree), 0))

    @lru_cache(None)
    def standard(tree, k, ranks):
        canonical = p.canonical(tree, k, list(ranks))
        assert canonical == v.model(tree, list(ranks), k)[2]
        return canonical

    def compatible(seed, tree):
        k = len(seed)
        nodes = p.layout(tree)
        ranks = v.profile_check(tree, k, seed)
        local = dict(zip((i for i, ch in enumerate(nodes) if ch), ranks))
        for ordered, sites in orderings(tree):
            qs = tuple(local[x] for x in sites if x in local)
            target = standard(ordered, k, qs)
            for labels in label_orders(target, represented(seed, sites, range(k))):
                yield ordered, sites, qs, labels

    def normalized(start, tree, ranks):
        trace = []
        path = p.normalize(start, tree, len(start), list(ranks), trace=trace)
        v.path_check(tree, len(start), list(ranks), path, start, standard(tree, len(start), ranks))
        cut = max(e["end"] for e in trace if e["kind"] == "child_normalization")
        return path, trace[0], cut

    @lru_cache(None)
    def stock(ordered, k, qs):
        compact = p.initial(ordered, k, list(qs), "identity", "compact")
        active = p.initial(ordered, k, list(qs), "identity", "interface_and_binary_inflated")
        return normalized(compact, ordered, qs), normalized(active, ordered, qs)

    def compare(seed, tree, presentation):
        ordered, sites, qs, labels = presentation
        quiet, active = stock(ordered, len(labels), qs)
        root_order = [sites[i] for i in p.layout(ordered)[0]]
        fmt = lambda path: [physical(f, sites, labels) for f in path]
        quiet_path, active_path = fmt(quiet[0]), fmt(active[0])
        assert quiet_path[0] == seed == quiet_path[-1] == active_path[-1]
        selected = ([root_order[j] for j in active[1]["pair"]], labels[active[1]["label"]])
        return root_order, quiet_path, active_path, active[2], selected

    count, digest = 0, sha256()
    panel = []
    path_file = HERE/"compact_order_paths.jsonl.xz"
    with lzma.open(path_file, "wb" if args.write_records else "rb") as stream:
        def record(data):
            nonlocal count
            line = (json.dumps(data, sort_keys=True, separators=(",", ":"))+"\n").encode()
            if args.write_records:
                stream.write(line)
            else:
                assert stream.readline() == line
            digest.update(line)
            count += 1

        # Search all compact identity-palette rank-two seeds in the original corpus.
        # A site qualifies only when the entire receiver is untouched in the paired
        # compact run and its start is identical in both arms.
        for i in range(0, len(cases), 2):
            base, active = cases[i:i+2]
            spec, seed = base["spec"], base["start"]
            if spec["q"][0] != 2 or spec["permutation"] != "identity":
                continue
            assert spec["mode"] == "compact" and active["spec"] == dict(spec, mode="interface_and_binary_inflated")
            tree = p.TREES[spec["tree"]]
            nodes = p.layout(tree)
            assert v.profile_check(tree, spec["k"], seed) == spec["q"]
            usual = stock(tree, len(seed), tuple(spec["q"]))
            assert usual[0][0] == base["path"] and usual[1][0] == active["path"]
            intersection = None
            orders = set()
            num = 0
            for pr in compatible(seed, tree):
                order, quiet_path, path, cut, chosen = compare(seed, tree, pr)
                orders.add(tuple(order))
                num += 1
                isolated = set()
                for child in nodes[0]:
                    region = p.vertices(nodes, child)
                    mask = sum(1 << vtx for vtx in region)
                    if any((a ^ b) & mask for state in [path[0], *quiet_path] for a, b in zip(seed, state)):
                        continue
                    if seed == path[0]:
                        continue
                    proper = mask ^ (1 << child)
                    for state in path[cut:]:
                        if state != seed and not any((a ^ b) & ~proper for a, b in zip(seed, state)):
                            if v.profile_check(tree, len(seed), state) == spec["q"]:
                                isolated.add((child, tuple(state)))
                intersection = isolated if intersection is None else intersection & isolated
                if i in (912, 948, 2208):
                    record(dict(test="archive_order", case=i, sites=pr[1], labels=pr[3], root_order=order,
                                selected=chosen, compact_path=quiet_path, expanded_path=path, cut=cut))
            assert num
            panel.append(dict(case=i, presentations=num, root_orders=sorted(orders), common_records=sorted(intersection)))

        positive = [row["case"] for row in panel if row["common_records"]]
        assert len(panel) == 144 and positive == [912, 948]
        controls = {}
        for i, narrow in ((912, (10,11,12)), (948, (13,14,15))):
            base, active = cases[i:i+2]
            seed, q, tree = base["start"], base["spec"]["q"], p.U
            nodes = p.layout(tree)
            top = nodes[0]
            leaves = (6,7,8)
            changed = edits(seed, active["start"], range(len(nodes)))
            assert len(changed) == 6
            original = tuple(compatible(seed, tree))
            altered = seed[:]
            mask = sum(1 << vtx for vtx in narrow)
            assert altered[0] & mask == mask and not altered[1] & mask
            altered[0] ^= mask
            altered[1] ^= mask
            reversed_orders = tuple(compatible(altered, tree))
            assert len(original) == len(reversed_orders) == 16
            for observed in (seed, altered):
                expected_order, expected_gain, expected_anchor, expected_leaves = receiver_from_compact(observed, nodes)
                # Renumber the same unordered input, independently of which serialized
                # traversals could have generated its holdings.
                for tree_order, sites in orderings(tree):
                    renamed_nodes = p.layout(tree_order)
                    for labels in permutations(range(len(seed))):
                        result = receiver_from_compact(represented(observed, sites, labels), renamed_nodes)
                        order, gain, anchor, holdings = result
                        assert tuple(sites[u] for u in order) == expected_order
                        assert (labels[gain], labels[anchor]) == (expected_gain, expected_anchor)
                        assert {sites[u]: labels[x] for u,x in holdings.items()} == expected_leaves
            summaries = Counter()
            physical_paths = []
            for pr in original:
                ordered, sites, qs, labels = pr
                order, quiet, path, cut, anchor = compare(seed, tree, pr)
                assert order == [1,4,9] and labels == (0,1,2) and anchor == ([1,4], 2)
                assert edits(seed, path[0], top) == [(1,2)]
                assert len(quiet) == 7 and len(path) == 37 and cut == 14
                assert support_table(path[20], leaves) == [[2],[2],[1]]
                assert {vtx for vtx, x in edits(seed, path[20], range(len(nodes)))} == {5,6,7,8}
                assert path[20] == active["path"][20]
                physical_paths.append(path)
                region = sum(1 << u for u in narrow)
                encoded_region = sum(1 << j for j,u in enumerate(sites) if u in narrow)
                seen_start, growth = observed_preparation(p, ordered, qs, labels.index(1), encoded_region)
                assert physical(seen_start, sites, labels) == path[0]
                added = [sum(1 << u for j,u in enumerate(sites) if raw & (1 << j)) for raw in growth]
                assert [x.bit_count() for x in added] == [0,1,2,3] and added[1] == 1 << narrow[0]
                passive = [x for x,_ in groupby(f[1] & region for f in quiet)]
                prepared = [x for x,_ in groupby(added + [f[1] & region for f in path])]
                assert passive == prepared and [x.bit_count() for x in passive] == [0,1,2,3,2,1,0]
                assert passive[-2] == 1 << narrow[0]
                record(dict(test="local_transfer_both_modes", case=i, sites=sites, labels=labels,
                            local_nodes=narrow, preparation_masks=added, compact_masks=passive,
                            expanded_lifecycle_masks=prepared))
                counts = Counter()
                for bits in product((0,1), repeat=len(changed)):
                    start = seed[:]
                    for bit, (site, label) in zip(bits, changed):
                        if bit:
                            start[label] |= 1 << site
                    try:
                        profile = v.profile_check(tree, len(seed), start)
                    except v.InterfaceNotPreserved:
                        continue
                    if profile != q:
                        continue
                    raw, _, local_cut = normalized(represented(start, sites, labels), ordered, qs)
                    local_path = [physical(f, sites, labels) for f in raw]
                    has_source = bool(start[2] & (1 << 1))
                    expected = [[2],[2],[1]] if has_source else [[1],[1],[2]]
                    assert support_table(local_path[local_cut], leaves) == expected
                    assert (path[20] in local_path) == has_source
                    counts[has_source] += 1
                    record(dict(test="preparation_subset", case=i, bits=bits, sites=sites, labels=labels,
                                source=has_source, cut=local_cut, path=local_path))
                assert counts == {True:20, False:5}

            alternatives = variable_leaf_steps(physical_paths, nodes)
            assert len(alternatives) == 8 and len({tuple(map(tuple,path)) for path in physical_paths}) == 8
            for choices in product(*(options for _, options in alternatives)):
                path = list(active["path"])
                for (frame, _), state in zip(alternatives, choices):
                    path[frame] = list(state)
                v.path_check(tree, len(seed), q, path, active["start"], seed)
                assert path[20] == active["path"][20]
                record(dict(test="independent_leaf_swaps", case=i, path=path))

            # Change the compact memory and the traversal independently. In crossed
            # arms only, replace the canonical seed at the historical initializer's
            # input seam; its expansion and normalization both run unchanged.
            for side, seed_used in (("original", seed), ("altered", altered)):
                for orient, encodings in (("forward", original), ("reverse", reversed_orders)):
                    for ordered, sites, qs, labels in encodings:
                        encoded = represented(seed_used, sites, labels)
                        if (side == "original") == (orient == "forward"):
                            expanded = p.initial(ordered, len(seed), list(qs), "identity", "interface_and_binary_inflated")
                            assert standard(ordered, len(seed), qs) == encoded
                        else:
                            with patch.object(p, "canonical", return_value=encoded):
                                expanded = p.initial(ordered, len(seed), list(qs), "identity", "interface_and_binary_inflated")
                        moves, selection, boundary = normalized(expanded, ordered, qs)
                        actual = [physical(f, sites, labels) for f in moves]
                        forward = orient == "forward"
                        assert edits(seed_used, actual[0], top) == [(1 if forward else 9, 2)]
                        assert labels[selection["label"]] == (2 if forward else 1)
                        assert support_table(actual[boundary], leaves) == ([[2],[2],[1]] if forward else [[1],[1],[2]])
                        if (side == "original") == forward:
                            inferred, gain, anchor, forecast = receiver_from_compact(seed_used, nodes)
                            assert tuple(sites[vtx] for vtx in p.layout(ordered)[0]) == inferred
                            assert edits(seed_used, actual[0], top) == [(inferred[0], gain)]
                            assert labels[selection["label"]] == anchor
                            assert all(support_table(actual[boundary], [u]) == [[x]] for u,x in forecast.items())
                        if not forward:
                            assert all(support_table(f, range(4,9)) == support_table(seed, range(4,9)) for f in actual)
                        summaries[side+"_"+orient] += 1
                        record(dict(test="memory_order", case=i, seed=side, order=orient, sites=sites, labels=labels,
                                    selected_label=labels[selection["label"]], cut=boundary, path=actual))
            controls[i] = dict(legal_subsets_per_presentation={"source_present":20,"source_absent":5},
                               crossed_counts=dict(summaries), narrow_sites=narrow,
                               variable_intermediate_frames=[frame for frame, _ in alternatives],
                               verified_interleavings=2**len(alternatives))
        if not args.write_records:
            assert stream.read(1) == b""
    print(json.dumps(dict(certificate_sha256=ARCHIVE_SHA256, panel=panel, controls=controls,
                          full_path_rows=count, uncompressed_sha256=digest.hexdigest()), indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
