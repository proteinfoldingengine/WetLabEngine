"""Rebuild the historical event universe and compare joint projections of reachable states."""
import hashlib
import itertools
import json
import lzma
import sys
from collections import Counter
from functools import cache
from pathlib import Path


def unite(items):
    total = 0
    for x in items:
        total |= x
    return total


def shapes():
    def tree(p, v):
        return tuple(sorted(tree(p, w) for w in range(1,len(p)) if p[w] == v))
    for n in range(1, 6):
        reps = {}
        for edges in itertools.product(*(range(i) for i in range(1, n))):
            p = (-1,) + edges
            reps.setdefault(tree(p, 0), p)
        yield from reps.values()


def check(p):
    full = (1 << len(p)) - 1
    children = [sum(1 << j for j in range(1,len(p)) if p[j] == x) for x in range(len(p))]
    subtree = children[:]
    for i in reversed(range(len(p))):
        subtree[i] |= 1 << i
        if i:
            subtree[p[i]] |= subtree[i]
    views = [mask for mask in range(1,full+1,2)
             if all(not mask >> i & 1 or mask >> p[i] & 1 for i in range(1,len(p)))]

    @cache
    def successors(s):
        out = []
        for i, v in enumerate(s):
            for x in range(1, len(p)):
                b = 1 << x
                if v & b and not v & children[x]:
                    t = s[:i] + (v ^ b,) + s[i+1:]
                    if unite(t) == full:
                        out.append((i, x, t))
        return out

    @cache
    def reachable(s):
        out = {s}
        for _, _, t in successors(s):
            out.update(reachable(t))
        return frozenset(out)

    @cache
    def project(s, members):
        return frozenset(tuple(t[i] for i in members) for t in reachable(s))

    @cache
    def profile(s):
        sizes = {unite(combo): size for size in reversed(range(len(s)+1))
                 for combo in itertools.combinations(s,size)}
        return tuple(min(size for v, size in sizes.items() if v & c == c) for c in children)

    counts = Counter()
    reached = set()
    records = []
    for k in range(1,min(4,len(views))+1):
        for s in itertools.combinations(views,k):
            if unite(s) != full:
                continue
            if len(p) <= 4:
                reached.update(reachable(s))
            for i, x, t in successors(s):
                bit = 1 << x
                others = sum(1 << j for j in range(k) if j != i and s[j] & bit)
                old, new = profile(s), profile(t)
                cells = []
                for g in range(1 << k):
                    if g >> i & 1:
                        continue
                    ext = unite(s[j] for j in range(k) if not g >> j & 1)
                    ext_after = unite(t[j] for j in range(k) if not g >> j & 1)
                    old_possible = ext & subtree[x] == subtree[x]
                    new_possible = ext_after & subtree[x] == subtree[x]
                    changed = not children[x] and g & others == others
                    assert (old_possible != new_possible) == bool(changed)
                    cells.append([g, int(old_possible), int(new_possible)])
                records.append([p,s,i,x,new[p[x]]-old[p[x]],max(1,*new)-max(1,*old),cells])
    # Traverse every interleaving, starting again from every reachable state, including
    # repeated view rows. Compare entire sets of projected endpoints for every event/group.
    for s in reached:
        for i, x, t in successors(s):
            bit = 1 << x
            other_holders = {j for j in range(len(s)) if j != i and s[j] & bit}
            for g in range(1 << len(s)):
                if g >> i & 1:
                    continue
                members = tuple(j for j in range(len(s)) if g >> j & 1)
                old, new = project(s, members), project(t, members)
                filtered = frozenset(row for row in old if any(mask & bit for mask in row))
                contains = other_holders.issubset(members)
                expected = filtered if contains else old
                assert new == expected
                assert (old != new) == (not children[x] and contains)
                counts["event_group_projections"] += 1
                counts["projected_endpoints_before"] += len(old)
    counts["reachable_indexed_states"] = len(reached)
    return records, counts


def main(path):
    all_rows = []
    counts = Counter()
    for p in shapes():
        rows, sizes = check(p)
        all_rows.extend(rows)
        counts.update(sizes)
    def encode(rows):
        return (json.dumps(rows,separators=(",",":"))+"\n").encode()
    all_rows.sort()
    raw = lzma.decompress(path.read_bytes())
    assert encode(all_rows) == raw, "Submitted certificate differs from exact regeneration"
    sample = next(row for row in all_rows if sum(b != a for _,b,a in row[-1]) == 1
                  and any(g.bit_count() == 2 and b != a for g,b,a in row[-1]))
    tampered = json.loads(encode([sample]))[0]
    loss = next(cell for cell in tampered[-1] if cell[1] != cell[2])
    loss[0] = 1 << sample[2]  # wrong chart, with the same number of reported changes
    pos = all_rows.index(sample)
    for name, changed in (("omission",all_rows[:-1]), ("duplicate",all_rows+[all_rows[-1]]),
                          ("substitution",all_rows[:1]*2+all_rows[2:]),
                          ("wrong group",all_rows[:pos]+[tampered]+all_rows[pos+1:])):
        assert encode(changed) != raw, name
    return dict(events=len(all_rows), record_sha256=hashlib.sha256(raw).hexdigest(),
                globally_enumerated_through_four_sites=dict(counts),
                rejecting_controls=["omission","duplicate","substitution","wrong group"])


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1])), sort_keys=True, indent=2))
