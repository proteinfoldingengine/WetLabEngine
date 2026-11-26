"""Submit the first cut return study to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/RESULT.md": "7abeaebf3d46b653ef01d1b5d4e20ce6bb4c9838",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/SCOPE.md": "8ea8183bc608bbac4d94a4c6bd47e5ee702a7c04",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/FOUR.md": "180967bf44d95fc87053a221de851a91ee41e7b3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/SINGLE_LEAF.md": "6a9fae4ba6eb1aed2899a3f8b4fd49a3756fd58a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/probe.py": "45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/verify.py": "28785cf7f2337030e16fc85de1ec19b55cf12b6a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/verification.json": "c0bb61bcf4bb942380152a53c120309b25260f99",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/raw.json": "c7b1e7ec8d319592b4517cd873c9b9f354056e16",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/verify.py": "65780a4c3374e49eacd44d47849430b6e5da4675",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/COVER.md": "f477af73cbc780dbcd641252a7c5fa3c8a64c78b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/COVER_SCOPE.md": "13f0894bb00a1c26291d8bad04f6353c6997de9e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/cover.py": "416f4ce2d337b9dbf3c8cb2916d62164cf091ffd",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/cover.json": "bb4489c8abd7189b2a5e8dffcb68775050a47041",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = "Independently adjudicate the pure-orbit collective return report. Reconstruct the 704 vs 1088 gap, actual diagonal full geometry, both cut indicators and constant shifts, and the exact two endpoints under arbitrarily many single-leaf edits. Check paths, intermediate irregularity, union legality, addressed and anonymous P1, odd-order parity hypotheses, exact four-edit exhaustion with independent counterleaves, weak-majority obstruction, and both length bounds. Distinguish pure orbit geometry from a derived footprint or invoked dynamics. Verdict enums ACCEPTED, REVISE, FAIL. Program status DERIVED, REFUTED, OPEN; native_bridge_status DERIVED, REFUTED, OPEN for physical enactment. Include proof_checks and limitations. Under the historical schema findings is a list of unresolved substantive defects ONLY. If and only if accepting, return literal empty arrays for findings, missing_assumptions, counterexamples. Put all successful checks only in proof_checks. Challenge freely and revise or fail if warranted."
QUESTION += '\n\nReturn exactly ONE JSON OBJECT. Do not wrap it in a list. Give separate worked checks for two distinct propositions. P_math: the bounded combinatorial results in RESULT.md and COVER.md, including exact cover constancy, endpoint witness equality and the native scalar controls. P_physical: the system autonomously initiates a physical update, with a physically accessible recipient. Establishing the first does not establish the second. Assign program_status to P_math and native_bridge_status to P_physical independently using DERIVED, REFUTED or OPEN and explain whether any supplied material establishes an actual physical process. Use a JSON object with verdict: ACCEPTED, REVISE or FAIL, both status fields, proof_checks, limitations, and the three defect arrays. Only on acceptance the three fields must literally be "findings": [], "missing_assumptions": [], "counterexamples": []. Positive checks belong only in proof_checks. Do not copy an expected verdict: adjudicate both propositions yourself.'
payload = DRIVER.read_bytes()
if sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest() != "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e":
    raise ValueError("Unexpected inherited review driver")
spec = spec_from_file_location("four_child_review_driver", DRIVER)
driver = module_from_spec(spec)
spec.loader.exec_module(driver)
driver.ROOT = ROOT
driver.DOCUMENTS = DOCUMENTS
driver.QUESTION = QUESTION
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if (answer.get("verdict"), answer.get("program_status"), answer.get("native_bridge_status")) != ("ACCEPTED", "DERIVED", "OPEN"):
        raise ValueError("Independent review requires adjudication")
