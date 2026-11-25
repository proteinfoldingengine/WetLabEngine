"""Independent reconstruction by retained subtree sums, bit sets and coalition covers.

This verifier imports neither the producer nor the historical algorithms.
"""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
import lzma
from pathlib import Path
import sys


def need(test, message):
    if not test:
        raise ValueError(message)


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def members(mask, size):
    return [i for i in range(size) if mask >> i & 1]


@lru_cache(maxsize=8192)
def restriction(parent, view, grade):
    sub = list(grade)
    for v in reversed(range(1, len(parent))):
        sub[parent[v]] += sub[v]
    return tuple(sub[v] - sum(sub[w] for w in range(1, len(parent))
                              if view >> w & 1 and parent[w] == v) for v in members(view, len(parent)))


def read(p, sets, g):
    combined = 0
    for mask in sets:
        combined |= mask
    return dict(views=list(sets), local=[list(restriction(p, mask, g)) for mask in sets],
                pair=list(restriction(p, sets[0] | sets[1], g)), whole=list(restriction(p, combined, g)),
                total=sum(g))


def covers(sets, full):
    choices = []
    for subset in range(1, 1 << len(sets)):
        ids = members(subset, len(sets))
        covered = 0
        for i in ids:
            covered |= sets[i]
        if covered == full:
            choices.append(ids)
    m = min(map(len, choices))
    return sorted(x for x in choices if len(x) == m)


def cut(sets, v):
    need(sets[1] & 1 << v and any(i != 1 and mask & 1 << v for i, mask in enumerate(sets)), "illegal cut")
    return (sets[0], sets[1] ^ 1 << v, *sets[2:])


def edit(sets, i, v):
    need(not (sets[i] & 1 << v), "repeated edit")
    return tuple(mask | 1 << v if j == i else mask for j, mask in enumerate(sets))


def transition(sets, after, full):
    left, right = covers(sets, full), covers(after, full)
    a, b = len(left[0]), len(right[0])
    return [a, b, b > a]


def label(sets):
    return "".join(str(sum((1 << i) for i, mask in enumerate(sets) if mask & 1 << v)) for v in range(1, 5))


def stars():
    pre, ends = {}, {}
    p = (-1, 0, 0, 0, 0)
    g = (3, 1, 1, 1, 1)
    for r, s, h in product(range(1, 32, 2), repeat=3):
        if r | s | h != 31:
            continue
        state = (r, s, h)
        key = label(state)
        ends[key] = read(p, state, g)
        if r | s != 31:
            continue
        cuts, outcomes, pairs = {}, {}, {}
        for v in members(s & (r | h) & ~1, 5):
            after = cut(state, v)
            cuts[str(v)] = dict(endpoint=label(after), trigger=transition(state, after, 31))
            outcomes[v] = read(p, after, g)
        for a, b in combinations(sorted(outcomes), 2):
            values = []
            for v in (a, b):
                t = outcomes[v]
                values.append([t["local"][0][0], t["local"][1][0], t["pair"][0], t["whole"][0], t["total"]])
            pairs[f"{a}/{b}"] = values
        pre[key] = dict(cuts=cuts, matched=pairs)
    return dict(endpoints=ends, preparations=pre)


def all_parents(p=(-1,)):
    yield p
    if len(p) < 5:
        for node in range(len(p)):
            yield from all_parents(p + (node,))


def tree_universe():
    result = {}
    for parent in all_parents():
        size = len(parent)
        prefix = [1]
        for v in range(1, size):
            prefix.extend([mask | 1 << v for mask in prefix if mask & 1 << parent[v]])
        pairs, comparisons = {}, {}
        for a in prefix:
            for b in prefix:
                u = a | b
                n = u.bit_count()
                key = f"{a}/{b}"
                pairs[key] = [u, n, n]
                absent = members(a & ~b, size)
                witness = [absent[0], parent[absent[0]]] if absent else None
                comparisons[key] = [n, not absent, witness]
        result["/".join(map(str, parent))] = dict(pairs=pairs, comparisons=comparisons)
    return result


