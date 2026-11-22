"""Replay different admissible futures of the same retained-tree source deletion."""
from collections import Counter
from fractions import Fraction
from hashlib import sha1, sha256
from itertools import combinations
import json
from pathlib import Path
import sys

import check_geometry_repair as repair


LABELS = repair.LABELS
A, B = repair.A, repair.B
T, ULEAF, R, CHILD = repair.T, repair.ULEAF, repair.R, repair.CHILD
C, D, WITNESS = 1, 4, 17
PAIRS = tuple(combinations(LABELS, 2))
FIXTURE_BLOB = "3324c0b46e09120ae526338444a19070b692d049"


def replay(before, before_work, actions, children, squares):
    """Apply the original atom's leaf, root and unchanged-union conditions."""
    views = list(map(set, before))
    supports = Counter(v for row in views for v in row)
    work = list(map(list, before_work))
    memberships = sum(supports.values())
    for i, v in actions:
        if v == 0 or v not in views[i] or children[v] & views[i] or supports[v] < 2:
            raise ValueError((i, v))
        views[i].remove(v)
        supports[v] -= 1
        for j in LABELS:
            if j != i:
                work[i][j] += squares[v] if v in views[j] else -squares[v]
                work[j][i] = work[i][j]
        yield views, work
    assert memberships - sum(map(len, views)) == len(actions)


def direct_work(state, subtotals, modules):
    rows = tuple(tuple(subtotals[v] if v in vertices else 0 for v in range(1, len(subtotals)))
                 for vertices in map(set, state))
    return modules["work"].construct_response_geometry(LABELS, rows, rows)


def check_native_atom(views, after, action, parents, modules):
    state = tuple(tuple(sorted(view)) for view in views)
    event = modules["atom"].atomic(parents, state, *action)
    modules["verify"].verify_atomic(event)
    assert tuple(map(set, event["after"])) == tuple(map(set, after))
    return {k: v for k, v in event.items() if k not in ("before", "after", "parents")}


