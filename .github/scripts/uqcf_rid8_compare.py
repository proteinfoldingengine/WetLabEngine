"""receiver_identification draft 8 (secs 14-15) freeze: COMPARATOR. Checks producer and checker certificates against the
preregistered exact instances (FREEZE.md section 2), equal exhaustive-universe counts and identity digests with zero
violations and non-vacuity (section 3), bounded evidence (section 4) and rejecting controls (section 5); runs tampering
controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d8_review")
FROZEN_RESULT_SHA = "a7a0caefce8621bde682e238c2ce1b3959ce25f2896f9d0740d5d0d754b7e7f0"
EXPECTED = {"Y1.holders": [3, 1, 0], "Y1.recoverable_last": True, "Y1.regimes": [1, 1], "Y1.rest_nondegenerate_last": True, "Y1.tvs": ["1", "1", "1"], "Y2.holders": [2, 0], "Y2.loss": "1/2", "Y2.overlap": "1/2", "Y2.regime": 3, "Y2.tvs": ["1", "1/2"], "Y3.recoverable": False, "Y3.regime": 2, "Y3.tv0": "1", "Y3.tv1": "1", "Y4.tv1": "1/4", "Y5.D": [0, 1, 4], "Y5.tv_w1": "1/2", "Y5.tv_w2": "1", "Y6.D_sum": [-3, -2, -1, 0, 1, 2, 3], "Y6.D_union": [-2, -1, 0, 1, 2], "Y6.tvs": ["1", "1", "3/4"], "Y7.tv_holder": "1/2", "Y7.tv_joint": "1", "Y7.tv_ref": "0", "Y8.corrected_pair": [[1, 0], [0, 1]], "Y8.corrected_sums": [1, 1], "Y8.draft7_pair": [[1, 1], [0, 0]], "Y8.draft7_sums": [2, 0], "Y9.cumulative_regimes": [3, 3], "Y9.per_step_regimes": [3, 1]}
UNIVERSE_KEYS = ["trees_n4", "u14_cases", "u14_steps", "u14_strict", "u14_reg1", "u14_reg2", "u14_reg3", "u14_gpt_case",
                 "u14_multi", "u14_lines", "u14_digest", "u15_cases", "u15_reg2", "u15_lines", "u15_digest",
                 "u15m_cases", "u15m_step_decrease", "u15m_lines", "u15m_digest"]
VIOL_KEYS = ["u14_viol", "u15_viol", "u15m_viol"]
NONVACUOUS = ["u14_strict", "u14_reg1", "u14_reg2", "u14_reg3", "u14_gpt_case", "u14_multi", "u15_reg2", "u15m_step_decrease"]
BOUNDED = {"B14": 1500}
CONTROLS = ["R1_preserve_iff_point_mass", "R2_unrecoverable_if_nondegenerate", "R3_draft7_witness_collides",
            "R4_preserved_implies_recoverable", "R5_per_step_regime_monotone", "R6_holder_sufficient_correlated_after_climb",
            "R7_union_instead_of_sumset", "R8_tv_restored_by_later_step"]


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
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-8 bytes")
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
    need(prod["universe"]["trees_n4"] == 10, "tree universe is not the declared 10 trees")
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
    p = copy.deepcopy(prod); del p["values"]["Y1.holders"]; cases.append(("missing", p, chk, sha))
    p = copy.deepcopy(prod); p["values"]["Y2.tvs"] = ["1", "1"]; cases.append(("wrong_value", p, chk, sha))
    q = copy.deepcopy(chk); q["values"]["Y8.corrected_sums"] = [2, 0]; cases.append(("substituted", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u14_steps"] -= 1; cases.append(("universe_count_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u15_digest"] = "0" * 64; cases.append(("digest_mismatch", prod, q, sha))
    q = copy.deepcopy(chk); q["meta"]["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R1_preserve_iff_point_mass"] = "ACCEPTED"; cases.append(("control_flip_R1", prod, q, sha))
    q = copy.deepcopy(chk); del q["controls"]["R5_per_step_regime_monotone"]; cases.append(("control_missing", prod, q, sha))
    q = copy.deepcopy(chk); q["universe"]["u14_viol"] = 1; cases.append(("violation_hidden", prod, q, sha))
    q = copy.deepcopy(chk); q["bounded"]["B14_viol"] = 3; cases.append(("bounded_violation", prod, q, sha))
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
