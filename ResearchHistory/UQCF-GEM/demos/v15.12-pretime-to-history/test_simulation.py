"""Integration tests, not a physical-theory certification."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
import numpy as np

if importlib.util.find_spec('simulation') is not None:
    import simulation as sim
else:
    sim = None
BASE=Path(__file__).resolve().parent
SCENARIO=json.loads((BASE/'scenario.json').read_text())

class IntegratedSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace=sim.build_demo(SCENARIO, cadence=4) if sim else None
    def setUp(self):
        self.assertIsNotNone(sim,'integrated simulation not implemented')
    def test_vendor_is_unchanged(self):
        self.assertEqual(sim.verify_vendor(),'8871e50f19322adbb62f34ea3837ba8e6cb16c8b')
    def test_every_displayed_state_is_positive_and_normalized(self):
        for frame in self.trace.frames:
            self.assertLess(np.linalg.norm(frame.rho-frame.rho.conj().T),1e-11)
            self.assertAlmostEqual(float(np.trace(frame.rho).real),1.0,places=11)
            self.assertGreaterEqual(float(np.linalg.eigvalsh(frame.rho).min()),-1e-11)
    def test_real_pretime_change_is_nontrivial(self):
        self.assertGreater(self.trace.checks['pretime_max_distance'],.1)
    def test_inverse_recovers_pretime_reference(self):
        self.assertLess(self.trace.checks['pretime_reversal_error'],1e-11)
    def test_pretime_has_no_actual_record_or_elapsed_time(self):
        frames=[f for f in self.trace.frames if f.phase.startswith('pretime')]
        self.assertTrue(frames)
        self.assertTrue(all(f.record=='' and f.ordinal==0 for f in frames))
        self.assertIsNone(self.trace.summary()['physical_duration'])
    def test_three_events_use_supplied_actual_records(self):
        self.assertEqual([e['chosen_record'] for e in self.trace.events],[1,0,1])
        self.assertTrue(all(e['selection_origin']=='SUPPLIED_RCR' for e in self.trace.events))
    def test_refinement_strictly_reduces_record_sector(self):
        self.assertEqual([8]+[e['record_rank'] for e in self.trace.events],[8,4,2,1])
        self.assertTrue(all(e['record_inclusion_error']<1e-11 for e in self.trace.events))
    def test_declared_retained_algebras_are_nested(self):
        self.assertEqual([64]+[e['algebra_dimension'] for e in self.trace.events],[64,32,16,8])
        self.assertTrue(all(e['nested_expectation_error']<1e-11 for e in self.trace.events))
    def test_nonselective_weights_normalize(self):
        for event in self.trace.events:
            self.assertAlmostEqual(sum(event['conditional_weights']),1.0,places=11)
            self.assertGreater(min(event['conditional_weights']),0)
    def test_ras_does_not_actualize_a_record(self):
        for f in self.trace.frames:
            if f.phase.startswith('ras'):
                self.assertEqual(f.ordinal,len(f.record))
                self.assertEqual(f.ordinal,f.event_number-1)
    def test_repeated_ras_does_not_add_history(self):
        self.assertTrue(all(e['idempotence_error']<1e-11 for e in self.trace.events))
        for phase in ['ras_1','ras_2','ras_3']:
            self.assertEqual(len(set(f.ordinal for f in self.trace.frames if f.phase==phase)),1)
    def test_phase_distinction_is_lost_by_declared_ras(self):
        self.assertTrue(all(e['witness_before']>.05 for e in self.trace.events))
        self.assertTrue(all(e['witness_after_ras']<1e-11 for e in self.trace.events))
    def test_classical_record_flag_does_not_restore_phase(self):
        self.assertTrue(all(e['witness_with_classical_record']<1e-11 for e in self.trace.events))
    def test_between_record_motion_preserves_prior_records(self):
        self.assertLess(self.trace.checks['retained_record_motion_error'],1e-11)
        for f in self.trace.frames:
            p=sim.prefix_projector(f.record)
            self.assertLess(np.linalg.norm(p@f.rho@p-f.rho),1e-11)
    def test_final_state_matches_supplied_bitstring(self):
        np.testing.assert_allclose(self.trace.frames[-1].rho,sim.prefix_projector('101'),atol=1e-11)
    def test_display_cadence_does_not_change_physics(self):
        other=sim.build_demo(SCENARIO,cadence=7)
        np.testing.assert_allclose(other.frames[-1].rho,self.trace.frames[-1].rho,atol=1e-11)
        self.assertEqual(other.events,self.trace.events)
    def test_all_eight_supplied_histories_work(self):
        for k in range(8):
            scenario=copy.deepcopy(SCENARIO); bits=f'{k:03b}'
            scenario['actual_records']=[int(c) for c in bits]
            trace=sim.build_demo(scenario,cadence=2)
            np.testing.assert_allclose(trace.frames[-1].rho,sim.prefix_projector(bits),atol=1e-11)
    def test_unitary_frame_covariance(self):
        g=sim.unitary(sim.motion_generator(0),.43)
        p=sim.prefix_projectors(1)
        r=sim.initial_state()
        np.testing.assert_allclose(sim.pinch(g@r@g.conj().T,[g@q@g.conj().T for q in p]),g@sim.pinch(r,p)@g.conj().T,atol=1e-11)
    def test_missing_records_are_not_chosen_by_algorithm(self):
        bad=copy.deepcopy(SCENARIO); del bad['actual_records']
        with self.assertRaises(ValueError): sim.build_demo(bad)
    def test_invalid_record_rejected(self):
        bad=copy.deepcopy(SCENARIO); bad['actual_records']=[1,2,0]
        with self.assertRaises(ValueError): sim.build_demo(bad)
    def test_clock_not_accepted_as_input(self):
        bad=copy.deepcopy(SCENARIO); bad['physical_duration']=1.0
        with self.assertRaises(ValueError): sim.build_demo(bad)
    def test_nonfinite_extent_rejected(self):
        bad=copy.deepcopy(SCENARIO); bad['pretime_extent']=float('nan')
        with self.assertRaises(ValueError): sim.build_demo(bad)
    def test_boolean_record_rejected(self):
        bad=copy.deepcopy(SCENARIO); bad['actual_records']=[True,0,1]
        with self.assertRaises(ValueError): sim.build_demo(bad)
    def test_no_automatic_physical_claims(self):
        s=self.trace.summary()
        self.assertEqual(s['new_physical_axioms'],[])
        self.assertEqual(s['status'],'EXECUTED_CONDITIONAL_DEMONSTRATOR')
        self.assertFalse(s['physical_entropy_law_derived'])
        self.assertFalse(s['gravity_derived'])
        self.assertEqual(s['Pillar_3'],'OPEN')

if __name__=='__main__': unittest.main(verbosity=2)
