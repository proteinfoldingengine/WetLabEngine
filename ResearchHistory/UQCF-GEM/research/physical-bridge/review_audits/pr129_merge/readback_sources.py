"""Post-execution independent source/ZIP readback, not preregistered science.

Usage: python readback_sources.py /path/to/repository verification.zip publication.zip
Checks all archive members, deterministic replay bytes and exact source-scope Git blobs.
"""
from pathlib import Path
import hashlib, io, json, subprocess, sys, zipfile

root = Path(sys.argv[1]).resolve()
science = '084617b4c392b8955f0a19d2c2b2c02dfa8d9d91'
expected = ['dd2263ab238d5a77e8898d7d23a22ae3f4c229837002b390a1e0fe203a5955bb',
            'c537b8c21663148125af03989d4605abdcf371cb8b65d009480c97faf5394821']
archives = []
for arg, digest in zip(sys.argv[2:4], expected):
    raw = Path(arg).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest
    z = zipfile.ZipFile(io.BytesIO(raw)); archives.append(z)
    manifest = json.loads(z.read('artifact_manifest.json'))
    assert set(z.namelist()) == set(manifest) | {'artifact_manifest.json'}
    for name, record in manifest.items():
        data = z.read(name)
        assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256']
assert len(archives) == 2
first, second = archives
receipt = json.loads(second.read('receipt.json'))
assert receipt['status'] == 'PASS' and receipt['fresh_publication_replay'] is True
assert receipt['science_sha'] == science
for name in receipt['deterministic_files'] + ['scientific-source.zip']:
    assert first.read(name) == second.read(name), name
rows = subprocess.check_output(['git', 'ls-tree', '-r', '-z', science], cwd=root).split(b'\0')
blobs = {}
for row in rows:
    if row:
        meta, path = row.split(b'\t', 1)
        mode, kind, digest = meta.split(); blobs[path.decode()] = digest.decode()
docs = json.loads(first.read('review-document-readback.json'))
required = {v['resolved_path'] for group in docs.values() for v in group.values()}
prefixes = ['.github/scripts/', 'ResearchHistory/UQCF-GEM/foundational-closure-verification/',
            'ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_delivery_boundary/',
            'ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/',
            'ResearchHistory/UQCF-GEM/demos/v16.15F-graded-obstruction-descent/']
required |= {p for p in blobs if any(p.startswith(pre) for pre in prefixes)}
required.add('ResearchHistory/UQCF-GEM/AGENTS.md')
with zipfile.ZipFile(io.BytesIO(first.read('scientific-source.zip'))) as source:
    actual = {n for n in source.namelist() if not n.endswith('/')}
    assert actual == required
    for name in sorted(actual):
        raw = source.read(name)
        digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert digest == blobs[name], name
print(json.dumps(dict(status='PASS', science_sha=science, source_files=len(actual),
                      deterministic_files=len(receipt['deterministic_files']),
                      exact_source_scope_and_git_blob_identity=True, artifact_sha256=expected,
                      native_bridge_status='NOT_DERIVED'), indent=2, sort_keys=True))
