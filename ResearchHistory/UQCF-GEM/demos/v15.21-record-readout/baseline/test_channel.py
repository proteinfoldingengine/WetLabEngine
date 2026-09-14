"""Physical-channel comparison tests; no empirical or collapse-law certification."""
import copy
import importlib.util
import unittest
import numpy as np
m = None
if importlib.util.find_spec('physical_predictor'):
    import physical_predictor as m

class ChannelTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(m, 'physical predictor implementation missing')

    def test_frozen_baseline(self):
        self.assertTrue(m.verify_baseline()['all_match'])
        self.assertEqual(m.verify_baseline()['python_files'],8)

    def test_pauli_basis_and_character_counts(self):
        p=m.paulis(); self.assertEqual(p.shape,(256,16,16))
        np.testing.assert_allclose(np.einsum('aij,bji->ab',p,p),16*np.eye(256),atol=1e-11)
        self.assertEqual(len(m.commuting_visible_indices()),126)
        self.assertEqual(int(np.sum(m.characters()[m.gamma_index()]<0)),128)

    def test_original_prediction_hyperplane(self):
        r=m.baseline_control()
        self.assertEqual(r['linear_dimension'],255)
        self.assertLess(r['projector_error'],1e-9)
        self.assertLess(r['motion_commutator'],1e-10)

    def test_multiplicative_domain_generators(self):
        r=m.rigidity_control()
        self.assertEqual(r['pauli_words_generated'],256)
        self.assertEqual(r['fixed_visible_generators'],8)
        self.assertLess(r['two_visible_unitaries_product_error'],1e-11)

    def test_identity_channel(self):
        r=m.fixture()
        np.testing.assert_allclose(m.apply_channel(r,1,1),r,atol=1e-11)

    def test_invalid_parameter_values(self):
        for x in (float('nan'),float('inf'),True,-.01,1.01):
            with self.assertRaises(ValueError): m.parameters(x,0)
            with self.assertRaises(ValueError): m.parameters(.5,x)

    def test_linear_map_accepts_matrix_units(self):
        e=np.zeros((16,16),complex);e[0,1]=1
        np.testing.assert_allclose(m.linear_map(e,.5,0).conj().T,m.linear_map(e.conj().T,.5,0),atol=1e-11)
        with self.assertRaises(ValueError):m.linear_map(np.eye(2),.5,0)

    def test_invalid_physical_channel_rejected(self):
        with self.assertRaises(ValueError):m.apply_channel(m.fixture(),1,0)
        with self.assertRaises(ValueError):m.channel_kraus(.5001,0)

    def test_raw_projection_matches_prior(self):
        rho=m.y_product_state();g=m.gamma()
        expected=rho-np.trace(g@rho)*g/16
        np.testing.assert_allclose(m.linear_map(rho,1,0),expected,atol=1e-11)
        self.assertAlmostEqual(np.linalg.eigvalsh(expected).min(),-1/16,places=11)

    def test_normalized_choi_eigenvalues_independent(self):
        for lam,t in ((1,1),(1,0),(.5,0),(.75,.5),(.2,.8)):
            j=m.choi_from_action(lambda a:m.linear_map(a,lam,t))
            np.testing.assert_allclose(np.linalg.eigvalsh(j),np.sort(m.pauli_weights(lam,t)),atol=1e-11)
            self.assertAlmostEqual(np.trace(j).real,1,places=11)

    def test_raw_projection_choi_has_127_negative_directions(self):
        q=m.pauli_weights(1,0)
        self.assertEqual(int(np.sum(q<0)),127)
        self.assertAlmostEqual(q.min(),-1/256,places=11)

    def test_cp_boundary_and_kraus_completeness(self):
        for t in np.linspace(0,1,9):
            lam=(1+t)/2;ks=m.channel_kraus(lam,float(t))
            np.testing.assert_allclose(sum(k.conj().T@k for k in ks),np.eye(16),atol=1e-11)
            np.testing.assert_allclose(sum(k@k.conj().T for k in ks),np.eye(16),atol=1e-11)
            if t<1:self.assertLess(m.pauli_weights(lam+.00001,float(t)).min(),0)

    def test_kraus_and_formula_routes_match(self):
        r=m.fixture()
        for lam,t in ((.5,0),(.75,.5),(.1,0),(1,1)):
            out=m.from_kraus(r,m.channel_kraus(lam,t))
            np.testing.assert_allclose(out,m.apply_channel(r,lam,t),atol=1e-11)

    def test_all_pauli_transfer_coefficients(self):
        for lam,t in ((.5,0),(.7,.4),(1,1)):
            for k,p in enumerate(m.paulis()):
                scale=1 if k==0 else t if k==m.gamma_index() else lam
                np.testing.assert_allclose(m.linear_map(p,lam,t),scale*p,atol=1e-11)

    def test_positive_noisy_representative(self):
        for rho in (m.fixture(),m.y_product_state(),*m.parity_twins()):
            out=m.apply_channel(rho,.5,0)
            self.assertGreaterEqual(np.linalg.eigvalsh(out).min(),-1e-11)
            self.assertAlmostEqual(np.trace(out).real,1,places=11)

    def test_unused_parity_is_erased(self):
        a,b=m.parity_twins()
        self.assertAlmostEqual(m.distance(a,b),1,places=11)
        self.assertLess(m.distance(m.apply_channel(a,.5,0),m.apply_channel(b,.5,0)),1e-11)

    def test_visible_feature_attenuation_and_readout(self):
        p=m.paulis()[m.labels().index('XIII')];rho=(np.eye(16)+p)/16
        out=m.apply_channel(rho,.5,0)
        self.assertAlmostEqual(np.trace(p@out).real,.5,places=11)
        self.assertAlmostEqual(m.decode_expectation(p,out,.5),1,places=11)

    def test_nontraceless_observable_readout(self):
        p=m.paulis()[m.labels().index('XIII')];a=(np.eye(16)+p)/2
        rho=m.fixture();out=m.apply_channel(rho,.5,0)
        self.assertAlmostEqual(m.decode_expectation(a,out,.5),np.trace(a@rho).real,places=11)

    def test_parity_and_zero_gain_not_decoded(self):
        with self.assertRaises(ValueError):m.decode_expectation(m.gamma(),m.fixture(),.5)
        with self.assertRaises(ValueError):m.decode_expectation(np.eye(16),m.fixture(),0)

    def test_noisy_map_commutes_with_frozen_motion(self):
        r=m.fixture()
        for u in m.frozen_motions():
            np.testing.assert_allclose(m.apply_channel(u@r@u.conj().T,.5,0),u@m.apply_channel(r,.5,0)@u.conj().T,atol=1e-10)

    def test_all_original_targets_predict_correctly(self):
        r=m.prediction_control()
        self.assertEqual(r['mask_count'],14)
        self.assertEqual(r['word_checkpoints'],13)
        self.assertGreater(r['observable_predictions_checked'],2000)
        self.assertLess(r['max_decoded_error'],1e-10)
        self.assertGreater(r['max_direct_readout_error'],.01)

    def test_compressed_register_cannot_be_recovered_by_readout_gain(self):
        r=m.rigidity_control()
        self.assertEqual(r['minimum_output_hilbert_dimension_with_common_cptp_recovery'],16)
        rho=m.y_product_state();sigma=m.apply_channel(rho,.5,0)
        signed=2*sigma-np.eye(16)/16
        self.assertLess(np.linalg.eigvalsh(signed).min(),-.06)

    def test_pauli_twirl_formula_on_nonunital_channel(self):
        ks=m.amplitude_damping_kraus(.37);r=m.twirl_certificate(ks)
        self.assertGreater(r['unital_error'],.1)
        self.assertLess(r['max_diagonal_transfer_error'],1e-10)
        self.assertLessEqual(r['mean_commuting_visible_gain'],r['bound']+1e-10)

    def test_nonpauli_unitary_twirl(self):
        r=m.twirl_certificate([m.frozen_motions()[0]])
        self.assertLess(r['max_diagonal_transfer_error'],1e-10)
        self.assertLessEqual(r['mean_commuting_visible_gain'],r['bound']+1e-10)

    def test_exact_character_sum_certificate(self):
        char=m.characters();vis=m.commuting_visible_indices();g=m.gamma_index()
        sums=char[:,vis].sum(axis=1)
        for k in range(256):
            expected=126 if k in (0,g) else -2 if char[k,g]==1 else 0
            self.assertEqual(sums[k],expected)

    def test_worst_case_direct_feature_bound_saturated(self):
        for t in (0.,.2,.5,1.):
            r=m.twirl_certificate(m.channel_kraus((1+t)/2,t))
            self.assertAlmostEqual(r['mean_commuting_visible_gain'],(1+t)/2,places=10)
            self.assertAlmostEqual(r['lower_bound_max_direct_feature_error'],(1-t)/2,places=10)

    def test_readout_variance_is_reported_not_hidden(self):
        r=m.readout_variance(0,.5)
        self.assertAlmostEqual(r['decoded_single_shot_variance'],4)
        self.assertAlmostEqual(r['ideal_single_shot_variance'],1)
        r=m.readout_variance(1,.5)
        self.assertAlmostEqual(r['decoded_single_shot_variance'],3)
        self.assertAlmostEqual(r['ideal_single_shot_variance'],0)

    def test_no_random_outcome_selected_and_strict_scope(self):
        a=m.audit()
        self.assertIsNone(a['actual_record_selected']);self.assertIsNone(a['physical_duration'])
        self.assertEqual(a['new_physical_axioms'],[])
        self.assertFalse(a['smaller_quantum_carrier_derived'])
        self.assertFalse(a['physical_collapse_law_derived'])

    def test_finite_and_fail_closed_report(self):
        a=copy.deepcopy(m.audit());a['max_decoded_prediction_error']=float('nan')
        with self.assertRaises(AssertionError):m.verify_result(a)
        b=copy.deepcopy(m.audit());b['actual_record_selected']='0'
        with self.assertRaises(AssertionError):m.verify_result(b)

    def test_explicit_noisy_map_is_not_idempotent(self):
        r=(np.eye(16)+m.paulis()[1])/16
        a=m.apply_channel(r,.5,0);b=m.apply_channel(a,.5,0)
        self.assertGreater(m.distance(a,b),.1)

    def test_probability_cost_is_not_claimed_universal_for_all_effects(self):
        r=m.audit()['boundary_channel']
        self.assertNotIn('maximal_direct_yes_no_probability_error',r)
        self.assertEqual(r['direct_probability_error_for_balanced_pauli_effect'],.25)
        rho=np.diag([1.]+[0.]*15)
        observed=float(np.trace(rho@m.apply_channel(rho,.5,0)).real)
        self.assertAlmostEqual(1-observed,15/32)

    def test_entropy_claim_flip_is_rejected(self):
        a=copy.deepcopy(m.audit());a['physical_entropy_production_derived']=True
        with self.assertRaises(AssertionError):m.verify_result(a)

if __name__=='__main__':unittest.main(verbosity=2)