def fixtures():
    p = (-1, 0, 0, 0, 0, 0, 0)
    g = (3, 2, 2, 1, 1, 1, 1)
    base = (25, 103, 3, 5)
    shared = (29, 103, 3, 5)
    out = {}
    for label_, before in (("two_exclusive", base), ("exclusive_and_shared", shared)):
        arms = {}
        for v in (1, 2):
            end = cut(before, v)
            arms[str(v)] = dict(read=read(p, end, g), trigger=transition(before, end, 127), minimum=covers(end, 127))
        out[label_] = dict(prior=read(p, before, g), prior_min=covers(before, 127), cuts=arms)
    first, second = cut(base, 1), cut(base, 2)
    routes = dict(direct=(first, [(0, 1)]), source_reversal=(first, [(1, 1)]),
                  helper_bypass=(first, [(2, 3), (2, 4)]), mask_after_1=(first, [(0, 2), (0, 1)]),
                  mask_after_2=(second, [(0, 1), (0, 2)]))
    paths = {}
    for name, (before, edits) in routes.items():
        rows = []
        for i, v in edits:
            before = edit(before, i, v)
            rows.append(dict(add=[i, v], reading=read(p, before, g), minimum=covers(before, 127)))
        paths[name] = rows
    out["paths"] = paths
    grade = {}
    for key, fine, end in (("positive_collision", (2, 3, 2, 1, 1, 1, 1), first),
                            ("zero", (3, 0, 2, 1, 1, 1, 1), first),
                            ("signed", (3, 2, -2, 1, 1, 1, 1), cut(first, 2))):
        grade[key] = [read(p, before, fine) for before in (base, end)]
    out["grade_controls"] = grade
    parent, grade_, before = (-1, 0, 1, 1), (3, 4, 2, 2), (3, 15, 15)
    after = cut(before, 2)
    out["nested_parent"] = dict(prior=read(parent, before, grade_), post=read(parent, after, grade_), trigger=[1, 1, False])
    return out


def implications(universe):
    star, trees, examples = (universe[key] for key in ("star", "trees", "examples"))
    ends, pre = star["endpoints"], star["preparations"]
    for key, reading in ends.items():
        r, s, h = reading["views"]
        missing = (31 & ~(r | s)).bit_count()
        need(reading["pair"][0] == 3 + missing and reading["whole"] == [3, 1, 1, 1, 1], key)
    deletions = matched = distinguished = 0
    for key, row in pre.items():
        for arm in row["cuts"].values():
            output = ends[arm["endpoint"]]
            need(output["local"][0] == ends[key]["local"][0] and output["views"][0] == ends[key]["views"][0], "receiver-local write")
            deletions += 1
        for a, b in row["matched"].values():
            need(a[:2] == b[:2] and a[3:] == b[3:] == [3, 7], "matched scalars")
            matched += 1
            distinguished += (a[2] != b[2])
    mix = examples["exclusive_and_shared"]
    need(mix["prior_min"] == [[0, 1]], "unique original pair")
    post = [mix["cuts"][str(i)]["read"] for i in (1, 2)]
    need([t["pair"][0] for t in post] == [5, 3]
         and all(t["local"][0] == [7, 2, 1, 1] and t["local"][1][0] == 7 and t["total"] == 11 for t in post),
         "same-grade witness")
    primary = examples["two_exclusive"]
    need([primary["cuts"][str(i)]["read"]["pair"][0] for i in (1, 2)] == [5, 5], "exclusive-sibling null")
    paths = examples["paths"]
    bypass = paths["helper_bypass"][-1]
    need(bypass["minimum"] == [[1, 2]] and bypass["reading"]["pair"][0] == 5, "old cover bypass")
    for key in ("direct", "source_reversal", "mask_after_1", "mask_after_2"):
        need(paths[key][-1]["reading"]["pair"][0] == 3, key)
    left, right = [paths[k][-1]["reading"] for k in ("mask_after_1", "mask_after_2")]
    need(left["views"][0] == right["views"][0] and left["local"][0] == right["local"][0], "masking")
    cp, cq = examples["grade_controls"]["positive_collision"]
    before, after = primary["prior"], primary["cuts"]["1"]["read"]
    need(cp["pair"][0] != before["pair"][0] and cq["local"][:2] == after["local"][:2] and
         cq["local"][2] != after["local"][2], "positive indistinguishability and helper discriminator")
    for label_ in ("zero", "signed"):
        a, b = examples["grade_controls"][label_]
        need(a["pair"][0] == b["pair"][0] and a["pair"] != b["pair"], label_)
    nested = examples["nested_parent"]
    need(nested["prior"]["pair"] == [3, 4, 2, 2] and nested["post"]["pair"] == [3, 6, 2], "internal parent")
    return dict(star_preparations=len(pre), star_endpoints=len(ends), source_deletions=deletions,
                matched_pairs=matched, distinguished_joint_root=distinguished, distinguished_local_roots=0,
                unchanged_entire_receiver=deletions, ordered_trees=len(trees),
                view_pairs=sum(len(t["pairs"]) for t in trees.values()),
                factor_comparisons=sum(len(t["comparisons"]) for t in trees.values()),
                positive_separators=sum(int(not v[1]) for t in trees.values() for v in t["comparisons"].values()))


