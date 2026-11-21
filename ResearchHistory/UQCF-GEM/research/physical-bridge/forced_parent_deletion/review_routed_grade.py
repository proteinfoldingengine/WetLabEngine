"""Review the frozen compatible grade lift on historical paths."""
import hashlib
from pathlib import Path

import review_common_field


DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROUTED_GRADE.md": "b63cf0e56440d2039d9882cc366ce979489fe527",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_routed_grade.py": "4c16f2f6243f4be4f0d34bd9a9e5f24a8c1e4133",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_routed_chain.py": "29bf8ba4c5cdda5b824f4ad51563fccd617789e4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROUTED_CHAIN.md": "1bc6ee43c3e91ef46dddecb2dec025f7df289c45",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/LOSS_SUPPORT.md": "3e25e54be68c827bc9d945ca976d06a043fe1354",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/produce_certificates.py": "a056d636900db6ab8f9a7775dd75e7dd190e6fe8",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/producer.py": "7c4f65714d6b9ccda7f4bb0fc378b0daef957fff",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = """Independently reconstruct and challenge ROUTED_GRADE.md using the exact code and proofs. Verify the hypotheses separately from consequences. Work through the following:
1. On a finite rooted cover, prove or falsify unique compatible grade evolution through all one-view edits when untouched chart grades are fixed, retention of old marginals is required, and the union stays fixed. Reconstruct Y, J, Jprime and the exact O2 argument. Address multiple unchanged holders, positive scope and zero-extension or moving-C counterexamples.
2. Show the inherited constrained continuation at the actual v1-v7 coarsening/refinement. For the two positive preparations, give complete-initial-B blindness and calculate the 4,4 versus 2,1 and 2,3 readouts, the exact B,C,A holder sequence boundaries and final carrier, and the unit-grade check. State whether the historic normalizer itself handles a source-grade vector, which chart may provide the old h amount, and why a fixed old port and the joint field are blind.
3. Check FCV old record types and 22/15 versus 2/3, chart address matching and scope. Verify the local Kirchhoff calculation against v16.22 and P6. Identify whether this old FCV operation is an automatic receiver-owned callback in v16.48.
4. Reconstruct when the same C event certificate appears inside the low run and as high input. Give competing next edits, the equal grade-family comparison and which role the saved target plays. Distinguish a defined atom certificate from an emitted hardware event. Challenge the native/physical interpretation and assert precisely what if anything becomes determined without a new gain or reader.
Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations and proof_checks, and native_bridge_status. Empty findings/missing_assumptions/counterexamples are required for ACCEPTED. Conditional declared hypotheses can count as limitations when the proof is accurate. A bare verdict is insufficient. Include numerical and structural checks."""
if __name__ == "__main__":
    parent = (Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(parent)).encode()+b"\0"+parent).hexdigest() == "423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
