"""Challenge the exact native-event menu, the raw receiver trace and its occurrence control."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_COVER_INCREMENT.md": "a52a3a45a97477586a7c1edef0ff851fffa9fc36",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_COVER_INCREMENT_PLAN.md": "259bc86627ebb158c0f3ca602ad1b86901d51b03",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_COVER_WORK_COMPARISON_PLAN.md": "9368c802c092d894cd1a4fba4ea71d7c71ab45eb",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_native_cover_increment.py": "7364b8cdcff5b40b5daf52c04d39d9ca82045681",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/native_cover_increment_certificate.json": "236f51092ee4e1d5fbe0606af16b9c6c7ca4a01a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/geometry_selected_record_certificate.json": "34fa8c957dec8b7433543553abb4c1d57db36b4a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py": "48f132d141167d9cd85ff79ec41720b5dca4f8bb",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/producer.py": "fc4a77fc4f01fce33fdb562423eca274cfb0c648",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/first_response_sector_review/RESULT.md": "af7d1ab985a856971944d1bce8e732677b8ad576",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_saturation/RESULT.md": "fd5a8d17871466da323e8fa28318252906e5e403",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_REACTIVE_RESULT.md": "28e765fb178b5e0f758b1360147b9dd123acbb49"
}

TOPICS = {"cover_proof","preparation","source_and_receiver","delayed_control","physical_scope"}
QUESTION = """Perform an independent adversarial review of NATIVE_COVER_INCREMENT.md.
Use frozen executable definitions and the data. Return REVISE or FAIL for a claim
that does not follow. Return verdict ACCEPTED only if the full scoped finite-fixture
argument survives, with empty arrays findings, counterexamples and missing_assumptions.
Also return limitations (array), native_bridge_status (OPEN if physical delivery or
reading remains open), and proof_checks. proof_checks must have five keys:
cover_proof, preparation, source_and_receiver, delayed_control, physical_scope.
Give at least 15 words of actual reasoning per key. Derive the before and after
minimum cover families after a cut, including the condition for the global h increment.
Explain the count method, what is supplied, which native call executes the claimed
effect, and whether the flag is an instruction to execute. Reconstruct, in words,
both source choices and what exactly becomes private. Challenge the equal-work returns,
the gate on intermediate states, the delay counterexample and what a local observer
would need to read. A global h trace alone need not reveal an indexed record.

Return these exact numeric_checks keys, using integers, integer arrays or strings as specified:
old_legal (count per source arm), old_strict (count per source arm), old_core
(sorted array), new_legal (count per arm), new_strict (count per arm), new_core (sorted),
extra_cuts (count), receiver_calls (array of two [chart,leaf] pairs in source order 718,719),
receiver_retained (two arrays of distinguished leaves actually present at chart 12 after
those calls, same source order), idle_vs_record_h (two endpoint values after work restoration),
delayed (array of [chart,leaf,h_after,number_of_minimum_covers] AFTER the two chart-0 cuts),
intermediate_gates (two raw v15.43 status strings after the single source and then the
strict receiver step), restored_gate (raw status for the two equal-work endpoints).
Do not count the historically supplied preparatory cuts as the source. Distinguish the
supplementary work-return plan, frozen after the initial census, from the original plan.
If a premise is missing from the claimed implication, record it even if the numbers agree."""

if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    data = json.loads(Path(__file__).with_name("native_cover_increment_certificate.json").read_text())
    old = data["states"]["original"]["arms"]["718"]
    newer = data["states"]["reinforced"]
    new = newer["arms"]["718"]
    arms = [newer["arms"][k] for k in ("718","719")]
    returned = new["returned_geometry"]
    expected = {
        "old_legal":old["legal"], "old_strict":len(old["strict"]), "old_core":old["minimum_cover"],
        "new_legal":new["legal"], "new_strict":len(new["strict"]), "new_core":new["minimum_cover"],
        "extra_cuts":len(data["extra"]),
        "receiver_calls":[[a["strict"][0]["editor"],a["strict"][0]["leaf"]] for a in arms],
        "receiver_retained":[a["receiver_sites_after"] for a in arms],
        "idle_vs_record_h":[returned["idle_h"],returned["recording_h"]],
        "delayed":newer["delayed_blind"]["after_common_cuts"],
        "intermediate_gates":[new["source_gate"],new["receiver_gate"]], "restored_gate":returned["both_gate"],
    }
    review = json.loads((Path(sys.argv[2]) / "review.txt").read_text())
    if json.dumps(review.get("numeric_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("Independent cover, ordering or geometry reconstruction disagrees")
