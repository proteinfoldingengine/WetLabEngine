"""Checks a classified channel family; the proof, not sampling, gives completeness."""
import copy
import importlib.util
from pathlib import Path
import unittest
import numpy as np
p=Path(__file__).with_name('retention_family.py');m=None
if p.exists():
    spec=importlib.util.spec_from_file_location('retention_family',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class FamilyTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m,'retention-family implementation absent')
    def test_baseline(self): self.assertEqual(m.verify_baseline()['event_sufficiency.py'],'0d6f625cc398ce1cd3e2edeac93156ad7b6c5f8e')
    def test_grid_has_33_distinct_values(self): self.assertEqual(len(set(m.disk_samples())),33)
    def test_outside_disk_and_nonfinite_rejected(self):
        for c in (1.01,1.01j,float('nan'),float('inf'),True,'x'):
            with self.assertRaises(ValueError): m.binary(c)
    def test_correlation_matrix_validation(self):
        for c in (np.eye(0),np.ones((2,3)),np.eye(2)*2,np.array([[1,1],[0,1]]),np.array([[1,2],[2,1]])):
            with self.assertRaises(ValueError): m.validate_correlation(c)
    def test_global_psd_not_pairwise_bounds(self):
        c=np.array([[1,.9,.9],[.9,1,-.9],[.9,-.9,1]])
        self.assertLess(np.linalg.eigvalsh(c).min(),-.1)
        with self.assertRaises(ValueError): m.validate_correlation(c)
    def test_projector_validation(self):
        for ps in ([np.eye(2),np.eye(2)],[np.eye(2),np.eye(3)],[np.zeros((2,2))]):
            with self.assertRaises(ValueError):m.projectors_checked(ps)
    def test_kraus_choi_and_direct_map_agree(self):
        f=m.old.prior.start();ps=m.old.effects(f,'A1');rho=f.rho
        for c in m.disk_samples():
            ks=m.channel_kraus(ps,m.binary(c));out=sum(k@rho@k.conj().T for k in ks)
            np.testing.assert_allclose(out,m.apply(rho,ps,m.binary(c)),atol=1e-10)
            np.testing.assert_allclose(sum(k.conj().T@k for k in ks),np.eye(16),atol=1e-10)
            eig=np.linalg.eigvalsh(m.old.choi(ks))
            np.testing.assert_allclose(eig[-2:],[(1-abs(c))/2,(1+abs(c))/2],atol=1e-10)
    def test_all_contexts_preserve_full_branches(self):
        r=m.audit();self.assertEqual(r['event_channel_cases'],1188);self.assertEqual(r['branch_map_checks'],2376)
        self.assertLess(r['max_branch_choi_error'],1e-10)
    def test_different_inputs_obey_positivity_and_trace(self):
        ps=m.old.effects(m.old.prior.start(),'A1')
        for rho in m.phase_pair(ps):
            for c in m.disk_samples():
                out=m.apply(rho,ps,m.binary(c));self.assertGreaterEqual(np.linalg.eigvalsh(out).min(),-1e-10)
                self.assertAlmostEqual(np.trace(out).real,1,places=10)
    def test_witness_distance_is_modulus(self):
        for row in m.audit()['disk']:
            self.assertAlmostEqual(row['trace_distance'],row['modulus'],places=10)
    def test_modulus_one_inverse_recovers(self):
        ps=m.old.effects(m.old.prior.start(),'A1');a,b=m.phase_pair(ps)
        for c in (1,-1,1j,-1j):
            np.testing.assert_allclose(m.apply(m.apply(a,ps,m.binary(c)),ps,m.binary(c.conjugate())),a,atol=1e-10)
    def test_interior_injectivity_not_physical_reversibility(self):
        row=m.analyze_binary(.5)
        self.assertTrue(row['linear_injective']);self.assertFalse(row['cptp_reversible']);self.assertFalse(row['idempotent'])
    def test_complete_pinching_has_kernel(self):
        r=m.analyze_binary(0);self.assertFalse(r['linear_injective']);self.assertTrue(r['idempotent'])
    def test_identity_only_other_binary_idempotent(self):
        ps=m.old.effects(m.old.prior.start(),'A1');rho=m.phase_pair(ps)[0]
        for c in m.disk_samples():
            out=m.apply(rho,ps,m.binary(c));err=np.linalg.norm(m.apply(out,ps,m.binary(c))-out)
            self.assertEqual(err<1e-10,abs(c)<1e-12 or abs(c-1)<1e-12)
    def test_composition_multiplies_coefficients(self):
        ps=m.old.effects(m.old.prior.start(),'A1');rho=m.phase_pair(ps)[0]
        for c,d in [(.5,.5),(1j,-1),(.5+.25j,-.2j)]:
            np.testing.assert_allclose(m.apply(m.apply(rho,ps,m.binary(c)),ps,m.binary(d)),m.apply(rho,ps,m.binary(c*d)),atol=1e-10)
    def test_kraus_fit_recovers_coefficient_without_choosing_it(self):
        ps=m.old.effects(m.old.prior.start(),'A1')
        for c in m.disk_samples():
            ks=m.channel_kraus(ps,m.binary(c));fit=m.fit_kraus(ks,ps)
            np.testing.assert_allclose(fit['correlation'],m.binary(c),atol=1e-10)
            self.assertLess(fit['central_residual'],1e-10)
    def test_probability_preserving_bad_channel_not_full_instrument(self):
        c=m.negative_control();self.assertLess(c['probability_error'],1e-10);self.assertGreater(c['branch_state_distance'],.1)
        self.assertGreater(c['central_kraus_residual'],.1)
    def test_open_alternative_restricts_family_to_identity(self):
        r=m.audit();self.assertEqual(r['open_alternative_checks'],231)
        self.assertEqual(r['common_identity_cases'],7)
        self.assertLess(r['max_other_event_formula_error'],1e-10)
    def test_64_boolean_correlations_have_15_psd(self):
        r=m.partition_audit();self.assertEqual(r['boolean_candidates'],64);self.assertEqual(r['psd_partitions'],15)
        self.assertEqual(r['partitions_by_blocks'],{'1':1,'2':7,'3':6,'4':1})
    def test_partition_maps_and_idempotence(self):
        for frame in m.old.contexts().values():
            if len(m.old.prior.enabled(frame))!=2:continue
            ps,ks=m.batch(frame)
            for c in m.idempotent_correlations(4):
                rho=m.old.sector(frame).conj().T@frame.rho@m.old.sector(frame)
                out=m.apply(rho,ps,c)
                np.testing.assert_allclose(m.apply(out,ps,c),out,atol=1e-10)
                for k in ks:np.testing.assert_allclose(k@out@k.conj().T,k@rho@k.conj().T,atol=1e-10)
    def test_all_batch_branches_checked(self):
        r=m.audit();self.assertEqual(r['batch_partition_cases'],105);self.assertEqual(r['batch_branch_checks'],420)
        self.assertLess(r['max_batch_choi_error'],1e-10)
    def test_pair_partitions_exceed_bit_masks(self):
        r=m.partition_audit();self.assertEqual(r['local_bit_masks'],4);self.assertEqual(r['additional_partitions'],11)
    def test_no_fixed_record_is_selected(self):
        r=m.audit();self.assertIsNone(r['actual_record_selected']);self.assertIsNone(r['physical_duration'])
        self.assertEqual(r['new_physical_axioms'],[]);self.assertFalse(r['physical_pruning_law_derived'])
    def test_integration_unchanged_for_all_selected_parameters(self):
        r=m.integration();self.assertEqual(r['histories'],400);self.assertEqual(r['branch_steps'],1600)
        self.assertLess(r['max_state_error'],1e-10);self.assertLess(r['max_mass_error'],1e-10)
    def test_fail_closed_schema_and_nan(self):
        for key,value in [('max_branch_choi_error',float('nan')),('physical_duration',1),('physical_pruning_law_derived',True)]:
            a=copy.deepcopy(m.audit());a[key]=value
            with self.assertRaises(AssertionError):m.verify_result(a)
        a=copy.deepcopy(m.audit());del a['batch_partition_cases']
        with self.assertRaises(AssertionError):m.verify_result(a)
    def test_trace_distance_after_actual_pinching_stays_zero(self):
        ps=m.old.effects(m.old.prior.start(),'A1');a,b=m.phase_pair(ps)
        for c in m.disk_samples():
            left=m.apply(m.apply(a,ps,m.binary(0)),ps,m.binary(c));right=m.apply(m.apply(b,ps,m.binary(0)),ps,m.binary(c))
            self.assertLess(m.old.prior.base.distance(left,right),1e-10)

if __name__=='__main__':unittest.main(verbosity=2)
