"""Challenge a separate historical receiver-side call on its own source and scope."""
import hashlib
from pathlib import Path
import review_common_field

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/TERNARY_CHILD.md": "a0ea3822b94f4c3b90b0c98d17fd7f0d13b263bf",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/readback_ternary_child.py": "3fea765875bd32312e4f4f2f8be3189a877a0ec4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/REMOTE_PORT.md": "158b806478df2dbf06d56e2d13d58926dac324b2",
    "ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/producer.py": "90108c926299ca7cb66dca6acc4530bafcdb4a7e",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3"
}
QUESTION = """Reconstruct and try to falsify the entire TERNARY_CHILD.md claim from the supplied historical code and trace program. Verify source leaf, masks, both tau values, relative ordered path and whole move counts for both archived arms. Give the actual raw argument, child return and surviving distinction for v6 and the subtree at v1. Check no-deletion and singleton-limiting controls. Is q calculated by v16.52 produce or input in its spec? Is the event output automatically passed to this routine and is an observable physically delivered? Compare the four-star v16.53 caller. This is a separate bounded mathematical and software comparison. Explicitly supplied premises count as limitations when correct. Return JSON with verdict ACCEPTED, REVISE or FAIL; arrays findings, missing_assumptions, counterexamples, limitations and proof_checks; and native_bridge_status. For ACCEPTED the first three arrays must be empty. Give checked numbers and precise limitations."""
if __name__ == "__main__":
    parent = (Path(__file__).resolve().parent / "review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob " + str(len(parent)).encode() + b"\0" + parent).hexdigest() == "423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
