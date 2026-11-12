"""Read-only audit of frozen T-246 evidence; no network or model calls.

Usage: python audit_t246.py /path/to/WetLabEngine output.json review.zip
Replays only the previously frozen checker/controls, not a new scientific domain.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

COMMIT = '85db2dde33896e3de68c4b4623c09a58e65a8c5d'
SCIENCE = 'ecbeaaef528e239abee43f891e376347c52a5c14'
ROOT = 'ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_delivery_boundary/successor_t241/'
REVIEW = ROOT + 'review/actions-41340518437/'
EVIDENCE = ROOT + 'evidence/actions-41335726832/'
repo = Path(sys.argv[1]).resolve()

def blob(path, commit=COMMIT):
    return subprocess.check_output(['git', '-C', str(repo), 'show', commit + ':' + path])

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def obj(path):
    return json.loads(blob(path))

checks = {}
manifest = obj(REVIEW + 'artifact_manifest.json')
for name, entry in manifest.items():
    raw = blob(REVIEW + name)
    assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], name
checks['review_manifest_files'] = len(manifest)
archive = Path(sys.argv[3])
assert sha(archive.read_bytes()) == 'b1ce7a3400e5a8e0914d8a7e7e367655df32635c7be6f3a25ef4221669f83d68'
with zipfile.ZipFile(archive) as z:
    expected = set(manifest) | {'artifact_manifest.json'}
    assert len(z.namelist()) == len(expected) and set(z.namelist()) == expected
    for name in expected:
        assert z.read(name) == blob(REVIEW + name), name
checks['original_review_zip_exact_members'] = len(expected)
checks['original_review_zip_sha256'] = sha(archive.read_bytes())
for line in blob(REVIEW + 'SHA256SUMS').decode().splitlines():
    digest, name = line.split(maxsplit=1)
    assert sha(blob(REVIEW + name.lstrip('*'))) == digest, name
checks['review_sha256sums'] = True
docs = obj(REVIEW + 'documents.json')
prompt = blob(REVIEW + 'prompt.txt')
for name, entry in docs.items():
    raw = blob(entry['path'], SCIENCE)
    assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], name
    assert blob(entry['path']) == raw, name
    marker = ('\nEXACT DOCUMENT ' + name + '\nUTF8-BYTES ' + str(len(raw)) + '\n').encode()
    assert prompt.count(marker) == 1 and marker + raw + b'\nEND EXACT DOCUMENT\n' in prompt, name
checks['documents_exact_in_prompt_and_at_both_commits'] = len(docs)
request = obj(REVIEW + 'request.json')
assert request['contents'][0]['parts'][0]['text'].encode() == prompt
checks['request_contains_exact_prompt'] = True
response = obj(REVIEW + 'response.json')
assert len(response['candidates']) == 1
candidate = response['candidates'][0]
assert candidate['finishReason'] == 'STOP'
assert not response.get('promptFeedback', {}).get('blockReason')
answer = '\n'.join(p['text'] for p in candidate['content']['parts'] if not p.get('thought', False) and isinstance(p.get('text'), str)).strip().encode()
assert answer == blob(REVIEW + 'review.txt')
verdict = json.loads(answer)
assert verdict == obj(REVIEW + 'verdict.json')
identity = obj(REVIEW + 'review_identity.json')
assert identity['prompt_sha256'] == sha(prompt)
assert identity['response_sha256'] == sha(blob(REVIEW + 'response.json'))
assert identity['model_returned'] == response['modelVersion'] == identity['model_requested']
assert identity['science_sha'] == identity['workflow_sha'] == SCIENCE
checks['raw_response_review_verdict_identity_agree'] = True
for line in blob(EVIDENCE + 'SHA256SUMS').decode().splitlines():
    digest, name = line.split(maxsplit=1)
    assert sha(blob(EVIDENCE + name.lstrip('*'))) == digest, name
checks['scientific_evidence_sha256sums'] = True
with tempfile.TemporaryDirectory(prefix='uqcf-t246-readback-') as tmp:
    directory = Path(tmp)
    for name in ('produce_s.py', 'verify_s.py', 'test_controls_s.py'):
        (directory / name).write_bytes(blob(ROOT + name))
    (directory / 'certificate.json').write_bytes(blob(EVIDENCE + 'certificate.json'))
    for script, output in [('verify_s.py', 'verification.json'), ('test_controls_s.py', 'controls.json')]:
        proc = subprocess.run([sys.executable, '-B', script, 'certificate.json', 'produce_s.py'], cwd=directory, capture_output=True, check=True)
        assert proc.stdout == blob(EVIDENCE + output), output
        checks[output] = json.loads(proc.stdout)
result = {
    'audited_commit': COMMIT,
    'review_science_commit': SCIENCE,
    'checks': checks,
    'model_verdict': verdict['verdict'],
    'findings_count': len(verdict['findings']),
    'established_acceptance_gate_passes': verdict['verdict'] == 'ACCEPTED' and all(verdict[k] == [] for k in ('findings', 'missing_assumptions', 'counterexamples')),
    'native_bridge_status': verdict['native_bridge_status'],
    'raw_response_sha256': identity['response_sha256'],
    'audit_script_sha256': sha(Path(__file__).read_bytes()),
    'python_version': sys.version,
    'scope': 'Published-byte integrity, original review ZIP and frozen stdlib checker/controls replay only. No producer, FCV or model rerun; no general proof certification, full log audit, or merge acceptance.',
}
Path(sys.argv[2]).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps(result, indent=2, sort_keys=True))
