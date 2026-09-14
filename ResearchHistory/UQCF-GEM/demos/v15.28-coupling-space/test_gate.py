import json
import unittest
import coupling_gate as gate
import representation_inventory as inv


class GateTests(unittest.TestCase):
    def test_q_baseline_orbit_and_character_dimensions_agree(self):
        r = gate.q_baseline_audit()
        self.assertEqual(r.dimension, r.orbit_dimension)
        self.assertEqual(r.dimension, r.character_dimension)

    def test_q_basis_maps_are_exactly_cycle_valued_and_quotient_safe(self):
        r = gate.q_baseline_audit()
        for k in r.ambient_basis:
            self.assertTrue(gate.matrix_is_zero(gate.left_multiply_B1(k)))
            self.assertTrue(gate.vector_is_zero(gate.apply_to_constant(k)))

    def test_q_baseline_schema_has_no_gravity_scores(self):
        text = json.dumps(gate.q_baseline_audit().as_dict()).lower()
        for forbidden in ('holonomy','newton','einstein','inverse_square','distance_score'):
            self.assertNotIn(forbidden, text)

    def test_genesis_field_does_not_get_arbitrary_embedding(self):
        r = gate.audit_candidate(inv.by_key('genesis-6d-field'))
        self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
        self.assertIsNone(r.dimension)

    def test_retained_graph_source_current_stays_blocked_without_label_bridge(self):
        r = gate.audit_candidate(inv.by_key('retained-graph-source-current'))
        self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
        self.assertIsNone(r.dimension)

    def test_v1404_supplied_intertwiner_remains_conditional(self):
        r = gate.audit_candidate(inv.by_key('v14.04-supplied-intertwiner-control'))
        self.assertEqual(r.status, 'CONDITIONAL_ON_SUPPLIED_INTERTWINER')
        self.assertIsNone(r.dimension)

    def test_only_q_control_is_currently_solver_eligible(self):
        rows = inv.frozen_inventory(inv.REPO_ROOT)
        self.assertEqual([r.key for r in inv.eligible_records(rows)], ['source-quotient-q-control'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
