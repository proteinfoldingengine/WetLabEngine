"""Test the rank-two preparation law and its use by the v16.51 receiver writer."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


PINS = {
    "../v16.50-recursive-binary-composition/producer.py": "720d1bb933b9172d4359c991e9c18c479f1ee5d061e792211b343b80d1604e21",
    "producer.py": "84078ff2bae228dbb3a5df553f238bf42622f7a2d05f6db51555000956278fd5",
    "verifier.py": "10c7887e00982d38d4a6f269799648e0d194d74232b2e38e324a7f53aeb1bdb2",
    "coverage.py": "af32c777264d094f044727d581fafe90d37b2888f69e68e42ad9499b18244c67",
}
ARCHIVE_SHA256 = "91aac71f6e786af4a3876ee9a7ec09d78b4bbe0906eb5461e08d9be1318b93f9"


def supports(state, vertices):
    return [{x for x, mask in enumerate(state) if mask & (1 << v)} for v in vertices]


def support_table(state, vertices):
    return [sorted(row) for row in supports(state, vertices)]


def signature(rows, palette):
    """Compute all three exclusive pair memberships from the compact rows."""
    _, middle, last = rows
    both01, both02, both12 = palette - last, last - middle, last & middle
    return [both01 | both02, both01 | both12, both02 | both12]


def first_overlap(rows):
    for i, j in combinations(range(3), 2):
        common = rows[i] & rows[j]
        if common:
            return [i, j], min(common)
    raise ValueError("Expected a shared label at rank two")


def census_masks():
    totals = []
    for k in range(1, 6):
        all_labels = (1 << k) - 1
        count = 0
        for a, b, c in product(range(1, all_labels+1), repeat=3):
            if a & b & c or not ((a & b) | (a & c) | (b & c)):
                continue
            rows = [a, b, c]
            for i in range(3):
                for x in range(k):
                    tentative = rows[:]
                    tentative[i] |= 1 << x
                    if not (tentative[0] & tentative[1] & tentative[2]):
                        rows = tentative
            ab, ac, bc = all_labels ^ c, c & (all_labels ^ b), b & c
            assert rows == [ab | ac, ab | bc, ac | bc]
            count += 1
        totals.append(count)
    return totals


def replay(row, producer, verifier):
    spec, start = row["spec"], row["start"]
    tree, k, q = producer.TREES[spec["tree"]], spec["k"], spec["q"]
    trace = []
    path = producer.normalize(start, tree, k, q, trace=trace)
    assert path == row["path"] and row["failure"] is None
    assert start == producer.initial(tree, k, q, spec["permutation"], spec["mode"])
    verifier.path_check(tree, k, q, path, start, verifier.model(tree, q, k)[2])
    cut = max(ev["end"] for ev in trace if ev["kind"] == "child_normalization")
    return (trace[0]["pair"], trace[0]["label"]), cut


def capture_control(initial, tree, k, q, producer, verifier):
    trace = []
    path = producer.normalize(initial, tree, k, q, trace=trace)
    peaks = verifier.path_check(tree, k, q, path, initial, verifier.model(tree, q, k)[2])
    cut = max(ev["end"] for ev in trace if ev["kind"] == "child_normalization")
    return {"start": initial, "path": path, "trace": trace, "peaks": peaks,
            "handoff_frame": cut, "receiver_parent_and_leaves_at_handoff": support_table(path[cut], [4, 6, 7, 8])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    demo = args.demo.resolve()
    for name, pin in PINS.items():
        assert sha256((demo / name).read_bytes()).hexdigest() == pin, name
    sys.path.insert(0, str(demo))
    import producer
    import verifier

    archive = (args.certificate or demo/"evidence/science/scientific/CERTIFICATE.json.gz").read_bytes()
    assert sha256(archive).hexdigest() == ARCHIVE_SHA256
    raw = gzip.decompress(archive)
    regenerated = producer.produce()
    assert (json.dumps(regenerated, sort_keys=True, separators=(",", ":"))+"\n").encode() == raw
    cases = json.loads(raw)["cases"]
    counts = Counter()
    witnesses = []
    isolated = []
    for i in range(0, len(cases), 2):
        compact, inflated = cases[i:i+2]
        spec, second = compact["spec"], inflated["spec"]
        assert spec["mode"] == "compact" and second == dict(spec, mode="interface_and_binary_inflated")
        if spec["q"][0] != 2:
            continue
        counts["rank_two_pairs"] += 1
        tree = producer.TREES[spec["tree"]]
        nodes = producer.layout(tree)
        roots = nodes[0]
        k = spec["k"]
        initial, after = compact["start"], inflated["start"]
        projected = signature(supports(initial, roots), set(range(k)))
        assert projected == supports(after, roots)
        old, old_cut = replay(compact, producer, verifier)
        new, new_cut = replay(inflated, producer, verifier)
        assert first_overlap(projected) == new
        if new == old:
            continue
        counts["anchor_changes"] += 1
        changed_bits = [(v, x) for x, (l, r) in enumerate(zip(initial, after))
                        for v in range(len(nodes)) if (l ^ r) & (1 << v)]
        assert all(after[x] & (1 << v) for v, x in changed_bits)
        for d, child in enumerate(roots):
            region = producer.vertices(nodes, child)
            if supports(initial, region) != supports(after, region):
                continue
            counts["unchanged_receiver_subtrees_with_anchor_change"] += 1
            leaves = [v for v in region if not nodes[v]]
            left, right = compact["path"][old_cut], inflated["path"][new_cut]
            if supports(left, leaves) == supports(right, leaves):
                continue
            counts["different_leaf_records_at_handoff"] += 1
            x = new[1]
            acquired = [v for v in leaves if not (initial[x] | left[x]) & (1 << v) and right[x] & (1 << v)]
            if not acquired:
                continue
            counts["new_anchor_at_new_named_leaf"] += 1
            counts["one_bit_examples"] += int(len(changed_bits) == 1)
            counts["one_bit_pair_switches"] += int(len(changed_bits) == 1 and old[0] != new[0])
            witnesses.append({"case_indices": [i, i+1], "edits_to_initial": changed_bits,
                              "receiver_node": child, "receiving_leaves": acquired, "anchor_before": old,
                              "anchor_after": new, "handoff_frames": [old_cut, new_cut]})
            assert compact["path"][-1] == inflated["path"][-1]
            if len(compact["path"]) != 1:
                continue
            proper = sum(1 << v for v in region[1:])
            for frame, state in enumerate(inflated["path"][new_cut:], new_cut):
                if any((a ^ b) & ~proper for a, b in zip(initial, state)):
                    continue
                if not any(state[x] & (1 << v) for v in acquired):
                    continue
                if verifier.profile_check(tree, k, state) != spec["q"]:
                    continue
                fresh = producer.normalize(state, tree, k, spec["q"])
                verifier.path_check(tree, k, spec["q"], fresh, state, initial)
                assert len(fresh) > 1
                isolated.append({"case_indices": [i, i+1], "frame": frame, "receiver_node": child,
                                 "restart_edits": len(fresh)-1, "restart_matches_archived_suffix": fresh == inflated["path"][frame:]})

    base, active = cases[2208:2210]
    s, k, q = base["start"], base["spec"]["k"], base["spec"]["q"]
    tree = producer.TREES[base["spec"]["tree"]]
    roots = producer.layout(tree)[0]
    candidates = []
    for v, x in product(roots, range(k)):
        if s[x] & (1 << v):
            continue
        probe = s[:]
        probe[x] |= 1 << v
        if verifier.profile_check(tree, k, probe) == q:
            candidates.append((v, x))
    assert candidates == [(1, 3), (9, 3)]
    alt = s[:]
    alt[3] |= 1 << 9
    primary = {}
    for tag, initial in (("compact_2208", s), ("inflated_2209", active["start"]), ("other_eligible_site", alt)):
        primary[tag] = capture_control(initial, tree, k, q, producer, verifier)
    baseline, actual, other = primary.values()
    assert baseline["path"] == base["path"] and actual["path"] == active["path"]
    assert other["path"] == [alt, s]
    assert supports(s, range(4, 9)) == supports(actual["start"], range(4, 9)) == supports(alt, range(4, 9))
    assert actual["start"][3] ^ s[3] == 1 << 1 and s[:3] == actual["start"][:3]
    assert baseline["receiver_parent_and_leaves_at_handoff"] == other["receiver_parent_and_leaves_at_handoff"] == [[2,3],[2],[2],[3]]
    assert actual["receiver_parent_and_leaves_at_handoff"] == [[2,3],[3],[3],[2]]
    assert actual["path"][-1] == other["path"][-1] == baseline["path"][-1] == s
    assert [row["frame"] for row in isolated if row["case_indices"] == [2208, 2209]] == [21]
    isolated_state = actual["path"][21]
    assert support_table(isolated_state, [4,6,7,8]) == [[2,3],[3],[3],[2]]
    fresh = capture_control(isolated_state, tree, k, q, producer, verifier)
    assert len(fresh["path"]) == 9 and all(supports(u, [0,1,2,3,4,9,10,11,12,13,14,15]) ==
                                            supports(s, [0,1,2,3,4,9,10,11,12,13,14,15]) for u in fresh["path"])

    # Vary sibling precedence for preparation and selection together, interpret the result
    # in the original node identities. This checks reliance on order without relabeling leaves.
    orders = []
    indices = [0, 1, 2]
    initial_rows = supports(s, roots)
    for perm in permutations(indices):
        ordered = [initial_rows[j] for j in perm]
        post = signature(ordered, set(range(k)))
        added = [(roots[perm[j]], x) for j in indices for x in sorted(post[j] - ordered[j])]
        pair, label = first_overlap(post)
        orders.append({"row_order": [roots[j] for j in perm], "added": added,
                       "chosen_nodes": [roots[perm[j]] for j in pair], "label": label})
    print(json.dumps({"archive_sha256": ARCHIVE_SHA256, "archive_cases": len(cases),
                      "rank_two_counts": dict(counts), "root_triples_checked_by_palette_size_1_to_5": census_masks(),
                      "positive_receiver_comparisons": witnesses, "witness_spec": base["spec"],
                      "isolated_receiver_checkpoints_with_stationary_compact_control": isolated,
                      "restart_from_frame_21": fresh,
                      "eligible_additions": candidates, "sibling_order_controls_on_parent_rule": orders,
                      "complete_witness_paths": primary}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
