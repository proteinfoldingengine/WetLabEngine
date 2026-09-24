import unittest
from dataclasses import replace
from fractions import Fraction as Q
from test_operator import fixture_carrier, actual_geometries
from operator_types import build_actual_carrier
from derive import derive_operator
from oracle import reference_operator
from presentations import (check_presentations, relabel_geometry, verify_alignment,
                           verify_orientations, gauge_assignments, verify_scale,
                           verify_gauge, verify_core_fields, memoized_core)


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.carrier = fixture_carrier(5)

    def test_presented_basis_and_wrong_derivative_slot(self):
        c = self.carrier
        assignments = list(gauge_assignments(c))
        self.assertEqual(len(assignments), 8 + 8 * 25)
        g = assignments[9][1]
        actual = derive_operator(c, g)
        expected = reference_operator(c, g)
        self.assertEqual(actual, expected)
        changed = [list(row) for row in actual.entries]
        changed[1][0] += Q(1)
        from derive import require_equal
        with self.assertRaisesRegex(ValueError, 'operator_mismatch'):
            require_equal(replace(actual, entries=tuple(map(tuple, changed))), expected)

    def test_all_orientations_reject_wrong_basepoint_and_reverse(self):
        c = self.carrier
        a = derive_operator(c)
        self.assertEqual(verify_orientations(c, a), 8*25*25)
        tampered = [list(row) for row in a.entries]
        tampered[0][0] += Q(1)
        with self.assertRaisesRegex(ValueError, 'orientation'):
            verify_orientations(c, replace(a, entries=tuple(map(tuple, tampered))))

    def test_relabel_requires_column_permutation_and_frame_alignment(self):
        c = self.carrier
        changed, names = relabel_geometry(c, tuple(reversed(c.complex.labels)))
        a, b = derive_operator(c), derive_operator(changed)
        self.assertEqual(verify_alignment(c, changed, a, b, names), 25*25)
        with self.assertRaisesRegex(ValueError, 'aligned_operator'):
            verify_alignment(c, changed, a, b, names, permute_columns=False)
        directions = list(changed.complex.direction_classes)
        directions[0] = tuple(-v for v in directions[0])
        broken = replace(changed, complex=replace(changed.complex, direction_classes=tuple(directions)))
        with self.assertRaisesRegex(ValueError, 'direction_frame_alignment'):
            verify_alignment(c, broken, a, b, names)

    def test_scale_aligned_operator(self):
        c, d = fixture_carrier(5), fixture_carrier(5, '7/3')
        self.assertEqual(verify_scale(c, d), 25*25)

    def test_reflection_and_core_fields(self):
        c = self.carrier
        a = derive_operator(c)
        reflected = next(p for key, p in gauge_assignments(c)
                         if key[0] == 'uniform' and
                         p.gauges[0][1][0][0]*p.gauges[0][1][1][1]
                         - p.gauges[0][1][0][1]*p.gauges[0][1][1][0] == -1)
        self.assertEqual(verify_gauge(c, a, reflected), (25, 25))
        rows = [list(row) for row in a.entries]
        rows[1][0] += Q(1)
        wrong = replace(a, entries=tuple(map(tuple, rows)))
        with self.assertRaisesRegex(ValueError, 'operator_mismatch|gauge_face_conjugation'):
            verify_gauge(c, a, reflected, actual=wrong)
        self.assertEqual(verify_core_fields(c, a), 3)

    def test_memoized_core_exact_and_restored_actual_basis(self):
        from bootstrap import load_pinned_modules
        from test_operator import ROOT
        from operator_types import build_actual_carrier
        c = build_actual_carrier(actual_geometries()[0])
        presentation = next(p for key, p in gauge_assignments(c)
                            if key == ('site', c.complex.labels[0], 1))
        expected = reference_operator(c, presentation)
        parent = load_pinned_modules(ROOT)
        original = parent['transport'].matmul
        with memoized_core(parent):
            self.assertEqual(reference_operator(c, presentation), expected)
        self.assertIs(parent['transport'].matmul, original)

if __name__ == '__main__': unittest.main()
