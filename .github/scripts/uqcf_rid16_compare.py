"""receiver_identification d16 freeze ([D16] + section 22): COMPARATOR. Checks producer and checker certificates against
the preregistered values of FREEZE.md section 3, equal identity digests, zero violations, the rejecting controls of
section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d16_review")
FROZEN = {"RESULT.md": "e1eaf4592be4f234c18eff86fbc831a194a87fc3955402ce39724d35ce98715d",
          "SOURCE.md": "c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8",
          "CORRESPONDENCE.md": "ab8d79316aeb2ced8bf52ba3c07e79b9975f63f8a85b3502de1f5936d76603fb"}
EXPECTED = {"Z1.depth_witness": ["1", "2"], "Z2.green_cone": [["0", "1", "1", "0"], ["1", "1"]],
            "Z3.signed_step": [[True, True, False, False, False], "2"],
            "Z4.pair": [["c1", "c3", "total"], ["c1", "total"], "0", "1"], "Z5.dump": "-1"}
SOLS = {"depth_indicators_solve_C": True, "unit_solves_C_RS": True, "depth_solves_C": True, "depth_violates_RS": True}
def U(carriers, unknowns, cones, classes, dimC):
    return {"carriers": carriers, "unknowns": unknowns, "cones": cones, "leaf_classes": classes,
            "dims": {"C": dimC, "C+RS": 1}, "solutions": SOLS, "random_tables": {"tables": 102, "mismatches": 0},
            "green": {"cones": cones, "violations": 0, "laplacian_exact": True}, "prop224": {"classes": classes, "violations": 0}}
PREREG = {"U7": U(84, 2417, 189, 151, 6), "U8": U(199, 8052, 560, 413, 7)}
GRID = {"vectors": 1554, "E2": 179, "E5plus": 259, "E2_E5plus": 32, "R": 4, "CN": 4, "deletion": 4, "E2_E5plus_nonneg": 4,
        "E2_E5plus_notR": 28, "mismatch_R_deletion": 0, "mismatch_CN_R": 0, "mismatch_CN_implies_E5plus": 0}
CONTROLS = ["R1_T_depth_satisfies_RS", "R2_nonconstant_table_satisfies_RS", "R3_C_alone_forces_dim_1",
            "R4_genesis_dump_is_coordinate_deletion", "R5_signed_step_satisfies_R", "R6_signed_step_satisfies_CN",
            "R7_depth_response_passes_green_cone_locality", "R8_genesis_dump_keeps_retained_cone_totals",
            "R9_E2_E5plus_forces_P1_without_positivity"]


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
        need(cert["grid"] == GRID, cert["role"] + " grid differs from preregistration")
        need(set(cert["controls"]) == set(CONTROLS), "control set differs from preregistration")
        for ctl in CONTROLS:
            need(cert["controls"][ctl] == "REJECTED", "rejecting control accepted: " + ctl)
        for k, e in EXPECTED.items():
            need(cert["instances"][k] == e, cert["role"] + " mismatch at " + k)
    for u, exp in PREREG.items():
        P, C = prod["universes"][u], chk["universes"][u]
        need(set(P) == set(C) == set(exp) | {"digest"}, "universe keys differ: " + u)
        need(P["digest"] == C["digest"], "identity digest mismatch: " + u)
        for k, v in exp.items():
            need(P[k] == v, "producer preregistered value differs: %s.%s" % (u, k))
            need(C[k] == v, "checker preregistered value differs: %s.%s" % (u, k))


def tamper_tests(prod, chk, shas):
    cases = []
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = "0" * 64; cases.append(("flipped_identity_digest", prod, q, shas))
    q = copy.deepcopy(chk); del q["universes"]["U8"]["green"]; cases.append(("missing_record", prod, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["carriers"] += 1; cases.append(("duplicated_carrier", p, chk, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = prod["universes"]["U8"]["digest"]; cases.append(("substituted_universe", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z1.depth_witness"][1] = "1"; cases.append(("wrong_value_Z1", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["dims"]["C+RS"] = 7
    cases.append(("wrong_dimension_both", p, q, shas))
    p = copy.deepcopy(prod); p["grid"]["E2_E5plus_notR"] = 0; cases.append(("signed_counterexamples_removed", p, chk, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["SOURCE.md"] = "1" * 64; cases.append(("wrong_source_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R9_E2_E5plus_forces_P1_without_positivity"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R1_T_depth_satisfies_RS"] = "ACCEPTED_WRONGLY"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["prop224"]["violations"] = 1; cases.append(("prop224_violation", prod, q, shas))
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
        report["instances"] = prod["instances"]; report["universes"] = prod["universes"]; report["grid"] = prod["grid"]
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
