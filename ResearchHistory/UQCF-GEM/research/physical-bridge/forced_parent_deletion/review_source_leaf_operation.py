"""Configure the inherited review driver for the v16.48 source-leaf operation trace."""
import hashlib
from pathlib import Path
import review_common_field

PREFIX = "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    PREFIX + "SOURCE_LEAF_OPERATION_TRACE.md": "7f88a48669677ac5b59c6a15d8e65d4d9ef16eff",
    PREFIX + "SOURCE_LEAF_WITNESS.md": "8ac79751417adfd7209166871fbc2c4a2952c809",
    PREFIX + "SOURCE_LEAF_WITNESS_REVIEW.md": "2be5dae407e9551ccd25ef7cdc7093aed275c370",
    PREFIX + "evidence/fixed_donor/result.json": "5e168bb4ad9da78ee7f85258c45048d914e88b0e",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/producer.py": "7c4f65714d6b9ccda7f4bb0fc378b0daef957fff",
    "ResearchHistory/UQCF-GEM/demos/v16.48-recursive-chain-repair/star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
}
QUESTION = """Independently reconstruct and challenge SOURCE_LEAF_OPERATION_TRACE.md from the exact code and existing fixed-donor result. This is an analytical operation trace, not a new numerical campaign. Develop the strongest valid claim and seek a concrete counterexample.
1. Inspect all palette_order_diagnostic rows for CD/delete_D. Are the named-B=455 endpoints exactly the six B-first permutations, with the stated masks and existing count?
2. Trace producer.normalize on the low AFTER state for q0=1<d0=2. Verify it invokes outer star before recursive inner normalization, that v8 is the sole outer vertex and C its sole holder, and h=1.
3. Trace star_normalize.normalize when B is palette position zero and H={C}. Does the code necessarily perform +B(v8) followed immediately by -C(v8), with no intervening inner edit or consumer? Check all six B-first orders.
4. From B=319 after that transfer and every recorded B=455 endpoint, prove at least one later B edit is unavoidable. At its first later B edit, do all unedited charts exclude v8?
5. Verify the lambda*(delta8-delta0) countermodel: every unchanged chart annihilates it under P1, W1 and W2 hold, B's v8 grade changes, and a sufficiently small rational lambda preserves strict positivity when applicable. Look for any overlap or code relation that blocks this drift.
6. Check the exact boundary: the operation supplies an ordered software path and B carrier only conditionally on B at palette position zero; it does not supply physical ownership, observable access, or protected original amplitude under W1/W2. Preserve the stronger conservative theorem under its original premises and reject any global impossibility claim.
Return only JSON with verdict ACCEPTED/REVISE/FAIL, arrays findings, missing_assumptions, counterexamples, limitations, proof_checks, and native_bridge_status. findings must contain only genuine defects. ACCEPTED requires empty findings, missing_assumptions and counterexamples. Reconstruct actual code branches, masks and the countermodel in proof_checks. Preserve adverse conclusions; do not infer a physical signal.
"""

if __name__ == "__main__":
    parent = (Path(__file__).resolve().parent / "review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob " + str(len(parent)).encode() + b"\0" + parent).hexdigest() == "423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS = DOCUMENTS
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
