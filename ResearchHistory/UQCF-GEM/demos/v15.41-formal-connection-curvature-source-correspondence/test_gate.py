import json
from pathlib import Path
import ast
import unittest

from connection_curvature_gate import (
    ALLOWED_GATE_STATUSES,
    _audit,
    audit,
    canonical_json,
    classify_gate,
    next_required_object_for_status,
)
from response_inputs import family_input, source_target_input
from source_target import construct_source_target


class ConnectionCurvatureGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_erratum_stops_before_scientific_adjudication(self):
        self.assertFalse(self.result["protocol_valid"])
        self.assertEqual(self.result["status"], "PROTOCOL_INVALID")
        self.assertEqual(
            self.result["next_required_object"],
            "REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION",
        )
        for key in (
            "connection_identifiable",
            "curvature_source_map_identifiable",
            "canonical_correspondence",
            "control_all_sizes",
        ):
            self.assertIsNone(self.result[key])

    def test_failed_protocol_never_calls_scientific_adjudicator(self):
        def forbidden(*_args, **_kwargs):
            raise AssertionError(
                "scientific adjudicator called after protocol failure"
            )

        result = _audit(adjudicator=forbidden)
        self.assertEqual(result["status"], "PROTOCOL_INVALID")

    def test_prior_result_and_diagnostics_are_non_authoritative(self):
        receipt = self.result["superseded_execution_receipt"]
        self.assertEqual(
            receipt["status"],
            "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE",
        )
        self.assertFalse(receipt["authoritative"])
        diagnostics = self.result["non_adjudicating_protocol_diagnostics"]
        self.assertEqual(
            diagnostics["label"], "NON_ADJUDICATING_PROTOCOL_DIAGNOSTIC"
        )
        self.assertTrue(diagnostics["all_tested_curvatures_zero"])

    def test_evidence_and_input_separation(self):
        self.assertTrue(self.result["evidence_verified"])
        self.assertTrue(
            self.result["input_separation"]["operational_constructor_blind"]
        )
        self.assertTrue(self.result["input_separation"]["source_target_blind"])
        sources, support = source_target_input(5)

        class HostileSequence:
            def __init__(self, permitted):
                self.permitted = permitted

            def __iter__(self):
                return iter(self.permitted)

            def __getattr__(self, name):
                raise AssertionError(f"forbidden source-target access: {name}")

        target = construct_source_target(
            HostileSequence(sources), HostileSequence(support)
        )
        self.assertEqual(
            target.neighbors,
            family_input(5, "GLOBAL_BALANCE_COMPLETION").neighbors,
        )
        tree = ast.parse(Path("source_target.py").read_text())
        imports = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        } | {
            node.module or ""
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        }
        self.assertTrue(
            imports <= {"dataclasses", "fractions", "itertools", "__future__"}
        )

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

        def contains_float(value):
            if isinstance(value, float):
                return True
            if isinstance(value, dict):
                return any(contains_float(item) for item in value.values())
            if isinstance(value, list):
                return any(contains_float(item) for item in value)
            return False

        self.assertFalse(contains_float(self.result))
        self.assertTrue(
            all(value == 0 for value in self.result["construction_firewall"].values())
        )
        expected = {
            "formal_tangent_carrier_new": True,
            "formal_connection_class_new": True,
            "formal_isotropic_lift_class_new": True,
            "formal_curvature_contraction_class_new": True,
            "historical_connection_used_for_adjudication": False,
            "physical_connection_derived": False,
            "physical_curvature_derived": False,
            "stress_energy_derived": False,
            "spacetime_derived": False,
            "continuum_limit_derived": False,
            "einstein_equations_derived": False,
            "scientific_breakthrough": False,
            "Pillar_3": "OPEN",
        }
        self.assertEqual(
            {key: self.result[key] for key in expected},
            expected,
        )


if __name__ == "__main__":
    unittest.main()
