"""receiver_identification draft 11 (sec 17) freeze: COMPARATOR. Checks producer and checker certificates against the
preregistered exact instances (FREEZE.md section 2, values transcribed from the hand-written table), equal
exhaustive-universe counts and identity digests with zero violations, the preregistered assignment-panel flags,
non-vacuity (section 3), bounded evidence (section 4) and rejecting controls (section 5); runs tampering controls.
Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d11_review")
FROZEN_RESULT_SHA = "2c730b0bec6defa8f40043340c299977f9efabeb07e0d71fb939f88cb5440679"
EXPECTED = {
    "X1.gtax_M": [["1", "1/2", "1/2", "1/2"], ["0", "1/2", "0", "0"], ["0", "0", "1/2", "0"], ["0", "0", "0", "1/2"]],
    "X1.gtax_a": ["1", "1/2", "1/2", "1/2"], "X1.colsums": ["1", "1", "1", "1"],
    "X2.gtax_before": ["10", "5/2", "7/2", "1"], "X2.gtax_after": ["10", "6", "1"], "X2.gtax_increment": "7/2",
    "X2.gtax_totals": ["17", "17"], "X2.own_before": ["3", "5", "7", "2"], "X2.own_after": ["3", "12", "2"],
    "X3.gptb_p": [["1/4", "0"], ["3/4", "0"]], "X3.gtax_p": [["0", "0"], ["1/2", "0"]],
    "X3.own_p": [["0", "0"], ["1", "0"]], "X3.sat_p": [["0", "0"], ["0", "0"]],
    "X3.acq": [False, True, True, False], "X3.gptb_ABDr": ["3/4", "1/4", "1/2", "1/3"],
    "X4.x_plus": ["1", "1", "2", "1"], "X4.x_minus": ["1", "4/3", "1", "5/3"], "X4.totals": ["5", "5"],
    "X4.before_plus": ["7/4", "5/4", "1", "1"], "X4.before_minus": ["19/12", "5/4", "1/2", "5/3"],
    "X4.Px_plus": ["1", "3", "1"], "X4.Px_minus": ["1", "7/3", "5/3"],
    "X4.after_plus": ["7/4", "9/4", "1"], "X4.after_minus": ["19/12", "7/4", "5/3"],
    "X4.p_before": ["5/4", "5/4"], "X4.p_after": ["9/4", "7/4"], "X4.separation": "1/2", "X4.leaf_holding": ["1", "1/2"],
    "X4.oneloc_before": "1/4",
    "X5.before": "1/2", "X5.after": "1", "X5.acq": False,
    "X6.C": ["15", "12", "7"], "X6.sumC": "34", "X6.total": "15", "X6.W1eq": False,
    "X7.before": ["8", "7", "0"], "X7.after": ["15", "0"], "X7.changed_nonreceivers": [0],
    "X8.chain2": [2, 5, 1, 1], "X8.chain5": [5, 55, 4, 10], "X8.T4": [6, 43, 3, 4], "X8.star3": [8, 56, 3, 3],
    "X8.bin2": [25, 493, 6, 10], "X8.mixed7": [27, 534, 6, 10], "X8.chain2_noW2": 2,
    "X9.M12": "1/4", "X9.M12_chain": "1/4", "X9.M32": "0", "X9.M21": "0"}
FLAGS = {"own": "111111111111", "gtax": "111111100000", "half": "111111100000", "deep": "111111100000",
         "sat": "111111100000", "mixed": "111111100000", "negative": "101101100000", "cone": "011100100000",
         "parent": "111000100000"}
PANEL = {"U17A": FLAGS, "U17B": FLAGS}
UNIVERSE_KEYS = ["ue_trees", "ue_lines", "ue_digest", "ue_n_ge2_dim_pos", "ue_noW2_gt", "flags_digest"] + \
    ["%s_%s" % (u, k) for u in ("u17a", "u17b") for k in ("carriers", "covers", "prunings", "prunings_pno", "lines", "digest")] + \
    ["nv_" + k for k in ("acq", "nonacq", "b0_a0", "corr_bpos", "D0", "deg2", "deg3")]
VIOL_KEYS = ["ue_viol", "u17a_viol", "u17b_viol"]
PREREG_COUNTS = {"ue_trees": 156, "ue_lines": 156, "ue_n_ge2_dim_pos": 155, "u17a_carriers": 676, "u17a_covers": 2652,
                 "u17a_prunings": 2652, "u17a_prunings_pno": 2600, "u17a_lines": 18564, "u17b_carriers": 182,
                 "u17b_covers": 593, "u17b_prunings": 593, "u17b_prunings_pno": 462, "u17b_lines": 4151}
NONVACUOUS = ["ue_noW2_gt"] + ["nv_" + k for k in ("acq", "nonacq", "b0_a0", "corr_bpos", "D0", "deg2", "deg3")]
BOUNDED = {"B17a_grid": 125, "B17a_W1eq_W2_W4": 125, "B17a_valid": 75, "B17a_ii": 1, "B17a_iii": 1, "B17a_iv": 1,
           "B17a_corr": 50, "B17a_corr_bpos": 30, "B17a_oneloc": 20}
CONTROLS = ["R1_W1_W2_W4_force_own", "R2_cone_is_partition", "R3_parent_is_local", "R4_gtax_every_pruning_acquires",
            "R5_sign_redundant", "R6_existential_implies_universal", "R7_b0_suffices", "R8_without_W4",
            "R9_without_W2", "R10_blind_with_b_nonzero"]


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
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-11 bytes")
    for cert in (prod, chk):
        need(cert["meta"]["result_sha256"] == FROZEN_RESULT_SHA, "false provenance: certificate hash")
        need(set(cert["values"]) == set(EXPECTED), "key set differs from preregistered instances")
        need(set(cert["universe"]) == set(UNIVERSE_KEYS + VIOL_KEYS), "universe key set differs")
        need(cert["panel"] == PANEL, "assignment-panel flags differ from preregistration")
    need(prod["meta"]["role"] == "producer" and chk["meta"]["role"] == "checker", "role confusion")
    for k, e in EXPECTED.items():
        need(prod["values"][k] == e, "producer mismatch at " + k)
        need(chk["values"][k] == e, "checker mismatch at " + k)
    for k in UNIVERSE_KEYS:
        need(prod["universe"][k] == chk["universe"][k], "universe count or digest mismatch: " + k)
    for k, v in PREREG_COUNTS.items():
        need(prod["universe"][k] == v, "preregistered count differs: " + k)
    for k in NONVACUOUS:
        need(prod["universe"][k] > 0, "non-vacuity failed: " + k)
    for k in VIOL_KEYS:
        need(prod["universe"][k] == 0 and chk["universe"][k] == 0, "exhaustive violation: " + k)
    need(chk["bounded"] == BOUNDED, "bounded evidence differs from preregistration")
    need(set(chk["controls"]) == set(CONTROLS), "control set differs from preregistration")
    for ctl in CONTROLS:
        need(chk["controls"].get(ctl) == "REJECTED", "rejecting control accepted: " + ctl)


def tamper_tests(prod, chk, sha):
    cases = []
    p = copy.deepcopy(prod); del p["values"]["X4.separation"]; cases.append(("missing", p, chk, sha))
    p = copy.deepcopy(prod); p["values"]["X3.acq"] = [True, True, True, False]; cases.append(("wrong_value_gptb_acq", p, chk, sha))
    q = copy.deepcopy(chk); q["values"]["X2.gtax_increment"] = "7"; cases.append(("substituted", prod, q, sha))
    p = copy.deepcopy(prod); p["values"]["X8.T4"] = [6, 43, 4, 4]; cases.append(("wrong_dim", p, chk, sha))
    q = copy.deepcopy(chk); q["universe"]["u17a_prunings"] -= 1; cases.append(("universe_count_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["ue_digest"] = "0" * 64; cases.append(("digest_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["meta"]["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R6_existential_implies_universal"] = "ACCEPTED"; cases.append(("control_flip_R6", prod, q, sha))
    q = copy.deepcopy(chk); del q["controls"]["R3_parent_is_local"]; cases.append(("control_missing", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u17b_viol"] = 1; cases.append(("violation_hidden", prod, q, sha))
    q = copy.deepcopy(chk); q["bounded"]["B17a_ii"] = 2; cases.append(("bounded_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["panel"]["U17B"] = dict(q["panel"]["U17B"]); q["panel"]["U17B"]["gtax"] = "111111110000"
    cases.append(("flags_flip_gtax_i", prod, q, sha))
    p = copy.deepcopy(prod); p["panel"]["U17A"] = dict(p["panel"]["U17A"]); p["panel"]["U17A"]["cone"] = "111100100000"
    cases.append(("flags_flip_cone_W1", p, chk, sha))
    q = copy.deepcopy(chk); q["universe"]["nv_corr_bpos"] = 0; p = copy.deepcopy(prod); p["universe"]["nv_corr_bpos"] = 0
    cases.append(("vacuous_corr", p, q, sha))
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
