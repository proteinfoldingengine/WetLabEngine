import json
import unittest
import coupling_gate as gate
import representation_inventory as inv


REQUIRED = {
    'version','status','base_sha','inventory_hash','q_control','candidates',
    'eligible_candidate_count','one_dimensional_candidate_count',
    'multi_dimensional_candidate_count','zero_dimensional_candidate_count',
    'blocked_candidate_count','unique_form_frozen','frozen_form','scale_resolved',
    'gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
    'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time',
    'scientific_breakthrough','signal_of_life','gravity_canary_certified',
    'Pillar_3','next_required_object'
}


class GateTests(unittest.TestCase):
    def test_q_baseline_orbit_and_character_dimensions_agree(self):
        r = gate.q_baseline_audit()
        self.assertEqual(r.dimension, 3)
        self.assertEqual(r.dimension, r.orbit_dimension)
        self.assertEqual(r.dimension, r.character_dimension)

    def test_q_basis_maps_are_exactly_cycle_valued_and_quotient_safe(self):
        r = gate.q_baseline_audit()
        for k in r.ambient_basis:
            self.assertTrue(gate.matrix_is_zero(gate.left_multiply_B1(k)))
            self.assertTrue(gate.vector_is_zero(gate.apply_to_constant(k)))

    def test_q_baseline_schema_has_no_gravity_scores(self):
        text = json.dumps(gate.q_baseline_audit().as_dict()).lower()
        for forbidden in ('holonomy','newton','einstein','inverse_square','distance_score'):
            self.assertNotIn(forbidden, text)

    def test_genesis_field_does_not_get_arbitrary_embedding(self):
        r = gate.audit_candidate(inv.by_key('genesis-6d-field'))
        self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
        self.assertIsNone(r.dimension)

    def test_retained_graph_source_current_stays_blocked_without_label_bridge(self):
        r = gate.audit_candidate(inv.by_key('retained-graph-source-current'))
        self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
        self.assertIsNone(r.dimension)

    def test_v1404_supplied_intertwiner_remains_conditional(self):
        r = gate.audit_candidate(inv.by_key('v14.04-supplied-intertwiner-control'))
        self.assertEqual(r.status, 'CONDITIONAL_ON_SUPPLIED_INTERTWINER')
        self.assertIsNone(r.dimension)
        self.assertEqual(r.metadata['supplied_link_count'], 3)
        self.assertTrue(r.metadata['inequivalent_supplied_links'])

    def test_only_q_control_is_currently_solver_eligible(self):
        rows = inv.frozen_inventory(inv.REPO_ROOT)
        self.assertEqual([r.key for r in inv.eligible_records(rows)], ['source-quotient-q-control'])

    def test_preregistered_adjudication_blocks_when_no_physical_candidate_is_eligible(self):
        self.assertEqual(gate.adjudicate(gate.audit_all_candidates()),
                         'PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK')

    def test_ledger_schema_and_claim_boundary(self):
        r = gate.audit()
        self.assertEqual(set(r), REQUIRED)
        self.assertEqual(r['status'], 'PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK')
        self.assertEqual(r['q_control']['dimension'], 3)
        self.assertEqual(r['eligible_candidate_count'], 0)
        self.assertFalse(r['unique_form_frozen'])
        self.assertIsNone(r['frozen_form'])
        self.assertFalse(r['scale_resolved'])
        for key in ('gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
                    'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time',
                    'scientific_breakthrough','signal_of_life','gravity_canary_certified'):
            self.assertFalse(r[key], key)
        self.assertEqual(r['Pillar_3'], 'OPEN')

    def test_unique_form_freeze_rejects_nonphysical_control(self):
        with self.assertRaises(ValueError):
            gate.freeze_unique_form(gate.q_baseline_audit())


if __name__ == '__main__':
    unittest.main(verbosity=2)
