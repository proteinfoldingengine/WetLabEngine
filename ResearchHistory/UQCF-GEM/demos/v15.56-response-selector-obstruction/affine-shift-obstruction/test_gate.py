import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        if not p.exists():raise AssertionError('v15.85 scientific implementation absent: expected RED')
        s=importlib.util.spec_from_file_location('affine85',p)
        cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_full_transpose_symbolic_identity_and_nonunital_controls(self):
        r=self.g.symbolic_identity()
        self.assertEqual(r['coefficient_count'],13)
        self.assertTrue(r['valid'],r)
        s=self.g.synthetic_controls()
        self.assertTrue(s['valid'],s)

    def test_verdicts_do_not_turn_invalid_or_no_into_yes(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,False,False),('AFFINE_SHIFT_RESCUE_OBSTRUCTION_NOT_CONFIRMED','NONUNITAL_RECOVERY_OBSTRUCTION_NOT_CONFIRMED'))

    def test_frozen_certificate_and_shift_ladder(self):
        r=self.g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual([x['n'] for x in r['witnesses']],[1,2,3])
        self.assertEqual([x['tau'] for x in r['shift_rows']],['-1','-.5','0','.5','1'])
        self.assertIn(r['verdict'],['AFFINE_SHIFT_RESCUE_OBSTRUCTED','AFFINE_SHIFT_RESCUE_OBSTRUCTION_NOT_CONFIRMED'])
        self.assertIn(r['recovery_verdict'],['NONUNITAL_RECOVERY_OBSTRUCTION_CONFIRMED','NONUNITAL_RECOVERY_OBSTRUCTION_NOT_CONFIRMED'])
        for row in r['shift_rows']:
            if row['tau'] in ['-.5','0','.5'] and row['classification']=='CPTP':self.assertEqual(len(row['recovery']['axes']),3)
            else:self.assertIsNone(row['recovery'])

if __name__=='__main__':unittest.main()
