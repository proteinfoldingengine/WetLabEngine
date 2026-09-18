from __future__ import annotations

import math
import unittest

import p8_source_certification as p8


class P8SourceCertificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = p8.build_result()

    def test_frozen_source_hashes(self):
        self.assertTrue(self.result["conditions"]["frozen_source_hashes_verified"])

    def test_patch622_exact_idealized_dag_trace(self):
        d = self.result["p622"]
        self.assertEqual(d["phase_step0"], "Compaction")
        self.assertEqual(d["phase_step98"], "Compaction")
        self.assertEqual(d["phase_step99"], "LockIn")
        self.assertEqual(d["transition_steps"], [99])
        self.assertTrue(d["runner_order"]["betti_history_append_before_dag"])
        self.assertTrue(d["runner_order"]["dag_before_force_loss"])

    def test_patch622_mechanism_is_not_contact_only(self):
        d = self.result["p622"]
        self.assertEqual(
            d["lockin_minus_compaction"],
            ["contact_springs", "screened_electrostatics"],
        )
        self.assertGreater(d["fractal_coordinate_gradient_norm"], 0.0)
        self.assertTrue(math.isfinite(d["fractal_coordinate_gradient_norm"]))
        self.assertGreater(d["electrostatic_coordinate_gradient_norm"], 0.0)
        self.assertTrue(math.isfinite(d["electrostatic_coordinate_gradient_norm"]))

    def test_patch624_extension_and_torsion_path(self):
        d = self.result["p624"]
        self.assertEqual(
            d["lockin_minus_compaction"],
            [
                "contact_springs",
                "screened_electrostatics",
                "torsional_incoherence_penalty",
            ],
        )
        self.assertTrue(d["runner_order"]["phi_rms_detached_to_python_scalar"])
        self.assertTrue(d["torsional_penalty"]["present"])
        self.assertTrue(d["torsional_penalty"]["coordinate_gradient_is_none"])
        self.assertIsNotNone(d["torsional_penalty"]["gamma_gradient"])
        self.assertNotEqual(d["torsional_penalty"]["gamma_gradient"], 0.0)

    def test_source_level_reopen_verdict(self):
        self.assertTrue(all(self.result["conditions"].values()))
        self.assertEqual(
            self.result["verdict"],
            "REOPEN_RULE_SATISFIED_DISTINCT_HISTORICAL_MECHANISM_SOURCE_LEVEL",
        )
        self.assertFalse(self.result["raw_historical_execution_log_recovered"])


if __name__ == "__main__":
    unittest.main()
