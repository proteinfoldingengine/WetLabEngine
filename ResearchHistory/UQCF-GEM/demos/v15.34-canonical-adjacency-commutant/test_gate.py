import unittest

from canonical_adjacency_gate import audit


class CanonicalAdjacencyGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_basic_structure(self):
        self.assertEqual(self.r["group_order"], 392)
        self.assertEqual(self.r["dim_Z"], 50)
        self.assertEqual(self.r["commutant_dimension"], 10)
        self.assertTrue(self.r["adjacency_preserves_Z"])
        self.assertTrue(self.r["all_group_commutators_zero"])
        self.assertTrue(self.r["primitive_translation_sum_D4_invariant"])

    def test_minimal_polynomial(self):
        self.assertEqual(self.r["minimal_polynomial_degree"], 10)
        self.assertEqual(
            self.r["minimal_polynomial_factors"],
            [
                [1, -4],
                [1, -5, 6, -1],
                [1, 2, -8, -8],
                [1, 2, -1, -1],
            ],
        )
        self.assertTrue(self.r["minimal_polynomial_annihilates_Z"])
        self.assertTrue(self.r["all_proper_factor_omissions_fail"])

    def test_commutant_generation(self):
        self.assertEqual(self.r["power_span_rank"], 10)
        self.assertTrue(self.r["full_commutant_generated_by_adjacency"])
        self.assertEqual(self.r["rational_factor_degrees"], [1, 3, 3, 3])
        self.assertEqual(self.r["splitting_field_sector_count"], 10)

    def test_adjudication(self):
        self.assertEqual(
            self.r["status"],
            "FULL_COMMUTANT_GENERATED_BY_CANONICAL_ADJACENCY_FUNCTION_UNSELECTED",
        )
        self.assertFalse(self.r["adjacency_function_selected"])
        self.assertEqual(
            self.r["next_required_object"],
            "TARGET_BLIND_PRINCIPLE_SELECTING_FUNCTION_OF_CANONICAL_ADJACENCY_OR_EXPLICIT_NEW_AXIOM",
        )

    def test_firewall(self):
        for key in (
            "new_source_semantics_axiom_added",
            "new_sector_weight_selector_added",
            "adjacency_function_selected",
            "low_degree_locality_assumed",
            "coupling_solver_reopened",
            "gravity_observables_evaluated",
            "uses_holonomy_selector",
            "uses_newton_or_gr",
            "uses_metric_selector",
            "uses_pruning_as_selector",
            "uses_entropy_as_selector",
            "uses_physical_time",
            "physical_gravity_derived",
            "scientific_breakthrough",
            "signal_of_life",
        ):
            self.assertFalse(self.r[key], key)
        self.assertEqual(self.r["Pillar_3"], "OPEN")


if __name__ == "__main__":
    unittest.main()
