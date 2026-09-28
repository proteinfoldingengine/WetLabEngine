import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.97 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1597_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_generator_cross_leakage_and_incoherent_null(self):
        # Wrong cross coefficient or complex transport changes these operators.
        g=self.g;I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
        for a,b,c,d in [(X,X,Z,I),(Z,X,X,I),(Y,Y,-I,Z),(Y,Z,I,Y)]:
            h=g.V96.tensor([a,b,X,I])/4
            cross=g.generator(h,1)-g.generator(h,0)
            np.testing.assert_allclose(cross,g.V96.tensor([c,d,X,I])/4,atol=1e-14)
        c=g.symbolic_certificate();self.assertEqual(c['check_count'],8);self.assertTrue(c['valid'])

    def test_polar_tangent_and_loop_product(self):
        # Catches denominator, sign, product-rule and trivialization mistakes.
        g=self.g;P=np.diag([2.,3.,0.]);D=np.array([[0.,-2.,0.],[3.,0.,0.],[0.,0.,0.]])
        Q,W=g.V93.tangent(np.eye(3),P,D)
        np.testing.assert_allclose(W,[[0,-1,0],[1,0,0],[0,0,0]],atol=1e-14)
        rs=[np.eye(3)]*5;dr=np.zeros((5,3,3));dr[1]=W
        hs,dhs=g.loop_derivative(rs,dr)
        np.testing.assert_allclose(dhs[0],W,atol=1e-14);np.testing.assert_allclose(dhs[1],0,atol=1e-14)
        np.testing.assert_allclose(g.invariant_derivative(hs,dhs),0,atol=1e-14)

    def test_frozen_measurement_and_valid_scientific_no(self):
        r=self.g.run_measurement();self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),72);self.assertEqual(r['hidden_count'],54);self.assertEqual(r['weight_four_count'],81)
        self.assertEqual((r['verdict'],r['planar_verdict']),self.g.adjudicate(r['all_valid'],r['full_predicate'],r['plane_predicate']))

    def test_no_and_invalid_adjudication(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('OVERLAP_HIDDEN_RESPONSE_NOT_CONFIRMED','PLANAR_TWO_LOOP_RESPONSE_NOT_CONFIRMED'))

if __name__=='__main__':unittest.main()
