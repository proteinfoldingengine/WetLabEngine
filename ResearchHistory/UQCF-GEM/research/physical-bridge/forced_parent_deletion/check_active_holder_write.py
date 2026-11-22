"""Replay ordered-star source deletions and the original v16.53 receiver writes."""
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import sympy as sp


DEMOS = Path(__file__).resolve().parents[3] / "demos"
STAR = "v16.53-four-child-boundary/"
ATOM = "v16.26-consistency-increment-law/"
ARCHIVE = STAR + "evidence/science/scientific/CERTIFICATE.json.gz"
PARENTS = (-1, 0, 0, 0, 0)
SITES = tuple(range(5))
SOURCES = {
    STAR + "producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    STAR + "cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    STAR + "coverage.py": "e90576a0285357f62ca2f9d9cac872b2a226e823",
    STAR + "verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    STAR + "feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    ARCHIVE: "9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e",
    ATOM + "engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    ATOM + "verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
}


def historical(path, name):
    spec = importlib.util.spec_from_file_location(name, DEMOS / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def view(mask):
    return tuple(site for site in SITES if mask & (1 << site))


def external_sites(state, receiver):
    return sorted({v for j, mask in enumerate(state) if j != receiver for v in view(mask) if v})


def own_changes(path, receiver):
    return [(i, s[receiver]) for i, s in enumerate(path)
            if i == 0 or s[receiver] != path[i - 1][receiver]]


def leaves(mask):
    return mask.bit_count() - 1


def delete(atom, verifier, state, actor, site):
    record = atom.atomic(PARENTS, list(map(view, state)), actor, site)
    delta, trigger = verifier.verify_atomic(record)
    after = tuple(sum(1 << v for v in y) for y in record["after"])
    assert after[actor] == state[actor] ^ (1 << site)
    return after, delta, bool(trigger)


def catalog_check(index, atom, verifier):
    totals = Counter()
    for start, (_, before) in index.items():
        old_degree = leaves(before["end"][0])
        assert old_degree == 5 - before["q"][0]
        options = {}
        for actor, mask in enumerate(start):
            affected = {}
            for site in view(mask)[1:]:
                if not any(i != actor and site in view(z) for i, z in enumerate(start)):
                    continue
                after, delta, triggered = delete(atom, verifier, start, actor, site)
                arm = index[after][1]
                assert arm["q"][0] - before["q"][0] == delta == int(triggered)
                assert leaves(arm["end"][0]) - old_degree == -delta
                totals["atoms"] += 1
                totals["triggered"] += triggered
                affected[site] = arm
            options[actor] = affected
        for actor, affected in options.items():
            for (h, one), (other, two) in itertools.combinations(affected.items(), 2):
                if one["q"] == two["q"]:
                    continue
                for r, mask in enumerate(start):
                    if r == actor or h not in view(mask) or other not in view(mask):
                        continue
                    low, high = sorted((one, two), key=lambda row: row["q"])
                    assert low["q"] == [2] and high["q"] == [3]
                    by_leaf = [frozenset(j for j, z in enumerate(start) if i in view(z)) for i in SITES[1:]]
                    third = (set(range(len(start))) - {r, actor}).pop()
                    assert set(by_leaf) == {frozenset({r, actor, third}), frozenset({r, actor}),
                                            frozenset({actor}), frozenset({third})}
                    a, b = [own_changes(row["path"], r) for row in (low, high)]
                    assert [leaves(v) for _, v in a[:3]] == [2, 3, 4]
                    assert [leaves(v) for _, v in b[:3]] == [2, 3, 2]
                    assert all(leaves(v) < 4 for _, v in b)
                    totals["eligible_two_site_choices"] += 1
                    totals["receiver_is_first_index"] += r == 0
                    totals["equal_path_lengths"] += len(low["path"]) == len(high["path"])
                    d_low, d_high = a[1][1] ^ a[2][1], b[1][1] ^ b[2][1]
                    if d_low == d_high and not d_low & ((1 << h) | (1 << other)):
                        totals["same_remote_second_write"] += 1
    assert totals == {"atoms": 12564, "triggered": 2708, "eligible_two_site_choices": 144,
                      "receiver_is_first_index": 48, "equal_path_lengths": 24, "same_remote_second_write": 40}
    return dict(totals)


def trace_record(index, packed, receiver=0):
    number, row = index[tuple(packed)]
    trace = own_changes(row["path"], receiver)
    return {"archived_row_zero_based": number, "identity": row["identity"], "q": row["q"][0],
            "path": row["path"], "moves": len(row["path"]) - 1, "end": row["end"],
            "receiver_masks": [m for _, m in trace], "own_write_indices": [i for i, _ in trace[1:]],
            "receiver_leaf_counts": [leaves(m) for _, m in trace]}


def common_counting(overlap, a, b):
    small = tuple(sorted(set(view(a)) & set(view(b))))
    images = []
    for mask in (a, b):
        marginal = overlap.push(PARENTS, SITES, view(mask), (1,) * 5)
        images.append(overlap.push(PARENTS, view(mask), small, marginal))
    assert images[0] == images[1]
    return {"sites": list(small), "both_grades": list(map(int, images[0]))}


def star_responses(green, masks):
    geometries = []
    for mask in masks:
        retained = view(mask)
        local_parents = (-1,) + (0,) * (len(retained) - 1)
        dim = len(retained) - 1
        inverse = green.candidate(local_parents)
        assert green.root_laplacian(local_parents) == inverse == sp.eye(dim)
        drive = sp.Matrix([int(v == 1) for v in retained[1:]])  # +1 at v1, balanced at o
        potential = (0, *map(int, inverse * drive))
        common = [potential[retained.index(v)] for v in (0, 1, 4)]
        assert common == [0, 1, 0]
        geometries.append({"root_degree_and_rank": dim, "fixed_port_potential_on_o_v1_v4": common})
    return geometries


def two_site_case(index, atom, verifier, star_verifier, overlap, green):
    initial = (19, 23, 11)
    arms = []
    for site in (1, 4):
        after, delta, _ = delete(atom, verifier, initial, 1, site)
        a = trace_record(index, after)
        a["source_site"] = site
        a["source_root_increment"] = delta
        a["external_leaf_coverage_at_onset"] = external_sites(after, 0)
        arms.append(a)
    low, high = arms
    assert [a["archived_row_zero_based"] for a in arms] == [1782, 2466]
    assert [a["q"] for a in arms] == [2, 3]
    assert [a["receiver_masks"] for a in arms] == [[19, 23, 31, 15], [19, 27, 19, 23, 7]]
    assert [a["external_leaf_coverage_at_onset"] for a in arms] == [[1, 2, 3, 4], [1, 2, 3]]
    for a, after_bit in zip(arms, (True, False)):
        assert a["moves"] == 14 and a["own_write_indices"][1] == 4
        path = a["path"]
        assert path[3][0] ^ path[4][0] == 1 << 3
        assert all(bool(s[0] & (1 << 3)) == after_bit for s in path[4:])
    no_event = trace_record(index, initial)
    assert no_event["archived_row_zero_based"] == 2468 and no_event["receiver_masks"] == low["receiver_masks"]
    alternative = [[19, 21, 11], [27, 21, 11], [11, 21, 11], [15, 21, 11],
                   [15, 17, 11], [15, 17, 9], [15, 17, 1]]
    assert star_verifier.path_check(star_verifier.Q, 3, [2], alternative, low["path"][0], low["end"]) == 0
    alt_counts = [leaves(m) for _, m in own_changes(alternative, 0)]
    assert alt_counts[:3] == [2, 3, 2]
    return {"start": initial, "receiver": "A", "source": "B", "arms": arms, "no_event": no_event,
            "response_after_second_own_write": star_responses(green, [low["path"][4][0], high["path"][4][0]]),
            "later_common_counting": common_counting(overlap, low["end"][0], high["end"][0]),
            "common_counting_after_second_write": common_counting(overlap, low["path"][4][0], high["path"][4][0]),
            "equally_admitted_alternative_low_path": alternative, "alternative_low_counts": alt_counts}


def same_site_case(index, atom, verifier, overlap):
    initial = (19, 3, 31)
    no_event = trace_record(index, initial)
    arms = []
    for j in (2, 1):
        after, _, _ = delete(atom, verifier, initial, j, 1)
        assert after[0] == initial[0] and external_sites(after, 0) == [1, 2, 3, 4]
        arms.append(trace_record(index, after))
    high, low = arms
    assert [high["archived_row_zero_based"], low["archived_row_zero_based"]] == [1196, 1882]
    assert high["q"] == 2 and low["q"] == 1 and high["moves"] == low["moves"] == 14
    assert high["path"][1:13] == low["path"][1:13] and high["path"][1] == list(initial)
    assert no_event["path"] == low["path"][1:]
    assert high["path"][13][0] == 15 and low["path"][13][0] == 31
    assert high["receiver_masks"][:-1] == low["receiver_masks"]
    assert all(s[0] & 2 for row in arms for s in row["path"])
    redundant = (19, 31, 31)
    neutral = [trace_record(index, delete(atom, verifier, redundant, j, 1)[0]) for j in (1, 2)]
    assert all(row["q"] == 1 and row["end"] == low["end"] for row in neutral)
    return {"start": initial, "C_deletion": high, "B_deletion": low, "no_event": no_event,
            "equal_incidence_indices_after_source": [1, 12], "old_common_A_counting_grade": [3, 1, 1],
            "later_common_counting": common_counting(overlap, high["end"][0], low["end"][0]),
            "two_universal_labels_control_rows": [a["archived_row_zero_based"] for a in neutral]}


def main():
    for path, expected in SOURCES.items():
        data = (DEMOS / path).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == expected, path
    sys.path.insert(0, str(DEMOS / STAR))
    producer = historical(STAR + "producer.py", "star_producer")
    checker = historical(STAR + "verifier.py", "star_verifier")
    atom = historical(ATOM + "engine.py", "atom_engine")
    verifier = historical(ATOM + "verify.py", "atom_verifier")
    overlap = historical("v16.23-overlap-descent/engine.py", "overlap_engine")
    green = historical("v16.22-response-selection-closure/engine.py", "response_engine")
    raw = (DEMOS / ARCHIVE).read_bytes()
    original = json.loads(gzip.decompress(raw))["records"]
    # Invoke the unchanged entry point with its own full catalogue. Only R is compared.
    reproduced = producer.produce()["records"]
    assert [row["identity"] for row in original] == producer.specs()
    old_r = [row for row in original if row["identity"][0] == "R"]
    fresh_r = [row for row in reproduced if row["identity"][0] == "R"]
    assert json.loads(json.dumps(fresh_r)) == old_r
    index = {}
    for i, row in enumerate(original):
        if row["identity"][0] == "R":
            assert row["status"] == "ok"
            checker.path_check(producer.Q, row["k"], row["q"], row["path"], row["start"], row["end"])
            index[tuple(row["start"])] = i, row
    assert len(index) == len(old_r) == 2507
    result = {"archive_git_blob": SOURCES[ARCHIVE], "archive_sha256": hashlib.sha256(raw).hexdigest(),
              "archive_rows": len(original), "unchanged_producer_R_rows_matching": len(old_r),
              "star_catalog": catalog_check(index, atom, verifier),
              "two_site_witness": two_site_case(index, atom, verifier, checker, overlap, green),
              "same_site_control": same_site_case(index, atom, verifier, overlap),
              "automatic_event_activation_and_physical_owner_read": "OPEN"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
