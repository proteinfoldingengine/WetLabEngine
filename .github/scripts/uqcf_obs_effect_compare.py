"""observation_effect draft 3 freeze: COMPARATOR. Checks producer and checker certificates
against the preregistered expected universe (FREEZE.md section 2), the bounded evidence and the
rejecting controls (sections 3-4), and runs certificate-tampering controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from fractions import Fraction
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/observation_effect_review")
FROZEN_RESULT_SHA = "97b031585f8cc947a69e240bde628258fd213c548d86903e157674ccc3855e87"
EXPECTED = {
    "W.tv_obs": "0", "W.tv_unobs": "1", "W.kappa": "1/2", "W.occ_tv": "1/2", "W.kyfan": "1/2",
    "P.tv_obs": "3/10", "P.tv_unobs": "0", "P.global_obs": ["5/8", "1/2", "3/10"],
    "P.kappa1": "3/8", "P.occ1": "3/10", "P.occ0": "0",
    "H.central_equal": True, "H.full_effect": "1", "Z.cadence": "1/2",
    "S.swap_record": ["0", "0", "0", "1"],
    "L.owner": ["1", "0"], "L.tracial": ["1/2", "1/2"], "L.unobs": ["1/2", "1/2"],
    "O.perfect": "1", "Q.D": "sin(theta/2)**2", "Q.C": "Abs(sin(theta))/2",
    "G4.D": "0", "G4.C": "1", "G3.D": "1", "G3.C": "1",
    "N.kernel": "inclusion_fails", "M.witness": "inZprime_nonnormalizing_keeps_record",
}
BOUNDED = {"thm1": 300, "thm2d": 300, "thm3": 300, "thm4a": 200, "thm12_3": 100, "prop12_4": 300, "thm12_5b": 1000}
CONTROLS = ["R1_closed_motion_substituted", "R2_classical_prefix_nonzero_record", "R3_linear_bound",
            "R4_owner_section_lambda_positive", "R5_three_atom_swap_preserving",
            "R6_multiplicity_only_nonnormalizer", "R7_kyfan_rank1_saturation", "R8_faithful_perfect_record"]


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


def same(exp, got, exact):
    if isinstance(exp, list):
        return isinstance(got, list) and len(exp) == len(got) and all(same(e, g, exact) for e, g in zip(exp, got))
    if isinstance(exp, bool) or exp in ("inclusion_fails", "inZprime_nonnormalizing_keeps_record") or "theta" in str(exp):
        return got == exp
    if exact or isinstance(got, str):
        return isinstance(got, str) and got == exp
    return isinstance(got, float) and abs(got - float(Fraction(exp))) <= 1e-12


def check(prod, chk, result_sha):
    need(result_sha == FROZEN_RESULT_SHA, "RESULT.md is not the frozen draft-3 bytes")
    for cert in (prod, chk):
        need(cert["meta"]["result_sha256"] == FROZEN_RESULT_SHA, "false provenance: certificate hash")
        need(set(cert["values"]) == set(EXPECTED), "key set differs from preregistered universe")
    need(prod["meta"]["role"] == "producer" and chk["meta"]["role"] == "checker", "role confusion")
    for k, e in EXPECTED.items():
        need(same(e, prod["values"][k], True), "producer mismatch at " + k)
        need(same(e, chk["values"][k], False), "checker mismatch at " + k)
    for name, n in BOUNDED.items():
        need(chk["bounded"].get(name + "_cases") == n, "bounded case count changed: " + name)
        need(chk["bounded"].get(name + "_violations") == 0, "bounded violation: " + name)
    need(0 < chk["bounded"]["thm1_closed_count"] < 300, "Thm 1 test vacuous")
    need(chk["bounded"]["thm3_nontrivial_kernel"] > 0, "Thm 3 test vacuous")
    need(0 < chk["bounded"]["thm4a_persistent_count"] < 200, "Thm 4(a) test vacuous")
    for ctl in CONTROLS:
        need(chk["controls"].get(ctl) == "REJECTED", "rejecting control accepted: " + ctl)


def tamper_tests(prod, chk, sha):
    cases = []
    p = copy.deepcopy(prod); del p["values"]["W.tv_unobs"]; cases.append(("missing", p, chk, sha))
    p = copy.deepcopy(prod); p["values"]["P.occ1"] = "3/8"; cases.append(("wrong_value", p, chk, sha))
    q = copy.deepcopy(chk); q["values"]["G4.C"] = q["values"]["G4.D"]; cases.append(("substituted", prod, q, sha))
    q = copy.deepcopy(chk); q["meta"]["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, sha))
    q = copy.deepcopy(chk); q["controls"]["R3_linear_bound"] = "ACCEPTED"; cases.append(("control_flip", prod, q, sha))
    cases.append(("wrong_result_bytes", prod, chk, "1" * 64))
    out = {}
    for name, a, b, s in cases:
        try:
            check(a, b, s)
            out[name] = "NOT_DETECTED"
        except Red:
            out[name] = "DETECTED"
    raw = json.dumps(prod)
    dup = raw[:-1] + ', "values": {}}'
    try:
        load(dup)
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
