"""Local RED/GREEN tests for a bounded mathematical probe, not engine certification."""
import importlib
import importlib.util
import unittest
from fractions import Fraction as Q

class TypingProbeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('typing_probe'), 'typing_probe is absent')
        self.p = importlib.import_module('typing_probe')

    def test_full_pauli_twirl_is_trace_only(self):
        for n in (1, 2, 3):
            d = 2**n
            for i in range(d):
                for j in range(d):
                    expected = tuple(tuple(Q(int(i == j and r == c),d)
                                     for c in range(d)) for r in range(d))
                    self.assertEqual(self.p.twirl_matrix_unit(n,i,j), expected)

    def test_boundary_rank_and_unaddressed_fixed_sector(self):
        for L in (5,6,7,8):
            c = self.p.translation_certificate(L)
            self.assertEqual(c['boundary_rank'], L*L-1)
            self.assertEqual(c['fixed_constraint_rank'], L*L-1)
            self.assertEqual(c['fixed_boundary_dimension'], 0)
            self.assertEqual(c['source_domain'], 'UNADDRESSED_INPUT_TRIVIAL_UNDER_CELL_TRANSLATIONS')

    def test_boundary_of_boundary_is_zero(self):
        for L in (5,6,7,8):
            b1, b2 = self.p.boundary_1(L), self.p.boundary_2(L)
            for row in b1:
                for col in zip(*b2):
                    self.assertEqual(sum(a*b for a,b in zip(row,col,strict=True)), 0)

    def test_explicit_address_is_a_nonzero_positive_control(self):
        for L in (5,6,7,8):
            v = self.p.addressed_boundary(L,0,Q(2,3))
            self.assertEqual(sum(x != 0 for x in v),4)
            self.assertEqual(sum(x*x for x in v),Q(16,9))
            self.assertEqual(self.p.addressed_boundary(L,0,Q(0)),(Q(0),)*(2*L*L))

    def test_addressed_control_is_covariant_and_signed(self):
        for L in (5,6,7,8):
            for dx,dy in ((1,0),(0,1)):
                source = self.p.addressed_boundary(L,0,Q(2,3))
                target = self.p.addressed_boundary(L,(dx%L)*L+dy%L,Q(2,3))
                self.assertEqual(self.p.translate_edges(source,L,dx,dy),target)
                self.assertEqual(self.p.addressed_boundary(L,0,Q(-2,3)),tuple(-x for x in source))

    def test_harmonic_cycle_escape_is_not_silently_erased(self):
        # Translation-invariant horizontal circulation is closed but not a boundary.
        for L in (5,6,7,8):
            n=L*L
            h=(1,)*n+(0,)*n
            self.assertEqual(self.p.translate_edges(h,L,1,0),h)
            self.assertEqual(self.p.translate_edges(h,L,0,1),h)
            self.assertTrue(all(sum(a*b for a,b in zip(row,h,strict=True)) == 0
                                for row in self.p.boundary_1(L)))
            b2=self.p.boundary_2(L)
            augmented=tuple(tuple(row)+(h[i],) for i,row in enumerate(b2))
            self.assertEqual(self.p.rational_rank(augmented),n)

    def test_invalid_inputs_rejected(self):
        for L in (True,0,1,2,5.0,'5',None):
            with self.assertRaises(ValueError): self.p.boundary_2(L)
        for n in (True,0,1.0,'2'):
            with self.assertRaises(ValueError): self.p.twirl_matrix_unit(n,0,0)
        with self.assertRaises(ValueError): self.p.addressed_boundary(5,25,Q(1))
        with self.assertRaises(ValueError): self.p.addressed_boundary(5,0,0.5)
        with self.assertRaises(ValueError): self.p.rational_rank(((0.5,),))

    def test_exact_deterministic_output_and_claim_boundary(self):
        a=self.p.run()
        self.assertEqual(a,self.p.run())
        self.assertEqual(a['twirl_matrix_units_checked'],84)
        self.assertFalse(a['physical_source_law_adopted'])
        self.assertFalse(a['new_native_joint_state_derived'])
        self.assertEqual(a['source_correspondence'],'NOT_EVALUATED')
        self.assertEqual(a['Pillar_3'],'OPEN')
        self.assertEqual(a['scope'],'EXPLORATORY_TYPING_LEMMAS_NOT_FULL_V1546_CERTIFICATION')

if __name__=='__main__': unittest.main()
