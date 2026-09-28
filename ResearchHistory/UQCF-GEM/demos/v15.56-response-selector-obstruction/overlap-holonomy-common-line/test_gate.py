import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.96 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1596_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_common_line_is_not_just_commutation(self):
        F=np.diag([1.,-1.,-1.]);Z=np.array([[.6,-.8,0],[.8,.6,0],[0,0,1.]])
        r=self.g.loop_diagnostic(F,Z)
        self.assertEqual(r['B_ranks'],[4,4,4])
        self.assertAlmostEqual(r['commutator_norm']**2,128/25,places=12)
        X=np.array([[1.,0,0],[0,0,-1],[0,1,0]]);Z90=np.array([[0.,-1,0],[1,0,0],[0,0,1.]])
        self.assertEqual(self.g.loop_diagnostic(X,Z90)['B_ranks'],[5,5,5])

    def test_exact_and_inherited_certificates(self):
        c=self.g.symbolic_certificate();self.assertEqual(c['check_count'],13);self.assertTrue(c['valid'])
        old=self.g.V92.symbolic_certificate();self.assertEqual(old['check_count'],45);self.assertTrue(old['valid'])

    def test_global_density_and_frozen_adjudication(self):
        r=self.g.run_measurement();self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),72);self.assertEqual(len(r['channels']),9)
        self.assertEqual((r['verdict'],r['planar_verdict']),self.g.adjudicate(r['all_valid'],r['fullspan_predicate'],r['planar_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['planar_verdict']])

    def test_no_and_invalid_are_preserved(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('OVERLAP_COMMON_LINE_OBSTRUCTION_NOT_CONFIRMED','PLANAR_COMMON_LINE_PRESERVATION_NOT_CONFIRMED'))
