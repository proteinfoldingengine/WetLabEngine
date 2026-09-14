"""Tests of different composition contracts, not a new locality axiom."""
import copy
import importlib.util
from pathlib import Path
import unittest
import numpy as np
p=Path(__file__).with_name('composition_gate.py');m=None
if p.exists():
    spec=importlib.util.spec_from_file_location('composition_gate',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class CompositionTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(m,'composition classifier absent')
    def test_baseline(self):self.assertEqual(m.verify_baseline(),'7c5a412c5f3925ad3656b08ccb035e9516ec108a')
    def test_all_fifteen_partitions(self):self.assertEqual(len(m.partitions()),15)
    def test_exact_classification_counts(self):
        rows=[m.classify(c) for c in m.partitions()]
        self.assertEqual(sum(r['non_signalling'] for r in rows),7)
        self.assertEqual(sum(r['product'] for r in rows),4)
        self.assertEqual(sum(r['non_signalling'] and not r['product'] for r in rows),3)
    def test_directional_counts(self):
        rows=[m.classify(c) for c in m.partitions()]
        self.assertEqual(sum(r['A_to_B'] and r['B_to_A'] for r in rows),4)
        self.assertEqual(sum(r['A_to_B'] and not r['B_to_A'] for r in rows),2)
        self.assertEqual(sum(r['B_to_A'] and not r['A_to_B'] for r in rows),2)
    def test_invalid_matrices_rejected(self):
        for c in (np.eye(3),np.eye(4)*2,np.ones((2,4)),np.eye(4)*np.nan):
            with self.assertRaises(ValueError):m.classify(c)
    def test_nonpartition_rejected(self):
        with self.assertRaises(ValueError):m.classify(.5*np.eye(4)+.5*np.ones((4,4)))
    def test_seven_contexts_retain_tensor_factors(self):
        self.assertEqual(len(m.contexts()),7)
        for f in m.contexts():
            a,b=m.local_effects(f)
            self.assertEqual(len(a),2);self.assertEqual(len(b),2)
            ps,_=m.old.batch(f)
            for p,q in zip(ps,[np.kron(x,y) for x in a for y in b]):np.testing.assert_allclose(p,q,atol=1e-10)
    def test_nonready_context_rejected(self):
        f=m.old.old.prior.advance(m.old.old.prior.start(),'B1',0)
        with self.assertRaises(ValueError):m.local_effects(f)
    def test_all_batch_maps_preserved(self):
        a=m.audit();self.assertEqual(a['context_partition_cases'],105);self.assertEqual(a['batch_branch_checks'],420)
        self.assertLess(a['max_batch_choi_error'],1e-10)
    def test_no_signal_checked_on_full_operator_space(self):
        a=m.audit();self.assertLess(a['max_non_signalling_operator_residual'],1e-10)
        self.assertEqual(a['non_signalling_context_cases'],49)
    def test_all_signalling_cases_have_valid_witness(self):
        a=m.audit();self.assertEqual(a['signalling_context_cases'],56)
        for r in a['contexts']:
            for w in r['witnesses']:
                self.assertLess(w['local_input_distance'],1e-10)
                self.assertAlmostEqual(w['local_output_distance'],.5,places=10)
                self.assertLess(w['local_record_probability_change'],1e-10)
    def test_product_channels_are_only_four_bit_masks(self):
        expected=[np.kron(a,b) for a in (np.eye(2),np.ones((2,2))) for b in (np.eye(2),np.ones((2,2)))]
        found=[c for c in m.partitions() if m.classify(c)['product']]
        self.assertEqual(len(found),4)
        for c in found:self.assertTrue(any(np.array_equal(c,d) for d in expected))
    def test_realignment_independent_product_certificate(self):
        for c in m.partitions():
            a=c.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4)
            self.assertEqual(np.linalg.matrix_rank(a)==1,m.classify(c)['product'])
    def test_shared_phase_mixtures_for_all_seven(self):
        for c in m.partitions():
            if not m.classify(c)['non_signalling']:continue
            recipe=m.phase_recipe(c)
            self.assertAlmostEqual(sum(w for w,_,_ in recipe),1)
            self.assertTrue(all(w>0 for w,_,_ in recipe))
            np.testing.assert_allclose(m.recipe_correlation(recipe),c,atol=1e-10)
    def test_signal_map_cannot_get_local_phase_certificate(self):
        c=next(c for c in m.partitions() if m.classify(c)['A_to_B'])
        with self.assertRaises(ValueError):m.phase_recipe(c)
    def test_lifted_phase_mixture_preserves_full_channel(self):
        a=m.audit();self.assertEqual(a['shared_phase_context_cases'],49)
        self.assertLess(a['max_phase_choi_error'],1e-10)
        self.assertLess(a['max_phase_tp_error'],1e-10)
    def test_parity_is_nonproduct_and_non_signalling(self):
        row=m.classify(m.parity_correlation())
        self.assertTrue(row['non_signalling']);self.assertFalse(row['product'])
    def test_equal_local_marginals_do_not_fix_global_retention(self):
        a=m.parity_control()
        self.assertLess(a['local_marginal_distance'],1e-10)
        self.assertLess(a['record_probability_difference'],1e-10)
        self.assertAlmostEqual(a['joint_state_distance'],.5,places=10)
        self.assertAlmostEqual(a['correlated_xx_expectation'],1,places=10)
        self.assertAlmostEqual(a['independent_xx_expectation'],0,places=10)
    def test_only_identity_preserves_both_next_instruments(self):
        a=m.audit();self.assertEqual(a['open_frontier_identity_cases'],7)
        self.assertLess(a['max_identity_frontier_error'],1e-10)
        self.assertGreater(a['min_nonidentity_frontier_error'],1e-4)
    def test_no_actual_record_or_entropy_added(self):
        a=m.audit();self.assertIsNone(a['actual_record_selected']);self.assertIsNone(a['physical_duration'])
        self.assertEqual(a['new_physical_axioms'],[]);self.assertFalse(a['physical_locality_derived'])
        self.assertFalse(a['shared_random_outcome_sampled'])
    def test_do_not_change_record_histories(self):
        a=m.integration()
        self.assertEqual(a['batched_histories'],1200)
        self.assertLess(a['max_final_state_error'],1e-10)
        self.assertLess(a['max_final_mass_error'],1e-10)
    def test_idempotence_and_postpruned_distinctions(self):
        ps=[np.diag(np.eye(4)[i]) for i in range(4)];rho=np.ones((4,4))/4
        for c in m.partitions():
            y=m.old.apply(rho,ps,c)
            np.testing.assert_allclose(m.old.apply(y,ps,c),y,atol=1e-10)
    def test_schema_missing_and_nan_fail_closed(self):
        a=copy.deepcopy(m.audit());del a['non_signalling_context_cases']
        with self.assertRaises(AssertionError):m.verify_result(a)
        a=copy.deepcopy(m.audit());a['max_batch_choi_error']=float('nan')
        with self.assertRaises(AssertionError):m.verify_result(a)
    def test_scope_flags_fail_closed(self):
        for key,value in [('physical_locality_derived',True),('actual_record_selected','00'),('physical_duration',1)]:
            a=copy.deepcopy(m.audit());a[key]=value
            with self.assertRaises(AssertionError):m.verify_result(a)

if __name__=='__main__':unittest.main(verbosity=2)
