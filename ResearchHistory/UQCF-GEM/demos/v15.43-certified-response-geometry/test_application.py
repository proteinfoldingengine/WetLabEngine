from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE = HERE.parent / "v15.42-duality-covariant-transport-repair"
for location in (str(HERE), str(CORE)):
    while location in sys.path:
        sys.path.remove(location)
sys.path[:0] = [str(HERE), str(CORE)]

from protocol_types import TransportManifest
from test_carriers import manufactured_payload


class ApplicationTests(unittest.TestCase):
    def test_post_bootstrap_math_with_file_and_process_entrypoints_denied(self):
        import builtins
        import io
        import os
        import subprocess
        from contextlib import ExitStack
        from unittest.mock import patch
        from carriers import build_carrier
        from application import evaluate_field
        from presentation_checks import check_presentations

        # Materialize inputs and imports before denial, but not the carrier or results.
        payload = manufactured_payload(5)
        values = tuple(Q(i == 0) for i in range(25))
        targets = ((builtins, 'open'), (io, 'open'), (os, 'open'),
                   (os, 'system'), (os, 'popen'), (subprocess, 'Popen'),
                   (subprocess, 'run'), (subprocess, 'call'),
                   (subprocess, 'check_call'), (subprocess, 'check_output'),
                   (Path, 'open'), (Path, 'read_bytes'), (Path, 'read_text'),
                   (Path, 'write_bytes'), (Path, 'write_text'))
        def denied(*args, **kwargs):
            raise RuntimeError('post_bootstrap_forbidden_operation')
        with ExitStack() as stack:
            for owner, name in targets:
                stack.enter_context(patch.object(owner, name, denied))
            carrier = build_carrier(payload)
            result = evaluate_field(carrier, values)
            receipt = check_presentations(carrier, values)
            self.assertEqual(dict(result.histogram), {Q(0): 13, Q(1, 64): 8, Q(1, 16): 4})
            self.assertTrue(receipt['all_exact'])
            self.assertEqual(receipt['gauge_presentations'], 201)
            # Positive sensitivity: every installed entrypoint really rejects a call.
            for owner, name in targets:
                with self.subTest(entrypoint=name), self.assertRaisesRegex(
                        RuntimeError, 'post_bootstrap_forbidden_operation'):
                    getattr(owner, name)('deliberately forbidden')

    @classmethod
    def setUpClass(cls):
        from carriers import build_carrier
        cls.carrier = build_carrier(manufactured_payload(5))

    def test_null_and_all_impulse_positions(self):
        from application import evaluate_field

        null = evaluate_field(self.carrier, (Q(7, 3),) * 25)
        self.assertEqual(null.nonzero_count, 0)
        self.assertEqual(null.zero_count, 25)
        self.assertEqual(null.invariant_sum, 0)
        for position in range(25):
            values = tuple(Q(1) if index == position else Q(0)
                           for index in range(25))
            impulse = evaluate_field(self.carrier, values)
            self.assertEqual(dict(impulse.histogram),
                             {Q(0): 13, Q(1, 64): 8, Q(1, 16): 4})
            self.assertEqual(len(impulse.records), 25)

    def test_independent_product_on_mixed_field(self):
        from application import evaluate_field
        from presentation_checks import expanded
        values = tuple(Q((i*i+3*i)%17,7) for i in range(25))
        result = evaluate_field(self.carrier, values)
        for cycle, matrix, _ in result.records:
            self.assertEqual(matrix, expanded(dict(result.transport.baseline),
                                             dict(result.transport.tangent_deltas), cycle))

    def test_rejects_field_length_and_type(self):
        from application import evaluate_field

        with self.assertRaisesRegex(ValueError, "field must contain"):
            evaluate_field(self.carrier, (Q(0),) * 24)
        with self.assertRaisesRegex(ValueError, "exact integer or Fraction"):
            evaluate_field(self.carrier, (Q(0),) * 24 + (1.0,))

    def test_rejects_baseline_label_mismatch(self):
        from application import evaluate_field

        damaged = replace(self.carrier, baseline=replace(
            self.carrier.baseline, labels=tuple(reversed(self.carrier.baseline.labels))))
        with self.assertRaisesRegex(ValueError, "baseline_carrier_mismatch"):
            evaluate_field(damaged, (Q(0),) * 25)

    def test_rejects_manifest_convention_mismatch(self):
        from application import evaluate_field

        wrong = replace(TransportManifest.certified(), orientation_rule="one_orientation")
        with self.assertRaisesRegex(ValueError, "manifest differs"):
            evaluate_field(self.carrier, (Q(0),) * 25, manifest=wrong)


if __name__ == "__main__":
    unittest.main()
