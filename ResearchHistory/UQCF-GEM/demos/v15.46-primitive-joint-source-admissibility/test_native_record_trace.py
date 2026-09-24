"""Stage B RED tests: fail-closed native-record trace for the strongest existing joint-state candidate."""
from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path

import native_record_trace as nrt


class NativeRecordTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[4]
        cls.result = nrt.trace_candidate(cls.root)

    def test_candidate_identity_and_source_pin(self):
        self.assertEqual(self.result["candidate"], "V13_27_SIX_QUBIT_THERMAL_DEMO")
        self.assertEqual(self.result["source"]["git_blob_sha"],
                         "bf0b84e3b3e627d7916a5fb1b46ab9bd5eba03e6")
        self.assertEqual(self.result["source"]["path"],
                         "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py")

    def test_joint_state_is_supplied_not_native_derived(self):
        p = self.result["stages"]["joint_state_provenance"]
        self.assertTrue(p["joint_state_constructed"])
        self.assertEqual(p["construction"], "NORMALIZED_EXP_MINUS_BETA_H")
        self.assertEqual(p["provenance"], "SUPPLIED_DEMO_MODEL")
        self.assertFalse(p["native_derivation_certified"])

    def test_trace_fails_at_first_unearned_interface(self):
        self.assertEqual(self.result["status"],
                         "SUPPLIED_JOINT_STATE_PRESENT_NATIVE_PROVENANCE_UNESTABLISHED")
        self.assertEqual(self.result["first_unmet_stage"], "B1_NATIVE_JOINT_STATE_PROVENANCE")
        self.assertFalse(self.result["interface_admitted"])
        self.assertEqual(self.result["later_stages"], "NOT_EXECUTED_AFTER_FIRST_FAILURE")

    def test_no_subsystem_or_incidence_choices_are_invented(self):
        self.assertEqual(self.result["stages"]["overlap_inclusions"]["status"],
                         "NOT_EXECUTED_AFTER_FIRST_FAILURE")
        self.assertEqual(self.result["stages"]["support_domain"]["status"],
                         "NOT_EXECUTED_AFTER_FIRST_FAILURE")
        self.assertEqual(self.result["stages"]["occurrence_link"]["status"],
                         "NOT_EXECUTED_AFTER_FIRST_FAILURE")
        self.assertEqual(self.result["stages"]["coupling_law"]["status"],
                         "NOT_EXECUTED_AFTER_FIRST_FAILURE")

    def test_claim_boundary(self):
        claims=self.result["claims"]
        self.assertEqual(claims["source_correspondence"], "NOT_EVALUATED")
        self.assertEqual(claims["Pillar_3"], "OPEN")
        self.assertFalse(claims["physical_source_law_adopted"])
        self.assertFalse(claims["physical_gravity"])
        self.assertFalse(claims["full_v1546_certification"])

    def test_static_source_drift_fails_closed(self):
        source=(self.root/self.result["source"]["path"])
        raw=source.read_bytes()+b"\n# drift\n"
        with self.assertRaisesRegex(ValueError,"candidate_blob_mismatch"):
            nrt.trace_candidate(self.root, source_bytes=raw)

    def test_replay_is_deterministic(self):
        self.assertEqual(nrt.canonical_bytes(self.result),
                         nrt.canonical_bytes(nrt.trace_candidate(self.root)))


if __name__ == "__main__":
    unittest.main()
