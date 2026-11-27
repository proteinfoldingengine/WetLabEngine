"""Independent bit-mask enumeration, projected global paths, and record mutation checks."""
import hashlib
import itertools
import json
import lzma
import sys
from collections import Counter
from functools import cache
from pathlib import Path


def shapes():
    def form(p, v):
        return tuple(sorted(form(p, w) for w in range(1, len(p)) if p[w] == v))
    for n in range(1, 6):
        trees = {}
        for edges in itertools.product(*(range(i) for i in range(1, n))):
            p = (-1,) + edges
            trees.setdefault(form(p, 0), p)
        yield from trees.values()


def universe(p):
    children = [sum(1 << j for j in range(1, len(p)) if p[j] == i) for i in range(len(p))]
    full = (1 << len(p)) - 1
    views = [mask for mask in range(1, full + 1, 2)
             if all(not mask & (1 << i) or mask & (1 << p[i]) for i in range(1, len(p)))]
    starts = (state for k in range(1, min(4, len(views)) + 1)
              for state in itertools.combinations(views, k) if union(state) == full)
    return children, starts


def union(masks):
    result = 0
    for mask in masks:
        result |= mask
    return result


def check_shape(p):
    kids, starts = universe(p)
    full = (1 << len(p)) - 1
    counts = Counter()

    @cache
    def edits(state):
        out = []
        for i, mask in enumerate(state):
            for x in range(1, len(p)):
                bit = 1 << x
                if not mask & bit or mask & kids[x]:
                    continue
                nxt = state[:i] + (mask ^ bit,) + state[i+1:]
                if union(nxt) == full:
                    out.append((i, x, nxt))
        return out

    @cache
    def projection(state, r):
        # Allow every move at every chart; erase each other chart's letters.
        result = {()}
        for actor, x, nxt in edits(state):
            prefix = (x,) if actor == r else ()
            result.update(prefix + tail for tail in projection(nxt, r))
        return frozenset(result)

    @cache
    def own(mask, exterior):
        words = {()}
        for x in range(1, len(p)):
            bit = 1 << x
            if mask & bit and not mask & kids[x] and (mask ^ bit) | exterior == full:
                words.update((x,) + tail for tail in own(mask ^ bit, exterior))
        return frozenset(words)

    @cache
    def profile(state):
        return tuple(min((k for k in range(len(state)+1)
                          if any(union(sub) & children == children
                                 for sub in itertools.combinations(state, k))))
                     for children in kids)

    rows = []
    projection_checks = set()

    def compare_projections(state, r):
        if len(p) > 4 or (state, r) in projection_checks:
            return
        projection_checks.add((state, r))
        assert own(state[r], union(state[:r] + state[r+1:])) == projection(state, r)
        for _, _, nxt in edits(state):
            compare_projections(nxt, r)

    for state in starts:
        before = profile(state)
        for r in range(len(state)):
            compare_projections(state, r)
        for actor, x, nxt in edits(state):
            holders = [i for i, mask in enumerate(state) if mask & (1 << x)]
            affected = [i for i in holders if i != actor] if len(holders) == 2 and not kids[x] else []
            after = profile(nxt)
            t = after[p[x]] - before[p[x]]
            dh = max(1, *after) - max(1, *before)
            counts["trigger_as_change_disagreements"] += bool(t) != bool(affected)
            counts["pair_of_holders_alone_false_positives"] += len(holders) == 2 and bool(kids[x])
            remote = []
            for r in range(len(state)):
                if actor == r:
                    continue
                words = own(state[r], union(state[:r] + state[r+1:]))
                expected_lost = {word for word in words if x in word and r in affected}
                actual = own(nxt[r], union(nxt[:r] + nxt[r+1:]))
                assert actual == words - expected_lost
                assert bool(expected_lost) == (r in affected)
                remote.append([r, len(words), len(actual), sorted(expected_lost)])
            rows.append([p, state, actor, x, t, dh, remote])
    counts["projected_state_chart_pairs"] += len(projection_checks)
    counts["global_states_in_projection_check"] += len({s for s, _ in projection_checks})
    return rows, counts


def verify(packed_path):
    rows = []
    counts = Counter()
    for p in shapes():
        data, checked = check_shape(p)
        rows.extend(data)
        counts.update(checked)
    canonical = (json.dumps(sorted(rows), separators=(",", ":")) + "\n").encode()
    supplied = lzma.decompress(packed_path.read_bytes())
    if supplied != canonical:
        raise ValueError("Event identities, numerical results or complete lost words differ")
    records = json.loads(canonical)
    keys = [json.dumps(row[:4]) for row in records]
    assert len(set(keys)) == len(records)
    # Reject corruption even when length, aggregate counts or identity keys are preserved.
    def encode(batch):
        return (json.dumps(batch, separators=(",", ":")) + "\n").encode()
    i = next(i for i, row in enumerate(records) if any(r[-1] for r in row[-1]))
    cell = json.loads(json.dumps(records[i]))
    remote = next(r for r in cell[-1] if r[-1])
    remote[0] = cell[2]  # substitute actor identity for affected nonactor
    assert all(encode(m) != canonical for m in (
        records[:-1], records + [records[-1]], [records[1], *records[1:]],
        records[:i] + [cell] + records[i+1:]))
    bad_move = json.loads(json.dumps(records[i]))
    bad_move[3] = 0
    assert json.dumps(bad_move[:4]) not in set(keys)
    assert counts["trigger_as_change_disagreements"] > 0
    assert counts["pair_of_holders_alone_false_positives"] > 0
    return dict(events=len(rows), record_sha256=hashlib.sha256(canonical).hexdigest(),
                controls=["missing", "duplicated", "substituted", "wrong affected chart",
                          "illegal root cut", "trigger as permission", "two holders at internal site"],
                **counts)


if __name__ == "__main__":
    print(json.dumps(verify(Path(sys.argv[1])), sort_keys=True, indent=2))
