"""receiver_identification d14 freeze: COMPARATOR. Checks producer and checker certificates against the preregistered
exact instances (FREEZE.md section 2, transcribed from the hand-written table), the preregistered universe counts and
equal identity digests with zero violations (section 3), the rejecting controls (section 4), and runs tampering
controls. Exit 0 = GREEN."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d14_review")
FROZEN = {"RESULT.md": "f6cc849663224a5a2c877cd32a6700ecad9df1ea2d4f723a040c66e55dbc38f9",
          "FOLLOWUP.md": "5e906ca758c2cd07459fa0e39afd2b0f26380a266b11191d8bfccc9d0ec7f146",
          "CORRESPONDENCE.md": "710d786c3cf6034844c753cd3bef54294f7fa838c8780232dad3612f86fc94da"}
H = "1/2"
EXPECTED = {
    "X1.inj_01_01": False, "X1.collision": [[0, 1], [1, 0]],
    "X2.sigma": [["0", "0", "1"], ["0", "1", "0"]], "X2.N": [H] * 6, "X2.Q": [H] * 6,
    "X2.G_can": [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
    "X2.G_alt": [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]],
    "X3.units": [9, 16, 16, 25, 9, 16, 36, 16, 16], "X3.det_dim": [3, 4, 4, 5, 7, 4, 6, 4, 10],
    "X3.pair_ext": [5, 13, 13, 31, 1, 6, 26, 6, 5], "X3.plocal": [[9, 3], [4, 2]],
    "X4.a": ["1", "0"], "X4.b": ["1", "1/2", "0", "1", "0"], "X4.c": ["1/3", "1/3"],
    "X5.illus": ["1/2", "3/4", "1/4"], "X5.controls": ["0", "0"], "X5.vminusu": "2",
    "X6.prefix": [["1", "2", "1"], ["0", "0", "1"], ["0", "1", "1"], ["1/2", "1", "1"]],
    "X6.rfail": [[2], [1, 2], [1], [1]], "X7.dump": [4, 2, "0"]}
PREREG = {
    "U19A": {"det_dim": [3, 4, 4, 5, 7, 4, 6, 4, 10], "pair_ext": [5, 13, 13, 31, 1, 6, 26, 6, 5], "plocal": [[9, 3], [4, 2]],
             "units": [9, 16, 16, 25, 9, 16, 36, 16, 16],
             "counts": {"extensions": 169, "dep": 9, "pair": 106, "rand": 54, "units": 159, "inv": 47, "noninv": 112}},
    "U19B": {"pairs": 225, "injective": 130, "noninjective": 95},
    "U19C": {"vectors": 1554, "R_true": [1, 1, 1, 1], "E2Rp": [1, 1, 5, 25], "E2Rp_notR": [0, 0, 4, 24], "E2Rp_nonneg": [1, 1, 1, 1]},
    "U20A": {"subsets": 31, "partitions": 202, "functions": 1023},
    "U20B": {"cases": 38, "partitions": 661, "covering": 1676},
    "U20C": {"subsets": 63, "partitions": 876, "invariant": 94, "admit_nontrivial": 31},
    "U20D": {"cases": 260, "transfers": 184, "nontransfers": 76},
    "U20E": {"cases": 6500, "transfers": 3680, "nontransfers": 2820}}
CONTROLS = ["R1_trivial_availability_transfers", "R2_genesis_dump_receiver_gains", "R3_sigma_event_determined",
            "R4_canonical_extension_unique", "R5_addition_injective_01", "R6_threshold_unit_invariant",
            "R7_E2_Rp_imply_R_signed", "R8_relabel_sharpens_E", "R9_unit_free_transfers_without_empty",
            "R10_A1_A2_force_full_access"]


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


def strip_rand_counts(c):
    return {k: v for k, v in c.items() if k in ("extensions", "dep", "pair", "rand", "units", "inv", "noninv")}


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
        need(prod["instances"][k] == e, "producer mismatch at " + k)
        need(chk["instances"][k] == e, "checker mismatch at " + k)
    for u, exp in PREREG.items():
        P, C = prod["universes"][u], chk["universes"][u]
        need(set(P) == set(C), "universe keys differ: " + u)
        for k in P:
            if k == "counts":
                need(strip_rand_counts(P[k]) == strip_rand_counts(C[k]), "count mismatch " + u)
            else:
                need(P[k] == C[k], "universe value or digest mismatch: %s.%s" % (u, k))
        for k, v in exp.items():
            if k == "counts":
                need(strip_rand_counts(P[k]) == v, "preregistered count differs: " + u)
            else:
                need(P[k] == v, "preregistered value differs: %s.%s" % (u, k))
    need(prod["universes"]["U20B"]["strict_decrease"] > 0 and prod["universes"]["U20B"]["positive"] > 0, "U20B vacuous")


def tamper_tests(prod, chk, shas):
    cases = []
    q = copy.deepcopy(chk); q["universes"]["U19A"]["digest"] = "0" * 64; cases.append(("flipped_invariance_digest", prod, q, shas))
    q = copy.deepcopy(chk); q["universes"]["U19A"]["det_dim"] = q["universes"]["U19A"]["det_dim"][:-1]; cases.append(("dropped_region", prod, q, shas))
    p = copy.deepcopy(prod); p["universes"]["U19B"]["pairs"] += 1; p["universes"]["U19B"]["injective"] += 1; cases.append(("duplicated_pair", p, chk, shas))
    q = copy.deepcopy(chk); q["universes"]["U20D"]["digest"] = prod["universes"]["U20E"]["digest"]; cases.append(("substituted_law", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["X4.b"][1] = "1/3"; cases.append(("wrong_fraction_X4", p, chk, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U20D"]["transfers"] = 185
    cases.append(("wrong_count_U20D", p, q, shas))
    q = copy.deepcopy(chk); q["result_sha256"] = "0" * 64; cases.append(("false_provenance", prod, q, shas))
    s2 = dict(shas); s2["RESULT.md"] = "1" * 64; cases.append(("wrong_result_bytes", prod, chk, s2))
    q = copy.deepcopy(chk); q["role"] = "producer"; cases.append(("producer_as_checker", prod, q, shas))
    q = copy.deepcopy(chk); del q["controls"]["R8_relabel_sharpens_E"]; cases.append(("missing_control", prod, q, shas))
    q = copy.deepcopy(chk); q["controls"]["R2_genesis_dump_receiver_gains"] = "ACCEPTED_WRONGLY"; cases.append(("control_flip", prod, q, shas))
    p = copy.deepcopy(prod); p["instances"]["X9.extra"] = 1; cases.append(("extra_key", p, chk, shas))
    q = copy.deepcopy(chk); q["violations"] = ["hidden"]; cases.append(("violation_hidden", prod, q, shas))
    p = copy.deepcopy(prod); q = copy.deepcopy(chk)
    for c in (p, q):
        c["universes"]["U19C"]["E2Rp_notR"] = [0, 0, 0, 0]
    cases.append(("signed_counterexample_removed", p, q, shas))
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
