"""Fail-closed, exact-head v15.43 certification; never publish artifacts in place."""
from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from evidence import git_blob, verify_repository_evidence
from firewall import verify_firewall

PARENT = '0f426fa28d22871ce042e39bf9704695ede8b336'
DEMO = 'ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry'
PLAN = 'docs/superpowers/plans/2026-09-20-v1543-certified-response-geometry-implementation.md'
SPEC = 'docs/superpowers/specs/2026-09-20-v1543-certified-response-geometry-design.md'
WORKFLOW = '.github/workflows/uqcf-v1543-certified-response-geometry.yml'
PLAN_PREFIX_BYTES = 41371
PLAN_PREFIX_BLOB = 'e4155758d83029f6b6727c8d75260feb67d1bcb1'
SPEC_BLOB = '680f691538b99037b89d52b6c93742495d039d4e'
V1543_TEST_COUNT = 79
MODULES = ('test_evidence', 'test_projection', 'test_carriers',
           'test_application', 'test_controls', 'test_gate')


def run_stage(stage, command, cwd, timeout):
    print(f'STAGE {stage}: {command!r}', flush=True)
    completed = subprocess.run(command, cwd=cwd, capture_output=True, timeout=timeout)
    if completed.stdout:
        sys.stdout.buffer.write(completed.stdout)
        sys.stdout.flush()
    if completed.stderr:
        sys.stderr.buffer.write(completed.stderr)
        sys.stderr.flush()
    if completed.returncode:
        raise RuntimeError(f'{stage}: exit {completed.returncode}')
    return completed.stdout


def git_diff_name_status(base, head):
    return run_stage('scope', ['git', 'diff', '--name-status', base, head], ROOT, 30).decode().splitlines()


def allowed_v1543_path(path):
    return path.startswith(DEMO + '/') or path in (PLAN, SPEC, WORKFLOW)


def validate_scope(lines):
    for line in lines:
        fields = line.split('\t')
        if len(fields) != 2 or fields[0] != 'A' or not allowed_v1543_path(fields[1]):
            raise ValueError('nonadditive_scope')


def verify_plan_prefix(raw):
    if len(raw) < PLAN_PREFIX_BYTES or git_blob(raw[:PLAN_PREFIX_BYTES]) != PLAN_PREFIX_BLOB:
        raise ValueError('plan_prefix_mismatch')


def verify_scope_pins():
    validate_scope(git_diff_name_status(PARENT, 'HEAD'))
    verify_repository_evidence(ROOT)
    if git_blob((ROOT / SPEC).read_bytes()) != SPEC_BLOB:
        raise ValueError('approved_spec_mismatch')
    verify_plan_prefix((ROOT / PLAN).read_bytes())
    paths = tuple(HERE / name for name in (
        'acquire.py', 'evaluate.py', 'response_geometry_gate.py', 'projection.py',
        'carriers.py', 'application.py', 'presentation_checks.py',
        'application_controls.py', 'evidence.py', 'firewall.py', 'ci_verify.py'))
    verify_firewall(paths)


def run_suite(directory, modules, count, timeout=1800):
    # Each suite owns a fresh isolated namespace, including sibling test modules.
    bootstrap = (
        'import pathlib, sys, unittest; '
        'root = pathlib.Path(sys.argv[1]).resolve(); sys.path.insert(0, str(root)); '
        'names = sys.argv[3:]; '
        'suite = unittest.defaultTestLoader.loadTestsFromNames(names); '
        'origins_ok = all(pathlib.Path(sys.modules[n].__file__).resolve().parent == root '
        'for n in names if n in sys.modules); '
        'result = unittest.TextTestRunner(verbosity=2).run(suite); '
        'ok = origins_ok and result.wasSuccessful() and result.testsRun == int(sys.argv[2]) '
        'and not result.skipped and not result.expectedFailures and not result.unexpectedSuccesses; '
        'print("SUITE_COUNT", result.testsRun, "EXPECTED", sys.argv[2], "ACCEPTED", ok); '
        'sys.exit(0 if ok else 1)')
    return run_stage(f'suite {directory.name}',
                     [sys.executable, '-I', '-B', '-c', bootstrap, str(directory), str(count), *modules],
                     directory, timeout)


def replay(directory, filename, timeout):
    bootstrap = ('import runpy, sys; sys.path.insert(0, sys.argv[1]); '
                 'sys.argv = sys.argv[2:]; runpy.run_path(sys.argv[0], run_name="__main__")')
    raw = run_stage(f'replay {directory.name}',
                    [sys.executable, '-I', '-c', bootstrap, str(directory),
                     str(directory / filename), '--check', 'docs/RESULTS.json'], directory, timeout)
    if raw != (directory / 'docs/RESULTS.json').read_bytes():
        raise ValueError('replay_byte_mismatch')


