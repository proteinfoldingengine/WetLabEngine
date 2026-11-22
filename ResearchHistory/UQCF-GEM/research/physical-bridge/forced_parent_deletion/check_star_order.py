"""Replay the original star archive and check receiver outcomes under relabeling."""
from collections import Counter, defaultdict
from functools import reduce
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations, product
from operator import or_
from pathlib import Path
import gzip
import hashlib
import json
import sys

ROOT = Path("ResearchHistory/UQCF-GEM/demos")
STAR = ROOT / "v16.43-star-fiber-classification"
ATOMIC = ROOT / "v16.26-consistency-increment-law"
ARCHIVE = "evidence/science/scientific/CERTIFICATE.json.gz"
DOMAINS = tuple((m, k) for m in range(2, 5) for k in range(2, 5)) + ((5, 2), (5, 3))


def pinned(path, identity):
    raw = path.read_bytes()
    assert hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == identity
    return raw


def original(name, path, identity):
    pinned(path, identity)
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def vertices(mask, leaf_count):
    return tuple(i for i in range(1, leaf_count + 1) if mask >> i & 1)


def universe(m, k):
    states = set()
    for supports in product(range(1, 1 << k), repeat=m):
        state = [1] * k
        for leaf, support in enumerate(supports, 1):
            for owner in range(k):
                if support >> owner & 1:
                    state[owner] |= 1 << leaf
        states.add(tuple(state))
    return states


def transitions(path):
    return [(i, after > before) for a, b in zip(path, path[1:])
            for i, (before, after) in enumerate(zip(a, b)) if before != after]


def archive_paths(entry, writer):
    m, k, graph = entry["m"], entry["k"], entry["graph"]
    states = graph["states"]
    ids = {tuple(s): i for i, s in enumerate(states)}
    assert len(ids) == len(states) and set(ids) == universe(m, k)
    rows = entry["normalizations"]
    assert [row["state"] for row in rows] == list(range(len(states)))
    cover_sizes = [graph["attained_profiles"][i][0] for i in graph["profile_ids"]]
    full = (1 << (m+1))-1
    for row, state in zip(rows, states):
        target = [1] * k
        q = row["q"]
        computed = next(r for r in range(1, k+1)
                        if any(reduce(or_, group) == full for group in combinations(state, r)))
        assert q == cover_sizes[row["state"]] == computed
        for v in range(1, m + 1):
            target[v-1 if v <= q else 0] |= 1 << v
        path = [states[t] for t in row["path"]]
        assert path[0] == state and path[-1] == target
        assert writer.normalize(state, m, k, q) == path
        for a, b in zip(path, path[1:]):
            (owner, bit), = [(j, x^y) for j, (x, y) in enumerate(zip(a, b)) if x != y]
            assert bit.bit_count() == 1
            lower = a if a[owner] < b[owner] else b
            assert graph["forward_moves"][ids[tuple(lower)]] >> ((m*owner) + bit.bit_length()-2) & 1
        band = int(m == q == k)
        assert all(abs(cover_sizes[t] - q) <= band for t in row["path"])
        yield row, path


def compare_events(path, changes, live_signatures, prep_signatures, seed):
    initial = path[0]
    first = {}
    for position, (owner, _) in enumerate(changes, 1):
        first.setdefault(owner, position)
    for position, (donor, addition) in enumerate(changes, 1):
        if addition:
            continue
        before, after = path[position-1:position+1]
        if before.count(1) != 1 or after.count(1) != 1:
            continue
        receiver = before.index(1)
        if initial[receiver] != 1 or first.get(receiver, len(path)) <= position:
            continue
        first_mask = None if receiver not in first else path[first[receiver]][receiver]
        others = [i for i in range(len(initial)) if i not in (donor, receiver)]
        live = (before[donor], after[donor], tuple(sorted(before[i] for i in others)))
        live_signatures[live].add(first_mask)
        if initial.count(1) == 1:
            prep = (initial[donor], before[donor], after[donor],
                    tuple(sorted((initial[i], before[i]) for i in others)))
            outputs, rows = prep_signatures[prep]
            outputs.add(first_mask)
            rows.add(seed)


def check_copy_phase(path, row, m, k, orbit_copies):
    initial = path[0]
    q = row["q"]
    if initial.count(1) != 1 or q != k-1 or m <= q:
        return
    assert len(set(initial)) == k
    duplicate_count = sum(mask.bit_count()-1 for mask in initial)-m
    clean = path[duplicate_count]
    blank = initial.index(1)
    assert clean[blank] == 1
    winners = {}
    for leaf in range(1, m + 1):
        holders = [i for i, mask in enumerate(initial) if mask >> leaf & 1]
        assert [i for i, mask in enumerate(clean) if mask >> leaf & 1] == holders[:1]
        winners[leaf] = holders[0]
    # Any mask used as a key here existed before cleanup and identifies exactly one view.
    precedences = {(initial[keeper], initial[other])
                   for leaf, keeper in winners.items()
                   for other, mask in enumerate(initial) if other != keeper and mask >> leaf & 1}
    active = set(initial) - {1}
    sinks = active - {a for a, _ in precedences}
    holdings = dict(zip(initial, clean))
    expected = {holdings[owner] for owner in sinks} | {1}
    key = tuple(sorted(holdings.items()))
    outcomes, old = orbit_copies.setdefault(key, (set(), expected))
    assert old == expected
    if blank == k-1:
        assert all(s[blank] == 1 for s in path)
        outcomes.add(1)
        return
    donor = k-1
    assert initial[donor] in sinks
    bundle = clean[donor]
    leaves = vertices(bundle, m)
    assert leaves
    current = clean[:]
    phase = []
    for leaf in leaves:
        current[blank] |= 1 << leaf
        phase.append(current[:])
    for leaf in leaves:
        current[donor] ^= 1 << leaf
        phase.append(current[:])
    assert path[duplicate_count+1:duplicate_count+1+len(phase)] == phase
    outcomes.add(bundle)


