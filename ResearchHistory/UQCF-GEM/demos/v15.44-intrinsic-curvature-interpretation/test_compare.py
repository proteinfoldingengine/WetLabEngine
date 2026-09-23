import json
import unittest
from fractions import Fraction as Q
from pathlib import Path
from operator_types import Operator
from kernel import analyze_kernel
from compare import analyze_field, compare_pair, validate_archived_cases, validate_pair_coverage, validate_archive_claims

HERE = Path(__file__).resolve().parent

def synthetic_case(curvature, field):
    n = len(field)
    a = Operator(tuple(range(n)), tuple((0, 1, 2, 3) for _ in curvature),
                 tuple(row for coefficients in curvature for row in
                       ((Q(0),)*n, tuple(coefficients), tuple(-x for x in coefficients), (Q(0),)*n)))
    return analyze_field(a, analyze_kernel(a), tuple(field))

class FieldTests(unittest.TestCase):
    def test_kernel_field_and_zero_profile(self):
        c = synthetic_case(((Q(1), Q(-1)),), (Q(3), Q(3)))
        self.assertEqual((c['energy'], c['S'], c['kernel_component'], c['visible_component']),
                         (Q(0), Q(18), (Q(3), Q(3)), (Q(0), Q(0))))
        self.assertEqual(c['E_over_S'], Q(0))
        self.assertIsNone(c['normalized_profile'])
        self.assertEqual(c['normalized_profile_reason'], 'UNDEFINED_ZERO_CURVATURE')

    def test_visible_field_exact(self):
        c = synthetic_case(((Q(1), Q(-1)),), (Q(2), Q(0)))
        self.assertEqual(c['response'], (Q(0), Q(2), Q(-2), Q(0)))
        self.assertEqual(c['face_invariants'], (Q(4),))
        self.assertEqual((c['kernel_component'], c['visible_component']), ((Q(1), Q(1)), (Q(1), Q(-1))))
        self.assertEqual((c['E_over_S'], c['E_over_visible_norm']), (Q(1), Q(2)))
        self.assertEqual((c['kernel_share'], c['visible_share']), (Q(1,2), Q(1,2)))

    def test_zero_field_ratios_and_skew_rejection(self):
        c = synthetic_case(((Q(1), Q(-1)),), (Q(0), Q(0)))
        self.assertEqual((c['E_over_S'], c['E_over_S_reason']), (None, 'UNDEFINED_ZERO_FIELD_NORM'))
        self.assertEqual((c['E_over_visible_norm'], c['E_over_visible_norm_reason']),
                         (None, 'UNDEFINED_ZERO_VISIBLE_NORM'))
        a = Operator((0, 1), ((0, 1, 2, 3),), ((Q(1), Q(0)),) + ((Q(0), Q(0)),)*3)
        with self.assertRaisesRegex(ValueError, 'skew'):
            analyze_field(a, analyze_kernel(a), (Q(1), Q(0)))

