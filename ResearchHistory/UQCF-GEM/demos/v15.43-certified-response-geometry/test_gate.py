from __future__ import annotations

import json
import importlib
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from projection import FAMILY_KEYS, canonical_bytes
from response_geometry_gate import Executors, _audit, case_key, classify, main


STAGES = ("evidence", "parent_replay", "acquisition_projection", "carriers",
          "actual_carrier_controls", "response_cases", "ledger")


def evaluator_origins():
    names = {"exact_algebra", "operational_complex", "protocol_types", "transport", "holonomy",
             "evaluate.py", "evidence.py", "projection.py", "carriers.py", "application.py",
             "presentation_checks.py", "application_controls.py"}
    return {name: {"blob": "a" * 40} for name in names}


def complete_cases(nonflat):
    records = []
    for L in (5, 7):
        for scale in ("1", "7/3"):
            for family in FAMILY_KEYS:
                for index in range(L * L):
                    flag = nonflat(L, scale, family, index)
                    def canonical(vertices):
                        vertices = tuple(vertices)
                        reverse = tuple(reversed(vertices))
                        return min(tuple(vertices[i:] + vertices[:i] for i in range(4)) +
                                   tuple(reverse[i:] + reverse[:i] for i in range(4)))
                    cycles = sorted(canonical((x + L * y, (x + 1) % L + L * y,
                                               (x + 1) % L + L * ((y + 1) % L),
                                               x + L * ((y + 1) % L)))
                                    for y in range(L) for x in range(L))
                    faces = [{"cycle": list(cycle),
                              "matrix": [["0", "1"], ["-1", "0"]] if flag and face == 0 else [["0", "0"], ["0", "0"]],
                              "invariant": "1" if flag and face == 0 else "0",
                              "nonzero": bool(flag and face == 0)} for face, cycle in enumerate(cycles)]
                    records.append({"key": [L, family, scale, index],
                                    "L": L, "family": family, "scale": scale,
                                    "response_index": index,
                                    "face_count": L * L,
                                    "zero_count": L * L - int(flag),
                                    "nonzero_count": int(flag),
                                    "histogram": ([ ["0", L * L] ] if not flag else
                                                  [["0", L * L - 1], ["1", 1]]),
                                    "invariant_sum": "1" if flag else "0", "faces": faces,
                                    "carrier_family": "GLOBAL_BALANCE_COMPLETION",
                                    "presentation_receipt": {
                                        "all_exact": True, "L": L, "scale": scale, "faces": L * L,
                                        "oriented_faces": 8 * L * L,
                                        "gauge_presentations": 8 * L * L + 1,
                                        "gauge_keys": [["gauge", j] for j in range(8 * L * L + 1)],
                                        "gradient_checks": (8 * L * L + 1) * L * L,
                                        "edge_checks": (8 * L * L + 1) * 4 * L * L,
                                        "gauge_face_checks": (8 * L * L + 1) * L * L,
                                        "relabelings": 2, "relabel_cycle_rotations": 0,
                                        "relabel_cycle_reversals": 0,
                                        "transformation_names": ["four_basepoints", "both_orientations", "duality",
                                            "independent_four_terms", "single_site_D4", "fixed_mixed_D4",
                                            "label_component_permutation"],
                                        "executed_oriented_face_checks": 16 * L * L,
                                        "oriented_face_scope": "distinct_four_basepoints_times_two_orientations",
                                        "executed_oriented_face_scope": "identity_plus_fixed_mixed_presentations"}})
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
        "response_cases": lambda *_: {"cases": cases, "response_control_receipts": ({"all_exact": True},)},
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
    def test_entrypoints_start_under_isolated_python(self):
        for name in ("response_geometry_gate.py", "evaluate.py"):
            with self.subTest(name=name):
                completed = subprocess.run(
                    [sys.executable, "-I", str(Path(__file__).with_name(name)), "--help"],
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(completed.returncode, 0, completed.stderr)

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

    def test_noncyclic_face_and_face_array_reorder_are_invalid(self):
        for mutation in ("noncyclic", "reordered"):
            cases = list(complete_cases(lambda *args: False))
            changed = dict(cases[0])
            faces = [dict(face) for face in changed["faces"]]
            if mutation == "noncyclic":
                cycle = list(faces[0]["cycle"])
                cycle[1], cycle[2] = cycle[2], cycle[1]
                faces[0] = {**faces[0], "cycle": cycle}
            else:
                faces[0], faces[1] = faces[1], faces[0]
            changed["faces"] = faces
            cases[0] = changed
            with self.subTest(mutation=mutation):
                self.assertEqual(classify(tuple(cases), True)[0], "RESPONSE_APPLICATION_INVALID")

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

    def test_empty_exception_message_is_reported(self):
        result, _ = run_test_gate(evidence=lambda: (_ for _ in ()).throw(ValueError()))
        self.assertEqual(result["failure"]["message"], "ValueError")

    def test_real_evidence_adapter_serializes_flat_spec_receipt(self):
        from response_geometry_gate import _evidence
        receipt = _evidence()
        self.assertIs(type(receipt["pins"]["spec"]), str)
        self.assertEqual(len(receipt["pins"]["spec"]), 40)

    def test_production_evaluator_adapter_preserves_failure_progress(self):
        import response_geometry_gate as gate
        with tempfile.TemporaryDirectory() as temporary:
            inputs = Path(temporary) / "INPUTS.json"
            inputs.write_text("{}")
            def failed(command, **kwargs):
                output = Path(command[command.index("--out") + 1])
                output.write_text(json.dumps({"failure": {
                    "stage": "response_cases", "case": [7, FAMILY_KEYS[0], "1", 3],
                    "completed_cases": 250, "completed_faces": 6250,
                    "error_category": "ArithmeticError", "message": "exact failure"}}))
                return SimpleNamespace(returncode=1, stderr=b"traceback evidence\n")
            with patch("response_geometry_gate.subprocess.run", side_effect=failed), \
                 patch("sys.stderr"):
                with self.assertRaises(gate.StageFailure) as caught:
                    gate._run_evaluator({"path": inputs}, "cases")
            self.assertEqual(caught.exception.stage, "response_cases")
            self.assertEqual((caught.exception.cases, caught.exception.faces), (250, 6250))

    def test_child_fallback_uses_public_stage_and_validates_progress(self):
        import response_geometry_gate as gate
        with tempfile.TemporaryDirectory() as temporary:
            inputs = Path(temporary) / "INPUTS.json"
            inputs.write_text("{}")
            with patch("response_geometry_gate.subprocess.run",
                       return_value=SimpleNamespace(returncode=1, stderr=b"")):
                with self.assertRaises(gate.StageFailure) as caught:
                    gate._run_evaluator({"path": inputs}, "controls")
            self.assertEqual(caught.exception.stage, "actual_carrier_controls")

    def test_ledger_failure_retains_completed_counts_but_no_partial_cases(self):
        result, _ = run_test_gate(ledger=lambda _: (_ for _ in ()).throw(ValueError("ledger stop")))
        self.assertEqual(result["first_failed_gate"], "ledger")
        self.assertEqual(result["completed_counts"], {"cases": 740, "faces": 30260})
        self.assertIsNone(result["cases"])

    def test_production_cases_adapter_rejects_malformed_nested_record(self):
        import response_geometry_gate as gate
        cases = list(complete_cases(lambda *args: False))
        cases[0] = {**cases[0], "faces": []}
        with patch("response_geometry_gate._run_evaluator", return_value={
                "cases": cases, "response_control_receipts": [{"all_exact": True}] * 2,
                "origin_receipts": evaluator_origins()}):
            with self.assertRaisesRegex(ValueError, "face_coverage"):
                gate._cases({"path": Path("unused")}, (), ())

    def test_production_adapter_rejects_incomplete_control_receipt(self):
        import response_geometry_gate as gate
        with patch("response_geometry_gate._run_evaluator", return_value={
                "control_receipts": [{"all_exact": True}] * 4,
                "origin_receipts": evaluator_origins()}):
            with self.assertRaisesRegex(ValueError, "control_receipt_schema"):
                gate._controls({"path": Path("unused")}, ({},) * 4)

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
