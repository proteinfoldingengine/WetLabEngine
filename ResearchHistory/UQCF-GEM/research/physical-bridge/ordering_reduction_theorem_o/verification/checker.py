#!/usr/bin/env python3
"""Independent checker for the Theorem O witness check.

Written without importing producer.py. Own legality implementation over a set of
(vertex, label) incidences; breadth-first enumeration over HISTORY PREFIXES (no
merging by state); exact identity-set and dead-end-set equality; per-record replay
with first-stopping verification; menus, Prop R closure histories and controls
C1-C5; mandatory mutation controls (AMENDMENT_1 A3). Standard library only.
Exit status 0 only if every declared expected result holds and every mutation is
rejected.
"""
import collections, copy, hashlib, json, re, sys

NEG = "\u2212"
TREE = {"o": None, "u": "o", "v": "o", "w": "o", "x": "u", "y": "u"}
LABELS = ("a", "b", "r")
RECEIVER = "r"
PREP = {
    0: {"o": "abr", "u": "ar", "x": "ar", "y": "ar", "v": "abr", "w": "r"},
    1: {"o": "abr", "u": "abr", "x": "abr", "y": "abr", "v": "ar", "w": "r"},
}
REQUESTS = ["%sa(x)" % NEG, "%sa(y)" % NEG, "%sa(u)" % NEG, "%sa(v)" % NEG]
CMD = re.compile(r"^([+%s])([abr])\(([ouvwxy])\)$" % NEG)


def initial(s):
    return frozenset((v, i) for v, lab in PREP[s].items() for i in lab)


def parse(c):
    m = CMD.match(c)
    if not m:
        raise ValueError("unparseable command %r" % c)
    return m.group(1), m.group(2), m.group(3)


def legal(inc, c):
    """P1 one-command condition, checked on the incidence set."""
    sg, i, v = parse(c)
    if TREE[v] is None:
        return False
    if sg == "+":
        return (v, i) not in inc and (TREE[v], i) in inc
    if (v, i) not in inc:
        return False
    for ch, par in TREE.items():
        if par == v and (ch, i) in inc:
            return False
    return sum(1 for (vv, _) in inc if vv == v) >= 2


def step(inc, c):
    sg, i, v = parse(c)
    return inc | {(v, i)} if sg == "+" else inc - {(v, i)}


def is_receiver(c):
    return parse(c)[1] == RECEIVER


def candidate_moves(inc, pos, first, used, tag, executed):
    out = []
    if pos < len(REQUESTS) and legal(inc, REQUESTS[pos]):
        out.append(REQUESTS[pos])
    for v in ("u", "v", "w", "x", "y"):
        c = "%sr(%s)" % (NEG, v)
        if legal(inc, c):
            out.append(c)
    if tag == "C3" and first is not None and not used:
        l = parse(first)[2]
        c = "+r(%s)" % l
        if ("%sa(%s)" % (NEG, l)) in executed and legal(inc, c):
            out.append(c)
    return out


def bfs(s, tag):
    """Enumerate stopped histories and dead ends by BFS over prefixes."""
    stopped, dead = set(), set()
    q = collections.deque([((), initial(s), 0, None, False)])
    while q:
        hist, inc, pos, first, used = q.popleft()
        if pos == len(REQUESTS) and first is not None:
            stopped.add(hist)
            continue
        moves = candidate_moves(inc, pos, first, used, tag, hist)
        if not moves:
            dead.add(hist)
            continue
        for c in moves:
            npos = pos + 1 if (pos < len(REQUESTS) and c == REQUESTS[pos]) else pos
            nfirst = first if (first is not None or not is_receiver(c)) else c
            nused = used or c.startswith("+")
            q.append((hist + (c,), step(inc, c), npos, nfirst, nused))
    return stopped, dead


def ident(s, tag, hist):
    return "|".join([str(s), tag] + list(hist))


def replay(s, tag, cmds):
    """Return (ok, reason, first_response). Verifies legality, admissibility of
    each command in the universe, and stopping exactly at the last command."""
    inc, pos, first, used = initial(s), 0, None, False
    for k, c in enumerate(cmds):
        if pos == len(REQUESTS) and first is not None:
            return False, "extends past first stopping boundary at step %d" % k, None
        try:
            parse(c)
        except ValueError as e:
            return False, str(e), None
        if c not in candidate_moves(inc, pos, first, used, tag, tuple(cmds[:k])):
            return False, "command %d %s not legal/admissible" % (k, c), None
        if pos < len(REQUESTS) and c == REQUESTS[pos]:
            pos += 1
        if first is None and is_receiver(c):
            first = c
        used = used or c.startswith("+")
        inc = step(inc, c)
    if not (pos == len(REQUESTS) and first is not None):
        return False, "stopping condition not met (truncated)", None
    return True, "", first


def post_source_menu(s):
    inc = initial(s)
    for c in REQUESTS:
        assert legal(inc, c), c
        inc = step(inc, c)
    return sorted(c for c in ("%sr(%s)" % (NEG, v) for v in "uvwxy") if legal(inc, c))


