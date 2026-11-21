"""Adjudicate the general single-atom loss on its separately frozen source set."""
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/LOSS_SUPPORT.md": "3e25e54be68c827bc9d945ca976d06a043fe1354",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_loss_support.py": "6e26973f70f4a54d5fbc66b26e716efda2f17212",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/loss_support_results.json": "fc1bffe06616376b41e234ece21a25d399afeebc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/COMMON_FIELD.md": "79f295f93bd4b35d6382ffa5280e948c348c9358",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/PROOFS.md": "fd92415cc08e83858d4368047721c2bb27f9e500",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = """Adjudicate LOSS_SUPPORT.md independently. Reconstruct the argument for every finite rooted tree, orient the sign and identify both inclusions. Challenge the claimed exact set of nonzero holders, old-amplitude recovery, unit-conductance Green step and invariance of a passive glued source/field. Test h internal to X but a leaf of M, proper union, multiple holders, signed cancellation and nonzero negative q. Determine exactly which claim depends on overlap source compatibility, coverage preservation, or initial compatible response classes. Give an example distinguishing a potential gauge from changing a balanced source and showing why independent mean-centering can fail. Identify which statements were already in O2–O4 and why an event and changed local physical record are still open. Inspect the bounded enumeration, the rational column checks and its proper-union controls; finite counts cannot prove arbitrary size.
Return a JSON object with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations and proof_checks, and field native_bridge_status. A bare verdict gives no evidence of inspection. Include specific equations, independent numerical controls and source references in proof_checks, and any genuine counterexample in findings. Acceptance requires empty findings, missing_assumptions and counterexamples. Existing declared model and empirical premises are limitations."""


if __name__ == "__main__":
    parent = (HERE / "review_common_field.py").read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(parent)).encode() + b"\0" + parent).hexdigest()
    if blob != "423357012a59a192b158204df03ffd9dbb4ee90e":
        raise ValueError("Parent review entry point changed")
    import review_common_field

    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
