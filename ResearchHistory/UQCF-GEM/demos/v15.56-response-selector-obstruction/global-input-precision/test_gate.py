import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v16.01 scientific implementation absent: expected RED'
        s=importlib.util.spec_from_file_location('v1601_gate',p);cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_complex_basis_reconstruction(self):
        g=self.g
        with g.mp.workdps(50):
            rho=g.mp.eye(16)/16;rho[0,1]=g.mp.j/100;rho[1,0]=-g.mp.j/100
            coeff,imag=g.coefficients(rho)
            self.assertLess(g.V100.norm(g.reconstruct(coeff)-rho),g.mp.mpf('1e-35'))
            self.assertLess(imag,g.mp.mpf('1e-35'))

    def test_global_witnesses(self):
        for dps in [50,80]:self.assertTrue(self.g.witness_controls(dps)['valid'])

    def test_frozen_measurement(self):
        r=self.g.run_measurement();self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['cases']),8);self.assertEqual(r['precision_digits'],[50,80])
        self.assertEqual(r['verdict'],self.g.adjudicate(r['all_valid'],r['recovery_predicate']))

    def test_verdicts(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True),'INVALID')
        self.assertEqual(g.adjudicate(True,True),'GLOBAL_INPUT_PRECISION_RECOVERY_CONFIRMED')
        self.assertEqual(g.adjudicate(True,False),'GLOBAL_INPUT_PRECISION_RECOVERY_NOT_CONFIRMED')

if __name__=='__main__':unittest.main()
