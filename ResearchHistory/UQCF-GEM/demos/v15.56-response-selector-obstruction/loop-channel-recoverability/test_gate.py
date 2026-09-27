import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        if not p.exists():raise AssertionError('v15.84 scientific implementation absent: expected RED')
        s=importlib.util.spec_from_file_location('channel84',p)
        cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_non_cp_is_not_a_small_roundoff_or_valid_channel(self):
        g=self.g
        self.assertEqual(g.cp_class(-.01),'NON_CP')
        self.assertEqual(g.cp_class(0),'CPTP')
        self.assertEqual(g.cp_class(-1e-20),'UNRESOLVED')
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,False,False),('LATE_CPTP_LOOP_POWER_NOT_CONFIRMED','CPTP_LOOP_RECOVERY_OBSTRUCTION_NOT_CONFIRMED'))

    def test_exact_channel_and_complex_controls(self):
        r=self.g.synthetic_controls()
        self.assertTrue(r['valid'],r)
        self.assertEqual(r['map_count'],4)

    def test_frozen_four_powers_and_valid_execution(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual([x['n'] for x in r['rows']],[1,2,3,4])
        self.assertIn(r['verdict'],['LATE_CPTP_LOOP_POWER_CONFIRMED','LATE_CPTP_LOOP_POWER_NOT_CONFIRMED'])
        self.assertIn(r['recovery_verdict'],['CPTP_LOOP_RECOVERY_OBSTRUCTED','CPTP_LOOP_RECOVERY_OBSTRUCTION_NOT_CONFIRMED'])
        if r['rows'][3]['classification']=='CPTP':
            self.assertEqual(len(r['recovery']['axes']),3)
            self.assertEqual(len(r['recovery']['inverse_witnesses']),2)
        else:self.assertIsNone(r['recovery'])

if __name__=='__main__':unittest.main()
