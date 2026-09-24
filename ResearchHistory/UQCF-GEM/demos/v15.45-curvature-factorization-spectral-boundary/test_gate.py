"""Task 6 RED tests: deterministic fail-closed v15.45 scientific ledger."""
from __future__ import annotations
import copy
import tempfile
import unittest
from pathlib import Path
from gate import audit, canonical_bytes, verify_result


class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_mechanical_adjudication(self):
        self.assertEqual(self.result["status"],
                         "FACTORIZATION_CERTIFIED_WITH_EXPLICIT_SPECTRAL_BOUNDARY")
        self.assertEqual(self.result["claims"]["source_correspondence"], "NOT_EVALUATED")
        self.assertEqual(self.result["claims"]["Pillar_3"], "OPEN")

    def test_task3_boundary_is_preserved(self):
        spectral = self.result["spectral_boundary"]
        self.assertEqual((spectral["L5"]["rank"], spectral["L5"]["centered_nullity"]), (24,0))
        self.assertEqual((spectral["L6"]["rank"], spectral["L6"]["centered_nullity"]), (24,11))
        self.assertEqual((spectral["L7"]["rank"], spectral["L7"]["centered_nullity"]), (48,0))
        self.assertEqual((spectral["L8"]["rank"], spectral["L8"]["centered_nullity"]), (48,15))

    def test_task4_dependency_is_not_double_counted(self):
        evidence = self.result["evidence_dependency"]
        self.assertEqual(evidence["pairs"], 592)
        self.assertEqual(evidence["dependent_response_nonproportionality"], 592)
        self.assertEqual(evidence["independent_response_nonproportionality"], 0)

    def test_task5_firewall_is_preserved(self):
        firewall = self.result["source_firewall"]
        self.assertEqual(firewall["canonical_identity"], "A_phi=ONE_HALF_M_s")
        self.assertEqual(firewall["classification"], "DEPENDENT_BY_CONSTRUCTION")

    def test_missing_or_forged_stage_fails_closed(self):
        forged = copy.deepcopy(self.result)
        forged["spectral_boundary"]["L6"]["centered_nullity"] = 0
        with self.assertRaises(ValueError):
            verify_result(forged)

    def test_canonical_bytes_are_deterministic(self):
        raw = canonical_bytes(self.result)
        self.assertEqual(raw, canonical_bytes(audit()))
        self.assertTrue(raw.endswith(b"\n"))


if __name__ == "__main__":
    unittest.main()
