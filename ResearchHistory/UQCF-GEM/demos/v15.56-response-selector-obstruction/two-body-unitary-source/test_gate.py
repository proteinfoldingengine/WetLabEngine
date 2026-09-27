import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():
            raise AssertionError('v15.73 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('unitary_gate',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_exact_commutator_sign_and_commuting_control(self):
        g=self.g;op=g.M.F.op
        np.testing.assert_allclose(g.response(op(1,1,0),op(1,2,1)/np.sqrt(8)),op(0,3,1)/np.sqrt(8),atol=1e-15)
        np.testing.assert_allclose(g.response(op(1,1,0),op(1,1,1)/np.sqrt(8)),0,atol=1e-15)

    def test_rank_uses_external_scale_and_skew_normalization(self):
        g=self.g
        self.assertEqual(g.ranks(np.eye(3)*1e-14,1.),[0,0,0])
        np.testing.assert_allclose(g.skew_coords(np.array([[0.,1,0],[-1,0,0],[0,0,0]])),[np.sqrt(2),0,0],atol=1e-15)

    def test_verdict_preserves_negative_and_invalid(self):
        g=self.g
        self.assertEqual(g.adjudicate(True,True),'TWO_BODY_UNITARY_HIDDEN_ROTATION_CONFIRMED')
        self.assertEqual(g.adjudicate(True,False),'TWO_BODY_UNITARY_HIDDEN_ROTATION_NOT_CONFIRMED')
        self.assertEqual(g.adjudicate(False,True),'INVALID')

    def test_frozen_coverage_and_controls(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['states']),12)
        self.assertEqual(r['probe_cases'],11664)
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertTrue(all(len(x['sources'])==27 for x in r['states']))
        self.assertIn(r['verdict'],['TWO_BODY_UNITARY_HIDDEN_ROTATION_CONFIRMED','TWO_BODY_UNITARY_HIDDEN_ROTATION_NOT_CONFIRMED'])

if __name__=='__main__':unittest.main()
