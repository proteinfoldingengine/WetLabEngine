import unittest
from fractions import Fraction as Q

from exact_matrix import add, apply_matrix, identity, inverse, matmul, nullspace, rank, rref, shape, transpose, zeros


class MatrixTests(unittest.TestCase):
    def test_exact_rectangular_product(self):
        a = ((Q(1, 2), Q(2), Q(-1)), (Q(3), Q(0), Q(4)))
        b = ((Q(2), Q(1)), (Q(1, 3), Q(0)), (Q(0), Q(5)))
        self.assertEqual(matmul(a, b), ((Q(5, 3), Q(-9, 2)), (Q(6), Q(23))))
        self.assertEqual(shape(transpose(a)), (3, 2))
        self.assertEqual(apply_matrix(a, (Q(2), Q(1), Q(0))), (Q(3), Q(6)))

    def test_zero_dimensions_keep_shape(self):
        self.assertEqual(transpose(zeros(0, 3), ncols=3), zeros(3, 0))
        self.assertEqual(matmul(zeros(2, 0), zeros(0, 4), right_ncols=4), zeros(2, 4))
        self.assertEqual(matmul(zeros(0, 3), zeros(3, 2), left_ncols=3), zeros(0, 2))
        self.assertEqual(add(zeros(0, 2), zeros(0, 2), ncols=2), zeros(0, 2))
        self.assertEqual(matmul(identity(0), zeros(0, 5), left_ncols=0, right_ncols=5), zeros(0, 5))

    def test_reject_ragged_and_incompatible(self):
        with self.assertRaisesRegex(ValueError, 'shape'):
            shape(())
        with self.assertRaisesRegex(ValueError, 'shape'):
            shape(((Q(1),), ()))
        with self.assertRaisesRegex(ValueError, 'shape'):
            matmul(zeros(2, 0), zeros(1, 3))
        with self.assertRaisesRegex(ValueError, 'shape'):
            add(zeros(0, 2), zeros(0, 3), ncols=2, other_ncols=3)
        with self.assertRaisesRegex(ValueError, 'shape'):
            apply_matrix(zeros(2, 3), (Q(1), Q(2)))

    def test_reject_inexact_and_boolean(self):
        with self.assertRaises(TypeError): shape(((0.5,),))
        with self.assertRaises(TypeError): shape(((True,),))

    def test_deterministic_reduction_and_inverse(self):
        a = ((Q(0), Q(2)), (Q(1), Q(1)))
        result = rref(a)
        self.assertEqual(result.reduced, identity(2))
        self.assertEqual(result.pivots, (0, 1))
        self.assertEqual(result.operations[0], ('swap', 0, 1))
        self.assertEqual(matmul(a, inverse(a)), identity(2))

    def test_empty_rows_explicit_width_and_singular_inverse(self):
        self.assertEqual(rref((), ncols=3).reduced, ())
        self.assertEqual(nullspace((), ncols=3), identity(3))
        self.assertEqual(rank((), ncols=3), 0)
        with self.assertRaises(ValueError): inverse(((Q(1), Q(1)), (Q(2), Q(2))))


if __name__ == '__main__': unittest.main()
