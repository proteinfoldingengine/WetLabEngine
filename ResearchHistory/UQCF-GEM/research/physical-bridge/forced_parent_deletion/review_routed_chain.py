"""Challenge a separate historical receiver-side call on its own source and scope."""
import hashlib
from pathlib import Path
import review_common_field

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROUTED_CHAIN.md": "1bc6ee43c3e91ef46dddecb2dec025f7df289c45",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_routed_chain.py": "29bf8ba4c5cdda5b824f4ad51563fccd617789e4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/REMOTE_PORT.md": "158b806478df2dbf06d56e2d13d58926dac324b2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/TERNARY_CHILD.md": "a0ea3822b94f4c3b90b0c98d17fd7f0d13b263bf",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/producer.py": "7c4f65714d6b9ccda7f4bb0fc378b0daef957fff",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/graph_producer.py": "6c8eca570cda82b64c0d06775672f33977be430a",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"
}
QUESTION = """Independently challenge the entire ROUTED_CHAIN.md scientific argument. Reconstruct both original source atoms and root/child hitting numbers on the nine-vertex tree. Verify the actual original graph and producer perform target computation and both parent calls. Inspect the independent replay code and compare the complete masks. Reconstruct child palettes, equal local q, first B update, final persistent B(v7), coalescing state and recomputed restart, whether no-deletion was in the graph or a selected normalization. Test the opposing passive and common-field controls and the sign and cancellation of the secondary B dipole on the v1–v7 edge. Check if unchanged ambient signed drives can change the shared field, and exactly which physical or activation premises were supplied. Compare historical v16.52 and v16.53 without treating different versions as stages of one physical run. The bounded comparison is exploratory. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations and proof_checks, and native_bridge_status. For ACCEPTED the first three arrays must be empty. State numerical or symbolic checks; a bare verdict is inadequate."""
if __name__ == "__main__":
    parent = (Path(__file__).resolve().parent / "review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob " + str(len(parent)).encode() + b"\0" + parent).hexdigest() == "423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
