import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.93 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1593_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_proper_completion_and_zero_eigenvalue_derivative(self):
        # Catches missing cofactor, reflection sign error and diagonal 0/0.
        for C,expected in [(np.diag([2.,3.,0.]),np.eye(3)),(np.diag([2.,-3.,0.]),np.diag([1.,-1.,-1.]))]:
            R,P,V=self.g.oriented(C)
            np.testing.assert_allclose(R,expected,atol=1e-14)
            np.testing.assert_allclose(R@P,C,atol=1e-14)
        C=np.diag([2.,3.,0.]);D=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,0.]])
        R,P,V=self.g.oriented(C);Q,W=self.g.tangent(R,P,D)
        np.testing.assert_allclose(W,[[0.,-.4,0.],[.4,0.,0.],[0.,0.,0.]],atol=1e-14)
        np.testing.assert_allclose(P@W+W@P,Q,atol=1e-14)

    def test_exact_rank_boundary_certificate(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],14)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))

    def test_frozen_measurement_and_validity(self):
        # Independent identities/physicality must pass, but a scientific NO is accepted.
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),36)
        self.assertEqual(len(r['channels']),6)
        self.assertEqual(sum(x['lambda']==0 for x in r['rows']),12)
        self.assertEqual((r['verdict'],r['response_verdict']),self.g.adjudicate(r['all_valid'],r['domain_predicate'],r['response_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['response_verdict']])

    def test_no_and_invalid_are_preserved(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('ORIENTED_RANK_TWO_READOUT_NOT_CONFIRMED','PLANAR_ORIENTED_RESPONSE_NOT_CONFIRMED'))
        self.assertEqual(self.g.adjudicate(True,True,False),('ORIENTED_RANK_TWO_READOUT_CONFIRMED','PLANAR_ORIENTED_RESPONSE_NOT_CONFIRMED'))
