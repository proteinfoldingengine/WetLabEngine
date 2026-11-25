"""Execute the historical pruning atom and work constructor on all competing last copies."""
from collections import Counter
from functools import lru_cache
import gzip
from hashlib import sha1, sha256
import importlib.util
from itertools import combinations, product
import json
import lzma
from pathlib import Path
import sys

CHARTS = range(4)
EDGES = tuple(combinations(CHARTS, 2))
DEMOS = Path("ResearchHistory/UQCF-GEM/demos")
ARCHIVE = DEMOS / "v16.43-star-fiber-classification/evidence/science/scientific/CERTIFICATE.json.gz"
ARCHIVE_SHA = "f2de35e7f7fea13621c332cae71dbdc69da63cf8dd806827601fa90b07145a25"
FILES = {
    "atom": ("v16.26-consistency-increment-law/engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b"),
    "verify": ("v16.26-consistency-increment-law/verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3"),
    "work": ("v15.40-global-balance-geometry-specificity/response_geometry.py", "9128c24b695c1b539ac60dc93aeaf0bd4795c57b"),
    "refine": ("v16.25-pruning-refinement-closure/engine.py", "e9c576a2590c8e16812f1b3fa0436111e3648f1c"),
    "invisible": ("v16.33-consistency-quotient-kernel/verifier.py", "c6cf3143423da17c09bbdbbc2eab4800c91acc24"),
}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def modules(root):
    result = {}
    for name, (path, pin) in FILES.items():
        full = root / DEMOS / path
        raw = full.read_bytes()
        need(sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == pin, path)
        spec = importlib.util.spec_from_file_location("historical_protected_" + name, full)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        result[name] = module
    return result


def key(row):
    return sum(m << (5*j) for j, m in enumerate(row))


def from_views(ys):
    return tuple(sum(1 << (v-1) for v in y if v) for y in ys)


def holders(row, v):
    return tuple(j for j in CHARTS if row[j] & (1 << (v-1)))


class Star:
    def __init__(self, size, historical):
        self.leaves = range(1, size+1)
        self.p = (-1,) + (0,)*size
        self.mod = historical

    def views(self, row):
        return tuple((0,) + tuple(v for v in self.leaves if j in holders(row, v)) for j in CHARTS)

    @lru_cache(maxsize=None)
    def moves(self, row):
        options = {}
        views = self.views(row)
        for j, view in enumerate(views):
            for v in view[1:]:
                try:
                    event = self.mod["atom"].atomic(self.p, views, j, v)
                except ValueError as err:
                    need(str(err) == "same union" and holders(row, v) == (j,), "unexpected deletion rejection")
                    continue
                self.mod["verify"].verify_atomic(event)
                options[j, v] = from_views(event["after"])
        return options

    @lru_cache(maxsize=None)
    def descendants(self, row):
        reached, terminals = {row}, set()
        children = self.moves(row)
        if not children:
            terminals.add(row)
        for child in children.values():
            family, ends = self.descendants(child)
            reached.update(family)
            terminals.update(ends)
        return frozenset(reached), frozenset(terminals)

    @lru_cache(maxsize=None)
    def geometry(self, row):
        coordinates = [tuple(int(j in holders(row, v)) for v in self.leaves) for j in CHARTS]
        historical = self.mod["work"]
        geom = historical.construct_response_geometry(CHARTS, coordinates, coordinates)
        return tuple(int(geom.work[i][j]) for i, j in EDGES), historical.metric_passes(geom)

    def descend_geometry(self, row, terminal):
        return {self.geometry(s)[0] for s in self.descendants(row)[int(terminal)]}

    def signature(self, row, event):
        result = self.mod["atom"].atomic(self.p, self.views(row), *event)
        self.mod["verify"].verify_atomic(result)
        return [result["h_before"], result["h_after"], result["delta_h"], result["trigger"]]

    def minimum(self, row):
        target = (1 << len(self.leaves))-1
        for size in range(1, 5):
            teams = []
            for group in combinations(CHARTS, size):
                mask = 0
                for j in group:
                    mask |= row[j]
                if mask == target:
                    teams.append(list(group))
            if teams:
                return teams
        raise ValueError("uncovered star")

    def p1(self, row, j):
        view = self.views(row)[j]
        return list(map(int, self.mod["refine"].push(self.p, view, [1]*len(self.p))))

    def profile_edge(self, a, b, expected=True):
        record = dict(parents=self.p, before=self.views(a), after=self.views(b))
        return self.mod["invisible"].verify_move(record, expected)


