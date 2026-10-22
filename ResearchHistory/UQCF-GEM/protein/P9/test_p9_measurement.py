from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import p9_core as p9
import p9_measurement as measurement


def test_measurement_contract_is_bound_to_frozen_source_manifest():
    payload = json.loads(measurement.SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert payload["schema"] == "protein-p9-source-manifest-v1"
    assert payload["core_green"]["implementation_head"] == (
        "b4573dd46436adc36fd7b957b4f546bdf0f00079"
    )
    assert payload["native_result_exposed"] is False
    assert measurement.EXPECTED_SOURCE_MANIFEST_GIT_BLOB == (
        "16ab23c9405b371af6886cf034e79370c54359bc"
    )


def test_measurement_matrix_and_outputs_are_frozen():
    assert measurement.expected_run_keys() == p9.expected_state_keys()
    assert len(measurement.expected_run_keys()) == 96
    assert measurement.REQUIRED_OUTPUTS == (
        "p9_results.csv",
        "p9_group_correlations.csv",
        "p9_primary_comparisons.csv",
        "p9_summary.csv",
        "p9_acceptance.json",
        "p9_run_manifest.json",
        "SHA256SUMS.txt",
    )


def test_run_manifest_is_outcome_blind_and_protocol_complete():
    manifest = measurement.build_run_manifest(git_head="TEST_HEAD")
    assert manifest["schema"] == "protein-p9-measurement-v1"
    assert manifest["git_head"] == "TEST_HEAD"
    assert manifest["source_manifest_commit"] == (
        "0f723410c39ba4fe03471720ec59d5acfc0c1fc3"
    )
    assert manifest["core_green_head"] == (
        "b4573dd46436adc36fd7b957b4f546bdf0f00079"
    )
    assert manifest["targets"] == list(p9.TARGET_NAMES)
    assert manifest["seeds"] == list(p9.SEEDS)
    assert manifest["checkpoints"] == list(p9.CHECKPOINTS)
    assert manifest["generator_steps"] == p9.GENERATOR_STEPS
    assert manifest["handoff_steps"] == p9.HANDOFF_STEPS
    assert manifest["v9_used_as_force"] is False
    assert manifest["native_information_used_in_dynamics"] is False


def test_secondary_group_correlations_are_pure_analysis():
    rows = p9.synthetic_acceptance_fixture(go=True)
    groups = measurement.all_observable_group_correlations(rows)
    assert len(groups) == 16
    first = groups[0]
    assert first["target"] in p9.TARGET_NAMES
    assert first["checkpoint"] in p9.CHECKPOINTS
    assert "spearman_closure_ready" in first


def test_csv_and_hash_packet_writer(tmp_path):
    measurement.write_csv(
        tmp_path / "x.csv",
        [{"a": 1, "b": 2}, {"a": 3, "b": 4}],
    )
    assert (tmp_path / "x.csv").read_text(encoding="utf-8").splitlines()[0] == "a,b"
    (tmp_path / "a.txt").write_text("alpha\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text("beta\n", encoding="utf-8")
    measurement.write_sha256sums(
        tmp_path,
        names=("a.txt", "b.txt"),
    )
    sums = (tmp_path / "SHA256SUMS.txt").read_text(encoding="utf-8")
    assert "a.txt" in sums
    assert "b.txt" in sums
