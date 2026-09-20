from dataclasses import replace
from fractions import Fraction
import unittest

from exact_algebra import matvec, nullspace, rank, rref, solve_unique
from operational_complex import (
    ConnectionStatus,
    construct_operational_complex,
    cycle_holonomy,
    enumerate_baseline_connection,
)
from response_inputs import family_input, verify_evidence


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
        return Fraction(dx * dx + dy * dy)

    work = tuple(tuple(distance(i, j) for j in labels) for i in labels)
    return labels, work, edges


def uniform_work(labels):
    return tuple(tuple(Fraction(i != j) for j in labels) for i in labels)


class OperationalComplexTests(unittest.TestCase):
    def test_exact_square_complex_and_tangent_quotient(self):
        matrix = ((Fraction(1), Fraction(1)), (Fraction(1), Fraction(-1)))
        rhs = (Fraction(3), Fraction(1))
        solution = solve_unique(matrix, rhs)
        self.assertEqual(solution, (Fraction(2), Fraction(1)))
        self.assertEqual(matvec(matrix, solution), rhs)
        self.assertEqual(rank(matrix), 2)
        self.assertEqual(nullspace(((Fraction(1), Fraction(1)),)), ((Fraction(-1), Fraction(1)),))
        self.assertEqual(rref((), ncols=2), ((), ()))
        with self.assertRaises(ValueError):
            rank(((1,), (1, 2)))
        with self.assertRaises(ValueError):
            matvec(((1, 0),), (1,))
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            solve_unique(((1,), (1,)), (0, 1))
        with self.assertRaisesRegex(ValueError, "nonunique"):
            solve_unique(((1, 1),), (1,))
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
        self.assertTrue(verify_evidence())
        inherited = family_input(5, "GLOBAL_BALANCE_COMPLETION", Fraction(1))
        self.assertEqual(len(inherited.labels), 25)
        self.assertEqual(len(inherited.work), 25)
        for forbidden in ("B1", "B2", "A", "D", "coordinates", "candidate_operator"):
            self.assertFalse(hasattr(inherited, forbidden))
        result = construct_operational_complex(*periodic_square_input())
        self.assertEqual(len(result.complex.d4_actions), 8)
        self.assertEqual(len(set(result.complex.d4_actions)), 8)

    def test_baseline_transport_has_one_gauge_orbit(self):
        labels, work, edges = periodic_square_input()
        complex_ = construct_operational_complex(labels, work, edges).complex
        result = enumerate_baseline_connection(complex_)
        self.assertEqual(result.status, ConnectionStatus.IDENTIFIABLE)
        self.assertEqual(result.connection.gauge_orbit_count, 1)
        self.assertEqual(set(result.connection.transport_candidate_counts), {8})
        scaled = construct_operational_complex(
            labels,
            tuple(tuple(Fraction(7, 3) * value for value in row) for row in work),
            edges,
        ).complex
        self.assertEqual(
            enumerate_baseline_connection(scaled).connection.holonomy_classes,
            result.connection.holonomy_classes,
        )
        permutation = tuple((2 * i + 1) % len(labels) for i in labels)
        changed_work = [[Fraction(0)] * len(labels) for _ in labels]
        for i in labels:
            for j in labels:
                changed_work[permutation[i]][permutation[j]] = work[i][j]
        changed_edges = frozenset(
            frozenset(permutation[label] for label in edge) for edge in edges
        )
        changed = construct_operational_complex(
            labels, tuple(tuple(row) for row in changed_work), changed_edges
        ).complex
        self.assertEqual(
            enumerate_baseline_connection(changed).connection.holonomy_classes,
            result.connection.holonomy_classes,
        )

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
        first_edge, first_matrix = connection.transports[0]
        reflected = ((Fraction(-1), Fraction(0)), (Fraction(0), Fraction(1)))
        reverse = (first_edge[1], first_edge[0])
        altered_transports = tuple(
            (edge, reflected if edge in (first_edge, reverse) else matrix)
            for edge, matrix in connection.transports
        )
        altered = replace(connection, transports=altered_transports, flat=False)
        incident = next(cycle for cycle in complex_.cycles if set(first_edge) <= set(cycle))
        self.assertNotEqual(
            cycle_holonomy(altered, incident, 1),
            connection.identity,
        )


if __name__ == "__main__":
    unittest.main()
