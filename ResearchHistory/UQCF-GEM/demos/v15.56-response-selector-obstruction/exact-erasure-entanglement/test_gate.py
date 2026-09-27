import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.88 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1588_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_partial_transpose_and_soft_family_exact_certificates(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['coefficient_count'],10)
        self.assertEqual(c['soft_equation_count'],8)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['coefficient_checks'].values()))
        self.assertTrue(all(c['soft_checks'].values()))

    def test_native_maps_and_nontrivial_entanglement_controls(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['native_rows']),6)
        self.assertEqual([x['epsilon'] for x in r['soft_rows']],['0','0.01','0.0001','0.000001'])
        self.assertEqual([x['ppt_class'] for x in r['controls']['synthetic']['rows']],['NOT_PPT','PPT','NOT_PPT'])
        self.assertEqual((r['verdict'],r['soft_verdict']),self.g.adjudicate(r['all_valid'],r['exact_erasure_predicate'],r['soft_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['soft_verdict']])

    def test_invalid_and_negative_gates_stay_negative(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('EXACT_ERASURE_ENTANGLEMENT_BREAKING_NOT_CONFIRMED','SOFT_ERASURE_ENTANGLEMENT_NOT_CONFIRMED'))
        self.assertEqual(self.g.adjudicate(True,True,False),('EXACT_ERASURE_ENTANGLEMENT_BREAKING_CONFIRMED','SOFT_ERASURE_ENTANGLEMENT_NOT_CONFIRMED'))
