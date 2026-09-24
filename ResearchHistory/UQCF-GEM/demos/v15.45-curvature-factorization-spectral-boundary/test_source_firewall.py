"""Task 5 RED tests: identify source-curvature identities guaranteed by construction."""
from __future__ import annotations
import unittest
from source_firewall import audit_source_relations, classify_source_relation


class SourceFirewallTests(unittest.TestCase):
    def test_global_balance_identity_is_dependent_by_construction(self):
        result = classify_source_relation("GLOBAL_BALANCE_COMPLETION")
        self.assertEqual(result["classification"], "DEPENDENT_BY_CONSTRUCTION")
        self.assertEqual(result["identity"], "A_phi=ONE_HALF_M_s")

    def test_all_frozen_families_are_classified_without_physical_verdict(self):
        audit = audit_source_relations()
        self.assertEqual(audit["family_count"], 5)
        self.assertEqual(audit["source_correspondence"], "NOT_EVALUATED")
        self.assertFalse(audit["physical_gravity"])
        self.assertEqual(audit["Pillar_3"], "OPEN")
        self.assertTrue(all(item["classification"] == "DEPENDENT_BY_CONSTRUCTION"
                            for item in audit["families"]))

    def test_global_balance_composition_is_exact_on_frozen_sizes(self):
        audit = audit_source_relations()
        canonical = next(item for item in audit["families"]
                         if item["family"] == "GLOBAL_BALANCE_COMPLETION")
        self.assertEqual(canonical["sizes"], (5, 7, 9, 11))
        self.assertTrue(canonical["exact_composition_verified"])

    def test_controls_do_not_become_physical_source_evidence(self):
        audit = audit_source_relations()
        controls = tuple(item for item in audit["families"]
                         if item["family"] != "GLOBAL_BALANCE_COMPLETION")
        self.assertEqual(len(controls), 4)
        self.assertTrue(all(item["physical_source_verdict"] == "NOT_EVALUATED"
                            for item in controls))


if __name__ == "__main__":
    unittest.main()
