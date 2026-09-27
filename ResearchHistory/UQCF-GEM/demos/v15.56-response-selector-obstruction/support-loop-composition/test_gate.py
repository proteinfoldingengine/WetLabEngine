import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        if not p.exists():raise AssertionError('v15.83 scientific implementation absent: expected RED')
        s=importlib.util.spec_from_file_location('support83',p)
        cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_closed_obstructed_and_unresolved_are_distinct(self):
        g=self.g
        self.assertEqual(g.composition_verdict([0,0,0]),'SUPPORT_LOOP_COMPOSITION_CLOSED')
        self.assertEqual(g.composition_verdict([.1,0,0]),'SUPPORT_LOOP_COMPOSITION_OBSTRUCTED')
        self.assertEqual(g.composition_verdict([1e-20,0,0]),'SUPPORT_LOOP_COMPOSITION_UNRESOLVED')
        self.assertEqual(g.core_verdict([0,0,0]),'LOSSLESS_LOOP_CORE_TRIVIAL')
        self.assertEqual(g.core_verdict([1,1,1]),'LOSSLESS_LOOP_CORE_NONTRIVIAL')
        self.assertEqual(g.core_verdict([0,1,1]),'LOSSLESS_LOOP_CORE_UNRESOLVED')

    def test_partial_isometry_and_lossless_core_controls(self):
        r=self.g.synthetic_controls()
        self.assertTrue(r['valid'],r)
        self.assertEqual(r['projector_dimensions'],[2,2,2,2])
        self.assertEqual(r['cycle_dimensions'],[2,1,0,0])

    def test_frozen_witness_valid_execution(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(r['candidate_index'],46)
        self.assertEqual([x['delta'] for x in r['crossing_rows']],['1e-3','1e-5','1e-7'])
        self.assertEqual([x['n'] for x in r['powers']],[1,2,3,4])
        self.assertIn(r['crossing_verdict'],['SUPPORT_RESTRICTED_CROSSING_CONFIRMED','SUPPORT_RESTRICTED_CROSSING_NOT_CONFIRMED'])
        self.assertIn(r['composition_verdict'],['SUPPORT_LOOP_COMPOSITION_CLOSED','SUPPORT_LOOP_COMPOSITION_OBSTRUCTED','SUPPORT_LOOP_COMPOSITION_UNRESOLVED'])
        self.assertIn(r['core_verdict'],['LOSSLESS_LOOP_CORE_TRIVIAL','LOSSLESS_LOOP_CORE_NONTRIVIAL','LOSSLESS_LOOP_CORE_UNRESOLVED'])
        self.assertEqual(r['powers'][0]['lossless_dimensions'],[2,2,2])
        self.assertIsNone(r['root_Q']);self.assertIsNone(r['root_E'])

if __name__=='__main__':unittest.main()
