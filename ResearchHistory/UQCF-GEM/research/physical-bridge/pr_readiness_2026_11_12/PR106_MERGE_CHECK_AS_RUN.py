"""Offline byte/provenance audit for the PR106 base-sync merge; no science run."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import zipfile
import yaml

ROOT = Path('/workspace/scratch/25b1738236c6/pr106_conflict')
OLD = 'fb80f4645342e0f25615ec1c52d7cfa03fa9b3d1'
BASE = '48e4282aae98f554ebc5c4dcd333bda304b04c9a'
ANCESTOR = '7a624ad9a93b47ccca6c6944b1f5720e9259958e'
REL = 'ResearchHistory/UQCF-GEM/research/physical-bridge/native_structure'
LEDGER = 'ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def contents(ref, path):
    return git('show', ref + ':' + path)

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def tree(ref):
    out = {}
    for entry in git('ls-tree', '-rz', ref).split(b'\0'):
        if entry:
            spec, path = entry.split(b'\t', 1)
            mode, kind, sha = spec.decode().split()
            out[path.decode()] = (mode, kind, sha)
    return out

assert not git('diff', '--name-only', '--diff-filter=U').strip()
merged_tree_sha = git('write-tree').decode().strip()
ancestor, old, base, merged = map(tree, [ANCESTOR, OLD, BASE, merged_tree_sha])
changed = {p for p in set(ancestor) | set(old) if ancestor.get(p) != old.get(p)}
assert len(changed) == 49
assert all(p in old for p in changed), 'PR unexpectedly deletes source paths'
actual_delta = {p for p in set(base) | set(merged) if base.get(p) != merged.get(p)}
assert actual_delta == changed, (actual_delta - changed, changed - actual_delta)
assert all(p in merged for p in base), 'Base paths deleted'
assert all(merged[p] == base[p] for p in base if p != LEDGER), 'Base content altered'
assert all(merged[p] == old[p] for p in changed if p != LEDGER), 'Reviewed PR content altered'
assert all(merged[p] == base[p] for p in base if p.endswith('AGENTS.md'))

a = contents(ANCESTOR, LEDGER)
h = contents(OLD, LEDGER)
b = contents(BASE, LEDGER)
r = (ROOT / LEDGER).read_bytes()
assert h.startswith(a) and b.startswith(a)
assert r == h + b[len(a):]
assert merged[LEDGER][2] == blob(r)
assert not re.search(rb'^(<<<<<<< |=======$|>>>>>>> )', r, re.M)
subprocess.run(['git', '-C', str(ROOT), 'diff', '--cached', '--check', BASE, '--', LEDGER], check=True)

packet = json.loads((ROOT / REL / 'source_packet.json').read_bytes())
assert packet['baseline'] == ANCESTOR
for entry in packet['files']:
    data = entry['content'].encode()
    assert blob(data) == entry['git_blob']
    assert contents(packet['baseline'], entry['path']) == data

manifests = sorted((ROOT / REL).glob('evidence/**/manifest.json'))
accepted = []
failed = []
for path in manifests:
    m = json.loads(path.read_bytes())
    folder = path.parent
    assert m['workflow_sha'] == m['scientific_sha']
    assert m['model_requested'] == m['model_returned'] == 'gemini-3.1-pro-preview'
    for name, identity in m['inputs'].items():
        data = contents(m['scientific_sha'], name)
        assert digest(data) == identity['sha256'] and blob(data) == identity['git_blob']
    for name in ('prompt', 'response', 'review'):
        extension = '.json' if name == 'response' else '.txt'
        assert digest((folder / (name + extension)).read_bytes()) == m[name + '_sha256']
    response = json.loads((folder / 'response.json').read_bytes())
    assert len(response['candidates']) == 1 and response['candidates'][0]['finishReason'] == 'STOP'
    answer = '\n'.join(part['text'] for part in response['candidates'][0]['content']['parts'] if not part.get('thought', False)).strip().encode()
    assert answer == (folder / 'review.txt').read_bytes()
    verdict = json.loads(answer)
    assert verdict == json.loads((folder / 'verdict.json').read_bytes())
    if (folder / 'failure.json').exists():
        failed.append(m['run_id'])
        assert verdict['findings'], 'Preserved failed-schema run must still fail strict gate'
    else:
        assert verdict['verdict'] == 'ACCEPTED'
        assert all(verdict[k] == [] for k in ('findings', 'missing_assumptions', 'counterexamples'))
        accepted.append(m['run_id'])
        if str(m['run_id']) == '39003068802':
            for name, identity in m['inputs'].items():
                data = (ROOT / name).read_bytes()
                assert digest(data) == identity['sha256'] and blob(data) == identity['git_blob']

zip_count = 0
member_count = 0
for path in sorted((ROOT / REL).glob('evidence/**/*.zip')):
    extracted = path.parent / ('files' if path.name == 'original.zip' else path.stem)
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            assert archive.read(name) == (extracted / name).read_bytes()
            member_count += 1
    zip_count += 1

latest = ROOT / REL / 'evidence/39003068802'
manifest = json.loads((latest / 'evidence_manifest.json').read_bytes())
for entry in manifest['files']:
    data = (latest / entry['path']).read_bytes()
    assert len(data) == entry['bytes'] and digest(data) == entry['sha256'] and blob(data) == entry['git_blob']
for entry, name in zip(manifest['artifacts'], ('review.zip', 'publication.zip')):
    data = (latest / name).read_bytes()
    assert len(data) == entry['size_in_bytes'] and 'sha256:' + digest(data) == entry['digest']
audit = json.loads((latest / 'publication/remote_readback.json').read_bytes())
assert audit['status'] == 'PASS'
assert audit['review_manifest'] == json.loads((latest / 'review/manifest.json').read_bytes())
assert len(audit['checked']) == 24
for entry in audit['checked']:
    data = contents(entry['ref'], entry['path'])
    assert blob(data) == entry['git_blob'] and digest(data) == entry['sha256']
for name in ('review', 'publication'):
    path = ROOT / ('.github/scripts/uqcf_native_structure_' + name + '.py')
    ast.parse(path.read_text(), filename=str(path))
workflow = yaml.load((ROOT / '.github/workflows/uqcf-gem-native-structure.yml').read_text(), Loader=yaml.BaseLoader)
assert set(workflow['jobs']) == {'argument-review', 'publication-audit'}
assert workflow['jobs']['publication-audit']['needs'] == 'argument-review'

report = {
    'status': 'PASS', 'old_head': OLD, 'pinned_live_base': BASE, 'merge_base': ANCESTOR,
    'tree_sha': merged_tree_sha, 'base_tree_sha': git('rev-parse', BASE + '^{tree}').decode().strip(),
    'tree_paths': len(merged), 'base_paths_preserved': len(base), 'pr_paths': len(changed),
    'reviewed_pr_blobs_unchanged': len(changed) - 1,
    'sole_resolved_path': LEDGER,
    'resolution': 'Exact common prefix + verbatim PR append + verbatim base append',
    'head_added_lines': len(h[len(a):].splitlines()), 'base_added_lines': len(b[len(a):].splitlines()),
    'source_packet_identities': len(packet['files']),
    'review_manifests_checked': len(manifests), 'historical_accepted_runs': accepted, 'preserved_failed_schema_run': failed,
    'zip_crc_checks': zip_count, 'exact_zip_member_checks': member_count,
    'latest_artifact_manifest_files': len(manifest['files']), 'latest_publication_identities': len(audit['checked']),
    'python_parse_checks': 2, 'workflow_parse_check': True,
    'scientific_execution': False, 'new_scientific_review': False,
    'scope': 'Merge preservation and historical evidence integrity only; no renewed certification or full inherited replay',
}
Path('/workspace/scratch/25b1738236c6/pr106_validation_report.json').write_text(json.dumps(report, indent=2) + '\n')
payload = {
    'base_tree_sha': report['base_tree_sha'],
    'expected_tree_sha': merged_tree_sha,
    'new_blob_path': LEDGER,
    'new_blob_sha': merged[LEDGER][2],
    'new_blob_content': r.decode(),
    'tree_elements': [{'path': p, 'mode': merged[p][0], 'type': merged[p][1], 'sha': merged[p][2]} for p in sorted(changed)],
}
Path('/workspace/scratch/25b1738236c6/pr106_publication_payload.json').write_text(json.dumps(payload) + '\n')
print(json.dumps(report, indent=2))
