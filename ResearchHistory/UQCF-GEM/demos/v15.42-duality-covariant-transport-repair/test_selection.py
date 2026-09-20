from dataclasses import replace
from fractions import Fraction
import unittest

from protocol_types import CarrierKind, MatrixAction, TransportManifest, TypedMap
from selection import audit_centered_stencil, audit_endpoint_average, audit_selection


class SelectionTests(unittest.TestCase):
    def test_certified_manifest_types_every_map_and_sign(self):
        manifest = TransportManifest.certified()
        self.assertEqual(
            manifest.tangent_forward,
            TypedMap("T_x", "T_y", MatrixAction.DIRECT),
        )
        self.assertEqual(
            manifest.tangent_reverse,
            TypedMap("T_y", "T_x", MatrixAction.INVERSE),
        )
        self.assertEqual(
            manifest.cotangent_pullback,
            TypedMap("T_y*", "T_x*", MatrixAction.TRANSPOSE),
        )
        self.assertEqual(
            manifest.cotangent_reverse,
            TypedMap("T_x*", "T_y*", MatrixAction.INVERSE_TRANSPOSE),
        )
        self.assertEqual(manifest.frame_variation_sign, -1)
        self.assertEqual(manifest.coframe_variation_sign, 1)
        self.assertTrue(manifest.validate())

    def test_every_manifest_substitution_is_rejected(self):
        manifest = TransportManifest.certified()
        changes = (
            {"carrier_pair": (CarrierKind.COVECTOR, CarrierKind.COVECTOR)},
            {"frame_variation_sign": 1},
            {"coframe_variation_sign": -1},
            {"basepoint_rule": "output_selected"},
            {"orientation_rule": "forward_only"},
            {
                "cotangent_pullback": TypedMap(
                    "T_y*", "T_x*", MatrixAction.INVERSE_TRANSPOSE
                )
            },
            {
                "cotangent_reverse": TypedMap(
                    "T_x*", "T_y*", MatrixAction.TRANSPOSE
                )
            },
        )
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                replace(manifest, **change).validate()

    def test_manifest_rejects_equality_compatible_type_impostors(self):
        manifest = TransportManifest.certified()
        changes = (
            {"frame_variation_sign": True},
            {"frame_variation_sign": -1.0},
            {"frame_variation_sign": "-1"},
            {"coframe_variation_sign": True},
            {"carrier_pair": ("tangent_vector", "covector")},
            {
                "tangent_forward": TypedMap(
                    "T_x", "T_y", "direct"
                )
            },
        )
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                replace(manifest, **change).validate()

    def test_manifest_rejects_subclass_even_when_values_are_certified(self):
        class ManifestSubclass(TransportManifest):
            pass

        with self.assertRaises(ValueError):
            ManifestSubclass.certified().validate()

    def test_centered_stencil_is_uniquely_selected(self):
        audit = audit_centered_stencil()
        self.assertTrue(audit.identifiable)
        self.assertEqual(
            audit.solution,
            (Fraction(1, 2), Fraction(0), Fraction(-1, 2)),
        )
        self.assertEqual((audit.rank, audit.unknowns), (3, 3))

    def test_endpoint_average_is_uniquely_selected(self):
        audit = audit_endpoint_average()
        self.assertTrue(audit.identifiable)
        self.assertEqual(audit.solution, (Fraction(1, 2), Fraction(1, 2)))
        self.assertEqual((audit.rank, audit.unknowns), (2, 2))

    def test_missing_affine_or_normalization_axiom_is_not_identifiable(self):
        self.assertFalse(audit_centered_stencil(drop="affine_exact").identifiable)
        self.assertFalse(audit_endpoint_average(drop="constant_exact").identifiable)

    def test_centered_drop_verdicts_follow_exact_remaining_rank(self):
        expected = {
            "constant_exact": (3, True),
            "odd_center": (3, True),
            "odd_endpoints": (3, True),
            "affine_exact": (2, False),
        }
        for axiom, verdict in expected.items():
            with self.subTest(axiom=axiom):
                audit = audit_centered_stencil(drop=axiom)
                self.assertEqual((audit.rank, audit.identifiable), verdict)

    def test_endpoint_drop_verdicts_follow_exact_remaining_rank(self):
        for axiom in ("constant_exact", "endpoint_symmetry"):
            with self.subTest(axiom=axiom):
                audit = audit_endpoint_average(drop=axiom)
                self.assertEqual((audit.rank, audit.identifiable), (1, False))

    def test_unknown_axiom_names_are_rejected(self):
        with self.assertRaises(ValueError):
            audit_centered_stencil(drop="unknown")
        with self.assertRaises(ValueError):
            audit_endpoint_average(drop="unknown")

    def test_aggregate_preserves_component_audits_and_verdict(self):
        audit = audit_selection()
        self.assertEqual(audit.centered_stencil, audit_centered_stencil())
        self.assertEqual(audit.endpoint_average, audit_endpoint_average())
        self.assertTrue(audit.identifiable)
        self.assertFalse(replace(audit, identifiable=False).identifiable)


if __name__ == "__main__":
    unittest.main()
