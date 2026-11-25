"""Reproduce same-start, equal-unit source alternatives through two historical callers."""
import argparse
from collections import Counter
from contextlib import ExitStack
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
import lzma
import os
from pathlib import Path
import sys
from unittest.mock import patch

from check_receiver_command import FIXTURE, PINS, SCI, hash_blob
from check_fixed_geometry_source_gain import commands_by_row, commands_by_column, raw, traced_run

FOUR = SCI / "demos/v16.53-four-child-boundary"
FOUR_PINS = {
    "producer": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "feasibility": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "cover": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "verifier": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "coverage": "e90576a0285357f62ca2f9d9cac872b2a226e823",
}
HIST = "e61d5b0e827f7b412824ad46021e2ad6cc6f7875"
STAR = (-1, 0, 0, 0, 0)
SOURCE = 2
LABELS = range(4)
CHILDREN = range(1, 5)
WITNESS = (2, 4, 12, 6)  # per-child bit masks using actual palette positions
CONTROL = (2, 4, 6, 6)


def members(mask, bits):
    return [i for i in bits if mask & (1 << i)]


def state_masks(views):
    return [sum(1 << v for v in y) for y in views]


def atlas(columns):
    return [[0] + [v for v, col in enumerate(columns, 1) if col & (1 << j)] for j in LABELS]


def specimen(views):
    return ["R", 4, *[[j for j, y in enumerate(views) if v in y] for v in CHILDREN]]


def source_event(modules, views, cut):
    event = modules["atom"].atomic(STAR, views, SOURCE, cut)
    modules["verify"].verify_atomic(event)
    return event


def geometry(f, modules, mode):
    features, target = f.fixture()
    parents, grades, supports = zip(*features)
    rows = f.initial_state(features)
    subtotal = list(grades)
    for v in range(len(features)-1, 0, -1):
        subtotal[parents[v]] += subtotal[v]
    squares = [s*s for s in subtotal]
    mu = f.MU
    _, old_edges = f.edges(target)
    assert all(any(i not in (f.A, j) and k not in (f.A, j) for i, k in old_edges)
               for j in f.LABELS if j != f.A)
    if mode == "incidence":
        assert f.work_for(rows, squares) == target
        menu = commands_by_column(rows, parents)
    else:
        menu = commands_by_row(rows, parents)
        masks = [sum(1 << v for v in row) for row in rows]
        weight_classes = {}
        for v, w in enumerate(squares):
            weight_classes[w] = weight_classes.get(w, 0) | (1 << v)
    domain = []
    for i, v in menu:
        if i != f.A:
            continue
        if mode == "incidence":
            distances = {j: target[i][j] + squares[v] * (1 if j in supports[v] else -1)
                         for j in f.LABELS if j != i}
        else:
            changed = masks[i] ^ (1 << v)
            distances = {j: sum(w * ((changed ^ masks[j]) & group).bit_count()
                                for w, group in weight_classes.items())
                         for j in f.LABELS if j != i}
        ties = [j for j, d in distances.items() if d == mu]
        below = [j for j, d in distances.items() if d < mu]
        domain.append([v, subtotal[v], ties, below])
        if v != f.T:
            assert len(f.ALL - supports[v]) <= 2 and len(ties) <= 2
    possible = [v for v, _, ties, _ in domain if len(ties) + 1 >= 4]
    assert possible == [f.T]
    traces = {}
    for cut in (f.T, 662):
        with patch.object(f, "T", cut):
            rec = traced_run(f, modules, features, target)
        traces[str(cut)] = {key: rec[key] for key in
                           ("calls", "verified", "candidate_return", "available", "exit",
                            "aggregate_before_second", "same_work_object")}
    assert traces["1"]["verified"] == [[0, 1], [12, 2]]
    assert traces["662"]["verified"] == [[0, 662]] and traces["662"]["exit"] == "singleton guard"
    return domain, dict(source_menu=len(domain), possible_cross_editor_sources=possible,
                        ordinary_postcut_tie_histogram=dict(sorted(Counter(len(r[2]) for r in domain if r[0]!=f.T).items())),
                        traces=traces)


