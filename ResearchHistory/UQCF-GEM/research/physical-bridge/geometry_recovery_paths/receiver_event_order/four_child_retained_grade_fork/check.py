"""Reproduce the four-child two-history comparison using the archived producer."""
import argparse
from collections import Counter
from functools import cache
from itertools import combinations, groupby
import json
from pathlib import Path
import sys


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("historical_checkout", type=Path)
parser.add_argument("--raw", type=Path)
args = parser.parse_args()
demos = args.historical_checkout.resolve() / "ResearchHistory/UQCF-GEM/demos"
sys.path[:0] = [str(demos / "v16.53-four-child-boundary"),
                str(demos / "v16.26-consistency-increment-law")]
import engine
import producer
import verifier

children = producer.layout(producer.Q)[0]


@cache
def route(start):
    count = len(start)
    target = verifier.profile_check(producer.Q, count, list(start))
    assert target == [producer.coordinate(start, children)]
    path = producer.normalize(list(start), producer.Q, count, target)
    _, _, end = verifier.model(producer.Q, target, count)
    verifier.path_check(producer.Q, count, target, path, list(start), end)
    return target[0], tuple(tuple(row) for row in path)


def holders(start, tip):
    return tuple(index for index, mask in enumerate(start) if mask & (1 << tip))


@cache
def cut(start, source, site):
    views = [[v for v in range(5) if mask & (1 << v)] for mask in start]
    atom = engine.atomic([-1, 0, 0, 0, 0], views, source, site)
    updated = tuple(sum(1 << v for v in view) for view in atom["after"])
    return updated, atom["tau_before"], atom["tau_after"]


def local_history(path, receiver):
    return [value for value, _ in groupby(row[receiver] for row in path)]


def changed_successor(null, event, receiver):
    for i, prior in enumerate(null[:-1]):
        for j, sourced in enumerate(event[:-1]):
            if prior == sourced and null[i + 1] != event[j + 1]:
                yield (i, j, local_history(null[:i + 1], receiver)
                       == local_history(event[:j + 1], receiver))


family = [item for item in verifier.expected_specs() if item[0] == "R"]
assert family == [item for item in producer.specs() if item[0] == "R"]
counts = Counter()
categories = Counter()
raw = []
for _, k, *roots in family:
    start = tuple(verifier.raw_roots(k, roots))
    null_target, null = route(start)
    for receiver in range(k):
        for first, second in combinations(children, 2):
            hidden = (1 << first) | (1 << second)
            if (start[receiver] | null[-1][receiver]) & hidden:
                continue
            if holders(start, first) != holders(start, second):
                continue
            for site in children:
                sources = holders(start, site)
                if site in (first, second) or len(sources) < 2:
                    continue
                for source in sources:
                    if source == receiver:
                        continue
                    updated, before, after = cut(start, source, site)
                    event_target, event = route(updated)
                    assert (before, after) == (null_target, event_target)
                    counts["eligible"] += 1
                    if not event[-1][receiver] & hidden:
                        continue
                    counts["positive"] += 1
                    common = set(null).intersection(event)
                    forks = list(changed_successor(null, event, receiver))
                    matching = any(match for _, _, match in forks)
                    counts["joint_reunion"] += bool(common)
                    counts["different_next_move_at_same_state"] += bool(forks)
                    counts["same_local_history_at_fork"] += matching
                    counts["shared_full_atlas"] += (31,) * k in common
                    counts["transient_null_exposure"] += any(row[receiver] & hidden for row in null)
                    categories[k, before, after, bool(forks), matching] += 1
                    raw.append({"start": start, "receiver": receiver, "hidden": [first, second],
                                "source": source, "site": site, "targets": [before, after],
                                "fork_indices_and_local_match": forks})

fork = (31, 17)
actual, _, target = cut((31, 9), 0, 3)
assert actual == (23, 9)
null_target, null = route((31, 9))
event_target, event = route(actual)
assert (null_target, event_target, target) == (1, 2, 2)
assert null[-2] == event[-2] == fork
assert local_history(null[:-1], 1) == local_history(event[:-1], 1) == [9, 11, 15, 31, 29, 25, 17]
assert cut(fork, 0, 4) == (event[-1], 1, 2)
assert cut(fork, 1, 4) == (null[-1], 1, 1)
restart_target, restart = route(fork)
assert restart_target == 1 and restart[-1] == null[-1]
try:
    producer.normalize(list(fork), producer.Q, 2, [2])
except producer.ConstructionFailure as failure:
    assert str(failure) == "recursive call requires exact parent"
    wrong_restart = str(failure)
else:
    raise AssertionError("a fresh call with the old target unexpectedly succeeded")

result = {
    "original_R_rows": len(family), "counts": dict(sorted(counts.items())),
    "category_columns": ["chart_count", "null_target", "source_target", "has_fork",
                         "has_matching_local_history_at_a_fork", "count"],
    "categories": [list(key) + [count] for key, count in sorted(categories.items())],
    "example": {"null_path": null, "source_path": event, "current_fork": fork,
                "receiver_history_to_fork": local_history(event[:-1], 1),
                "null_target": null_target, "source_target_from_atom": target,
                "fresh_restart_target": restart_target, "fresh_restart_path": restart,
                "fresh_restart_at_target_two": wrong_restart},
}
assert [len(family), counts["eligible"], counts["positive"]] == [2507, 2730, 312]
if args.raw:
    args.raw.write_text(json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n")
print(json.dumps(result, sort_keys=True, indent=2))
