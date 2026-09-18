import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class P7SourceReductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cp = subprocess.run(
            [sys.executable, str(ROOT / "p7_source_reduction.py")],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(cp.stdout)

    def test_source_hashes_are_frozen(self):
        self.assertTrue(self.result["hashes_match_freeze"])

    def test_phase0_is_skipped_before_first_force_application(self):
        self.assertTrue(self.result["initial_exit_triggered_with_source_initial_history"])
        self.assertEqual("Initial_Relaxation", self.result["phase_before_step0_update"])
        self.assertEqual(
            "Coherence_Growth_and_Compaction",
            self.result["phase_after_step0_update"],
        )
        self.assertEqual(0, self.result["phase0_effective_optimizer_steps"])

    def test_fractal_funnel_is_not_a_coordinate_gradient(self):
        self.assertFalse(self.result["fractal_funnel_coordinate_gradient_path"])

    def test_only_late_force_addition_is_contact_springs(self):
        self.assertEqual(
            ["contact_springs"],
            self.result["phase2_minus_phase1"],
        )
        self.assertTrue(
            self.result["only_late_adaptive_force_addition_is_contact_springs"]
        )

    def test_recovered_controller_path_is_native_blind(self):
        self.assertFalse(self.result["dag_mentions_rmsd_or_native"])
        self.assertFalse(self.result["force_field_mentions_rmsd_or_native"])

    def test_verdict(self):
        self.assertEqual(
            "NO_DISTINCT_MULTIFORCE_ADAPTIVE_CONTROLLER_AFTER_SOURCE_REDUCTION",
            self.result["verdict"],
        )


if __name__ == "__main__":
    unittest.main()
