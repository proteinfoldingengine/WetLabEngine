#!/usr/bin/env python3
"""Independent bounded C3 reconstruction: bit-mask relations, no producer import.

The reachability key is a set of full states, NOT a claimed deficit. All
possible history deficits are annotated after the observational graph exists.
This is a same-author algorithmic cross-check, not independent peer review.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
from typing import Any


class CheckError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        _require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def loads(text: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_object)
    except json.JSONDecodeError as exc:
        raise CheckError('Malformed JSON') from exc


def _same(actual: Any, expected: Any, path: str = '$') -> None:
    _require(type(actual) is type(expected), 'Wrong type at ' + path)
    if isinstance(expected, dict):
        _require(actual.keys() == expected.keys(), 'Wrong keys at ' + path)
        for key in expected:
            _same(actual[key], expected[key], path + '.' + key)
    elif isinstance(expected, list):
        _require(len(actual) == len(expected), 'Missing/extra records at ' + path)
        for i, value in enumerate(expected):
            _same(actual[i], value, path + '[' + str(i) + ']')
    else:
        _require(actual == expected, 'Wrong value at ' + path)


def _letters(mask: int, alphabet: str) -> str:
    return ''.join(letter for bit, letter in enumerate(alphabet) if mask & (1 << bit))


def reconstruct(n: int) -> dict[str, Any]:
    _require(type(n) is int and n in (1, 2), 'Only the frozen N=1,2 slice is allowed')
    limit = 1 << (5 + n)
    # Exhaust the complete full-state universe, not a supplied list of cases.
    admissible = set()
    observed = {}
    for state in range(limit):
        if state.bit_count() < 2:
            continue
        hit_sizes = [h.bit_count() for h in range(limit)
                     if (h & 3) and (h & 6) and (h & 5) and (h & state)]
        tau = min(hit_sizes)
        if not 3 <= tau <= 4:
            continue
        admissible.add(state)
        miss = tuple(sum(1 for root in (3, 6, 5, state) if not (h & root))
                     for h in range(1, 32) if h.bit_count() <= 4)
        observed[state] = (state & 31, tau, True, miss)
    blocks = {}
    for state in admissible:
        blocks.setdefault(observed[state], set()).add(state)
    commands = tuple(sign + c for sign in ('+', '-') for c in 'abcde')
    relation = {}
    for command in commands:
        bit = 1 << ('abcde'.index(command[1]))
        rows = {(s, s) for s in admissible}  # Every command may reject.
        for state in admissible:
            member = bool(state & bit)
            changes = (command[0] == '+' and not member) or (command[0] == '-' and member)
            target = state ^ bit
            if changes and target in admissible:
                rows.add((state, target))
        relation[command] = rows

    initial = frozenset(24 | (z << 5) for z in range(1 << n))
    _require(initial <= admissible, 'Prepared initial state invalid')
    known = {initial}
    edges = set()
    # Relational image + observation partition, synchronous least fixed point.
    while True:
        expanded = set(known)
        for belief in known:
            for command, rows in relation.items():
                image = {target for source, target in rows if source in belief}
                for block in blocks.values():
                    successor = frozenset(image & block)
                    if successor:
                        edges.add((belief, command, successor))
                        expanded.add(successor)
        if expanded == known:
            break
        known = expanded

    # D did not participate in construction above. Now consider ALL histories.
    labels = {belief: set() for belief in known}
    labels[initial].add(0)
    while True:
        changed = False
        for source, _, target in edges:
            cores = {s & 31 for s in target}
            _require(len(cores) == 1, 'Observation block mixes projected supports')
            deficit = max(0, 2 - next(iter(cores)).bit_count())
            values = {max(d, deficit) for d in labels[source]}
            old_size = len(labels[target])
            labels[target].update(values)
            changed |= len(labels[target]) != old_size
        if not changed:
            break
    records = {}
    palette = 'uv'[:n]
    all_hidden = sorted(_letters(z, palette) for z in range(1 << n))
    for belief in known:
        _require(len(labels[belief]) == 1, 'A knowledge state has nonunique history deficit')
        d = next(iter(labels[belief]))
        core = _letters(next(iter(belief)) & 31, 'abcde')
        hidden = tuple(sorted(_letters(s >> 5, palette) for s in belief))
        # Test the claimed threshold formula only after direct reconstruction.
        _require(hidden == tuple(z for z in all_hidden if len(z) >= d),
                 'The claimed history-fiber theorem fails in this slice')
        records[belief] = (core, hidden, d)
    ordered = sorted(records.values())
    _require(len(set(ordered)) == len(known), 'Canonical records collide')
    ids = {record: i for i, record in enumerate(ordered)}
    canonical_edges = sorted((records[a], c, records[b]) for a, c, b in edges)
    return {'spectator_palette': palette,
            'nodes': [{'id': ids[r], 'core4': r[0], 'hidden_subsets': list(r[1]), 'D': r[2]}
                      for r in ordered],
            'edges': [{'source': ids[a], 'command': c, 'target': ids[b]}
                      for a, c, b in canonical_edges]}


def _counterexamples() -> list[dict[str, Any]]:
    # Fixed, explicit refutations retained from the original evidence contract.
    rows = [('attempt', 'de', 1, ['', 'u', 'uv', 'v'], ['u', 'uv', 'v']),
            ('forget', 'de', 0, ['u', 'uv', 'v'], ['', 'u', 'uv', 'v']),
            ('boolean', '', 1, ['uv'], ['u', 'uv', 'v']),
            ('identity', 'e', 1, ['u', 'uv', 'v'], ['u', 'uv'])]
    return [{'mutant': kind, 'counterexample': {
        'mutant': kind, 'core4': core, 'D': d,
        'explicit_hidden_subsets': actual, 'predicted': wrong}}
        for kind, core, d, actual, wrong in rows]


def verify(report: Any) -> dict[str, Any]:
    graphs = [reconstruct(1), reconstruct(2)]
    expected = {
        'schema': 'c3-core-probe-replay-v1',
        'source': {
            'proof_commit': 'e7dc592d0f98121c7c232f33018a0a199c30ba8e',
            'proof_blob': 'd619932c44d051f2a0c698365709d6f42e02f078',
            'replay_scope_commit': '5a993893a99d6cab75c0a2fae4170cad61838117'},
        'status': 'BOUNDED_REPLAY_PASS_NOT_INDEPENDENT_REVIEW',
        'graphs': graphs, 'rejected_estimators': _counterexamples()}
    _same(report, expected)
    return {'status': 'ALGORITHMICALLY_INDEPENDENT_BOUNDED_PASS',
            'nodes': [len(g['nodes']) for g in graphs],
            'edges': [len(g['edges']) for g in graphs],
            'full_assignments_enumerated': [64, 128],
            'deficit_used_to_generate_beliefs': False,
            'independent_mathematical_review': False,
            'scope': 'fixed triangle; root-4 core edits; N=1,2 only'}


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: c3_core_probe_independent.py EVIDENCE.json', file=sys.stderr)
        return 2
    try:
        result = verify(loads(Path(sys.argv[1]).read_text(encoding='utf-8')))
    except (CheckError, OSError) as exc:
        print('REJECTED: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
