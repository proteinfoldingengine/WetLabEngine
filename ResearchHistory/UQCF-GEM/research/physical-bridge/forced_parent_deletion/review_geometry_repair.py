"""Review the frozen geometric recovery proof."""
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
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_REPAIR.md': 'a72990e589c016edd0b7eb75567738fb361ae1ac',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_REPAIR_CHECK_PLAN.md': '7f2a78217eac25fe96d15fd8ae7c7a9df413957e',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py': '3324c0b46e09120ae526338444a19070b692d049'}
QUESTION = 'Independently challenge this precise geometry-selection theorem and replay, without inferring a physical law. Return JSON with exact verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, native_bridge_status as a string OPEN or DERIVED after reasoning, and proof_checks as four keyed worked paragraphs named rigidity, construction, recovery, output. Your response feeds a strict validator. If you accept the mathematical scope, use verbatim the status fields {"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[]}. Put AFFIRMATIVE observations and successful controls in proof_checks. Use REVISE or FAIL and nonempty objection fields for genuine unresolved objections. Under rigidity prove or refute common minimum after one or two rows change and the two-view separation bound, including the adjacency/opposite argument. Under construction independently reconstruct the cut sum identity, special supports and input positivity. Under recovery reason through every competing index, shorter recovery, union legality and unique receiver address. Under output derive the P1 root change and centered loop check, then address what is supplied about one-deletion geometric recovery, preparation, field, physical actuation and access. The review includes the full checker and its concise replay summary. Return the calculations regardless of verdict.'

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
    topics = ("rigidity", "construction", "recovery", "output")
    if isinstance(checks, dict):
        paragraphs = [checks.get(topic) for topic in topics]
    elif isinstance(checks, list) and len(checks) == len(topics):
        paragraphs = checks
    else:
        raise ValueError("Expected four worked checks")
    if not all(isinstance(p, str) and len(p.split()) >= 10 for p in paragraphs):
        raise ValueError("The review did not supply four written mathematical checks")
