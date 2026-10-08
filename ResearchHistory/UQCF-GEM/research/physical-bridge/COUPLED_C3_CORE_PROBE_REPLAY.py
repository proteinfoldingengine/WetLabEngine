#!/usr/bin/env python3
"""Exact, bounded C3 core-probe review replay; standard library only.

Roots 1-3 stay {a,b},{b,c},{a,c}. Root 4 receives +/- core commands.
All actual full supports and hidden subsets are enumerated directly. The
history-deficit formula is compared with the result, never used to generate
possible hidden worlds. Fixed-point coverage is for this slice only, not
all four-root edits, all spectator palettes, or independent peer review.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
from typing import Any

CORE = 'abcde'
TRIANGLE = (frozenset('ab'), frozenset('bc'), frozenset('ac'))
COMMANDS = tuple(sign + label for sign in ('+', '-') for label in CORE)
SOURCE = {
    'proof_commit': 'e7dc592d0f98121c7c232f33018a0a199c30ba8e',
    'proof_blob': 'd619932c44d051f2a0c698365709d6f42e02f078',
    'replay_scope_commit': '5a993893a99d6cab75c0a2fae4170cad61838117',
}


class ReplayError(ValueError):
    """A claim, coverage record, or supplied report failed exact checking."""


def subsets(palette: str) -> tuple[str, ...]:
    return tuple(''.join(s) for size in range(len(palette) + 1)
                 for s in combinations(palette, size))


@lru_cache(maxsize=None)
def full_tau(core4: str, hidden: str) -> int | None:
    roots = TRIANGLE + (frozenset(core4 + hidden),)
    palette = ''.join(sorted(set().union(*roots)))
    for candidate in subsets(palette):
        if all(set(candidate) & root for root in roots):
            return len(candidate)
    return None


def admissible(core4: str, hidden: str) -> bool:
    if len(set(core4 + hidden)) < 2:
        return False
    value = full_tau(core4, hidden)
    return value is not None and 3 <= value <= 4


@lru_cache(maxsize=None)
def observation(core4: str, hidden: str) -> tuple[Any, ...]:
    roots = TRIANGLE + (frozenset(core4 + hidden),)
    # All nonempty core miss-count coordinates through order four.
    miss = tuple(sum(not (set(h) & root) for root in roots)
                 for h in subsets(CORE) if 1 <= len(h) <= 4)
    return (core4, full_tau(core4, hidden),
            all(len(root) >= 2 for root in roots), miss)


def proposed(core4: str, command: str) -> str | None:
    sign, label = command
    present = label in core4
    if (sign == '+' and present) or (sign == '-' and not present):
        return None  # No actual toggle satisfies the membership condition.
    support = set(core4)
    if sign == '+':
        support.add(label)
    else:
        support.remove(label)
    return ''.join(sorted(support))


def outcomes(core4: str, hidden: str, command: str) -> tuple[tuple[Any, ...], ...]:
    if not admissible(core4, hidden):
        raise ReplayError('Oracle called on an inadmissible state')
    result = [observation(core4, hidden)]  # Rejection is ALWAYS allowed.
    successor = proposed(core4, command)
    if successor is not None and admissible(successor, hidden):
        result.append(observation(successor, hidden))
    return tuple(result)


def build_graph(n: int, mutant: str | None = None) -> dict[str, Any]:
    if n not in (1, 2):
        raise ReplayError('Frozen replay supports only N=1 or N=2')
    if mutant not in (None, 'attempt', 'forget', 'boolean', 'identity'):
        raise ReplayError('Unknown deliberately incorrect estimator')
    worlds = tuple(sorted(subsets('uv'[:n])))
    # Node: current core, explicit compatible hidden subsets, retained deficit.
    initial = ('de', worlds, 0)
    queue = deque([initial])
    seen = {initial}
    edges = set()
    while queue:
        core4, belief, deficit = node = queue.popleft()
        prediction = tuple(z for z in worlds if len(z) >= deficit)
        if mutant == 'identity' and deficit == 1 and 'v' in prediction:
            prediction = tuple(z for z in prediction if z != 'v')
        if prediction != belief:
            raise ReplayError(json.dumps({
                'mutant': mutant, 'core4': core4, 'D': deficit,
                'explicit_hidden_subsets': belief, 'predicted': prediction,
            }, sort_keys=True))
        for command in COMMANDS:
            groups: dict[tuple[Any, ...], set[str]] = defaultdict(set)
            for hidden in belief:
                for observed in outcomes(core4, hidden, command):
                    groups[observed].add(hidden)
            for observed, surviving in groups.items():
                next_core = observed[0]
                next_deficit = max(deficit, 0, 2 - len(next_core))
                if mutant == 'attempt':
                    intended = proposed(core4, command)
                    if intended is not None:
                        next_deficit = max(deficit, 0, 2 - len(intended))
                elif mutant == 'forget':
                    next_deficit = max(0, 2 - len(next_core))
                elif mutant == 'boolean':
                    next_deficit = int(next_deficit > 0)
                successor = (next_core, tuple(sorted(surviving)), next_deficit)
                edges.add((node, command, successor))
                if successor not in seen:
                    seen.add(successor)
                    queue.append(successor)
    ordered = sorted(seen)
    ids = {node: i for i, node in enumerate(ordered)}
    return {
        'spectator_palette': 'uv'[:n],
        'nodes': [dict(id=ids[node], core4=node[0], hidden_subsets=list(node[1]),
                       D=node[2]) for node in ordered],
        'edges': [dict(source=ids[a], command=command, target=ids[b])
                  for a, command, b in sorted(edges)],
    }


def check_graph(report: dict[str, Any]) -> None:
    palette = report.get('spectator_palette')
    if palette not in ('u', 'uv'):
        raise ReplayError('Wrong or missing frozen palette')
    expected = build_graph(len(palette))
    if report != expected:
        raise ReplayError('Exact graph mismatch: missing, extra, changed, or reordered record')


def make_report() -> dict[str, Any]:
    graphs = [build_graph(n) for n in (1, 2)]
    rejected = []
    for mutant in ('attempt', 'forget', 'boolean', 'identity'):
        try:
            build_graph(2, mutant)
        except ReplayError as exc:
            rejected.append({'mutant': mutant, 'counterexample': json.loads(str(exc))})
        else:
            raise ReplayError('Incorrect estimator was not rejected: ' + mutant)
    return {'schema': 'c3-core-probe-replay-v1', 'source': SOURCE,
            'status': 'BOUNDED_REPLAY_PASS_NOT_INDEPENDENT_REVIEW',
            'graphs': graphs, 'rejected_estimators': rejected}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path, help='Freshly reconstruct and check saved JSON')
    args = parser.parse_args()
    expected = make_report()
    if args.check is not None:
        supplied = json.loads(args.check.read_text(encoding='utf-8'))
        if supplied != expected:
            raise ReplayError('Saved evidence differs from fresh exact reconstruction')
        print('Exact evidence readback PASS; independent review remains unfulfilled.')
    else:
        print(json.dumps(expected, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
