"""Submit the ordered actor-pair derivation to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/derived_actor_pair/SCOPE.md": "5bc30ac1b9e64c8d572fd0b7454b62b87d14042f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/derived_actor_pair/RESULT.md": "c6cc636afd18e7cca3c68d26aed609b13e4d2e3a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/derived_actor_pair/probe.py": "9b9d27ef4216226a6ef8a603712b0faef634e431",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/derived_actor_pair/raw.json": "ec50c11a7e8de6a1c15ebb12ee2b1b79f42858f7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/derived_actor_pair/verify.py": "25061597f2333ae5d3fae4707d33df95d7105335",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/derived_actor_pair/verification.json": "433a6cbfb09206f0e2bd29fb9458381b4d5c0b5b",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = "Independently adjudicate the conditional role derivation, exact eight-history enumeration, and complementary-column work involution. Verify the two signed-edit extension of the minimum and opposite-pair exclusion, the 150/28 integer-grade test, grade-2 support candidates, and the difference between deriving actors of a two-edit recovery and selecting a physical event. Check reverse acquisition, literal equality of complete work traces at fixed actor order, and which ambiguity is removed if the first sign is independently known. Check actual original carrier calls, independent raw verification, and the withdrawal-only historical caller scope. State any real flaw with a falsifier. REQUIRED FIELD ENUMS (separate): verdict must be exactly ACCEPTED, REVISE, or FAIL. program_status must be exactly DERIVED, REFUTED, or OPEN, not ACCEPTED/REVISE/FAIL; this is the conditional executable mathematical claim alone. native_bridge_status must be exactly DERIVED, REFUTED, or OPEN and concerns physical enactment/access. If you find no defect and choose ACCEPTED, findings, missing_assumptions, counterexamples must each be literal []; successful verification goes in proof_checks and acknowledged scope gaps in limitations. Otherwise use REVISE or FAIL and state the unresolved issue. Do not trust author conclusions. Verify that all status values match their separate enums before returning JSON."
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
