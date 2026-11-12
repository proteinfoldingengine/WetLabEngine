"""receiver_identification d18 freeze (section 24, initial blindness from the read ledger): COMPARATOR. Checks producer
and checker certificates against the preregistered values of FREEZE.md section 3, equal identity digests, zero
violations, the rejecting controls of section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d18_review")
FROZEN = {"RESULT.md": "b13d2cd4c2b688cb40ca9d31845f3d1cdbdb6230e0e03596e7f623e3dbd38ae6",
          "SOURCE.md": "c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8"}
EXPECTED = {"Z1.e2": ["1", "0", "-1"], "Z1.e1": ["1", "-1", "0"], "Z2.depth_one": ["1", "1", "-2"],
            "Z2.depth_inv": ["1", "0", "-1"], "Z3.lemma_dim": 3, "Z4.rsf_alt": [False, True],
            "Z5.theta0": ["1", "0"], "Z5.theta_neg1": ["0", "-1"], "Z6.childcount_sum": "-1"}
FAMS = ["F1", "F2", "F3", "F4", "F5", "F6", "F7"]
CONST = {"F1": "-1", "F2": "-3", "F3": "-1", "F4": "-1"}


def U(car, pos, wc, ev, lv, gl, npar, D, trip):
    nl = lv - gl
    fam = {f: {"K_carriers": car, "composite": trip, "genesis_read": car - 1,
               "blind": pos if f in CONST else lv, "own_grade": pos if f in CONST else lv} for f in FAMS}
    event = {f: {"pn_cases": lv * 6, "pn_ok": lv * 6, "nonroot_contrast_ok": nl * 3,
                 "nonroot_blind_before": nl * 3 if f in CONST else 0, "genesis_contrast_ok": gl * 3} for f in FAMS}
    total = {}
    for f, neg in CONST.items():
        total[f] = {t: {"contrast_ok": gl * 3, "blind_before": gl * 3 if t == neg else 0, "pn_cases": gl * 6, "pn_ok": gl * 6}
                    for t in (neg, "0", "2")}
        total[f]["neg_id"] = trip + pos + car
    elim = {an: {"dims": {"PN": D, "SC": D, "K": D, "ALL": D}, "family_exact": True} for an in ("unit", "depth", "alt")}
    return {"carriers": car, "positions": pos, "positions_with_children": wc, "leaves": lv, "genesis_leaves": gl,
            "cones": wc, "lemma_ok_carriers": car, "parameters": npar, "max_depth": D, "families": fam, "event": event,
            "total": total, "elimination": elim, "rs_f": {"one": wc, "k": 0, "inv": 0, "alt": ev}}


PREREG = {"U7": U(85, 441, 189, 68, 252, 69, 42, 6, 2858), "U8": U(200, 1246, 560, 217, 686, 154, 56, 7, 9298)}
CONTROLS = ["R1_cone_read_satisfies_PN", "R2_childcount_rule_satisfies_K", "R3_F5_blind_at_every_position_with_children",
            "R4_inverse_depth_reads_satisfy_RS_F", "R5_PN_space_larger_than_depth_tables", "R6_genesis_blind_with_theta_zero",
            "R7_named_family_violates_PN", "R8_lemma_dim_or_structure_fails"]
DIAG = {"R1_fail_prunings", "R2_fail_carriers", "digest", "universe_digest"}


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
        need(set(P) == set(C) == set(exp) | DIAG, "universe keys differ: " + u)
        need(P["digest"] == C["digest"], "identity digest mismatch: " + u)
        need(P["universe_digest"] == C["universe_digest"], "universe digest mismatch: " + u)
        for k in ("R1_fail_prunings", "R2_fail_carriers"):
            need(P[k] == C[k], "diagnostic differs between programs: %s.%s" % (u, k))
        for k, v in exp.items():
            need(P[k] == v, "producer preregistered value differs: %s.%s" % (u, k))
            need(C[k] == v, "checker preregistered value differs: %s.%s" % (u, k))


def tamper_tests(prod, chk, shas):
    cases = []
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = "0" * 64; cases.append(("flipped_identity_digest", prod, q, shas))
    q = copy.deepcopy(chk); del q["universes"]["U8"]["event"]; cases.append(("missing_record", prod, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["carriers"] += 1; cases.append(("duplicated_carrier", p, chk, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = prod["universes"]["U8"]["digest"]; cases.append(("substituted_universe", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z2.depth_one"][1] = "0"; cases.append(("wrong_value_Z2", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["elimination"]["alt"]["dims"]["PN"] += 1
    cases.append(("wrong_dimension_both", p, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U8"]["R2_fail_carriers"] += 1; cases.append(("diagnostic_altered", p, chk, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["SOURCE.md"] = "1" * 64; cases.append(("wrong_source_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R8_lemma_dim_or_structure_fails"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R7_named_family_violates_PN"] = "ACCEPTED_WRONGLY"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["families"]["F5"]["blind"] += 1; cases.append(("blind_count_changed", prod, q, shas))
    q = copy.deepcopy(chk); q["universes"]["U8"]["rs_f"]["alt"] -= 1; cases.append(("rs_f_count_changed", prod, q, shas))
    out = {}
    for name, a, b, s in cases:
        try:
            check(a, b, s); out[name] = "NOT_DETECTED"
        except (Red, KeyError):
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
