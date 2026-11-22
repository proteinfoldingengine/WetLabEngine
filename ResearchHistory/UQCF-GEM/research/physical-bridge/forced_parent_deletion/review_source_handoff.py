"""Audit the archived source-leaf handoff and its readout correction."""
import hashlib
from pathlib import Path
import review_common_field
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/SOURCE_HANDOFF.md": "a70da18b20f6b23b688d946af05b8d07ae25536e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_source_handoff.py": "dbbb3e3c7d4afcd114d3debc6390d5bacf98f03f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_adjacent_handoff.py": "8545c740360a93e2860d2b64b0d8db388aa439ba",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/source_handoff/census.json": "7026e1dd1426ed80beeee9fe4ce3dee929a93100",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/source_handoff/adjacent.json": "1a4f459e22af0b80f214a9479e3d077a33e9ef07",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_minimal_completion.py": "5e2d136c0e1bb092d9d92fcf187c0f792a717631",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fixed_donor.py": "1dda2e6c075282731db9c5c8b34df321ceaf50e3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_routed_chain.py": "29bf8ba4c5cdda5b824f4ad51563fccd617789e4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_routed_grade.py": "4c16f2f6243f4be4f0d34bd9a9e5f24a8c1e4133",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/producer.py": "7c4f65714d6b9ccda7f4bb0fc378b0daef957fff",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/graph_producer.py": "6c8eca570cda82b64c0d06775672f33977be430a",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/verifier.py": "a2f8b9d9b0be3b8d243b11fc5fdab443603f420f",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/graph_verifier.py": "ff8af4ecf743507d0d601daffa9b054441b85fd1",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py": "48f132d141167d9cd85ff79ec41720b5dca4f8bb",
    "ResearchHistory/UQCF-GEM/demos/v16.28-diamond-attribution-closure/producer.py": "36c894db328c0865007df3ca273ddb059475fe4a",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/THEOREM.md": "dd0a396e19e18a4302d93a40933cd87865c5eab4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/SOURCE_HANDOFF_PROTOCOL.md": "9e07b0becc8f43895ff269c64f56d7736d2c95f2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/MINIMAL_COMPLETION_EXACT_READOUT.md": "0303deb422c5ab12e351cd47ec0f0e04719f6bbf",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_minimal_completion_exact.py": "855ded2a4f92ce6ce7d01aca4bd20fd28f4d2fbf",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/minimal_completion/exact_readout.json": "e1fd988881f089839fddb433b33813c488f4b411"
}
QUESTION = "Challenge the conditional single-history result in SOURCE_HANDOFF.md using original sources and the complete directed-corpus evidence. Independently reconstruct the source-grade identity for the +B9, -D9, +C9 sequence at indices 178,184,190, root-fiber h=g0+g10 and a=g9. Test arbitrary compatible intermediate grade histories with only W1 fixed unchanged-chart grades and W2 overlap compatibility. Examine exact kernel checks, explicit positive source comparison, possible drift in other coordinates, and whether the source-root distinction vanishes on coarsening under the stated P1 comparison. Reconstruct the actual controller, temporary slot and eventual release, and check if the deletion itself could suffice, including the terminal factor control. Distinguish the prospective largest leaf / unique twin null from the explicitly exploratory scan across outer leaves without a twin requirement. Distinguish transient chart grade, structural occupancy, physical read access and any gravitational observable. Inspect additive checker correction, exact fractional example and two false claims under unchanged prior theorem. The raw historical compressed corpus is pinned by blob and compared in full during replay. Do not claim to have run code. Return JSON with verdict ACCEPTED, REVISE or FAIL, findings, missing_assumptions, counterexamples, limitations, proof_checks and native_bridge_status. Include concrete source cases, counts, numbers or exact equations in proof_checks. Give specific actionable defects in findings. ACCEPTED requires empty findings/missing_assumptions/counterexamples."
if __name__ == "__main__":
    data=(Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS=DOCUMENTS
    review_common_field.QUESTION=QUESTION
    review_common_field.main()
