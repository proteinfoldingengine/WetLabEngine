import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v16.00 scientific implementation absent: expected RED'
        s=importlib.util.spec_from_file_location('v1600_gate',p);cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_complex_transport(self):
        g=self.g
        with g.mp.workdps(80):
            z=g.exact_complex(complex(.125,-.0625))
            self.assertEqual(z.real,g.mp.mpf(1)/8);self.assertEqual(z.imag,-g.mp.mpf(1)/16)

    def test_readout_controls(self):
        for dps in [50,80]:self.assertTrue(self.g.solver_controls(dps)['valid'])

    def test_frozen_audit(self):
        r=self.g.run_measurement();self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['cases']),8);self.assertEqual(r['precision_digits'],[50,80])
        self.assertEqual(r['verdict'],self.g.adjudicate(r['all_valid'],r['recovery_predicate']))

    def test_verdict_precedence(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True),'INVALID')
        self.assertEqual(g.adjudicate(True,True),'READOUT_ARITHMETIC_NOISE_CONFIRMED')
        self.assertEqual(g.adjudicate(True,False),'FROZEN_INPUT_RANK_RESIDUAL_PERSISTS')

if __name__=='__main__':unittest.main()
