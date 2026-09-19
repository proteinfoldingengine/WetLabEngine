import json
from pathlib import Path
import unittest

from connection_curvature_gate import (
    ALLOWED_GATE_STATUSES,
    audit,
    canonical_json,
    classify_gate,
    next_required_object_for_status,
)


class ConnectionCurvatureGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_evidence_and_input_separation(self):
        self.assertTrue(self.result["evidence_verified"])
        self.assertTrue(
            self.result["input_separation"]["operational_constructor_blind"]
        )
        self.assertTrue(self.result["input_separation"]["source_target_blind"])

    def test_unique_contraction_and_independent_source_target(self):
        self.assertIn(self.result["curvature_contraction_dimension"], (None, 1))
        self.assertTrue(self.result["source_target_frozen_before_adjudication"])

    def test_controls_relabeling_scale_superposition_and_holdout(self):
        self.assertEqual(self.result["projective_scales"], ["1", "7/3"])
        self.assertTrue(self.result["all_relabeling_checks_complete"])
        self.assertTrue(self.result["all_superposition_checks_complete"])
        self.assertEqual(self.result["holdout_size"], 11)

    def test_status_firewalls_and_claim_boundary(self):
        self.assertIn(self.result["status"], ALLOWED_GATE_STATUSES)
        self.assertEqual(
            self.result["status"],
            classify_gate(
                self.result["protocol_valid"],
                self.result["connection_identifiable"],
                self.result["curvature_source_map_identifiable"],
                self.result["canonical_correspondence"],
                self.result["control_all_sizes"],
            ),
        )
        self.assertEqual(
            self.result["next_required_object"],
            next_required_object_for_status(self.result["status"]),
        )
        self.assertTrue(
            all(value == 0 for value in self.result["construction_firewall"].values())
        )
        self.assertFalse(self.result["historical_connection_used_for_adjudication"])
        self.assertEqual(self.result["Pillar_3"], "OPEN")

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed, canonical_json(self.result))
        self.assertEqual(json.loads(committed), self.result)


if __name__ == "__main__":
    unittest.main()
