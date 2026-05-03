from pathlib import Path
import pandas as pd
import json
from hashlib import sha256

OUTDIR = Path("/content/challenge15_locked_sample")
OUTDIR.mkdir(parents=True, exist_ok=True)

locked_sample = pd.DataFrame([
    {
        "tier": "tier_1_relaxed",
        "system_name": "Abell 1689",
        "system_type": "relaxed_cluster",
        "primary_observable": "radial_mass_lensing_profile",
        "gas_data_expected": "xray_gas_profile_or_map",
        "reference_mass_expected": "strong_plus_weak_lensing_profile",
        "must_include_offset_test": False,
        "notes": "Relaxed reference cluster"
    },
    {
        "tier": "tier_1_relaxed",
        "system_name": "Abell 1835",
        "system_type": "relaxed_cluster",
        "primary_observable": "radial_mass_lensing_profile",
        "gas_data_expected": "xray_gas_profile_or_map",
        "reference_mass_expected": "lensing_or_hydrostatic_profile",
        "must_include_offset_test": False,
        "notes": "Relaxed reference cluster"
    },
    {
        "tier": "tier_1_relaxed",
        "system_name": "Abell 2261",
        "system_type": "relaxed_cluster",
        "primary_observable": "radial_mass_lensing_profile",
        "gas_data_expected": "xray_gas_profile_or_map",
        "reference_mass_expected": "lensing_profile",
        "must_include_offset_test": False,
        "notes": "Relaxed reference cluster"
    },
    {
        "tier": "tier_2_merger",
        "system_name": "1E 0657-56 (Bullet Cluster)",
        "system_type": "merging_cluster",
        "primary_observable": "gas_mass_lensing_offset",
        "gas_data_expected": "xray_gas_map",
        "reference_mass_expected": "weak_plus_strong_lensing_mass_map",
        "must_include_offset_test": True,
        "notes": "Canonical skeptic stress test"
    },
    {
        "tier": "tier_2_merger",
        "system_name": "MACS J0025.4-1222",
        "system_type": "merging_cluster",
        "primary_observable": "gas_mass_lensing_offset",
        "gas_data_expected": "xray_gas_map",
        "reference_mass_expected": "lensing_mass_map",
        "must_include_offset_test": True,
        "notes": "Bullet-like merger analog"
    },
    {
        "tier": "tier_2_merger",
        "system_name": "Abell 2744",
        "system_type": "merging_cluster",
        "primary_observable": "gas_mass_lensing_offset",
        "gas_data_expected": "xray_gas_map",
        "reference_mass_expected": "lensing_mass_map",
        "must_include_offset_test": True,
        "notes": "Complex merger stress test"
    },
])

locked_csv = OUTDIR / "challenge15_locked_sample.csv"
locked_sample.to_csv(locked_csv, index=False)

protocol = {
    "challenge": 15,
    "name": "skeptics_challenge_cluster_lensing_stress_test",
    "frozen_from": "Challenge 14 closeout",
    "rules": {
        "retuning_allowed": False,
        "new_parameters_allowed": False,
        "new_selector_logic_allowed": False,
        "dark_component_added_by_hand": False,
        "post_hoc_cluster_specific_fixes": False
    },
    "success_criteria": {
        "profile_fit_required": True,
        "offset_test_required_for_mergers": True,
        "zero_catastrophic_failures_required": True,
        "worst_case_audit_required": True
    },
    "sample_file": str(locked_csv),
    "n_systems": int(len(locked_sample))
}

protocol_path = OUTDIR / "challenge15_precommit_protocol.json"
protocol_path.write_text(json.dumps(protocol, indent=2))

# simple commit hash for the locked packet
digest = sha256()
digest.update(locked_csv.read_bytes())
digest.update(protocol_path.read_bytes())
hash_path = OUTDIR / "challenge15_precommit_sha256.txt"
hash_path.write_text(digest.hexdigest() + "\n")

print("Saved:")
print(locked_csv)
print(protocol_path)
print(hash_path)
print("\nLocked sample:")
print(locked_sample.to_string(index=False))
print("\nPrecommit SHA256:")
print(digest.hexdigest())
