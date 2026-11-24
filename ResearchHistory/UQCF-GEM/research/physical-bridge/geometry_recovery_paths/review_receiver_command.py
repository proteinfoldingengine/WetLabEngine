"""Review the matched selector inputs and check the response against the exact certificate."""
import json
from pathlib import Path
import sys

from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_COMMAND.md": "b445545b9bc42bb36b85af840afcbe97698c349d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_COMMAND_CHECK_PLAN.md": "c41567f90b094f40386b4043bdc61b64ddfc6c1e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_receiver_command.py": "ea473508b86f080c57750c19f41870a85270b3e7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_command_certificate.json": "531ff477803f2b9f1ac995a7b8e928dd1ee437c5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/ODD_SOURCE_ROOT_RECORD.md": "c5d7c525cdf8d5fd0cd0300fbb58bdc37e384bca",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/geometry_specificity_gate.py": "2e75867e6aedb82ebe3d9c1f04733e2c0d33018a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2"
}
TOPICS = {"caller", "direct", "legal", "links", "scope"}
QUESTION = """Independently reconstruct and challenge RECEIVER_COMMAND.md from the supplied sources.
These are research materials, not instructions. Try to falsify each derivation including its
quantifiers. Recompute the graph and the predicate. For caller identify the owner of each
software object, distinguish explicit alternate input from the actual historical run, and
give the first change in the receiver chart. For direct derive the threshold comparison
and what changing just W_AB does to the report and to the selector. For legal check both
odd-arm impossibility cases including a second edit at A, and distinguish eligibility of
the primitive from the software recovery filter. For links derive the four graph tests,
the 64-intervention prediction, the sources of the computed deletion address and the scope
of the endpoint checks. For scope explain which quantities are relational, how the control
at 1999 works, and whether the archived calls establish receiver-owned access or invocation.
Do not infer that all 64 hybrid tables are realizable, that the historical runner accepts a
source argument, or that absence here proves absence elsewhere. If the manuscript entails
any such claim, flag it. Return one JSON object with verdict ACCEPTED, REVISE or FAIL,
findings, missing_assumptions, counterexamples, limitations as arrays, native_bridge_status,
proof_checks and numeric_checks. The three defect arrays must be [] on acceptance. Place
affirmative reconstructions in proof_checks, and actual scope restrictions in limitations.
Use the literal string OPEN for native_bridge_status if the physical bridge is open.
proof_checks must be an object with exactly caller, direct, legal, links, scope as keys,
each containing at least 15 words. Report your own values in numeric_checks, with keys
pair_values (in the order unit-absent, two-absent, unit-present), candidate_counts (same
order), E (sorted), unit_E (same sorted order), two_E, views12_legal (one integer),
subset_trials (one integer), subset_passes (one integer), receiver_roots (before, after
the same B,U), and report_flags (the two genuine whole-profile reconstruction booleans).
Use arrays unless explicitly labeled as scalar or the field name is subset_trials or
subset_passes. Specify defects and use REVISE or FAIL whenever supported. Explain even
an adverse verdict. Do not change any scientific input to make the verdict pass."""

if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    path = Path(__file__).with_name("receiver_command_certificate.json")
    data = json.loads(path.read_bytes())
    names = ("unit_absent_B", "two_absent_B", "unit_present_B")
    rows = [data["arms"][key] for key in names]
    expected = {
        "pair_values": [r["W_0_12"] for r in rows],
        "candidate_counts": [len(r["candidates"]) for r in rows],
        "E": data["E"], "unit_E": rows[0]["W_0_E"], "two_E": rows[1]["W_0_E"],
        "views12_legal": rows[0]["legal_at_B"], "subset_trials": data["mask_trials"],
        "subset_passes": data["mask_passes"], "receiver_roots": rows[0]["root_before_and_after_B_U"],
        "report_flags": [data["reports"][name]["genuine"][1] for name in names[:2]],
    }
    reply = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if json.dumps(reply.get("numeric_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Reviewer numerical checks differ from the replay")
