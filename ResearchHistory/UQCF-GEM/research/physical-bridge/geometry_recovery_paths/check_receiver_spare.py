"""Run the historical six-leaf fork through the archived star normalizer."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha1, sha256
import importlib.util
from itertools import combinations, permutations
import json
import lzma
from pathlib import Path
import sys
from unittest.mock import patch

from check_protected_work import DEMOS, Star, modules, need

CHARTS = range(4)
LEAVES = range(1, 7)
ORIGINAL = ((5,), (1, 4, 6), (2,), (3, 4, 5))
UNIT = (1,) * 7
COMMON = (1, 1, 1, 2, 1, 1, 2)
EQUAL_ROOT = (1, 1, 1, 2, 1, 1, 1)
MATCHED = ((1, 1, 1, 4, 3, 1, 5), (1, 1, 1, 5, 3, 1, 4))
STAR = "v16.43-star-fiber-classification/"
COMPLEX = "v15.42-duality-covariant-transport-repair/"
GEOMETRY = "v15.43-certified-response-geometry/"
SOURCES = {
    "graph_producer": (STAR+"graph_producer.py", "6c8eca570cda82b64c0d06775672f33977be430a"),
    "graph_verifier": (STAR+"graph_verifier.py", "ff8af4ecf743507d0d601daffa9b054441b85fd1"),
    "writer": (STAR+"producer.py", "ffd513619d182abea2b31bd90c38e12784557bf3"),
    "star_verifier": (STAR+"verifier.py", "80a47f10231a086af161c4999c582fa038d064c7"),
    "exact_algebra": (COMPLEX+"exact_algebra.py", "c67ea42b61321469f7735ce589f2e729b241666a"),
    "operational_complex": (COMPLEX+"operational_complex.py", "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c"),
    "projection": (GEOMETRY+"projection.py", "f857f2cf1cd4c265c193121236af8e441b1f01dc"),
    "carrier": (GEOMETRY+"carriers.py", "5cd286b014bb44025e16832ee91a6e6665291c8c"),
}


def load_sources(root):
    hist = modules(root)
    for name, (source, pin) in SOURCES.items():
        path = root / DEMOS / source
        data = path.read_bytes()
        need(sha1(f"blob {len(data)}\0".encode()+data).hexdigest() == pin, source)
        spec = importlib.util.spec_from_file_location(name, path)
        hist[name] = sys.modules[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hist[name])
    return hist


def masks(views):
    return tuple(1 + sum(1 << v for v in group) for group in views)


def leaves(mask):
    return [v for v in LEAVES if mask & (1 << v)]


def cut(start, chart, v):
    need(start[chart] & (1 << v), "source absent")
    return tuple(x ^ (1 << v) if j == chart else x for j, x in enumerate(start))


def native_cut(star, start, chart, v):
    event = star.mod["atom"].atomic(star.p, [[0]+leaves(mask) for mask in start], chart, v)
    star.mod["verify"].verify_atomic(event)
    end = masks([group[1:] for group in event["after"]])
    need(end == cut(start, chart, v), "archived cut differs")
    return end


@lru_cache(maxsize=None)
def cover(state):
    for size in range(1, 5):
        for team in combinations(state, size):
            union = 1
            for mask in team:
                union |= mask
            if union == 127:
                return size
    raise ValueError("uncovered leaf")


def encode(path):
    """Positive code adds, negative code deletes. Magnitude is 6*chart + leaf."""
    codes = []
    for before, after in zip(path, path[1:]):
        (j, bit), = [(j, a ^ b) for j, (a, b) in enumerate(zip(before, after)) if a != b]
        need(bit.bit_count() == 1 and 2 <= bit <= 64, "not one leaf")
        value = 6*j + bit.bit_length()-1
        codes.append(value if after[j] & bit else -value)
    return codes


def local(codes, receiver):
    return [x-6*receiver if x > 0 else x+6*receiver for x in codes
            if (abs(x)-1)//6 == receiver]


def classification(left, right):
    if left == right:
        return "identical" if left else "both_empty"
    if not left or not right:
        return "one_empty"
    return "first_differs" if left[0] != right[0] else "later_differs"


def traced(hist, start, q, priority=False):
    writer = hist["writer"]
    writer_code = writer.normalize.__code__
    operations = {hist["work"].construct_response_geometry.__code__: "pair_work",
                  hist["refine"].push.__code__: "p1", hist["carrier"].build_carrier.__code__: "carrier"}
    counts = dict.fromkeys(operations.values(), 0)
    reads, edits, order = [], [], []
    live = []
    def trace(frame, event, arg):
        code = frame.f_code
        if event == "call" and code in operations:
            counts[operations[code]] += 1
        if code == writer_code and event == "line" and frame.f_lineno == 28:
            loc = frame.f_locals
            reads.append(dict(index=loc["i"], owners=list(loc["c"]), receiver=leaves(loc["s"][2])))
            live.append(loc["s"])
        if code.co_filename == writer_code.co_filename and code.co_name == "change" and event == "call":
            loc = frame.f_locals
            edits.append([loc["j"], loc["v"], loc["add"]])
            live.append(loc["s"])
        return trace
    def reverse_full(charts, size):
        teams = list(combinations(charts, size))
        need(teams == [(0, 1, 2, 3)], "intervention must retain sole covering team")
        order.append(list(reversed(teams[0])))
        return iter([tuple(order[-1])])
    old_trace = sys.gettrace()
    try:
        sys.settrace(trace)
        if priority:
            with patch.object(writer, "combinations", reverse_full):
                path = writer.normalize(start, 6, 4, q)
        else:
            path = writer.normalize(start, 6, 4, q)
    finally:
        sys.settrace(old_trace)
    sequence = encode(path)
    need([(1 if add else -1)*(6*j+v) for j, v, add in edits] == sequence, "trace/path mismatch")
    need(live and all(s is live[0] for s in live) and all(row is not live[0] for row in path),
         "live state and copied snapshots")
    need(tuple(path[0]) == start and counts == dict.fromkeys(operations.values(), 0), "input/effect")
    return path, dict(owner_reads=reads, edits=edits, numeric_calls=counts, priority_calls=order,
                      single_internal_list=True, independent_snapshots=True)


def grade_record(star, state, grades):
    views = [[0]+leaves(mask) for mask in state]
    vectors = [tuple(grades[v] if v in group else 0 for v in LEAVES) for group in views]
    g = star.mod["work"].construct_response_geometry(CHARTS, vectors, vectors)
    p1 = [int(x) for x in star.mod["refine"].push(star.p, views[2], grades)]
    return dict(work=[int(g.work[i][j]) for i, j in combinations(CHARTS, 2)], receiver_p1=p1), g


def path_checks(star, path, q):
    for s in path:
        need(cover(tuple(s)) == q, "left cover class")
    for a, b in zip(path, path[1:]):
        code, = encode([a, b])
        chart, v = divmod(abs(code)-1, 6)
        fine, coarse = (a, b) if code < 0 else (b, a)
        need(native_cut(star, tuple(fine), chart, v+1) == tuple(coarse), "native/inverse edit")
    need(tuple(path[-1]) == star.mod["star_verifier"].canonical(6, 4, q), "canonical endpoint")


def named(star):
    hist = star.mod
    start = masks(ORIGINAL)
    prepared = native_cut(star, start, 3, 5)
    rows, tests = [], []
    for i, actor in enumerate((1, 3)):
        after = native_cut(star, start, actor, 4)
        rest = star.moves(tuple(x >> 1 for x in after))
        need(set(rest) == {(0, 5), (3, 5)}, "all remaining pure-pruning events")
        for j in (0, 3):
            terminal = native_cut(star, after, j, 5)
            need(not star.moves(tuple(x >> 1 for x in terminal)), "hidden later cut")
        for nuisance in (None, 0, 3):
            state = after if nuisance is None else native_cut(star, after, nuisance, 5)
            first = start if nuisance is None else native_cut(star, start, nuisance, 5)
            need(native_cut(star, first, actor, 4) == state, "source/other cut square")
            q = cover(state)
            path, trace = traced(hist, state, q)
            path_checks(star, path, q)
            stream = local(encode(path), 2)
            first_edit = next(n for n in range(1, len(path)) if path[n][2] != path[n-1][2])
            unit, g = grade_record(star, state, UNIT)
            edges = tuple(sorted(tuple(sorted(pair)) for pair in g.neighbors))
            payload = hist["projection"].Payload(2, Fraction(1), tuple(CHARTS), g.work, edges, ())
            try:
                hist["carrier"].build_carrier(payload)
            except ValueError as err:
                carrier = str(err)
            else:
                carrier = "returned"
            rows.append(dict(actor=actor, nuisance=nuisance, start=list(state), cover=q,
                             path=encode(path), receiver_edits=stream, receiver_first=leaves(path[first_edit][2]),
                             final_receiver=leaves(path[-1][2]), unit=unit, carrier=carrier, trace=trace))
            if nuisance != 3:
                continue
            for title, grades in (("unit", UNIT), ("common", COMMON), ("matched", MATCHED[i]),
                                  ("equal_root", EQUAL_ROOT)):
                entries = {k:grade_record(star, s, grades)[0] for k, s in
                           (("original", start), ("prepared", prepared), ("post", state),
                            ("first_receiver_edit", path[first_edit]), ("end", path[-1]))}
                if title == "equal_root":
                    entries["source_before_after"] = [
                        [int(x) for x in hist["refine"].push(star.p, [0]+leaves(s[actor]), grades)]
                        for s in (prepared, state)]
                tests.append(dict(label=title, actor=actor, grades=list(grades), **entries))
    invocations, detours = [], []
    for reverse, actor in ((False, 3), (True, 1)):
        path, trace = traced(hist, prepared, 4, reverse)
        post = native_cut(star, prepared, actor, 4)
        tail = hist["writer"].normalize(post, 6, 4, 4)
        need(path[1:] == tail, "intervened caller changed suffix")
        path_checks(star, path, 4)
        invocations.append(dict(actor=actor, reversed_priority=reverse, trace=trace, path=encode(path)))
        # Original moves leaf 1 to chart 0 before the receiver needs a replacement.
        need(encode(tail[:3]) == [1, -7], "unexpected common relocation of leaf 1")
        alternate = list(tail[:3])
        for j, v, add in ((2, 5, True), (0, 5, False), (1, 2, True), (2, 2, False)):
            current = list(alternate[-1])
            need(bool(current[j] & (1 << v)) != add, "detour idle")
            current[j] ^= 1 << v
            alternate.append(current)
        alternate.extend(hist["writer"].normalize(alternate[-1], 6, 4, 4)[1:])
        path_checks(star, alternate, 4)
        detours.append(dict(actor=actor, path=encode(alternate), receiver_edits=local(encode(alternate), 2)))
    return dict(original=list(start), prepared=list(prepared), primary=rows, grade_controls=tests,
                one_call=invocations, legal_detours=detours, archive_campaign_includes_6_4=(6,4) in hist["writer"].DOMAIN)


def orbit(writer):
    priors = {}
    for chart in permutations(CHARTS):
        for labels in permutations(LEAVES):
            state = [1]*4
            for j, vs in enumerate(ORIGINAL):
                state[chart[j]] += sum(1 << labels[v-1] for v in vs)
            key = tuple(state)
            roles = (chart[0], chart[1], chart[2], chart[3], labels[3], labels[4])
            if key in priors:
                need(priors[key][0] == roles, "ambiguous transported roles")
                priors[key][1] += 1
            else:
                priors[key] = [roles, 1]
    rows, tallies = [], [Counter() for _ in range(3)]
    for state, (roles, multiplicity) in sorted(priors.items()):
        j0, left, receiver, right, source, other = roles
        need(multiplicity == 2, "unexpected symmetry")
        runs = []
        for index, remover in enumerate((None, j0, right)):
            prep = state if remover is None else cut(state, remover, other)
            pair, streams = [], []
            for actor in (left, right):
                post = cut(prep, actor, source)
                q = cover(post)
                path = writer.normalize(post, 6, 4, q)
                seq = encode(path)
                pair.append(bytes(x+32 for x in seq).hex())
                streams.append(local(seq, receiver))
            tallies[index][classification(*streams)] += 1
            runs.append(pair)
        rows.append([list(state), list(roles), runs])
    return rows, [dict(sorted(c.items())) for c in tallies]


if __name__ == "__main__":
    root, out = (Path(v).resolve() for v in sys.argv[1:])
    hist = load_sources(root)
    case = named(Star(6, hist))
    data, counts = orbit(hist["writer"])
    raw = (json.dumps(data, separators=(",", ":"))+"\n").encode()
    out.mkdir(parents=True, exist_ok=True)
    (out/"receiver_spare_universe.json.xz").write_bytes(lzma.compress(raw))
    certificate = dict(schema=1, priors=len(data), group_elements=24*720, paired_histories=3*len(data),
                       arms=6*len(data), counts=counts, raw_sha256=sha256(raw).hexdigest(), named=case)
    (out/"receiver_spare_certificate.json").write_text(json.dumps(certificate, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in certificate.items() if k != "named"},sort_keys=True))
