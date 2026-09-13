"""Regression tests of fixed-algebra descent, not physical-time claims."""
import copy
import importlib.util
import unittest
import numpy as np
m = None
if importlib.util.find_spec('retained_motion'):
    import retained_motion as m

class MotionTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m, 'retained-motion implementation missing')
    def test_baseline_hashes(self):
        self.assertEqual(m.verify_baseline()['recoverability.py'],'0a01d2eea4f0114b119fbb7beaf4619775c0f9f6')
    def test_invalid_unitaries_rejected(self):
        for u in [np.ones((16,16)), np.eye(2), np.eye(16)*np.nan]:
            with self.assertRaises(ValueError): m.classify(u,'1000')
    def test_invalid_masks_rejected(self):
        for mask in ['1',None,2,'x000']:
            with self.assertRaises(ValueError): m.classify(np.eye(16),mask)
    def test_all_frozen_motions_are_unitary(self):
        self.assertEqual(len(m.frozen_motions()),6)
        for u in m.frozen_motions().values(): np.testing.assert_allclose(u.conj().T@u,np.eye(16),atol=1e-11)
    def test_no_pinching_always_closed(self):
        for u in m.frozen_motions().values(): self.assertEqual(m.classify(u,'0000')['status'],'CLOSED_FIXED_RECORDS')
    def test_internal_motion_closed_and_nontrivial(self):
        r=m.classify(m.control_unitary('within'),'1000')
        self.assertEqual(r['status'],'CLOSED_FIXED_RECORDS')
        self.assertGreater(m.controls()['within_state_change'],.1)
    def test_block_permutation_closed_but_relabels(self):
        r=m.classify(m.control_unitary('swap'),'1000')
        self.assertEqual(r['status'],'CLOSED_RECORD_PERMUTATION')
        self.assertEqual(r['block_permutation'],[1,0])
        self.assertGreater(r['fixed_record_error'],1)
    def test_cross_block_mixing_fails_fixed_closure(self):
        self.assertEqual(m.classify(m.control_unitary('mix'),'1000')['status'],'NOT_CLOSED_ON_FIXED_ALGEBRA')
    def test_identity_and_center_act_trivially(self):
        r=m.old.fixture();e=m.old.reduce_input(r,'1000');u=m.control_unitary('center')
        np.testing.assert_allclose(u@e@u.conj().T,e,atol=1e-11)
    def test_effective_generator_dimensions(self):
        self.assertEqual([m.dimensions('1'*k+'0'*(4-k))['effective_continuous_motion_dimension'] for k in range(5)],[255,126,60,24,0])
    def test_generator_record_preservation_is_block_diagonality(self):
        for mask in m.old.masks():
            raw=np.arange(256).reshape(16,16);h=m.old.reduce_input(raw+raw.T,mask)
            self.assertTrue(m.generator_preserves_records(h,mask))
            self.assertEqual(m.classify(m.exp_unitary(h,.013),mask)['status'],'CLOSED_FIXED_RECORDS')
    def test_swap_endpoint_does_not_certify_entire_path(self):
        h=m.label_operator('XIII');u=m.exp_unitary(h,np.pi/2)
        self.assertTrue(m.classify(u,'1000')['closed'])
        self.assertFalse(m.generator_preserves_records(h,'1000'))
        self.assertFalse(m.classify(m.exp_unitary(h,.2),'1000')['closed'])
    def test_phase_witness_same_retained_input(self):
        r=m.controls()['witness'];self.assertLess(r['same_retained_input_distance'],1e-11)
        self.assertAlmostEqual(r['move_then_retain_distance'],1,places=10)
    def test_actually_pruned_pair_stays_identical(self):
        self.assertLess(m.controls()['witness']['retain_then_move_then_retain_distance'],1e-11)
    def test_projection_cadence_changes_process(self):
        self.assertAlmostEqual(m.controls()['projection_cadence_distance'],.5,places=10)
    def test_transported_algebra_always_intertwines(self):
        for u in m.frozen_motions().values():
            for mask in m.old.masks():
                self.assertLess(m.transport_error(u,mask),1e-11)
    def test_coprepared_transport_retains_record_identity(self):
        u=m.control_unitary('mix');ps=m.old.projectors('1000');r=ps[0]/8
        moved=u@r@u.conj().T;p=u@ps[0]@u.conj().T
        np.testing.assert_allclose(p@moved@p,moved,atol=1e-11)
    def test_closure_implies_commuting_expectation(self):
        for name in ['within','swap','center']:
            u=m.control_unitary(name);rho=m.old.fixture()
            np.testing.assert_allclose(m.old.reduce_input(u@rho@u.conj().T,'1000'),u@m.old.reduce_input(rho,'1000')@u.conj().T,atol=1e-11)
    def test_full_operator_matrix_agrees_with_direct_channel(self):
        u=m.frozen_motions()['A1'];mask='1000';r=m.old.fixture();f=m.old.basis();v=(f@r@f.conj().T).reshape(-1,order='F')
        lhs=m.leakage_matrix(u,mask)@v
        delta=m.old.reduce_input(u@(r-m.old.reduce_input(r,mask))@u.conj().T,mask)
        np.testing.assert_allclose(lhs,(f@delta@f.conj().T).reshape(-1,order='F'),atol=1e-11)
    def test_certificate_produces_valid_indistinguishable_inputs(self):
        u=m.control_unitary('mix');a,b=m.collision_pair(u,'1000')
        for r in (a,b):
            self.assertGreaterEqual(np.linalg.eigvalsh(r).min(),-1e-11)
            self.assertAlmostEqual(np.trace(r).real,1,places=10)
        self.assertLess(m.distance(m.old.reduce_input(a,'1000'),m.old.reduce_input(b,'1000')),1e-11)
        self.assertGreater(m.distance(m.old.reduce_input(u@a@u.conj().T,'1000'),m.old.reduce_input(u@b@u.conj().T,'1000')),1e-4)
    def test_no_collision_witness_for_closed_map(self):
        with self.assertRaises(ValueError):m.collision_pair(m.control_unitary('within'),'1000')
    def test_nested_identity_preserved(self):
        m.verify_baseline();self.assertEqual(m.old.details('1111')['hermitian_dimension'],16)
    def test_all_96_cases_and_scoped_status(self):
        a=m.audit();self.assertEqual(len(a['cases']),96)
        self.assertEqual(sum(a['classification_counts'].values()),96)
        self.assertIsNone(a['physical_duration']);self.assertIsNone(a['actual_record_selected'])
        self.assertFalse(a['new_physical_motion_law_derived']);self.assertEqual(a['new_physical_axioms'],[])
    def test_fail_closed_verifier(self):
        bad=copy.deepcopy(m.audit());bad['max_transport_error']=float('nan')
        with self.assertRaises(AssertionError): m.verify_result(bad)
    def test_superoperator_dual_leaks_match(self):
        for u in m.frozen_motions().values():
            r=m.classify(u,'1000')
            self.assertAlmostEqual(r['discarded_to_retained_leakage'],r['retained_to_discarded_leakage'],places=10)
    def test_all_failed_cases_have_collision(self):
        a=m.audit()
        for r in a['cases']:
            if not r['closed']:
                self.assertLess(r['collision']['retained_input_distance'],1e-11)
                self.assertGreater(r['collision']['unpruned_motion_output_distance'],1e-8)

if __name__=='__main__':unittest.main(verbosity=2)
