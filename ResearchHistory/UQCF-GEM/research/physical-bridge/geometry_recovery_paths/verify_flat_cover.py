"""Recover the switch class from arbitrary chart masks; use assignments and original archive rows."""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import gzip
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import lzma
from pathlib import Path
import sys

from verify_cover_member_pruning import ARCHIVE, check, reject

CHARTS = tuple(range(4))
LEAVES = (1, 2, 3, 4)
PARENT_ARCHIVE = "f2de35e7f7fea13621c332cae71dbdc69da63cf8dd806827601fa90b07145a25"


@lru_cache(maxsize=None)
def minimum(row):
    teams = []
    for bits in range(1, 16):
        union = 0
        team = tuple(j for j in CHARTS if (bits >> j) & 1)
        for j in team:
            union |= row[j]
        if union == 31:
            teams.append(team)
    if not teams:
        raise ValueError("uncovered leaf")
    size = min(map(len, teams))
    return sorted(group for group in teams if len(group) == size)


def toggle(row, j, v):
    return tuple(x ^ (1 << v) if i == j else x for i, x in enumerate(row))


def cuts(row, source):
    return [v for v in LEAVES if row[source] & (1 << v)
            and any(row[j] & (1 << v) for j in CHARTS if j != source)]


def census():
    population = {}
    for blank, source in permutations(CHARTS, 2):
        active = [j for j in CHARTS if j != blank]
        for words in product(range(1, 32, 2), repeat=3):
            if words[0] | words[1] | words[2] != 31:
                continue
            masks = [1] * 4
            for j, word in zip(active, words):
                masks[j] = word
            row = tuple(masks)
            if len(minimum(row)[0]) != 2:
                continue
            for u, v in combinations(cuts(row, source), 2):
                left, right = [minimum(toggle(row, source, w)) for w in (u, v)]
                if len(left[0]) != 2 or len(right[0]) != 2:
                    continue
                switches = [j for j in CHARTS if j != source and
                            {j in h for h in left}.isdisjoint(j in h for h in right)]
                if switches:
                    check(row not in population, "multiple designated switches per preparation")
                    population[row] = (blank, source, (u, v))
    return population


def assignments_and_orders(row):
    holders = [[j for j in CHARTS if row[j] & (1 << v)] for v in LEAVES]
    orders = []
    for owners in product(*holders):
        if len(set(owners)) == 2:
            extras = [(j, v) for v, col in zip(LEAVES, holders) for j in col if j != owners[v - 1]]
            orders.extend([list(pair) for pair in order] for order in permutations(extras))
    return sorted(orders)


def expected_arm(row, source, v, other, ids):
    after = toggle(row, source, v)
    subtractions, additions = [], []
    for j in CHARTS:
        for w in LEAVES:
            neighbor = toggle(after, j, w)
            if neighbor not in ids:
                continue
            q = len(minimum(neighbor)[0])
            if neighbor[j] < after[j]:
                subtractions.append([j, w, q])
            elif q == 2:
                additions.append([j, w])
    orders = assignments_and_orders(after)
    first = {order[0][0] for order in orders}
    check(len(first) == 1 and all(len(order) == 2 for order in orders), "one-step receiver")
    receiver, = first
    check(len(orders) == 2 and all(j == receiver for order in orders for j, _ in order), "two receiver orders")
    joined = toggle(after, source, other)
    check(len(minimum(joined)[0]) == 3 and [source, v] in additions, "join or inverse")
    return dict(leaf=v, row=ids[after], signature=[2, 0, False], receiver=receiver,
                deletions=subtractions, fixed_paths=orders, exact_additions=additions, double_cut=ids[joined])


def expect_writer(row, source, marked, entry, ids):
    team = minimum(row)[0]
    i = ids[row]
    stored = entry["normalizations"][i]
    check(stored["state"] == i and stored["q"] == 2 and stored["path"][0] == i, "archived input")
    # First holder of each leaf in the frozen ordered cover is kept. The other
    # incidences sort by leaf, then chart, independently of the trace hook.
    commands = []
    for v in LEAVES:
        members = [j for j in CHARTS if row[j] & (1 << v)]
        keeper = min(set(members).intersection(team))
        commands.extend((v, j, keeper) for j in members if j != keeper)
    steps, cur = [], row
    for v, j, k in sorted(commands):
        new = toggle(cur, j, v)
        before, after = minimum(cur), minimum(new)
        item = dict(chart=j, leaf=v, keeper=k, before=ids[cur], after=ids[new],
                    covers_before=list(map(list, before)), covers_after=list(map(list, after)))
        if j == source:
            other, = set(marked) - {v}
            possible = other in cuts(cur, j)
            alt = minimum(toggle(cur, j, other)) if possible else []
            item["opposite"] = dict(legal=possible, keeps_q=bool(alt and len(alt[0]) == 2),
                                    keeps_bound=team in alt)
        steps.append(item)
        cur = new
    check(len(steps) == 3 and stored["path"][1:4] == [s["after"] for s in steps], "original cleanup order")
    check(all(len(cuts(cur, j)) == 0 for j in CHARTS), "nonmaximal deletion prefix")
    return dict(bound_before=i, bound_cover=list(team), cleanup=steps, archived_path=stored["path"])


