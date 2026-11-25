"""Reconstruct two-step returns by changing chart coordinates and measuring work."""
from collections import defaultdict


def measured_pairs(parents, rows, squared, work):
    masks = [sum(1 << v for v in row if v) for row in rows]
    levels = defaultdict(int)
    for v in range(1, len(parents)):
        levels[squared[v]] |= 1 << v
    external = [set().union(*(y for k, y in enumerate(rows) if k != i))
                for i in range(len(rows))]
    result = []
    for i, row in enumerate(rows):
        by_change = defaultdict(list)
        children = defaultdict(set)
        for v in row:
            if v:
                children[parents[v]].add(v)
        for v in row:
            if v == 0 or v not in external[i]:
                continue
            new = masks[i] ^ (1 << v)
            differences = [new ^ other for j, other in enumerate(masks) if j != i]
            distances = [sum(w * (d & mask).bit_count() for w, mask in levels.items())
                         for d in differences]
            delta = tuple(d - base for d, base in zip(
                distances, (w for j, w in enumerate(work[i]) if j != i), strict=True))
            for u in by_change[tuple(-x for x in delta)]:
                if not (children.get(v, set()) - {u} or children.get(u, set()) - {v}):
                    result.append((i, min(u, v), max(u, v)))
            by_change[delta].append(v)
    return sorted(result)
