"""Independent review of the neighborhood-work criterion."""
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
SCI = MEM + "/receiver_work_response"
DOCUMENTS = {
    SCI + "/RESULT.md": "98bba20f6072de3cc83c3720dee584b7684f4128",
    SCI + "/check.py": "baa3d1e8ec01be91df7b3becb6a4bc50c11e627d",
    SCI + "/result.json": "e123edb88ed0bade83b18ba66482b9425946092c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    SCI + "/SCOPE.md": "ff5d23ca8863f9da1144cbf59be69951c6cdcb4e",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
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
TOPICS = {"inputs", "work", "repair", "caller", "scope"}
QUESTION = """Review the full receiver_work_response/RESULT.md as a mathematical and source-level
claim. Independently derive the degrees of freedom after fixing all receiver prior grades,
incident work values, and the initial minimum graph. Check the exact supports, signs
and multiplicities in the six affected comparisons. Challenge necessity and sufficiency
of the source grade for a one-step repair by some DIFFERENT editor. Consider a second edit
at any chart outside the original two, and verify the common-minimum lemma. Do not grade
two edits by the source, with which the theorem makes no claim. Check the three positive
preparations, the raw scan versus carrier admission, and the distinction between an empty
candidate list and a failed fixed-minimum precondition. Audit the trace of the actual
opposite-neighbor computation, its index, what controls its branch, and where absolute values
are available in the code. Does any chart-local write or repair invocation follow from
observing the number? Check the universal five-chart carrier obstruction independently.

Return one JSON object. verdict is ACCEPTED, REVISE, or FAIL. native_bridge_status is OPEN
if the actual event-to-access bridge remains open. findings, missing_assumptions, counterexamples
and limitations must be arrays of strings. Write five worked proof_checks entries under
inputs, work, repair, caller and scope. ACCEPTED with no substantive defects leaves findings,
missing_assumptions and counterexamples empty. Otherwise state defects candidly. In check_values
give a dictionary with the following independently calculated values: changed_neighbor_pairs
(integer, maximum possible number of starting works that can change in this class);
local_maxima_twice (list of three integers, TWICE the original starting maximum over the
six neighbor pairs of chart 12 for source grades 1, 2, 5/2 IN THAT ORDER);
receiver_source_work_after_times_four (list of three integers, FOUR TIMES chart 12's work to source 0
after the first source cut, for the same ordered grades);
outer_legal_count (integer, legal second edits in the 25-chart example);
only_non_source_command (a list of two INTEGERS, chart then site, for the admitted
non-source edit when one exists). Check all factors of two, including fractional responses.
Do not alter your scientific conclusions to produce a passing result."""


def main():
    data = (ROOT / DRIVER).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != DRIVER_BLOB:
        raise ValueError("Unexpected inherited review driver identity")
    spec = importlib.util.spec_from_file_location("receiver_work_review_driver", ROOT / DRIVER)
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
    expected = dict(changed_neighbor_pairs=6, local_maxima_twice=[4020,4008,3999],
                    receiver_source_work_after_times_four=[7988,7976,7967],
                    outer_legal_count=32575,only_non_source_command=[12,2])
    if verdict.get("check_values") != expected:
        raise ValueError("Review values require examination")
    for key in ("findings","missing_assumptions","counterexamples"):
        if verdict.get(key) != []:
            raise ValueError("Review contains an unresolved concern")


if __name__ == "__main__":
    main()
