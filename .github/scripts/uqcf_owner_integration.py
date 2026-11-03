"""Replay the frozen T-277 packet and check archive integrity without a model call."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path.cwd()
BASE = ROOT / 'ResearchHistory/UQCF-GEM/research/physical-bridge/native_owner_correspondence'
OLD = BASE / 'evidence/run-41540085233-attempt-1'
OUT = ROOT / 'owner_integration_audit'
FCV = ROOT / 'ResearchHistory/UQCF-GEM/foundational-closure-verification'
DEMOS = ROOT / 'ResearchHistory/UQCF-GEM/demos'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def check_bytes(raw, expected, label):
    require(len(raw) == expected['bytes'] and digest(raw) == expected['sha256'], label)

def main():
    OUT.mkdir()
    commands = []
    def call(name, argv, cwd=ROOT):
        with (OUT / name).open('wb') as log:
            result = subprocess.run(argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
        commands.append({'name': name, 'argv': argv, 'exit_code': result.returncode,
                         'cwd': str(cwd.relative_to(ROOT))})
        write('commands.json', commands)
        print(name, 'exit', result.returncode, flush=True)
        require(result.returncode == 0, name)
    try:
        checkout = git('rev-parse', 'HEAD')
        require(checkout == os.environ['GITHUB_SHA'], 'checkout identity')
        freeze = json.loads((BASE / 'REVIEW_FREEZE.json').read_bytes())
        for row in freeze['sources']:
            raw = (ROOT / row['path']).read_bytes()
            check_bytes(raw, row, row['path'])
            require(git('hash-object', row['path']) == row['blob'], 'source blob')
        for path, row in freeze['controllers'].items():
            check_bytes((ROOT / path).read_bytes(), row, path)

        # Reject deliberate byte corruption before trusting hash-based checks.
        controls = []
        for label, raw, expected in [
            ('altered-bytes', b'wrong', {'bytes': 5, 'sha256': digest(b'right')}),
            ('wrong-length', b'right', {'bytes': 4, 'sha256': digest(b'right')})]:
            try:
                check_bytes(raw, expected, label)
            except ValueError:
                controls.append(label)
            else:
                raise ValueError('control accepted: ' + label)
        write('archive_controls.json', {'rejected': controls})

        declared = {}
        for line in (OLD / 'SHA256SUMS').read_text().splitlines():
            sha, name = line.split('  ', 1)
            require(name not in declared and (OLD / name).resolve().is_relative_to(OLD.resolve()), 'manifest path')
            declared[name] = sha
            require(digest((OLD / name).read_bytes()) == sha, 'archive file ' + name)
        actual = {str(p.relative_to(OLD)) for p in OLD.rglob('*') if p.is_file() and p.name != 'SHA256SUMS'}
        require(actual == set(declared), 'archive exact inventory')
        parts = json.loads((OLD / 'owner-correspondence-verification-1.zip.parts.json').read_bytes())
        whole = hashlib.sha256()
        total = 0
        for row in parts['parts']:
            raw = (OLD / row['file']).read_bytes()
            check_bytes(raw, row, 'archive chunk')
            whole.update(raw)
            total += len(raw)
        require(total == parts['bytes'] and whole.hexdigest() == parts['sha256'], 'original ZIP reconstruction')
        review = OLD / 'owner-correspondence-review-1'
        require(digest((review / 'response.json').read_bytes()) == '2f3be2ac1058c5d9e58eeb55bf6fec9253d26c965c86195348dc3dd133ec46ef', 'original review')

        scripts = BASE / 'review_tools'
        call('certificate.json', [sys.executable, str(scripts / 'produce.py')])
        call('verification.json', [sys.executable, str(scripts / 'verify.py'), str(OUT / 'certificate.json')])
        call('controls.json', [sys.executable, str(scripts / 'controls.py'), str(OUT / 'certificate.json'), str(OUT / 'red')])
        for name in ('certificate.json', 'verification.json', 'controls.json'):
            require((OUT / name).read_bytes() == (OLD / 'owner-correspondence-verification-1' / name).read_bytes(), 'frozen replay ' + name)

        call('dependencies.log', [sys.executable, '-m', 'pip', 'freeze'])
        call('fcv-tests.log', [sys.executable, 'tests/test_fcv.py'], FCV)
        call('parent-tests.log', [sys.executable, '-m', 'unittest', '-v', 'test_pruning_consistency_audit'], DEMOS / 'v15.56-response-selector-obstruction')
        call('historical-tests.log', [sys.executable, '-m', 'unittest', '-v'], DEMOS / 'v16.15F-graded-obstruction-descent')
        call('historical-reproduction.log', [sys.executable, 'gate.py'], DEMOS / 'v16.15F-graded-obstruction-descent')
        (FCV / 'evidence').mkdir(exist_ok=True)
        (FCV / 'evidence/REPRODUCED_1615F.json').write_bytes((DEMOS / 'v16.15F-graded-obstruction-descent/result.json').read_bytes())
        call('producer.log', [sys.executable, 'produce_certificates.py'], FCV)
        call('independent-verifier.log', [sys.executable, 'verify_certificates.py'], FCV)
        for name in ('certificates.json.xz', 'PRODUCTION.json', 'VERIFICATION.json', 'REPRODUCED_1615F.json'):
            raw = (FCV / 'evidence' / name).read_bytes()
            require(raw == (OLD / 'owner-correspondence-verification-1/inherited' / name).read_bytes(), 'inherited replay ' + name)
            (OUT / name).write_bytes(raw)
        require(json.loads((OUT / 'VERIFICATION.json').read_bytes())['all_valid'] is True, 'inherited certificate')
        write('receipt.json', {'status': 'PASS', 'checkout_sha': checkout,
              'workflow_sha': os.environ.get('UQCF_WORKFLOW_SHA'), 'run_id': os.environ['GITHUB_RUN_ID'],
              'run_attempt': os.environ['GITHUB_RUN_ATTEMPT'], 'ref': os.environ['GITHUB_REF'],
              'original_execution_sha': 'c721762f4890a81036fb2bff11d394881384496f',
              'argument_blob': git('hash-object', str(BASE / 'ANALYTICAL_BOUNDARY.md')),
              'archived_files_checked': len(declared), 'original_zip_sha256': whole.hexdigest(),
              'replayed_files': 7, 'new_model_calls': 0, 'native_bridge': 'NOT_DERIVED'})
        for path in (Path('.github/scripts/uqcf_owner_integration.py'), Path('.github/workflows/uqcf-owner-integration.yml')):
            (OUT / path.name).write_bytes((ROOT / path).read_bytes())
    except Exception as exc:
        write('failure.json', {'status': 'FAILED', 'type': type(exc).__name__, 'detail': str(exc)})
        raise
    finally:
        write('artifact_manifest.json', {str(p.relative_to(OUT)): {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
              for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'artifact_manifest.json'})

if __name__ == '__main__':
    main()
