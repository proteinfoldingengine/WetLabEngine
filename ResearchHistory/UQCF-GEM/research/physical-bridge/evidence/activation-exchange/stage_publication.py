"""Stage a source reconciliation; no scientific execution or remote mutation."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
B = 'ResearchHistory/UQCF-GEM/research/physical-bridge/'
E = B + 'evidence/activation-exchange/'

def hashes(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest())

sources = json.loads((P/'source_readbacks.json').read_text())
assert sources['commit'] == '1282d628b2639e8a695b2893954f8e00d476644b'
for row in sources['sources']:
    actual = hashes((P/'sources'/row['name']).read_bytes())
    assert actual == dict(bytes=row['bytes'], sha256=row['sha256'], git_blob=row['sha']), row['name']

assert '**ACCEPTED**' in (P/'REVIEW.md').read_text()
names = ['COUPLED_C3_C4_DEFICIT_CONTINUATION.md', 'POST_A12_THEOREM_FIRST_SYNTHESIS.md']
for name in names:
    assert (P/name).read_bytes().startswith((P/'sources'/name).read_bytes()), name

mapping = {
    'RESULT.md': B+'COUPLED_C3_ACTIVATION_EXCHANGE_RECONCILIATION.md',
    'REVIEW.md': B+'COUPLED_C3_ACTIVATION_EXCHANGE_REVIEW.md',
    **{name: B+name for name in names},
    **{name: E+name for name in ['PLAN.md', 'PLAN_CURRENT.md', 'PUBLICATION.md',
                                'source_readbacks.json', 'stage_publication.py']},
}
for name in ['immutable_readback.json', 'binding.json']:
    if (P/name).exists():
        mapping[name] = E+name
entries = []
manifest = {'classification': 'inherited analytical source reconciliation; no new scientific campaign',
            'source_commit': sources['commit'], 'files': {}}
for local, remote in mapping.items():
    data = (P/local).read_bytes()
    entries.append(dict(path=remote, mode='100644', type='blob', content=data.decode()))
    manifest['files'][remote] = hashes(data)
data = json.dumps(manifest, indent=2, sort_keys=True)+'\n'
(P/'publication_hash_manifest.json').write_text(data)
entries.append(dict(path=E+'publication_hash_manifest.json', mode='100644', type='blob', content=data))
(P/'publication_entries.json').write_text(json.dumps(entries)+'\n')
print(json.dumps({'texts': len(entries), 'immutable_sources_checked': len(sources['sources']),
                  'historical_indices_append_only': True, 'new_scientific_tests': 0}))
