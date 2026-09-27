import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():raise AssertionError('v15.76 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('composition_gate',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_depth_coefficients(self):
        g=self.g
        np.testing.assert_allclose(g.depth_coefficients(.1,1),[.9,.1],atol=1e-15)
        np.testing.assert_allclose(g.depth_coefficients(.1,2),[.81,.18],atol=1e-15)
        np.testing.assert_allclose(g.depth_coefficients(.1,0),[1.,0.],atol=1e-15)

    def test_primary_adjudication_includes_unresolved_and_invalid(self):
        g=self.g
        self.assertEqual(g.primary_verdict(True,[1e-3],[0.],[0.]),'FROZEN_CHANNEL_FINITE_NULL_CONFIRMED')
        self.assertEqual(g.primary_verdict(True,[1e-3],[.01],[.01]),'FROZEN_CHANNEL_FINITE_NULL_OBSTRUCTED')
        self.assertEqual(g.primary_verdict(True,[1e-3],[1e-8],[1e-8]),'FROZEN_CHANNEL_FINITE_NULL_UNRESOLVED')
        self.assertEqual(g.primary_verdict(False,[1e-3],[0.],[0.]),'INVALID')

    def test_frozen_coverage_and_controls(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(r['anchor_candidate'],13)
        self.assertEqual(r['depths'],[1,2,4,8])
        self.assertEqual(r['finite_cases'],216)
        self.assertEqual(len(r['rows']),8)
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['FROZEN_CHANNEL_FINITE_NULL_CONFIRMED','FROZEN_CHANNEL_FINITE_NULL_OBSTRUCTED','FROZEN_CHANNEL_FINITE_NULL_UNRESOLVED'])
        self.assertIn(r['anchored_verdict'],['ANCHOR_FIXED_CPTP_COMPOSITION_NULL_CONFIRMED','ANCHOR_FIXED_CPTP_COMPOSITION_NULL_NOT_CONFIRMED'])

if __name__=='__main__':unittest.main()
