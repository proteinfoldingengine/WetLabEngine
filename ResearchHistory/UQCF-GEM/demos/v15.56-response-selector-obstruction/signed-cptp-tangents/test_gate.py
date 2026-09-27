import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        if not p.exists():raise AssertionError('v15.80 scientific implementation absent: expected RED')
        s=importlib.util.spec_from_file_location('signed80',p)
        cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_verdicts_preserve_no(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,False,True),('SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_NOT_CONFIRMED','SIGNED_CPTP_RETAINED_IMAGE_FOUR_CONFIRMED'))
        self.assertEqual(g.adjudicate(True,True,False),('SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_CONFIRMED','SIGNED_CPTP_RETAINED_IMAGE_FOUR_NOT_CONFIRMED'))

    def test_identity_choi_convention(self):
        g=self.g;j=g.choi_from_ptm(np.eye(64))
        omega=np.eye(8).ravel()
        np.testing.assert_allclose(j,np.outer(omega,omega),atol=1e-14)
        np.testing.assert_allclose(g.P@j@g.P,0,atol=1e-14)

    def test_frozen_coverage_and_validity(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['blocks']),7)
        self.assertEqual(len(r['states']),12)
        self.assertEqual(r['source_count'],63)
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_CONFIRMED','SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_NOT_CONFIRMED'])
        self.assertIn(r['retained_verdict'],['SIGNED_CPTP_RETAINED_IMAGE_FOUR_CONFIRMED','SIGNED_CPTP_RETAINED_IMAGE_FOUR_NOT_CONFIRMED'])

if __name__=='__main__':unittest.main()
