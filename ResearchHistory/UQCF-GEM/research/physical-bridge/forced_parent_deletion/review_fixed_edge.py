"""Independent mathematical challenge of fixed-port tests."""
import hashlib
from pathlib import Path
import review_common_field
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fixed_edge.py": "a3e2aa71c57ab946094b5deb0fd0dede01728b0c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_grade_relay.py": "fe87a11ab5f6030dfdb8a5b9b240bb0e53978195",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/fixed_edge/geometry.json": "26a6f5b19aafc1887e14d872ea9ff7ba73d1cb50",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/fixed_edge/relay.json": "6e17e4075e5b8f049d44aeacf06a0ab55070d7cd",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FIXED_EDGE.md": "99986805a8a770f7fbb3397db3fa811300becf54",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FIXED_EDGE_PROTOCOL.md": "687f9bd9ef9e264704cd3d097825481e2cdb9e8b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FIXED_EDGE_PROTOCOL_ADDENDUM.md": "bd724647727b9d459375ec5b17b2035c858a132d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/SOURCE_HANDOFF.md": "a70da18b20f6b23b688d946af05b8d07ae25536e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_source_handoff.py": "dbbb3e3c7d4afcd114d3debc6390d5bacf98f03f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fixed_donor.py": "1dda2e6c075282731db9c5c8b34df321ceaf50e3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_routed_chain.py": "29bf8ba4c5cdda5b824f4ad51563fccd617789e4",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/producer.py": "7c4f65714d6b9ccda7f4bb0fc378b0daef957fff",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b"
}
QUESTION = "Independently audit FIXED_EDGE.md. Give numerical and algebraic reconstructions: what is forced on edge 9, why zero baseline-subtracted change at the common chart B, how a root/leaf half-unit dipole is distinguished, and what the quadratic edge term can mean. Check the full, ungrounded Schur argument, the balanced load push, arbitrary fixed-old-port susceptibilities and effective resistances for this normalized kernel and the difference between altered loads and altered coupling. Verify the W1/W2 rational increment-space proof and the explicit positive counterexample to a unique total energy kick. Inspect the actual source and recovered occupancy read, protected relay to A, end of its protection and two positive continuations. Challenge an inference to amplitude consumption, gravity, or a measured nonzero field change. The archive is pinned and replayed by Actions; do not claim to have run code yourself. Return JSON with verdict ACCEPTED/REVISE/FAIL, findings, missing_assumptions, counterexamples, limitations, proof_checks and native_bridge_status. Give specific equations and values in proof_checks. An accepted verdict requires empty findings/missing_assumptions/counterexamples."
if __name__ == "__main__":
    data=(Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS=DOCUMENTS
    review_common_field.QUESTION=QUESTION
    review_common_field.main()
