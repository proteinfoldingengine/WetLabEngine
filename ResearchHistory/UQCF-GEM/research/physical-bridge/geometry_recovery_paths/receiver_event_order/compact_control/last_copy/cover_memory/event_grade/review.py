"""Independent review of numerical overlap and retrospective work."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
while not (ROOT / ".git").exists():
    if ROOT == ROOT.parent:
        raise ValueError("Expected a repository checkout")
    ROOT = ROOT.parent

DRIVER = "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
BASE = "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/compact_control"
LAST = BASE + "/last_copy"
MEM = LAST + "/cover_memory"
SCI = MEM + "/event_grade"
DOCUMENTS = {
    SCI + "/RESULT.md": "a2fdfa50f95313661cb50e83875fcc4c4c143419",
    SCI + "/check.py": "f5dd9c2660b48bfed0de9e8efe602c10fba50d29",
    SCI + "/result.json": "91dbe84c6ac6a914ec78beac43f1774cd7366cdc",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    BASE + "/FIXTURE.json": "806d2bc487e358f498cafa806226d1f658e98d26",
    LAST + "/check.py": "c7b0586362e74c22612a9926f1d7135cf074dfb0",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py":
        "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py":
        "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py":
        "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py":
        "3324c0b46e09120ae526338444a19070b692d049",
}
TOPICS = {"work", "locality", "compatibility", "scale", "scope"}
QUESTION = """Independently referee event_grade/RESULT.md and its tests. Attempt to disprove the result.
Reconstruct the incident work changes at B's actual withdrawal. Challenge the sign, fixed fine
source, square, signed and zero cases. Check what current P1 alone can reconstruct, the necessity
perturbation at an absent internal site, and when other records or known inputs could invalidate
a necessity claim. Independently compute the current F, historical B and overlap rows under
the private-site exchange. Verify whether the same proposed historical B row flips an actual
legacy operation's verdict, and whether any mismatch is an honest joint history. Test the minimal
coalitions required for the old full B row for arbitrary positive grades. Explain whether the procedure
derives a present B write or autonomous caller. Reconstruct the two branch examples, and check
the scope of the square-root law. Identify any errors in the finite evidence or overclaims.
Return a single JSON object. verdict is ACCEPTED, REVISE, or FAIL. native_bridge_status is
the literal OPEN if the wider bridge remains open. findings, missing_assumptions, counterexamples
and limitations are each arrays of strings. Put substantiated positive checks in proof_checks,
a dictionary with keys work, locality, compatibility, scale, scope, each with a worked argument.
ACCEPTED with no substantive defects leaves findings, missing_assumptions and counterexamples
empty. Record any defects freely. In check_values give a dictionary with keys
B_to_F_jumps (two signed integers for grades 1 then 3), old_B (the two triples in the same
order), child_jumps (two lists, balanced split then unequal), parent_jump (one integer),
states_per_arm (one integer). Report your independently calculated values."""


def main():
    data = (ROOT / DRIVER).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != DRIVER_BLOB:
        raise ValueError("Unexpected inherited review driver identity")
    spec = importlib.util.spec_from_file_location("event_grade_review_driver", ROOT / DRIVER)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    driver.ROOT = ROOT
    driver.DOCUMENTS = DOCUMENTS
    driver.QUESTION = QUESTION
    driver.main()
    out = Path(sys.argv[2])
    verdict = json.loads((out / "review.txt").read_bytes())
    if verdict.get("verdict") != "ACCEPTED":
        raise ValueError("Independent review requires adjudication; preserve its raw response")
    if verdict.get("native_bridge_status") != "OPEN":
        raise ValueError("Review must preserve the physical access boundary")
    checks = verdict.get("proof_checks")
    if not isinstance(checks, dict) or set(checks) != TOPICS or not all(isinstance(v, str) and v.strip() for v in checks.values()):
        raise ValueError("Missing worked argument checks")
    expected = dict(B_to_F_jumps=[1,9], old_B=[[8,1,1],[6,3,1]],
                    child_jumps=[[4,4],[1,9]], parent_jump=25, states_per_arm=9)
    if verdict.get("check_values") != expected:
        raise ValueError("Review values require examination")
    for key in ("findings","missing_assumptions","counterexamples"):
        if verdict.get(key) != []:
            raise ValueError("Review contains an unresolved concern")


if __name__ == "__main__":
    main()
