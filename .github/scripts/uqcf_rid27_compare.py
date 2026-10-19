"""receiver_identification d27 freeze (sections 31-32): COMPARATOR. Checks producer and checker against the preregistered
values of FREEZE.md section 3 (ranges by the hand rule, tables, instances, structural counts), equal digests, exact
certification, zero violations, the rejecting controls of section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d27_review")
FROZEN = {"RESULT.md": "2fe553f978b92e6c013372b8796047bbf676436a4acad993593a38c58dd34ef6"}
KIDS = {"TB": lambda v: (0, 1) if len(v) < 3 else (),
        "TM": lambda v: (0, 1, 2) if len(v) == 0 else ((0, 1) if len(v) < 3 else ())}
COUNTS = {"TB": [676, 49], "TM": [17576, 73], "S1": [4, 5], "S2": [6, 8]}  # S1/S2 variable counts per FREEZE.md section 7 erratum
FULLROWS = {"TB": 128, "TM": 200}


def addrs(k, v=()):
    out = [v]
    for i in k(v): out += addrs(k, v + (i,))
    return out


def s(v): return "r" + "".join("." + str(i) for i in v)


def ac(d): return (0,) * d


def um(m): return (0,) * m + (1,)


def strictly_below(x, v): return len(x) > len(v) and x[:len(v)] == v


def hand():
    E = {}
    for kind, tn, Ds, conds in (("FULL", "TB", (1, 2, 3), ("none", "SE", "SX")), ("FULL", "TM", (1, 2, 3), ("none", "SE", "SX")),
                                 ("REST", "TM", (1, 2, 3), ("none", "SE"))):
        AD = addrs(KIDS[tn])
        for D in Ds:
            for c in conds:
                r = {}
                for d in range(D + 1): r["A[%s|%s]" % (s(ac(d)), s(ac(d)))] = ["1", "1"]
                for m in range(D):
                    a, n = ac(m), ac(m + 1)
                    for x in AD:
                        if strictly_below(x, a) and not (x == n or strictly_below(x, n)): r["A[%s|%s]" % (s(x), s(a))] = ["0", "0"]
                    r["A[%s|%s]" % (s(n), s(a))] = ["0", "1"] if c == "none" else ["0", "0"]
                    for x in AD:
                        if strictly_below(x, n):
                            if c != "none": r["A[%s|%s]" % (s(x), s(a))] = ["0", "0"]
                            elif kind == "FULL" and tn == "TB": r["A[%s|%s]" % (s(x), s(a))] = ["0", "1"]
                    if kind == "FULL": r["A[%s|%s]" % (s(um(m)), s(um(m)))] = ["1", "1"] if c == "SX" else ["0", "1"]
                    else: r["A[%s|%s]" % (s(um(m)), s(um(m)))] = ["-inf", "inf"]
                E["%s|%s|%d|%s" % (kind, tn, D, c)] = r
    for m, u in ((0, (1,)), (0, (2,)), (1, (0, 1))):
        r = {"A[%s|%s]" % (s(u), s(ac(m))): ["0", "1"]}
        if u == um(m): r["A[%s|%s]" % (s(ac(m + 1)), s(ac(m)))] = ["0", "1"]
        E["DROPF|TM|2|SE|%d,%s" % (m, s(u))] = r
    for c, m in (((1, 0), 0), ((0, 0, 1), 1), ((2, 1, 0), 0)):
        E["DROPC|TM|2|SE|%s,%d" % (s(c), m)] = {"A[%s|%s]" % (s(c), s(ac(m))): ["-inf", "inf"]}
    return E


EXPECTED_RANGES = hand()
EXPECTED_X = {"X%d" % k: True for k in range(1, 13)}
EXPECTED_Y = {"Y1": ["1/2", "1/2", "0"], "Y2": ["2/3", "0", "1/3"], "Y3": ["1/2", "1/4", "1/4", "0"],
              "Y4": ["0", "1/2", "1/2", "0"], "Y5": ["1", "-1/2", "1/2", "0"], "Y6": ["-1/2", "1", "1/2"], "Y7": "-1"}
CONTROLS = ["R%d" % k for k in range(1, 11)]
PKEYS = {"role", "classes", "full_pos_rows", "ranges", "certified_exact", "tables", "instances", "controls", "result_sha256"}
CKEYS = {"role", "classes", "full_pos_rows", "ranges", "lp_only_upper_ends", "violations", "tables", "instances", "controls",
         "result_sha256"}


class Red(Exception):
    pass


def need(c, msg):
    if not c: raise Red(msg)


def load(raw):
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)): raise Red("duplicated JSON key")
        return dict(pairs)
    return json.loads(raw, object_pairs_hook=hook)


def lp_only():
    out = []
    AD = addrs(KIDS["TB"])
    for D in (1, 2, 3):
        for m in range(D):
            for x in AD:
                if strictly_below(x, ac(m + 1)): out.append("FULL|TB|%d|none|A[%s|%s]" % (D, s(x), s(ac(m))))
    return sorted(out)


def check(p, c, shas):
    need(shas == FROZEN, "frozen bytes differ")
    need(p.get("role") == "producer" and c.get("role") == "checker", "role confusion")
    need(p.get("result_sha256") == FROZEN["RESULT.md"] and c.get("result_sha256") == FROZEN["RESULT.md"], "false provenance")
    need(set(p) == PKEYS, "producer keys")
    need(set(c) == CKEYS, "checker keys")
    need(p["certified_exact"] is True, "producer certificate failed")
    need(c["violations"] == 0, "checker violations")
    need(p["classes"] == c["classes"], "class digests differ")
    need({k: [v["carriers"], v["vars"]] for k, v in p["classes"].items()} == COUNTS, "carrier/variable counts")
    need(p["full_pos_rows"] == c["full_pos_rows"] == FULLROWS, "full POS row counts")
    need(c["lp_only_upper_ends"] == lp_only(), "LP-only disclosure set differs")
    for x in (p, c):
        need(x["ranges"] == EXPECTED_RANGES, "ranges differ from preregistered values")
        need(x["tables"] == EXPECTED_X, "tables differ")
        need(x["instances"] == EXPECTED_Y, "instances differ")
        need(sorted(x["controls"]) == sorted(CONTROLS), "control set")
        need(all(v == "REJECTED" for v in x["controls"].values()), "a control was not rejected")


def tamper_tests(prod, chk, shas):
    cases = []
    k0 = "FULL|TM|2|SE"
    p = copy.deepcopy(prod); del p["ranges"][k0]; cases.append(("missing_record", p, chk, shas))
    p = copy.deepcopy(prod); p["ranges"]["FULL|TM|9|SE"] = p["ranges"][k0]; cases.append(("duplicated_record", p, chk, shas))
    p = copy.deepcopy(prod); p["ranges"][k0] = p["ranges"]["FULL|TM|2|none"]; cases.append(("substituted_record", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for x in (p, q): x["ranges"]["FULL|TM|2|SE"]["A[r.0|r]"] = ["0", "1"]
    cases.append(("leak_survives_SE_both", p, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for x in (p, q): x["ranges"]["REST|TM|2|SE"]["A[r.1|r.1]"] = ["0", "1"]
    cases.append(("signed_read_bounded_both", p, q, shas))
    p = copy.deepcopy(prod); p["classes"]["TM"]["digest"] = "0" * 64; cases.append(("false_digest", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for x in (p, q): x["classes"]["TM"]["carriers"] = 17575
    cases.append(("wrong_count_both", p, q, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["RESULT.md"] = "1" * 64; cases.append(("wrong_result_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R10"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R2"] = "ACCEPTED"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = 1; cases.append(("violation_hidden", prod, q, shas))
    p = copy.deepcopy(prod); p["certified_exact"] = False; cases.append(("certificate_failed", p, chk, shas))
    p = copy.deepcopy(prod); p["full_pos_rows"]["TM"] = 201; cases.append(("row_count_altered", p, chk, shas))
    q = copy.deepcopy(chk); q["lp_only_upper_ends"] = q["lp_only_upper_ends"][1:]; cases.append(("lp_only_set_altered", prod, q, shas))
    p = copy.deepcopy(prod); p["tables"]["X10"] = False; cases.append(("table_failed", p, chk, shas))
    p = copy.deepcopy(prod); p["instances"]["Y5"] = ["1", "-1/2", "1/2", "1"]; cases.append(("wrong_value_Y5", p, chk, shas))
    out = {}
    for name, a, b, sh in cases:
        try:
            check(a, b, sh); out[name] = "NOT_DETECTED"
        except (Red, KeyError, TypeError):
            out[name] = "DETECTED"
    raw = json.dumps(prod)
    try:
        load(raw[:-1] + ', "instances": {}}'); out["duplicated_key"] = "NOT_DETECTED"
    except Red:
        out["duplicated_key"] = "DETECTED"
    return out


def main():
    prod_raw, chk_raw = Path(sys.argv[1]).read_bytes(), Path(sys.argv[2]).read_bytes()
    shas = {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in FROZEN}
    report = {"producer_sha256": hashlib.sha256(prod_raw).hexdigest(), "checker_sha256": hashlib.sha256(chk_raw).hexdigest(),
              "frozen_sha256": shas, "freeze_sha256": hashlib.sha256((ROOT / "FREEZE.md").read_bytes()).hexdigest()}
    try:
        prod, chk = load(prod_raw), load(chk_raw)
        check(prod, chk, shas)
        report["ranges"] = prod["ranges"]; report["classes"] = prod["classes"]; report["tables"] = prod["tables"]
        report["instances"] = prod["instances"]; report["controls"] = chk["controls"]
        report["full_pos_rows"] = prod["full_pos_rows"]; report["lp_only_upper_ends"] = chk["lp_only_upper_ends"]
        report["entries"] = sum(len(v) for v in prod["ranges"].values())
        report["tamper"] = tamper_tests(prod, chk, shas)
        need(all(v == "DETECTED" for v in report["tamper"].values()), "tampering not detected")
        report["status"] = "GREEN"
    except Red as e:
        report["status"] = "RED"; report["reason"] = str(e)
    Path(sys.argv[3]).write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in report if k in ("status", "reason", "tamper", "frozen_sha256", "entries")}, indent=1, sort_keys=True))
    sys.exit(0 if report["status"] == "GREEN" else 1)


if __name__ == "__main__":
    main()
