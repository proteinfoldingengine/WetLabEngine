"""Task 7 RED tests: exact-head, additive-scope and claim-boundary certification."""
from __future__ import annotations
import copy
import unittest
from pathlib import Path
import ci_verify


class CIVerifyTests(unittest.TestCase):
    def test_frozen_parent_and_governance_hashes(self):
        receipt = ci_verify.verify_static_contract()
        self.assertEqual(receipt["parent"], "9085e4fa0bec3dbd700f759a8a9629b230d226ff")
        self.assertTrue(receipt["additive_scope"])

    def test_wrong_runtime_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "python_runtime"):
            ci_verify.verify_runtime((3, 13, 4))

    def test_false_physical_claim_is_rejected(self):
        ledger = ci_verify.load_ledger()
        ledger["claims"]["physical_gravity"] = True
        with self.assertRaises(ValueError):
            ci_verify.verify_ledger(ledger)

    def test_incomplete_ledger_is_rejected(self):
        ledger = ci_verify.load_ledger()
        del ledger["spectral_boundary"]["L8"]
        with self.assertRaises(ValueError):
            ci_verify.verify_ledger(ledger)

    def test_head_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "head_mismatch"):
            ci_verify.verify_head("0"*40, "1"*40)

    def test_skipped_tests_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "skipped_tests"):
            ci_verify.verify_test_summary(tests_run=1, failures=0, errors=0, skipped=1)


if __name__ == "__main__":
    unittest.main()
