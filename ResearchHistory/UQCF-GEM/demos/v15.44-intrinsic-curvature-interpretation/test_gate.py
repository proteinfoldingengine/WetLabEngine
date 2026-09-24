"""Fail-closed coordinator and strict child-wire regression tests."""
import unittest
import subprocess
import sys
import tempfile
from pathlib import Path
from fractions import Fraction

from gate import STAGES, _audit, _decode_worker, result_bytes
from worker import comparison_wire


def executors_with_failure(stage, completed=0):
    def execute(name, context, progress):
        if name == stage:
            if name == 'all_archived_field_comparisons':
                for index in range(completed):
                    progress['cases'].append({'key': [5, 'test', '1', index]})
            raise ValueError('deliberate stage failure')
        return {'accepted': True}
    return execute


class GateTests(unittest.TestCase):
    def test_result_bytes_are_compact_deterministic_json(self):
        self.assertEqual(result_bytes({'z':[1,2],'a':True}), b'{"a":true,"z":[1,2]}\n')

    def test_comparison_wire_encodes_carrier_keys_canonically(self):
        result = {'cases': (), 'pairs': (), 'scale_pairs': (),
                  'counts': {'cases': 0, 'pairs': 0, 'scale_pairs': 0,
                             'by_control': {'control': 0},
                             'by_carrier': {(5, Fraction(1)): 0,
                                            (5, Fraction(7, 3)): 0}}}
        encoded = comparison_wire(result)
        self.assertEqual(encoded['counts']['by_carrier'], [
            {'L': 5, 'scale': '1', 'pairs': 0},
            {'L': 5, 'scale': '7/3', 'pairs': 0}])

    def test_isolated_entrypoints_resolve_sibling_modules(self):
        from operator_types import canonical_bytes
        here=Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'input.json').write_bytes(canonical_bytes({}))
            result=subprocess.run([sys.executable,'-I','-B',str(here/'worker.py'),
                '--stage','evidence','--input',str(root/'input.json'),
                '--output',str(root/'output.json'),'--progress',str(root/'progress.txt')],
                capture_output=True,timeout=60)
            self.assertEqual(result.returncode,0,result.stderr[-1000:])
            self.assertIn(b'"stage": "evidence"',(root/'output.json').read_bytes())
            gate=subprocess.run([sys.executable,'-I','-B','-c',
                'import runpy; runpy.run_path('+repr(str(here/'gate.py'))+', run_name="isolated_import")'],
                capture_output=True,timeout=10)
            self.assertEqual(gate.returncode,0,gate.stderr[-1000:])

    def test_failure_order_every_stage(self):
        for stage in STAGES:
            with self.subTest(stage=stage):
                result = _audit(executors_with_failure(stage))
                self.assertEqual(result['status'], 'INTRINSIC_CURVATURE_INTERPRETATION_INVALID')
                self.assertEqual(result['first_failed_stage'], stage)
                self.assertIsNone(result['scientific_verdict'])
                self.assertEqual(result['completed_stages'], list(STAGES[:STAGES.index(stage)]))

    def test_partial_comparison_never_succeeds(self):
        result = _audit(executors_with_failure('all_archived_field_comparisons', completed=12))
        self.assertEqual(result['status'], 'INTRINSIC_CURVATURE_INTERPRETATION_INVALID')
        self.assertEqual(result['first_failed_stage'], 'all_archived_field_comparisons')
        self.assertEqual(result['completed_counts']['cases'], 12)
        self.assertIsNone(result['scientific_verdict'])

    def test_malformed_worker_json_rejected(self):
        for raw in (b'{"stage":"x","stage":"x","result":{}}\n',
                    b'{"result":{},"stage":"x","extra":1}\n',
                    b'{"result":{"x":NaN},"stage":"x"}\n',
                    b'{"result":{"x":1.0},"stage":"x"}\n',
                    b'{"result":{"x":true},"stage":"x"}\n',
                    b'{"result":{},"stage":"x"} trailing'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                _decode_worker(raw, 'x')

    def test_timeout_nonzero_and_malformed_child_fail_closed(self):
        from gate import _worker_process
        for kind in ('timeout', 'nonzero', 'malformed'):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                _worker_process('evidence', {}, timeout=1, _test_command=kind)


if __name__ == '__main__': unittest.main()
