"""Rebuild the first-acquisition population from terminal ownership and check its ledger."""
import argparse
from collections import Counter
from copy import deepcopy
from functools import cache
from itertools import combinations, product
import json
from pathlib import Path

PARENT = (-1, 0, 0, 0, 3, 3, 3, 0, 7, 7)
TIP = (1, 2, 4, 5, 6, 8, 9)
CHARTS = range(3)
PAIRS = tuple(combinations(CHARTS, 2))
CHILDREN = {p: {v for v in range(1, 10) if PARENT[v] == p} for p in (0, 3, 7)}
FINAL = (31, 425, 713)


def require(condition, message):
    if not condition:
        raise ValueError(message)


@cache
def sites(mask):
    return frozenset(v for v in range(10) if mask & (1 << v))


def starting_allocations():
    result = {}
    for labels in product(CHARTS, repeat=len(TIP)):
        x, y, w1, w2, w3, left, right = labels
        if x != y or len({w1, w2, w3}) < 3 or len({x, left, right}) < 3:
            continue
        masks = [1, 1, 1]
        for leaf, chart in zip(TIP, labels):
            v = leaf
            while v > 0:
                masks[chart] |= 1 << v
                v = PARENT[v]
        result[tuple(masks)] = dict(zip(TIP, labels))
    return result


@cache
def valid(masks):
    rows = [sites(mask) for mask in masks]
    return (all(0 in row and all(PARENT[v] in row for v in row if v) for row in rows)
            and len(set.union(set(), *rows)) == 10)


@cache
def profile(masks):
    rows = [sites(mask) for mask in masks]
    return [min(n for n in (1, 2, 3) if any(children <= set.union(set(), *choice)
                for choice in combinations(rows, n))) for children in CHILDREN.values()]


def in_band(counts):
    return sum(abs(a-b) for a, b in zip(counts, (2, 3, 2))) <= 1


def subtotal_vector(fine):
    values = list(fine)
    for site in range(9, 0, -1):
        values[PARENT[site]] += values[site]
    return tuple(values)


def work(masks, subtotal):
    return tuple(sum(subtotal[v] ** 2 for v in sites(masks[i]) ^ sites(masks[j]))
                 for i, j in PAIRS)


def shifted(start, receiver, site):
    return tuple(mask ^ (1 << site) if j == receiver else mask for j, mask in enumerate(start))


def expected_first(owners):
    # The unmodified writer processes W, then S, then the root expansion.
    for rank, leaf in enumerate((4, 5, 6)):
        if owners[leaf] != rank:
            return rank, leaf
    if owners[8] > owners[9]:
        return owners[9], 8
    return min(j for j in CHARTS if j != owners[1]), 1


def verify_worlds(worlds, owners):
    require(len(worlds) == 8, "missing independent grade preparation")
    for bits, (fine, totals) in enumerate(worlds):
        reconstructed = subtotal_vector(fine)
        require(len(fine) == 10 and all(type(v) is int and v > 0 for v in fine) and
                tuple(totals) == reconstructed and (totals[0], totals[3], totals[7]) == (80, 30, 24),
                "subtree totals or positivity")
        for chart in CHARTS:
            (w,) = [v for v in (4, 5, 6) if owners[v] == chart]
            bit = (bits >> chart) & 1
            if owners[1] == chart:
                addresses, expect = (1, 2, w), ((1, 2, 3), (2, 3, 1))
            elif owners[8] == chart:
                addresses, expect = (w, 8), ((4, 5), (5, 4))
            else:
                addresses, expect = (w, 9), ((6, 7), (7, 6))
            require(tuple(fine[v] for v in addresses) == expect[bit], "private-leaf assignment")