def true_caller(r, verifier, views):
    identity = specimen(views)
    with patch.object(r, "specs", return_value=[identity]):
        record, = r.produce()["records"]
    assert record["status"] == "ok", record
    assert record["identity"] == identity and record["start"] == state_masks(views)
    verifier.path_check(r.Q, 4, record["q"], record["path"], record["start"], record["end"])
    assert any(x[0] != record["start"][0] for x in record["path"])
    return record


def direct_census(r, verifier, modules):
    @lru_cache(maxsize=None)
    def outcome(post):
        actual = true_caller(r, verifier, post)
        return actual["q"][0], actual["end"]

    universe = {}
    for columns in product(range(2, 16, 2), repeat=4):
        views = atlas(columns)
        before = r.coordinate(state_masks(views), list(CHILDREN))
        moves = []
        for cut, col in enumerate(columns, 1):
            if SOURCE not in members(col, LABELS) or col.bit_count() < 2:
                continue
            event = source_event(modules, views, cut)
            q, end = outcome(tuple(tuple(row) for row in event["after"]))
            assert event["h_before"] == before and event["h_after"] == q
            moves.append([cut, q, end])
        universe[columns] = [before, moves]
    return universe


@lru_cache(maxsize=None)
def independent_endpoint(q):
    # Direct lexicographic definition. No producer feasibility or dynamic program.
    assignment = next(row for row in product(LABELS, repeat=4) if len(set(row)) == q)
    return [1 + sum(1 << v for v, owner in enumerate(assignment, 1) if owner == j) for j in LABELS]


def subset_cover(masks):
    full = 15
    for n in range(1, 4):
        for selected in combinations(masks, n):
            reach = 0
            for mask in selected:
                reach |= mask
            if reach == full:
                return n
    raise ValueError("Outside covering domain")


def independent_census():
    # Enumerate the three entire chart masks first, independently of the column-product grammar.
    records = {}
    for a, c, d in product(range(16), repeat=3):
        if a | c | d != 15:
            continue
        columns = tuple(2*bool(a & bit) + 4*bool(c & bit) + 8*bool(d & bit) for bit in (1,2,4,8))
        before = subset_cover((a, c, d))
        moves = []
        for pos in range(4):
            bit = 1 << pos
            if not c & bit:
                continue
            after_c = c ^ bit
            if a | after_c | d != 15:
                continue
            q = subset_cover((a, after_c, d))
            moves.append([pos+1, q, independent_endpoint(q)])
        records[columns] = [before, moves]
    return records


def package_rows(records):
    return [[list(columns), *records[columns]] for columns in sorted(records)]


def summary(records):
    total_pairs = 0
    alternatives = Counter()
    distinct = []
    post_inputs = set()
    for columns, (before, moves) in records.items():
        for cut, _, _ in moves:
            post = list(columns)
            post[cut-1] ^= 1 << SOURCE
            post_inputs.add(tuple(post))
        for (u, p, x), (v, q, y) in combinations(moves, 2):
            total_pairs += 1
            alternatives[tuple(sorted((p, q)))] += 1
            assert (p != q) == (x[0].bit_count() != y[0].bit_count())
            if p != q:
                assert before == 2 and {p, q} == {2,3}
                distinct.append([list(columns), u, v])
    return dict(preparations=len(records), legal_source_arms=sum(len(s[1]) for s in records.values()),
                unique_postcut_inputs=len(post_inputs), unordered_pairs=total_pairs, separating_pairs=len(distinct),
                pair_target_histogram={f"{p},{q}":n for (p,q),n in sorted(alternatives.items())},
                separating_prior_count=len({tuple(x[0]) for x in distinct})), sorted(distinct)


def unit_grade(lineage, view):
    key = lambda v: () if v == 0 else (v,)
    fine = lineage.Carrier("ordered-star", tuple(key(v) for v in range(5)))
    local = lineage.Carrier(fine.genesis, tuple(key(v) for v in view))
    return [int(x) for x in lineage.Pruning(fine, local).aggregate((1,)*5)]


