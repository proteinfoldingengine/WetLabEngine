import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent


class SharedWitnessContracts(unittest.TestCase):
    def setUp(self):
        path = HERE / 'shared_witness_independent.py'
        self.assertTrue(path.is_file(), 'Independent verifier absent: expected tests-first RED')
        spec = importlib.util.spec_from_file_location('independent', path)
        self.v = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.v)

    def produced(self):
        run = subprocess.run([sys.executable, str(HERE / 'shared_witness_producer.py')],
                             capture_output=True, text=True, check=True, timeout=30)
        return self.v.loads(run.stdout)

    def test_complete_independent_identity_equality(self):
        report = self.produced()
        result = self.v.verify(report)
        self.assertEqual(result['states'], 4)
        self.assertEqual(result['outcomes'], 24)
        self.assertEqual(result['locked_outcomes'], 6)
        self.assertFalse(result['physical_observer_derived'])

    def test_independent_root_choice_oracle_without_producer(self):
        report = self.v.reconstruct()
        self.assertEqual({r['id']: r['tau'] for r in report['states']},
                         {'00': 4, '01': 4, '10': 4, '11': 3})
        self.assertEqual(report['fibers'], {'3': ['11'], '4': ['00', '01', '10']})

    def test_missing_duplicate_substituted_outcomes_reject(self):
        for collection in ('states', 'outcomes', 'locked_outcomes'):
            for change in ('missing', 'duplicate', 'substitute'):
                report = self.produced()
                rows = report[collection]
                if change == 'missing':
                    rows.pop()
                elif change == 'duplicate':
                    rows.append(copy.deepcopy(rows[0]))
                else:
                    rows[-1] = copy.deepcopy(rows[0])
                with self.subTest(collection=collection, change=change):
                    with self.assertRaises(self.v.CheckError):
                        self.v.verify(report)

    def test_wrong_tau_and_boolean_value_reject(self):
        for value in (2, True):
            report = self.produced()
            report['states'][0]['tau'] = value
            with self.assertRaises(self.v.CheckError):
                self.v.verify(report)

    def test_premature_decoder_and_silent_anchor_counterexamples(self):
        report = self.produced()
        self.assertEqual(report['controls']['premature_decoder'], ['00', '01'])
        self.assertEqual(report['controls']['silent_anchor'], ['11', '-1', '01'])
        self.assertEqual(report['controls']['invisible_anchor_cleanup'], ['10', '-1', '00'])
        for key in report['controls']:
            damaged = copy.deepcopy(report)
            damaged['controls'][key] = []
            with self.subTest(key=key), self.assertRaises(self.v.CheckError):
                self.v.verify(damaged)

    def test_claim_and_provenance_forgery_reject(self):
        for key, value in [('guaranteed_synchronization', True),
                           ('physical_observer_derived', True)]:
            report = self.produced()
            report['claims'][key] = value
            with self.assertRaises(self.v.CheckError):
                self.v.verify(report)
        report = self.produced()
        report['proof_commit'] = '0' * 40
        with self.assertRaises(self.v.CheckError):
            self.v.verify(report)

    def test_each_command_can_reject_and_locked_decoder_is_exact(self):
        report = self.produced()
        edges = {tuple(row) for row in report['outcomes']}
        for s in ('00', '01', '10', '11'):
            for c in ('+1', '-1', '+2', '-2'):
                self.assertIn((s, c, s), edges)
        tau = {r['id']: r['tau'] for r in report['states']}
        for s, c, t in report['locked_outcomes']:
            self.assertEqual(int(t[1]), 4 - tau[t])
            self.assertEqual(s != t, tau[s] != tau[t])

    def test_duplicate_json_keys_reject(self):
        with self.assertRaises(self.v.CheckError):
            self.v.loads('{"states": [], "states": []}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
