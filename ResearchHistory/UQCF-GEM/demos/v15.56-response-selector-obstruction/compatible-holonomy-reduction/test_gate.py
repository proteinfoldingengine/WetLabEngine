import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.95 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1595_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_product_rule_does_not_project_unrestricted_controls(self):
        # Catches a missing derivative term or artificial projection to z.
        J=np.array([[[0,0,0],[0,0,-1],[0,1,0]],[[0,0,1],[0,0,0],[-1,0,0]],[[0,-1,0],[1,0,0],[0,0,0]]],float)
        Rs=np.array([np.eye(3)]*3)
        for edge in range(3):
            ws=np.zeros((3,3,3,3));ws[edge]=J
            h,dh,omega,k=self.g.loop_tangent(Rs,ws)
            np.testing.assert_allclose(k,np.eye(3),atol=1e-14)
            np.testing.assert_allclose(omega,J,atol=1e-14)

    def test_exact_stabilizer_and_discrete_noncommutation(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],13)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))
        n=self.g.numerical_controls()
        self.assertTrue(n['valid'])
        self.assertAlmostEqual(n['flip_commutator_squared'],128/25,places=12)

    def test_frozen_aggregation_validity(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),36)
        self.assertEqual(sum(x['lambda']==0 for x in r['rows']),12)
        self.assertEqual((r['verdict'],r['response_verdict']),self.g.adjudicate(r['all_valid'],r['reduction_predicate'],r['response_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['response_verdict']])

    def test_no_and_invalid_are_preserved(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('FIXED_SUPPORT_HOLONOMY_REDUCTION_NOT_CONFIRMED','PLANAR_LOOP_RESPONSE_NOT_CONFIRMED'))
        self.assertEqual(self.g.adjudicate(True,True,False),('FIXED_SUPPORT_HOLONOMY_REDUCTION_CONFIRMED','PLANAR_LOOP_RESPONSE_NOT_CONFIRMED'))
