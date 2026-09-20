"""Independent exact oracles for the frozen transport rule."""
import inspect
import unittest
from dataclasses import replace
from fractions import Fraction as Q

from exact_algebra import identity, matmul, matvec, scale, transpose
from fixtures import periodic_square_input, relabel_input
from operational_complex import construct_operational_complex, enumerate_baseline_connection
from protocol_types import TransportManifest
from transport import (FramePresentation, centered_derivatives, construct_transport,
                       cotangent_pullback_delta)


def deterministic_mixed_presentation(complex_):
    return FramePresentation(tuple((x, complex_.d4_actions[(3*i+1) % 8])
                                   for i, x in enumerate(complex_.labels)))


def one_site_presentations(complex_, label):
    return tuple(FramePresentation(tuple((x, g if x == label else identity(2))
                                        for x in complex_.labels))
                 for g in complex_.d4_actions)


def gauge_transform(record, presentation):
    gauges = dict(presentation.gauges)
    def forward(values):
        return tuple(((x, y), matmul(gauges[y], matmul(m, transpose(gauges[x]))))
                     for (x, y), m in values)
    return replace(record, baseline=forward(record.baseline),
                   source_endomorphisms=tuple(((x, y), matmul(gauges[x], matmul(m, transpose(gauges[x]))))
                                             for (x, y), m in record.source_endomorphisms),
                   tangent_deltas=forward(record.tangent_deltas),
                   cotangent_pullback_deltas=tuple(((x, y), matmul(gauges[x], matmul(m, transpose(gauges[y]))))
                                                  for (x, y), m in record.cotangent_pullback_deltas))


def relabeled_problem(complex_, baseline, field, permutation):
    data = (complex_.labels, complex_.work, complex_.neighbors)
    new = construct_operational_complex(*relabel_input(data, permutation)).complex
    values = dict(zip(permutation, field))
    return new, enumerate_baseline_connection(new).connection, tuple(values[x] for x in new.labels)


def relabel_transport(record, old, new, permutation):
    """Rename an existing record, then change to the substrate's new canonical frame."""
    names = dict(zip(old.labels, permutation))
    old_d = dict(zip(old.directed_edges, old.direction_classes))
    new_d = dict(zip(new.directed_edges, new.direction_classes))
    gauges = FramePresentation(tuple((x, next(g for g in old.d4_actions if all(
        matvec(g, d) == new_d[(names[x], names[y])]
        for (a, y), d in old_d.items() if a == x))) for x in old.labels))
    changed = gauge_transform(record, gauges)
    fields = {}
    for name in ('baseline', 'source_endomorphisms', 'tangent_deltas', 'cotangent_pullback_deltas'):
        values = {(names[x], names[y]): m for (x, y), m in getattr(changed, name)}
        fields[name] = tuple((edge, values[edge]) for edge in new.directed_edges)
    return replace(changed, **fields)


class TransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.complex = construct_operational_complex(*periodic_square_input(5)).complex
        cls.baseline = enumerate_baseline_connection(cls.complex).connection
        cls.impulse = tuple(Q(i == 0) for i in range(25))

    def test_constant_field_has_zero_edge_variation(self):
        zero = ((Q(0), Q(0)), (Q(0), Q(0)))
        for presentation in (None, deterministic_mixed_presentation(self.complex)):
            result = construct_transport(self.complex, self.baseline, (Q(7, 3),)*25, presentation=presentation)
            self.assertTrue(all(value == zero for _, value in result.tangent_deltas))

    def test_field_validation_rejects_float_bool_and_wrong_dimension(self):
        for field in ((Q(0),)*24, (Q(0),)*26, (0.0,)*25, (False,)*25, ((Q(0),),)*25, [Q(0)]*25):
            with self.subTest(field=field), self.assertRaises((TypeError, ValueError)):
                construct_transport(self.complex, self.baseline, field)
        good = FramePresentation.identity(self.complex).gauges
        for gauges in (good[:-1], good + good[:1], ((999, identity(2)),) + good[1:],
                       ((False, identity(2)),) + good[1:],
                       ((0, ((Q(2), Q(0)), (Q(0), Q(1)))),) + good[1:],
                       ((0, ((1.0, 0), (0, 1))),) + good[1:],
                       ((0, ((True, 0), (0, 1))),) + good[1:],
                       ((0, ((Q(1),),)),) + good[1:], list(good)):
            with self.subTest(gauges=gauges), self.assertRaises((TypeError, ValueError)):
                construct_transport(self.complex, self.baseline, self.impulse, presentation=FramePresentation(gauges))

    def test_metric_compatibility_is_exact_on_every_directed_edge(self):
        result = construct_transport(self.complex, self.baseline, self.impulse)
        self.assertTrue(result.metric_compatibility_exact)
        self.assertEqual(len(result.tangent_deltas), len(self.complex.directed_edges))
        b = dict(result.source_endomorphisms)
        self.assertEqual(b[(0, 1)], ((Q(1, 2), Q(0)), (Q(0), Q(1, 2))))
        # At 1, q=(-1/2,0); at 6, q=0; d_1,6=(0,-1).
        self.assertEqual(b[(1, 6)], ((Q(0), Q(1, 8)), (Q(-1, 8), Q(0))))
        gradient = dict(centered_derivatives(self.complex, self.baseline, self.impulse, FramePresentation.identity(self.complex)))
        self.assertEqual(gradient[1], (Q(-1, 2), Q(0)))

    def test_reverse_edge_is_derivative_of_inverse_transport(self):
        result = construct_transport(self.complex, self.baseline, self.impulse)
        self.assertTrue(result.reversal_exact)
        b, p = dict(result.source_endomorphisms), dict(result.baseline)
        for x, y in self.complex.directed_edges:
            self.assertEqual(b[(y, x)], scale(-1, matmul(p[(x, y)], matmul(b[(x, y)], p[(y, x)]))))
        for edge, delta in result.tangent_deltas:
            self.assertEqual(dict(result.cotangent_pullback_deltas)[edge], transpose(delta))
        self.assertEqual(cotangent_pullback_delta(((Q(1), Q(2)), (Q(3), Q(4)))), ((Q(1), Q(3)), (Q(2), Q(4))))

    def test_frame_and_coframe_signs_are_derived_not_arguments(self):
        parameters = inspect.signature(construct_transport).parameters
        self.assertNotIn('frame_variation_sign', parameters)
        self.assertNotIn('coframe_variation_sign', parameters)
        self.assertEqual(TransportManifest.certified().frame_variation_sign, -1)
        self.assertEqual(TransportManifest.certified().coframe_variation_sign, 1)
        for name, sign in (('frame_variation_sign', 1), ('coframe_variation_sign', -1)):
            with self.subTest(name=name), self.assertRaises(ValueError):
                construct_transport(self.complex, self.baseline, self.impulse, manifest=replace(TransportManifest.certified(), **{name: sign}))

    def test_every_local_d4_frame_change_is_covariant(self):
        original = construct_transport(self.complex, self.baseline, self.impulse)
        presentations = (deterministic_mixed_presentation(self.complex),) + one_site_presentations(self.complex, 0)
        for presentation in presentations:
            with self.subTest(presentation=presentation):
                actual = construct_transport(self.complex, self.baseline, self.impulse, presentation=presentation)
                self.assertEqual(actual, gauge_transform(original, presentation))

    def test_relabeling_commutes_with_transport_construction(self):
        original = construct_transport(self.complex, self.baseline, self.impulse)
        for permutation in (tuple((7*i+3) % 25 for i in range(25)), tuple(100-13*i for i in range(25))):
            with self.subTest(permutation=permutation):
                c, b, field = relabeled_problem(self.complex, self.baseline, self.impulse, permutation)
                self.assertEqual(construct_transport(c, b, field), relabel_transport(original, self.complex, c, permutation))


if __name__ == '__main__':
    unittest.main()
