"""Independent review of the frozen fixed-donor construction."""
import hashlib
from pathlib import Path
import review_common_field
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FIXED_DONOR.md": "f9a9941146466e2de50846a0646ddccf92d3d1df",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FIXED_DONOR_PROTOCOL.md": "290231800a5b32861108126d3053bd46a97d5fcc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fixed_donor.py": "1dda2e6c075282731db9c5c8b34df321ceaf50e3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/fixed_donor/result.json": "5e168bb4ad9da78ee7f85258c45048d914e88b0e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/fixed_donor/initial_failed_stderr.txt": "c46961d920ccd4c89749f5d502c3eb94f7bf25a8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROUTED_GRADE.md": "14cf866d326a4fece8484f1baa08258598aaeeb3",
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
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2"
}
QUESTION = "Independently reconstruct FIXED_DONOR.md, using exact original code and evidence. This is a bounded support result for the existing native-receiver research, not a physical detection or universal native-necessity claim. Check every positive claim and limitations, including:\n1. Two preparations only differ at v8 while B and D and their full initial grades agree. Compute root hitting profiles before/after all four edits; distinguish local deleting data from full differing event certificates.\n2. Reconstruct the original six normalization calls and canonical endpoints, first high B write, persistent junction formula R=g1+(1-I)g7, exact interaction -g7, positive contrast-holder sequence and zero/negative controls. Does formula use g7 or g8, and is anything unjustified about the source amount comparison?\n3. Check every required hypothesis of the referenced unique compatible grade lift. Check common-field blindness and the corrected literal-intersection comparison when B199 no longer contains B63. The preserved initial exception is a checker-domain error, not a physical negative result. Any false mathematical claim in the report needs an explicit correction.\n4. Analyze same literal D deletion as first internal move of the no-external-deletion caller, then +A1 vs +B7. Are the source-family records really equal? Identify fresh call, target, grade association and receiver read as supplied.\n5. All24 permutation diagnostic: the named B has endpoint h exactly when at position1 in the high arm and position0 otherwise. Does any invariant receiver selection follow? Check the limited four-label minimality statement.\n6. Inspect the independent verifier and reconstruction, 900 grade-state/3600 chart checks, 150 checked main/diagnostic paths, 210 original directed regression, corruption controls. Delimit constructed runs versus archived representative runs and general rational proof vs finite evidence.\nReturn only JSON with verdict ACCEPTED/REVISE/FAIL, findings, missing_assumptions, counterexamples, limitations, proof_checks, native_bridge_status. Reconstruct actual equations and numerical values in proof_checks. findings is only actual defects; limitations is for already-declared constraints. ACCEPTED requires empty findings, missing_assumptions, counterexamples. Otherwise provide the explicit counterexample or precise repair. Never infer a gravity signal or real measurement from an accepted mathematical argument."
if __name__ == "__main__":
    parent = (Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(parent)).encode()+b"\0"+parent).hexdigest() == "423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
