import importlib.util
import unittest
import numpy as np

if importlib.util.find_spec('coherent_records'):
    import coherent_records as m
else:
    m=None

class CoherentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=m.audit() if m else None
    def setUp(self):
        self.assertIsNotNone(m,'coherent comparison not implemented')
    def test_unchanged_baseline(self):
        self.assertEqual(m.verify_baseline()['adaptive.py'],'44a87e4cc5bcf531ef7798aadab5d9dbba3482cb')
    def test_five_schedules(self):
        self.assertEqual(len(m.prior.schedules()),5)
    def test_gate_unitaries(self):
        for e in m.EVENTS:
            g=m.event_gate(e)
            np.testing.assert_allclose(g.conj().T@g,np.eye(256),atol=1e-11)
    def test_copy_gate_is_involution(self):
        for e in m.EVENTS:
            c=m.copy_gate(e)
            np.testing.assert_array_equal(c@c,np.eye(256))
    def test_coherent_controller_uses_both_values(self):
        g=m.controller_gate('B2')
        np.testing.assert_allclose(g[:16,:16],m.prior.instrument('B2',{'A1':0,'B1':0}),atol=1e-12)
        np.testing.assert_allclose(g[128:144,128:144],m.prior.instrument('B2',{'A1':1,'B1':0}),atol=1e-12)
    def test_isometric_encoding(self):
        for s in m.prior.schedules():
            for stage in m.encoding(s):
                np.testing.assert_allclose(stage['V'].conj().T@stage['V'],np.eye(16),atol=1e-11)
    def test_branch_operator_agreement_all_inputs(self):
        self.assertEqual(self.result['final_branch_maps_compared'],80)
        self.assertEqual(self.result.get('prefix_branch_maps_compared'),155)
        self.assertLess(self.result['max_branch_operator_error'],1e-11)
        self.assertLess(self.result['max_labeled_choi_error'],1e-11)
    def test_common_ideals_same_encoding(self):
        self.assertEqual(self.result['common_ideals'],8)
        self.assertLess(self.result['max_shared_encoding_error'],1e-11)
    def test_fixture_weights_and_states_agree(self):
        self.assertLess(self.result['max_prior_state_error'],1e-11)
        self.assertLess(self.result['max_prior_mass_error'],1e-11)
    def test_eventwise_and_deferred_pinching(self):
        self.assertLess(self.result['max_deferred_pinching_error'],1e-11)
    def test_pinching_changes_no_record_probability(self):
        self.assertLess(self.result['max_record_probability_error'],1e-11)
    def test_full_inverse_restores_input(self):
        self.assertLess(self.result['echo']['coherent_inverse_error'],1e-11)
    def test_inverse_does_not_restore_pinched_fixture(self):
        self.assertGreater(self.result['echo']['pinched_inverse_distance'],.05)
    def test_strong_unrecoverability_witness(self):
        w=self.result['distinguishability_witness']
        self.assertAlmostEqual(w['input_distance'],1.,places=11)
        self.assertAlmostEqual(w['coherent_output_distance'],1.,places=11)
        self.assertLess(w['pinched_output_distance'],1e-11)
    def test_reduced_memory_is_not_joint_coherence(self):
        r=self.result['echo']
        self.assertLess(r['memory_marginal_offdiagonal_norm'],1e-11)
        self.assertGreater(r['joint_record_offdiagonal_norm'],.1)
    def test_classical_alternatives_do_not_select_actuality(self):
        self.assertIsNone(self.result['actual_record_selected'])
    def test_phase_variation_preserves_labeled_channel_not_coherent_state(self):
        r=self.result['phase_control']
        self.assertLess(r['labeled_channel_error'],1e-11)
        self.assertGreater(r['coherent_state_distance'],.01)
    def test_wrong_controller_detected(self):
        r=self.result['wrong_controller_control']
        self.assertGreater(r['max_labeled_choi_error'],.01)
    def test_bad_schedule_rejected(self):
        with self.assertRaises(ValueError):m.encoding(('B1','B2','A1','A2'))
    def test_record_assignment_validation(self):
        for bad in (None,'10x1','101'):
            with self.assertRaises(ValueError):m.branch_operator(m.prior.schedules()[0],bad)
    def test_pinching_validation(self):
        with self.assertRaises(ValueError):m.pinch_records(np.eye(4))
    def test_scope(self):
        self.assertEqual(self.result['new_physical_axioms'],[])
        self.assertIsNone(self.result['physical_duration'])
        self.assertFalse(self.result['objective_collapse_derived'])
        self.assertFalse(self.result['physical_entropy_production_derived'])
        self.assertEqual(self.result['Pillar_3'],'OPEN')
    def test_fail_closed_verification(self):
        bad=dict(self.result);bad['max_branch_operator_error']=.1
        with self.assertRaises(AssertionError):m.verify_result(bad)
    def test_outcome_distribution_normalizes(self):
        self.assertLess(self.result['max_distribution_normalization_error'],1e-11)

if __name__=='__main__':unittest.main(verbosity=2)
