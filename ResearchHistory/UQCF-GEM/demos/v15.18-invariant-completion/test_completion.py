"""Tests of algebraic completion, not a new physical retention law."""
import copy
import importlib.util
import itertools
import unittest
import numpy as np
m=None
if importlib.util.find_spec('completion'):
    import completion as m

class CompletionTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m,'dynamical algebra completion not implemented')
    def test_frozen_baseline(self):
        self.assertEqual(m.verify_baseline()['retained_motion.py'],'e3e8ac11cd5a856c66763faa071957fd9a220b42')
    def test_partition_rejects_missing_and_duplicate_labels(self):
        for p in [[],[[0,0],[1]],[[0],[2]],[[True],[1]]]:
            with self.assertRaises(ValueError):m.canonical(p,2)
    def test_bad_unitary_rejected(self):
        for u in [np.ones((2,2)),np.eye(2)*np.nan,np.eye(3)]:
            with self.assertRaises(ValueError):m.complete([[0],[1]],[u])
    def test_empty_family_leaves_algebra_unchanged(self):
        r=m.complete([[0,1],[2,3]],[])
        self.assertEqual(r['final_blocks'],[[0,1],[2,3]])
    def test_ambiguous_support_fails_closed(self):
        u=np.array([[np.cos(1e-10),-np.sin(1e-10)],[np.sin(1e-10),np.cos(1e-10)]])
        with self.assertRaises(m.AmbiguousSupport):m.complete([[0],[1]],[u])
    def test_diagonal_phases_do_not_expand(self):
        r=m.complete([[0],[1]],[np.diag([1,1j])])
        self.assertEqual(r['final_dimension'],2)
    def test_sector_permutation_does_not_force_merging(self):
        x=np.array([[0,1],[1,0]])
        r=m.complete([[0],[1]],[x])
        self.assertEqual(r['dimension_history'],[2])
    def test_mixing_two_sectors_requires_full_qubit_algebra(self):
        h=np.array([[1,1],[1,-1]])/np.sqrt(2)
        r=m.complete([[0],[1]],[h])
        self.assertEqual(r['dimension_history'],[2,4])
    def test_repeated_orbit_not_only_one_conjugation(self):
        # permutation moves the first 2x2 block along a four-cycle
        p=np.roll(np.eye(6),1,axis=0)
        r=m.complete([[0,1],[2],[3],[4],[5]],[p])
        self.assertEqual(r['final_dimension'],36)
        self.assertGreaterEqual(r['strict_completion_rounds'],2)
    def test_two_motion_family_can_exceed_either_single_completion(self):
        h=np.array([[1,1],[1,-1]])/np.sqrt(2);a=np.eye(4);b=np.eye(4)
        a[:2,:2]=h;b[1:3,1:3]=h
        part=[[i] for i in range(4)]
        self.assertEqual(m.complete(part,[a])['final_dimension'],6)
        self.assertEqual(m.complete(part,[b])['final_dimension'],6)
        self.assertEqual(m.complete(part,[a,b])['final_dimension'],10)
    def test_all_rounds_are_nested_coarsenings(self):
        r=m.complete([[0],[1],[2],[3]],[np.fft.fft(np.eye(4))/2])
        hist=r['partition_history']
        for a,b in zip(hist,hist[1:]):self.assertTrue(m.contains(b,a))
    def test_every_final_algebra_is_closed_for_both_directions(self):
        for r in m.audit()['cases']:
            self.assertLess(r['max_normalizer_error'],1e-10)
            self.assertLess(r['max_superoperator_leakage'],1e-10)
    def test_unchanged_cases_match_v1517(self):
        for name,u in m.old.frozen_motions().items():
            for mask in m.old.old.masks():
                r=m.case(name,mask)
                self.assertEqual(r['initial_dimension']==r['final_dimension'],m.old.classify(u,mask)['closed'])
    def test_all_112_cases_present(self):
        a=m.audit()
        self.assertEqual(len(a['cases']),112)
        self.assertEqual(len({(r['family'],r['mask']) for r in a['cases']}),112)
    def test_exhaustive_small_partition_minimality(self):
        h=np.array([[1,1],[1,-1]])/np.sqrt(2)
        unitaries=[np.kron(h,np.eye(2)),np.roll(np.eye(4),1,axis=0),np.diag([1,1j,-1,-1j])]
        partitions=m.partitions(4)
        self.assertEqual(len(partitions),15)
        for initial in partitions:
            for units in ([unitaries[0]],[unitaries[1]],unitaries):
                r=m.complete(initial,units)
                for candidate in partitions:
                    if m.contains(candidate,initial) and m.normalizer_error(candidate,units)<1e-10:
                        self.assertTrue(m.contains(candidate,r['final_blocks']))
    def test_completion_idempotent(self):
        for r in m.audit()['cases']:
            units=m.label_motions(r['family'])
            self.assertEqual(m.complete(r['final_blocks'],units)['final_blocks'],r['final_blocks'])
    def test_inverse_and_family_order_do_not_change_result(self):
        units=m.label_motions('all_six');p=m.old.old.groups('1111')
        expected=m.complete(p,units)['final_blocks']
        self.assertEqual(m.complete(p,units[::-1])['final_blocks'],expected)
        self.assertEqual(m.complete(p,[u.conj().T for u in units])['final_blocks'],expected)
    def test_completed_projection_is_cptp_conditional_expectation(self):
        rho=m.old.old.fixture()
        for r in m.audit()['cases']:
            out=m.retain(rho,r['final_blocks'])
            self.assertAlmostEqual(np.trace(out).real,1,places=10)
            self.assertGreaterEqual(np.linalg.eigvalsh(out).min(),-1e-10)
            np.testing.assert_allclose(m.retain(out,r['final_blocks']),out,atol=1e-10)
    def test_exact_unpruned_prediction_from_completed_input(self):
        rho=m.old.old.fixture()
        for r in m.audit()['cases']:
            for u in m.input_motions(r['family']):
                kept=m.retain(rho,r['final_blocks'])
                np.testing.assert_allclose(m.old.old.reduce_input(u@rho@u.conj().T,r['mask']),
                    m.old.old.reduce_input(u@kept@u.conj().T,r['mask']),atol=1e-10)
    def test_earlier_retained_observables_preserved(self):
        rho=m.old.old.fixture()
        for r in m.audit()['cases']:
            np.testing.assert_allclose(m.old.old.reduce_input(m.retain(rho,r['final_blocks']),r['mask']),
                                      m.old.old.reduce_input(rho,r['mask']),atol=1e-10)
    def test_completion_does_not_recover_already_lost_distinction(self):
        c=m.controls()
        self.assertLess(c['already_pruned_then_enlarged_distance'],1e-10)
        self.assertAlmostEqual(c['kept_in_completed_algebra_distance'],1,places=10)
    def test_linear_sufficiency_not_confused_with_algebra(self):
        c=m.controls()
        self.assertEqual(c['linear_orbit_dimension'],3)
        self.assertEqual(c['multiplicative_algebra_dimension'],4)
        self.assertGreater(c['linear_space_product_residual'],.5)
    def test_coordinate_permutation_covariance(self):
        h=np.array([[1,1],[1,-1]])/np.sqrt(2);u=np.kron(h,np.eye(2));p=[[0],[1],[2],[3]]
        order=[2,0,3,1];t=np.eye(4)[order];r=m.complete(p,[u]);v=m.complete(p,[t@u@t.T])
        transformed=[[order.index(i) for i in g] for g in r['final_blocks']]
        self.assertEqual(v['final_blocks'],m.canonical(transformed,4))
    def test_support_gap_is_recorded(self):
        for r in m.audit()['cases']:
            self.assertLessEqual(r['support']['max_discarded_entry'],m.ZERO_TOL)
            self.assertGreaterEqual(r['support']['min_retained_entry'],m.NONZERO_TOL)
    def test_fail_closed_nan_and_boundary(self):
        for key,val in [('max_closure_error',float('nan')),('physical_duration',1),('actual_record_selected','0')]:
            a=copy.deepcopy(m.audit());a[key]=val
            with self.assertRaises(AssertionError):m.verify_result(a)
    def test_enlargement_does_not_preserve_all_old_central_records(self):
        r=m.case('B1','1111')
        self.assertIn('old_center_preserved',r,'central-record boundary not reported')
        self.assertFalse(r['old_center_preserved'])
        self.assertEqual(r['initial_center_dimension'],16)
        self.assertEqual(r['final_center_dimension'],4)
        self.assertTrue(m.case('B1','1100')['old_center_preserved'])

    def test_direct_full_algebra_certificate(self):
        self.assertTrue(hasattr(m,'dense_witness'),'direct full-algebra witness missing')
        r=m.dense_witness('pretime')
        self.assertEqual(r['matrix_units_generated'],256)
        self.assertGreater(r['minimum_projector_entry'],1e-6)
        self.assertLess(r['matrix_unit_reconstruction_error'],1e-10)

    def test_no_new_physical_selector(self):
        a=m.audit();self.assertEqual(a['new_physical_axioms'],[])
        self.assertFalse(a['physical_pruning_law_derived']);self.assertFalse(a['GOSM_derived'])
        self.assertEqual(a['scope_type'],'MINIMAL_INVARIANT_UNITAL_STAR_ALGEBRA_FOR_SUPPLIED_MOTIONS')

if __name__=='__main__':unittest.main(verbosity=2)
