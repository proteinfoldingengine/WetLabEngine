import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.98 scientific implementation absent: expected RED'
        s=importlib.util.spec_from_file_location('v1598_gate',p);cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_order_witness_and_commuting_activation(self):
        # Detects reversed source ordering, wrong local embedding or Pauli-Y transport.
        g=self.g;h=g.word((2,2,1,1))/4
        ab=g.generator(g.generator(h,'A'),'B');ba=g.generator(g.generator(h,'B'),'A')
        expected=-g.word((0,1,0,1))/4
        np.testing.assert_allclose(g.V97.pairs(ab),g.V97.pairs(expected),atol=1e-14)
        np.testing.assert_allclose(g.V97.pairs(ba),0,atol=1e-14)
        h=g.word((1,1,1,1))/4;ad=g.generator(g.generator(h,'A'),'D');da=g.generator(g.generator(h,'D'),'A')
        np.testing.assert_allclose(ad,da,atol=1e-14)
        np.testing.assert_allclose(g.V97.pairs(ad),g.V97.pairs(g.word((3,0,3,0))/4),atol=1e-14)

    def test_exact_composition_certificate(self):
        c=self.g.symbolic_certificate();self.assertEqual(c['check_count'],8);self.assertTrue(c['valid'],c)

    def test_frozen_measurement_and_no_preservation(self):
        r=self.g.run_measurement();self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),48);self.assertEqual(r['hidden_count'],81)
        self.assertEqual((r['verdict'],r['commuting_verdict']),self.g.adjudicate(r['all_valid'],r['order_predicate'],r['commuting_predicate']))

    def test_no_and_invalid(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('COMPOSITION_ORDER_GEOMETRY_NOT_CONFIRMED','COMMUTING_COMPOSITION_ACTIVATION_NOT_CONFIRMED'))

if __name__=='__main__':unittest.main()
