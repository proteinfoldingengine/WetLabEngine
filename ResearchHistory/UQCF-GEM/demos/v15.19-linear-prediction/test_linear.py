import copy
import importlib.util
import unittest
import numpy as np
m=None
if importlib.util.find_spec('linear_module'):
    import linear_module as m

class LinearTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m,'linear prediction module not implemented')
    def test_baseline(self):
        self.assertEqual(m.verify_baseline()['completion.py'],'f50d12b46c72d564a4e69ebab38d477f147becba')
    def test_hermitian_basis(self):
        b=m.hermitian_basis(4); self.assertEqual(b.shape,(16,4,4))
        np.testing.assert_allclose(b,b.conj().transpose(0,2,1),atol=1e-12)
        q=b.reshape(16,16).T
        np.testing.assert_allclose(q.conj().T@q,np.eye(16),atol=1e-12)
    def test_bad_unitary_rejected(self):
        with self.assertRaises(ValueError): m.adjoint_action(np.ones((2,2)))
        with self.assertRaises(ValueError): m.adjoint_action(np.eye(2)*np.nan)
    def test_bad_seed_rejected(self):
        with self.assertRaises(ValueError): m.minimal_module([np.eye(2)],np.ones((3,1)))
        with self.assertRaises(ValueError): m.minimal_module([np.eye(2)],np.eye(4)*np.nan)
    def test_ambiguous_rank_stops(self):
        with self.assertRaises(m.AmbiguousRank):m.orthogonal_columns(np.diag([1.,1e-10]))
    def test_identity_leaves_seed(self):
        r=m.minimal_module([np.eye(2)],m.diagonal_seed(2))
        self.assertEqual(r['dimension_history'],[2])
    def test_qubit_z_orbit_is_three_not_four(self):
        y=np.array([[0,-1j],[1j,0]]); u=m.exp_unitary(y,.31)
        r=m.minimal_module([u],m.diagonal_seed(2))
        self.assertEqual(r['dimension'],3)
        self.assertLess(r['max_closure_error'],1e-10)
    def test_permutation_does_not_expand_diagonal_seed(self):
        u=np.array([[0,1],[1,0]])
        self.assertEqual(m.minimal_module([u],m.diagonal_seed(2))['dimension'],2)
    def test_two_noncommuting_axes_fill_qubit(self):
        y=np.array([[0,-1j],[1j,0]]); x=np.array([[0,1],[1,0]])
        r=m.minimal_module([m.exp_unitary(y,.31),m.exp_unitary(x,.27)],m.diagonal_seed(2))
        self.assertEqual(r['dimension'],4)
    def test_hermitian_action_matches_direct(self):
        y=np.array([[0,-1j],[1j,0]]);u=m.exp_unitary(y,.31);a=np.diag([.6,.4])
        v=m.coordinates(a); out=m.adjoint_action(u)@v
        np.testing.assert_allclose(m.from_coordinates(out),u.conj().T@a@u,atol=1e-12)
    def test_spectral_dimension_matches_krylov(self):
        for h in [np.array([[0,-1j],[1j,0]]),np.diag([1.,-1.])]:
            u=m.exp_unitary(h,.31);q=m.diagonal_seed(2)
            self.assertEqual(m.spectral_dimension(u,q)['dimension'],m.minimal_module([u],q)['dimension'])
    def test_four_dimensional_tensor_spectral_crosscheck(self):
        y=np.array([[0,-1j],[1j,0]]);u=np.kron(m.exp_unitary(y,.31),m.exp_unitary(y,.17))
        q=m.diagonal_seed(4)
        self.assertEqual(m.spectral_dimension(u,q)['dimension'],m.minimal_module([u],q)['dimension'])
    def test_prediction_coordinates_match_direct_state(self):
        y=np.array([[0,-1j],[1j,0]]);u=m.exp_unitary(y,.31);q=m.minimal_module([u],m.diagonal_seed(2))['basis']
        rho=np.array([[.7,.12],[.12,.3]],complex)
        z=m.state_features(rho,q);t=q.T@m.adjoint_action(u)@q
        for _ in range(12):
            z=t.T@z;rho=u@rho@u.conj().T
            np.testing.assert_allclose(z,m.state_features(rho,q),atol=1e-10)
    def test_discarded_input_cannot_be_recovered(self):
        c=m.controls(); self.assertLess(c['already_pruned_feature_distance'],1e-10)
        self.assertGreater(c['required_before_pruning_feature_distance'],.5)
    def test_linear_projection_not_cp_control(self):
        c=m.controls();self.assertLess(c['qubit_projection_min_choi_eigenvalue'],-.1)
    def test_linear_space_not_closed_under_multiplication(self):
        self.assertGreater(m.controls()['multiplication_residual'],1.)
    def test_all_112_cases(self):
        a=m.audit();self.assertEqual(len(a['cases']),112)
        self.assertEqual(len({(r['family'],r['mask']) for r in a['cases']}),112)
    def test_single_motion_independent_rank_check(self):
        for r in m.audit()['cases']:
            if r['family']!='all_six':self.assertEqual(r['linear_dimension'],r['spectral_dimension'])
    def test_module_between_seed_and_algebra(self):
        for r in m.audit()['cases']:
            self.assertLessEqual(r['initial_dimension'],r['linear_dimension'])
            self.assertLessEqual(r['linear_dimension'],r['algebra_dimension'])
    def test_prediction_checks(self):
        self.assertLess(m.audit()['max_prediction_error'],1e-9)
    def test_exact_number_not_empirical_time(self):
        a=m.audit();self.assertIsNone(a['physical_duration']);self.assertIsNone(a['actual_record_selected'])
        self.assertEqual(a['new_physical_axioms'],[]);self.assertFalse(a['GOSM_rederived'])
    def test_nan_rejected_by_verifier(self):
        a=copy.deepcopy(m.audit());a['max_prediction_error']=float('nan')
        with self.assertRaises(AssertionError):m.verify_result(a)