def verify_artifacts():
    raw = (HERE / 'docs/RESULTS.json').read_bytes()
    result = json.loads(raw)
    if raw != (json.dumps(result, sort_keys=True, indent=2) + '\n').encode():
        raise ValueError('noncanonical_results')
    if result['status'] not in ('CANONICAL_RESPONSE_CURVATURE_NULL',
                                'CANONICAL_RESPONSE_CURVATURE_NONZERO',
                                'CANONICAL_RESPONSE_CURVATURE_MIXED'):
        raise ValueError('invalid_status')
    cases = result['cases']
    if (result['completed_counts'] != {'cases': 740, 'faces': 30260} or len(cases) != 740 or
            sum(c['family'] == 'GLOBAL_BALANCE_COMPLETION' for c in cases) != 148 or
            sum(len(c['faces']) for c in cases) != 30260):
        raise ValueError('incomplete_coverage')
    expected_claims = {
        'source_correspondence': 'NOT_EVALUATED', 'Pillar_3': 'OPEN',
        'physical_metric': False, 'physical_curvature': False, 'stress_energy': False,
        'einstein_equations': False, 'continuum_limit': False, 'spacetime': False,
        'physical_gravity': False, 'scientific_breakthrough': False,
        'fundamental_time_introduced': False, 'dark_matter_primitive_introduced': False,
        'inherited_axiom_dependence': True, 'isotropic_scalar_lift_dependence': True}
    if result['claims'] != expected_claims:
        raise ValueError('claim_boundary')
    inputs = (HERE / 'docs/INPUTS.json').read_bytes()
    if result['input_hashes'][-1] != sha256(inputs).hexdigest():
        raise ValueError('input_hash_mismatch')
    print('COVERAGE 740 cases / 148 canonical / 30260 faces; claims verified', flush=True)


def main():
    if sys.version_info[:3] != (3, 13, 5):
        raise ValueError('official_python_must_be_3.13.5')
    head = run_stage('head', ['git', 'rev-parse', 'HEAD'], ROOT, 30).decode().strip()
    run_stage('clean tracked tree', ['git', 'diff', '--exit-code', 'HEAD'], ROOT, 30)
    # Bound the inherited ancestry subprocess too, without editing its frozen owner.
    bootstrap = ('import sys; sys.path.insert(0, sys.argv[1]); '
                 'import ci_verify; ci_verify.verify_scope_pins()')
    run_stage('scope and pins', [sys.executable, '-I', '-c', bootstrap, str(HERE)], ROOT, 60)
    parent = HERE.parent / 'v15.42-duality-covariant-transport-repair'
    run_suite(parent, ('test_evidence', 'test_selection', 'test_transport',
                       'test_holonomy', 'test_controls', 'test_gate'), 48)
    run_stage('install pinned numpy', [sys.executable, '-m', 'pip', 'install', 'numpy==2.3.5'], ROOT, 600)
    run_suite(HERE, MODULES, V1543_TEST_COUNT)
    for directory, modules, count in (
        ('v15.39-higher-incidence-source-axioms', ('test_gate',), 8),
        ('v15.40-global-balance-geometry-specificity', ('test_gate',), 9),
        ('v15.41-formal-connection-curvature-source-correspondence',
         ('test_operational_complex', 'test_linearized_connection', 'test_gate'), 26)):
        run_suite(HERE.parent / directory, modules, count)
    old = HERE.parent / 'v15.41-formal-connection-curvature-source-correspondence'
    replay(old, 'connection_curvature_gate.py', 1800)
    input_before = (HERE / 'docs/INPUTS.json').read_bytes()
    replay(HERE, 'response_geometry_gate.py', 7200)
    if (HERE / 'docs/INPUTS.json').read_bytes() != input_before:
        raise ValueError('committed_inputs_changed')
    # --check compared the newly projected temporary bytes with these committed bytes.
    print('PROJECTED_INPUTS_BYTE_IDENTICAL', flush=True)
    run_stage('compile', [sys.executable, '-m', 'compileall', '-q', str(HERE)], ROOT, 120)
    verify_artifacts()
    run_stage('unchanged tracked tree', ['git', 'diff', '--exit-code', 'HEAD'], ROOT, 30)
    if run_stage('final head', ['git', 'rev-parse', 'HEAD'], ROOT, 30).decode().strip() != head:
        raise ValueError('certification_head_changed')
    print(f'V1543_CERTIFIED_HEAD {head}', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
