"""Read back the independent challenge of coverage, work and receiver ownership."""
from pathlib import Path
import json
import sys

from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_RECEIVER_VETO.md": "bec8104c6e3b867dd8819358f4c7d7edecfdfe00",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_RECEIVER_VETO_PLAN.md": "75072e18683ada2115c21fc215ea59b9f3187f15",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_RECEIVER_VETO_GEOMETRY_PLAN.md": "02bb503fa7cc4d461d98a181d314ce2e58247b44",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_RECEIVER_OWNER_PLAN.md": "b3ec7589e84c34733feb0a2939e149ac25735649",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_native_receiver_veto.py": "4678edf257886351677134998bed6357591c2761",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_veto_owner.py": "9975de14dad92da6082d940a0e9e7ad8e4ef3c69",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_receiver_command.py": "ea473508b86f080c57750c19f41870a85270b3e7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/native_receiver_veto_certificate.json": "fe6597fbe42ef5f0738ce0f576014932ac7c3bee",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_owner_certificate.json": "72a0d62db1012b66a65ea834ca5f3d12c68a59ae",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/ODD_SOURCE_ROOT_RECORD.md": "c5d7c525cdf8d5fd0cd0300fbb58bdc37e384bca",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_move_interface/RESULT.md": "0371d4a8aa66ce02ffbda084ad5dde93f1ec1136",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/source_enabled_record/RESULT.md": "b63d70a7636146e34ef54970461c6bbfab9b1df8"
}
TOPICS = {"coverage", "geometry", "minimum", "control", "scope"}
QUESTION = """Challenge the complete frozen manuscript NATIVE_RECEIVER_VETO.md against its exact
code, controls and prior coverage result. Do not presume acceptance. Work through the fixed
preparation and check the mathematical and causal quantifiers. Return a JSON object with
verdict ACCEPTED, REVISE or FAIL; arrays findings, missing_assumptions, counterexamples,
limitations; native_bridge_status; and objects proof_checks and numeric_checks. Put only
unresolved substantive defects in the first three arrays; these must be [] for acceptance.
Put accepted supporting observations in proof_checks and scope conditions in limitations.
Use literal string OPEN for native_bridge_status if physical actuation/access is open.
proof_checks keys must be exactly coverage, geometry, minimum, control, scope, each with
at least 15 words of reasoning. Under coverage check the sign in the work identity, all
nonsource command losses, and whether a receiving label was logically inferred or physically
chosen. Under geometry reconstruct the complementary cut supports and check which full
carriers actually pass before and immediately after the events. Under minimum prove or
challenge both lower bounds with their precise hypotheses. Under control distinguish
the baseline states, both unit events, the matched non-isolated and two-unit controls, and
the difference between an exception and a returned unchanged state. Under scope distinguish
the original fixture from the new common preparation, the old coverage mechanism from the
geometric contribution, and mathematical availability from a lasting physical readout.
Be precise about the condition under which all possible other commands are classified.
In numeric_checks give your values with exactly these entries. leaf_ids is an array [p,q,r].
prep_costs is [unconstrained minimum, minimum for q with untouched B and admitted endpoint].
changed_pairs is [original, isolated, balanced] compared to the initial 300. balanced_B_menu
is [before source, after p, after q]. pair_work is [before, after p, after q] in the
balanced preparation. positive_labels_q lists all nonsource positive labels on the balanced
q-event. returns is [B root returned by identical q probe after source p, result after
source q as JSON null if no state returns]. original_probes gives the two literal status
strings after p and q at original unreduced cover. nonsource_menus is the integer number of
whole menus compared. Only use the source evidence. If a claim fails state the counterexample
or needed repair rather than conforming to the author's prediction."""

if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    directory = Path(__file__).resolve().parent
    primary = json.loads((directory / "native_receiver_veto_certificate.json").read_bytes())
    all_menus = json.loads((directory / "receiver_owner_certificate.json").read_bytes())
    original, balanced = (primary["arms"][k] for k in ("original", "balanced"))
    p, q = (str(primary[k]) for k in ("p","q"))
    arms = balanced["source_arms"]
    expected = {
        "leaf_ids": [primary[k] for k in ("p","q","r")],
        "prep_costs": [primary["first_bound"], primary["balanced_bound_unit_untouched_B"]],
        "changed_pairs": [primary["arms"][k]["changed_work_pairs"] for k in ("original","isolated","balanced")],
        "balanced_B_menu": [balanced["B_menu_size"],arms[p]["B_menu_size"],arms[q]["B_menu_size"]],
        "pair_work": [balanced["work_AB"],arms[p]["work_AB"],arms[q]["work_AB"]],
        "positive_labels_q": all_menus["comparisons"]["balanced"][q]["positive_labels"],
        "returns": [arms[p]["probe_returned_B_root"],arms[q]["probe_returned_B_root"]],
        "original_probes": [original["source_arms"][k]["probe"] for k in (p,q)],
        "nonsource_menus": all_menus["nonsource_menus_compared"],
    }
    result = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if json.dumps(result.get("numeric_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Reviewer values disagree with the native trials")
