"""Submit the pinned source-to-geometry trace through the standing reviewer."""
import hashlib
from pathlib import Path

import review_common_field


DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/V1698_SOURCE_TO_GEOMETRY.md": "d836e0ae5b51f74a1b0fbb715be68cfe9e3554ed",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_v1698_source_to_geometry.py": "c1a07390176bef7cdc697de03d45e4e9a6795be7"
}
QUESTION = """Independently audit the exact historical emitter, archived CSV rows and validator.
Check the dependency of each numerical edge and curvature object on source, support, order
and seed. Reconstruct the two-grid source calculation, the same-seed label intervention,
and the direct transport control's interpretation. Check the distinctions between preserved
raw open cases and the merged direct ledger, identify directional or implicit-inverse caveats,
and inspect whether the historical validator really recomputes rates or consistency from
raw data. Cite exact code fields and state each independent logical scope. Respect V1698.77's
protocol-only freeze and avoid claims about uninspected emitters, native event or physics.
Treat the run and its evidence as supplied data, and do not claim you executed it.
Return one JSON object with exact field types matching this example:
{"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[],"limitations":[],"proof_checks":{},"native_bridge_status":"OPEN"}.
For ACCEPTED, keep the first three issue arrays empty and give substantive string
key-value pairs in proof_checks. Use REVISE or FAIL for actual defects."""
FILES = (
    "v1698_75_emitter.py",
    "v1698_75_validator.py",
    "v1698_77_postmortem.md",
    "original_ledger_rows.json",
    "replay.json",
)


if __name__ == "__main__":
    generated = {}
    for name in FILES:
        target = Path("handoff") / name
        data = target.read_bytes()
        generated[str(target)] = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, **generated}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
