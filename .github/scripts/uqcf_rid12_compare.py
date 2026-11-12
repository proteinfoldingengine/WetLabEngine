"""receiver_identification draft 12 (sec 18) freeze: COMPARATOR. Checks producer and checker certificates against the
preregistered exact instances (FREEZE.md section 2, values transcribed from the hand-written table), equal
exhaustive-universe counts and identity digests with zero violations and the preregistered counts and confusion
cells (section 3), bounded evidence (section 4) and rejecting controls (section 5); runs tampering controls.
Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d12_review")
FROZEN_RESULT_SHA = "509fdab734431a15cc99e3d45d8748fcb5267df68c71ef799b00ff797fdb055e"
H2 = [["0", "1/2"], ["1", "1/2"]]
EXPECTED = {
    "Y1.mu_plus": H2, "Y1.mu_minus": H2,
    "Y1.nu": [["0", "1/3"], ["1", "1/3"], ["2", "1/6"], ["3", "1/6"]],
    "Y1.after_plus": [["1", "1/3"], ["2", "1/3"], ["3", "1/6"], ["4", "1/6"]],
    "Y1.blind": True, "Y1.sep": True, "Y1.tv": "1/3", "Y1.maxnu": "1/3", "Y1.tvq": "1/3",
    "Y1.tv_joint": "1/3", "Y1.tv_full": "1", "Y1.eqclass": True,
    "Y2.tv": "2/3", "Y2.tvq": "1/3", "Y2.tv_joint": "2/3", "Y2.tv_full": "2/3", "Y2.eqclass": False,
    "Y3.after_plus": [["1", "1/2"], ["2", "1/2"]], "Y3.after_minus": H2,
    "Y3.blind": True, "Y3.tv": "1/2", "Y3.maxnu": "1/2", "Y3.tv_joint": "1", "Y3.tv_full": "1", "Y3.tvq": "1/2",
    "Y3.fiber_product": False,
    "Y4.p_before": ["0", "0"], "Y4.v_before": ["0", "1"], "Y4.p_after": ["1", "0"],
    "Y4.tv": "1", "Y4.tvq": "1", "Y4.tv_full": "1", "Y4.blind": True,
    "Y5.nu": [["0", "1/4"], ["1", "3/4"]], "Y5.tv": "3/4", "Y5.tvq": "1/4", "Y5.maxnu": "3/4", "Y5.eqclass": False,
    "Y6.K0": [["1", "0", "0", "0"], ["0", "1", "0", "0"], ["0", "0", "0", "0"]],
    "Y6.K1": [["0", "0", "0", "0"], ["0", "0", "1", "0"], ["0", "0", "0", "1"]],
    "Y6.tp": True, "Y6.intertwine": [True, True], "Y6.out_psi": ["0", "1", "0"], "Y6.branch": ["1/2", "1/2"],
    "Y6.rank": 2, "Y6.maxfiber": 2,
    "Y7.values": ["3", "3", "3"], "Y7.components": 3,
    "Y8.own": [["3", "5", "7", "2"], ["3", "12", "2"], ["3", "12", "2"], True, ["0", "-1", "1", "0"]],
    "Y8.gtax": [["10", "5/2", "7/2", "1"], ["10", "6", "1"], ["10", "6", "1"], True, ["0", "-1/2", "1/2", "0"]],
    "Y8.parent": [["10", "7", "0", "0"], ["17", "0", "0"], ["10", "7", "0"], False, ["-1", "1", "0", "0"]],
    "Y8.parent_iv": ["0", "1"],
    "Y9.forced": ["3", "12", "2"], "Y9.dump": ["10", "5", "2"], "Y9.totals": ["17", "17", "17"],
    "Y9.changed": [1, 0], "Y9.region": [[1, 0], [1, 1]],
    "Y10.invariant": [9, 9]}
UNIVERSE_KEYS = ["u18a_trees", "u18a_carriers", "u18a_leaf", "u18a_pairs", "u18a_orders", "u18a_digest",
                 "u18b_cases", "u18b_conf_blind", "u18b_conf_sep", "u18b_digest", "u18b_laws", "u18b_nv_bound_eq",
                 "u18b_nv_bound_gt", "u18b_nv_corr_adv", "u18b_nv_multi", "u18b_oneloc", "u18b_prodclass_fiberprod",
                 "u18b_prodclass_total", "u18b_transfer", "u18c_true", "u18c_acq", "u18c_digest", "u18c_lines",
                 "u18d_families", "u18d_ops", "u18d_classical", "u18d_coherent", "u18d_digest"]
VIOL_KEYS = ["u18a_viol", "u18b_viol", "u18c_viol", "u18d_viol"]
PREREG = {"u18a_trees": 154, "u18a_carriers": 2107, "u18a_leaf": 3612, "u18a_pairs": 9436, "u18a_orders": 23649,
          "u18b_cases": 149820, "u18b_laws": 454, "u18b_conf_blind": [98064, 0, 0, 51756],
          "u18b_conf_sep": [87168, 0, 0, 62652], "u18b_transfer": 40860, "u18b_oneloc": 2724,
          "u18d_families": 24, "u18d_ops": 66, "u18d_classical": 150, "u18d_coherent": 96}
NONVACUOUS = ["u18b_nv_bound_eq", "u18b_nv_bound_gt", "u18b_nv_corr_adv", "u18b_nv_multi"]
TOTALS = {"U17A": 2652, "U17B": 593}
P0 = {"U17A": 52, "U17B": 131}
ACQ = {u + "." + a: a in ("own", "field") for u in ("U17A", "U17B") for a in ("own", "gtax", "mixed", "root", "field")}
BOUNDED = {"B18a_cases": 2250, "B18a_class_true": 76, "B18a_class_false": 2174, "B18a_eq_match": 2250,
           "B18a_tvq_nu0": 2250, "B18a_tvq_one": 10, "B18a_tvq_one_delta0": 10, "B18a_e_checks": 9000,
           "B18a_e_equal": 9000, "B18a_tvq_lt_tv": 2174, "B18b": [2600, 462]}
CONTROLS = ["R1_sufficiency_every_background", "R2_Q_as_informative_as_coordinate", "R3_Q_distinguishes_amounts",
            "R4_conservation_selects_receiver", "R5_W1_W2_grade_facts_imply_W4", "R6_W4_implies_acquisition",
            "R7_receiver_keeps_source_identity", "R8_receiver_blind_for_every_pair", "R9_retained_side_initially_blind",
            "R10_leaky_family_agrees_with_forced_step"]


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
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-12 bytes")
    for cert in (prod, chk):
        need(cert["meta"]["result_sha256"] == FROZEN_RESULT_SHA, "false provenance: certificate hash")
        need(set(cert["values"]) == set(EXPECTED), "key set differs from preregistered instances")
        need(set(cert["universe"]) == set(UNIVERSE_KEYS + VIOL_KEYS), "universe key set differs")
    need(prod["meta"]["role"] == "producer" and chk["meta"]["role"] == "checker", "role confusion")
    for k, e in EXPECTED.items():
        need(prod["values"][k] == e, "producer mismatch at " + k)
        need(chk["values"][k] == e, "checker mismatch at " + k)
    for k in UNIVERSE_KEYS:
        need(prod["universe"][k] == chk["universe"][k], "universe count or digest mismatch: " + k)
    for k, v in PREREG.items():
        need(prod["universe"][k] == v, "preregistered count differs: " + k)
    need(prod["universe"]["u18b_prodclass_fiberprod"] == prod["universe"]["u18b_prodclass_total"] == 729,
         "product-class law without fiber product")
    for k in NONVACUOUS:
        need(prod["universe"][k] > 0, "non-vacuity failed: " + k)
    for k in VIOL_KEYS:
        need(prod["universe"][k] == 0 and chk["universe"][k] == 0, "exhaustive violation: " + k)
    t = prod["universe"]["u18c_true"]
    for u in TOTALS:
        for a in ("own", "gtax", "mixed", "root", "field"):
            need(t[u][a] == TOTALS[u], "W4 count differs: %s %s" % (u, a))
        for a in ("parent", "uniform"):
            need(t[u][a] == P0[u], "W4 count differs: %s %s" % (u, a))
        need(0 < t[u]["pert"] < TOTALS[u], "pert not mixed: " + u)
        need(P0[u] <= t[u]["rand"] < TOTALS[u], "rand outside preregistered range: " + u)
    need(prod["universe"]["u18c_lines"] == 9 * (TOTALS["U17A"] + TOTALS["U17B"]), "U18C line count")
    need(prod["universe"]["u18c_acq"] == ACQ, "universal acquisition flags differ")
    need(chk["bounded"] == BOUNDED, "bounded evidence differs from preregistration")
    need(set(chk["controls"]) == set(CONTROLS), "control set differs from preregistration")
    for ctl in CONTROLS:
        need(chk["controls"].get(ctl) == "REJECTED", "rejecting control accepted: " + ctl)


def tamper_tests(prod, chk, sha):
    cases = []
    p = copy.deepcopy(prod); del p["values"]["Y1.tv"]; cases.append(("missing", p, chk, sha))
    p = copy.deepcopy(prod); p["values"]["Y3.fiber_product"] = True; cases.append(("wrong_value_fiber_product", p, chk, sha))
    q = copy.deepcopy(chk); q["values"]["Y2.tvq"] = "2/3"; cases.append(("substituted_tvq", prod, q, sha))
    p = copy.deepcopy(prod); p["values"]["Y8.parent"][3] = True; cases.append(("wrong_naturality", p, chk, sha))
    q = copy.deepcopy(chk); q["universe"]["u18a_orders"] -= 1; cases.append(("universe_count_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u18b_digest"] = "0" * 64; cases.append(("digest_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["meta"]["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R4_conservation_selects_receiver"] = "ACCEPTED"; cases.append(("control_flip_R4", prod, q, sha))
    q = copy.deepcopy(chk); del q["controls"]["R1_sufficiency_every_background"]; cases.append(("control_missing", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u18c_viol"] = 1; cases.append(("violation_hidden", prod, q, sha))
    q = copy.deepcopy(chk); q["bounded"]["B18a_class_true"] = 116; cases.append(("bounded_mismatch", prod, q, sha))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universe"]["u18b_conf_sep"] = [87167, 1, 0, 62652]
    cases.append(("confusion_cell_flip", p, q, sha))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universe"]["u18c_true"] = copy.deepcopy(c["universe"]["u18c_true"]); c["universe"]["u18c_true"]["U17B"]["parent"] = 593
    cases.append(("parent_W4_flip", p, q, sha))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universe"]["u18b_nv_corr_adv"] = 0
    cases.append(("vacuous_corr_adv", p, q, sha))
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
        report["universe"] = prod["universe"]
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