def full_menu(inc):
    out = []
    for v in "uvwxy":
        for sg in ("+", NEG):
            c = "%sr(%s)" % (sg, v)
            if legal(inc, c):
                out.append(c)
    return sorted(out)


def decode(f, m0, m1):
    return 0 if f in m0 else (1 if f in m1 else None)


def uhash(ids):
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def check_producer(data, truth, m0, m1):
    """Return list of rejection reasons (empty = accepted)."""
    errs = []
    if set(data.get("universes", {})) != set(truth):
        return ["universe keys %r != %r" % (sorted(data.get("universes", {})), sorted(truth))]
    for key, (s, tag, ids, deads) in truth.items():
        u = data["universes"][key]
        recs = u["records"]
        got = [r["id"] for r in recs]
        if len(got) != len(set(got)):
            dup = sorted(x for x, n in collections.Counter(got).items() if n > 1)
            errs.append("%s: duplicate identities %s" % (key, dup[:3]))
        missing, extra = ids - set(got), set(got) - ids
        if missing or extra:
            errs.append("%s: identity set mismatch missing=%s extra=%s" % (key, sorted(missing)[:3], sorted(extra)[:3]))
        gd = u["dead_ends"]
        if len(gd) != len(set(gd)) or set(gd) != deads:
            errs.append("%s: dead-end set mismatch" % key)
        if u.get("count") != len(recs) or u.get("dead_end_count") != len(gd):
            errs.append("%s: declared counts disagree with records" % key)
        if u.get("universe_hash") != uhash(got) or u.get("dead_end_hash") != uhash(gd):
            errs.append("%s: declared hash disagrees with records" % key)
        for r in recs:
            if r.get("source") != s or r.get("universe") != tag:
                errs.append("%s: record %s has wrong source/universe field" % (key, r["id"]))
                continue
            if ident(s, tag, r["commands"]) != r["id"]:
                errs.append("%s: identity string does not match commands for %s" % (key, r["id"]))
                continue
            ok, why, first = replay(s, tag, r["commands"])
            if not ok:
                errs.append("%s: replay failed for %s: %s" % (key, r["id"], why))
                continue
            if first != r.get("first_response") or decode(first, m0, m1) != r.get("decoded"):
                errs.append("%s: first response/decoded mismatch for %s" % (key, r["id"]))
    return errs


def mutations(data, m0, m1):
    """Deterministic corruptions of AMENDMENT_1 A3 (first eligible record)."""
    out = []
    for key in sorted(data["universes"]):
        recs = data["universes"][key]["records"]
        if not recs:
            continue
        s, tag = recs[0]["source"], recs[0]["universe"]
        def mk(name, f):
            d = copy.deepcopy(data)
            f(d["universes"][key])
            out.append(("%s:%s" % (key, name), d))
        mk("omission", lambda u: u["records"].pop(0))
        if len(recs) >= 2:
            mk("duplicate-for-omission", lambda u: u["records"].__setitem__(1, copy.deepcopy(u["records"][0])))
        def trunc(u):
            r = u["records"][0]; r["commands"] = r["commands"][:-1]; r["id"] = ident(s, tag, r["commands"])
        mk("truncation", trunc)
        def ext(u):
            # extend first record that admits a further legal command after stopping
            for r in u["records"]:
                inc = initial(s)
                for c in r["commands"]:
                    inc = step(inc, c)
                more = [c for c in ["%sr(%s)" % (NEG, v) for v in "uvwxy"] + ["+r(%s)" % v for v in "uvwxy"] if legal(inc, c)]
                if more:
                    r["commands"] = r["commands"] + [more[0]]; r["id"] = ident(s, tag, r["commands"]); return
            raise RuntimeError("no extendable record in %s" % key)
        mk("extension", ext)
        mk("wrong-decoded", lambda u: u["records"][0].__setitem__("decoded", 1 - u["records"][0]["decoded"]))
        def illegal(u):
            r = u["records"][0]; r["commands"] = ["+a(o)"] + r["commands"]; r["id"] = ident(s, tag, r["commands"])
        mk("illegal-splice", illegal)
        def wrongsrc(u):
            r = u["records"][0]; r["source"] = 1 - s; r["id"] = ident(1 - s, tag, r["commands"])
        mk("wrong-source", wrongsrc)
        mk("false-metadata-count", lambda u: u.__setitem__("count", u["count"] + 1))
        mk("false-metadata-hash", lambda u: u.__setitem__("universe_hash", "0" * 64))
    return out


