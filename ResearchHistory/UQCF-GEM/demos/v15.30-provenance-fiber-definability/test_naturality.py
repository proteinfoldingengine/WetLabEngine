import unittest
import naturality as nat


class NaturalityTests(unittest.TestCase):
    def test_swap_preserving_reduct_rejects_noninvariant_relation(self):
        relation, action = nat.synthetic_swap_counterexample()
        result = nat.audit_relation_naturality(relation, action)
        self.assertFalse(result.certified)
        self.assertFalse(result.equivariant)

    def test_equivariant_synthetic_relation_passes(self):
        relation, action = nat.synthetic_equivariant_control()
        result = nat.audit_relation_naturality(relation, action)
        self.assertTrue(result.certified)
        self.assertTrue(result.group_law_exact)
        self.assertTrue(result.equivariant)

    def test_missing_certified_action_fails_closed(self):
        relation, action = nat.synthetic_equivariant_control()
        result = nat.audit_relation_naturality(relation, None)
        self.assertFalse(result.certified)
        self.assertEqual(result.reason, 'NO_CERTIFIED_ACTION_FOR_DEFINABILITY')

    def test_group_law_checked_exactly_for_finite_control(self):
        relation, action = nat.synthetic_equivariant_control()
        self.assertTrue(nat.check_group_law(action))
        broken = nat.break_multiplication_table(action)
        self.assertFalse(nat.check_group_law(broken))


if __name__ == '__main__':
    unittest.main()
