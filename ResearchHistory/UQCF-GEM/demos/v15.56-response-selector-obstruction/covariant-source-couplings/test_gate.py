import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        if not p.exists():raise AssertionError('v15.79 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('couplings79',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_adjudication_preserves_no(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,False,True),('COVARIANT_SOURCE_COUPLING_CLASSIFICATION_NOT_CONFIRMED','COVARIANT_COUPLINGS_ENSEMBLE_NULL_EXCLUDED'))
        self.assertEqual(g.adjudicate(True,True,False),('COVARIANT_SOURCE_COUPLING_CLASSIFICATION_CONFIRMED','COVARIANT_COUPLINGS_ENSEMBLE_NULL_NOT_EXCLUDED'))

    def test_local_cross_convention(self):
        g=self.g;t=g.local_tensor(True,True)
        self.assertEqual(t.shape,(3,3,3))
        self.assertEqual(t[2,0,1],1)
        self.assertEqual(t[2,1,0],-1)
        np.testing.assert_allclose(np.einsum('rah,a,h->r',t,[1,0,0],[0,1,0]),[0,0,1],atol=0)

    def test_frozen_coverage_and_validity(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['states']),12)
        self.assertEqual(r['source_count'],63)
        self.assertEqual(r['hidden_count'],27)
        self.assertEqual(r['stacked_Q']['shape'],[183708,18])
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['COVARIANT_SOURCE_COUPLING_CLASSIFICATION_CONFIRMED','COVARIANT_SOURCE_COUPLING_CLASSIFICATION_NOT_CONFIRMED'])
        self.assertIn(r['observability_verdict'],['COVARIANT_COUPLINGS_ENSEMBLE_NULL_EXCLUDED','COVARIANT_COUPLINGS_ENSEMBLE_NULL_NOT_EXCLUDED'])

if __name__=='__main__':unittest.main()
