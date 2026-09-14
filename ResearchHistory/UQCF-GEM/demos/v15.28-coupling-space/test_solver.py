import unittest
import exact_linear as ql
import coupling_solver as solver


class SolverTests(unittest.TestCase):
    def test_d0_sign_mismatch(self):
        self.assertEqual(solver.solve_exact_intertwiners(
            solver.synthetic_c2_sign_mismatch()).dimension, 0)

    def test_d1_identical_sign_irrep(self):
        self.assertEqual(solver.solve_exact_intertwiners(
            solver.synthetic_c2_identical_sign()).dimension, 1)

    def test_dgt1_multiplicity(self):
        self.assertEqual(solver.solve_exact_intertwiners(
            solver.synthetic_trivial_multiplicity(2,1)).dimension, 2)

    def test_basis_change_invariance(self):
        pair = solver.synthetic_trivial_multiplicity(2,2)
        base = solver.solve_exact_intertwiners(pair).dimension
        changed = solver.change_pair_basis(
            pair,
            ql.matrix(((1,1),(0,1))),
            ql.matrix(((1,0),(1,1))))
        self.assertEqual(solver.solve_exact_intertwiners(changed).dimension, base)

    def test_projective_normalization_is_scale_and_sign_invariant(self):
        a = ql.matrix(((0, ql.q(1)/2), (-1,0)))
        b = ql.scale(-6, a)
        self.assertEqual(solver.canonical_projective_matrix(a),
                         solver.canonical_projective_matrix(b))


if __name__ == '__main__':
    unittest.main(verbosity=2)
