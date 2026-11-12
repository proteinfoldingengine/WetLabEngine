"""receiver_identification d15 freeze (section 21): COMPARATOR. Checks producer and checker certificates against the
preregistered values of FREEZE.md section 3, equal identity digests, zero violations, the rejecting controls of
section 4, and runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d15_review")
FROZEN = {"RESULT.md": "b32481cf40d83691176972eef1c1deb8caadb7f25c4febd352aadba487a9f40c",
          "CORRESPONDENCE.md": "2b2ba0083fc4a3dcc5caa0c98256916521f21882e1f5852d936f0065cb806a1a"}
EXPECTED = {"Y1.dump_residual": ["-1", "1"], "Y2.split_residual": ["-1/2", "1/2"], "Y3.sibling": [True, True, False],
            "Y4.annihilate": ["0", True, True], "Y5.P1_counts": [1, 1]}
RULES = {"P1": [True] * 4, "GenesisDump": [True, True, False, False], "Grandparent": [True, True, False, False],
         "Split": [True, True, False, False], "Annihilate": [False, True, True, True]}
RAND = {"tables": 300, "E2": 300, "NI": 300, "CNparent": 0, "P1": 0}
UNIQ = {"E2+CN": True, "E2+CNparent": True, "E2+NI+CNparent": True}
PREREG = {
    "U7": {"carriers": 151, "unknowns": 363, "by_depth": [37, 50, 38, 19, 6, 1],
           "dims": {"E2": 212, "E2+NI": 15, "E2+CN": 0, "E2+CNparent": 0, "CN": 37, "CNparent": 37, "NI+CN": 1, "E2+NI+CNparent": 0},
           "rules": RULES, "random_tables": RAND, "unique_P1": UNIQ},
    "U8": {"carriers": 413, "unknowns": 1085, "by_depth": [85, 124, 107, 63, 26, 7, 1],
           "dims": {"E2": 672, "E2+NI": 21, "E2+CN": 0, "E2+CNparent": 0, "CN": 85, "CNparent": 85, "NI+CN": 1, "E2+NI+CNparent": 0},
           "rules": RULES, "random_tables": RAND, "unique_P1": UNIQ}}
CONTROLS = ["R1_genesis_dump_satisfies_CNparent", "R2_grandparent_satisfies_CNparent", "R3_split_satisfies_CNparent",
            "R4_annihilation_satisfies_E2", "R5_sibling_rule_satisfies_E4", "R6_NI_alone_forces_P1",
            "R7_CN_without_E2_forces_P1", "R8_P1_with_one_substituted_carrier_satisfies_CNparent"]


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
        need(set(P) == set(C) == set(exp) | {"digest"}, "universe keys differ: " + u)
        need(P["digest"] == C["digest"], "identity digest mismatch: " + u)
        for k, v in exp.items():
            need(P[k] == v, "producer preregistered value differs: %s.%s" % (u, k))
            need(C[k] == v, "checker preregistered value differs: %s.%s" % (u, k))


def tamper_tests(prod, chk, shas):
    cases = []
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = "0" * 64; cases.append(("flipped_identity_digest", prod, q, shas))
    q = copy.deepcopy(chk); q["universes"]["U8"]["by_depth"] = q["universes"]["U8"]["by_depth"][:-1]; cases.append(("missing_record", prod, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U7"]["carriers"] += 1; cases.append(("duplicated_carrier", p, chk, shas))
    q = copy.deepcopy(chk); q["universes"]["U7"]["digest"] = prod["universes"]["U8"]["digest"]; cases.append(("substituted_universe", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Y2.split_residual"][0] = "-1/3"; cases.append(("wrong_fraction_Y2", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U8"]["dims"]["E2+NI"] = 15
    cases.append(("wrong_dimension_both", p, q, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["RESULT.md"] = "1" * 64; cases.append(("wrong_result_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R8_P1_with_one_substituted_carrier_satisfies_CNparent"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R1_genesis_dump_satisfies_CNparent"] = "ACCEPTED_WRONGLY"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["Y9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U7"]["rules"]["GenesisDump"] = [True] * 4
    cases.append(("receiver_selection_control_removed", p, q, shas))
    out = {}
    for name, a, b, s in cases:
        try:
            check(a, b, s); out[name] = "NOT_DETECTED"
        except Red:
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
        report["instances"] = prod["instances"]; report["universes"] = prod["universes"]; report["controls"] = chk["controls"]
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
