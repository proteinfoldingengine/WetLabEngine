import importlib.util
import itertools
import unittest
import numpy as np

if importlib.util.find_spec('adaptive'):
    import adaptive as m
else:
    m = None

class AdaptiveTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(m, 'record-dependent simulation not implemented')

    def test_vendor_unchanged(self):
        self.assertEqual(m.verify_vendor(), '95d0303d617422d74e61ae017f0354233ec9454b')

    def test_dependency_edges_are_explicit(self):
        self.assertEqual(set(m.edges()), {('A1','A2'), ('B1','B2'), ('A1','B2')})

    def test_five_schedules(self):
        self.assertEqual(len(m.schedules()), 5)
        self.assertEqual(len(set(m.schedules())), 5)
        self.assertNotIn(('B1','B2','A1','A2'), m.schedules())

    def test_initial_readiness(self):
        self.assertEqual(m.enabled(m.start()), ('A1','B1'))

    def test_after_b1_waits_for_a1(self):
        f=m.advance(m.start(),'B1',0)
        self.assertEqual(m.enabled(f), ('A1',))
        self.assertEqual(m.missing(f,'B2'), ('A1',))

    def test_after_a1_b1_both_remaining_ready(self):
        f=m.advance(m.advance(m.start(),'B1',0),'A1',1)
        self.assertEqual(m.enabled(f), ('A2','B2'))

    def test_premature_event_does_not_mutate_state(self):
        f=m.advance(m.start(),'B1',0); before=f.rho.copy()
        with self.assertRaises(m.MissingRecord): m.advance(f,'B2',1)
        np.testing.assert_array_equal(f.rho,before)
        self.assertEqual(f.records,(('B1',0),))

    def test_full_future_script_does_not_authorize_premature_event(self):
        with self.assertRaises(m.MissingRecord):
            m.run(('B1','B2','A1','A2'),'1001')

    def test_instrument_requires_only_realized_reads(self):
        with self.assertRaises(m.MissingRecord): m.instrument('B2',{'B1':0})
        with self.assertRaises(ValueError): m.instrument('B2',{'A1':1,'B1':0,'B2':1})

    def test_control_value_matters(self):
        u0=m.instrument('B2',{'A1':0,'B1':0})
        u1=m.instrument('B2',{'A1':1,'B1':0})
        self.assertGreater(np.linalg.norm(u0-u1),.1)

    def test_no_future_leak_before_event(self):
        s=m.schedules()[0]
        # Changing B2 outcome cannot affect any earlier state.
        a=m.run(s,'1000'); b=m.run(s,'1001')
        for f,g in zip(a[:-1],b[:-1]):
            np.testing.assert_array_equal(f.rho,g.rho)
            self.assertEqual(f.mass,g.mass)

    def test_history_read_only(self):
        f=m.start()
        with self.assertRaises(ValueError): f.rho[0,0]=1
        with self.assertRaises(Exception): f.records=(('A1',0),)

    def test_all_instruments_complete(self):
        for a in (0,1):
            for event in m.EVENTS:
                context={e:a for e in m.READS[event]}
                u=m.instrument(event,context)
                ks=[m.base.projector(m.EVENTS.index(event),b)@u for b in (0,1)]
                np.testing.assert_allclose(sum(k.conj().T@k for k in ks),np.eye(16),atol=1e-11)

    def test_state_validity_and_record_retention(self):
        for r in (f'{k:04b}' for k in range(16)):
            for s in m.schedules():
                for f in m.run(s,r):
                    self.assertGreaterEqual(np.linalg.eigvalsh(f.rho).min(),-1e-11)
                    self.assertLess(np.linalg.norm(f.rho-f.rho.conj().T),1e-11)
                    self.assertAlmostEqual(np.trace(f.rho).real,1,places=11)
                    p=m.base.record_projector(f.done,r)
                    np.testing.assert_allclose(p@f.rho@p,f.rho,atol=1e-11)

    def test_80_runs_eight_ideals_agree(self):
        a=m.audit()
        self.assertEqual(a['runs_checked'],80)
        self.assertEqual(a['ideals_per_assignment'],8)
        self.assertLess(a['max_state_distance'],1e-11)
        self.assertLess(a['max_mass_error'],1e-11)
        self.assertLess(a['max_subnormalized_error'],1e-11)

    def test_joint_distribution(self):
        for s in m.schedules():
            self.assertAlmostEqual(sum(m.run(s,f'{k:04b}')[-1].mass for k in range(16)),1,places=11)

    def test_conditional_product(self):
        for s in m.schedules():
            fs=m.run(s,'1001')
            self.assertAlmostEqual(np.prod([f.conditional_weight for f in fs[1:]]),fs[-1].mass,places=11)

    def test_every_noncausal_permutation_blocked(self):
        accepted=0; rejected=0
        for s in itertools.permutations(m.EVENTS):
            try: m.run(s,'1001'); accepted+=1
            except m.MissingRecord: rejected+=1
        self.assertEqual((accepted,rejected),(5,19))

    def test_duplicate_event_rejected(self):
        f=m.advance(m.start(),'A1',1)
        with self.assertRaises(ValueError): m.advance(f,'A1',1)

    def test_record_validation(self):
        for bad in (True,2,-1,None,'0'):
            with self.assertRaises(ValueError): m.advance(m.start(),'A1',bad)
        for bad in ('','101',None,'100a'):
            with self.assertRaises(ValueError): m.run(m.schedules()[0],bad)

    def test_channel_family_differs_without_guessing_an_outcome(self):
        a=m.audit()
        self.assertGreater(a['control_channel_choi_distance'],.01)

    def test_guessed_record_control_is_detected_in_mass(self):
        a=m.guess_controls()
        for row in a:
            self.assertGreater(row['max_joint_mass_error'],1e-4)
            self.assertGreater(row['total_variation'],1e-4)
            self.assertLess(row['max_final_state_distance'],1e-11)
            self.assertEqual(row['status'],'REJECTED_RECORD_GUESS_CONTROL')

    def test_backward_compatibility(self):
        # A1, A2, B1 unchanged until adaptive B2.
        s=('A1','A2','B1','B2')
        for f,g in zip(m.run(s,'1001')[:-1],m.base.run(s,'1001')[:-1]):
            np.testing.assert_allclose(f.rho,g.rho,atol=1e-11)
            self.assertAlmostEqual(f.mass,g.mass,places=11)

    def test_scope_no_clock_or_automatic_choice(self):
        a=m.audit()
        self.assertIsNone(a['physical_duration'])
        self.assertFalse(a['physical_causality_derived'])
        self.assertEqual(a['new_physical_axioms'],[])
        self.assertEqual(a['record_rule_status'],'SUPPLIED_ILLUSTRATIVE_FEED_FORWARD')
        self.assertEqual(a['Pillar_3'],'OPEN')

if __name__=='__main__': unittest.main(verbosity=2)
