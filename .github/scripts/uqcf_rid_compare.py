"""receiver_identification draft 1 freeze: COMPARATOR. Checks producer and checker certificates against the
preregistered exact instances (FREEZE.md section 2), equal exhaustive-universe counts with zero violations
(section 3), bounded evidence (section 4) and rejecting controls (section 5); runs tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_review")
FROZEN_RESULT_SHA = "0d4d68e72ec95ce06a9ddb4698bd444bd733fe114db042a9e9d9911f80bf58a0"
EXPECTED = {
    "E1.mu_x": ["1", "1"], "E1.mu_xp": ["1", "0"], "E1.owner": [1],
    "E2.owner": [], "E2.equal": True,
    "E3.holders": [2, 1, 0], "E3.diffs": ["1", "1", "1"], "E3.merge_step": 2,
    "E4a.tv_src": "1", "E4a.tv_owner": "1/2", "E4a.tv_point": "1",
    "E4b.tv_src": "1/4", "E4b.tv_owner": "1/8",
    "E4c.tv_src_marg": "0", "E4c.tv_owner": "1", "E4c.tv_joint_before": "1",
    "E5.cnot": True, "E5.owner_reduced": [["1/2", "0"], ["0", "1/2"]], "P1.factor": True,
}
UNIVERSE_KEYS = ["t2_pairs", "t2_W_checks", "t2_single", "t2_cancel", "t3_cases", "p4_triples", "trees", "retained_sets"]
VIOL_KEYS = ["t2_viol", "t3_viol", "p4_viol"]
BOUNDED = {"B2": 3000, "B3": 2000, "B4": 2000, "B5a": 200, "B5b": 200}
CONTROLS = ["R1_wrong_owner_root", "R2_copy_unique_holder", "R3_swapped_lineage", "R4_equality_nonpoint_prior",
            "R5_marginal_bound_correlated", "R6_commutes_on_owner", "R7_retained_diff_uninformed"]


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
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-1 bytes")
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
    need(prod["universe"]["p4_triples"] == 1000, "P4 grid is not the declared 1000 triples")
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
