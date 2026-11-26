"""Adjudicate the frozen fixed-exterior family via the existing pinned model driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import subprocess
import sys

root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
path = root / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
data = path.read_bytes()
if sha1(b"blob " + str(len(data)).encode() + bytes(1) + data).hexdigest() != "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e":
    raise ValueError("Unexpected historical review driver")
spec = spec_from_file_location("frozen_model_review", path)
driver = module_from_spec(spec)
spec.loader.exec_module(driver)
driver.ROOT = root
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/fixed_exterior_records/RESULT.md': 'bf83bd43309741e02c1a304b7e516216ebac63b2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/fixed_exterior_records/SCOPE.md': 'b28ee8dbb11dac2c8dcb3d0606005e4e4f865c3b',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/fixed_exterior_records/replay.py': 'e31252cad791503ce6d5ca829d48cffa063522f6',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/fixed_exterior_records/results.json': '2b6b5fbf39e2905b0b1a587e45d259b424e3fdb8',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/fixed_exterior_records/verification.json': '1642cbc1ecf7ee8a1c07343678baa5389e149331',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/fixed_exterior_records/verify.py': 'dc73f4c7c153054b4b1c60a2fc52a0cc9fa1947f',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/verify.py': '65780a4c3374e49eacd44d47849430b6e5da4675'}
driver.QUESTION = """Independently referee RESULT.md against the exact attached scope and programs. Look for a counterexample. Are population constraints necessary? Check injectivity modulo p, the pointwise named exterior versus a relabelled or scalar-only interface, cardinality of the 9x9 and 10x10 families, and the proportional-to-p^2 logarithm in a native square even if the inner boundary ring is frozen. Recalculate the 25-holder control, and check each interval and the normalization of work. Assess what the computation tests versus the general proof. P_math is the stated finite and asymptotic combinatorial result. P_physical is a native dynamical or thermodynamic interpretation. Adjudicate each separately. Return exactly ONE JSON OBJECT, with verdict ACCEPTED, REVISE or FAIL, program_status and native_bridge_status (each independently DERIVED, REFUTED or OPEN), proof_checks with worked mathematical reasoning, limitations and the three arrays findings, missing_assumptions, counterexamples. On acceptance the three arrays are empty. Positive checks belong in proof_checks. Be willing to revise or fail any unsupported claim."""
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))
