import unittest

from support_radius_locality_gate import audit


class SupportRadiusLocalityGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_orbit_basis(self):
        self.assertEqual(self.r["displacement_orbit_count"], 10)
        self.assertEqual(self.r["displacement_orbit_size_sum"], 49)
        self.assertEqual(self.r["orbit_basis_rank"], 10)
        self.assertTrue(self.r["orbit_polynomial_reconstruction_exact"])
        self.assertEqual(self.r["orbit_to_power_change_rank"], 10)

    def test_support_radius_filtration(self):
        self.assertEqual(
            self.r["support_radius_dimensions"],
            {"0":1,"1":2,"2":4,"3":6,"4":8,"5":9,"6":10},
        )
        self.assertEqual(
            self.r["support_radius_projective_dimensions"],
            {"0":0,"1":1,"2":3,"3":5,"4":7,"5":8,"6":9},
        )

    def test_degree_is_not_radius(self):
        self.assertEqual(
            self.r["polynomial_degree_filtration_dimensions"],
            {"0":1,"1":2,"2":3,"3":4,"4":5,"5":6,"6":7,"7":8,"8":9,"9":10},
        )
        self.assertFalse(self.r["support_radius_equals_polynomial_degree_filtration"])
        self.assertEqual(self.r["first_radius_degree_mismatch"], 2)

    def test_frozen_locality_audit(self):
        self.assertIsNone(self.r["frozen_hard_radius_selected"])
        self.assertEqual(self.r["frozen_hard_radius_constraint_count"], 0)
        self.assertEqual(self.r["surviving_response_dimension"], 10)
        self.assertEqual(self.r["surviving_projective_response_dimension"], 9)
        self.assertEqual(self.r["unresolved_locality_typing_count"], 0)

    def test_adjudication(self):
        self.assertEqual(
            self.r["status"],
            "CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED",
        )
        self.assertEqual(
            self.r["next_required_object"],
            "TARGET_BLIND_TYPED_CONSTRAINT_ON_ADJACENCY_RESPONSE_FUNCTION_OR_EXPLICIT_PRETIME_RESPONSE_FUNCTION_AXIOM",
        )

    def test_firewall(self):
        for key in (
            "new_source_semantics_axiom_added",
            "new_locality_axiom_added",
            "hard_radius_selected",
            "polynomial_degree_selected",
            "adjacency_function_selected",
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
