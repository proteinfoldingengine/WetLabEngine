"""Tests frozen before the v15.71 implementation."""
import importlib.util
import pathlib
import unittest
import numpy as np


class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():
            raise AssertionError('v15.71 scientific implementation absent: expected RED')
        spec = importlib.util.spec_from_file_location('memory_gate', path)
        cls.g = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.g)

    def test_polar_derivative_against_exact_diagonal_solution(self):
        c = np.diag([2.,3.,4.]); k = np.array([[0.,1.,0.],[-1.,0.,0.],[0.,0.,0.]])
        np.testing.assert_allclose(self.g.polar_derivative(c, k), .4*k, atol=1e-14)
        np.testing.assert_allclose(self.g.polar_derivative(c, np.eye(3)), np.zeros((3,3)), atol=1e-14)

    def test_regional_lift_and_explicit_memory_response(self):
        i=np.eye(2);x=np.array([[0,1],[1,0]]);y=np.array([[0,-1j],[1j,0]]);z=np.diag([1,-1])
        xx,yy,zz=[np.kron(p,p) for p in [x,y,z]]
        rho=(np.eye(4)+.1*xx+.08*yy+.06*zz)/4
        expected=(xx+yy+zz)/(4*np.sqrt(3))
        np.testing.assert_allclose(self.g.regional_lift(rho), expected, atol=1e-14)
        np.testing.assert_allclose(self.g.regional_step(rho,.02,.1),rho+.002*expected,atol=1e-14)
        np.testing.assert_allclose(self.g.regional_step(rho,0.,.1),rho,atol=1e-14)
        # Keeps complex state entries and ordered subsystem coordinates.
        a=np.array([[.5,-.5j],[.5j,.5]])
        full=np.kron(np.kron(a,i/2),z*.1+i/2)
        np.testing.assert_allclose(self.g.V70.restrict(full,(2,0)),np.kron(z*.1+i/2,a),atol=1e-14)

    def test_zero_source_memory_and_nonzero_shifted_memory(self):
        base=self.g.V70.V64.ASYM.select_states()[0]['rho'];h=self.g.HIDDEN[0]
        np.testing.assert_allclose(self.g.field(base,h),np.zeros((8,8)),atol=1e-13)
        y=self.g.global_lift(base)
        np.testing.assert_allclose(self.g.field(base+1e-4*h,h),1e-4*y,atol=1e-13)

    def test_adjudication_does_not_force_a_scientific_pass(self):
        g=self.g
        self.assertEqual(g.adjudicate(True,True,[1.]),('MEMORY_ENRICHED_NULL_CONFIRMED','FROZEN_FULL_JACOBIAN_OBSTRUCTED'))
        self.assertEqual(g.adjudicate(True,False,[0.]),('MEMORY_ENRICHED_NULL_NOT_CONFIRMED','FROZEN_FULL_JACOBIAN_NOT_OBSTRUCTED_ON_PROBES'))
        self.assertEqual(g.adjudicate(False,True,[1.]),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,True,[float('nan')]),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,True,[]),('INVALID','INVALID'))

    def test_full_measurement_has_frozen_counts_and_valid_controls(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(r['n_cases'],972)
        self.assertEqual(r['n_edge_restrictions'],2916)
        self.assertEqual(len(r['derivative_rows']),12)
        self.assertTrue(r['all_valid'],r)
        for row in r['derivative_rows']:
            self.assertEqual(len(row['visible_columns']),27)
            self.assertEqual(len(row['curl_singular_values']),27)
            self.assertGreater(row['skew_control'],1.)
            self.assertEqual(row['constant_lift_curl_control'],0.)


if __name__=='__main__':
    unittest.main()
