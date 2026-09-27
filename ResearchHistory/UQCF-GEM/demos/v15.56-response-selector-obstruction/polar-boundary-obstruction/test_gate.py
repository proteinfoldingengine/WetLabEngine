import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        if not p.exists():
            raise AssertionError('v15.82 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('polar_boundary82',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_preserves_scientific_no_and_invalid(self):
        self.assertEqual(self.g.adjudicate(False,True),'INVALID')
        self.assertEqual(self.g.adjudicate(True,False),'POLAR_CONTINUATION_OBSTRUCTION_NOT_CONFIRMED')
        self.assertEqual(self.g.adjudicate(True,True),'POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED')

    def test_complex_transport_and_exact_root_controls(self):
        g=self.g
        z=g.np.array([[.5,.125j],[-.125j,.5]])
        self.assertEqual(g.to_numpy(g.exact_matrix(z))[0,1],.125j)
        r=g.synthetic_controls()
        self.assertTrue(r['valid'],r)
        self.assertEqual(r['crossing_root_count'],1)
        self.assertEqual(r['smooth_root_count'],0)

    def test_frozen_witness_and_valid_execution(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(r['candidate_index'],46)
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(r['lambda'],-1)
        self.assertEqual(r['edge'],[0,1])
        self.assertEqual(len(r['identity_checks']),5)
        self.assertIn(r['verdict'],['POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED','POLAR_CONTINUATION_OBSTRUCTION_NOT_CONFIRMED'])
        if r['unique_simple_root']:
            self.assertEqual([x['delta'] for x in r['sides']],['1e-3','1e-5','1e-7'])
            self.assertIsNone(r['root']['Q'])
            self.assertIsNone(r['root']['E'])
        if r['verdict']=='POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED':
            self.assertTrue(all(r['gate_checks'].values()))

if __name__=='__main__':unittest.main()