def compare_rows(actual, expected):
    check(len(actual) == len(expected), "preparation count")
    keys = [tuple(r["start"]) for r in actual]
    check(len(set(keys)) == len(keys), "duplicate preparation")
    check(keys == sorted(expected), "preparation identity")
    for key, record in zip(keys, actual):
        check(record == expected[key], "case fields or provenance")


def quantities(records):
    def key(r):
        moves = r["writer"]["cleanup"]
        by_source = [(i, s) for i, s in enumerate(moves) if s["chart"] == r["source"]]
        return by_source[0] if by_source else (3, None)
    events = [key(r) for r in records]
    positions = Counter(index for index, _ in events)
    actual = [step for _, step in events if step]
    return dict(starts=len(records), source_first=positions[0], source_second=positions[1],
                source_last=positions[2], source_absent=positions[3],
                source_resolves_visible_cover=sum(len(s["covers_before"]) > len(s["covers_after"]) for s in actual),
                source_after_visible_resolution=sum(len(s["covers_before"]) == 1 for s in actual),
                source_followed_by_receiver=positions[0] + positions[1],
                opposite_native=sum(s["opposite"]["legal"] for s in actual),
                opposite_flat=sum(s["opposite"]["keeps_q"] for s in actual),
                opposite_keeps_bound=sum(s["opposite"]["keeps_bound"] for s in actual))


def main(source_dir, output):
    archive = (source_dir / ARCHIVE).read_bytes()
    check(sha256(archive).hexdigest() == PARENT_ARCHIVE, "archive bytes")
    entry, = (e for e in json.loads(gzip.decompress(archive))["entries"] if (e["m"], e["k"]) == (4, 4))
    ids = {tuple(row): i for i, row in enumerate(entry["graph"]["states"])}
    data = lzma.decompress((output / "flat_cover_universe.json.xz").read_bytes())
    actual = json.loads(data)
    expected = {}
    for row, (blank, source, marked) in census().items():
        arms = [expected_arm(row, source, u, v, ids) for u, v in (marked, marked[::-1])]
        check(arms[0]["receiver"] != arms[1]["receiver"], "same destination")
        expected[row] = dict(start=list(row), row=ids[row], blank=blank, source=source, arms=arms,
                             writer=expect_writer(row, source, marked, entry, ids))
    compare_rows(actual, expected)
    original = [r for r in expected.values() if (r["blank"], r["source"]) == (0, 2)]
    counts = quantities(list(expected.values()))
    named = expected[(1, 21, 15, 25)]
    # Independent full group action on the named incidence relation.
    multiplicity = Counter()
    for chart_labels, leaf_labels in product(permutations(CHARTS), permutations(LEAVES)):
        relabeled = [1] * 4
        for j, mask in enumerate(named["start"]):
            for v in LEAVES:
                if mask & (1 << v):
                    relabeled[chart_labels[j]] |= 1 << leaf_labels[v - 1]
        multiplicity[tuple(relabeled)] += 1
    check(set(expected) == set(multiplicity) and set(multiplicity.values()) == {2}, "relabeling multiplicity")
    certificate = json.loads((output / "flat_cover_certificate.json").read_bytes())
    check(certificate == dict(original=quantities(original), all_labels=counts, named=named,
                               archive_sha256=PARENT_ARCHIVE, universe_sha256=sha256(data).hexdigest(),
                               chart_leaf_relabelings=sum(multiplicity.values())), "scientific certificate")

    reject(lambda: compare_rows(actual[:-1], expected), "preparation count")
    reject(lambda: compare_rows([actual[0], *actual[:-1]], expected), "duplicate preparation")
    forged = dict(actual[0], start=[1]*4)
    reject(lambda: compare_rows([forged, *actual[1:]], expected), "preparation identity")
    first = actual[0]
    for defect in ("missed", "extra", "receiver", "bound", "order", "provenance", "addition", "join"):
        wrong = deepcopy(first)
        arm = wrong["arms"][0]
        writer = wrong["writer"]
        if defect == "missed":
            arm["deletions"].pop()
        elif defect == "extra":
            arm["deletions"].append([0, 0, 2])
        elif defect == "receiver":
            arm["receiver"] = wrong["source"]
        elif defect == "bound":
            writer["bound_cover"] = [wrong["blank"], wrong["source"]]
        elif defect == "order":
            writer["cleanup"][0], writer["cleanup"][1] = writer["cleanup"][1], writer["cleanup"][0]
        elif defect == "provenance":
            writer["archived_path"][0] = -1
        elif defect == "addition":
            arm["fixed_paths"].append([[wrong["source"], arm["leaf"]]])
        else:
            arm["double_cut"] = wrong["row"]
        reject(lambda: compare_rows([wrong, *actual[1:]], expected), "case fields or provenance")
    reject(lambda: minimum((1, 1, 1, 1)), "uncovered leaf")
    print(json.dumps(dict(all_labels=counts, original=quantities(original), controls="passed"), sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]))

