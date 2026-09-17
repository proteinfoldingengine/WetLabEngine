import unittest
import exact_fiber as ef


class ExactFiberTests(unittest.TestCase):
    def test_face_shift_is_distinct_and_same_q(self):
        root, face, cycle = ef.canonical_fiber_cases()
        self.assertNotEqual(root.edge_vector, face.edge_vector)
        self.assertTrue(ef.same_q_exact(root, face))

    def test_cycle_shift_is_distinct_and_same_q(self):
        root, face, cycle = ef.canonical_fiber_cases()
        self.assertNotEqual(root.edge_vector, cycle.edge_vector)
        self.assertTrue(ef.same_q_exact(root, cycle))

    def test_noncycle_shift_changes_q(self):
        root = ef.canonical_fiber_cases()[0]
        self.assertFalse(ef.noncycle_control_preserves_q(root, edge_index=3))

    def test_q_only_label_collapses_entire_fiber(self):
        labels = ef.evaluate_labeling_on_fiber(lambda case: case.q)
        self.assertEqual(len(set(labels)), 1)


if __name__ == '__main__':
    unittest.main()
