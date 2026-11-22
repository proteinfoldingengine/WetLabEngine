"""Review the measured profile and its downstream write."""
import hashlib
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fork_grade.py': 'c6ab5b08cda72ee4485c3cf4c067e6b680eba0b4',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FORK_GRADE.md': 'd8e5138480b6d5e91f65bcf9a424ab715e363e14',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROUTED_GRADE.md': '14cf866d326a4fece8484f1baa08258598aaeeb3',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FORK_PROFILE_WRITE_RESULT.md': '8ad94af1b0dc4c6eb2653d1e2821b9947afb2e0e',
 'ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md': '0c8223367caf4d81dd1fe5a33a4e94d092f1aac4'}
QUESTION = 'Independently derive and attack the stepwise gluing induction, the fifth-edit and endpoint root covector, the root-only compression control, the exact three temporary failed overlaps in the zero-inclusion experiment and separate compatibility of the endpoints. Check both the signed example and owner-local ambiguity with nonnegative preparations. Assess whether anything selects or physically triggers the receiver write. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, substantive proof_checks and native_bridge_status OPEN. For acceptance the first three arrays must be empty.'

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json", "grade_certificate.json", "fork_paths.json"):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
