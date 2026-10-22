from __future__ import annotations

import unittest
from dataclasses import replace

import torch

import p8b_core as p8b
import p8b_measurement as m


def make_fixture(*, controller_ok: bool = True):
    rows = []
    final_by_mode = {
        "recovered_state_gate": 0.80,
        "fixed_step99_lockin": 0.40,
        "static_lockin": 0.30,
        "compaction_only": 0.20,
    }
    for target in p8b.TARGET_NAMES:
        for seed in p8b.SEEDS:
            for mode in p8b.MODES:
                candidate = mode == "recovered_state_gate"
                rows.append(
                    {
                        "target": target,
                        "seed": seed,
                        "mode": mode,
                        "start_topk_native_contact_precision": 0.10,
                        "final_topk_native_contact_precision": final_by_mode[mode],
                        "final_rg_ratio": 1.0,
                        "max_bond_length_drift_A": 1e-12,
                        "max_bond_angle_drift_rad": 1e-12,
                        "failed": False,
                        "failure_reason": "",
                        "final_step": p8b.STEPS,
                        "transitioned_to_lockin": (
                            controller_ok if candidate else False
                        ),
                        "lockin_active_steps": (
                            100 if candidate and controller_ok else 0
                        ),
                    }
                )
    return rows


class P8BMeasurementContractTests(unittest.TestCase):
    def test_run_matrix_is_exactly_72_matched_trajectories(self):
        keys = m.expected_run_keys()
        self.assertEqual(72, len(keys))
        self.assertEqual(72, len(set(keys)))
        self.assertEqual(
            {
                (target, seed, mode)
                for target in p8b.TARGET_NAMES
                for seed in p8b.SEEDS
                for mode in p8b.MODES
            },
            set(keys),
        )

    def test_frozen_checkpoints_and_output_schema(self):
        self.assertEqual((0, 99, 100, 500, 1000, 2000), m.CHECKPOINTS)
        self.assertEqual(
            {
                "p8b_results.csv",
                "p8b_controller_traces.csv",
                "p8b_checkpoint_traces.csv",
                "p8b_summary.csv",
                "p8b_primary_comparisons.csv",
                "p8b_acceptance.json",
                "p8b_run_manifest.json",
                "SHA256SUMS.txt",
            },
            set(m.REQUIRED_OUTPUTS),
        )

    def test_tiny_trajectory_is_native_evaluator_blind(self):
        target = p8b.load_target("1UAO")
        changed = replace(
            target,
            native_ca=target.native_ca * 11.0
            + target.native_ca.new_tensor([31.0, -17.0, 9.0]),
        )
        a = m.simulate_trajectory(
            target,
            seed=2,
            mode="compaction_only",
            step_budget=3,
            collect_trace=False,
        )
        b = m.simulate_trajectory(
            changed,
            seed=2,
            mode="compaction_only",
            step_budget=3,
            collect_trace=False,
        )
        torch.testing.assert_close(
            a["phi_free"], b["phi_free"], rtol=0.0, atol=0.0
        )
        torch.testing.assert_close(
            a["psi"], b["psi"], rtol=0.0, atol=0.0
        )
        self.assertEqual(a["controller_state"], b["controller_state"])

    def test_adjudicator_returns_go_only_when_all_frozen_conditions_pass(self):
        acceptance = m.adjudicate(make_fixture())
        self.assertEqual(
            "GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",
            acceptance["decision"],
        )
        self.assertTrue(all(acceptance["conditions"].values()))
        self.assertEqual(3, len(acceptance["primary_comparisons"]))
        for row in acceptance["primary_comparisons"]:
            self.assertLess(row["holm_adjusted_p"], 0.05)

    def test_controller_use_requirement_is_load_bearing(self):
        acceptance = m.adjudicate(make_fixture(controller_ok=False))
        self.assertEqual(
            "NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",
            acceptance["decision"],
        )
        self.assertFalse(
            acceptance["conditions"][
                "all_candidate_trajectories_exercise_lockin"
            ]
        )

    def test_starting_state_improvement_is_load_bearing(self):
        rows = make_fixture()
        for row in rows:
            if (
                row["target"] == "1L2Y"
                and row["mode"] == "recovered_state_gate"
            ):
                row["start_topk_native_contact_precision"] = 0.90
        acceptance = m.adjudicate(rows)
        self.assertEqual(
            "NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",
            acceptance["decision"],
        )
        self.assertFalse(
            acceptance["conditions"][
                "candidate_improves_from_start_on_every_target"
            ]
        )

    def test_rg_sanity_gate_is_load_bearing(self):
        rows = make_fixture()
        for row in rows:
            if (
                row["target"] == "1VII"
                and row["mode"] == "recovered_state_gate"
            ):
                row["final_rg_ratio"] = 0.70
        acceptance = m.adjudicate(rows)
        self.assertEqual(
            "NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",
            acceptance["decision"],
        )
        self.assertFalse(
            acceptance["conditions"][
                "candidate_rg_ratio_gate_every_target"
            ]
        )

    def test_holm_three_known_case(self):
        adjusted = p8b.holm_three((0.01, 0.04, 0.20))
        self.assertAlmostEqual(0.03, adjusted[0])
        self.assertAlmostEqual(0.08, adjusted[1])
        self.assertAlmostEqual(0.20, adjusted[2])


if __name__ == "__main__":
    unittest.main()
