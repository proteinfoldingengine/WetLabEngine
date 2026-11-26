"""Classify the possible next native edits after a shared tip is withdrawn."""
from collections import Counter
from functools import cache
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations, product


@cache
def primitive_ops(state, n):
    result = set()
    for chart, mask in enumerate(state):
        for tip in range(1, n + 1):
            present = bool(mask & (1 << tip))
            if not present or any(j != chart and m & (1 << tip) for j, m in enumerate(state)):
                result.add((chart, tip, "withdraw" if present else "add"))
    return result


def classification():
    """Enumerate root-sharing covers by assigning one nonempty holder set per tip."""
    result = []
    for k, n in ((2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 3)):
        totals = Counter()
        for supports in product(range(1, 1 << k), repeat=n):
            before = tuple(1 + sum(1 << i for i, h in enumerate(supports, 1) if h & (1 << c))
                           for c in range(k))
            for receiver in range(k):
                missing = [i for i in range(1, n + 1) if not before[receiver] & (1 << i)]
                for tip, support in enumerate(supports, 1):
                    if not support & (1 << receiver):
                        continue
                    for source in range(k):
                        if source == receiver or not support & (1 << source):
                            continue
                        after = before[:source] + (before[source] ^ (1 << tip),) + before[source + 1:]
                        moves = primitive_ops(after, n) - {(source, tip, "add")}
                        for size in range(1, len(missing) + 1):
                            for hidden in combinations(missing, size):
                                accepting = {(receiver, h, "add") for h in hidden}
                                predicted = (k == 2 and len(hidden) == n - 1
                                             and before[receiver] == 1 + (1 << tip))
                                assert moves and (moves <= accepting) == predicted
                                totals["tests"] += 1
                                totals["positive"] += predicted
        result.append([k, n, totals["tests"], totals["positive"]])
    return result


def example(demos, engine, producer, verifier):
    spec = spec_from_file_location("source_star_original_push", demos / "v16.23-overlap-descent/engine.py")
    projection = module_from_spec(spec)
    spec.loader.exec_module(projection)
    parents = (-1, 0, 0, 0)
    full = (0, 1, 2, 3)
    grades = ((1, 1, 3, 1), (1, 3, 1, 1))
    before = (15, 9)
    after = (7, 9)
    def sites(mask):
        return tuple(i for i in full if mask & (1 << i))
    def emitted(state, c, tip):
        atom = engine.atomic(parents, [sites(mask) for mask in state], c, tip)
        return tuple(sum(1 << i for i in row) for row in atom["after"])
    def records(mask):
        addresses = sites(mask)
        return [tuple(zip(addresses, map(int, projection.push(parents, full, addresses, g))))
                for g in grades]
    assert emitted(before, 0, 3) == after
    prior = records(after[1])
    assert prior == [((0, 5), (3, 1))] * 2
    options = []
    arms = [set(), set()]
    for chart, tip, kind in sorted(primitive_ops(after, 3)):
        assert kind == "add"
        new = after[:chart] + (after[chart] | (1 << tip),) + after[chart + 1:]
        assert emitted(new, chart, tip) == after
        output = records(new[1])
        if new != before:
            for i in range(2):
                arms[i].add(output[i])
        options.append([chart, tip, new, output])
    assert arms[0].isdisjoint(arms[1]) and len(arms[0]) == len(arms[1]) == 2
    assert primitive_ops(before, 3) == {(0,3,"withdraw"),(1,3,"withdraw"),(1,1,"add"),(1,2,"add")}
    try:
        emitted(after, 1, 3)
    except ValueError as error:
        assert str(error) == "same union"
    else:
        raise AssertionError("Receiver can withdraw its last copy")
    assert emitted(before, 1, 3) == (15, 1)
    counts = Counter()
    traces = []
    for ordered_tips in permutations((1, 2, 3)):
        def encode(mask):
            return 1 + sum(1 << i for i, t in enumerate(ordered_tips, 1) if mask & (1 << t))
        def decode(mask):
            return 1 + sum(1 << t for i, t in enumerate(ordered_tips, 1) if mask & (1 << i))
        for order in permutations((0, 1)):
            pair = []
            for state, target in ((after, 2), (before, 1)):
                ordered = [encode(mask) for mask in state]
                path = producer.normalize(ordered, producer.T, 2, [target], order=order)
                # Original verifier's canonical endpoint is in the original index order.
                indexed = [[row[i] for i in order] for row in path]
                _, _, end = verifier.model(producer.T, [target], 2)
                verifier.path_check(producer.T, 2, [target], indexed, indexed[0], end)
                physical_path = [tuple(map(decode, row)) for row in path]
                assert physical_path[0] == state
                if len(path) == 1:
                    first = "stop"
                elif physical_path[1][1] & 6:
                    first = "receiver acquires"
                else:
                    assert state == after and physical_path[1] == before
                    first = "undo"
                pair.append(first)
                traces.append([ordered_tips, order, target, physical_path])
            counts[tuple(pair)] += 1
    return {
        "bounded_columns": ["charts","tips","eligible_role_and_hidden_sets","dichotomy_cases"],
        "bounded": classification(), "source_event": [before, after], "prior_addressed_P1": prior,
        "next_move_columns": ["chart","added_tip","new_atlas","receiver_P1_by_grade_arm"],
        "next_moves": options, "acquiring_output_sets_disjoint": True,
        "caller_columns": ["source_first_action","null_first_action","order_pairs"],
        "original_caller_first_actions": [list(k) + [v] for k, v in sorted(counts.items())],
    }, traces
