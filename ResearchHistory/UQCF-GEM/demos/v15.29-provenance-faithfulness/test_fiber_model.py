import unittest
import fiber_model as fm


class FiberModelTests(unittest.TestCase):
    def test_face_boundary_shift_preserves_q_exactly(self):
        rep = fm.root_fixture()
        shifted = fm.face_shift(rep, face_index=0, coefficient=3)
        self.assertTrue(fm.same_coarse_source(rep, shifted))
        self.assertNotEqual(rep.edge_vector, shifted.edge_vector)

    def test_general_cycle_shift_preserves_q_exactly(self):
        rep = fm.root_fixture()
        z = fm.canonical_cycle_basis()[7]
        shifted = fm.cycle_shift(rep, z)
        self.assertTrue(fm.same_coarse_source(rep, shifted))

    def test_noncycle_shift_changes_q(self):
        rep = fm.root_fixture()
        bad = list(rep.edge_vector)
        bad[3] += 1
        other = fm.FiberRepresentative(tuple(bad), fm.apply_B1(tuple(bad)))
        self.assertFalse(fm.same_coarse_source(rep, other))


if __name__ == '__main__':
    unittest.main()
