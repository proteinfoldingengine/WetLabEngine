"""Tests of a supplied partial-pinching model, not a physical collapse law."""
import copy
import importlib.util
import itertools
import unittest
import numpy as np

if importlib.util.find_spec('recoverability'):
    import recoverability as m
else:
    m=None

class RecoverabilityTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m, 'partial recoverability implementation missing')
    def test_baseline_is_frozen(self):
        self.assertEqual(m.verify_baseline()['coherent_records.py'],'fdf5367b11729fc1e2bfccd8d8daa2a0c7209049')
    def test_all_sixteen_masks(self): self.assertEqual(len(set(m.masks())),16)
    def test_invalid_masks_rejected(self):
        for mask in [None,'','01','00000','0x00',True,5]:
            with self.assertRaises(ValueError): m.keep_matrix(mask)
    def test_basis_is_unitary_in_all_schedules(self):
        for s in range(5):
            f=m.basis(s);np.testing.assert_allclose(f.conj().T@f,np.eye(16),atol=1e-11)
    def test_basis_comes_from_existing_branch_maps(self):
        for s in range(5):
            f=m.basis(s);v=m.encoding(s)
            for r in range(16):
                k=np.zeros((16,16),complex);k[r]=f[r]
                np.testing.assert_allclose(v[r*16:(r+1)*16],k,atol=1e-11)
    def test_projectors_complete_and_orthogonal(self):
        for mask in m.masks():
            ps=m.projectors(mask)
            np.testing.assert_allclose(sum(ps),np.eye(16),atol=1e-11)
            for i,p in enumerate(ps):
                np.testing.assert_allclose(p@p,p,atol=1e-11)
                for q in ps[i+1:]:np.testing.assert_allclose(p@q,0,atol=1e-11)
    def test_group_ranks(self):
        for mask in m.masks():
            self.assertEqual(len(m.groups(mask)),2**mask.count('1'))
            self.assertTrue(all(len(g)==2**(4-mask.count('1')) for g in m.groups(mask)))
    def test_full_and_empty_limits(self):
        r=m.fixture();np.testing.assert_allclose(m.reduce_input(r,'0000'),r,atol=1e-11)
        f=m.basis();np.testing.assert_allclose(f@m.reduce_input(r,'1111')@f.conj().T,np.diag(np.diag(f@r@f.conj().T)),atol=1e-11)
    def test_joint_and_input_routes_agree(self):
        r=m.fixture()
        for s in range(5):
            v=m.encoding(s)
            for mask in m.masks():
                lhs=m.pinch_joint(v@r@v.conj().T,mask)
                rhs=v@m.reduce_input(r,mask,s)@v.conj().T
                np.testing.assert_allclose(lhs,rhs,atol=1e-11)
    def test_range_intertwining_all_inputs(self):
        for s in range(5):
            v=m.encoding(s)
            for mask in m.masks():
                for inds,p in zip(m.groups(mask),m.projectors(mask,s)):
                    qv=np.zeros_like(v)
                    for i in inds:qv[i*16:(i+1)*16]=v[i*16:(i+1)*16]
                    np.testing.assert_allclose(qv,v@p,atol=1e-11)
    def test_decoder_returns_exact_reduced_input(self):
        r=m.fixture();v=m.encoding()
        for mask in m.masks():
            out=m.pinch_joint(v@r@v.conj().T,mask)
            np.testing.assert_allclose(v.conj().T@out@v,m.reduce_input(r,mask),atol=1e-11)
    def test_conditional_expectation_properties(self):
        r=m.fixture()
        for mask in m.masks():
            out=m.reduce_input(r,mask)
            np.testing.assert_allclose(m.reduce_input(out,mask),out,atol=1e-11)
            self.assertAlmostEqual(np.trace(out).real,1,places=11)
            self.assertGreaterEqual(np.linalg.eigvalsh(out).min(),-1e-11)
    def test_pinching_orders_compose_by_union(self):
        r=m.fixture()
        for a,b in itertools.product(m.masks(),repeat=2):
            union=f'{int(a,2)|int(b,2):04b}'
            np.testing.assert_allclose(m.reduce_input(m.reduce_input(r,a),b),m.reduce_input(r,union),atol=1e-11)
    def test_dimensions_of_fixed_algebra(self):
        for mask in m.masks():
            n=m.details(mask)
            self.assertEqual(n['hermitian_dimension'],256//2**mask.count('1'))
            self.assertEqual(n['lost_hermitian_directions'],256-n['hermitian_dimension'])
            self.assertEqual(n['center_dimension'],2**mask.count('1'))
    def test_surviving_phase_pair_counts(self):
        for k,expected in enumerate([120,56,24,8,0]):
            self.assertEqual(m.details('1'*k+'0'*(4-k))['surviving_unordered_pairs'],expected)
    def test_both_real_and_imaginary_phase_witnesses(self):
        for mask in m.masks():
            for i,j in itertools.combinations(range(16),2):
                for phase in (1,1j):
                    a,b=m.phase_pair(i,j,phase)
                    expected=float((i&int(mask,2))==(j&int(mask,2)))
                    self.assertAlmostEqual(m.distance(a,b),1,places=10)
                    self.assertAlmostEqual(m.distance(m.reduce_input(a,mask),m.reduce_input(b,mask)),expected,places=10)
    def test_expectations_of_surviving_observables(self):
        f=m.basis();r=m.fixture()
        for mask in m.masks():
            a=m.reduce_input(np.arange(256).reshape(16,16)+np.arange(256).reshape(16,16).T,mask)
            self.assertTrue(m.observable_recoverable(a,mask))
            self.assertAlmostEqual(float(np.trace(a@r).real),float(np.trace(a@m.reduce_input(r,mask)).real),places=9)
    def test_cross_block_observable_is_not_recoverable(self):
        f=m.basis();a=np.zeros((16,16),complex);a[0,8]=a[8,0]=1;a=f.conj().T@a@f
        self.assertFalse(m.observable_recoverable(a,'1000'))
        self.assertTrue(m.observable_recoverable(a,'0001'))
    def test_equal_size_masks_lose_different_distinctions(self):
        a,b=m.phase_pair(0,8)
        self.assertLess(m.distance(m.reduce_input(a,'1000'),m.reduce_input(b,'1000')),1e-11)
        self.assertAlmostEqual(m.distance(m.reduce_input(a,'0001'),m.reduce_input(b,'0001')),1,places=11)
    def test_records_probabilities_unchanged(self):
        r=m.fixture();f=m.basis();p=np.diag(f@r@f.conj().T)
        for mask in m.masks():
            np.testing.assert_allclose(np.diag(f@m.reduce_input(r,mask)@f.conj().T),p,atol=1e-11)
    def test_schedule_covariance_of_input_projectors(self):
        for s in range(5):
            for mask in m.masks():
                for p,q in zip(m.projectors(mask,s),m.projectors(mask,0)):np.testing.assert_allclose(p,q,atol=1e-11)
    def test_purity_of_one_state_does_not_count_map_loss(self):
        f=m.basis();r=np.outer(f[0].conj(),f[0])
        np.testing.assert_allclose(m.reduce_input(r,'1111'),r,atol=1e-11)
        self.assertEqual(m.details('1111')['lost_hermitian_directions'],240)
    def test_nonprojective_negative_control_rejects_formula(self):
        a=m.negative_control()
        self.assertGreater(a['intertwining_error'],.1)
        self.assertGreater(a['naive_compressed_output_error'],.1)
        self.assertGreater(a['compression_idempotence_error'],.01)
    def test_invalid_operators_and_labels_rejected(self):
        with self.assertRaises(ValueError):m.reduce_input(np.eye(2),'1000')
        with self.assertRaises(ValueError):m.pinch_joint(np.eye(16),'1000')
        with self.assertRaises(ValueError):m.phase_pair(0,0)
        with self.assertRaises(ValueError):m.basis(True)
    def test_audit_counts_and_fail_closed_status(self):
        a=m.audit();self.assertEqual(a['phase_witness_cases'],3840);self.assertEqual(a['schedule_mask_cases'],80)
        self.assertIsNone(a['actual_record_selected']);self.assertIsNone(a['physical_duration'])
        self.assertEqual(a['new_physical_axioms'],[])
        self.assertFalse(a['physical_entropy_law_derived'])
        bad=copy.deepcopy(a);bad['max_phase_witness_error']=float('nan')
        with self.assertRaises(AssertionError):m.verify_result(bad)
    def test_all_output_checks_are_finite(self):
        a=m.audit();m.verify_result(a)
        self.assertLess(a['max_phase_witness_error'],1e-11)

if __name__=='__main__':unittest.main(verbosity=2)