def witness_arm(r, verifier, modules, cols, cut, catalog, supplied_q=None):
    initial = atlas(cols)
    event = source_event(modules, initial, cut)
    post = event["after"]
    identity = specimen(post)
    encoded = []
    observed = {}
    top_inputs = []
    original_encode, original_coordinate, original_normalize = r.encode_roots, r.coordinate, r.normalize

    def encode(*args):
        obj = original_encode(*args)
        encoded.append(obj)
        return obj

    def coordinate(obj, children):
        value = original_coordinate(obj, children)
        if "first_profile" not in observed:
            observed["first_profile"] = value
            observed["coordinate_received_encoded_object"] = obj is encoded[0]
            if supplied_q is not None:
                return supplied_q
        return value

    def normalize(obj, tree, k, q, *args):
        if not top_inputs:
            top_inputs.append([obj is encoded[0], list(q)])
        return original_normalize(obj, tree, k, q, *args)

    class P1Probe(Exception):
        pass

    lineage = modules["lineage"]
    with ExitStack() as stack:
        for obj, name, replacement in ((r,"encode_roots",encode), (r,"coordinate",coordinate),
                (r,"normalize",normalize), (r,"specs",lambda:[identity])):
            stack.enter_context(patch.object(obj,name,replacement))
        stack.enter_context(patch.object(lineage.Pruning, "aggregate", side_effect=P1Probe))
        try:
            unit_grade(lineage, post[SOURCE])
        except P1Probe:
            probe_live = True
        else:
            raise AssertionError("Dead P1 read probe")
        row, = r.produce()["records"]
    if supplied_q is not None:
        assert row["status"] == "interrupted" and row["message"] == "recursive call requires exact parent"
        assert row["partial_path"] == [row["start"]]
        return dict(true_q=observed["first_profile"], overridden_q=supplied_q,
                    exit=row["status"], reason=row["message"], completed_receiver_write=False)
    assert row["status"] == "ok"
    assert observed["coordinate_received_encoded_object"] and top_inputs == [[True, row["q"]]]
    peak = verifier.path_check(r.Q, 4, row["q"], row["path"], row["start"], row["end"])
    receiver_trace = [s[0] for s in row["path"]]
    first = next(i for i, s in enumerate(receiver_trace) if s != receiver_trace[0])
    first_bit = receiver_trace[0] ^ receiver_trace[first]
    assert first_bit.bit_count() == 1
    return dict(cut=cut, before=state_masks(initial), after_source=state_masks(post), q=row["q"][0],
                before_cover=event["h_before"], atomic_strict=event["trigger"], receiver_trace=receiver_trace,
                end=row["end"], path=row["path"], path_peak=peak, first_receiver_step=first,
                first_receiver_leaf=first_bit.bit_length()-1,
                prior_receiver_unit_root=unit_grade(lineage, initial[0])[0],
                immediate_receiver_unit_root=unit_grade(lineage, post[0])[0],
                source_unit_root=[unit_grade(lineage, views[SOURCE])[0] for views in (initial,post)],
                final_receiver_unit_root=unit_grade(lineage, members(row["end"][0],range(5)))[0],
                archived_specimen=raw(identity) in catalog, profile_input_is_encoding=True,
                normalize_input_is_encoding=True, p1_probe_live=probe_live,
                p1_called_in_normalizer=False)