def component(row, leaves, omitted, root):
    found = {root}
    while True:
        nxt = set(found)
        for v in leaves:
            others = set(holders(row, v))
            if v != omitted and others & found:
                nxt.update(others)
        if nxt == found:
            return sorted(found)
        found = nxt


def conflict(star, row, v, source, other):
    a, b = (star.moves(row)[j, v] for j in (source, other))
    ca, cb = (component(row, star.leaves, v, j) for j in (source, other))
    separate = other not in ca
    joint = []
    for terminal in (False, True):
        shared = star.descend_geometry(a, terminal) & star.descend_geometry(b, terminal)
        need(bool(shared) != separate, "component versus work intersection")
        joint.append(sorted(map(list, shared)))
    for j in set(CHARTS)-{source, other}:
        need({r[j] for r in star.descendants(a)[1]} == {r[j] for r in star.descendants(b)[1]},
             "forced third-chart terminal record")
    isol = [j for j, group in ((source, ca), (other, cb)) if len(group) == 1]
    if separate:
        need(isol, "no isolated owner in three-active domain")
        for j in isol:
            edge = EDGES.index((0, j))
            vals = [{w[edge] for w in star.descend_geometry(z, False)} for z in (a, b)]
            need(all(len(h) == 1 for h in vals) and vals[0].isdisjoint(vals[1]), "blank-to-owner signal")
    return dict(leaf=v, owners=[source, other], post=[key(a), key(b)], components=[ca, cb], isolated=isol,
                disconnected=separate, common_work=joint[0], common_terminal_work=joint[1])


def census(star):
    table, forks = [], []
    stats = Counter()
    for word in product(range(2, 16, 2), repeat=4):
        row = tuple(sum(1 << i for i, mask in enumerate(word) if mask & (1 << j)) for j in CHARTS)
        choices = star.moves(row)
        reaches, ends = star.descendants(row)
        squares = []
        for (e, a), (f, b) in combinations(choices.items(), 2):
            left = star.moves(a).get(f)
            right = star.moves(b).get(e)
            exclusive = e[1] == f[1] and len(holders(row, e[1])) == 2
            need(left == right and (left is None) == exclusive, "two-step square")
            squares.append([*e, *f, None if exclusive else key(left)])
            if exclusive:
                item = conflict(star, row, e[1], e[0], f[0])
                item["start"] = key(row)
                forks.append(item)
                stats["disconnected" if item["disconnected"] else "connected"] += 1
            else:
                stats["commuting"] += 1
        work, metric = star.geometry(row)
        table.append(dict(start=key(row), masks=list(row), moves=[[*e, key(child)] for e, child in choices.items()],
                          pairs=squares, reachable=sorted(map(key, reaches)), terminals=sorted(map(key, ends)),
                          work=list(work), metric=metric))
        stats["directed_moves"] += len(choices)
        stats["event_pairs"] += len(squares)
    stats.update(preparations=len(table), conflicts=len(forks))
    return dict(states=sorted(table, key=lambda r:r["start"]),
                forks=sorted(forks, key=lambda r:(r["start"], r["leaf"]))), dict(stats)


