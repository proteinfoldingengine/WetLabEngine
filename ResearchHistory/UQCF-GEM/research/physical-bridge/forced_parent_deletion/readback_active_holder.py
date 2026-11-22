"""Additional archived readback of local degree transitions and the child-call boundary."""
import gzip
import hashlib
import itertools
import json
import sys
from collections import Counter

from check_active_holder_write import ARCHIVE, DEMOS, SOURCES, STAR, historical, leaves, own_changes


def main():
    for rel, identity in SOURCES.items():
        raw = (DEMOS / rel).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == identity
    sys.path.insert(0, str(DEMOS / STAR))
    producer = historical(STAR + "producer.py", "star_during_readback")
    records = json.loads(gzip.decompress((DEMOS / ARCHIVE).read_bytes()))["records"]
    indexed = {tuple(r["start"]): r for r in records if r["identity"][:2] == ["R", 3]}
    traces = {2: Counter(), 3: Counter()}
    # Exhaust the motif with receiver in the first palette position, R=0.
    for source, third in ((1, 2), (2, 1)):
        for all_three, pair, solo_s, solo_t in itertools.permutations((1, 2, 3, 4)):
            masks = [0, 0, 0]
            masks[0] = 1 | (1 << all_three) | (1 << pair)
            masks[source] = masks[0] | (1 << solo_s)
            masks[third] = 1 | (1 << all_three) | (1 << solo_t)
            for site, target, sign in ((all_three, 2, 1), (pair, 3, -1)):
                edited = masks[:]
                edited[source] ^= 1 << site
                row = indexed[tuple(edited)]
                assert row["q"] == [target]
                counts = tuple(leaves(m) for _, m in own_changes(row["path"], 0))
                exits = [v-u for u, v in itertools.pairwise(counts) if u == 3]
                assert exits and set(exits) == {sign}
                traces[target][counts] += 1
    assert traces[2] == {(2, 3, 4, 3): 48}
    assert traces[3] == {(2, 3, 2): 8, (2, 3, 2, 3, 2): 40}
    calls = {}
    for idx in (1782, 2466):
        row = records[idx]
        original = producer.normalize
        leaf_calls = []

        def observed(state, tree, k, q, *args, **kwargs):
            result = original(state, tree, k, q, *args, **kwargs)
            if tree == ():
                leaf_calls.append({"raw": list(state), "k": k, "q": q, "returned": result})
            return result

        producer.normalize = observed
        try:
            replay = observed(row["start"], producer.Q, 3, row["q"])
        finally:
            producer.normalize = original
        assert replay == row["path"] and len(leaf_calls) == 8
        before, after = [producer.coordinate(replay[i], [1, 2, 3, 4]) for i in (3, 4)]
        assert (before, after) == ((2, 1) if idx == 1782 else (2, 2))
        slot = {"raw": [1], "k": 1, "q": [], "returned": [[1]]}
        assert leaf_calls[2] == leaf_calls[6] == slot
        end_label = [i for i, mask in enumerate(replay[-1]) if mask & (1 << 3)]
        assert end_label == ([0] if idx == 1782 else [1])
        calls[str(idx)] = {"root_cover_before_after_write": [before, after],
                           "caller_end_labels_at_v3": end_label,
                           "v3_callee_initial": leaf_calls[2], "v3_callee_final": leaf_calls[6]}
    print(json.dumps({"first_palette_receiver_degree_histories": {
        str(t): [{"degrees": c, "number": n} for c, n in sorted(count.items())]
        for t, count in traces.items()}, "caller_and_child": calls}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