def controls(m0, m1):
    res = {}
    def run(s, cmds, noop_last=False):
        inc = initial(s)
        for k, c in enumerate(cmds):
            if not legal(inc, c):
                if noop_last and k == len(cmds) - 1:
                    sg, i, v = parse(c)
                    assert (v, i) in inc and sum(1 for (vv, _) in inc if vv == v) == 1
                    return True, "NOOP at final request (support {%s})" % i
                return False, "illegal at step %d %s" % (k, c)
            inc = step(inc, c)
        return True, "all executed"
    def first(cmds):
        return next(c for c in cmds if is_receiver(c))
    S = REQUESTS
    c1 = ["%sr(v)" % NEG] + S
    ok, note = run(1, c1, noop_last=True)
    res["C1"] = {"legal": ok and "NOOP" in note, "note": note, "first": first(c1), "decoded": decode(first(c1), m0, m1), "expected_source": 1}
    c2 = ["%sr(v)" % NEG, "+r(v)"] + S
    ok, note = run(1, c2)
    res["C2"] = {"legal": ok, "note": note, "first": first(c2), "decoded": decode(first(c2), m0, m1), "expected_source": 1}
    c4 = S + ["+b(v)", "%sr(v)" % NEG]
    ok, note = run(1, c4)
    res["C4"] = {"legal": ok, "note": note, "first": first(c4), "decoded": decode(first(c4), m0, m1), "expected_source": 1}
    c5 = {}
    for s in (0, 1):
        h = S + ["+a(w)", "%sr(w)" % NEG]
        ok, note = run(s, h)
        c5[str(s)] = {"legal": ok, "note": note, "first": first(h), "in_initial_menu": first(h) in full_menu(initial(s))}
    res["C5"] = c5
    return res


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    report = {"checker": "checker.py (BFS over prefixes, incidence-set legality)", "failures": []}
    fail = report["failures"]
    m0, m1 = post_source_menu(0), post_source_menu(1)
    report["menus_post_source"] = {"0": m0, "1": m1}
    if not (m0 == ["%sr(v)" % NEG] and m1 == ["%sr(x)" % NEG, "%sr(y)" % NEG]):
        fail.append("expected result 1: menus differ from declaration")
    truth, counts = {}, {}
    for s, tag in ((0, "O"), (1, "O"), (1, "C3")):
        st, dd = bfs(s, tag)
        key = "%s_%d" % (tag, s)
        truth[key] = (s, tag, {ident(s, tag, h) for h in st}, {ident(s, tag, h) for h in dd})
        decs = collections.Counter(decode(next(c for c in h if is_receiver(c)), m0, m1) for h in st)
        counts[key] = {"stopped": len(st), "dead_ends": len(dd), "decoded_values": {str(k): v for k, v in sorted(decs.items(), key=str)}}
        if tag == "O" and set(decs) != {s}:
            fail.append("expected result 2: %s has a wrong or undecodable first response" % key)
    report["independent_counts"] = counts
    # C3 restricted class
    c3 = truth["C3_1"][2]
    disp = ident(1, "C3", ["%sa(x)" % NEG, "%sr(x)" % NEG, "+r(x)", "%sa(y)" % NEG, "%sa(u)" % NEG, "%sa(v)" % NEG])
    report["C3"] = {"wrong_first_responses": counts["C3_1"]["decoded_values"], "contains_displayed_restoration": disp in c3,
                    "restoration_histories": sum(1 for i in c3 if "|+r(" in i)}
    if set(counts["C3_1"]["decoded_values"]) != {"1"} or disp not in c3:
        fail.append("expected result 4: C3 class")
    # Prop R
    a0, a1 = full_menu(initial(0)), full_menu(initial(1))
    q = {}
    for s, A in ((0, a0), (1, a1)):
        for rho in A:
            sg, i, v = parse(rho)
            h = [rho, ("+" if sg == NEG else NEG) + "%s(%s)" % (i, v)] + REQUESTS if sg == NEG else [rho] + REQUESTS
            inc, ok = initial(s), True
            for c in h:
                ok = ok and legal(inc, c)
                inc = step(inc, c) if ok else inc
            q["%d:%s" % (s, rho)] = ok
    report["prop_R"] = {"A_r(S0)": a0, "A_r(S1)": a1, "closure_Q_legal_and_complete": q}
    if a0 != a1 or not all(q.values()):
        fail.append("expected result 3: Prop R")
    # Controls
    ctl = controls(m0, m1)
    report["controls"] = ctl
    for k in ("C1", "C2", "C4"):
        if not (ctl[k]["legal"] and ctl[k]["decoded"] != ctl[k]["expected_source"]):
            fail.append("expected result 4: control %s not rejecting" % k)
    if not all(v["legal"] and not v["in_initial_menu"] for v in ctl["C5"].values()):
        fail.append("expected result 4: control C5 not rejecting")
    # Producer verification
    perr = check_producer(data, truth, m0, m1)
    report["producer_check"] = {"accepted": not perr, "reasons": perr}
    if perr:
        fail.append("producer output rejected")
    # Mutation controls
    mlog = []
    for name, d in mutations(data, m0, m1):
        reasons = check_producer(d, truth, m0, m1)
        mlog.append({"mutation": name, "rejected": bool(reasons), "first_reason": reasons[0] if reasons else None})
        if not reasons:
            fail.append("UNSOUND: checker accepted mutation %s" % name)
    report["mutation_controls"] = mlog
    report["verdict"] = "PASS" if not fail else "FAIL"
    json.dump(report, sys.stdout, indent=1, sort_keys=True, ensure_ascii=False)
    print()
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "producer_output.json"))
