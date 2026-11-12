"""receiver_identification d24 freeze (sections 28-30): COMPARATOR. Checks producer and checker against the preregistered
values of FREEZE.md section 3 (ranges by the hand rule, witnesses, instances), equal class digests and diagnostics, exact
certification, zero violations, the rejecting controls of section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_review")
FROZEN = {"RESULT.md": "7600ad3708baa287ac877afa582d83073a02f0ec72bf11d6ddcfbeb091ba43cc"}
CARRIERS = {"BIN_5": 13, "BIN_6": 24, "BIN_7": 47, "BIN_8": 93, "ALL_7": 85, "ALL_8": 200, "CH_7": 7,
            "COMB_1": 3, "COMB_2": 7, "COMB_3": 15, "COMB_4": 31, "COMB_1-0": 2, "COMB_2-0": 4, "COMB_2-1": 5,
            "COMB_3-0": 8, "COMB_3-1": 9, "COMB_3-2": 11, "COMB_4-0": 16, "COMB_4-1": 17, "COMB_4-2": 19, "COMB_4-3": 23,
            "K_2,0": 25, "K_2,1": 28, "K_2,2": 35, "K_2,3": 42, "K_2,4": 46, "K_3,0": 34, "K_3,1": 40, "K_3,2": 54, "K_3,3": 66}


def canon_par(par):
    ch = {v: [] for v in range(len(par))}
    for v in range(1, len(par)): ch[par[v]].append(v)
    def c(v): return "(" + "".join(sorted(c(u) for u in ch[v])) + ")"
    return c(0)


def systems():
    s = []
    for N in (5, 6, 7, 8): s += [("BIN_%d" % N, D) for D in range(1, N)]
    for N in (7, 8): s += [("ALL_%d" % N, D) for D in range(1, N)]
    s += [("CH_7", D) for D in range(1, 7)]
    for D in range(1, 5):
        s.append(("COMB_%d" % D, D)); s += [("COMB_%d-%d" % (D, k), D) for k in range(D)]
    s += [("K_2,%d" % m, D) for m in range(5) for D in range(m + 1, 6)]
    s += [("K_3,%d" % m, D) for m in range(4) for D in range(m + 1, 5)]
    return s


def hand(n, D, j, i):
    if i == j: return ["1", "1"]
    if n.startswith(("BIN", "ALL")):
        N = int(n.split("_")[1]); return ["0", "1"] if (j, i) == (N - 1, N - 2) else ["0", "0"]
    if n == "CH_7": return ["0", "1"]
    if n.startswith("COMB"):
        if "-" in n:
            k = int(n.split("-")[1]); return ["0", str(Fr(1, 2 ** (j - k - 1)))] if i == k else ["0", "0"]
        return ["0", "0"]
    B, m = map(int, n[2:].split(","))
    return ["0", str(Fr(1, B ** (j - m - 1)))] if i == m else ["0", "0"]


EXPECTED_RANGES = {"%s|D=%d" % (n, D): {"A(%d,%d)" % (j, i): hand(n, D, j, i) for j in range(D + 1) for i in range(j + 1)}
                   for n, D in systems()}
EXPECTED_W = {"W0": True, "W1": True, "W2": True, "W3": True, "W4": True, "W5": True, "W6": True, "W7": True, "W8": True,
              "W9": [[3, 2, True, 0, 1], [5, 2, True, 0, 1], [7, 2, True, 0, 1], [9, 2, True, 0, None]], "W10": True}
EXPECTED_Y = {"Y1": ["1", "-1", "1"], "Y2": "-1", "Y3": "1/2", "Y4": ["1/2", "-1/2"], "Y5": ["-1/2", "1/2"], "Y6": "1/9",
              "Y7": canon_par([None, 0, 1, 0, 1])}
CONTROLS = ["R%d" % k for k in range(1, 11)]


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


def check(p, c, shas):
    need(shas == FROZEN, "frozen bytes differ")
    need(p.get("role") == "producer" and c.get("role") == "checker", "role confusion")
    need(p.get("result_sha256") == FROZEN["RESULT.md"] and c.get("result_sha256") == FROZEN["RESULT.md"], "false provenance")
    need(set(p) == {"classes", "ranges", "rows", "diagnostic_nobl_BIN_7", "certified_exact", "witnesses", "instances",
                    "controls", "diagnostic_row_counts_total", "role", "result_sha256"}, "producer keys")
    need(set(c) == {"classes", "ranges", "diagnostic_nobl_BIN_7_attained_upper", "witnesses", "instances", "controls",
                    "violations", "diagnostic_row_counts_total", "role", "result_sha256"}, "checker keys")
    need(p["certified_exact"] is True, "producer certificate failed")
    need(c["violations"] == 0, "checker violations")
    need(p["classes"] == c["classes"], "class digests differ")
    need({k: v["carriers"] for k, v in p["classes"].items()} == CARRIERS, "carrier counts")
    for x in (p, c):
        need(x["ranges"] == EXPECTED_RANGES, "ranges differ from preregistered values")
        need(x["witnesses"] == EXPECTED_W, "witnesses differ")
        need(x["instances"] == EXPECTED_Y, "instances differ")
        need(sorted(x["controls"]) == sorted(CONTROLS), "control set")
        need(all(v == "REJECTED" for v in x["controls"].values()), "a control was not rejected")
    need(p["diagnostic_row_counts_total"] == c["diagnostic_row_counts_total"], "row-count diagnostic differs")
    need(sum(p["rows"].values()) == p["diagnostic_row_counts_total"], "row-count diagnostic inconsistent")
    need(p["diagnostic_nobl_BIN_7"] == ["0", "1/2"] and c["diagnostic_nobl_BIN_7_attained_upper"] == "1/2", "diagnostic differs")


def tamper_tests(prod, chk, shas):
    cases = []
    k0 = "BIN_7|D=3"
    p = copy.deepcopy(prod); del p["ranges"][k0]; cases.append(("missing_record", p, chk, shas))
    p = copy.deepcopy(prod); p["ranges"]["BIN_7|D=99"] = p["ranges"][k0]; cases.append(("duplicated_record", p, chk, shas))
    p = copy.deepcopy(prod); p["ranges"][k0] = p["ranges"]["BIN_7|D=4"]; cases.append(("substituted_record", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for x in (p, q): x["ranges"]["K_3,1|D=4"]["A(4,1)"] = ["0", "1/4"]
    cases.append(("wrong_leak_both", p, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for x in (p, q): x["ranges"]["CH_7|D=6"]["A(1,0)"] = ["0", "0"]
    cases.append(("forks_unneeded_both", p, q, shas))
    p = copy.deepcopy(prod); p["classes"]["ALL_8"]["digest"] = "0" * 64; cases.append(("false_digest", p, chk, shas))
    p = copy.deepcopy(prod); p["classes"]["ALL_8"]["carriers"] = 199; q = copy.deepcopy(chk); q["classes"]["ALL_8"]["carriers"] = 199
    cases.append(("wrong_count_both", p, q, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["RESULT.md"] = "1" * 64; cases.append(("wrong_result_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R10"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R2"] = "ACCEPTED"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = 1; cases.append(("violation_hidden", prod, q, shas))
    p = copy.deepcopy(prod); p["certified_exact"] = False; cases.append(("certificate_failed", p, chk, shas))
    p = copy.deepcopy(prod); p["diagnostic_row_counts_total"] += 1; cases.append(("diagnostic_altered", p, chk, shas))
    p = copy.deepcopy(prod); p["diagnostic_nobl_BIN_7"] = ["0", "1"]; cases.append(("nobl_diagnostic_altered", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for x in (p, q): x["witnesses"]["W9"][3][3] = 1
    cases.append(("small_comb_both", p, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Y6"] = "1/3"; cases.append(("wrong_value_Y6", p, chk, shas))
    out = {}
    for name, a, b, s in cases:
        try:
            check(a, b, s); out[name] = "NOT_DETECTED"
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
        report["ranges"] = prod["ranges"]; report["classes"] = prod["classes"]; report["witnesses"] = prod["witnesses"]
        report["instances"] = prod["instances"]; report["controls"] = chk["controls"]
        report["diagnostics"] = {"rows_total": prod["diagnostic_row_counts_total"], "nobl_BIN_7_A(1,0)": prod["diagnostic_nobl_BIN_7"]}
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