def named(star, row, v, observer, reference):
    actors = holders(row, v)
    need(len(actors) == 2, "named dispute")
    arms = []
    for actor in actors:
        post = star.moves(row)[actor, v]
        reached, ends = star.descendants(post)
        states = []
        for state in sorted(reached):
            w, metric = star.geometry(state)
            states.append(dict(masks=list(state), terminal=state in ends, work=list(w), metric=metric,
                               h=len(star.minimum(state)[0]), receiver_p1=star.p1(state, observer)))
        need(star.profile_edge(post, row), "archived exact inverse addition")
        arms.append(dict(actor=actor, post=list(post), atom=star.signature(row, (actor,v)),
                         source_root=[star.p1(row, actor)[0], star.p1(post, actor)[0]],
                         covers=star.minimum(post), states=states))
    index = EDGES.index(tuple(sorted((observer, reference))))
    return dict(prior=list(row), prior_work=list(star.geometry(row)[0]), prior_covers=star.minimum(row),
                disputed=v, receiver=observer, partner=reference, pair_index=index, arms=arms)


def legacy_checks(star, row):
    e, f = (2, 2), (2, 3)
    a, b = (star.moves(row)[event] for event in (e, f))
    joined = star.moves(a)[f]
    need(joined == star.moves(b)[e], "same-source join")
    refs = star.mod["refine"]
    views = star.views
    records = {}
    all_views = {from_views(x) for x in refs.refinements(star.p, views(row))}
    need(all_views == set(star.descendants(row)[0]), "refinement enumeration")
    for label, x, y in [("left", row, a), ("right", row, b), ("second", a, joined), ("inverse", a, row)]:
        try:
            result = refs.certify_refinement(star.p, views(x), views(y))
            directed = "strict" if result["strict"] else "flat"
        except ValueError as err:
            need(str(err) == "not componentwise retained subview", "unexpected direction control")
            directed = "rejected"
        try:
            equal_profile = star.profile_edge(x, y, True)
        except ValueError as err:
            need(str(err) == "wrong invisibility", "unexpected profile control")
            star.profile_edge(x, y, False)
            equal_profile = False
        records[label] = dict(before=list(x), after=list(y), refinement=directed,
                              v1633_accepts_as_invisible=equal_profile)
    return records


def main(history, out):
    imported = modules(history)
    star = Star(4, imported)
    data, stats = census(star)
    triangle = (0, 10, 7, 12)
    cut = (1, 2)
    prepared = star.moves(triangle)[cut]
    old = named(star, triangle, 4, 2, 1)
    opened = named(star, prepared, 4, 2, 1)
    five = named(Star(5, imported), (16, 9, 2, 28), 4, 2, 1)
    six = named(Star(6, imported), (16, 41, 2, 28), 4, 2, 1)
    original = (history/ARCHIVE).read_bytes()
    need(sha256(original).hexdigest() == ARCHIVE_SHA, "archive digest")
    entry, = (e for e in json.loads(gzip.decompress(original))["entries"] if (e["m"],e["k"]) == (4,4))
    ids = {tuple((n-1)//2 for n in row):i for i,row in enumerate(entry["graph"]["states"])}
    refs = {str(key(tuple(x))):ids[tuple(x)] for case in (old, opened)
            for x in [case["prior"], *(s["masks"] for a in case["arms"] for s in a["states"])]}
    for case in (old, opened):
        for a in case["arms"]:
            source = a["actor"]
            post_id = ids[tuple(a["post"])]
            need(entry["graph"]["forward_moves"][post_id] & (1 << (4*source + case["disputed"]-1)),
                 "missing archived inverse")
    serialized = (json.dumps(data, separators=(",",":"), sort_keys=True)+"\n").encode()
    out.mkdir(parents=True, exist_ok=True)
    (out/"protected_work_universe.json.xz").write_bytes(lzma.compress(serialized, preset=9))
    cert = dict(domain=stats, archive_sha256=ARCHIVE_SHA, raw_universe_sha256=sha256(serialized).hexdigest(),
                legacy=legacy_checks(star, triangle), triangle=old, common_cut=list(cut), opened=opened,
                five_leaf=five, six_leaf_equal_source=six, archived_four_leaf_rows=refs)
    (out/"protected_work_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2)+"\n")
    print(json.dumps(dict(**stats, five_leaf_pair_values=[
        sorted({s["work"][five["pair_index"]] for s in a["states"]}) for a in five["arms"]]), sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]))