class PairTests(unittest.TestCase):
    def test_negative_factor_profile(self):
        a = synthetic_case(((Q(1), Q(-1)),), (Q(1), Q(-1)))
        b = synthetic_case(((Q(1), Q(-1)),), (Q(-2), Q(2)))
        p = compare_pair(a, b)
        self.assertEqual((p['proportionality'], p['factor_control_over_canonical']),
                         ('NONZERO_PROPORTIONAL', Q(-2)))
        self.assertFalse(p['matrix_equal'])
        self.assertTrue(p['normalized_profile_equal'])
        self.assertEqual(p['energy_difference'], Q(12))

    def test_zero_cases_and_nonproportional(self):
        zero = synthetic_case(((Q(0), Q(0)),), (Q(1), Q(0)))
        other = synthetic_case(((Q(0), Q(0)),), (Q(0), Q(3)))
        p = compare_pair(zero, other)
        self.assertEqual(p['proportionality'], 'BOTH_ZERO')
        self.assertTrue(p['matrix_equal'])
        self.assertEqual((p['normalized_profile_equal'], p['normalized_profile_equal_reason']),
                         (None, 'UNDEFINED_ZERO_CURVATURE'))
        self.assertEqual(p['S_difference'], Q(8))
        one = synthetic_case(((Q(1), Q(-1)), (Q(0), Q(0))), (Q(1), Q(0)))
        two = synthetic_case(((Q(0), Q(0)), (Q(1), Q(-1))), (Q(1), Q(0)))
        oneface = synthetic_case(((Q(1), Q(-1)),), (Q(1), Q(0)))
        self.assertEqual(compare_pair(zero, oneface)['proportionality'], 'CANONICAL_ZERO_ONLY')
        self.assertEqual(compare_pair(oneface, zero)['proportionality'], 'CONTROL_ZERO_ONLY')
        self.assertEqual(compare_pair(one, two)['proportionality'], 'NONZERO_NONPROPORTIONAL')
        self.assertFalse(compare_pair(one, two)['normalized_profile_equal'])
        with self.assertRaisesRegex(ValueError, 'face'):
            compare_pair(oneface, one)

class ArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads((HERE.parent / 'v15.43-certified-response-geometry/docs/RESULTS.json').read_text())['cases']

    def test_actual_archive_complete(self):
        self.assertEqual(len(validate_archived_cases(self.cases)), 740)

    def test_reject_forbidden_physical_claim_and_unknown_claim(self):
        claims = json.loads((HERE.parent / 'v15.43-certified-response-geometry/docs/RESULTS.json').read_text())['claims']
        self.assertTrue(validate_archive_claims(claims))
        for name in ('physical_curvature', 'physical_gravity', 'physical_metric',
                     'spacetime', 'einstein_equations', 'stress_energy',
                     'continuum_limit', 'scientific_breakthrough'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'archive_claim_boundary'):
                validate_archive_claims(dict(claims, **{name: True}))
        with self.assertRaisesRegex(ValueError, 'archive_claim_boundary'):
            validate_archive_claims({k:v for k,v in claims.items() if k != 'physical_curvature'})
        with self.assertRaisesRegex(ValueError, 'archive_claim_boundary'):
            validate_archive_claims(dict(claims, physical_uniqueness=True))
        with self.assertRaisesRegex(ValueError, 'archive_claim_boundary'):
            validate_archive_claims(dict(claims, inherited_axiom_dependence=False))

    def test_missing_pair_rejected(self):
        from bootstrap import load_pinned_modules
        families = load_pinned_modules(HERE.parents[3])['projection'].FAMILY_KEYS
        pairs = [{'canonical_key': (L,families[0],scale,index),
                  'control_key': (L,family,scale,index)}
                 for L in (5,7) for scale in (Q(1),Q(7,3)) for index in range(L*L)
                 for family in families[1:]]
        self.assertEqual(validate_pair_coverage(pairs), 592)
        with self.assertRaisesRegex(ValueError, 'pair_coverage'):
            validate_pair_coverage(pairs[:-1])

    def test_missing_reordered_face_and_invariant_rejected(self):
        with self.assertRaisesRegex(ValueError, 'coverage'):
            validate_archived_cases(self.cases[:-1])
        swapped = list(self.cases)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        with self.assertRaisesRegex(ValueError, 'order'):
            validate_archived_cases(swapped)
        wrong = dict(self.cases[0], faces=list(self.cases[0]['faces']))
        wrong['faces'][0], wrong['faces'][1] = wrong['faces'][1], wrong['faces'][0]
        with self.assertRaisesRegex(ValueError, 'face_order'):
            validate_archived_cases([wrong] + self.cases[1:])
        wrong = dict(self.cases[0], faces=list(self.cases[0]['faces']))
        wrong['faces'][0] = dict(wrong['faces'][0], invariant='0')
        with self.assertRaisesRegex(ValueError, 'invariant'):
            validate_archived_cases([wrong] + self.cases[1:])

if __name__ == '__main__': unittest.main()
