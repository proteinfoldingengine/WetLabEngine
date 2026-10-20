"""receiver_identification d28 freeze (section 33): COMPARATOR. Checks producer and checker against the preregistered values
of FREEZE.md section 3 (ranks, side counts, supports, leaf-carrier counts, structural counts, tables, instances), equal
digests and counts, zero violations, the rejecting controls of section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

FROZEN = "a747459613ab088fb363c583cc6cd5ed4333850b64758b88fbba14fcd50529e4"
PRE = {  # name: (side, rank, support, leaf carriers)
    "TM|1": (14, 15, 16, [676]), "TM|2": (17, 19, 20, [676, 3380]), "TM|3": (18, 21, 22, [676, 3380, 6760]),
    "MX|1": (2, 3, 4, [3]), "MX|2": (2, 4, 5, [3, 3]), "MX|3": (3, 6, 7, [3, 3, 6]),
    "CH|1": (0, 1, 2, [1]), "CH|2": (0, 2, 3, [1, 1]), "CH|3": (0, 3, 4, [1, 1, 1]),
    "S4α|1": (1, 2, 3, [2]), "S4β|1": (2, 3, 4, [3]),
}
STRUCT = {"TM": (17576, 73), "MX": (18, 19), "CH": (4, 10), "S4": (6, 8)}
INST = {"Y1": ["0", "-1", "1", "1"], "Y2": "1/2", "Y3": "1", "Y4": "-1/2", "Y5": ["0", "0", "1"]}
TABLES = ["X1", "X2", "X3", "X4", "X5", "X6"]
CONTROLS = ["R%d" % i for i in range(1, 10)]
KEYS = {"role", "frozen_result_sha256", "structural", "systems", "tables", "instances", "controls", "violations"}
SYSKEYS = {"side", "rank_et", "rank_ds", "rank_union", "span_equal", "support", "support_equals_ds_support", "leaf_carriers",
           "et_rows", "side_addresses"}


def nodup(pairs):
    d = {}
    for k, v in pairs:
        if k in d: raise ValueError("duplicated JSON key " + k)
        d[k] = v
    return d


def check_one(r, role):
    e = []
    if set(r) != KEYS: e.append(role + ": key set")
    if r.get("role") != role: e.append(role + ": role")
    if r.get("frozen_result_sha256") != FROZEN: e.append(role + ": frozen hash")
    if r.get("violations") != 0: e.append(role + ": violations")
    st = r.get("structural", {})
    if set(st) != set(STRUCT): e.append(role + ": structural trees")
    for t, (c, v) in STRUCT.items():
        if st.get(t, {}).get("carriers") != c or st.get(t, {}).get("variables") != v: e.append(role + ": structural " + t)
    sy = r.get("systems", {})
    if set(sy) != set(PRE): e.append(role + ": system set")
    for n, (side, rk, sp, lc) in PRE.items():
        x = sy.get(n, {})
        if set(x) != SYSKEYS: e.append(role + ": system keys " + n); continue
        if x["side"] != side or len(x["side_addresses"]) != side: e.append(role + ": side " + n)
        if not (x["rank_et"] == x["rank_ds"] == x["rank_union"] == rk) or x["span_equal"] is not True: e.append(role + ": rank/span " + n)
        if x["support"] != sp or x["support_equals_ds_support"] is not True: e.append(role + ": support " + n)
        if x["leaf_carriers"] != lc: e.append(role + ": leaf carriers " + n)
    tb = r.get("tables", {})
    if set(tb) != set(TABLES) or any(tb[t] != {"violations": 0} for t in tb): e.append(role + ": tables")
    if r.get("instances") != INST: e.append(role + ": instances")
    co = r.get("controls", {})
    if set(co) != set(CONTROLS) or any(co[c] != "REJECTED" for c in co): e.append(role + ": controls")
    return e


def compare(p, c):
    e = check_one(p, "producer") + check_one(c, "checker")
    for k in ("structural", "systems", "tables", "instances", "controls"):
        if p.get(k) != c.get(k): e.append("producer/checker differ: " + k)
    return e


def main(pp, cp, outp):
    pb, cb = Path(pp).read_bytes(), Path(cp).read_bytes()
    p = json.loads(pb, object_pairs_hook=nodup); c = json.loads(cb, object_pairs_hook=nodup)
    errs = compare(p, c)
    tamper = {}
    def T(name, fn, target="p"):
        q, r = copy.deepcopy(p), copy.deepcopy(c)
        fn(q if target == "p" else r)
        tamper[name] = "DETECTED" if compare(q, r) else "MISSED"
    T("missing system", lambda x: x["systems"].pop("TM|3"))
    T("duplicated system record", lambda x: x["systems"].__setitem__("TM|4", x["systems"]["TM|3"]))
    T("substituted system", lambda x: x["systems"].__setitem__("MX|3", x["systems"]["MX|2"]))
    T("wrong rank", lambda x: x["systems"]["TM|2"].__setitem__("rank_et", 18), "c")
    T("wrong support", lambda x: x["systems"]["MX|3"].__setitem__("support", 8))
    T("wrong frozen hash", lambda x: x.__setitem__("frozen_result_sha256", "0" * 64))
    T("false digest", lambda x: x["structural"]["TM"].__setitem__("carrier_digest", "f" * 64), "c")
    T("wrong count", lambda x: x["structural"]["MX"].__setitem__("carriers", 17))
    T("wrong et row count", lambda x: x["systems"]["TM|1"].__setitem__("et_rows", x["systems"]["TM|1"]["et_rows"] + 1))
    T("false provenance", lambda x: x.__setitem__("role", "checker"))
    T("role confusion", lambda x: x.__setitem__("role", "producer"), "c")
    T("missing control", lambda x: x["controls"].pop("R5"))
    T("flipped control", lambda x: x["controls"].__setitem__("R2", "ACCEPTED"), "c")
    T("extra key", lambda x: x.__setitem__("note", "ok"))
    T("hidden violation", lambda x: x["tables"]["X3"].__setitem__("violations", 1))
    T("span not equal", lambda x: x["systems"]["CH|2"].__setitem__("span_equal", False))
    T("wrong instance", lambda x: x["instances"].__setitem__("Y4", "1/2"), "c")
    T("wrong leaf carriers", lambda x: x["systems"]["TM|2"].__setitem__("leaf_carriers", [676, 3381]))
    try:
        json.loads(pb.decode().replace('{\n "controls"', '{\n "controls": {}, \n "controls"', 1), object_pairs_hook=nodup)
        tamper["duplicated JSON key"] = "MISSED"
    except ValueError:
        tamper["duplicated JSON key"] = "DETECTED"
    if any(v != "DETECTED" for v in tamper.values()): errs.append("tamper control missed")
    rep = {"status": "GREEN" if not errs else "RED", "errors": errs, "tamper": tamper,
           "producer_sha256": hashlib.sha256(pb).hexdigest(), "checker_sha256": hashlib.sha256(cb).hexdigest(),
           "frozen_result_sha256": FROZEN, "systems": p.get("systems"), "structural": p.get("structural"),
           "tables": p.get("tables"), "instances": p.get("instances"), "controls": p.get("controls")}
    Path(outp).write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    print(rep["status"], errs, sum(v == "DETECTED" for v in tamper.values()), "/", len(tamper), "tamper detected")
    raise SystemExit(0 if not errs else 1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
