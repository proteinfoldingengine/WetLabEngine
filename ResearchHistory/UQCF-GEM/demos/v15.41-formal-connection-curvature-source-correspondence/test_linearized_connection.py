import ast
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import unittest

from linearized_connection import (
    construct_isotropic_lift,
    differentiate_holonomy,
    solve_linearized_connection,
)
from operational_complex import (
    ConnectionStatus,
    construct_operational_complex,
    enumerate_baseline_connection,
)
from test_operational_complex import periodic_square_input


class LinearizedConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.complex = construct_operational_complex(*periodic_square_input()).complex
        cls.baseline = enumerate_baseline_connection(cls.complex).connection
        cls.field = tuple(Fraction(i - 12) for i in range(25))

    def test_isotropic_symmetric_tensor_space_has_rank_one(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        self.assertEqual(lift.invariant_dimension, 1)
        self.assertTrue(lift.glues_equivariantly)
        reflection_only = replace(
            self.complex,
            d4_actions=(
                ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
                ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(-1))),
            ),
        )
        ambiguous = construct_isotropic_lift(reflection_only, self.field)
        self.assertEqual(ambiguous.status, ConnectionStatus.NOT_IDENTIFIABLE)
        self.assertEqual(ambiguous.invariant_dimension, 2)

    def test_metric_compatibility_is_exact_on_every_edge(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        self.assertTrue(result.metric_compatibility_exact)

    def test_cartan_closure_rank_and_residual_are_exact(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        self.assertEqual(result.coefficient_rank, result.augmented_rank)
        self.assertTrue(result.residual_zero)

    def test_solution_is_unique_and_linear_or_stops(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        self.assertEqual(result.nullity, result.gauge_dimension)
        self.assertTrue(result.unique_mod_gauge)
        other = tuple(Fraction((i * i + 3 * i) % 11 - 5) for i in range(25))
        left, right = Fraction(2, 3), Fraction(-5, 7)
        combined = tuple(
            left * first + right * second
            for first, second in zip(self.field, other)
        )
        other_result = solve_linearized_connection(
            self.complex,
            self.baseline,
            construct_isotropic_lift(self.complex, other),
        )
        combined_result = solve_linearized_connection(
            self.complex,
            self.baseline,
            construct_isotropic_lift(self.complex, combined),
        )
        for (_, first), (_, second), (_, actual) in zip(
            result.delta_transports,
            other_result.delta_transports,
            combined_result.delta_transports,
        ):
            expected = tuple(
                tuple(left * first[i][j] + right * second[i][j] for j in range(2))
                for i in range(2)
            )
            self.assertEqual(actual, expected)

    def test_curvature_is_differentiated_holonomy_not_laplacian(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        values = tuple(
            differentiate_holonomy(self.baseline, result, cycle)
            for cycle in self.complex.cycles
        )
        self.assertEqual(len(values), len(self.complex.cycles))
        path = Path("linearized_connection.py")
        tree = ast.parse(path.read_text())
        names = {
            node.id.lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }
        imports = {
            alias.name.lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        } | {
            (node.module or "").lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        }
        forbidden = {
            "b1",
            "b2",
            "laplacian",
            "defect",
            "response_generation",
            "coordinates",
            "numpy",
            "eig",
            "svd",
            "pinv",
        }
        self.assertTrue(names.isdisjoint(forbidden))
        self.assertTrue(imports.isdisjoint(forbidden))


if __name__ == "__main__":
    unittest.main()
