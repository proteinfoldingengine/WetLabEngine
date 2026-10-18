"""receiver_identification draft 9 (sec 16) freeze: COMPARATOR. Checks producer and checker certificates against the
preregistered exact instances (FREEZE.md section 2), equal exhaustive-universe counts and identity digests with zero
violations, preregistered outcomes and non-vacuity (section 3), the preregistered rule-panel classification, bounded
evidence (section 4) and rejecting controls (section 5); runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d9_review")
FROZEN_RESULT_SHA = "18a88aa5b1879994b0756dfe6faa921f37c7bdcb7b6cf7605ce512f1a465c875"
EXPECTED = {
    "X1.P1": ["3", "12"], "X1.genesis": ["10", "5"], "X1.grandparent": ["10", "5"], "X1.halfsplit": ["13/2", "17/2"],
    "X1.receiver_P1": 1, "X1.receiver_genesis": 0, "X1.receiver_grandparent": 0,
    "X2.p_before": ["0", "0"], "X2.T_plus": ["0", "1", "0"], "X2.T_minus": ["0", "0", "1"], "X2.p_after": ["1", "0"],
    "X2.totals": ["1", "1", "1", "1"], "X2.p_after_genesis": ["0", "0"], "X2.p_after_grandparent": ["0", "0"],
    "X2.p_after_halfsplit": ["1/2", "0"],
    "X3.Tx": ["1", "1", "4"], "X3.Txp": ["1", "-4", "4"], "X3.diff": ["0", "-5", "0"], "X3.changed_before": [2],
    "X3.changed_after": [1], "X3.totals": ["6", "6", "1", "1"],
    "X4.w": ["1", "0", "0", "0", "0", "0"], "X4.depths": [1, 2, 3, 4, 5, 6],
    "X5.P1": [["1"], ["1", "0"], ["1", "0", "0"]], "X5.genesis": [["1"], ["0", "1"], ["0", "0", "1"]],
    "X5.grandparent": [["1"], ["0", "1"], ["0", "1", "0"]], "X5.halfsplit": [["1"], ["1/2", "1/2"], ["1/2", "1/2", "0"]],
    "X6.orders": 12, "X6.maximal": [2, 3, 5], "X6.r": [0, 1, 1, 1, 0, 0], "X6.P1": ["12", "9"],
    "X6.genesis": ["19", "2"], "X6.grandparent": ["19", "2"], "X6.halfsplit": ["31/2", "11/2"],
    "X7.removable": [2, 3, 5], "X7.genesis_removable": False,
    "X8.T_plus": ["0", "1"], "X8.T_minus": ["-1", "0"], "X8.neg_T_plus": ["0", "-1"],
    "X9.T_e3": ["1", "0", "0"], "X9.T_e1": ["0", "1", "0"],
    "X10.dipole": ["1", "1", "-1"], "X10.P1": ["1", "0", "0"],
    "X11.erase": ["0"], "X11.double": ["2"], "X11.fixed_e2": ["0"]}
PANEL = {"P1": "111111", "genesis": "111100", "grandparent": "111100", "halfsplit": "111100", "erase": "101110",
         "double": "101110", "fixed_e2": "101110", "leafshift": "110110", "dipole": "111010", "sign": "011110"}
UNIVERSE_KEYS = ["trees", "pairs", "sequences", "nontrivial", "multi_max", "multi_fiber", "multi_order", "lemma_states",
                 "u16_lines", "u16_digest", "u16l_cases", "u16l_pos", "u16l_neg", "u16l_digest", "u16r_instances",
                 "u16r_digest", "u16p_cases", "u16p_ycases", "u16p_genesis_moved", "u16p_lines", "u16p_digest",
                 "u16j_rules", "u16j_oi", "u16j_e5", "u16j_eqp", "u16j_digest"] + \
                ["%s_%s" % (a, r) for r in ("P1", "genesis", "grandparent", "halfsplit") for a in ("oi", "eq", "neq")]
VIOL_KEYS = ["u16_viol", "u16l_viol", "u16r_viol", "u16p_viol", "u16j_viol"]
PREREG_COUNTS = {"trees": 874, "pairs": 19689, "sequences": 190109, "u16l_cases": 5913, "u16j_rules": 120,
                 "u16j_oi": 120, "u16j_e5": 1, "u16j_eqp": 1, "oi_P1": 19689, "eq_P1": 19689, "neq_P1": 0,
                 "oi_genesis": 19689, "oi_grandparent": 19689, "oi_halfsplit": 19689}
NONVACUOUS = ["nontrivial", "multi_max", "multi_fiber", "multi_order", "neq_genesis", "neq_grandparent", "neq_halfsplit",
              "u16l_pos", "u16l_neg", "u16p_ycases", "u16p_genesis_moved"]
BOUNDED = {"B16a_cases": 400, "B16a_seqs": 12000, "B16a_viol": 0, "B16b_grid": 15625,
           "B16b_solutions": [["1", "0", "0", "0", "0", "0"]]}
CONTROLS = ["R1_confluence_selects_P1", "R2_genesis_satisfies_E5", "R3_grandparent_satisfies_E5",
            "R4_halfsplit_satisfies_E5", "R5_E1_to_E4_force_P1", "R6_without_E2_forces_P1", "R7_absolute_e2_conserves",
            "R8_without_E3_forces_P1", "R9_without_E4_forces_P1", "R10_without_E1_forces_P1",
            "R11_jump_confluence_selects_P1", "R12_other_grid_vector_satisfies_E1_E5"]


class Red(Exception):
    pass


def need(c, msg):
    if not c:
        raise Red(msg)


def no_dup(pairs):
    keys = [k for k, _ in pairs]
    need(len(keys) == len(set(keys)), "duplicated key in certificate")
    return dict(pairs)


def load(raw):
    return json.loads(raw, object_pairs_hook=no_dup)


def check(prod, chk, result_sha):
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-9 bytes")
    for cert in (prod, chk):
        need(cert["meta"]["result_sha256"] == FROZEN_RESULT_SHA, "false provenance: certificate hash")
        need(set(cert["values"]) == set(EXPECTED), "key set differs from preregistered instances")
        need(set(cert["universe"]) == set(UNIVERSE_KEYS + VIOL_KEYS), "universe key set differs")
        need(cert["panel"] == PANEL, "rule-panel classification differs from preregistration")
    need(prod["meta"]["role"] == "producer" and chk["meta"]["role"] == "checker", "role confusion")
    for k, e in EXPECTED.items():
        need(prod["values"][k] == e, "producer mismatch at " + k)
        need(chk["values"][k] == e, "checker mismatch at " + k)
    for k in UNIVERSE_KEYS:
        need(prod["universe"][k] == chk["universe"][k], "universe count or digest mismatch: " + k)
    for k, v in PREREG_COUNTS.items():
        need(prod["universe"][k] == v, "preregistered count or outcome differs: " + k)
    for k in NONVACUOUS:
        need(prod["universe"][k] > 0, "non-vacuity failed: " + k)
    for k in VIOL_KEYS:
        need(prod["universe"][k] == 0 and chk["universe"][k] == 0, "exhaustive violation: " + k)
    for k, v in BOUNDED.items():
        need(chk["bounded"].get(k) == v, "bounded evidence differs: " + k)
    need(set(chk["controls"]) == set(CONTROLS), "control set differs from preregistration")
    for ctl in CONTROLS:
        need(chk["controls"].get(ctl) == "REJECTED", "rejecting control accepted: " + ctl)


def tamper_tests(prod, chk, sha):
    cases = []
    p = copy.deepcopy(prod); del p["values"]["X1.P1"]; cases.append(("missing", p, chk, sha))
    p = copy.deepcopy(prod); p["values"]["X1.P1"] = ["10", "5"]; cases.append(("wrong_value_P1_as_genesis", p, chk, sha))
    q = copy.deepcopy(chk); q["values"]["X2.p_after"] = ["0", "0"]; cases.append(("substituted", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["sequences"] -= 1; cases.append(("universe_count_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u16_digest"] = "0" * 64; cases.append(("digest_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["meta"]["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R1_confluence_selects_P1"] = "ACCEPTED"; cases.append(("control_flip_R1", prod, q, sha))
    q = copy.deepcopy(chk); del q["controls"]["R5_E1_to_E4_force_P1"]; cases.append(("control_missing", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u16_viol"] = 1; cases.append(("violation_hidden", prod, q, sha))
    q = copy.deepcopy(chk); q["bounded"]["B16a_viol"] = 2; cases.append(("bounded_violation", prod, q, sha))
    q = copy.deepcopy(chk); q["panel"]["genesis"] = "111110"; cases.append(("panel_flip_genesis_E5", prod, q, sha))
    q = copy.deepcopy(chk); q["bounded"]["B16b_solutions"] = [["1", "0", "0", "0", "0", "0"], ["0", "1", "0", "0", "0", "0"]]
    cases.append(("grid_nonunique", prod, q, sha))
    cases.append(("wrong_result_bytes", prod, chk, "1" * 64))
    out = {}
    for name, a, b, s in cases:
        try:
            check(a, b, s)
            out[name] = "NOT_DETECTED"
        except Red:
            out[name] = "DETECTED"
    raw = json.dumps(prod)
    try:
        load(raw[:-1] + ', "values": {}}')
        out["duplicated"] = "NOT_DETECTED"
    except Red:
        out["duplicated"] = "DETECTED"
    return out


def main():
    prod_raw, chk_raw = Path(sys.argv[1]).read_bytes(), Path(sys.argv[2]).read_bytes()
    sha = hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()
    report = {"producer_sha256": hashlib.sha256(prod_raw).hexdigest(),
              "checker_sha256": hashlib.sha256(chk_raw).hexdigest(), "result_sha256": sha}
    try:
        prod, chk = load(prod_raw), load(chk_raw)
        check(prod, chk, sha)
        report["universe"] = prod["universe"]; report["panel"] = prod["panel"]
        report["bounded"] = chk["bounded"]; report["controls"] = chk["controls"]
        report["tamper"] = tamper_tests(prod, chk, sha)
        need(all(v == "DETECTED" for v in report["tamper"].values()), "tampering not detected")
        report["status"] = "GREEN"
    except Red as e:
        report["status"] = "RED"
        report["reason"] = str(e)
    Path(sys.argv[3]).write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print(json.dumps(report, indent=1, sort_keys=True))
    sys.exit(0 if report["status"] == "GREEN" else 1)


if __name__ == "__main__":
    main()
