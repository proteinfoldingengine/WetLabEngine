import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.87 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1587_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_exact_spectrum_and_unrestricted_translation_certificate(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],6)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))

    def test_frozen_physical_controls_and_scientific_adjudication(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual([x['classification'] for x in r['isotropic_rows']],['CPTP']*3+['NON_CP']*2)
        self.assertEqual([x['classification'] for x in r['anisotropic_rows']],['CPTP']*3)
        self.assertEqual(len(r['translation_rows']),7)
        self.assertEqual(len(r['distinguishability_rows']),4)
        self.assertEqual(tuple(r[k] for k in ['verdict','translation_verdict','distinguishability_verdict']),self.g.adjudicate(r['all_valid'],r['bound_predicate'],r['translation_predicate'],r['distinguishability_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['translation_verdict'],r['distinguishability_verdict']])

    def test_invalid_and_negative_predicates_remain_negative(self):
        self.assertEqual(self.g.adjudicate(False,True,True,True),('INVALID',)*3)
        self.assertEqual(self.g.adjudicate(True,False,True,True),('ERASURE_COST_BOUND_NOT_ATTAINED','OPTIMAL_ERASURE_TRANSLATION_RIGIDITY_NOT_CONFIRMED','OPTIMAL_ERASURE_DISTINGUISHABILITY_NOT_CONFIRMED'))
        self.assertEqual(self.g.adjudicate(True,True,False,False),('ERASURE_COST_BOUND_ATTAINED','OPTIMAL_ERASURE_TRANSLATION_RIGIDITY_NOT_CONFIRMED','OPTIMAL_ERASURE_DISTINGUISHABILITY_NOT_CONFIRMED'))
