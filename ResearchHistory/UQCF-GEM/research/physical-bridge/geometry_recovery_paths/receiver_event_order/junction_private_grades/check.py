"""Check every first private-leaf acquisition against the original P1, work and move code."""
import argparse
from collections import Counter, deque
from functools import cache
from hashlib import sha256
from itertools import combinations, permutations
import json
import lzma
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "endogenous_junction"))
from historical import History, move, positions, toggle

CHARTS = (0, 1, 2)
SITES = tuple(range(10))
X, Y, W, S = 1, 2, 3, 7
TERNARY, BINARY = (4, 5, 6), (8, 9)
LEAVES = (X, Y, *TERNARY, *BINARY)
PAIRS = tuple(combinations(CHARTS, 2))
TARGET = (2, 3, 2)


def has(mask, site):
    return bool(mask & (1 << site))


def holdership(start):
    return {site: next(j for j in CHARTS if has(start[j], site)) for site in LEAVES}


def preparations():
    starts = set()
    for outside, left, right in permutations(CHARTS):
        for w_owners in permutations(CHARTS):
            rows = [1 | (1 << W)] * 3
            for j, sites in ((outside, (X, Y)), (left, (S, 8)), (right, (S, 9))):
                for v in sites:
                    rows[j] |= 1 << v
            for j, v in zip(w_owners, TERNARY):
                rows[j] |= 1 << v
            starts.add(tuple(rows))
    prior = json.loads(lzma.decompress((HERE.parent / "junction_reachability/raw.json.xz").read_bytes()))
    assert starts == {tuple(row["start"]) for row in prior["original_preparation_family"]}
    return sorted(starts)


def world(start, bits, parents):
    owner = holdership(start)
    totals = [0] * len(parents)
    totals[0], totals[W], totals[S] = 80, 30, 24
    for anchor, first in ((X, 1), (8, 4), (9, 6)):
        chart = owner[anchor]
        twig, = (v for v in TERNARY if owner[v] == chart)
        group = (X, Y, twig) if anchor == X else (twig, anchor)
        shift = (bits >> chart) & 1
        for i, site in enumerate(group):
            totals[site] = first + ((i + shift) % len(group))
    fine = totals.copy()
    for v in SITES[1:]:
        fine[parents[v]] -= totals[v]
    assert min(fine) > 0
    return tuple(fine), tuple(totals)


class Readers:
    def __init__(self, lib, checkout, tree):
        self.lib = lib
        self.parents = lib.parents(tree)
        demos = checkout / "ResearchHistory/UQCF-GEM/demos"
        sys.path.insert(0, str(demos / "v15.40-global-balance-geometry-specificity"))
        import response_geometry
        self.work = response_geometry

    @cache
    def p1(self, mask, fine):
        sites = positions(mask, len(self.parents))
        projected = self.lib.p1.push(self.parents, SITES, sites, fine)
        return tuple(zip(sites, map(int, projected)))

    @cache
    def works(self, rows, totals):
        coordinates = [tuple(totals[v] if has(mask, v) else 0 for v in SITES[1:]) for mask in rows]
        geometry = self.work.construct_response_geometry(CHARTS, coordinates, coordinates)
        assert self.work.metric_passes(geometry)
        return tuple(int(geometry.work[a][b]) for a, b in PAIRS)


def boundary(lib, tree, start):
    pending = deque([start])
    seen = {start}
    edges = []
    while pending:
        before = pending.popleft()
        for (j, site, sign), after in sorted(lib.moves(tree, before).items()):
            profile = lib.profile(tree, after)
            band = sum(abs(a - b) for a, b in zip(profile, TARGET)) <= 1
            edges.append((before, after, j, site, sign, profile, band))
            if site not in LEAVES and after not in seen:
                seen.add(after)
                pending.append(after)
    outside = holdership(start)[X]
    assert seen == {start, toggle(start, outside, S)}
    return sorted(seen), edges


def read_signed_change(delta):
    lower, = (edge for edge, n in zip(PAIRS, delta) if n < 0)
    higher, = (edge for edge, n in zip(PAIRS, delta) if n > 0)
    recipient, = set(lower) & set(higher)
    sender, = set(lower) - {recipient}
    power = -delta[PAIRS.index(lower)]
    assert power == delta[PAIRS.index(higher)] and delta.count(0) == 1
    return sender, recipient, power


