"""Exhaust the local projection of every possible peak-clipping choice in the largest stock M9 plan."""
import gzip
from itertools import combinations
from math import comb
import json
from hashlib import sha256

from replay import FIRST, HERE, LINE_PINS

# A history records a leaf tuple only when the receiver changes it.
def bridge(before, after, history):
    current = set(before)
    current.update(after - before)
    for label in sorted(before - after):
        held = list(history[-1])
        if label in held:
            held[held.index(label)] = min(current - set(held))
            history += (tuple(held),)
        current.remove(label)
    assert current == after
    return history


def row_path(initial, target):
    current = initial
    yield current
    for x in sorted(target - initial):
        current = current | {x}
        yield current
    for x in sorted(initial - target):
        current = current - {x}
        yield current


def choices(row):
    return {row, row | {0}} if 1 in row else {row}


def dwell(states, possible):
    # Remote moves can leave this preliminary row constant for any number of frames.
    # Close under every shadow choice at that row before advancing one local edit.
    reached = set(states)
    work = list(reached)
    while work:
        current, hist = work.pop()
        for target in possible:
            child = (target, bridge(current, target, hist))
            if child not in reached:
                reached.add(child)
                work.append(child)
    return reached


def all_histories(initial, target):
    initial_history = (tuple(sorted(initial)[:3]),)
    states = {(initial, initial_history)}
    previous = initial
    ground = initial_history
    for row in row_path(initial, target):
        ground = bridge(previous, row, ground)
        possible = choices(row)
        states = {(next_row, bridge(current, next_row, history))
                  for current, history in states for next_row in possible}
        states = dwell(states, possible)
        previous = row
    assert states == {(target, ground)}


def main():
    lines = gzip.decompress((HERE / "original_m9.jsonl.gz").read_bytes()).splitlines(keepends=True)
    assert tuple(sha256(line).hexdigest() for line in lines) == LINE_PINS
    for line in lines[1:]:
        _, dims, roots, _ = json.loads(line)["identity"]
        k, q, h = (dims[key] for key in ("k", "q", "h"))
        banned = len(roots) * comb(k-h, q)
        candidates = comb(k, q)
        assert banned < candidates
        print(f"h={h}, q={q}: disjoint-cover count at most {banned} of {candidates}")
    archive = json.loads(lines[0])
    _, p, _, ch = archive["identity"]
    assert FIRST == 2393446 and (p["k"], p["q"], p["h"], p["N"]) == (8, 4, 3, 10)
    labels = frozenset(range(8))
    inputs = [frozenset(s) for k in range(3, 9) for s in combinations(labels, k)]
    targets = set(map(frozenset, ch["target"]))
    high = {frozenset(row) for row in combinations(range(3, 8), 3)}
    assert targets == high | {labels, frozenset(range(3))}
    # The actual phase assignment matters for the proof and the unsupplied shadow histories do not.
    parent = archive["facts"]["parent_record"]["facts"]
    perm = [frozenset(ch["target"][i]) for i in parent["target_order"]]
    assert set(perm[10:]) == high and set(perm[:10]) == {labels, frozenset(range(3))}
    assert all(set((0, 3, 4, 5)).intersection(t) for t in targets)
    # A six-cover lower bound would require all 56 excluded triples as rows.
    assert comb(8, 3) > 20
    # If every five-cover containing 0 and 1 failed, its excluded triple
    # would have to be an entire row. Those twenty triples have rank four.
    forced = list(map(set, combinations(range(2, 8), 3)))
    assert len(forced) == 20
    assert next(len(c) for n in range(1, 9) for c in combinations(range(8), n)
                if all(t.intersection(c) for t in forced)) == 4
    for initial in inputs:
        for target in targets:
            all_histories(initial, target)
    print(f"Archive {FIRST}. {len(inputs)} starting supports x {len(targets)} targets = "
          f"{len(inputs)*len(targets)} local cases. All optional 0-at-1 shadows, "
          "including arbitrary stuttering, preserve the ordered leaf-change history.")


if __name__ == "__main__":
    main()
