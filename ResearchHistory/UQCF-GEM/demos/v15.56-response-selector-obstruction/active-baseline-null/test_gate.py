import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():raise AssertionError('v15.77 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('active_gate',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_skew_lift_normalization(self):
        g=self.g;z=g.skew_lift(np.eye(3))
        self.assertAlmostEqual(np.linalg.norm(z),np.sqrt(3/8),places=14)
        np.testing.assert_allclose(g.M.moments(z,g.M.ONE),0,atol=1e-15)
        pairs=g.M.moments(z,g.M.PAIR).reshape(3,3,3)
        np.testing.assert_allclose(pairs[0],np.sqrt(3)*g.K,atol=1e-15)
        np.testing.assert_allclose(pairs[1:],0,atol=1e-15)

    def test_adjudication_keeps_gates_separate(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,False,True),('ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_NOT_CONFIRMED','EQUAL_NORM_SKEW_BASELINE_VISIBLE_CONFIRMED'))
        self.assertEqual(g.adjudicate(True,True,False),('ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_CONFIRMED','EQUAL_NORM_SKEW_BASELINE_VISIBLE_NOT_CONFIRMED'))

    def test_frozen_coverage_and_controls(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(r['finite_cases'],3888)
        self.assertEqual(len(r['rows']),144)
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_CONFIRMED','ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_NOT_CONFIRMED'])
        self.assertIn(r['skew_verdict'],['EQUAL_NORM_SKEW_BASELINE_VISIBLE_CONFIRMED','EQUAL_NORM_SKEW_BASELINE_VISIBLE_NOT_CONFIRMED'])

if __name__=='__main__':unittest.main()
