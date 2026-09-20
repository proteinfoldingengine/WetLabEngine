import ast
from dataclasses import replace
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from controls import ControlExecutors, ControlStage, run_control_family
from protocol_gate import (_audit, audit, main, verify_firewall, verify_gate_evidence,
                           verify_operational, PRODUCTION_FILES)
from selection import audit_selection


def production_imports_and_names(paths):
    observed = set()
    for path in paths:
        for node in ast.walk(ast.parse(Path(path).read_text())):
            if isinstance(node, ast.Name):
                observed.add(node.id)
            elif isinstance(node, ast.Attribute):
                observed.add(node.attr)
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                observed.add(node.name)
            elif isinstance(node, ast.arg):
                observed.add(node.arg)
            elif isinstance(node, ast.alias):
                observed.update(node.name.split('.'))
                if node.asname:
                    observed.add(node.asname)
            elif isinstance(node, ast.ImportFrom):
                observed.update((node.module or '').split('.'))
    return observed


def contains_float(value):
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(contains_float(k) or contains_float(v) for k,v in value.items())
    if isinstance(value, (list,tuple)):
        return any(map(contains_float,value))
    return False


def render_result(value):
    return json.dumps(value, sort_keys=True, indent=2) + '\n'


class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def guarded_controls():
            def denied(*args, **kwargs):
                raise AssertionError('scientific controls attempted external I/O')
            with patch('builtins.open',side_effect=denied), patch('io.open',side_effect=denied), \
                 patch('subprocess.run',side_effect=denied):
                return run_control_family()
        cls.result = _audit(control_runner=guarded_controls)

    def test_all_exact_gates_produce_protocol_certified(self):
        self.assertEqual(self.result['status'], 'TRANSPORT_PROTOCOL_CERTIFIED')
        self.assertEqual(self.result['next_required_object'],
                         'APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION')
        self.assertEqual(self.result['Pillar_3'], 'OPEN')
        for name in ('scientific_breakthrough','response_geometry_applied','source_target_constructed',
                     'source_correspondence_evaluated','physical_connection_derived','physical_curvature_derived',
                     'stress_energy_derived','einstein_equations_derived','continuum_limit_derived','spacetime_derived'):
            self.assertIs(self.result[name],False)

    def test_early_failures_stop_before_later_callbacks(self):
        names = ('evidence_verifier','operational_verifier','manifest_factory','selection_auditor','control_runner')
        expected = ('evidence','operational','manifest','selection','controls')
        for index,name in enumerate(names):
            with self.subTest(name=name):
                def fail():
                    raise TypeError('injected stage failure')
                def forbidden():
                    raise AssertionError('later callback reached')
                kwargs = {key:forbidden for key in names[index+1:]}
                kwargs[name] = fail
                result = _audit(**kwargs)
                self.assertEqual(result['status'],'PROTOCOL_INVALID')
                self.assertEqual(result['failed_gate'],expected[index])

    def test_nonunique_selection_stops_before_controls(self):
        ambiguous = replace(audit_selection(), identifiable=False)
        result = _audit(selection_auditor=lambda:ambiguous,
                        control_runner=lambda: self.fail('controls reached'))
        self.assertEqual(result['status'],'PROTOCOL_NOT_IDENTIFIABLE')
        self.assertEqual(result['failed_gate'],'selection')

    def test_controls_stop_at_each_failed_or_raising_stage(self):
        stages = ('covariance','constant_null','l5_nonflat','every_root_equivalent',
                  'l7_holdout_nonflat','scale_exact','superposition_exact')
        for index,name in enumerate(stages):
            for raises in (False,True):
                calls=[]
                def callback(stage):
                    def invoke():
                        calls.append(stage)
                        if stages.index(stage)>index:
                            raise AssertionError('later control reached')
                        if stage == name and raises:
                            raise ArithmeticError('injected exact failure')
                        return ControlStage(stage != name)
                    return invoke
                executors=ControlExecutors(**{s:callback(s) for s in stages})
                result=_audit(operational_verifier=lambda:self.result['operational'],
                              control_runner=lambda:run_control_family(executors))
                self.assertEqual(result['status'],'PROTOCOL_INVALID')
                self.assertEqual(result['failed_gate'],name)
                self.assertEqual(calls,list(stages[:index+1]))

    def test_firewall_scans_full_production_closure(self):
        forbidden={'response_inputs','response_generation','source_target','coordinates','spectrum',
                   'numpy','newton','einstein','observational','fit','svd','eig','pinv'}
        self.assertTrue(production_imports_and_names(PRODUCTION_FILES).isdisjoint(forbidden))
        self.assertIn('fixtures.py',{p.name for p in PRODUCTION_FILES})
        self.assertIn('operational_complex.py',{p.name for p in PRODUCTION_FILES})
        self.assertTrue(verify_firewall()['import_closure_verified'])

    def test_firewall_rejects_prohibited_imports_identifiers_and_dynamic_access(self):
        for source in ('import response_inputs', 'from numpy.linalg import norm',
                       'def f(source_target): return source_target',
                       'x = __import__("os")', 'import importlib',
                       'from dataclasses import sys', 'x = f.__globals__',
                       'x = open("secret")', 'import unreviewed_module'):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'transport.py'
                path.write_text(source)
                with self.assertRaises(ValueError):
                    verify_firewall((path,))

    def test_evidence_verifies_parent_ancestry_and_vendor_bytes(self):
        actual=verify_gate_evidence()
        self.assertEqual(actual['parent_head'],'b9c5f29d8687a7dbc2af0595430aa73fbc5b8553')
        self.assertEqual(actual['exact_algebra.py'],'c67ea42b61321469f7735ce589f2e729b241666a')
        with patch('protocol_gate.subprocess.run') as run:
            run.return_value.returncode=1
            with self.assertRaises(ValueError):
                verify_gate_evidence()
        with patch('protocol_gate.git_blob_sha',return_value='bad'):
            with self.assertRaises(ValueError):
                verify_gate_evidence()

    def test_operational_stage_builds_canonical_verified_carriers(self):
        result=verify_operational()
        self.assertEqual([r['vertices'] for r in result],[25,49])
        self.assertTrue(all(r['baseline_flat'] for r in result))
        with patch('protocol_gate.construct_operational_complex',side_effect=ValueError('bad substrate')):
            failed=_audit(manifest_factory=lambda:self.fail('manifest reached'))
        self.assertEqual(failed['failed_gate'],'operational')

    def test_committed_ledger_exact_float_free_byte_stable(self):
        path=Path(__file__).parent/'docs/RESULTS.json'
        self.assertEqual(self.result,json.loads(path.read_text()))
        self.assertFalse(contains_float(self.result))
        self.assertEqual(render_result(self.result),path.read_text())
        self.assertEqual(self.result['selection']['centered_stencil']['solution'],['1/2','0','-1/2'])

    def test_cli_output_check_and_mismatch_exit(self):
        with tempfile.TemporaryDirectory() as tmp, patch('protocol_gate.audit',return_value=self.result):
            path=Path(tmp)/'result.json'
            with patch('sys.stdout'):
                self.assertEqual(main(['--out',str(path)]),0)
                self.assertEqual(main(['--check',str(path)]),0)
                path.write_text('{}\n')
                self.assertNotEqual(main(['--check',str(path)]),0)


if __name__=='__main__':
    unittest.main()
