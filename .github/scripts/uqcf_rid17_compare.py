"""receiver_identification d17 freeze (section 23, field-to-state association): COMPARATOR. Checks producer and checker certificates against
the preregistered values of FREEZE.md section 3, equal identity digests, zero violations, the rejecting controls of
section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d17_review")
FROZEN = {"RESULT.md": "4f55e562a8dddb4ed565128104637294b15836f0a3f226afb854ba0c4cce05be",
          "SOURCE.md": "c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8",
          "CORRESPONDENCE.md": "1c4534458fdff2d8f5c1eeb264f9eab60e70d9af93d4d9e89297f2c397dde9f3"}
EXPECTED = {"Z1.unit": ["-1", "2", "-1"], "Z1.depth": ["-1", "3/2", "-1/2"], "Z2.star": ["-1", "3", "-1", "-1"],
            "Z3.genesis": [1, 0],
            "Z4.event": [["0", "0", "0"], ["0", "1", "2"], ["0", "0"], ["0", "1"], "0", "1"],
            "Z5.genesis_event": [["0", "0"], ["0", "1"], ["0"], ["0"]], "Z6.dense": [1, False]}
def U(carriers, positions, withch, leaves, gleaves):
    tab = {"local_dim_deg": positions + carriers, "blind_dim1": positions, "genesis_dim0": carriers,
           "own_grade_read": positions, "coefficients_match": positions}
    return {"carriers": carriers, "positions": positions, "positions_with_children": withch, "leaves": leaves,
            "genesis_leaves": gleaves, "tables": {t: dict(tab) for t in ("unit", "three", "depth", "alt")},
            "event": {"cases": leaves * 24, "field_identity": leaves * 24, "contrast_ok": (leaves - gleaves) * 12,
                      "genesis_coincide": gleaves * 12}}
PREREG = {"U7": U(85, 441, 189, 252, 69), "U8": U(200, 1246, 560, 686, 154)}
CONTROLS = ["R1_grounded_value_is_descendant_blind", "R2_parent_edge_read_is_descendant_blind",
            "R3_dense_J_gives_own_grade_everywhere", "R4_nonzero_blind_read_at_genesis", "R5_event_changes_retained_field",
            "R6_blind_read_preinformed", "R7_genesis_pair_fields_differ_after_event", "R8_nonroot_blind_dim_not_1"]
DIAG = {"dense", "digest", "universe_digest"}


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
        need(P["dense"] == C["dense"], "dense-control diagnostic differs between programs: " + u)
        for k, v in exp.items():
            need(P[k] == v, "producer preregistered value differs: %s.%s" % (u, k))
            need(C[k] == v, "checker preregistered value differs: %s.%s" % (u, k))


def tamper_tests(prod, chk, shas):
    cases = []
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = "0" * 64; cases.append(("flipped_identity_digest", prod, q, shas))
    q = copy.deepcopy(chk); del q["universes"]["U8"]["event"]; cases.append(("missing_record", prod, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["carriers"] += 1; cases.append(("duplicated_carrier", p, chk, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = prod["universes"]["U8"]["digest"]; cases.append(("substituted_universe", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z1.depth"][1] = "2"; cases.append(("wrong_value_Z1", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["tables"]["alt"]["blind_dim1"] -= 1
    cases.append(("wrong_dimension_both", p, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U8"]["dense"]["counts"]["1,own"] += 1; cases.append(("dense_diagnostic_altered", p, chk, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["SOURCE.md"] = "1" * 64; cases.append(("wrong_source_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R8_nonroot_blind_dim_not_1"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R5_event_changes_retained_field"] = "ACCEPTED_WRONGLY"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Z9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["event"]["field_identity"] -= 1; cases.append(("event_field_changed", prod, q, shas))
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
        report["instances"] = prod["instances"]; report["universes"] = prod["universes"]; 
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
