"""Compare an original local command with the original common-field response."""
import gzip
import hashlib
import itertools
import json
import lzma
import sys
from collections import Counter
from functools import lru_cache

import sympy as sp

import check_active_holder_write as original


X = original.SITES
TREE = original.PARENTS
START = (19, 23, 11)
REMOTE = 3
OWNER = 2
CONSISTENCY = "v16.24-consistency-order/"


def exact_integers(values):
    result = tuple(map(int, values))
    assert all(v == i for v, i in zip(values, result))
    return result


def support(state, site):
    return tuple(i for i, mask in enumerate(state) if mask & (1 << site))


def local_changes(path, site):
    trace = []
    for step, state in enumerate(path):
        members = support(state, site)
        if not trace or trace[-1][1] != members:
            trace.append((step, members))
    return trace


def width_word(trace):
    return tuple(len(members) for _, members in trace)


def command(atom, verifier, state, actor, site):
    before = list(map(original.view, state))
    try:
        response = atom.atomic(TREE, before, actor, site)
    except ValueError as exc:
        assert tuple(map(original.view, state)) == tuple(before)
        return {"accepted": False, "reason": str(exc)}
    verifier.verify_atomic(response)
    assert response["before"] == list(map(list, before))
    return {"accepted": True, "result_at_site": [
        i for i, sites in enumerate(response["after"]) if site in sites]}


def local_test(atom, verifier, row):
    path = row["path"]
    trace = local_changes(path, REMOTE)
    receipts = [command(atom, verifier, path[k], OWNER, REMOTE) for k, _ in trace[:3]]
    return {"local_trace": [[k, "".join(chr(65 + j) for j in members)] for k, members in trace],
            "widths": width_word(trace), "same_C_command_on_separate_copies": receipts,
            "endpoint": row["end"]}


def motif_census(index, atom, verifier):
    results = {name: Counter() for name in ("source_private", "third_private")}
    both = Counter()
    terminals = Counter()
    for source, receiver, third in itertools.permutations(range(3)):
        for triple, double, private_s, private_t in itertools.permutations(X[1:]):
            masks = [1] * 3
            for site, labels in ((triple, (source, receiver, third)), (double, (source, receiver)),
                                 (private_s, (source,)), (private_t, (third,))):
                for label in labels:
                    masks[label] |= 1 << site
            rows = []
            for site in (triple, double):
                after, _, _ = original.delete(atom, verifier, masks, source, site)
                rows.append(index[after][1])
            assert [row["q"] for row in rows] == [[2], [3]]
            differs = []
            for name, site, owner in (("source_private", private_s, source), ("third_private", private_t, third)):
                left, right = (local_changes(row["path"], site) for row in rows)
                low, high = width_word(left), width_word(right)
                assert low == (1, 2, 3, 2, 1)
                results[name]["high_widths_" + "".join(map(str, high))] += 1
                differs.append(low != high)
                if len(high) > 2 and high[2] == 1:
                    results[name]["second_edit_3_vs_1"] += 1
                    same_prefix = left[1][1] == right[1][1]
                    results[name]["also_same_named_prefix"] += same_prefix
                    if owner in right[2][1]:
                        results[name]["original_owner_still_present"] += 1
                        results[name]["also_same_named_prefix_and_owner"] += same_prefix
                        commands = [command(atom, verifier, row["path"][trace[2][0]], owner, site)
                                    for row, trace in zip(rows, (left, right))]
                        assert commands[0]["accepted"] and commands[1] == {"accepted": False, "reason": "same union"}
                elif high != low:
                    assert high == (1,)
            both[str(tuple(differs))] += 1
            pair = [int(any(mask & (1 << private_s) and mask & (1 << private_t) for mask in row["end"]))
                    for row in rows]
            terminals["".join(map(str, pair))] += 1
    assert sum(both.values()) == 144
    for count in results.values():
        assert count["second_edit_3_vs_1"] == 48 and count["also_same_named_prefix"] == 36
        assert count["original_owner_still_present"] == 12 and count["also_same_named_prefix_and_owner"] == 8
    return {"remote_roles": results, "whole_width_word_differs_at_S_T": both,
            "canonical_single_holder_of_both_private_leaves_low_high": terminals}


