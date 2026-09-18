import json
from pathlib import Path
import unittest

from source_extension_gate import audit, canonical_json


class SourceExtensionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_inherited_dimensions(self):
        self.assertEqual(self.r["group_order"], 392)
        self.assertEqual(self.r["dim_C1"], 98)
        self.assertEqual(self.r["dim_Q"], 48)
        self.assertEqual(self.r["dim_Z"], 50)
        self.assertEqual(self.r["dim_Y_cyc"], 50)
        self.assertTrue(self.r["group_closure_exact"])
        self.assertTrue(self.r["target_definition_verified"])

    def test_exact_character_dimension(self):
        self.assertEqual(
            self.r["cycle_character_histogram"],
            {"-6": 28, "-2": 49, "0": 98, "1": 216, "50": 1},
        )
        self.assertEqual(self.r["character_square_sum"], 3920)
        self.assertEqual(self.r["dim_Hom_Z_to_Y"], 10)
        self.assertEqual(self.r["hom_dimension_method"], "EXACT_CHARACTER_INNER_PRODUCT")
        self.assertTrue(self.r["character_spotchecks_exact"])

    def test_semisimple_linear_boundary(self):
        self.assertTrue(self.r["rational_semisimplicity_verified"])
        self.assertTrue(self.r["rational_extension_splits"])
        self.assertFalse(self.r["rational_splitting_canonical"])
        self.assertEqual(
            self.r["integral_extension_status"],
            "NOT_ADJUDICATED_WITHOUT_TYPED_INTEGRAL_SOURCE_AXIOM",
        )

    def test_nonunique_early_stop(self):
        self.assertEqual(self.r["status"], "FIBER_EXTENSION_CHANNELS_EXIST_BUT_NONUNIQUE")
        self.assertEqual(self.r["early_stop_reason_or_null"], "DIM_HOM_Z_TO_Y_GT_1")
        self.assertFalse(self.r["unique_projective_fiber_channel"])
        self.assertIsNone(self.r["minimal_kernel_type_count_or_null"])
        self.assertIsNone(self.r["minimal_kernel_types_or_null"])

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed, canonical_json(self.r))
        self.assertEqual(json.loads(committed), self.r)

    def test_claim_firewall(self):
        for key in (
            "new_source_semantics_axiom_added",
            "coupling_solver_reopened",
            "gravity_observables_evaluated",
            "uses_holonomy_selector",
            "uses_newton_or_gr",
            "uses_metric_selector",
            "uses_pruning_as_selector",
            "uses_entropy_as_selector",
            "uses_physical_time",
            "scientific_breakthrough",
            "signal_of_life",
            "physical_gravity_derived",
        ):
            self.assertFalse(self.r[key], key)
        self.assertEqual(self.r["Pillar_3"], "OPEN")


if __name__ == "__main__":
    unittest.main()