class ConditioningRegressionTests(unittest.TestCase):
    def test_spectral_basis_handles_weak_krylov_direction(self):
        self.assertTrue(hasattr(m,'spectral_module'),'stable spectral module absent')
        u=m.old.label_motions('pretime')[0];q=m.block_seed(m.old.old.old.groups('0101'))
        r=m.spectral_module(u,q)
        self.assertEqual(r['dimension'],m.spectral_dimension(u,q)['dimension'])
        self.assertLess(r['max_closure_error'],1e-9)
    def test_common_seed_reuse_keeps_fixed_rank_gap(self):
        self.assertTrue(hasattr(m,'family_module'),'nested-seed closure absent')
        r=m.family_module('all_six','1101')
        self.assertLess(r['max_closure_error'],1e-9)
        self.assertEqual(m.ZERO_TOL,1e-11);self.assertEqual(m.NONZERO_TOL,1e-8)

class ParityTests(unittest.TestCase):
    def setUp(self):self.assertTrue(hasattr(m,'parity_control'),'conserved-parity verification absent')
    def test_commutes_with_all_original_generators(self):
        c=m.parity_control();self.assertLess(c['max_motion_commutator'],1e-10)
        self.assertTrue(all(x['commutes_exactly'] for x in c['pauli_terms']))
    def test_complement_matches_full_family_module(self):
        c=m.parity_control();self.assertLess(c['complement_projector_error'],1e-9)
        self.assertEqual(c['module_dimension'],255)
    def test_indistinguishable_parity_states(self):
        c=m.parity_control();self.assertAlmostEqual(c['opposite_parity_state_distance'],1,places=10)
        self.assertLess(c['opposite_parity_feature_distance'],1e-9)
        self.assertLess(c['opposite_parity_record_probability_difference'],1e-9)
    def test_projection_is_not_a_positive_channel(self):
        self.assertAlmostEqual(m.parity_control()['projected_pure_state_min_eigenvalue'],-1/16,places=10)
    def test_masks_explain_full_family_counts(self):
        for mask in m.old.old.old.masks():
            row,_=m.case('all_six',mask)
            self.assertEqual(row['linear_dimension'],255 if '1' in mask[:3] else 256)
    def test_numeric_counts_not_physical_laws(self):
        self.assertFalse(m.parity_control()['new_physical_law'])

if __name__=='__main__':unittest.main(verbosity=2)
