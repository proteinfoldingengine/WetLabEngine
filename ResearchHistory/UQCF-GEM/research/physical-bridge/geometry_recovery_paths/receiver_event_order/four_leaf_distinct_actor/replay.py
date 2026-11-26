"""Run with the pinned WetLabEngine ResearchHistory/UQCF-GEM/demos directory."""
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
from runpy import run_path

NAMES = "AXYZCB"
A, X, Y, Z, C, B = range(len(NAMES))
PARENTS = (-1, 0, 0, 0, 0)
START = ((0, 1, 2, 3), (0, 1), (0, 1), (0, 2), (0, 2, 4), (0, 3, 4))
PREP = (("+", C, 1), ("-", X, 1), ("-", Y, 1), ("-", Z, 2), ("-", C, 4), ("-", B, 3))


def prepare(atom, commands):
    rows = START
    for op, i, leaf in commands:
        if op == "+":
            assert leaf not in rows[i] and PARENTS[leaf] in rows[i]
            rows = tuple(tuple(sorted((*row, leaf))) if j == i else row
                         for j, row in enumerate(rows))
        else:
            rows = tuple(map(tuple, atom(PARENTS, rows, i, leaf)["after"]))
    return rows


def next_states(atom, rows):
    result = {}
    for i, row in enumerate(rows):
        for leaf in row:
            if not leaf:
                continue
            try:
                receipt = atom(PARENTS, rows, i, leaf)
            except ValueError as exc:
                if str(exc) != "same union":
                    raise
            else:
                result[i, leaf] = tuple(map(tuple, receipt["after"]))
    return result


def transpose(rows):
    return tuple(sum(1 << i for i, row in enumerate(rows) if leaf in row)
                 for leaf in range(1, len(PARENTS)))


def swap_source_leaves(rows):
    swap = {1: 2, 2: 1}
    return tuple(tuple(sorted(swap.get(v, v) for v in row)) for row in rows)


def check_original(atom):
    for count in (5, 6):
        before = prepare(atom, PREP[:count])
        after = next_states(atom, before)
        assert before[C] == (0, 1, 2) and swap_source_leaves(before) == before
        both_source = []
        remote_endpoints = []
        for first, other in ((1, 2), (2, 1)):
            arm = after[A, first]
            moves = next_states(atom, arm)
            assert arm[C] == before[C]
            assert {leaf for i, leaf in moves if i == C} == {other}
            non_source = set(k for k in moves if k[0] != A)
            expected = {(C, other)} if count == 6 else {(C, other), (B, 3)}
            assert non_source == expected
            retained = moves[C, other]
            assert retained[C] == (0, first)
            overlap = (set(START[C]) & set(retained[C])) - {0}
            assert len(overlap) == first - 1
            remote_endpoints.append(retained)
            both_source.append(moves[A, other])
            if count == 6:
                assert set(moves) == {(A, other), (C, other)}
                assert all(not next_states(atom, end) for end in moves.values())
            print(count, "edits; A withdraws", first, "non-A options",
                  sorted((NAMES[i], leaf) for i, leaf in non_source),
                  "C retains", retained[C][1:])
        assert both_source[0] == both_source[1]
        assert both_source[0][C] == before[C]
        assert swap_source_leaves(remote_endpoints[0]) == remote_endpoints[1]


def census():
    # Distances count single incidence changes. Any target with nonempty columns
    # is attainable at this distance by adding new memberships before deleting.
    source = 1 << A
    receiver = 1 << C
    masks = range(1, 1 << len(NAMES))
    source_masks = [m for m in masks if m & source and m != source]
    start = transpose(START)

    def removable(mask):
        return mask if mask.bit_count() > 1 else 0

    # Group columns 3 and 4 by the two pieces needed in either source arm.
    # Multiplicity retains every labelled preparation in the exact count.
    background = Counter()
    for third, fourth in product(masks, repeat=2):
        common_actors = removable(third) | removable(fourth)
        cost = (third ^ start[2]).bit_count() + (fourth ^ start[3]).bit_count()
        background[bool(common_actors & receiver), common_actors & ~source, cost] += 1

    tested = 0
    successes = [Counter(), Counter()]
    for first, second in product(source_masks, repeat=2):
        arms = ((removable(first ^ source), removable(second)),
                (removable(first), removable(second ^ source)))
        menus = [{i for i, m in enumerate(arm) if m & receiver} for arm in arms]
        split = bool(menus[0] and menus[1] and menus[0].isdisjoint(menus[1]))
        other_actors = (arms[0][0] | arms[0][1] | arms[1][0] | arms[1][1]) & ~source
        pair_cost = (first ^ start[0]).bit_count() + (second ^ start[1]).bit_count()
        for (c_has_common, common_remote, bg_cost), multiplicity in background.items():
            tested += multiplicity
            if c_has_common or not split:
                continue
            successes[0][pair_cost + bg_cost] += multiplicity
            if (other_actors | common_remote) == receiver:
                successes[1][pair_cost + bg_cost] += multiplicity
    assert tested == 31**2 * 63**2
    print("Eligible prepared states:", tested)
    for i, label in enumerate(("disjoint nonempty C menus", "also forces non-A actor C")):
        costs = successes[i]
        print(label, "total", sum(costs.values()), "minimum edits", min(costs),
              "minimizing preparations", costs[min(costs)])
    assert [min(c) for c in successes] == [5, 6]
    # With source columns {A,C}, each other column either omits C or is {C}.
    # In the actor-forcing case each other column must be a singleton.
    assert [sum(c.values()) for c in successes] == [32**2, 6**2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demos", type=Path)
    engine = parser.parse_args().demos / "v16.26-consistency-increment-law" / "engine.py"
    check_original(run_path(str(engine))["atomic"])
    census()
