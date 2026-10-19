"""receiver_identification d19 freeze (section 25, the Genesis datum is forced): COMPARATOR. Checks producer and checker
certificates against the preregistered values of FREEZE.md section 3, equal identity digests, equal diagnostics, zero
violations, the rejecting controls of section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d19_review")
FROZEN = {"RESULT.md": "9f307412224e835f4fccedccdabc408ab0e48c06b74ace9dbc3795a1b7a2c615",
          "SOURCE.md": "c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8"}
EXPECTED = {"Z1.theta_neg1": [["0", "-1"], ["0", "-1"]], "Z1.theta0": [["1", "-1"], ["0", "0"]],
            "Z2.total": ["0", "0", "-1"], "Z2.zero": ["1", "0", "-1"], "Z3.G5": [["0", "1", "-2"], ["0", "0", "-1"]],
            "Z4.inv_dim": 1, "Z5.genesis": ["0", "-1"], "Z6.arb_dim": 2, "Z7.comp_dim": 1}
NEG = {"G1": "-1", "G2": "-3", "G3": "-1", "G4": "-1"}
THETAS = ["-1", "-3", "0", "2"]


def U(car, pos, lv, gl, cases, unk, top, D, sq):
    truth = {f: {t: (cases if t == neg else 0) for t in THETAS} for f, neg in NEG.items()}
    arb = {f: {"consistent": True, "dim": top, "neg_total_solves": True, "forced_to_minus_one": unk - top,
               "free_are_top_roots": True} for f in ("G1", "G3")}
    arb["G5"] = {"consistent": False}
    ev = {f: {"pn_ok": lv * 6, "cases": lv * 6, "conserved": lv * 6, "contrast_ok": lv * 3, "pairs": lv * 3, "neg_id": sq}
          for f in NEG}
    return {"carriers": car, "positions": pos, "leaves": lv, "genesis_leaves": gl, "cases": cases, "unknowns": unk,
            "top_carriers": top, "max_depth": D, "sum_sq": sq, "truth_const": truth, "arbitrary": arb,
            "composite": {"dim": 1, "contains_const": True}, "p1_invariant": {"dim": 1, "contains_total": True},
            "event": ev, "zero_apex_fail": {f: pos for f in NEG}}


PREREG = {"U7": U(85, 441, 252, 69, 899, 526, 48, 6, 3384), "U8": U(200, 1246, 686, 154, 2788, 1446, 115, 7, 10744)}
CONTROLS = ["R1_zero_datum_satisfies_CN_F_at_apex", "R2_nonconstant_mu_satisfies_CN_F_everywhere",
            "R3_wrong_theta_satisfies_CN_F_somewhere", "R4_arbitrary_datum_space_wrong", "R5_G5_arbitrary_system_consistent",
            "R6_p1_invariant_space_wrong", "R7_composite_space_wrong", "R8_event_violation"]
KEYS = (set(PREREG["U7"]) - {"truth_const"}) | {"truth", "digest", "universe_digest"}


class Red(Exception):
    pass


def need(c, msg):
    if not c:
        raise Red(msg)


def no_dup(pairs):
    keys = [k for k, _ in pairs]
    need(len(keys) == len(set(keys)), "duplicated key in certificate")
    return dict(pairs)


def load(raw): return json.loads(raw, object_pairs_hook=no_dup)


def check(prod, chk, shas):
    need(shas == FROZEN, "frozen document bytes differ")
    need(prod["role"] == "producer" and chk["role"] == "checker", "role confusion")
    for cert in (prod, chk):
        need(cert["result_sha256"] == FROZEN["RESULT.md"], "false provenance: certificate hash")
        need(set(cert["instances"]) == set(EXPECTED), "instance key set differs from preregistration")
        need(set(cert["universes"]) == set(PREREG), "universe set differs")
        need(cert["violations"] == [], "violations reported")
        need(set(cert["controls"]) == set(CONTROLS), "control set differs from preregistration")
        for ctl in CONTROLS:
            need(cert["controls"][ctl] == "REJECTED", "rejecting control accepted: " + ctl)
        for k, e in EXPECTED.items():
            need(cert["instances"][k] == e, cert["role"] + " mismatch at " + k)
    for u, exp in PREREG.items():
        P, C = prod["universes"][u], chk["universes"][u]
        need(set(P) == set(C) == KEYS, "universe keys differ: " + u)
        need(P["digest"] == C["digest"], "identity digest mismatch: " + u)
        need(P["universe_digest"] == C["universe_digest"], "universe digest mismatch: " + u)
        need(P["truth"] == C["truth"], "truth table (incl. G5/G6 diagnostics) differs between programs: " + u)
        for cert, nm in ((P, "producer"), (C, "checker")):
            need(set(cert["truth"]) == set(NEG) | {"G5", "G6"}, nm + " family set differs: " + u)
            for f in NEG:
                need(cert["truth"][f] == exp["truth_const"][f], "%s truth table differs: %s.%s" % (nm, u, f))
            for f in ("G5", "G6"):
                need(set(cert["truth"][f]) == set(THETAS), nm + " theta set differs")
                need(all(v < exp["cases"] for v in cert["truth"][f].values()), "%s %s holds everywhere" % (nm, f))
            for k, v in exp.items():
                if k == "truth_const":
                    continue
                need(cert[k] == v, "%s preregistered value differs: %s.%s" % (nm, u, k))


def tamper_tests(prod, chk, shas):
    cases = []
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = "0" * 64; cases.append(("flipped_identity_digest", prod, q, shas))
    q = copy.deepcopy(chk); del q["universes"]["U8"]["event"]; cases.append(("missing_record", prod, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["carriers"] += 1; cases.append(("duplicated_carrier", p, chk, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = prod["universes"]["U8"]["digest"]; cases.append(("substituted_universe", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z3.G5"][0][2] = "-1"; cases.append(("wrong_value_Z3", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["arbitrary"]["G1"]["dim"] += 1
    cases.append(("wrong_dimension_both", p, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U8"]["truth"]["G6"]["-1"] += 1; cases.append(("diagnostic_altered", p, chk, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["SOURCE.md"] = "1" * 64; cases.append(("wrong_source_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R8_event_violation"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R5_G5_arbitrary_system_consistent"] = "ACCEPTED_WRONGLY"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["arbitrary"]["G5"]["consistent"] = True; cases.append(("consistency_flipped", prod, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U7"]["truth"]["G5"]["-1"] = c["universes"]["U7"]["cases"]
    cases.append(("nonconstant_holds_everywhere_both", p, q, shas))
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
        report["instances"] = prod["instances"]; report["universes"] = prod["universes"]
        report["controls"] = chk["controls"]
        report["tamper"] = tamper_tests(prod, chk, shas)
        need(all(v == "DETECTED" for v in report["tamper"].values()), "tampering not detected")
        report["status"] = "GREEN"
    except Red as e:
        report["status"] = "RED"; report["reason"] = str(e)
    Path(sys.argv[3]).write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in report if k in ("status", "reason", "tamper", "frozen_sha256")}, indent=1, sort_keys=True))
    sys.exit(0 if report["status"] == "GREEN" else 1)


if __name__ == "__main__":
    main()