def test_start(lib, read, tree, start):
    owner = holdership(start)
    outsider = owner[X]
    incumbents = tuple(j for j in CHARTS if j != outsider)
    states, edges = boundary(lib, tree, start)
    worlds = [world(start, b, read.parents) for b in range(8)]
    prestates = []
    for state in states:
        works = {read.works(state, totals) for fine, totals in worlds}
        assert len(works) == 1
        geom, = works
        for bits, (fine, totals) in enumerate(worlds):
            for j in CHARTS:
                for s in CHARTS:
                    flipped = worlds[bits ^ (1 << s)][0]
                    assert (read.p1(state[j], fine) != read.p1(state[j], flipped)) == (s == j)
            if state == start:
                left, right = incumbents
                def pair(a, b):
                    return geom[PAIRS.index(tuple(sorted((a, b))))]
                isolated = (pair(outsider, left) + pair(outsider, right) - pair(left, right)) // 2
                own = dict(read.p1(state[outsider], fine))
                residue = isolated - sum(own[v] ** 2 for v in LEAVES if owner[v] == outsider)
                assert residue == totals[S] ** 2
        prestates.append(dict(state=state, work=geom))
    ledger = []
    for before, after, j, site, sign, profile, band in edges:
        private = site in owner
        if private:
            assert sign == 1 and j != owner[site] and has(before[owner[site]], site)
        else:
            assert j == outsider and site == S and after in states
        signatures, values = [], []
        for bits, (fine, totals) in enumerate(worlds):
            delta = tuple(b - a for a, b in zip(read.works(before, totals), read.works(after, totals)))
            if private:
                s = owner[site]
                assert read_signed_change(delta) == (s, j, fine[site] ** 2)
                old = worlds[bits ^ (1 << s)][0]
                acquired = dict(read.p1(after[j], fine))[site]
                assert acquired == fine[site] != dict(read.p1(after[j], old))[site]
                for peer in CHARTS:
                    if peer != j:
                        assert read.p1(before[peer], fine) == read.p1(after[peer], fine)
                values.append(acquired)
            else:
                assert delta == tuple(-sign * totals[S] ** 2 if j in pair else 0 for pair in PAIRS)
                if sign == 1:
                    assert dict(read.p1(after[j], fine))[S] == totals[S]
            signatures.append(delta)
        ledger.append(dict(before=before, after=after, chart=j, site=site, sign=sign,
                           profile=profile, band=band, work_deltas=signatures, acquired=values))
    path = lib.normalize(tree, TARGET, start)
    events = [(i, move(path[i-1], path[i])) for i in range(1, len(path))]
    first = next(((i, op) for i, op in events if op[1] in LEAVES), None)
    observed = None
    if first:
        index, (j, site, sign) = first
        assert sign == 1 and path[index-1] in states
        sender = owner[site]
        at_return = set()
        for bits, (fine, _) in enumerate(worlds):
            flipped = worlds[bits ^ (1 << sender)][0]
            at_return.add(read.p1(path[-1][j], fine) != read.p1(path[-1][j], flipped))
        assert len(at_return) == 1
        retained = at_return.pop()
        assert retained == any(has(path[-1][j], leaf) and holder == sender for leaf, holder in owner.items())
        observed = dict(step=index, receiver=j, sender=sender, site=site,
                        same_site_at_return=has(path[-1][j], site), bit_at_return=retained)
    else:
        assert set(path) <= set(states)
    return dict(start=start, frontier=prestates, worlds=worlds, edges=ledger, original=path, first=observed)


def experiment(checkout):
    lib = History(checkout)
    tree = (lib.p.L, lib.p.L, lib.p.T, lib.p.B)
    readers = Readers(lib, checkout, tree)
    rows = [test_start(lib, readers, tree, start) for start in preparations()]
    counts = Counter(original_without_acquisition=0, original_idle=0)
    for row in rows:
        for edge in row["edges"]:
            leaf = edge["site"] in LEAVES
            stage = "compact" if edge["before"] == row["start"] else "bare_S"
            if leaf:
                counts[stage + "_leaf_exits"] += 1
                counts[stage + "_in_band_leaf_exits"] += int(edge["band"])
            else:
                counts["silent_edges"] += 1
        first = row["first"]
        if first:
            counts["original_with_acquisition"] += 1
            counts["original_first_step_" + str(first["step"])] += 1
            counts["original_same_bit_at_return"] += int(first["bit_at_return"])
            counts["original_same_leaf_at_return"] += int(first["same_site_at_return"])
        else:
            counts["original_without_acquisition"] += 1
            counts["original_idle"] += int(len(row["original"]) == 1)
    raw = (json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n").encode()
    summary = dict(starts=len(rows), worlds_per_start=8, work_pair_order=PAIRS,
                   counts=dict(sorted(counts.items())), raw_sha256=sha256(raw).hexdigest())
    return summary, raw


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical_checkout", type=Path)
    parser.add_argument("--raw", type=Path)
    args = parser.parse_args()
    summary, raw = experiment(args.historical_checkout.resolve())
    if args.raw:
        args.raw.write_bytes(raw)
    print(json.dumps(summary, indent=2, sort_keys=True))
