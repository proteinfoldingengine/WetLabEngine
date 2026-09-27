import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():raise AssertionError('v15.75 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('affine_gate',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_choi_convention_identity_and_transpose(self):
        g=self.g
        j=g.choi(lambda z:z,2)
        v=np.array([1.,0.,0.,1.])
        np.testing.assert_allclose(j,np.outer(v,v),atol=1e-15)
        np.testing.assert_allclose(g.trace_output(j,2),np.eye(2),atol=1e-15)
        self.assertLess(np.linalg.eigvalsh(g.choi(lambda z:z.T,2)).min(),-.9)

    def test_three_validity_outcomes(self):
        g=self.g
        self.assertEqual(g.adjudicate(True,True,True),('AFFINE_OPEN_NULL_RETAINED_CLOSED_CONFIRMED','CPTP_POINTWISE_NULL_ONLY_CONFIRMED'))
        self.assertEqual(g.adjudicate(True,False,False),('AFFINE_RETAINED_NULL_NOT_EXCLUDED','CPTP_POINTWISE_NULL_ONLY_NOT_CONFIRMED'))
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))

    def test_frozen_coverage_controls_and_verdicts(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(r['stack_shape'],[108,36])
        self.assertEqual(r['finite_cases'],972)
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['AFFINE_OPEN_NULL_RETAINED_CLOSED_CONFIRMED','AFFINE_RETAINED_NULL_NOT_EXCLUDED'])
        self.assertIn(r['channel_verdict'],['CPTP_POINTWISE_NULL_ONLY_CONFIRMED','CPTP_POINTWISE_NULL_ONLY_NOT_CONFIRMED'])

if __name__=='__main__':unittest.main()