def check_field(overlap, green, paths):
    states = sorted({tuple(state) for path in paths for state in path})
    masks = sorted({m for state in states for m in state})
    balanced = [tuple(-1 if v == 0 else int(v == site) for v in X) for site in X[1:]]

    @lru_cache(None)
    def solve_view(mask, drive):
        sites = original.view(mask)
        p = (-1,) + (0,) * (len(sites) - 1)
        grade = overlap.push(TREE, X, sites, drive)
        inverse = green.candidate(p)
        assert inverse * green.root_laplacian(p) == sp.eye(len(sites) - 1)
        rhs = sp.Matrix(len(sites) - 1, 1, list(grade[1:]))
        values = (0,) + exact_integers(inverse * rhs)
        return sites, values

    @lru_cache(None)
    def glue_step(sites, values, other_sites, other_values):
        combined = overlap.glue_response(TREE, sites, other_sites, values, other_values)
        return tuple(sorted(set(sites) | set(other_sites))), combined

    for state in states:
        for drive in balanced:
            sites, values = solve_view(state[0], drive)
            for mask in state[1:]:
                sites, values = glue_step(sites, values, *solve_view(mask, drive))
            assert sites == X and values == (0, *drive[1:])
    return {"distinct_visited_cover_states": len(states), "distinct_views": len(masks),
            "basis_size": len(balanced), "full_glued_field_comparisons": len(balanced) * len(states),
            "nonzero_residuals": 0, "unit_root_to_v3_at_v3": 1, "unit_v2_to_v3_drop": 2}


def loss_test(index, atom, verifier, overlap, green):
    rows = []
    source_mask = START[1]
    source_view = original.view(source_mask)
    before = dict(zip(source_view, overlap.push(TREE, X, source_view, (1,) * len(X))))
    for site in (1, 4):
        after, _, _ = original.delete(atom, verifier, START, 1, site)
        keep = original.view(after[1])
        coarse = dict(zip(keep, overlap.push(TREE, source_view, keep, tuple(before.values()))))
        old_minus_coarse = exact_integers([before.get(v, 0) - coarse.get(v, 0) for v in X])
        assert sum(old_minus_coarse) == 0 and old_minus_coarse[site] == 1
        field = (0, *exact_integers(green.candidate(TREE) * sp.Matrix(old_minus_coarse[1:])))
        assert field[REMOTE] == 0 and field[site] == 1
        k, members = local_changes(index[after][1]["path"], REMOTE)[2]
        assert OWNER in members
        receiver = original.view(index[after][1]["path"][k][OWNER])
        local_source = overlap.push(TREE, X, receiver, old_minus_coarse)
        local_field = (0, *exact_integers(green.candidate((-1,) + (0,) * (len(receiver) - 1)) *
                                         sp.Matrix(len(receiver) - 1, 1, list(local_source[1:]))))
        assert local_field[receiver.index(REMOTE)] == 0
        rows.append({"deleted_site": site, "formal_lost_source": old_minus_coarse, "ambient_field": field,
                     "root_to_v3_in_surviving_C": 0})
    return rows


