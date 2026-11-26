"""Submit the one-leaf regular recovery proof to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/same_leaf_regular_recovery/SCOPE.md": "2649733967070ab4dc41f0142d78b3a8b0c4a90b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/same_leaf_regular_recovery/RESULT.md": "3c58d023eb39675c63498b5965253b551f285bb7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/same_leaf_regular_recovery/probe.py": "6d8f316436fa476769c951ccc897c0c848dff88d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/same_leaf_regular_recovery/probe.json": "c92f50d8ff692fed82bfd9c33497ebced58178b4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/same_leaf_regular_recovery/verify.py": "d8154aafc955827ceff825807dae4076b0d6dd17",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/same_leaf_regular_recovery/verification.json": "eb60309ae1af3e4ff168d75faef4dbd158a97033",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/transport.py": "df552284c16d43bc876340fbc13fe91eb9ee6a00",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/application.py": "30348d71d366a751932ec2d58d18a9148d81ae83",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = "Independently adjudicate the bounded theorem and replay in RESULT.md. Reconstruct the same-source-leaf addition, complement supports and isolated A–B work difference; test full v15.43 geometry admission, equality or inequality of invariant evaluation for every common scalar field, completeness of the legal one-edit round (including inverse withdrawals and source undo), and the different receiver P1 outputs. Identify whether a comparison is a supplied action, an actual old caller, or a conditional proved branch. Look for a hidden assumption, numerical error or a real counterexample to any scoped claim. Do not infer physical event selection, endogenous recovery, metric novelty or native access from a successful symbolic composition. Return JSON fields verdict (ACCEPTED, REVISE or FAIL), findings, missing_assumptions, counterexamples, limitations, proof_checks, program_status and native_bridge_status (DERIVED, REFUTED or OPEN). OUTPUT CONTRACT: If you independently find no defect in the bounded mathematics and elect ACCEPTED, findings, missing_assumptions, and counterexamples must each be literal []; put affirmative checks in proof_checks, and already-disclosed scope limitations (including absent physical access) in limitations. If there is a real flaw within the bounded scope, say REVISE or FAIL and explain rather than emptying the arrays. Do not trust the author conclusions. REQUIRED FIELD ENUMS: verdict is one of ACCEPTED, REVISE, FAIL. Independently, program_status must be exactly one of DERIVED, REFUTED, OPEN. Do NOT put ACCEPTED, REVISE, or FAIL into program_status. DERIVED means the predeclared conditional executable/mathematical result follows; REFUTED means it does not; OPEN means evidence is insufficient. Separately, native_bridge_status must be exactly one of DERIVED, REFUTED, OPEN and concerns native event/physical access, not the conditional replay. Check both status values belong to their own enumerations before returning JSON."
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
