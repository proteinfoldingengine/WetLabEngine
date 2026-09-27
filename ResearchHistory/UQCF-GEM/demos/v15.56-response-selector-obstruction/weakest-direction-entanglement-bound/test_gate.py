import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.89 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1589_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_exact_comparison_norm_and_saturation_certificates(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],22)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))

    def test_frozen_cptp_inputs_and_verdicts(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),25)
        self.assertEqual(sum(x['family']=='saturation' for x in r['rows']),7)
        self.assertEqual(sum(x['family']=='amplitude_damping' for x in r['rows']),5)
        self.assertEqual(sum(x['family']=='depolarizing' for x in r['rows']),3)
        self.assertEqual((r['verdict'],r['sharpness_verdict']),self.g.adjudicate(r['all_valid'],r['bound_predicate'],r['sharpness_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['sharpness_verdict']])

    def test_invalid_and_negative_gates_remain_negative(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,True),('WEAKEST_DIRECTION_NEGATIVITY_BOUND_NOT_CONFIRMED','NEGATIVITY_BOUND_SHARPNESS_NOT_CONFIRMED'))
        self.assertEqual(self.g.adjudicate(True,True,False),('WEAKEST_DIRECTION_NEGATIVITY_BOUND_CONFIRMED','NEGATIVITY_BOUND_SHARPNESS_NOT_CONFIRMED'))
