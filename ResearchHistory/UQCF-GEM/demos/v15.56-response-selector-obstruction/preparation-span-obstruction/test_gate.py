import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.92 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1592_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_exact_affine_and_preparation_certificate(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],45)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))

    def test_frozen_rank_and_geometry_adjudication(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),144)
        self.assertEqual(len(r['composite_channels']),12)
        self.assertEqual(sum(x['arm']=='plane' for x in r['rows']),36)
        self.assertEqual((r['verdict'],r['noncommuting_verdict']),self.g.adjudicate(r['all_valid'],r['span_predicate'],r['noncommuting_predicate']))
        self.assertNotIn('INVALID',[r['verdict'],r['noncommuting_verdict']])

    def test_negative_and_invalid_preserved(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,False),('PREPARATION_SPAN_GEOMETRY_OBSTRUCTION_NOT_CONFIRMED','NONCOMMUTING_PREPARATIONS_INSUFFICIENT_NOT_CONFIRMED'))
