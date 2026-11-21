"""Independently challenge the frozen fixed-site signed response and common-field calculation."""
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/REMOTE_PORT_PROTOCOL.md": "896b209ace68948ce00a98179efd61ce48ff0c2f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/REMOTE_PORT.md": "158b806478df2dbf06d56e2d13d58926dac324b2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_remote_port.py": "b7468a58d6a9bdb8bd4dd6182c83c41ec6a50ce4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/remote_port_results.json": "a4f2b70c02ada576c3fda3b7855f19410b8d3f28",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_active_holder_write.py": "9b43594319f0d35dc477aa52cfeb899c8552d7cf",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ACTIVE_HOLDER_WRITE.md": "ec1b1f22f54ff26c7cb36ae36f010dadbcba5a5a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/LOSS_SUPPORT.md": "3e25e54be68c827bc9d945ca976d06a043fe1354",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/PROOFS.md": "fd92415cc08e83858d4368047721c2bb27f9e500",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.24-consistency-order/engine.py": "666617d33bf8925699d0dc440565588a5e40e57e"
}
QUESTION = """Independently challenge REMOTE_PORT.md. Use the exact producer, verifier, prior report and supplied results. Interpret the procedure as an exploratory comparison of two existing models with fixed common input. Reconstruct these checks and report actual signs, counts and controls. Identify defective mathematics, historical operational claims, or a hidden physical assumption. Do not infer a detector.
1. Project masks at v3 for rows 1782, 2466 and 2468. Verify the second site-local step, named initial prefix, queried C-command outcomes, original guard and child input. Verify the 144-case classification and limits, quiet/identical placements, weaker six-move path, and why a local algorithm seeing only this prehistory cannot decide the next edit from that input.
2. Derive the sign of (E_new-E_old)g, crossed primary loss at v1/v4, the sign of the local Green response to each secondary dipole, and the effect of overlap subtraction. Derive the coefficient and five-column functional. Compare the second-v3-update comparison and the same-actor step-four comparison. What actually changed in C? Separate the physical observable, computed component and extra command. Check the four-drive replay under v16.22/O4 on 2576 states and any universal assertion within the finite star.
3. Derive one-versus-two port representation and the same effective resistance. Inspect the independent v16.24 certify code. Reconstruct the signed sample, positive control, threshold max(a,b)<=T<a+b, mask and limits. Check the historical continuity gap. An empty or verbal verdict alone is inadequate. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations and proof_checks, and native_bridge_status. For ACCEPTED the first three arrays must be empty. Distinguish explicitly supplied boundaries from defects. Report actual numbers."""


if __name__ == "__main__":
    parent = (HERE / "review_common_field.py").read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(parent)).encode() + b"\0" + parent).hexdigest()
    if blob != "423357012a59a192b158204df03ffd9dbb4ee90e":
        raise ValueError("Parent review entry point changed")
    import review_common_field

    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
