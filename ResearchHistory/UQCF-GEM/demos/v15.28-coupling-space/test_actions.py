import unittest
import numpy as np
import exact_linear as ql
import representation_actions as actions


class ActionTests(unittest.TestCase):
    def setUp(self):
        self.c = actions.load_frozen_complex(7)
        self.group = actions.torus_automorphisms(7)

    def test_full_group_has_392_elements(self):
        self.assertEqual(len(self.group), 392)
        self.assertEqual(len(set(self.group)), 392)

    def test_boundary_maps_are_exact_chain_maps(self):
        b1 = self.c.B1.astype(int)
        b2 = self.c.B2.astype(int)
        for g in self.group:
            p0 = actions.vertex_action(self.c, g).matrix_int()
            p1 = actions.edge_action(self.c, g).matrix_int()
            p2 = actions.face_action(self.c, g).matrix_int()
            np.testing.assert_array_equal(p0 @ b1, b1 @ p1)
            np.testing.assert_array_equal(p1 @ b2, b2 @ p2)

    def test_source_and_cycle_dimensions(self):
        source = actions.augmentation_basis(len(self.c.vertices))
        cycle = actions.cycle_basis_exact(self.c.B1.astype(int))
        self.assertEqual(len(source.columns), 48)
        self.assertEqual(len(cycle.columns), 50)

    def test_restricted_identity_is_identity(self):
        identity_g = next(g for g in self.group
                          if g.matrix == ((1,0),(0,1)) and g.translation == (0,0))
        source = actions.augmentation_basis(len(self.c.vertices))
        cycle = actions.cycle_basis_exact(self.c.B1.astype(int))
        self.assertEqual(actions.restricted_representation(source, actions.vertex_action(self.c, identity_g)), ql.identity(48))
        self.assertEqual(actions.restricted_representation(cycle, actions.edge_action(self.c, identity_g)), ql.identity(50))

    def test_group_composition_matches_vertex_and_edge_actions(self):
        samples = [self.group[i] for i in (0,1,7,49,100,211,391)]
        for a, b in zip(samples, samples[1:]):
            c = a.compose(b)
            self.assertEqual(actions.vertex_action(self.c, c),
                             actions.vertex_action(self.c, a).compose(actions.vertex_action(self.c, b)))
            self.assertEqual(actions.edge_action(self.c, c),
                             actions.edge_action(self.c, a).compose(actions.edge_action(self.c, b)))

    def test_baseline_blob_is_frozen(self):
        self.assertEqual(actions.verify_baseline(),
                         '99110f943550751645539c0c8a7339024d7fefd3')


if __name__ == '__main__':
    unittest.main(verbosity=2)
