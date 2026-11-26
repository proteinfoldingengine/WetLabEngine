"""Submit the symmetric matched-event paper to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/RESULT.md": "2daf9d691b19b8679374daebbafb9bf2f704159e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/SCOPE.md": "a9130fd06b9158bc482fa39f0fe4b8f01444bfdb",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/probe.py": "81014d679f411c78922e9c9de322ede5721b2fb6",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/verify.py": "65780a4c3374e49eacd44d47849430b6e5da4675",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/raw.json": "6644ccf92a61bb588646b47e37dc4274125cfa57",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/verification.json": "f3102c1764d2f62b2aef6b0376aaad753559f788",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = "Independently adjudicate the two matched first-event alternatives in one vertex-transitive graded incidence preparation. Check that the complete initial work and support multiset really have no absolute marked chart/pair, but the relational leaf construction and geometry are purpose-built. Verify cut realization and positive grades, no smaller or adjacent rescue in the claimed distinct-two-actor class, the unique inferred recipient per first event, exact accepted same-address gain versus three alternatives rejected by opposite pairing for each arm, the independent coordinate checker and nonrepair controls, and the fixed chart 36's unchanged starting P1 record and -2 versus 0 terminal Pin. Challenge support multiplicities, P1 distinction, and any implicit enforcement of completion, event writing or receiver access. The symbol scope is a supplied first structural withdrawal and exact one-further-edit distinct-chart complete return. No physical reader or occurrence law claimed. REQUIRED FIELD ENUMS: verdict exactly ACCEPTED, REVISE or FAIL; program_status exactly DERIVED, REFUTED or OPEN for the conditional mathematical claim, not ACCEPTED/REVISE/FAIL; native_bridge_status exactly DERIVED, REFUTED or OPEN for actual physical relation. On an ACCEPTED verdict, findings, missing_assumptions and counterexamples must be literal []; successful checks belong in proof_checks, scope gaps in limitations. Otherwise report actual findings. Check each enum and do not take the author's verdict for granted."
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