def signed_local_edit(row, step, overlap, green):
    before, after = row["path"][step - 1:step + 1]
    (actor,) = [i for i, (old, new) in enumerate(zip(before, after)) if old != new]
    old, new = original.view(before[actor]), original.view(after[actor])
    holder = original.view(after[OWNER])
    assert before[actor] ^ after[actor] == 1 << REMOTE
    assert before[OWNER] == after[OWNER] and REMOTE in holder
    sign = 1 if REMOTE in new else -1

    def representation(view, grade):
        lifted = dict(zip(view, overlap.push(TREE, X, view, grade)))
        return tuple(lifted.get(v, 0) for v in X)

    def difference(left, right):
        return tuple(a - b for a, b in zip(left, right))

    def edge_drop(grade):
        local = overlap.push(TREE, X, holder, grade)
        rhs = sp.Matrix(len(holder) - 1, 1, list(local[1:]))
        potential = green.candidate((-1,) + (0,) * (len(holder) - 1)) * rhs
        return exact_integers(potential)[holder.index(REMOTE) - 1]

    old_overlap = tuple(sorted(set(holder) & set(old)))
    new_overlap = tuple(sorted(set(holder) & set(new)))
    whole_old = tuple(sorted(set(holder) | set(old)))
    assert whole_old == tuple(sorted(set(holder) | set(new)))
    changed_view_drops, changed_intersection_drops, own_drops = [], [], []
    for vertex in X:
        grade = tuple(int(v == vertex) for v in X)
        delta = difference(representation(new, grade), representation(old, grade))
        duplicate = difference(representation(new_overlap, grade), representation(old_overlap, grade))
        expected = tuple(sign * grade[REMOTE] * (int(v == REMOTE) - int(v == 0)) for v in X)
        assert delta == duplicate == expected
        for v, overlap_v in ((old, old_overlap), (new, new_overlap)):
            union = tuple(a + b - c for a, b, c in zip(
                representation(holder, grade), representation(v, grade), representation(overlap_v, grade)))
            assert union == representation(whole_old, grade)
        own_delta = difference(representation(original.view(after[OWNER]), grade),
                               representation(original.view(before[OWNER]), grade))
        changed_view_drops.append(edge_drop(delta))
        changed_intersection_drops.append(edge_drop(duplicate))
        own_drops.append(edge_drop(own_delta))
    assert changed_view_drops == changed_intersection_drops == [0, 0, 0, sign, 0]
    assert own_drops == [0] * len(X)
    return {"whole_path_step": step, "changing_index": chr(65 + actor), "C_view_mask_on_both_sides": before[OWNER],
            "change_in_view_representative_port_functional": changed_view_drops,
            "change_in_overlap_port_functional": changed_intersection_drops,
            "change_in_Cs_own_port_functional": own_drops, "change_after_overlap_subtraction": 0}


def certificate_crosscheck(endpoint_masks):
    engine = original.historical(CONSISTENCY + "engine.py", "port_consistency")
    data = (original.DEMOS / CONSISTENCY / "evidence/certificates.json.xz").read_bytes()
    cases = json.loads(lzma.decompress(data))["instances"][32]
    assert cases["parents"] == list(TREE) and cases["variant"] == "original"
    samples = {"signed": (1, 0, 1, 1, 0), "nonnegative": (2, 0, 1, 1, 0)}
    result = {}
    for masks in endpoint_masks:
        views = [original.view(mask) for mask in masks]
        matches = [(i, row) for i, row in enumerate(cases["cases"])
                   if set(map(tuple, row["views"])) == set(views)]
        (i, row), = matches
        assert engine.certify(TREE, row["views"]) == row
        distinct = {}
        for name, totals in samples.items():
            grade = engine._local(TREE, totals, X)
            local = [engine._local(TREE, totals, v) for v in views]
            assert all(engine.push(TREE, v, grade) == x for v, x in zip(views, local))
            hits = [bad for c, bad in row["samples"] if tuple(c) == totals]
            assert len(hits) <= 1
            distinct[name] = {"ambient_grade": grade, "A_root_grade": local[0][0], "bad_mask_entries": hits}
        catalog = {tuple(c): bad for c, bad in row["samples"]}
        for total, a, b in itertools.product(range(3), repeat=3):
            observed = catalog.get((total, 0, a, b, 0))
            if total >= a + b:
                expected = 0
            elif i == 174 and total >= max(a, b):
                expected = 3
            else:
                expected = None
            assert observed == expected
        result[str(i)] = {"accepted_sample_count": len(row["samples"]), "checks": distinct,
                          "subfamily_triples_checked": 27}
    assert set(result) == {"59", "174"}
    for i, signed, positive, bad in (("59", -1, 0, []), ("174", 0, 1, [3])):
        checks = result[i]["checks"]
        assert checks["signed"]["A_root_grade"] == signed and checks["signed"]["bad_mask_entries"] == bad
        assert checks["nonnegative"]["A_root_grade"] == positive and checks["nonnegative"]["bad_mask_entries"] == [0]
    return {"v1624_archive_sha256": hashlib.sha256(data).hexdigest(), "cases_zero_based": result}


