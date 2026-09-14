"""Event-instrument preservation, not derivation of physical pruning."""
import copy
import importlib.util
from pathlib import Path
import unittest
import numpy as np

m=None
path=Path(__file__).with_name('event_sufficiency.py')
if path.exists():
    spec=importlib.util.spec_from_file_location('event_sufficiency',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class EventSufficiencyTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(m,'event-sufficiency implementation absent')
    def test_baseline_identity(self):
        self.assertEqual(m.verify_baseline()['adaptive.py'],'44a87e4cc5bcf531ef7798aadab5d9dbba3482cb')
    def test_context_coverage(self):
        self.assertEqual(len(m.contexts()),45)
        self.assertEqual(sum(bool(m.prior.enabled(f)) for f in m.contexts().values()),29)
    def test_readiness_counts(self):
        counts={k:sum(len(m.prior.enabled(f))==k for f in m.contexts().values()) for k in (0,1,2)}
        self.assertEqual(counts,{0:16,1:22,2:7})
    def test_sector_isometry(self):
        for f in m.contexts().values():
            w=m.sector(f);np.testing.assert_allclose(w.conj().T@w,np.eye(w.shape[1]),atol=1e-11)
            np.testing.assert_allclose(w@w.conj().T@f.rho,f.rho,atol=1e-11)
    def test_ready_effects_are_complete_projectors(self):
        for f in m.contexts().values():
            for e in m.prior.enabled(f):
                ps=m.effects(f,e);d=ps[0].shape[0]
                np.testing.assert_allclose(sum(ps),np.eye(d),atol=1e-11)
                for p in ps:
                    np.testing.assert_allclose(p@p,p,atol=1e-11)
                    self.assertAlmostEqual(np.trace(p).real,d/2,places=10)
    def test_event_specific_map_cptp_and_idempotent(self):
        for f in m.contexts().values():
            w=m.sector(f);rho=w.conj().T@f.rho@w
            for e in m.prior.enabled(f):
                out=m.retain(rho,m.effects(f,e))
                self.assertAlmostEqual(np.trace(out).real,1,places=10)
                self.assertGreaterEqual(np.linalg.eigvalsh(out).min(),-1e-10)
                np.testing.assert_allclose(m.retain(out,m.effects(f,e)),out,atol=1e-10)
    def test_all_input_kraus_factorization(self):
        for f in m.contexts().values():
            for e in m.prior.enabled(f):
                ks=m.kraus(f,e);ps=m.effects(f,e)
                for b,k in enumerate(ks):
                    for c,p in enumerate(ps):np.testing.assert_allclose(k@p,k if b==c else 0,atol=1e-10)
    def test_reference_safe_choi_identity(self):
        for f in m.contexts().values():
            for e in m.prior.enabled(f):
                ps=m.effects(f,e)
                for k in m.kraus(f,e):
                    np.testing.assert_allclose(m.choi([k@p for p in ps]),m.choi([k]),atol=1e-10)
    def test_preprocessing_does_not_select_record(self):
        f=m.prior.start();g=m.preprocess_frame(f,'A1')
        self.assertEqual(g.records,());self.assertEqual(g.mass,f.mass)
        np.testing.assert_array_equal(f.rho,m.prior.start().rho)
    def test_missing_record_and_duplicate_events_rejected(self):
        f=m.prior.start()
        with self.assertRaises(ValueError):m.effects(f,'B2')
        with self.assertRaises(ValueError):m.preprocess_frame(f,'unknown')
        g=m.prior.advance(f,'A1',0)
        with self.assertRaises(ValueError):m.effects(g,'A1')
    def test_invalid_operator_and_projectors_rejected(self):
        with self.assertRaises(ValueError):m.retain(np.eye(2),[np.eye(2),np.eye(2)])
        with self.assertRaises(ValueError):m.retain(np.eye(3),[np.eye(2)])
        with self.assertRaises(ValueError):m.retain(np.eye(2)*np.nan,[np.eye(2)])
    def test_same_record_support_retained(self):
        for f in m.contexts().values():
            for e in m.prior.enabled(f):
                g=m.preprocess_frame(f,e);w=m.sector(f)
                self.assertEqual(g.records,f.records)
                np.testing.assert_allclose(w@w.conj().T@g.rho,g.rho,atol=1e-10)
    def test_all_adaptive_histories_exact(self):
        a=m.integration_control()
        self.assertEqual(a['histories'],80);self.assertEqual(a['branch_steps'],320)
        for key in ('max_state_distance','max_joint_mass_error','max_conditional_error'):
            self.assertLess(a[key],1e-10)
    def test_two_ready_effects_commute(self):
        for f in m.contexts().values():
            es=m.prior.enabled(f)
            if len(es)==2:
                a=m.effects(f,es[0])[0];b=m.effects(f,es[1])[0]
                np.testing.assert_allclose(a@b,b@a,atol=1e-10)
    def test_four_joint_sectors_are_nonzero(self):
        for f in m.contexts().values():
            if len(m.prior.enabled(f))==2:
                cert=m.joint_certificate(f);d=m.sector(f).shape[1]
                self.assertEqual(cert['joint_ranks'],[d//4]*4)
    def test_pair_algebras_generate_full_algebra(self):
        a=m.audit()
        self.assertEqual(a['two_ready_contexts'],7)
        self.assertEqual(a['matrix_unit_certificates'],448)
        self.assertLess(a['max_multiplication_certificate_error'],1e-10)
    def test_wrong_event_keeps_probability_but_changes_state(self):
        c=m.root_control()
        self.assertLess(c['wrong_event_probability_error'],1e-10)
        self.assertAlmostEqual(c['wrong_event_output_state_distance'],.5,places=10)
    def test_wrong_event_erases_distinction(self):
        c=m.root_control()
        self.assertAlmostEqual(c['unpruned_other_event_pair_distance'],1,places=10)
        self.assertLess(c['prepruned_other_event_pair_distance'],1e-10)
    def test_matching_event_is_transparent(self):
        self.assertLess(m.root_control()['matching_event_choi_error'],1e-10)
    def test_complete_two_event_batch_is_different_contract(self):
        a=m.audit();self.assertLess(a['max_two_event_batch_choi_error'],1e-10)
        self.assertGreater(m.root_control()['wrong_event_output_state_distance'],.1)
    def test_parity_erasure_has_no_matching_branch_attenuation(self):
        c=m.root_control();self.assertLess(c['event_map_parity_norm'],1e-10)
        self.assertLess(c['matching_event_choi_error'],1e-10)
    def test_proper_coarsening_cannot_preserve_single_event_algebra(self):
        for d in (2,4,8,16):
            self.assertEqual(m.single_event_dimension(d),d*d//2)
        with self.assertRaises(ValueError):m.single_event_dimension(3)
    def test_prepruning_is_not_silently_global(self):
        a=m.audit()
        self.assertEqual(a['common_preprocessor_at_two_ready'],'IDENTITY_ON_CURRENT_SECTOR')
        self.assertEqual(a['event_specific_rule_status'],'DERIVED_FROM_SUPPLIED_NEXT_INSTRUMENT_NOT_SELECTED_PHYSICS')
    def test_failure_checks_reject_nan_and_missing_fields(self):
        a=copy.deepcopy(m.audit());a['max_event_choi_error']=float('nan')
        with self.assertRaises(AssertionError):m.verify_result(a)
        a=copy.deepcopy(m.audit());del a['nonterminal_contexts']
        with self.assertRaises(AssertionError):m.verify_result(a)
    def test_failure_checks_protect_ontology(self):
        for key,value in [('physical_duration',1),('actual_record_selected','0'),('physical_pruning_law_derived',True)]:
            a=copy.deepcopy(m.audit());a[key]=value
            with self.assertRaises(AssertionError):m.verify_result(a)
    def test_no_change_of_input_dynamics(self):
        a=m.audit();self.assertEqual(a['new_physical_axioms'],[])
        self.assertFalse(a['new_motion_law_derived']);self.assertEqual(a['Pillar_3'],'OPEN')

if __name__=='__main__':unittest.main(verbosity=2)
