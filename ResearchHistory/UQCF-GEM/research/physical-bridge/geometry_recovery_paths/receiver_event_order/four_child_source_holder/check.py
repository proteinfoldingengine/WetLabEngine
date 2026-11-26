"""Replay remote withdrawal permissions, the eight deferred forks, and child-order controls."""
import argparse
from collections import Counter, deque
from functools import cache
from hashlib import sha256
from itertools import permutations
import json
import linecache
import lzma
from pathlib import Path
import sys


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("historical_checkout", type=Path)
parser.add_argument("--raw", type=Path)
args = parser.parse_args()
demos = args.historical_checkout.resolve() / "ResearchHistory/UQCF-GEM/demos"
sys.path[:0] = [str(demos / "v16.53-four-child-boundary"),
                str(demos / "v16.26-consistency-increment-law")]
import cover
import engine
import producer
import verifier
import source_star

tips = (1, 2, 3, 4)
parents = (-1, 0, 0, 0, 0)


@cache
def height(state):
    return verifier.profile_check(producer.Q, len(state), list(state))[0]


@cache
def route(state):
    target = [height(state)]
    assert producer.coordinate(state, tips) == target[0]
    path = producer.normalize(list(state), producer.Q, len(state), target)
    _, _, end = verifier.model(producer.Q, target, len(state))
    verifier.path_check(producer.Q, len(state), target, path, list(state), end)
    return tuple(map(tuple, path))


def holders(state, tip):
    return tuple(i for i, mask in enumerate(state) if mask & (1 << tip))


def private_tips(state, chart):
    return tuple(tip for tip in tips if holders(state, tip) == (chart,))


@cache
def withdrawals(state):
    views = [[v for v in range(5) if mask & (1 << v)] for mask in state]
    accepted = {}
    for chart, sites in enumerate(views):
        for tip in sites[1:]:
            try:
                event = engine.atomic(parents, views, chart, tip)
            except ValueError as error:
                if str(error) != "same union":
                    raise
                continue
            new = tuple(sum(1 << v for v in sites) for sites in event["after"])
            assert (height(state), height(new)) == (event["tau_before"], event["tau_after"])
            accepted[chart, tip] = new
    return accepted


@cache
def neighbors(state):
    """All one-tip changes on this fixed covered star."""
    result = set(withdrawals(state).values())
    for chart, mask in enumerate(state):
        for tip in tips:
            if mask & (1 << tip):
                continue
            added = state[:chart] + (mask | (1 << tip),) + state[chart + 1:]
            assert withdrawals(added)[chart, tip] == state
            result.add(added)
    return tuple(sorted(result))


def audit_source_campaign():
    specs = [row for row in verifier.expected_specs() if row[0] == "R"]
    assert specs == [row for row in producer.specs() if row[0] == "R"]
    full_jumps = []
    count = 0
    for _, k, *roots in specs:
        state = tuple(verifier.raw_roots(k, roots))
        assert state == tuple(producer.encode_roots(k, roots))
        before = withdrawals(state)
        for (source, tip), after in before.items():
            count += 1
            if (height(state), height(after)) != (k - 1, k):
                continue
            other, = (c for c in holders(state, tip) if c != source)
            assert not private_tips(state, other)
            assert private_tips(after, other) == (tip,)
            assert all(private_tips(state, c) for c in range(k) if c != other)
            remote_before = {key for key in before if key[0] != source}
            remote_after = {key for key in withdrawals(after) if key[0] != source}
            assert remote_before - remote_after == {(other, tip)}
            assert not remote_after - remote_before and state[other] == after[other]
            full_jumps.append([state, source, tip, other])
    return len(specs), count, full_jumps


def exact_paths_to(end):
    """Breadth-first distances and one shortest path to end in its exact-cover stratum."""
    queue = deque([end])
    toward_end = {end: None}
    while queue:
        state = queue.popleft()
        for new in neighbors(state):
            if height(new) == height(end) and new not in toward_end:
                toward_end[new] = state
                queue.append(new)
    return toward_end


def shortest(start, toward_end):
    path = [start]
    while toward_end[path[-1]] is not None:
        path.append(toward_end[path[-1]])
    return path


def complement_trace(start):
    """Observe the actual complementary-cover edits in the source-prepared R call."""
    trace = []
    cover_file = str(Path(cover.__file__).resolve())
    def capture(frame, event, argument):
        if event != "call" or frame.f_code.co_name != "edit" or frame.f_code.co_filename != cover_file:
            return
        caller = frame.f_back
        trace.append([frame.f_locals["i"] + 1, frame.f_locals["x"], frame.f_locals["add"],
                      linecache.getline(cover_file, caller.f_lineno).strip()])
    previous_hook = sys.getprofile()
    sys.setprofile(capture)
    try:
        path = producer.normalize(list(start), producer.Q, len(start), [height(start)])
    finally:
        sys.setprofile(previous_hook)
    assert tuple(map(tuple, path)) == route(start)
    return trace


def prioritized(mask, order):
    return 1 + sum(1 << i for i, tip in enumerate(order, 1) if mask & (1 << tip))


def physical(mask, order):
    return 1 + sum(1 << tip for i, tip in enumerate(order, 1) if mask & (1 << i))


def order_control(start, event, receiver, hidden):
    """Reindex into the original caller and undo that reindexing on its output."""
    contrasts = Counter()
    for order in permutations(tips):
        null_start = tuple(prioritized(m, order) for m in start)
        src_start = tuple(prioritized(m, order) for m in event)
        assert tuple(physical(m, order) for m in src_start) == event
        null = physical(route(null_start)[-1][receiver], order)
        src = physical(route(src_start)[-1][receiver], order)
        contrasts[(bool(src & hidden), bool(null & hidden))] += 1
    return [contrasts[True, False], contrasts[False, False],
            contrasts[True, True], contrasts[False, True]]


