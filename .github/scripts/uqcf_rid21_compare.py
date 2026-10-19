"""receiver_identification d21 freeze (section 27, a leaf reads only what it holds, and one record climb fixes the reads up
to its depth): COMPARATOR. Checks producer and checker certificates against the preregistered values of FREEZE.md section 3,
equal identity digests, equal diagnostics, zero violations, the rejecting controls of section 4, and runs tampering
controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d21_review")
FROZEN = {"RESULT.md": "7c0eb6f830e6ca167ec62839e760d092c88fb1084ce72c91877b7c314414b229"}
EXPECTED = {"Y1.read": ["1", "-1", "1"], "Y1.defect": ["0", "-1", "1"],
            "Y2": {"PN": 6, "PN+S_L": 3, "PN+W2_1": 3, "PN+S_L+C_recv": 1, "PN+S_L+CL_1": 2, "PN+S_L+CL_2": 1,
                   "PN+S_L+BU_1": 2, "PN+S_L+BU_2": 1, "PN+CL_1": 5, "PN+CL_2": 4},
            "Y3": ["0", "-7", "8"], "Y4": {"r": "3/2", "before": "0", "after": "5"}, "Y5": {"before": "-3", "after": "2"}}


def dims(N):
    t = N * (N + 1) // 2
    d = {"PN": t, "PN+S_L": N, "PN+W2_1": N, "PN+S_L+C_recv": 1}
    for D in range(1, N):
        d["PN+S_L+CL_%d" % D] = N - D; d["PN+S_L+BU_%d" % D] = N - D; d["PN+CL_%d" % D] = t - D
    return d


def big(N, car, lv, sn, unk, pnc, w1, hc, hv, hs, slv):
    return {"carriers": car, "leaves": lv, "sum_n": sn, "unknowns": unk, "dims": dims(N),
            "horizon": {"carriers": hc, "vertices": hv, "sharp": hs, "ok": True}, "family_acquisition": True,
            "ledger": {"cases": pnc, "ok": pnc}, "kernel": {"cases": w1, "ok": w1, "T1_zero": w1},
            "before_after": {"cases": 2 * lv, "before_after": 2 * lv, "pair": 2 * lv},
            "nu_off": {"pn_and_climbs_hold": True, "SL_violations": slv}, "R7_holds": False,
            "row_counts": {"SL": w1}, "event": {k: 9 * lv for k in ("cases", "pn", "conserved", "blind", "contrast")}}


PREREG = {"U3": big(3, 4, 4, 9, 23, 11, 7, [3, 4], [4, 8], [1, 0], 1),
          "U7": big(7, 85, 252, 526, 3384, 1621, 1369, [7, 30, 60, 78, 84, 85], [85, 248, 398, 484, 517, 525],
                    [150, 86, 33, 8, 1, 0], 227),
          "U8": big(8, 200, 686, 1446, 10744, 5093, 4407, [8, 45, 113, 167, 192, 199, 200],
                    [200, 595, 997, 1267, 1394, 1436, 1445], [402, 270, 127, 42, 9, 1, 0], 660)}
CONTROLS = ["R1_nu_off_leaf_local", "R2_climb_without_leaf_locality_forces_identity", "R3_no_depth_horizon",
            "R4_identity_below_horizon", "R5_ledger_forces_zero_extension_square", "R6_general_defect_vanishes",
            "R7_offdiagonal_passes_leaf_locality", "R8_case_failure"]


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
    p = copy.deepcopy(prod); p["instances"]["Y1.defect"][1] = "0"; cases.append(("wrong_value_Y1", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["dims"]["PN+S_L+CL_3"] = 1
    cases.append(("no_horizon_both", p, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U8"]["kernel"]["nonzero_off"] += 1
    cases.append(("diagnostic_altered", p, chk, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["row_counts"]["PN"] -= 1; cases.append(("row_count_altered", p, chk, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["RESULT.md"] = "1" * 64; cases.append(("wrong_result_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R8_case_failure"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R2_climb_without_leaf_locality_forces_identity"] = "ACCEPTED_WRONGLY"
    cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Y9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U7"]["horizon"]["sharp"][0] -= 1
    cases.append(("sharpness_case_dropped_both", p, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["nu_off"]["SL_violations"] = 0
    cases.append(("witness_leaf_local_both", p, q, shas))
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
