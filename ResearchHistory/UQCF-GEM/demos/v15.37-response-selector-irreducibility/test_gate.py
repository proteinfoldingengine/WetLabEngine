import unittest

from response_selector_irreducibility_gate import audit


class ResponseSelectorIrreducibilityGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_manifest_complete(self):
        self.assertEqual(self.r["candidate_class_count"], 14)
        self.assertEqual(self.r["resolved_candidate_class_count"], 14)
        self.assertEqual(self.r["unresolved_candidate_count"], 0)

    def test_status_partition(self):
        self.assertEqual(self.r["typed_nonselective_count"], 3)
        self.assertEqual(self.r["type_blocked_count"], 4)
        self.assertEqual(self.r["feasibility_not_selector_count"], 2)
        self.assertEqual(self.r["gauge_only_count"], 1)
        self.assertEqual(self.r["irreducible_upstream_count"], 2)
        self.assertEqual(self.r["downstream_circular_prohibited_count"], 1)
        self.assertEqual(self.r["ontology_order_prohibited_count"], 1)

    def test_combined_constraint_rank(self):
        self.assertEqual(self.r["frozen_actual_function_equation_count"], 0)
        self.assertEqual(self.r["combined_frozen_selector_rank"], 0)
        self.assertEqual(self.r["surviving_projective_function_dimension"], 9)
        self.assertTrue(self.r["combination_closure_certified"])

    def test_sensitivity_control(self):
        self.assertEqual(self.r["synthetic_new_axiom_control"], "F_PROPORTIONAL_TO_A")
        self.assertEqual(self.r["synthetic_control_projective_dimension"], 0)
        self.assertFalse(self.r["synthetic_control_is_frozen"])

    def test_adjudication(self):
        self.assertEqual(
            self.r["status"],
            "RESPONSE_FUNCTION_IRREDUCIBLE_RELATIVE_TO_AUDITED_FROZEN_ONTOLOGY",
        )
        self.assertTrue(self.r["branch_stop_relative_to_audited_frozen_ontology"])
        self.assertEqual(
            self.r["next_required_object"],
            "EXPLICIT_NEW_PRETIME_RESPONSE_FUNCTION_AXIOM_OR_NEWLY_DISCOVERED_TYPED_FROZEN_STRUCTURE",
        )

    def test_firewall(self):
        for key in (
            "new_source_semantics_axiom_added",
            "new_response_function_axiom_added",
            "new_representation_link_added",
            "response_function_selected",
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
