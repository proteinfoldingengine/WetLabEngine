"""Task 3 RED tests: exact finite spectral statements, never fitted thresholds."""
import copy
import importlib
import importlib.util
import unittest
from fractions import Fraction as Q


class SpectralTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('spectral'), 'Task 3 spectral implementation is absent')
        self.s = importlib.import_module('spectral')

    def test_odd_period_ranks(self):
        for L, rank in ((5, 24), (7, 48)):
            c = self.s.spectral_certificate(L)
            self.assertEqual((c['rank'], c['nullity'], c['centered_nullity']), (rank, 1, 0))
            self.assertEqual(c['zero_modes'], [[0, 0]])
            self.assertTrue(c['centered_injective'])

    def test_even_period_ranks_and_complete_modes(self):
        for L, rank, nullity in ((6, 24, 12), (8, 48, 16)):
            c = self.s.spectral_certificate(L)
            self.assertEqual((c['rank'], c['nullity'], c['centered_nullity']), (rank, nullity, nullity-1))
            want = [[k, l] for k in range(L) for l in range(L)
                    if (k, l) == (0, 0) or k == L//2 or l == L//2]
            self.assertEqual(c['zero_modes'], want)
            self.assertFalse(c['centered_injective'])

    def test_x_y_and_checkerboard_witnesses(self):
        for L in (6, 8):
            A = self.s.scalar_operator(L)
            for axis in (0, 1, 2):
                v = tuple(Q((-1)**(x if axis == 0 else y if axis == 1 else x+y))
                          for x in range(L) for y in range(L))
                self.assertEqual(sum(v), 0)
                self.assertTrue(any(v))
                self.assertEqual(self.s.apply(A, v), (Q(0),)*(L*L))

    def test_explicit_basis_is_independent_and_complete(self):
        for L in (5, 6, 7, 8):
            c = self.s.spectral_certificate(L)
            basis = tuple(tuple(Q(x) for x in v) for v in c['kernel_basis'])
            A = self.s.scalar_operator(L)
            self.assertEqual(self.s.rational_rank(basis), c['nullity'])
            self.assertEqual(self.s.rational_rank(A)+len(basis), L*L)
            for v in basis:
                self.assertEqual(self.s.apply(A, v), (Q(0),)*(L*L))
            self.assertEqual([sum(v) for v in basis], [L*L]+[0]*(len(basis)-1))

    def test_every_nonconstant_basis_vector_is_a_centered_null(self):
        for L in (6, 8):
            c = self.s.spectral_certificate(L)
            self.assertEqual(len(c['kernel_basis'][1:]), 2*L-1)
            for v in c['kernel_basis'][1:]:
                self.assertEqual(sum(v), 0)
                self.assertGreater(len(set(v)), 1)

    def test_constant_is_null(self):
        for L in (5, 6, 7, 8):
            self.assertEqual(self.s.apply(self.s.scalar_operator(L), (Q(1),)*(L*L)), (Q(0),)*(L*L))

    def test_frozen_impulse_coefficients(self):
        for L in (5, 6, 7, 8):
            values = [row[0] for row in self.s.scalar_operator(L)]
            self.assertEqual(values.count(Q(1, 4)), 4)
            self.assertEqual(values.count(Q(-1, 8)), 8)
            self.assertEqual(values.count(Q(0)), L*L-12)

    def test_exact_rank_not_mode_count_alone(self):
        self.assertEqual(self.s.rational_rank(((Q(1),Q(2)),(Q(2),Q(4)))), 1)
        self.assertEqual(self.s.rational_rank(((Q(0),Q(0)),)), 0)
        self.assertEqual(self.s.rational_rank(((Q(1),Q(0)),(Q(0),Q(1)))), 2)

    def test_invalid_periods_and_types_rejected(self):
        for L in (True, 1, 2, 0, -1, 5.0, '6', None):
            with self.subTest(L=L), self.assertRaises(ValueError):
                self.s.spectral_certificate(L)

    def test_inexact_or_malformed_linear_algebra_rejected(self):
        for matrix in (((0.0,),), ((True,),), ((Q(1),),(Q(1),Q(2))), ()):
            with self.assertRaises(ValueError):
                self.s.rational_rank(matrix)
        with self.assertRaises(ValueError):
            self.s.apply(((Q(1),),), (1.0,))
        with self.assertRaises(ValueError):
            self.s.apply(((Q(1),),), (Q(1),Q(2)))

    def test_replay_is_deterministic(self):
        c = self.s.spectral_certificate(6)
        self.assertEqual(c, self.s.spectral_certificate(6))
        self.assertTrue(self.s.verify_certificate(c))

    def test_forged_rank_or_missing_basis_rejected(self):
        good = self.s.spectral_certificate(6)
        for key, value in (('rank', 35), ('kernel_basis', good['kernel_basis'][:-1]),
                           ('zero_modes', [[0,0]]), ('centered_injective', True), ('extra_claim', True)):
            broken = copy.deepcopy(good)
            broken[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.s.verify_certificate(broken)

    def test_damaged_and_dependent_basis_rejected(self):
        for mode in ('entry', 'duplicate'):
            broken = copy.deepcopy(self.s.spectral_certificate(8))
            if mode == 'entry':
                broken['kernel_basis'][1][0] += 1
            else:
                broken['kernel_basis'][2] = broken['kernel_basis'][1][:]
            with self.assertRaises(ValueError):
                self.s.verify_certificate(broken)

    def test_pure_evaluation_needs_no_io(self):
        from unittest.mock import patch
        with patch('builtins.open', side_effect=AssertionError('no I/O')), \
             patch('subprocess.run', side_effect=AssertionError('no process')):
            self.assertTrue(self.s.verify_certificate(self.s.spectral_certificate(6)))


if __name__ == '__main__':
    unittest.main()
