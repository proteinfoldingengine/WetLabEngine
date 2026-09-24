"""Task 4 RED tests: conditioning is descriptive and pair separation is dependency-audited."""
from __future__ import annotations
import unittest
from dependency_audit import (
    archived_pair_dependency_audit,
    classify_pair_dependency,
    conditioning_diagnostic,
)
from spectral import spectral_certificate


class DependencyAuditTests(unittest.TestCase):
    def test_injective_centered_nonproportional_inputs_force_output_nonproportionality(self):
        result = classify_pair_dependency(
            centered_injective=True,
            canonical_centered=True,
            control_centered=True,
            input_proportional=False,
            output_proportional=False,
        )
        self.assertEqual(result["classification"], "DEPENDENT_ON_CENTERED_INJECTIVITY")

    def test_nonconstant_kernel_blocks_dependency_claim(self):
        result = classify_pair_dependency(
            centered_injective=False,
            canonical_centered=True,
            control_centered=True,
            input_proportional=False,
            output_proportional=False,
        )
        self.assertEqual(result["classification"], "NOT_FORCED_BY_INJECTIVITY")

    def test_contradiction_is_rejected_on_injective_centered_domain(self):
        with self.assertRaisesRegex(ValueError, "injectivity_contradiction"):
            classify_pair_dependency(
                centered_injective=True,
                canonical_centered=True,
                control_centered=True,
                input_proportional=False,
                output_proportional=True,
            )

    def test_conditioning_is_descriptive_and_has_no_threshold_or_tuning_surface(self):
        before = spectral_certificate(7)
        diagnostic = conditioning_diagnostic(7)
        self.assertEqual(diagnostic["role"], "DESCRIPTIVE_ONLY")
        self.assertNotIn("threshold", diagnostic)
        self.assertNotIn("tuned", diagnostic)
        diagnostic["condition_number"] = -1.0
        after = spectral_certificate(7)
        self.assertEqual(before, after)

    def test_conditioning_values_are_frozen_descriptions(self):
        five = conditioning_diagnostic(5)
        seven = conditioning_diagnostic(7)
        self.assertAlmostEqual(five["min_nonzero_response_scale"], 0.34549150281252616, places=14)
        self.assertAlmostEqual(five["condition_number"], 2.6180339887498967, places=14)
        self.assertAlmostEqual(seven["min_nonzero_response_scale"], 0.18825509907063312, places=14)
        self.assertAlmostEqual(seven["condition_number"], 5.048917339522309, places=14)

    def test_archive_audit_covers_all_592_pairs(self):
        audit = archived_pair_dependency_audit()
        self.assertEqual(audit["pair_count"], 592)
        self.assertEqual(audit["centered_pair_count"], 592)
        self.assertEqual(audit["output_nonproportional_count"], 592)
        self.assertEqual(audit["dependent_on_injectivity_count"], 592)
        self.assertEqual(audit["not_forced_count"], 0)

    def test_claim_dependency_map_separates_forced_from_independent_diagnostics(self):
        audit = archived_pair_dependency_audit()
        expected = {
            "response_nonproportionality": "DEPENDENT_ON_CENTERED_INJECTIVITY",
            "matrix_inequality": "DEPENDENT_ON_CENTERED_INJECTIVITY",
            "normalized_profile_inequality": "NOT_FORCED_BY_INJECTIVITY",
            "energy_difference": "NOT_FORCED_BY_INJECTIVITY",
            "face_invariant_differences": "NOT_FORCED_BY_INJECTIVITY",
            "norm_and_ratio_differences": "NOT_FORCED_BY_INJECTIVITY",
        }
        self.assertEqual(audit["claim_dependency"], expected)

    def test_archive_audit_reports_both_odd_carrier_conditioning_records(self):
        audit = archived_pair_dependency_audit()
        records = audit["conditioning"]
        self.assertEqual(tuple(record["L"] for record in records), (5, 7))
        self.assertTrue(all(record["centered_injective"] for record in records))
        self.assertTrue(all(record["min_nonzero_response_scale"] > 0 for record in records))
        self.assertTrue(all(record["condition_number"] >= 1 for record in records))


if __name__ == "__main__":
    unittest.main()
