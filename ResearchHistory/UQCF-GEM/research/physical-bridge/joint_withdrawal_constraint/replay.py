"""Use the original atom to challenge groups on both sides of each source cut."""
import hashlib
import importlib.util
import json
import lzma
import sys
from collections import Counter
from functools import cache
from pathlib import Path

STAGE = "v16.26-consistency-increment-law"


def pin(path, sha):
    raw = path.read_bytes()
    if hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() != sha:
        raise ValueError(f"Unexpected original at {path}")
    return raw


def load(path, sha):
    pin(path, sha)
    spec = importlib.util.spec_from_file_location("historical", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rows(raw):
    return tuple(map(tuple, raw))


def mask(view):
    return sum(1 << v for v in view)


def cut(native, p, s, i, x):
    return rows(native.atomic(p, s, i, x)["after"])


def shape_rows(native, code, p, historical):
    @cache
    def strip(state, x, actors):
        # Clear x and everything below it from these rows, children first.
        def path(v):
            chain = [v]
            while v:
                v = p[v]
                chain.append(v)
            return chain
        for i in actors:
            subtree = [v for v in state[i] if x in path(v)]
            for v in sorted(subtree, key=lambda w: -len(path(w))):
                try:
                    state = cut(native, p, state, i, v)
                except ValueError as error:
                    if str(error) != "same union":
                        raise
                    return False
        return True

    out = []
    old_digest = hashlib.sha256()
    for s in native.covers(p):
        for i, view in enumerate(s):
            for x in view:
                try:
                    event = native.atomic(p, s, i, x)
                except ValueError:
                    continue
                t = rows(event["after"])
                fields = tuple(event[k] for k in ("tau_before", "tau_after", "h_before", "h_after", "trigger"))
                old_digest.update((repr((s, i, x) + fields) + "\n").encode())
                groups = []
                for group in range(1 << len(s)):
                    if group & (1 << i):
                        continue
                    actors = tuple(j for j in range(len(s)) if group >> j & 1)
                    old = strip(s, x, actors)
                    new = strip(t, x, actors)
                    groups.append([group, int(old), int(new)])
                out.append([p, tuple(map(mask, s)), i, x, int(event["trigger"]), event["delta_h"], groups])
    assert historical["code"] == code and len(out) == historical["atomic"]
    assert old_digest.hexdigest() == historical["digest"]
    return out


def five_chart(native, verifier):
    stored = pin(Path(__file__).with_name("fixture.json"), "806d2bc487e358f498cafa806226d1f658e98d26")
    cfg = json.loads(stored)
    names = cfg["charts"]
    p = (-1,) + (0,) * 7
    start = tuple((0,) + tuple(x for x, holders in enumerate(cfg["tip_holders"], 1) if n in holders)
                  for n in names)

    def step(s, n, x):
        event = native.atomic(p, s, names.index(n), x)
        verifier.verify_atomic(event)
        return rows(event["after"]), event

    @cache
    def paths(s):
        found = []
        for i, view in enumerate(s):
            for x in view:
                try:
                    t = cut(native, p, s, i, x)
                except ValueError:
                    continue
                found.extend((((names[i], x),) + moves, end) for moves, end in paths(t))
        return found or [((), s)]

    output = []
    terminals = []
    for route in cfg["receipt_paths"]:
        s = start
        for j in route[:3]:
            s, event = step(s, *cfg["edits"][j])
        assert event["index"] == names.index("B") and event["leaf"] == 5
        bit = int(event["trigger"])
        changes = []
        for n, x in (("E", 2), ("X", 4)):
            old = [c for j, c in enumerate(names) if x in s[j]]
            s, _ = step(s, n, x)
            new = [c for j, c in enumerate(names) if x in s[j]]
            changes.append([n, x, old, new])
        target, = [v for v in (2, 4) if {c for i, c in enumerate(names) if v in s[i]} == {"A", "F"}]
        seen = Counter()
        ends = set()
        examples = {}
        for word, end in paths(s):
            [(actor, _)] = [e for e in word if e[1] == target]
            assert actor in "AF"
            holder = "A" if actor == "F" else "F"
            assert {n for j, n in enumerate(names) if target in end[j]} == {holder}
            if actor == "A":
                assert s[names.index("F")] == end[names.index("F")]
            seen[actor] += 1
            ends.add(end)
            examples.setdefault(actor, word)
        # Test the endpoint-driven historical caller with all non-target decisions matched.
        endpoint_tests = {}
        for actor, other in (("A", "F"), ("F", "A")):
            alt = names.index(actor)
            endpoint = list(s)
            for site in range(1, len(p)):
                if site == target:
                    owner = names.index(other)
                else:
                    owner = next(k for k, row in enumerate(s) if site in row)
                for k, row in enumerate(endpoint):
                    if k != owner and site in row:
                        endpoint[k] = tuple(v for v in row if v != site)
            endpoint = tuple(endpoint)
            assert endpoint in ends
            factor = native.factor(p, s, endpoint)
            assert verifier.verify_factor(factor)
            receipts = [(names[e["index"]], e["leaf"]) for e in factor["steps"]]
            assert [e for e in receipts if e[1] == target] == [(actor, target)]
            assert ((target in endpoint[alt]) is False)
            endpoint_tests[actor] = dict(endpoint=endpoint, executed=receipts)
        ends_a, ends_f = (endpoint_tests[n]["endpoint"] for n in "AF")
        assert [(names[k], x) for k in range(len(s))
                for x in sorted(set(ends_a[k]) ^ set(ends_f[k]))] == [("A", target), ("F", target)]
        terminals.append(ends)
        output.append(dict(earlier_bit=bit, changes=changes, compulsory_site=target,
                           paths_by_releasing_chart=dict(seen), terminals=len(ends), example=examples,
                           supplied_endpoint_factor=endpoint_tests))
    return dict(arms=output, common_terminal_states=len(set.intersection(*terminals)))


def repeat_control(native):
    p = (-1, 0, 0, 0, 0)
    # Prepared #166 fixture, chart order A,X,Y,Z,C,B.
    start = ((0, 1, 2, 3), (0,), (0,), (0,), (0, 1, 2), (0, 4))
    arm_ends = []
    for x in (1, 2):
        t = cut(native, p, start, 0, x)
        u = cut(native, p, t, 0, 3-x)
        v = cut(native, p, t, 4, 3-x)
        assert u[4] == start[4] and v[4] == (0, x)
        arm_ends.append(u)
    assert arm_ends[0] == arm_ends[1]
    return arm_ends[0]


def archived_square(native, demos):
    path = demos / "v16.29-local-profile-closure/evidence/EXAMPLES.json"
    doc = json.loads(pin(path, "94909a58db4d8dcc59c76fcfb61f2712edb5627f"))["zero"]
    p = tuple(doc["parents"])
    start, after_a, after_b, end = map(rows, doc["states"])
    assert start == rows(doc["before"]) and doc["events"] == [[0, 1], [1, 1]]
    assert cut(native,p,start,0,1) == after_a and cut(native,p,start,1,1) == after_b
    assert cut(native,p,after_a,1,1) == end == cut(native,p,after_b,0,1)
    assert doc["heights"] == [1]*4 and doc["profiles"] == [[1,0]]*4
    assert after_a[1] == after_a[2] == start[1] == start[2]
    # Rows 1 and 2 can jointly clear site 1 in either order before row 0's cut.
    for first, second in ((1,2), (2,1)):
        t = cut(native,p,start,first,1)
        assert cut(native,p,t,second,1) == ((0,1),(0,),(0,))
    # After row 0's cut both first calls succeed and either second call fails.
    answers = []
    for first, second in ((1,2), (2,1)):
        t = cut(native,p,after_a,first,1)
        try:
            cut(native,p,t,second,1)
        except ValueError as exc:
            assert str(exc) == "same union"
        else:
            raise AssertionError("Final copy lost")
        answers.append(dict(released=first,retained=second,endpoint=t))
    return dict(archived_class=doc["mechanism"],heights=doc["heights"],resolutions=answers)


def main(demos, outfile):
    base = demos / STAGE
    native = load(base / "engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = load(base / "verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    official = json.loads(pin(base / "evidence/PRODUCTION.json", "25e15faf44bb59c77cdd48abf7c8473395c1ae04"))
    orig = {v["code"]: v for v in official["instances"]}
    records = []
    for code, p in native.shapes(5):
        records.extend(shape_rows(native, code, p, orig[code]))
    assert len(records) == official["atomic"] and len(orig) == len(native.shapes(5))
    by_order = Counter()
    by_t = Counter()
    totals = Counter()
    for p, s, i, x, t, dh, groups in records:
        changed = [g for g, old, new in groups if old != new]
        ranked = sorted(changed, key=int.bit_count)
        if ranked:
            core = ranked[0]
            assert set(changed) == {g for g, _, _ in groups if g & core == core}
            order = core.bit_count()
        else:
            order = 0
        by_order[order] += 1
        by_t[order, t, dh] += 1
        totals["tested"] += len(groups)
        totals["changed"] += len(changed)
    raw = (json.dumps(sorted(records), separators=(",", ":")) + "\n").encode()
    outfile.write_bytes(lzma.compress(raw))
    return dict(events=len(records), groups=totals, events_by_minimum_group_size=by_order,
                counts_by_size_trigger_delta=sorted([*k,v] for k,v in by_t.items()),
                record_sha256=hashlib.sha256(raw).hexdigest(), record_bytes=len(raw),
                five_chart=five_chart(native, verifier), archived_square=archived_square(native, demos),
                source_repeat_common_endpoint=repeat_control(native))


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1]), Path(sys.argv[2])), sort_keys=True, indent=2))
