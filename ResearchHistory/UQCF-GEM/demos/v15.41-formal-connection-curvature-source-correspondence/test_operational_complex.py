from fractions import Fraction
import unittest

from operational_complex import (
    ConnectionStatus,
    construct_operational_complex,
    enumerate_baseline_connection,
)


def periodic_square_input(L=5):
    labels = tuple(range(L * L))

    def label(x, y):
        return (x % L) + L * (y % L)

    edges = frozenset(
        frozenset((label(x, y), label(x + dx, y + dy)))
        for x in range(L)
        for y in range(L)
        for dx, dy in ((1, 0), (0, 1))
    )

    def distance(i, j):
        ix, iy = i % L, i // L
        jx, jy = j % L, j // L
        dx = min((ix - jx) % L, (jx - ix) % L)
        dy = min((iy - jy) % L, (jy - iy) % L)
        return Fraction(dx + dy)

    work = tuple(tuple(distance(i, j) for j in labels) for i in labels)
    return labels, work, edges


def uniform_work(labels):
    return tuple(tuple(Fraction(i != j) for j in labels) for i in labels)


class OperationalComplexTests(unittest.TestCase):
    def test_exact_square_complex_and_tangent_quotient(self):
        result = construct_operational_complex(*periodic_square_input())
        self.assertEqual(result.status, ConnectionStatus.IDENTIFIABLE)
        self.assertEqual(result.complex.tangent_rank, 2)
        self.assertEqual(len(result.complex.cycles), 25)

    def test_malformed_stars_cycles_and_opposites_stop(self):
        labels = (0, 1, 2, 3)
        path = frozenset(
            (frozenset((0, 1)), frozenset((1, 2)), frozenset((2, 3)))
        )
        cases = [(labels, uniform_work(labels), path)]
        k5_labels = tuple(range(5))
        k5 = frozenset(
            frozenset((i, j))
            for i in k5_labels
            for j in k5_labels
            if i < j
        )
        cases.append((k5_labels, uniform_work(k5_labels), k5))
        square_labels, square_work, square_edges = periodic_square_input()
        cases.append((square_labels, uniform_work(square_labels), square_edges))
        cases.append(
            (
                square_labels,
                square_work,
                frozenset(edge for edge in square_edges if frozenset((0, 1)) != edge),
            )
        )
        for candidate in cases:
            with self.subTest(edge_count=len(candidate[2])):
                result = construct_operational_complex(*candidate)
                self.assertEqual(result.status, ConnectionStatus.NOT_IDENTIFIABLE)
                self.assertIn(
                    result.reason,
                    {
                        "degree_not_four",
                        "edge_cycle_count",
                        "opposites_ambiguous",
                        "tangent_rank_not_two",
                    },
                )

    def test_local_d4_gauge_is_complete(self):
        result = construct_operational_complex(*periodic_square_input())
        self.assertEqual(len(result.complex.d4_actions), 8)
        self.assertEqual(len(set(result.complex.d4_actions)), 8)

    def test_baseline_transport_has_one_gauge_orbit(self):
        complex_ = construct_operational_complex(*periodic_square_input()).complex
        result = enumerate_baseline_connection(complex_)
        self.assertEqual(result.status, ConnectionStatus.IDENTIFIABLE)
        self.assertEqual(result.connection.gauge_orbit_count, 1)

    def test_holonomy_is_orientation_and_frame_covariant(self):
        complex_ = construct_operational_complex(*periodic_square_input()).complex
        connection = enumerate_baseline_connection(complex_).connection
        self.assertTrue(connection.flat)
        self.assertTrue(
            all(
                conjugacy_class == connection.identity_class
                for conjugacy_class in connection.holonomy_classes
            )
        )


if __name__ == "__main__":
    unittest.main()
