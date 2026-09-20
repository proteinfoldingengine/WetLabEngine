import ast
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import unittest

from linearized_connection import (
    CarrierKind,
    MatrixAction,
    TransportDirection,
    TransportManifest,
    audit_transport_protocol,
    construct_isotropic_lift,
    differentiate_holonomy,
    executed_flatness_diagnostic,
    local_circulation_rowspace_witness,
    parity_witness,
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

    def test_literal_frozen_manifest_is_explicit_and_inconsistent(self):
        manifest = TransportManifest.literal_frozen()
        self.assertEqual(manifest.carrier, CarrierKind.TANGENT_VECTOR)
        self.assertEqual(manifest.edge_direction, TransportDirection.REVERSE)
        self.assertEqual(manifest.matrix_action, MatrixAction.DIRECT)
        self.assertEqual(manifest.variation_sign, 1)
        for L, expected in ((5, (50, 51)), (7, (98, 99))):
            complex_ = construct_operational_complex(*periodic_square_input(L)).complex
            field = tuple(Fraction((i * i + 3 * i) % 11 - 5) for i in range(L * L))
            result = audit_transport_protocol(complex_, field, manifest)
            self.assertFalse(result.protocol_valid)
            self.assertEqual(
                (result.coefficient_rank, result.augmented_rank), expected
            )
            self.assertEqual(result.reason, "literal_frozen_rank_inconsistency")

    def test_transport_manifest_rejects_implicit_repair(self):
        manifest = TransportManifest.literal_frozen()
        with self.assertRaises(ValueError):
            replace(
                manifest, edge_direction=TransportDirection.FORWARD
            ).validate_literal_frozen()
        with self.assertRaises(ValueError):
            replace(
                manifest, matrix_action=MatrixAction.TRANSPOSE
            ).validate_literal_frozen()
        with self.assertRaises(ValueError):
            replace(manifest, variation_sign=-1).validate_literal_frozen()

    def test_local_closure_implies_zero_face_circulation(self):
        witness = local_circulation_rowspace_witness()
        self.assertEqual(
            witness["closure_rank"],
            witness["augmented_with_circulation_rank"],
        )

    def test_executed_diagnostic_is_flat_for_arbitrary_exact_fields(self):
        fields = (
            self.field,
            tuple(Fraction((7 * i + 2) % 13 - 6) for i in range(25)),
            tuple(Fraction(i == 3) for i in range(25)),
        )
        for field in fields:
            diagnostic = executed_flatness_diagnostic(self.complex, field)
            self.assertTrue(diagnostic.all_face_curvatures_zero)

    def test_odd_even_periodic_parity_witnesses(self):
        expected = {
            5: (50, 50, 0),
            6: (71, 72, 1),
            7: (98, 98, 0),
            8: (127, 128, 1),
            9: (162, 162, 0),
        }
        for L, values in expected.items():
            complex_ = construct_operational_complex(*periodic_square_input(L)).complex
            witness = parity_witness(complex_)
            self.assertEqual(
                (witness.rank, witness.unknowns, witness.nullity), values
            )
            self.assertTrue(witness.all_face_curvatures_zero)

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
