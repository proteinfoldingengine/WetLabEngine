"""Regression checks for ontology continuity, not tests of a physical theory."""
import importlib.util
import math
import unittest
from pathlib import Path

import numpy as np

spec = importlib.util.find_spec('ontology_continuity_audit')
if spec is not None:
    import ontology_continuity_audit as audit
else:
    audit = None


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(audit, 'ontology_continuity_audit is not implemented')

    def test_pretime_motion_changes_state_and_has_inverse(self):
        r = audit.motion_control()
        self.assertGreater(r['state_change'], 0.1)
        self.assertLess(r['inverse_error'], 1e-12)
        self.assertLess(r['composition_error'], 1e-12)

    def test_ras_noninjectivity_does_not_require_state_rank_decrease(self):
        r = audit.pruning_control()
        self.assertAlmostEqual(r['input_trace_distance'], 1.0)
        self.assertLess(r['output_trace_distance'], 1e-12)
        self.assertEqual(r['input_ranks'], [1, 1])
        self.assertEqual(r['output_ranks'], [2, 2])
        self.assertEqual(r['channel_kernel_dimension'], 2)

    def test_conditional_expectation_is_idempotent_and_cptp(self):
        r = audit.pruning_control()
        self.assertLess(r['idempotence_error'], 1e-12)
        self.assertLess(r['trace_error'], 1e-12)
        self.assertGreaterEqual(r['minimum_choi_eigenvalue'], -1e-12)

    def test_frame_covariance_does_not_choose_an_axis(self):
        self.assertLess(audit.pruning_control()['covariance_error'], 1e-12)

    def test_fixed_points_and_repeated_projection_are_not_new_strict_loss(self):
        r = audit.pruning_control()
        self.assertLess(r['fixed_point_change'], 1e-12)
        self.assertLess(r['repeat_change'], 1e-12)

    def test_same_channel_has_different_instrument_records(self):
        r = audit.record_control()
        self.assertLess(r['instrument_channel_error'], 1e-12)
        np.testing.assert_allclose(r['projective_weights'], [.6, .4])
        np.testing.assert_allclose(r['random_unitary_weights'], [.5, .5])

    def test_actuality_is_not_selected_automatically(self):
        with self.assertRaises(ValueError):
            audit.select_record(np.eye(2)/2, [np.diag([1.,0.]), np.diag([0.,1.])])

    def test_zero_weight_record_is_rejected(self):
        with self.assertRaises(ValueError):
            audit.select_record(np.diag([1.,0.]), [np.diag([1.,0.]), np.diag([0.,1.])], 1)

    def test_compatible_record_refinement_forms_poset(self):
        r = audit.history_control()
        self.assertTrue(r['antisymmetric'])
        self.assertTrue(r['transitive'])
        self.assertEqual(r['maximal_record_chains'], 4)
        self.assertEqual(r['strict_record_rank_chain'], [4, 2, 1])
        self.assertEqual(r['incomparable_coarse_pair'], ['A', 'B'])

    def test_nested_selective_conditioning_composes(self):
        self.assertLess(audit.history_control()['selective_composition_error'], 1e-12)

    def test_nested_algebras_do_not_automatically_retain_old_center(self):
        r = audit.center_persistence_control()
        self.assertLess(r['nested_expectation_error'], 1e-12)
        self.assertAlmostEqual(r['old_record_erasure_norm'], 1.0)
        self.assertEqual(r['old_center_dimension'], 2)
        self.assertEqual(r['new_center_dimension'], 1)

    def test_independent_events_are_not_given_global_clock_order(self):
        r = audit.history_control()
        self.assertEqual(r['independent_two_chain_linear_extensions'], 6)
        self.assertLess(r['commuting_pruning_error'], 1e-12)

    def test_duration_freedom_survives_one_common_unit(self):
        r = audit.duration_control()
        self.assertAlmostEqual(r['D2_normalized'][0], 1.0)
        self.assertAlmostEqual(r['D3_normalized'][0], 1.0)
        self.assertGreater(r['normalized_interval_separation'], .05)

    def test_environment_information_is_not_silently_discarded(self):
        r = audit.scope_control()
        self.assertLess(r['retained_output_distance'], 1e-12)
        self.assertAlmostEqual(r['joint_output_distance'], 1.0)
        self.assertLess(r['joint_inverse_error'], 1e-12)
        self.assertLess(r['classical_record_output_distance'], 1e-12)

    def test_entropy_diagnostics_do_not_define_time_or_a_second_law(self):
        r = audit.scope_control()
        self.assertAlmostEqual(r['nonselective_entropy'], math.log(2))
        self.assertAlmostEqual(r['selected_entropy'], 0.0)
        self.assertAlmostEqual(r['neutral_state_entropy'], math.log(2))

    def test_noninjectivity_alone_does_not_prove_acyclic_order(self):
        r = audit.noninjective_cycle_control()
        self.assertFalse(r['injective'])
        self.assertTrue(r['two_cycle_exists'])

    def test_failed_checks_cannot_become_opposite_scientific_outcome(self):
        self.assertEqual(audit.adjudicate(False), 'VERIFICATION_FAILED_NO_SCIENTIFIC_ADJUDICATION')
        self.assertEqual(audit.adjudicate(True), 'CONTINUITY_RESTORED_CONDITIONAL_ORDINAL_ORDER_PRESERVED')

    def test_source_manifest_excerpts_are_bound(self):
        r = audit.verify_sources(Path(__file__).with_name('SOURCE_MANIFEST.json'))
        self.assertEqual(r['source_count'], 7)
        self.assertTrue(r['excerpt_hashes_valid'])
        self.assertFalse(r['original_bytes_checked'])

    def test_no_new_physical_selector_is_adopted(self):
        r = audit.run_audit()
        self.assertEqual(r['new_physical_axioms_adopted'], [])
        self.assertEqual(r['RAS'], 'EXISTING_EXPLICIT_PRIMITIVE_NOT_DERIVED')
        self.assertEqual(r['RCR'], 'EXISTING_EXPLICIT_PRIMITIVE_NOT_DERIVED')
        self.assertFalse(r['physical_entropy_law_derived'])
        self.assertFalse(r['unconditional_metric_time_derived'])
        self.assertEqual(r['Pillar_3'], 'OPEN')
        self.assertFalse(r['scientific_breakthrough'])

    def test_invalid_pinching_does_not_silently_become_measurement(self):
        with self.assertRaises(ValueError):
            audit.pinch(np.eye(2)/2, [np.eye(2), np.eye(2)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
