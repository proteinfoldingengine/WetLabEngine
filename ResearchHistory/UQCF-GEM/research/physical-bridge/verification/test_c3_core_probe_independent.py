"""Contracts for the independent C3 bounded checker; not a peer-review verdict."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CHECKER = HERE / 'c3_core_probe_independent.py'
EVIDENCE = ROOT / 'COUPLED_C3_CORE_PROBE_REPLAY_EVIDENCE.json'
PRODUCER = ROOT / 'COUPLED_C3_CORE_PROBE_REPLAY.py'


class IndependentC3Contracts(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHECKER.is_file(), 'Independent checker not implemented (expected RED)')
        spec = importlib.util.spec_from_file_location('c3_independent_under_test', CHECKER)
        self.checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.checker)

    def saved(self):
        return self.checker.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_saved_complete_evidence(self):
        result = self.checker.verify(self.saved())
        self.assertEqual(result['nodes'], [4, 8])
        self.assertEqual(result['edges'], [46, 96])
        self.assertFalse(result['independent_mathematical_review'])
        print('C3 independent bounded verification:', json.dumps(result, sort_keys=True))

    def test_fresh_producer_matches_stored_evidence_and_independent_checker(self):
        run = subprocess.run([sys.executable, str(PRODUCER)], capture_output=True,
                             text=True, timeout=60, check=True)
        actual = self.checker.loads(run.stdout)
        self.assertEqual(actual, self.saved())
        self.checker.verify(actual)

    def test_isolated_checker_without_producer(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copyfile(CHECKER, target / 'checker.py')
            shutil.copyfile(EVIDENCE, target / 'evidence.json')
            run = subprocess.run([sys.executable, '-I', str(target / 'checker.py'),
                                  str(target / 'evidence.json')], cwd=target,
                                 capture_output=True, text=True, timeout=60)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['nodes'], [4, 8])

    def test_missing_duplicate_and_changed_graph_records_rejected(self):
        for collection in ('nodes', 'edges'):
            for change in ('remove', 'duplicate', 'substitute'):
                data = copy.deepcopy(self.saved())
                rows = data['graphs'][1][collection]
                if change == 'remove':
                    rows.pop()
                elif change == 'duplicate':
                    rows.append(copy.deepcopy(rows[0]))
                elif collection == 'nodes':
                    rows[0]['hidden_subsets'] = ['uw']
                else:
                    rows[0]['command'] = '+z'
                with self.subTest(collection=collection, change=change):
                    with self.assertRaises(self.checker.CheckError):
                        self.checker.verify(data)

    def test_wrong_deficit_and_boolean_integer_rejected(self):
        for value in (0, True):
            data = self.saved()
            data['graphs'][1]['nodes'][0]['D'] = value
            with self.assertRaises(self.checker.CheckError):
                self.checker.verify(data)

    def test_metadata_and_coverage_forgery_rejected(self):
        for kind in ('proof', 'status', 'graph', 'counterexample'):
            data = self.saved()
            if kind == 'proof':
                data['source']['proof_commit'] = '0' * 40
            elif kind == 'status':
                data['status'] = 'CLOSED'
            elif kind == 'graph':
                data['graphs'].pop()
            else:
                data['rejected_estimators'][0]['counterexample']['D'] = 0
            with self.subTest(kind=kind):
                with self.assertRaises(self.checker.CheckError):
                    self.checker.verify(data)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(self.checker.CheckError):
            self.checker.loads('{"status": 1, "status": 2}')

    def test_restored_fibers_and_empty_core(self):
        graph = self.checker.reconstruct(2)
        restored = [r for r in graph['nodes'] if r['core4'] == 'de']
        self.assertEqual([r['D'] for r in restored], [0, 1, 2])
        self.assertEqual(len({tuple(r['hidden_subsets']) for r in restored}), 3)
        empty = [r for r in graph['nodes'] if r['core4'] == '']
        self.assertEqual(len(empty), 1)
        self.assertEqual(empty[0]['hidden_subsets'], ['uv'])
        self.assertEqual(empty[0]['D'], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
