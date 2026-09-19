from __future__ import annotations

import json
from pathlib import Path
import unittest

from source_axiom_canary import CANDIDATE_KEYS, audit, canonical_json


ALLOWED_CANDIDATE_VERDICTS = {
    "STRUCTURALLY_REJECTED",
    "STRUCTURAL_ONLY_LOCAL",
    "PRETIME_GLOBAL_ORGANIZATION_SURVIVES",
}

ALLOWED_GATE_STATUSES = {
    "SOURCE_AXIOM_PROTOCOL_INVALID",
    "NO_ADMISSIBLE_RESPONSE_CANDIDATE",
    "ADMISSIBLE_CANDIDATES_NO_GLOBAL_SIGNAL",
    "AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL",
}


def contains_float(value):
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(contains_float(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(contains_float(v) for v in value)
    return False


class HigherIncidenceSourceAxiomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_source_lift_typing_covariance_and_composition(self):
        protocol = self.result["source_protocol"]
        self.assertTrue(protocol["all_B1_kappa_zero"])
        self.assertTrue(protocol["generator_covariance_exact"])
        self.assertTrue(protocol["source_additivity_exact"])
        self.assertTrue(protocol["source_reversal_exact"])
        self.assertEqual(protocol["source_carrier"], "Q_PLUS_BOUNDARY_INCIDENCE_PROVENANCE")

    def test_closed_face_q_null_is_fiber_nonnull(self):
        protocol = self.result["source_protocol"]
        self.assertTrue(protocol["closed_face_coarse_q_null"])
        self.assertTrue(protocol["closed_face_higher_incidence_source_nonnull"])
        self.assertEqual(protocol["closed_face_kappa_multiple"], 4)
        self.assertTrue(self.result["closed_face_null_reinterpreted_by_new_axiom"])

    def test_exact_chain_sector_and_adjacency_contract(self):
        protocol = self.result["source_protocol"]
        self.assertTrue(protocol["all_B1_B2_zero"])
        self.assertTrue(protocol["canonical_cycle_boundary_homology_split_exact"])
        self.assertTrue(protocol["adjacency_preserves_boundary_sector_exact"])
        for row in self.result["size_audits"]:
            L = row["L"]
            self.assertTrue(row["B1_B2_zero"])
            self.assertEqual(row["cycle_dimension"], L * L + 1)
            self.assertEqual(row["boundary_dimension"], L * L - 1)
            self.assertEqual(row["homology_dimension"], 2)
            self.assertTrue(row["canonical_cycle_boundary_homology_split_exact"])
            self.assertTrue(row["adjacency_preserves_boundary_sector_exact"])

    def test_candidate_formulas_and_balance_uniqueness(self):
        self.assertEqual(tuple(self.result["candidate_keys"]), CANDIDATE_KEYS)
        formulas = self.result["candidate_formula_manifest"]
        self.assertEqual(formulas, {
            "DIRECT_INHERITANCE": "y=kappa",
            "ONE_INCIDENCE_TRANSPORT": "y=A*kappa",
            "GLOBAL_BALANCE_COMPLETION": "(4I-A)y=kappa_on_imB2",
        })
        self.assertTrue(self.result["all_candidate_outputs_in_boundary_sector"])
        self.assertTrue(self.result["global_balance_boundary_inverse_exact"])
        self.assertFalse(self.result["ambient_pseudoinverse_used"])

    def test_exact_remote_and_commutator_predicates(self):
        self.assertTrue(self.result["exact_zero_nonzero_predicates_only"])
        self.assertEqual(self.result["candidate_specific_thresholds"], 0)
        self.assertEqual(self.result["accepted_candidate_spectrum_queries"], 0)
        self.assertEqual(self.result["accepted_candidate_spectral_edge_parameters"], 0)
        self.assertTrue(self.result["commuting_axis_precursor_zero"])
        self.assertFalse(contains_float(self.result))

    def test_multisize_holdout_and_mechanical_verdicts(self):
        self.assertEqual(self.result["finite_size_controls"], [5, 7, 9, 11])
        self.assertEqual(self.result["holdout_size"], 11)
        self.assertTrue(self.result["holdout_formula_unchanged"])
        self.assertTrue(self.result["mechanical_candidate_rule_applied"])
        self.assertEqual(set(self.result["candidate_verdicts"]), set(CANDIDATE_KEYS))
        self.assertTrue(set(self.result["candidate_verdicts"].values()) <= ALLOWED_CANDIDATE_VERDICTS)
        self.assertIn(self.result["status"], ALLOWED_GATE_STATUSES)
        survivor_count = sum(
            value == "PRETIME_GLOBAL_ORGANIZATION_SURVIVES"
            for value in self.result["candidate_verdicts"].values()
        )
        self.assertEqual(self.result["global_survivor_count"], survivor_count)
        self.assertEqual(
            self.result["pretime_global_organization_signal"],
            survivor_count > 0,
        )
        for size_row in self.result["size_audits"]:
            for row in size_row["candidate_rows"]:
                orientation_structural = all(
                    orientation["response_nonzero"]
                    and orientation["boundary_sector"]
                    and orientation["B1_response_zero"]
                    and orientation["unique_response_ray"]
                    and orientation["candidate_equation_exact"]
                    and orientation["lambda_closure_exact"]
                    and orientation["projective_scale_predicates_exact"]
                    for orientation in row["orientation_rows"]
                )
                expected_structural = all((
                    size_row["B1_B2_zero"],
                    size_row["canonical_cycle_boundary_homology_split_exact"],
                    size_row["adjacency_preserves_boundary_sector_exact"],
                    row["response_covariance_exact"],
                    row["response_reversal_exact"],
                    row["response_additivity_exact"],
                    row["translation_remote_metrics_exact"],
                    orientation_structural,
                ))
                self.assertEqual(row["structural_checks_pass"], expected_structural)
                expected_verdict = (
                    "STRUCTURALLY_REJECTED"
                    if not expected_structural
                    else "PRETIME_GLOBAL_ORGANIZATION_SURVIVES"
                    if row["remote_support_all_orientations"]
                    and row["remote_commutator_all_orientations"]
                    else "STRUCTURAL_ONLY_LOCAL"
                )
                self.assertEqual(row["size_verdict"], expected_verdict)

    def test_projective_scale_and_hostile_controls(self):
        self.assertTrue(self.result["projective_scale_discipline_enforced"])
        self.assertFalse(self.result["absolute_response_scale_derived"])
        self.assertTrue(self.result["lambda_closure_exact_for_tested_scales"])
        self.assertTrue(self.result["projective_verdict_scale_invariant"])
        self.assertTrue(all(self.result["hostile_controls"].values()))

    def test_axiom_and_claim_firewall(self):
        self.assertTrue(self.result["new_source_semantics_axiom_added"])
        self.assertTrue(self.result["new_response_axiom_candidates_tested"])
        self.assertFalse(self.result["source_axiom_derived_from_frozen_ontology"])
        self.assertTrue(self.result["source_axiom_user_approved_before_execution"])
        for key in (
            "physical_gravity_derived",
            "gravity_canary_certified",
            "einstein_equations_derived",
            "continuum_limit_derived",
            "uses_pruning",
            "uses_entropy",
            "uses_physical_time",
            "uses_metric_selector",
            "uses_holonomy_selector",
            "uses_newton_or_gr_selector",
            "scientific_breakthrough",
        ):
            self.assertFalse(self.result[key], key)
        self.assertEqual(self.result["Pillar_3"], "OPEN")

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed, canonical_json(self.result))
        self.assertEqual(json.loads(committed), self.result)


if __name__ == "__main__":
    unittest.main()
