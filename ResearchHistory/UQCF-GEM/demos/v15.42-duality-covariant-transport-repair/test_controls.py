"""Manufactured exact controls and fail-fast stage orchestration."""
import unittest
from fractions import Fraction as Q
from dataclasses import replace
from unittest.mock import patch
from exact_algebra import scale
from holonomy import ZERO
from controls import (constant_control, impulse_control, impulse_field,
                      superposition_control, run_control_family, ControlExecutors,
                      ControlStage)


class ControlTests(unittest.TestCase):
    def test_constant_fields_are_flat_at_l5_and_l7(self):
        for L in (5, 7):
            for value in (Q(0), Q(7, 3)):
                result = constant_control(L, value)
                self.assertEqual(result.invariant_counts, ((Q(0), L * L),))
                self.assertTrue(all(matrix == ZERO for matrix in result.curvatures))
                self.assertTrue(result.all_covariances_exact)

    def test_l5_impulse_has_frozen_nonflat_multiset(self):
        result = impulse_control(5, 0, Q(1))
        self.assertEqual(dict(result.invariant_counts), {Q(1,16):4, Q(1,64):8, Q(0):13})
        self.assertEqual(len(result.curvatures),25)
        self.assertEqual(sum(matrix != ZERO for matrix in result.curvatures),12)

    def test_l7_holdout_has_frozen_nonflat_multiset(self):
        result = impulse_control(7, 0, Q(1))
        self.assertEqual(dict(result.invariant_counts), {Q(1,16):4, Q(1,64):8, Q(0):37})
        self.assertEqual(len(result.curvatures),49)
        self.assertEqual(sum(matrix != ZERO for matrix in result.curvatures),12)

    def test_every_marked_vertex_has_the_same_multiset(self):
        for L in (5,7):
            expected = impulse_control(L,0,Q(1)).invariant_counts
            self.assertEqual({impulse_control(L,r,Q(1)).invariant_counts for r in range(L*L)}, {expected})

    def test_exact_scale_law_at_one_and_seven_thirds(self):
        unit, scaled = impulse_control(5,0,Q(1)), impulse_control(5,0,Q(7,3))
        self.assertEqual(scaled.curvatures, tuple(scale(Q(7,3),v) for v in unit.curvatures))
        self.assertEqual(dict(scaled.invariant_counts), {k*Q(49,9):v for k,v in unit.invariant_counts})

    def test_transport_and_curvature_are_linear_under_superposition(self):
        self.assertTrue(superposition_control(5,impulse_field(5,0),impulse_field(5,7),Q(2,3),Q(-5,7)))

    def test_relabel_gauge_basepoint_orientation_and_dual_controls_all_pass(self):
        family = run_control_family()
        self.assertTrue(family.all_required_pass, family.failed_stage)
        self.assertEqual(len(family.results),29)
        self.assertEqual([(r.L,r.root,r.amplitude) for r in family.results],
                         [(5,None,Q(7,3)),(7,None,Q(7,3))]+[(5,r,Q(1)) for r in range(25)]+[(7,0,Q(1)),(5,0,Q(7,3))])
        self.assertTrue(all(r.all_covariances_exact for r in family.results))

    def test_stages_fail_fast_with_unrun_flags(self):
        names = ('covariance','constant_null','l5_nonflat','every_root_equivalent',
                 'l7_holdout_nonflat','scale_exact','superposition_exact')
        flags = ('covariance_exact',)+names[1:]
        for failed in range(7):
            seen = []
            def stage(index):
                def execute():
                    seen.append(index)
                    return ControlStage(index != failed)
                return execute
            result = run_control_family(ControlExecutors(*(stage(i) for i in range(7))))
            self.assertEqual(seen,list(range(failed+1)))
            self.assertEqual(result.failed_stage,names[failed])
            self.assertEqual([getattr(result,name) for name in flags],
                             [True]*failed+[False]+[None]*(6-failed))
            self.assertFalse(result.all_required_pass)

    def test_invalid_exact_inputs_are_rejected(self):
        for value in (False, 1.0):
            with self.assertRaises((TypeError,ValueError)):
                constant_control(5,value)
            with self.assertRaises((TypeError,ValueError)):
                impulse_control(5,0,value)
        for root in (True,1.0,-1,25):
            with self.assertRaises((TypeError,ValueError)):
                impulse_control(5,root,Q(1))


if __name__ == '__main__':
    unittest.main()
