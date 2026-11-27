"""Adjudicate the joint withdrawal result via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_withdrawal_constraint/RESULT.md': '657e9004a81e88c5f0f1c3b2b194c625f77810a1',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_withdrawal_constraint/SCOPE.md': 'c609fe90b8985e9085889809b2b4e668ae1d28c1',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_withdrawal_constraint/fixture.json': '806d2bc487e358f498cafa806226d1f658e98d26',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_withdrawal_constraint/replay.py': 'c070cc062069f3e2b28bf22b27b0b1b9da56e334',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_withdrawal_constraint/results.json': 'e90716d658cb8de20297feec02a75af7c68eed56',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_withdrawal_constraint/verification.json': '77fdb50302f34f09fff3d013c3e9e381634ec83d',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_withdrawal_constraint/verify.py': 'ae17ce07a856d7110823c54323626254cb49fab9',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/evidence/EXAMPLES.json': '94909a58db4d8dcc59c76fcfb61f2712edb5627f'}
driver.QUESTION = 'Independently try to refute the theorem in RESULT.md. Check the quantifiers over finite projected addressed sequences, arbitrary interleavings, the precise lost sequences for supersets and proper subsets of the remaining holders, internal sites on the covered union, and the difference between optional stopping and maximal completion. Is the two-untouched-chart relation in the archived ZERO example real? Inspect conditional symmetry, the five-chart source histories, terminal counts, the historical factor endpoint control and the six-chart preemption. Identify any overstatement of what the group can observe, of causal propagation between sites, or of participant-owned delivery. The historic census has up to four distinct initial rows and the independent four-site graph includes reached duplicate rows. Distinguish the unbounded proof, finite enumerations, and program custody. Return JSON with verdict ACCEPTED, REVISE, or FAIL; program_status and native_bridge_status independently DERIVED, REFUTED, or OPEN; and five string arrays proof_checks, limitations, findings, missing_assumptions, counterexamples. Put verified conclusions in proof_checks and explicit scope limitations in limitations. Use findings only for substantive unresolved defects. For an ACCEPTED verdict findings, missing_assumptions, and counterexamples must all be empty. If a defect exists, use REVISE or FAIL and describe it concretely.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))

    if answer.get("verdict") != "ACCEPTED" or answer.get("program_status") != "DERIVED" or answer.get("native_bridge_status") != "OPEN":
        raise ValueError("Independent review requires adjudication")
