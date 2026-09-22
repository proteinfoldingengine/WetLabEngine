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


def response_control(L):
    n = L * L
    return {"L": L, "scale_pairs": 5 * n,
            "scale_keys": [[L, family, index] for family in FAMILY_KEYS for index in range(n)],
            "shift_cases": 10 * n,
            "shift_keys": [[L, family, scale, index] for family in FAMILY_KEYS for index in range(n)
                           for scale in ("1", "7/3")],
            "superpositions": 10,
            "superposition_keys": [[L, family, scale, 0, 1]
                                   for scale in ("1", "7/3") for family in FAMILY_KEYS],
            "transformation_names": ["scale_7/3", "shift_7/3", "superposition_2/3_-5/7"],
            "all_exact": True}


def carrier_control(L, scale):
    n, gauges = L * L, 8 * L * L + 1
    certified = (n + 2) * gauges
    identity = [["1", "0"], ["0", "1"]]
    directions = [["-1", "0"], ["0", "-1"], ["0", "1"], ["1", "0"]]
    return {"L": L, "scale": scale, "constants": 2, "constant_keys": ["0", "7/3"],
            "impulses": n, "impulse_keys": list(range(n)),
            "impulse_histogram": [["0", n - 12], ["1/64", 8], ["1/16", 4]],
            "basis_core_comparisons": 9 * n + 2, "identity_core_comparisons": n + 2,
            "algebraically_certified_gauge_comparisons": certified,
            "local_linear_certificate": {"edge_types": [[identity, direction] for direction in directions],
                "endpoint_frame_pairs": 64, "linear_basis_dimension": 5,
                "local_basis_comparisons": 1280, "gradient_basis_comparisons": 32, "all_exact": True},
            "edge_checks": certified * 4 * n, "face_checks": certified * n, "all_exact": True}


