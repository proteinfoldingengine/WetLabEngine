"""Review the measured profile and its downstream write."""
import hashlib
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FORK_PROFILE_WRITE.md': '05ac78b6cc39ae3fb7e8cbba378838ff810e15c1',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fork_profile_write.py': '202f16ffedea32fba34755c38425663f3da70af7',
 'ResearchHistory/UQCF-GEM/demos/v16.45-binary-fork-unit-barrier/producer.py': 'e73a02ee05e11f0c6b041b783ba6ff9738271073',
 'ResearchHistory/UQCF-GEM/demos/v16.45-binary-fork-unit-barrier/star_normalize.py': 'd58cc9d1168d219b2869affd2d4ede889ebe579b',
 'ResearchHistory/UQCF-GEM/demos/v16.45-binary-fork-unit-barrier/verifier.py': '26b4ab278c70ad9c958dbaccc676b2f18f2b30ad',
 'ResearchHistory/UQCF-GEM/demos/v16.45-binary-fork-unit-barrier/graph_producer.py': '6c8eca570cda82b64c0d06775672f33977be430a',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b'}
QUESTION = 'Independently reconstruct the matched source atom and receiver mask histories. Check that the same right-star input and program phase are reached and isolate the stored palette from the live cover. Use the extracted exact archived paths to decide what was in the original campaign and what was newly composed. Attack the five-state predictor bound, ordering dependence, forced write in software and limits on physical occurrence and access. Recompute vertex 5 ownership, both next edits and fifth receiver edits. Verify the coalescing full-view control. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, a substantive proof_checks object, and native_bridge_status OPEN. An acceptance requires empty first three arrays. Do not claim to have run code.'


if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json", "fork_certificate.json"):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
