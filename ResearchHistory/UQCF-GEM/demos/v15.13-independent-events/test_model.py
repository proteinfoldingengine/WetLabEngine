import importlib.util
import unittest
import numpy as np

if importlib.util.find_spec('event_model'):
    import event_model as m
else:
    m = None

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(m, 'independent-event model not implemented')

    def test_six_schedules(self):
        self.assertEqual(len(m.schedules()), 6)
        self.assertEqual(len(set(m.schedules())), 6)

    def test_all_schedules_preserve_local_dependencies(self):
        for s in m.schedules():
            self.assertLess(s.index('A1'), s.index('A2'))
            self.assertLess(s.index('B1'), s.index('B2'))

    def test_invalid_schedule_rejected(self):
        for s in [('A2','A1','B1','B2'),('A1','A1','B1','B2'),('A1','B1')]:
            with self.assertRaises(ValueError): m.run(s, '1001')

    def test_explicit_records_required(self):
        for r in (None, '', '100', '10x1', [True,0,0,1]):
            with self.assertRaises(ValueError): m.run(m.schedules()[0], r)

    def test_initial_state_full_rank(self):
        r=m.initial_state()
        self.assertGreater(np.linalg.eigvalsh(r).min(), 0)
        self.assertAlmostEqual(np.trace(r).real,1)

    def test_pretime_motion_reversible(self):
        c=m.pretime_control()
        self.assertGreater(c['state_change'],.1)
        self.assertLess(c['inverse_error'],1e-11)

    def test_joint_input_not_product(self):
        self.assertGreater(m.pretime_control()['product_state_residual'],.05)

    def test_cross_stream_kraus_operators_commute(self):
        self.assertLess(m.commutator_residual(),1e-11)

    def test_local_motion_preserves_previous_record(self):
        for e,q in [('A2',0),('B2',2)]:
            u=m.event_unitary(e)
            for b in (0,1):
                p=m.projector(q,b)
                self.assertLess(np.linalg.norm(u@p-p@u),1e-11)

    def test_maps_form_complete_instrument(self):
        for e in m.EVENTS:
            ks=[m.kraus(e,b) for b in (0,1)]
            np.testing.assert_allclose(sum(k.conj().T@k for k in ks),np.eye(16),atol=1e-11)

    def test_every_state_valid(self):
        for s in m.schedules():
            for f in m.run(s,'1001'):
                r=f.rho
                self.assertGreaterEqual(np.linalg.eigvalsh(r).min(),-1e-11)
                self.assertLess(np.linalg.norm(r-r.conj().T),1e-11)
                self.assertAlmostEqual(np.trace(r).real,1,places=11)

    def test_record_sector_rank(self):
        for s in m.schedules():
            fs=m.run(s,'1001')
            self.assertEqual([f.record_rank for f in fs],[16,8,4,2,1])

    def test_record_persistence(self):
        for s in m.schedules():
            for f in m.run(s,'1001'):
                p=m.record_projector(f.done,'1001')
                np.testing.assert_allclose(p@f.rho@p,f.rho,atol=1e-11)

    def test_every_shared_ideal_agrees(self):
        c=m.compare_schedules('1001')
        self.assertEqual(c['ideal_count'],9)
        self.assertLess(c['max_shared_ideal_state_error'],1e-11)
        self.assertLess(c['max_shared_ideal_mass_error'],1e-11)
        self.assertLess(c['max_shared_ideal_subnormalized_error'],1e-11)

    def test_all_96_runs(self):
        a=m.audit()
        self.assertEqual(a['record_assignments'],16)
        self.assertEqual(a['runs_checked'],96)
        self.assertLess(a['max_state_error'],1e-11)
        self.assertLess(a['max_mass_error'],1e-11)

    def test_joint_record_distribution_normalizes(self):
        for s in m.schedules():
            mass=sum(m.run(s,f'{k:04b}')[-1].mass for k in range(16))
            self.assertAlmostEqual(mass,1,places=11)

    def test_conditional_factors_multiply_to_joint_mass(self):
        for s in m.schedules():
            fs=m.run(s,'1001')
            self.assertAlmostEqual(np.prod([f.conditional_weight for f in fs[1:]]),fs[-1].mass,places=11)

    def test_event_conditionals_can_differ(self):
        a=m.audit()
        self.assertGreater(a['max_contextual_weight_change'],.001)

    def test_coupled_negative_control_detected(self):
        c=m.negative_control()
        self.assertGreater(c['cross_commutator'],.01)
        self.assertGreater(c['shared_ideal_state_error'],.001)
        self.assertGreater(c['joint_mass_difference'],.001)

    def test_premature_global_clock_not_derived(self):
        a=m.audit()
        self.assertIsNone(a['physical_duration'])
        self.assertEqual(a['new_physical_axioms'],[])
        self.assertFalse(a['source_law_derived'])

    def test_ras_removes_phase_witness(self):
        for s in m.schedules():
            for f in m.run(s,'1001')[1:]:
                self.assertLess(f.witness_after,1e-11)
        self.assertGreater(m.run(m.schedules()[0],'1001')[1].witness_before,.05)

    def test_zero_probability_branch_rejected(self):
        rho=np.diag([1.]+[0.]*15)
        with self.assertRaises(ValueError):
            m.apply_selected(rho,m.projector(0,1))

    def test_frame_covariance(self):
        rho=m.initial_state(); u=m.unitary(m.PAULIS['Y'],.7)
        v=np.kron(u,np.eye(8)); k=m.kraus('A1',1)
        left=m.apply_selected(v@rho@v.conj().T,v@k@v.conj().T)
        right=m.apply_selected(rho,k)
        np.testing.assert_allclose(left[0],v@right[0]@v.conj().T,atol=1e-11)
        self.assertAlmostEqual(left[1],right[1],places=11)

if __name__=='__main__': unittest.main(verbosity=2)
