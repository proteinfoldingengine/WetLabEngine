import unittest
from fractions import Fraction
import exact_linear as ql


class ExactLinearTests(unittest.TestCase):
    def test_rank_and_nullspace_are_exact(self):
        a = ql.matrix(((1,2,3),(2,4,6)))
        self.assertEqual(ql.rank(a), 1)
        ns = ql.nullspace(a)
        self.assertEqual(len(ns), 2)
        for v in ns:
            self.assertEqual(ql.matvec(a, v), (Fraction(0), Fraction(0)))

    def test_unimodular_inverse_is_exact(self):
        u = ql.matrix(((1,1),(0,1)))
        self.assertEqual(ql.matmul(u, ql.inverse(u)), ql.identity(2))

    def test_conjugation_preserves_trace(self):
        a = ql.matrix(((0,1),(1,0)))
        u = ql.matrix(((1,1),(0,1)))
        b = ql.conjugate(a, u)
        self.assertEqual(ql.trace(a), ql.trace(b))

    def test_singular_inverse_rejected(self):
        with self.assertRaises(ValueError):
            ql.inverse(ql.matrix(((1,2),(2,4))))

    def test_shape_errors_fail_closed(self):
        with self.assertRaises(ValueError):
            ql.matmul(ql.matrix(((1,2),)), ql.matrix(((1,2),)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
