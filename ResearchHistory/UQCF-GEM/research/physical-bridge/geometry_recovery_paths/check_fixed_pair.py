"""Run pinned P1 restriction, positive gluing and legal source cuts on the frozen domains."""
from functools import lru_cache
from hashlib import sha1, sha256
import importlib.util
from itertools import combinations, product
import json
import lzma
from pathlib import Path
import sys

from sympy import Matrix

PINS = {
    "overlap": ("v16.23-overlap-descent/engine.py", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"),
    "cut": ("v16.26-consistency-increment-law/engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b"),
    "gate": ("v16.26-consistency-increment-law/verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3"),
}
HIST = "e61d5b0e827f7b412824ad46021e2ad6cc6f7875"


def require(test, reason):
    if not test:
        raise ValueError(reason)


def modules(root):
    result = {}
    for key, (name, expected) in PINS.items():
        file = root / "ResearchHistory/UQCF-GEM/demos" / name
        data = file.read_bytes()
        require(sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected, name)
        spec = importlib.util.spec_from_file_location("fixed_pair_" + key, file)
        result[key] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(result[key])
    return result


def wire(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()


def integer_tuple(values):
    require(all(x.denominator == 1 for x in values), "unexpected nonintegral amount")
    return tuple(map(int, values))


def bitmask(view):
    return sum(1 << v for v in view)


def views(rows, k):
    return tuple((0,) + tuple(v for v, mask in enumerate(rows, 1) if mask & (1 << i)) for i in range(k))


def minimum_covers(family, nodes):
    for count in range(1, len(family) + 1):
        found = [list(indices) for indices in combinations(range(len(family)), count)
                 if set().union(*(family[i] for i in indices)) == set(nodes)]
        if found:
            return found
    raise ValueError("family omits a node")


class Reader:
    def __init__(self, operators):
        self.op = operators

    @lru_cache(maxsize=8192)
    def observe(self, parents, family, grade, positive=True):
        e = self.op["overlap"]
        full = tuple(range(len(parents)))
        local = tuple(e.push(parents, full, view, grade) for view in family)
        pair = e.glue(parents, family[0], family[1], local[0], local[1], positive=positive)
        all_charts = e.glue_many(parents, family, local, positive=positive)
        totals = {e.push(parents, view, (0,), g) for view, g in zip(family, local)}
        require(len(totals) == 1, "inconsistent root-only observations")
        return dict(views=list(map(bitmask, family)), local=[list(integer_tuple(g)) for g in local],
                    pair=list(integer_tuple(pair)), whole=list(integer_tuple(all_charts)),
                    total=integer_tuple(totals.pop())[0])

    def delete(self, parents, family, leaf):
        frozen = tuple(tuple(v) for v in family)
        native = self.op["cut"].atomic(parents, family, 1, leaf)
        self.op["gate"].verify_atomic(native)
        result = tuple(map(tuple, native["after"]))
        require(family == frozen and result[0] == family[0], "receiver state changed inside atomic")
        return result, [native["tau_before"], native["tau_after"], native["trigger"]]


def star_domain(reader):
    p, g = (-1, 0, 0, 0, 0), (3, 1, 1, 1, 1)
    endpoints, preparations = {}, {}
    for rows in product(range(1, 8), repeat=4):
        key = "".join(map(str, rows))
        family = views(rows, 3)
        snap = reader.observe(p, family, g)
        endpoints[key] = snap
        if not all(mask & 3 for mask in rows):
            continue
        arms = {}
        for leaf in family[1][1:]:
            if rows[leaf - 1] == 2:
                continue
            post, trigger = reader.delete(p, family, leaf)
            after = reader.observe(p, post, g)
            masks = tuple(sum(1 << i for i, view in enumerate(post) if v in view) for v in range(1, 5))
            arms[str(leaf)] = dict(endpoint="".join(map(str, masks)), trigger=trigger)
            require(snap["local"][0] == after["local"][0], "receiver had a numerical write")
        contrasts = {}
        for a, b in combinations(map(int, arms), 2):
            readings = []
            for leaf in (a, b):
                state = views(tuple(map(int, arms[str(leaf)]["endpoint"])), 3)
                reading = reader.observe(p, state, g)
                readings.append([reading["local"][0][0], reading["local"][1][0],
                                 reading["pair"][0], reading["whole"][0], reading["total"]])
            contrasts[f"{a}/{b}"] = readings
        preparations[key] = dict(cuts=arms, matched=contrasts)
    return dict(endpoints=endpoints, preparations=preparations)


def tree_domain(reader):
    e = reader.op["overlap"]
    result = {}
    for size in range(1, 6):
        for tail in product(*(range(v) for v in range(1, size))):
            p = (-1,) + tail
            full = tuple(range(size))
            legal = sorted(e.subsets(p), key=bitmask)
            units = [tuple(int(v == j) for v in full) for j in full]
            matrices = {view: Matrix([e.push(p, full, view, u) for u in units]).T for view in legal}
            pairs, representatives = {}, {}
            for left, right in product(legal, repeat=2):
                union = tuple(sorted(set(left) | set(right)))
                stack = matrices[left].col_join(matrices[right])
                rank = int(stack.rank())
                combined = int(stack.col_join(matrices[union]).rank())
                require(rank == combined == len(union), "joint and union rows differ")
                pairs[f"{bitmask(left)}/{bitmask(right)}"] = [bitmask(union), rank, combined]
                representatives.setdefault(union, (stack, (left, right)))
            comparisons = {}
            for a, b in product(legal, repeat=2):
                stack_a, family_a = representatives[a]
                stack_b, family_b = representatives[b]
                augmented = int(stack_b.col_join(stack_a).rank())
                determines = augmented == len(b)
                missing = sorted(set(a) - set(b))
                require(determines == (not missing), "kernel order")
                witness = None
                if missing:
                    v = missing[0]
                    base = (2,) * size
                    other = list(base)
                    other[v] += 1
                    other[p[v]] -= 1
                    same = lambda family: all(e.push(p, full, view, base) == e.push(p, full, view, other)
                                              for view in family)
                    require(min(other) > 0 and same(family_b) and not same(family_a), "positive separation")
                    witness = [v, p[v]]
                comparisons[f"{bitmask(a)}/{bitmask(b)}"] = [augmented, determines, witness]
            result["/".join(map(str, p))] = dict(pairs=pairs, comparisons=comparisons)
    return result


def examples(reader):
    p = (-1, 0, 0, 0, 0, 0, 0)
    g = (3, 2, 2, 1, 1, 1, 1)
    basic = (6, 10, 1, 1, 2, 2)
    shared = (6, 11, 1, 1, 2, 2)
    examples = {}
    for name, prior in (("two_exclusive", basic), ("exclusive_and_shared", shared)):
        fam = views(prior, 4)
        examples[name] = dict(prior=reader.observe(p, fam, g),
                              prior_min=minimum_covers(fam, range(len(p))), cuts={})
        for leaf in (1, 2):
            after, change = reader.delete(p, fam, leaf)
            examples[name]["cuts"][str(leaf)] = dict(read=reader.observe(p, after, g), trigger=change,
                                                      minimum=minimum_covers(after, range(len(p))))
    fixed = views(basic, 4)
    cut1, _ = reader.delete(p, fixed, 1)
    cut2, _ = reader.delete(p, fixed, 2)
    paths = {}
    routes = {"direct": (cut1, [(0, 1)]), "source_reversal": (cut1, [(1, 1)]),
              "helper_bypass": (cut1, [(2, 3), (2, 4)]), "mask_after_1": (cut1, [(0, 2), (0, 1)]),
              "mask_after_2": (cut2, [(0, 1), (0, 2)])}
    for name, (family, edits) in routes.items():
        path = []
        for index, vertex in edits:
            require(vertex not in family[index], "repeated addition")
            updated = list(family)
            updated[index] = tuple(sorted((*family[index], vertex)))
            family = tuple(updated)
            path.append(dict(add=[index, vertex], reading=reader.observe(p, family, g),
                             minimum=minimum_covers(family, range(len(p)))))
        paths[name] = path
    examples["paths"] = paths
    altered = (2, 3, 2, 1, 1, 1, 1)
    zero = (3, 0, 2, 1, 1, 1, 1)
    signed = (3, 2, -2, 1, 1, 1, 1)
    both, _ = reader.delete(p, cut1, 2)
    examples["grade_controls"] = {
        "positive_collision": [reader.observe(p, fixed, altered), reader.observe(p, cut1, altered)],
        "zero": [reader.observe(p, fixed, zero), reader.observe(p, cut1, zero)],
        "signed": [reader.observe(p, fixed, signed, False), reader.observe(p, both, signed, False)],
    }
    nested = (-1, 0, 1, 1)
    ng = (3, 4, 2, 2)
    fam = ((0, 1), (0, 1, 2, 3), (0, 1, 2, 3))
    after, c = reader.delete(nested, fam, 2)
    examples["nested_parent"] = dict(prior=reader.observe(nested, fam, ng), post=reader.observe(nested, after, ng), trigger=c)
    return examples


def main(history, out):
    out.mkdir(exist_ok=True, parents=True)
    reader = Reader(modules(history))
    raw = dict(star=star_domain(reader), trees=tree_domain(reader), examples=examples(reader))
    data = wire(raw)
    (out / "fixed_pair_universe.json.xz").write_bytes(lzma.compress(data, preset=6))
    stars, trees = raw["star"], raw["trees"]
    pre = list(stars["preparations"].values())
    comparisons = [arms for entry in pre for arms in entry["matched"].values()]
    counts = dict(star_preparations=len(pre), star_endpoints=len(stars["endpoints"]),
                  source_deletions=sum(len(row["cuts"]) for row in pre), matched_pairs=len(comparisons),
                  distinguished_joint_root=sum(a[2] != b[2] for a, b in comparisons),
                  distinguished_local_roots=sum(a[:2] != b[:2] for a, b in comparisons),
                  unchanged_entire_receiver=sum(stars["endpoints"][key]["local"][0] ==
                      stars["endpoints"][arm["endpoint"]]["local"][0] for key, prep in stars["preparations"].items()
                      for arm in prep["cuts"].values()),
                  ordered_trees=len(trees), view_pairs=sum(len(t["pairs"]) for t in trees.values()),
                  factor_comparisons=sum(len(t["comparisons"]) for t in trees.values()),
                  positive_separators=sum(row[2] is not None for t in trees.values() for row in t["comparisons"].values()))
    cert = dict(historical_sha=HIST, historical_blobs={key: blob for key, (_, blob) in PINS.items()},
                raw_sha256=sha256(data).hexdigest(), counts=counts, examples=raw["examples"])
    (out / "fixed_pair_certificate.json").write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
