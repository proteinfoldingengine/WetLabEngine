import json
from pathlib import Path
import unittest

from geometry_specificity_gate import (
    ALLOWED_GATE_STATUSES,
    CONTROL_KEYS,
    audit,
    canonical_json,
    classify_gate,
    next_required_object_for_status,
)


class GlobalBalanceGeometrySpecificityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_evidence_and_exact_generation_protocol(self):
        self.assertTrue(self.result["evidence_verified"])
        self.assertTrue(self.result["canonical_augmentation_isomorphism_exact"])
        self.assertTrue(self.result["all_response_equations_exact"])

    def test_response_geometry_is_blind_exact_and_total(self):
        self.assertTrue(self.result["input_separation"]["response_constructor_blind"])
        self.assertTrue(self.result["all_required_pairs_evaluated"])
        self.assertTrue(self.result["all_required_ordered_triples_evaluated"])

    def test_incidence_target_is_blind_four_regular_and_connected(self):
        self.assertTrue(self.result["input_separation"]["target_constructor_blind"])
        self.assertTrue(self.result["all_targets_four_regular"])
        self.assertTrue(self.result["all_targets_connected"])

    def test_orientation_additivity_covariance_and_relabeling(self):
        self.assertTrue(self.result["all_orientation_rays_exact"])
        self.assertTrue(self.result["all_additivity_exact"])
        self.assertTrue(self.result["all_translation_D4_covariance_exact"])
        self.assertTrue(self.result["all_relabeling_equivariant"])

    def test_projective_scale_and_holdout_rules(self):
        self.assertEqual(self.result["projective_scales"], ["1", "7/3"])
        self.assertTrue(self.result["all_scale_verdicts_identical"])
        self.assertEqual(self.result["holdout_size"], 11)
        self.assertTrue(self.result["holdout_formula_unchanged"])

    def test_controls_and_mechanical_correspondence(self):
        self.assertEqual(tuple(self.result["control_keys"]), CONTROL_KEYS)
        self.assertTrue(self.result["matched_controls_structurally_admissible"])
        self.assertTrue(self.result["mechanical_correspondence_rule_applied"])

    def test_status_and_next_object_are_mechanical(self):
        self.assertIn(self.result["status"], ALLOWED_GATE_STATUSES)
        self.assertEqual(
            self.result["next_required_object"],
            next_required_object_for_status(self.result["status"]),
        )

    def test_construction_and_interpretation_firewalls(self):
        self.assertTrue(all(value == 0 for value in self.result["construction_firewall"].values()))
        self.assertFalse(self.result["physical_metric_derived"])
        self.assertFalse(self.result["scientific_breakthrough"])
        self.assertEqual(self.result["Pillar_3"], "OPEN")

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed, canonical_json(self.result))
        self.assertEqual(json.loads(committed), self.result)


if __name__ == "__main__":
    unittest.main()
