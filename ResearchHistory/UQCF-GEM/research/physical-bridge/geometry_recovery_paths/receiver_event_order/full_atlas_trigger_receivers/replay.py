"""Replay the full star and the archived atomic routine on a sufficient restriction."""
from collections import Counter
from hashlib import sha1, sha256
from itertools import combinations
from pathlib import Path
import json
import runpy
import sys

ARMS = ((41, 217, 278, 454), (91, 157, 338, 404))
TARGETS = set(ARMS[0] + ARMS[1])
LINE = {i for i in range(121) if (i // 11 + 3 * (i % 11)) % 11 == 0}
RECEIVERS = (15, 5)
PIVOTS = (278, 338)
KEEP_ON_LINE = {18: {91, 454}, 50: {217, 157}, 82: {41, 404}}
PINS = ('45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b',
        'c10ac57f988a439144e21898bd2b33ece0838a9b',
        'b18f52109ccff9c7dc77542d3b8f3e5d5989102a')


def original(path, expected):
    raw = Path(path).read_bytes()
    if sha1(b'blob ' + str(len(raw)).encode() + bytes(1) + raw).hexdigest() != expected:
        raise ValueError('Unexpected input source')
    return runpy.run_path(path)


def row_at(holds, chart):
    return {a for a, charts in holds.items() if chart in charts}


def remove(holds, chart, leaf):
    remaining = holds[leaf] - {chart}
    assert chart in holds[leaf] and remaining
    holds[leaf] = remaining


def prepare(orbit):
    start = {a: {j for j in range(121) if mask >> j & 1}
             for a, mask in enumerate(orbit, 1)}
    holds = start.copy()
    anchors = {}
    for h in sorted(LINE):
        leaf = next(a for a, owners in start.items()
                    if owners & LINE == {h} and not owners.intersection(RECEIVERS)
                    and a not in TARGETS)
        anchors[h] = leaf
        for chart in sorted(start[leaf] - {h}):
            remove(holds, chart, leaf)
    for chart in sorted(set(range(121)) - {0, *RECEIVERS}):
        incident = row_at(start, chart) & TARGETS
        if chart in LINE:
            keep = KEEP_ON_LINE.get(chart, set())
        else:
            arms = [sorted(incident.intersection(arm) - set(PIVOTS)) for arm in ARMS]
            n = min(map(len, arms))
            keep = set(arms[0][:n] + arms[1][:n])
        assert keep <= incident
        for leaf in sorted(incident - keep):
            remove(holds, chart, leaf)
    assert all(owners & LINE for owners in holds.values())
    assert [holds[p] for p in PIVOTS] == [{0, 15}, {0, 5}]
    assert all(row_at(start, j) == row_at(holds, j) for j in (0, *RECEIVERS))
    return start, holds, anchors


def required(holds):
    """Here every singleton chart is necessary, and together they suffice."""
    mandatory = set.union(*(owners for owners in holds.values() if len(owners) == 1))
    assert all(owners & mandatory for owners in holds.values())
    return mandatory


def work(holds):
    rows = [sum(1 << a for a in row_at(holds, i)) for i in range(121)]
    return [4 * (a ^ b).bit_count() for a, b in combinations(rows, 2)]


def signature(values):
    return sha256(json.dumps(values, separators=(',', ':')).encode()).hexdigest()


def chart_views(holds, charts, leaves):
    ids = {a: pos for pos, a in enumerate(leaves, 1)}
    return [(0,) + tuple(ids[a] for a in leaves if j in holds[a]) for j in charts]


def audit(start, ready, anchors, atomic, push):
    selected = sorted(LINE | set(RECEIVERS))
    subset = sorted(TARGETS | set(anchors.values()))
    flat = (-1,) + (0,) * len(subset)
    all_leaves = tuple(sorted(ready))
    full = (-1,) + (0,) * len(all_leaves)
    ambient = tuple(range(len(full)))
    grades = (1,) + (2,) * len(all_leaves)
    native_checks = 0

    def advance(holds, actor, leaf):
        nonlocal native_checks
        before = required(holds)
        views = chart_views(holds, selected, subset)
        entry = atomic(flat, views, selected.index(actor), subset.index(leaf) + 1)
        remove(holds, actor, leaf)
        after = required(holds)
        assert entry['after'] == [list(v) for v in chart_views(holds, selected, subset)]
        assert (entry['tau_before'], entry['tau_after']) == (len(before), len(after))
        assert (entry['h_before'], entry['h_after']) == (len(before), len(after))
        assert entry['trigger'] == (not all(owners & before for owners in holds.values()))
        native_checks += 1
        return [len(before), len(after), entry['trigger']]

    def record(holds, actor):
        leaves = sorted(row_at(holds, actor))
        pin = push(full, ambient, (0, *leaves), grades)[0]
        assert pin == 1 + 2 * (968 - len(leaves))
        return [len(leaves), int(pin)]

    def blocked(holds, actor, leaf):
        for parents, charts, leaves in [(flat, selected, subset), (full, list(range(121)), all_leaves)]:
            try:
                atomic(parents, chart_views(holds, charts, leaves), charts.index(actor),
                       leaves.index(leaf) + 1)
            except ValueError as exc:
                assert str(exc) == 'same union'
            else:
                raise AssertionError('Expected loss of the final copy')

    assert required(ready) == LINE
    preparations = [(j, a) for a in start for j in sorted(start[a] - ready[a])]
    initial_menu = Counter()
    paired_events = []
    positive_actors = Counter()
    for address, owners in ready.items():
        if len(owners) <= 1:
            continue
        for j in owners:
            if owners & LINE != {j}:
                initial_menu['zero'] += 1
            else:
                initial_menu['positive'] += 1
                positive_actors[j] += 1
                if len(owners) == 2:
                    initial_menu['one_new_compulsory_chart'] += 1
                    paired_events.append((j, address, next(iter(owners - {j}))))
    assert sorted(paired_events) == [(0, 278, 15), (0, 338, 5)]
    traces, endings, probes = [], [], []
    for k, arm in enumerate(ARMS):
        state = ready.copy()
        events = []
        pair_signatures = [signature(work(state))]
        for a in arm:
            events.append(advance(state, 0, a))
            pair_signatures.append(signature(work(state)))
        assert events == [[11, 11, False], [11, 11, False], [11, 12, True], [12, 12, False]]
        assert required(state) == LINE | {RECEIVERS[k]}
        traces.append(dict(events=events, pair_signatures=pair_signatures,
                           minimum_cover=sorted(required(state)), source=record(state, 0)))
        endings.append(state)
        local = {}
        for i, (r, p) in enumerate(zip(RECEIVERS, PIVOTS)):
            entry = {'before': record(state, r)}
            if k == i:
                blocked(state, r, p)
                entry.update(outcome='same union', after=record(state, r))
            else:
                trial = state.copy()
                receipt = advance(trial, r, p)
                assert receipt == [12, 12, False]
                entry.update(outcome='permitted', after=record(trial, r))
            local[str(r)] = entry
        probes.append(local)

    W = list(map(work, endings))
    assert W[0] == W[1] and len(W[0]) == 7260
    assert all(row_at(endings[0], j) == row_at(endings[1], j) for j in range(1, 121))
    joins = []
    for i in range(2):
        joined = endings[i].copy()
        receipts = [advance(joined, 0, a) for a in ARMS[1-i]]
        assert sum(e[2] for e in receipts) == 1 and len(required(joined)) == 13
        joins.append((joined, receipts))
    assert joins[0][0] == joins[1][0]

    def terminal_examples(state, r):
        cover = required(state)
        mine = row_at(state, r)
        force = [a for a in mine if state[a] & cover == {r}]
        choices = sorted(mine - set(force))
        if r not in cover:
            return [0]
        assert len(force) == 1 and len(choices) == 199
        counts = []
        for n in range(200):
            keep = set(force + choices[:n])
            # One designated surviving old holder per leaf defines a legal thinning.
            dest = {a: (r if a in keep else min((owners & cover) - {r}))
                    for a, owners in state.items()}
            assert set(dest.values()) == cover
            counts.append(sum(h == r for h in dest.values()))
        assert counts == list(range(1, 201))
        return [min(counts), max(counts)]

    return dict(preparatory_withdrawals=len(preparations),
                distinct_preparatory_actors=len({j for j, _ in preparations}),
                completely_original_chart_rows=[j for j in range(121) if row_at(start,j)==row_at(ready,j)],
                singleton_anchors=anchors, starting_menu=initial_menu, arms=traces,
                trigger_positive_withdrawals_by_chart=positive_actors,
                unique_new_chart_events=sorted(paired_events),
                full_equal_pairs=len(W[0]), local_withdrawal_probes=probes,
                terminal_leaf_count_ranges=[{r: terminal_examples(state, r) for r in RECEIVERS}
                                            for state in endings],
                join_receipts=[x[1] for x in joins], join_cover=sorted(required(joins[0][0])),
                archived_successful_restriction_calls=native_checks,
                archived_rejected_full_calls=2)


if __name__ == '__main__':
    orbit, native, p1 = [original(path, pin) for path, pin in zip(sys.argv[1:], PINS, strict=True)]
    origin, common, markers = prepare(orbit['orbit'])
    print(json.dumps(audit(origin, common, markers, native['atomic'], p1['push']),
                     sort_keys=True, indent=2))
