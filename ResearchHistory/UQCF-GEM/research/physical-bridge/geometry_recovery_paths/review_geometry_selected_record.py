"""Challenge the conditional recording law and its two blind controls."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/GEOMETRY_SELECTED_RECORD.md": "5db94e33376a4c904904c2ffc280078cc3544317",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/GEOMETRY_SELECTED_RECORD_PLAN.md": "58f354346abbaec8924bd3881fcc6496f664993f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/GEOMETRY_SELECTED_RECORD_CONTROLS.md": "6c8f04b871fe3774d2731f8cd13e452fe32fe9b5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_geometry_selected_record.py": "711a83fd1e8411e79ac5dd3e3d77d91efe175fee",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_return_pairs.py": "b89d2196f8a1bc2972940e47cf2bbf2e6192b604",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/geometry_selected_record_certificate.json": "34fa8c957dec8b7433543553abb4c1d57db36b4a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_RETAINED_STATE.md": "e9d3dde48d3164240c7c83b23da8a9409c3d836d",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/producer.py": "fc4a77fc4f01fce33fdb562423eca274cfb0c648",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c"
}
TOPICS = {"preparation", "global_minimum", "longer_local", "record", "blind_controls"}
QUESTION = """Independently reconstruct and challenge GEOMETRY_SELECTED_RECORD.md from
the frozen historical tree, certificate and programs. The 134-action common preparation,
the choice of source deletion, and occurrence of globally shortest exact-work returns
are supplied. Test the derivation of the editor, the partner families and the retained
address without granting an editor selection after the source. Test all lengths for
B-only refinements, global versus local shortestness, both crossed controls, sibling
symmetry versus indexed memory, identical work paths, permanence, and whether actual
invocation or physical readout has been earned. Inspect the genuine historical caller
and native atom. Cite a specific failure if there is one.

Return JSON with verdict ACCEPTED, REVISE or FAIL, native_bridge_status, proof_checks,
numeric_checks and the arrays findings, missing_assumptions, counterexamples,
limitations. With ACCEPTED the first three defect arrays must be empty. Use the literal
OPEN if the physical bridge remains open. Each of these five proof_checks must contain
at least 15 words of worked reasoning: preparation, global_minimum, longer_local,
record, blind_controls. Return these exact numeric_checks keys: preparation_edits
(integer), source_leaves (ascending array), source_partner (integer), receiver (integer),
receiver_partners (ascending array), unordered_pair_counts (before source, after restored
source 718, after restored source 719, as one array), protected_leaf_after_each
(array for source 718, then 719), B_roots (before and after the shortest return),
long_blind_length (integer). Use limitations for the assumptions that are explicitly
disclosed. An adverse analytical outcome with a reason is welcome."""

if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    data = json.loads(Path(__file__).with_name("geometry_selected_record_certificate.json").read_bytes())
    xs = sorted(map(int, data["arms"]))
    arms = [data["arms"][str(x)] for x in xs]
    expected = {
        "preparation_edits": data["preparation_edits"],
        "source_leaves": xs,
        "source_partner": data["source_mate"],
        "receiver": arms[0]["minimal_returns"][0][0],
        "receiver_partners": data["unit_mates_at_B"],
        "unordered_pair_counts": [len(data["common_two_step_returns"])]
                                  + [len(arm["minimal_returns"]) for arm in arms],
        "protected_leaf_after_each": [arm["witnesses"][0]["q_present"][0] for arm in arms],
        "B_roots": [data["B_root_before"], arms[0]["witnesses"][0]["root"]],
        "long_blind_length": len(arms[0]["long_return"]["cuts"]),
    }
    verdict = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if json.dumps(verdict.get("numeric_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Independent review values disagree with the scientific replay")
