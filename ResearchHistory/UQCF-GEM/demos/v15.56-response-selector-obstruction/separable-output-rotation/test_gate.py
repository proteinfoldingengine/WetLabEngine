import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.91 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1591_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_exact_measure_prepare_and_connected_scaling(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],19)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))

    def test_frozen_measurement_validity_and_verdicts(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),144)
        self.assertEqual(sum(x['a']==0 for x in r['rows']),36)
        self.assertEqual(len(r['composite_channels']),12)
        self.assertEqual((r['verdict'],r['zero_verdict']),self.g.adjudicate(r['all_valid'],r['response_predicate'],r['zero_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['zero_verdict']])

    def test_negative_science_and_invalid_are_preserved(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('SEPARABLE_OUTPUT_ROTATIONAL_RESPONSE_NOT_CONFIRMED','ZERO_ATTENUATION_POLAR_UNDEFINED_NOT_CONFIRMED'))