def run(destination):
    source_file = Path(repair.__file__).read_bytes()
    assert sha1(f"blob {len(source_file)}\0".encode() + source_file).hexdigest() == FIXTURE_BLOB
    m = repair.modules()
    features, work_before = repair.fixture()
    parents, grades, supports = map(tuple, zip(*features))
    children = [set() for _ in parents]
    subtotals = list(grades)
    keys = [()]
    for v, p in enumerate(parents[1:], start=1):
        assert p < v and supports[v] <= supports[p]
        children[p].add(v)
        keys.append(keys[p] + (v,))
    for v in range(len(parents) - 1, 0, -1):
        subtotals[parents[v]] += subtotals[v]
    squares = [s**2 for s in subtotals]
    before = repair.initial_state(features)
    assert repair.work_for(before, squares) == work_before
    [(after, work_after)] = replay(before, work_before, [(A, T)], children, squares)
    source = check_native_atom(before, after, (A, T), parents, m)
    original_mu, original_edges = repair.edges(work_before)
    mu, after_edges = repair.edges(work_after)
    assert (original_mu, mu) == (repair.MU, repair.MU)

    def observe(work):
        exact = tuple(tuple(map(Fraction, row)) for row in work)
        _, edges = repair.edges(exact)
        p = m["projection"].Payload(repair.SIDE, Fraction(1), LABELS, exact, edges, ())
        return m["carriers"].build_carrier(p)

    def rejection(work):
        try:
            observe(work)
        except ValueError as error:
            return str(error)
        raise AssertionError("expected rejection")

    base_carrier = observe(work_before)
    assert rejection(work_after) == "degree_not_four"
    neighbors = repair.grid()
    baseline_sum = sum(work_before[A][j] for j in neighbors[A])
    after_sum = sum(work_after[A][j] for j in neighbors[A])
    assert (baseline_sum, after_sum) == (4 * mu, 4 * mu + 16)
    assert R in after[A] and CHILD in after[A] and supports[CHILD] == {A}
    assert children[R] == {CHILD}
    assert set(after[A]) - {0, R, CHILD} == set(after[A]) & set(range(6, len(parents)))
    assert all(len(set(LABELS) - supports[v]) <= 2 and not children[v]
               for v in after[A] if v >= 6)

    def depth_moment(views):
        return sum(len(keys[v]) * s for i in LABELS if i != A for v, s in enumerate(subtotals)
                   if v in views[i])

    anchor = depth_moment(after)
    lin = m["lineage"]
    ambient = lin.Carrier("recovery-test", tuple(keys))

    def retained_B(views):
        current = lin.Carrier(ambient.genesis, tuple(keys[v] for v in sorted(views[B])))
        return lin.Pruning(ambient, current).aggregate(grades)

    field = tuple(Fraction(i == A) - Fraction(1, len(LABELS)) for i in LABELS)
    base_field = m["application"].evaluate_field(base_carrier, field)

    def face_value(result):
        return next(str(v) for face, _, v in result.records if set(face) == set(repair.FACE))

    [(fast, fast_work)] = replay(after, work_after, [(B, ULEAF)], children, squares)
    fast_event = check_native_atom(after, fast, (B, ULEAF), parents, m)
    base_B, fast_B = retained_B(after), retained_B(fast)
    assert (base_B[0], fast_B[0]) == (242, 244)
    fast_field = m["application"].evaluate_field(observe(fast_work), field)
    assert (face_value(base_field), face_value(fast_field), anchor - depth_moment(fast)) == ("1/64", "0", 2)

    actions = [tuple(pair) for pair in json.loads(Path(__file__).with_name("geometry_delay_witness.json").read_bytes())]
    assert actions == sorted(actions) and len(actions) == len({v for _, v in actions}) == 100
    assert all(i not in (A, B) and v >= 6 and grades[v] == 1 for i, v in actions)
    assert Counter(i for i, _ in actions) == {i: 6 if i in neighbors[B] else 4
                                              for i in LABELS if i not in (A, B)}
    replay_records, admissions, native_atoms = [], [], []
    for step, (delayed, delayed_work) in enumerate(replay(after, work_after, actions, children, squares), 1):
        one_min, near = repair.edges(delayed_work)
        degrees = Counter(i for edge in near for i in edge)
        if all(degrees[i] == 4 for i in LABELS):
            admissions.append(step)
            observe(delayed_work)
        if step in (1, len(actions)):
            i, v = actions[step - 1]
            previous = list(map(set, delayed))
            previous[i].add(v)
            native_atoms.append(check_native_atom(previous, delayed, (i, v), parents, m))
        replay_records.append((one_min, [degrees[i] for i in LABELS]))
    assert delayed[A] == after[A] and delayed[B] == after[B]
    assert admissions == [100]
    delayed_min, delayed_edges = repair.edges(delayed_work)
    assert (delayed_min, delayed_edges) == (mu + 4, original_edges)
    assert retained_B(delayed) == base_B and anchor - depth_moment(delayed) == 100
    delayed_carrier = observe(delayed_work)
    assert base_carrier.baseline == delayed_carrier.baseline
    for attribute in ("labels", "directed_edges", "direction_classes", "cycles", "d4_actions"):
        assert getattr(base_carrier.complex, attribute) == getattr(delayed_carrier.complex, attribute)
    delayed_field = m["application"].evaluate_field(delayed_carrier, field)
    assert delayed_field.records == base_field.records
    for state, reference in ((before, work_before), (after, work_after), (fast, fast_work), (delayed, delayed_work)):
        inherited = direct_work(state, subtotals, m)
        assert inherited.work == tuple(map(tuple, reference)) and m["work"].metric_passes(inherited)

    # Collapse two rows. Until their work reaches zero, an untouched row obstructs degree four.
    frozen_neighbors = {j for j in LABELS if work_after[WITNESS][j] == mu}
    assert len(frozen_neighbors) == 5 and not {C, D} & (frozen_neighbors | {WITNESS, A, B})
    collapse_actions = [(i, v) for i in (C, D) for v in sorted(after[i] - {0}, reverse=True)]
    starting_atoms = []
    counts = Counter()
    for step, (collapsed, collapse_work) in enumerate(replay(after, work_after, collapse_actions, children, squares), 1):
        collapse_min, near = repair.edges(collapse_work)
        d = sum(WITNESS in edge for edge in near)
        counts[d] += 1
        assert collapse_min <= mu and (d >= 5 if collapse_min == mu else d <= 2)
        assert all(collapse_work[WITNESS][j] == mu for j in frozen_neighbors)
        if step in (1, len(after[C])):
            i, v = collapse_actions[step - 1]
            previous = list(map(set, collapsed))
            previous[i].add(v)
            starting_atoms.append(check_native_atom(previous, collapsed, (i, v), parents, m))
    assert collapsed[C] == collapsed[D] == {0}
    assert collapse_work[C][D] == 0 and rejection(collapse_work) == "work_off_diagonal"

    owner = {}
    for v in range(1, len(parents)):
        holders = [i for i in LABELS if v in collapsed[i]]
        owner[v] = next(i for i in (B, A, *holders) if i in holders)
    assert owner[R] == owner[CHILD] == A
    final_actions = [(i, v) for i in LABELS for v in sorted(collapsed[i] - {0}, reverse=True)
                     if owner[v] != i]
    for terminal, terminal_work in replay(collapsed, collapse_work, final_actions, children, squares):
        assert terminal_work[C][D] == 0
    assert terminal[B] == after[B] and terminal[C] == terminal[D] == {0}
    assert retained_B(terminal) == base_B
    assert repair.work_for(terminal, squares) == tuple(map(tuple, terminal_work))
    assert Counter(v for view in terminal for v in view if v) == dict.fromkeys(owner, 1)
    assert rejection(terminal_work) == "work_off_diagonal"
    try:
        next(replay(terminal, terminal_work, [(B, ULEAF)], children, squares))
    except ValueError as error:
        assert error.args == ((B, ULEAF),)
    else:
        raise AssertionError("terminal last-owner deletion was accepted")

    digest = sha256((json.dumps(collapse_actions + final_actions, separators=(",", ":")) + "\n").encode())
    summary = {
        "full_source_row_obstruction": [baseline_sum, after_sum],
        "source_event": [A, T],
        "immediate_recovery": [B, ULEAF],
        "delayed_recovery_actions": len(actions),
        "delayed_admission_steps": admissions,
        "terminal_actions": len(collapse_actions) + len(final_actions),
        "root_only_at": len(collapse_actions),
        "terminal_rejection": "work_off_diagonal",
        "B_root_grade_before_immediate_delayed_terminal": [242, 244, 242, 242],
        "face_invariants_before_immediate_delayed": [face_value(base_field), face_value(fast_field), face_value(delayed_field)],
        "unchanged_delayed_face_records": len(delayed_field.records),
        "delayed_labeled_transport_inputs_identical": True,
        "remote_depth_moment_debit_immediate_delayed": [2, 100],
    }
    certificate = {
        **summary, "work_before": work_before, "work_after": work_after, "work_delayed": delayed_work,
        "source_atom": source, "fast_atom": fast_event, "tested_delayed_atoms": native_atoms,
        "delayed_prefix_minima_and_degrees": replay_records, "delayed_actions": actions,
        "collapse_atoms": starting_atoms, "collapse_witness_degrees": dict(counts),
        "collapse_and_terminal_actions_sha256": digest.hexdigest(),
        "terminal_support": [sorted(v) for v in terminal],
    }
    raw = (json.dumps(certificate, sort_keys=True, indent=2) + "\n").encode()
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "geometry_delay_certificate.json").write_bytes(raw)
    return {**summary, "certificate_sha256": sha256(raw).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), indent=2, sort_keys=True))
