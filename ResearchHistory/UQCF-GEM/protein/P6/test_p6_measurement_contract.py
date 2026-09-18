import inspect
import unittest

import p6_core as p6
import p6_measurement as measurement


def synthetic_results(*, break_target: str | None = None) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target in p6.TARGET_NAMES:
        for seed in p6.SEEDS:
            values = {
                "physical_real_sequence": 1.0,
                "physical_shuffled_sequence": 0.2,
                "generic_collapse": 0.1,
            }
            if break_target == target:
                values["physical_real_sequence"] = 0.0
                values["generic_collapse"] = 0.1
            for mode in p6.MODES:
                rows.append(
                    {
                        "target": target,
                        "seed": seed,
                        "mode": mode,
                        "topk_native_contact_precision": values[mode],
                        "ca_rmsd_A": 4.0,
                        "rg_ratio": 0.95 if mode == "physical_real_sequence" else 1.0,
                        "max_bond_length_drift_A": 1e-12,
                        "max_bond_angle_drift_rad": 1e-12,
                        "failed": False,
                    }
                )
    return rows


class P6MeasurementContractTests(unittest.TestCase):
    def test_fixed_checkpoints_and_final_budget(self):
        self.assertEqual((0, 50, 100, 200, 300), measurement.CHECKPOINTS)
        self.assertEqual(p6.STEPS, measurement.CHECKPOINTS[-1])

    def test_optimization_loop_does_not_reference_native_coordinates(self):
        source = inspect.getsource(measurement.run_one)
        self.assertNotIn("native_ca", source)
        self.assertNotIn("topk_native_contact_precision", source)
        self.assertNotIn("kabsch_rmsd", source)
        self.assertNotIn("radius_of_gyration", source)

    def test_synthetic_all_conditions_produces_go(self):
        rows = synthetic_results()
        comparisons, acceptance = measurement.adjudicate(rows)
        self.assertEqual(2, len(comparisons))
        self.assertEqual(
            "GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION",
            acceptance["decision"],
        )
        self.assertTrue(all(acceptance["conditions"].values()))

    def test_target_specific_failure_forces_no_go(self):
        rows = synthetic_results(break_target="1UAO")
        _, acceptance = measurement.adjudicate(rows)
        self.assertEqual(
            "NO_GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION",
            acceptance["decision"],
        )
        self.assertFalse(
            acceptance["conditions"]["real_sequence_beats_generic_on_every_target"]
        )

    def test_expected_measurement_cardinality_is_54(self):
        self.assertEqual(
            54,
            len(p6.TARGET_NAMES) * len(p6.SEEDS) * len(p6.MODES),
        )

    def test_firewall_selfcheck_passes(self):
        self.assertTrue(measurement.native_firewall_selfcheck())


if __name__ == "__main__":
    unittest.main()
