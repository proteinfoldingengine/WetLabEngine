import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v15.86 scientific implementation absent: expected RED'
        spec=importlib.util.spec_from_file_location('v1586_gate',p)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_exact_certificate_covers_free_column_and_translation(self):
        c=self.g.symbolic_certificate()
        self.assertEqual(c['check_count'],8)
        self.assertTrue(c['valid'])
        self.assertTrue(all(c['checks'].values()))

    def test_frozen_measurement_controls_and_independent_verdicts(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual([x['c'] for x in r['controls']['synthetic']['ladder']],['-1','0','0.5','1','1.5'])
        self.assertEqual([x['classification'] for x in r['controls']['synthetic']['ladder']],['NON_CP']*3+['CPTP','NON_CP'])
        self.assertEqual(len(r['basis_rows']),3)
        self.assertEqual((r['verdict'],r['restoration_verdict']),self.g.adjudicate(r['all_valid'],r['completion_predicate'],r['restoration_predicate']))
        self.assertIn(r['verdict'],['UNIQUE_CPTP_SUPPORT_COMPLETION_CONFIRMED','UNIQUE_CPTP_SUPPORT_COMPLETION_NOT_CONFIRMED'])
        self.assertIn(r['restoration_verdict'],['DISCARDED_DIRECTION_RESTORATION_CONFIRMED','DISCARDED_DIRECTION_RESTORATION_NOT_CONFIRMED'])

    def test_invalid_and_no_are_not_promoted(self):
        self.assertEqual(self.g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(self.g.adjudicate(True,False,True),('UNIQUE_CPTP_SUPPORT_COMPLETION_NOT_CONFIRMED','DISCARDED_DIRECTION_RESTORATION_NOT_CONFIRMED'))
        self.assertEqual(self.g.adjudicate(True,True,False),('UNIQUE_CPTP_SUPPORT_COMPLETION_CONFIRMED','DISCARDED_DIRECTION_RESTORATION_NOT_CONFIRMED'))
