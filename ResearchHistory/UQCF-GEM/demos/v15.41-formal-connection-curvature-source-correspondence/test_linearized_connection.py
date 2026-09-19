import ast
from fractions import Fraction
from pathlib import Path
import unittest

from linearized_connection import (
    construct_isotropic_lift,
    differentiate_holonomy,
    solve_linearized_connection,
)
from operational_complex import (
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
