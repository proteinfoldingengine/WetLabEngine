import importlib.util
import pathlib
import unittest
import numpy as np


class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():
            raise AssertionError('v15.72 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('mixture_gate',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_mixture_defect_distinguishes_affine_and_nonlinear_maps(self):
        a=np.array([[.8,0],[0,.2]]);b=np.array([[.2,0],[0,.8]])
        z=np.diag([1.,-1.])
        np.testing.assert_allclose(self.g.mixture_defect(lambda r:2*r+z,a,b,.25),np.zeros((2,2)),atol=1e-15)
        d=self.g.mixture_defect(lambda r:float(np.trace(z@r))**2*z,a,b,.25)
        np.testing.assert_allclose(d,.27*z,atol=1e-15)

    def test_skew_coordinates_are_hs_normalized(self):
        q=np.array([[0.,1.,0.],[-1.,0.,0.],[0.,0.,0.]])
        np.testing.assert_allclose(self.g.skew_coords(q),[np.sqrt(2),0.,0.],atol=1e-15)

    def test_adjudication_preserves_obstruction_negative_and_invalid(self):
        g=self.g
        self.assertEqual(g.adjudicate(True,[1.],True),('UNCONDITIONED_MIXTURE_AFFINITY_OBSTRUCTED','PREPARATION_DEPENDENT_SKEW_CONFIRMED'))
        self.assertEqual(g.adjudicate(True,[0.],True),('MIXTURE_AFFINITY_NOT_OBSTRUCTED_ON_PROBES','PREPARATION_DEPENDENT_SKEW_NOT_CONFIRMED'))
        self.assertEqual(g.adjudicate(True,[1.],False),('UNCONDITIONED_MIXTURE_AFFINITY_OBSTRUCTED','PREPARATION_DEPENDENT_SKEW_NOT_CONFIRMED'))
        self.assertEqual(g.adjudicate(False,[1.],True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,[float('nan')],True),('INVALID','INVALID'))

    def test_measurement_frozen_coverage_and_controls(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['rows']),972)
        self.assertEqual(len(r['rank_rows']),36)
        self.assertTrue(r['all_valid'],r)
        for x in r['rows']:
            self.assertGreater(x['toy_norm'],1e-10)
            self.assertLessEqual(x['toy_relative_error'],1e-8)
            self.assertLessEqual(x['unitary_mixture_error'],1e-12)
        self.assertIn(r['verdict'],['UNCONDITIONED_MIXTURE_AFFINITY_OBSTRUCTED','MIXTURE_AFFINITY_NOT_OBSTRUCTED_ON_PROBES'])


if __name__=='__main__':unittest.main()
