import copy
import importlib.util
import unittest
import numpy as np
m = None
if importlib.util.find_spec('record_readout'):
    import record_readout as m

class RecordReadoutTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m, 'record-readout model is not implemented')
    def test_frozen_baseline(self):
        self.assertEqual(m.verify_baseline()['predictor_git_blob'],'e48f19de7c74d9c7dcf917a66bf7b06138fd36eb')
    def test_first_effect_is_rank_eight_projector(self):
        f=m.first_effect()
        np.testing.assert_allclose(f@f,f,atol=1e-11)
        self.assertAlmostEqual(np.trace(f).real,8,places=11)
    def test_first_effect_sign_anticommutes_with_parity(self):
        a=2*m.first_effect()-np.eye(16);g=m.pp.gamma()
        np.testing.assert_allclose(a@g+g@a,0,atol=1e-11)
    def test_distinguishing_inputs_are_valid(self):
        for rho in m.eigenpair():
            self.assertAlmostEqual(np.trace(rho).real,1,places=11)
            self.assertGreaterEqual(np.linalg.eigvalsh(rho).min(),-1e-11)
    def test_encoding_halves_pair_distinguishability(self):
        a,b=m.eigenpair()
        self.assertAlmostEqual(m.pp.distance(a,b),1,places=11)
        self.assertAlmostEqual(m.pp.distance(m.encode(a),m.encode(b)),.5,places=11)
    def test_encoded_pair_is_full_rank(self):
        for r in m.eigenpair(): self.assertAlmostEqual(np.linalg.eigvalsh(m.encode(r)).min(),1/32,places=11)
    def test_best_one_copy_binary_error(self):
        c=m.obstruction()
        self.assertAlmostEqual(c['minimax_binary_probability_error'],.25,places=11)
        np.testing.assert_allclose(c['native_encoded_probabilities'],[.75,.25],atol=1e-11)
    def test_all_kernel_effect_extensions_fail(self):
        for c in [-10.,-1.,0.,1.,10.]:
            b=m.readout_effect(c)
            self.assertAlmostEqual(np.linalg.eigvalsh(b).min(),.5-np.sqrt(1+c*c),places=10)
            np.testing.assert_allclose(m.pp.linear_map(b,.5,0),m.first_effect(),atol=1e-10)
    def test_corrected_effect_is_not_a_probability_effect(self):
        self.assertAlmostEqual(np.linalg.eigvalsh(m.readout_effect()).min(),-.5,places=11)
        self.assertAlmostEqual(np.linalg.eigvalsh(m.readout_effect()).max(),1.5,places=11)
    def test_signed_inverse_is_not_stochastic(self):
        l=m.distribution_decoder()
        np.testing.assert_allclose(l.sum(axis=0),np.ones(16),atol=1e-11)
        self.assertAlmostEqual(l.min(),-1/16)
    def test_full_history_effects_are_complete_and_parity_blind(self):
        for s in m.adaptive.schedules():
            hs=[m.history_operator(s,f'{r:04b}').conj().T@m.history_operator(s,f'{r:04b}') for r in range(16)]
            np.testing.assert_allclose(sum(hs),np.eye(16),atol=1e-10)
            for h in hs:
                np.testing.assert_allclose(h@h,h,atol=1e-11)
                self.assertLess(abs(np.trace(m.pp.gamma()@h)),1e-11)
    def test_every_nonempty_branch_kills_parity(self):
        for s in m.adaptive.schedules():
            for i in range(1,5):
                for r in range(16):
                    k=m.history_operator(s[:i],f'{r:04b}')
                    self.assertLess(np.linalg.norm(k@m.pp.gamma()@k.conj().T),1e-11)
    def test_joint_probability_noise_and_decode(self):
        for rho in m.inputs().values():
            for s in m.adaptive.schedules():
                d=m.history_distribution(rho,s)
                np.testing.assert_allclose(d['raw'],.5*np.array(d['ideal'])+1/32,atol=1e-11)
                np.testing.assert_allclose(d['decoded'],d['ideal'],atol=1e-11)
    def test_joint_distribution_normalization(self):
        for rho in m.inputs().values():
            d=m.history_distribution(rho,m.adaptive.schedules()[0])
            self.assertAlmostEqual(sum(d['ideal']),1,places=10)
            self.assertAlmostEqual(sum(d['raw']),1,places=10)
    def test_peak_record_probability_not_binary_bound(self):
        rho=m.inputs()['basis_0000'];d=m.history_distribution(rho,m.adaptive.schedules()[0])
        self.assertAlmostEqual(d['ideal'][0],1,places=10)
        self.assertAlmostEqual(d['raw'][0],17/32,places=10)
    def test_decode_joint_masses_before_conditioning(self):
        for s in m.adaptive.schedules():
            for r in range(16):
                for row in m.path_rows(m.pp.fixture(),s,f'{r:04b}'):
                    self.assertAlmostEqual(row['decoded_conditional'],row['ideal_conditional'],places=10)
    def test_naive_local_gain_is_wrong_after_conditioning(self):
        self.assertGreater(m.audit()['max_naive_conditional_error'],.01)
    def test_formal_branch_computation_matches_on_image(self):
        c=m.formal_control()
        self.assertLess(c['max_on_image_branch_error'],1e-11)
        self.assertGreater(c['outside_image_negative_branch_weight_magnitude'],.1)
    def test_finite_copy_error_is_positive_not_exact_recovery(self):
        self.assertAlmostEqual(m.copy_error(1),.25)
        self.assertAlmostEqual(m.copy_error(3),.15625)
        self.assertGreater(m.copy_error(15),0)
        self.assertLess(m.copy_error(15),m.copy_error(3))
    def test_invalid_copy_count_rejected(self):
        for n in [0,True,-1,1.5]:
            with self.assertRaises(ValueError):m.copy_error(n)
    def test_invalid_states_rejected(self):
        for rho in [np.eye(2),np.eye(16),np.eye(16)*np.nan]:
            with self.assertRaises(ValueError):m.encode(rho)
    def test_premature_schedule_and_bad_records_rejected(self):
        with self.assertRaises(ValueError):m.history_operator(('B2',),'1001')
        with self.assertRaises(ValueError):m.history_operator(('A1',),'10x1')
    def test_zero_parent_never_silently_selects(self):
        with self.assertRaises(ValueError):m.conditional(0.,0.)
    def test_no_negative_decoded_estimates_clipped(self):
        d=m.distribution_decoder()@np.eye(16)[0]
        self.assertLess(d.min(),0)
    def test_all_cases_complete_and_fail_closed(self):
        a=m.audit();self.assertEqual(a['full_history_probabilities_checked'],1440)
        self.assertEqual(a['fixture_conditional_checks'],320)
        bad=copy.deepcopy(a);bad['max_decoded_joint_error']=float('nan')
        with self.assertRaises(AssertionError):m.verify_result(bad)
    def test_claim_boundaries_checked(self):
        a=m.audit();self.assertIsNone(a['actual_record_selected']);self.assertIsNone(a['physical_duration'])
        self.assertFalse(a['physical_pruning_law_derived'])
        self.assertEqual(a['new_physical_axioms'],[])
        bad=copy.deepcopy(a);bad['single_copy_event_channel_derived']=True
        with self.assertRaises(AssertionError):m.verify_result(bad)

if __name__=='__main__':unittest.main(verbosity=2)
