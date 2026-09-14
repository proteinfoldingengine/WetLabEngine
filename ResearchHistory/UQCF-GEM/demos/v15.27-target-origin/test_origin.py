import importlib.util, pathlib, sys, unittest, numpy as np
m=None
path=pathlib.Path(__file__).with_name('target_origin.py')
if path.exists():
    spec=importlib.util.spec_from_file_location('target_origin',path);m=importlib.util.module_from_spec(spec);sys.modules['target_origin']=m;spec.loader.exec_module(m)

class TargetOriginTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m,'target-origin implementation absent')
    def test_baseline_frozen(self):
        self.assertEqual(m.verify_baseline(),'623defd0d8284e5d9cba6d8f8679de698e5202bc')
    def test_factorization_obstruction_exact(self):
        a=m.audit();self.assertFalse(a['response_target_factors_through_source'])
        self.assertEqual(a['factorization_obstruction_dimension'],50)
        self.assertGreater(a['factorization_witness_norm'],.5)
    def test_response_cannot_be_inherited_from_all_same_q_currents(self):
        a=m.audit();self.assertEqual(a['inheritance_verdict'],'NO_FACTOR_THROUGH_SOURCE_QUOTIENT')
        self.assertLess(a['same_q_error'],1e-10);self.assertGreater(a['same_q_response_difference'],.1)
    def test_microscopic_inheritance_fails_quotient(self):
        a=m.audit();self.assertFalse(a['microscopic_inheritance_quotient_covariant'])
        self.assertLess(a['microscopic_q_equivalence_error'],1e-10);self.assertGreater(a['microscopic_target_drift'],1.)
    def test_hodge_depends_on_edge_inner_product(self):
        a=m.audit();self.assertFalse(a['hodge_metric_independent'])
        self.assertGreater(a['hodge_weighted_current_difference'],.05)
        self.assertGreater(a['hodge_weighted_target_difference'],.05)
    def test_zero_target_is_extra_condition(self):
        a=m.audit();self.assertTrue(a['zero_target_lawful']);self.assertFalse(a['zero_target_derived'])
        self.assertGreater(a['zero_target_vs_hodge_current_distance'],.1)
    def test_topology_only_cycle_correction_is_closed(self):
        a=m.audit();self.assertLess(a['topology_cycle_closure_error'],1e-10)
        self.assertGreater(a['topology_cycle_norm'],.1)
    def test_topology_family_same_q_different_targets(self):
        a=m.audit();self.assertEqual(a['topology_family_parameters'],[-1.0,0.0,1.0])
        self.assertLess(a['topology_family_max_source_error'],1e-10)
        self.assertGreater(a['topology_family_target_spread'],1.)
        self.assertGreater(a['topology_family_current_spread'],1.)
    def test_topology_family_is_linear_in_source(self):
        self.assertLess(m.audit()['topology_family_linearity_error'],1e-10)
    def test_topology_family_is_quotient_covariant(self):
        self.assertLess(m.audit()['topology_family_quotient_error'],1e-10)
    def test_topology_family_is_relabeling_covariant(self):
        self.assertLess(m.audit()['topology_family_relabeling_error'],1e-10)
    def test_topology_family_is_not_selected_by_covariance(self):
        a=m.audit();self.assertTrue(a['multiple_covariant_target_laws_survive']);self.assertFalse(a['covariance_selects_target'])
    def test_homology_basis_change_is_coordinate_only(self):
        a=m.audit();self.assertLess(a['homology_basis_reconstruction_error'],1e-10)
        self.assertGreater(a['homology_target_coordinate_change'],.1)
    def test_response_rank_still_closes_given_each_target(self):
        a=m.audit();self.assertTrue(a['rank_gate_closes_given_target']);self.assertLess(a['max_reconstruction_error'],1e-10)
    def test_historical_stop_rules_not_reopened(self):
        a=m.audit();self.assertEqual(a['metric_origin_status'],'CONDITIONAL_NOT_DERIVED')
        self.assertEqual(a['response_rank_status'],'CONDITIONAL_ON_TARGET')
        self.assertEqual(a['source_geometry_pairing_status'],'REQUIRES_NEW_AXIOM_OR_CALIBRATION')
    def test_no_downstream_selector_used(self):
        a=m.audit()
        for k in ('uses_holonomy_as_selector','uses_newton_or_gr','uses_pruning','uses_entropy','uses_physical_time'):
            self.assertFalse(a[k])
    def test_final_verdict(self):
        a=m.audit();self.assertEqual(a['selector_verdict'],'PRETIME_CYCLE_TARGET_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY')
        self.assertFalse(a['cycle_target_derived']);self.assertFalse(a['signal_of_life']);self.assertFalse(a['gravity_canary_certified'])
    def test_next_step_requires_explicit_new_law(self):
        a=m.audit();self.assertEqual(a['next_required_object'],'EXPLICIT_PRETIME_SOURCE_TO_HIGHER_INCIDENCE_COUPLING_AXIOM_OR_NEW_DERIVED_STRUCTURE')
    def test_invalid_alpha_rejected(self):
        c=m.base.base.torus_complex(7);q,_=m.base.base.incidence_defect(c)
        for x in (float('nan'),float('inf'),'x',True):
            with self.assertRaises(ValueError):m.topological_target(c,q,x)
    def test_corner_map_dimensions_and_neutral_cycle(self):
        c=m.base.base.torus_complex(7);A=m.vertex_to_face_average(c)
        self.assertEqual(A.shape,(49,49));np.testing.assert_allclose(A.sum(axis=1),np.ones(49),atol=1e-12)
        q,_=m.base.base.incidence_defect(c);z=c.B2@A@q;self.assertLess(np.linalg.norm(c.B1@z),1e-12)
    def test_schema_fails_closed(self):
        import copy
        a=copy.deepcopy(m.audit());a['selector_verdict']='GRAVITY'
        with self.assertRaises(AssertionError):m.verify_result(a)

if __name__=='__main__':unittest.main(verbosity=2)