def compare(expected, actual):
    need(encoded(expected) == encoded(actual), "identity, value or type mismatch")


def rejecting_controls(raw, certificate):
    # Each mutation must fail the very equality check used on the real certificate.
    def rejects(obj, mutate):
        altered = deepcopy(obj)
        mutate(altered)
        try:
            compare(obj, altered)
        except ValueError:
            return
        raise AssertionError("accepted altered evidence")

    group = raw["star"]["preparations"]
    key = next(k for k, x in group.items() if x["cuts"] and x["matched"])
    arm = next(iter(group[key]["cuts"]))
    cases = [
        (group[key], lambda x: x["cuts"].pop(arm)),
        (group[key], lambda x: x["cuts"].update({"duplicate": x["cuts"][arm]})),
        (group[key], lambda x: x["cuts"][arm].update(endpoint=key)),
        (group[key], lambda x: x["cuts"][arm].update(trigger=[0, 0, False])),
        (raw["examples"]["exclusive_and_shared"], lambda x: x["cuts"]["1"]["read"]["pair"].__setitem__(0, 3)),
        (raw["examples"]["nested_parent"], lambda x: x["post"]["pair"].__setitem__(1, 4)),
        (raw["examples"]["paths"], lambda x: x["helper_bypass"][-1].update(minimum=[[0, 1]])),
        (raw["trees"]["-1/0"]["comparisons"], lambda x: x.__setitem__("3/1", [2, True, None])),
        (certificate, lambda x: x.update(historical_sha="unbound")),
        (certificate, lambda x: x["counts"].update(star_endpoints=2400)),
    ]
    for obj, change in cases:
        rejects(obj, change)
    return len(cases)


def main(directory):
    raw_bytes = lzma.decompress((directory / "fixed_pair_universe.json.xz").read_bytes())
    raw = json.loads(raw_bytes)
    expected = dict(star=stars(), trees=tree_universe(), examples=fixtures())
    compare(expected, raw)
    need(raw_bytes == encoded(raw), "noncanonical encoding")
    counts = implications(expected)
    cert = json.loads((directory / "fixed_pair_certificate.json").read_bytes())
    pins = dict(overlap="b18f52109ccff9c7dc77542d3b8f3e5d5989102a", cut="c10ac57f988a439144e21898bd2b33ece0838a9b",
                gate="91cd1e507e955683e744fbdbb0745cac19d66cb3")
    compare(dict(historical_sha="e61d5b0e827f7b412824ad46021e2ad6cc6f7875", historical_blobs=pins, counts=counts,
                 raw_sha256=sha256(raw_bytes).hexdigest(), examples=expected["examples"]), cert)
    negative = rejecting_controls(expected, cert)
    print(json.dumps(dict(status="PASS", rejecting_controls=negative, **counts), sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