def carrier_receipt(L, scale):
    return {"L": L, "scale": scale, "status": "IDENTIFIABLE", "complex_reason": None,
            "baseline_status": "IDENTIFIABLE", "baseline_reason": None, "tangent_rank": 2,
            "gauge_orbit_count": 1, "flat": True}


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
                                        "gauge_keys": [["site", label, action]
                                                       for label in range(L * L) for action in range(8)] + [["mixed"]],
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

    def test_parent_replay_bootstrap_imports_siblings_with_fixed_isolated_arguments(self):
        import response_geometry_gate as gate
        with tempfile.TemporaryDirectory(prefix="parent ' path ; ") as temporary:
            parent = Path(temporary)
            (parent / "docs").mkdir()
            expected = canonical_bytes({"status": "TRANSPORT_PROTOCOL_CERTIFIED"})
            (parent / "docs/RESULTS.json").write_bytes(expected)
            (parent / "controls.py").write_text("VALUE = 'local parent controls'\n")
            (parent / "protocol_gate.py").write_text(
                "import controls, pathlib, sys\n"
                "assert controls.VALUE == 'local parent controls'\n"
                "assert pathlib.Path(controls.__file__).parent == pathlib.Path.cwd()\n"
                "assert sys.flags.isolated == 1\n"
                "assert __name__ == '__main__'\n"
                "assert pathlib.Path(sys.argv[0]).resolve() == pathlib.Path(__file__).resolve()\n"
                "assert sys.argv[1:] == ['--check', 'docs/RESULTS.json']\n"
                "sys.stdout.buffer.write(pathlib.Path(sys.argv[2]).read_bytes())\n")
            with patch.object(gate, "PARENT_DIR", parent):
                try:
                    receipt = gate._parent_replay()
                except RuntimeError as error:
                    self.fail(f"isolated parent launch failed: {error}")
            self.assertEqual(receipt["status"], "TRANSPORT_PROTOCOL_CERTIFIED")

    def test_parent_replay_bootstrap_starts_unchanged_parent_help(self):
        import response_geometry_gate as gate
        real_run = gate._run
        expected = (gate.PARENT_DIR / "docs/RESULTS.json").read_bytes()
        def help_only(command, cwd, timeout):
            try:
                output = real_run(command[:-2] + ["--help"], cwd, 10)
            except RuntimeError as error:
                self.fail(f"unchanged parent isolated imports failed: {error}")
            self.assertIn(b"--check", output)
            return expected
        with patch.object(gate, "_run", side_effect=help_only):
            receipt = gate._parent_replay()
        self.assertEqual(receipt["status"], "TRANSPORT_PROTOCOL_CERTIFIED")

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
                    "stage": "response_cases", "case": [7, FAMILY_KEYS[0], "1", 0],
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

    def test_nested_receipts_require_exact_ordered_keys_and_certificate_counts(self):
        import response_geometry_gate as gate
        valid_response = response_control(5)
        gate._validate_response_control(valid_response, 5)
        for changed in ({**valid_response, "scale_keys": "x" * 125},
                        {**valid_response, "scale_keys": [valid_response["scale_keys"][0]] * 125}):
            with self.assertRaises(ValueError):
                gate._validate_response_control(changed, 5)
        valid_carrier = carrier_control(5, "1")
        gate._validate_carrier_control(valid_carrier, 5, "1")
        changed_certificate = dict(valid_carrier["local_linear_certificate"])
        changed_certificate["local_basis_comparisons"] = 1279
        with self.assertRaises(ValueError):
            gate._validate_carrier_control({**valid_carrier,
                "local_linear_certificate": changed_certificate}, 5, "1")
        keys = list(valid_carrier["impulse_keys"])
        keys[1] = True
        with self.assertRaises(ValueError):
            gate._validate_carrier_control({**valid_carrier, "impulse_keys": keys}, 5, "1")

    def test_carrier_receipt_rejects_boolean_numeric_field(self):
        import response_geometry_gate as gate
        receipts = [carrier_receipt(L, scale) for L, scale in
                    ((5, "1"), (5, "7/3"), (7, "1"), (7, "7/3"))]
        receipts[0]["gauge_orbit_count"] = True
        with patch("response_geometry_gate._run_evaluator", return_value={
                "carrier_receipts": receipts, "origin_receipts": evaluator_origins()}):
            with self.assertRaisesRegex(ValueError, "carrier_receipt"):
                gate._carriers({"path": Path("unused")})

    def test_presentation_gauge_keys_must_be_complete_unique_ordered(self):
        cases = list(complete_cases(lambda *args: False))
        first = dict(cases[0])
        receipt = dict(first["presentation_receipt"])
        keys = list(receipt["gauge_keys"])
        keys[1] = keys[0]
        receipt["gauge_keys"] = keys
        first["presentation_receipt"] = receipt
        cases[0] = first
        self.assertEqual(classify(tuple(cases), True)[0], "RESPONSE_APPLICATION_INVALID")

    def test_failure_case_must_equal_next_ordered_prefix(self):
        import response_geometry_gate as gate
        with tempfile.TemporaryDirectory() as temporary:
            inputs = Path(temporary) / "INPUTS.json"
            inputs.write_text("{}")
            def failed(command, **kwargs):
                Path(command[command.index("--out") + 1]).write_text(json.dumps({"failure": {
                    "stage": "response_cases", "case": [7, FAMILY_KEYS[0], "1", 3],
                    "completed_cases": 250, "completed_faces": 6250,
                    "error_category": "ValueError", "message": "bad"}}))
                return SimpleNamespace(returncode=1, stderr=b"")
            with patch("response_geometry_gate.subprocess.run", side_effect=failed):
                with self.assertRaises(gate.StageFailure) as caught:
                    gate._run_evaluator({"path": inputs}, "cases")
            self.assertEqual(caught.exception.category, "MalformedChildFailure")

    def test_public_audit_has_no_executor_override(self):
        import inspect
        from response_geometry_gate import audit
        self.assertEqual(tuple(inspect.signature(audit).parameters), ())

    def test_cli_check_compares_exact_bytes_and_rejects_invalid_outcome(self):
        import response_geometry_gate as gate
        result, _ = run_test_gate()
        with tempfile.TemporaryDirectory() as temporary, patch(
                "response_geometry_gate.audit", return_value=result):
            path = Path(temporary) / "result.json"
            docs = Path(temporary) / 'docs'
            docs.mkdir()
            (docs / 'INPUTS.json').write_bytes(b'projection')
            def replay(input_path):
                input_path.write_bytes(b'projection')
                return result
            with patch("sys.stdout"), patch.object(gate, 'HERE', Path(temporary)), \
                 patch.object(gate, '_audit_to', side_effect=replay):
                self.assertEqual(main(["--out", str(path)]), 0)
                self.assertEqual(main(["--check", str(path)]), 0)
                path.write_bytes(canonical_bytes({}))
                self.assertNotEqual(main(["--check", str(path)]), 0)
        invalid, _ = run_test_gate(evidence=lambda: (_ for _ in ()).throw(ValueError("bad")))
        with patch("response_geometry_gate.audit", return_value=invalid), patch("sys.stdout"):
            self.assertNotEqual(main([]), 0)

    def test_check_uses_temporary_inputs_and_never_rewrites_committed_files(self):
        import response_geometry_gate as gate
        result = {'status': 'CANONICAL_RESPONSE_CURVATURE_NULL'}
        with tempfile.TemporaryDirectory() as temporary:
            checkout = Path(temporary)
            docs = checkout / 'docs'
            docs.mkdir()
            inputs = docs / 'INPUTS.json'
            inputs.write_bytes(b'committed projection\n')
            ledger = docs / 'RESULTS.json'
            ledger.write_bytes(canonical_bytes(result))
            original_stat = inputs.stat()
            def fake_audit(path):
                self.assertNotEqual(path, inputs)
                self.assertFalse(path.is_relative_to(checkout))
                path.write_bytes(b'committed projection\n')
                return result
            self.assertTrue(hasattr(gate, '_audit_to'), 'private output-path adapter is missing')
            with patch.object(gate, 'HERE', checkout), patch.object(gate, '_audit_to', side_effect=fake_audit), \
                 patch.object(gate, 'audit', side_effect=AssertionError('public audit would publish')), patch('sys.stdout'):
                self.assertEqual(main(['--check', str(ledger)]), 0)
                self.assertEqual(inputs.stat().st_mtime_ns, original_stat.st_mtime_ns)
                inputs.write_bytes(b'mismatched projection\n')
                self.assertEqual(main(['--check', str(ledger)]), 1)
                self.assertEqual(inputs.read_bytes(), b'mismatched projection\n')
                inputs.unlink()
                self.assertEqual(main(['--check', str(ledger)]), 1)

    def test_acquisition_output_adapter_preserves_default_and_explicit_destinations(self):
        import response_geometry_gate as gate
        from test_projection import valid_projection_bytes
        raw = valid_projection_bytes()
        origins = {name: {'blob': 'a' * 40} for name in (
            'pretime_gravity_canary.py', 'exact_linear.py', 'representation_actions.py',
            'response_generation.py', 'response_geometry.py', 'acquire.py', 'evidence.py', 'projection.py')}
        def produce(command, cwd, timeout):
            Path(command[command.index('--out') + 1]).write_bytes(raw)
            Path(command[command.index('--receipt') + 1]).write_bytes(canonical_bytes(origins))
            return b''
        with tempfile.TemporaryDirectory() as temporary:
            checkout = Path(temporary) / 'checkout'
            checkout.mkdir()
            destination = Path(temporary) / 'elsewhere/INPUTS.json'
            self.assertTrue(hasattr(gate, '_audit_to'), 'private output-path adapter is missing')
            with patch.object(gate, 'HERE', checkout), patch.object(gate, '_run', side_effect=produce):
                for supplied, expected in ((None, checkout / 'docs/INPUTS.json'), (destination, destination)):
                    with patch.object(gate, '_audit', side_effect=lambda executors: executors.acquisition_projection()):
                        acquired = gate.audit() if supplied is None else gate._audit_to(supplied)
                    self.assertEqual(acquired['path'], expected)
                    self.assertEqual(expected.read_bytes(), raw)

    def test_ci_scope_rejects_changes_outside_additive_allowlist_and_plan_prefix_drift(self):
        self.assertIsNotNone(importlib.util.find_spec('ci_verify'), 'Task 6 runner is missing')
        import ci_verify as ci
        ci.validate_scope(['A\t' + ci.DEMO + '/application.py', 'A\t' + ci.PLAN])
        for line in ('M\t' + ci.DEMO + '/application.py', 'A\tREADME.md',
                     'R100\told\t' + ci.DEMO + '/new.py', 'A\t' + ci.DEMO + '-other/file'):
            with self.subTest(line=line), self.assertRaisesRegex(ValueError, 'nonadditive_scope'):
                ci.validate_scope([line])
        approved = (ci.ROOT / ci.PLAN).read_bytes()[:ci.PLAN_PREFIX_BYTES]
        ci.verify_plan_prefix(approved + b'\nExecution appendix\n')
        with self.assertRaisesRegex(ValueError, 'plan_prefix'):
            ci.verify_plan_prefix(b'!' + approved[1:])

    def test_ci_suite_rejects_wrong_counts_skips_expected_failures_and_test_failures(self):
        self.assertIsNotNone(importlib.util.find_spec('ci_verify'), 'Task 6 runner is missing')
        import ci_verify as ci
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            module = directory / 'test_sample.py'
            cases = ('pass', 'self.skipTest("skip")', 'self.fail("failure")')
            for body in cases:
                module.write_text('import unittest\nclass Sample(unittest.TestCase):\n'
                                  '    def test_one(self):\n        ' + body + '\n')
                if body == 'pass':
                    ci.run_suite(directory, ('test_sample',), 1, timeout=10)
                    with self.assertRaises(RuntimeError):
                        ci.run_suite(directory, ('test_sample',), 2, timeout=10)
                else:
                    with self.assertRaises(RuntimeError):
                        ci.run_suite(directory, ('test_sample',), 1, timeout=10)
            module.write_text('import unittest\nclass Sample(unittest.TestCase):\n'
                              '    @unittest.expectedFailure\n'
                              '    def test_one(self):\n        self.fail("expected")\n')
            with self.assertRaises(RuntimeError):
                ci.run_suite(directory, ('test_sample',), 1, timeout=10)

    def test_ci_stage_failure_and_timeout_fail_closed(self):
        import ci_verify as ci
        with self.assertRaises(RuntimeError):
            ci.run_stage('failure probe', [sys.executable, '-c', 'raise SystemExit(7)'], Path.cwd(), 10)
        with self.assertRaises(subprocess.TimeoutExpired):
            ci.run_stage('timeout probe', [sys.executable, '-c', 'while True: pass'], Path.cwd(), 0.1)


if __name__ == "__main__":
    unittest.main()
