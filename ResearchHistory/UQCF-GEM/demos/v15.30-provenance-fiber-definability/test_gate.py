import unittest
import definability_gate as gate

ALLOWED = {
    'NO_TYPED_COMMON_CARRIER',
    'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE',
    'MULTIPLE_NATURAL_RELATIONS_REMAIN',
    'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED',
}

REQUIRED = {
    'version', 'base_sha', 'status', 'candidate_count', 'candidate_results',
    'common_carrier_count', 'exact_fiber_relation_count', 'natural_relation_count',
    'countermodels_survive', 'canonical_relation_certified',
    'new_source_semantics_axiom_added', 'coupling_solver_reopened',
    'gravity_observables_evaluated', 'uses_holonomy_selector', 'uses_newton_or_gr',
    'uses_metric_selector', 'uses_pruning_as_selector', 'uses_entropy_as_selector',
    'uses_physical_time', 'scientific_breakthrough', 'signal_of_life',
    'gravity_canary_certified', 'physical_gravity_derived', 'Pillar_3',
    'next_required_object',
}


class GateTests(unittest.TestCase):
    def test_ledger_schema_and_claim_boundary(self):
        result = gate.audit()
        self.assertEqual(set(result), REQUIRED)
        self.assertIn(result['status'], ALLOWED)
        self.assertEqual(result['candidate_count'], 4)
        for key in (
            'new_source_semantics_axiom_added', 'coupling_solver_reopened',
            'gravity_observables_evaluated', 'uses_holonomy_selector',
            'uses_newton_or_gr', 'uses_metric_selector', 'uses_pruning_as_selector',
            'uses_entropy_as_selector', 'uses_physical_time', 'signal_of_life',
            'gravity_canary_certified', 'physical_gravity_derived',
        ):
            self.assertFalse(result[key])
        self.assertEqual(result['Pillar_3'], 'OPEN')
        self.assertEqual(
            result['scientific_breakthrough'],
            result['status'] == 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED',
        )

    def test_no_common_carrier_has_highest_precedence(self):
        result = gate.synthetic_no_common_carrier_control()
        self.assertEqual(result.status, 'NO_TYPED_COMMON_CARRIER')

    def test_global_multiple_relations_outrank_positive_candidate(self):
        result = gate.synthetic_cross_candidate_multiple_control()
        self.assertEqual(result.status, 'MULTIPLE_NATURAL_RELATIONS_REMAIN')

    def test_unique_synthetic_control_can_reach_positive_status(self):
        result = gate.synthetic_unique_natural_control()
        self.assertEqual(result.status, 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED')
        self.assertTrue(result.canonical_relation_certified)

    def test_supplied_embedding_control_never_certifies_real_relation(self):
        result = gate.synthetic_supplied_embedding_control()
        self.assertNotEqual(result.status, 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED')


if __name__ == '__main__':
    unittest.main()
