"""Review the frozen delayed geometry proof and finite witnesses."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py': '8163beba8e52bc2a3a6d0c8cf59dd1257222f65c',
 'ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/transport.py': 'df552284c16d43bc876340fbc13fe91eb9ee6a00',
 'ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/application.py': '30348d71d366a751932ec2d58d18a9148d81ae83',
 'ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py': '5cd286b014bb44025e16832ee91a6e6665291c8c',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_DELAY.md': '29702dfc76d0cec8e07d8a454fae77a8adebcebc',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_DELAY_CHECK_PLAN.md': 'b93616e98e0839547f470b3d12a5102849740b26',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_delay.py': '8f079b8fc0150a0f6468661f788099e7db40d0a7',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py': '3324c0b46e09120ae526338444a19070b692d049',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/geometry_delay_witness.json': 'c16cb37c282773c9c95c3348b27f67540dd2ee86'}
QUESTION = 'Independently challenge the exact delayed-recovery theorem and witnesses, with no inference to a physical law. Return JSON with verdict ACCEPTED, REVISE, or FAIL, arrays findings, missing_assumptions, counterexamples, and limitations, native_bridge_status OPEN or DERIVED, and proof_checks as four keyed, worked paragraphs source_only, silent_recovery, terminal, scope. Output feeds a strict validator. If you accept the mathematical scope, use exactly these status fields {"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[]}. Put affirmative observations in proof_checks and supplied conditions in limitations. Use REVISE or FAIL with nonempty objection fields for unresolved errors. For source_only derive why min and adjacency at the only edited row are fixed between two regular endpoints, check the 16 increase and the sign bound on every remaining source deletion. For silent_recovery check the integer work update rule, membership and 100-step witness, same labeled carrier inputs feeding transport for any fixed exact field, and how the B record stays fixed. You are supplied the exact scripts and finite list and replay result, and may reason from the independently runnable integer replay. For terminal, calculate the five held minimum edges at witness 17, prove the conditional degree upper and lower bounds, and check permanent positivity failure, the monotone terminal construction and B preservation. For scope, derive the adjacency path count formula for the depth moment from P1, check immediate and delayed decreases 2/100 against the actions, and address exactly which recovery-selection and physical-delivery claims are open. Return the worked calculations regardless of verdict.'

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json",):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()

    response = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    checks = response.get("proof_checks", {})
    topics = ("source_only", "silent_recovery", "terminal", "scope")
    if isinstance(checks, dict):
        paragraphs = [checks.get(topic) for topic in topics]
    elif isinstance(checks, list) and len(checks) == len(topics):
        paragraphs = checks
    else:
        raise ValueError("Expected four worked checks")
    if not all(isinstance(p, str) and len(p.split()) >= 10 for p in paragraphs):
        raise ValueError("The review did not supply four written mathematical checks")
