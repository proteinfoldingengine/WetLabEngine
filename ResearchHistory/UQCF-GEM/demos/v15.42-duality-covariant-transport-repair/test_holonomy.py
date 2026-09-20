"""Independent exact tests for differentiated tangent and cotangent holonomy."""
import unittest
from dataclasses import replace
from fractions import Fraction as Q

from exact_algebra import add, identity, matmul, matvec, scale, transpose
from fixtures import periodic_square_input
from holonomy import (cotangent_holonomy, curvature_invariant,
                      linearized_holonomy, reverse_cycle, rotate_cycle)
from operational_complex import construct_operational_complex, enumerate_baseline_connection
from transport import FramePresentation, construct_transport


def impulse_field(size, root):
    return tuple(Q(label == root) for label in range(size * size))


def impulse_problem(size, root=0):
    complex_ = construct_operational_complex(*periodic_square_input(size)).complex
    baseline = enumerate_baseline_connection(complex_).connection
    return complex_, baseline, construct_transport(complex_, baseline,
                                                   impulse_field(size, root))


def path_transport(transports, cycle, steps):
    result = identity(2)
    for index in range(steps):
        result = matmul(transports[(cycle[index], cycle[index + 1])], result)
    return result


def pair(vector, covector):
    return vector[0] * covector[0] + vector[1] * covector[1]


def presented_baseline(baseline, presentation):
    gauges = dict(presentation.gauges)
    values = tuple((edge, matmul(gauges[edge[1]],
                                  matmul(matrix, transpose(gauges[edge[0]]))))
                   for edge, matrix in baseline.transports)
    return replace(baseline, transports=values)


class HolonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.complex, cls.baseline, cls.transport = impulse_problem(5, root=0)

    def variants(self, cycle):
        for oriented in (cycle, reverse_cycle(cycle)):
            for steps in range(4):
                yield rotate_cycle(oriented, steps)

    def test_product_derivative_matches_independent_four_term_expansion(self):
        p, d = dict(self.baseline.transports), dict(self.transport.tangent_deltas)
        for face in self.complex.cycles:
            for cycle in self.variants(face):
                edges = tuple((cycle[i], cycle[(i + 1) % 4]) for i in range(4))
                p0, p1, p2, p3 = (p[edge] for edge in edges)
                d0, d1, d2, d3 = (d[edge] for edge in edges)
                expected = add(
                    add(matmul(d3, matmul(p2, matmul(p1, p0))),
                        matmul(p3, matmul(d2, matmul(p1, p0)))),
                    add(matmul(p3, matmul(p2, matmul(d1, p0))),
                        matmul(p3, matmul(p2, matmul(p1, d0)))),
                )
                self.assertEqual(linearized_holonomy(self.baseline, self.transport,
                                                      cycle), expected)

    def test_cyclic_basepoints_and_reversal_on_every_face(self):
        p = dict(self.baseline.transports)
        for cycle in self.complex.cycles:
            first = linearized_holonomy(self.baseline, self.transport, cycle)
            for steps in (1, 2, 3):
                bridge = path_transport(p, cycle, steps)
                self.assertEqual(
                    linearized_holonomy(self.baseline, self.transport,
                                        rotate_cycle(cycle, steps)),
                    matmul(bridge, matmul(first, transpose(bridge))))
            self.assertEqual(
                linearized_holonomy(self.baseline, self.transport,
                                    reverse_cycle(cycle)), scale(-1, first))

    def test_every_local_d4_gauge_conjugates_every_based_curvature(self):
        unit = identity(2)
        original = {(cycle,): linearized_holonomy(self.baseline, self.transport, cycle)
                    for face in self.complex.cycles for cycle in self.variants(face)}
        for label in self.complex.labels:
            for action in self.complex.d4_actions:
                presentation = FramePresentation(tuple(
                    (x, action if x == label else unit) for x in self.complex.labels))
                changed = construct_transport(self.complex, self.baseline,
                                              impulse_field(5, 0),
                                              presentation=presentation)
                changed_baseline = presented_baseline(self.baseline, presentation)
                gauges = dict(presentation.gauges)
                for (cycle,), value in original.items():
                    gauge = gauges[cycle[0]]
                    self.assertEqual(
                        linearized_holonomy(changed_baseline, changed, cycle),
                        matmul(gauge, matmul(value, transpose(gauge))))

    def test_tangent_and_cotangent_paths_preserve_pairing_everywhere(self):
        vectors = ((Q(1), Q(0)), (Q(2), Q(-3)))
        covectors = ((Q(0), Q(1)), (Q(5), Q(7)))
        for face in self.complex.cycles:
            for cycle in self.variants(face):
                tangent = linearized_holonomy(self.baseline, self.transport, cycle)
                cotangent = cotangent_holonomy(self.baseline, self.transport, cycle)
                for vector in vectors:
                    for covector in covectors:
                        self.assertEqual(pair(matvec(tangent, vector), covector),
                                         pair(vector, matvec(cotangent, covector)))

    def test_curvature_invariant_is_exact_presentation_independent_and_strict(self):
        value = ((Q(0), Q(-1, 4)), (Q(1, 4), Q(0)))
        self.assertEqual(curvature_invariant(value), Q(1, 16))
        for action in self.complex.d4_actions:
            changed = matmul(action, matmul(value, transpose(action)))
            self.assertEqual(curvature_invariant(changed), Q(1, 16))
        for invalid in (((Q(1), Q(0)), (Q(0), Q(0))),
                        ((Q(0), Q(1)), (Q(0), Q(0))),
                        ((1.0, 0), (0, -1.0)), ((True, 0), (0, False))):
            with self.assertRaises((TypeError, ValueError)):
                curvature_invariant(invalid)

    def test_rejects_malformed_cycles_and_incompatible_records(self):
        cycle = self.complex.cycles[0]
        bad_baseline = replace(self.baseline, transports=self.baseline.transports[1:])
        bad_transport = replace(self.transport, baseline=self.transport.baseline[1:])
        cases = ((bad_baseline, self.transport, cycle),
                 (self.baseline, bad_transport, cycle),
                 (self.baseline, self.transport, cycle[:3]),
                 (self.baseline, self.transport, cycle[:3] + cycle[:1]),
                 (self.baseline, self.transport, list(cycle)),
                 (self.baseline, self.transport, (cycle[0], cycle[1], cycle[2], 999)))
        for baseline, transport, value in cases:
            with self.subTest(cycle=value), self.assertRaises((TypeError, ValueError)):
                linearized_holonomy(baseline, transport, value)
            with self.subTest(cycle=value), self.assertRaises((TypeError, ValueError)):
                cotangent_holonomy(baseline, transport, value)
        for cycle_value, steps in ((cycle, True), (cycle, 1.0), (cycle, 4),
                                   (cycle, -1), (cycle[:3], 1)):
            with self.assertRaises((TypeError, ValueError)):
                rotate_cycle(cycle_value, steps)


if __name__ == '__main__':
    unittest.main()
