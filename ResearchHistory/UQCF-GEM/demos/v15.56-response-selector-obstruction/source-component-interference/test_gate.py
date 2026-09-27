import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        if not p.exists():raise AssertionError('v15.81 scientific implementation absent: expected RED')
        s=importlib.util.spec_from_file_location('interference81',p)
        cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_verdicts_keep_domain_no(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,True,False),('MATCHED_COMPONENT_INTERFERENCE_RESPONSE_CONFIRMED','FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED'))
        self.assertEqual(g.adjudicate(True,False,True),('MATCHED_COMPONENT_INTERFERENCE_RESPONSE_NOT_CONFIRMED','FINITE_COMPONENT_INTERFERENCE_WINDOW_CONFIRMED'))

    def test_zero_interference_weights(self):
        g=self.g
        w=g.weights(0,.1)
        self.assertAlmostEqual(sum(w),1,places=14)
        self.assertAlmostEqual(w[1]-w[2],0,places=14)
        self.assertAlmostEqual(g.retained_factor(1,.1),(1-np.exp(-.2))/2,places=14)

    def test_frozen_coverage_validity(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['generator_rows']),60)
        self.assertEqual(len(r['finite_rows']),240)
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['MATCHED_COMPONENT_INTERFERENCE_RESPONSE_CONFIRMED','MATCHED_COMPONENT_INTERFERENCE_RESPONSE_NOT_CONFIRMED'])
        self.assertIn(r['finite_verdict'],['FINITE_COMPONENT_INTERFERENCE_WINDOW_CONFIRMED','FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED'])
        for row in r['finite_rows']:
            if not row['polar_domain']['valid']:
                self.assertIsNone(row['Q']);self.assertIsNone(row['E'])
                self.assertEqual(r['finite_verdict'],'FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED')

if __name__=='__main__':unittest.main()
