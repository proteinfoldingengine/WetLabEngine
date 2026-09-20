from __future__ import annotations

import json
import importlib
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from projection import FAMILY_KEYS, canonical_bytes
from response_geometry_gate import Executors, _audit, case_key, classify, main


STAGES = ("evidence", "parent_replay", "acquisition_projection", "carriers",
          "actual_carrier_controls", "response_cases", "ledger")


def complete_cases(nonflat):
    records = []
    for L in (5, 7):
        for scale in ("1", "7/3"):
            for family in FAMILY_KEYS:
                for index in range(L * L):
                    flag = nonflat(L, scale, family, index)
                    records.append({"key": [L, family, scale, index],
                                    "L": L, "family": family, "scale": scale,
                                    "response_index": index,
                                    "face_count": L * L,
                                    "zero_count": L * L - int(flag),
                                    "nonzero_count": int(flag),
                                    "histogram": [["0", L * L - int(flag)]],
                                    "invariant_sum": "0", "faces": [],
                                    "presentation_receipt": {"all_exact": True}})
    return tuple(records)


def run_test_gate(**changes):
    calls = []
    cases = complete_cases(lambda *args: False)
    defaults = {
        "evidence": lambda: {"ok": True},
        "parent_replay": lambda: {"status": "TRANSPORT_PROTOCOL_CERTIFIED"},
        "acquisition_projection": lambda: {"projection": "ok"},
        "carriers": lambda _: ({"L": 5}, {"L": 5}, {"L": 7}, {"L": 7}),
        "actual_carrier_controls": lambda *_: ({"all_exact": True},),
        "response_cases": lambda *_: {"cases": cases, "control_receipts": ({"all_exact": True},)},
        "ledger": lambda value: value,
    }
    defaults.update(changes)
    wrapped = {}
    for name in STAGES:
        callback = defaults[name]
        def invoke(*args, _name=name, _callback=callback):
            calls.append(_name)
            return _callback(*args)
        wrapped[name] = invoke
    return _audit(Executors(**wrapped)), calls


class GateTests(unittest.TestCase):
    def test_declared_suite_modules_resolve_to_new_demo(self):
        expected = ("test_evidence", "test_projection", "test_carriers",
                    "test_application", "test_controls", "test_gate")
        observed = {name: Path(importlib.import_module(name).__file__).resolve().parent
                    for name in expected}
        self.assertEqual(set(observed.values()), {Path(__file__).resolve().parent})
        controls = importlib.import_module("test_controls")
        self.assertTrue(hasattr(controls, "ControlsTests"))
        self.assertFalse(hasattr(controls, "ControlTests"))

    def test_each_failure_stops_before_every_later_stage(self):
        for index, stage in enumerate(STAGES):
            with self.subTest(stage=stage):
                def fail(*_):
                    raise ValueError("injected failure")
                result, calls = run_test_gate(**{stage: fail})
                self.assertEqual(result["status"], "RESPONSE_APPLICATION_INVALID")
                self.assertEqual(result["first_failed_gate"], stage)
                self.assertEqual(calls, list(STAGES[:index + 1]))
                self.assertEqual(result["claims"]["source_correspondence"], "NOT_EVALUATED")

    def test_case_key_rejects_malformed_boolean_fraction_and_extra_fields(self):
        valid = {"L": 5, "family": FAMILY_KEYS[0], "scale": "1", "response_index": 0}
        self.assertEqual(case_key(valid), (5, FAMILY_KEYS[0], Fraction(1), 0))
        for changed in ({**valid, "L": True}, {**valid, "scale": "2/2"},
                        {**valid, "unexpected": 1}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                case_key(changed)

    def test_classify_all_four_mappings_and_complete_coverage(self):
        null = complete_cases(lambda *args: False)
        nonzero = complete_cases(lambda L, s, f, i: f == FAMILY_KEYS[0])
        mixed = complete_cases(lambda L, s, f, i: f == FAMILY_KEYS[0] and i == 0)
        self.assertEqual(classify(null, True)[0], "CANONICAL_RESPONSE_CURVATURE_NULL")
        self.assertEqual(classify(nonzero, True)[0], "CANONICAL_RESPONSE_CURVATURE_NONZERO")
        self.assertEqual(classify(mixed, True)[0], "CANONICAL_RESPONSE_CURVATURE_MIXED")
        self.assertEqual(classify(null[:-1], False)[0], "RESPONSE_APPLICATION_INVALID")

    def test_missing_or_duplicate_case_is_invalid(self):
        cases = complete_cases(lambda *args: False)
        for changed in (cases[:-1], cases[:-1] + (cases[0],)):
            with self.subTest(count=len(changed)):
                result, _ = run_test_gate(response_cases=lambda *_: {"cases": changed, "control_receipts": ()})
                self.assertEqual(result["status"], "RESPONSE_APPLICATION_INVALID")
                self.assertEqual(result["first_failed_gate"], "response_cases")

    def test_malformed_evaluator_payload_is_invalid(self):
        result, _ = run_test_gate(response_cases=lambda *_: {"cases": "not-a-list"})
        self.assertEqual(result["first_failed_gate"], "response_cases")

    def test_failure_ledger_sanitizes_message_and_has_no_partial_claim(self):
        result, _ = run_test_gate(parent_replay=lambda: (_ for _ in ()).throw(
            RuntimeError("/private/location\nsecond line")))
        self.assertNotIn("/private/location", result["failure"]["message"])
        self.assertIsNone(result["cases"])
        self.assertEqual(result["completed_counts"], {"cases": 0, "faces": 0})
        self.assertFalse(result["claims"]["physical_curvature"])

    def test_public_audit_has_no_executor_override(self):
        import inspect
        from response_geometry_gate import audit
        self.assertEqual(tuple(inspect.signature(audit).parameters), ())

    def test_cli_check_compares_exact_bytes_and_rejects_invalid_outcome(self):
        result, _ = run_test_gate()
        with tempfile.TemporaryDirectory() as temporary, patch(
                "response_geometry_gate.audit", return_value=result):
            path = Path(temporary) / "result.json"
            with patch("sys.stdout"):
                self.assertEqual(main(["--out", str(path)]), 0)
                self.assertEqual(main(["--check", str(path)]), 0)
                path.write_bytes(canonical_bytes({}))
                self.assertNotEqual(main(["--check", str(path)]), 0)
        invalid, _ = run_test_gate(evidence=lambda: (_ for _ in ()).throw(ValueError("bad")))
        with patch("response_geometry_gate.audit", return_value=invalid), patch("sys.stdout"):
            self.assertNotEqual(main([]), 0)


if __name__ == "__main__":
    unittest.main()
