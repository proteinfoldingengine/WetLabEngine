"""receiver_identification draft 2 freeze: COMPARATOR. Checks producer and checker certificates against the
preregistered exact instances (FREEZE.md section 2), equal exhaustive-universe counts with zero violations
(section 3), bounded evidence (section 4) and rejecting controls (section 5); runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d2_review")
FROZEN_RESULT_SHA = "833c011b6c623dfb1d3fdb6e1214015e047e71a5b1a3d1ebc2160eb663b8eb24"
EXPECTED = {
    "E1.mu_x": ["1", "1"], "E1.mu_xp": ["1", "0"], "E1.owner": [1],
    "E2.owner": [], "E2.equal": True,
    "E3.holders": [2, 1, 0], "E3.diffs": ["1", "1", "1"], "E3.merge_step": 2,
    "E4a.tv_src": "1", "E4a.tv_owner": "1/2", "E4a.tv_point": "1",
    "E4b.tv_src": "1/4", "E4b.tv_owner": "1/8",
    "E4c.tv_src_marg": "0", "E4c.tv_owner": "1", "E4c.tv_joint_before": "1",
    "E5.cnot": True, "E5.owner_reduced": [["1/2", "0"], ["0", "1/2"]], "P1.factor": True,
    "E6.tv_src": "1", "E6.tv_owner": "1/2", "E6.tv_draft1_formula": "1", "E7.tv": "1/6",
    "E8.tv": "3/4", "E8.max_nu": "1/2", "E9.tv": "1/2",
}
UNIVERSE_KEYS = ["t2_pairs", "t2_W_checks", "t2_single", "t2_cancel", "t3_cases", "trees", "retained_sets",
                 "p4f_trees", "p4f_cases", "p4f_multi", "p4f_draft1_wrong", "p4f_point_nu", "p4f_det_pairs", "p4f_digest",
                 "p42_cases", "p42_laws", "p42_attained", "p42_uniform_k1_attained", "p42_digest"]
VIOL_KEYS = ["t2_viol", "t3_viol", "p4f_viol", "p42_viol"]
BOUNDED = {"B2": 3000, "B3": 2000, "B4F": 2000, "B5a": 200, "B5b": 200, "B6": 2000}
CONTROLS = ["R1_wrong_owner_root", "R2_copy_unique_holder", "R3_swapped_lineage", "R4_equality_nonpoint_prior",
            "R5_marginal_bound_correlated", "R6_commutes_on_owner", "R7_retained_diff_uninformed",
            "R8_draft1_owner_law", "R9_draft1_equality_clause", "R10_uniform_lower_bound_half",
            "R11_wrapping_injectivity", "R12_double_max_bound"]


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
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-2 bytes")
    for cert in (prod, chk):
        need(cert["meta"]["result_sha256"] == FROZEN_RESULT_SHA, "false provenance: certificate hash")
        need(set(cert["values"]) == set(EXPECTED), "key set differs from preregistered instances")
        need(set(cert["universe"]) == set(UNIVERSE_KEYS + VIOL_KEYS), "universe key set differs")
    need(prod["meta"]["role"] == "producer" and chk["meta"]["role"] == "checker", "role confusion")
    for k, e in EXPECTED.items():
        need(prod["values"][k] == e, "producer mismatch at " + k)
        need(chk["values"][k] == e, "checker mismatch at " + k)
    for k in UNIVERSE_KEYS:
        need(prod["universe"][k] == chk["universe"][k], "universe count mismatch: " + k)
    need(prod["universe"]["trees"] == 34, "tree universe is not the declared 34 trees")
    need(prod["universe"]["t2_cancel"] > 0 and prod["universe"]["t2_single"] > 0, "Thm 2 test vacuous")
    need(prod["universe"]["p4f_trees"] == 10, "P4F tree universe is not the declared 10 trees")
    need(prod["universe"]["p4f_multi"] > 0 and prod["universe"]["p4f_draft1_wrong"] > 0, "P4F universe vacuous for the multi-member fiber case")
    need(prod["universe"]["p4f_det_pairs"] > 0 and prod["universe"]["p4f_point_nu"] > 0, "P4F sub-claims vacuous")
    need(prod["universe"]["p42_laws"] == 462 and prod["universe"]["p42_cases"] == 2772, "P42 universe is not the declared 462 x 6")
    need(prod["universe"]["p42_attained"] > 0 and prod["universe"]["p42_uniform_k1_attained"] == 1, "P42 sharpness not exhibited")
    for k in VIOL_KEYS:
        need(prod["universe"][k] == 0 and chk["universe"][k] == 0, "exhaustive violation: " + k)
    for name, n in BOUNDED.items():
        need(chk["bounded"].get(name + "_cases") == n, "bounded case count changed: " + name)
        need(chk["bounded"].get(name + "_viol") == 0, "bounded violation: " + name)
    for ctl in CONTROLS:
        need(chk["controls"].get(ctl) == "REJECTED", "rejecting control accepted: " + ctl)


def tamper_tests(prod, chk, sha):
    cases = []
    p = copy.deepcopy(prod); del p["values"]["E1.owner"]; cases.append(("missing", p, chk, sha))
    p = copy.deepcopy(prod); p["values"]["E4b.tv_owner"] = "1/4"; cases.append(("wrong_value", p, chk, sha))
    q = copy.deepcopy(chk); q["values"]["E3.holders"] = [2, 2, 0]; cases.append(("substituted", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["t3_cases"] -= 1; cases.append(("universe_count_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["meta"]["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R2_copy_unique_holder"] = "ACCEPTED"; cases.append(("control_flip", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["p4f_digest"] = "0" * 64; cases.append(("digest_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R8_draft1_owner_law"] = "ACCEPTED"; cases.append(("control_flip_R8", prod, q, sha))
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
        report["universe"] = prod["universe"]; report["bounded"] = chk["bounded"]; report["controls"] = chk["controls"]
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
