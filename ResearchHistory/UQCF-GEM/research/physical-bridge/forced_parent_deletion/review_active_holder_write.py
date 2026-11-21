"""Independently review the frozen source-to-receiver comparisons in the original star."""
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ACTIVE_HOLDER_WRITE.md": "ec1b1f22f54ff26c7cb36ae36f010dadbcba5a5a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_active_holder_write.py": "9b43594319f0d35dc477aa52cfeb899c8552d7cf",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/active_holder_write_results.json": "1ebc19091794d6cdf4c758d2a1a23bc0e120b560",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/coverage.py": "e90576a0285357f62ca2f9d9cac872b2a226e823",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/run_campaign.py": "6d09f058232fcda6166b303abb0559bc3d9d9f5b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/TYPE_AND_PROOF.md": "69ace252586ad0b323ca3c460304ead8da8fd917",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_move_interface/RESULT.md": "0371d4a8aa66ce02ffbda084ad5dde93f1ec1136",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/profile_receiver_signal/RESULT.md": "0c30baebd38f794ad41626884749c3aa21c7a0d3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/LOSS_SUPPORT.md": "3e25e54be68c827bc9d945ca976d06a043fe1354"
}
QUESTION = """Independently reconstruct and challenge ACTIVE_HOLDER_WRITE.md. Adjudicate the arithmetic, logical quantifiers, historical source/record types and scope. Be specific about any defect. Reproduce these checks in your own terms:
1. Classify all eligible four-leaf R pairs into the 144 cases. Identify S, R and T without presupposing the selected receiver. Show the local count sequences and signs at the second true receiver edit from the original low and high paths. Distinguish a high-branch band consequence from the actual coverage algorithm and the existence of a second edit. Does any claim wrongly extend to arbitrary routes, physical events, or nonarchived four-label inputs?
2. Rebuild both star examples from the raw masks. For rows 1782/2466 check old full receiver data vs bare external coverage, which site changes at each first write, signed remote write at second own index, global indices/lengths, no-deletion control, terminal bit stability, common-carrier and unit Green blind-port control. Check alternate six-move route for exact admissibility and sign. For rows 1196/1882 verify same source site, equal loss, equal bare receiver interface, restoration/shared incidence states and saved target causing later branch-specific writes; distinguish a one-sided prefix from two-sided second-own-write discrimination.
3. Derive the first-role degree versus old minimum-cover trigger law, and distinguish finite archive counts from probabilities. Inspect actual R producer, complement cover, bit-write, immediate guard, recursive leaf remapping, primitive selection and physical readout boundary. Credit October’s earlier profile writer and directly state what improves over it. A source-atom result has the shape of a historic R input, but is there a native runtime subscription? Determine what is mathematically observable and what actual physics remains unknown.
Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations and proof_checks plus native_bridge_status. Empty findings/missing_assumptions/counterexamples are required for ACCEPTED. A bare verdict is insufficient; give concrete checked numbers or equations. Different explicitly declared physical premises are limitations if the conditional proof is correct."""


if __name__ == "__main__":
    parent = (HERE / "review_common_field.py").read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(parent)).encode() + b"\0" + parent).hexdigest()
    if blob != "423357012a59a192b158204df03ffd9dbb4ee90e":
        raise ValueError("Parent review entry point changed")
    import review_common_field

    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
