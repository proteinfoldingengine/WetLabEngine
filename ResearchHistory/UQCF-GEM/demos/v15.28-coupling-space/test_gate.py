import json
import unittest
import coupling_gate as gate


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


if __name__ == '__main__':
    unittest.main(verbosity=2)