def audit_red(rows, geometry_domain, reference_rows, reference_geometry, verifier, r, modules, witness, catalog):
    def check(r, g):
        if r != reference_rows or g != reference_geometry:
            raise ValueError("Independent canonical universe mismatch")
    check(rows, geometry_domain)
    n = next(i for i, row in enumerate(rows) if len(row[2]) > 1)
    bad_value = json.loads(json.dumps(rows[n]))
    bad_value[2][0][1] += 1
    controls = {"omitted":(rows[:-1], geometry_domain), "duplicate":(rows+[rows[-1]], geometry_domain),
                "substituted":(rows[:n]+[rows[n+1]]+rows[n+1:], geometry_domain),
                "wrong_profile":(rows[:n]+[bad_value]+rows[n+1:], geometry_domain),
                "false_source_identity":(rows, [[0,*geometry_domain[0][1:]]]+geometry_domain[1:])}
    rejected = []
    for name, (bad_rows, bad_geometry) in controls.items():
        try:
            check(bad_rows, bad_geometry)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    try:
        verifier.path_check(((),)*4, 4, [2], [[1,1,1,1]], [1,1,1,1], [1,1,1,1])
    except ValueError:
        rejected.append("uncovered_state")
    else:
        raise AssertionError("Uncovered state accepted")
    try:
        source_event(modules, atlas(WITNESS), 2)
    except ValueError:
        rejected.append("delete_last_holder")
    else:
        raise AssertionError("Source deleted its private child")
    arm = witness[0]
    bad_path = arm["path"][:1] + arm["path"][2:]
    try:
        verifier.path_check(r.Q, 4, [arm["q"]], bad_path, arm["path"][0],arm["end"])
    except ValueError:
        rejected.append("two_incidence_jump")
    else:
        raise AssertionError("Invalid two-edit transition accepted")
    identity = specimen([members(mask, range(5)) for mask in arm["after_source"]])
    if raw(identity) in catalog:
        raise AssertionError("New specimen falsely credited to the historical campaign")
    rejected.append("false_archived_provenance")
    return sorted(rejected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--mode", choices=("incidence","bitsets"), required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    os.chdir(args.sources)
    for name, expected in FOUR_PINS.items():
        assert hash_blob((FOUR/(name+".py")).read_bytes()) == expected
    assert hash_blob(FIXTURE.read_bytes()) == PINS[FIXTURE]
    sys.path[:0] = [str(FOUR.resolve()), str(FIXTURE.parent.resolve())]
    import producer as r
    import verifier
    import check_geometry_repair as f
    modules = f.modules()
    geom, geo_note = geometry(f, modules, args.mode)
    if args.mode == "incidence":
        all_states = direct_census(r, verifier, modules)
    else:
        all_states = independent_census()
    rows = package_rows(all_states)
    stats, distinct = summary(all_states)
    assert len(distinct) == 96
    inventory = {raw(x) for x in r.specs()}
    witness = [witness_arm(r, verifier, modules, WITNESS, v, inventory) for v in (3,4)]
    neutral = [witness_arm(r, verifier, modules, CONTROL, v, inventory) for v in (3,4)]
    assert neutral[0]["end"] == neutral[1]["end"]
    swapped = tuple(sum(1 << (3 if j==0 else 0 if j==3 else j) for j in members(col,LABELS)) for col in WITNESS)
    permuted = [witness_arm(r, verifier, modules, swapped, v, inventory) for v in (3,4)]
    assert [s["end"] for s in permuted] == [s["end"] for s in witness]
    assert all(s["end"][3] == 1 for s in permuted)
    stale = witness_arm(r, verifier, modules, WITNESS, 3, inventory, supplied_q=2)
    reference_geometry, _ = geometry_domain_only(f)
    reds = audit_red(rows,geom,package_rows(independent_census()),reference_geometry,verifier,r,modules,witness,inventory)
    domain = raw(dict(columns_before_moves=rows,chart0_source_menu=geom,separating_pairs=distinct)) + b"\n"
    (out/"matched_source_universe.json.xz").write_bytes(lzma.compress(domain, preset=6))
    cert = dict(schema=1, inherited=HIST, original_geometry=geo_note, star_domain=stats,
                witness=witness, same_target_control=neutral, relabeled_control=permuted,
                stale_target_control=stale, rejected=reds, universe_sha256=sha256(domain).hexdigest())
    (out/"matched_source_certificate.json").write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"mode":args.mode,"geometry_source_count":len(geom),**stats,"universe_sha256":cert["universe_sha256"]}))


def geometry_domain_only(f):
    features, target = f.fixture()
    rows = f.initial_state(features)
    parents, grades, holders = zip(*features)
    totals = list(grades)
    for v in reversed(range(1,len(features))):
        totals[parents[v]] += totals[v]
    local = set(rows[f.A])
    other = set().union(*(set(row) for row in rows[1:]))
    allowed = sorted((local & other) - {parents[v] for v in local} - {0})
    result = []
    for v in allowed:
        values = {j:target[0][j]+totals[v]**2*(1 if j in holders[v] else -1) for j in range(1,25)}
        result.append([v,totals[v],[j for j in values if values[j]==f.MU],[j for j in values if values[j]<f.MU]])
    return result, allowed


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    main()