def main():
    sources = {**original.SOURCES, CONSISTENCY + "engine.py": "666617d33bf8925699d0dc440565588a5e40e57e",
               CONSISTENCY + "evidence/certificates.json.xz": "0202d032c55db9c7cbfe45487679118ccaa39d98"}
    for path, expected in sources.items():
        raw = (original.DEMOS / path).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == expected
    sys.path.insert(0, str(original.DEMOS / original.STAR))
    star = original.historical(original.STAR + "producer.py", "port_star")
    check = original.historical(original.STAR + "verifier.py", "port_check")
    atom = original.historical(original.ATOM + "engine.py", "port_atom")
    verifier = original.historical(original.ATOM + "verify.py", "port_atom_verify")
    overlap = original.historical("v16.23-overlap-descent/engine.py", "port_overlap")
    green = original.historical("v16.22-response-selection-closure/engine.py", "port_green")
    raw = (original.DEMOS / original.ARCHIVE).read_bytes()
    archived = json.loads(gzip.decompress(raw))["records"]
    archived_r = [x for x in archived if x["identity"][0] == "R"]
    fresh = [x for x in star.produce()["records"] if x["identity"][0] == "R"]
    assert [x["identity"] for x in archived] == star.specs()
    assert json.loads(json.dumps(fresh)) == archived_r
    index = {tuple(r["start"]): (i, r) for i, r in enumerate(archived) if r["identity"][0] == "R"}
    assert len(index) == len(archived_r) == 2507
    for row in archived_r:
        check.path_check(star.Q, row["k"], row["q"], row["path"], row["start"], row["end"])
    traces = {}
    terminal = {}
    secondary = {}
    for name, site in (("no_deletion", None), ("delete_v1", 1), ("delete_v4", 4)):
        state = START if site is None else original.delete(atom, verifier, START, 1, site)[0]
        number, row = index[state]
        record = local_test(atom, verifier, row)
        record["archive_row_zero_based"] = number
        traces[name] = record
        local_second = local_changes(row["path"], REMOTE)[2][0]
        secondary[name] = {"second_v3_edit": signed_local_edit(row, local_second, overlap, green)}
        if site is not None:
            secondary[name]["same_index_A_at_whole_step_four"] = signed_local_edit(row, 4, overlap, green)
        masks = row["end"]
        terminal[name] = {"minimum_holders_for_v2_v3": star.coordinate(masks, [2, 3]),
                          "holders_of_both": [j for j, m in enumerate(masks) if m & 12 == 12]}
        receipts = record["same_C_command_on_separate_copies"]
        assert [r["accepted"] for r in receipts] == [False, True, site != 4]
        assert receipts[0]["reason"] == "same union"
        if site == 4:
            assert receipts[2]["reason"] == "same union"
    assert [traces[k]["archive_row_zero_based"] for k in traces] == [2468, 1782, 2466]
    assert [terminal[k]["minimum_holders_for_v2_v3"] for k in traces] == [1, 1, 2]
    alt = [[19,21,11], [27,21,11], [11,21,11], [15,21,11], [15,17,11], [15,17,9], [15,17,1]]
    low = index[tuple(alt[0])][1]
    assert check.path_check(star.Q, 3, [2], alt, low["start"], low["end"]) == 0
    alt_trace = local_changes(alt, REMOTE)
    assert width_word(alt_trace) == (1, 2, 1)
    assert support(alt[alt_trace[2][0]], REMOTE) == (0,)
    print(json.dumps({"historical_R_rows_reproduced": len(archived_r), "v1653_archive_sha256": hashlib.sha256(raw).hexdigest(),
                      "fixed_v3": traces, "canonical_terminal_pair": terminal,
                      "same_endpoint_alternative_q2": {"path": alt, "widths": width_word(alt_trace),
                                                       "v3_named_trace": alt_trace, "profile_excursion": 0},
                      "whole_role_placement_census": motif_census(index, atom, verifier),
                      "common_background_field": check_field(overlap, green, [r["path"] for r in archived_r]),
                      "source_specific_formal_loss_fields": loss_test(index, atom, verifier, overlap, green),
                      "signed_secondary_source_and_overlap_cancellation": secondary,
                      "separate_original_v1624_endpoint_consumer": certificate_crosscheck(
                          [traces[name]["endpoint"] for name in ("delete_v1", "delete_v4")]),
                      "physical_event_and_local_receipt": "OPEN"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