def inspect_archive(entries, writer):
    result = {}
    for entry in entries:
        m, k = entry["m"], entry["k"]
        live = defaultdict(set)
        prep = defaultdict(lambda: (set(), set()))
        copies = {}
        for row, path in archive_paths(entry, writer):
            moves = transitions(path)
            assert len(moves) == len(path)-1
            compare_events(path, moves, live, prep, row["state"])
            check_copy_phase(path, row, m, k, copies)
        assert all(None in r and len(r) > 1 for r in live.values())
        all_write = [rows for r, rows in prep.values() if None not in r]
        for outputs, rows in prep.values():
            if None not in outputs:
                assert len(outputs) == 1 and len(rows) == 1
        assert all(observed == expected for observed, expected in copies.values())
        result[f"{m}:{k}"] = {
            "original_paths": len(entry["normalizations"]),
            "live_event_classes": len(live),
            "live_with_multiple_acquisitions": sum(len(r-{None})>1 for r in live.values()),
            "classes_with_preparation": len(prep),
            "always_silent_with_preparation": sum(r == {None} for r, _ in prep.values()),
            "ambiguous_with_preparation": sum(None in r and len(r)>1 for r, _ in prep.values()),
            "forced_write_but_one_ordered_start": len(all_write),
            "copy_classes": len(copies),
            "copy_classes_multiple_donors": sum(len(outcomes)>2 for outcomes, _ in copies.values()),
            "maximum_copy_outcomes_including_silence": max((len(x) for x, _ in copies.values()), default=0)
        }
    return result


def extract_example(entry, role_state, donor, receiver, vertex, wanted_site_ids, atom, verifier, star_verify):
    m, k = entry["m"], entry["k"]
    graph = entry["graph"]
    states = graph["states"]
    ids = {tuple(s): i for i, s in enumerate(states)}
    seen = []
    for order in permutations(range(k)):
        start = tuple(role_state[i] for i in order)
        row = entry["normalizations"][ids[start]]
        path = [states[t] for t in row["path"]]
        assert star_verify.path_valid(row["path"], ids[start], row["path"][-1], graph, row["q"], 0)
        position = order.index(donor)
        b_position = order.index(receiver)
        expected = list(start)
        expected[position] ^= 1 << vertex
        if path[1] != expected:
            continue
        views = [(0,) + vertices(mask, m) for mask in start]
        source_event = atom.atomic([-1]+[0]*m, views, position, vertex)
        verifier.verify_atomic(source_event)
        assert source_event["tau_before"] == source_event["tau_after"] == k-1
        acquired = next((s[b_position] for s in path[2:] if s[b_position] != 1), 1)
        seen.append({"start": ids[start], "rank_order": order, "source": source_event,
                     "first_B": acquired, "path": path})
    histogram = Counter(r["first_B"] for r in seen)
    assert histogram == wanted_site_ids
    return {"receiver_outcomes": dict(histogram), "executions": seen}


def main(out):
    archive = pinned(STAR/ARCHIVE, "b226fdef7d908f1f0186060ebf408eb0db823418")
    entries = json.loads(gzip.decompress(archive))["entries"]
    assert tuple((e["m"], e["k"]) for e in entries) == DOMAINS
    sys.path.insert(0, str(STAR.resolve()))
    writer = original("original_star", STAR/"producer.py", "ffd513619d182abea2b31bd90c38e12784557bf3")
    verify = original("original_star_verify", STAR/"verifier.py", "80a47f10231a086af161c4999c582fa038d064c7")
    atom = original("original_atom", ATOMIC/"engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    atomic_verify = original("original_atomic_verify", ATOMIC/"verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    results = inspect_archive(entries, writer)
    three = next(e for e in entries if (e["m"], e["k"]) == (3,3))
    four = next(e for e in entries if (e["m"], e["k"]) == (4,4))
    # Role order for the three-view cases is reference, receiver, source.
    # The four-view case orders the roles receiver, leaf-one holder, reference, source.
    cases = {
        "star_184": extract_example(three, (11,1,7), 2,1,1, {1:1,5:2}, atom, atomic_verify, verify),
        "star_232": extract_example(three, (13,1,7), 2,1,2, {1:1,3:2}, atom, atomic_verify, verify),
        "four_view": extract_example(four, (1,3,13,21), 3,0,2, {1:3,3:3,17:6}, atom, atomic_verify, verify)
    }
    recorded = {r["start"]:r["first_B"] for r in cases["four_view"]["executions"]}
    assert (recorded[103],recorded[765],recorded[3289]) == (17,3,1)
    totals = {key:sum(r[key] for r in results.values()) for key in next(iter(results.values()))
              if not key.startswith("maximum_")}
    assert totals["live_event_classes"] == 844 and totals["live_with_multiple_acquisitions"] == 313
    assert totals["classes_with_preparation"] == 3504
    assert totals["forced_write_but_one_ordered_start"] == 258
    assert totals["always_silent_with_preparation"] == 1206 and totals["ambiguous_with_preparation"] == 2040
    assert totals["original_paths"] == 74185
    assert totals["copy_classes"] == 263 and totals["copy_classes_multiple_donors"] == 67
    certificate = {"domain":results, "cases":cases}
    out.mkdir(parents=True,exist_ok=True)
    raw = (json.dumps(certificate,sort_keys=True,indent=2)+"\n").encode()
    (out/"star_order_certificate.json").write_bytes(raw)
    return {"certificate_sha256":hashlib.sha256(raw).hexdigest(), **totals}


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1])),sort_keys=True,indent=2))