def analyze_deferred(row, event, path, toward_end):
    start = tuple(row["start"])
    source, tip = row["source"], row["site"]
    assert row["fork_indices_and_local_match"] == [[0, 1, True]]
    assert path[:2] == (event, start) and height(start) == 2
    traces = complement_trace(event)
    sweep = "if x in A and i!=owners[x]:edit(i,x,False)"
    assert traces[0] == [tip, source, False, sweep] and traces[1][2:] == [False, sweep]
    restoring = [s for s in neighbors(start) if height(s) == 3]
    assert restoring == [event] and all(height(s) == 2 for s in path[1:-1])
    direct = shortest(event, toward_end)
    assert direct[-1] == path[-1]
    distance_bound = sum((a ^ b).bit_count() for a, b in zip(event, path[-1]))
    assert len(direct) - 1 == distance_bound
    verifier.path_check(producer.Q, len(event), [3], list(map(list, direct)), list(event), list(path[-1]))
    return {"start": start, "source_command": [source, tip], "receiver": row["receiver"],
            "hidden": row["hidden"], "program_path": path, "first_two_complement_edits": traces[:2],
            "only_immediate_restoration": restoring[0], "shortest_exact_path": direct,
            "hamming_bound": distance_bound}


input_path = Path(__file__).resolve().parent.parent / "four_child_retained_grade_fork/positive_rows.json.xz"
input_bytes = input_path.read_bytes()
rows = json.loads(lzma.decompress(input_bytes))
family_rows, atom_count, full_jumps = audit_source_campaign()
end = (7, 9, 17)
toward_end = exact_paths_to(end)
all_exact = {tuple(verifier.raw_roots(row[1], row[2:])) for row in verifier.expected_specs()
             if row[0] == "R" and row[1] == 3
             and height(tuple(verifier.raw_roots(row[1], row[2:]))) == 3}
assert set(toward_end) == all_exact
matches = Counter()
orders = Counter()
shortest_lengths = Counter()
deferred = []
comparisons = []
for row in rows:
    state = tuple(row["start"])
    source, tip, receiver = row["source"], row["site"], row["receiver"]
    event = withdrawals(state)[source, tip]
    path = route(event)
    has_fork = bool(row["fork_indices_and_local_match"])
    remaining = holders(event, tip)
    role = "multiple holders" if len(remaining) > 1 else ("same chart" if remaining == (receiver,) else "other chart")
    matches[len(state), height(event), has_fork, role] += 1
    hidden_mask = sum(1 << v for v in row["hidden"])
    first_hidden, second_hidden = row["hidden"]
    assert tip not in row["hidden"] and not state[receiver] & hidden_mask
    assert holders(state, first_hidden) == holders(state, second_hidden)
    assert not route(state)[-1][receiver] & hidden_mask
    assert (path[-1][receiver] & hidden_mask).bit_count() == 1
    order_outcomes = order_control(state, event, receiver, hidden_mask)
    orders[tuple(order_outcomes)] += 1
    if row["targets"] == [2, 3]:
        distance = len(shortest(event, toward_end)) - 1
        assert distance == sum((a ^ b).bit_count() for a, b in zip(event, end))
        shortest_lengths[has_fork, distance, len(path) - 1] += 1
        if has_fork:
            deferred.append(analyze_deferred(row, event, path, toward_end))
    comparisons.append([state, source, tip, receiver, row["hidden"], role, order_outcomes])

example = next(r for r in deferred if r["start"] == (11, 5, 21))
later = example["program_path"][2]
forward = [s for s in neighbors(later) if height(s) == 3 and s != example["program_path"][1]]
assert len(forward) == 2 and height(example["program_path"][3]) == 2
def table(counter):
    return [list(key) + [value] for key, value in sorted(counter.items())]

three_tip, caller_traces = source_star.example(demos, engine, producer, verifier)
raw = {"three_tip_caller_paths": caller_traces,
       "full_jump_columns": ["before", "source", "tip", "new_indispensable_chart"],
       "full_jumps": full_jumps, "deferred": deferred,
       "comparison_columns": ["before", "source", "tip", "receiver", "hidden_tips", "holder_match", "order_counts"],
       "comparisons": comparisons}
raw_bytes = (json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n").encode()
summary = {"three_tip": three_tip, "historical_R_rows": family_rows, "legal_source_withdrawals": atom_count,
           "full_jumps_by_charts": dict(sorted(Counter(len(s) for s, _, _, _ in full_jumps).items())),
           "exact_three_chart_states": len(toward_end), "deferred_cases": len(deferred),
           "positive_comparisons": len(rows), "source_holder_columns": ["charts", "source_cover", "fork", "role", "comparisons"],
           "source_holder_matches": table(matches),
           "distance_columns": ["fork", "shortest_exact", "historical", "comparisons"],
           "distance_counts_for_source_cover_three": table(shortest_lengths),
           "order_columns": ["source_only", "neither", "both", "null_only", "comparisons"],
           "order_counts": table(orders), "example": example, "later_forward_restorations": forward,
           "prior_positive_ledger_sha256": sha256(input_bytes).hexdigest(), "raw_sha256": sha256(raw_bytes).hexdigest()}
if args.raw:
    args.raw.write_bytes(raw_bytes)
print(json.dumps(summary, sort_keys=True, indent=2))
