import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.94 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1594_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_nonmultiplicative_completion_and_rank_one_rejection(self):
        # Catches completing factors before raw multiplication or filling rank-one axes.
        P=np.diag([1.,1.,0.]);U=np.array([[.6,0,.8],[0,1,0],[-.8,0,.6]])
        r=self.g.pair_diagnostic(U@P@U.T,P)
        self.assertEqual(r['product_ranks'],[2,2,2])
        self.assertAlmostEqual(r['discrepancy_squared'],1.6,places=12)
        self.assertAlmostEqual(r['c'],.6,places=12)
        self.assertAlmostEqual(self.g.pair_diagnostic(P,P)['discrepancy'],0.,places=12)
        with self.assertRaises(ValueError):self.g.complete(np.diag([1.,0.,0.]))

    def test_exact_compatibility_certificate(self):
        r=self.g.symbolic_certificate()
        self.assertEqual(r['check_count'],12)
        self.assertTrue(r['valid'])
        self.assertTrue(all(r['checks'].values()))

    def test_native_measurement_validity(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['planar_rows']),36)
        self.assertEqual(sum(len(x['pairs']) for x in r['planar_rows']),108)
        self.assertEqual(len(r['fixtures']),3)
        self.assertEqual((r['verdict'],r['matched_verdict']),self.g.adjudicate(r['all_valid'],r['obstruction_predicate'],r['matched_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['matched_verdict']])

    def test_negative_and_invalid_are_not_rescued(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('ORIENTED_COMPOSITION_OBSTRUCTION_NOT_CONFIRMED','MATCHED_SUPPORT_COMPOSITION_NOT_CONFIRMED'))
        self.assertEqual(self.g.adjudicate(True,True,False),('ORIENTED_COMPOSITION_OBSTRUCTED','MATCHED_SUPPORT_COMPOSITION_NOT_CONFIRMED'))
