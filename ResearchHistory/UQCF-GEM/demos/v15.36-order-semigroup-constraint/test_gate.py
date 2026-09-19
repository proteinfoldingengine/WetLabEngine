import json
from pathlib import Path
import unittest

from order_semigroup_gate import audit, canonical_json


class OrderSemigroupGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_semigroup_nonselection(self):
        self.assertEqual(self.r["sector_count"], 10)
        self.assertEqual(self.r["continuous_semigroup_generator_dimension"], 10)
        self.assertEqual(self.r["projective_relative_generator_dimension"], 9)
        self.assertEqual(self.r["exact_rational_semigroup_witness_count"], 5)
        self.assertEqual(self.r["projectively_distinct_semigroup_witness_count"], 5)
        self.assertTrue(self.r["all_exact_semigroup_composition_checks_pass"])

    def test_positive_and_contractive_controls(self):
        self.assertEqual(self.r["positive_cone_affine_dimension"], 10)
        self.assertEqual(self.r["positive_projective_dimension"], 9)
        self.assertEqual(self.r["nonpositive_generator_cone_affine_dimension"], 10)
        self.assertFalse(self.r["sectorwise_positivity_is_frozen_physical_order_law"])
        self.assertFalse(self.r["contractive_semigroup_is_frozen_physical_law"])

    def test_frozen_typing(self):
        self.assertEqual(self.r["nonselective_frozen_family_closure_count"], 1)
        self.assertEqual(self.r["type_blocked_frozen_candidate_count"], 4)
        self.assertEqual(self.r["unresolved_typing_count"], 0)
        self.assertEqual(self.r["frozen_actual_function_equation_count"], 0)
        self.assertEqual(self.r["frozen_function_constraint_rank"], 0)
        self.assertEqual(self.r["surviving_projective_function_dimension"], 9)

    def test_adjudication(self):
        self.assertEqual(self.r["status"],"FROZEN_ORDER_SEMIGROUP_CONSTRAINTS_LEAVE_FUNCTION_UNSELECTED")
        self.assertEqual(self.r["next_required_object"],"NEW_TYPED_PRETIME_RESPONSE_PRINCIPLE_OR_EXPLICIT_RESPONSE_FUNCTION_AXIOM")

    def test_committed_ledger_is_exact(self):
        committed=Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed,canonical_json(self.r))
        self.assertEqual(json.loads(committed),self.r)

    def test_firewall(self):
        for key in (
            "new_source_semantics_axiom_added","new_order_axiom_added","new_semigroup_axiom_added",
            "response_generator_selected","adjacency_function_selected","coupling_solver_reopened",
            "gravity_observables_evaluated","uses_holonomy_selector","uses_newton_or_gr",
            "uses_metric_selector","uses_pruning_as_selector","uses_entropy_as_selector",
            "uses_physical_time","physical_gravity_derived","scientific_breakthrough","signal_of_life",
        ):
            self.assertFalse(self.r[key],key)
        self.assertEqual(self.r["Pillar_3"],"OPEN")


if __name__=="__main__":
    unittest.main()
