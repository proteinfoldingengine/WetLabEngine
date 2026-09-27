import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():raise AssertionError('v15.78 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('covariance78',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_adjudication_preserves_no(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,False,True),('SOURCE_FREE_COVARIANCE_CLOSURE_NOT_CONFIRMED','COVARIANTIZATION_ERASES_POSITIVE_AND_NULL_LEAKAGE'))
        self.assertEqual(g.adjudicate(True,True,False),('SOURCE_FREE_COVARIANCE_FORCES_RETAINED_CLOSURE','COVARIANTIZATION_ERASURE_NOT_CONFIRMED'))

    def test_projector_does_not_preserve_cross_support(self):
        g=self.g;x=np.zeros((64,64));x[1,63]=1
        np.testing.assert_allclose(g.support_project(x),0,atol=1e-15)
        np.testing.assert_allclose(g.support_project(np.eye(64)),np.eye(64),atol=1e-15)

    def test_frozen_coverage_and_validity(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['rows']),72)
        self.assertEqual(r['hidden_probes_per_row'],27)
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['SOURCE_FREE_COVARIANCE_FORCES_RETAINED_CLOSURE','SOURCE_FREE_COVARIANCE_CLOSURE_NOT_CONFIRMED'])
        self.assertIn(r['erasure_verdict'],['COVARIANTIZATION_ERASES_POSITIVE_AND_NULL_LEAKAGE','COVARIANTIZATION_ERASURE_NOT_CONFIRMED'])

if __name__=='__main__':unittest.main()
