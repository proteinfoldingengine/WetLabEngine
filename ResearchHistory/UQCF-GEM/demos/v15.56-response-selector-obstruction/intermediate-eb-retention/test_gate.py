import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.99 scientific implementation absent: expected RED'
        s=importlib.util.spec_from_file_location('v1599_gate',p);cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_middle_weight_and_erasure(self):
        g=self.g;h=g.V98.word((2,2,1,1))/4;a=1/3
        np.testing.assert_allclose(g.middle(h[None],a)[0],a**4*h,atol=1e-15)
        y=g.V98.generator(g.middle(g.V98.generator(h,'A')[None],a)[0],'B')
        np.testing.assert_allclose(g.V97.pairs(y),-a**3*g.V97.pairs(g.V98.word((0,1,0,1))/4),atol=1e-14)
        z=np.diag(np.arange(1,17)/136)
        np.testing.assert_allclose(g.middle(z[None],0)[0],np.eye(16)/16,atol=1e-15)
        np.testing.assert_allclose(g.middle(h[None],0)[0],0,atol=1e-15)

    def test_exact_certificate(self):
        c=self.g.symbolic_certificate();self.assertEqual(c['check_count'],8);self.assertTrue(c['valid'],c)

    def test_frozen_measurement(self):
        r=self.g.run_measurement();self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),192);self.assertEqual(len(r['intermediate_centers']),108)
        self.assertEqual(sum(x['a']>0 for x in r['rows']),144)
        self.assertEqual((r['verdict'],r['erasure_verdict']),self.g.adjudicate(r['all_valid'],r['scaling_predicate'],r['erasure_predicate']))
        for row in r['rows']:
            if row['a']==0:
                self.assertTrue(all(x is None for x in row['responses'].values()))

    def test_no_and_invalid(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('INTERMEDIATE_EB_RESPONSE_SCALING_NOT_CONFIRMED','COMPLETE_INTERMEDIATE_ERASURE_NOT_CONFIRMED'))

if __name__=='__main__':unittest.main()
