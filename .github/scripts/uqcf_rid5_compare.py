"""receiver_identification draft 5 (secs 11-13) freeze: COMPARATOR. Checks producer and checker certificates against the
preregistered exact instances (FREEZE.md section 2), equal exhaustive-universe counts and identity digests with zero
violations and non-vacuity (section 3), bounded evidence (section 4) and rejecting controls (section 5); runs tampering
controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d5_review")
FROZEN_RESULT_SHA = "84b17c36379df2d6361149eae1ce24dd2ff7f75a85dc585fbb579eaef8e2bb82"
EXPECTED = {
    "X1.y1": [["1", "0", "1", "1"], ["1", "2"], ["3"]], "X1.y0": [["1", "0", "1", "0"], ["1", "1"], ["2"]],
    "X1.holders": [3, 1, 0], "X1.diffs": ["1", "1", "1"], "X1.depths": [3, 1, 0],
    "X2.holders_A": [4, 1], "X2.holders_B": [1, 1], "X2.final_equal": True, "X2.cor125_B1": [1],
    "X3.pairs": [[3, 4], [3, 0], []], "X3.merge_step": 3, "X3.totals_equal": True,
    "X4.holder": 0, "X4.tv": "1/2", "X4.max_nu": "1/2", "X4.helstrom_success": "3/4",
    "X5.holder": 2, "X5.tv": "1", "X5.tv_addr1": "0",
    "X6.tv_joint": "1", "X6.tv_holder": "1/2", "X6.tv_ref": "0",
    "X7.pinch_fixed": True, "X7.trace_distance": "1/2",
}
UNIVERSE_KEYS = ["trees_n5", "trees_n4",
                 "u12_cases", "u12_steps", "u12_strict", "u12_h_ne_e", "u12_lines", "u12_digest",
                 "u114_cases", "u114_steps", "u114_merged", "u114_unmerged", "u114_lines", "u114_digest",
                 "u13_steps", "u13_tv_lt1", "u13_h_ne_e", "u13_multi", "u13_attained", "u13_lines", "u13_digest"]
VIOL_KEYS = ["u12_viol", "u114_viol", "u13_viol"]
NONVACUOUS = ["u12_strict", "u12_h_ne_e", "u114_merged", "u114_unmerged", "u13_tv_lt1", "u13_h_ne_e", "u13_multi", "u13_attained"]
BOUNDED = {"B12": 3000, "B114": 2000, "B13": 1000}
CONTROLS = ["R1_holder_is_parent", "R2_copy_two_holders", "R3_nonnested_depth_nonincreasing",
            "R4_holder_sufficient_correlated", "R5_double_max_bound", "R6_survives_merge",
            "R7_records_incomparable_order", "R8_zero_power_with_holder"]


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
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-5 bytes")
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
    need(prod["universe"]["trees_n5"] == 34 and prod["universe"]["trees_n4"] == 10, "tree universe is not the declared 34 / 10 trees")
    for k in NONVACUOUS:
        need(prod["universe"][k] > 0, "non-vacuity failed: " + k)
    for k in VIOL_KEYS:
        need(prod["universe"][k] == 0 and chk["universe"][k] == 0, "exhaustive violation: " + k)
    for name, n in BOUNDED.items():
        need(chk["bounded"].get(name + "_cases") == n, "bounded case count changed: " + name)
        need(chk["bounded"].get(name + "_viol") == 0, "bounded violation: " + name)
    need(set(chk["controls"]) == set(CONTROLS), "control set differs from preregistration")
    for ctl in CONTROLS:
        need(chk["controls"].get(ctl) == "REJECTED", "rejecting control accepted: " + ctl)


def tamper_tests(prod, chk, sha):
    cases = []
    p = copy.deepcopy(prod); del p["values"]["X1.holders"]; cases.append(("missing", p, chk, sha))
    p = copy.deepcopy(prod); p["values"]["X4.tv"] = "1"; cases.append(("wrong_value", p, chk, sha))
    q = copy.deepcopy(chk); q["values"]["X1.holders"] = [3, 2, 0]; cases.append(("substituted", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u12_steps"] -= 1; cases.append(("universe_count_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u13_digest"] = "0" * 64; cases.append(("digest_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["meta"]["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R4_holder_sufficient_correlated"] = "ACCEPTED"; cases.append(("control_flip_R4", prod, q, sha))
    q = copy.deepcopy(chk); del q["controls"]["R7_records_incomparable_order"]; cases.append(("control_missing", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u13_viol"] = 1; cases.append(("violation_hidden", prod, q, sha))
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
