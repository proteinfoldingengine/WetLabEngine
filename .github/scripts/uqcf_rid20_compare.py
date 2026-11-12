"""receiver_identification d20 freeze (section 26, every vertex is a possible receiver): COMPARATOR. Checks producer and
checker certificates against the preregistered values of FREEZE.md section 3, equal identity digests, equal diagnostics,
zero violations, the rejecting controls of section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d20_review")
FROZEN = {"RESULT.md": "2e10cfddb22129177e304e7a4456055d69769f42c36be811277c856cbd32883c"}
EXPECTED = {"Z1": ["0", "-1", "1", "1"], "Z2": {"PN": 6, "PN+Z": 3, "PN+CN_F": 2}, "Z3.dump": ["1", "0"],
            "Z3.field0": ["1", "-1"], "Z4.before": ["0", "0"], "Z4.after": "1", "Z5": ["0", "1", "-2"]}
FAMS = ["G1", "G2", "G3", "G4", "G5", "G6"]
THETAS = ["-1", "-3", "0", "2"]


def dims(N, w2):
    t = N * (N + 1) // 2
    d = {"PN": t, "PN+Z": N, "PN+CN_F": 2, "PN+G+": N, "PN+C_recv": t - (2 * N - 3), "PN+C_climb": t - (2 * N - 3),
         "PN+S": N, "PN+S_leaf": 2 * N - 1, "PN+S+C_climb": 1, "PN+S+C_recv": 1, "PN+S+G+": 1}
    if w2:
        d.update({"PN+W2_F": N, "PN+W2_F+C_recv": 1})
    return d


def big(N, car, lv, gl, sn, unk, pnc, nonanc):
    zt = {}
    for f in FAMS:
        for th in THETAS:
            full = (f in ("G1", "G3", "G4") and th == "-1") or (f == "G2" and th == "-3")
            zt[f + ":" + th] = lv if full else (gl if f in ("G5", "G6") and th == "-1" else 0)
    keys = [f + ":" + th for f in FAMS for th in THETAS]
    wit = {"genesis_dump": {"pn": pnc, "z_holds": 0}, "field_zero": {"pn": pnc, "z_holds": 0},
           "nu_off": {"pn": pnc, "climb_blind": lv, "S_everywhere": False}}
    if nonanc is not None:
        wit["nu_off"].update({"nonancestor_leaves": nonanc, "z_holds": lv - nonanc})
    return {"carriers": car, "leaves": lv, "genesis_leaves": gl, "sum_n": sn, "unknowns": unk, "pn_cases": pnc,
            "dims": dims(N, N == 7), "kappa_id_small": True, "R6_holds": False,
            "field_identity": {k: sn for k in keys}, "field_pn": {k: pnc for k in keys}, "field_z": zt,
            "witnesses": wit, "event": {k: 9 * lv for k in ("cases", "pn", "conserved", "blind", "contrast")}}


PREREG = {"U3": {"carriers": 4, "leaves": 4, "sum_n": 9, "unknowns": 23, "kappa_id_small": True, "R6_holds": False,
                 "dims": {"PN": 6, "PN+Z": 3, "PN+CN_F": 2}},
          "U7": big(7, 85, 252, 69, 526, 3384, 1621, 88), "U8": big(8, 200, 686, 154, 1446, 10744, 5093, None)}
CONTROLS = ["R1_genesis_dump_leaf_blind", "R2_zero_datum_field_leaf_blind", "R3_nu_off_cone_local",
            "R4_climb_alone_forces_identity", "R5_apex_alone_forces_identity", "R6_offdiagonal_passes_leaf_blindness",
            "R7_unpredicted_field_setting_leaf_blind", "R8_event_violation", "R9_PN_Z_not_identity_on_small"]


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


def sub_eq(exp, got, path):
    if isinstance(exp, dict):
        need(isinstance(got, dict), "not a record: " + path)
        for k, v in exp.items():
            need(k in got, "missing record: " + path + "." + k)
            sub_eq(v, got[k], path + "." + k)
    else:
        need(exp == got, "preregistered value differs: %s (%r vs %r)" % (path, exp, got))


def check(prod, chk, shas):
    need(shas == FROZEN, "frozen document bytes differ")
    need(prod["role"] == "producer" and chk["role"] == "checker", "role confusion")
    need(set(prod) == set(chk) == {"role", "result_sha256", "universes", "instances", "controls", "violations"}, "certificate keys")
    for cert in (prod, chk):
        need(cert["result_sha256"] == FROZEN["RESULT.md"], "false provenance: certificate hash")
        need(cert["violations"] == [], "violations reported")
        need(set(cert["instances"]) == set(EXPECTED), "instance key set differs from preregistration")
        for k, e in EXPECTED.items():
            need(cert["instances"][k] == e, cert["role"] + " mismatch at " + k)
        need(set(cert["controls"]) == set(CONTROLS), "control set differs from preregistration")
        for c in CONTROLS:
            need(cert["controls"][c] == "REJECTED", "rejecting control accepted: " + c)
        need(set(cert["universes"]) == set(PREREG), "universe set differs")
        for u, exp in PREREG.items():
            sub_eq(exp, cert["universes"][u], cert["role"] + "." + u)
            need(set(cert["universes"][u]["dims"]) == set(exp["dims"]), "system set differs: " + u)
    for u in PREREG:
        need(prod["universes"][u] == chk["universes"][u],
             "producer and checker records differ (identity digests or diagnostics): " + u)


def tamper_tests(prod, chk, shas):
    cases = []
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = "0" * 64; cases.append(("flipped_identity_digest", prod, q, shas))
    q = copy.deepcopy(chk); del q["universes"]["U8"]["event"]; cases.append(("missing_record", prod, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["carriers"] += 1; cases.append(("duplicated_carrier", p, chk, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["universe_digest"] = prod["universes"]["U8"]["universe_digest"]
    cases.append(("substituted_universe", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z1"][1] = "0"; cases.append(("wrong_value_Z1", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["dims"]["PN+C_climb"] += 1
    cases.append(("wrong_dimension_both", p, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U8"]["witnesses"]["nu_off"]["nonancestor_leaves"] += 1
    cases.append(("diagnostic_altered", p, chk, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["row_counts"]["PN"] -= 1; cases.append(("row_count_altered", p, chk, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["RESULT.md"] = "1" * 64; cases.append(("wrong_result_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R8_event_violation"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R4_climb_alone_forces_identity"] = "ACCEPTED_WRONGLY"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U7"]["field_z"]["G5:-1"] = c["universes"]["U7"]["leaves"]
    cases.append(("nonconstant_mu_blind_both", p, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["kappa_id_small"] = False
    cases.append(("finite_artifact_leaks_both", p, q, shas))
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