def verify_row(row, owners):
    start = tuple(row["start"])
    bare = shifted(start, owners[1], 7)
    edges = {}
    for before in (start, bare):
        for r, v in product(CHARTS, range(1, 10)):
            after = shifted(before, r, v)
            if valid(after):
                edges[before, after] = r, v, 1 if after[r] > before[r] else -1
    worlds = row["worlds"]
    verify_worlds(worlds, owners)
    expected_frontier = [{"state": list(state), "work": list(work(state, worlds[0][1]))}
                         for state in sorted((start, bare))]
    require(row["frontier"] == expected_frontier, "frontier identity")
    require(all(len({work(z, total) for fine, total in worlds}) == 1 for z in (start, bare)),
            "unmatched prior work")
    supplied = row["edges"]
    identities = [(tuple(e["before"]), tuple(e["after"])) for e in supplied]
    require(len(identities) == len(edges) and set(identities) == edges.keys(), "edge coverage")
    for edge, key in zip(supplied, identities):
        a, b = key
        r, v, sign = edges[key]
        require((edge["chart"], edge["site"], edge["sign"]) == (r, v, sign), "edit identity")
        require(edge["profile"] == profile(b) and edge["band"] is in_band(profile(b)), "profile")
        deltas, values = [], []
        for fine, total in worlds:
            before, after = work(a, total), work(b, total)
            deltas.append([y-x for x, y in zip(before, after)])
            if v in TIP:
                require(sign == 1 and owners[v] != r, "first copy")
                values.append(fine[v])
        require(edge["work_deltas"] == deltas and edge["acquired"] == values, "edge numbers")
    path = list(map(tuple, row["original"]))
    require(path[0] == start and path[-1] == FINAL and all(valid(z) and in_band(profile(z)) for z in path),
            "original endpoints or excursion")
    require(all(sum((x ^ y).bit_count() for x, y in zip(a, b)) == 1 for a, b in zip(path, path[1:])),
            "nonprimitive original path")
    r, v = expected_first(owners)
    s = owners[v]
    require(len(path) > 1 and path[1] == shifted(start, r, v), "original first edit")
    # Holding a subtree total is equivalent to knowing that entry from one's own P1.
    # All world-dependent subtotals are at the original holder's terminal leaves.
    has_bit = any((owners[t] == s and t in sites(FINAL[r])) for t in TIP)
    expected = dict(step=1, receiver=r, sender=s, site=v, same_site_at_return=v in sites(FINAL[r]),
                    bit_at_return=has_bit)
    require(row["first"] == expected, "return record")
    return r, v


def collision(rows):
    # D privately holds W leaf 4 and binary leaf 8. B can legally copy either.
    row = next(z for z in rows if z["start"] == [409, 681, 79])
    edges = {e["site"]: e for e in row["edges"] if e["chart"] == 1 and e["before"] == row["start"]}
    a, b = edges[4], edges[8]
    require(a["band"] and b["band"] and a["after"] != b["after"], "collision paths")
    require(a["work_deltas"][0] == b["work_deltas"][1] and a["acquired"][0] == b["acquired"][1],
            "geometry collision")
    return dict(start=row["start"], receiver=1, sender=0, sites=[4, 8], bits=[0, 1],
                grade=a["acquired"][0], delta=a["work_deltas"][0])


def verify(raw):
    populations = starting_allocations()
    starts = [tuple(row["start"]) for row in raw]
    require(len(starts) == len(populations) and set(starts) == populations.keys(), "starting population")
    events = Counter(verify_row(row, populations[start]) for row, start in zip(raw, starts))
    return dict(starts=len(raw), first_moves=[[r, v, n] for (r, v), n in sorted(events.items())],
                geometry_collision=collision(raw))


def rejection_checks(rows):
    base = rows[0]
    owners = starting_allocations()[tuple(base["start"])]
    def reject(action):
        try:
            action()
        except ValueError as exc:
            return str(exc)
        raise AssertionError("corrupt record passed")
    reasons = [reject(lambda: verify(rows[:-1])), reject(lambda: verify([rows[0], *rows[:-1]]))]
    for kind in ("missing", "duplicate", "substituted", "wrong_work", "wrong_return", "wrong_grade"):
        damaged = deepcopy(base)
        edges = damaged["edges"]
        if kind == "missing":
            edges.pop()
        elif kind == "duplicate":
            edges.append(edges[0])
        elif kind == "substituted":
            edges[-1] = edges[0]
        elif kind == "wrong_work":
            edges[0]["work_deltas"][0][0] += 1
        elif kind == "wrong_return":
            damaged["first"]["bit_at_return"] = not damaged["first"]["bit_at_return"]
        else:
            damaged["worlds"][1][0][0] += 1
        reasons.append(reject(lambda: verify_row(damaged, owners)))
    return reasons


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    args = parser.parse_args()
    rows = json.loads(args.raw.read_bytes())
    result = verify(rows)
    result["rejecting_controls"] = rejection_checks(rows)
    print(json.dumps(result, indent=2, sort_keys=True))
