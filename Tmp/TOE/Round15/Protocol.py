from pathlib import Path
import json

protocol = {
    "challenge": "15",
    "name": "skeptics_challenge_cluster_lensing_stress_test",
    "frozen_from": "Challenge 14 closeout",
    "rules": {
        "retuning_allowed": False,
        "new_parameters_allowed": False,
        "new_selector_logic_allowed": False,
        "dark_component_added_by_hand": False,
        "post_hoc_cluster_specific_fixes": False
    },
    "tiers": {
        "tier_1_relaxed_clusters": {
            "goal": "test frozen scaffold against cluster-scale radial mass/lensing structure",
            "required_inputs": [
                "gas_map_or_profile",
                "reference_total_mass_or_lensing_profile"
            ]
        },
        "tier_2_merging_clusters": {
            "goal": "test frozen scaffold on merger-offset systems",
            "required_inputs": [
                "gas_map_or_profile",
                "reference_lensing_or_mass_map",
                "merger_system"
            ]
        }
    },
    "outputs": [
        "locked_sample.csv",
        "per_system_summary.csv",
        "aggregate_summary.json",
        "top_gain_audit.csv",
        "top_failure_audit.csv",
        "challenge15_closeout_memo.md"
    ],
    "success_logic": {
        "positive_signal_required": True,
        "catastrophic_failures_should_be_zero_or_bounded": True,
        "worst_case_audit_required": True,
        "public_precommit_required": True
    }
}

out = Path("/content/challenge15_precommit_protocol.json")
out.write_text(json.dumps(protocol, indent=2))
print(f"Saved: {out}")
print(json.dumps(protocol, indent=2))
