import unittest
import definability_gate as gate

ALLOWED = {
    'NO_TYPED_COMMON_CARRIER',
    'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE',
    'MULTIPLE_NATURAL_RELATIONS_REMAIN',
    'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED',
}


class GateTests(unittest.TestCase):
    def test_real_status_is_preregistered_and_candidate_count_is_four(self):
        result = gate.audit_real_archive()
        self.assertIn(result.status, ALLOWED)
        self.assertEqual(len(result.candidates), 4)

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
