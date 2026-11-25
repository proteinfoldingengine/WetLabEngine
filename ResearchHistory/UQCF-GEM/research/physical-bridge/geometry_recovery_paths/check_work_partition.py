"""Read the two existing replay certificates and rebuild the complete pair partition."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys


def rebuild(original, odd):
    features = original["fixture"]
    totals = [grade for _, grade, _ in features]
    for v in range(len(features) - 1, 0, -1):
        totals[features[v][0]] += totals[v]
    views = [{v for v, (_, _, holders) in enumerate(features) if i in holders} for i in range(25)]
    chosen = [row["raw_leaf"] for row in odd["sites"]]
    end = [members - {v} for members, v in zip(views, chosen, strict=True)]
    old = original["work_tables"][0]
    old_edges = set(map(tuple, original["before_edges"]))
    counts = Counter()
    zero_partners = []

    def distance(x, y):
        return sum(totals[v] ** 2 for v in x ^ y)

    for i, j in combinations(range(25), 2):
        assert distance(views[i], views[j]) == old[i][j]
        gain = distance(end[i], end[j]) - old[i][j]
        assert gain in (0, 2) and ((i, j) in old_edges) == (old[i][j] == 1984)
        counts[(i, j) in old_edges, gain] += 1
        if i == 0 and gain == 0:
            zero_partners.append(j)
    a, b = views[0], views[12]
    original_even = original["source"]["leaf"]
    assert chosen[0] not in b and original_even not in b
    after_unit = distance(a - {chosen[0]}, b)
    after_two = distance(a - {original_even}, b)
    assert after_two == original["work_tables"][1][0][12]
    def retained_root(state):
        amount = 0
        for v, (_, grade, _) in enumerate(features):
            while v not in state[12]:
                v = features[v][0]
            if v == 0:
                amount += grade
        return amount

    single_source = [[a - {source}, *views[1:]] for source in (chosen[0], original_even)]
    root_readings = [retained_root(state) for state in (views, *single_source)]
    assert root_readings[0] == odd["initial"]["B_root"]
    return {
        "old_minimum_edges": {"gain_0": counts[True, 0], "gain_2": counts[True, 2]},
        "other_pairs": {"gain_0": counts[False, 0], "gain_2": counts[False, 2]},
        "zero_gain_partners_of_0": zero_partners,
        "pair_0_1": [old[0][1], distance(end[0], end[1])],
        "pair_0_7": [old[0][7], distance(end[0], end[7])],
        "pair_0_12_source_only": [old[0][12], after_unit, after_two],
        "root_12_source_only": root_readings,
    }


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled.")
    original, odd, destination = map(Path, sys.argv[1:])
    result = rebuild(json.loads(original.read_bytes()), json.loads(odd.read_bytes()))
    raw = json.dumps(result, sort_keys=True, indent=2) + "\n"
    destination.write_text(raw)
    print(raw, end="")
