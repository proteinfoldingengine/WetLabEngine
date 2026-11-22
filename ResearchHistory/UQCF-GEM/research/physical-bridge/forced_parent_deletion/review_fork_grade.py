"""Review the measured profile and its downstream write."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fork_grade.py': 'c6ab5b08cda72ee4485c3cf4c067e6b680eba0b4',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FORK_GRADE.md': 'd8e5138480b6d5e91f65bcf9a424ab715e363e14',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROUTED_GRADE.md': '14cf866d326a4fece8484f1baa08258598aaeeb3',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FORK_PROFILE_WRITE_RESULT.md': '8ad94af1b0dc4c6eb2653d1e2821b9947afb2e0e',
 'ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md': '0c8223367caf4d81dd1fe5a33a4e94d092f1aac4'}
QUESTION = "Give a worked mathematical review using the supplied proof, exact code and trajectories. Return one JSON object. In a JSON object named proof_checks, write each of the four following keys with a nonempty paragraph of your own concrete calculations. Under induction use the O2 cover on a one-site addition and derive the grade result at the meeting. Under root_readout compute B's two fifth-edit root coordinate functions, their difference and what changes when both are aggregated to their common one-site view. Under failed_agreements reconstruct the A and B grade on the newly restored site in the first conflict, identify all offending path indices and explain why compatibility returns. Under scope distinguish a fixed positive probe from a signed contrast and address whether any of this triggers the software writer. Attack the claim critically, including possible counterexamples. Include verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, and native_bridge_status. An acceptance requires the first three arrays empty. Proof_checks is required for every verdict. Supply the actual derivations in the response, including when you find no defects."

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json", "grade_certificate.json", "fork_paths.json"):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()

    response = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    checks = response.get("proof_checks", {})
    if not all(isinstance(checks.get(k), str) and len(checks[k].split()) >= 10
               for k in ("induction", "root_readout", "failed_agreements", "scope")):
        raise ValueError("The review did not supply four written mathematical checks")
