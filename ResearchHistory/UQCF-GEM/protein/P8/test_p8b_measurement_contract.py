from __future__ import annotations

import math
import unittest

import p8b_core as p8b
import p8b_measurement as measurement


def synthetic_results(*, break_control: str | None = None):
    rows = []
    for seed in p8b.SEEDS:
        for mode in p8b.MODES:
            precision = {
                "dynamic_622": 0.90,
                "compaction_only": 0.30,
                "force_gate_only": 0.40,
                "all_lockin_from_start": 0.50,
            }[mode]
            if break_control is not None and mode == break_control:
                precision = 0.95
            rows.append(
                {
                    "seed": seed,
                    "mode": mode,
                    "topk_native_contact_precision": precision,
                    "rg_ratio": 1.0,
                    "max_bond_length_drift_A": 1e-12,
                    "max_bond_angle_drift_rad": 1e-12,
                    "failed": False,
                    "finite": True,
                }
            )
    return rows


class P8BMeasurementContractTests(unittest.TestCase):
    def test_checkpoints_and_primary_controls_are_frozen(self):
        self.assertEqual(measurement.CHECKPOINTS, (0, 50, 100, 250, 500, 1000, 2000))
        self.assertEqual(
            measurement.PRIMARY_CONTROLS,
            ("compaction_only", "force_gate_only", "all_lockin_from_start"),
        )

    def test_exact_sign_flip_with_eight_same_sign_pairs(self):
        p = measurement.exact_sign_flip_p([1.0] * 8)
        self.assertEqual(p, 2 / 256)

    def test_holm_three(self):
        adjusted = measurement.holm_adjust([0.01, 0.02, 0.03])
        self.assertEqual(len(adjusted), 3)
        self.assertTrue(all(0.0 <= p <= 1.0 for p in adjusted))
        self.assertEqual(adjusted, [0.03, 0.04, 0.04])

    def test_synthetic_go_requires_all_frozen_predicates(self):
        _, acceptance = measurement.adjudicate(synthetic_results())
        self.assertEqual(
            acceptance["decision"],
            "GO_PATCH622_CONTROLLER_SIGNAL_ON_PHYSICALLY_CONSTRAINED_1VII",
        )
        self.assertTrue(all(acceptance["conditions"].values()))

    def test_control_failure_forces_no_go(self):
        _, acceptance = measurement.adjudicate(
            synthetic_results(break_control="all_lockin_from_start")
        )
        self.assertEqual(
            acceptance["decision"],
            "NO_GO_PATCH622_CONTROLLER_SIGNAL_ON_PHYSICALLY_CONSTRAINED_1VII",
        )
        self.assertFalse(
            acceptance["conditions"][
                "dynamic_has_highest_mean_primary_precision"
            ]
        )

    def test_rg_failure_forces_no_go(self):
        rows = synthetic_results()
        for row in rows:
            if row["mode"] == "dynamic_622":
                row["rg_ratio"] = 0.70
        _, acceptance = measurement.adjudicate(rows)
        self.assertEqual(
            acceptance["decision"],
            "NO_GO_PATCH622_CONTROLLER_SIGNAL_ON_PHYSICALLY_CONSTRAINED_1VII",
        )
        self.assertFalse(
            acceptance["conditions"]["dynamic_rg_ratio_gate"]
        )

    def test_geometry_or_numerical_failure_forces_no_go(self):
        rows = synthetic_results()
        rows[0]["max_bond_length_drift_A"] = 1e-4
        rows[1]["failed"] = True
        rows[1]["finite"] = False
        _, acceptance = measurement.adjudicate(rows)
        self.assertEqual(
            acceptance["decision"],
            "NO_GO_PATCH622_CONTROLLER_SIGNAL_ON_PHYSICALLY_CONSTRAINED_1VII",
        )
        self.assertFalse(
            acceptance["conditions"]["all_runs_preserve_canonical_geometry"]
        )
        self.assertFalse(
            acceptance["conditions"]["all_runs_numerically_healthy"]
        )

    def test_native_firewall_selfcheck_is_required(self):
        rows = synthetic_results()
        _, acceptance = measurement.adjudicate(
            rows, firewall_override=False
        )
        self.assertFalse(
            acceptance["conditions"]["native_information_firewall_passed"]
        )
        self.assertEqual(
            acceptance["decision"],
            "NO_GO_PATCH622_CONTROLLER_SIGNAL_ON_PHYSICALLY_CONSTRAINED_1VII",
        )


if __name__ == "__main__":
    unittest.main()
