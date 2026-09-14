import importlib.util, pathlib, sys, unittest, numpy as np
m=None
path=pathlib.Path(__file__).with_name('selector_rank.py')
if path.exists():
    spec=importlib.util.spec_from_file_location('selector_rank',path);m=importlib.util.module_from_spec(spec);sys.modules['selector_rank']=m;spec.loader.exec_module(m)

class SelectorRankTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(m,'selector-rank implementation absent')
    def test_v1525_kill_is_preserved(self):
        self.assertEqual(m.base.audit()['canary_verdict'],'KILLED_BARE_COMPATIBILITY_DOES_NOT_FORCE_GLOBAL_RESPONSE')
    def test_torus_homology_dimensions(self):
        a=m.audit();self.assertEqual(a['cycle_dimension'],50);self.assertEqual(a['face_boundary_rank'],48);self.assertEqual(a['homology_dimension'],2)
    def test_face_response_cannot_resolve_harmonic_cycles(self):
        a=m.audit();self.assertEqual(a['face_response_rank_on_cycle_space'],48);self.assertEqual(a['face_response_residual_cycle_freedom'],2)
    def test_full_topological_response_resolves_cycle_space(self):
        a=m.audit();self.assertEqual(a['full_response_rank_on_cycle_space'],50);self.assertGreater(a['full_response_sigma_min'],1e-3)
    def test_period_rows_are_cycles_dual_controls(self):
        c=m.base.torus_complex(7);H=m.period_rows(c)
        self.assertEqual(H.shape,(2,98));self.assertLess(np.linalg.norm(H@c.B2),1e-10)
        rank=np.linalg.matrix_rank(c.B1,tol=1e-10);Z=np.linalg.svd(c.B1,full_matrices=True)[2][rank:].T
        self.assertEqual(np.linalg.matrix_rank(H@Z,tol=1e-10),2)
    def test_three_targets_reconstruct_three_different_currents(self):
        a=m.audit();self.assertLess(a['hodge_reconstruction_error'],1e-10);self.assertLess(a['local_reconstruction_error'],1e-10);self.assertLess(a['cycle_shift_reconstruction_error'],1e-10)
        self.assertGreater(a['hodge_vs_local_distance'],.1);self.assertGreater(a['cycle_shift_vs_hodge_distance'],.1)
    def test_all_targets_have_same_source(self):
        a=m.audit();self.assertLess(a['max_common_source_residual'],1e-10)
    def test_hodge_target_reconstructs_global_representative_without_metric_in_solver(self):
        a=m.audit();self.assertLess(a['hodge_reconstruction_error'],1e-10);self.assertGreater(a['hodge_remote_holonomy'],1e-4)
    def test_face_zero_target_leaves_two_harmonic_modes(self):
        a=m.audit();self.assertEqual(a['face_response_residual_cycle_freedom'],2);self.assertTrue(a['face_zero_target_not_unique'])
    def test_microscopic_inheritance_selects_local_cancellation(self):
        a=m.audit();self.assertLess(a['microscopic_target_local_error'],1e-10);self.assertLess(a['microscopic_target_remote_holonomy'],1e-12)
    def test_q_alone_does_not_choose_cycle_target(self):
        a=m.audit();self.assertTrue(a['same_q_multiple_full_rank_targets']);self.assertFalse(a['cycle_target_derived'])
    def test_source_equivalence_shift_changes_microscopic_target(self):
        a=m.audit();self.assertLess(a['equivalent_source_q_error'],1e-10);self.assertGreater(a['equivalent_source_target_difference'],.1)
    def test_target_zero_is_not_implied_by_compatibility(self):
        a=m.audit();self.assertTrue(a['zero_target_is_additional_condition']);self.assertEqual(a['selector_verdict'],'CYCLE_RESPONSE_TARGET_NOT_DERIVED')
    def test_response_rank_theorem_matches_reconstruction(self):
        a=m.audit();self.assertTrue(a['rank_gate_closes_given_target']);self.assertFalse(a['rank_gate_supplies_target'])
    def test_no_metric_pruning_time_or_gr_fit(self):
        a=m.audit()
        for k in ('uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time','fits_newton_or_gr','physical_gravity_derived'):
            self.assertFalse(a[k])
    def test_canary_stays_negative_until_target_origin(self):
        a=m.audit();self.assertFalse(a['signal_of_life']);self.assertFalse(a['gravity_canary_certified'])
    def test_invalid_target_dimensions_rejected(self):
        c=m.base.torus_complex(7);q,_=m.base.incidence_defect(c)
        with self.assertRaises(ValueError):m.reconstruct(c.B1,q,np.zeros((2,97)),np.zeros(2))
        with self.assertRaises(ValueError):m.reconstruct(c.B1,q,np.zeros((2,98)),np.zeros(3))
    def test_non_neutral_source_rejected(self):
        c=m.base.torus_complex(7);q=np.zeros(49);q[0]=1
        with self.assertRaises(ValueError):m.reconstruct(c.B1,q,m.response_operator(c),np.zeros(51))
    def test_permutation_invariance_of_rank_gate(self):
        self.assertLess(m.audit()['rank_gate_permutation_error'],1e-10)
    def test_result_schema_has_next_target(self):
        a=m.audit();self.assertEqual(a['next_required_object'],'PRETIME_SOURCE_TO_CYCLE_RESPONSE_TARGET_LAW')

if __name__=='__main__':unittest.main(verbosity=2)
