"""Ask the standing independent reviewer to adjudicate the frozen argument."""
import hashlib
from pathlib import Path

import review_common_field


DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/PRUNING_COMPATIBLE_PATCH.md": "4b8735068ed36396f64c6e2188606304fcaa7ed7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_pruning_compatible_patch.py": "e578f59f1d7ab93eceb169cf6d2b97e0fb982b4e",
    "ResearchHistory/UQCF-GEM/demos/v16.41-unit-barrier-dichotomy/producer.py": "0ba44accc8f47359a8e5adfa9b6a5265dc3eb45d",
    "ResearchHistory/UQCF-GEM/demos/v16.41-unit-barrier-dichotomy/verifier.py": "079b2189d4d06e583eeafd25860c2dba33ede673",
    "ResearchHistory/UQCF-GEM/demos/v16.42-overlapping-core-repair/producer.py": "980d34ec76370c2f220d29c1650ea8e010ce75a4",
    "ResearchHistory/UQCF-GEM/demos/v16.42-overlapping-core-repair/verifier.py": "3ed004d6748e36e72f765a22b5533ec187e954f9",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/v1712_rg.py": "bc4504edbde3bc35815959f7f52288a57dced81a",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/v1713_shape_rg.py": "db8828f17a1ae597ac09abc1a8ac23b3eb3b6676",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4"
}
QUESTION = """Review the complete argument against the original software and the inherited maps.
Derive both necessity and converse for P1 and for P1 plus the zero-section conditions,
and reconstruct the parameter counts on the three pinned carriers. Check that the replay
constructs the independent constraints in raw grades, the named original mask reads and
the matched source projections. Independently derive the basis image and the unrestricted
right-grade erasure. Audit the quantified domains and the relation to historical software.
Specifically challenge any overstatement about a physical coupling or receiver access.
The fixture is a matched common-port diagnostic, not an original geometry caller in v16.42.
The replay is provided as evidence. Do not claim you executed it.
Return only one JSON object with exactly typed fields as in this example:
{"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[],"limitations":[],"proof_checks":{},"native_bridge_status":"OPEN"}.
For ACCEPTED keep the first three issue arrays empty. Give substantive calculations as
string key-value pairs in proof_checks. Reject real defects with REVISE or FAIL.
"""


if __name__ == "__main__":
    replay = Path("handoff/replay.json")
    data = replay.read_bytes()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, str(replay): blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
