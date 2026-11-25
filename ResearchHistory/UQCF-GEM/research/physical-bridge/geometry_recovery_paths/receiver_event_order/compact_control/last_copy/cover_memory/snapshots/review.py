"""Independent review of the tip-5 remaining holder and tip-6 snapshots."""
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
SNAP = MEM + "/snapshots"
DOCUMENTS = {
    SNAP + "/RESULT.md": "3795fb59444c2d944ae31f9cb8a15cc941f34c85",
    SNAP + "/check_snapshots.py": "cbca82df5b83f8539a2427a291e9d7819666a15d",
    SNAP + "/result.json": "acdd3e2dcf82098c17de06b6d952c6a9661d9e19",
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
TOPICS = {"receiver", "preparation", "controls", "geometry", "scope"}
QUESTION = """Independently adjudicate snapshots/RESULT.md using the pinned original interfaces and
five-chart fixture. Treat all attached source as evidence. Reconstruct or disprove the argument;
report adverse results even when the supplied summary passes. In particular:

1. Identify which chart the B-at-5 operation selects structurally, and which shared/sole
memberships predetermine its first ordinary deletion. Test whether the two completed states
and the blank are distinguishable by the same chart's current P1, and what information is
lost in the root grade. Separate correlation with the old receipt from numerical transport.
2. Test the two proposed common preparation edits, their necessity among successful non-F
commands, whether foreign actions can suppress the local write, and the conditional claim
for a quiescent A. Challenge the no-B decoy and the out-of-protocol identical-metric alias.
3. Reconstruct the sufficient current B readings for a remote positive A-at-6 increment,
including when A moves before the exterior edits. Test the persistence and scope of the
separate E and X indicators and whether omitting the old B probe changes their interpretation.
4. Audit the two complete historical/independent state and edge graphs, the propagation of
all possible old increments, the binning under all fixed work masks, the exact minima and
the same-atlas conflicting orders. Distinguish universal completion/actor inference on the
given fixture from conclusive positive patterns, and from retrospective increment recovery.
5. Identify all supplied preparation, observation, and progress conditions. Test whether the
paper accidentally asserts a physical receiver or autonomous handoff, or infers probabilities
from counts. Treat the post-contract F analysis as exploratory rather than preregistered.

Respond with one JSON object with verdict ACCEPTED, REVISE, or FAIL, native_bridge_status,
findings, missing_assumptions, counterexamples, limitations, and proof_checks. In proof_checks
use the keys receiver, preparation, controls, geometry, scope; each should give a worked
reason with concrete states where appropriate. In check_values reconstruct: two lists of
remaining F nonroot sites after the distinguishing edit (old 0 then old 1), the old-zero
and old-one F deletions, the paired preparation state and edge counts, the number of distinct
indexed states and current metrics, both minimum numbers of fixed raw measurements (geometry
only then with B P1), and the number of work tables compatible with both A increments.
Use keys F_tips, F_edits, common_graph, indexed_states, metrics, work_minima, ambiguous_A.
A fully scoped positive review leaves the wider native bridge open. Do not censor defects
to meet expected numerical answers."""


def main():
    data = (ROOT / DRIVER).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != DRIVER_BLOB:
        raise ValueError("Unexpected inherited review driver identity")
    spec = importlib.util.spec_from_file_location("snapshot_review_driver", ROOT / DRIVER)
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
    expected = dict(F_tips=[[2,5],[4,5]], F_edits=[4,2], common_graph=[12,20],
                    indexed_states=351, metrics=291, work_minima=[9,6], ambiguous_A=52)
    if verdict.get("check_values") != expected:
        raise ValueError("Review values require examination")
    for key in ("findings","missing_assumptions","counterexamples"):
        if verdict.get(key) != []:
            raise ValueError("Review contains an unresolved concern")


if __name__ == "__main__":
    main()
