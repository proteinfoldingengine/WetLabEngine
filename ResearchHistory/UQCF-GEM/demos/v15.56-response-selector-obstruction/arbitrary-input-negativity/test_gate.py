import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.90 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1590_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_exact_certificate(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],8)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))

    def test_frozen_inputs_and_scientific_adjudication(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),114)
        self.assertEqual(sum(x['family']=='inherited_pure' for x in r['rows']),75)
        self.assertEqual(sum(x['family']=='inherited_mixed' for x in r['rows']),25)
        self.assertEqual(sum(x['family']=='amplitude_damping' for x in r['rows']),14)
        self.assertEqual((r['verdict'],r['extension_verdict'],r['constant_verdict']),self.g.adjudicate(r['all_valid'],r['bound_predicate'],r['extension_falsified_predicate'],r['constant_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['extension_verdict'],r['constant_verdict']])

    def test_negative_and_invalid_are_preserved(self):
        self.assertEqual(self.g.adjudicate(False,True,True,True),('INVALID',)*3)
        self.assertEqual(self.g.adjudicate(True,False,False,True),('UNIVERSAL_INPUT_NEGATIVITY_BOUND_NOT_CONFIRMED','CHOI_CEILING_EXTENSION_NOT_FALSIFIED','OPTIMAL_LINEAR_NEGATIVITY_CONSTANT_NOT_CONFIRMED'))
