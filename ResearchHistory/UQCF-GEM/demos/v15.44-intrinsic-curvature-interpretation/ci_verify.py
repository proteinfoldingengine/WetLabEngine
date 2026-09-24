"""Fail-closed exact-head certification for the finite v15.44 characterization."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from hashlib import sha1, sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from evidence import PARENT, PARENT_TREE, verify_evidence
from gate import result_bytes

DEMO = 'ResearchHistory/UQCF-GEM/demos/v15.44-intrinsic-curvature-interpretation'
SPEC = 'docs/superpowers/specs/2026-09-22-v1544-intrinsic-curvature-interpretation-design.md'
PLAN = 'docs/superpowers/plans/2026-09-22-v1544-intrinsic-curvature-interpretation-implementation.md'
WORKFLOW = '.github/workflows/uqcf-v1544-intrinsic-curvature-interpretation.yml'
SPEC_BLOB = '6df4678d903d5a841f426505abf0a5e1070436e8'
PLAN_BLOB = 'eb86258e2753bbcddcacf661178de9a8c5ec5e2b'
V1544_TEST_COUNT = 64
MODULES = ('test_evidence','test_exact_matrix','test_operator','test_kernel',
           'test_presentations','test_compare','test_gate','test_ci')
EXPECTED_CLAIMS = {
    'source_correspondence':'NOT_EVALUATED','Pillar_3':'OPEN',
    'physical_metric':False,'physical_curvature':False,'stress_energy':False,
    'einstein_equations':False,'continuum_limit':False,'spacetime':False,
    'physical_gravity':False,'foundational_uniqueness':False,
    'scientific_breakthrough':False,'inherited_axiom_dependence':True,
    'isotropic_scalar_lift_dependence':True,'fundamental_time_introduced':False,
    'dark_matter_primitive_introduced':False}


def git_blob(raw):
    return sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def run_stage(stage, command, cwd, timeout, *, runner=subprocess.run):
    print(f'STAGE {stage}: {command!r}', flush=True)
    completed=runner(command,cwd=cwd,capture_output=True,timeout=timeout)
    if completed.stdout:
        sys.stdout.buffer.write(completed.stdout); sys.stdout.flush()
    if completed.stderr:
        sys.stderr.buffer.write(completed.stderr); sys.stderr.flush()
    if completed.returncode: raise RuntimeError(f'{stage}: exit {completed.returncode}')
    return completed.stdout


def verify_runtime(version):
    if tuple(version)!=(3,13,5): raise ValueError('official_python_must_be_3.13.5')


def verify_head(expected, observed, stage):
    if not expected or observed != expected: raise ValueError(stage+'_head_mismatch')


def verify_blob(raw, expected, name):
    if git_blob(raw) != expected: raise ValueError(name+'_mismatch')


def validate_scope(lines):
    allowed=(SPEC,PLAN,WORKFLOW)
    for line in lines:
        fields=line.split('\t')
        if (len(fields)!=2 or fields[0]!='A' or
                not (fields[1].startswith(DEMO+'/') or fields[1] in allowed)):
            raise ValueError('nonadditive_scope')


def verify_scope_and_pins():
    raw=run_stage('scope',['git','diff','--name-status',PARENT,'HEAD'],ROOT,30)
    validate_scope(raw.decode().splitlines())
    if run_stage('parent tree',['git','rev-parse',PARENT+'^{tree}'],ROOT,30).decode().strip()!=PARENT_TREE:
        raise ValueError('parent_tree_mismatch')
    run_stage('parent ancestry',['git','merge-base','--is-ancestor',PARENT,'HEAD'],ROOT,30)
    verify_blob((ROOT/SPEC).read_bytes(),SPEC_BLOB,'approved_spec')
    verify_blob((ROOT/PLAN).read_bytes(),PLAN_BLOB,'approved_plan')
    verify_evidence(ROOT)


def suite_command():
    bootstrap=(
        'import pathlib,sys,unittest; '
        'root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root)); '
        'names=sys.argv[3:];suite=unittest.defaultTestLoader.loadTestsFromNames(names); '
        'origins=all(pathlib.Path(sys.modules[n].__file__).resolve().parent==root for n in names); '
        'r=unittest.TextTestRunner(verbosity=2).run(suite); '
        'ok=origins and r.wasSuccessful() and r.testsRun==int(sys.argv[2]) and not r.skipped '
        'and not r.expectedFailures and not r.unexpectedSuccesses; '
        'print();print("SUITE_COUNT",r.testsRun,"EXPECTED",sys.argv[2],"SKIPS",len(r.skipped),'
        '"EXPECTED_FAILURES",len(r.expectedFailures),"UNEXPECTED_SUCCESSES",len(r.unexpectedSuccesses),'
        '"ACCEPTED",ok);sys.exit(0 if ok else 1)')
    return [sys.executable,'-I','-B','-c',bootstrap,str(HERE),str(V1544_TEST_COUNT),*MODULES]


def verify_suite_receipt(raw, expected):
    marker=(f'SUITE_COUNT {expected} EXPECTED {expected} SKIPS 0 EXPECTED_FAILURES 0 '
            'UNEXPECTED_SUCCESSES 0 ACCEPTED True').encode()
    if raw.splitlines().count(marker)!=1: raise ValueError('suite_receipt')


def verify_result(result):
    if (type(result) is not dict or result.get('status')!='INTRINSIC_CURVATURE_CHARACTERIZED' or
            result.get('first_failed_stage') is not None or result.get('failure') is not None or
            result.get('completed_counts')!={'cases':740,'controls':4,'pairs':592,'scale_pairs':370}):
        raise ValueError('incomplete_coverage')
    verdict=result.get('scientific_verdict')
    if type(verdict) is not dict or verdict.get('claims') != EXPECTED_CLAIMS:
        raise ValueError('claim_boundary')
    if (len(verdict.get('cases',()))!=740 or len(verdict.get('pairs',()))!=592 or
            len(verdict.get('scale_pairs',()))!=370 or
            verdict.get('interpretation')!='EXACT_FINITE_FOUR_CARRIER_CHARACTERIZATION_ONLY'):
        raise ValueError('incomplete_coverage')
    coverage=verdict.get('coverage',{})
    if (coverage.get('cases')!=740 or coverage.get('pairs')!=592 or coverage.get('scale_pairs')!=370 or
            coverage.get('by_carrier') != [
                {'L':5,'scale':'1','pairs':100},{'L':5,'scale':'7/3','pairs':100},
                {'L':7,'scale':'1','pairs':196},{'L':7,'scale':'7/3','pairs':196}] or
            sorted(coverage.get('by_control',{}).values()) != [148,148,148,148]):
        raise ValueError('incomplete_coverage')
    carriers=verdict.get('carriers')
    if type(carriers) is not list or [(c.get('L'),c.get('scale')) for c in carriers] != [
            (5,'1'),(5,'7/3'),(7,'1'),(7,'7/3')]:
        raise ValueError('certificate_coverage')
    for carrier in carriers:
        certificate=carrier.get('certificate',{}); control=carrier.get('control',{})
        n=carrier['L']**2; rank=certificate.get('rank'); nullity=certificate.get('nullity')
        if (type(rank) is not int or type(nullity) is not int or rank+nullity!=n or
                len(certificate.get('null_basis',()))!=n or
                any(len(row)!=nullity for row in certificate.get('null_basis',())) or
                control.get('rank')!=rank or control.get('nullity')!=nullity or
                control.get('exact') is not True or carrier.get('constant_field_annihilated') is not True):
            raise ValueError('certificate_coverage')


def verify_artifact():
    raw=(HERE/'docs/RESULTS.json').read_bytes()
    result=json.loads(raw)
    if raw != result_bytes(result):
        raise ValueError('noncanonical_results')
    verify_result(result)
    digest=sha256(raw).hexdigest()
    print('LEDGER_SHA256 '+digest,flush=True)
    return digest


def main():
    verify_runtime(sys.version_info[:3])
    expected=os.environ.get('GITHUB_SHA')
    head=run_stage('head',['git','rev-parse','HEAD'],ROOT,30).decode().strip()
    verify_head(expected,head,'initial')
    run_stage('clean tracked tree',['git','diff','--exit-code','HEAD'],ROOT,30)
    verify_scope_and_pins()
    suite=run_stage('focused suite',suite_command(),HERE,1800)
    verify_suite_receipt(suite,V1544_TEST_COUNT)
    run_stage('complete canonical replay',[sys.executable,'-I','-B',str(HERE/'gate.py'),
              '--check','docs/RESULTS.json'],HERE,7200)
    digest=verify_artifact()
    run_stage('compile',[sys.executable,'-m','compileall','-q',str(HERE)],ROOT,120)
    run_stage('unchanged tracked tree',['git','diff','--exit-code','HEAD'],ROOT,30)
    final=run_stage('final head',['git','rev-parse','HEAD'],ROOT,30).decode().strip()
    verify_head(expected,final,'final')
    print(f'V1544_CERTIFIED_HEAD {final} LEDGER_SHA256 {digest}',flush=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
