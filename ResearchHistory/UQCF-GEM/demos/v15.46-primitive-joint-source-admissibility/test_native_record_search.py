"""Stage B2 RED tests: bounded search for a primitive-derived joint-state record."""
from __future__ import annotations
import unittest
from pathlib import Path
import native_record_search as nrs


class NativeRecordSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.result=nrs.audit_scope(cls.root)

    def test_scope_is_finite_and_pinned(self):
        self.assertEqual(self.result["scope"],
                         "DECLARED_FIVE_ARTIFACT_NATIVE_RECORD_SEARCH_NOT_ARCHIVE_WIDE")
        self.assertEqual(self.result["computed"]["artifacts_checked"],5)
        self.assertEqual(len(self.result["artifacts"]),5)
        self.assertTrue(all(len(x["git_blob_sha"])==40 for x in self.result["artifacts"]))

    def test_no_qualified_native_joint_record_in_declared_scope(self):
        self.assertEqual(self.result["qualified_native_joint_records"],[])
        self.assertEqual(self.result["status"],
                         "NO_NATIVE_DERIVED_JOINT_RECORD_FOUND_IN_DECLARED_SCOPE")
        self.assertFalse(self.result["archive_absence_proved"])

    def test_coherent_record_state_is_supplied_diagnostic_structure(self):
        x=self.result["by_key"]["coherent_records"]
        self.assertEqual(x["joint_state_status"],"JOINT_STATE_PRESENT")
        self.assertEqual(x["provenance_status"],"SUPPLIED_DIAGNOSTIC_STRUCTURE")
        self.assertFalse(x["native_derived"])

    def test_partial_pruning_reuses_supplied_encoding(self):
        x=self.result["by_key"]["partial_pruning"]
        self.assertEqual(x["joint_state_status"],"INHERITED_JOINT_ENCODING")
        self.assertEqual(x["provenance_status"],"SUPPLIED_REDUCTION_CHOICE")
        self.assertFalse(x["native_derived"])

    def test_event_records_are_supplied_not_derived(self):
        for key in ("independent_events","record_dependencies"):
            x=self.result["by_key"][key]
            self.assertEqual(x["provenance_status"],"SUPPLIED_EVENT_RECORD_MODEL")
            self.assertFalse(x["native_derived"])

    def test_carrier_origin_is_an_explicit_obstruction(self):
        x=self.result["by_key"]["carrier_origin"]
        self.assertEqual(x["joint_state_status"],"NO_NATIVE_CARRIER_DERIVATION")
        self.assertEqual(x["provenance_status"],"FROZEN_NEGATIVE_GATE")
        self.assertFalse(x["native_derived"])

    def test_claim_boundary(self):
        self.assertEqual(self.result["source_correspondence"],"NOT_EVALUATED")
        self.assertEqual(self.result["Pillar_3"],"OPEN")
        self.assertFalse(self.result["physical_source_law_adopted"])
        self.assertFalse(self.result["geometry_executed"])

    def test_source_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
            nrs.audit_scope(self.root,overrides={"coherent_records":b"drift"})

    def test_deterministic_replay(self):
        self.assertEqual(nrs.canonical_bytes(self.result),
                         nrs.canonical_bytes(nrs.audit_scope(self.root)))


if __name__=="__main__":
    unittest.main()
